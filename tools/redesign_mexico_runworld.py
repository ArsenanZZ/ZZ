from pathlib import Path
from html import escape
import re

from lxml import html
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SITE = "https://arsenanzz.github.io/ZZ"
SLUG = "mexico-marathon"
VERSION = "20260604-12"
OG_IMAGE = f"{SITE}/assets/og-run50-mexico-icons.png"


NORMAL_CSS = """
    :root {
      --paper: #f3f6ef;
      --surface: #ffffff;
      --ink: #20242b;
      --muted: #667085;
      --line: #d5dfd0;
      --river: #2f855a;
      --brick: #2f855a;
      --gold: #b7892f;
      --leaf: #2f855a;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      background: linear-gradient(180deg, #edf5ec 0, var(--paper) 300px);
      color: var(--ink);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
      line-height: 1.78;
      letter-spacing: 0;
    }
    a { color: var(--river); text-decoration-thickness: 1px; text-underline-offset: 4px; }
    .story-nav {
      max-width: 860px;
      margin: 0 auto;
      padding: 18px 22px 0;
      display: flex;
      gap: 14px;
      justify-content: space-between;
      color: var(--muted);
      font-size: 14px;
    }
    .story-nav a {
      color: inherit;
      text-decoration: none;
      border-bottom: 1px solid transparent;
    }
    .story-nav a:hover { border-color: currentColor; }
    .page-header {
      max-width: 860px;
      margin: 0 auto;
      padding: 42px 22px 24px;
    }
    .kicker { margin: 0 0 14px; color: var(--brick); font-size: 14px; font-weight: 800; }
    h1 {
      margin: 0;
      max-width: 780px;
      color: #111827;
      font-size: 34px;
      line-height: 1.22;
      font-weight: 850;
      letter-spacing: 0;
    }
    .meta {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      align-items: center;
      margin-top: 18px;
      color: var(--muted);
      font-size: 14px;
    }
    .meta span,
    .meta a {
      display: inline-flex;
      align-items: center;
      min-height: 30px;
      padding: 3px 10px;
      border: 1px solid var(--line);
      border-radius: 999px;
      background: rgba(255, 255, 255, .72);
      color: var(--muted);
      text-decoration: none;
    }
    .dek {
      margin: 22px 0 0;
      padding-left: 16px;
      border-left: 4px solid var(--river);
      color: #344054;
      font-size: 15px;
    }
    .article-shell {
      background: var(--surface);
      border-top: 1px solid var(--line);
      border-bottom: 1px solid var(--line);
      box-shadow: 0 24px 60px rgba(15, 23, 42, .06);
    }
    .article-body {
      max-width: 760px;
      margin: 0 auto;
      padding: 44px 22px 56px;
      overflow-wrap: anywhere;
    }
    .article-body .chapter {
      margin: 0;
      padding: 0;
      border: 0;
    }
    .article-body h2 {
      display: flex;
      align-items: center;
      gap: 12px;
      margin: 0 0 26px;
      color: #111827;
      font-size: 28px;
      line-height: 1.25;
      font-weight: 850;
      letter-spacing: 0;
    }
    .article-body h2:not(:first-child),
    .article-body .chapter:not(:first-child) h2 { margin-top: 54px; }
    .article-body h2::before {
      content: "";
      width: 34px;
      height: 3px;
      border-radius: 999px;
      background: var(--gold);
      flex: 0 0 auto;
    }
    .article-body .kicker {
      margin: 0 0 14px;
      color: var(--muted);
      font-size: 14px;
      font-weight: 800;
    }
    .article-body .loc { color: var(--river); }
    .article-body p { margin: 0 0 17px; font-size: 17px; line-height: 1.86; }
    .single, .gallery { margin: 28px 0 30px; }
    .gallery {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 16px;
    }
    figure.shot,
    .article-body figure { margin: 0; }
    .article-body img {
      display: block;
      width: 100%;
      max-width: 100%;
      height: auto;
      border-radius: 8px;
      background: #e1e8dc;
      box-shadow: 0 16px 40px rgba(15, 23, 42, .12);
    }
    .gallery img {
      aspect-ratio: 16 / 10;
      object-fit: cover;
    }
    figcaption {
      margin-top: 9px;
      color: #7a828c;
      font-size: 13px;
      line-height: 1.55;
      text-align: center;
    }
    .end,
    .credits,
    .credit-line {
      text-align: center;
      color: var(--muted);
    }
    .credits {
      padding-top: 22px;
      border-top: 1px solid var(--line);
      font-size: 15px;
      line-height: 2;
    }
    .article-body hr { width: 72px; height: 1px; margin: 34px auto; border: 0; background: var(--line); }
    .page-footer { max-width: 860px; margin: 0 auto; padding: 22px 22px 48px; color: var(--muted); font-size: 13px; }
    @media (max-width: 640px) {
      .story-nav { flex-wrap: wrap; }
      .page-header { padding: 30px 18px 20px; }
      h1 { font-size: 26px; }
      .article-body { padding: 34px 18px 44px; }
      .article-body h2 { font-size: 24px; }
      .article-body p { font-size: 16px; }
      .single, .gallery { margin-left: -2px; margin-right: -2px; }
    }
"""


