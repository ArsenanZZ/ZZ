from pathlib import Path
import json,re
from bs4 import BeautifulSoup
r=Path(__file__).resolve().parents[1];a=json.loads((r/'tools/data/run50-style-audit-20261020.json').read_text(encoding='utf8'))
errors=[];stats=[]
for p in (r/'tools/data/run50-refresh-20261020').glob('*.json'):
 d=json.loads(p.read_text(encoding='utf8'));s=BeautifulSoup((r/f'run50/wechat/{d["slug"]}-editorial.html').read_text(encoding='utf8'),'html.parser')
 old=[b['src'] for b in d['blocks'] if b['kind']=='figure'];new=[i['src'] for f in s.select('figure.photo-strip:not(.location-poster)') for i in f.select('img')]
 if old!=new:errors.append((d['slug'],'photo order'))
 text=lambda x:re.sub(r'\s+','',x)
 before=''.join(BeautifulSoup(b['html'],'html.parser').get_text() for b in d['blocks'] if b['kind']=='paragraph')
 after=''.join(n.get_text() for n in s.select('main > p.prose'))
 if text(before)!=text(after):errors.append((d['slug'],'prose'))
 stats.append((d['slug'],len(old),sum(not b.get('caption') for b in d['blocks'] if b['kind']=='figure')))
print('Preservation errors',errors);print('Photo counts / empty captions',stats)

assert not errors, errors
