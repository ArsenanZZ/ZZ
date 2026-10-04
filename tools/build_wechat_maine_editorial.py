from pathlib import Path
import json,re
from html import escape
import build_wechat_michigan_editorial as template
ROOT=Path(__file__).resolve().parents[1]
SLUG='maine-sanford-marathon'
def render():
 d=json.loads((ROOT/'tools/data/maine-editorial.json').read_text(encoding='utf-8'));css=re.search(r'<style>(.*?)</style>',template.render(),re.S).group(1)
 css+='\nmain{padding-left:20px;padding-right:20px}.cover,.intro,.chapter{margin-left:0;margin-right:0}'
 body=[f'<header class="masthead"><h1>{escape(d["title"])}</h1><p class="byline">文字 / Arsenan</p></header>','<picture class="brand-intro"><source media="(prefers-reduced-motion: reduce)" srcset="/assets/run50-robot-intro-compact-still.png"><img src="/assets/run50-robot-intro-compact.gif" alt="Run50 机器人片头" width="224" height="300"></picture>','<figure class="cover"><picture><source media="(prefers-reduced-motion: reduce)" srcset="/assets/maine-editorial/hero-still.png"><img src="/assets/maine-editorial/hero.gif?v=me-selected-5" alt="缅因：跑步、合影与系列赛奖牌" width="900" height="900"></picture><figcaption class="hero-credit">摄影署名见正文</figcaption></figure>','<div class="down" aria-hidden="true">⌄<br>⌄<br>⌄</div><section class="intro"><p>第五天在新罕布什尔跑5K，第六天到缅因完成全马。六天四场全马、两场5K，新英格兰之行收官。</p></section>','<figure class="photo-strip map-poster" style="margin:32px 0 36px"><img src="/assets/maine-editorial/map.jpg?v=pine-pointer-2" alt="第35州缅因，星标桑福德" style="display:block;width:100%;height:auto;margin:0"><img src="/assets/maine-editorial/poster.jpg" alt="2026 缅因 桑福德 RUN50 35" style="display:block;width:100%;height:auto;margin:0"><figcaption style="margin:10px 0 0;text-align:center;font-size:12px;line-height:1.8;color:#888">第35州 · 缅因，星标为桑福德｜制图 / Arsenan<br>2026 · Sanford · New England Series Day 6</figcaption></figure>']
 for block in d["blocks"]:
  if block["kind"] == "figure":
   assert all(Path(im["src"]).stem in d["allowed_photo_stems"] for im in block["images"]), "Only curated folder photos are allowed"
 n=0
 for b in d['blocks']:
  if b['kind']=='heading':
   n+=1;body.append(f'<header class="chapter"><span class="chapter-number">{n:02}</span><p class="chapter-label">{escape(b["label"])}</p><h2>{escape(b["title"])}</h2></header>')
  elif b['kind']=='paragraph':body.append('<p class="prose" style="margin:0 0 22px;font-size:15px;line-height:1.95;letter-spacing:.5px;text-align:justify">'+b['html']+'</p>')
  else:body.append('<figure style="margin:32px 0 36px">'+''.join(f'<img src="{escape(im["src"])}" alt="{escape(im["alt"])}" loading="lazy" style="display:block;width:100%;height:auto;margin:0">' for im in b['images'])+'<figcaption style="margin:10px 0 0;text-align:center;font-size:12px;line-height:1.8;color:#888">'+escape(b['caption'])+'</figcaption></figure>')
 body.append('<footer class="ending"><p class="end-mark">— 本文完 —</p><p class="series">RUN50 · 第35州</p><h2 style="margin:16px 0 0;text-align:center">缅因，点亮</h2><p class="closing" style="margin:0;padding:24px 0 0;text-align:center;font-size:13px;line-height:1.9">美国东北角的松树之州，以森林和海岸闻名。</p><p class="credits">文字 / Arsenan<br>摄影 / Arsenan、Siqi</p></footer>')
 nav='<nav class="copy-tools"><a href="/CN/" style="color:inherit">全部中文文章</a><a href="/run50/wechat-new/maine-sanford-marathon-d-rail-original.html" style="color:inherit">原版赛道风</a><button data-theme-choice="light" aria-pressed="true" type="button">白底</button><button data-theme-choice="dark" aria-pressed="false" type="button">黑底</button><button id="copy-wechat" type="button">一键复制到公众号</button><span id="copy-status" role="status" aria-live="polite"></span></nav>'
 return '<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+escape(d['title'])+'</title><style>'+css+'</style></head><body>'+nav+'<main data-edition="maine-editorial">'+'\n'.join(body)+'</main><script src="/assets/maine-wechat-copy.js?v=20261003" defer></script></body></html>'
if __name__=='__main__':
 text=render()
 for name in ['run50/wechat/maine-sanford-marathon-editorial.html','run50/wechat-new/maine-sanford-marathon-d-rail.html']:(ROOT/name).write_text(text,encoding='utf-8')
