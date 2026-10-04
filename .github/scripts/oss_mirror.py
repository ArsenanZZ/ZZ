#!/usr/bin/env python3
"""Mirror only a successful Pages artifact; never delete OSS objects."""
import argparse
import base64
import hashlib
import json
import mimetypes
import os
from pathlib import Path, PurePosixPath
import shutil
import tarfile
import time
from urllib.request import Request, urlopen
from concurrent.futures import ThreadPoolExecutor

REPOSITORY = 'ArsenanZZ/ZZ'
BUCKET = 'zhennanzhang-web-hk'
ENDPOINT = 'https://oss-cn-hongkong.aliyuncs.com'
# One-shot analytics.js snapshot. Authenticated OSS console verified no tags on 2026-10-04 20:52 UTC.
WRITE_SMOKE_MD5 = '3f7c57137ba6041d93fbb6aef42f54b8'
WRITE_SMOKE_NO_TAGS_VERIFIED = True
FORBIDDEN_ROOTS = {'.git', '.github', '.claude', 'scratch', 'tools', 'work', '_site'}


def api(path):
    request = Request('https://api.github.com/repos/' + REPOSITORY + path, headers={
        'Authorization': 'Bearer ' + os.environ['GH_TOKEN'],
        'Accept': 'application/vnd.github+json', 'X-GitHub-Api-Version': '2022-11-28'})
    with urlopen(request, timeout=60) as response:
        return json.load(response)


def trusted(run):
    return (run.get('conclusion') == 'success' and run.get('head_branch') == 'main'
            and run.get('head_repository', {}).get('full_name') == REPOSITORY
            and run.get('event') in {'push', 'workflow_dispatch'}
            and run.get('path') == '.github/workflows/pages.yml')


def latest_run():
    # Do not use status/branch query filters: GitHub caps filtered searches at 1,000.
    valid = []
    page = 1
    while True:
        runs = api(f'/actions/workflows/pages.yml/runs?per_page=100&page={page}')['workflow_runs']
        valid.extend(run for run in runs if trusted(run))
        if len(runs) < 100:
            break
        page += 1
    if not valid:
        raise RuntimeError('No successful trusted Pages run is available')
    # A rerun of an old commit can be the most recent successful deployment.
    return max(valid, key=lambda run: (run['updated_at'], run['run_number'], run['run_attempt']))



def select_run():
    event = json.loads(Path(os.environ['GITHUB_EVENT_PATH']).read_text())
    latest = latest_run()
    if os.environ['GITHUB_EVENT_NAME'] == 'workflow_run' and not trusted(event['workflow_run']):
        raise RuntimeError('Refusing an untrusted Pages event')
    # Always reconcile the newest success, even for a late older event. GitHub
    # concurrency can replace a pending run, so skipping stale events can lose
    # the only queued reconciliation of the latest deployment.
    run = latest
    with open(os.environ['GITHUB_OUTPUT'], 'a') as output:
        output.write(f"selected=true\nrun_id={run['id']}\nrun_attempt={run['run_attempt']}\nsha={run['head_sha']}\n")
    print(f"Selected latest Pages run {run['id']}, commit {run['head_sha']}")



def extract_archive(archive, destination):
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=False)
    with tarfile.open(archive, 'r:') as tar:
        members = tar.getmembers()
        seen = set()
        for member in members:
            path = PurePosixPath(member.name)
            if path.is_absolute() or '..' in path.parts or '\\' in member.name:
                raise ValueError('Unsafe archive path')
            if not (member.isfile() or member.isdir()):
                raise ValueError('Archive links and special files are forbidden')
            if path.parts and path.parts[0] in FORBIDDEN_ROOTS:
                raise ValueError('Non-published source directory in archive')
            if member.isfile():
                if str(path) in seen or member.size > 5 * 1024**3:
                    raise ValueError('Duplicate path or file exceeding simple upload limit')
                seen.add(str(path))
        if 'index.html' not in seen:
            raise ValueError('Artifact has no index.html')
        for member in members:
            target = destination / member.name
            if member.isdir():
                target.mkdir(parents=True, exist_ok=True)
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                with tar.extractfile(member) as source, target.open('xb') as output:
                    shutil.copyfileobj(source, output)


def inventory(root):
    result = {}
    for path in sorted(Path(root).rglob('*')):
        if path.is_symlink():
            raise ValueError('Site contains a symbolic link')
        if path.is_file():
            key = path.relative_to(root).as_posix()
            with path.open('rb') as source:
                digest = hashlib.file_digest(source, 'md5').hexdigest()
            result[key] = (path, path.stat().st_size, digest)
    if not result or 'index.html' not in result:
        raise ValueError('Refusing empty/incomplete site')
    return result


def changed_files(local, remote):
    return [key for key, (_, size, digest) in local.items()
            if remote.get(key) != (size, digest)]


def phase(key):
    return 2 if key == 'index.html' else (1 if key.lower().endswith(('.html', '.htm')) else 0)


def retry(operation):
    for attempt in range(4):
        try:
            return operation()
        except Exception as error:
            status = getattr(error, 'status', None)
            if attempt == 3 or (status and status < 500 and status not in {408, 429}):
                raise
            time.sleep(2 ** attempt)


