from pathlib import Path
from html import escape
from lxml import html
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps
import json
import re
import shutil
import tempfile
import time
import urllib.parse
import urllib.request


REPO = Path(__file__).resolve().parents[1]
SOURCE_BASE = Path(
    r"Z:\ZhennanZ Folder\000-Marathon-Story-2024-2025\20230000-Marathons\2022-State-06-HI"
)
SOURCE_HTMLS = sorted(SOURCE_BASE.glob("*.html"), key=lambda path: path.stat().st_size)
CITY_HTML = SOURCE_HTMLS[0]
RACE_HTML = SOURCE_HTMLS[-1]

SITE = "https://arsenanzz.github.io/ZZ"
SLUG = "honolulu-marathon"
VERSION = "20260615-6"
ENGAGEMENT_VERSION = "20260615"

OUT_IMG_DIR = (
    REPO
    / "run50"
    / "stories"
    / "chinese"
    / "Run50-Honolulu-Marathon-clean_files"
)
OG_PATH = REPO / "assets" / "og-run50-honolulu-marathon-icons.png"
THUMB_PATH = REPO / "assets" / "thumb-run50-honolulu-marathon-icons.svg"
FB_THUMB_PATH = REPO / "assets" / "facebook" / THUMB_PATH.name
MEDAL_COVER_PATH = REPO / "assets" / "cover-medal-hi.jpg"
TRANSLATION_CACHE = Path(tempfile.gettempdir()) / "zz_honolulu_translation_cache.json"

TITLE_ZH = "Run50 #第6州｜夏威夷：火奴鲁鲁马拉松｜50周年海岛白日梦"
TITLE_EN = "Run50 #6 | Hawaii: Honolulu Marathon and an Island Daydream"
TITLE_FB = "Honolulu made a first marathon feel like an all-day island celebration"
DATE_ZH = "2022.12.11"
DATE_EN = "Dec 11, 2022"
RACE_NAME = "50th Honolulu Marathon"

SKIP_TEXTS = {
    "0/0",
    "继续观看",
    "▲ Honolulu Vlog @Arsenan",
    "- Honolulu",
    "- Honolulu -",
    "▲50th Honolulu Marathon Course @Arsenan",
    "▲Marathon Vlog @Arsenan",
}

SPECIAL_TRANSLATIONS = {
    "丨HAWAII丨": "| HAWAII |",
    "前言": "Preface",
    "后记": "Postscript",
    "- 本文完 -": "- End -",
    "文字丨Arsenan": "Words | Arsenan",
    "摄影丨Arsenan": "Photos | Arsenan",
    "设计丨Arsenan": "Design | Arsenan",
    "🌴 Honolulu, Hawaii": "Honolulu, Hawaii",
    "🥝 Honolulu, Hawaii": "Honolulu, Hawaii",
    "01": "01",
    "02": "02",
    "03": "03",
    "04": "04",
    "Maunalua Bay Beach Park": "Maunalua Bay Beach Park",
    "Keawaula Beach": "Keawaula Beach",
    "Kea'au Beach Park": "Kea'au Beach Park",
    "Holiday": "Holiday",
}


def norm(value: str) -> str:
    return re.sub(
        r"\s+",
        " ",
        value.replace("\xa0", " ").replace("\u200d", "").replace("\u200b", ""),
    ).strip()


def clean_story_text(text: str) -> str:
    text = norm(text)
    text = text.replace("彷佛", "仿佛")
    text = text.replace("的的", "的")
    text = text.replace("damn", "damn")
    text = text.replace("Menorial", "Memorial")
    text = text.replace("Mongo Ice Cream", "Mango Ice Cream")
    text = text.replace("Hotport", "Hotpot")
    text = text.replace("Aloha Moana Blvd", "Ala Moana Blvd")
    text = text.replace("Kahanamoku Lagoon", "Kahanamoku Lagoon")
    return text.strip()


def is_styleish(value: str) -> bool:
    return ":host {" in value or "--weui-" in value or len(value) > 1700


def has_desc_leaf_container(el) -> bool:
    for desc in el.iterdescendants():
        if desc.tag in ("p", "section"):
            text = norm("".join(desc.itertext()))
            if text and not is_styleish(text):
                return True
    return False


def files_dir_for(path: Path) -> Path:
    return path.parent / f"{path.stem}_files"


def local_source_path(path: Path, src: str) -> Path:
    name = Path(src.split("#", 1)[0].split("?", 1)[0].replace("\\", "/")).name
    candidate = files_dir_for(path) / name
    if candidate.exists():
        return candidate
    raise FileNotFoundError(f"Could not map image source {src!r} for {path.name}")


def is_story_image(src: str) -> bool:
    name = Path(src.split("#", 1)[0].split("?", 1)[0].replace("\\", "/")).name
    return name.startswith("640")


def extract_article(path: Path, article: str):
    source = path.read_text(encoding="utf-8", errors="replace")
    doc = html.fromstring(source)
    roots = doc.xpath('//*[@id="js_content"]')
    root = roots[0] if roots else doc
    events = []

    def walk(el):
        if not isinstance(el.tag, str):
            return
        if el.tag == "img":
            src = el.get("src") or el.get("data-src") or ""
            if src and is_story_image(src):
                events.append({"type": "image", "source": local_source_path(path, src), "article": article})
            return
        if el.tag in ("p", "section"):
            text = clean_story_text("".join(el.itertext()))
            if text and not is_styleish(text) and not has_desc_leaf_container(el):
                if (
                    text not in SKIP_TEXTS
                    and text != path.stem
                    and not text.startswith("鲜花")
                ):
                    events.append({"type": "text", "text": text, "article": article})
                for img in el.xpath(".//img"):
                    src = img.get("src") or img.get("data-src") or ""
                    if src and is_story_image(src):
                        events.append({"type": "image", "source": local_source_path(path, src), "article": article})
                return
        for child in el:
            walk(child)

    for child in root:
        walk(child)

    clean = []
    for event in events:
        key = (
            event["type"],
            event.get("text") or event["source"].name,
        )
        prev = (
            clean[-1]["type"],
            clean[-1].get("text") or clean[-1]["source"].name,
        ) if clean else None
        if key != prev:
            clean.append(event)

    end = len(clean)
    for idx, event in enumerate(clean):
        if event["type"] == "text" and event["text"] == "设计丨Arsenan":
            end = idx + 1
            break
    return clean[:end]


def is_caption(text: str) -> bool:
    return text.startswith("▲") or text.startswith("Keawaula Beach @")


def clean_caption(text: str) -> str:
    text = clean_story_text(text)
    text = text.replace("▲Arrived in Honolulu @Arsenan▲Arrived in Honolulu @Arsenan", "▲ Arrived in Honolulu @Arsenan")
    text = text.replace("▲", "▲ ")
    text = re.sub(r"\s+", " ", text)
    text = text.replace("Wahine&Kane", "Wahine & Kane")
    text = text.replace("AlaWai", "Ala Wai")
    text = text.replace("Keawaula Beach@", "Keawaula Beach @")
    text = text.replace("Menorial", "Memorial")
    text = text.replace("Mongo Ice Cream", "Mango Ice Cream")
    text = text.replace("Hotport", "Hotpot")
    text = text.replace("Aloha Moana Blvd", "Ala Moana Blvd")
    if not text.startswith("▲") and "@" in text:
        text = "▲ " + text
    return text.strip()


