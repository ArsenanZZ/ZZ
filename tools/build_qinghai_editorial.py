"""Publish the Qinghai/Xining story from the author's Vlog and 123 selected photographs."""
from pathlib import Path
from html import escape
import json,re,shutil
from PIL import Image,ImageOps
import build_wechat_louisville_editorial as style
ROOT=Path(__file__).resolve().parents[1]
ASSET=ROOT/'assets/runcn-qinghai-2026'
SLUG='qinghai-xining-marathon'
TITLE='RunCN #第30站｜青海西宁高原马拉松｜从天空之镜到夏都，踩着盐跑完一场全马'
COVER_SRC='/assets/runcn-qinghai-cover-20261011.jpg'
POSTER_SRC='/assets/runcn-qinghai-article-poster-20261011.jpg'
assert COVER_SRC!=POSTER_SRC
OFFICIAL_PHOTOS=set('009-3 009-4 009-6 009-7 009-8-1 009-8-7-1 009-8-7-2 009-8-8-1 009-8-8-2 009-9-1'.split())
KEYS='青海 西宁 RunCN 夏都 日月山 青海湖 茶卡盐湖 天空之镜 凤凰台 南山公园 莫家街 经幡 牦牛 羊群 小青稞 2261米 2419 3059米 3196米 高原 四十二公里 盐水 小火车 二十公里 二十五公里 三十公里 四十公里 四小时二十左右 路易斯维尔大学 哈尔滨 湟水河 三点半 奖牌 酸奶'.split()
UNDER=['踩着盐跑','跑鞋都先去旅游了','太热情了','来都来了','小哈尔滨','假装跑一跑','挺穿越的','四小时二十左右','不需要为了镜头硬顶着','飞机','这个时间，比大中午舒服多了','机场那一程可没有跑完','旅行还在继续','一站一站','跑一段，调整一下']
def emphasize(text):
 parts=re.split('('+'|'.join(map(re.escape,sorted(set(KEYS+UNDER),key=len,reverse=True)))+')',text)
 return ''.join(('<strong data-cn-tone="'+str(sum(map(ord,t))%4)+'"'+(' data-cn-emphasis="underline"' if t in UNDER else '')+'>'+escape(t)+'</strong>') if i%2 else escape(t) for i,t in enumerate(parts))
def prepare():
 cap=dict(l.split('|',1) for l in (ROOT/'tools/data/qinghai-captions.txt').read_text(encoding='utf-8').splitlines() if l.strip())
 meta={v['key']:v for v in json.loads((ROOT/'tools/data/qinghai-photos.json').read_text(encoding='utf-8'))}
 photo={}
 for key,c in cap.items():
  p=ASSET/f'QH-{key}.webp'
  with Image.open(p) as im:w,h=im.size
  credit='官方摄影' if key in OFFICIAL_PHOTOS else 'Arsenan'
  if key=='009-8-1':credit='gxh（官方摄影）'
  photo[key]={'kind':'figure','src':'/assets/runcn-qinghai-2026/'+p.name,'alt':c,'caption':c+' · 摄影 / '+credit,'width':w,'height':h,'source_file':meta[key]['file']}
 blocks=[];used=[];paras=[]
 for line in (ROOT/'tools/data/qinghai-story.txt').read_text(encoding='utf-8').splitlines():
  if not line.strip():continue
  if line.startswith('# '):
   label,title=line[2:].split('｜',1);blocks.append({'kind':'heading','label':label,'title':title})
  elif line.startswith('@'):
   for key in line[1:].split():blocks.append(photo[key]);used.append(key)
  else:paras.append(line);blocks.append({'kind':'paragraph','html':'<p>'+emphasize(line)+'</p>'})
 sources={p.stem.removeprefix('QH-') for p in ASSET.glob('QH-*.webp')}
 assert len(used)==len(set(used))==123 and set(used)==sources==set(cap)
 milestones={'009-6-alt':5,'009-8':8,'009-8-2':12,'009-8-4':20,'009-8-5':30,'009-8-8':36,'009-9':40,'009-9-1':42}
 progress=[milestones[k] for k in used if k in milestones]
 assert progress==sorted(progress),f'Race photos out of kilometer order: {progress}'
 d={'title':TITLE,'intro':'从西宁的晚霞和夜市，到日月山的经幡、青海湖和茶卡盐湖。鞋里进了盐水，第二天照样去跑全马；跑完，绿箱子和下午三点半的飞机还在等着。','source_photo_count':123,'source_subtitles':'青海这一趟 · 28分钟Vlog完整字幕','original_paragraphs':paras,'ending_paragraphs':[],'blocks':blocks}
 (ROOT/'tools/data/qinghai-editorial.json').write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
 return d
