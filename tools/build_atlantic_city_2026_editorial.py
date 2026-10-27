"""Atlantic City oral-history article with chronological original-quality photographs."""
from pathlib import Path
from html import escape
import json,re
from bs4 import BeautifulSoup
from PIL import Image,ImageOps
import build_wechat_louisville_editorial as style

ROOT=Path(__file__).resolve().parents[1]
SLUG='atlantic-city-marathon-2026'
ASSET=ROOT/'assets/run50-atlantic-city-2026'
DATA=ROOT/'tools/data'
TITLE='Run50 #第38州｜新泽西大西洋城马拉松｜背靠背跑两州，从金螃蟹跑到小海龟'
COVER_SRC='/assets/run50-atlantic-city-2026/cover.jpg?v=20261025'
POSTER_SRC='/assets/run50-atlantic-city-2026/poster.jpg?v=20261025'
INTRO='巴尔的摩跑完，继续开往大西洋城。第二天换上绿色阿森纳，从酒店窗外的日出跑到海边木栈道，经过灯塔、摩天轮和一头大象；昨天跑坡，今天顶风，两天完成两场全马。'
KEYS=['花园之州','Garden State','人口密度最高','Trenton','大西洋城','新泽西','Siqi','阿森纳','第38州','Bally’s','Boardwalk','Absecon Lighthouse','Lucy','Margate','Longport','Ventnor','小海龟','金螃蟹','三十公里','二十英里','木栈道','摩天轮','Luna','Planet Fitness']
UNDER=['背靠背','先吃点热乎的','昨天才见过','跑三走一','把帽子反过来戴','今天只要顺利完成','从金螃蟹跑到小海龟','两天，两场全马']

SETTINGS=json.loads((DATA/'atlantic-city-2026-settings.json').read_text(encoding='utf8'))
INTRO=SETTINGS['intro']
KEYS=list(set(KEYS+SETTINGS['emphasis']))

def em(t):
    parts=re.split('('+'|'.join(map(re.escape,sorted(KEYS+UNDER,key=len,reverse=True)))+')',t)
    html=''.join('<strong data-cn-tone="'+str(sum(map(ord,v))%4)+'"'+(' data-cn-emphasis="underline"' if v in UNDER else '')+'>'+escape(v)+'</strong>' if i%2 else escape(v) for i,v in enumerate(parts))
    for label,url in SETTINGS['refs'].items():
        html=html.replace(label,'<a href="'+escape(url,quote=True)+'">'+label+'</a>')
    return html

