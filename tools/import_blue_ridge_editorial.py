"""Import all Blue Ridge magazine content, preserving photo and paragraph order."""
from pathlib import Path
from lxml import html
from urllib.parse import urlparse
import json
ROOT=Path(__file__).resolve().parents[1]
doc=html.fromstring((ROOT/'run50/wechat/blue-ridge-marathon-magazine-wechat.html').read_text(encoding='utf-8'))
source=doc.xpath('//*[@data-cn-content]')[0]
blocks=[]
for e in list(source)[4:-1]:
 if e.tag=='h2': blocks.append(dict(kind='heading',title=e.text_content()[2:].strip(),label=''))
 elif e.get('data-photo'):
  im=e.xpath('.//img')[0]
  blocks.append(dict(kind='figure',src=urlparse(im.get('src')).path,alt=im.get('alt'),caption=' · '.join(p.text_content() for p in e.xpath('./p'))))
 elif e.tag=='p':
  for n in e.iter(): n.attrib.clear()
  blocks.append(dict(kind='paragraph',html=html.tostring(e,encoding='unicode',with_tail=False)))
headings=[b for b in blocks if b['kind']=='heading']
for i,b in enumerate(headings): b['label']='前言' if i==0 else ('后记' if i==len(headings)-1 else f'Chapter {i}')
# Only confirmed comparable landscapes are joined; individual photo records remain intact.
groups=[(['001','002-1'],'向蓝岭山出发'),(['005-1','005','006'],'雨雾中的来时路'),(['007-2','007'],'驶近山城'),(['010-1','010'],'清晨的罗阿诺克街道'),(['013','014'],'起点前的人群'),(['017','018'],'山脚的赛道与春日树林'),(['020','021'],'林间赛道，来到三英里'),(['026','027'],'沿着树林继续向上'),(['028','029','030'],'山顶的路与远处的蓝岭'),(['042','043'],'林间相遇'),(['050','051'],'山脚小镇的街道'),(['053','054'],'过桥，经过铁路'),(['058','059'],'街坊与孩子们的加油声'),(['063-1','063','064'],'一步步靠近终点'),(['071','072'],'夕阳与暮色中的归途')]
for names,caption in groups:
 names=['va-'+n+'.webp' for n in names]
 ix=[i for i,b in enumerate(blocks) if b.get('src','').split('/')[-1] in names]
 assert len(ix)==len(names) and ix==list(range(ix[0],ix[0]+len(names)))
 blocks[ix[0]:ix[-1]+1]=[dict(kind='photo-strip',images=[blocks[i] for i in ix],caption=caption+'｜摄影 / Arsenan')]
data=dict(title='Run50 #第24州｜弗吉尼亚：蓝岭马拉松｜一路爬坡，跑过罗阿诺克之星',blocks=blocks)
(ROOT/'tools/data/blue-ridge-wechat-editorial.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
