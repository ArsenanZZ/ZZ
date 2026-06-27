from __future__ import annotations

import html
import re
from pathlib import Path

from lxml import html as lxml_html


ROOT = Path(__file__).resolve().parents[1]
SLUG = "arizona-phoenix-marathon"
VERSION = "20260627-run50-style"
SITE = "https://zhennanzhang.com"
IMAGE_DIR = ROOT / "run50" / "stories" / "chinese" / "Run50-Arizona-Phoenix-Marathon-clean_files"


def normalize_arizona_story_style() -> None:
    rename_story_images()

    zh_path = ROOT / "run50" / "stories" / "chinese" / f"{SLUG}.html"
    en_path = ROOT / "run50" / "stories" / "english" / f"{SLUG}.html"
    fb_path = ROOT / "run50" / "facebook" / f"{SLUG}.html"

    zh_article = extract_article_html(zh_path, "zh")
    en_article = extract_article_html(en_path, "en")
    fb_article = extract_article_html(fb_path, "en")

    zh_path.write_text(
        render_standard_story_page(
            lang="zh-CN",
            nav_label="页面导航",
            back_href="./index.html",
            back_text="← 中文故事",
            nav_links=[
                ("../english/arizona-phoenix-marathon.html", "English"),
                ("../../facebook/arizona-phoenix-marathon.html", "Facebook"),
                ("../../index.html", "Run50"),
            ],
            title="Run50 #第29州｜亚利桑那：Buckeye Marathon｜沙漠公路、机场终点和二〇二六第一跑破4",
            meta_title="Run50 #第29州｜亚利桑那：Buckeye Marathon",
            description="二〇二六第一跑，落地凤凰城，跑过 Buckeye 的沙漠公路、巨人柱、机场终点和一场意外的 3:58。",
            canonical=f"{SITE}/run50/stories/chinese/{SLUG}.html",
            asset_prefix="../../../assets",
            kicker="Run50 #第29州 · 亚利桑那",
            meta_items=["By Arsenan", "Race: 2026.01.10", "Buckeye / Phoenix, Arizona", "Buckeye Marathon"],
            article_html=zh_article,
            engagement_locale="zh-CN",
            page_key="run50-arizona-phoenix-marathon-zh",
            comments_id="supabase-comments-arizona-phoenix-marathon-zh",
            engagement_kicker="留言 / 浏览",
            engagement_heading="在路边留一句",
            engagement_note="不用登录。新的留言会直接显示在页面里。",
            views_label="浏览",
            loading_text="留言区加载中...",
            footer="© 2023-2026 ArsenanZZ. Built with love.",
        ),
        encoding="utf-8",
    )

    en_path.write_text(
        render_standard_story_page(
            lang="en",
            nav_label="Page navigation",
            back_href="./index.html",
            back_text="← English Stories",
            nav_links=[
                ("../chinese/arizona-phoenix-marathon.html", "中文"),
                ("../../facebook/arizona-phoenix-marathon.html", "Facebook"),
                ("../../index.html", "Run50"),
            ],
            title="Run50 State #29 | Arizona: Buckeye Marathon",
            meta_title="Run50 State #29 | Arizona: Buckeye Marathon",
            description="My first race of 2026 started in the Phoenix desert: Buckeye’s downhill road, saguaro silhouettes, an airport finish, and a surprise 3:58.",
            canonical=f"{SITE}/run50/stories/english/{SLUG}.html",
            asset_prefix="../../../assets",
            kicker="Run50 #29 · Arizona",
            meta_items=["By Arsenan", "Race: Jan 10, 2026", "Buckeye / Phoenix, Arizona", "Buckeye Marathon"],
            article_html=en_article,
            engagement_locale="en",
            page_key="run50-arizona-phoenix-marathon-en",
            comments_id="supabase-comments-arizona-phoenix-marathon-en",
            engagement_kicker="Comments / Views",
            engagement_heading="Leave a note from the road",
            engagement_note="No login needed. New comments appear directly on the page.",
            views_label="Views",
            loading_text="Loading comments...",
            footer="© 2023-2026 ArsenanZZ. Built with love.",
        ),
        encoding="utf-8",
    )

    fb_path.write_text(
        render_standard_story_page(
            lang="en",
            nav_label="Page navigation",
            back_href="./index.html",
            back_text="← Facebook",
            nav_links=[
                ("../stories/english/arizona-phoenix-marathon.html", "English"),
                ("../stories/chinese/arizona-phoenix-marathon.html", "中文"),
                ("../index.html", "Run50"),
            ],
            title="Arizona turned a cold desert runway race into my first sub-four of 2026",
            meta_title="Run50 State #29 | Arizona: Buckeye Marathon | Facebook Edition",
            description="Buckeye Marathon started in the Phoenix desert and ended beside a runway, with saguaros, dry air, and a finish time I did not see coming.",
            canonical=f"{SITE}/run50/facebook/{SLUG}.html",
            asset_prefix="../../assets",
            kicker="Run50 #29 · Arizona",
            meta_items=["By Arsenan", "Race: Jan 10, 2026", "Buckeye / Phoenix, Arizona", "Buckeye Marathon"],
            article_html=fb_article,
            engagement_locale="en",
            page_key="run50-arizona-phoenix-marathon-facebook-en",
            comments_id="supabase-comments-arizona-phoenix-marathon-facebook-en",
            engagement_kicker="Comments / Views",
            engagement_heading="Leave a note from the road",
            engagement_note="No login needed. New comments appear directly on the page.",
            views_label="Views",
            loading_text="Loading comments...",
            footer="© 2023-2026 ArsenanZZ. Built with love.",
        ),
        encoding="utf-8",
    )

    update_index_copy()


