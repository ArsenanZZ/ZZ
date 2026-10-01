"""Render the Omaha #36 story from source-grounded editorial blocks."""
from pathlib import Path
from html import escape
import json,re
import build_wechat_michigan_editorial as template
ROOT=Path(__file__).resolve().parents[1]
def emphasize(text):
 text=escape(text)
 for phrase in ['三分钟，三公里','第36州，完成','下午五点五十七','四十五公里','我走一跑二','我的摄影师呢','表上已经三十一点五公里','四小时三十分','Bob Kerrey步行桥','再晚五分钟','2026年9月27日']:
  text=text.replace(phrase,'<strong>'+phrase+'</strong>')
 return text

def render():
 data=json.loads((ROOT/'tools/data/omaha-wechat-editorial.json').read_text(encoding='utf-8'))
 css=re.search(r'<style>(.*?)</style>',template.render(),re.S).group(1)
 css+='\nmain{padding-left:20px;padding-right:20px}.cover,.intro,.chapter{margin-left:0;margin-right:0}.photo-pair{display:grid;grid-template-columns:1fr 1fr;gap:6px;align-items:start}.photo-pair img{width:100%;height:auto}.source-note{font-size:12px;line-height:1.8;color:#888} .source-note a{color:inherit}'
 title=escape(data['title']);body=[f'<header class="masthead"><h1>{title}</h1><p class="byline">文字 / Arsenan</p></header>', '<picture class="brand-intro"><source media="(prefers-reduced-motion: reduce)" srcset="../../assets/run50-robot-intro-compact-still.png"><img src="../../assets/run50-robot-intro-compact.gif" alt="Run50 机器人片头" width="224" height="300"></picture>', '<figure class="cover"><picture><source media="(prefers-reduced-motion: reduce)" srcset="../../assets/omaha-2026/P195.jpg"><img src="../../assets/omaha-2026/hero.gif" alt="奥马哈：完赛、两人合影、奖牌与跨河大桥" width="900" height="820"></picture><figcaption class="hero-credit">完赛照 / Siqi · 合影与奖牌署名见正文</figcaption></figure>', '<div class="down" aria-hidden="true">⌄<br>⌄<br>⌄</div><section class="intro"><p>周末一路向西，赶在领物结束前抵达奥马哈。Siqi跑半马，我跑完全马加上绕错的三公里，再一起开车回家。</p></section>']
 body.append('<figure class="photo-strip map-poster" style="margin:32px 0 36px"><img src="../../assets/omaha-2026/map.jpg" alt="Run50第36州，内布拉斯加；星标奥马哈" style="display:block;width:100%;height:auto;margin:0"><img src="../../assets/omaha-2026/cover-cn.jpg" alt="2026 奥马哈 · RUN50 36 珐琅牌封面" style="display:block;width:100%;height:auto;margin:0"><figcaption style="margin:10px 0 0;text-align:center;font-size:12px;line-height:1.75;color:#888">第36州 · 内布拉斯加，星标为奥马哈｜制图 / Arsenan<br>2026 · 奥马哈 · Omaha Marathon</figcaption></figure>')
 n=0
 for b in data['blocks']:
  if b['kind']=='heading':
   n+=1;body.append(f'<header class="chapter"><span class="chapter-number">{n:02}</span><p class="chapter-label">{escape(b["label"])}</p><h2>{escape(b["title"])}</h2></header>')
  elif b['kind']=='paragraph':body.append('<p class="prose" style="margin:0 0 22px;font-size:15px;line-height:1.95;letter-spacing:.5px;text-align:justify">'+emphasize(b['text'])+'</p>')
  else:
   # Preserve each photograph's full native aspect; thematic horizontal pairs form seamless strips.
   body.append('<figure style="margin:28px 0 32px">'+''.join(f'<img src="../../assets/omaha-2026/{key}.jpg" alt="{escape(b["caption"].split("｜")[0])}" loading="lazy" style="display:block;width:100%;height:auto;margin:0">' for key in b['ids'])+'<figcaption style="margin:10px 0 0;text-align:center;font-size:12px;line-height:1.8;color:#888">'+escape(b['caption'])+'</figcaption></figure>')
 body.append('<footer class="ending"><p class="end-mark">— 本文完 —</p><p class="series">RUN50 · 第36州</p><h2 style="margin:16px 0 0;text-align:center">内布拉斯加，点亮</h2><p class="closing" style="margin:0;padding:24px 0 0;text-align:center;font-size:13px;line-height:1.9">美国中部的平原州，奥马哈临密苏里河。</p><p class="credits">文字 / Arsenan<br>旅途摄影 / Arsenan、Siqi<br>跑步画面 / Ace Pro 2、Go Ultra · 旅途视频 / Luna</p></footer>')
 body.append('<aside class="source-note"><p>本文依据2026年9月25日至28日的旅途视频、对话、照片与运动轨迹整理。44.97公里、4:50:51为个人轨迹记录，并非赛事官方成绩。封面为 imagegen 创作的系列插画，非赛事奖牌实物。</p><p>资料核对：<a href="https://omahamarathon.com/participant-guide/">赛事领物指南</a> · <a href="https://www.nps.gov/places/bob-kerrey-pedestrian-bridge.htm">Bob Kerrey 步行桥</a></p></aside>')
 nav='<nav class="copy-tools"><a href="/CN/" style="color:inherit">Run50 中文故事</a><button data-theme-choice="light" aria-pressed="true" type="button">白底</button><button data-theme-choice="dark" aria-pressed="false" type="button">黑底</button><button id="copy-wechat" type="button">一键复制到公众号</button><span id="copy-status" role="status" aria-live="polite"></span></nav>'
 return '<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+title+'</title><meta name="description" content="Run50第36州，2026奥马哈马拉松：周末自驾、最后三分钟领物、跑错路多跑约三公里，与Siqi一起完成全马和半马。"><meta property="og:image" content="https://zhennanzhang.com/assets/omaha-2026/cover-cn.jpg"><style>'+css+'</style></head><body>'+nav+'<main data-edition="omaha-editorial">'+'\n'.join(body)+'</main><script src="../../assets/omaha-wechat-copy.js?v=blue-ridge-standard-2" defer></script></body></html>'
if __name__=='__main__':
 for suffix in ['editorial','modern-rail']:(ROOT/f'run50/wechat/omaha-marathon-{suffix}.html').write_text(render(),encoding='utf-8')
