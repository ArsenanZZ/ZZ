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
<h1>__ARTICLE_TITLE__</h1>
<p class="byline">文字 / Arsenan</p>
</header>
<picture class="brand-intro"><source media="(prefers-reduced-motion: reduce)" srcset="../../assets/run50-robot-intro-compact-still.png?v=20261001-static-mark"><img src="../../assets/run50-robot-intro-compact.gif?v=20261001-static-mark" alt="Run50 跑步机器人片头" width="224" height="300"></picture>
<figure class="cover" aria-label="密歇根马拉松官方照片">
<picture><source media="(prefers-reduced-motion: reduce)" srcset="../stories/chinese/Run50-Michigan-Meadows-Marathon-clean_files/img-033.webp"><img src="../../assets/michigan-wechat-hero-slideshow.gif?v=five-photos" alt="密歇根马拉松：三张比赛照、与 Siqi 合影、完赛奖牌" fetchpriority="high" width="900" height="820"></picture>
<figcaption class="hero-credit">比赛照 / 赛事官方 · 合影、奖牌 / Arsenan</figcaption>
</figure>
<div class="down" aria-hidden="true">⌄<br>⌄<br>⌄</div>
<section class="intro">
<p>从肯塔基北上大急流城，先用 <strong>Parkrun</strong> 热身，再在 <strong>Millennium Park</strong> 绕六圈完成密歇根州。不是最快的一场，但很有夏天、湿地和重复路线的味道。</p>
</section>''']
    body.append(figure('../../assets/wechat-run50-map-michigan-21-editorial.png', '密歇根手绘地图，星标大急流城', '第 21 州 · 密歇根，星标为大急流城｜制图 / Arsenan'))
    body.append(figure('../../assets/wechat-michigan-grand-rapids-poster-20261001.png', 'Michigan，2024，Grand Rapids，Run50 21', '2024 · 大急流城 · Run50 第21州'))
    n = 0
    for block in data['blocks']:
        kind = block['kind']
        if kind == 'heading':
            n += 1
            body.append(f'<header class="chapter"><span class="chapter-number" aria-hidden="true">{n:02}</span><p class="chapter-label">{escape(block["label"])}</p><h2>{escape(block["title"])}</h2></header>')
        elif kind == 'paragraph':
            body.append(block['html'].replace('<p>', '<p class="prose" style="margin:0 0 22px;font-size:15px;line-height:1.95;letter-spacing:.5px;text-align:justify">', 1))
        elif kind == 'figure':
            body.append(figure(block['src'], block['alt'], block['caption']))
    body.append('''<footer class="ending">
<p class="end-mark">— 本文完 —</p>
<p class="series">RUN50 · 第21州</p>
<h2>密歇根，点亮。</h2>
<p class="finish-stats">6 圈 &nbsp; / &nbsp; 42.195 公里 &nbsp; / &nbsp; 4:44</p>
<p>密歇根位于美国五大湖地区，以汽车工业和湖岸风光闻名。</p>
''')
    body.append('<p class="credits">文字 / Arsenan<br>摄影 / 见图片署名</p></footer>')
    css = '''
