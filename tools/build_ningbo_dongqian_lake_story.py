from __future__ import annotations

from html import escape
from pathlib import Path
import json
import re
import tempfile
import time
import urllib.parse
import urllib.request

from lxml import html
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps, ImageSequence


REPO = Path(__file__).resolve().parents[1]
SOURCE_DIR = Path(r"Z:\ZhennanZ Folder\0-Running Story Web\宁波，东钱湖边的聚会_files")
SOURCE_HTML = SOURCE_DIR / "宁波，东钱湖边的聚会.html"
SITE = "https://arsenanzz.github.io/ZZ"
SLUG = "ningbo-dongqian-lake-marathon"
IMAGE_DIR = "RunCN-Ningbo-Dongqian-Lake-Marathon-clean_files"
OUT_IMG_DIR = REPO / "run50" / "stories" / "chinese" / IMAGE_DIR
VERSION = "20260626-medal-polish"
ENGAGEMENT_VERSION = "20260617"
TRANSLATION_CACHE = Path(tempfile.gettempdir()) / "zz_ningbo_dongqian_lake_translation_cache.json"
FONT_DIR = Path(r"C:\Windows\Fonts")

TITLE_ZH = "RunCN 归档｜宁波东钱湖马拉松：宁波，东钱湖边的聚会"
TITLE_EN = "RunCN Archive | Ningbo Dongqian Lake Marathon: a gathering by the lake"
TITLE_FB = "Ningbo turned a lakeside marathon into a warm farewell"
DECK_ZH = "2019 年岁末，在浙江最大的天然湖泊东钱湖边，骑行、跑马、见老友，也走进奉化的历史深处。"
DECK_EN = "At the end of 2019, beside Dongqian Lake in Ningbo, this trip became a warm farewell made of cycling, a marathon, old friendship, and a walk into Fenghua history."
LOCATION_ZH = "浙江宁波 · 东钱湖"
LOCATION_EN = "Ningbo, Zhejiang · Dongqian Lake"
DATE_ZH = "2019.12.08"
DATE_EN = "Dec 8, 2019"
RACE_NAME_ZH = "宁波东钱湖马拉松"
RACE_NAME_EN = "Ningbo Dongqian Lake Marathon"

SPECIAL_TRANSLATIONS = {
    "丨宁波 · 东钱湖丨": "Ningbo · Dongqian Lake",
    "- 宁波寄语 -": "- Message from Ningbo -",
    "是谁去宁波跑马，却囿于咖喱湖泊与爱": "Who went to Ningbo for a marathon, only to be caught by curry, lakes, and love?",
    "前言": "Preface",
    "后记": "Postscript",
    "骑行，刚刚好": "Cycling was just right",
    "跑马，爱爱爱不完": "Running, with love that does not run out",
    "姑娘，这次不尴尬": "This time, seeing the girl was not awkward",
    "双面，走近蒋介石": "Two sides: getting closer to Chiang Kai-shek",
    "- 本文完 -": "- End -",
    "文字丨Arsenan": "Words | Arsenan",
    "摄影丨Arsenan": "Photos | Arsenan",
    "设计丨Arsenan": "Design | Arsenan",
}


def norm(value: str) -> str:
    return re.sub(r"\s+", " ", value.replace("\xa0", " ")).strip()


def is_styleish(value: str) -> bool:
    return ":host {" in value or "--weui-" in value or len(value) > 700


def has_text_descendant(el) -> bool:
    for desc in el.iterdescendants():
        if desc.tag in ("p", "section", "h1", "h2", "h3"):
            text = norm("".join(desc.itertext()))
            if text and not is_styleish(text):
                return True
    return False


def is_caption(value: str) -> bool:
    return value.startswith("▲")


def clean_caption(value: str) -> str:
    return value.lstrip("▲").strip()


def font(size: int, bold: bool = False):
    names = ["arialbd.ttf", "msyhbd.ttc", "simhei.ttf"] if bold else ["arial.ttf", "msyh.ttc", "simhei.ttf"]
    for name in names:
        path = FONT_DIR / name
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def fit_font(draw: ImageDraw.ImageDraw, text: str, max_width: int, start: int, minimum: int, bold: bool = True):
    for size in range(start, minimum - 1, -2):
        candidate = font(size, bold)
        bbox = draw.textbbox((0, 0), text, font=candidate)
        if bbox[2] - bbox[0] <= max_width:
            return candidate
    return font(minimum, bold)


