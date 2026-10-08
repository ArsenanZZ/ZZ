"""Refresh the Virginia through Alabama CN stories using the approved editorial layout."""
from pathlib import Path
from html import escape
import json,re,copy,subprocess
from PIL import Image
from bs4 import BeautifulSoup
import build_wechat_louisville_editorial as style
import build_wechat_michigan_editorial as template
ROOT=Path(__file__).resolve().parents[1]
CONFIG={
'blue-ridge-marathon':('blue-ridge-wechat',24,'弗吉尼亚',[76,51,1,85,82],['前言','罗阿诺克','长途出发','清晨起跑','山路向上','山顶之星','16英里以后','终点之前','回程路上']),
'kentucky-derby-marathon-2025':('kentucky-derby-marathon-2025',1,'肯塔基',[46,9,3,58,95],None),
'fargo-marathon':('fargo-marathon',25,'北达科他',[86,64,17,90,93],None),
'hell-on-gravel-marathon':('hell-on-gravel-marathon',26,'堪萨斯',[70,43,15,2,76],None),
'mad-marathon':('mad-marathon',27,'佛蒙特',[90,78,102,48,98],None),
'rocket-city-marathon':('rocket-city-marathon',28,'阿拉巴马',[96,25,77,102,105],None)}
CROPS={
 'blue-ridge-marathon':[(.5,0),(.5,.3),(.5,.5),(.5,.3),(.5,1)],
 'kentucky-derby-marathon-2025':[(.5,0),(.3,.5),(.5,.5),(.5,.3),(.5,.5)],
 'fargo-marathon':[(.5,0),(0,.3),(.5,.5),(.75,.1),(.5,0)],
 'hell-on-gravel-marathon':[(.5,0),(.5,0),(.5,.5),(.5,.3),(.5,.3)],
 'mad-marathon':[(.5,0),(.5,.4),(.5,.3),(.5,.5),(.5,1)],
 'rocket-city-marathon':[(.5,.3),(.5,.2),(.5,.3),(.5,.3),(.5,1)]}
ENDINGS={
 'blue-ridge-marathon':('第24州','弗吉尼亚，翻过蓝岭山','弗吉尼亚位于美国东部，蓝岭山脉穿州而过，罗阿诺克坐落在山谷之间。'),
 'kentucky-derby-marathon-2025':('第1州番外 · 肯塔基#4','路易斯维尔，第50场','肯塔基位于美国中东部，以赛马、波本威士忌和蓝草音乐闻名。'),
 'fargo-marathon':('第25州','法戈，50州跑到一半','北达科他位于美国北部大平原，法戈坐落在红河西岸，与明尼苏达隔河相望。'),
 'hell-on-gravel-marathon':('第26州','堪萨斯，十个人里的冠军','堪萨斯位于美国中部，麦田、草原和向日葵铺展在大平原上。'),
 'mad-marathon':('第27州','佛蒙特，跑过绿山与谷仓','佛蒙特位于新英格兰，以绿山、枫糖和乡间廊桥闻名。'),
 'rocket-city-marathon':('第28州','阿拉巴马，跑进火箭城','阿拉巴马位于美国南部，亨茨维尔因火箭研发与航天工业被称为火箭城。')}
KEYWORDS='罗阿诺克之星|蓝岭山|阿巴拉契亚山脉|人车双充|全美最虐赛道|第一次开电车长途|第50场|第 50 场|三块奖牌|一块蛋糕|Derby Festival|Big Four Bridge|Churchill Downs|路易斯维尔|俄亥俄河|Siqi|FargoDome|Fargo|Red River|阿森纳|破4|半程分水岭|最后6英里|星链|玉米棒子|北达科他|Hell on Gravel|十个人|冠军|砂石路|埃尔多拉多|向日葵|牛群|Wichita|疯河谷|绿山|枫糖|红色谷仓|Mad River|Vermont|新英格兰|Waitsfield|火箭城|Huntsville|Saturn V|土星五号|航天|东北大花袄|零下|室内终点|寒流|NASA|美国太空与火箭中心|半马|全马'
UNDER=['又虐又美','能跑完，就是胜利','找到属于自己的节奏','第一次开电车长途','人车双充','自由、倔强、往上爬','把我的外套给了她','温暖，也在接力','整个比赛的灵魂地段','又开始上坡','举起双臂，冲线','第 50 场马拉松','第50场马拉松','三个奖牌','三块奖牌','一块蛋糕','破4','分水岭','冠军','只有十个人','十个人','加量不加价','绿色的山','乡村油画','绿山','零下','室内','寒流','东北大花袄']
def local(src):
 src=src.split('?')[0]
 return ROOT/src.lstrip('/') if src.startswith('/') else (ROOT/'run50/wechat'/src).resolve()
def photos(blocks):
 return [im for b in blocks for im in (b['images'] if b['kind']=='photo-strip' else [b] if b['kind']=='figure' else [])]
