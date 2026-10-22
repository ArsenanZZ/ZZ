"""Refresh the remaining Run50 pages from frozen source blocks; preserve photo/text order."""
from pathlib import Path
from html import escape
import json,re,sys
from functools import lru_cache
from bs4 import BeautifulSoup
from PIL import Image,ImageOps,ImageDraw,ImageFont
from normalize_wechat_presentation import normalize
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'tools/data/run50-refresh-20261020'
SELECT=json.loads((ROOT/'tools/data/run50-refresh-selection.json').read_text(encoding='utf-8'))
def local(src):
 return ROOT/src.lstrip('/') if src.startswith('/') else (ROOT/'run50/wechat'/src.split('?')[0]).resolve()
@lru_cache(maxsize=None)
def dimensions(src):
 try:
  with Image.open(local(src)) as im:return f' width="{im.width}" height="{im.height}"'
 except (OSError,ValueError):return ''

def tidy(html):
 s=BeautifulSoup(html,'html.parser')
 for x in s.find_all():
  x.attrs={k:v for k,v in x.attrs.items() if k in ['href','data-cn-tone','data-cn-emphasis']}
 p=s.find('p')
 if p:p['class']='prose'
 return str(s)
def credit(c):
 match=re.search(r'(?:@|\bby\s+)(Arsenan|Siqi|ACE|MarathonFoto|FinisherPix)(?=\s|$)',c,flags=re.I)
 if match:
  name={'arsenan':'Arsenan','siqi':'Siqi','ace':'ACE','marathonfoto':'MarathonFoto','finisherpix':'FinisherPix'}[match[1].lower()]
  c=(c[:match.start()]+c[match.end():]).strip(' ·')+' · 摄影 / '+name
 c=re.sub(r'\s*(?:@|\bby\s+)Google\b',r' · 资料图 / Google',c,flags=re.I)
 if '赛事官方' in c and '摄影 /' not in c:c=c.replace(' · 赛事官方','').strip(' ·')+' · 摄影 / 官方摄影'
 return c


def generate_hero(d):
 slug=d['slug'];out=ROOT/f'assets/run50-refresh-20261020/{slug}';out.mkdir(parents=True,exist_ok=True)
 photos=[b for b in d['blocks'] if b['kind']=='figure'];frames=[]
 for idx,center in zip(SELECT[slug]['hero_indices'],SELECT[slug]['crop_centers']):
  im=ImageOps.exif_transpose(Image.open(local(photos[idx]['src']))).convert('RGB')
  frames.append(ImageOps.fit(im,(900,900),centering=tuple(center)))
 frames[0].save(out/'hero-still.jpg',quality=90)
 frames[0].save(out/'hero.gif',save_all=True,append_images=frames[1:],duration=3000,loop=0,optimize=True)
 return out