def rename_story_images() -> None:
    for idx in range(1, 88):
        old = IMAGE_DIR / f"{idx:02d}-{SLUG}.webp"
        new = IMAGE_DIR / f"img-{idx:03d}.webp"
        if old.exists() and not new.exists():
            old.rename(new)
        elif old.exists() and new.exists():
            if old.read_bytes() == new.read_bytes():
                old.unlink()
            else:
                raise RuntimeError(f"Both old and new image names exist with different bytes: {old} / {new}")


def extract_article_html(path: Path, lang: str) -> str:
    doc = lxml_html.fromstring(path.read_bytes())
    nodes = doc.xpath("//article[contains(concat(' ', normalize-space(@class), ' '), ' article-body ') or contains(concat(' ', normalize-space(@class), ' '), ' article ')]")
    if not nodes:
        raise RuntimeError(f"Could not find article in {path}")
    article = nodes[0]

    for img in article.xpath(".//img"):
        src = img.get("src") or ""
        img.set("src", normalize_image_src(src))
        img.set("decoding", "async")
        if not img.get("loading"):
            img.set("loading", "lazy")

    for figure in article.xpath(".//figure"):
        figure.attrib.pop("class", None)

    for heading in article.xpath(".//h2"):
        heading.set("class", "section-label")

    for para in article.xpath(".//p"):
        cls = para.get("class") or ""
        text = " ".join(para.text_content().split())
        if "story-end" in cls:
            para.set("class", "end-mark")
        elif "story-credit" in cls:
            para.set("class", "credit-line")
        elif "story-meta-line" in cls:
            para.set("class", "place")
        elif cls in {"story-end", "story-credit", "story-meta-line"}:
            para.attrib.pop("class", None)
        if text in {"- Run50 State #29 | Arizona -", "- Run50 #第29州｜亚利桑那 -"}:
            para.getparent().remove(para)
        elif text.startswith(("📍Location:", "🎽Event:", "📍地点", "🎽赛事")):
            para.getparent().remove(para)

    html_blocks = [lxml_html.tostring(child, encoding="unicode", method="html") for child in article]
    article_html = "\n".join(html_blocks)
    article_html = article_html.replace("<h2>", '<h2 class="section-label">')
    article_html = article_html.replace("凤凰城马拉松 Vlog 封面", "Buckeye Marathon Vlog 封面")
    article_html = article_html.replace("Phoenix marathon weekend vlog cover", "Buckeye Marathon weekend vlog cover")
    return normalize_image_src(article_html)


def normalize_image_src(value: str) -> str:
    def repl(match: re.Match[str]) -> str:
        return f"img-{int(match.group(1)):03d}.webp"

    value = re.sub(r"(\d{2})-arizona-phoenix-marathon\.webp", repl, value)
    return value.replace("v=20260626-arizona", f"v={VERSION}")


