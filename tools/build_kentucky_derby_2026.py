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
from PIL import Image, ImageDraw, ImageFont, ImageOps


REPO = Path(__file__).resolve().parents[1]
WORK_SOURCE = Path(
    r"C:\Users\ZZ\Documents\Codex\2026-06-26\https-mp-weixin-qq-com-cgi\work\kentucky_source\source_files"
)
SOURCE_HTML = next(p for p in WORK_SOURCE.glob("*.html") if p.name != "s.html")
SITE = "https://arsenanzz.github.io/ZZ"
SLUG = "kentucky-derby-marathon"
IMAGE_DIR = "Run50-Kentucky-Derby-Marathon-clean_files"
VERSION = "20260626-ky-derby"
ENGAGEMENT_VERSION = "20260616"
TRANSLATION_CACHE = Path(tempfile.gettempdir()) / "zz_kentucky_derby_2026_translation_cache.json"
FONT_DIR = Path(r"C:\Windows\Fonts")

TITLE_ZH = "Run50 #第1州｜肯塔基：赛马节马拉松｜四刷主场，蓝草州终破4！"
TITLE_EN = "Run50 #1 | Kentucky Derby Marathon: fourth time at home, finally under four"
TITLE_FB = "Louisville turned my fourth Derby Marathon into a hometown sub-four"
DECK_ZH = "第四次回到 Louisville Derby Marathon，从赛马节、热气球、Old Louisville、Churchill Downs 到 Iroquois Park，终于在主场把全马跑进四小时。"
DECK_EN = "My fourth Louisville Derby Marathon brought together Derby season, hot-air balloons, Old Louisville, Churchill Downs, Iroquois Park, and finally a hometown sub-four."
LOCATION_ZH = "路易斯维尔，肯塔基"
LOCATION_EN = "Louisville, Kentucky"
DATE_ZH = "2026.04.25"
DATE_EN = "Apr 25, 2026"
RACE_NAME = "Kentucky Derby Marathon"

SPECIAL_TRANSLATIONS = {
    "- Run50# 第1州全马 -": "- Run50 #1 Full Marathon -",
    "📍地点：路易斯维尔，肯塔基": "Location: Louisville, Kentucky",
    "🎽赛事：Kentucky Derby Marathon": "Race: Kentucky Derby Marathon",
    "前言": "Preface",
    "后记": "Postscript",
    "- 本文完 -": "- End -",
    "文字丨Arsenan": "Words | Arsenan",
    "摄影丨Arsenan": "Photos | Arsenan",
    "设计丨Arsenan": "Design | Arsenan",
    "🍹Louisville, KY": "Louisville, KY",
}


def norm(value: str) -> str:
    return re.sub(r"\s+", " ", value.replace("\xa0", " ")).strip()


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


def extract_items() -> list[dict]:
    doc = html.fromstring(SOURCE_HTML.read_text(encoding="utf-8", errors="replace"))
    raw: list[dict] = []
    for el in doc.iter():
        if el.tag == "img":
            src = el.get("src") or el.get("data-src") or ""
            cls = el.get("class") or ""
            if src and "rich_pages" in cls and "640" in src:
                raw.append({"type": "image", "src": src})
            continue
        if el.tag not in ("p", "section", "h1", "h2", "h3"):
            continue
        text = norm("".join(el.itertext()))
        if not text or len(text) > 500:
            continue
        if ":host {" in text or "--weui-" in text:
            continue
        raw.append({"type": "text", "text": text})

    start = next(i for i, item in enumerate(raw) if item["type"] == "text" and item["text"] == "- Run50# 第1州全马 -")
    end = next(i for i, item in enumerate(raw) if item["type"] == "text" and item["text"] == "设计丨Arsenan") + 1
    story = raw[start:end]

    cleaned: list[dict] = []
    last_heading: str | None = None
    for item in story:
        if item["type"] == "text":
            text = item["text"]
            if "📍" in text and "🎽" in text:
                continue
            if set(text) <= {"★"}:
                continue
            if text.startswith("# "):
                title = re.sub(r"🍹Louisville, KY$", "", text[2:]).strip()
                if title == last_heading:
                    continue
                last_heading = title
                cleaned.append({"type": "text", "text": "# " + title})
                continue
            if text == last_heading:
                continue
            if cleaned and cleaned[-1]["type"] == "text" and cleaned[-1]["text"] == text:
                continue
        cleaned.append(item)
    return cleaned


