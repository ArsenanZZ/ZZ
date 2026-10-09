"""Build the complete RunCN Liupanshui story from the author's export and 88 selected photos."""
from pathlib import Path
from html import escape
import json,re,hashlib
from concurrent.futures import ThreadPoolExecutor
from PIL import Image,ImageOps,ImageDraw,ImageFont
from bs4 import BeautifulSoup
import build_wechat_louisville_editorial as style
ROOT=Path(__file__).resolve().parents[1]
SOURCE=Path(r'Z:\ZhennanZ Folder\0000-ZZ-Run-2026\20260719-六盘水马拉松')
SLUG='liupanshui-marathon'
ASSET=ROOT/'assets/runcn-liupanshui-2026'
DATA=ROOT/'tools/data/liupanshui-editorial.json'
TITLE='RunCN #第27站｜贵州六盘水马拉松｜乌蒙山里跑一个周末，凉都也会晒'
# Captions were checked against all 88 source photographs, not inferred from filenames alone.
CAPTIONS='''00|坐高铁，从广州出发
00-1|车窗外，山开始多起来
00-2|山峰之间的村庄和田地
01|到达六盘水站
01-1|街边的水城羊肉粉店
02|抵达后的第一晚，先去街上转转
03|夜里的餐馆招牌
04|雨伞下面听演唱会
04-1|舞台上的歌手
05|雨后的街道，摊位还很热闹
05-1|摊主正在处理刺梨
05-2|鲜榨刺梨汁的摊位
06|凤池园清晨，楼房映在水里
06-1|湖面上的石拱桥
06-2|亭楼与倒影
07|乌蒙山里的水面和草坡
07-0|风机下面留张照片
07-1|观景台上，大家都朝着远山
07-2|草地上的马，也来合个影
07-3|到了乌蒙大草原
08|牛在斜坡上吃草
08-0|草地上散着几匹马
08-0-1|骑马的游客和牵马人
08-1|七月的山上，外套还得穿着
08-2|一日游认识的伙伴们
08-3|草原入口的小摊
08-4|炉子上的烤串
09|又换回花衬衫，继续逛
09-0|树林之间的草地
10|路边指向北盘江大桥的招牌
10-1|从桥下仰望，桥塔伸进云里
10-1-1|高桥横跨两侧山谷
10-2|峡谷底下的流水
10-2-1|索桥这一头，是河边的餐馆
11-0|海坪山坡上的房屋
11-1|海坪彝族小镇留影
11-2|巡游队伍从身边经过
11-3|土司宴现场
11-4|回城后，先吃一碗猪脚饭
12-1|傍晚的商场外
12-2|领物现场的跑者们
12-3|展位和志愿者
12-4|举着加油棒的志愿者
12-5|换好比赛穿的衣服
13-0|早上六点四十，准备出门
13-1|沿着河边步道去起点
13-2|去起点的路上，也有摄影师
14-0|起跑前，街道上全是跑者
14-1|人群开始向前移动
14-2|起跑的人群里找找我
14-2-1|跑者们经过路口
14-3|蓝色上衣、绿色袖套，出发了
14-4|看见镜头，先打个招呼
14-5|路边穿民族服饰的加油者
14-6|在补给站拿杯水
14-7|6公里的加油点
14-8|跑在人群里
14-9|赛道上的特色装扮
14-9-1|跑着跑着，抬头看看山
15-0|补给站的志愿者把水杯排好
15-1|赛道旁遇到举旗的跑友
15-2|路上还是一大群人
15-2-1|23公里，继续往前
15-2-2|“冲破这个坡，前路皆坦途”
15-3|张开双臂，跑过镜头
15-4|一路跑，一路拍
15-5|沿路围观和加油的居民
15-6|到30公里了
15-7|经过护栏旁的拍照点
15-8|跑过明湖湿地公园
16-0|树荫外面，太阳已经很足
16-1|35公里，拍张照再走
16-2|树荫下的一段赛道
16-3|后半程，继续和镜头打招呼
16-4|举起双手，离终点又近一点
17-0|最后一段，慢慢往前跑
17-1|和其他跑者一起往终点去
17-2|再举一次手
17-3|遇到穿阿根廷文化衫的跑友
17-4|聊着球，一起往终点跑
17-5|终点前，和球迷跑友合个影
18-0|六盘水马拉松完赛奖牌
18-1|完赛了，活动一下腿
18-2|拿上奖牌，今天跑完了
19-0|背好东西，准备赶下一程
19-1|车站里都是刚跑完的跑者
19-2|六盘水站，准备返程
19-3|跑完马拉松，晚上接着看球'''
CAP=dict(line.split('|',1) for line in CAPTIONS.splitlines())
OFFICIAL=set('14-1 14-2 14-2-1 14-3 14-4 14-5 14-8 14-9 15-2 15-3 15-4 15-7 16-3 16-4 17-0 17-1 17-2 17-3 17-4'.split())
UNKNOWN=set('07-0 07-2 07-3 08-1 08-2 09 11-1 15-6 16-1 17-5 18-1 18-2'.split())
# Each entry is a photo group inserted after the given paragraph index, maintaining the author's prose order.
INSERT={
'lede':{5:['00','00-1','00-2']},
'arrival':{1:['01','01-1','02'],2:['03'],3:['05-1','05-2'],4:['04','04-1','05']},
'morning':{1:['06','06-1'],3:['06-2']},
'wumeng':{2:['07'],3:['07-0','07-1'],4:['08','08-0','08-0-1'],5:['08-3','08-4'],7:['07-2','08-2'],9:['07-3','08-1','09','09-0']},
'bridge':{1:['10'],3:['10-1','10-1-1'],4:['10-2','10-2-1']},
'yizu':{1:['11-0','11-1'],2:['11-2','11-3']},
'expo':{1:['11-4','12-1'],2:['12-2','12-3','12-4'],4:['12-5']},
'race':{1:['13-0'],2:['13-1','13-2'],3:['14-0','14-1','14-2','14-2-1'],6:['14-3','14-4'],7:['14-5','14-7'],8:['15-1','15-5'],10:['14-8','14-9','15-2']},
'football':{2:['14-9-1'],4:['15-6'],6:['17-3','17-4','17-5']},
'glasses':{2:['14-6'],4:['15-4']},
'finish':{1:['15-0','15-2-1','15-2-2'],2:['15-8','16-0','16-2'],3:['15-3','15-7'],4:['16-1','16-3','16-4'],5:['17-0','17-1','17-2'],6:['18-0','18-1','18-2']},
'return':{3:['19-0'],4:['19-1','19-2'],7:['19-3']}}
LABELS={'lede':'前言','arrival':'抵达水城','morning':'赛前清晨','wumeng':'乌蒙山里','bridge':'北盘江畔','yizu':'海坪火把季','expo':'傍晚领物','race':'清晨起跑','football':'赛道闲聊','glasses':'第一视角','finish':'30公里以后','return':'返程路上'}
KEYS=['六盘水','乌蒙大草原','水城古镇','凤池园','北盘江','海坪','火把季','火把节','贵州','中国凉都','江南煤都','三线建设','2018 年','五小时二十分','两小时五十多分','雷鸟 V4','Meta Oakley','C 罗','西班牙','阿根廷','五百米','三十公里','四十二公里','跑跑走走','高原','凉都','时差','新鞋','摄影师','志愿者','刺梨汁','七点四十','乌蒙山连着山外山']
UNDER=['没中签','翻过一座，还有下一座','凉都','跑跑走走','最后我们一起冲线','跑的挺慢，但谁在乎呢？','五小时二十分','不想支持阿根廷','这段旺季很重要','不用一直掏手机']

