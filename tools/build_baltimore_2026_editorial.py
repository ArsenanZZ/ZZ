"""Baltimore oral-history article with chronological original-quality photographs."""
from pathlib import Path
from html import escape
import json,re
from bs4 import BeautifulSoup
from PIL import Image,ImageOps
import build_wechat_louisville_editorial as style

ROOT=Path(__file__).resolve().parents[1]
SLUG='baltimore-marathon-2026'
ASSET=ROOT/'assets/run50-baltimore-2026'
DATA=ROOT/'tools/data'
TITLE='Run50 #第37州｜马里兰巴尔的摩马拉松｜跑过内港的风，带走一只金螃蟹'
COVER_SRC='/assets/run50-baltimore-2026/cover.jpg?v=20261024'
POSTER_SRC='/assets/run50-baltimore-2026/poster.jpg?v=20261024'
INTRO='第三次来巴尔的摩，这次不开会，也不培训。我和Siqi开了一天车，来完成Run50的第37州。先把这只金螃蟹跑回来，明天还有新泽西。'
KEYS=['切萨皮克湾','美国缩影','Annapolis','蓝蟹','巴尔的摩','马里兰','Siqi','阿森纳','第37州','Inner Harbor','Power Plant','Lake Montebello','Druid Hill Park','Clifton Park','金螃蟹','二十英里','二十一英里','四十一公里','醉心工作','尿点和充电','无缝衔接','Cold gas','Be Kind','BE KIND','金螃蟹','分苹果','Roadster','Clifton Park Valve House','Lake Montebello','Ravens Walk','Atlantic City','路易维尔']
UNDER=['这次不开会，也不培训','尿点和充电无缝衔接','别人等起跑，我研究飞车','腿累是腿累，照片不能不拍','螃蟹奖牌能翻盖','一个trip拿下两个州','马里兰，第37州，拿下了']
def em(t):
    parts=re.split('('+'|'.join(map(re.escape,sorted(KEYS+UNDER,key=len,reverse=True)))+')',t)
    return ''.join('<strong data-cn-tone="'+str(sum(map(ord,v))%4)+'"'+(' data-cn-emphasis="underline"' if v in UNDER else '')+'>'+escape(v)+'</strong>' if i%2 else escape(v) for i,v in enumerate(parts))