def verify_existing_write(bucket, local):
    """Optional one-object, byte-identical write test; never creates a new key."""
    key = 'analytics.js'
    path, size, digest = local[key]
    if digest != WRITE_SMOKE_MD5:
        raise ValueError('Write verification asset differs from reviewed snapshot')
    if size > 65536:
        raise ValueError('Write-verification asset exceeds 64 KiB')
    before = retry(lambda: bucket.head_object(key))
    headers = {name.lower(): value for name, value in before.headers.items()}
    if headers.get('x-oss-force-download', '').lower() == 'true':
        raise ValueError('Cannot establish original metadata: response headers were rewritten')
    if (int(headers['content-length']), headers['etag'].strip('"').lower()) != (size, digest):
        raise ValueError('Write verification requires existing byte-identical analytics.js')
    if headers.get('x-oss-object-type', 'Normal') != 'Normal':
        raise ValueError('Write verification only supports a normal object')
    tag_count = headers.get('x-oss-tagging-count')
    if tag_count is None and not WRITE_SMOKE_NO_TAGS_VERIFIED:
        raise ValueError('No independently verified object tag state')
    if headers.get('x-oss-server-side-encryption') or int(tag_count or '0'):
        raise ValueError('Refusing to alter encryption or tagged-object metadata')
    keep = {'content-type', 'cache-control', 'content-disposition', 'content-encoding',
            'content-language', 'expires', 'x-oss-storage-class'}
    preserved = {name: value for name, value in headers.items()
                 if name in keep or name.startswith('x-oss-meta-')}
    upload_headers = dict(preserved)
    upload_headers['Content-MD5'] = base64.b64encode(bytes.fromhex(digest)).decode()
    result = retry(lambda: bucket.put_object_from_file(key, str(path), headers=upload_headers))
    if result.etag.strip('"').lower() != digest:
        raise RuntimeError('Write-verification upload checksum mismatch')
    after = retry(lambda: bucket.head_object(key))
    after_headers = {name.lower(): value for name, value in after.headers.items()}
    if (int(after_headers['content-length']), after_headers['etag'].strip('"').lower()) != (size, digest):
        raise RuntimeError('Write-verification readback checksum mismatch')
    if any(after_headers.get(name) != value for name, value in preserved.items()):
        raise RuntimeError('Write-verification metadata readback mismatch')
    print(f'Live PutObject verified: {key}, {size} identical bytes; MD5 {digest}; original metadata preserved')


def mirror(root, run_id, run_attempt, verify_write=False):
    import oss2
    # Never accept arbitrary endpoints/buckets through workflow inputs.
    auth = oss2.StsAuth(os.environ['ALIBABA_CLOUD_ACCESS_KEY_ID'],
                        os.environ['ALIBABA_CLOUD_ACCESS_KEY_SECRET'],
                        os.environ['ALIBABA_CLOUD_SECURITY_TOKEN'], auth_version='v4')
    bucket = oss2.Bucket(auth, ENDPOINT, BUCKET, connect_timeout=60, region='cn-hongkong')
    local = inventory(root)

    def remote_inventory():
        return {obj.key: (obj.size, obj.etag.strip('"').lower())
                for obj in oss2.ObjectIterator(bucket, max_keys=1000)}

    remote = retry(remote_inventory)
    changed = changed_files(local, remote)
    retained = len(remote.keys() - local.keys())
    print(f'{len(local)} artifact files; {len(changed)} uploads; {retained} destination-only files retained')
    # Recheck after artifact download/hash work, immediately before mutation.
    latest = latest_run()
    if (str(latest['id']), str(latest['run_attempt'])) != (str(run_id), str(run_attempt)):
        print('A newer Pages deployment succeeded; skip superseded mirror')
        return
    if verify_write:
        verify_existing_write(bucket, local)

    def upload(key):
        path, _, digest = local[key]
        content_type = mimetypes.guess_type(key)[0] or 'application/octet-stream'
        if content_type.startswith('text/') or content_type in {'application/javascript', 'application/json'}:
            content_type += '; charset=utf-8'
        headers = {'Content-MD5': base64.b64encode(bytes.fromhex(digest)).decode(),
                   'Content-Type': content_type,
                   'Cache-Control': 'public, max-age=300' if phase(key) else 'public, max-age=3600'}
        result = retry(lambda: bucket.put_object_from_file(key, str(path), headers=headers))
        if result.etag.strip('"').lower() != digest:
            raise RuntimeError(f'Upload checksum mismatch: {key}')

    # Assets finish before HTML; root entry point is last. Failures stop later phases.
    for group in range(3):
        with ThreadPoolExecutor(max_workers=6) as pool:
            list(pool.map(upload, [key for key in changed if phase(key) == group]))
    remaining = changed_files(local, retry(remote_inventory))
    if remaining:
        raise RuntimeError(f'Post-upload verification failed for {len(remaining)} files')
    summary = (f'OSS Hong Kong mirror verified: {len(local)} files match Pages run {run_id}; '
               f'{len(changed)} uploaded, {len(local)-len(changed)} unchanged, '
               f'{retained} old files retained. No objects deleted.\n')
    print(summary)
    if os.environ.get('GITHUB_STEP_SUMMARY'):
        with open(os.environ['GITHUB_STEP_SUMMARY'], 'a') as output:
            output.write(summary)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['select-run', 'extract', 'sync'])
    parser.add_argument('--archive')
    parser.add_argument('--site')
    parser.add_argument('--run-id')
    parser.add_argument('--run-attempt')
    parser.add_argument('--verify-write', action='store_true')
    args = parser.parse_args()
    if args.command == 'select-run':
        select_run()
    elif args.command == 'extract':
        extract_archive(args.archive, args.site)
    else:
        mirror(args.site, args.run_id, args.run_attempt, args.verify_write)