def emphasize(html):
 soup=BeautifulSoup(html,'html.parser')
 for node in list(soup.find_all(string=True)):
  if node.parent.name in ['strong','b','a']:continue
  chunks=re.split('('+KEYWORDS+r'|\d+(?:\.\d+)?\s*英里|\d+\s*公里)',str(node))
  if len(chunks)>1:
   for i,ch in enumerate(chunks):
    if i%2:
     tag=soup.new_tag('strong');tag.string=ch;node.insert_before(tag)
    else:node.insert_before(ch)
   node.extract()
 for i,tag in enumerate(soup.find_all(['strong','b'])):
  tag.name='strong';tag['data-cn-tone']=str(sum(map(ord,tag.get_text()))%4)
  extra=['第50个马拉松','第一次在傍晚跑跨州','最后我们一起冲线','到处都是熟面孔','公司的同事们已经在等我','三十多岁的我，还在路上','白天跑步，晚上在车里露营','风大得能把人跑偏','我们就躺在车里','赶在马拉松Expo关门前','一路都是热闹的街坊氛围','一边击掌一边接水','他还记得我，太巧了','离终点越来越近了','已经整整跑了 25 个州','每一场都有故事','16 小时的长途车程','充电、吃饭、赶路、看风景','居然还有西瓜','只要主动一点','这绝对不是终点','Run50 的第 27 个州']
  if any(x in tag.get_text() for x in UNDER+extra):tag['data-cn-emphasis']='underline'
 return str(soup)
def caption(s):
 s=re.sub(r'\s*@\s*(Arsenan|Siqi)\b',r' · 摄影 / \1',s)
 s=s.replace('摄影 | 待确认','家庭影像').replace('摄影 |','摄影 /').replace('赛事摄影','赛事官方摄影')
 return s
def landscape(b):
 if b['kind']!='figure':return False
 with Image.open(local(b['src'])) as im:return im.width>=im.height*1.15
def groups(blocks):
 out=[];i=0
 while i<len(blocks):
  b=blocks[i]
  if landscape(b):
   ims=[b];j=i+1
   while j<len(blocks) and len(ims)<3 and landscape(blocks[j]):ims.append(blocks[j]);j+=1
   # An adjacent short paragraph introduces the next photo in the same scene.
   k=j;between=[]
   while k<len(blocks) and blocks[k]['kind']=='paragraph' and len(between)<2:
    between.append(blocks[k]);k+=1
   if len(ims)==1 and between and k<len(blocks) and sum(len(BeautifulSoup(p['html'],'html.parser').get_text()) for p in between)<240 and landscape(blocks[k]):
    out.extend(between);ims.append(blocks[k]);j=k+1
   if len(ims)>1:out.append({'kind':'photo-strip','images':ims});i=j;continue
  out.append(b);i+=1
 return out
