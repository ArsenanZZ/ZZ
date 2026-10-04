import base64
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import tarfile
import tempfile
import types
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('mirror', Path(__file__).with_name('oss_mirror.py'))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class MirrorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
    def tearDown(self):
        self.temp.cleanup()
    def archive(self, name='index.html', kind=None):
        path = self.root / 'artifact.tar'
        with tarfile.open(path, 'w') as tar:
            member = tarfile.TarInfo(name)
            if kind:
                member.type = kind
                member.linkname = '/tmp/escape'
                tar.addfile(member)
            else:
                member.size = 2
                tar.addfile(member, io.BytesIO(b'ok'))
        return path
    def test_safe_extraction(self):
        m.extract_archive(self.archive('./index.html'), self.root / 'site')
        self.assertEqual((self.root/'site/index.html').read_text(), 'ok')
    def test_reject_unsafe_archive(self):
        for index, (name, kind) in enumerate([('../index.html', None), ('/index.html', None), ('index.html', tarfile.SYMTYPE), ('index.html', tarfile.LNKTYPE), ('.github/workflows/x', None), ('assets/file', tarfile.FIFOTYPE), ('a\\b', None)]):
            with self.subTest(name=name, kind=kind), self.assertRaises(ValueError):
                m.extract_archive(self.archive(name, kind), self.root / f'bad{index}')
    def test_reject_missing_home(self):
        with self.assertRaises(ValueError):
            m.extract_archive(self.archive('a.txt'), self.root/'site')
    def test_checksum_detects_same_size_change_and_multipart(self):
        local = {'same': (None, 2, 'aaa'), 'changed': (None, 2, 'bbb'), 'new': (None, 3, 'ccc'), 'multipart': (None, 4, 'ddd')}
        remote = {'same': (2, 'aaa'), 'changed': (2, 'xxx'), 'old': (5, 'eee'), 'multipart': (4, 'ddd-2')}
        self.assertEqual(m.changed_files(local, remote), ['changed', 'new', 'multipart'])
    def test_trust_checks(self):
        good = {'conclusion': 'success', 'head_branch': 'main', 'head_repository': {'full_name': m.REPOSITORY}, 'event': 'push', 'path': '.github/workflows/pages.yml'}
        self.assertTrue(m.trusted(good))
        for key, value in [('conclusion', 'failure'), ('head_branch', 'dev'), ('head_repository', {'full_name': 'attacker/fork'}), ('event', 'pull_request'), ('path', 'other.yml')]:
            self.assertFalse(m.trusted(dict(good, **{key: value})))
    def test_late_event_selects_latest_not_old(self):
        good = {'conclusion': 'success', 'head_branch': 'main', 'head_repository': {'full_name': m.REPOSITORY}, 'event': 'push', 'path': '.github/workflows/pages.yml', 'id': 1, 'run_attempt': 1, 'head_sha': 'old'}
        event = self.root/'event.json'; event.write_text(json.dumps({'workflow_run': good}))
        out = self.root/'out'
        with patch.dict(os.environ, GITHUB_EVENT_PATH=str(event), GITHUB_EVENT_NAME='workflow_run', GITHUB_OUTPUT=str(out)), patch.object(m, 'latest_run', return_value=dict(good, id=2, head_sha='new')):
            m.select_run()
        self.assertIn('run_id=2', out.read_text())
    def test_old_rerun_is_latest_and_all_pages_scanned(self):
        good = {'conclusion': 'success', 'head_branch': 'main', 'head_repository': {'full_name': m.REPOSITORY}, 'event': 'push', 'path': '.github/workflows/pages.yml', 'run_attempt': 1}
        newer = dict(good, id=100, run_number=100, updated_at='2026-10-04T20:00:00Z')
        old_rerun = dict(good, id=1, run_number=1, run_attempt=2, updated_at='2026-10-04T21:00:00Z')
        with patch.object(m, 'api', side_effect=[{'workflow_runs': [newer]*100}, {'workflow_runs': [old_rerun]}]) as api:
            self.assertEqual(m.latest_run()['id'], 1)
            self.assertIn('page=2', api.call_args.args[0])
    def test_inventory_unicode_and_symlinks(self):
        (self.root/'index.html').write_bytes(b'home')
        (self.root/'中文.txt').write_bytes(b'abc')
        data=m.inventory(self.root)
        self.assertEqual(data['中文.txt'][2], hashlib.md5(b'abc').hexdigest())
        (self.root/'link').symlink_to(self.root/'index.html')
        with self.assertRaises(ValueError): m.inventory(self.root)
    def test_mirror_end_to_end_incremental_without_deletes(self):
        files={'index.html': b'home', 'a.html': b'page', 'image.png': b'asset', 'unchanged.txt': b'same'}
        for key, content in files.items(): (self.root/key).write_bytes(content)
        remote={'unchanged.txt': b'same', 'removed.txt': b'retain'}
        uploads=[]
        class Bucket:
            def __init__(self,*args,**kwargs): pass
            def put_object_from_file(self,key,path,headers):
                content=Path(path).read_bytes(); digest=hashlib.md5(content).digest()
                self_test.assertEqual(headers['Content-MD5'], base64.b64encode(digest).decode())
                remote[key]=content; uploads.append(key)
                return types.SimpleNamespace(etag=digest.hex().upper())
        self_test=self
        sdk=types.SimpleNamespace(StsAuth=lambda *a,**k: None, Bucket=Bucket,
            ObjectIterator=lambda *a,**k: [types.SimpleNamespace(key=key,size=len(content),etag=hashlib.md5(content).hexdigest().upper()) for key,content in remote.items()])
        with patch.dict('sys.modules', oss2=sdk), patch.dict(os.environ, ALIBABA_CLOUD_ACCESS_KEY_ID='test', ALIBABA_CLOUD_ACCESS_KEY_SECRET='test', ALIBABA_CLOUD_SECURITY_TOKEN='test'), patch.object(m,'latest_run',return_value={'id': 7, 'run_attempt': 1}):
            m.mirror(self.root, '7', '1')
            self.assertEqual(uploads,['image.png','a.html','index.html'])
            self.assertEqual(remote['removed.txt'], b'retain')
            uploads.clear(); m.mirror(self.root, '7', '1'); self.assertEqual(uploads,[])
            (self.root/'index.html').write_bytes(b'new content')
            with patch.object(m, 'latest_run', return_value={'id': 7, 'run_attempt': 2}):
                m.mirror(self.root, '7', '1')
            self.assertEqual(uploads, [])
            self.assertEqual(remote['index.html'], b'home')
    def smoke_fixture(self, changes=None):
        path=self.root/'analytics.js'; path.write_bytes(b'public script')
        digest=hashlib.md5(path.read_bytes()).hexdigest()
        self.enterContext(patch.object(m, 'WRITE_SMOKE_MD5', digest))
        self.enterContext(patch.object(m, 'WRITE_SMOKE_NO_TAGS_VERIFIED', True))
        headers={'Content-Type':'application/javascript', 'Content-Length':str(path.stat().st_size), 'ETag':f'"{digest}"', 'Cache-Control':'max-age=60', 'x-oss-meta-example':'kept', 'x-oss-storage-class':'Standard'}
        headers.update(changes or {})
        bucket=types.SimpleNamespace()
        bucket.head_object=unittest.mock.Mock(return_value=types.SimpleNamespace(headers=headers))
        bucket.put_object_from_file=unittest.mock.Mock(return_value=types.SimpleNamespace(etag=digest))
        return bucket, {'analytics.js':(path,path.stat().st_size,digest)}
    def test_live_write_smoke_preserves_metadata_one_existing_put(self):
        bucket,local=self.smoke_fixture()
        m.verify_existing_write(bucket,local)
        bucket.put_object_from_file.assert_called_once()
        call=bucket.put_object_from_file.call_args
        self.assertEqual(call.args[0],'analytics.js')
        self.assertEqual(call.kwargs['headers']['content-type'],'application/javascript')
        self.assertEqual(call.kwargs['headers']['cache-control'],'max-age=60')
        self.assertEqual(call.kwargs['headers']['x-oss-meta-example'],'kept')
        self.assertNotIn('content-disposition',call.kwargs['headers'])
    def test_live_write_smoke_mismatch_and_injected_metadata_abort(self):
        for changes in [{'ETag':'"wrong"'}, {'Content-Length':'999'}, {'x-oss-force-download':'true'}, {'x-oss-tagging-count':'1'}, {'x-oss-server-side-encryption':'AES256'}]:
            bucket,local=self.smoke_fixture(changes)
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                m.verify_existing_write(bucket,local)
            bucket.put_object_from_file.assert_not_called()
    def test_live_write_smoke_requires_known_snapshot_and_tag_state(self):
        bucket,local=self.smoke_fixture()
        with patch.object(m, 'WRITE_SMOKE_MD5', 'different'), self.assertRaises(ValueError):
            m.verify_existing_write(bucket,local)
        with patch.object(m, 'WRITE_SMOKE_NO_TAGS_VERIFIED', False), self.assertRaises(ValueError):
            m.verify_existing_write(bucket,local)
        bucket.put_object_from_file.assert_not_called()
    def test_live_write_smoke_head_denied_never_writes(self):
        bucket,local=self.smoke_fixture()
        error=RuntimeError('denied'); error.status=403
        bucket.head_object.side_effect=error
        with self.assertRaises(RuntimeError): m.verify_existing_write(bucket,local)
        bucket.put_object_from_file.assert_not_called()
    def test_live_write_smoke_metadata_readback_failure_is_fatal(self):
        bucket,local=self.smoke_fixture()
        before=bucket.head_object.return_value
        after=types.SimpleNamespace(headers=dict(before.headers, **{'Cache-Control':'changed'}))
        bucket.head_object.side_effect=[before,after]
        with self.assertRaises(RuntimeError): m.verify_existing_write(bucket,local)
        bucket.put_object_from_file.assert_called_once()
    def test_retry_stops_on_auth_errors(self):
        error=RuntimeError('denied'); error.status=403
        with patch.object(m.time,'sleep') as sleep, self.assertRaises(RuntimeError):
            m.retry(lambda: (_ for _ in ()).throw(error))
        sleep.assert_not_called()

if __name__ == '__main__': unittest.main()