def load_translation_cache() -> dict[str, str]:
    if TRANSLATION_CACHE.exists():
        return json.loads(TRANSLATION_CACHE.read_text(encoding="utf-8"))
    return {}


def save_translation_cache(cache: dict[str, str]) -> None:
    TRANSLATION_CACHE.parent.mkdir(parents=True, exist_ok=True)
    TRANSLATION_CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")


def needs_machine_translation(text: str) -> bool:
    if text in SPECIAL_TRANSLATIONS:
        return False
    if is_caption(text):
        return False
    if re.fullmatch(r"\d{2}", text):
        return False
    return True


def google_translate_joined(texts: list[str]) -> list[str]:
    if not texts:
        return []
    separators = [f"ZZSEP{i:04d}ZZ" for i in range(1, len(texts))]
    joined = texts[0]
    for sep, text in zip(separators, texts[1:]):
        joined += f"\n{sep}\n{text}"
    query = urllib.parse.urlencode(
        {
            "client": "gtx",
            "sl": "zh-CN",
            "tl": "en",
            "dt": "t",
            "q": joined,
        }
    )
    url = "https://translate.googleapis.com/translate_a/single?" + query
    with urllib.request.urlopen(url, timeout=45) as response:
        data = json.loads(response.read().decode("utf-8"))
    translated = "".join(part[0] for part in data[0])
    pieces = [translated]
    for sep in separators:
        next_pieces = []
        for piece in pieces:
            next_pieces.extend(piece.split(sep))
        pieces = next_pieces
    if len(pieces) != len(texts):
        raise RuntimeError("Batch translation separator split mismatch")
    return [polish_translation(piece.strip()) for piece in pieces]


def ensure_translations(events) -> dict[str, str]:
    cache = load_translation_cache()
    missing = []
    for event in events:
        if event["type"] != "text":
            continue
        text = event["text"]
        key = translation_key(text)
        if needs_machine_translation(text) and key not in cache:
            missing.append(key)

    # Preserve first occurrence order while removing duplicates.
    missing = list(dict.fromkeys(missing))
    batch = []
    batch_chars = 0
    for key in missing:
        if batch and batch_chars + len(key) > 1400:
            for src, dst in zip(batch, safe_translate_batch(batch)):
                cache[src] = dst
            batch = []
            batch_chars = 0
            time.sleep(0.2)
        batch.append(key)
        batch_chars += len(key)
    if batch:
        for src, dst in zip(batch, safe_translate_batch(batch)):
            cache[src] = dst
    save_translation_cache(cache)
    return cache


def safe_translate_batch(texts: list[str]) -> list[str]:
    try:
        return google_translate_joined(texts)
    except Exception:
        translated = []
        for text in texts:
            translated.extend(google_translate_joined([text]))
            time.sleep(0.15)
        return translated


def translation_key(text: str) -> str:
    if text.startswith("# "):
        return text[2:].strip()
    return text


