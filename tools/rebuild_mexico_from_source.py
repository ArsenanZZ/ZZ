from collections import deque
from html import escape
from pathlib import Path
import re

from lxml import html
from PIL import Image, ImageDraw, ImageFont, ImageOps


REPO = Path(__file__).resolve().parents[1]
SOURCE_BASE = Path(r"Z:\ZhennanZ Folder\000-Marathon-Story-2024-2025\20250831-Mexico City Marathon\0000-Web")
SOURCE_HTML = next(p for p in SOURCE_BASE.iterdir() if p.suffix.lower() == ".html")
OUT_IMG_DIR = REPO / "run50" / "stories" / "chinese" / "mexico-marathon_files"
SITE = "https://arsenanzz.github.io/ZZ"
VERSION = "20260605-1"
SLUG = "mexico-marathon"


def norm(value: str) -> str:
    return re.sub(r"\s+", " ", value.replace("\xa0", " ")).strip()


def is_styleish(value: str) -> bool:
    return ":host {" in value or "--weui-" in value or len(value) > 1200


def is_caption(value: str) -> bool:
    return norm(value).startswith("▲")


def should_skip_text(value: str) -> bool:
    text = norm(value)
    return bool(text) and set(text) <= {"★"}


def has_desc_leaf_container(el) -> bool:
    for desc in el.iterdescendants():
        if desc.tag in ("p", "section"):
            text = norm("".join(desc.itertext()))
            if text and not is_styleish(text):
                return True
    return False


def extract_story_events():
    doc = html.fromstring(SOURCE_HTML.read_text(encoding="utf-8", errors="replace"))
    root = doc.xpath('//*[@id="js_content"]')[0]
    events = []

    def walk(el):
        if el.tag == "img":
            src = el.get("src") or el.get("data-src") or ""
            if src:
                events.append({"type": "img", "src": src})
            return
        if el.tag in ("p", "section"):
            text = norm("".join(el.itertext()))
            if text and not is_styleish(text) and not has_desc_leaf_container(el):
                if text not in ["，赞"] and not text.startswith("鲜花"):
                    events.append({"type": "text", "text": text})
                for img in el.xpath(".//img"):
                    src = img.get("src") or img.get("data-src") or ""
                    if src:
                        events.append({"type": "img", "src": src})
                return
        for child in el:
            walk(child)

    for child in root:
        walk(child)

    clean = []
    for idx, event in enumerate(events):
        key = (event["type"], event.get("text") or event.get("src"))
        prev = (clean[-1][1]["type"], clean[-1][1].get("text") or clean[-1][1].get("src")) if clean else None
        if prev != key:
            clean.append((idx, event))

    story = [(idx, event) for idx, event in clean if idx >= 5]
    for pos, (_, event) in enumerate(story):
        if event["type"] == "text" and event["text"].startswith("设计"):
            return story[: pos + 1]
    return story


def local_source_path(src: str) -> Path:
    normalized = src[2:] if src.startswith("./") else src
    return SOURCE_BASE / normalized


def copy_story_images(indexed):
    OUT_IMG_DIR.mkdir(parents=True, exist_ok=True)
    for old in OUT_IMG_DIR.glob("img-*.webp"):
        old.unlink()

    count = 0
    for _, event in indexed:
        if event["type"] != "img":
            continue
        count += 1
        out_name = f"img-{count:03d}.webp"
        src_path = local_source_path(event["src"])
        with Image.open(src_path) as im:
            im = ImageOps.exif_transpose(im)
            if im.mode != "RGB":
                im = im.convert("RGB")
            im.save(OUT_IMG_DIR / out_name, "WEBP", quality=90, method=6)
        event["out"] = out_name
    return count