def assets():
 for name in ['intro-light.gif','intro-dark.gif','intro-light-still.png','intro-dark-still.png']:
  shutil.copyfile(ROOT/'assets/runcn-chuxiong-2026'/name,ASSET/name)
 frames=[]
 for key,center in [('001-5',(0,.3)),('002-5',(.5,.3)),('003-2',(.6,.15)),('003-6-5',(.25,.5)),('007-5-1',(.5,.3)),('007-5-9',(.5,.5)),('009-8-4',(.5,.3)),('009-9-1',(.5,.1)),('010-2',(.5,.5))]:
  with Image.open(ASSET/f'QH-{key}.webp') as im:frames.append(ImageOps.fit(im.convert('RGB'),(900,900),centering=center))
 frames[0].save(ASSET/'hero-still.jpg',quality=95)
 frames[0].save(ASSET/'hero-9photos-20261011.gif',save_all=True,append_images=frames[1:],duration=2800,loop=0,optimize=False)

def render(d):
 css=re.search(r'<style>(.*?)</style>',style.render(),re.S).group(1)
 css+='''\nmain{padding-left:20px;padding-right:20px}.cover,.intro,.chapter{margin-left:0;margin-right:0}.photo-strip{margin:32px 0 36px}.photo-strip img{display:block;width:100%;height:auto;margin:0}.photo-strip figcaption,figure figcaption{margin:10px 0 0;text-align:center;font-size:12px;line-height:1.8;color:var(--muted)}.brand-intro{display:block;text-align:center;margin:0 auto 14px}.brand-intro img{display:inline-block;width:128px;height:128px}.cover img{display:block;width:100%;height:auto;aspect-ratio:1}.location-poster img{width:100%;height:auto}.location-poster img:first-child{width:100%;max-width:100%;box-sizing:border-box;padding:0;background:#f3efdf;margin:0}.source-note{font-size:11px;line-height:1.8;color:var(--muted);margin-top:24px}.source-note a{color:inherit}.chapter-label{color:#b8452e}html[data-theme="dark"] .chapter-label{color:#ffd36e}.byline{line-height:2}.series{letter-spacing:3px}'''
 pfx='/assets/runcn-qinghai-2026/'
 body=[f'<header class="masthead"><h1>{escape(TITLE)}</h1><p class="byline">青海西宁 · 2026年9月6日<br>文字 / Arsenan</p></header>',
 f'<picture class="brand-intro"><source media="(prefers-reduced-motion: reduce)" srcset="{pfx}intro-light-still.png" data-light-src="{pfx}intro-light-still.png" data-dark-src="{pfx}intro-dark-still.png"><img src="{pfx}intro-light.gif" data-light-src="{pfx}intro-light.gif" data-dark-src="{pfx}intro-dark.gif" alt="RunCN 山路片头" width="280" height="280"></picture>',
 f'<figure class="cover"><picture><source media="(prefers-reduced-motion: reduce)" srcset="{pfx}hero-still.jpg"><img src="{pfx}hero-9photos-20261011.gif" width="900" height="900" alt="青海湖、茶卡盐湖、西宁夜色与高原全马" fetchpriority="high"></picture><figcaption>从天空之镜到夏都，踩着盐跑完一场全马<br>摄影 / Arsenan、官方摄影</figcaption></figure>',
 '<div class="down" aria-hidden="true">⌄<br>⌄<br>⌄</div>',f'<section class="intro"><p>{emphasize(d["intro"])}</p></section>',
 f'<figure class="photo-strip location-poster"><img src="/assets/runcn-article-maps-20261022/qinghai-xining-marathon.jpg" alt="RunCN 中国地图，盐湖小火车与星标定位青海西宁"><img src="{POSTER_SRC}" alt="青海西宁 · 2026 · RunCN 30"><figcaption>青海 · 西宁 · RunCN 第30站<br>封面设计 / Arsenan × AI</figcaption></figure>']
 blocks=d['blocks'];i=0;n=0
 while i<len(blocks):
  b=blocks[i]
  if b['kind']=='heading':
   n+=1;body.append(f'<header class="chapter"><span class="chapter-number">{n:02}</span><p class="chapter-label">{b["label"]}</p><h2>{escape(b["title"])}</h2></header>')
  elif b['kind']=='paragraph':body.append(b['html'].replace('<p>','<p class="prose" style="margin:0 0 22px;font-size:15px;line-height:1.95;letter-spacing:.5px;text-align:justify">'))
  else:
   group=[b]
   while i+1<len(blocks) and len(group)<3:
    nxt=blocks[i+1]
    if nxt['kind']!='figure':break
    group.append(nxt);i+=1
   body.append('<figure class="photo-strip">'+''.join(f'<img src="{x["src"]}" srcset="{x["src"].replace("/QH-","/preview/QH-")} 1600w" sizes="(max-width:677px) calc(100vw - 40px), 637px" data-copy-src="{x["src"].replace("/QH-","/preview/QH-")}" alt="{escape(x["alt"])}" width="{x["width"]}" height="{x["height"]}" loading="lazy" decoding="async" style="display:block;width:100%;height:auto">' for x in group)+'<figcaption>'+'<br>'.join(escape(x['caption']) for x in group)+'</figcaption></figure>')
  i+=1
 for p in d['ending_paragraphs']:body.append('<p class="prose" style="font-size:15px;line-height:1.95;text-align:justify">'+emphasize(p)+'</p>')
 body.append('<footer class="ending"><p class="end-mark">本文完</p><p class="series">RUNCN · 第30站 · 青海西宁</p><h2>从天空之镜到夏都，踩着盐跑完一场全马</h2><p class="closing">经幡、盐湖、四十二公里，再赶上飞机。把青海这一趟放进RunCN地图里。</p><p class="credits">文字 / Arsenan<br>摄影 / Arsenan、官方摄影</p></footer>')
 body.append('<p class="source-note">背景资料：<a href="https://www.qhnews.com/newscenter/system/2026/09/08/030607559.shtml">2026大美青海高原马拉松</a> · <a href="https://sjfw.mct.gov.cn/site/dataservice/culdetails?curId=10&amp;id=35111">青海湖 · 文化和旅游部</a> · <a href="https://www.chakasl.com/wap/index">茶卡盐湖景区</a> · <a href="https://zwgk.mct.gov.cn/zfxxgkml/scgl/202012/W020200728458297782567.pdf">日月山背景</a> · <a href="https://www.hainanzhou.gov.cn/lnb/xwzx1/hnyw1__xwzx/hnyw/content_1013649156">青海特色面点</a>。旅行与比赛经历依据作者28分钟Vlog口述及选图整理；成绩按视频中的个人记录表述。</p>')
 nav='<nav class="copy-tools"><a href="/CN/#runcn-series" style="color:inherit">RunCN 目录</a><button class="theme-choice" data-theme-choice="light" aria-pressed="true" type="button">白底</button><button class="theme-choice" data-theme-choice="dark" aria-pressed="false" type="button">黑底</button><button id="copy-wechat" type="button">一键复制到公众号</button><span id="copy-status" role="status" aria-live="polite"></span></nav>'
 html='<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+escape(TITLE)+'</title><meta name="description" content="从天空之镜到夏都，踩着盐跑完一场全马。123张照片，记录西宁夜色、日月山、青海湖、茶卡盐湖和跑完赶飞机的高原全马。"><meta property="og:image" content="https://zhennanzhang.com'+COVER_SRC+'"><style>'+css+'</style></head><body>'+nav+'<main data-edition="runcn-qinghai">'+'\n'.join(body)+'</main><script src="/assets/runcn-qinghai-copy.js?v=20261022-text-numbers" defer></script></body></html>'
 for suffix in ['editorial','modern-rail']:(ROOT/f'run50/wechat/{SLUG}-{suffix}.html').write_text(html,encoding='utf-8')
 js=(ROOT/'assets/run50-six-editorial-copy.js').read_text(encoding='utf-8').replace('img.height = 120','img.height = 96')
 js=js.replace("if (tag === 'img' || number || down) {", "if (number) { const p=document.createElement('p'); p.textContent=node.textContent; p.style.cssText='font-family:Arial,sans-serif;font-size:74px;line-height:1;color:' + ink + ';margin:48px 0 14px;font-weight:400;'; return p; }\n      if (tag === 'img' || down) {")
 js=js.replace("node.getAttribute('data-' + theme + '-src') || node.getAttribute('src')", "node.getAttribute('data-' + theme + '-src') || node.getAttribute('data-copy-src') || node.getAttribute('src')")
 js=js.replace("        return img;", "        if (node.matches('.location-poster > img:first-child')) img.style.cssText='display:block;width:100%;max-width:100%;height:auto;box-sizing:border-box;padding:0;background:#f3efdf;margin:0;border:0;';\n        return img;")
 (ROOT/'assets/runcn-qinghai-copy.js').write_text(js,encoding='utf-8')
 print('Rendered',len(d['original_paragraphs']),'source paragraphs,',sum(b['kind']=='figure' for b in blocks),'photos')


if __name__=='__main__':
 import sys
 d=prepare()
 if '--assets' in sys.argv:assets()
 render(d)
