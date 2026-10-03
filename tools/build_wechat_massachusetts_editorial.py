from pathlib import Path
import json,re
from html import escape
import build_wechat_michigan_editorial as template
ROOT=Path(__file__).resolve().parents[1]
SLUG='massachusetts-holyoke-marathon'
def render():
 d=json.loads((ROOT/'tools/data/massachusetts-editorial.json').read_text(encoding='utf-8'));css=re.search(r'<style>(.*?)</style>',template.render(),re.S).group(1)
 css+='\nmain{padding-left:20px;padding-right:20px}.cover,.intro,.chapter{margin-left:0;margin-right:0}'
 body=[f'<header class="masthead"><h1>{escape(d["title"])}</h1><p class="byline">文字 / Arsenan</p></header>','<picture class="brand-intro"><source media="(prefers-reduced-motion: reduce)" srcset="/assets/run50-robot-intro-compact-still.png"><img src="/assets/run50-robot-intro-compact.gif" alt="Run50 机器人片头" width="224" height="300"></picture>','<figure class="cover"><picture><source media="(prefers-reduced-motion: reduce)" srcset="/assets/massachusetts-editorial/hero-still.png"><img src="/assets/massachusetts-editorial/hero.gif?v=ma-medal-square-2" alt="马萨诸塞：跑步、合影与加油木牌" width="900" height="900"></picture><figcaption class="hero-credit">赛道人物照 / Siqi · 其他照片署名见正文</figcaption></figure>','<div class="down" aria-hidden="true">⌄<br>⌄<br>⌄</div><section class="intro"><p>第三天在霍利奥克绕水库跑完第34州，随后去佛蒙特跑5K、逛廊桥，住进树林里的小木屋。</p></section>','<figure class="photo-strip map-poster" style="margin:32px 0 36px"><img src="/assets/massachusetts-editorial/map.jpg?v=paper-quill-1" alt="第34州马萨诸塞，星标霍利奥克" style="display:block;width:100%;height:auto;margin:0"><img src="/assets/massachusetts-editorial/poster.jpg" alt="2026 马萨诸塞 霍利奥克 RUN50 34" style="display:block;width:100%;height:auto;margin:0"><figcaption style="margin:10px 0 0;text-align:center;font-size:12px;line-height:1.8;color:#888">第34州 · 马萨诸塞，星标为霍利奥克｜制图 / Arsenan<br>2026 · Holyoke · New England Series Day 3</figcaption></figure>']
 for block in d["blocks"]:
  if block["kind"] == "figure":
   assert all(Path(im["src"]).stem in d["allowed_photo_stems"] for im in block["images"]), "Only curated folder photos are allowed"
 n=0
 for b in d['blocks']:
  if b['kind']=='heading':
   n+=1;body.append(f'<header class="chapter"><span class="chapter-number">{n:02}</span><p class="chapter-label">{escape(b["label"])}</p><h2>{escape(b["title"])}</h2></header>')
  elif b['kind']=='paragraph':body.append('<p class="prose" style="margin:0 0 22px;font-size:15px;line-height:1.95;letter-spacing:.5px;text-align:justify">'+b['html']+'</p>')
  else:body.append('<figure style="margin:32px 0 36px">'+''.join(f'<img src="{escape(im["src"])}" alt="{escape(im["alt"])}" loading="lazy" style="display:block;width:100%;height:auto;margin:0">' for im in b['images'])+'<figcaption style="margin:10px 0 0;text-align:center;font-size:12px;line-height:1.8;color:#888">'+escape(b['caption'])+'</figcaption></figure>')
 body.append('<footer class="ending"><p class="end-mark">— 本文完 —</p><p class="series">RUN50 · 第34州</p><h2 style="margin:16px 0 0;text-align:center">马萨诸塞，点亮</h2><p class="closing" style="margin:0;padding:24px 0 0;text-align:center;font-size:13px;line-height:1.9">新英格兰的历史重地，霍利奥克曾以造纸闻名。</p><p class="credits">文字 / Arsenan<br>摄影 / Arsenan、Siqi</p></footer>')
 nav='<nav class="copy-tools"><a href="/CN/" style="color:inherit">全部中文文章</a><a href="/run50/wechat-new/massachusetts-holyoke-marathon-d-rail-original.html" style="color:inherit">原版赛道风</a><button data-theme-choice="light" aria-pressed="true" type="button">白底</button><button data-theme-choice="dark" aria-pressed="false" type="button">黑底</button><button id="copy-wechat" type="button">一键复制到公众号</button><span id="copy-status" role="status" aria-live="polite"></span></nav>'
 return '<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+escape(d['title'])+'</title><style>'+css+'</style></head><body>'+nav+'<main data-edition="massachusetts-editorial">'+'\n'.join(body)+'</main><script src="/assets/massachusetts-wechat-copy.js?v=20261003" defer></script></body></html>'
if __name__=='__main__':
 text=render()
 for name in ['run50/wechat/massachusetts-holyoke-marathon-editorial.html','run50/wechat-new/massachusetts-holyoke-marathon-d-rail.html']:(ROOT/name).write_text(text,encoding='utf-8')
