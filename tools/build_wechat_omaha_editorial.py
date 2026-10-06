"""Render the Omaha #36 story from source-grounded editorial blocks."""
from pathlib import Path
from html import escape
import json,re
import build_wechat_louisville_editorial as template
ROOT=Path(__file__).resolve().parents[1]

def photo_layout(blocks):
 groups=[['NE-04','NE-04-1','NE-04-2'],['NE-07-1','NE-07-2'],['NE-11','NE-11-1'],['NE-22','NE-22-1'],['NE-24','NE-25'],['NE-31','NE-32'],['NE-40-1','NE-41'],['NE-49-1','NE-50','NE-50-1'],['NE-58-0','NE-58-1']]
 result=[];i=0
 while i<len(blocks):
  match=next((g for g in groups if [b.get('ids') for b in blocks[i:i+len(g)]]==[[k] for k in g]),None)
  if match:
   result.append({'kind':'photo-strip','photos':blocks[i:i+len(match)]});i+=len(match)
  else:result.append(blocks[i]);i+=1
 return result
def emphasize(text):
 text=escape(text)
 phrases=['社区感','巴菲特','Cornhusker State','5点57分','还有三分钟','我们都有美好的未来','Huskers','7点出发','Fertile Ground','河搬家了，州界却没搬','两公里','15英里','约3公里','加量不加价','Omaha North Mill','免费的，真香','BIG EAST','Bob Kerrey Pedestrian Bridge','Looking Up','24英里','赠送里程','熟悉的鞋','4小时50分51秒','第36州，六六三十六',
 '越来越想念在美国跑马的日子','像参加了一场社区活动','“旅行纪念品”','我和 Siqi 都报了名','我们去不了股神的饭局，但可以去他老家跑一圈','别人下班回家，我们下班开始跨州','把中秋过在美国中部的公路上','窗外像在不停换壁纸','“欺骗一下观众”','一个移动版','被放大的瑞士卷','我以为领物到晚上9点，实际上下午6点就结束','车里已经开始默默倒计时','Millwork Commons','Archetype Coffee','来得刚刚好','大学棒球世界大赛','亨利·多利动物园与水族馆','农业传统就这样穿在了球迷身上','先学会认当地人的队服','Charles Schwab Field','《沃土》','大桥还没到，我已经先跑进了一趟爱荷华','卡特湖市属于爱荷华，却在河的西边','1892年的判决','没有过桥，也没有下水，就跨了一次州','部落土地和联邦博彩法律','同一个15英里，看到了两次','将近45公里','那些巨大的白色圆筒是粮仓','小麦和面粉','照片可以免费下载','“大东联盟”','跨州大桥','可以同时踩着两个州','双脚跨过州界','一个小小的真人在脚边活动','新的飞影跑鞋','脚掌也越来越疼','经验都在，就是不一定用得上','我的手表已经够一个全马了','比赛还是穿熟悉的鞋，岔路口还是多看一眼','她拍我冲线，我们再一起拍几张合影','蓝色和黄色','后面还有十来个小时的车程','爱荷华是 Iowa','爱达荷是 Idaho','第36州，六六三十六','领物差三分钟就结束，我们赶上了','是我实在应该认真研究一下路线','这趟奥马哈，来得挺值','谢谢老婆支持这种有点折腾的周末','一起去下一个州。故事还在继续']
 underlines={'河搬家了，州界却没搬','同一个15英里，看到了两次','经验都在，就是不一定用得上','我的手表已经够一个全马了','我们都有美好的未来','一起去下一个州。故事还在继续'}
 phrases += ['在中国待了两个月','总得给减肥找个目标','还有两周可以恢复训练','周末自驾圈','当时已经96岁了','尽量不耽误工作，利用好周末','2026年9月25日','中秋节','粉色','金黄','火烧云','健身房打了个卡','月亮格外圆','进入了中部时间','玉米、大豆','提前二十来分钟到','离收摊还有三分钟','Siqi 去停车，我去领装备','她领养了两个来自中国的孩子','她还想给我们做早餐','内布拉斯加大学林肯分校','Cardinals','三三两两地集合','嘎吱嘎吱','美国最高法院','州界仍然沿着原来的河道','早上7点53分','8点04分','Prairie Flower Casino','我真的又来了一遍','重新找回正确路线','看到镜头，还是要精神起来','Creighton University','一场比赛还是老老实实记一个州','太阳出来了','换了个州，却有一点熟悉的感觉','脚疼就慢一点，能跑就跑','没在手表到达全马距离时停表','最后这几公里，就当认真逛一逛','Siqi 已经跑完一个多小时了','挂在脖子上','周一早晨继续赶路，回去工作','密苏里跑错过路，在堪萨斯也跑错过','一点不让我吃亏','继续好好锻炼，把身体练好']
 underlines.update(['像参加了一场社区活动','我和 Siqi 都报了名','我们去不了股神的饭局，但可以去他老家跑一圈','别人下班回家，我们下班开始跨州','“欺骗一下观众”','我以为领物到晚上9点，实际上下午6点就结束','离收摊还有三分钟','农业传统就这样穿在了球迷身上','没有过桥，也没有下水，就跨了一次州','加量不加价','免费的，真香','可以同时踩着两个州','比赛还是穿熟悉的鞋，岔路口还是多看一眼','她拍我冲线，我们再一起拍几张合影','第36州，六六三十六','这趟奥马哈，来得挺值','谢谢老婆支持这种有点折腾的周末'])
 tones={escape(p):i%4 for i,p in enumerate(dict.fromkeys(phrases))}
 def mark(m):
  p=m.group();extra=' data-cn-emphasis="underline"' if p in underlines else ''
  return f'<strong data-cn-tone="{tones[p]}"{extra}>{p}</strong>'
 return re.sub('|'.join(re.escape(p) for p in sorted(tones,key=len,reverse=True)),mark,text)