def render_text(text: str) -> str:
    value = norm(text)
    if not value or should_skip_text(value):
        return ""
    if value in ("前言", "后记"):
        return f'<h2 class="section-label">{escape(value)}</h2>'
    if value.startswith("# "):
        return f"<h2>{escape(value[2:])}</h2>"
    if value.startswith(("🌶️", "📍", "🎽")):
        return f'<p class="place">{escape(value)}</p>'
    if value.startswith("- "):
        return f'<p class="end-mark">{escape(value)}</p>'
    if value.startswith(("文字丨", "摄影丨", "设计丨")):
        return f'<p class="credit-line">{escape(value)}</p>'
    return f"<p>{escape(value)}</p>"


def render_chinese_article(indexed):
    parts = []
    skip_next = False
    for pos, (_, event) in enumerate(indexed):
        if skip_next:
            skip_next = False
            continue
        if event["type"] == "img":
            caption = ""
            if pos + 1 < len(indexed):
                next_event = indexed[pos + 1][1]
                if next_event["type"] == "text" and is_caption(next_event["text"]):
                    caption = norm(next_event["text"])
                    skip_next = True
            src = f"mexico-marathon_files/{event['out']}"
            alt = caption.lstrip("▲").strip() or "墨西哥城马拉松照片"
            figcaption = f"<figcaption>{escape(caption)}</figcaption>" if caption else ""
            parts.append(f'<figure><img src="{escape(src)}" alt="{escape(alt)}" loading="lazy" decoding="async">{figcaption}</figure>')
            continue
        if is_caption(event["text"]):
            continue
        html_text = render_text(event["text"])
        if html_text:
            parts.append(html_text)
    return "\n      ".join(parts)


def caption_key(value: str) -> str:
    text = norm(value).lstrip("▲").strip()
    text = text.replace("&", " ").replace("#", " ")
    text = re.sub(r"[^0-9A-Za-z\u4e00-\u9fff]+", " ", text)
    return norm(text).lower()


def build_caption_queues(indexed):
    queues = {}
    for pos, (_, event) in enumerate(indexed):
        if event["type"] != "img" or "out" not in event:
            continue
        caption = ""
        if pos + 1 < len(indexed):
            next_event = indexed[pos + 1][1]
            if next_event["type"] == "text" and is_caption(next_event["text"]):
                caption = next_event["text"]
        key = caption_key(caption)
        if key:
            queues.setdefault(key, deque()).append(event["out"])
    return queues


def first_by_class(doc, class_name):
    expr = f'//*[contains(concat(" ", normalize-space(@class), " "), " {class_name} ")]'
    nodes = doc.xpath(expr)
    if not nodes:
        raise RuntimeError(f"Missing .{class_name}")
    return nodes[0]


def clear_children_keep_attrs(node):
    node.text = None
    for child in list(node):
        node.remove(child)


def set_inner_html(node, fragment: str):
    clear_children_keep_attrs(node)
    for child in html.fragments_fromstring(fragment):
        node.append(child)


def clean_figure(figure):
    figure.attrib.pop("class", None)
    for img in figure.xpath(".//img"):
        for attr in ("style", "width", "height"):
            img.attrib.pop(attr, None)


def normalize_media_blocks(container):
    for block in list(container.xpath('.//*[contains(concat(" ", normalize-space(@class), " "), " gallery ") or contains(concat(" ", normalize-space(@class), " "), " single ")]')):
        parent = block.getparent()
        if parent is None:
            continue
        index = parent.index(block)
        figures = list(block.xpath(".//figure"))
        for figure in figures:
            clean_figure(figure)
            parent.insert(index, figure)
            index += 1
        parent.remove(block)
    for figure in container.xpath(".//figure"):
        clean_figure(figure)


def fix_facebook_image_sources(container, caption_queues):
    for figure in container.xpath(".//figure[.//img]"):
        caption = norm(" ".join(figure.xpath(".//figcaption//text()")))
        key = caption_key(caption)
        if not key or key not in caption_queues or not caption_queues[key]:
            continue
        out_name = caption_queues[key].popleft()
        img = figure.xpath(".//img")[0]
        img.set("src", f"../stories/chinese/mexico-marathon_files/{out_name}")


