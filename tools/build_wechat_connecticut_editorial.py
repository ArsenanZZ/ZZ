from pathlib import Path
import json,re
from html import escape
import build_wechat_michigan_editorial as template
ROOT=Path(__file__).resolve().parents[1]
SLUG='connecticut-simsbury-marathon'
def render():
 d=json.loads((ROOT/'tools/data/connecticut-editorial.json').read_text(encoding='utf-8'));css=re.search(r'<style>(.*?)</style>',template.render(),re.S).group(1)
 css+='\nmain{padding-left:20px;padding-right:20px}.cover,.intro,.chapter{margin-left:0;margin-right:0}'
 body=[f'<header class="masthead"><h1>{escape(d["title"])}</h1><p class="byline">文字 / Arsenan</p></header>','<picture class="brand-intro"><source media="(prefers-reduced-motion: reduce)" srcset="/assets/run50-robot-intro-compact-still.png"><img src="/assets/run50-robot-intro-compact.gif" alt="Run50 机器人片头" width="224" height="300"></picture>','<figure class="cover"><picture><source media="(prefers-reduced-motion: reduce)" srcset="/assets/connecticut-editorial/CT-50.jpg"><img src="/assets/connecticut-editorial/hero.gif?v=square-medal-2" alt="康涅狄格：跑步、合影、小鸭子与奖牌" width="900" height="900"></picture><figcaption class="hero-credit">人物照 / Siqi · 合影与奖牌署名见正文</figcaption></figure>','<div class="down" aria-hidden="true">⌄<br>⌄<br>⌄</div><section class="intro"><p>从尼亚加拉到新英格兰，凌晨五点穿着7号球衣起跑。十二圈绿道，一排小鸭子，六连赛的第一站。</p></section>','<figure class="photo-strip map-poster" style="margin:32px 0 36px"><img src="/assets/connecticut-editorial/map.jpg?v=oak-hand-2" alt="第32州康涅狄格，星标辛斯伯里" style="display:block;width:100%;height:auto;margin:0"><img src="/assets/connecticut-editorial/poster.jpg" alt="2026 康涅狄格 辛斯伯里 RUN50 32" style="display:block;width:100%;height:auto;margin:0"><figcaption style="margin:10px 0 0;text-align:center;font-size:12px;line-height:1.8;color:#888">第32州 · 康涅狄格，星标为辛斯伯里｜制图 / Arsenan<br>2026 · Simsbury · New England Series Day 1</figcaption></figure>']
 n=0
 for b in d['blocks']:
  if b['kind']=='heading':
   n+=1;body.append(f'<header class="chapter"><span class="chapter-number">{n:02}</span><p class="chapter-label">{escape(b["label"])}</p><h2>{escape(b["title"])}</h2></header>')
  elif b['kind']=='paragraph':body.append('<p class="prose" style="margin:0 0 22px;font-size:15px;line-height:1.95;letter-spacing:.5px;text-align:justify">'+b['html']+'</p>')
  else:body.append('<figure style="margin:32px 0 36px">'+''.join(f'<img src="{escape(im["src"])}" alt="{escape(im["alt"])}" loading="lazy" style="display:block;width:100%;height:auto;margin:0">' for im in b['images'])+'<figcaption style="margin:10px 0 0;text-align:center;font-size:12px;line-height:1.8;color:#888">'+escape(b['caption'])+'</figcaption></figure>')
 body.append('<footer class="ending"><p class="end-mark">— 本文完 —</p><p class="series">RUN50 · 第32州</p><h2 style="margin:16px 0 0;text-align:center">康涅狄格，点亮</h2><p class="closing" style="margin:0;padding:24px 0 0;text-align:center;font-size:13px;line-height:1.9">新英格兰南部的小州，绿道串起小镇。</p><p class="credits">文字 / Arsenan<br>摄影 / Arsenan、Siqi</p></footer>')
 nav='<nav class="copy-tools"><a href="/CN/" style="color:inherit">全部中文文章</a><a href="/run50/wechat-new/connecticut-simsbury-marathon-d-rail-original.html" style="color:inherit">原版赛道风</a><button data-theme-choice="light" aria-pressed="true" type="button">白底</button><button data-theme-choice="dark" aria-pressed="false" type="button">黑底</button><button id="copy-wechat" type="button">一键复制到公众号</button><span id="copy-status" role="status" aria-live="polite"></span></nav>'
 return '<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+escape(d['title'])+'</title><style>'+css+'</style></head><body>'+nav+'<main data-edition="connecticut-editorial">'+'\n'.join(body)+'</main><script src="/assets/connecticut-wechat-copy.js?v=20261003" defer></script></body></html>'
if __name__=='__main__':
 text=render()
 for name in ['run50/wechat/connecticut-simsbury-marathon-editorial.html','run50/wechat-new/connecticut-simsbury-marathon-d-rail.html']:(ROOT/name).write_text(text,encoding='utf-8')
