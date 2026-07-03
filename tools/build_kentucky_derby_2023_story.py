from __future__ import annotations

from dataclasses import dataclass
from html import escape
from html.parser import HTMLParser
from pathlib import Path
import json
import re
import shutil
import tempfile
import time
import urllib.parse
import urllib.request

from PIL import Image, ImageDraw, ImageFont, ImageOps


REPO = Path(__file__).resolve().parents[1]
SOURCE_ROOT = Path("Z:/ZhennanZ Folder/0-Running Story Web/ADDDDD")
SLUG = "kentucky-derby-marathon-2023"
IMAGE_DIR = "Run50-Kentucky-Derby-Marathon-2023-clean_files"
SITE = "https://zhennanzhang.com"
VERSION = "20260703-ky23"
ENGAGEMENT_VERSION = "20260616"
TRANSLATION_CACHE = Path(tempfile.gettempdir()) / "zz_run50_kentucky_derby_2023_translation_cache.json"
FONT_DIR = Path("C:/Windows/Fonts")

TITLE_ZH = "Run50 #第1州番外｜肯塔基：德比马拉松｜赛马城最大的跑步 Party"
TITLE_EN = "Run50 #1 Revisit | Kentucky: Derby Marathon, Louisville's Biggest Running Party"
TITLE_FB = "Louisville Turned Derby Season Into the City's Biggest Running Party"
WECHAT_TITLE = "Run50 #第1州番外 肯塔基 德比马拉松 赛马城最大的跑步 Party"
DATE_ZH = "2023.04.29"
DATE_EN = "Apr 29, 2023"
LOCATION_ZH = "肯塔基路易斯维尔"
LOCATION_EN = "Louisville, Kentucky"
RACE_ZH = "Kentucky Derby Festival Marathon"
RACE_EN = "Kentucky Derby Festival Marathon"
DECK_ZH = "回到自己的城市，把肯塔基德比马拉松补成一篇：赛马季、Twin Spires、市中心、朋友们，还有路城最大的跑步 Party。"
DECK_EN = "Back in my own city for the Kentucky Derby Festival Marathon: Derby season, Twin Spires, downtown Louisville, running friends, and the city's biggest running party."
FB_DEK = "On April 29, 2023, Louisville's Derby season became a marathon morning: a hometown course, Churchill Downs energy, friends on the road, and one more Kentucky chapter worth saving."

ASSET_COVER = "cover-medal-kentucky-derby-marathon-2023.jpg"
ASSET_COVER_ZH = "cover-medal-zh-kentucky-derby-marathon-2023.jpg"
ASSET_COVER_FB = "cover-medal-fb-kentucky-derby-marathon-2023.jpg"
ASSET_MAP = "wechat-run50-map-kentucky-derby-2023.png"
ASSET_OG = f"og-run50-{SLUG}-icons.png"
ASSET_THUMB = f"thumb-run50-{SLUG}-icons.svg"


@dataclass
class Block:
    kind: str
    text: str = ""
    src: str = ""
    caption: str = ""
    alt: str = ""


class ExportParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.cur: list[str] | None = None
        self.events: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = {k: v or "" for k, v in attrs}
        if tag in {"p", "section", "h1", "h2", "h3", "span"} and self.cur is None:
            self.cur = [tag, ""]
        if tag == "img":
            src = attrs_dict.get("src") or attrs_dict.get("data-src") or attrs_dict.get("data-backsrc") or ""
            if "_files/640" in src:
                self.events.append({"type": "img", "src": src})

    def handle_endtag(self, tag: str) -> None:
        if self.cur and self.cur[0] == tag:
            text = re.sub(r"\s+", " ", self.cur[1]).strip()
            if text and len(text) < 1000 and text not in {"图片", "音频", "超链接"}:
                self.events.append({"type": "text", "text": text})
            self.cur = None

    def handle_data(self, data: str) -> None:
        if self.cur is not None:
            self.cur[1] += data


