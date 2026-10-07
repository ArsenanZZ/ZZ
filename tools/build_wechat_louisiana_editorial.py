"""Separate Louisiana editorial edition; never regenerates the original Rail page."""
from pathlib import Path
from html import escape
import json,re
import build_wechat_louisville_editorial as style_template
import build_wechat_michigan_editorial as template
ROOT=Path(__file__).resolve().parents[1]
SLUG='louisiana-marathon'
OUT=ROOT/f'run50/wechat/{SLUG}-editorial.html'

def strip_caption(block):
 if block.get('caption'):return escape(block['caption'])
 labels=['上','下'] if len(block['images'])==2 else ['上','中','下']
 return '<br>'.join(labels[i]+'：'+escape(im['caption']) for i,im in enumerate(block['images']))

def emphasize(html):
 phrases=['日复一日投喂','南方还有几个州没打卡','租车一路开到巴吞鲁日','爵士乐','湿地沼泽','狂欢节和美食','红色木杆','LSU 老虎队','庞恰特雷恩湿地','旧州议会大厦','密西西比河畔','1 英里','2 英里','3 英里','4 英里','7 英里','8 英里到 9 英里','11 英里','50 States Marathon Club','金光粼粼','路易斯安那州立大学（LSU）','虎体育场（Tiger Stadium）','超过 10 万人','死亡之谷','紫金色的热情','University Lake（大学湖）','Powerade','17 英里','Save TikTok','打卡大老虎','20 英里','Mile 20','啤酒','奶昔杯的充气服','奶牛装','25 英里','26 英里','落羽杉','5 小时出头','Martin Luther King Day','只能自己请一天假']
 # Apply accents to text nodes only, avoiding nested markup and preserving existing emphasis.
 parts=re.split(r'(<[^>]+>)',html);depth=0;out=[]
 pat=re.compile('|'.join(re.escape(x) for x in sorted(phrases,key=len,reverse=True)))
 for part in parts:
  if part.startswith('<'):
   if re.match(r'<strong\b',part):depth+=1
   if part=='</strong>':depth-=1
   out.append(part)
  else:out.append(pat.sub(lambda m:'<strong>'+m.group()+'</strong>',part) if not depth else part)
 html=''.join(out);count=0
 under=['把状态拉回来','那就它了','先飞达拉斯，再转机新奥尔良','可别和加州的洛杉矶搞混','一个是州，一个是城','真正的首府','高速公路像是直接架在水面上','车子就像在水上漂','等着明天在密西西比河畔开跑','跑慢点也没关系','Save TikTok','举罐畅饮','跑跑走走','全美最高的州议会楼','Siqi 已经完赛','学校放假、公司不放','别想太远，多做眼前能做的事','行好事，信好运，剩下的交给时间']
 def mark(m):
  nonlocal count
  text=m.group(1);tone=(sum(ord(c) for c in re.sub('<[^>]+>','',text)))%4;count+=1
  extra=' data-cn-emphasis="underline"' if any(p in text for p in under) else ''
  return f'<strong data-cn-tone="{tone}"{extra}>'+text+'</strong>'
 return re.sub(r'<strong>(.*?)</strong>',mark,html)
