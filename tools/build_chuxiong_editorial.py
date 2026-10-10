"""Build the RunCN Chuxiong story from the author's firsthand written draft and 128 selected photos."""
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
TITLE='RunCN #第28站｜云南楚雄马拉松｜从凉都到火城，跑进彝乡楚雄'
COVER_SRC='/assets/runcn-chuxiong-poster-framed-v3-20261010.jpg'
POSTER_SRC='/assets/runcn-chuxiong-article-poster-v5-20261010.jpg'
assert COVER_SRC != POSTER_SRC, 'Homepage plaque cover and article paper poster must stay separate.'
# Captions were checked against all 128 selected photographs.
CAPTIONS=(ROOT/'tools/data/chuxiong-captions.txt').read_text(encoding='utf-8')
CAP=dict(line.split('|',1) for line in CAPTIONS.splitlines() if line.strip())
OFFICIAL=set('15-1 15-2 15-2-0 15-2-1 15-3 15-4 15-5 16-2-1 16-2-2 16-4-1 16-9-1 17-2-1 17-2-2 17-4-1 17-6-3-1 18-1-1 18-3-1 18-4-1 18-5-0 18-6'.split())
UNKNOWN=set('01-2 05-2-11 05-3 05-4 08-1 11-1 11-6 11-7 13-5 18-4-1-0'.split())
KEYS=['楚雄','云南','中国凉都','中国火城','彝乡','福塔','彝人古镇','太阳历文化园','菌菇小火锅','坛子肉','火把节','接驳车','志愿者','两块钱','15000号','4小时15分','三十五公里','四十公里','羊汤锅一条街','7:30','能量胶','影石露娜','RunCN']
UNDER=['来都来了','跑马打工人','一人旅行神器','火车算是稳了','4小时15分','两块钱','一点不后悔']
KEYS += ['新省份','昆明','烟火气','悦然广场','白墙青瓦','老拼','1800米','遥控自拍','天南海北','楚雄州文化活动中心广场','防晒','锁水塔','2004年','彝族左脚舞','国家4A级景区','民族表演','星光夜市','十月太阳历','三十六天','彭姐姐','葡萄牙体育','青龙河','彝海','花山大道','茶花大道','亚高原','下午两点的高铁','民族特色服装','二十四公里','三十公里','水雾','香蕉','小西红柿','最后两百米','大金饼','高原训练','鸡肉和咖喱饭','Siqi','岳父岳母','即拔即种']
UNDER += ['值得折腾吗','自己选号','过了这个村，没这个店了','看到人就高兴','同路人','各有各的特色','拿过去就行','价格嘛，也是很接轨','真的成煤球了','居然这么肥','毛毛虫','心里还挂着一张车票','用自己的脚把一座陌生城市跑上一圈','汗就开始哗哗地流','没必要跟自己硬拧着','胜利在望','超出了我的预期','这一趟没白折腾','提前一个小时','送到座位上','跑完的爽感','满足感很强烈','三十五公里之后的酸痛感','放进了我的RunCN地图里']