def story_css() -> str:
    return """
    :root {
      --paper: #edf3f7;
      --surface: #ffffff;
      --ink: #20242b;
      --muted: #667085;
      --line: #d0dfe8;
      --accent: #0b67c2;
      --accent2: #d8d6c7;
      --soft: #edf3f7;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      background: linear-gradient(180deg, color-mix(in srgb, var(--accent) 12%, #ffffff) 0, var(--paper) 340px);
      color: var(--ink);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
      line-height: 1.75;
      letter-spacing: 0;
    }
    a { color: var(--accent); text-decoration-thickness: 1px; text-underline-offset: 4px; }
    .story-nav {
      max-width: 900px;
      margin: 0 auto;
      padding: 18px 22px 0;
      display: flex;
      gap: 14px;
      justify-content: space-between;
      color: var(--muted);
      font-size: 14px;
    }
    .story-nav a { color: inherit; text-decoration: none; border-bottom: 1px solid transparent; }
    .story-nav a:hover { border-color: currentColor; }
    .page-header {
      max-width: 900px;
      margin: 0 auto;
      padding: 42px 22px 24px;
    }
    .kicker { margin: 0 0 14px; color: var(--accent); font-size: 14px; font-weight: 850; }
    h1 {
      margin: 0;
      max-width: 820px;
      color: #111827;
      font-size: clamp(29px, 4vw, 42px);
      line-height: 1.18;
      font-weight: 900;
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
      background: rgba(255, 255, 255, .76);
      color: var(--muted);
      text-decoration: none;
    }
    .dek {
      margin: 22px 0 0;
      padding-left: 16px;
      border-left: 4px solid var(--accent);
      color: #344054;
      font-size: 16px;
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
      padding: 54px 22px 64px;
      overflow-wrap: anywhere;
    }
    .article-body p {
      margin: 0 0 22px;
      font-size: 17.5px;
      line-height: 1.82;
      color: #2c323f;
    }
    .article-body p.place {
      margin: -8px 0 24px;
      color: var(--muted);
      font-size: 15px;
      font-weight: 700;
    }
    .article-body h2.section-label {
      margin: 50px 0 20px;
      padding-top: 24px;
      border-top: 1px solid var(--line);
      color: var(--accent);
      font-size: 22px;
      line-height: 1.3;
      font-weight: 850;
    }
    .article-body h2.section-label:first-child {
      margin-top: 0;
      padding-top: 0;
      border-top: 0;
    }
    .article-body h3 {
      margin: 32px 0 16px;
      color: #111827;
      font-size: 19px;
      font-weight: 850;
    }
    figure { margin: 32px 0; }
    figure img {
      display: block;
      width: 100%;
      height: auto;
      border: 1px solid var(--line);
      border-radius: 4px;
      background: #f3f4f6;
    }
    figcaption {
      margin-top: 8px;
      color: var(--muted);
      font-size: 13px;
      line-height: 1.55;
      text-align: center;
    }
    figcaption span { color: #98a2b3; }
    .end-mark, .credit-line {
      text-align: center;
      color: var(--muted);
      font-size: 14px;
    }
    .end-mark { margin: 48px 0 12px; font-weight: 800; }
    .credit-line { margin: 6px 0; }
    .page-footer {
      max-width: 900px;
      margin: 0 auto;
      padding: 42px 22px 64px;
      color: var(--muted);
      font-size: 14px;
      text-align: center;
    }
    @media (max-width: 640px) {
      .story-nav { flex-wrap: wrap; }
      .page-header { padding-top: 32px; }
      .article-body { padding: 42px 18px 54px; }
      .article-body p { font-size: 16.5px; }
    }
    """.strip()


