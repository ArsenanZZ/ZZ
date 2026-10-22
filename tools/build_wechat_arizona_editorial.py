"""Reformat the complete Arizona WeChat source in the Run50 photography editorial standard."""
from pathlib import Path
from html import escape
import json,re,shutil
from PIL import Image,ImageOps
from bs4 import BeautifulSoup
import build_wechat_louisville_editorial as style
ROOT=Path(__file__).resolve().parents[1]
ASSET=ROOT/'assets/arizona-editorial-20261013'
SLUG='arizona-phoenix-marathon'
TITLE='Run50 #第29州｜亚利桑那 Buckeye Marathon：沙漠清晨，机场终点，2026 第一跑破4'
COVER_SRC='/assets/cover-medal-zh-index-arizona-phoenix-cn-flat.jpg'
POSTER_SRC='/assets/arizona-editorial-20261013/poster.jpg'
KEYS=['亚利桑那','巴克艾','凤凰城','Siqi','Buckeye','3:58','破 4','破4','Saguaro','巨人柱','机场','Deborah','沙漠','Dobbins Lookout','Papago Park','Hole-in-the-Rock','Tempe Town Lake','阿森纳','UFO','Tesla Model Y','Run50','二〇二六','志愿者','半马','全马','自动驾驶']
UNDER=['去个稍微暖和点的地方','还有就是我一直对这片儿地方充满好奇','总得自己站进去','审美在线','2026 年来了','居然破 4 了','最后十分钟','才算对得起这趟沙漠之行','我心里很清楚','挺好挺好']
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
 d=json.loads((ROOT/'tools/data/arizona-editorial.json').read_text(encoding='utf-8'))
 for b in d['blocks']:
  if b['kind']=='figure':
   with Image.open(ROOT/b['src'].lstrip('/')) as im:b['width'],b['height']=im.size
 assert len([b for b in d['blocks'] if b['kind']=='figure'])==87
 return d
def assets():
 ASSET.mkdir(exist_ok=True)
 for name in ['intro-light.gif','intro-dark.gif','intro-light-still.png','intro-dark-still.png']:
  source={'intro-light.gif':'run50-cutout-intro-light.gif','intro-dark.gif':'run50-cutout-intro-dark.gif','intro-light-still.png':'run50-cutout-intro-light-still.png','intro-dark-still.png':'run50-cutout-intro-dark-still.png'}[name]
  shutil.copyfile(ROOT/'assets'/source,ASSET/name)
 frames=[]
 for n,c in [(13,(.5,.5)),(37,(.45,.25)),(54,(.5,.3)),(60,(.4,.2)),(85,(.5,1))]:
  with Image.open(ROOT/f'run50/stories/chinese/Run50-Arizona-Phoenix-Marathon-clean_files/img-{n:03}.webp') as im:frames.append(ImageOps.fit(im.convert('RGB'),(900,900),centering=c))
 frames[0].save(ASSET/'hero-still.jpg',quality=94)
 frames[0].save(ASSET/'hero.gif',save_all=True,append_images=frames[1:],duration=3000,loop=0,optimize=False)

def arrange(d):
 chapters=[]
 for b in d['blocks']:
  if b['kind']=='heading':chapters.append({'heading':b,'paras':[]})
  elif b['kind']=='paragraph':chapters[-1]['paras'].append(b)
 images={b['id']:b for b in d['blocks'] if b['kind']=='figure' and b['id']!=1}
 plans={
  0:{2:[4],5:[2]},
  1:{3:[7],4:[8],6:[12]},
  2:{4:[3],7:[5,6],10:[9,10,11],11:[13,14],12:[15]},
  3:{0:[16,17],1:[18,19],2:[20,21,22,23],3:[24,25],4:[26,27],5:[29,30],6:[31,32],7:[33],8:[28,34,35],9:[36],10:[37],11:[38,39],12:[40],13:[41,42],14:[43],16:[44],17:[45,46],18:[47,48,49],19:[50,51],20:[52,53,54,55,56,57,58],21:[59,60,61],22:[62,63,64]},
  4:{0:[65],1:[66,67],2:[68,69,70],3:[71],4:[73,74,75],5:[72],6:[76,77,78],7:[79],8:[80],10:[81,82,83],11:[84,85,86]},
  5:{3:[87]}}
 result=[]
 for n,ch in enumerate(chapters):
  result.append(ch['heading'])
  for j,para in enumerate(ch['paras']):
   ids=plans[n].get(j,[])
   # Split long narration at sentence boundaries so large photo sets alternate with prose.
   text=para['text'];sentences=re.findall(r'.*?[。！？](?:[”’])?|.+$',text)
   if len(ids)>3 and len(sentences)>1:
    groups=[ids[k:k+3] for k in range(0,len(ids),3)]
    cuts=[round(k*len(sentences)/len(groups)) for k in range(len(groups)+1)]
    for k,group in enumerate(groups):
     part=''.join(sentences[cuts[k]:cuts[k+1]])
     if part:result.append({'kind':'paragraph','text':part,'original_html':'<p>'+escape(part)+'</p>'})
     result.extend(images[i] for i in group)
   else:
    result.append(para);result.extend(images[i] for i in ids)
 ids=[b['id'] for b in result if b['kind']=='figure']
 assert len(ids)==len(set(ids))==86 and set(ids)==set(images)
 assert ''.join(b['text'] for b in result if b['kind']=='paragraph')==''.join(d['original_paragraphs'])
 return result

