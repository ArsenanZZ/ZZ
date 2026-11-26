"""Harbin 2026: author video narrative, chronological photos, original-byte copying."""
from pathlib import Path
from html import escape
import json,re,shutil,sys
from PIL import Image,ImageOps
import build_wechat_louisville_editorial as style

ROOT=Path(__file__).resolve().parents[1]
SLUG='harbin-marathon-2026'
ASSET=ROOT/'assets/runcn-harbin-2026'
DATA=ROOT/'tools/data'
TITLE='RunCN #第31站｜黑龙江哈尔滨马拉松｜红肠配格瓦斯，跑完去吃排骨包'
COVER_SRC='/assets/runcn-harbin-2026/cover.jpg?v=20261024-tall-rail'
# User preference: homepage stays light lilac; article poster uses deeper layered purple clouds.
POSTER_SRC='/assets/runcn-harbin-2026/poster.jpg?v=20261120-trim'
INTRO_PARAGRAPHS = ['九月十四号，我要从哈尔滨飞回美国。一看日子，前一天正好是哈马。算上今年，我大概跑过四回哈马了。八月初刚回东北看过我爸我妈，这回跑完还能回家住一宿。', '比赛那天，我跑到太阳岛，隔着栏杆看见我爸我妈。往旁边一看，大娘也来了，表妹张鑫还带着她家甜馨。']
INTRO = ''.join(INTRO_PARAGRAPHS)
TONE_GROUPS = (
    '红肠 哈尔滨红肠 一身汗 锅包肉 红光 溜肉段 大红箱子 辣椒排骨 狍跑 张哥 我上哪儿追得上啊 太阳晒 锅包肉、一盘溜肉段',
    '湿地 水曲柳 小绿箱子 深绿色的桥塔 绿钟楼 红黄相间 能完赛我就挺高兴 全国制霸 来都来了 怎么还没跑完啊 跟C区一块儿出发 这还打什么车啊 慢慢吃、慢慢玩 张鑫 甜馨 能完赛就挺好 我跟我妈一起去合了影 东北人',
    '松花江 松花江边 松花江北岸 冰雪大世界 冰雪之冠 中东铁路桥 老江桥 防洪纪念塔 阳明滩大桥 雪花摩天轮 冰面上的裂纹 蓝色参赛服 太阳岛 太阳石广场 大剧院 一点水汽 冰裂纹 合唱班 小皇冠',
    '回家住一宿 家乡的马拉松 格瓦斯 张包铺 排骨包子 排骨包 果脯面包 大列巴 锅里还有我惦记的那几段玉米 马迭尔 猪脚饭 中央大街 中华巴洛克 顺德 青年宫 哈尔滨市青年宫 五小时零二分 家乡这一口 豆角排骨 三百多米 齐齐哈尔滨 刚领的小皇冠 三个月 我爷爷就爱去 坐地铁到老道外 发面馒头 我妈炖的豆角排骨',
)
UNDERLINED = {
    '能完赛我就挺高兴',
    '全国制霸',
    '来都来了',
    '怎么还没跑完啊',
    '我上哪儿追得上啊',
    '跟C区一块儿出发',
    '这还打什么车啊',
    '家乡的马拉松',
    '五小时零二分',
    '家乡这一口',
    '齐齐哈尔滨',
    '慢慢吃、慢慢玩',
    '锅里还有我惦记的那几段玉米',
    '能完赛就挺好',
    '我爷爷就爱去',
    '三个月',
    '我妈炖的豆角排骨',
    '刚领的小皇冠',
}
TONE_BY_PHRASE = {phrase: tone
                 for tone, group in enumerate(TONE_GROUPS)
                 for phrase in group.split()}
EMPHASIS_PATTERN = re.compile('(' + '|'.join(re.escape(phrase) for phrase in
                              sorted(TONE_BY_PHRASE, key=len, reverse=True)) + ')')


def em(text):
    pieces = []
    for part in EMPHASIS_PATTERN.split(text):
        if part not in TONE_BY_PHRASE:
            pieces.append(escape(part))
            continue
        underline = ' data-cn-emphasis="underline"' if part in UNDERLINED else ''
        tone = TONE_BY_PHRASE[part]
        pieces.append(f'<strong data-cn-tone="{tone}"{underline}>{escape(part)}</strong>')
    return ''.join(pieces)