FACEBOOK_CSS = """
    :root {
      --red: #cc0000;
      --ink: #111111;
      --muted: #666666;
      --line: #d9d9d9;
      --soft: #f4f4f4;
      --paper: #ffffff;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      background: var(--paper);
      color: var(--ink);
      font-family: Arial, Helvetica, sans-serif;
      line-height: 1.6;
      letter-spacing: 0;
    }
    a { color: inherit; text-decoration-thickness: 1px; text-underline-offset: 3px; }
    img { max-width: 100%; height: auto; }
    .breaking {
      background: var(--red);
      color: #ffffff;
      font-size: 13px;
      font-weight: 900;
      letter-spacing: .08em;
      text-transform: uppercase;
    }
    .breaking-inner {
      width: min(1180px, calc(100% - 32px));
      margin: 0 auto;
      min-height: 38px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 18px;
    }
    .breaking a { color: #ffffff; text-decoration: none; }
    .site-head {
      border-bottom: 1px solid var(--line);
      background: #ffffff;
    }
    .site-head-inner {
      width: min(1180px, calc(100% - 32px));
      margin: 0 auto;
      min-height: 68px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 18px;
    }
    .wordmark {
      color: var(--red);
      font-size: 30px;
      line-height: 1;
      font-weight: 950;
      letter-spacing: 0;
      text-decoration: none;
    }
    .section-nav {
      display: flex;
      flex-wrap: wrap;
      justify-content: flex-end;
      gap: 14px;
      color: #333333;
      font-size: 13px;
      font-weight: 800;
      text-transform: uppercase;
    }
    .section-nav a { text-decoration: none; }
    .article {
      width: min(1180px, calc(100% - 32px));
      margin: 0 auto;
    }
    .hero {
      padding: 34px 0 26px;
      border-bottom: 1px solid var(--line);
    }
    .label {
      display: inline-flex;
      align-items: center;
      min-height: 28px;
      padding: 4px 9px;
      background: var(--red);
      color: #ffffff;
      font-size: 12px;
      font-weight: 900;
      letter-spacing: .08em;
      text-transform: uppercase;
    }
    h1 {
      max-width: 980px;
      margin: 18px 0 14px;
      font-size: clamp(2.45rem, 7vw, 5.5rem);
      line-height: .94;
      letter-spacing: 0;
    }
    .dek {
      max-width: 820px;
      margin: 0;
      color: #333333;
      font-size: clamp(1.08rem, 2vw, 1.32rem);
      line-height: 1.55;
    }
    .byline {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-top: 18px;
      color: var(--muted);
      font-size: 13px;
      font-weight: 800;
      text-transform: uppercase;
    }
    .byline span,
    .byline a {
      min-height: 30px;
      display: inline-flex;
      align-items: center;
      padding: 4px 9px;
      background: var(--soft);
      text-decoration: none;
    }
    .lead-media {
      margin: 26px 0 0;
      border-top: 6px solid var(--red);
    }
    .lead-media img {
      display: block;
      width: 100%;
      aspect-ratio: 1200 / 630;
      object-fit: cover;
      background: var(--soft);
    }
    figcaption {
      margin-top: 8px;
      color: var(--muted);
      font-size: 12px;
      line-height: 1.4;
    }
    .story-grid {
      display: grid;
      grid-template-columns: minmax(220px, 300px) minmax(0, 720px);
      gap: 34px;
      align-items: start;
      padding: 34px 0 12px;
    }
    .rail {
      position: sticky;
      top: 16px;
      display: grid;
      gap: 18px;
    }
    .brief-box {
      border-top: 5px solid var(--red);
      background: var(--soft);
      padding: 16px;
    }
    .brief-box h2 {
      margin: 0 0 12px;
      font-size: 19px;
      line-height: 1.1;
    }
    .brief-box dl { margin: 0; display: grid; gap: 12px; }
    .brief-box dt {
      color: var(--red);
      font-size: 11px;
      font-weight: 900;
      letter-spacing: .08em;
      text-transform: uppercase;
    }
    .brief-box dd {
      margin: 2px 0 0;
      color: #222222;
      font-size: 14px;
      line-height: 1.45;
    }
    .share-note {
      border: 1px solid var(--line);
      padding: 14px;
      color: #333333;
      font-size: 13px;
      line-height: 1.55;
    }
    .share-note strong {
      display: block;
      margin-bottom: 5px;
      color: var(--ink);
      font-size: 12px;
      letter-spacing: .08em;
      text-transform: uppercase;
    }
    .copy { min-width: 0; }
    .copy p {
      margin: 0 0 19px;
      font-family: Georgia, "Times New Roman", serif;
      font-size: 19px;
      line-height: 1.72;
    }
    .copy h2 {
      margin: 36px 0 16px;
      padding-top: 20px;
      border-top: 1px solid var(--line);
      font-size: 30px;
      line-height: 1.1;
      letter-spacing: 0;
    }
    .copy .kicker {
      margin: 0 0 12px;
      color: var(--red);
      font-family: Arial, Helvetica, sans-serif;
      font-size: 13px;
      font-weight: 900;
      letter-spacing: .08em;
      text-transform: uppercase;
    }
    .copy .loc { color: var(--red); }
    .copy figure { margin: 25px 0 30px; }
    .copy figure img {
      display: block;
      width: 100%;
      border: 1px solid var(--line);
      background: var(--soft);
    }
    .copy .gallery {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 14px;
      margin: 26px 0 30px;
    }
    .copy .gallery img { aspect-ratio: 4 / 3; object-fit: cover; }
    .copy hr {
      width: 74px;
      height: 5px;
      margin: 34px 0;
      border: 0;
      background: var(--red);
    }
    .end,
    .credits {
      text-align: center;
      color: var(--muted);
    }
    .zz-engagement {
      max-width: 1180px;
      padding-left: 0;
      padding-right: 0;
    }
    .zz-engagement-kicker,
    .zz-engagement h2 { color: var(--red); }
    @media (max-width: 860px) {
      .site-head-inner {
        align-items: flex-start;
        flex-direction: column;
        padding: 16px 0;
      }
      .section-nav { justify-content: flex-start; }
      .story-grid { grid-template-columns: 1fr; }
      .rail { position: static; }
    }
    @media (max-width: 640px) {
      .copy .gallery { grid-template-columns: 1fr; }
    }
"""


SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 750" role="img" aria-labelledby="title desc">
<title id="title">Mexico City icon cover</title>
<desc id="desc">Icon style cover with Mexico City title, fixed RunWorld badge, Aztec pyramid, Angel of Independence, cactus, sun and highland scenery.</desc>
<rect width="1200" height="750" fill="#edf5ec"/>
<text x="70" y="104" font-family="Arial, Helvetica, sans-serif" font-size="66" font-weight="900" fill="#20242b">MEXICO CITY</text>
<text x="72" y="150" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="800" fill="#667085">ALTITUDE, ZOCALO, PYRAMIDS</text>
<rect x="758" y="62" width="364" height="166" rx="22" fill="#ffffff" stroke="#20242b" stroke-width="8"/>
<text x="790" y="122" font-family="Arial, Helvetica, sans-serif" font-size="41" font-weight="900" fill="#20242b">RunWorld #5</text>
<text x="790" y="182" font-family="Arial, Helvetica, sans-serif" font-size="52" font-weight="900" fill="#2f855a">MEXICO</text>
<circle cx="1052" cy="352" r="62" fill="#f59e0b"/>
<path d="M0 612 C190 540 330 590 500 538 C690 480 830 590 1000 545 C1100 518 1168 515 1200 498 L1200 750 L0 750 Z" fill="#a3c4ad"/>
<path d="M0 682 C180 620 370 705 560 650 C760 592 930 690 1200 620 L1200 750 L0 750 Z" fill="#749b7f"/>
<g>
  <rect x="118" y="560" width="372" height="60" rx="2" fill="#d97706"/>
  <rect x="158" y="500" width="292" height="60" rx="2" fill="#b45309"/>
  <rect x="204" y="440" width="200" height="60" rx="2" fill="#78350f"/>
  <rect x="254" y="380" width="104" height="60" rx="2" fill="#451a03"/>
  <polygon points="292 620,300 380,316 380,324 620" fill="#fbbf24"/>
  <path d="M118 560 H490 M158 500 H450 M204 440 H404" stroke="#20242b" stroke-width="5" opacity=".45"/>