def render(d):
 css=re.search(r'<style>(.*?)</style>',style.render(),re.S).group(1)
 css+='''\nmain{padding-left:20px;padding-right:20px}.cover,.intro,.chapter{margin-left:0;margin-right:0}.photo-strip{margin:32px 0 36px}.photo-strip img{display:block;width:100%;height:auto;margin:0}.photo-strip figcaption,figure figcaption{margin:10px 0 0;text-align:center;font-size:12px;line-height:1.8;color:var(--muted)}.brand-intro{display:block;text-align:center;margin:0 auto 14px}.brand-intro img{display:inline-block;width:128px;height:128px}.cover img{display:block;width:100%;height:auto;aspect-ratio:1}.location-poster img{width:100%;height:auto}.location-poster img:first-child{width:100%;max-width:100%;box-sizing:border-box;padding:0 1.26183%;background:#f3efdf;margin:0}.source-note{font-size:11px;line-height:1.8;color:var(--muted);margin-top:24px}.source-note a{color:inherit}.chapter-label{color:#b8452e}html[data-theme="dark"] .chapter-label{color:#ffd36e}.byline{line-height:2}.series{letter-spacing:3px}'''
 pfx='/assets/arizona-editorial-20261013/'
 body=[f'<header class="masthead"><h1>{escape(TITLE)}</h1><p class="byline">亚利桑那巴克艾 · 2026年1月10日<br>文字 / Arsenan</p></header>',
 f'<picture class="brand-intro"><source media="(prefers-reduced-motion: reduce)" srcset="{pfx}intro-light-still.png" data-light-src="{pfx}intro-light-still.png" data-dark-src="{pfx}intro-dark-still.png"><img src="{pfx}intro-light.gif" data-light-src="{pfx}intro-light.gif" data-dark-src="{pfx}intro-dark.gif" alt="Run50 山路片头" width="280" height="280"></picture>',
 f'<figure class="cover"><picture><source media="(prefers-reduced-motion: reduce)" srcset="{pfx}hero-still.jpg"><img src="{pfx}hero.gif" width="900" height="900" alt="沙漠日落、赛道、终点合影、巨人柱和奖牌" fetchpriority="high"></picture><figcaption>沙漠清晨，机场终点，2026第一跑破4<br>摄影 / Arsenan、Siqi、官方摄影</figcaption></figure>',
 '<div class="down" aria-hidden="true">⌄<br>⌄<br>⌄</div>',f'<section class="intro"><p>{emphasize(d["intro"])}</p></section>',
 f'<figure class="photo-strip location-poster"><img src="/assets/arizona-editorial-20261013/map-arizona.jpg" alt="Run50 美国地图，巨人柱指引与星标定位亚利桑那巴克艾"><img src="{POSTER_SRC}" alt="亚利桑那巴克艾 · 2026 · Run50 29"><figcaption>亚利桑那 · 巴克艾 · Run50 第29州<br>封面设计 / Arsenan × AI</figcaption></figure>']
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
 body.append('<footer class="ending"><p class="end-mark">本文完</p><p class="series">RUN50 · 第29州 · 亚利桑那巴克艾</p><h2>亚利桑那，点亮</h2><p class="closing">亚利桑那位于美国西南部，索诺兰沙漠、巨人柱与红岩，构成了这一站的底色。</p><p class="credits">文字 / Arsenan<br>摄影 / Arsenan、Siqi、官方摄影</p></footer>')
 nav='<nav class="copy-tools"><a href="/CN/#run50-series" style="color:inherit">Run50 目录</a><button class="theme-choice" data-theme-choice="light" aria-pressed="true" type="button">白底</button><button class="theme-choice" data-theme-choice="dark" aria-pressed="false" type="button">黑底</button><button id="copy-wechat" type="button">一键复制到公众号</button><span id="copy-status" role="status" aria-live="polite"></span></nav>'
 html='<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+escape(TITLE)+'</title><meta name="description" content="沙漠清晨，机场终点，2026第一跑破4。86张照片，完整保留亚利桑那巴克艾马拉松与赛后红岩、仙人掌旅行。"><meta property="og:image" content="https://zhennanzhang.com'+COVER_SRC+'"><style>'+css+'</style></head><body>'+nav+'<main data-edition="arizona-editorial">'+'\n'.join(body)+'</main><script src="/assets/arizona-editorial-copy.js?v=20261022-text-numbers" defer></script></body></html>'
 for suffix in ['editorial','modern-rail']:(ROOT/f'run50/wechat/{SLUG}-{suffix}.html').write_text(html,encoding='utf-8')
 js=(ROOT/'assets/run50-six-editorial-copy.js').read_text(encoding='utf-8').replace('img.height = 120','img.height = 96')
 js=js.replace("if (tag === 'img' || number || down) {", "if (number) { const p=document.createElement('p'); p.textContent=node.textContent; p.style.cssText='font-family:Arial,sans-serif;font-size:74px;line-height:1;color:' + ink + ';margin:48px 0 14px;font-weight:400;'; return p; }\n      if (tag === 'img' || down) {")
 js=js.replace("node.getAttribute('data-' + theme + '-src') || node.getAttribute('src')", "node.getAttribute('data-' + theme + '-src') || node.getAttribute('data-copy-src') || node.getAttribute('src')")
 js=js.replace("        return img;", "        if (node.matches('.location-poster > img:first-child')) img.style.cssText='display:block;width:100%;max-width:100%;height:auto;box-sizing:border-box;padding:0 1.26183%;background:#f3efdf;margin:0;border:0;';\n        return img;")
 (ROOT/'assets/arizona-editorial-copy.js').write_text(js,encoding='utf-8')
 print('Rendered',len(d['original_paragraphs']),'source paragraphs,',sum(b['kind']=='figure' for b in blocks),'photos')



if __name__=='__main__':
 import sys
 d=prepare()
 if '--assets' in sys.argv:assets()
 render(d)