def prepare_assets():
 ASSET.mkdir(exist_ok=True);(ASSET/'photos').mkdir(exist_ok=True);(ASSET/'preview').mkdir(exist_ok=True)
 meta=json.loads((ROOT/'tmp/harbin-2026/photo-index.json').read_text(encoding='utf-8'))
 for p in meta:
  key=p['id'][1:];src=ROOT/'tmp/harbin-2026/photos'/p['name'];dst=ASSET/'photos'/p['name']
  if not dst.exists():shutil.copyfile(src,dst)
  preview=ASSET/'preview'/f'{key}.jpg'
  if not preview.exists():
   with Image.open(src) as im:
    im=ImageOps.exif_transpose(im).convert('RGB');im.thumbnail((1600,1600));im.save(preview,quality=92)
 (DATA/'harbin-2026-photos.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')
 import build_remaining_series_editorials as series
 series.SELECT[SLUG]={'light':'#753d99','dark':'#d0a4ed'};series.mountain_intro(SLUG)
 frames=[]
 for n,center in [(30,(.5,.3)),(164,(.5,.18)),(160,(.5,.5)),(52,(.5,.3)),(112,(.5,.25)),(130,(.5,.35)),(141,(.5,.35)),(158,(1,.5)),(156,(.5,.5)),(166,(.05,.5))]:
  with Image.open(ASSET/'photos'/meta[n-1]['name']) as im:frames.append(ImageOps.fit(ImageOps.exif_transpose(im).convert('RGB'),(900,900),centering=center))
 frames[0].save(ASSET/'hero-still.jpg',quality=95)
 frames[0].save(ASSET/'hero.gif',save_all=True,append_images=frames[1:],duration=3000,loop=0,optimize=False)