def emphasize(text):
 parts=re.split('('+'|'.join(map(re.escape,sorted(set(KEYS+UNDER),key=len,reverse=True)))+')',text)
 return ''.join(('<strong data-cn-tone="'+str(sum(map(ord,t))%4)+'"'+(' data-cn-emphasis="underline"' if any(u in t for u in UNDER) else '')+'>'+escape(t)+'</strong>') if i%2 else escape(t) for i,t in enumerate(parts))

def prepare():
 ASSET.mkdir(exist_ok=True)
 soup=BeautifulSoup((SOURCE/'liupanshui-marathon-run-cn-updated-editable.html').read_text(encoding='utf-8'),'html.parser')
 def convert(item):
  key,cap=item
  f=SOURCE/'00-文章照片'/f'Liu-{key}.jpg';dest=ASSET/f'Liu-{key}.webp'
  if dest.exists():
   try:
    with Image.open(dest) as check:check.verify()
   except Exception:dest.unlink()
  with Image.open(f) as raw:
   im=ImageOps.exif_transpose(raw).convert('RGB');w,h=im.size
   if not dest.exists():im.save(dest,quality=90,method=3)
  credit='赛事官方' if key in OFFICIAL else '' if key in UNKNOWN else 'Arsenan'
  return key,{'kind':'figure','src':'/assets/runcn-liupanshui-2026/'+dest.name,'alt':cap,'caption':cap+(' · 摄影 / '+credit if credit else ''),'source_file':f.name,'width':w,'height':h,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()}
 with ThreadPoolExecutor(max_workers=6) as pool:photo=dict(pool.map(convert,CAP.items()))
 blocks=[];original=[];used=[]
 sections=[('lede',soup.select_one('.lede'))]+[(s['id'],s) for s in soup.select('section.chapter')]
 for sid,s in sections:
  heading=s.select_one('h2');title=heading.get_text(strip=True) if heading else '2018年没中签，2026年总算跑上了'
  blocks.append({'kind':'heading','label':LABELS[sid],'title':title})
  paragraphs=s.select('.prose p, aside.note p') if sid!='lede' else s.select('p')
  for i,p in enumerate(paragraphs,1):
   text=p.get_text('',strip=True);original.append(text)
   blocks.append({'kind':'paragraph','html':'<p>'+emphasize(text)+'</p>'})
   for key in INSERT.get(sid,{}).get(i,[]):blocks.append(photo[key]);used.append(key)
  assert not any(i>len(paragraphs) for i in INSERT.get(sid,{})),(sid,len(paragraphs))
 assert len(used)==88 and len(set(used))==88 and set(used)==set(CAP),(len(used),set(CAP)-set(used))
 ending=[p.get_text('',strip=True) for p in soup.select('section.finish p')]
 d={'title':TITLE,'intro':'2018年没中签，2026年终于跑上了。先逛乌蒙山，再跑六盘水；草原、高桥、火把季，全塞进一个周末。','source_html':str(SOURCE/'liupanshui-marathon-run-cn-updated-editable.html'),'source_photo_count':88,'original_paragraphs':original,'ending_paragraphs':ending,'blocks':blocks}
 DATA.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
 return d