def polish_translation(text: str) -> str:
    replacements = {
        "HonuLuLu": "Honolulu",
        "Honolulu Horse": "Honolulu Marathon",
        "Horse Expo": "Marathon Expo",
        "horse Expo": "Marathon Expo",
        "horse expo": "Marathon Expo",
        "Hawaii Marathon Expo": "Honolulu Marathon Expo",
        "Hawaii Honolulu Marathon": "Honolulu Marathon",
        "Hawaii Marathon": "Honolulu Marathon",
        "Honolulu Marathon Horse": "Honolulu Marathon",
        "Hawaiian Horse logo": "Honolulu Marathon logo",
        "Hawaiian Horse": "Honolulu Marathon",
        "maiden horse": "first marathon",
        "running a horse race": "running a marathon",
        "horse racing": "running a marathon",
        "running a horse": "running a marathon",
        "number book": "bib",
        "finishing clothes": "finisher shirt",
        "only has finisher shirt and needs to be collected after the race": "only gives out the finisher shirt after the race",
        "competition day": "race day",
        "Before the game": "Before the race",
        "pre-game concert": "pre-race concert",
        "large-scale anniversary game": "big anniversary race",
        "we naturally have to clean up": "we naturally had to do some shopping",
        "leather jacket": "light shell jacket",
        "felt very beautiful": "felt pretty great",
        "infantry posture": "mostly walk it",
        "if the condition was good": "if we felt okay",
        "King Kameha": "King Kamehameha",
        "Missionary Home Museum": "Mission Houses Museum",
        "probably probably": "probably",
        "the only marathon in the world that is open": "probably the only major marathon in the world with no cutoff",
        "being closed": "being cut off",
        "maiden full marathon": "first full marathon",
        "Before the race, Marathon Expo, music festival": "Before the race: expo and music festival",
        "Mathea himself": "Mathea herself",
        "On this day, she was": "That day, she was",
        "will start at 5 o'clock in the morning": "starts at 5 o'clock in the morning",
        "The tram rides": "The EV drives",
        "the oil pipe": "YouTube",
        "Waikiki": "Waikiki",
        "Louisville": "Louisville",
        "Costco": "Costco",
        "Tesla": "Tesla",
        "Aloha": "Aloha",
        "Diamond Head": "Diamond Head",
        "Ala Wai": "Ala Wai",
        "Ala Moana": "Ala Moana",
        "Sun Yat-sen Menorial": "Sun Yat-sen Memorial",
        "Mongo Ice Cream": "Mango Ice Cream",
        "Hotport": "Hotpot",
        "damn's parade": "damn parade",
        "relay": "relay",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = text.replace(" ,", ",").replace(" .", ".").replace(" !", "!")
    text = text.replace("probably probably", "probably")
    return text


def translate_text(text: str, cache: dict[str, str]) -> str:
    if is_caption(text):
        return clean_caption(text)
    if text in SPECIAL_TRANSLATIONS:
        return SPECIAL_TRANSLATIONS[text]
    if re.fullmatch(r"\d{2}", text):
        return text
    key = translation_key(text)
    return polish_translation(cache[key])


FONT_DIR = Path(r"C:\Windows\Fonts")


def font(size: int, bold: bool = False):
    names = ["arialbd.ttf", "msyhbd.ttc", "simhei.ttf"] if bold else ["arial.ttf", "msyh.ttc"]
    for name in names:
        path = FONT_DIR / name
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def copy_story_images(all_events):
    OUT_IMG_DIR.mkdir(parents=True, exist_ok=True)
    for old in OUT_IMG_DIR.glob("img-*.webp"):
        old.unlink()
    image_index = 0
    for event in all_events:
        if event["type"] != "image":
            continue
        image_index += 1
        out_name = f"img-{image_index:03d}.webp"
        with Image.open(event["source"]) as image:
            image = ImageOps.exif_transpose(image)
            if image.mode != "RGB":
                image = image.convert("RGB")
            image.save(OUT_IMG_DIR / out_name, "WEBP", quality=88, method=6)
        event["out"] = out_name
    return image_index


def render_text(text: str, lang: str, cache: dict[str, str]) -> str:
    original = text
    value = clean_story_text(text) if lang == "zh" else translate_text(text, cache)
    if original.startswith("# "):
        value = clean_story_text(original[2:]) if lang == "zh" else value
        return f"<h2>{escape(value)}</h2>"
    if original in {"前言", "后记"}:
        return f"<h2>{escape(value)}</h2>"
    if re.fullmatch(r"\d{2}", original):
        return f"<h3>{escape(value)}</h3>"
    if original == "丨HAWAII丨":
        return f'<p class="story-kicker-line">{escape(value)}</p>'
    if original == "- 本文完 -":
        return f'<p class="end-mark">{escape(value)}</p>'
    return f"<p>{escape(value)}</p>"


def render_events(events, lang: str, image_prefix: str, alt_prefix: str, cache: dict[str, str]) -> str:
    output = []
    pending_caption = None
    for event in events:
        if event["type"] == "image":
            number = event["out"].split("-")[1].split(".")[0]
            figure = (
                f'<figure><img src="{image_prefix}{event["out"]}" '
                f'alt="{escape(alt_prefix)} {number}" loading="lazy" decoding="async">'
            )
            if pending_caption:
                figure += f"<figcaption>{escape(pending_caption)}</figcaption>"
                pending_caption = None
            figure += "</figure>"
            output.append(figure)
            continue

        original = event["text"]
        if is_caption(original):
            caption = clean_caption(original) if lang == "zh" else translate_text(original, cache)
            if output and output[-1].endswith("</figure>") and "<figcaption>" not in output[-1]:
                output[-1] = output[-1].replace("</figure>", f"<figcaption>{escape(caption)}</figcaption></figure>")
            else:
                pending_caption = caption
            continue
        if pending_caption:
            output.append(f'<p class="caption-line">{escape(pending_caption)}</p>')
            pending_caption = None
        output.append(render_text(original, lang, cache))
    if pending_caption:
        output.append(f'<p class="caption-line">{escape(pending_caption)}</p>')
    return "\n".join(output)


def engagement_block(lang: str) -> str:
    page_key = f"run50-{SLUG}-zh" if lang == "zh" else f"run50-{SLUG}-en"
    comments_id = f"supabase-comments-honolulu-{'zh' if lang == 'zh' else 'en'}"
    if lang == "zh":
        return f"""
  <section class="zz-engagement" data-zz-engagement data-locale="zh-CN" data-page-key="{page_key}">
    <div class="zz-engagement-shell">
      <div>
        <p class="zz-engagement-kicker">留言 / 阅读</p>
        <h2>跑完也说两句</h2>
        <p class="zz-engagement-note">不用登录，留下名字就可以评论。新评论会直接显示。</p>
        <div class="zz-engagement-stats">
          <span class="zz-engagement-stat" id="busuanzi_container_page_pv"><span>阅读</span><strong id="busuanzi_value_page_pv" data-zz-view-count>--</strong></span>
        </div>
      </div>
      <div class="zz-engagement-card">
        <div id="{comments_id}" data-zz-supabase-comments></div>
        <p class="zz-engagement-status" data-zz-engagement-status>评论加载中...</p>
      </div>
    </div>
  </section>
  <script src="../../../assets/zz-engagement-config.js?v={ENGAGEMENT_VERSION}"></script>
  <script src="../../../assets/zz-engagement.js?v={ENGAGEMENT_VERSION}"></script>
"""
    return f"""
  <section class="zz-engagement" data-zz-engagement data-locale="en" data-page-key="{page_key}">
    <div class="zz-engagement-shell">
      <div>
        <p class="zz-engagement-kicker">Comments / Views</p>
        <h2>Say something after the run</h2>
        <p class="zz-engagement-note">No account is needed to submit a comment. New comments appear right away.</p>
        <div class="zz-engagement-stats">
          <span class="zz-engagement-stat" id="busuanzi_container_page_pv"><span>Views</span><strong id="busuanzi_value_page_pv" data-zz-view-count>--</strong></span>
        </div>
      </div>
      <div class="zz-engagement-card">
        <div id="{comments_id}" data-zz-supabase-comments></div>
        <p class="zz-engagement-status" data-zz-engagement-status>Loading comments...</p>
      </div>
    </div>
  </section>
  <script src="../../../assets/zz-engagement-config.js?v={ENGAGEMENT_VERSION}"></script>
  <script src="../../../assets/zz-engagement.js?v={ENGAGEMENT_VERSION}"></script>
"""


def facebook_engagement() -> str:
    return f"""
  <section class="zz-engagement" data-zz-engagement data-locale="en" data-page-key="run50-{SLUG}-facebook-en">
    <div class="zz-engagement-shell">
      <div>
        <p class="zz-engagement-kicker">Comments / Views</p>
        <h2>Say something after the run</h2>
        <p class="zz-engagement-note">No account is needed to submit a comment. New comments appear right away.</p>
        <div class="zz-engagement-stats">
          <span class="zz-engagement-stat" id="busuanzi_container_page_pv"><span>Views</span><strong id="busuanzi_value_page_pv" data-zz-view-count>--</strong></span>
        </div>
      </div>
      <div class="zz-engagement-card">
        <div id="supabase-comments-honolulu-fb" data-zz-supabase-comments></div>
        <p class="zz-engagement-status" data-zz-engagement-status>Loading comments...</p>
      </div>
    </div>
  </section>
  <script src="../../assets/zz-engagement-config.js?v={ENGAGEMENT_VERSION}"></script>
  <script src="../../assets/zz-engagement.js?v={ENGAGEMENT_VERSION}"></script>
"""


BASE_STORY_CSS = """
  :root { color-scheme: light; --ink:#20242b; --muted:#667085; --paper:#edf3f7; --line:#d0dfe8; --blue:#0b67c2; }
  * { box-sizing: border-box; }
  body { margin:0; font-family: Inter, "Segoe UI", Arial, sans-serif; background:#f6f9fb; color:var(--ink); line-height:1.78; }
  a { color:inherit; }
  nav { max-width:1080px; margin:0 auto; padding:22px 20px; display:flex; gap:18px; justify-content:flex-end; font-weight:800; color:#526170; }
  .hero { background:linear-gradient(180deg,#e7f1f6,#f6f9fb); border-bottom:1px solid var(--line); }
  .hero-inner { max-width:1080px; margin:0 auto; padding:34px 20px 42px; }
  .eyebrow { color:var(--blue); font-size:13px; font-weight:900; letter-spacing:.08em; text-transform:uppercase; }
  h1 { margin:10px 0 14px; font-family: Georgia, "Times New Roman", serif; font-size:clamp(36px,5vw,66px); line-height:1.02; letter-spacing:0; max-width:900px; }
  .deck { max-width:820px; color:#53606b; font-size:19px; margin:0 0 22px; }
  .meta-row { display:flex; flex-wrap:wrap; gap:10px; margin:22px 0 28px; }
  .meta-row span { border:1px solid var(--line); background:#fff; border-radius:999px; padding:8px 13px; font-size:13px; font-weight:800; color:#344252; }
  .cover { width:100%; max-width:980px; display:block; border-radius:8px; border:1px solid var(--line); box-shadow:0 24px 60px rgba(15,23,42,.12); background:#cfe9f4; }
  main { max-width:860px; margin:0 auto; padding:40px 20px 72px; }
  article { background:#fff; border:1px solid var(--line); border-radius:8px; padding:clamp(22px,4vw,44px); box-shadow:0 18px 48px rgba(15,23,42,.08); }
  article p { margin:0 0 18px; font-size:18px; }
  article h2 { margin:32px 0 14px; font-family: Georgia, "Times New Roman", serif; font-size:32px; line-height:1.2; }
  article h3 { margin:30px 0 10px; color:var(--blue); font-size:18px; letter-spacing:.08em; }
  .story-kicker-line, .section-label { color:var(--blue); font-weight:900; letter-spacing:.08em; text-transform:uppercase; }
  .end-mark { text-align:center; color:var(--muted); font-weight:800; }
  figure { margin:26px 0; }
  figure img { width:100%; height:auto; display:block; border-radius:8px; border:1px solid #d7e3ea; background:#f4f7f9; }
  figcaption, .caption-line { margin-top:8px; color:#6a7480; font-size:14px; text-align:center; }
  @media (max-width: 620px) {
    nav { justify-content:flex-start; overflow-x:auto; }
    article { padding:20px 16px; }
    article p { font-size:17px; }
  }
"""


FB_CSS = """
  :root { color-scheme: light; --ink:#111827; --muted:#53606b; --line:#d0dfe8; --blue:#0b67c2; --soft:#edf3f7; }
  * { box-sizing:border-box; }
  body { margin:0; background:#f7f9fb; color:var(--ink); font-family:Inter,"Segoe UI",Arial,sans-serif; line-height:1.78; }
  a { color:inherit; text-decoration:none; }
  .topbar { background:#0b111c; color:#fff; border-bottom:4px solid var(--blue); }
  .topbar-inner { max-width:1180px; margin:0 auto; padding:17px 20px; display:flex; align-items:center; justify-content:space-between; gap:14px; flex-wrap:wrap; }
  .brand { font-size:18px; font-weight:950; letter-spacing:.12em; }
  .brand span { color:#8ab9f0; }
  .topbar nav { display:flex; gap:16px; font-size:14px; font-weight:800; flex-wrap:wrap; }
  .hero { max-width:1180px; margin:0 auto; padding:42px 20px 30px; }
  .eyebrow { color:var(--blue); font-size:14px; font-weight:950; letter-spacing:.12em; text-transform:uppercase; }
  h1 { margin:12px 0 18px; max-width:980px; font-family:Georgia,"Times New Roman",serif; font-size:clamp(38px,5vw,70px); line-height:1.02; letter-spacing:0; }
  .dek { max-width:900px; font-size:20px; color:#3f4d5a; }
  .meta-row { display:flex; flex-wrap:wrap; gap:10px; margin:24px 0 30px; }
  .meta-row span { background:#e9f2f8; border:1px solid var(--line); border-radius:999px; padding:8px 14px; font-weight:850; font-size:13px; }
  .lead-cover { width:100%; max-width:1060px; display:block; border-radius:8px; border:1px solid var(--line); box-shadow:0 20px 54px rgba(15,23,42,.14); background:#cfe9f4; }
  .layout { max-width:1180px; margin:0 auto; padding:28px 20px 76px; display:grid; grid-template-columns:minmax(0,780px) 320px; gap:34px; align-items:start; }
  article { background:#fff; border:1px solid var(--line); border-radius:8px; padding:36px; box-shadow:0 18px 48px rgba(15,23,42,.08); }
  article p { margin:0 0 18px; font-size:18px; }
  article h2 { margin:34px 0 14px; font-family:Georgia,"Times New Roman",serif; font-size:32px; line-height:1.2; }
  article h3 { margin:30px 0 10px; color:var(--blue); font-size:18px; letter-spacing:.08em; }
  .section-label { color:var(--blue); font-weight:950; letter-spacing:.12em; text-transform:uppercase; }
  .transition { border-left:5px solid var(--blue); padding:14px 0 14px 18px; color:#334155; background:#f0f6fb; }
  figure { margin:26px 0; }
  figure img { width:100%; height:auto; display:block; border-radius:8px; border:1px solid #d7e3ea; }
  figcaption, .caption-line { margin-top:8px; color:#6a7480; font-size:14px; text-align:center; }
  .rail { position:sticky; top:18px; display:grid; gap:18px; }
  .brief, .related { background:#fff; border:1px solid var(--line); border-radius:8px; padding:20px; box-shadow:0 14px 36px rgba(15,23,42,.08); }
  .brief h2 { margin:0 0 12px; font-size:18px; }
  dl { margin:0; display:grid; gap:12px; }
  dt { color:var(--muted); font-size:12px; font-weight:900; text-transform:uppercase; }
  dd { margin:2px 0 0; font-weight:750; line-height:1.45; }
  .related a { display:block; margin-top:10px; color:var(--blue); font-weight:850; }
  @media (max-width:900px) {
    .layout { grid-template-columns:1fr; }
    .rail { position:static; }
  }
  @media (max-width:620px) {
    .topbar-inner { align-items:flex-start; }
    article { padding:22px 16px; }
    article p { font-size:17px; }
  }
"""


def story_page(lang: str, city_article: str, race_article: str) -> str:
    is_zh = lang == "zh"
    title = TITLE_ZH if is_zh else TITLE_EN
    desc = (
        "Run50第6州夏威夷：火奴鲁鲁白日梦、威基基、钻石头山、彩虹船、自驾西海岸，以及2022年12月11日第50届火奴鲁鲁马拉松，47的第一个全马。"
        if is_zh
        else "Run50 State 6 in Hawaii: an island daydream in Honolulu, Waikiki, Diamond Head, rainbows, the west coast drive, and the 50th Honolulu Marathon on December 11, 2022, 47's first full marathon."
    )
    other = "English" if is_zh else "中文"
    other_href = f"../english/{SLUG}.html" if is_zh else f"../chinese/{SLUG}.html"
    lang_attr = "zh-Hans" if is_zh else "en"
    eyebrow = "Run50 #第6州 · 夏威夷" if is_zh else "Run50 #6 · Hawaii"
    city_label = "海岛白日梦" if is_zh else "Island daydream"
    race_label = "50周年火奴鲁鲁马拉松" if is_zh else "The 50th Honolulu Marathon"
    return f"""<!doctype html>
<html lang="{lang_attr}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)}</title>
  <meta name="description" content="{escape(desc)}">
  <meta property="og:title" content="{escape(title)}">
  <meta property="og:description" content="{escape(desc)}">
  <meta property="og:image" content="{SITE}/assets/{OG_PATH.name}?v={VERSION}">
  <meta property="og:type" content="article">
  <link rel="stylesheet" href="../../../assets/zz-engagement.css?v={ENGAGEMENT_VERSION}">
  <style>{BASE_STORY_CSS}</style>
</head>
<body>
  <nav>
    <a href="./">← {"中文故事" if is_zh else "English Stories"}</a>
    <a href="{other_href}">{other}</a>
    <a href="../../facebook/{SLUG}.html">Facebook</a>
    <a href="../../index.html">Run50</a>
  </nav>
  <section class="hero">
    <div class="hero-inner">
      <p class="eyebrow">{escape(eyebrow)}</p>
      <h1>{escape(title)}</h1>
      <p class="deck">{escape(desc)}</p>
      <div class="meta-row"><span>Honolulu, Hawaii</span><span>{DATE_EN}</span><span>Run50 #6</span><span>{RACE_NAME}</span></div>
      <img class="cover" src="../../../assets/{THUMB_PATH.name}?v={VERSION}" alt="Honolulu Marathon icon cover">
    </div>
  </section>
  <main>
    <article>
      <p class="section-label">{escape(city_label)}</p>
{city_article}
      <p class="section-label">{escape(race_label)}</p>
{race_article}
    </article>
  </main>
{engagement_block(lang)}
</body>
</html>
"""


def facebook_page(race_article: str, city_article: str) -> str:
    desc = "Race date: December 11, 2022. Run50 State 6 at the 50th Honolulu Marathon became 47's first full marathon, with fireworks, Waikiki, Diamond Head, an all-day no-cutoff course and a gold medal after nearly eleven hours."
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(TITLE_FB)}</title>
  <meta name="description" content="{escape(desc)}">
  <meta property="og:title" content="{escape(TITLE_FB)}">
  <meta property="og:description" content="{escape(desc)}">
  <meta property="og:image" content="{SITE}/assets/{OG_PATH.name}?v={VERSION}">
  <meta property="og:type" content="article">
  <link rel="stylesheet" href="../../assets/zz-engagement.css?v={ENGAGEMENT_VERSION}">
  <style>{FB_CSS}</style>
