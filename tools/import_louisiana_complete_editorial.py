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
for group,caption in [(['img-004.webp','img-005.webp'],'飞机显示屏上的航线｜摄影 / Arsenan'),(['img-037.webp','img-038.webp'],'湖畔的晨光与跑者｜摄影 / Arsenan'),(['img-052.webp','img-053.webp'],'沿湖继续跑｜摄影 / Arsenan'),(['img-024.webp','img-025.webp'],'起点人群与出发拱门｜摄影 / Arsenan'),(['img-047.webp','img-048.webp'],'沿途伸来的手与加油牌｜摄影 / Arsenan'),(['la-062-1.webp','la-062.webp'],'州议会大厦前，终点就在眼前｜摄影 / Arsenan'),(['la-070.webp','la-071.webp'],'返程途中，在海湾边走走｜摄影 / Arsenan')]:
 ix=[i for i,b in enumerate(blocks) if b['kind']=='figure' and b['src'].split('/')[-1] in group];assert ix==list(range(ix[0],ix[0]+2))
 blocks[ix[0]:ix[-1]+1]=[dict(kind='photo-strip',images=[blocks[i] for i in ix],caption=caption)]
headings=[b for b in blocks if b['kind']=='heading']
for i,heading in enumerate(headings):
 heading['label']='前言' if i==0 else ('后记' if i==len(headings)-1 else f'Chapter {i}')
siqi_photos={'img-013.webp','la-065-2.webp','la-065-3.webp','la-065-4.webp'}
for block in blocks:
 for im in (block.get('images',[]) if block['kind']=='photo-strip' else [block]):
  if im.get('src','').endswith('img-004.webp'):im['alt']='飞机显示屏上的飞行位置'
  if im.get('src','').split('/')[-1] in siqi_photos:
   im['caption']=im['caption'].split(' · 摄影')[0]+' · 摄影 / Siqi'
p=ROOT/'tools/data/louisiana-wechat-editorial.json';data=json.loads(p.read_text(encoding='utf-8'));data['blocks']=blocks;p.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
for p in (ROOT/'assets/louisiana-magazine-photos').glob('*.webp'):
 if (ROOT/'assets/louisiana-wechat-copy'/(p.stem+'.jpg')).exists():continue
 subprocess.run(['ffmpeg','-y','-loglevel','error','-i',str(p),'-vf','scale=min(1080\\,iw):-1','-q:v','3',str(ROOT/'assets/louisiana-wechat-copy'/(p.stem+'.jpg'))],check=True)