def hero(slug,ims,indices):
 out=ROOT/f'assets/{slug}-editorial-hero.gif'
 tmp=ROOT/'tmp'/f'hero-{slug}';tmp.mkdir(exist_ok=True)
 for j,k in enumerate(indices):
  x,y=CROPS[slug][j]
  subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(local(ims[k]['src'])),'-vf',f'scale=900:900:force_original_aspect_ratio=increase,crop=900:900:(iw-900)*{x}:(ih-900)*{y},setsar=1','-frames:v','1',str(tmp/f'{j}.png')],check=True)
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(tmp/'0.png'),str(ROOT/f'assets/{slug}-editorial-hero-still.jpg')],check=True)
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-framerate','1/3','-i',str(tmp/'%d.png'),'-filter_complex','split[a][b];[a]palettegen=stats_mode=full[p];[b][p]paletteuse=dither=sierra2_4a','-loop','0',str(out)],check=True)
def render(slug,make_hero=True):
 name,n,state,indices,labels=CONFIG[slug]
 d=json.loads((ROOT/f'tools/data/{name}-editorial.json').read_text(encoding='utf-8'))
 ims=photos(d['blocks'])
 if make_hero:hero(slug,ims,indices)
 if labels:
  for b,label in zip([b for b in d['blocks'] if b['kind']=='heading'],labels):b['label']=label
  d.update(intro='第一次开电车跑长途，穿过雨雾抵达罗阿诺克，再跑进蓝岭山，完成第24州。',map=d.get('map','../../assets/wechat-run50-map-blue-ridge-24-editorial.png?v=feather-1'),poster=d.get('poster','../../assets/wechat-blue-ridge-poster.png'))
 css=re.search(r'<style>(.*?)</style>',style.render(),re.S).group(1)
 css+='\nmain{padding-left:20px;padding-right:20px}.cover{margin-left:0;margin-right:0}.intro,.chapter{margin-left:0;margin-right:0}.photo-strip img{display:block;width:100%;height:auto;margin:0}.photo-strip figcaption{margin-top:10px;text-align:center;font-size:12px;line-height:1.75;color:#888}.photo-strip{margin:32px 0 36px}'
 brand='<picture class="brand-intro"><source media="(prefers-reduced-motion: reduce)" srcset="../../assets/run50-cutout-intro-light-still.png" data-light-src="../../assets/run50-cutout-intro-light-still.png" data-dark-src="../../assets/run50-cutout-intro-dark-still.png"><img src="../../assets/run50-cutout-intro-light.gif" data-light-src="../../assets/run50-cutout-intro-light.gif" data-dark-src="../../assets/run50-cutout-intro-dark.gif" alt="Run50 机器人片头" width="280" height="350"></picture>'
 body=[f'<header class="masthead"><h1>{escape(d["title"])}</h1><p class="byline">文字 / Arsenan</p></header>',brand,f'<figure class="cover"><picture><source media="(prefers-reduced-motion: reduce)" srcset="../../assets/{slug}-editorial-hero-still.jpg?v=20261008-crop"><img src="../../assets/{slug}-editorial-hero.gif?v=20261008-crop" width="900" height="900" alt="{state}跑马与旅行"></picture><figcaption class="hero-credit">跑马与旅行 · 照片来源及署名见正文</figcaption></figure>',f'<div class="down" aria-hidden="true">⌄<br>⌄<br>⌄</div><section class="intro"><p>{escape(d["intro"])}</p></section>',f'<figure class="photo-strip map-poster"><img src="{escape(d["map"])}" alt="Run50 {state}地图"><img src="{escape(d["poster"])}" alt="{state}赛事海报"><figcaption>Run50 · {state} · 第{n}州'+('番外' if n==1 else '')+'<br>制图 / Arsenan</figcaption></figure>']
 count=0;blocks=groups(d['blocks'])
 for b in blocks:
  if b['kind']=='heading':
   count+=1;body.append(f'<header class="chapter"><span class="chapter-number">{count:02}</span><p class="chapter-label">{escape(b["label"])}</p><h2>{escape(b["title"])}</h2></header>')
  elif b['kind']=='paragraph':body.append(emphasize(b['html']).replace('<p>','<p class="prose" style="margin:0 0 22px;font-size:15px;line-height:1.95;letter-spacing:.5px;text-align:justify">',1))
  elif b['kind']=='figure':body.append(template.figure(b['src'],b['alt'],caption(b['caption'])))
  else:
   lines=[caption(x.get('caption','')) for x in b['images']]
   if not any(lines):lines=[caption(b.get('caption',''))]
   body.append('<figure class="photo-strip">'+''.join(f'<img src="{escape(x["src"])}" alt="{escape(x.get("alt",""))}" loading="lazy">' for x in b['images'])+'<figcaption>'+'<br>'.join(escape(x) for x in lines if x)+'</figcaption></figure>')
 series,title,closing=ENDINGS[slug]
 body.append(f'<footer class="ending"><p class="end-mark">本文完</p><p class="series">RUN50 · {series}</p><h2>{title}</h2><p class="closing" style="margin:0;padding:24px 0 0;text-align:center;font-size:13px;line-height:1.9">{closing}</p><p class="credits">文字 / Arsenan<br>摄影 / 见图片署名</p></footer>')
 nav=f'<nav class="copy-tools"><a href="../../CN/" style="color:inherit">Run50 目录</a><a href="{slug}-magazine-wechat.html" style="color:inherit">旅行杂志版</a><span>摄影杂志版</span><button class="theme-choice" data-theme-choice="light" aria-pressed="true" type="button">白底</button><button class="theme-choice" data-theme-choice="dark" aria-pressed="false" type="button">黑底</button><button id="copy-wechat" type="button">一键复制到公众号</button><span id="copy-status" role="status" aria-live="polite"></span></nav>'
 html='<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+escape(d['title'])+'</title><style>'+css+'</style></head><body>'+nav+'<main data-edition="'+slug+'-editorial">'+'\n'.join(body)+'</main><script src="../../assets/run50-six-editorial-copy.js?v=20261007" defer></script></body></html>'
 for suffix in ['modern-rail','editorial']:(ROOT/f'run50/wechat/{slug}-{suffix}.html').write_text(html,encoding='utf-8')
 print(slug,len(ims),'photos',sum(b['kind']=='photo-strip' for b in blocks),'strips',html.count('data-cn-tone'), 'accents',html.count('data-cn-emphasis="underline"'),'underlines')
if __name__=='__main__':
 for slug in CONFIG:render(slug)
 js=(ROOT/'assets/louisiana-wechat-copy.js').read_text(encoding='utf-8')
 js=js.replace("const canonical = 'https://zhennanzhang.com/run50/wechat/louisiana-marathon-editorial.html';","const canonical = 'https://zhennanzhang.com' + location.pathname;")
 js=re.sub(r"          const photo = url.match.*?if \(url.includes\('wechat-louisiana-poster\.'\)\) url = base \+ 'poster.jpg';\n",'',js,flags=re.S)
 (ROOT/'assets/run50-six-editorial-copy.js').write_text(js,encoding='utf-8')
 index=ROOT/'CN/index.html';s=index.read_text(encoding='utf-8')
 for slug in CONFIG:s=re.sub(re.escape(slug)+r'-modern-rail.html\?v=[^"\s]+',slug+'-modern-rail.html?v=20261008-complete',s)
 index.write_text(s,encoding='utf-8')