def assets():
 preview=ASSET/'preview';preview.mkdir(exist_ok=True)
 def small_photo(key):
  with Image.open(ASSET/f'Liu-{key}.webp') as im:
   im.thumbnail((1600,2000));im.save(preview/f'Liu-{key}.webp',quality=88,method=3)
 with ThreadPoolExecutor(max_workers=6) as pool:list(pool.map(small_photo,CAP))
 # Only the opening montage is cropped. All body photographs retain full dimensions and aspect ratios.
 frames=[]
 for key,center in [('16-4',(.5,.05)),('08-2',(.5,.3)),('10-1-1',(.5,.45)),('17-3',(.5,.05)),('18-0',(.5,.65))]:
  im=Image.open(ASSET/f'Liu-{key}.webp');frames.append(ImageOps.fit(im,(900,900),centering=center))
 frames[0].save(ASSET/'hero-still.jpg',quality=95)
 frames[0].save(ASSET/'hero.gif',save_all=True,append_images=frames[1:],duration=3000,loop=0,optimize=False)
 # A RunCN-specific native wordmark, revealed after a mountain-shaped running line.
 font=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',53)
 small=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',15)
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
    if k>=17:ld.text((140,202),'跑过中国 · 记下每一站',font=small,fill=ink,anchor='mm')
    if alpha<1:layer.putalpha(layer.getchannel('A').point(lambda x:int(x*alpha)))
    im=Image.alpha_composite(im.convert('RGBA'),layer).convert('RGB')
   frames.append(im)
  frames[-1].save(ASSET/f'intro-{theme}-still.png')
  frames[0].save(ASSET/f'intro-{theme}.gif',save_all=True,append_images=frames[1:],duration=[70]*23+[1600],loop=0,optimize=False)