def render_standard_story_page(
    *,
    lang: str,
    nav_label: str,
    back_href: str,
    back_text: str,
    nav_links: list[tuple[str, str]],
    title: str,
    meta_title: str,
    description: str,
    canonical: str,
    asset_prefix: str,
    kicker: str,
    meta_items: list[str],
    article_html: str,
    engagement_locale: str,
    page_key: str,
    comments_id: str,
    engagement_kicker: str,
    engagement_heading: str,
    engagement_note: str,
    views_label: str,
    loading_text: str,
    footer: str,
) -> str:
    nav = "".join(f'<a href="{href}">{html.escape(text)}</a>' for href, text in nav_links)
    meta = "\n      ".join(f"<span>{html.escape(item)}</span>" for item in meta_items)
    return f"""<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(meta_title)}</title>
  <meta name="description" content="{html.escape(description, quote=True)}">
  <link rel="canonical" href="{canonical}">
  <meta property="og:title" content="{html.escape(meta_title, quote=True)}">
  <meta property="og:description" content="{html.escape(description, quote=True)}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="{canonical}">
  <meta property="og:site_name" content="ArsenanZZ">
  <meta property="og:locale" content="{'zh-CN' if lang == 'zh-CN' else 'en_US'}">
  <meta property="og:image" content="{SITE}/assets/og-run50-arizona-phoenix-marathon-icons.png?v={VERSION}">
  <meta property="og:image:secure_url" content="{SITE}/assets/og-run50-arizona-phoenix-marathon-icons.png?v={VERSION}">
  <meta property="og:image:type" content="image/png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="{html.escape(meta_title, quote=True)} cover">
  <meta property="article:author" content="Arsenan">
  <meta property="article:published_time" content="2026-01-10T08:00:00-07:00">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{html.escape(meta_title, quote=True)}">
  <meta name="twitter:description" content="{html.escape(description, quote=True)}">
  <meta name="twitter:image" content="{SITE}/assets/og-run50-arizona-phoenix-marathon-icons.png?v={VERSION}">
  <link rel="stylesheet" href="{asset_prefix}/zz-engagement.css?v=20260605-1">
  <style>
{story_css()}
  </style>
</head>
<body>
  <nav class="story-nav" aria-label="{html.escape(nav_label, quote=True)}">
    <a href="{back_href}">{html.escape(back_text)}</a>{nav}
  </nav>
  <header class="page-header">
    <p class="kicker">{html.escape(kicker)}</p>
    <h1>{html.escape(title)}</h1>
    <div class="meta">
      {meta}
    </div>
    <div class="dek">{html.escape(description)}</div>
  </header>
  <main class="article-shell">
    <article class="article-body">
{article_html}
    </article>
  </main>
  <section class="zz-engagement" data-zz-engagement data-locale="{engagement_locale}" data-page-key="{page_key}">
    <div class="zz-engagement-shell">
      <div>
        <p class="zz-engagement-kicker">{html.escape(engagement_kicker)}</p>
        <h2>{html.escape(engagement_heading)}</h2>
        <p class="zz-engagement-note">{html.escape(engagement_note)}</p>
        <div class="zz-engagement-stats"><span class="zz-engagement-stat" id="busuanzi_container_page_pv"><span>{html.escape(views_label)}</span><strong id="busuanzi_value_page_pv" data-zz-view-count>--</strong></span></div>
      </div>
      <div class="zz-engagement-card"><div id="{comments_id}" data-zz-supabase-comments></div><p class="zz-engagement-status" data-zz-engagement-status>{html.escape(loading_text)}</p></div>
    </div>
  </section>
  <footer class="page-footer">{html.escape(footer)}</footer>
  <script src="{asset_prefix}/zz-engagement-config.js?v=20260605-1"></script>
  <script src="{asset_prefix}/zz-engagement.js?v=20260605-1"></script>
</body>
</html>
"""


def update_index_copy() -> None:
    replacements = {
        ROOT / "run50" / "stories" / "chinese" / "index.html": [
            ("cover-medal-arizona-phoenix-marathon.jpg?v=20260626-arizona", f"cover-medal-arizona-phoenix-marathon.jpg?v={VERSION}"),
            ("Run50 #第29州｜亚利桑那：凤凰城马拉松奖牌封面", "Run50 #第29州｜亚利桑那：Buckeye Marathon 奖牌封面"),
            ("<h2>亚利桑那：凤凰城马拉松</h2>", "<h2>亚利桑那：Buckeye Marathon</h2>"),
        ],
        ROOT / "run50" / "stories" / "english" / "index.html": [
            ("cover-medal-arizona-phoenix-marathon.jpg?v=20260626-arizona", f"cover-medal-arizona-phoenix-marathon.jpg?v={VERSION}"),
        ],
        ROOT / "run50" / "facebook" / "index.html": [
            ("cover-medal-fb-arizona-phoenix-marathon.jpg?v=20260626-arizona", f"cover-medal-fb-arizona-phoenix-marathon.jpg?v={VERSION}"),
        ],
    }
    for path, pairs in replacements.items():
        text = path.read_text(encoding="utf-8")
        for old, new in pairs:
            text = text.replace(old, new)
        path.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    normalize_arizona_story_style()