</head>
<body>
  <header class="topbar">
    <div class="topbar-inner">
      <a class="brand" href="./">RUN50 <span>FACEBOOK</span></a>
      <nav><a href="../hub.html">Run50 Hub</a><a href="../stories/english/{SLUG}.html">English</a><a href="../stories/chinese/{SLUG}.html">中文</a></nav>
    </div>
  </header>
  <section class="hero">
    <p class="eyebrow">World / USA / Marathon</p>
    <h1>{escape(TITLE_FB)}</h1>
    <p class="dek">On December 11, 2022, the 50th Honolulu Marathon turned Run50 State 6 into something bigger than a race: a dawn firework start, 47's first marathon, and a long warm walk through Waikiki, Diamond Head and the east side of Oahu.</p>
    <div class="meta-row"><span>Honolulu, Hawaii</span><span>{DATE_EN}</span><span>Run50 #6</span><span>50th anniversary race</span></div>
    <img class="lead-cover" src="../../assets/{THUMB_PATH.name}?v={VERSION}" alt="Honolulu Marathon icon cover">
  </section>
  <main class="layout">
    <article>
      <p class="section-label">Race day</p>
      <p>The Honolulu Marathon is famous for a generous spirit: no hard cutoff, a huge Japanese running crowd, and a course that lets people finish in their own time. That spirit is why the race comes first here.</p>
{race_article}
      <p class="transition">Before that long race day, Honolulu had already set the stage: a Tesla pickup, Waikiki mornings, a rainbow whale-watch boat, a west-side drive, a lost drone, and the kind of unplanned parade that turns a trip into a memory.</p>
      <p class="section-label">The island before the race</p>
{city_article}
    </article>
    <aside class="rail">
      <div class="brief">
        <h2>Race Brief</h2>
        <dl>
          <div><dt>Race</dt><dd>{RACE_NAME}</dd></div>
          <div><dt>Date</dt><dd>{DATE_EN}</dd></div>
          <div><dt>State</dt><dd>Hawaii · Run50 #6</dd></div>
          <div><dt>Route memory</dt><dd>5 a.m. fireworks, Aloha Tower, Waikiki, Diamond Head, Kalanianaole Highway, no cutoff, and a nearly eleven-hour finish for 47's first marathon.</dd></div>
        </dl>
      </div>
      <div class="related">
        <strong>More versions</strong>
        <a href="../stories/english/{SLUG}.html">Read in original order</a>
        <a href="../stories/chinese/{SLUG}.html">中文原文整理版</a>
      </div>
    </aside>
  </main>
{facebook_engagement()}
</body>
</html>
"""


def draw_badge(draw, x, y, w, h):
    draw.rounded_rectangle((x, y, x + w, y + h), radius=22, fill="#ffffff", outline="#20242b", width=7)
    draw.text((x + 30, y + 48), "Run50 #06", fill="#20242b", font=font(38, True))
    draw.text((x + 30, y + 102), "HAWAII", fill="#0b67c2", font=font(50, True))


def draw_honolulu_scene(draw, height: int):
    scale = height / 630

    def p(x, y):
        return (int(x * scale), int(y * scale))

    sky = "#cfe9f4"
    ocean = "#40bfd1"
    sand = "#f3d890"
    green = "#78bb61"
    dark = "#20242b"
    draw.rectangle((0, 0, int(1200 * scale), height), fill=sky)
    draw.ellipse((p(930, 112), p(1024, 206)), fill="#f7bc3b")
    draw.polygon([p(0, 390), p(300, 340), p(520, 365), p(780, 315), p(1200, 355), p(1200, 630), p(0, 630)], fill=green)
    draw.polygon([p(0, 448), p(420, 420), p(900, 452), p(1200, 420), p(1200, 630), p(0, 630)], fill=ocean)
    for y in (465, 505):
        draw.arc((p(-40, y - 60), p(500, y + 60)), 8, 172, fill="#e8fbff", width=max(2, int(5 * scale)))
    draw.polygon([p(0, 555), p(460, 505), p(1200, 560), p(1200, 630), p(0, 630)], fill=sand)

    # Diamond Head.
    draw.polygon([p(120, 380), p(300, 285), p(585, 380)], fill="#8cc96b", outline="#5f9f56")
    draw.polygon([p(295, 285), p(390, 345), p(585, 380), p(390, 372)], fill="#6fb45d")

    # Waikiki blocks.
    for x, y, w, h, c in [
        (685, 330, 54, 138, "#b7d7e5"),
        (754, 305, 64, 164, "#f5d66c"),
        (836, 350, 48, 120, "#a7dccd"),
        (905, 315, 66, 155, "#d2c2ee"),
    ]:
        draw.rectangle((p(x, y), p(x + w, 470)), fill=c, outline="#6b7280", width=max(1, int(2 * scale)))
        for wx in range(x + 12, x + w - 8, 22):
            for wy in range(y + 18, 458, 32):
                draw.rectangle((p(wx, wy), p(wx + 8, wy + 12)), fill="#fff6bf")

    # Palm.
    draw.line((p(620, 500), p(662, 328)), fill="#8b5e34", width=max(7, int(12 * scale)))
    for angle in [(-84, -18), (-58, -70), (-18, -92), (34, -72), (76, -22)]:
        x2 = 660 + angle[0]
        y2 = 330 + angle[1]
        draw.polygon([p(660, 330), p(x2, y2), p(675, 346)], fill="#27965f")

    # Fireworks over the ocean.
    for cx, cy, color in [(472, 236, "#ff7f50"), (552, 208, "#f7bc3b"), (635, 242, "#8ab9f0")]:
        for dx, dy in [(0, -44), (36, -24), (44, 10), (20, 38), (-24, 36), (-42, 0), (-26, -30)]:
            draw.line((p(cx, cy), p(cx + dx, cy + dy)), fill=color, width=max(2, int(3 * scale)))
        draw.ellipse((p(cx - 5, cy - 5), p(cx + 5, cy + 5)), fill=color)

    # Two walkers/runners.
    for x, y, shirt in [(520, 485, "#0b67c2"), (565, 492, "#ff7f50")]:
        draw.ellipse((p(x, y), p(x + 24, y + 24)), fill=shirt)
        draw.line((p(x + 12, y + 24), p(x + 10, y + 68)), fill=dark, width=max(3, int(5 * scale)))
        draw.line((p(x + 10, y + 42), p(x - 18, y + 60)), fill=dark, width=max(3, int(5 * scale)))
        draw.line((p(x + 10, y + 68), p(x - 10, y + 98)), fill=dark, width=max(3, int(5 * scale)))
        draw.line((p(x + 10, y + 68), p(x + 38, y + 96)), fill=dark, width=max(3, int(5 * scale)))


def generate_cover_png():
    image = Image.new("RGB", (1200, 630), "#cfe9f4")
    draw = ImageDraw.Draw(image)
    draw_honolulu_scene(draw, 630)
    draw.text((64, 64), "HONOLULU", fill="#20242b", font=font(66, True))
    draw.text((66, 136), "WAIKIKI · DIAMOND HEAD · FIREWORKS", fill="#667085", font=font(26, True))
    draw_badge(draw, 760, 64, 362, 164)
    image.save(OG_PATH)


def generate_cover_svg():
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 750" width="1200" height="750" role="img" aria-labelledby="title desc">
  <title id="title">Honolulu Marathon Run50 icon cover</title>
  <desc id="desc">Icon cover with Waikiki, Diamond Head, ocean waves, fireworks and a Run50 Hawaii badge.</desc>
  <rect width="1200" height="750" fill="#cfe9f4"/>
  <circle cx="960" cy="132" r="58" fill="#f7bc3b"/>
  <path d="M0 470 L300 405 L520 440 L780 380 L1200 430 L1200 750 L0 750Z" fill="#78bb61"/>
  <path d="M0 535 L420 505 L900 540 L1200 505 L1200 750 L0 750Z" fill="#40bfd1"/>
  <path d="M0 650 L460 595 L1200 660 L1200 750 L0 750Z" fill="#f3d890"/>
  <path d="M120 455 L300 340 L585 455Z" fill="#8cc96b" stroke="#5f9f56" stroke-width="4"/>
  <path d="M295 340 L390 405 L585 455 L390 445Z" fill="#6fb45d"/>
  <g stroke="#e8fbff" stroke-width="5" fill="none" opacity=".9">
    <path d="M-40 545 Q230 475 500 545"/>
    <path d="M-40 595 Q230 525 500 595"/>
  </g>
  <g stroke="#6b7280" stroke-width="2">
    <rect x="685" y="395" width="54" height="165" fill="#b7d7e5"/>
    <rect x="754" y="365" width="64" height="195" fill="#f5d66c"/>
    <rect x="836" y="420" width="48" height="140" fill="#a7dccd"/>
    <rect x="905" y="378" width="66" height="182" fill="#d2c2ee"/>
  </g>
  <line x1="620" y1="595" x2="662" y2="390" stroke="#8b5e34" stroke-width="13" stroke-linecap="round"/>
  <g fill="#27965f">
    <path d="M660 390 L576 372 L675 410Z"/>
    <path d="M660 390 L602 320 L675 410Z"/>
    <path d="M660 390 L642 298 L675 410Z"/>
    <path d="M660 390 L694 318 L675 410Z"/>
    <path d="M660 390 L736 368 L675 410Z"/>
  </g>
  <g stroke-width="4" stroke-linecap="round">
    <g stroke="#ff7f50"><line x1="472" y1="280" x2="472" y2="228"/><line x1="472" y1="280" x2="510" y2="252"/><line x1="472" y1="280" x2="516" y2="292"/><line x1="472" y1="280" x2="494" y2="322"/><line x1="472" y1="280" x2="446" y2="320"/><line x1="472" y1="280" x2="426" y2="280"/></g>
    <g stroke="#f7bc3b"><line x1="552" y1="250" x2="552" y2="198"/><line x1="552" y1="250" x2="592" y2="225"/><line x1="552" y1="250" x2="595" y2="263"/><line x1="552" y1="250" x2="574" y2="292"/><line x1="552" y1="250" x2="525" y2="287"/></g>
    <g stroke="#8ab9f0"><line x1="635" y1="288" x2="635" y2="238"/><line x1="635" y1="288" x2="673" y2="260"/><line x1="635" y1="288" x2="680" y2="300"/><line x1="635" y1="288" x2="657" y2="328"/><line x1="635" y1="288" x2="607" y2="322"/></g>
  </g>
  <g stroke="#20242b" stroke-width="6" fill="none">
    <circle cx="532" cy="575" r="14" fill="#0b67c2" stroke="none"/>
    <line x1="532" y1="589" x2="530" y2="640"/>
    <line x1="530" y1="610" x2="502" y2="632"/>
    <line x1="530" y1="640" x2="510" y2="686"/>
    <line x1="530" y1="640" x2="568" y2="678"/>
    <circle cx="578" cy="584" r="14" fill="#ff7f50" stroke="none"/>
    <line x1="578" y1="598" x2="575" y2="650"/>
    <line x1="575" y1="620" x2="548" y2="640"/>
    <line x1="575" y1="650" x2="555" y2="694"/>
    <line x1="575" y1="650" x2="612" y2="684"/>
  </g>
  <text x="70" y="104" font-family="Arial, Helvetica, sans-serif" font-size="66" font-weight="900" fill="#20242b">HONOLULU</text>
  <text x="72" y="150" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="800" fill="#667085">WAIKIKI · DIAMOND HEAD · FIREWORKS</text>
  <rect x="758" y="62" width="364" height="166" rx="22" fill="#ffffff" stroke="#20242b" stroke-width="8"/>
  <text x="790" y="122" font-family="Arial, Helvetica, sans-serif" font-size="41" font-weight="900" fill="#20242b">Run50 #06</text>
  <text x="790" y="182" font-family="Arial, Helvetica, sans-serif" font-size="52" font-weight="900" fill="#0b67c2">HAWAII</text>
</svg>
'''
    THUMB_PATH.write_text(svg, encoding="utf-8")
    FB_THUMB_PATH.parent.mkdir(parents=True, exist_ok=True)
    FB_THUMB_PATH.write_text(svg, encoding="utf-8")


def generate_medal_cover():
    source = files_dir_for(RACE_HTML) / "640(116)"
    with Image.open(source) as image:
        image = ImageOps.exif_transpose(image).convert("RGB")
        bg = ImageOps.fit(image, (1200, 750), method=Image.LANCZOS, centering=(0.5, 0.5))
        bg = bg.filter(ImageFilter.GaussianBlur(18))
        overlay = Image.new("RGB", (1200, 750), "#edf3f7")
        bg = Image.blend(bg, overlay, 0.16)
        fg = image.copy()
        fg.thumbnail((1120, 720), Image.LANCZOS)
        x = (1200 - fg.width) // 2
        y = (750 - fg.height) // 2
        bg.paste(fg, (x, y))
        bg.save(MEDAL_COVER_PATH, quality=92)


def clean_text(text: str) -> str:
    return "\n".join(line.rstrip() for line in text.splitlines()) + "\n"


def remove_existing_card(text: str, href: str) -> str:
    pattern = re.compile(rf'\n\s*<a class="story-card [^"]+" href="{re.escape(href)}">.*?</a>', re.S)
    return pattern.sub("", text)


def insert_after_card(text: str, target_href: str, card: str, fallback_marker: str) -> str:
    pattern = re.compile(rf'(\n\s*<a class="story-card [^"]+" href="{re.escape(target_href)}">.*?</a>\s*)', re.S)
    if pattern.search(text):
        return pattern.sub(lambda match: match.group(1) + "\n" + card, text, count=1)
    return text.replace(fallback_marker, fallback_marker + "\n" + card, 1)


def update_mapping(text: str, new_line: str, after_line: str) -> str:
    key = new_line.strip().split(":", 1)[0]
    text = re.sub(rf"\n\s*{re.escape(key)}: '.*?',", "", text)
    if new_line in text:
        return text
    return text.replace(after_line, after_line + "\n" + new_line, 1)


def update_story_indexes():
    zh_path = REPO / "run50" / "stories" / "chinese" / "index.html"
    en_path = REPO / "run50" / "stories" / "english" / "index.html"
    fb_path = REPO / "run50" / "facebook" / "index.html"

    zh_card = f"""      <a class="story-card run-50" href="./{SLUG}.html">
        <img src="../../../assets/{MEDAL_COVER_PATH.name}?v={VERSION}" alt="火奴鲁鲁马拉松奖牌封面" loading="lazy" decoding="async">
        <div class="story-copy">
          <p class="story-meta">夏威夷火奴鲁鲁 · {DATE_ZH}</p>
          <h2 class="story-title">Run50 #第6州｜火奴鲁鲁马拉松</h2>
          <p class="story-desc">两篇合并：火奴鲁鲁白日梦、威基基晨光、钻石头和彩虹船，以及50周年火奴鲁鲁马拉松，47的第一个全马。</p>
          <div class="story-foot"><span>长文图记</span><span>阅读 →</span></div>
        </div>
      </a>
