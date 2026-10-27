"""Build Lhasa RunCN editorial from the author's Vlog narration and 135 selected photos."""
from pathlib import Path
from html import escape
import json,re,shutil
from PIL import Image,ImageOps
import build_wechat_louisville_editorial as style
from normalize_wechat_presentation import normalize
ROOT=Path(__file__).resolve().parents[1]
ASSET=ROOT/'assets/runcn-lhasa-2026'
SLUG='lhasa-half-marathon'
TITLE='RunCN #第29站｜西藏拉萨半程马拉松｜在日光之城，跑到布达拉宫脚下'
COVER_SRC='/assets/runcn-lhasa-cover-20261011.jpg'
POSTER_SRC='/assets/runcn-lhasa-article-poster-20261011.jpg'
assert COVER_SRC!=POSTER_SRC
OFFICIAL_PHOTOS=set('18-3-1 18-5-0 18-5-1 18-5-2 18-7 19-4 19-5 19-8-0-1 20-0 20-5 21-0'.split())
KEYS='拉萨 西藏 RunCN 布达拉宫 八廓街 大昭寺 青藏铁路 西宁 格尔木 牛肉包 雪城民宿 田村火锅鸡 藏戏面具 三十五块钱 山东小伙 警察 志愿者 三千六百六十米 二十一公里 高原 半马 氧气 拉萨河 会展中心 九公里 十四公里 十七 十八 十九 三小时多一点 奖牌 月亮 彩色流苏 煲仔饭 西瓜汁'.split()
UNDER=['Now or 可能就是 never','半马就半马呗','这时候有多自信，后面就有多喘','先吃饭，别的等会儿再说','话不能说太早','国内领个装备跟过节似的','实力不允许啊','照片和视频','凌晨一点半','第三个派出所','惊喜，惊喜，还TM是惊喜','不舒服就退赛','来都来了，多拍几张呗','该喘还是喘','配速自然是没眼看了','照片不能太狼狈','已经关门了','闲鱼淘一块二手的','这趟没白折腾','我用手比个3','飞机等了我们','第二天继续上班','一点不后悔','云散日朗，人意山光，俱有喜态','何妨吟啸且徐行','每时每刻都是夕阳也都是旭日']
KEYS += ['史铁生','我与地坛','徐霞客','游天台山日记','苏轼','定风波','平安跑回来','金光灿灿','能留一张是一张','硬卧','C位','天南海北','自给自足','心凉了半截','好心人','两个半小时到三个半小时','绿色阿森纳球衣','二十几个人','人生愿望清单']
KEYS += ['郑钧','回到拉萨','韩红','天路','巴桑','屈塬','印青','赵雷','大冰','王维','仓央嘉措','龙仁青','唐东杰布','温巴','20周年']
SOURCES = [
 ('郑钧谈《回到拉萨》创作', 'https://ent.sina.com.cn/y/2013-05-31/15533933658.shtml'),
 ('青藏铁路与唐古拉车站 · 国家铁路局', 'https://source.nra.gov.cn/tlfc/tpsy/202204/t20220405_292987.shtml'),
 ('拉萨地理与气候 · 中国天气网', 'https://www.weather.com.cn/cityintro/101140101.shtml'),
 ('宗角禄康公园 · 中国科学院地理资源所', 'https://igsnrr.cas.cn/cbkx/kpyd/kcsj/kksj/202009/t20200910_5693305.html'),
 ('布达拉宫历史建筑群 · UNESCO', 'https://whc.unesco.org/en/list/707'),
 ('布达拉宫粉刷季 · 西藏自治区文旅厅', 'https://wlt.xizang.gov.cn/xwzx_69/xydt/202310/t20231023_381924.html'),
 ('海拔与紫外线 · 香港天文台', 'https://www.hko.gov.hk/sc/wxinfo/uvinfo/uvinfo.html'),
 ('2026拉萨半程马拉松开赛与路线 · 拉萨市政府', 'https://lasa.gov.cn/lasa/ldhd/202608/be3f762ce1834559ac0b66a44de0dde2.shtml'),
 ('藏戏及其面具艺术 · 中国非遗网', 'https://www.ihchina.cn/Article/Index/detail?id=8234'),
 ('贡嘎县自然地理 · 贡嘎县政府', 'https://www.gongga.gov.cn/zjgg/gggk/zrdl/202607/t20260727_173987.html'),
 ('《天路》的词曲与首唱 · 央视网', 'https://www.cctv.com/performance/20060721/100912.shtml'),
 ('韩红谈姥姥的乘车愿望 · 澎湃新闻专访', 'https://m.voc.com.cn/xhn/news/202302/15767231.html'),
 ('赵雷谈赴拉萨经历 · 音乐财经专访', 'https://www.jiemian.com/article/1125309.html'),
 ('大冰谈小屋与流浪歌手 · 环球人物专访', 'https://paper.people.com.cn/hqrw/html/2016-09/16/content_1726801.htm'),
 ('仓央嘉措诗歌新译 · 龙仁青译，花城出版社', 'https://houtai.tibetcul.com/wx/ctwx/csgy/27193.html'),
 ('唐东杰布与七姐妹的藏戏故事 · 西藏自治区文旅厅', 'https://wlt.xizang.gov.cn/xwzx_69/wlyw/wldt/202308/t20230815_370947.html'),
 ('王维《终南别业》 · 古诗文网', 'https://www.gushiwen.cn/shiwenv_cd7027786b98.aspx'),
 ('史铁生《我与地坛》第七节', 'https://www.xuges.com/ddmj/sts/wydt/07.htm'),
 ('徐霞客《游天台山日记》', 'https://m.gushiwen.cn/guwen/bookv_ce90629b5932.aspx'),
 ('苏轼《定风波·莫听穿林打叶声》', 'https://www.gushiwen.cn/shiwenv_6b30455fdd3c.aspx'),
]
UNDER += ['那是一条神奇的天路','行到水穷处，坐看云起时','因为它在我心里是最远的地方','在那东山顶上，升起皎洁月亮']
def emphasize(text):
 parts=re.split('('+'|'.join(map(re.escape,sorted(set(KEYS+UNDER),key=len,reverse=True)))+')',text)
 html=''.join(('<strong data-cn-tone="'+str(sum(map(ord,t))%4)+'"'+(' data-cn-emphasis="underline"' if t in UNDER else '')+'>'+escape(t)+'</strong>') if i%2 else escape(t) for i,t in enumerate(parts))
 for n,(label,url) in enumerate(SOURCES,1):
  html=html.replace(f'〔{n}〕',f'<a class="fact-ref" href="{url}" title="{escape(label)}">〔{n}〕</a>')
 return html