def local_image_path(src: str) -> Path:
    if "_files/" in src:
        name = src.split("_files/", 1)[1].split("?", 1)[0]
    else:
        parsed = urllib.parse.urlparse(src)
        name = Path(parsed.path).name
    name = urllib.parse.unquote(name)
    candidate = WORK_SOURCE / name
    if candidate.exists():
        return candidate
    raise FileNotFoundError(src)


def copy_images(events: list[dict]) -> int:
    out_dir = REPO / "run50" / "stories" / "chinese" / IMAGE_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    for old in out_dir.glob("img-*.webp"):
        old.unlink()
    count = 0
    seen: set[str] = set()
    for event in events:
        if event["type"] != "image":
            continue
        src = event["src"]
        if src in seen:
            event["skip"] = True
            continue
        seen.add(src)
        count += 1
        out_name = f"img-{count:03d}.webp"
        with Image.open(local_image_path(src)) as image:
            image = ImageOps.exif_transpose(image)
            if image.mode != "RGB":
                image = image.convert("RGB")
            image.save(out_dir / out_name, "WEBP", quality=90, method=6)
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
    if text.startswith("▲"):
        return False
    if re.fullmatch(r"[A-Za-z0-9 .,'’!?:&@()/-]+", text):
        return False
    return True


def polish_translation(text: str) -> str:
    replacements = {
        "horse pull loose": "marathon",
        "Derby horse": "Derby Marathon",
        "full horse": "full marathon",
        "half horse": "half marathon",
        "Run Fifty": "Run50",
        "Louisville Derby Horse": "Louisville Derby Marathon",
        "race horse": "marathon",
        "competition": "race",
        "Competition": "Race",
        "bib number": "bib",
        "number cloth": "bib",
        "Old Road Easyville": "Old Louisville",
        "Churchill Tangsi": "Churchill Downs",
        "Iroquois": "Iroquois",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return re.sub(r"\s+", " ", text.replace(" ,", ",").replace(" .", ".")).strip()


def google_translate(texts: list[str]) -> list[str]:
    if not texts:
        return []
    seps = [f"ZZKYSEP{i:04d}ZZ" for i in range(1, len(texts))]
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
    missing = []
    for event in events:
        if event["type"] == "text":
            key = event["text"][2:].strip() if event["text"].startswith("# ") else event["text"]
            if needs_translation(key) and key not in cache:
                missing.append(key)
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
    if text.startswith("▲"):
        return text
    key = text[2:].strip() if text.startswith("# ") else text
    if not needs_translation(key):
        return key
    return cache.get(key, key)


def is_caption(text: str) -> bool:
    return text.startswith("▲")


def render_text(text: str, lang: str, cache: dict[str, str]) -> str:
    value = text if lang == "zh" else translate(text, cache)
    clean = value[2:].strip() if value.startswith("# ") else value
    source_clean = text[2:].strip() if text.startswith("# ") else text
    if text.startswith("# "):
        return f"<h2>{escape(clean)}</h2>"
    if source_clean in {"前言", "后记"}:
        return f'<h2 class="section-label">{escape(clean)}</h2>'
    if source_clean.startswith("- ") and source_clean.endswith(" -"):
        return f'<p class="end-mark">{escape(clean)}</p>'
    if source_clean.startswith(("文字丨", "摄影丨", "设计丨")):
        return f'<p class="credit-line">{escape(clean)}</p>'
    if source_clean.startswith(("📍", "🎽", "🍹")):
        return f'<p class="place">{escape(clean)}</p>'
    return f"<p>{escape(clean)}</p>"


def render_events(events: list[dict], lang: str, image_prefix: str, cache: dict[str, str]) -> str:
    parts: list[str] = []
    pending_caption: str | None = None
    for event in events:
        if event["type"] == "image":
            if event.get("skip"):
                continue
            number = int(event["out"].split("-")[1].split(".")[0])
            alt = f"{LOCATION_EN} story photo {number}" if lang == "en" else f"{LOCATION_ZH}故事照片 {number}"
            figure = f'<figure><img src="{image_prefix}{event["out"]}" alt="{escape(alt)}" loading="lazy" decoding="async">'
            if pending_caption:
                figure += f"<figcaption>{escape(pending_caption)}</figcaption>"
                pending_caption = None
            figure += "</figure>"
            parts.append(figure)
            continue
        text = event["text"]
        if is_caption(text):
            caption = text[1:].strip()
            if parts and parts[-1].endswith("</figure>") and "<figcaption>" not in parts[-1]:
                parts[-1] = parts[-1].replace("</figure>", f"<figcaption>{escape(caption)}</figcaption></figure>")
            else:
                pending_caption = caption
            continue
        if pending_caption:
            parts.append(f'<p class="caption-line">{escape(pending_caption)}</p>')
            pending_caption = None
        parts.append(render_text(text, lang, cache))
    return "\n      ".join(parts)


STORY_CSS = """
    :root { color-scheme: light; --ink:#20242b; --muted:#667085; --paper:#edf3f7; --line:#d0dfe8; --blue:#0b67c2; }
    * { box-sizing: border-box; }
    body { margin:0; font-family: Inter, "Segoe UI", Arial, sans-serif; background:#f6f9fb; color:var(--ink); line-height:1.78; letter-spacing:0; }
    a { color:inherit; text-underline-offset:4px; }
    nav { max-width:1080px; margin:0 auto; padding:22px 20px; display:flex; gap:18px; justify-content:flex-end; font-weight:800; color:#526170; flex-wrap:wrap; }
    nav a { text-decoration:none; }
    .hero { background:linear-gradient(180deg,#e7f1f6,#f6f9fb); border-bottom:1px solid var(--line); }
    .hero-inner { max-width:1080px; margin:0 auto; padding:34px 20px 42px; }
    .eyebrow { color:var(--blue); font-size:13px; font-weight:900; letter-spacing:.08em; text-transform:uppercase; }
    h1 { margin:10px 0 14px; font-family: Georgia, "Times New Roman", serif; font-size:clamp(34px,5vw,64px); line-height:1.04; letter-spacing:0; max-width:980px; }
    .deck { max-width:840px; color:#53606b; font-size:19px; margin:0 0 22px; }
    .meta-row { display:flex; flex-wrap:wrap; gap:10px; margin:22px 0 28px; }
    .meta-row span { border:1px solid var(--line); background:#fff; border-radius:999px; padding:8px 13px; font-size:13px; font-weight:800; color:#344252; }
    .cover { width:100%; max-width:980px; display:block; border-radius:8px; border:1px solid var(--line); box-shadow:0 24px 60px rgba(15,23,42,.12); background:#cfe9f4; }
    main { max-width:860px; margin:0 auto; padding:40px 20px 72px; }
    article { background:#fff; border:1px solid var(--line); border-radius:8px; padding:clamp(22px,4vw,44px); box-shadow:0 18px 48px rgba(15,23,42,.08); overflow-wrap:anywhere; }
    article p { margin:0 0 18px; font-size:18px; }
    article h2 { margin:34px 0 14px; font-family: Georgia, "Times New Roman", serif; font-size:32px; line-height:1.2; }
    .section-label { color:var(--blue); font-weight:900; letter-spacing:.08em; text-transform:uppercase; }
    .place { color:#334155; font-weight:850; }
    .credit-line, .end-mark { text-align:center; color:var(--muted); font-weight:850; }
    figure { margin:26px 0; }
    figure img { width:100%; height:auto; display:block; border-radius:8px; border:1px solid #d7e3ea; background:#f4f7f9; }
    figcaption, .caption-line { margin-top:8px; color:#6a7480; font-size:14px; text-align:center; }
    @media (max-width: 620px) { nav { justify-content:flex-start; } article { padding:20px 16px; } article p { font-size:17px; } }
"""


FB_CSS = """
    :root { --red:#0b67c2; --ink:#111; --muted:#666; --line:#d9d9d9; --soft:#f4f4f4; --paper:#fff; }
    * { box-sizing:border-box; }
    body { margin:0; background:var(--paper); color:var(--ink); font-family:Arial,Helvetica,sans-serif; line-height:1.62; letter-spacing:0; }
    a { color:inherit; }
    .topbar { border-bottom:1px solid var(--line); padding:12px 20px; display:flex; justify-content:space-between; gap:12px; flex-wrap:wrap; font-size:13px; font-weight:800; text-transform:uppercase; }
    .masthead { max-width:1180px; margin:0 auto; padding:34px 20px 30px; border-bottom:4px solid var(--ink); }
    .brand { color:var(--red); font-size:13px; font-weight:900; letter-spacing:.08em; text-transform:uppercase; }
    h1 { max-width:980px; margin:10px 0 12px; font-family:Georgia,"Times New Roman",serif; font-size:clamp(36px,6vw,74px); line-height:.98; letter-spacing:0; }
    .summary { max-width:860px; color:#333; font-size:20px; margin:0; }
    .meta-row { display:flex; flex-wrap:wrap; gap:8px; margin-top:20px; }
    .meta-row span { border:1px solid var(--line); background:var(--soft); padding:7px 10px; font-size:12px; font-weight:800; text-transform:uppercase; }
    .content-grid { max-width:1180px; margin:0 auto; padding:30px 20px 70px; display:grid; grid-template-columns:minmax(0,1fr) 300px; gap:34px; align-items:start; }
    article { max-width:760px; }
    article p { margin:0 0 18px; font-size:18px; }
    article h2 { margin:34px 0 14px; font-family:Georgia,"Times New Roman",serif; font-size:32px; line-height:1.14; }
    .section-label { color:var(--red); font-family:Arial,Helvetica,sans-serif; font-size:18px; letter-spacing:.08em; text-transform:uppercase; }
    .lede { padding:18px 0 20px; border-top:1px solid var(--line); border-bottom:1px solid var(--line); font-size:21px; font-weight:700; }
    figure { margin:25px 0; }
    figure img { width:100%; height:auto; display:block; border-radius:4px; background:#eee; }
    figcaption,.caption-line { margin-top:7px; color:#777; font-size:13px; text-align:center; }
    .place,.credit-line,.end-mark { color:#555; font-weight:800; }
    .credit-line,.end-mark { text-align:center; }
    .rail { position:sticky; top:18px; border-top:6px solid var(--red); background:#f7f7f7; padding:18px; }
    .rail h2 { margin:0 0 12px; font-size:20px; }
    .rail p,.rail a { font-size:14px; }
    .zz-engagement { grid-column:1 / -1; }
    @media (max-width: 860px) { .content-grid { grid-template-columns:1fr; } .rail { position:static; } }
"""


def engagement(lang: str, fb: bool = False) -> str:
    suffix = "facebook-en" if fb else ("zh" if lang == "zh" else "en")
    page_key = f"run50-{SLUG}-{suffix}"
    rel = "../../assets" if fb else "../../../assets"
    locale = "zh-CN" if lang == "zh" else "en"
    if lang == "zh":
        kicker, heading, note, views, loading = "留言 / 阅读", "跑完以后，说两句", "不用登录也可以留言。新留言会直接显示。", "阅读", "留言加载中..."
    else:
        kicker, heading, note, views, loading = "Comments / Views", "Say something after the run", "No account is needed to submit a comment. New comments appear right away.", "Views", "Loading comments..."
    return f"""<section class="zz-engagement" data-zz-engagement data-locale="{locale}" data-page-key="{page_key}">
    <div class="zz-engagement-shell">
      <div>
        <p class="zz-engagement-kicker">{kicker}</p>
        <h2>{heading}</h2>
        <p class="zz-engagement-note">{note}</p>
        <div class="zz-engagement-stats"><span class="zz-engagement-stat" id="busuanzi_container_page_pv"><span>{views}</span><strong id="busuanzi_value_page_pv" data-zz-view-count>--</strong></span></div>
      </div>
      <div class="zz-engagement-card"><div id="supabase-comments-{SLUG}-{suffix}" data-zz-supabase-comments></div><p class="zz-engagement-status" data-zz-engagement-status>{loading}</p></div>
    </div>
  </section>
  <script src="{rel}/zz-engagement-config.js?v={ENGAGEMENT_VERSION}"></script>
  <script src="{rel}/zz-engagement.js?v={ENGAGEMENT_VERSION}"></script>"""


def render_page(article: str, lang: str) -> str:
    is_zh = lang == "zh"
    title = TITLE_ZH if is_zh else TITLE_EN
    deck = DECK_ZH if is_zh else DECK_EN
    nav = (
        '<a href="./index.html">← 中文故事</a><a href="../english/kentucky-derby-marathon.html">English</a><a href="../../facebook/kentucky-derby-marathon.html">Facebook</a><a href="../../index.html">Run50</a>'
        if is_zh
        else '<a href="./index.html">← English Stories</a><a href="../chinese/kentucky-derby-marathon.html">中文</a><a href="../../facebook/kentucky-derby-marathon.html">Facebook</a><a href="../../index.html">Run50</a>'
    )
    meta = (
        f"<span>{LOCATION_ZH}</span><span>{DATE_ZH}</span><span>Run50 #第1州</span><span>{RACE_NAME}</span>"
        if is_zh
        else f"<span>{LOCATION_EN}</span><span>{DATE_EN}</span><span>Run50 #1</span><span>{RACE_NAME}</span>"
    )
    filename = "chinese" if is_zh else "english"
    lang_attr = "zh-CN" if is_zh else "en"
    return f"""<!doctype html>
<html lang="{lang_attr}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)}</title>
  <meta name="description" content="{escape(deck)}">
  <meta property="og:title" content="{escape(title)}">
  <meta property="og:description" content="{escape(deck)}">
  <meta property="og:image" content="{SITE}/assets/og-run50-kentucky-derby-marathon-icons.png?v={VERSION}">
  <meta property="og:url" content="{SITE}/run50/stories/{filename}/{SLUG}.html">
  <meta property="og:type" content="article">
  <link rel="stylesheet" href="../../../assets/zz-engagement.css?v={ENGAGEMENT_VERSION}">
  <style>{STORY_CSS}</style>
</head>
<body>
  <nav>{nav}</nav>
  <section class="hero"><div class="hero-inner">
    <p class="eyebrow">Run50 #01 · Kentucky</p>
    <h1>{escape(title)}</h1>
    <p class="deck">{escape(deck)}</p>
    <div class="meta-row">{meta}</div>
    <img class="cover" src="../../../assets/thumb-run50-kentucky-derby-marathon-icons.svg?v={VERSION}" alt="Kentucky Derby Marathon icon cover">
  </div></section>
  <main><article>
      {article}
    </article></main>
  {engagement(lang)}
</body>
</html>
"""


def render_facebook(article: str) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(TITLE_FB)}</title>
  <meta name="description" content="{escape(DECK_EN)}">
  <meta property="og:title" content="{escape(TITLE_FB)}">
  <meta property="og:description" content="{escape(DECK_EN)}">
  <meta property="og:image" content="{SITE}/assets/og-run50-kentucky-derby-marathon-icons.png?v={VERSION}">
  <meta property="og:url" content="{SITE}/run50/facebook/{SLUG}.html">
  <meta property="og:type" content="article">
  <link rel="stylesheet" href="../../assets/zz-engagement.css?v={ENGAGEMENT_VERSION}">
  <style>{FB_CSS}</style>