KEYS += ['龙川江','坝子','金沙江','长江水系','茶花园','清香园','鹿园','羊汤锅','银色','太阳状纹样','镂空','建筑浮雕','中国火城·浪漫花都']
UNDER += ['城市和山坡离得很近','也是当地人每天生活的一部分','昨天我还在古镇里找吃的，今天就把它挂脖子上了','可以翻折']

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
 d={'title':TITLE,'intro':'从六盘水的凉都，跑到云南的火城。两块钱登福塔，夜游彝人古镇，穿过火把节的羊汤锅一条街；原本犹豫的一趟远行，最后成了RunCN里一个舍不得忘的周末。','source_photo_count':128,'source_subtitles':str(SOURCE/'04-成片/楚雄旅行Vlog_25分钟_中文字幕.srt'),'original_paragraphs':original,'ending_paragraphs':[],'blocks':blocks}

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
 for key,center in [('17-6-3-1',(.5,0)),('10-2',(.5,.2)),('11-6',(.5,.15)),('13-5',(1,.2)),('16-2-2',(.5,.1)),('17-4-1',(.5,0)),('19-1',(0,.75)),('03-3',(1,.15)),('19-8',(.6,.5))]:
  im=Image.open(ASSET/f'CX-{key}.webp');frames.append(ImageOps.fit(im,(900,900),centering=center))
 frames[0].save(ASSET/'hero-still.jpg',quality=95)
 frames[0].save(ASSET/'hero-9photos-20261010.gif',save_all=True,append_images=frames[1:],duration=3000,loop=0,optimize=False)

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
 f'<figure class="cover"><picture><source media="(prefers-reduced-motion: reduce)" srcset="{pfx}hero-still.jpg"><img src="{pfx}hero-9photos-20261010.gif" width="900" height="900" alt="楚雄的比赛、福塔、古镇和奖牌" fetchpriority="high"></picture><figcaption>逛吃一个周末，再跑楚雄 · 照片署名见正文</figcaption></figure>',
 '<div class="down" aria-hidden="true">⌄<br>⌄<br>⌄</div>',f'<section class="intro"><p>{emphasize(d["intro"])}</p></section>',
 f'<figure class="photo-strip location-poster"><img src="/assets/runcn-chuxiong-2026/map-yunnan-chuxiong.jpg" alt="RunCN 中国地图，福塔图案与星标定位云南楚雄"><img src="{POSTER_SRC}" alt="云南楚雄 · 2026 · RunCN 28"><figcaption>云南 · 楚雄 · RunCN 第28站<br>封面设计 / Arsenan × AI</figcaption></figure>']
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
 body.append('<footer class="ending"><p class="end-mark">本文完</p><p class="series">RUNCN · 第28站 · 云南楚雄</p><h2>从凉都到火城，跑进彝乡楚雄</h2><p class="closing">一个新的省份，云南。这次，把楚雄的跑步故事放进RunCN地图里。</p><p class="credits">文字 / Arsenan<br>摄影 / 见图片署名</p></footer>')
 body.append('<p class="source-note">地方与赛事背景：<a href="https://www.cxs.gov.cn/info/1014/912799.htm">2026赛事路线</a> · <a href="https://www.sohu.com/a/1055878836_121106902">赛事接驳与起跑时间</a> · <a href="https://www.cxs.gov.cn/info/egovinfo/1016/xxgkcontent/cxs001-/2023-1026015.htm">城区海拔</a> · <a href="https://www.cxs.gov.cn/info/8735/249388.htm">福塔沿革</a> · <a href="https://www.cxs.gov.cn/info/8825/252228.htm">彝人古镇</a> · <a href="https://ynck.cxz.gov.cn/info/1002/6119.htm">十月太阳历</a> · <a href="https://www.cxs.gov.cn/info/2913/103912.htm">左脚舞</a> · <a href="https://www.ynich.cn/item/41.html">白族民居彩绘</a> · <a href="https://www.cxs.gov.cn/info/1011/921159.htm">火把节美食街</a> · <a href="https://www.cxs.gov.cn/info/12605/344648.htm">青龙河与滨水公园</a> · <a href="https://www.cxs.gov.cn/info/8825/252278.htm">彝海公园</a> · <a href="https://www.weather.com.cn/yunnan/tqyw/07/1934551.shtml">羊汤锅与火把节</a> · <a href="https://mzzj.yn.gov.cn/html/2023/mzwh_0812/50880.html">火把节的餐桌习俗</a>。旅行与比赛经历据作者亲笔稿整理，完赛时间由作者确认。摄影署名见各图。</p>')
 nav='<nav class="copy-tools"><a href="/CN/#runcn-series" style="color:inherit">RunCN 目录</a><button class="theme-choice" data-theme-choice="light" aria-pressed="true" type="button">白底</button><button class="theme-choice" data-theme-choice="dark" aria-pressed="false" type="button">黑底</button><button id="copy-wechat" type="button">一键复制到公众号</button><span id="copy-status" role="status" aria-live="polite"></span></nav>'
 html='<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+escape(TITLE)+'</title><meta name="description" content="从凉都到火城，跑进彝乡楚雄。128张照片与作者亲笔经历，记录福塔、彝人古镇、亚高原马拉松和赶上高铁的周末。"><meta property="og:image" content="https://zhennanzhang.com'+COVER_SRC+'"><style>'+css+'</style></head><body>'+nav+'<main data-edition="runcn-chuxiong">'+'\n'.join(body)+'</main><script src="/assets/runcn-chuxiong-copy.js?v=20261010" defer></script></body></html>'
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