def prepare():
 cap=dict(l.split('|',1) for l in (ROOT/'tools/data/lhasa-captions.txt').read_text(encoding='utf-8').splitlines() if l.strip())
 photo={}
 for key,c in cap.items():
  p=ASSET/f'Lhsa-{key}.webp'
  with Image.open(p) as im:w,h=im.size
  photo[key]={'kind':'figure','src':'/assets/runcn-lhasa-2026/'+p.name,'alt':c,'caption':c+' · 摄影 / '+('官方摄影' if key in OFFICIAL_PHOTOS else 'Arsenan'),'width':w,'height':h,'source_file':f'Lhsa-{key}.jpg'}
 blocks=[];used=[];paras=[]
 for line in (ROOT/'tools/data/lhasa-story-20261026.txt').read_text(encoding='utf-8').splitlines():
  if not line.strip():continue
  if line.startswith('# '):
   label,title=line[2:].split('｜',1);blocks.append({'kind':'heading','label':label,'title':title})
  elif line.startswith('@'):
   for key in line[1:].split():blocks.append(photo[key]);used.append(key)
  else:paras.append(line);blocks.append({'kind':'paragraph','html':'<p>'+emphasize(line)+'</p>'})
 sources={p.stem.removeprefix('Lhsa-') for p in ASSET.glob('Lhsa-*.webp')}
 assert len(used)==len(set(used))==135 and set(used)==sources==set(cap),(len(used),sources-set(used),set(used)-sources)
 d={'title':TITLE,'intro':'想去拉萨的念头来了十几次，这回终于买了票。坐青藏铁路，逛布达拉宫，半夜找回相机，第二天再去跑个半马。','source_photo_count':135,'source_subtitles':'作者2026年10月26日三段完整口述，结合原45分钟Vlog与135张照片','original_paragraphs':paras,'ending_paragraphs':[],'blocks':blocks}
 (ROOT/'tools/data/lhasa-editorial.json').write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
 return d
def assets():
 for name in ['intro-light.gif','intro-dark.gif','intro-light-still.png','intro-dark-still.png']:
  shutil.copyfile(ROOT/'assets/runcn-chuxiong-2026'/name,ASSET/name)
 frames=[]
 for key,center in [('18-5-0',(.5,.08)),('05-0',(.5,.4)),('09-2',(.5,.3)),('15-7',(.5,.25)),('17-0',(.5,.2)),('19-1',(.5,.2)),('21-0',(.5,.08)),('22-1',(0,.3)),('22-3',(.5,.15))]:
  with Image.open(ASSET/f'Lhsa-{key}.webp') as im:frames.append(ImageOps.fit(im.convert('RGB'),(900,900),centering=center))
 frames[0].save(ASSET/'hero-still.jpg',quality=95)
 frames[0].save(ASSET/'hero-9photos-20261011.gif',save_all=True,append_images=frames[1:],duration=2800,loop=0,optimize=False)

