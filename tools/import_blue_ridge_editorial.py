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
# Bring opening illustrations forward, then split long prose without changing text.
for filename,prefix in [('va-019.webp','肯塔基周边'),('va-031.webp','弗吉尼亚（Virginia）')]:
 image_index=next(i for i,b in enumerate(blocks) if b.get('src','').endswith(filename))
 photo=blocks.pop(image_index)
 paragraph_index=next(i for i,b in enumerate(blocks) if b['kind']=='paragraph' and html.fromstring(b['html']).text_content().startswith(prefix))
 blocks.insert(paragraph_index+1,photo)

def split_paragraph(markup):
 import re
 root=html.fromstring(markup);runs=[]
 def walk(el,ancestors):
  if el.text:runs.append((el.text,ancestors))
  for child in el:
   walk(child,ancestors+[child.tag])
   if child.tail:runs.append((child.tail,ancestors))
 walk(root,[])
 text=''.join(t for t,_ in runs)
 if len(text)<=135:return [markup]
 ends=[];start=0
 for match in re.finditer('[。！？；][”」]?|$',text):
  end=match.end()
  if end-start>=65 or end==len(text):
   if end>start:ends.append((start,end));start=end
 result=[]
 for start,end in ends:
  out=html.Element('p');pos=0
  for text,tags in runs:
   part=text[max(0,start-pos):max(0,min(len(text),end-pos))] if end>pos and start<pos+len(text) else ''
   pos+=len(text)
   if not part:continue
   if tags:
    parent=out
    for tag in tags:child=html.Element(tag);parent.append(child);parent=child
    parent.text=part
   elif len(out):out[-1].tail=(out[-1].tail or '')+part
   else:out.text=(out.text or '')+part
  result.append(html.tostring(out,encoding='unicode'))
 return result
reflowed=[];i=0
while i<len(blocks):
 block=blocks[i]
 if block['kind']!='paragraph':reflowed.append(block);i+=1;continue
 parts=split_paragraph(block['html'])
 following=blocks[i+1] if i+1<len(blocks) else None
 for j,part in enumerate(parts):
  reflowed.append(dict(kind='paragraph',html=part))
  if j==0 and len(parts)>1 and following and following['kind'] in ('figure','photo-strip'):
   reflowed.append(following)
 if len(parts)>1 and following and following['kind'] in ('figure','photo-strip'):i+=1
 i+=1
blocks=reflowed
data=dict(title='Run50 #第24州｜弗吉尼亚：蓝岭马拉松｜一路爬坡，跑过罗阿诺克之星',blocks=blocks)
(ROOT/'tools/data/blue-ridge-wechat-editorial.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