def page_css() -> str:
    return """
    :root {
      --paper: #f3f6ef;
      --surface: #ffffff;
      --ink: #20242b;
      --muted: #667085;
      --line: #d5dfd0;
      --river: #2f855a;
      --brick: #2f855a;
      --gold: #b7892f;
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
      color: var(--muted);
      font-size: 14px;
      justify-content: space-between;
    }
    .story-nav a { color: inherit; text-decoration: none; border-bottom: 1px solid transparent; }
    .story-nav a:hover { border-color: currentColor; }
    .page-header { max-width: 860px; margin: 0 auto; padding: 42px 22px 24px; }
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
    .article-body .chapter { margin: 0; padding: 0; border: 0; }
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
    .article-body .section-label { color: #111827; font-size: 28px; letter-spacing: 0; text-transform: none; }
    .article-body p { margin: 0 0 17px; font-size: 17px; line-height: 1.86; }
    .article-body .kicker { margin: 0 0 14px; color: var(--muted); font-size: 14px; font-weight: 800; }
    .place { margin: -8px 0 24px; color: var(--muted); font-size: 15px; font-weight: 700; }
    .article-body figure { margin: 28px 0 30px; }
    .article-body img {
      display: block;
      width: 100%;
      max-width: 100%;
      height: auto;
      border-radius: 8px;
      background: #e1e8dc;
      box-shadow: 0 16px 40px rgba(15, 23, 42, .12);
    }
    figcaption { margin-top: 9px; color: #7a828c; font-size: 13px; line-height: 1.55; text-align: center; }
    .article-body hr { width: 72px; height: 1px; margin: 34px auto; border: 0; background: var(--line); }
    .end-mark,
    .end,
    .credits,
    .credit-line { text-align: center; color: var(--muted); }
    .page-footer { max-width: 860px; margin: 0 auto; padding: 22px 22px 48px; color: var(--muted); font-size: 13px; }
    @media (max-width: 640px) {
      .story-nav { flex-wrap: wrap; }
      .page-header { padding: 30px 18px 20px; }
      h1 { font-size: 26px; }
      .article-body { padding: 34px 18px 44px; }
      .article-body h2,
      .article-body .section-label { font-size: 24px; }
      .article-body p { font-size: 16px; }
      .article-body figure { margin-left: -2px; margin-right: -2px; }
    }
    """


