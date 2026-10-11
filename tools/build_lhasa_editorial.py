"""Build Lhasa RunCN editorial from the author's Vlog narration and 135 selected photos."""
from pathlib import Path
from html import escape
import json,re,shutil
from PIL import Image,ImageOps
import build_wechat_louisville_editorial as style
ROOT=Path(__file__).resolve().parents[1]
ASSET=ROOT/'assets/runcn-lhasa-2026'
SLUG='lhasa-half-marathon'
TITLE='RunCN #第29站｜西藏拉萨半程马拉松｜在日光之城，跑到布达拉宫脚下'
COVER_SRC='/assets/runcn-lhasa-cover-20261011.jpg'
POSTER_SRC='/assets/runcn-lhasa-article-poster-20261011.jpg'
assert COVER_SRC!=POSTER_SRC
KEYS='拉萨 西藏 RunCN 布达拉宫 八廓街 大昭寺 青藏铁路 西宁 格尔木 牛肉包 雪城民宿 田村火锅鸡 藏戏面具 三十五块钱 山东小伙 警察 志愿者 三千六百六十米 二十一公里 高原 半马 氧气 拉萨河 会展中心 九公里 十四公里 十七 十八 十九 三小时多一点 奖牌 月亮 彩色流苏 煲仔饭 西瓜汁'.split()
UNDER=['不是上山，是上宫殿了','找回来了','最喜欢的风景还是下一个公里牌','慢慢往前','都在里面','第三层台阶','也算数','高原的比赛，确实得敬畏','你们下班，我也下班','这一趟','回车上','真牛肉','也有一整段很具体的记忆','先把步子放稳','不急着','舍不得','相机可别再忘了']
def emphasize(text):
 parts=re.split('('+'|'.join(map(re.escape,sorted(set(KEYS+UNDER),key=len,reverse=True)))+')',text)
 return ''.join(('<strong data-cn-tone="'+str(sum(map(ord,t))%4)+'"'+(' data-cn-emphasis="underline"' if t in UNDER else '')+'>'+escape(t)+'</strong>') if i%2 else escape(t) for i,t in enumerate(parts))
def prepare():
 cap=dict(l.split('|',1) for l in (ROOT/'tools/data/lhasa-captions.txt').read_text(encoding='utf-8').splitlines() if l.strip())
 photo={}
 for key,c in cap.items():
  p=ASSET/f'Lhsa-{key}.webp'
  with Image.open(p) as im:w,h=im.size
  photo[key]={'kind':'figure','src':'/assets/runcn-lhasa-2026/'+p.name,'alt':c,'caption':c,'width':w,'height':h,'source_file':f'Lhsa-{key}.jpg'}
 blocks=[];used=[];paras=[]
 for line in (ROOT/'tools/data/lhasa-story.txt').read_text(encoding='utf-8').splitlines():
  if not line.strip():continue
  if line.startswith('# '):
   label,title=line[2:].split('｜',1);blocks.append({'kind':'heading','label':label,'title':title})
  elif line.startswith('@'):
   for key in line[1:].split():blocks.append(photo[key]);used.append(key)
  else:paras.append(line);blocks.append({'kind':'paragraph','html':'<p>'+emphasize(line)+'</p>'})
 sources={p.stem.removeprefix('Lhsa-') for p in ASSET.glob('Lhsa-*.webp')}
 assert len(used)==len(set(used))==135 and set(used)==sources==set(cap),(len(used),sources-set(used),set(used)-sources)
 d={'title':TITLE,'intro':'凌晨从广州出发，在西宁换乘卧铺。先看车窗里的高原，再走进布宫与八廓街；相机失而复得之后，用一场三小时多的半马，把拉萨留在RunCN地图里。','source_photo_count':135,'source_subtitles':'拉萨这一趟 · 45分钟Vlog完整字幕','original_paragraphs':paras,'ending_paragraphs':[],'blocks':blocks}
 (ROOT/'tools/data/lhasa-editorial.json').write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
 return d