def render():
 caps=dict(x.split('|',1) for x in (DATA/'harbin-2026-captions.txt').read_text(encoding='utf-8').splitlines() if x.strip())
 meta={p['id'][1:]:p for p in json.loads((DATA/'harbin-2026-photos.json').read_text(encoding='utf-8'))}
 official=set(f'{i:03}' for i in [*range(109,119),139,141])
 css=re.search(r'<style>(.*?)</style>',style.render(),re.S)[1]
 css+='''main{padding-left:20px;padding-right:20px}.cover,.intro,.chapter{margin-left:0;margin-right:0}.photo-strip{margin:26px 0 30px}.photo-strip img{display:block;width:100%;height:auto;margin:0}.photo-strip figcaption,figure figcaption{margin:10px 0 0;text-align:center;font-size:12px;line-height:1.8;color:var(--muted)}.brand-intro{display:block;text-align:center;margin:0 auto 14px}.brand-intro img{display:inline-block;width:110px;height:110px}.cover img{display:block;width:100%;height:auto;aspect-ratio:1}.location-poster{background:#f0ede4}.location-poster img{display:block;width:100%;max-width:100%;height:auto;padding:0;margin:0;border:0;box-sizing:border-box}.location-poster figcaption{background:var(--paper);margin:0;padding-top:10px}.source-note{font-size:11px;line-height:1.8;color:var(--muted);margin-top:24px}.source-note a{color:inherit}.chapter-label{color:#753d99}html[data-theme="dark"] .chapter-label{color:#d0a4ed}.byline{line-height:2}.series{letter-spacing:3px}.prose{margin:0 0 22px;font-size:15px;line-height:1.95;letter-spacing:.5px;text-align:justify}'''
 intro='/assets/series-intros-20261020/'+SLUG+'/'
 out=[f'<header class="masthead"><h1>{TITLE}</h1><p class="byline">黑龙江哈尔滨 · 2026年9月13日<br>文字 / Arsenan</p></header>',f'<picture class="brand-intro"><source media="(prefers-reduced-motion: reduce)" srcset="{intro}light-still.png?v=20261024-transparent" data-light-src="{intro}light-still.png?v=20261024-transparent" data-dark-src="{intro}dark-still.png?v=20261024-transparent"><img src="{intro}light.gif?v=20261024-transparent" data-light-src="{intro}light.gif?v=20261024-transparent" data-dark-src="{intro}dark.gif?v=20261024-transparent" width="280" height="280" alt="紫色 RunCN 山路片头"></picture>',
 '<figure class="cover"><picture><source media="(prefers-reduced-motion: reduce)" srcset="/assets/runcn-harbin-2026/hero-still.jpg"><img src="/assets/runcn-harbin-2026/hero.gif?v=20261120-medal-guobaorou" width="900" height="900" fetchpriority="high" alt="哈马完赛奖牌、张包铺锅包肉、紫衣跑马和家人合影"></picture><figcaption>回哈尔滨，跑一场家乡的马拉松<br>摄影 / Arsenan、官方摄影</figcaption></figure>',
 '<div class="down" aria-hidden="true">⌄<br>⌄<br>⌄</div>','<section class="intro">'+''.join('<p class="prose">'+em(p)+'</p>' for p in INTRO_PARAGRAPHS)+'</section>']
 location_poster=f'<figure class="photo-strip location-poster"><img src="/assets/runcn-article-maps-20261022/{SLUG}.jpg?v=20261024-north-callout" alt="RunCN 第31站历史足迹，定位黑龙江哈尔滨"><img src="{POSTER_SRC}" alt="黑龙江哈尔滨，紫色雨中双桥与大剧院，2026 RunCN31"><figcaption>黑龙江 · 哈尔滨 · RunCN 第31站<br>制图 / Arsenan · 封面设计 / Arsenan × AI</figcaption></figure>'
 used=[];blocks=[];n=0
 for line in (DATA/'harbin-2026-story.txt').read_text(encoding='utf-8').splitlines():
  if not line.strip():continue
  if line.startswith('# '):
   if n==0:out.append(location_poster)
   title=line[2:];n+=1;out.append(f'<header class="chapter"><span class="chapter-number">{n:02}</span><h2>{escape(title)}</h2></header>');blocks.append({'kind':'heading','label':'','title':title})
  elif line.startswith('@'):
   keys=line[1:].split();used+=keys
   assert 1<=len(keys)<=3
   images=[];credits=[]
   for key in keys:
    p=meta[key];credit='官方摄影' if key in official else 'Arsenan';credits.append(credit)
    src='/assets/runcn-harbin-2026/photos/'+p['name'];preview='/assets/runcn-harbin-2026/preview/'+key+'.jpg'
    images.append(f'<img src="{src}" srcset="{preview} 1600w" sizes="(max-width:677px) calc(100vw - 40px), 637px" data-copy-src="{src}" data-photo-id="{key}" alt="{escape(caps[key])}" width="{p["width"]}" height="{p["height"]}" loading="lazy" decoding="async">')
   if len(set(credits))==1:caption='；'.join(caps[k] for k in keys)+' · 摄影 / '+credits[0]
   else:caption='；'.join(caps[k]+' · 摄影 / '+c for k,c in zip(keys,credits))
   out.append('<figure class="photo-strip">'+''.join(images)+'<figcaption>'+escape(caption)+'</figcaption></figure>');blocks.append({'kind':'photos','ids':keys,'credits':credits})
  else:out.append('<p class="prose">'+em(line)+'</p>');blocks.append({'kind':'paragraph','text':line})
 assert len(used)==len(set(used))==198 and set(used)==set(meta)==set(caps)
 km={'098':5,'097':6,'101':7,'106':10,'119':14,'121':17,'132':28,'137':36,'140':37,'148':42}
 progress=[km[k] for k in used if k in km];assert progress==sorted(progress)
 out.append('<footer class="ending"><p class="end-mark">本文完</p><p class="series">RUNCN · 第31站 · 黑龙江哈尔滨</p><p class="credits">文字 / Arsenan<br>摄影 / Arsenan、官方摄影</p></footer>')
 out.append('<p class="source-note">旅行及比赛经历依据作者哈尔滨原始视频口述与选图整理，完赛时间为个人记录约5小时02分。背景资料：<a href="https://wlt.hlj.gov.cn/wlt/c114169/202609/c00_31972491.shtml">赛事、吉祥物及奖牌介绍</a> · <a href="https://wlt.hlj.gov.cn/wlt/c114169/202404/c00_31731149.shtml">中华巴洛克建筑</a> · <a href="https://www.weather.com.cn/heilongjiang/shtq/lyjd/05/436022.shtml">防洪纪念塔</a> · <a href="https://cdn.archilovers.com/projects/bc1fb6ff-4680-40be-9e7a-53e065a51ce0.pdf">哈尔滨大剧院设计</a> · <a href="https://harbin.joyhua.cn/hebrb/20260913/mhtml/page_01_content_20260913002002.htm">四枪出发和参赛规模</a> · <a href="https://www.imharbin.com/post/51743">中央大街的面包石</a> · <a href="https://m.fx361.com/news/2010/0706/21032307.html">哈尔滨段历史洪水</a> · <a href="https://www.hrbdag.org.cn/hbfm/hbsh/2026/01/20944.html">老江桥与新铁路桥</a> · <a href="https://m.thepaper.cn/newsDetail_forward_30832900">丁香与哈尔滨</a> · <a href="https://m.thepaper.cn/newsDetail_forward_28505044">音乐长廊和沿途地标</a> · <a href="https://www.sucdri.com/case/casedetails-161.html">阳明滩大桥设计</a> · <a href="https://i-mad.cn/zh/projects/harbin-opera-house">MAD哈尔滨大剧院</a> · <a href="https://wlt.hlj.gov.cn/wlt/c114165/202307/c00_31646684.shtml">雪花摩天轮</a> · <a href="https://www.aisixiang.com/data/16911.html">迟子建《起舞》</a> · <a href="https://www.aisixiang.com/data/120166.html">鲁迅《小杂感》</a> · <a href="https://zh.wikisource.org/zh-hans/呼蘭河傳/第一章">萧红《呼兰河传》</a> · <a href="https://www.chinawriter.com.cn/n1/2025/1204/c404063-40617346.html">卞之琳《断章》</a> · <a href="https://www.chinawriter.com.cn/n1/2017/1214/c404014-29706815.html">汪曾祺《端午的鸭蛋》引文</a> · <a href="https://www.hljszw.org.cn/home/book/info/get_id/402175.html">中东铁路的修筑</a> · <a href="https://lzhbwg.mofcom.gov.cn/edi_ecms_web_front/thb/detail/5f9c6f49bdce4168b2e0a599dbc2f55b">华梅西餐厅沿革</a> · <a href="https://hrbcredit.harbin.gov.cn/creditMess.do?conId=f6d9f6e28c524902a94a9c351b631a54&amp;method=showDetailHtml">秋林格瓦斯与大列巴</a>。插画为地标组合，并非实地空间比例。</p>')
 nav='<nav class="copy-tools"><a href="/CN/#runcn-series" style="color:inherit">RunCN 目录</a><button data-theme-choice="light" aria-pressed="true">白底</button><button data-theme-choice="dark" aria-pressed="false">黑底</button><button id="copy-wechat">一键复制到公众号</button><span id="copy-status" role="status" aria-live="polite"></span></nav>'
 html=f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{TITLE}</title><meta name="description" content="{escape(INTRO)}"><meta property="og:image" content="https://zhennanzhang.com{COVER_SRC}"><style>{css}</style></head><body>{nav}<main data-edition="runcn-harbin-2026">'+ '\n'.join(out)+'</main><script src="/assets/run50-six-editorial-copy.js?v=20261022-original-quality" defer></script></body></html>'
 for suffix in ['editorial','modern-rail']:(ROOT/f'run50/wechat/{SLUG}-{suffix}.html').write_text(html,encoding='utf-8')
 (DATA/'harbin-2026-editorial.json').write_text(json.dumps({'slug':SLUG,'title':TITLE,'intro':INTRO,'blocks':blocks,'photo_count':198},ensure_ascii=False,indent=2),encoding='utf-8')
 print('Harbin:',n,'chapters;',len(used),'photos; kilometer sequence:',progress)

if __name__=='__main__':
 if '--assets' in sys.argv:prepare_assets()
 render()
