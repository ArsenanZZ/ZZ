from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urlparse,unquote
import json,sys,re
sys.path.insert(0,str(Path(__file__).resolve().parent))
import build_remaining_series_editorials as build
r=build.ROOT;errors=[];photos=0
norm=lambda s:re.sub(r'\s+','',s)
for p in build.DATA.glob('*.json'):
 d=build.prepare(json.loads(p.read_text(encoding='utf8')));s=BeautifulSoup((r/f'run50/wechat/{d["slug"]}-editorial.html').read_text(encoding='utf8'),'html.parser')
 expected=[b['src'] for b in d['blocks'] if b['kind']=='figure'];actual=[i['src'] for i in s.select('.photo-strip:not(.location-poster) img')];photos+=len(expected)
 if expected!=actual:errors.append((d['slug'],'photo order'))
 expected_text=''.join(b['title'] if b['kind']=='heading' else BeautifulSoup(b['html'],'html.parser').get_text() for b in d['blocks'] if b['kind']!='figure')
 actual_text=''.join(e.h2.get_text() if 'chapter' in e.get('class',[]) else e.get_text() for e in s.main.find_all(recursive=False) if 'chapter' in e.get('class',[]) or 'prose' in e.get('class',[]))
 if d['blocks'][0]['kind']!='heading':expected_text='出发之前'+expected_text
 if norm(actual_text)!=norm(expected_text):errors.append((d['slug'],'text'))
 for im in s.select('img,source'):
  for attr in ['src','srcset','data-light-src','data-dark-src']:
   if not im.get(attr):continue
   u=urlparse(im[attr]);path=unquote(u.path);f=r/path.lstrip('/') if path.startswith('/') else (r/'run50/wechat'/path).resolve()
   if not u.netloc or u.netloc=='zhennanzhang.com':
    if not f.exists():errors.append((d['slug'],'asset',path))
 if '不用注册账号即可' in s.get_text() or '留言 / 访问次数' in s.get_text():errors.append((d['slug'],'old comments'))
print('23 articles;',photos,'photos; errors:',errors)
assert not errors,errors