def extract_story() -> list[dict]:
    doc = html.fromstring(SOURCE_HTML.read_text(encoding="utf-8", errors="replace"))
    root = doc.xpath('//*[@id="js_content"]')[0]
    raw: list[dict] = []
    seen_img: set[str] = set()

    def walk(el) -> None:
        if el.tag == "img":
            src = el.get("src") or el.get("data-src") or ""
            cls = el.get("class") or ""
            if src and "rich_pages" in cls and src not in seen_img:
                seen_img.add(src)
                raw.append({"type": "image", "src": src})
            return
        if el.tag in ("p", "section", "h1", "h2", "h3"):
            text = norm("".join(el.itertext()))
            if text and not is_styleish(text) and not has_text_descendant(el):
                if text not in {"继续观看", "宁波，东钱湖边的聚会", "0/0", "\u200d\u200d"}:
                    if not ("Vlog" in text and is_caption(text)):
                        raw.append({"type": "text", "text": text})
                for img in el.xpath(".//img"):
                    walk(img)
                return
        for child in el:
            walk(child)

    walk(root)

    clean: list[dict] = []
    for event in raw:
        key = event.get("text") or event.get("src")
        prev = clean[-1].get("text") or clean[-1].get("src") if clean else None
        if prev == key and clean[-1]["type"] == event["type"]:
            continue
        clean.append(event)

    story: list[dict] = []
    for event in clean:
        story.append(event)
        if event["type"] == "text" and event["text"] == "设计丨Arsenan":
            break
    return story


def local_image_path(src: str) -> Path:
    parsed = urllib.parse.urlparse(src)
    name = Path(urllib.parse.unquote(parsed.path)).name
    if "_files/" in src:
        name = urllib.parse.unquote(src.split("_files/", 1)[1].split("?", 1)[0])
    candidate = SOURCE_DIR / name
    if candidate.exists():
        return candidate
    raise FileNotFoundError(src)


def save_story_image(source: Path, target: Path) -> None:
    with Image.open(source) as image:
        image = ImageOps.exif_transpose(image)
        if getattr(image, "is_animated", False):
            frames = []
            durations = []
            for frame in ImageSequence.Iterator(image):
                frame = ImageOps.exif_transpose(frame).convert("RGB")
                frames.append(frame.copy())
                durations.append(frame.info.get("duration", image.info.get("duration", 80)))
            frames[0].save(
                target,
                "WEBP",
                save_all=True,
                append_images=frames[1:],
                duration=durations,
                loop=image.info.get("loop", 0),
                quality=82,
                method=6,
            )
            return
        if image.mode != "RGB":
            image = image.convert("RGB")
        image.save(target, "WEBP", quality=90, method=6)


def copy_images(events: list[dict]) -> int:
    OUT_IMG_DIR.mkdir(parents=True, exist_ok=True)
    for old in OUT_IMG_DIR.glob("img-*.webp"):
        old.unlink()
    count = 0
    for event in events:
        if event["type"] != "image":
            continue
        count += 1
        out_name = f"img-{count:03d}.webp"
        save_story_image(local_image_path(event["src"]), OUT_IMG_DIR / out_name)
        event["out"] = out_name
    return count


def load_cache() -> dict[str, str]:
    if TRANSLATION_CACHE.exists():
        return json.loads(TRANSLATION_CACHE.read_text(encoding="utf-8"))
    return {}


def save_cache(cache: dict[str, str]) -> None:
    TRANSLATION_CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")


def needs_translation(text: str) -> bool:
    if text in SPECIAL_TRANSLATIONS:
        return False
    if re.fullmatch(r"[A-Za-z0-9 .,'’!?:&@()/-]+", text):
        return False
    return True