"""
    en_card = f"""      <a class="story-card run-50" href="./{SLUG}.html">
        <img src="../../../assets/{THUMB_PATH.name}?v={VERSION}" alt="Icon cover for Honolulu Marathon" loading="lazy" decoding="async">
        <div class="story-card-content">
          <div class="meta">Hawaii · Honolulu · {DATE_ZH}</div>
          <h2>Honolulu Marathon: an island daydream and 47's first full marathon</h2>
          <p>A two-part Hawaii story: Waikiki mornings, Diamond Head, rainbow seas, west-side roads, then the 50th Honolulu Marathon with fireworks and a nearly eleven-hour finish.</p>
        </div>
      </a>
"""
    fb_card = f"""    <a class="story-card run-50" href="./{SLUG}.html">
      <div>
        <p class="eyebrow">World / USA / Marathon</p>
        <h2>{escape(TITLE_FB)}</h2>
        <p>Race date: December 11, 2022. State 6 of Run50 at the 50th Honolulu Marathon: fireworks, Waikiki, Diamond Head, no cutoff, and 47's first marathon finish.</p>
        <div class="meta"><span>Honolulu, HI</span><span>Run50 #6</span><span>50th anniversary race</span></div>
      </div>
      <img src="../../assets/facebook/{THUMB_PATH.name}?v={VERSION}" alt="Icon-style Honolulu Marathon cover">
    </a>