def render():
    caps=dict(x.split('|',1) for x in (DATA/'baltimore-2026-captions.txt').read_text(encoding='utf8').splitlines() if x.strip())
    meta={p['id'][1:]:p for p in json.loads((DATA/'baltimore-2026-photos.json').read_text(encoding='utf8'))}
    official={f'{i:03}' for i in [63,64,68,69,98,100,114,115,116,123,124,125,126]}
    siqi={'017'}
    css=re.search(r'<style>(.*?)</style>',style.render(),re.S)[1]
    css+='''main{padding-left:20px;padding-right:20px}.cover,.intro,.chapter{margin-left:0;margin-right:0}.photo-strip{margin:26px 0 30px}.photo-strip img{display:block;width:100%;height:auto;margin:0}.photo-strip figcaption,figure figcaption{margin:10px 0 0;text-align:center;font-size:12px;line-height:1.8;color:var(--muted)}.brand-intro{display:block;text-align:center;margin:0 auto 14px}.brand-intro img{display:inline-block;width:112px;height:140px}.cover img{display:block;width:100%;height:auto;aspect-ratio:1}.location-poster{background:#f3efdf}.location-poster img{display:block;width:100%;height:auto;margin:0;padding:0;border:0;box-sizing:border-box}.location-poster figcaption{background:var(--paper);margin:0;padding-top:10px}.source-note{font-size:11px;line-height:1.8;color:var(--muted);margin-top:24px}.source-note a{color:inherit}.chapter-label{color:#9d5930}html[data-theme="dark"] .chapter-label{color:#e5bd7e}.byline{line-height:2}.prose{margin:0 0 22px;font-size:15px;line-height:1.95;letter-spacing:.5px;text-align:justify}'''
    intro='/assets/run50-shirt-intros/'+SLUG+'/'
    out=[f'<header class="masthead"><h1>{TITLE}</h1><p class="byline">马里兰 · 巴尔的摩 · 2026年10月17日<br>文字 / Arsenan</p></header>',f'<picture class="brand-intro"><source media="(prefers-reduced-motion: reduce)" srcset="{intro}light-still.png" data-light-src="{intro}light-still.png" data-dark-src="{intro}dark-still.png"><img src="{intro}light.gif" data-light-src="{intro}light.gif" data-dark-src="{intro}dark.gif" width="280" height="350" alt="黑色球衣配色的 Run50 片头"></picture>',
    '<figure class="cover"><picture><source media="(prefers-reduced-motion: reduce)" srcset="/assets/run50-baltimore-2026/hero-still.jpg?v=20261024-medal"><img src="/assets/run50-baltimore-2026/hero.gif?v=20261024-medal" width="900" height="900" fetchpriority="high" alt="巴尔的摩赛前合影、沿途跑步与完赛留影"></picture><figcaption>黑色阿森纳，内港边的一场马拉松<br>摄影 / Arsenan、官方摄影、现场跑友</figcaption></figure>',
    '<div class="down" aria-hidden="true">⌄<br>⌄<br>⌄</div>',f'<section class="intro"><p>{em(INTRO)}</p></section>',
    f'<figure class="photo-strip location-poster"><img src="/assets/run50-baltimore-2026/map.jpg" alt="截至第37州马里兰的 Run50 足迹，未点亮新泽西"><img src="{POSTER_SRC}" alt="马里兰巴尔的摩内港帆船与蓝蟹，2026 Run50 37"><figcaption>马里兰 · 巴尔的摩 · Run50 第37州<br>制图 / Arsenan · 封面设计 / Arsenan × AI</figcaption></figure>']
    used=[];blocks=[];n=0
    for line in (DATA/'baltimore-2026-story.txt').read_text(encoding='utf8').splitlines():
        if not line.strip():continue
        if line.startswith('# '):
            label,title=line[2:].split('｜',1);n+=1
            out.append(f'<header class="chapter"><span class="chapter-number">{n:02}</span><p class="chapter-label">{escape(label)}</p><h2>{escape(title)}</h2></header>');blocks.append({'kind':'heading','label':label,'title':title})
        elif line.startswith('@'):
            keys=line[1:].split();used+=keys;assert 1<=len(keys)<=3
            images=[];credits=[]
            for key in keys:
                p=meta[key];credits.append('官方摄影' if key in official else '现场跑友帮拍' if key in {'128','129','130'} else 'Siqi' if key in siqi else 'Arsenan')
                src='/assets/run50-baltimore-2026/photos/'+p['name'];preview='/assets/run50-baltimore-2026/preview/'+key+'.jpg'
                images.append(f'<img src="{src}" srcset="{preview} 1600w" sizes="(max-width:677px) calc(100vw - 40px), 637px" data-copy-src="{src}" data-photo-id="{key}" alt="{escape(caps[key])}" width="{p["width"]}" height="{p["height"]}" loading="lazy" decoding="async">')
            caption='；'.join(caps[k] for k in keys)+' · 摄影 / '+credits[0] if len(set(credits))==1 else '；'.join(caps[k]+' · 摄影 / '+c for k,c in zip(keys,credits))
            out.append('<figure class="photo-strip">'+''.join(images)+'<figcaption>'+escape(caption)+'</figcaption></figure>');blocks.append({'kind':'photos','ids':keys,'credits':credits})
        else:out.append('<p class="prose">'+em(line)+'</p>');blocks.append({'kind':'paragraph','text':line})
    assert len(used)==len(set(used))==142 and set(used)==set(meta)==set(caps)
    assert used.index('101')<used.index('104')<used.index('124')
    out.append('<footer class="ending"><p class="end-mark">本文完</p><p class="series">RUN50 · 第37州 · 马里兰</p><h2>金螃蟹收好，明天接着跑</h2><p class="closing">下一站，大西洋城。一个周末，跑两个州。</p><p class="credits">文字 / Arsenan<br>摄影 / Arsenan、Siqi、官方摄影、现场跑友</p></footer>')
    out.append('<p class="source-note">本文依据作者亲笔手稿、142张精选照片及已有视频审核记录整理。赛后视频自述用时约4小时56分，非另行核验的官方净成绩。背景资料：<a href="https://www.thebaltimoremarathon.com/Race/TheBaltimoreRunningFestival/Page/ScheduleofEvents">赛事日程与领物</a> · <a href="https://www.thebaltimoremarathon.com/Race/TheBaltimoreRunningFestival/Page/Marathon">路线与坡段</a> · <a href="https://www.nps.gov/cajo/planyourvisit/maryland.htm">马里兰地理</a> · <a href="https://msa.maryland.gov/msa/mdmanual/01glance/html/symbols/crab.html">州蓝蟹</a> · <a href="https://www.ntsb.gov/investigations/Pages/DCA24MM031.aspx">2024年大桥事故</a> · <a href="https://www.vicinityenergy.us/products-services/district-steam/">街道白汽</a> · <a href="https://www.promotionandarts.org/baltimore-mural-program/">社区壁画</a> · <a href="https://asr-group.com/news/Employees/Baltimore-Refinery-Celebrates-100-Years">Domino糖厂</a> · <a href="https://cafe.hardrock.com/baltimore/">Power Plant</a> · <a href="https://explore.baltimoreheritage.org/items/show/198">Clifton阀门房</a> · <a href="https://historicships.org/explore">内港历史船舶</a> · <a href="https://www.baltimorepolice.org/news/baltimore-police-department-releases-2025-mid-year-crime-report-and-key-highlights">近年治安数据</a> · <a href="https://www.tesla.com/roadster">Roadster</a>。未把个人经历当作全市安全判断。</p>')
    nav='<nav class="copy-tools"><a href="/CN/#run50-series" style="color:inherit">Run50 目录</a><button data-theme-choice="light" aria-pressed="true">白底</button><button data-theme-choice="dark" aria-pressed="false">黑底</button><button id="copy-wechat">一键复制到公众号</button><span id="copy-status" role="status" aria-live="polite"></span></nav>'
    html=f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{TITLE}</title><meta name="description" content="{INTRO}"><meta property="og:image" content="https://zhennanzhang.com{COVER_SRC}"><style>{css}</style></head><body>{nav}<main data-edition="run50-baltimore-2026" data-copy-chunks>'+'\n'.join(out)+'</main><script src="/assets/run50-six-editorial-copy.js?v=20261024-original-chunks" defer></script></body></html>'
    soup=BeautifulSoup(html,'html.parser')
    for img in soup.find_all('img'):
        candidates=[img.get('src',''),img.get('data-dark-src','')]
        img['data-copy-bytes']=str(max([0]+[(ROOT/u.split('?')[0].lstrip('/')).stat().st_size for u in candidates if u and (ROOT/u.split('?')[0].lstrip('/')).exists()]))
    html=str(soup)
    for suffix in ['editorial','modern-rail']:(ROOT/f'run50/wechat/{SLUG}-{suffix}.html').write_text(html,encoding='utf8')
    (DATA/'baltimore-2026-editorial.json').write_text(json.dumps({'slug':SLUG,'title':TITLE,'intro':INTRO,'blocks':blocks,'photo_count':142},ensure_ascii=False,indent=2),encoding='utf8')
    print(n,'chapters',len(used),'photos')
def hero():
    meta=json.loads((DATA/'baltimore-2026-photos.json').read_text(encoding='utf8'));frames=[]
    for n,center in [(134,(.5,.5)),(50,(.5,.3)),(64,(.5,0)),(88,(.5,.25)),(98,(.5,.25)),(129,(.5,.45))]:
        with Image.open(ASSET/'photos'/meta[n-1]['name']) as im:frames.append(ImageOps.fit(ImageOps.exif_transpose(im).convert('RGB'),(900,900),centering=center))
    frames[0].save(ASSET/'hero-still.jpg',quality=95)
    frames[0].save(ASSET/'hero.gif',save_all=True,append_images=frames[1:],duration=3000,loop=0,optimize=False)
if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--rebuild-hero',action='store_true',help='Explicitly rebuild the approved hero GIF and still')
    args=parser.parse_args()
    if args.rebuild_hero: hero()
    render()