def polish_translation(text: str) -> str:
    replacements = {
        "Dongqianhu": "Dongqian Lake",
        "Route Gif": "Route GIF",
        "route Gif": "route GIF",
        "Dongqian Lake Marathon route Gif": "Dongqian Lake Marathon route GIF",
        "cycling route Gif": "cycling route GIF",
        "by Arsenan": "by Arsenan",
        "Miaoer": "Miao'er",
        "Han Qiaosheng": "Han Qiaosheng",
        "Fenghua": "Fenghua",
        "Xikou": "Xikou",
        "Xuedou Mountain": "Xuedou Mountain",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return re.sub(r"\s+", " ", text.replace(" ,", ",").replace(" .", ".")).strip()


def google_translate(texts: list[str]) -> list[str]:
    if not texts:
        return []
    seps = [f"ZZNBSEP{i:04d}ZZ" for i in range(1, len(texts))]
    joined = texts[0]
    for sep, text in zip(seps, texts[1:]):
        joined += f"\n{sep}\n{text}"
    query = urllib.parse.urlencode({"client": "gtx", "sl": "zh-CN", "tl": "en", "dt": "t", "q": joined})
    with urllib.request.urlopen("https://translate.googleapis.com/translate_a/single?" + query, timeout=60) as response:
        data = json.loads(response.read().decode("utf-8"))
    translated = "".join(part[0] for part in data[0])
    pieces = [translated]
    for sep in seps:
        next_pieces: list[str] = []
        for piece in pieces:
            next_pieces.extend(piece.split(sep))
        pieces = next_pieces
    if len(pieces) != len(texts):
        raise RuntimeError("translation split mismatch")
    return [polish_translation(piece) for piece in pieces]


def ensure_translations(events: list[dict]) -> dict[str, str]:
    cache = load_cache()
    missing: list[str] = []
    for event in events:
        if event["type"] != "text":
            continue
        text = clean_caption(event["text"]) if is_caption(event["text"]) else event["text"]
        if needs_translation(text) and text not in cache:
            missing.append(text)
    missing = list(dict.fromkeys(missing))
    print(f"translation cache: {len(cache)} existing, {len(missing)} missing")
    batch: list[str] = []
    chars = 0
    for text in missing:
        if batch and chars + len(text) > 1100:
            for src, dst in zip(batch, google_translate(batch)):
                cache[src] = dst
            save_cache(cache)
            batch = []
            chars = 0
            time.sleep(0.08)
        batch.append(text)
        chars += len(text)
    if batch:
        for src, dst in zip(batch, google_translate(batch)):
            cache[src] = dst
        save_cache(cache)
    return cache


def translate(text: str, cache: dict[str, str]) -> str:
    if text in SPECIAL_TRANSLATIONS:
        return SPECIAL_TRANSLATIONS[text]
    if not needs_translation(text):
        return text
    return polish_translation(cache.get(text, text))


def render_text(text: str, lang: str, cache: dict[str, str]) -> str:
    value = text if lang == "zh" else translate(text, cache)
    source = text
    if source in {"前言", "后记"}:
        return f'<h2 class="section-label">{escape(value)}</h2>'
    if source.startswith("- ") and source.endswith(" -"):
        return f'<p class="end-mark">{escape(value)}</p>'
    if source.startswith(("文字丨", "摄影丨", "设计丨")):
        return f'<p class="credit-line">{escape(value)}</p>'
    if source in {"丨宁波 · 东钱湖丨", "- 宁波寄语 -"}:
        return f'<p class="place">{escape(value)}</p>'
    if re.fullmatch(r"0[1-4]", source):
        return f'<h3 class="section-number">{escape(value)}</h3>'
    if source in {"骑行，刚刚好", "跑马，爱爱爱不完", "姑娘，这次不尴尬", "双面，走近蒋介石"}:
        return f"<h2>{escape(value)}</h2>"
    return f"<p>{escape(value)}</p>"


def render_events(events: list[dict], lang: str, image_prefix: str, cache: dict[str, str]) -> str:
    parts: list[str] = []
    pending_image: str | None = None
    caption_for_next: str | None = None

    def localized_caption(text: str) -> str:
        caption = clean_caption(text)
        return caption if lang == "zh" else translate(caption, cache)

    def flush(caption: str = "") -> None:
        nonlocal pending_image
        if not pending_image:
            return
        number = int(pending_image.split("-")[1].split(".")[0])
        alt_base = f"{LOCATION_EN} story photo" if lang == "en" else f"{LOCATION_ZH}故事照片"
        figcap = f"<figcaption>{escape(caption)}</figcaption>" if caption else ""
        parts.append(
            f'<figure><img src="{image_prefix}{pending_image}" alt="{escape(alt_base)} {number}" '
            f'loading="lazy" decoding="async">{figcap}</figure>'
        )
        pending_image = None

    for event in events:
        if event["type"] == "image":
            flush()
            pending_image = event["out"]
            if caption_for_next:
                flush(caption_for_next)
                caption_for_next = None
            continue
        text = event["text"]
        if is_caption(text):
            caption = localized_caption(text)
            if pending_image:
                flush(caption)
            else:
                caption_for_next = caption
            continue
        flush()
        if caption_for_next:
            parts.append(f'<p class="caption-line">{escape(caption_for_next)}</p>')
            caption_for_next = None
        parts.append(render_text(text, lang, cache))
    flush()
    return "\n      ".join(parts)


def extract_style(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    match = re.search(r"<style>(.*?)</style>", text, re.S)
    if not match:
        raise RuntimeError(f"No style block in {path}")
    css = match.group(1)
    css = "\n".join(line.rstrip() for line in css.splitlines())
    return css + "\n    :root { --accent:#cc0000; --soft:#faf2ee; }\n    .section-number { color:var(--accent); font-size:18px; letter-spacing:.12em; margin-top:34px; }\n"


def engagement(locale: str, key: str, ident: str, depth: str) -> str:
    if locale == "zh-CN":
        return f'''<section class="zz-engagement" data-zz-engagement data-locale="zh-CN" data-page-key="{key}">
    <div class="zz-engagement-shell">
      <div>
        <p class="zz-engagement-kicker">留言 / 访问次数</p>
        <h2>跑完也可以聊两句</h2>
        <p class="zz-engagement-note">不用注册账号即可提交留言，提交后会直接显示。</p>
        <div class="zz-engagement-stats">
          <span class="zz-engagement-stat" id="busuanzi_container_page_pv"><span>访问</span><strong id="busuanzi_value_page_pv" data-zz-view-count>--</strong><span>次</span></span>
        </div>
      </div>
      <div class="zz-engagement-card"><div id="{ident}" data-zz-supabase-comments></div><p class="zz-engagement-status" data-zz-engagement-status>留言区加载中...</p></div>
    </div>
  </section>
  <script src="{depth}assets/zz-engagement-config.js?v={ENGAGEMENT_VERSION}"></script>
  <script src="{depth}assets/zz-engagement.js?v={ENGAGEMENT_VERSION}"></script>'''
    return f'''<section class="zz-engagement" data-zz-engagement data-locale="en" data-page-key="{key}">
    <div class="zz-engagement-shell">
      <div>
        <p class="zz-engagement-kicker">Comments / Views</p>
        <h2>Say something after the run</h2>
        <p class="zz-engagement-note">No account is needed to submit a comment. New comments appear right away.</p>
        <div class="zz-engagement-stats"><span class="zz-engagement-stat" id="busuanzi_container_page_pv"><span>Views</span><strong id="busuanzi_value_page_pv" data-zz-view-count>--</strong></span></div>
      </div>
      <div class="zz-engagement-card"><div id="{ident}" data-zz-supabase-comments></div><p class="zz-engagement-status" data-zz-engagement-status>Loading comments...</p></div>
    </div>
  </section>
  <script src="{depth}assets/zz-engagement-config.js?v={ENGAGEMENT_VERSION}"></script>
  <script src="{depth}assets/zz-engagement.js?v={ENGAGEMENT_VERSION}"></script>'''


def normal_page(lang: str, article: str, css: str) -> str:
    zh = lang == "zh"
    if zh:
        page_lang = "zh-CN"
        title = TITLE_ZH
        desc = DECK_ZH
        canonical = f"{SITE}/run50/stories/chinese/{SLUG}.html"
        nav = f'<a href="./index.html">← 中文故事</a><a href="../english/{SLUG}.html">English</a><a href="../../facebook/{SLUG}.html">Facebook</a><a href="../../index.html">Run50</a>'
        meta = f"<span>Arsenan</span><span>{DATE_ZH}</span><span>RunCN 归档</span><span>{RACE_NAME_ZH}</span>"
        kicker = "RunCN 归档 · 浙江宁波"
        engage = engagement("zh-CN", f"run50-{SLUG}-zh", f"supabase-comments-{SLUG}-zh", "../../../")
        og_locale = "zh_CN"
    else:
        page_lang = "en"
        title = TITLE_EN
        desc = DECK_EN
        canonical = f"{SITE}/run50/stories/english/{SLUG}.html"
        nav = f'<a href="./index.html">← English Stories</a><a href="../chinese/{SLUG}.html">中文</a><a href="../../facebook/{SLUG}.html">Facebook</a><a href="../../index.html">Run50</a>'
        meta = f'<span>Arsenan</span><span>{DATE_EN}</span><span>RunCN Archive</span><span>{RACE_NAME_EN}</span><a href="../chinese/{SLUG}.html">Original Chinese</a>'
        kicker = "RunCN Archive · Ningbo"
        engage = engagement("en", f"run50-{SLUG}-en", f"supabase-comments-{SLUG}-en", "../../../")
        og_locale = "en_US"

    og_img = f"{SITE}/assets/og-run50-{SLUG}-icons.png"
    cover = f"../../../assets/cover-medal-{SLUG}.jpg?v={VERSION}"
    return f'''<!doctype html>
<html lang="{page_lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)}</title>
  <meta name="description" content="{escape(desc)}">
  <link rel="canonical" href="{canonical}">
  <meta property="og:title" content="{escape(title)}">
  <meta property="og:description" content="{escape(desc)}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="{canonical}">
  <meta property="og:site_name" content="ArsenanZZ">
  <meta property="og:locale" content="{og_locale}">
  <meta property="og:image" content="{og_img}">
  <meta property="og:image:secure_url" content="{og_img}">
  <meta property="og:image:type" content="image/png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="article:author" content="Arsenan">
  <meta property="article:published_time" content="2019-12-15T23:00:00+08:00">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{escape(title)}">
  <meta name="twitter:description" content="{escape(desc)}">
  <meta name="twitter:image" content="{og_img}">
  <link rel="stylesheet" href="../../../assets/zz-engagement.css?v={ENGAGEMENT_VERSION}">
  <style>{css}</style>
</head>
<body>
  <nav class="story-nav" aria-label="Page navigation">{nav}</nav>
  <header class="page-header">
    <p class="kicker">{escape(kicker)}</p>
    <h1>{escape(title)}</h1>
    <div class="meta">{meta}</div>
    <p class="dek">{escape(desc)}</p>
    <img class="cover" src="{cover}" alt="{escape(title)} cover" loading="eager" decoding="async">
  </header>
  <main class="article-shell"><article class="article-body">
      {article}
  </article></main>
  {engage}
</body>
</html>
'''


def facebook_page(article: str, css: str) -> str:
    desc = f"Race date: {DATE_EN}. A full marathon around Dongqian Lake, plus a cycling warm-up, an old friendship in Ningbo, and a walk through Fenghua history."
    og_img = f"{SITE}/assets/og-run50-{SLUG}-icons.png"
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(TITLE_FB)} | Run50 Facebook</title>
  <meta name="description" content="{escape(desc)}">
  <link rel="canonical" href="{SITE}/run50/facebook/{SLUG}.html">
  <meta property="og:title" content="{escape(TITLE_FB)}">
  <meta property="og:description" content="{escape(desc)}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="{SITE}/run50/facebook/{SLUG}.html">
  <meta property="og:site_name" content="ArsenanZZ">
  <meta property="og:locale" content="en_US">
  <meta property="og:image" content="{og_img}">
  <meta property="og:image:secure_url" content="{og_img}">
  <meta property="og:image:type" content="image/png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="article:author" content="Arsenan">
  <meta property="article:published_time" content="2019-12-15T23:00:00+08:00">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{escape(TITLE_FB)}">
  <meta name="twitter:description" content="{escape(desc)}">
  <meta name="twitter:image" content="{og_img}">
  <link rel="stylesheet" href="../../assets/zz-engagement.css?v={ENGAGEMENT_VERSION}">
  <style>{css}</style>
</head>
<body>
  <div class="breaking"><div class="breaking-inner"><a href="./index.html">Run50 Facebook</a><span>Ningbo / China / Dongqian Lake</span></div></div>
  <header class="site-head"><div class="site-head-inner"><div class="wordmark">Run50</div><nav class="section-nav" aria-label="Story links"><a href="../stories/english/{SLUG}.html">Full English</a><a href="../stories/chinese/{SLUG}.html">中文原文</a><a href="../index.html">Run50</a></nav></div></header>
  <article class="article">
    <section class="hero">
      <span class="label">RunCN / China / Marathon</span>
      <h1>{escape(TITLE_FB)}</h1>
      <p class="dek">{escape(desc)}</p>
      <div class="byline"><span>By Arsenan</span><span>{LOCATION_EN}</span><span>{DATE_EN}</span></div>
      <figure class="lead-media"><img src="../../assets/og-run50-{SLUG}-icons.png" alt="Icon-style Ningbo Dongqian Lake Marathon cover"><figcaption>Dongqian Lake, cycling, marathon roads, Fenghua history, and a finisher medal.</figcaption></figure>
    </section>
    <section class="story-grid">
      <aside class="rail">
        <section class="brief-box"><h2>At a glance</h2><dl><div><dt>Race</dt><dd>{RACE_NAME_EN}</dd></div><div><dt>Course</dt><dd>A lakeside marathon through Dongqian Lake, villages, climbs, descents, and tunnel roads.</dd></div><div><dt>What stayed with me</dt><dd>A 43 km cycling warm-up, a 4:08 finish, curry with an old friend, and Fenghua history after the race.</dd></div></dl></section>
        <section class="share-note"><strong>Notes</strong>The comments box is below the story. New comments appear right away.</section>
      </aside>
      <div class="copy full-story">
        {article}
      </div>
    </section>
  </article>
  {engagement("en", f"run50-{SLUG}-facebook-en", f"supabase-comments-{SLUG}-facebook-en", "../../")}
</body>
</html>
'''


def create_medal_cover() -> None:
    src = OUT_IMG_DIR / "img-033.webp"
    assets = REPO / "assets"
    for target_name in [f"cover-medal-{SLUG}.jpg", f"cover-medal-fb-{SLUG}.jpg"]:
        with Image.open(src) as im:
            im = ImageOps.exif_transpose(im).convert("RGB")
            bg = ImageOps.fit(im, (1200, 750), method=Image.Resampling.LANCZOS).filter(ImageFilter.GaussianBlur(16))
            bg = Image.blend(bg, Image.new("RGB", bg.size, (250, 244, 239)), 0.38)
            fg = im.copy()
            fg.thumbnail((820, 590), Image.Resampling.LANCZOS)
            x = (1200 - fg.width) // 2
            y = (750 - fg.height) // 2 + 18
            bg.paste(fg, (x, y))
            draw = ImageDraw.Draw(bg)
            draw.rounded_rectangle((46, 40, 630, 160), radius=22, fill=(255, 255, 255), outline=(32, 36, 43), width=4)
            draw.text((64, 58), "NINGBO", font=font(58, True), fill="#20242b")
            draw.text((66, 120), "DONGQIAN LAKE MARATHON", font=font(25, True), fill="#667085")
            bg.save(assets / target_name, "JPEG", quality=92)


def create_icon_covers() -> None:
    assets = REPO / "assets"
    image = Image.new("RGB", (1200, 630), "#faf2ee")
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 395, 1200, 630), fill="#d8e9ee")
    draw.ellipse((-80, 300, 1280, 740), fill="#b8dce8")
    draw.rectangle((0, 515, 1200, 630), fill="#f4d7c8")
    draw.arc((90, 285, 1070, 760), 200, 342, fill="#2f7d6f", width=16)
    draw.arc((130, 322, 1030, 740), 202, 340, fill="#ffffff", width=8)
    draw.polygon([(110, 350), (230, 230), (355, 350)], fill="#8cbf8d")
    draw.polygon([(290, 370), (470, 210), (650, 370)], fill="#72a870")
    draw.polygon([(600, 360), (790, 235), (990, 360)], fill="#8fc28f")
    draw.rectangle((720, 356, 1020, 374), fill="#b0663f")
    for x in range(735, 1010, 38):
        draw.line((x, 356, x + 22, 374), fill="#fff7ed", width=5)
    draw.ellipse((240, 430, 330, 520), outline="#20242b", width=8)
    draw.ellipse((390, 430, 480, 520), outline="#20242b", width=8)
    draw.line((285, 475, 390, 475), fill="#20242b", width=8)
    draw.line((340, 415, 390, 475), fill="#20242b", width=8)
    draw.line((340, 415, 430, 415), fill="#20242b", width=8)
    draw.ellipse((615, 430, 660, 475), outline="#cc0000", width=8)
    draw.line((638, 475, 638, 555), fill="#20242b", width=8)
    draw.line((638, 505, 590, 548), fill="#20242b", width=8)
    draw.line((638, 505, 690, 545), fill="#20242b", width=8)
    draw.line((638, 555, 600, 605), fill="#20242b", width=8)
    draw.line((638, 555, 690, 606), fill="#20242b", width=8)
    draw.ellipse((850, 435, 1010, 595), fill="#f4c542", outline="#20242b", width=7)
    draw.ellipse((888, 473, 972, 557), fill="#fff7d6", outline="#cc0000", width=6)
    draw.text((64, 64), "NINGBO", font=font(66, True), fill="#20242b")
    draw.text((66, 136), "DONGQIAN LAKE MARATHON", font=font(26, True), fill="#667085")
    draw.rounded_rectangle((760, 64, 1122, 228), radius=22, fill="#ffffff", outline="#20242b", width=7)
    draw.text((790, 112), "RunCN", font=font(40, True), fill="#20242b")
    badge_font = fit_font(draw, "NINGBO", 302, 52, 36, True)
    draw.text((790, 166), "NINGBO", font=badge_font, fill="#cc0000")
    image.save(assets / f"og-run50-{SLUG}-icons.png", "PNG")

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 750" role="img" aria-labelledby="title desc">
<title id="title">Ningbo Dongqian Lake Marathon icon cover</title>
<desc id="desc">Icon cover with Dongqian Lake, hills, bridge, bicycle, runner, medal, and RunCN badge.</desc>
<rect width="1200" height="750" fill="#faf2ee"/>
<rect y="470" width="1200" height="280" fill="#d8e9ee"/>
<ellipse cx="600" cy="565" rx="690" ry="190" fill="#b8dce8"/>
<rect y="620" width="1200" height="130" fill="#f4d7c8"/>
<path d="M110 420 Q240 250 370 420" fill="#8cbf8d"/>
<path d="M310 440 Q480 240 660 440" fill="#72a870"/>
<path d="M610 430 Q800 270 1000 430" fill="#8fc28f"/>
<path d="M720 430 L1030 430" stroke="#b0663f" stroke-width="18"/>
<path d="M120 430 Q600 620 1080 430" fill="none" stroke="#2f7d6f" stroke-width="18"/>
<path d="M150 468 Q600 650 1050 468" fill="none" stroke="#fff" stroke-width="8"/>
<circle cx="290" cy="570" r="48" fill="none" stroke="#20242b" stroke-width="8"/>
<circle cx="455" cy="570" r="48" fill="none" stroke="#20242b" stroke-width="8"/>
<path d="M290 570 L390 500 L455 570 L350 570 L390 500 L450 500" fill="none" stroke="#20242b" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
<circle cx="670" cy="525" r="22" fill="none" stroke="#cc0000" stroke-width="8"/>
<path d="M670 548 L670 640 M670 585 L620 630 M670 585 L720 625 M670 640 L630 705 M670 640 L720 705" fill="none" stroke="#20242b" stroke-width="8" stroke-linecap="round"/>
<circle cx="930" cy="590" r="82" fill="#f4c542" stroke="#20242b" stroke-width="8"/>
<circle cx="930" cy="590" r="43" fill="#fff7d6" stroke="#cc0000" stroke-width="7"/>
<text x="70" y="104" font-family="Arial, Helvetica, sans-serif" font-size="66" font-weight="900" fill="#20242b">NINGBO</text>
<text x="72" y="150" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="800" fill="#667085">DONGQIAN LAKE MARATHON</text>
<rect x="758" y="62" width="364" height="166" rx="22" fill="#ffffff" stroke="#20242b" stroke-width="8"/>
<text x="790" y="122" font-family="Arial, Helvetica, sans-serif" font-size="41" font-weight="900" fill="#20242b">RunCN</text>
<text x="790" y="182" font-family="Arial, Helvetica, sans-serif" font-size="52" font-weight="900" fill="#cc0000">NINGBO</text>
</svg>
'''
    (assets / f"thumb-run50-{SLUG}-icons.svg").write_text(svg, encoding="utf-8", newline="\n")


def replace_once(text: str, old: str, new: str) -> str:
    if old not in text:
        raise RuntimeError(f"anchor not found: {old[:80]}")
    return text.replace(old, new, 1)


def insert_after_card(text: str, href: str, card: str) -> str:
    if f'href="./{SLUG}.html"' in text:
        return text
    pattern = re.compile(rf'(<a class="story-card run-cn" href="{re.escape(href)}".*?</a>)', re.S)
    match = pattern.search(text)
    if not match:
        raise RuntimeError(f"card anchor not found: {href}")
    return text[: match.end()] + "\n\n" + card + text[match.end():]


def update_indexes() -> None:
    zh_card = f'''        <a class="story-card run-cn" href="./{SLUG}.html">
          <img src="../../../assets/cover-medal-{SLUG}.jpg?v={VERSION}" alt="{TITLE_ZH}" loading="lazy" decoding="async">
          <div class="story-copy">
            <p class="story-meta">浙江宁波 · {DATE_ZH}</p>
            <h2 class="story-title">{TITLE_ZH}</h2>
            <p class="story-desc">{DECK_ZH}</p>
            <div class="story-foot"><span>长文图记</span><span>阅读 →</span></div>
          </div>
        </a>'''
    en_card = f'''        <a class="story-card run-cn" href="./{SLUG}.html" data-map-meta="Ningbo, Zhejiang · {DATE_EN}">
          <img src="../../../assets/cover-medal-fb-{SLUG}.jpg?v={VERSION}" alt="Ningbo, Zhejiang cover" loading="lazy" decoding="async">
          <div class="story-copy">
            <p class="story-meta">Ningbo, Zhejiang · RunCN Archive</p>
            <h2 class="story-title">{TITLE_FB}</h2>
            <p class="story-desc">Dongqian Lake cycling, a 4:08 full marathon, curry with an old friend, and a post-race walk into Fenghua history.</p>
            <div class="story-foot"><span>Run50 Facebook</span><span>Read →</span></div>
          </div>
        </a>'''
    fb_card = en_card.replace("../../../assets/", "../../assets/").replace(' data-map-meta="Ningbo, Zhejiang · Dec 8, 2019"', "")

    zh_index = REPO / "run50" / "stories" / "chinese" / "index.html"
    text = zh_index.read_text(encoding="utf-8")
    text = insert_after_card(text, './shanghai-vertical-marathon.html', zh_card)
    if "ningbo-dongqian-lake-marathon.html" not in re.search(r"name:'宁波'.*?\}\s*,", text, re.S).group(0) if re.search(r"name:'宁波'.*?\}\s*,", text, re.S) else True:
        ningbo_record = f'''      {{ name:'宁波', province:'cn_zhejiang', lat:29.8683, lon:121.5440, races:[
        {{ title:'RunCN 归档｜宁波东钱湖马拉松', date:'{DATE_ZH}', url:'./{SLUG}.html' }}
      ]}},
'''
        text = replace_once(text, "      { name:'海口', province:'cn_hainan'", ningbo_record + "      { name:'海口', province:'cn_hainan'")
    zh_index.write_text(text, encoding="utf-8", newline="\n")

    en_index = REPO / "run50" / "stories" / "english" / "index.html"
    text = en_index.read_text(encoding="utf-8")
    text = insert_after_card(text, './shanghai-vertical-marathon.html', en_card)
    if "ningbo-dongqian-lake-marathon.html" not in re.search(r"name:'Ningbo'.*?\}\s*,", text, re.S).group(0) if re.search(r"name:'Ningbo'.*?\}\s*,", text, re.S) else True:
        ningbo_record = f'''      {{ name:'Ningbo', province:'cn_zhejiang', lat:29.8683, lon:121.5440, races:[
        {{ title:'Ningbo Dongqian Lake Marathon', date:'{DATE_EN}', url:'./{SLUG}.html' }}
      ]}},
'''
        text = replace_once(text, "      { name:'Haikou', province:'cn_hainan'", ningbo_record + "      { name:'Haikou', province:'cn_hainan'")
    en_index.write_text(text, encoding="utf-8", newline="\n")

    fb_index = REPO / "run50" / "facebook" / "index.html"
    text = fb_index.read_text(encoding="utf-8")
    text = insert_after_card(text, './shanghai-vertical-marathon.html', fb_card)
    fb_index.write_text(text, encoding="utf-8", newline="\n")


def main() -> None:
    events = extract_story()
    image_count = copy_images(events)
    cache = ensure_translations(events)
    normal_css = extract_style(REPO / "run50" / "stories" / "chinese" / "west-lake-half-marathon.html")
    fb_css = extract_style(REPO / "run50" / "facebook" / "west-lake-half-marathon.html").replace("#0b67c2", "#cc0000")
    zh_article = render_events(events, "zh", f"{IMAGE_DIR}/", cache)
    en_article = render_events(events, "en", f"../chinese/{IMAGE_DIR}/", cache)
    fb_article = "\n        ".join(
        [
            '<section class="context-note"><p>Dongqian Lake was not only a race course. For this 2019 trip, it was a way to say goodbye before returning north, a reason to ride around the lake, and a reason to meet an old friend without the awkwardness of youth.</p></section>',
            render_events(events, "en", f"../stories/chinese/{IMAGE_DIR}/", cache),
        ]
    )
    (REPO / "run50" / "stories" / "chinese" / f"{SLUG}.html").write_text(normal_page("zh", zh_article, normal_css), encoding="utf-8", newline="\n")
    (REPO / "run50" / "stories" / "english" / f"{SLUG}.html").write_text(normal_page("en", en_article, normal_css), encoding="utf-8", newline="\n")
    (REPO / "run50" / "facebook" / f"{SLUG}.html").write_text(facebook_page(fb_article, fb_css), encoding="utf-8", newline="\n")
    create_medal_cover()
    create_icon_covers()
    update_indexes()
    print(f"Ningbo Dongqian Lake story built. events={len(events)} images={image_count}")


if __name__ == "__main__":
    main()