def interleave(blocks):
 # Split existing long paragraphs across the adjacent photo run, without rewriting
 # text or changing the relative order of either the photos or the prose.
 out=[];i=0
 while i<len(blocks):
  b=blocks[i]
  if b['kind']=='paragraph':
   j=i+1
   while j<len(blocks) and blocks[j]['kind']=='figure':j+=1
   pics=blocks[i+1:j]
   s=BeautifulSoup(b['html'],'html.parser');p=s.find('p')
   if len(pics)>3 and p:
    chunks=re.findall(r'.*?[。！？](?:[”’])?|.+$',p.get_text(),re.S)
    if len(pics)>6 and len(chunks)<(len(pics)+2)//3:
     chunks=re.findall(r'.*?[。！？，；](?:[”’])?|.+$',p.get_text(),re.S)
    if len(chunks)>1:
     n=min(len(chunks),(len(pics)+2)//3)
     for k in range(n):
      start=round(k*len(chunks)/n);end=round((k+1)*len(chunks)/n)
      out.append({'kind':'paragraph','html':'<p>'+escape(''.join(chunks[start:end]))+'</p>'})
      out.extend(pics[round(k*len(pics)/n):round((k+1)*len(pics)/n)])
     i=j;continue
  out.append(b);i+=1
 return out

def render(d,hero=True):
 slug=d['slug'];asset='/assets/run50-refresh-20261020/'+slug
 if hero:generate_hero(d)
 template=BeautifulSoup((ROOT/'run50/wechat/san-francisco-marathon-editorial.html').read_text(encoding='utf-8'),'html.parser')
 css=template.style.get_text()+'''\n.prose{margin:0 0 22px;font-size:15px;line-height:1.95;letter-spacing:.5px;text-align:justify}.brand-intro img{width:96px;height:auto}.photo-strip img{width:100%;height:auto}.poster-window{overflow:hidden;border:1px solid #b7a77d}.poster-window img{width:104%;max-width:none;transform:none;margin:-2%}.location-poster{margin:32px 0}.photo-strip figcaption{font-size:12px;line-height:1.8;text-align:center}.prose a{color:inherit}'''
 title=d['title'];state=re.search(r'第\s*(\d+)州',title);n=int(state[1]) if state else 1
 intro=d['intro'];poster=d['poster'];map_src=d['map']
 if not map_src and slug.startswith('kentucky'):map_src='/assets/cn-article-maps/us-light-322942d44d981f33.png'
 if not poster:
  # Match the existing homepage cover for this exact story.
  home=BeautifulSoup((ROOT/'CN/index.html').read_text(encoding='utf-8'),'html.parser')
  a=next((a for a in home.find_all('a',href=True) if slug+'-' in a['href'] and a.img),None)
  if a:poster=a.img['src'];poster='/'+poster.lstrip('../') if not poster.startswith('/') else poster
 if not intro:intro=re.sub(r'^Run50\s*[^｜|]*[｜|]','',title)
 brand='/assets/run50-shirt-intros/'+slug+'/'
 body=[f'<header class="masthead"><h1>{escape(title)}</h1><p class="byline">文字 / Arsenan</p></header>',
 f'<picture class="brand-intro" data-logo-theme="shirt"><source media="(prefers-reduced-motion: reduce)" srcset="{brand}light-still.png" data-light-src="{brand}light-still.png" data-dark-src="{brand}dark-still.png"><img src="{brand}light.gif" data-light-src="{brand}light.gif" data-dark-src="{brand}dark.gif" alt="Run50 机器人片头"></picture>',
 f'<figure class="cover"><picture><source media="(prefers-reduced-motion: reduce)" srcset="{asset}/hero-still.jpg"><img src="{asset}/hero.gif" width="900" height="900" alt="比赛与旅行的五个瞬间"></picture><figcaption>跑步与旅行 · 照片来源及署名见正文</figcaption></figure>',
 '<div class="down" aria-hidden="true">⌄<br>⌄<br>⌄</div>',f'<section class="intro"><p>{escape(intro)}</p></section>']
 if map_src or poster:
  body.append('<figure class="photo-strip location-poster">'+(f'<img src="{escape(map_src)}" alt="Run50 本站地图">' if map_src else '')+(f'<div class="poster-window"><img src="{escape(poster)}" alt="本州赛事海报"></div>' if poster else '')+f'<figcaption>Run50 · 第{n}州<br>制图 / Arsenan</figcaption></figure>')
 blocks=interleave(d['blocks']);num=0;i=0
 if blocks and blocks[0]['kind']!='heading':blocks.insert(0,{'kind':'heading','title':'出发之前'})
 while i<len(blocks):
  b=blocks[i]
  if b['kind']=='heading':
   num+=1;body.append(f'<header class="chapter"><span class="chapter-number">{num:02}</span><p class="chapter-label">RUN50 · 第{n}州</p><h2>{escape(b["title"])}</h2></header>')
  elif b['kind']=='paragraph':body.append(tidy(b['html']))
  else:
   group=[b]
   while i+1<len(blocks) and blocks[i+1]['kind']=='figure' and len(group)<3:i+=1;group.append(blocks[i])
   labels=['上','下'] if len(group)==2 else ['上','中','下'];caps=[credit(x['caption']) for x in group]
   body.append('<figure class="photo-strip">'+''.join(f'<img src="{escape(x["src"])}" alt="{escape(x["alt"])}"{dimensions(x["src"])} loading="lazy">' for x in group)+'<figcaption>'+'<br>'.join(escape((labels[j]+'：' if len(group)>1 else '')+c) for j,c in enumerate(caps) if c)+'</figcaption></figure>')
  i+=1
 ending=title.split('｜')[1].split('：')[0] if '｜' in title else '这一站'
 body.append(f'<footer class="ending"><p class="end-mark">本文完</p><p class="series">RUN50 · 第{n}州</p><h2>{escape(ending)}，点亮</h2><p class="credits">文字 / Arsenan<br>摄影 / 见图片署名</p></footer>')
 nav='<nav class="copy-tools"><a href="../../CN/" style="color:inherit">Run50 目录</a><span>摄影杂志版</span><button data-theme-choice="light" aria-pressed="true">白底</button><button data-theme-choice="dark" aria-pressed="false">黑底</button><button id="copy-wechat">一键复制到公众号</button><span id="copy-status" role="status"></span></nav>'
 html='<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+escape(title)+'</title><style>'+css+'</style></head><body>'+nav+'<main data-edition="'+slug+'-editorial">'+'\n'.join(body)+'</main><script src="../../assets/run50-six-editorial-copy.js?v=20261022-original-copy" defer></script></body></html>'
 html,_=normalize(html,slug+'-editorial.html')
 for suffix in ['editorial','modern-rail']:(ROOT/f'run50/wechat/{slug}-{suffix}.html').write_text(html,encoding='utf-8')
 if '/wechat-new/' in d['page']:(ROOT/d['page'].lstrip('/')).write_text(html,encoding='utf-8')
 print(slug,len([b for b in d['blocks'] if b['kind']=='figure']),'photos',num,'chapters',flush=True)
if __name__=='__main__':
 for p in sorted(DATA.glob('*.json')):
  if len(sys.argv)>1 and sys.argv[1] not in p.stem:continue
  render(json.loads(p.read_text(encoding='utf-8')))