</g>
<g>
  <rect x="680" y="438" width="26" height="218" fill="#8b5e20"/>
  <rect x="642" y="656" width="104" height="26" fill="#8b5e20"/>
  <circle cx="693" cy="418" r="24" fill="#d9a441" stroke="#8b5e20" stroke-width="5"/>
  <path d="M693 342 L706 398 L693 386 L680 398 Z" fill="#d9a441" stroke="#8b5e20" stroke-width="4"/>
  <path d="M642 414 C664 386 722 386 744 414" stroke="#d9a441" stroke-width="10" stroke-linecap="round" fill="none"/>
</g>
<g>
  <rect x="970" y="420" width="24" height="250" rx="12" fill="#15803d"/>
  <path d="M930 480 L930 520 A16 16 0 0 0 946 536 L970 536" stroke="#15803d" stroke-width="24" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
  <path d="M1026 450 L1026 490 A16 16 0 0 1 1010 506 L994 506" stroke="#15803d" stroke-width="24" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
  <rect x="870" y="512" width="16" height="150" rx="8" fill="#166534"/>
  <path d="M840 555 L840 575 A10 10 0 0 0 850 585 L870 585" stroke="#166534" stroke-width="16" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
  <path d="M910 540 L910 560 A10 10 0 0 1 900 570 L886 570" stroke="#166534" stroke-width="16" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