def render():
 data=json.loads((ROOT/'tools/data/louisiana-wechat-editorial.json').read_text(encoding='utf-8'))
 shell=style_template.render()
 css=re.search(r'<style>(.*?)</style>',shell,re.S).group(1)
 css+='\nmain{padding-left:20px;padding-right:20px}.cover{margin-left:0;margin-right:0}.intro,.chapter{margin-left:0;margin-right:0}'
 body=[f'<header class="masthead"><h1>{escape(data["title"])}</h1><p class="byline">文字 / Arsenan</p></header>', '<picture class="brand-intro"><source media="(prefers-reduced-motion: reduce)" srcset="../../assets/run50-robot-intro-compact-still.png"><img src="../../assets/run50-robot-intro-compact.gif" alt="Run50 机器人片头" width="224" height="300"></picture>', '<figure class="cover"><picture><source media="(prefers-reduced-motion: reduce)" srcset="../stories/chinese/Run50-Louisiana-Marathon-clean_files/img-042.webp"><img src="../../assets/louisiana-wechat-hero.gif?v=20261007-square" alt="路易斯安那：比赛、合影与巴吞鲁日" width="900" height="900"></picture><figcaption class="hero-credit">比赛照 / 赛事摄影 · 合影与奖牌署名见正文</figcaption></figure>', '<div class="down" aria-hidden="true">⌄<br>⌄<br>⌄</div><section class="intro"><p>从新奥尔良机场出发，穿过湿地，去巴吞鲁日跑马。湖边的晨光、LSU 的紫金色、20英里的啤酒，还有沿街热闹的加油声，这场南方派对得用双脚参加。</p></section>']
 body.append('<figure class="photo-strip map-poster" style="margin:32px 0 36px"><img src="../../assets/wechat-run50-map-louisiana-23-editorial.png?v=crawfish-pointer-1" alt="第23州路易斯安那，星标巴吞鲁日" style="display:block;width:100%;height:auto;margin:0"><img src="../../assets/wechat-louisiana-poster.png" alt="2025 巴吞鲁日 路易斯安那海报" style="display:block;width:100%;height:auto;margin:0"><figcaption style="margin:10px 0 0;text-align:center;font-size:12px;line-height:1.75;color:#888">第23州 · 路易斯安那，星标为巴吞鲁日｜制图 / Arsenan<br>2025 · 巴吞鲁日 · Louisiana Marathon</figcaption></figure>')

 n=0
 for block in data['blocks']:
  if block['kind']=='heading':
   n+=1;body.append(f'<header class="chapter"><span class="chapter-number">{n:02}</span><p class="chapter-label">{escape(block["label"])}</p><h2>{escape(block["title"])}</h2></header>')
  elif block['kind']=='photo-strip':
   body.append('<figure class="photo-strip" style="margin:32px 0 36px">'+''.join('<img src="'+escape(im['src'])+'" alt="'+escape(im['alt'])+'" loading="lazy" style="display:block;width:100%;height:auto;margin:0">' for im in block['images'])+'<figcaption style="margin:10px 0 0;text-align:center;font-size:12px;line-height:1.75;color:#888">'+strip_caption(block)+'</figcaption></figure>')
  elif block['kind']=='figure':body.append(template.figure(block['src'],block['alt'],block['caption']))
  else:body.append(emphasize(block['html']).replace('<p>','<p class="prose" style="margin:0 0 22px;font-size:15px;line-height:1.95;letter-spacing:.5px;text-align:justify">',1))
 body.append('<footer class="ending"><p class="end-mark">本文完</p><p class="series">RUN50 · 第23州</p><h2 style="margin:16px 0 0;text-align:center">路易斯安那，点亮</h2><p class="closing" style="margin:0;padding:24px 0 0;text-align:center;font-size:13px;line-height:1.9">美国南部，以爵士乐与湿地闻名。</p><p class="credits">文字 / Arsenan<br>摄影 / 见图片署名</p></footer>')
 nav=f'<nav class="copy-tools"><a href="{SLUG}-rail-clear-colors.html?wechat=1" style="color:inherit">原版 Rail</a><a href="{SLUG}-magazine-wechat.html" style="color:inherit">旅行杂志版</a><span>摄影杂志版</span><button class="theme-choice" data-theme-choice="light" aria-pressed="true" type="button">白底</button><button class="theme-choice" data-theme-choice="dark" aria-pressed="false" type="button">黑底</button><button id="copy-wechat" type="button">一键复制到公众号</button><span id="copy-status" role="status" aria-live="polite"></span></nav>'
 return '<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+escape(data['title'])+'</title><style>'+css+'</style></head><body>'+nav+'<main data-edition="louisiana-editorial">'+'\n'.join(body)+'</main><script src="../../assets/louisiana-wechat-copy.js?v=20261007-colors" defer></script></body></html>'
if __name__=='__main__':
 content=render()
 OUT.write_text(content,encoding='utf-8')
 (ROOT/f'run50/wechat/{SLUG}-modern-rail.html').write_text(content,encoding='utf-8')