def facebook_css() -> str:
    return """
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
    .breaking { background: var(--red); color: #ffffff; font-size: 13px; font-weight: 900; letter-spacing: .08em; text-transform: uppercase; }
    .breaking-inner,
    .site-head-inner,
    .article {
      width: min(1180px, calc(100% - 32px));
      margin: 0 auto;
    }
    .breaking-inner,
    .site-head-inner {
      min-height: 38px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 18px;
    }
    .breaking a,
    .section-nav a { color: inherit; text-decoration: none; }
    .site-head { border-bottom: 1px solid var(--line); background: #ffffff; }
    .site-head-inner { min-height: 68px; }
    .wordmark { color: var(--red); font-size: 30px; line-height: 1; font-weight: 950; letter-spacing: 0; text-decoration: none; }
    .section-nav { display: flex; flex-wrap: wrap; justify-content: flex-end; gap: 14px; color: #333333; font-size: 13px; font-weight: 800; text-transform: uppercase; }
    .hero { padding: 34px 0 26px; border-bottom: 1px solid var(--line); }
    .label { display: inline-flex; align-items: center; min-height: 28px; padding: 4px 9px; background: var(--red); color: #ffffff; font-size: 12px; font-weight: 900; letter-spacing: .08em; text-transform: uppercase; }
    h1 { max-width: 980px; margin: 18px 0 14px; font-size: clamp(2.45rem, 7vw, 5.5rem); line-height: .94; letter-spacing: 0; }
    .dek { max-width: 820px; margin: 0; color: #333333; font-size: clamp(1.08rem, 2vw, 1.32rem); line-height: 1.55; }
    .byline { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 18px; color: var(--muted); font-size: 13px; font-weight: 800; text-transform: uppercase; }
    .byline span,
    .byline a { min-height: 30px; display: inline-flex; align-items: center; padding: 4px 9px; background: var(--soft); text-decoration: none; }
    .lead-media { margin: 26px 0 0; border-top: 6px solid var(--red); }
    .lead-media img { display: block; width: 100%; aspect-ratio: 1200 / 630; object-fit: cover; background: var(--soft); }
    figcaption { margin-top: 8px; color: var(--muted); font-size: 12px; line-height: 1.4; }
    .story-grid { display: grid; grid-template-columns: minmax(220px, 300px) minmax(0, 720px); gap: 34px; align-items: start; padding: 34px 0 12px; }
    .rail { position: sticky; top: 16px; display: grid; gap: 18px; }
    .brief-box { border-top: 5px solid var(--red); background: var(--soft); padding: 16px; }
    .brief-box h2 { margin: 0 0 12px; font-size: 19px; line-height: 1.1; }
    .brief-box dl { margin: 0; display: grid; gap: 12px; }
    .brief-box dt { color: var(--red); font-size: 11px; font-weight: 900; letter-spacing: .08em; text-transform: uppercase; }
    .brief-box dd { margin: 2px 0 0; color: #222222; font-size: 14px; line-height: 1.45; }
    .share-note { border: 1px solid var(--line); padding: 14px; color: #333333; font-size: 13px; line-height: 1.55; }
    .share-note strong { display: block; margin-bottom: 5px; color: var(--ink); font-size: 12px; letter-spacing: .08em; text-transform: uppercase; }
    .copy { min-width: 0; }
    .copy p { margin: 0 0 19px; font-family: Georgia, "Times New Roman", serif; font-size: 19px; line-height: 1.72; }
    .copy h2 { margin: 36px 0 16px; padding-top: 20px; border-top: 1px solid var(--line); font-size: 30px; line-height: 1.1; letter-spacing: 0; }
    .copy .kicker { margin: 0 0 12px; color: var(--red); font-family: Arial, Helvetica, sans-serif; font-size: 13px; font-weight: 900; letter-spacing: .08em; text-transform: uppercase; }
    .copy .loc { color: var(--red); }
    .copy figure { margin: 25px 0 30px; }
    .copy figure img { display: block; width: 100%; height: auto; border: 1px solid var(--line); background: var(--soft); }
    .copy hr { width: 74px; height: 5px; margin: 34px 0; border: 0; background: var(--red); }
    .end,
    .credits,
    .credit-line { text-align: center; color: var(--muted); }
    .zz-engagement { max-width: 1180px; padding-left: 0; padding-right: 0; }
    .zz-engagement-kicker,
    .zz-engagement h2 { color: var(--red); }
    @media (max-width: 860px) {
      .site-head-inner { align-items: flex-start; flex-direction: column; padding: 16px 0; }
      .section-nav { justify-content: flex-start; }
      .story-grid { grid-template-columns: 1fr; }
      .rail { position: static; }
    }
    """


def replace_first_style(doc, css: str):
    styles = doc.xpath("//style")
    if not styles:
        raise RuntimeError("No inline style block found")
    styles[0].text = css


def serialize_doc(doc) -> str:
    text = "<!doctype html>\n" + html.tostring(doc, encoding="unicode", method="html")
    return re.sub(r"[ \t]+\n", "\n", text).rstrip() + "\n"


def load_doc(path: Path):
    return html.fromstring(path.read_text(encoding="utf-8"))


def write_doc(path: Path, doc):
    text = serialize_doc(doc)
    path.write_text(text, encoding="utf-8", newline="\n")


