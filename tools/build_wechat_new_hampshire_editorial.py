"""Separate New Hampshire editorial edition; never regenerates the original Rail page."""
from pathlib import Path
from html import escape
import json,re
import build_wechat_michigan_editorial as template
ROOT=Path(__file__).resolve().parents[1]
SLUG='new-hampshire-clarence-demar-marathon'
OUT=ROOT/f'run50/wechat/{SLUG}-editorial.html'
def render():
 data=json.loads((ROOT/'tools/data/new-hampshire-wechat-editorial.json').read_text(encoding='utf-8'))
 shell=template.render()
 css=re.search(r'<style>(.*?)</style>',shell,re.S).group(1)
 body=[f'<header class="masthead"><h1>{escape(data["title"])}</h1><p class="byline">文字 / Arsenan</p></header>', '<picture class="brand-intro"><source media="(prefers-reduced-motion: reduce)" srcset="../../assets/run50-robot-intro-compact-still.png"><img src="../../assets/run50-robot-intro-compact.gif" alt="Run50 机器人片头" width="224" height="300"></picture>', '<figure class="cover"><picture><source media="(prefers-reduced-motion: reduce)" srcset="../stories/chinese/Run50-New-Hampshire-Clarence-DeMar-Marathon-clean_files/img-096.webp"><img src="../../assets/new-hampshire-wechat-hero.gif" alt="新罕布什尔：比赛、完赛合影与奖牌" width="900" height="820"></picture><figcaption class="hero-credit">新罕布什尔 · 比赛、完赛合影与奖牌｜摄影署名见正文</figcaption></figure>', '<div class="down" aria-hidden="true">⌄<br>⌄<br>⌄</div><section class="intro"><p>从尼亚加拉瀑布一路开进新英格兰秋色，在基恩的小镇清晨、山林赛道和校园终点里完成第22州。</p></section>']
 body.append(template.figure('/assets/cn-article-maps/us-light-3ec8245ecf7480df.png','Run50 第22州，新罕布什尔地图','Run50 第22州 · 新罕布什尔｜制图 / Arsenan'))
 body.append(template.figure('../../assets/cover-medal-zh-index-new-hampshire-cn-flat.jpg','新罕布什尔奖牌封面','新罕布什尔 · Clarence DeMar Marathon'))
 n=0
 for block in data['blocks']:
  if block['kind']=='heading':
   n+=1;body.append(f'<header class="chapter"><span class="chapter-number">{n:02}</span><p class="chapter-label">{escape(block["label"])}</p><h2>{escape(block["title"])}</h2></header>')
  elif block['kind']=='figure':body.append(template.figure(block['src'],block['alt'],block['caption']))
  else:body.append(block['html'].replace('<p>','<p class="prose" style="margin:0 8px 22px;font-size:15px;line-height:1.95;letter-spacing:.5px;text-align:justify">',1))
 body.append('<footer class="ending"><p class="end-mark">— 本文完 —</p><p class="series">RUN50 · 第22州</p><h2>新罕布什尔，点亮。</h2><p>第22州，跑在新英格兰的秋色里，见到的人和事都很特别。</p><p class="credits">文字 / Arsenan<br>摄影 / 见图片署名</p></footer>')
 nav=f'<nav class="copy-tools"><a href="{SLUG}-modern-rail.html?v=20260917-clear-colors" style="color:inherit">原版 Rail</a><span>摄影杂志版</span><button class="theme-choice" data-theme-choice="light" aria-pressed="true" type="button">白底</button><button class="theme-choice" data-theme-choice="dark" aria-pressed="false" type="button">黑底</button><button id="copy-wechat" type="button">一键复制到公众号</button><span id="copy-status" role="status" aria-live="polite"></span></nav>'
 return '<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+escape(data['title'])+'</title><style>'+css+'</style></head><body>'+nav+'<main data-edition="new-hampshire-editorial">'+'\n'.join(body)+'</main><script src="../../assets/new-hampshire-wechat-copy.js?v=editorial-1" defer></script></body></html>'
if __name__=='__main__':OUT.write_text(render(),encoding='utf-8')