def assets():
 for name in ['intro-light.gif','intro-dark.gif','intro-light-still.png','intro-dark-still.png']:
  shutil.copyfile(ROOT/'assets/runcn-chuxiong-2026'/name,ASSET/name)
 frames=[]
 for key,center in [('18-5-0',(.5,.08)),('05-0',(.5,.4)),('09-2',(.5,.3)),('15-7',(.5,.25)),('17-0',(.5,.2)),('19-1',(.5,.2)),('21-0',(.5,.08)),('22-1',(0,.3)),('22-3',(.5,.15))]:
  with Image.open(ASSET/f'Lhsa-{key}.webp') as im:frames.append(ImageOps.fit(im.convert('RGB'),(900,900),centering=center))
 frames[0].save(ASSET/'hero-still.jpg',quality=95)
 frames[0].save(ASSET/'hero-9photos-20261011.gif',save_all=True,append_images=frames[1:],duration=2800,loop=0,optimize=False)

def render(d):
 css=re.search(r'<style>(.*?)</style>',style.render(),re.S).group(1)
 css+='''\nmain{padding-left:20px;padding-right:20px}.cover,.intro,.chapter{margin-left:0;margin-right:0}.photo-strip{margin:32px 0 36px}.photo-strip img{display:block;width:100%;height:auto;margin:0}.photo-strip figcaption,figure figcaption{margin:10px 0 0;text-align:center;font-size:12px;line-height:1.8;color:var(--muted)}.brand-intro{display:block;text-align:center;margin:0 auto 14px}.brand-intro img{display:inline-block;width:128px;height:128px}.cover img{display:block;width:100%;height:auto;aspect-ratio:1}.location-poster img{width:100%;height:auto}.location-poster img:first-child{width:97.47634%;margin-left:auto;margin-right:auto}.source-note{font-size:11px;line-height:1.8;color:var(--muted);margin-top:24px}.source-note a{color:inherit}.chapter-label{color:#b8452e}html[data-theme="dark"] .chapter-label{color:#ffd36e}.byline{line-height:2}.series{letter-spacing:3px}'''
 pfx='/assets/runcn-lhasa-2026/'
 body=[f'<header class="masthead"><h1>{escape(TITLE)}</h1><p class="byline">西藏拉萨 · 2026年8月23日<br>文字 / Arsenan</p></header>',
 f'<picture class="brand-intro"><source media="(prefers-reduced-motion: reduce)" srcset="{pfx}intro-light-still.png" data-light-src="{pfx}intro-light-still.png" data-dark-src="{pfx}intro-dark-still.png"><img src="{pfx}intro-light.gif" data-light-src="{pfx}intro-light.gif" data-dark-src="{pfx}intro-dark.gif" alt="RunCN 山路片头" width="280" height="280"></picture>',
 f'<figure class="cover"><picture><source media="(prefers-reduced-motion: reduce)" srcset="{pfx}hero-still.jpg"><img src="{pfx}hero-9photos-20261011.gif" width="900" height="900" alt="进藏列车、布达拉宫、拉萨半马与藏戏奖牌" fetchpriority="high"></picture><figcaption>坐着火车进藏，跑到布达拉宫脚下</figcaption></figure>',
 '<div class="down" aria-hidden="true">⌄<br>⌄<br>⌄</div>',f'<section class="intro"><p>{emphasize(d["intro"])}</p></section>',
 f'<figure class="photo-strip location-poster"><img src="/assets/runcn-lhasa-2026/map-tibet-lhasa.jpg" alt="RunCN 中国地图，藏戏面具与星标定位西藏拉萨"><img src="{POSTER_SRC}" alt="西藏拉萨 · 2026 · RunCN 29"><figcaption>西藏 · 拉萨 · RunCN 第29站<br>封面设计 / Arsenan × AI</figcaption></figure>']
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
   body.append('<figure class="photo-strip">'+''.join(f'<img src="{x["src"]}" srcset="{x["src"].replace("/Lhsa-","/preview/Lhsa-")} 1600w" sizes="(max-width:677px) calc(100vw - 40px), 637px" data-copy-src="{x["src"].replace("/Lhsa-","/preview/Lhsa-")}" alt="{escape(x["alt"])}" width="{x["width"]}" height="{x["height"]}" loading="lazy" decoding="async" style="display:block;width:100%;height:auto">' for x in group)+'<figcaption>'+'<br>'.join(escape(x['caption']) for x in group)+'</figcaption></figure>')
  i+=1
 for p in d['ending_paragraphs']:body.append('<p class="prose" style="font-size:15px;line-height:1.95;text-align:justify">'+emphasize(p)+'</p>')
 body.append('<footer class="ending"><p class="end-mark">本文完</p><p class="series">RUNCN · 第29站 · 西藏拉萨</p><h2>在日光之城，跑到布达拉宫脚下</h2><p class="closing">从车窗到赛道，从失而复得的相机到藏戏奖牌，把拉萨放进RunCN地图里。</p><p class="credits">文字 / Arsenan<br>摄影 / 见图片署名</p></footer>')
 body.append('<p class="source-note">背景资料：<a href="https://whc.unesco.org/zh/list/707">布达拉宫历史建筑群 · UNESCO</a> · <a href="https://www.runninginchina.org/event/default/414.html?action=view">拉萨半程马拉松规程与路线</a>。旅行与比赛经历根据作者Vlog中的口述整理；比赛年份由作者确认为2026年。</p>')
 nav='<nav class="copy-tools"><a href="/CN/#runcn-series" style="color:inherit">RunCN 目录</a><button class="theme-choice" data-theme-choice="light" aria-pressed="true" type="button">白底</button><button class="theme-choice" data-theme-choice="dark" aria-pressed="false" type="button">黑底</button><button id="copy-wechat" type="button">一键复制到公众号</button><span id="copy-status" role="status" aria-live="polite"></span></nav>'
 html='<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+escape(TITLE)+'</title><meta name="description" content="在日光之城，跑到布达拉宫脚下。135张照片，记录卧铺进藏、布宫夜色、相机失而复得和高原半马。"><meta property="og:image" content="https://zhennanzhang.com'+COVER_SRC+'"><style>'+css+'</style></head><body>'+nav+'<main data-edition="runcn-lhasa">'+'\n'.join(body)+'</main><script src="/assets/runcn-lhasa-copy.js?v=20261011-align" defer></script></body></html>'
 for suffix in ['editorial','modern-rail']:(ROOT/f'run50/wechat/{SLUG}-{suffix}.html').write_text(html,encoding='utf-8')
 js=(ROOT/'assets/run50-six-editorial-copy.js').read_text(encoding='utf-8').replace('img.height = 120','img.height = 96')
 js=js.replace("if (tag === 'img' || number || down) {", "if (number) { const p=document.createElement('p'); p.textContent=node.textContent; p.style.cssText='font-family:Arial,sans-serif;font-size:74px;line-height:1;color:' + ink + ';margin:48px 0 14px;font-weight:400;'; return p; }\n      if (tag === 'img' || down) {")
 js=js.replace("node.getAttribute('data-' + theme + '-src') || node.getAttribute('src')", "node.getAttribute('data-' + theme + '-src') || node.getAttribute('data-copy-src') || node.getAttribute('src')")
 js=js.replace("        return img;", "        if (node.matches('.location-poster > img:first-child')) img.style.cssText='display:block;width:97.47634%;max-width:97.47634%;height:auto;margin:0 auto;border:0;';\n        return img;")
 (ROOT/'assets/runcn-lhasa-copy.js').write_text(js,encoding='utf-8')
 print('Rendered',len(d['original_paragraphs']),'source paragraphs,',sum(b['kind']=='figure' for b in blocks),'photos')

if __name__=='__main__':
 import sys
 d=prepare()
 if '--assets' in sys.argv:assets()
 render(d)