def update_normal_pages(zh_article: str):
    zh_path = REPO / "run50" / "stories" / "chinese" / f"{SLUG}.html"
    zh_doc = load_doc(zh_path)
    replace_first_style(zh_doc, page_css())
    set_inner_html(first_by_class(zh_doc, "article-body"), zh_article)
    write_doc(zh_path, zh_doc)

    en_path = REPO / "run50" / "stories" / "english" / f"{SLUG}.html"
    en_doc = load_doc(en_path)
    replace_first_style(en_doc, page_css())
    en_body = first_by_class(en_doc, "article-body")
    normalize_media_blocks(en_body)
    write_doc(en_path, en_doc)


def update_facebook_page(caption_queues):
    fb_path = REPO / "run50" / "facebook" / f"{SLUG}.html"
    fb_doc = load_doc(fb_path)
    replace_first_style(fb_doc, facebook_css())
    full_story = first_by_class(fb_doc, "full-story")
    fix_facebook_image_sources(full_story, caption_queues)
    normalize_media_blocks(full_story)
    write_doc(fb_path, fb_doc)


def font(size, bold=False):
    fonts = [
        "arialbd.ttf" if bold else "arial.ttf",
        "seguisb.ttf" if bold else "segoeui.ttf",
        "calibrib.ttf" if bold else "calibri.ttf",
    ]
    for name in fonts:
        path = Path("C:/Windows/Fonts") / name
        if path.exists():
            return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default()


def write_mexico_cover():
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 750" role="img" aria-labelledby="title desc">
<title id="title">Mexico City icon cover</title>
<desc id="desc">Icon style cover with Mexico City title, subtitle, fixed RunWorld badge, Aztec pyramid, Angel of Independence, cactus, sun and highland scenery.</desc>
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
    (REPO / "assets" / "thumb-run50-mexico-icons.svg").write_text(svg, encoding="utf-8", newline="\n")

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
    image.save(REPO / "assets" / "og-run50-mexico-icons.png", "PNG")


def update_versions():
    index_files = [
        REPO / "index.html",
        REPO / "run50" / "facebook" / "index.html",
        REPO / "run50" / "stories" / "chinese" / "index.html",
        REPO / "run50" / "stories" / "english" / "index.html",
    ]
    for path in index_files:
        original = path.read_text(encoding="utf-8")
        text = original
        for slug in ("miami", "pisa", "mexico"):
            text = re.sub(
                rf"thumb-run50-{slug}-icons\.svg\?v=[0-9A-Za-z-]+",
                f"thumb-run50-{slug}-icons.svg?v={VERSION}",
                text,
            )
        if text != original:
            path.write_text(text, encoding="utf-8", newline="\n")

    story_files = []
    for slug in ("miami", "pisa", "mexico"):
        story_files.extend([
            REPO / "run50" / "stories" / "chinese" / f"{slug}-marathon.html",
            REPO / "run50" / "stories" / "english" / f"{slug}-marathon.html",
            REPO / "run50" / "facebook" / f"{slug}-marathon.html",
        ])
    for path in story_files:
        original = path.read_text(encoding="utf-8")
        text = original
        for slug in ("miami", "pisa", "mexico"):
            absolute = f"{SITE}/assets/og-run50-{slug}-icons.png"
            text = re.sub(re.escape(absolute) + r"(?:\?v=[0-9A-Za-z-]+)?", f"{absolute}?v={VERSION}", text)
            text = re.sub(
                rf"(\.\./(?:\.\./)?assets/og-run50-{slug}-icons\.png)(?:\?v=[0-9A-Za-z-]+)?",
                rf"\1?v={VERSION}",
                text,
            )
        if text != original:
            path.write_text(text, encoding="utf-8", newline="\n")


def main():
    indexed = extract_story_events()
    image_count = copy_story_images(indexed)
    zh_article = render_chinese_article(indexed)
    caption_queues = build_caption_queues(indexed)
    update_normal_pages(zh_article)
    update_facebook_page(caption_queues)
    write_mexico_cover()
    update_versions()
    print(f"rebuilt Mexico from source: events={len(indexed)} images={image_count}")


if __name__ == "__main__":
    main()