def render(d):
 css=re.search(r'<style>(.*?)</style>',style.render(),re.S).group(1)
 css+='''\nmain{padding-left:20px;padding-right:20px}.cover,.intro,.chapter{margin-left:0;margin-right:0}.photo-strip{margin:32px 0 36px}.photo-strip img{display:block;width:100%;height:auto;margin:0}.photo-strip figcaption,figure figcaption{margin:10px 0 0;text-align:center;font-size:12px;line-height:1.8;color:var(--muted)}.brand-intro{display:block;text-align:center;margin:0 auto 14px}.brand-intro img{display:inline-block;width:128px;height:128px}.cover img{display:block;width:100%;height:auto;aspect-ratio:1}.location-poster img{width:100%;height:auto}.location-poster img:first-child{width:100%;max-width:100%;box-sizing:border-box;padding:0;background:#f3efdf;margin:0}.source-note{font-size:11px;line-height:1.8;color:var(--muted);margin-top:24px}.source-note a{color:inherit}.chapter-label{color:#b8452e}html[data-theme="dark"] .chapter-label{color:#ffd36e}.byline{line-height:2}.series{letter-spacing:3px}'''
 pfx='/assets/runcn-lhasa-2026/'
 body=[f'<header class="masthead"><h1>{escape(TITLE)}</h1><p class="byline">西藏拉萨 · 2026年8月23日<br>文字 / Arsenan</p></header>',
 f'<picture class="brand-intro"><source media="(prefers-reduced-motion: reduce)" srcset="{pfx}intro-light-still.png" data-light-src="{pfx}intro-light-still.png" data-dark-src="{pfx}intro-dark-still.png"><img src="{pfx}intro-light.gif" data-light-src="{pfx}intro-light.gif" data-dark-src="{pfx}intro-dark.gif" alt="RunCN 山路片头" width="280" height="280"></picture>',
 f'<figure class="cover"><picture><source media="(prefers-reduced-motion: reduce)" srcset="{pfx}hero-still.jpg"><img src="{pfx}hero-9photos-20261011.gif" width="900" height="900" alt="进藏列车、布达拉宫、拉萨半马与藏戏奖牌" fetchpriority="high"></picture><figcaption>坐着火车进藏，跑到布达拉宫脚下<br>摄影 / Arsenan、官方摄影</figcaption></figure>',
 '<div class="down" aria-hidden="true">⌄<br>⌄<br>⌄</div>',f'<section class="intro"><p>{emphasize(d["intro"])}</p></section>',
 f'<figure class="photo-strip location-poster"><img src="/assets/runcn-article-maps-20261022/lhasa-half-marathon.jpg" alt="RunCN 中国地图，藏戏面具与星标定位西藏拉萨"><img src="{POSTER_SRC}" alt="西藏拉萨 · 2026 · RunCN 29"><figcaption>西藏 · 拉萨 · RunCN 第29站<br>封面设计 / Arsenan × AI</figcaption></figure>']
 blocks=d['blocks'];i=0;n=0
 while i<len(blocks):
  b=blocks[i]
  if b['kind']=='heading':
   n+=1;body.append(f'<header class="chapter"><span class="chapter-number">{n:02}</span><p class="chapter-label">{b["label"]}</p><h2>{escape(b["title"])}</h2></header>')
  elif b['kind']=='paragraph':body.append(b['html'].replace('<p>','<p class="prose" style="margin:0 0 22px;font-size:15px;line-height:1.95;letter-spacing:.5px;text-align:justify">'))
  else:
   group=[b]
   while b['width']>b['height']*1.15 and i+1<len(blocks) and len(group)<3:
    nxt=blocks[i+1]
    if nxt['kind']!='figure' or nxt['width']<=nxt['height']*1.15:break
    group.append(nxt);i+=1
   body.append('<figure class="photo-strip">'+''.join(f'<img src="{x["src"]}" srcset="{x["src"].replace("/Lhsa-","/preview/Lhsa-")} 1600w" sizes="(max-width:677px) calc(100vw - 40px), 637px" data-copy-src="{x["src"]}" alt="{escape(x["alt"])}" width="{x["width"]}" height="{x["height"]}" loading="lazy" decoding="async" style="display:block;width:100%;height:auto">' for x in group)+'<figcaption>'+'<br>'.join(escape(x['caption']) for x in group)+'</figcaption></figure>')
  i+=1
 for p in d['ending_paragraphs']:body.append('<p class="prose" style="font-size:15px;line-height:1.95;text-align:justify">'+emphasize(p)+'</p>')
 body.append('<footer class="ending"><p class="end-mark">本文完</p><p class="series">RUNCN · 第29站 · 西藏拉萨</p><h2>在日光之城，跑到布达拉宫脚下</h2><p class="closing">坐过青藏铁路，走进布达拉宫，也跑到了这里的终点。</p><p class="credits">文字 / Arsenan<br>摄影 / Arsenan、官方摄影</p></footer>')
 body.append('<p class="source-note">背景资料：<br>'+ '<br>'.join(f'〔{i}〕<a href="{url}">{escape(label)}</a>' for i,(label,url) in enumerate(SOURCES,1)) + '<br>旅行与比赛经历根据作者2026年10月26日口述及原Vlog整理。</p>')
 nav='<nav class="copy-tools"><a href="/CN/#runcn-series" style="color:inherit">RunCN 目录</a><button class="theme-choice" data-theme-choice="light" aria-pressed="true" type="button">白底</button><button class="theme-choice" data-theme-choice="dark" aria-pressed="false" type="button">黑底</button><button id="copy-wechat" type="button">一键复制到公众号</button><span id="copy-status" role="status" aria-live="polite"></span></nav>'
 html='<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+escape(TITLE)+'</title><meta name="description" content="在日光之城，跑到布达拉宫脚下。135张照片，记录卧铺进藏、布宫夜色、相机失而复得和高原半马。"><meta property="og:image" content="https://zhennanzhang.com'+COVER_SRC+'"><style>'+css+'</style></head><body>'+nav+'<main data-edition="runcn-lhasa">'+'\n'.join(body)+'</main><script src="/assets/runcn-lhasa-copy.js?v=20261027-literary" defer></script></body></html>'
 html=html.replace('<main data-edition="runcn-lhasa">','<main data-edition="runcn-lhasa" data-copy-chunks>')
 def copy_size(match):
  tag=match[0]
  paths=re.findall(r'(?:src|data-copy-src|data-dark-src)="(/assets/[^"?]+)',tag)
  size=max(((ROOT/p.lstrip('/')).stat().st_size for p in paths if (ROOT/p.lstrip('/')).is_file()),default=0)
  return tag[:-1]+f' data-copy-bytes="{size}">'
 html=re.sub(r'<img\b[^>]*>',copy_size,html)
 html=normalize(html,SLUG+'-editorial.html')[0]
 for suffix in ['editorial','modern-rail']:(ROOT/f'run50/wechat/{SLUG}-{suffix}.html').write_text(html,encoding='utf-8')
 js=(ROOT/'assets/run50-six-editorial-copy.js').read_text(encoding='utf-8').replace('img.height = 120','img.height = 96')
 js=js.replace("if (tag === 'img' || number || down) {", "if (number) { const p=document.createElement('p'); p.textContent=node.textContent; p.style.cssText='font-family:Arial,sans-serif;font-size:74px;line-height:1;color:' + ink + ';margin:48px 0 14px;font-weight:400;'; return p; }\n      if (tag === 'img' || down) {")
 js=js.replace("node.getAttribute('data-' + theme + '-src') || node.getAttribute('src')", "node.getAttribute('data-' + theme + '-src') || node.getAttribute('data-copy-src') || node.getAttribute('src')")
 js=js.replace("        return img;", "        if (node.matches('.location-poster > img:first-child')) img.style.cssText='display:block;width:100%;max-width:100%;height:auto;box-sizing:border-box;padding:0;background:#f3efdf;margin:0;border:0;';\n        return img;")
 js=js.replace("status.textContent = scope.value === 'all' ? '已复制；如公众号截断，请选择分段复制' : '本段已复制，请按顺序粘贴到公众号';", "const mb = new Blob([html]).size / 1000000; status.textContent = '已复制 ' + mb.toFixed(2) + ' MB（原图未压缩）' + (mb >= 10 ? '；超过10MB，请分段复制' : '');")
 (ROOT/'assets/runcn-lhasa-copy.js').write_text(js,encoding='utf-8')
 print('Rendered',len(d['original_paragraphs']),'source paragraphs,',sum(b['kind']=='figure' for b in blocks),'photos')

if __name__=='__main__':
 import sys
 d=prepare()
 if '--assets' in sys.argv:assets()
 render(d)