:root{color-scheme:light;--paper:#fff;--ink:#262626;--muted:#888;--accent:#c0a04c}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font-family:"PingFang SC","Microsoft YaHei",Arial,sans-serif}
main{width:100%;max-width:677px;margin:auto;padding:0 20px 72px}img{max-width:100%}
.masthead{text-align:center;padding:36px 8px 4px}.series{font-size:12px;font-weight:700;letter-spacing:4px}.issue{font-size:10px;letter-spacing:2px;color:var(--muted);margin-top:18px}
h1{font-family:"Songti SC",SimSun,serif;font-size:32px;line-height:1.6;font-weight:700;margin:0 0 18px;letter-spacing:1px}.byline{font-size:12px;color:var(--muted);line-height:1.9}
.brand-intro{display:block;width:96px;max-width:100%;margin:0 auto 4px}.brand-intro img{display:block;width:100%;height:auto}.cover{margin:0}.hero-credit{margin:10px 0 0;text-align:center;font-size:12px;line-height:1.8;color:#888}.cover img{display:block;width:100%;height:auto}
.down{text-align:center;color:#aaa;display:block;width:100%;font-size:24px;line-height:13px;margin:30px 0 36px}.intro{margin:0 0 54px;font-size:15px;line-height:2;letter-spacing:.5px}
.chapter{margin:72px 0 34px}.chapter-number{display:block;font-family:Arial,sans-serif;font-size:94px;line-height:1;font-weight:400;color:transparent;-webkit-text-stroke:1px var(--ink);letter-spacing:-5px}.chapter-label{font-size:11px;letter-spacing:2px;color:var(--muted);margin:18px 0 10px}.chapter h2{font-size:20px;line-height:1.65;letter-spacing:.5px;margin:0;font-weight:700}
strong{font-weight:700}em{font-family:Georgia,serif}figure+figure{margin-top:42px}.ending{margin-top:64px;padding-top:32px;border-top:1px solid #ddd;text-align:center;font-size:14px;line-height:1.9}.end-mark{font-size:12px;color:#888;margin-bottom:44px}.ending h2{font-family:SimSun,serif;font-size:30px;margin:16px 0}.finish-stats{font-size:12px;letter-spacing:1px;color:#777}.credits{font-size:12px;line-height:2;color:#888;margin:36px 0}.closing{font-size:13px;line-height:2}
@media(max-width:520px){main{padding:0 20px 48px}.masthead{padding-top:28px}h1{font-size:25px}.chapter{margin-top:58px}.chapter-number{font-size:80px}.chapter h2{font-size:18px}}
.copy-tools{position:sticky;top:0;z-index:10;display:flex;flex-wrap:wrap;justify-content:center;align-items:center;gap:10px;padding:10px 14px;background:#f7f7f5;border-bottom:1px solid #e6e6e2;font-size:12px;color:#666}.copy-tools button{padding:10px 16px;border:0;border-radius:4px;background:#2d6649;color:white;font:600 14px/1.4 "Microsoft YaHei",sans-serif;cursor:pointer}.copy-tools button:disabled{opacity:.6;cursor:wait}.copy-tools button:focus-visible{outline:3px solid #d0a32e;outline-offset:2px}
html[data-theme="dark"]{color-scheme:dark;--paper:#191919;--ink:#ece9e2;--muted:#aaa}
html[data-theme="dark"] figcaption,html[data-theme="dark"] .credits,html[data-theme="dark"] .end-mark,html[data-theme="dark"] .finish-stats{color:#aaa!important}
html[data-theme="dark"] .ending{border-color:#444}html[data-theme="dark"] .copy-tools{background:#242424;color:#ddd;border-color:#444}
.copy-tools .theme-choice{background:transparent;color:inherit;border:1px solid #888;padding:9px 12px}.copy-tools .theme-choice[aria-pressed="true"]{border-color:#b99b49;box-shadow:inset 0 -2px #b99b49}
@media print{.copy-tools{display:none}main{max-width:677px}.chapter,figure{break-inside:avoid}}
'''
    return '<!doctype html>\n<html lang="zh-CN"><head><meta charset="utf-8"><script>if(new URLSearchParams(location.search).get("v")==="20260917-clear-colors"){location.replace("michigan-meadows-marathon-rail-clear-colors.html"+location.hash);}</script><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="Run50 第21州：密歇根梅多马拉松，在大急流城的夏天六次穿越千禧公园。"><title>' + escape(data['title']) + '</title><style>' + css + '</style></head><body><nav class="copy-tools" aria-label="公众号复制"><a href="michigan-meadows-marathon-versions.html" style="color:inherit;font-size:13px">全部版本</a><button class="theme-choice" data-theme-choice="light" aria-pressed="true" type="button">白底</button><button class="theme-choice" data-theme-choice="dark" aria-pressed="false" type="button">黑底</button><button id="copy-wechat" type="button">一键复制到公众号</button><span id="copy-status" role="status" aria-live="polite"></span></nav><main data-edition="michigan-editorial-20261001">' + '\n'.join(body).replace('__ARTICLE_TITLE__', escape(data['title'])) + '</main><script src="../../assets/michigan-wechat-copy.js?v=20261001-copy-justify" defer></script></body></html>\n'


if __name__ == '__main__':
    OUT.write_text(render(), encoding='utf-8', newline='\n')
    print(OUT)

