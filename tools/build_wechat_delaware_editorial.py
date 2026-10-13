"""Reformat the complete Arizona WeChat source in the Run50 photography editorial standard."""
from pathlib import Path
from html import escape
import json,re,shutil
from PIL import Image,ImageOps
from bs4 import BeautifulSoup
import build_wechat_louisville_editorial as style
ROOT=Path(__file__).resolve().parents[1]
ASSET=ROOT/'assets/delaware-editorial-20261013'
SLUG='delaware-marathon'
TITLE='Run50 #第30州｜特拉华马拉松：迟到的第30州，从威尔明顿跑进湿地'
COVER_SRC='/run50/wechat-new/media/delaware/cover-imagegen-v2.webp'
POSTER_SRC='/run50/wechat-new/media/delaware/delaware-fine-border-20260920.png'
KEYS=['特拉华','威尔明顿','Siqi','第 30 州','The First State','Norton','阿巴拉契亚','布兰迪万','克里斯蒂娜河','Cool Spring','Swinging Footbridge','Jack A. Markell Trail','湿地','Run50','Planet Fitness','南翔','250 周年','官方照片']
UNDER=['这是我的生活，又不是我的人设','我自己喜欢就够了','把第 30 州补上','不慌不忙、从从容容','这次终于完成了','没白坐','按自己的节奏继续','这是我和 Siqi 一起走的旅程']

def emphasize(html):
 soup=BeautifulSoup(html,'html.parser')
 for el in soup.find_all(True):
  el.attrs={}
  if el.name in ['b','strong']:el.name='strong'
 for node in list(soup.find_all(string=True)):
  if node.parent.name=='strong':continue
  parts=re.split('('+'|'.join(map(re.escape,sorted(set(KEYS+UNDER),key=len,reverse=True)))+')',str(node))
  if len(parts)>1:
   for i,t in enumerate(parts):
    if i%2:
     tag=soup.new_tag('strong');tag.string=t;node.insert_before(tag)
    else:node.insert_before(t)
   node.extract()
 for tag in soup.find_all('strong'):
  text=tag.get_text();tag['data-cn-tone']=str(sum(map(ord,text))%4)
  if any(t in text for t in UNDER):tag['data-cn-emphasis']='underline'
 return str(soup)
def prepare():
 d=json.loads((ROOT/'tools/data/delaware-editorial.json').read_text(encoding='utf-8'))
 for b in d['blocks']:
  if b['kind']=='figure':
   with Image.open(ROOT/b['src'].lstrip('/')) as im:b['width'],b['height']=im.size
 assert len([b for b in d['blocks'] if b['kind']=='figure'])==106
 return d
def assets():
 ASSET.mkdir(exist_ok=True)
 for name in ['intro-light.gif','intro-dark.gif','intro-light-still.png','intro-dark-still.png']:
  source={'intro-light.gif':'run50-cutout-intro-light.gif','intro-dark.gif':'run50-cutout-intro-dark.gif','intro-light-still.png':'run50-cutout-intro-light-still.png','intro-dark-still.png':'run50-cutout-intro-dark-still.png'}[name]
  shutil.copyfile(ROOT/'assets'/source,ASSET/name)
 frames=[]
 for key,c in [('DE-005',(.5,.5)),('DE-014',(.5,.45)),('DE-032-3',(.5,.2)),('DE-050-1',(.5,.35)),('DE-053',(.5,.5))]:
  source=next(b['src'] for b in prepare()['blocks'] if b.get('id')==key)
  with Image.open(ROOT/source.lstrip('/')) as im:frames.append(ImageOps.fit(im.convert('RGB'),(900,900),centering=c))
 frames[0].save(ASSET/'hero-still.jpg',quality=94)
 frames[0].save(ASSET/'hero.gif',save_all=True,append_images=frames[1:],duration=3000,loop=0,optimize=False)