def render():
    caps=dict(x.split('|',1) for x in (DATA/'atlantic-city-2026-captions.txt').read_text(encoding='utf8').splitlines() if x.strip())
    meta={p['id'][1:]:p for p in json.loads((DATA/'atlantic-city-2026-photos.json').read_text(encoding='utf8'))}
    official={f'{i:03}' for i in [141,142,143,144,145,146]}
    siqi={f'{i:03}' for i in [140,153,154,155,157,158,164,165]}
    confirmed_credits={'135':'路人','136':'路人','150':'现场跑友','151':'现场跑友','152':'现场跑友'}
    css=re.search(r'<style>(.*?)</style>',style.render(),re.S)[1]
    css+='''main{padding-left:20px;padding-right:20px}.cover,.intro,.chapter{margin-left:0;margin-right:0}.photo-strip{margin:26px 0 30px}.photo-strip img{display:block;width:100%;height:auto;margin:0}.photo-strip figcaption,figure figcaption{margin:10px 0 0;text-align:center;font-size:12px;line-height:1.8;color:var(--muted)}.brand-intro{display:block;text-align:center;margin:0 auto 14px}.brand-intro img{display:inline-block;width:112px;height:140px}.cover img{display:block;width:100%;height:auto;aspect-ratio:1}.location-poster{background:#f3efdf}.location-poster img{display:block;width:100%;height:auto;margin:0;padding:0;border:0;box-sizing:border-box}.location-poster figcaption{background:var(--paper);margin:0;padding-top:10px}.source-note{font-size:11px;line-height:1.8;color:var(--muted);margin-top:24px}.source-note a{color:inherit}.chapter-label{color:#9d5930}html[data-theme="dark"] .chapter-label{color:#e5bd7e}.byline{line-height:2}.prose{margin:0 0 22px;font-size:15px;line-height:1.95;letter-spacing:.5px;text-align:justify}'''
    intro='/assets/run50-shirt-intros/'+SLUG+'/'
    out=[f'<header class="masthead"><h1>{TITLE}</h1><p class="byline">新泽西 · 大西洋城 · 2026年10月18日<br>文字 / Arsenan</p></header>',f'<picture class="brand-intro"><source media="(prefers-reduced-motion: reduce)" srcset="{intro}light-still.png" data-light-src="{intro}light-still.png" data-dark-src="{intro}dark-still.png"><img src="{intro}light.gif" data-light-src="{intro}light.gif" data-dark-src="{intro}dark.gif" width="280" height="350" alt="绿色球衣配色的 Run50 片头"></picture>',
    '<figure class="cover"><picture><source media="(prefers-reduced-motion: reduce)" srcset="/assets/run50-atlantic-city-2026/hero-still.jpg?v=20261025-medal"><img src="/assets/run50-atlantic-city-2026/hero.gif?v=20261025-medal" width="900" height="900" fetchpriority="high" alt="大西洋城海龟奖牌、海边合影与跑步留影"></picture><figcaption>绿色阿森纳，背靠背的第二场全马<br>摄影 / Arsenan、官方摄影</figcaption></figure>',
    '<div class="down" aria-hidden="true">⌄<br>⌄<br>⌄</div>',f'<section class="intro"><p>{em(INTRO)}</p></section>',
    f'<figure class="photo-strip location-poster"><img src="/assets/run50-atlantic-city-2026/map.jpg" alt="截至第38州新泽西的 Run50 足迹"><img src="{POSTER_SRC}" alt="新泽西大西洋城摩天轮、大象和赌场元素，2026 Run50 38"><figcaption>新泽西 · 大西洋城 · Run50 第38州<br>制图 / Arsenan · 封面设计 / Arsenan × AI</figcaption></figure>']
    used=[];blocks=[];n=0
    for line in (DATA/'atlantic-city-2026-story.txt').read_text(encoding='utf8').splitlines():
        if not line.strip():continue
        if line.startswith('# '):
            label,title=line[2:].split('｜',1);n+=1
            out.append(f'<header class="chapter"><span class="chapter-number">{n:02}</span><p class="chapter-label">{escape(label)}</p><h2>{escape(title)}</h2></header>');blocks.append({'kind':'heading','label':label,'title':title})
        elif line.startswith('@'):
            keys=line[1:].split();used+=keys;assert 1<=len(keys)<=3
            images=[];credits=[]
            for key in keys:
                p=meta[key];credits.append(confirmed_credits.get(key,'官方摄影' if key in official else 'Siqi' if key in siqi else 'Arsenan'))
                src='/assets/run50-atlantic-city-2026/photos/'+p['name'];preview='/assets/run50-atlantic-city-2026/preview/'+key+'.jpg'
                images.append(f'<img src="{src}" srcset="{preview} 1600w" sizes="(max-width:677px) calc(100vw - 40px), 637px" data-copy-src="{src}" data-photo-id="{key}" alt="{escape(caps[key])}" width="{p["width"]}" height="{p["height"]}" loading="lazy" decoding="async">')
            caption='；'.join(caps[k] for k in keys)+' · 摄影 / '+credits[0] if len(set(credits))==1 else '；'.join(caps[k]+' · 摄影 / '+c for k,c in zip(keys,credits))
            out.append('<figure class="photo-strip">'+''.join(images)+'<figcaption>'+escape(caption)+'</figcaption></figure>');blocks.append({'kind':'photos','ids':keys,'credits':credits})
        else:out.append('<p class="prose">'+em(line)+'</p>');blocks.append({'kind':'paragraph','text':line})
    assert len(used)==len(set(used))==187 and set(used)==set(meta)==set(caps)
    assert used.index('012')<used.index('006') and used.index('122')<used.index('142')
    out.append('<footer class="ending"><p class="end-mark">本文完</p><p class="series">RUN50 · 第38州 · 新泽西</p><h2>两天，两场全马</h2><p class="closing">从巴尔的摩的金螃蟹，到大西洋城的小海龟。这个周末，跑过两个新的州。</p><p class="credits">文字 / Arsenan<br>摄影 / Arsenan、Siqi、官方摄影、现场跑友、路人</p></footer>')
    out.append('<p class="source-note">本文根据作者大西洋城原始视频口述与187张选图整理。背景资料：<a href="https://www.nj.gov/nj/about/history/short_history.shtml">新泽西州历史与特色</a> · <a href="https://pubs.usgs.gov/publication/fs20223054/full">新泽西地理</a> · <a href="https://www.acraceseries.com/event-information">赛事信息</a> · <a href="https://www.acraceseries.com/course">赛道与补给</a> · <a href="https://blogs.loc.gov/loc/2015/06/under-the-boardwalk/">木栈道历史</a> · <a href="https://abseconlighthouse.org/about/">Absecon 灯塔</a> · <a href="https://lucytheelephant.org/">Lucy 大象</a>。封面为地标组合插画，不表示实际空间比例。</p>')
    nav='<nav class="copy-tools"><a href="/CN/#run50-series" style="color:inherit">Run50 目录</a><button data-theme-choice="light" aria-pressed="true">白底</button><button data-theme-choice="dark" aria-pressed="false">黑底</button><button id="copy-wechat">一键复制到公众号</button><span id="copy-status" role="status" aria-live="polite"></span></nav>'
    html=f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{TITLE}</title><meta name="description" content="{INTRO}"><meta property="og:image" content="https://zhennanzhang.com{COVER_SRC}"><style>{css}</style></head><body>{nav}<main data-edition="run50-atlantic-city-2026" data-copy-chunks>'+'\n'.join(out)+'</main><script src="/assets/run50-six-editorial-copy.js?v=20261025-original-chunks" defer></script></body></html>'
    soup=BeautifulSoup(html,'html.parser')
    for img in soup.find_all('img'):
        candidates=[img.get('src',''),img.get('data-dark-src','')]
        img['data-copy-bytes']=str(max([0]+[(ROOT/u.split('?')[0].lstrip('/')).stat().st_size for u in candidates if u and (ROOT/u.split('?')[0].lstrip('/')).exists()]))
    soup.select_one('.source-note').replace_with(BeautifulSoup(SETTINGS['source_note'],'html.parser'))
    soup.select_one('footer.ending').replace_with(BeautifulSoup(SETTINGS['footer'],'html.parser'))
    html=str(soup)

    for suffix in ['editorial','modern-rail']:(ROOT/f'run50/wechat/{SLUG}-{suffix}.html').write_text(html,encoding='utf8')
    (DATA/'atlantic-city-2026-editorial.json').write_text(json.dumps({'slug':SLUG,'title':TITLE,'intro':INTRO,'blocks':blocks,'photo_count':187},ensure_ascii=False,indent=2),encoding='utf8')
    print(n,'chapters',len(used),'photos')
def hero():
    meta=json.loads((DATA/'atlantic-city-2026-photos.json').read_text(encoding='utf8'));frames=[]
    for n,center in [(147,(.5,.5)),(45,(.5,0)),(107,(.5,.4)),(124,(.5,.4)),(142,(.5,0)),(168,(.5,.4))]:
        with Image.open(ASSET/'photos'/meta[n-1]['name']) as im:frames.append(ImageOps.fit(ImageOps.exif_transpose(im).convert('RGB'),(900,900),centering=center))
    frames[0].save(ASSET/'hero-still.jpg',quality=95)
    frames[0].save(ASSET/'hero.gif',save_all=True,append_images=frames[1:],duration=3000,loop=0,optimize=False)
if __name__=='__main__':hero();render()