"""

    text = remove_existing_card(zh_path.read_text(encoding="utf-8"), f"./{SLUG}.html")
    text = insert_after_card(text, "./indianapolis-monumental-marathon.html", zh_card, '<section class="story-grid"')
    text = update_mapping(text, f"      'HI-火奴鲁鲁': '{SLUG}.html',", "      'IN-印第安纳波利斯': 'indianapolis-monumental-marathon.html',")
    text = re.sub(
        r"'HI': \[\{city: '火奴鲁鲁', raceName: '50th Honolulu Marathon', date: '2022.12.11', emoji: '🌺', num: '#06', isPlaceholder: true\}\],",
        "'HI': [{city: '火奴鲁鲁', raceName: '50th Honolulu Marathon', date: '2022.12.11', emoji: '🌺', num: '#06', isPlaceholder: false}],",
        text,
    )
    zh_path.write_text(clean_text(text), encoding="utf-8")

    text = remove_existing_card(en_path.read_text(encoding="utf-8"), f"./{SLUG}.html")
    text = insert_after_card(text, "./indianapolis-monumental-marathon.html", en_card, '<section class="story-grid"')
    text = update_mapping(text, f"      'HI-Honolulu': '{SLUG}.html',", "      'IN-Indianapolis': 'indianapolis-monumental-marathon.html',")
    text = re.sub(
        r"'HI': \[\{city: 'Honolulu', raceName: '50th Honolulu Marathon', date: '2022.12.11', emoji: '🌺', num: '#06', isPlaceholder: false\}\],",
        "'HI': [{city: 'Honolulu', raceName: '50th Honolulu Marathon', date: '2022.12.11', emoji: '🌺', num: '#06', isPlaceholder: false}],",
        text,
    )
    en_path.write_text(clean_text(text), encoding="utf-8")

    text = remove_existing_card(fb_path.read_text(encoding="utf-8"), f"./{SLUG}.html")
    text = insert_after_card(text, "./indianapolis-monumental-marathon.html", fb_card, '<main class="shell">')
    fb_path.write_text(clean_text(text), encoding="utf-8")


def update_root_home():
    path = REPO / "index.html"
    text = path.read_text(encoding="utf-8")
    text = re.sub(
        r"\n\s*<!-- Hawaii Run50 story -->.*?<!-- /Hawaii Run50 story -->\n",
        "\n",
        text,
        flags=re.S,
    )
    card = f"""
      <!-- Hawaii Run50 story -->
      <article class="video-card" data-section="run50" data-category="run50 facebook" data-title="{escape(TITLE_FB)}">
        <a class="thumb" href="run50/facebook/{SLUG}.html">
          <img src="assets/facebook/{THUMB_PATH.name}?v={VERSION}" alt="Icon-style Honolulu Marathon cover">
          <span class="duration">Story</span>
        </a>
        <div class="meta">
          <span class="avatar run50">50</span>
          <div>
            <a class="video-title" href="run50/facebook/{SLUG}.html">{escape(TITLE_FB)}</a>
            <p class="video-sub">Honolulu, HI &middot; Dec 11, 2022</p>
          </div>
        </div>
      </article>
      <!-- /Hawaii Run50 story -->