def arrange(d):
 chapters=[]
 images={b['id']:b for b in d['blocks'] if b['kind']=='figure'}
 for b in d['blocks']:
  if b['kind']=='heading':chapters.append([b,[]])
  else:chapters[-1][1].append(b)
 # Two opening photographs are previews; the journey itself keeps its source order.
 for ch in chapters:ch[1][:]=[b for b in ch[1] if b.get('id') not in ['DE-014','DE-011']]
 chapters[0][1].insert(3,images['DE-014'])
 chapters[1][1].insert(1,images['DE-011'])
 result=[]
 for h,bs in chapters:
  result.append(h);i=0
  while i<len(bs):
   b=bs[i]
   if b['kind']!='paragraph':result.append(b);i+=1;continue
   photos=[];j=i+1
   while j<len(bs) and bs[j]['kind']=='figure':photos.append(bs[j]);j+=1
   sentences=re.findall(r'.*?[。！？](?:[”’])?|.+$',b['text'])
   groups=[photos[k:k+3] for k in range(0,len(photos),3)]
   if len(groups)>1 and len(sentences)>=len(groups):
    cuts=[round(k*len(sentences)/len(groups)) for k in range(len(groups)+1)]
    for k,g in enumerate(groups):
     t=''.join(sentences[cuts[k]:cuts[k+1]])
     result.append({'kind':'paragraph','text':t,'original_html':'<p>'+escape(t)+'</p>'});result.extend(g)
   else:result.append(b);result.extend(photos)
   i=j
 ids=[b['id'] for b in result if b['kind']=='figure']
 assert len(ids)==len(set(ids))==106
 assert ''.join(b['text'] for b in result if b['kind']=='paragraph')==''.join(d['original_paragraphs'])
 return result

