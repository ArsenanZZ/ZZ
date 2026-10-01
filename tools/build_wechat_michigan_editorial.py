"""Render the Michigan WeChat edition from its preserved, edited article content.

The JSON retains the published paragraph, caption and photo order. Only the
presentation is changed; other Run50 editions keep their existing renderer.
"""
from pathlib import Path
from html import escape
import json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'run50/wechat/michigan-meadows-marathon-modern-rail.html'
PHOTO = '../stories/chinese/Run50-Michigan-Meadows-Marathon-clean_files/'


def figure(src, alt, caption, eager=False):
    return (f'<figure style="margin:32px 0 36px">'
            f'<img src="{escape(src)}" alt="{escape(alt)}" loading="{"eager" if eager else "lazy"}" '
            'decoding="async" style="display:block;width:100%;height:auto">'
            f'<figcaption style="margin:10px 12px 0;text-align:center;font-size:12px;line-height:1.75;color:#888;letter-spacing:.5px">{escape(caption)}</figcaption></figure>')


def render():
    data = json.loads((ROOT / 'tools/data/michigan-wechat.json').read_text(encoding='utf-8'))
    body = ['''<header class="masthead">
<p class="series">RUN50 · 行走五十州</p>
<p class="issue">第二十一站 / MICHIGAN</p>
<h1>__ARTICLE_TITLE__</h1>
<p class="byline">梅多马拉松 · 大急流城<br>文字 / Arsenan</p>
</header>
<picture class="brand-intro"><source media="(prefers-reduced-motion: reduce)" srcset="../../assets/run50-robot-intro-still.png?v=20261001-running"><img src="../../assets/run50-robot-intro.gif?v=20261001-running" alt="Run50 跑步机器人片头" width="720" height="480"></picture>
<section class="cover" aria-label="密歇根草甸赛道开篇">
<img src="''' + PHOTO + '''img-033.webp" alt="在草甸赛道上举起双手" fetchpriority="high" width="1438" height="1310">
<p class="hero-credit">摄影 / 赛事官方</p>
<div class="cover-type"><span>第21州 · 密歇根</span><small>Michigan · Meadow Marathon</small></div>
</section>
<div class="down" aria-hidden="true">⌄<br>⌄</div>
<section class="intro">
<p>从肯塔基北上大急流城，先用 <strong>Parkrun</strong> 热身，再在 <strong>Millennium Park</strong> 绕六圈完成密歇根州。不是最快的一场，但很有夏天、湿地和重复路线的味道。</p>
</section>''']
    body.append(figure('../../assets/wechat-run50-map-michigan-21-editorial.png', '密歇根手绘地图，星标大急流城', '第 21 州 · 密歇根，星标为大急流城｜制图 / Arsenan'))
    body.append(figure('../../assets/wechat-michigan-grand-rapids-poster-20261001.png', '密歇根金属浮雕海报：2024，大急流城，Run50 21', '2024 · 大急流城 · Run50 第21州'))
    n = 0
    for block in data['blocks']:
        kind = block['kind']
        if kind == 'heading':
            n += 1
            body.append(f'<header class="chapter"><span class="chapter-number" aria-hidden="true">{n:02}</span><p class="chapter-label">{escape(block["label"])}</p><h2>{escape(block["title"])}</h2></header>')
        elif kind == 'paragraph':
            body.append(block['html'].replace('<p>', '<p class="prose" style="margin:0 8px 22px;font-size:15px;line-height:1.95;letter-spacing:.5px;text-align:justify">', 1))
        elif kind == 'figure':
            body.append(figure(block['src'], block['alt'], block['caption']))
    body.append('''<footer class="ending">
<p class="end-mark">— 本文完 —</p>
<p class="series">RUN50 · 第21州</p>
<h2>密歇根，点亮。</h2>
<p class="finish-stats">6 圈 &nbsp; / &nbsp; 42.195 公里 &nbsp; / &nbsp; 4:44</p>
<p>烈火烤过，也就更能相信，否极必然泰来。</p>
''')
    body.append('<p class="credits">文字 / Arsenan<br>摄影 / 见图片署名</p><p class="closing">你跑过需要一圈又一圈的马拉松吗？<br>欢迎在公众号留言，聊聊你的故事。</p></footer>')
    css = '''
:root{color-scheme:light;--paper:#fff;--ink:#262626;--muted:#888;--accent:#c0a04c}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font-family:"PingFang SC","Microsoft YaHei",Arial,sans-serif}
main{width:100%;max-width:677px;margin:auto;padding:0 16px 72px}img{max-width:100%}
.masthead{text-align:center;padding:54px 8px 32px}.series{font-size:12px;font-weight:700;letter-spacing:4px}.issue{font-size:10px;letter-spacing:2px;color:var(--muted);margin-top:18px}
h1{font-family:"Songti SC",SimSun,serif;font-size:32px;line-height:1.6;font-weight:700;margin:25px 0 20px;letter-spacing:1px}.byline{font-size:12px;color:var(--muted);line-height:1.9}
.brand-intro{display:block;width:280px;max-width:100%;margin:0 auto 26px}.brand-intro img{display:block;width:100%;height:auto}.hero-credit{font-size:12px;line-height:1.8;text-align:center;color:#888;margin:10px 0 0}.cover{position:relative;background:transparent}.cover img{display:block;width:100%;height:auto}.cover-type{position:static;padding:22px 8px 0;background:transparent;color:var(--ink)}.cover-type span{display:block;font-family:KaiTi,"STKaiti",serif;font-size:clamp(30px,5.8vw,52px);font-weight:900;letter-spacing:1px}.cover-type small{display:block;font-family:Georgia,"Times New Roman",serif;font-size:15px;font-weight:400;line-height:1.5;letter-spacing:0;color:#666;margin-top:8px}
.down{text-align:center;color:#aaa;font-size:30px;line-height:12px;margin:38px 0 44px}.intro{margin:0 8px 54px;font-size:15px;line-height:2;letter-spacing:.5px}
.chapter{margin:72px 8px 34px}.chapter-number{display:block;font-family:Arial,sans-serif;font-size:94px;line-height:1;font-weight:400;color:transparent;-webkit-text-stroke:1px var(--ink);letter-spacing:-5px}.chapter-label{font-size:11px;letter-spacing:2px;color:var(--muted);margin:18px 0 10px}.chapter h2{font-size:20px;line-height:1.65;letter-spacing:.5px;margin:0;font-weight:700}
strong{font-weight:700}em{font-family:Georgia,serif}figure+figure{margin-top:42px}.ending{margin-top:64px;padding-top:32px;border-top:1px solid #ddd;text-align:center;font-size:14px;line-height:1.9}.end-mark{font-size:12px;color:#888;margin-bottom:44px}.ending h2{font-family:SimSun,serif;font-size:30px;margin:16px 0}.finish-stats{font-size:12px;letter-spacing:1px;color:#777}.credits{font-size:12px;line-height:2;color:#888;margin:36px 0}.closing{font-size:13px;line-height:2}
@media(max-width:520px){main{padding:0 14px 48px}.masthead{padding-top:38px}h1{font-size:25px}.chapter{margin-top:58px}.chapter-number{font-size:80px}.chapter h2{font-size:18px}.cover-type{padding:18px 8px 0}}
@media print{main{max-width:677px}.chapter,figure{break-inside:avoid}}
'''
    return '<!doctype html>\n<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="Run50 第21州：密歇根梅多马拉松，在大急流城的夏天六次穿越千禧公园。"><title>' + escape(data['title']) + '</title><style>' + css + '</style></head><body><main data-edition="michigan-editorial-20261001">' + '\n'.join(body).replace('__ARTICLE_TITLE__', escape(data['title'])) + '</main></body></html>\n'


if __name__ == '__main__':
    OUT.write_text(render(), encoding='utf-8', newline='\n')
    print(OUT)

