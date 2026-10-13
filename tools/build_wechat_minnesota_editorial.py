"""Reformat the complete Minnesota WeChat source in the Run50 photography editorial standard."""
from pathlib import Path
from html import escape
import json,re,shutil
from PIL import Image,ImageOps
from bs4 import BeautifulSoup
import build_wechat_louisville_editorial as style
ROOT=Path(__file__).resolve().parents[1]
ASSET=ROOT/'assets/minnesota-editorial-20261013'
SLUG='minnesota-med-city-marathon'
TITLE='Run50 #第31州｜明尼苏达马拉松：从农田出发，沿 Zumbro 河跑进罗切斯特'
COVER_SRC='/run50/wechat-new/media/minnesota/cover-imagegen-v2.webp'
POSTER_SRC='/run50/wechat-new/media/minnesota/full-20260920/minnesota-fine-border.png'
KEYS=['明尼苏达','罗切斯特','Siqi','21 天','第 31 州','破四','农历生日','森林狼','梅奥诊所','Zumbro','赞布罗河','Med City','Chateau Theatre','injera','银湖','万湖之州','第一次检验','官方摄影师']
UNDER=['21 天自律计划','第一次检验','这是很适合跑马的天气','这份生日礼物倒挺实在','下一个 21 天也接着来','变化终于能看得见','这个周末挺值']

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
 d=json.loads((ROOT/'tools/data/minnesota-editorial.json').read_text(encoding='utf-8'))
 for b in d['blocks']:
  if b['kind']=='figure':
   with Image.open(ROOT/b['src'].lstrip('/')) as im:b['width'],b['height']=im.size
 assert len([b for b in d['blocks'] if b['kind']=='figure'])==91
 return d
def assets():
 ASSET.mkdir(exist_ok=True)
 for name in ['intro-light.gif','intro-dark.gif','intro-light-still.png','intro-dark-still.png']:
  source={'intro-light.gif':'run50-cutout-intro-light.gif','intro-dark.gif':'run50-cutout-intro-dark.gif','intro-light-still.png':'run50-cutout-intro-light-still.png','intro-dark-still.png':'run50-cutout-intro-dark-still.png'}[name]
  shutil.copyfile(ROOT/'assets'/source,ASSET/name)
 frames=[]
 for key,c in [('MN-007-1',(.5,.45)),('MN-021',(.5,.25)),('MN-027-2',(.5,.25)),('MN-040',(.5,.2)),('MN-042',(.65,.5))]:
  source=next(b['src'] for b in prepare()['blocks'] if b.get('id')==key)
  with Image.open(ROOT/source.lstrip('/')) as im:frames.append(ImageOps.fit(im.convert('RGB'),(900,900),centering=c))
 frames[0].save(ASSET/'hero-still.jpg',quality=94)
 frames[0].save(ASSET/'hero.gif',save_all=True,append_images=frames[1:],duration=3000,loop=0,optimize=False)