def render(d):
 css=re.search(r'<style>(.*?)</style>',style.render(),re.S).group(1)
 css+='''\nmain{padding-left:20px;padding-right:20px}.cover,.intro,.chapter{margin-left:0;margin-right:0}.photo-strip{margin:32px 0 36px}.photo-strip img{display:block;width:100%;height:auto;margin:0}.photo-strip figcaption,figure figcaption{margin:10px 0 0;text-align:center;font-size:12px;line-height:1.8;color:var(--muted)}.brand-intro{display:block;text-align:center;margin:0 auto 14px}.brand-intro img{display:inline-block;width:128px;height:128px}.cover img{display:block;width:100%;height:auto;aspect-ratio:1}.location-poster img{width:100%;height:auto}.source-note{font-size:11px;line-height:1.8;color:var(--muted);margin-top:24px}.source-note a{color:inherit}.chapter-label{color:#b8452e}html[data-theme="dark"] .chapter-label{color:#ffd36e}.byline{line-height:2}.series{letter-spacing:3px}'''
 pfx='/assets/runcn-liupanshui-2026/'
 body=[f'<header class="masthead"><h1>{escape(TITLE)}</h1><p class="byline">贵州六盘水 · 2026年7月19日<br>文字 / Arsenan</p></header>',
 f'<picture class="brand-intro"><source media="(prefers-reduced-motion: reduce)" srcset="{pfx}intro-light-still.png" data-light-src="{pfx}intro-light-still.png" data-dark-src="{pfx}intro-dark-still.png"><img src="{pfx}intro-light.gif" data-light-src="{pfx}intro-light.gif" data-dark-src="{pfx}intro-dark.gif" alt="RunCN 山路片头" width="280" height="280"></picture>',
 f'<figure class="cover"><picture><source media="(prefers-reduced-motion: reduce)" srcset="{pfx}hero-still.jpg"><img src="{pfx}hero.gif" width="900" height="900" alt="六盘水的比赛、草原、桥和奖牌" fetchpriority="high"></picture><figcaption>乌蒙山里跑一个周末 · 照片署名见正文</figcaption></figure>',
 '<div class="down" aria-hidden="true">⌄<br>⌄<br>⌄</div>',f'<section class="intro"><p>{emphasize(d["intro"])}</p></section>',
 '<figure class="photo-strip location-poster"><img src="/assets/runcn-liupanshui-2026/map.png" alt="RunCN 中国地图，山形指引与星标定位贵州六盘水"><img src="/assets/runcn-liupanshui-cover-20261009.jpg" alt="贵州六盘水 · 2026 · RunCN 27"><figcaption>贵州 · 六盘水 · RunCN 第27站<br>封面设计 / Arsenan × AI</figcaption></figure>']
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
   body.append('<figure class="photo-strip">'+''.join(f'<img src="{x["src"]}" srcset="{x["src"].replace("/Liu-","/preview/Liu-")} 1600w" sizes="(max-width:677px) calc(100vw - 40px), 637px" data-copy-src="{x["src"].replace("/Liu-","/preview/Liu-")}" alt="{escape(x["alt"])}" width="{x["width"]}" height="{x["height"]}" loading="lazy" decoding="async" style="display:block;width:100%;height:auto">' for x in group)+'<figcaption>'+'<br>'.join(escape(x['caption']) for x in group)+'</figcaption></figure>')
  i+=1
 for p in d['ending_paragraphs']:body.append('<p class="prose" style="font-size:15px;line-height:1.95;text-align:justify">'+emphasize(p)+'</p>')
 body.append('<footer class="ending"><p class="end-mark">本文完</p><p class="series">RUNCN · 第27站 · 贵州六盘水</p><h2>乌蒙山里，跑一个周末</h2><p class="closing">六盘水位于贵州西部，乌蒙山间，从水城古镇走到高山草甸。</p><p class="credits">文字 / Arsenan<br>摄影 / 见图片署名</p></footer>')
 body.append('<p class="source-note">地方背景参考：<a href="https://www.gzlps.gov.cn/ywdt/jrld/202307/t20230726_81268927.html">六盘水市政府：中国凉都</a> · <a href="https://www.gzlps.gov.cn/zjld/ldwh/sxjs/sxjy/202310/t20231016_82760126.html">三线建设与六盘水市的兴起</a>。比赛与旅行经历依作者原稿。</p>')
 nav='<nav class="copy-tools"><a href="/CN/#runcn-series" style="color:inherit">RunCN 目录</a><button class="theme-choice" data-theme-choice="light" aria-pressed="true" type="button">白底</button><button class="theme-choice" data-theme-choice="dark" aria-pressed="false" type="button">黑底</button><button id="copy-wechat" type="button">一键复制到公众号</button><span id="copy-status" role="status" aria-live="polite"></span></nav>'
 html='<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+escape(TITLE)+'</title><meta name="description" content="从水城古镇、乌蒙大草原、北盘江到海坪火把季，88张照片记录2026六盘水马拉松周末。"><meta property="og:image" content="https://zhennanzhang.com/assets/runcn-liupanshui-cover-20261009.jpg"><style>'+css+'</style></head><body>'+nav+'<main data-edition="runcn-liupanshui">'+'\n'.join(body)+'</main><script src="/assets/runcn-liupanshui-copy.js?v=20261009" defer></script></body></html>'
 for suffix in ['editorial','modern-rail']:(ROOT/f'run50/wechat/{SLUG}-{suffix}.html').write_text(html,encoding='utf-8')
 js=(ROOT/'assets/run50-six-editorial-copy.js').read_text(encoding='utf-8').replace('img.height = 120','img.height = 96')
 js=js.replace("if (tag === 'img' || number || down) {", "if (number) { const p=document.createElement('p'); p.textContent=node.textContent; p.style.cssText='font-family:Arial,sans-serif;font-size:74px;line-height:1;color:' + ink + ';margin:48px 0 14px;font-weight:400;'; return p; }\n      if (tag === 'img' || down) {")
 js=js.replace("node.getAttribute('data-' + theme + '-src') || node.getAttribute('src')", "node.getAttribute('data-' + theme + '-src') || node.getAttribute('data-copy-src') || node.getAttribute('src')")
 (ROOT/'assets/runcn-liupanshui-copy.js').write_text(js,encoding='utf-8')
 print('Rendered',len(d['original_paragraphs']),'source paragraphs,',sum(b['kind']=='figure' for b in blocks),'photos')

if __name__=='__main__':
 import argparse
 ap=argparse.ArgumentParser();ap.add_argument('--assets',action='store_true');ap.add_argument('--import-source',action='store_true');args=ap.parse_args()
 d=prepare() if args.import_source or not DATA.exists() else json.loads(DATA.read_text(encoding='utf-8'))
 if args.assets:assets()
 render(d)
