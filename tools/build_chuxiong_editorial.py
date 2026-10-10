"""Build the RunCN Chuxiong story from the author's Vlog transcript and 128 selected photos."""
from pathlib import Path
from html import escape
import json,re,hashlib
from concurrent.futures import ThreadPoolExecutor
from PIL import Image,ImageOps,ImageDraw,ImageFont
from bs4 import BeautifulSoup
import build_wechat_louisville_editorial as style
ROOT=Path(__file__).resolve().parents[1]
SOURCE=Path(r'Z:\ZhennanZ Folder\0000-ZZ-Run-2026\20260802-楚雄马拉松')
SLUG='chuxiong-marathon'
ASSET=ROOT/'assets/runcn-chuxiong-2026'
DATA=ROOT/'tools/data/chuxiong-editorial.json'
TITLE='RunCN #第28站｜云南楚雄马拉松｜赛前逛吃到天黑，跑完赶火车'
# Captions were checked against all 128 selected photographs.
CAPTIONS=(ROOT/'tools/data/chuxiong-captions.txt').read_text(encoding='utf-8')
CAP=dict(line.split('|',1) for line in CAPTIONS.splitlines() if line.strip())
OFFICIAL=set('15-1 15-2 15-2-0 15-2-1 15-3 15-4 15-5 16-2-1 16-2-2 16-4-1 16-9-1 17-2-1 17-2-2 17-4-1 17-6-3-1 18-1-1 18-3-1 18-4-1 18-5-0 18-6'.split())
UNKNOWN=set('01-2 03-3 05-2-11 05-3 05-4 08-1 09-4-1 10-1 10-2 10-3 11-1 11-6 11-7 13-5 18-4-1-0'.split())
KEYS=['楚雄','云南','福塔','彝人古镇','太阳历文化园','米线','昆明南','火把节','接驳车','志愿者','两块钱','五小时二十分','四小时零六分钟','二十七公里','三十五公里','四十公里','周一上班','7点50分','12点22分','能量胶','金色展翅的大鸟']
UNDER=['跑三走一','跑一走三','最后一哆嗦','说好的雨呢','帽子忘带了','跑完赶火车','没破四','四小时零六分钟','还来得及','差点迟到了','两块钱','明天应该不会这么热吧']

def emphasize(text):
 parts=re.split('('+'|'.join(map(re.escape,sorted(set(KEYS+UNDER),key=len,reverse=True)))+')',text)
 return ''.join(('<strong data-cn-tone="'+str(sum(map(ord,t))%4)+'"'+(' data-cn-emphasis="underline"' if any(u in t for u in UNDER) else '')+'>'+escape(t)+'</strong>') if i%2 else escape(t) for i,t in enumerate(parts))

def prepare():
 ASSET.mkdir(exist_ok=True)

 def convert(item):
  key,cap=item
  f=SOURCE/'000-楚雄-文章照片'/f'CX-{key}.jpg';dest=ASSET/f'CX-{key}.webp'
  if dest.exists():
   try:
    with Image.open(dest) as check:check.verify()
   except Exception:dest.unlink()
  with Image.open(f) as raw:
   im=ImageOps.exif_transpose(raw).convert('RGB');w,h=im.size
   if not dest.exists():im.save(dest,quality=90,method=3)
  credit='赛事官方' if key in OFFICIAL else '' if key in UNKNOWN else 'Arsenan'
  return key,{'kind':'figure','src':'/assets/runcn-chuxiong-2026/'+dest.name,'alt':cap,'caption':cap+(' · 摄影 / '+credit if credit else ''),'source_file':f.name,'width':w,'height':h,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()}
 with ThreadPoolExecutor(max_workers=6) as pool:photo=dict(pool.map(convert,CAP.items()))
 blocks=[];original=[];used=[]
 for line in (ROOT/'tools/data/chuxiong-story.txt').read_text(encoding='utf-8').splitlines():
  if not line.strip():continue
  if line.startswith('# '):
   label,title=line[2:].split('｜',1);blocks.append({'kind':'heading','label':label,'title':title})
  elif line.startswith('@'):
   for key in line[1:].split():blocks.append(photo[key]);used.append(key)
  else:original.append(line);blocks.append({'kind':'paragraph','html':'<p>'+emphasize(line)+'</p>'})
 sources={f.stem.removeprefix('CX-') for f in (SOURCE/'000-楚雄-文章照片').glob('*.jpg')}
 assert len(used)==128 and len(set(used))==128 and set(used)==set(CAP)==sources,(len(used),sources-set(used),set(used)-sources)
 d={'title':TITLE,'intro':'落地昆明，坐火车到楚雄。两块钱登福塔，彝人古镇逛到天黑；第二天跑完四十二公里，再赶火车回去上班。','source_photo_count':128,'source_subtitles':str(SOURCE/'04-成片/楚雄旅行Vlog_25分钟_中文字幕.srt'),'original_paragraphs':original,'ending_paragraphs':[],'blocks':blocks}

 DATA.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
 return d