def render(d):
 css=re.search(r'<style>(.*?)</style>',style.render(),re.S).group(1)
 css+='''\nmain{padding-left:20px;padding-right:20px}.cover,.intro,.chapter{margin-left:0;margin-right:0}.photo-strip{margin:32px 0 36px}.photo-strip img{display:block;width:100%;height:auto;margin:0}.photo-strip figcaption,figure figcaption{margin:10px 0 0;text-align:center;font-size:12px;line-height:1.8;color:var(--muted)}.brand-intro{display:block;text-align:center;margin:0 auto 14px}.brand-intro img{display:inline-block;width:128px;height:128px}.cover img{display:block;width:100%;height:auto;aspect-ratio:1}.location-poster img{width:100%;height:auto}.location-poster img:first-child{width:100%;max-width:100%;box-sizing:border-box;padding:0;background:#f3efdf;margin:0}.source-note{font-size:11px;line-height:1.8;color:var(--muted);margin-top:24px}.source-note a{color:inherit}.chapter-label{color:#b8452e}html[data-theme="dark"] .chapter-label{color:#ffd36e}.byline{line-height:2}.series{letter-spacing:3px}'''
 pfx='/assets/delaware-editorial-20261013/'
 body=[f'<header class="masthead"><h1>{escape(TITLE)}</h1><p class="byline">特拉华威尔明顿 · 2026年4月19日<br>文字 / Arsenan</p></header>',
 f'<picture class="brand-intro"><source media="(prefers-reduced-motion: reduce)" srcset="{pfx}intro-light-still.png" data-light-src="{pfx}intro-light-still.png" data-dark-src="{pfx}intro-dark-still.png"><img src="{pfx}intro-light.gif" data-light-src="{pfx}intro-light.gif" data-dark-src="{pfx}intro-dark.gif" alt="Run50 山路片头" width="280" height="280"></picture>',
 f'<figure class="cover"><picture><source media="(prefers-reduced-motion: reduce)" srcset="{pfx}hero-still.jpg"><img src="{pfx}hero.gif" width="900" height="900" alt="朝霞、河滨合影、铁桥自拍、冲线与奖牌" fetchpriority="high"></picture><figcaption>迟到的第30州，从威尔明顿跑进湿地<br>摄影 / Arsenan、Siqi、官方摄影</figcaption></figure>',
 '<div class="down" aria-hidden="true">⌄<br>⌄<br>⌄</div>',f'<section class="intro"><p>{emphasize(d["intro"])}</p></section>',
 f'<figure class="photo-strip location-poster"><img src="/run50/wechat-new/media/delaware/run50-de-star-map-20260920.png" alt="Run50 美国地图，星标定位特拉华威尔明顿"><img src="{POSTER_SRC}" alt="特拉华威尔明顿 · 2026 · Run50 30"><figcaption>特拉华 · 威尔明顿 · Run50 第30州<br>封面设计 / Arsenan × AI</figcaption></figure>']
 blocks=arrange(d);i=0;n=0
 while i<len(blocks):
  b=blocks[i]
  if b['kind']=='heading':
   n+=1;body.append(f'<header class="chapter"><span class="chapter-number">{n:02}</span><p class="chapter-label">{b["label"]}</p><h2>{escape(b["title"])}</h2></header>')
  elif b['kind']=='paragraph':body.append(emphasize(b['original_html']).replace('<p>','<p class="prose" style="margin:0 0 22px;font-size:15px;line-height:1.95;letter-spacing:.5px;text-align:justify">'))
  else:
   group=[b]
   while i+1<len(blocks) and len(group)<3:
    nxt=blocks[i+1]
    if nxt['kind']!='figure':break
    group.append(nxt);i+=1
   labels=['上','下'] if len(group)==2 else ['上','中','下']
   body.append('<figure class="photo-strip">'+''.join(f'<img src="{x["src"]}" alt="{escape(x["alt"])}" loading="lazy" decoding="async" style="display:block;width:100%;height:auto;margin:0">' for x in group)+'<figcaption>'+'<br>'.join((labels[j]+'：' if len(group)>1 else '')+escape(x['caption']) for j,x in enumerate(group))+'</figcaption></figure>')
  i+=1
 for p in d.get('ending_paragraphs',[]):body.append('<p class="prose" style="font-size:15px;line-height:1.95;text-align:justify">'+emphasize(p)+'</p>')
 body.append('<footer class="ending"><p class="end-mark">本文完</p><p class="series">RUN50 · 第30州 · 特拉华威尔明顿</p><h2>特拉华，点亮</h2><p class="closing">美国第一州，也是我的第三十州。从河滨老城跑进湿地，再和Siqi一起开车回家。</p><p class="credits">文字 / Arsenan<br>摄影 / Arsenan、Siqi、官方摄影</p></footer>')
 nav='<nav class="copy-tools"><a href="/CN/#run50-series" style="color:inherit">Run50 目录</a><button class="theme-choice" data-theme-choice="light" aria-pressed="true" type="button">白底</button><button class="theme-choice" data-theme-choice="dark" aria-pressed="false" type="button">黑底</button><button id="copy-wechat" type="button">一键复制到公众号</button><span id="copy-status" role="status" aria-live="polite"></span></nav>'
 html='<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+escape(TITLE)+'</title><meta name="description" content="迟到的第30州，从威尔明顿跑进湿地。106张照片，完整记录特拉华马拉松、威尔明顿河滨与自驾往返。"><meta property="og:image" content="https://zhennanzhang.com'+COVER_SRC+'"><style>'+css+'</style></head><body>'+nav+'<main data-edition="delaware-editorial">'+'\n'.join(body)+'</main><script src="/assets/delaware-editorial-copy.js?v=20261013" defer></script></body></html>'
 for suffix in ['editorial','modern-rail']:(ROOT/f'run50/wechat/{SLUG}-{suffix}.html').write_text(html,encoding='utf-8')
 (ROOT/'run50/wechat-new/delaware-marathon-modern-rail.html').write_text(html,encoding='utf-8')
 js=(ROOT/'assets/run50-six-editorial-copy.js').read_text(encoding='utf-8').replace('img.height = 120','img.height = 96')
 js=js.replace("if (tag === 'img' || number || down) {", "if (number) { const p=document.createElement('p'); p.textContent=node.textContent; p.style.cssText='font-family:Arial,sans-serif;font-size:74px;line-height:1;color:' + ink + ';margin:48px 0 14px;font-weight:400;'; return p; }\n      if (tag === 'img' || down) {")
 js=js.replace("node.getAttribute('data-' + theme + '-src') || node.getAttribute('src')", "node.getAttribute('data-' + theme + '-src') || node.getAttribute('data-copy-src') || node.getAttribute('src')")
 js=js.replace("        return img;", "        if (node.matches('.location-poster > img:first-child')) img.style.cssText='display:block;width:100%;max-width:100%;height:auto;box-sizing:border-box;padding:0;background:#f3efdf;margin:0;border:0;';\n        return img;")
 (ROOT/'assets/delaware-editorial-copy.js').write_text(js,encoding='utf-8')
 print('Rendered',len(d['original_paragraphs']),'source paragraphs,',sum(b['kind']=='figure' for b in blocks),'photos')



if __name__=='__main__':
 import sys
 d=prepare()
 if '--assets' in sys.argv:assets()
 render(d)

