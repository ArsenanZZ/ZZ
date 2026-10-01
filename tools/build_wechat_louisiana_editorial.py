"""Separate Louisiana editorial edition; never regenerates the original Rail page."""
from pathlib import Path
from html import escape
import json,re
import build_wechat_michigan_editorial as template
ROOT=Path(__file__).resolve().parents[1]
SLUG='louisiana-marathon'
OUT=ROOT/f'run50/wechat/{SLUG}-editorial.html'
def render():
 data=json.loads((ROOT/'tools/data/louisiana-wechat-editorial.json').read_text(encoding='utf-8'))
 shell=template.render()
 css=re.search(r'<style>(.*?)</style>',shell,re.S).group(1)
 css+='\nmain{padding-left:20px;padding-right:20px}.cover{margin-left:0;margin-right:0}.intro,.chapter{margin-left:0;margin-right:0}'
 body=[f'<header class="masthead"><h1>{escape(data["title"])}</h1><p class="byline">文字 / Arsenan</p></header>', '<picture class="brand-intro"><source media="(prefers-reduced-motion: reduce)" srcset="../../assets/run50-robot-intro-compact-still.png"><img src="../../assets/run50-robot-intro-compact.gif" alt="Run50 机器人片头" width="224" height="300"></picture>', '<figure class="cover"><picture><source media="(prefers-reduced-motion: reduce)" srcset="../stories/chinese/Run50-Louisiana-Marathon-clean_files/img-042.webp"><img src="../../assets/louisiana-wechat-hero.gif?v=clear-medal" alt="路易斯安那：比赛、合影与巴吞鲁日" width="900" height="820"></picture><figcaption class="hero-credit">比赛照 / 赛事摄影 · 合影与奖牌署名见正文</figcaption></figure>', '<div class="down" aria-hidden="true">⌄<br>⌄<br>⌄</div><section class="intro"><p>新年第一跑，从转机到新奥尔良，再开进巴吞鲁日，把南方湿地、LSU 紫金色和 Finish Fest 串在一起。</p></section>']
 body.append('<figure class="photo-strip map-poster" style="margin:32px 0 36px"><img src="../../assets/wechat-run50-map-louisiana-23-editorial.png?v=crawfish-pointer-1" alt="第23州路易斯安那，星标巴吞鲁日" style="display:block;width:100%;height:auto;margin:0"><img src="../../assets/wechat-louisiana-poster.png" alt="2025 巴吞鲁日 路易斯安那海报" style="display:block;width:100%;height:auto;margin:0"><figcaption style="margin:10px 0 0;text-align:center;font-size:12px;line-height:1.75;color:#888">第23州 · 路易斯安那，星标为巴吞鲁日｜制图 / Arsenan<br>2025 · 巴吞鲁日 · Louisiana Marathon</figcaption></figure>')

 n=0
 for block in data['blocks']:
  if block['kind']=='heading':
   n+=1;body.append(f'<header class="chapter"><span class="chapter-number">{n:02}</span><p class="chapter-label">{escape(block["label"])}</p><h2>{escape(block["title"])}</h2></header>')
  elif block['kind']=='photo-strip':
   body.append('<figure class="photo-strip" style="margin:32px 0 36px">'+''.join('<img src="'+escape(im['src'])+'" alt="'+escape(im['alt'])+'" loading="lazy" style="display:block;width:100%;height:auto;margin:0">' for im in block['images'])+'<figcaption style="margin:10px 0 0;text-align:center;font-size:12px;line-height:1.75;color:#888">'+escape(block['caption'])+'</figcaption></figure>')
  elif block['kind']=='figure':body.append(template.figure(block['src'],block['alt'],block['caption']))
  else:body.append(block['html'].replace('<p>','<p class="prose" style="margin:0 0 22px;font-size:15px;line-height:1.95;letter-spacing:.5px;text-align:justify">',1))
 body.append('<footer class="ending"><p class="end-mark">— 本文完 —</p><p class="series">RUN50 · 第23州</p><h2>路易斯安那，点亮。</h2><p>路易斯安那位于美国南部、密西西比河下游，以爵士乐、湿地和卡津美食闻名。</p><p class="credits">文字 / Arsenan<br>摄影 / 见图片署名</p></footer>')
 nav=f'<nav class="copy-tools"><a href="{SLUG}-rail-clear-colors.html?wechat=1" style="color:inherit">原版 Rail</a><a href="{SLUG}-magazine-wechat.html" style="color:inherit">旅行杂志版</a><span>摄影杂志版</span><button class="theme-choice" data-theme-choice="light" aria-pressed="true" type="button">白底</button><button class="theme-choice" data-theme-choice="dark" aria-pressed="false" type="button">黑底</button><button id="copy-wechat" type="button">一键复制到公众号</button><span id="copy-status" role="status" aria-live="polite"></span></nav>'
 return '<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+escape(data['title'])+'</title><style>'+css+'</style></head><body>'+nav+'<main data-edition="louisiana-editorial">'+'\n'.join(body)+'</main><script src="../../assets/louisiana-wechat-copy.js?v=six-strips" defer></script></body></html>'
if __name__=='__main__':
 content=render()
 OUT.write_text(content,encoding='utf-8')
 (ROOT/f'run50/wechat/{SLUG}-modern-rail.html').write_text(content,encoding='utf-8')