def assets():
 preview=ASSET/'preview';preview.mkdir(exist_ok=True)
 def small_photo(key):
  with Image.open(ASSET/f'CX-{key}.webp') as im:
   im.thumbnail((1600,2000));im.save(preview/f'CX-{key}.webp',quality=88,method=3)
 with ThreadPoolExecutor(max_workers=6) as pool:list(pool.map(small_photo,CAP))
 hero_assets()
 intro_assets()

def hero_assets():
 # Only the opening montage is cropped. All body photographs retain full dimensions and aspect ratios.
 frames=[]
 for key,center in [('18-6',(.5,.15)),('10-2',(.5,.2)),('11-6',(.5,.15)),('13-5',(1,.2)),('16-2-2',(.5,.1)),('19-1',(0,.75)),('03-3',(1,.15))]:
  im=Image.open(ASSET/f'CX-{key}.webp');frames.append(ImageOps.fit(im,(900,900),centering=center))
 frames[0].save(ASSET/'hero-still.jpg',quality=95)
 frames[0].save(ASSET/'hero.gif',save_all=True,append_images=frames[1:],duration=3000,loop=0,optimize=False)

def intro_assets():
 # Mountain, RunCN wordmark, then a river; no small slogan.
 font=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',53)
 for theme,bg,ink in [('light','#ffffff','#b8452e'),('dark','#191919','#ffd36e')]:
  frames=[]
  points=[(30,110),(65,110),(100,68),(135,110),(158,88),(190,110),(250,110)]
  for k in range(24):
   im=Image.new('RGB',(280,280),bg);dr=ImageDraw.Draw(im)
   for j in range(min(6,(k+1)//2)):
    dr.line([points[j],points[j+1]],fill=ink,width=5)
   if k>=12:
    alpha=min(1,(k-11)/5)
    layer=Image.new('RGBA',(280,280));ld=ImageDraw.Draw(layer)
    ld.text((140,151),'RunCN',font=font,fill=ink,anchor='mm')
    if k>=17:
     import math
     river=[(x,200+6*math.sin((x-60)*math.pi/70)) for x in range(60,221)]
     end=min(len(river),int(len(river)*(k-16)/6))
     if end>1:
      ld.line(river[:end],fill=ink,width=3)
      ld.line([(x,y+12) for x,y in river[:end]],fill=ink,width=2)
    if alpha<1:layer.putalpha(layer.getchannel('A').point(lambda x:int(x*alpha)))
    im=Image.alpha_composite(im.convert('RGBA'),layer).convert('RGB')
   frames.append(im)
  frames[-1].save(ASSET/f'intro-{theme}-still.png')
  frames[0].save(ASSET/f'intro-{theme}.gif',save_all=True,append_images=frames[1:],duration=[70]*23+[1600],loop=0,optimize=False)

def render(d):
 css=re.search(r'<style>(.*?)</style>',style.render(),re.S).group(1)
 css+='''\nmain{padding-left:20px;padding-right:20px}.cover,.intro,.chapter{margin-left:0;margin-right:0}.photo-strip{margin:32px 0 36px}.photo-strip img{display:block;width:100%;height:auto;margin:0}.photo-strip figcaption,figure figcaption{margin:10px 0 0;text-align:center;font-size:12px;line-height:1.8;color:var(--muted)}.brand-intro{display:block;text-align:center;margin:0 auto 14px}.brand-intro img{display:inline-block;width:128px;height:128px}.cover img{display:block;width:100%;height:auto;aspect-ratio:1}.location-poster img{width:100%;height:auto}.source-note{font-size:11px;line-height:1.8;color:var(--muted);margin-top:24px}.source-note a{color:inherit}.chapter-label{color:#b8452e}html[data-theme="dark"] .chapter-label{color:#ffd36e}.byline{line-height:2}.series{letter-spacing:3px}'''
 pfx='/assets/runcn-chuxiong-2026/'
 body=[f'<header class="masthead"><h1>{escape(TITLE)}</h1><p class="byline">云南楚雄 · 2026年8月2日<br>文字 / Arsenan</p></header>',
 f'<picture class="brand-intro"><source media="(prefers-reduced-motion: reduce)" srcset="{pfx}intro-light-still.png" data-light-src="{pfx}intro-light-still.png" data-dark-src="{pfx}intro-dark-still.png"><img src="{pfx}intro-light.gif" data-light-src="{pfx}intro-light.gif" data-dark-src="{pfx}intro-dark.gif" alt="RunCN 山路片头" width="280" height="280"></picture>',
 f'<figure class="cover"><picture><source media="(prefers-reduced-motion: reduce)" srcset="{pfx}hero-still.jpg"><img src="{pfx}hero.gif" width="900" height="900" alt="楚雄的比赛、福塔、古镇和奖牌" fetchpriority="high"></picture><figcaption>逛吃一个周末，再跑楚雄 · 照片署名见正文</figcaption></figure>',
 '<div class="down" aria-hidden="true">⌄<br>⌄<br>⌄</div>',f'<section class="intro"><p>{emphasize(d["intro"])}</p></section>',
 '<figure class="photo-strip location-poster"><img src="/assets/runcn-chuxiong-2026/map-yunnan-chuxiong.jpg" alt="RunCN 中国地图，福塔图案与星标定位云南楚雄"><img src="/assets/runcn-chuxiong-poster-print-v2-20261010.jpg" alt="云南楚雄 · 2026 · RunCN 28"><figcaption>云南 · 楚雄 · RunCN 第28站<br>封面设计 / Arsenan × AI</figcaption></figure>']
 blocks=d['blocks'];i=0;n=0
 while i<len(blocks):
  b=blocks[i]
  if b['kind']=='heading':
   n+=1;body.append(f'<header class="chapter"><span class="chapter-number">{n:02}</span><p class="chapter-label">{b["label"]}</p><h2>{escape(b["title"])}</h2></header>')
  elif b['kind']=='paragraph':body.append(b['html'].replace('<p>','<p class="prose" style="margin:0 0 22px;font-size:15px;line-height:1.95;letter-spacing:.5px;text-align:justify">'))
  else:
   group=[b]
   while b['width']>b['height']*1.15 and i+1<len(blocks) and len(group)<3:
    nxt=blocks[i+1]
    if nxt['kind']!='figure' or nxt['width']<=nxt['height']*1.15:break
    group.append(nxt);i+=1
   body.append('<figure class="photo-strip">'+''.join(f'<img src="{x["src"]}" srcset="{x["src"].replace("/CX-","/preview/CX-")} 1600w" sizes="(max-width:677px) calc(100vw - 40px), 637px" data-copy-src="{x["src"].replace("/CX-","/preview/CX-")}" alt="{escape(x["alt"])}" width="{x["width"]}" height="{x["height"]}" loading="lazy" decoding="async" style="display:block;width:100%;height:auto">' for x in group)+'<figcaption>'+'<br>'.join(escape(x['caption']) for x in group)+'</figcaption></figure>')
  i+=1
 for p in d['ending_paragraphs']:body.append('<p class="prose" style="font-size:15px;line-height:1.95;text-align:justify">'+emphasize(p)+'</p>')
 body.append('<footer class="ending"><p class="end-mark">本文完</p><p class="series">RUNCN · 第28站 · 云南楚雄</p><h2>赛前逛吃，跑完赶车</h2><p class="closing">从福塔俯看楚雄，到彝人古镇逛吃，再跑完一场晒着太阳的马拉松。</p><p class="credits">文字 / Arsenan<br>摄影 / 见图片署名</p></footer>')
 body.append('<p class="source-note">地方与赛事背景：<a href="https://www.cxs.gov.cn/info/1014/912799.htm">楚雄市政府：2026赛事路线</a> · <a href="https://www.cxs.gov.cn/info/8735/249388.htm">福塔沿革</a> · <a href="https://www.cxs.gov.cn/info/8825/252228.htm">彝人古镇</a>。旅行与比赛经历据本人视频口述整理；四小时零六分钟为当时口述，并非赛事官方计时。未标明摄影者的合影与人像，署名待核实。</p>')
 nav='<nav class="copy-tools"><a href="/CN/#runcn-series" style="color:inherit">RunCN 目录</a><button class="theme-choice" data-theme-choice="light" aria-pressed="true" type="button">白底</button><button class="theme-choice" data-theme-choice="dark" aria-pressed="false" type="button">黑底</button><button id="copy-wechat" type="button">一键复制到公众号</button><span id="copy-status" role="status" aria-live="polite"></span></nav>'
 html='<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+escape(TITLE)+'</title><meta name="description" content="128张照片记录2026楚雄马拉松周末：福塔、彝人古镇、太阳历文化园，从赛前逛吃到完赛赶火车。"><meta property="og:image" content="https://zhennanzhang.com/assets/runcn-chuxiong-poster-print-v2-20261010.jpg"><style>'+css+'</style></head><body>'+nav+'<main data-edition="runcn-chuxiong">'+'\n'.join(body)+'</main><script src="/assets/runcn-chuxiong-copy.js?v=20261010" defer></script></body></html>'
 for suffix in ['editorial','modern-rail']:(ROOT/f'run50/wechat/{SLUG}-{suffix}.html').write_text(html,encoding='utf-8')
 js=(ROOT/'assets/run50-six-editorial-copy.js').read_text(encoding='utf-8').replace('img.height = 120','img.height = 96')
 js=js.replace("if (tag === 'img' || number || down) {", "if (number) { const p=document.createElement('p'); p.textContent=node.textContent; p.style.cssText='font-family:Arial,sans-serif;font-size:74px;line-height:1;color:' + ink + ';margin:48px 0 14px;font-weight:400;'; return p; }\n      if (tag === 'img' || down) {")
 js=js.replace("node.getAttribute('data-' + theme + '-src') || node.getAttribute('src')", "node.getAttribute('data-' + theme + '-src') || node.getAttribute('data-copy-src') || node.getAttribute('src')")
 (ROOT/'assets/runcn-chuxiong-copy.js').write_text(js,encoding='utf-8')
 print('Rendered',len(d['original_paragraphs']),'source paragraphs,',sum(b['kind']=='figure' for b in blocks),'photos')

if __name__=='__main__':
 import argparse
 ap=argparse.ArgumentParser();ap.add_argument('--assets',action='store_true');ap.add_argument('--import-source',action='store_true');args=ap.parse_args()
 d=prepare() if args.import_source or not DATA.exists() else json.loads(DATA.read_text(encoding='utf-8'))
 if args.assets:assets()
 render(d)
