"""Import the complete magazine photo sequence into the editorial edition."""
from pathlib import Path
from lxml import html
from urllib.parse import urlparse
import json,subprocess
ROOT=Path(__file__).resolve().parents[1]
doc=html.fromstring((ROOT/'run50/wechat/louisiana-marathon-magazine-wechat.html').read_text(encoding='utf-8'))
source=doc.xpath('//*[@data-cn-content]')[0]
blocks=[]
for e in list(source)[4:-1]:
 if e.tag=='h2':
  title=''.join(e.itertext());title=title[2:].strip();blocks.append(dict(kind='heading',title=title,label=''))
 elif e.get('data-photo'):
  im=e.xpath('.//img')[0];src=urlparse(im.get('src')).path
  blocks.append(dict(kind='figure',src=src,alt=im.get('alt'),caption=' · '.join(p.text_content() for p in e.xpath('./p'))))
 elif e.tag=='p':
  for n in e.iter():n.attrib.clear()
  blocks.append(dict(kind='paragraph',html=html.tostring(e,encoding='unicode',with_tail=False)))
for group,caption in [(['img-037.webp','img-038.webp'],'湖畔的晨光与跑者｜摄影 / Arsenan'),(['img-052.webp','img-053.webp'],'沿湖继续跑｜摄影 / Arsenan')]:
 ix=[i for i,b in enumerate(blocks) if b['kind']=='figure' and b['src'].split('/')[-1] in group];assert ix==list(range(ix[0],ix[0]+2))
 blocks[ix[0]:ix[-1]+1]=[dict(kind='photo-strip',images=[blocks[i] for i in ix],caption=caption)]
p=ROOT/'tools/data/louisiana-wechat-editorial.json';data=json.loads(p.read_text(encoding='utf-8'));data['blocks']=blocks;p.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
for p in (ROOT/'assets/louisiana-magazine-photos').glob('*.webp'):
 subprocess.run(['ffmpeg','-y','-loglevel','error','-i',str(p),'-vf','scale=min(1080\\,iw):-1','-q:v','3',str(ROOT/'assets/louisiana-wechat-copy'/(p.stem+'.jpg'))],check=True)