def font(name: str, size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for candidate in [FONT_DIR / name, FONT_DIR / "arial.ttf"]:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default()


def write_text_fit(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, max_width: int, start_size: int, fill: str, font_name: str = "arialbd.ttf") -> None:
    size = start_size
    while size > 18:
        fnt = font(font_name, size)
        if draw.textbbox((0, 0), text, font=fnt)[2] <= max_width:
            draw.text(xy, text, fill=fill, font=fnt)
            return
        size -= 2
    draw.text(xy, text, fill=fill, font=font(font_name, size))


def make_cover_assets() -> None:
    assets = REPO / "assets"
    assets.mkdir(exist_ok=True)

    for src_name, dst_name in [
        ("cover-medal-ky-derby.jpg", ASSET_COVER),
        ("cover-medal-zh-kentucky-derby.jpg", ASSET_COVER_ZH),
        ("cover-medal-zh-kentucky-derby.jpg", ASSET_COVER_FB),
        ("wechat-run50-map-kentucky-1-derby-2024.png", ASSET_MAP),
    ]:
        src = assets / src_name
        dst = assets / dst_name
        if src.exists():
            shutil.copy2(src, dst)

    im = Image.new("RGB", (1200, 630), "#edf3f7")
    draw = ImageDraw.Draw(im)
    draw.rounded_rectangle((38, 34, 1162, 596), radius=36, fill="#f7fbfd", outline="#20242b", width=5)
    draw.rectangle((72, 402, 1130, 536), fill="#146b4a")
    draw.rounded_rectangle((760, 64, 1122, 228), radius=22, fill="#ffffff", outline="#20242b", width=7)
    draw.text((790, 112), "Run50 #1", fill="#20242b", font=font("arialbd.ttf", 40))
    draw.text((790, 169), "KENTUCKY", fill="#0b67c2", font=font("arialbd.ttf", 44))
    draw.text((64, 72), "LOUISVILLE", fill="#20242b", font=font("arialbd.ttf", 66))
    draw.text((66, 144), "DERBY CITY · TWIN SPIRES · RUNNING PARTY", fill="#667085", font=font("arialbd.ttf", 25))
    draw.line((120, 450, 285, 395, 430, 465, 580, 418, 735, 492, 940, 430), fill="#d12c2c", width=16, joint="curve")
    draw.line((120, 450, 285, 395, 430, 465, 580, 418, 735, 492, 940, 430), fill="#ffd36e", width=6, joint="curve")
    draw.rectangle((850, 290, 902, 410), fill="#203044")
    draw.rectangle((940, 290, 992, 410), fill="#203044")
    draw.polygon([(840, 290), (875, 220), (912, 290)], fill="#caa15a")
    draw.polygon([(930, 290), (965, 220), (1002, 290)], fill="#caa15a")
    draw.ellipse((128, 308, 244, 424), fill="#f6d886", outline="#20242b", width=4)
    draw.text((148, 343), "2023", fill="#20242b", font=font("arialbd.ttf", 36))
    draw.rectangle((84, 536, 1116, 570), fill="#d6a14b")
    write_text_fit(draw, (210, 448), "KENTUCKY DERBY MARATHON", 620, 48, "#fff7df")
    im.save(assets / ASSET_OG, quality=95)

    (assets / ASSET_THUMB).write_text(
        f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 750">
  <rect width="1200" height="750" rx="34" fill="#edf3f7"/>
  <rect x="38" y="34" width="1124" height="682" rx="38" fill="#f7fbfd" stroke="#20242b" stroke-width="7"/>
  <text x="70" y="110" font-family="Arial, Helvetica, sans-serif" font-size="66" font-weight="900" fill="#20242b">LOUISVILLE</text>
  <text x="72" y="158" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="800" fill="#667085">DERBY CITY · TWIN SPIRES</text>
  <rect x="758" y="62" width="364" height="166" rx="22" fill="#ffffff" stroke="#20242b" stroke-width="8"/>
  <text x="790" y="122" font-family="Arial, Helvetica, sans-serif" font-size="41" font-weight="900" fill="#20242b">Run50 #1</text>
  <text x="790" y="182" font-family="Arial, Helvetica, sans-serif" font-size="46" font-weight="900" fill="#0b67c2">KENTUCKY</text>
  <path d="M105 510 C250 430 360 550 500 480 S745 575 980 470" fill="none" stroke="#d12c2c" stroke-width="20" stroke-linecap="round"/>
  <path d="M105 510 C250 430 360 550 500 480 S745 575 980 470" fill="none" stroke="#ffd36e" stroke-width="7" stroke-linecap="round"/>
  <rect x="855" y="320" width="52" height="125" fill="#203044"/>
  <rect x="945" y="320" width="52" height="125" fill="#203044"/>
  <polygon points="845,320 881,238 917,320" fill="#caa15a"/>
  <polygon points="935,320 971,238 1007,320" fill="#caa15a"/>
  <rect x="150" y="600" width="900" height="82" rx="18" fill="#146b4a" stroke="#20242b" stroke-width="5"/>
  <text x="600" y="655" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="52" font-weight="900" fill="#fff7df">KENTUCKY DERBY MARATHON</text>
</svg>
''',
        encoding="utf-8",
    )


def extract_events() -> list[dict[str, str]]:
    source = next(SOURCE_ROOT.glob("2023*.html"))
    parser = ExportParser()
    parser.feed(source.read_text(encoding="utf-8", errors="replace"))
    clean: list[dict[str, str]] = []
    for event in parser.events:
        key = (event["type"], event.get("text") or event.get("src"))
        last = clean[-1] if clean else None
        last_key = (last["type"], last.get("text") or last.get("src")) if last else None
        if key != last_key:
            clean.append(event)

    start = next(i for i, e in enumerate(clean) if e["type"] == "text" and "Louisville" in e["text"])
    end = len(clean)
    for i, event in enumerate(clean[start:], start):
        if event["type"] == "text" and "设计" in event["text"] and "Arsenan" in event["text"]:
            end = i + 1
            break
    return clean[start:end]


def source_image_path(src: str) -> Path:
    name = src.split("/")[-1]
    return SOURCE_ROOT / "2023 肯塔基_files" / name


def convert_images(events: list[dict[str, str]]) -> dict[str, str]:
    out_dir = REPO / "run50" / "stories" / "chinese" / IMAGE_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    mapping: dict[str, str] = {}
    count = 0
    for event in events:
        if event["type"] != "img":
            continue
        count += 1
        src = event["src"]
        dst_name = f"img-{count:03d}.webp"
        dst = out_dir / dst_name
        with Image.open(source_image_path(src)) as im:
            im = ImageOps.exif_transpose(im)
            if im.mode not in {"RGB", "L"}:
                im = im.convert("RGB")
            elif im.mode == "L":
                im = im.convert("RGB")
            im.save(dst, "WEBP", quality=88, method=6)
        mapping[src] = dst_name
    return mapping


def split_captions(text: str) -> list[str]:
    caps = [part.strip() for part in re.findall(r"▲\s*[^▲]+", text)]
    if not caps and text.strip().startswith("▲"):
        caps = [text.strip()]
    return [re.sub(r"^▲\s*", "", c).strip() for c in caps if c.strip()]


def make_blocks(events: list[dict[str, str]], image_map: dict[str, str]) -> list[Block]:
    blocks: list[Block] = []
    pending_images: list[int] = []
    for event in events:
        if event["type"] == "img":
            idx = len([b for b in blocks if b.kind == "image"]) + 1
            blocks.append(Block(kind="image", src=image_map[event["src"]], alt=f"Kentucky Derby Marathon photo {idx}"))
            pending_images.append(len(blocks) - 1)
            continue

        text = event["text"].strip()
        if not text or text in {"★", "★★"}:
            continue
        if text.startswith("▲"):
            caps = split_captions(text)
            if pending_images and caps:
                targets = pending_images[-len(caps) :] if len(caps) <= len(pending_images) else pending_images
                for target, cap in zip(targets, caps[-len(targets) :]):
                    blocks[target].caption = cap
                    blocks[target].alt = re.sub(r"@\w+.*$", "", cap).strip() or blocks[target].alt
                pending_images = [i for i in pending_images if not blocks[i].caption]
            elif caps:
                blocks.append(Block(kind="caption", text=" / ".join(caps)))
            continue
        blocks.append(Block(kind="text", text=text))
    return blocks


def load_cache() -> dict[str, str]:
    if TRANSLATION_CACHE.exists():
        return json.loads(TRANSLATION_CACHE.read_text(encoding="utf-8"))
    return {}


def save_cache(cache: dict[str, str]) -> None:
    TRANSLATION_CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")


def google_translate(text: str, cache: dict[str, str]) -> str:
    if not text or not re.search(r"[\u4e00-\u9fff]", text):
        return text
    if text in cache:
        return cache[text]
    query = urllib.parse.urlencode({"client": "gtx", "sl": "zh-CN", "tl": "en", "dt": "t", "q": text})
    url = "https://translate.googleapis.com/translate_a/single?" + query
    for attempt in range(3):
        try:
            with urllib.request.urlopen(url, timeout=12) as response:
                data = json.loads(response.read().decode("utf-8"))
            out = "".join(part[0] for part in data[0] if part and part[0])
            out = polish_english(out)
            cache[text] = out
            save_cache(cache)
            time.sleep(0.04)
            return out
        except Exception:
            if attempt == 2:
                return text
            time.sleep(0.4)
    return text


def translate_caption(caption: str, cache: dict[str, str]) -> str:
    credit = ""
    match = re.search(r"\s(@[A-Za-z][A-Za-z0-9 _.-]*)$", caption)
    if match:
        credit = match.group(1).strip()
        caption = caption[: match.start()].strip()
    translated = google_translate(caption, cache) if caption else ""
    if credit:
        translated = f"{translated} {credit}".strip()
    return polish_english(translated)


def polish_english(text: str) -> str:
    replacements = {
        "Louisville": "Louisville",
        "Derby Marathon": "Derby Marathon",
        "Kentucky Derby Marathon": "Kentucky Derby Marathon",
        "half horse": "half marathon",
        "full horse": "full marathon",
        "whole horse": "marathon",
        "horse race": "marathon",
        "Road City": "Louisville",
        "Route City": "Louisville",
        "Runyou": "running friends",
        "running friend": "running friend",
        "Siqi": "Siqi",
        "Twin Spires": "Twin Spires",
        "Churchill Downs": "Churchill Downs",
        "Big Four Bridge": "Big Four Bridge",
        "Ohio River": "Ohio River",
        "KFC Yum! Center": "KFC Yum! Center",
        "MaraFoto": "MaraFoto",
        "Arsenan": "Arsenan",
    }
    out = text
    for bad, good in replacements.items():
        out = out.replace(bad, good)
    out = out.replace(" ,", ",").replace(" .", ".").replace(" !", "!").replace(" ?", "?")
    out = re.sub(r"\s+", " ", out).strip()
    return out


def translated_blocks(blocks: list[Block]) -> list[Block]:
    cache = load_cache()
    result: list[Block] = []
    for block in blocks:
        if block.kind == "text":
            result.append(Block(kind="text", text=google_translate(block.text, cache)))
        elif block.kind == "caption":
            result.append(Block(kind="caption", text=translate_caption(block.text, cache)))
        elif block.kind == "image":
            result.append(
                Block(
                    kind="image",
                    src=block.src,
                    caption=translate_caption(block.caption, cache) if block.caption else "",
                    alt=translate_caption(block.alt, cache) if block.alt else "Kentucky Derby Marathon photo",
                )
            )
    save_cache(cache)
    return result


def nav_html(kind: str) -> str:
    if kind == "zh":
        links = [
            ("← Run50", "../../index.html"),
            ("Chinese Stories", "./index.html"),
            ("English Stories", f"../english/{SLUG}.html"),
            ("Wechat", f"../../wechat/{SLUG}-modern-rail.html"),
            ("Facebook", f"../../facebook/{SLUG}.html"),
        ]
    elif kind == "en":
        links = [
            ("← Run50", "../../index.html"),
            ("English Stories", "./index.html"),
            ("Chinese Stories", f"../chinese/{SLUG}.html"),
            ("Wechat", f"../../wechat/{SLUG}-modern-rail.html"),
            ("Facebook", f"../../facebook/{SLUG}.html"),
        ]
    else:
        links = [
            ("← Run50", "../index.html"),
            ("Facebook", "./index.html"),
            ("Chinese Stories", f"../stories/chinese/{SLUG}.html"),
            ("English Stories", f"../stories/english/{SLUG}.html"),
            ("Wechat", f"../wechat/{SLUG}-modern-rail.html"),
        ]
    return '<nav class="topnav">' + "".join(f'<a href="{href}">{label}</a>' for label, href in links) + "</nav>"


def engagement(locale: str, page_key: str, asset_prefix: str) -> str:
    is_zh = locale == "zh-CN"
    kicker = "留言 / 阅读" if is_zh else "Comments / Views"
    title = "跑完也可以聊两句" if is_zh else "Say something after the run"
    note = "不用登录，新的留言会直接显示在页面里。" if is_zh else "No account is needed to submit a comment. New comments appear right away."
    views = "阅读" if is_zh else "Views"
    loading = "留言区加载中..." if is_zh else "Loading comments..."
    ident = f"supabase-comments-{page_key.replace('run50-', '').replace('-facebook-en','-fb')}"
    return f'''
<section class="zz-engagement" data-zz-engagement data-locale="{locale}" data-page-key="{page_key}">
  <div class="zz-engagement-shell">
    <div>
      <p class="zz-engagement-kicker">{kicker}</p>
      <h2>{title}</h2>
      <p class="zz-engagement-note">{note}</p>
      <div class="zz-engagement-stats"><span class="zz-engagement-stat" id="busuanzi_container_page_pv"><span>{views}</span><strong id="busuanzi_value_page_pv" data-zz-view-count>--</strong></span></div>
    </div>
    <div class="zz-engagement-card"><div id="{ident}" data-zz-supabase-comments></div><p class="zz-engagement-status" data-zz-engagement-status>{loading}</p></div>
  </div>
</section>
<script src="{asset_prefix}/zz-engagement-config.js?v={ENGAGEMENT_VERSION}"></script>
<script src="{asset_prefix}/zz-engagement.js?v={ENGAGEMENT_VERSION}"></script>'''


def story_css() -> str:
    return """
:root{--bg:#edf3f7;--paper:#fff;--ink:#17212b;--muted:#5d6b78;--blue:#236b9c;--line:#d7e4ec;--gold:#b88935}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",Arial,sans-serif}
.topnav{max-width:1080px;margin:0 auto;padding:20px 22px;display:flex;gap:18px;justify-content:space-between;flex-wrap:wrap;font-weight:800}.topnav a{color:#435569;text-decoration:none}
.hero{max-width:980px;margin:28px auto 0;padding:42px 28px 28px;border-top:5px solid var(--blue);background:rgba(255,255,255,.68)}
.kicker{margin:0 0 12px;color:var(--blue);font-size:13px;letter-spacing:2.5px;font-weight:900}.hero h1{margin:0;font-size:clamp(34px,6vw,62px);line-height:1.08;letter-spacing:0}.dek{max-width:760px;margin:16px 0 0;color:var(--muted);font-size:18px;line-height:1.8}.meta{margin:20px 0 0;color:#8a6a2f;font-weight:800}
.cover{display:block;width:100%;max-width:980px;margin:28px auto 0;border-radius:8px}
.article{max-width:860px;margin:0 auto;padding:34px 24px 70px;background:#fff}.article p{font-size:18px;line-height:1.95;margin:0 0 20px;text-align:justify}.article h2{margin:52px 0 18px;padding-left:14px;border-left:5px solid var(--blue);font-size:28px;line-height:1.35}.article .intro-line{color:var(--blue);font-weight:900;letter-spacing:1.5px;text-align:center}.article .end-mark{text-align:center;color:#8a6a2f;font-weight:900}.article .credit{font-size:15px;color:var(--muted);text-align:center}
figure{margin:32px 0}figure img{display:block;width:100%;height:auto;border-radius:8px}figcaption{margin-top:9px;padding-left:12px;border-left:3px solid var(--gold);color:#687684;font-size:14px;line-height:1.7}
@media(max-width:640px){.article{padding:26px 17px 56px}.article p{font-size:16px}.hero{margin-top:0}.topnav{justify-content:flex-start}.hero h1{font-size:34px}}
"""


def render_body_blocks(blocks: list[Block], image_prefix: str, lang: str) -> str:
    out: list[str] = []
    for block in blocks:
        if block.kind == "image":
            cap = escape(block.caption) if block.caption else ""
            out.append(f'<figure><img src="{image_prefix}{block.src}" alt="{escape(block.alt)}" loading="lazy" decoding="async">{f"<figcaption>{cap}</figcaption>" if cap else ""}</figure>')
            continue
        text = block.text.strip()
        if not text:
            continue
        if lang == "en":
            if text.startswith("丨") and text.endswith("丨"):
                text = text.strip("丨")
            text = text.replace("丨", " | ")
        if text in {"前言", "后记", "Preface", "Postscript"} or text.startswith("# "):
            heading = text[2:].strip() if text.startswith("# ") else text
            out.append(f"<h2>{escape(heading)}</h2>")
        elif text.startswith("丨") or text.startswith("- Derby") or text == "赛马城最大的跑步Party":
            out.append(f'<p class="intro-line">{escape(text)}</p>')
        elif "本文完" in text or "End" in text:
            out.append(f'<p class="end-mark">{escape(text)}</p>')
        elif re.match(r"^(文字|摄影|设计|Text|Photos|Design)", text):
            out.append(f'<p class="credit">{escape(text)}</p>')
        else:
            out.append(f"<p>{escape(text)}</p>")
    return "\n".join(out)


def write_story_page(blocks: list[Block], lang: str) -> None:
    is_zh = lang == "zh"
    out_path = REPO / "run50" / "stories" / ("chinese" if is_zh else "english") / f"{SLUG}.html"
    title = TITLE_ZH if is_zh else TITLE_EN
    deck = DECK_ZH if is_zh else DECK_EN
    meta = f"{LOCATION_ZH} · {DATE_ZH} · {RACE_ZH}" if is_zh else f"{LOCATION_EN} · {DATE_EN} · {RACE_EN}"
    image_prefix = "" if is_zh else f"../chinese/{IMAGE_DIR}/"
    if is_zh:
        image_prefix = f"{IMAGE_DIR}/"
    page_key = f"run50-{SLUG}-{'zh' if is_zh else 'en'}"
    locale = "zh-CN" if is_zh else "en"
    html = f'''<!doctype html>
<html lang="{'zh-CN' if is_zh else 'en'}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)}</title>
  <meta name="description" content="{escape(deck)}">
  <meta property="og:title" content="{escape(title)}">
  <meta property="og:description" content="{escape(deck)}">
  <meta property="og:image" content="{SITE}/assets/{ASSET_OG}?v={VERSION}">
  <link rel="stylesheet" href="../../../assets/zz-engagement.css?v={ENGAGEMENT_VERSION}">
  <style>{story_css()}</style>
</head>
<body>
  {nav_html('zh' if is_zh else 'en')}
  <header class="hero">
    <p class="kicker">RUN50 DISPATCH · KENTUCKY</p>
    <h1>{escape(title)}</h1>
    <p class="dek">{escape(deck)}</p>
    <p class="meta">{escape(meta)}</p>
  </header>
  <img class="cover" src="../../../assets/{ASSET_COVER_ZH if is_zh else ASSET_COVER}?v={VERSION}" alt="{escape(title)} cover">
  <main class="article">
{render_body_blocks(blocks, image_prefix, lang)}
  </main>
  {engagement(locale, page_key, '../../../assets')}
</body>
</html>
'''
    out_path.write_text(html, encoding="utf-8")


def fb_css() -> str:
    return """
:root{--bg:#f2f5f8;--ink:#111827;--muted:#586575;--blue:#0b67c2;--line:#d9e2ea}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:Arial,"Helvetica Neue",sans-serif}.topnav{max-width:1180px;margin:0 auto;padding:18px 20px;display:flex;gap:18px;justify-content:space-between;flex-wrap:wrap;font-weight:800}.topnav a{color:#34465b;text-decoration:none}
.mast{background:#0f172a;color:#fff}.mast-inner{max-width:1180px;margin:0 auto;padding:28px 20px}.mast p{margin:0;color:#9dc3eb;font-weight:900;letter-spacing:2px}.mast h1{max-width:980px;margin:12px 0 0;font-size:clamp(36px,6vw,68px);line-height:1.02}.dek{max-width:820px;margin:18px 0 0;color:#dbeafe;font-size:19px;line-height:1.7}
.layout{max-width:1180px;margin:28px auto;padding:0 20px 70px;display:grid;grid-template-columns:minmax(0,1fr) 300px;gap:28px}.article{background:#fff;padding:28px;border:1px solid var(--line)}.article p{font-size:18px;line-height:1.85;margin:0 0 20px}.article h2{margin:46px 0 18px;font-size:28px;line-height:1.25;border-top:4px solid var(--blue);padding-top:14px}.article figure{margin:30px 0}.article img{display:block;width:100%;height:auto}.article figcaption{margin-top:8px;color:#64748b;font-size:14px;line-height:1.6}
.side{position:sticky;top:20px;align-self:start;background:#fff;border:1px solid var(--line);padding:20px}.side img{width:100%;height:auto;display:block}.side h2{font-size:20px}.side p{color:var(--muted);line-height:1.65}.end-mark{text-align:center;font-weight:900;color:#0b67c2}.credit{font-size:14px;color:#64748b}
@media(max-width:860px){.layout{display:block}.side{position:static;margin-top:24px}.article{padding:20px}.article p{font-size:16px}}
"""


def write_facebook_page(blocks_en: list[Block]) -> None:
    out_path = REPO / "run50" / "facebook" / f"{SLUG}.html"
    html = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(TITLE_FB)}</title>
  <meta name="description" content="{escape(FB_DEK)}">
  <meta property="og:image" content="{SITE}/assets/{ASSET_OG}?v={VERSION}">
  <link rel="stylesheet" href="../../assets/zz-engagement.css?v={ENGAGEMENT_VERSION}">
  <style>{fb_css()}</style>
</head>
<body>
  {nav_html('fb')}
  <header class="mast"><div class="mast-inner">
    <p>RUN50 · KENTUCKY · APRIL 29, 2023</p>
    <h1>{escape(TITLE_FB)}</h1>
    <div class="dek">{escape(FB_DEK)}</div>
  </div></header>
  <main class="layout">
    <article class="article">
{render_body_blocks(blocks_en, f"../stories/chinese/{IMAGE_DIR}/", "en")}
    </article>
    <aside class="side">
      <img src="../../assets/{ASSET_COVER_FB}?v={VERSION}" alt="Kentucky Derby Marathon cover">
      <h2>Race File</h2>
      <p><strong>Race:</strong> {RACE_EN}<br><strong>City:</strong> {LOCATION_EN}<br><strong>Date:</strong> {DATE_EN}<br><strong>Run50:</strong> Kentucky revisit</p>
      <p>{escape(DECK_EN)}</p>
    </aside>
  </main>
  {engagement('en', f'run50-{SLUG}-facebook-en', '../../assets')}
</body>
</html>
'''
    out_path.write_text(html, encoding="utf-8")


def wx_p(text: str) -> str:
    text = escape(text)
    highlights = [
        "Louisville", "Kentucky", "Derby", "Churchill Downs", "Twin Spires", "Big Four Bridge",
        "肯塔基", "路易斯维尔", "德比", "赛马", "Churchill", "Siqi", "MaraFoto", "Arsenan",
    ]
    for item in highlights:
        text = text.replace(escape(item), f'<strong style="color:#9b6d24;font-weight:800;">{escape(item)}</strong>')
    text = re.sub(r"(26\.2|13\.1|47|4小时\d+分|四年|三次)", r'<span style="border-bottom:2px solid #d4a669;color:#162636;font-weight:800;">\1</span>', text)
    return f'<p style="margin:0 0 18px;line-height:1.95;text-align:justify;font-size:16px;letter-spacing:.2px;color:#26343f;">{text}</p>'


def wx_figure(block: Block) -> str:
    cap = escape(block.caption) if block.caption else ""
    cap_html = ""
    if cap:
        cap_html = f'<p style="margin:9px 0 0;padding-left:10px;border-left:3px solid #d4a669;font-size:12px;line-height:1.8;letter-spacing:.4px;color:#6f7d89;font-family:Optima-Regular,\'PingFang SC\',serif;">{cap}</p>'
    return f'''<section style="margin:28px 0 30px;">
  <img src="../stories/chinese/{IMAGE_DIR}/{block.src}" alt="{escape(block.alt)}" style="width:100%;height:auto;display:block;margin:0 auto;border-radius:6px;">
  {cap_html}
</section>'''


def wx_heading(no: int, title: str, sub: str) -> str:
    return f'''<section style="margin:44px 0 18px;padding:0 0 0 14px;border-left:5px solid #236b9c;">
  <p style="margin:0 0 5px;font-size:11px;line-height:1.4;letter-spacing:1.6px;color:#8a9bad;font-weight:800;">FIELD NOTE {no:02d}</p>
  <h2 style="margin:0;font-size:20px;line-height:1.45;font-weight:900;color:#162636;letter-spacing:0;">{escape(title)}</h2>
  <p style="margin:7px 0 0;font-size:12px;line-height:1.6;color:#9b6d24;">{escape(sub)}</p>
</section>'''


def write_wechat_page(blocks: list[Block]) -> None:
    out_path = REPO / "run50" / "wechat" / f"{SLUG}-modern-rail.html"
    body: list[str] = []
    note_no = 0
    skip_intro = {"丨Louisville丨", "- Derby Marathon -", "赛马城最大的跑步Party"}
    for block in blocks:
        if block.kind == "image":
            body.append(wx_figure(block))
            continue
        text = block.text.strip()
        if not text or text in skip_intro or text in {"- 本文完 -"}:
            continue
        if text in {"前言", "后记"} or text.startswith("# "):
            note_no += 1
            body.append(wx_heading(note_no, text[2:].strip() if text.startswith("# ") else text, "Kentucky · Louisville"))
        elif re.match(r"^(文字|摄影|设计)", text):
            body.append(f'<p style="margin:0 0 6px;text-align:center;font-size:13px;color:#7a8793;">{escape(text)}</p>')
        else:
            body.append(wx_p(text))

    html = f'''<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(WECHAT_TITLE)}</title>
</head>
<body style="margin:0;padding:0;background:#ffffff;font-family:-apple-system,BlinkMacSystemFont,'Helvetica Neue','PingFang SC','Microsoft YaHei',Arial,sans-serif;">
<section style="max-width:677px;width:100%;box-sizing:border-box;margin:0 auto;padding:28px 18px 58px;background:#ffffff;">
<section style="margin:0 0 22px;padding:16px 0 18px;border-top:4px solid #236b9c;border-bottom:1px solid #dfe9ef;">
  <p style="margin:0 0 8px;font-size:12px;line-height:1.4;letter-spacing:2px;color:#236b9c;font-weight:800;">RUN50 DISPATCH · KENTUCKY</p>
  <p style="margin:0;font-size:20px;line-height:1.55;font-weight:900;color:#17212b;letter-spacing:0;">第1州番外 · 肯塔基 · Derby Marathon</p>
  <p style="margin:14px 0 0;font-size:13px;line-height:1.7;color:#6f7d89;">Louisville · Churchill Downs · Kentucky Derby Festival Marathon</p>
</section>
<section style="margin:24px 0 30px;">
  <section style="position:relative;width:100%;padding-top:56.25%;border-radius:8px;overflow:hidden;background:#12384a;border:1px solid #d5e4eb;box-shadow:0 16px 36px rgba(20,52,68,.16);">
    <section style="position:absolute;inset:0;padding:24px 26px;box-sizing:border-box;background:linear-gradient(135deg,#102a38 0%,#236b4b 52%,#18324f 100%);color:#ffffff;">
      <p style="margin:0 0 10px;font-size:12px;line-height:1.3;letter-spacing:2.2px;font-weight:900;color:#ffdd75;">RUN50 VLOG · KENTUCKY</p>
      <p style="margin:0;max-width:430px;font-size:28px;line-height:1.25;font-weight:900;letter-spacing:0;">先看一段德比城</p>
      <p style="margin:10px 0 0;max-width:460px;font-size:15px;line-height:1.75;color:rgba(255,255,255,.86);">赛马季的 Louisville，Twin Spires、市中心、桥和朋友们，都在这场跑步 Party 里。</p>
      <section style="position:absolute;left:26px;bottom:22px;display:inline-block;padding:7px 12px;border-radius:999px;background:rgba(255,255,255,.14);color:rgba(255,255,255,.9);font-size:12px;line-height:1.4;letter-spacing:.5px;">Louisville · 16:9 Vlog</section>
      <section style="position:absolute;right:30px;bottom:26px;width:64px;height:64px;border-radius:50%;background:#ffcc00;box-shadow:0 10px 24px rgba(0,0,0,.22);"><span style="position:absolute;left:25px;top:19px;display:block;width:0;height:0;border-top:13px solid transparent;border-bottom:13px solid transparent;border-left:20px solid #153242;"></span></section>
    </section>
  </section>
  <p style="margin:9px 0 0;padding-left:10px;border-left:3px solid #d4a669;font-size:12px;line-height:1.8;letter-spacing:.4px;color:#6f7d89;font-family:Optima-Regular,'PingFang SC',serif;">Vlog 开场位｜Kentucky Derby Marathon</p>
</section>
<section style="margin:0 0 28px;padding:16px 18px;background:#edf5f8;border-radius:6px;"><p style="margin:0 0 6px;font-size:12px;line-height:1.5;letter-spacing:1px;color:#236b9c;font-weight:800;">OPENING NOTE</p><p style="margin:0;font-size:15px;line-height:1.9;color:#26343f;text-align:justify;">在<strong style="color:#9b6d24;font-weight:800;">路易斯维尔</strong>住了快四年，肯塔基的<strong style="color:#9b6d24;font-weight:800;">德比马拉松</strong>也跑过三次。2023 这一场，像是把主场、赛马季、朋友和城市记忆一起跑了一遍。</p></section>
<section style="margin:0 0 28px;display:block;"><p style="margin:0 0 8px;font-size:14px;line-height:1.8;color:#8a6a2f;font-weight:800;">本文速记</p><p style="margin:0;font-size:14px;line-height:1.9;color:#53616f;">一场属于 Derby City 的跑步 Party：<strong style="color:#9b6d24;font-weight:800;">Churchill Downs</strong>、<strong style="color:#236b9c;font-weight:800;">Big Four Bridge</strong>、市中心、MaraFoto 路照，以及一群熟悉的路城朋友。</p></section>
<section style="margin:24px 0 28px;"><img src="../../assets/{ASSET_COVER_ZH}?v={VERSION}" alt="肯塔基德比马拉松奖牌质感封面" style="width:100%;height:auto;display:block;margin:0 auto;border-radius:7px;"><p style="margin:9px 0 0;padding-left:10px;border-left:3px solid #d4a669;font-size:12px;line-height:1.8;letter-spacing:.4px;color:#6f7d89;font-family:Optima-Regular,'PingFang SC',serif;">Run50 · 肯塔基德比马拉松奖牌质感封面。</p></section>
<section style="margin:24px 0 28px;"><img src="../../assets/{ASSET_MAP}?v={VERSION}" alt="Run50 肯塔基位置地图" style="width:100%;height:auto;display:block;margin:0 auto;border-radius:7px;"><p style="margin:9px 0 0;padding-left:10px;border-left:3px solid #d4a669;font-size:12px;line-height:1.8;letter-spacing:.4px;color:#6f7d89;font-family:Optima-Regular,'PingFang SC',serif;">第1州 · Kentucky · Louisville</p></section>
{''.join(body)}
<section style="margin:42px 0 0;padding:22px 20px;border-radius:8px;background:#102a38;color:#ffffff;">
  <p style="margin:0 0 8px;font-size:12px;letter-spacing:1.6px;color:#ffdd75;font-weight:900;">RUN50 FINISH LINE</p>
  <p style="margin:0;font-size:16px;line-height:1.9;">这一篇像是给 Louisville 补的一张老照片：不是最快，也不是最新，但很主场。后来再看，才发现很多跑步记忆不是发生在远方，而是藏在自己住过的城市里。</p>
  <p style="margin:14px 0 0;font-size:13px;line-height:1.8;color:rgba(255,255,255,.75);">欢迎在公众号留言区聊聊你的主场比赛。</p>
</section>
</section>
</body>
</html>'''
    out_path.write_text(html, encoding="utf-8")


def card_blocks() -> tuple[str, str, str, str]:
    zh = f'''        <a class="story-card run-50" href="./{SLUG}.html">
          <img src="../../../assets/{ASSET_COVER_ZH}?v={VERSION}" alt="肯塔基德比马拉松奖牌封面" loading="lazy" decoding="async">
          <div class="story-copy">
            <p class="story-meta">肯塔基路易斯维尔 · {DATE_ZH}</p>
            <h2 class="story-title">Run50 #第1州番外｜肯塔基德比马拉松</h2>
            <p class="story-desc">{DECK_ZH}</p>
            <div class="story-foot"><span>长文图记</span><span>阅读 →</span></div>
          </div>
        </a>
'''
    en = f'''        <a class="story-card run-50" href="./{SLUG}.html" data-map-meta="Kentucky · Louisville · 2023.04.29">
          <img src="../../../assets/{ASSET_COVER}?v={VERSION}" alt="Kentucky Derby Marathon medal cover" loading="lazy" decoding="async">
          <div class="story-copy">
            <p class="story-meta">Louisville, KY · Run50 #1 revisit</p>
            <h2 class="story-title">Kentucky Derby Marathon: Louisville's biggest running party</h2>
            <p class="story-desc">Race date: April 29, 2023. A hometown Derby-season marathon in Louisville, with horse-racing energy, city streets, friends, and one more Kentucky chapter.</p>
            <div class="story-foot"><span>Derby season</span><span>Read →</span></div>
          </div>
        </a>
'''
    fb = f'''        <a class="story-card run-50" href="./{SLUG}.html">
          <img src="../../assets/{ASSET_COVER_FB}?v={VERSION}" alt="Kentucky Derby Marathon medal cover" loading="lazy" decoding="async">
          <div class="story-copy">
            <p class="story-meta">Louisville, KY · Run50</p>
            <h2 class="story-title">Louisville turned Derby season into the city's biggest running party</h2>
            <p class="story-desc">Race date: April 29, 2023. A hometown Derby-season marathon with Churchill Downs energy, city streets, and running friends.</p>
            <div class="story-foot"><span>Derby season</span><span>Read →</span></div>
          </div>
        </a>
'''
    wx = f'''      <a class="card" href="{SLUG}-modern-rail.html?v={VERSION}">
        <img class="cover" src="../../assets/{ASSET_COVER_ZH}?v={VERSION}" alt="肯塔基德比马拉松奖牌封面">
        <div class="body">
          <p class="meta">RUN50 DISPATCH · KENTUCKY</p>
          <h2>{WECHAT_TITLE}</h2>
          <p class="place">肯塔基路易斯维尔 · {DATE_ZH}</p>
          <p class="summary">{DECK_ZH}</p>
          <span class="button">Open WeChat Edition →</span>
        </div>
      </a>
'''
    return zh, en, fb, wx


def remove_existing_card(text: str, href: str, card_class: str = "story-card") -> str:
    return re.sub(rf"\n\s*<a class=\"{card_class}[^\"]*\" href=\"\.\/{re.escape(href)}\".*?</a>\s*", "\n", text, flags=re.S)


def insert_before(text: str, anchor_href: str, block: str, card_class: str = "story-card") -> str:
    pattern = re.compile(rf"(\s*<a class=\"{card_class}[^\"]*\" href=\"\.\/{re.escape(anchor_href)}\".*?</a>)", re.S)
    match = pattern.search(text)
    if not match:
        raise RuntimeError(f"anchor not found: {anchor_href}")
    return text[: match.start()] + "\n" + block + text[match.start() :]


def update_story_indexes() -> None:
    zh_card, en_card, fb_card, wx_card = card_blocks()
    targets = [
        (REPO / "run50/stories/chinese/index.html", f"{SLUG}.html", "kentucky-derby-marathon.html", zh_card, "story-card"),
        (REPO / "run50/stories/english/index.html", f"{SLUG}.html", "kentucky-derby-marathon.html", en_card, "story-card"),
        (REPO / "run50/facebook/index.html", f"{SLUG}.html", "kentucky-derby-marathon.html", fb_card, "story-card"),
    ]
    for path, href, anchor, card, cls in targets:
        text = path.read_text(encoding="utf-8")
        text = remove_existing_card(text, href, cls)
        text = insert_before(text, anchor, card, cls)
        path.write_text(text, encoding="utf-8")

    wx_path = REPO / "run50/wechat/index.html"
    text = wx_path.read_text(encoding="utf-8")
    text = re.sub(rf"\n\s*<a class=\"card\" href=\"{re.escape(SLUG)}-modern-rail\.html[^\"]*\".*?</a>\s*", "\n", text, flags=re.S)
    anchor = re.compile(r'(\s*<a class="card" href="kentucky-derby-marathon-modern-rail\.html[^"]*".*?</a>)', re.S)
    match = anchor.search(text)
    if not match:
        raise RuntimeError("wechat anchor not found")
    text = text[: match.start()] + "\n" + wx_card + text[match.start() :]
    wx_path.write_text(text, encoding="utf-8")


def update_run50_data() -> None:
    hub = REPO / "run50/hub.html"
    text = hub.read_text(encoding="utf-8")
    new = "{city:'Louisville',date:'Apr 29, 2023',story:'stories/english/kentucky-derby-marathon-2023.html',fb:'facebook/kentucky-derby-marathon-2023.html'},"
    if "kentucky-derby-marathon-2023.html" not in text:
        text = text.replace(
            "'KY':[{city:'Louisville',date:'Nov 8, 2020',story:'stories/english/louisville-marathon.html',fb:'facebook/louisville-marathon.html'},",
            "'KY':[{city:'Louisville',date:'Nov 8, 2020',story:'stories/english/louisville-marathon.html',fb:'facebook/louisville-marathon.html'}," + new,
        )
        text = text.replace(
            "[476, 264, '#ff4040', false, 'Louisville Derby, KY', 'Apr 2024', 'stories/english/kentucky-derby-marathon.html'],",
            "[476, 264, '#ff4040', false, 'Louisville Derby, KY', 'Apr 2023', 'stories/english/kentucky-derby-marathon-2023.html'],\n   [476, 264, '#ff4040', false, 'Louisville Derby, KY', 'Apr 2024', 'stories/english/kentucky-derby-marathon.html'],",
        )
    hub.write_text(text, encoding="utf-8")

    idx = REPO / "run50/index.html"
    text = idx.read_text(encoding="utf-8")
    if "kentucky-derby-marathon-2023.html" not in text:
        text = text.replace(
            "['Louisville Marathon', '2020.11.08', './stories/english/louisville-marathon.html'],\n      ['Kentucky Derby Marathon', '2024.04.27', './stories/english/kentucky-derby-marathon.html'],",
            "['Louisville Marathon', '2020.11.08', './stories/english/louisville-marathon.html'],\n      ['Kentucky Derby Marathon', '2023.04.29', './stories/english/kentucky-derby-marathon-2023.html'],\n      ['Kentucky Derby Marathon', '2024.04.27', './stories/english/kentucky-derby-marathon.html'],",
        )
    idx.write_text(text, encoding="utf-8")


def update_comments_sql() -> None:
    path = REPO / "supabase/run50-comments.sql"
    text = path.read_text(encoding="utf-8")
    keys = [
        "run50-kentucky-derby-marathon-2023-en",
        "run50-kentucky-derby-marathon-2023-facebook-en",
        "run50-kentucky-derby-marathon-2023-zh",
    ]
    if all(text.count(key) == 3 for key in keys):
        return
    insert = "\n".join(f"      '{key}'," for key in keys) + "\n"
    text = re.sub(r"(\s*'run50-kentucky-derby-marathon-2025-en',)", insert + r"\1", text)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    make_cover_assets()
    events = extract_events()
    image_map = convert_images(events)
    blocks = make_blocks(events, image_map)
    blocks_en = translated_blocks(blocks)
    write_story_page(blocks, "zh")
    write_story_page(blocks_en, "en")
    write_facebook_page(blocks_en)
    write_wechat_page(blocks)
    update_story_indexes()
    update_run50_data()
    update_comments_sql()
    print(json.dumps({"events": len(events), "blocks": len(blocks), "images": sum(1 for b in blocks if b.kind == "image")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