"""
    text = text.replace("      <!-- /Indiana Run50 story -->\n", "      <!-- /Indiana Run50 story -->\n" + card, 1)
    path.write_text(clean_text(text), encoding="utf-8")


def update_landing_counts():
    path = REPO / "run50" / "index.html"
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"(\s)17 stories", r"\g<1>18 stories", text)
    text = text.replace("<strong>17</strong> stories", "<strong>18</strong> stories")
    path.write_text(clean_text(text), encoding="utf-8")


def update_hub():
    path = REPO / "run50" / "hub.html"
    text = path.read_text(encoding="utf-8")
    if "'Honolulu':{lat:21.3069,lon:-157.8583}" not in text:
        text = text.replace(
            "'San Antonio':{lat:29.4241,lon:-98.4936},'Greer'",
            "'San Antonio':{lat:29.4241,lon:-98.4936},'Honolulu':{lat:21.3069,lon:-157.8583},'Greer'",
            1,
        )
    text = re.sub(r"^\s*'HI':\[\{city:'Honolulu'.*?\}\],\n", "", text, flags=re.M)
    text = text.replace(
        "  'IN':[{city:'Indianapolis',date:'Nov 5, 2022',story:'stories/english/indianapolis-monumental-marathon.html',fb:'facebook/indianapolis-monumental-marathon.html'}],",
        "  'IN':[{city:'Indianapolis',date:'Nov 5, 2022',story:'stories/english/indianapolis-monumental-marathon.html',fb:'facebook/indianapolis-monumental-marathon.html'}],\n"
        "  'HI':[{city:'Honolulu',date:'Dec 11, 2022',story:'stories/english/honolulu-marathon.html',fb:'facebook/honolulu-marathon.html'}],",
        1,
    )
    text = re.sub(
        r"\n\s*<!-- Hawaii Honolulu story dot -->.*?<!-- /Hawaii Honolulu story dot -->\n",
        "\n",
        text,
        flags=re.S,
    )
    dot = """
    <!-- Hawaii Honolulu story dot -->
    <circle cx="168" cy="188" r="10" fill="rgba(255,80,40,0.18)" pointer-events="none"/>
    <circle cx="168" cy="188" r="5" fill="#ff4040" stroke="#fff" stroke-width="1.6" class="wm-dot"
      data-city="Honolulu, HI" data-date="Dec 11, 2022" data-story="stories/english/honolulu-marathon.html"/>
    <!-- /Hawaii Honolulu story dot -->