def render():
 data=json.loads((ROOT/'tools/data/omaha-wechat-editorial.json').read_text(encoding='utf-8'))
 css=re.search(r'<style>(.*?)</style>',template.render(),re.S).group(1)
 css+='\nmain{padding-left:20px;padding-right:20px}.cover,.intro,.chapter{margin-left:0;margin-right:0}.photo-pair{display:grid;grid-template-columns:1fr 1fr;gap:6px;align-items:start}.photo-pair img{width:100%;height:auto}.source-note{font-size:12px;line-height:1.8;color:#888} .source-note a{color:inherit}'
 title=escape(data['title']);body=[f'<header class="masthead"><h1>{title}</h1><p class="byline">文字 / Arsenan</p></header>', '<picture class="brand-intro"><source media="(prefers-reduced-motion: reduce)" srcset="../../assets/run50-robot-intro-compact-still.png"><img src="../../assets/run50-robot-intro-compact.gif" alt="Run50 机器人片头" width="224" height="300"></picture>', '<figure class="cover"><picture><source media="(prefers-reduced-motion: reduce)" srcset="../../assets/omaha-2026/selected-20261006/hero-still.jpg"><img src="../../assets/omaha-2026/selected-20261006/hero.gif?v=20261006-square-medal" alt="奥马哈：起跑、跨州大桥、冲线、合影与奖牌" width="900" height="900"></picture><figcaption class="hero-credit">2026年9月27日 · 我和 Siqi 的奥马哈周末<br>起跑、桥、合影与奖牌 / Arsenan · 冲线 / 赛事官方摄影</figcaption></figure>', '<div class="down" aria-hidden="true">⌄<br>⌄<br>⌄</div><section class="intro"><p>中秋下班出发，去巴菲特老家跑马。领物差三分钟，比赛多跑三公里。玉米地、跨州大桥，还有第36州的两块奖牌。</p></section>']
 body.append('<figure class="photo-strip map-poster" style="margin:32px 0 36px"><img src="../../assets/omaha-2026/map-corn-20261006.jpg" alt="Run50第36州，内布拉斯加；星标奥马哈" style="display:block;width:100%;height:auto;margin:0"><img src="../../assets/omaha-2026/poster-cn-corn-20261006.png" alt="2026 奥马哈 · RUN50 36 玉米纸质海报" style="display:block;width:100%;height:auto;margin:0"><figcaption style="margin:10px 0 0;text-align:center;font-size:12px;line-height:1.75;color:#888">第36州 · 内布拉斯加，星标为奥马哈｜制图 / Arsenan<br>2026 · 奥马哈 · Omaha Marathon</figcaption></figure>')
 n=0
 for b in photo_layout(data['blocks']):
  if b['kind']=='heading':
   n+=1;body.append(f'<header class="chapter"><span class="chapter-number">{n:02}</span><p class="chapter-label">{escape(b["label"])}</p><h2>{escape(b["title"])}</h2></header>')
  elif b['kind']=='paragraph':body.append('<p class="prose" style="margin:0 0 22px;font-size:15px;line-height:1.95;letter-spacing:.5px;text-align:justify">'+emphasize(b['text'])+'</p>')
  else:
   photos=b['photos'] if b['kind']=='photo-strip' else [b]
   labels=['上','下'] if len(photos)==2 else ['上','中','下']
   imgs=[];captions=[]
   for j,photo in enumerate(photos):
    key=photo['ids'][0]
    imgs.append(f'<img src="../../assets/omaha-2026/{data["photo_folder"]}/{key}.webp" alt="{escape(photo["caption"])}" loading="lazy" decoding="async" style="display:block;width:100%;height:auto;margin:0">')
    captions.append((labels[j]+'：' if len(photos)>1 else '')+escape(photo['caption'])+(' · '+escape(photo['credit']) if photo.get('credit') else ''))
   cls='story-photo photo-strip' if len(photos)>1 else 'story-photo'
   body.append(f'<figure class="{cls}" style="margin:28px 0 32px">'+''.join(imgs)+'<figcaption style="margin:10px 0 0;text-align:center;font-size:12px;line-height:1.8;color:#888">'+'<br>'.join(captions)+'</figcaption></figure>')
 body.append('<footer class="ending"><p class="end-mark">本文完</p><p class="series">RUN50 · 第36州</p><h2 style="margin:16px 0 0;text-align:center">内布拉斯加，点亮</h2><p class="closing" style="margin:0;padding:24px 0 0;text-align:center;font-size:13px;line-height:1.9">玉米地、密苏里河，奥马哈的第一个马拉松周末</p><p class="credits">文字 / Arsenan</p></footer>')
 sources=[('赛事领物指南','https://omahamarathon.com/participant-guide/'),('玉米与农业','https://nebraskacorn.gov/about-us/faq/'),('Huskers 队名','https://huskers.com/news/2019/08/12/origin-of-the-cornhusker-nickname-1'),('奥马哈城市介绍','https://www.visitomaha.com/blog/post/omaha-fun-facts/'),('卡特湖历史','https://cityofcarterlake.com/departments/city-hall-department/history/'),('1892年州界判决','https://www.law.cornell.edu/supremecourt/text/143/359'),('赌场诉讼判决','https://ecf.ca8.uscourts.gov/opndir/21/08/192898P.pdf'),('Omaha North Mill','https://www.ardentmillscareers.com/our-facilities/nebraska/omaha-north-mill/'),('老面粉厂历史','https://northomahahistory.com/2025/12/26/a-history-of-the-mothers-best-flour-mill-in-north-omaha/'),('沃土壁画','https://www.megsaligman.com/murals/evolvingfaces-mjxsa'),('BIG EAST','https://www.bigeast.com/sports/2026/9/10/BE_history_090926.aspx'),('跨州大桥','https://www.visitomaha.com/bob/'),('Looking Up','https://www.iowawestfoundation.org/for-our-communities/public-art/')]
 body.append('<aside class="source-note"><p>44.97公里、4:50:51为个人轨迹记录，并非赛事官方成绩。卡特湖跨州时间依据个人轨迹与美国人口普查局州界数据估算。</p><p>延伸阅读：'+' · '.join(f'<a href="{url}">{label}</a>' for label,url in sources)+'</p></aside>')
 nav='<nav class="copy-tools"><a href="/CN/" style="color:inherit">Run50 中文故事</a><button data-theme-choice="light" aria-pressed="true" type="button">白底</button><button data-theme-choice="dark" aria-pressed="false" type="button">黑底</button><button id="copy-wechat" type="button">一键复制到公众号</button><span id="copy-status" role="status" aria-live="polite"></span></nav>'
 return '<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+title+'</title><link rel="canonical" href="https://zhennanzhang.com/run50/wechat/omaha-marathon-editorial.html"><meta property="og:title" content="'+title+'"><meta name="description" content="Run50第36州，2026奥马哈马拉松：中秋周末自驾，去巴菲特老家跑马。卡特湖飞地、跨州大桥与多跑的三公里，和Siqi一起完赛。"><meta property="og:image" content="https://zhennanzhang.com/assets/omaha-2026/poster-cn-corn-20261006.png"><style>'+css+'</style></head><body>'+nav+'<main data-edition="omaha-editorial">'+'\n'.join(body)+'</main><script src="../../assets/omaha-wechat-copy.js?v=20261006-colors" defer></script></body></html>'
if __name__=='__main__':
 for suffix in ['editorial','modern-rail']:(ROOT/f'run50/wechat/omaha-marathon-{suffix}.html').write_text(render(),encoding='utf-8')