def arrange(d):
 chapters=[];images={b['id']:b for b in d['blocks'] if b['kind']=='figure'}
 for b in d['blocks']:
  if b['kind']=='heading':chapters.append([b,[]])
  else:chapters[-1][1].append(b)
 moves={'MN-008-1':(0,1),'MN-024':(1,1),'MN-027':(1,3),'MN-025-1':(1,5),'MN-031':(2,0),'MN-043':(12,3),'MN-014-1':(5,2),'MN-014-2':(5,2),'MN-025-4':(9,0)}
 result=[]
 for ci,(h,bs) in enumerate(chapters):
  h=dict(h)
  if ci==len(chapters)-1:h['label']='后记'
  result.append(h);i=0;pi=0
  while i<len(bs):
   b=bs[i]
   if b['kind']!='paragraph':
    if b.get('id') not in moves:result.append(b)
    i+=1;continue
   photos=[];j=i+1
   while j<len(bs) and bs[j]['kind']=='figure':
    if bs[j]['id'] not in moves:photos.append(bs[j])
    j+=1
   photos.extend(images[key] for key,dest in moves.items() if dest==(ci,pi))
   if ci==10 and pi==1:photos=[x for x in photos if x['id']!='MN-029-1']
   if ci==10 and pi==2:photos.insert(0,images['MN-029-1'])
   if ci==10 and pi==3:photos=[images['MN-030-1']]
   if ci==10 and pi==4:photos=[images['MN-030-2']]
   if ci==10 and pi==5:photos=[]
   sentences=re.findall(r'.*?[。！？](?:[”’])?|.+$',b['text'])
   count=min(max(1,(len(photos)+1)//2),len(sentences))
   cuts=[round(k*len(sentences)/count) for k in range(count+1)]
   photo_cuts=[round(k*len(photos)/count) for k in range(count+1)]
   for k in range(count):
    parts=[];chunk=''
    for sentence in sentences[cuts[k]:cuts[k+1]]:
     if chunk and len(chunk)+len(sentence)>130:parts.append(chunk);chunk=''
     chunk+=sentence
    if chunk:parts.append(chunk)
    for t in parts:result.append({'kind':'paragraph','text':t,'original_html':'<p>'+escape(t)+'</p>'})
    result.extend(photos[photo_cuts[k]:photo_cuts[k+1]])
   i=j;pi+=1
 ids=[b['id'] for b in result if b['kind']=='figure']
 assert len(ids)==len(set(ids))==91,(len(ids),len(set(ids)))
 assert set(ids)==set(images)
 assert ''.join(b['text'] for b in result if b['kind']=='paragraph')==''.join(d['original_paragraphs'])
 return result

def render(d):
 css=re.search(r'<style>(.*?)</style>',style.render(),re.S).group(1)
 css+='''\nmain{padding-left:20px;padding-right:20px}.cover,.intro,.chapter{margin-left:0;margin-right:0}.photo-strip{margin:32px 0 36px}.photo-strip img{display:block;width:100%;height:auto;margin:0}.photo-strip figcaption,figure figcaption{margin:10px 0 0;text-align:center;font-size:12px;line-height:1.8;color:var(--muted)}.brand-intro{display:block;text-align:center;margin:0 auto 14px}.brand-intro img{display:inline-block;width:128px;height:128px}.cover img{display:block;width:100%;height:auto;aspect-ratio:1}.location-poster img{width:100%;height:auto}.location-poster img:first-child{width:100%;max-width:100%;box-sizing:border-box;padding:0;background:#f3efdf;margin:0}.source-note{font-size:11px;line-height:1.8;color:var(--muted);margin-top:24px}.source-note a{color:inherit}.chapter-label{color:#b8452e}html[data-theme="dark"] .chapter-label{color:#ffd36e}.byline{line-height:2}.series{letter-spacing:3px}'''
 pfx='/assets/minnesota-editorial-20261013/'
 body=[f'<header class="masthead"><h1>{escape(TITLE)}</h1><p class="byline">明尼苏达罗切斯特 · 2026年5月17日<br>文字 / Arsenan</p></header>',
 f'<picture class="brand-intro"><source media="(prefers-reduced-motion: reduce)" srcset="{pfx}intro-light-still.png" data-light-src="{pfx}intro-light-still.png" data-dark-src="{pfx}intro-dark-still.png"><img src="{pfx}intro-light.gif" data-light-src="{pfx}intro-light.gif" data-dark-src="{pfx}intro-dark.gif" alt="Run50 山路片头" width="280" height="280"></picture>',
 f'<figure class="cover"><picture><source media="(prefers-reduced-motion: reduce)" srcset="{pfx}hero-still.jpg"><img src="{pfx}hero.gif" width="900" height="900" alt="领物合影、赛道、河岸、奖牌与赛后自拍" fetchpriority="high"></picture><figcaption>从农田跑进罗切斯特，把破四作为生日礼物<br>摄影 / Arsenan、Siqi、官方摄影</figcaption></figure>',
 '<div class="down" aria-hidden="true">⌄<br>⌄<br>⌄</div>',f'<section class="intro"><p>{emphasize(d["intro"])}</p></section>',
 f'<figure class="photo-strip location-poster"><img src="/assets/minnesota-editorial-20261013/map-minnesota.jpg" alt="Run50 美国地图，罗切斯特城市地标指向明尼苏达星标"><img src="{POSTER_SRC}" alt="明尼苏达罗切斯特 · 2026 · Run50 31"><figcaption>明尼苏达 · 罗切斯特 · Run50 第31州<br>封面设计 / Arsenan × AI</figcaption></figure>']
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
 body.append('<footer class="ending"><p class="end-mark">本文完</p><p class="series">RUN50 · 第31州 · 明尼苏达罗切斯特</p><h2>明尼苏达，点亮</h2><p class="closing">万湖之州的五月，农田、林荫与河岸，把我送进罗切斯特。</p><p class="credits">文字 / Arsenan<br>摄影 / Arsenan、Siqi、官方摄影、现场跑友</p></footer>')
 nav='<nav class="copy-tools"><a href="/CN/#run50-series" style="color:inherit">Run50 目录</a><button class="theme-choice" data-theme-choice="light" aria-pressed="true" type="button">白底</button><button class="theme-choice" data-theme-choice="dark" aria-pressed="false" type="button">黑底</button><button id="copy-wechat" type="button">一键复制到公众号</button><span id="copy-status" role="status" aria-live="polite"></span></nav>'
 html='<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+escape(TITLE)+'</title><link rel="canonical" href="https://zhennanzhang.com/run50/wechat/minnesota-med-city-marathon-editorial.html"><script src="/analytics.js" defer></script><meta name="description" content="从农田跑进罗切斯特，把破四作为生日礼物。91张照片，记录21天自律计划后的第31州、生日破四和周末自驾。"><meta property="og:image" content="https://zhennanzhang.com'+COVER_SRC+'"><style>'+css+'</style></head><body>'+nav+'<main data-edition="minnesota-editorial">'+'\n'.join(body)+'</main><script src="/assets/minnesota-editorial-copy.js?v=20261013" defer></script></body></html>'
 for suffix in ['editorial','modern-rail']:(ROOT/f'run50/wechat/{SLUG}-{suffix}.html').write_text(html,encoding='utf-8')
 (ROOT/'run50/wechat-new/minnesota-med-city-marathon-modern-rail.html').write_text(html,encoding='utf-8')
 js=(ROOT/'assets/run50-six-editorial-copy.js').read_text(encoding='utf-8').replace('img.height = 120','img.height = 96')
 js=js.replace("if (tag === 'img' || number || down) {", "if (number) { const p=document.createElement('p'); p.textContent=node.textContent; p.style.cssText='font-family:Arial,sans-serif;font-size:74px;line-height:1;color:' + ink + ';margin:48px 0 14px;font-weight:400;'; return p; }\n      if (tag === 'img' || down) {")
 js=js.replace("node.getAttribute('data-' + theme + '-src') || node.getAttribute('src')", "node.getAttribute('data-' + theme + '-src') || node.getAttribute('data-copy-src') || node.getAttribute('src')")
 js=js.replace("        return img;", "        if (node.matches('.location-poster > img:first-child')) img.style.cssText='display:block;width:100%;max-width:100%;height:auto;box-sizing:border-box;padding:0;background:#f3efdf;margin:0;border:0;';\n        return img;")
 (ROOT/'assets/minnesota-editorial-copy.js').write_text(js,encoding='utf-8')
 print('Rendered',len(d['original_paragraphs']),'source paragraphs,',sum(b['kind']=='figure' for b in blocks),'photos')



if __name__=='__main__':
 import sys
 d=prepare()
 if '--assets' in sys.argv:assets()
 render(d)