"""
    text = text.replace("    <!-- /Indiana Indianapolis story dot -->\n", "    <!-- /Indiana Indianapolis story dot -->\n" + dot, 1)
    path.write_text(clean_text(text), encoding="utf-8")


def update_supabase_sql():
    path = REPO / "supabase" / "run50-comments.sql"
    text = path.read_text(encoding="utf-8")
    keys = [
        f"run50-{SLUG}-facebook-en",
        f"run50-{SLUG}-en",
        f"run50-{SLUG}-zh",
    ]
    for key in keys:
        text = re.sub(rf"^\s*'{re.escape(key)}',\n", "", text, flags=re.M)

    def add_keys(match):
        indent = match.group(1)
        return "".join(f"{indent}'{key}',\n" for key in keys) + match.group(0)

    text = re.sub(
        r"^(\s*)'run50-indianapolis-monumental-marathon-facebook-en',",
        add_keys,
        text,
        flags=re.M,
    )
    path.write_text(clean_text(text), encoding="utf-8")


def main():
    city_events = extract_article(CITY_HTML, "city")
    race_events = extract_article(RACE_HTML, "race")
    all_events = city_events + race_events
    cache = ensure_translations(all_events)
    image_count = copy_story_images(all_events)
    if image_count != 247:
        raise RuntimeError(f"Expected 247 story images, got {image_count}")

    zh_city = render_events(city_events, "zh", "Run50-Honolulu-Marathon-clean_files/", "火奴鲁鲁旅行照片", cache)
    zh_race = render_events(race_events, "zh", "Run50-Honolulu-Marathon-clean_files/", "火奴鲁鲁马拉松照片", cache)
    en_city = render_events(city_events, "en", "../chinese/Run50-Honolulu-Marathon-clean_files/", "Honolulu travel photo", cache)
    en_race = render_events(race_events, "en", "../chinese/Run50-Honolulu-Marathon-clean_files/", "Honolulu Marathon photo", cache)
    fb_city = render_events(city_events, "en", "../stories/chinese/Run50-Honolulu-Marathon-clean_files/", "Honolulu travel photo", cache)
    fb_race = render_events(race_events, "en", "../stories/chinese/Run50-Honolulu-Marathon-clean_files/", "Honolulu Marathon photo", cache)

    (REPO / "run50" / "stories" / "chinese" / f"{SLUG}.html").write_text(
        story_page("zh", zh_city, zh_race), encoding="utf-8"
    )
    (REPO / "run50" / "stories" / "english" / f"{SLUG}.html").write_text(
        story_page("en", en_city, en_race), encoding="utf-8"
    )
    (REPO / "run50" / "facebook" / f"{SLUG}.html").write_text(
        facebook_page(fb_race, fb_city), encoding="utf-8"
    )

    generate_cover_png()
    generate_cover_svg()
    shutil.copyfile(THUMB_PATH, FB_THUMB_PATH)
    generate_medal_cover()
    update_story_indexes()
    update_root_home()
    update_landing_counts()
    update_hub()
    update_supabase_sql()
    print(f"Built {SLUG}: {image_count} images, {len(city_events)} city events, {len(race_events)} race events")


if __name__ == "__main__":
    main()