</g>
<path d="M0 702 C180 675 340 720 520 695 C720 668 900 720 1200 678 L1200 750 L0 750 Z" fill="#4f8f68"/>
</svg>
"""


def font(size, bold=False):
    candidates = [
        r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\segoeuib.ttf" if bold else r"C:\Windows\Fonts\segoeui.ttf",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size)
        except Exception:
            pass
    return ImageFont.load_default()


def inner_html(node):
    return "\n".join(html.tostring(child, encoding="unicode", method="html") for child in node)


def clean_text(text):
    return "\n".join(line.rstrip() for line in text.splitlines()) + "\n"


def write_clean(path, text):
    path.write_text(clean_text(text), encoding="utf-8", newline="\n")


def first_by_class(doc, class_name):
    expr = f"//*[contains(concat(' ', normalize-space(@class), ' '), ' {class_name} ')]"
    items = doc.xpath(expr)
    return items[0] if items else None


def extract_content(path, facebook=False):
    doc = html.fromstring(path.read_text(encoding="utf-8"))
    if facebook:
        node = first_by_class(doc, "full-story")
    else:
        node = first_by_class(doc, "article-body")
    if node is None:
        mains = doc.xpath("//main")
        node = mains[0] if mains else None
    if node is None:
        raise RuntimeError(f"No story content found in {path}")
    return inner_html(node)


def engagement(locale, page_key, mount_id):
    is_zh = locale == "zh-CN"
    kicker = "留言 / 阅读" if is_zh else "Comments / Views"
    title = "跑完也可以聊两句" if is_zh else "Say something after the run"
    note = "不用登录就可以留言，新留言会直接显示。" if is_zh else "No account is needed to submit a comment. New comments appear right away."
    loading = "留言区加载中..." if is_zh else "Loading comments..."
    views = "阅读" if is_zh else "Views"
    return f'''
  <section class="zz-engagement" data-zz-engagement data-locale="{locale}" data-page-key="{page_key}">
    <div class="zz-engagement-shell">
      <div>
        <p class="zz-engagement-kicker">{escape(kicker)}</p>
        <h2>{escape(title)}</h2>
        <p class="zz-engagement-note">{escape(note)}</p>
        <div class="zz-engagement-stats"><span class="zz-engagement-stat" id="busuanzi_container_page_pv"><span>{escape(views)}</span><strong id="busuanzi_value_page_pv" data-zz-view-count>--</strong></span></div>
      </div>
      <div class="zz-engagement-card"><div id="{mount_id}" data-zz-supabase-comments></div><p class="zz-engagement-status" data-zz-engagement-status>{escape(loading)}</p></div>
    </div>
  </section>'''


def normal_page(lang, content):
    is_zh = lang == "zh"
    path = "chinese" if is_zh else "english"
    other = "../english/mexico-marathon.html" if is_zh else "../chinese/mexico-marathon.html"
    title = (
        "RunWorld #第5国｜墨西哥：墨西哥城马拉松｜阿兹特克高原42公里，金字塔外一场奇遇"
        if is_zh
        else "RunWorld #5 | Mexico: Mexico City Marathon"
    )
    short = "RunWorld #第5国｜墨西哥城马拉松" if is_zh else "RunWorld #5 | Mexico City Marathon"
    desc = (
        "这是我跑世界的第五站，墨西哥城马拉松。趁 Labor Day 三天小长假，从美国飞墨城，在 2,240 米高原跑过城市主轴、改革大道、终点冲进宪法广场；赛后还有金字塔、洞穴餐厅，和漆黑郊外一车陌生人带我们回城的奇遇。"
        if is_zh
        else "Race date: August 31, 2025. My fifth country in RunWorld: Mexico City Marathon at 2,240 m, finishing at the Zocalo, plus pyramids at dusk, a cave restaurant, and a ride home with kind strangers."
    )
    nav = (
        f'<a href="./index.html">← 中文故事</a><a href="{other}">English</a><a href="../../facebook/{SLUG}.html">Facebook</a><a href="../../index.html">Run50</a>'
        if is_zh
        else f'<a href="./index.html">← English Stories</a><a href="{other}">中文</a><a href="../../facebook/{SLUG}.html">Facebook</a><a href="../../index.html">Run50</a>'
    )
    meta = (
        '<span>墨西哥城</span><span>2025.08.31</span><span>RunWorld #5</span><a href="https://mp.weixin.qq.com/s/FDy9_9325Rq0P9fhbksWiw" target="_blank" rel="noopener">原文链接</a>'
        if is_zh
        else '<span>Mexico City</span><span>Aug 31, 2025</span><span>RunWorld #5</span><a href="https://mp.weixin.qq.com/s/FDy9_9325Rq0P9fhbksWiw" target="_blank" rel="noopener">Original post</a>'
    )
    kicker = "RunWorld Stories · 墨西哥" if is_zh else "RunWorld Stories · Mexico"
    footer = "中文原文页面，英文和 Facebook 版已链接在顶部。" if is_zh else "English version of the Mexico City Marathon story. Original Chinese page is linked above."
    locale = "zh-CN" if is_zh else "en"
    key = "run50-mexico-marathon-zh" if is_zh else "run50-mexico-marathon-en"
    mount = "supabase-comments-mexico-zh" if is_zh else "supabase-comments-mexico-en"
    canonical = f"{SITE}/run50/stories/{path}/{SLUG}.html"
    return f'''<!doctype html>
<html lang="{'zh-CN' if is_zh else 'en'}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)}</title>
  <meta name="description" content="{escape(desc)}">
  <link rel="canonical" href="{canonical}">
  <meta property="og:title" content="{escape(short)}">
  <meta property="og:description" content="{escape(desc)}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="{canonical}">
  <meta property="og:site_name" content="ArsenanZZ">
  <meta property="og:locale" content="{'zh_CN' if is_zh else 'en_US'}">
  <meta property="og:locale:alternate" content="{'en_US' if is_zh else 'zh_CN'}">
  <meta property="og:image" content="{OG_IMAGE}">
  <meta property="og:image:secure_url" content="{OG_IMAGE}">
  <meta property="og:image:type" content="image/png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Mexico City Marathon icon cover with RunWorld badge, Aztec pyramid, Angel of Independence and cactus.">
  <meta property="article:author" content="Arsenan">
  <meta property="article:published_time" content="2025-08-31T07:00:00-06:00">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{escape(short)}">
  <meta name="twitter:description" content="{escape(desc)}">
  <meta name="twitter:image" content="{OG_IMAGE}">
  <link rel="stylesheet" href="../../../assets/zz-engagement.css?v=20260604">
  <style>{NORMAL_CSS}</style>
</head>
<body>
  <nav class="story-nav" aria-label="Page navigation">{nav}</nav>
  <header class="page-header">
    <p class="kicker">{escape(kicker)}</p>
    <h1>{escape(title)}</h1>
    <div class="meta">{meta}</div>
    <p class="dek">{escape(desc)}</p>
  </header>
  <main class="article-shell">
    <article class="article-body">
      {content}
    </article>
  </main>
  {engagement(locale, key, mount)}
  <footer class="page-footer">{escape(footer)}</footer>
  <script src="../../../assets/zz-engagement-config.js?v=20260604"></script>
  <script src="../../../assets/zz-engagement.js?v=20260604"></script>
</body>
</html>
'''


def facebook_page(content):
    title = "I ran Mexico City's marathon at altitude, then got stranded by the pyramids at midnight"
    desc = "Race date: August 31, 2025. Mexico City Marathon at 7,300 feet: corrals chaos, a full-blown toilet crisis, a cobblestone sprint into the Zocalo, then a strange night by the pyramids."
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Mexico City Marathon | Run50 Facebook</title>
  <meta name="description" content="{escape(desc)}">
  <link rel="canonical" href="{SITE}/run50/facebook/{SLUG}.html">
  <meta property="og:title" content="{escape(title)}">
  <meta property="og:description" content="{escape(desc)}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="{SITE}/run50/facebook/{SLUG}.html">
  <meta property="og:site_name" content="ArsenanZZ">
  <meta property="og:locale" content="en_US">
  <meta property="og:image" content="{OG_IMAGE}">
  <meta property="og:image:secure_url" content="{OG_IMAGE}">
  <meta property="og:image:type" content="image/png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Mexico City Marathon icon cover with RunWorld badge, Aztec pyramid, Angel of Independence and cactus.">
  <meta property="article:author" content="Arsenan">
  <meta property="article:published_time" content="2025-08-31T07:00:00-06:00">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{escape(title)}">
  <meta name="twitter:description" content="{escape(desc)}">
  <meta name="twitter:image" content="{OG_IMAGE}">
  <link rel="stylesheet" href="../../assets/zz-engagement.css?v=20260604">
  <style>{FACEBOOK_CSS}</style>
</head>
<body>
  <div class="breaking">
    <div class="breaking-inner">
      <a href="./index.html">Run50 Facebook</a>
      <span>Race date: August 31, 2025</span>
    </div>
  </div>
  <header class="site-head">
    <div class="site-head-inner">
      <a class="wordmark" href="./index.html" aria-label="Run50 Facebook home">RUN50 WORLD</a>
      <nav class="section-nav" aria-label="Story navigation">
        <a href="../index.html">Run50</a>
        <a href="../stories/english/{SLUG}.html">Full English Story</a>
        <a href="../stories/chinese/{SLUG}.html">Chinese Original</a>
      </nav>
    </div>
  </header>
  <article class="article">
    <section class="hero">
      <span class="label">World / Mexico / Marathon</span>
      <h1>{escape(title)}</h1>
      <p class="dek">{escape(desc)}</p>
      <div class="byline">
        <span>By Arsenan</span>
        <span>Race: August 31, 2025</span>
        <span>Mexico City</span>
        <span>RunWorld #5</span>
      </div>
      <figure class="lead-media"><img src="../../assets/og-run50-mexico-icons.png" alt="Icon-style Mexico City Marathon cover"><figcaption>Mexico City icon cover with an Aztec pyramid, the Angel of Independence, cactus, highland sun and RunWorld badge.</figcaption></figure>
    </section>
    <section class="story-grid">
      <aside class="rail">
        <section class="brief-box"><h2>At a glance</h2><dl><div><dt>Race</dt><dd>Mexico City Marathon, RunWorld country 5.</dd></div><div><dt>Course</dt><dd>UNAM, Reforma, the Angel of Independence, downtown streets, and a finish at the Zocalo.</dd></div><div><dt>What stayed with me</dt><dd>High-altitude running, crowd energy, bathroom panic, pyramids after sunset, and a ride home with strangers who turned into the best kind of travel story.</dd></div></dl></section>
        <section class="share-note"><strong>Notes</strong>The comments box is below the story. New comments appear right away.</section>
      </aside>
      <div class="copy full-story">
        {content}
      </div>
    </section>
  </article>
  {engagement("en", "run50-mexico-marathon-facebook-en", "supabase-comments-mexico-facebook-en")}
  <script src="../../assets/zz-engagement-config.js?v=20260604"></script>
  <script src="../../assets/zz-engagement.js?v=20260604"></script>
</body>
</html>
'''


def write_svg():
    write_clean(ROOT / "assets" / "thumb-run50-mexico-icons.svg", SVG)


def write_png():
    image = Image.new("RGB", (1200, 630), "#edf5ec")
    draw = ImageDraw.Draw(image)
    text = "#20242b"
    green = "#2f855a"
    draw.text((64, 64), "MEXICO CITY", font=font(66, True), fill=text)
    draw.text((66, 136), "ALTITUDE, ZOCALO, PYRAMIDS", font=font(26, True), fill="#667085")
    draw.rounded_rectangle((760, 64, 1122, 228), radius=22, fill="#ffffff", outline=text, width=7)
    draw.text((790, 112), "RunWorld #5", font=font(40, True), fill=text)
    draw.text((790, 166), "MEXICO", font=font(50, True), fill=green)
    draw.ellipse((1000, 260, 1098, 358), fill="#f59e0b")
    draw.polygon([(0, 515), (160, 455), (330, 520), (515, 465), (710, 420), (900, 510), (1080, 460), (1200, 438), (1200, 630), (0, 630)], fill="#a3c4ad")
    draw.polygon([(0, 584), (190, 535), (380, 596), (560, 545), (770, 598), (980, 548), (1200, 516), (1200, 630), (0, 630)], fill="#749b7f")
    draw.rectangle((0, 592, 1200, 630), fill="#4f8f68")

    for rect, color in [
        ((112, 500, 488, 558), "#d97706"),
        ((154, 442, 446, 500), "#b45309"),
        ((204, 384, 396, 442), "#78350f"),
        ((254, 326, 354, 384), "#451a03"),
    ]:
        draw.rectangle(rect, fill=color)
    draw.polygon([(292, 558), (300, 326), (316, 326), (324, 558)], fill="#fbbf24")
    draw.line((112, 500, 488, 500), fill="#20242b", width=4)
    draw.line((154, 442, 446, 442), fill="#20242b", width=4)
    draw.line((204, 384, 396, 384), fill="#20242b", width=4)

    draw.rectangle((666, 380, 692, 562), fill="#8b5e20")
    draw.rectangle((628, 562, 732, 588), fill="#8b5e20")
    draw.ellipse((653, 346, 705, 398), fill="#d9a441", outline="#8b5e20", width=5)
    draw.polygon([(679, 280), (693, 374), (679, 360), (665, 374)], fill="#d9a441", outline="#8b5e20")
    draw.arc((612, 332, 746, 420), 205, 335, fill="#d9a441", width=10)

    draw.rounded_rectangle((968, 354, 992, 594), radius=12, fill="#15803d")
    draw.line((930, 420, 930, 462, 968, 462), fill="#15803d", width=22)
    draw.line((1028, 392, 1028, 434, 992, 434), fill="#15803d", width=22)
    draw.rounded_rectangle((870, 450, 886, 590), radius=8, fill="#166534")
    draw.line((840, 500, 840, 520, 870, 520), fill="#166534", width=15)
    draw.line((910, 488, 910, 508, 886, 508), fill="#166534", width=15)
    image.save(ROOT / "assets" / "og-run50-mexico-icons.png", "PNG")


def update_indexes():
    replacements = {
        "thumb-run50-mexico-icons.svg?v=20260604-9": f"thumb-run50-mexico-icons.svg?v={VERSION}",
    }
    for path in [
        ROOT / "run50" / "facebook" / "index.html",
        ROOT / "run50" / "stories" / "chinese" / "index.html",
        ROOT / "run50" / "stories" / "english" / "index.html",
    ]:
        text = path.read_text(encoding="utf-8")
        for old, new in replacements.items():
            text = text.replace(old, new)
        write_clean(path, text)


def main():
    zh_path = ROOT / "run50" / "stories" / "chinese" / f"{SLUG}.html"
    en_path = ROOT / "run50" / "stories" / "english" / f"{SLUG}.html"
    fb_path = ROOT / "run50" / "facebook" / f"{SLUG}.html"
    zh_content = extract_content(zh_path)
    en_content = extract_content(en_path)
    fb_content = extract_content(fb_path, facebook=True)
    write_clean(zh_path, normal_page("zh", zh_content))
    write_clean(en_path, normal_page("en", en_content))
    write_clean(fb_path, facebook_page(fb_content))
    write_svg()
    write_png()
    update_indexes()
    print("redesigned Mexico RunWorld pages and covers")


if __name__ == "__main__":
    main()
