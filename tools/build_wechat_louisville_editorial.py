"""Separate Louisville editorial edition; never regenerates the original Rail page."""
from pathlib import Path
from html import escape
import json,re
import build_wechat_michigan_editorial as template
ROOT=Path(__file__).resolve().parents[1]
SLUG='louisville-marathon-2024'
OUT=ROOT/f'run50/wechat/{SLUG}-editorial.html'
def render():
 data=json.loads((ROOT/'tools/data/louisville-wechat-editorial.json').read_text(encoding='utf-8'))
 shell=template.render()
 css=re.search(r'<style>(.*?)</style>',shell,re.S).group(1)
 css+='\nmain{padding-left:20px;padding-right:20px}.cover{margin-left:0;margin-right:0}.intro,.chapter{margin-left:0;margin-right:0}'
 body=[f'<header class="masthead"><h1>{escape(data["title"])}</h1><p class="byline">文字 / Arsenan</p></header>', '<picture class="brand-intro"><source media="(prefers-reduced-motion: reduce)" srcset="../../assets/run50-robot-intro-compact-still.png"><img src="../../assets/run50-robot-intro-compact.gif" alt="Run50 机器人片头" width="224" height="300"></picture>', '<figure class="cover"><picture><source media="(prefers-reduced-motion: reduce)" srcset="../stories/chinese/Run50-Louisville-Marathon-2024-clean_files/img-082.webp"><img src="../../assets/louisville-wechat-hero.gif?v=family-seven" alt="路易斯维尔：比赛、小红花、毕业合影与奖牌" width="900" height="820"></picture><figcaption class="hero-credit">比赛、小红花、毕业合影与奖牌｜摄影署名见正文</figcaption></figure>', '<div class="down" aria-hidden="true">⌄<br>⌄<br>⌄</div><section class="intro"><p>回到美国跑马起点，在 Floyds Fork 的秋色里把博士生涯跑成一个完整的 loop。</p></section>']
 body.append(template.figure('../../assets/wechat-run50-map-louisville-2024-editorial.png','Run50 肯塔基第1州番外，路易斯维尔地图','第1州番外 · 肯塔基#3，星标为路易斯维尔｜制图 / Arsenan'))
 body.append(template.figure('../../assets/wechat-louisville-2024-poster.png','路易斯维尔博士收官战海报','2024 · 路易斯维尔 · 肯塔基#3'))
 n=0
 for block in data['blocks']:
  if block['kind']=='heading':
   n+=1;body.append(f'<header class="chapter"><span class="chapter-number">{n:02}</span><p class="chapter-label">{escape(block["label"])}</p><h2>{escape(block["title"])}</h2></header>')
  elif block['kind']=='figure':body.append(template.figure(block['src'],block['alt'],block['caption']))
  else:body.append(block['html'].replace('<p>','<p class="prose" style="margin:0 0 22px;font-size:15px;line-height:1.95;letter-spacing:.5px;text-align:justify">',1))
 body.append('<footer class="ending"><p class="end-mark">— 本文完 —</p><p class="series">RUN50 · 第1州番外 · 肯塔基#3</p><h2>路易斯维尔，博士收官。</h2><p>肯塔基位于美国中东部，以赛马、波本威士忌和蓝草音乐闻名。</p><p class="credits">文字 / Arsenan<br>摄影 / 见图片署名</p></footer>')
 nav=f'<nav class="copy-tools"><a href="{SLUG}-modern-rail.html?v=20260917-clear-colors" style="color:inherit">原版 Rail</a><span>摄影杂志版</span><button class="theme-choice" data-theme-choice="light" aria-pressed="true" type="button">白底</button><button class="theme-choice" data-theme-choice="dark" aria-pressed="false" type="button">黑底</button><button id="copy-wechat" type="button">一键复制到公众号</button><span id="copy-status" role="status" aria-live="polite"></span></nav>'
 return '<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+escape(data['title'])+'</title><style>'+css+'</style></head><body>'+nav+'<main data-edition="louisville-editorial">'+'\n'.join(body)+'</main><script src="../../assets/louisville-wechat-copy.js?v=aligned-margins-3" defer></script></body></html>'
if __name__=='__main__':OUT.write_text(render(),encoding='utf-8')