</head>
<body>
  <div class="topbar"><span>Run50 / USA</span><span>{LOCATION_EN} · {RACE_NAME}</span></div>
  <header class="masthead">
    <div class="brand">Run50 Dispatch</div>
    <h1>{escape(TITLE_FB)}</h1>
    <p class="summary">{escape(DECK_EN)}</p>
    <div class="meta-row"><span>Run50 #1</span><span>Kentucky</span><span>Hometown sub-four</span><span>Full story</span></div>
  </header>
  <main class="content-grid">
    <article>
      <p class="lede">The fourth time back on Louisville's Derby course finally changed the story: the familiar streets, race-season noise, friends on the route, and a finish clock under four hours.</p>
      {article}
    </article>
    <aside class="rail">
      <h2>Why this race matters</h2>
      <p>Louisville is both the starting point of my U.S. marathon map and the city that made running feel local.</p>
      <p>This edition turns the Derby Marathon into a hometown chapter: bluegrass, bourbon, horse racing, friends, and a long-awaited sub-four.</p>
      <a href="../stories/english/kentucky-derby-marathon.html">Read the archive edition</a>
    </aside>
    {engagement("en", fb=True)}
  </main>
</body>
</html>
"""


def write_covers() -> None:
    bg = "#edf3f7"
    ink = "#20242b"
    blue = "#0b67c2"
    muted = "#667085"
    img = Image.new("RGB", (1200, 630), bg)
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((42, 42, 1158, 588), radius=34, fill="#f7fbfd", outline="#c8d9e4", width=4)
    draw.text((64, 64), "LOUISVILLE", font=font(66, True), fill=ink)
    draw.text((66, 136), "DERBY MARATHON · HOMETOWN SUB-4", font=font(26, True), fill=muted)
    draw.rounded_rectangle((760, 64, 1122, 228), radius=22, fill="#ffffff", outline=ink, width=7)
    draw.text((790, 112), "Run50 #1", font=font(40, True), fill=ink)
    draw.text((790, 166), "KENTUCKY", font=fit_font(draw, "KENTUCKY", 302, 50, 32, True), fill=blue)
    draw.rectangle((92, 435, 1108, 488), fill="#30465a")
    for x in range(122, 1070, 112):
        draw.rounded_rectangle((x, 292, x + 56, 435), radius=12, fill="#d8e9f2", outline=ink, width=5)
        draw.polygon([(x - 12, 292), (x + 28, 250), (x + 68, 292)], fill="#ffffff", outline=ink)
    draw.ellipse((472, 326, 728, 582), fill="#f0c75e", outline=ink, width=8)
    draw.text((520, 418), "26.2", font=font(54, True), fill=ink)
    draw.arc((416, 235, 784, 610), 198, 342, fill=blue, width=10)
    draw.line((170, 520, 1030, 520), fill=blue, width=8)
    draw.line((180, 540, 1020, 540), fill="#d64b3c", width=8)
    (REPO / "assets").mkdir(exist_ok=True)
    img.save(REPO / "assets" / "og-run50-kentucky-derby-marathon-icons.png", "PNG")

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 750" width="1200" height="750">
  <rect width="1200" height="750" fill="{bg}"/>
  <rect x="44" y="44" width="1112" height="662" rx="34" fill="#f7fbfd" stroke="#c8d9e4" stroke-width="4"/>
  <text x="70" y="104" font-family="Arial, Helvetica, sans-serif" font-size="66" font-weight="900" fill="{ink}">LOUISVILLE</text>
  <text x="72" y="150" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="800" fill="{muted}">DERBY MARATHON · HOMETOWN SUB-4</text>
  <rect x="758" y="62" width="364" height="166" rx="22" fill="#ffffff" stroke="{ink}" stroke-width="8"/>
  <text x="790" y="122" font-family="Arial, Helvetica, sans-serif" font-size="41" font-weight="900" fill="{ink}">Run50 #1</text>
  <text x="790" y="182" font-family="Arial, Helvetica, sans-serif" font-size="52" font-weight="900" fill="{blue}">KENTUCKY</text>
  <rect x="92" y="520" width="1016" height="56" fill="#30465a"/>
  <g fill="#d8e9f2" stroke="{ink}" stroke-width="6">
    <rect x="130" y="358" width="58" height="162" rx="12"/><path d="M118 358 L159 312 L200 358 Z" fill="#fff"/>
    <rect x="270" y="338" width="58" height="182" rx="12"/><path d="M258 338 L299 292 L340 338 Z" fill="#fff"/>
    <rect x="410" y="370" width="58" height="150" rx="12"/><path d="M398 370 L439 324 L480 370 Z" fill="#fff"/>
    <rect x="690" y="370" width="58" height="150" rx="12"/><path d="M678 370 L719 324 L760 370 Z" fill="#fff"/>
    <rect x="830" y="338" width="58" height="182" rx="12"/><path d="M818 338 L859 292 L900 338 Z" fill="#fff"/>
    <rect x="970" y="358" width="58" height="162" rx="12"/><path d="M958 358 L999 312 L1040 358 Z" fill="#fff"/>
  </g>
  <circle cx="600" cy="518" r="128" fill="#f0c75e" stroke="{ink}" stroke-width="8"/>
  <text x="520" y="536" font-family="Arial, Helvetica, sans-serif" font-size="56" font-weight="900" fill="{ink}">26.2</text>
  <path d="M418 430 C500 318 700 318 782 430" fill="none" stroke="{blue}" stroke-width="10"/>
  <path d="M180 622 H1020" stroke="{blue}" stroke-width="9"/>
  <path d="M196 648 H1004" stroke="#d64b3c" stroke-width="9"/>
</svg>
'''
    (REPO / "assets" / "thumb-run50-kentucky-derby-marathon-icons.svg").write_text(svg, encoding="utf-8", newline="\n")


def update_indexes() -> None:
    replacements = [
        (
            REPO / "run50" / "stories" / "chinese" / "index.html",
            r'(<a class="story-card run-50" href="./kentucky-derby-marathon.html">.*?</a>)',
            f'''<a class="story-card run-50" href="./kentucky-derby-marathon.html">
          <img src="../../../assets/cover-medal-zh-kentucky-derby.jpg?v={VERSION}" alt="肯塔基德比马拉松奖牌封面" loading="lazy" decoding="async">
          <div class="story-card-body">
            <span class="story-tag">Run50 #1 · Kentucky</span>
            <h2 class="story-title">肯塔基：赛马节马拉松｜四刷主场，蓝草州终破4！</h2>
            <p class="story-desc">第四次跑 Louisville Derby Marathon，从赛马节和 Churchill Downs 到 Iroquois Park，终于在主场破四。</p>
            <p class="story-meta">路易斯维尔 · 肯塔基 · 2026.04.25</p>
          </div>
        </a>''',
        ),
        (
            REPO / "run50" / "stories" / "english" / "index.html",
            r'(<a class="story-card run-50" href="./kentucky-derby-marathon.html"[^>]*>.*?</a>)',
            f'''<a class="story-card run-50" href="./kentucky-derby-marathon.html" data-map-meta="Kentucky · Louisville · 2026.04.25">
          <img src="../../../assets/cover-medal-zh-kentucky-derby.jpg?v={VERSION}" alt="Kentucky Derby Marathon medal cover" loading="lazy" decoding="async">
          <div class="story-card-body">
            <span class="story-tag">Run50 #1 · Kentucky</span>
            <h2 class="story-title">Kentucky Derby Marathon: fourth time at home, finally under four</h2>
            <p class="story-desc">A hometown Louisville Derby Marathon with Derby-season color, Churchill Downs, Iroquois Park, running friends, and a long-awaited sub-four.</p>
            <p class="story-meta">Louisville · Kentucky · Apr 25, 2026</p>
          </div>
        </a>''',
        ),
        (
            REPO / "run50" / "facebook" / "index.html",
            r'(<a class="story-card run-50" href="./kentucky-derby-marathon.html">.*?</a>)',
            f'''<a class="story-card run-50" href="./kentucky-derby-marathon.html">
          <img src="../../assets/cover-medal-zh-kentucky-derby.jpg?v={VERSION}" alt="Kentucky Derby Marathon medal cover" loading="lazy" decoding="async">
          <div class="story-card-body">
            <span class="story-tag">Run50 #1 · Kentucky</span>
            <h2 class="story-title">Louisville turned my fourth Derby Marathon into a hometown sub-four</h2>
            <p class="story-desc">Derby season, familiar streets, friends all over the course, and one fourth try that finally broke four hours at home.</p>
            <p class="story-meta">Louisville · Kentucky · Run50</p>
          </div>
        </a>''',
        ),
    ]
    for path, pattern, repl in replacements:
        text = path.read_text(encoding="utf-8")
        new_text, count = re.subn(pattern, repl, text, count=1, flags=re.S)
        if count != 1:
            raise RuntimeError(f"Could not update index card in {path}")
        path.write_text(new_text, encoding="utf-8", newline="\n")


def main() -> None:
    events = extract_items()
    text_count = sum(1 for event in events if event["type"] == "text")
    image_refs = sum(1 for event in events if event["type"] == "image")
    print(f"extracted {text_count} text blocks, {image_refs} image refs")
    image_count = copy_images(events)
    print(f"copied {image_count} images")
    cache = ensure_translations(events)
    zh = render_events(events, "zh", f"{IMAGE_DIR}/", cache)
    en = render_events(events, "en", f"../chinese/{IMAGE_DIR}/", cache)
    fb = render_events(events, "en", f"../stories/chinese/{IMAGE_DIR}/", cache)
    (REPO / "run50" / "stories" / "chinese" / f"{SLUG}.html").write_text(render_page(zh, "zh"), encoding="utf-8", newline="\n")
    (REPO / "run50" / "stories" / "english" / f"{SLUG}.html").write_text(render_page(en, "en"), encoding="utf-8", newline="\n")
    (REPO / "run50" / "facebook" / f"{SLUG}.html").write_text(render_facebook(fb), encoding="utf-8", newline="\n")
    write_covers()
    update_indexes()


if __name__ == "__main__":
    main()
