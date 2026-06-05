from pathlib import Path
from lxml import html
from html import escape
from PIL import Image, ImageDraw, ImageFont, ImageOps
import math
import re

REPO = Path(__file__).resolve().parents[1]
SOURCE_BASE = Path(r"Z:\ZhennanZ Folder\000-Marathon-Story-2024-2025\20230000-Marathons\2023-State-14-TX")
SOURCE_HTML = next(p for p in SOURCE_BASE.iterdir() if p.suffix.lower() == ".html")
SOURCE_FILES = next(p for p in SOURCE_BASE.iterdir() if p.is_dir() and p.name.endswith("_files"))
SITE = "https://arsenanzz.github.io/ZZ"
SLUG = "san-antonio-marathon"
VERSION = "20260605-1"
ENGAGEMENT_VERSION = "20260605"
OUT_IMG_DIR = REPO / "run50" / "stories" / "chinese" / "Run50-San-Antonio-Marathon-clean_files"
OG_PATH = REPO / "assets" / "og-run50-san-antonio-marathon-icons.png"
THUMB_PATH = REPO / "assets" / "thumb-run50-san-antonio-marathon-icons.svg"

TITLE_ZH = "Run50 #第14州｜德克萨斯：圣安东尼奥摇滚马拉松｜没有马刺，也没有文班亚马"
TITLE_EN = "Run50 #14 | Texas: San Antonio Rock 'n' Roll Marathon"
TITLE_FB = "I went to San Antonio for the Spurs and ended up running Texas"
DATE_ZH = "2023.12.03"
DATE_EN = "Dec 3, 2023"
RACE_NAME = "Rock 'n' Roll San Antonio Marathon"


def norm(value: str) -> str:
    return re.sub(r"\s+", " ", value.replace("\xa0", " ")).strip()


def is_styleish(value: str) -> bool:
    return ":host {" in value or "--weui-" in value or len(value) > 1200


def has_desc_leaf_container(el) -> bool:
    for desc in el.iterdescendants():
        if desc.tag in ("p", "section"):
            text = norm("".join(desc.itertext()))
            if text and not is_styleish(text):
                return True
    return False


def is_caption(text: str) -> bool:
    return text.startswith("▲")


def should_skip_text(text: str) -> bool:
    return text in {"★", "★★", "★★★", "★★★★", "\u200d"} or not text.strip("\u200d").strip()


def extract_story():
    source = SOURCE_HTML.read_text(encoding="utf-8", errors="replace")
    doc = html.fromstring(source)
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

    start = 0
    for pos, (_, event) in enumerate(clean):
        if event["type"] == "text" and event["text"] == "前言":
            start = pos
            break
    end = len(clean)
    for pos, (_, event) in enumerate(clean):
        if event["type"] == "text" and event["text"].startswith("设计"):
            end = pos + 1
            break
    return clean[start:end]


def local_source_path(src: str) -> Path:
    normalized = src[2:] if src.startswith("./") else src
    return SOURCE_BASE / normalized


def copy_story_images(indexed):
    OUT_IMG_DIR.mkdir(parents=True, exist_ok=True)
    image_total = sum(1 for _, event in indexed if event["type"] == "img")
    existing = sorted(OUT_IMG_DIR.glob("img-*.webp"))
    if len(existing) == image_total:
        count = 0
        for _, event in indexed:
            if event["type"] != "img":
                continue
            count += 1
            event["out"] = f"img-{count:03d}.webp"
        return count

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
            im.save(OUT_IMG_DIR / out_name, "WEBP", quality=88, method=4)
        event["out"] = out_name
    return count


def clean_caption(text: str) -> str:
    caption = text.lstrip("▲").strip()
    replacements = {
        "Offical": "Official",
        "Bulding": "Building",
        "Kng": "King",
        "Rock'n Roll": "Rock 'n' Roll",
        "Rock'n' Roll": "Rock 'n' Roll",
        "Rock 'n' Roll Start": "Rock 'n' Roll Start",
        "Qingting": "Dragonfly",
        "India Food": "Indian Food",
        "Korea Food": "Korean Food",
        "Paopao": "Bubbles",
    }
    for old, new in replacements.items():
        caption = caption.replace(old, new)
    return caption


def figure_html(src: str, caption: str, alt_base: str) -> str:
    alt = caption or alt_base
    figcaption = f"<figcaption>{escape(caption)}</figcaption>" if caption else ""
    return f'<figure><img src="{escape(src)}" alt="{escape(alt)}" loading="lazy" decoding="async">{figcaption}</figure>'


def render_figures(indexed, img_prefix: str, alt_base: str) -> str:
    parts = []
    pending_caption = ""
    for _, event in indexed:
        if event["type"] == "text":
            if is_caption(event["text"]):
                pending_caption = clean_caption(event["text"])
            continue
        if event["type"] == "img":
            parts.append(figure_html(img_prefix + event["out"], pending_caption, alt_base))
            pending_caption = ""
    return "\n      ".join(parts)


def render_zh_text(idx: int, text: str) -> str:
    if should_skip_text(text) or is_caption(text):
        return ""
    if text in ("前言", "后记"):
        return f'<h2 class="section-label">{escape(text)}</h2>'
    if text.startswith("# "):
        return f"<h2>{escape(text[2:])}</h2>"
    if text.startswith("## "):
        return f"<h3>{escape(text[3:])}</h3>"
    if text.startswith(("🏀", "📍", "🎽")):
        return f'<p class="place">{escape(text)}</p>'
    if text.startswith("- "):
        return f'<p class="end-mark">{escape(text)}</p>'
    if text.startswith(("文字", "摄影", "设计")):
        return f'<p class="credit-line">{escape(text)}</p>'
    return f"<p>{escape(text)}</p>"


def render_chinese_article(indexed):
    parts = []
    pending_caption = ""
    for idx, event in indexed:
        if event["type"] == "text":
            if is_caption(event["text"]):
                pending_caption = clean_caption(event["text"])
                continue
            html_text = render_zh_text(idx, event["text"])
            if html_text:
                parts.append(html_text)
            continue
        if event["type"] == "img":
            parts.append(figure_html("Run50-San-Antonio-Marathon-clean_files/" + event["out"], pending_caption, "圣安东尼奥摇滚马拉松照片"))
            pending_caption = ""
    return "\n      ".join(parts)


def find_pos(indexed, needle: str) -> int:
    for pos, (_, event) in enumerate(indexed):
        if event["type"] == "text" and event["text"] == needle:
            return pos
    raise RuntimeError(f"Could not find section marker: {needle}")


def split_sections(indexed):
    city = find_pos(indexed, "# 圣安东尼奥：墨味儿十足")
    race = find_pos(indexed, "# 圣安东尼奥：「25周年」摇滚马拉松")
    post = find_pos(indexed, "后记")
    return {
        "foreword": indexed[:city],
        "city": indexed[city:race],
        "race": indexed[race:post],
        "post": indexed[post:],
    }


ENGLISH_COPY = {
    "foreword": (
        "Preface: the Spurs trip that became a marathon",
        "Texas · San Antonio",
        [
            "The whole idea started with basketball. I have been a Spurs fan for years, the Ginobili-Parker-Duncan era kind of Spurs: calm, stubborn, disciplined, and somehow a little magical.",
            "When San Antonio landed the No. 1 pick and Victor Wembanyama arrived, I figured I should go see this living alien in person. And if there happened to be a marathon in town, even better.",
            "The joke, of course, was that the Spurs were away during marathon weekend. No Wemby, no live Spurs game. But we still got a terrific Rock 'n' Roll marathon and a deeply Mexican-flavored San Antonio weekend. State 14 was checked off after all.",
        ],
    ),
    "city": (
        "State 14: Texas, the Alamo, and San Antonio's Mexican soul",
        "Texas · San Antonio",
        [
            "San Antonio is not just a Spurs city. It is one of the most distinctive travel cities in the United States, shaped by Spanish missions, Mexican culture, Indigenous history, Texas independence, and that soft water-city romance around the River Walk.",
            "The Alamo gives the place its Texas mythology. The phrase 'Remember the Alamo' still sits at the center of how the Lone Star story is told, and standing there downtown makes the history feel less like a textbook and more like a street corner.",
            "But what I loved more was how San Antonio never really let go of its Mexican texture: music, food, lights, colors, churches, the River Walk, the Main Plaza projection show, and that easy mix of tourist bustle and local life.",
            "We flew in through Dallas under a huge Texas sunset, walked into the Alamo almost by accident, ate by the river, watched The Saga light up San Fernando Cathedral, took photos on Arsenal Bridge, climbed toward the Tower of the Americas, and eventually picked up our race gear.",
            "So if the article needed a Texas introduction, San Antonio already wrote one for us: Lone Star history on one side, Mexican warmth on the other, and a river running right through the middle.",
        ],
    ),
    "race": (
        "Race day: bands, Fort Sam Houston, greenways, and one brutal late hill",
        "Rock 'n' Roll San Antonio Marathon · Dec 3, 2023",
        [
            "The race started at 7 a.m. near San Antonio City Hall. Because I was in a later corral, I crossed the start closer to 7:20, just as the sky was finally brightening and the DJ was waking everyone up properly.",
            "The first miles felt exactly like a happy city run. We rolled through downtown, onto Broadway, into Brackenridge Park, past murals, costumes, live bands, Santa sightings, Mexican dance performances, and a surprising number of little street moments that made the Rock 'n' Roll name feel earned.",
            "Around Mile 5, the course entered Joint Base San Antonio-Fort Sam Houston. Running through a U.S. military base, past aircraft, armored vehicles, old theater buildings, and uniformed volunteers, was one of those odd marathon-only experiences I never would have planned on my own.",
            "After the half/full split, the course changed tone. The second half moved through Lincoln Park, Salado Creek Greenway, Martin Luther King Park, Covington Park, and Southside Lions Park. It was greener and quieter, with bands and volunteers still keeping the road alive.",
            "Then Texas reminded me it had hills. From roughly Mile 20 to Mile 25, there was a long exposed climb under stronger sun, with grades that felt rude for that stage of a marathon. I let go of the sub-four idea and switched into survival mode.",
            "The Tower of the Americas eventually came back into view, the crowd thickened, and I crossed the line in 4 hours and 12 minutes. Not the cleanest finish, but for State 14 and the final marathon of 2023, it felt just right.",
            "The medal carried the bright colors of Mexican Jarabe dance, and the post-race area turned into a small music-and-medal picnic. We ate Korean food, visited the McNay Art Museum with the medal, and somehow made the whole day feel like one long San Antonio afterparty.",
        ],
    ),
    "post": (
        "Postscript: closing out 2023 with State 14",
        "Texas sky · 2023 finale",
        [
            "On the flight home, the Texas sky shifted from orange to deep blue, which felt like the right closing image for the year.",
            "This was our final marathon of 2023, and our tenth marathon of the year. Ten races, papers, PhD work, early mornings, new habits, a lot of alien documentaries, and a slowly clearer sense that I was finally getting the hang of things.",
            "State 14, Texas: San Antonio Rock 'n' Roll Marathon. No Spurs game, no Wembanyama sighting, but a full Texas story anyway.",
        ],
    ),
}


def render_english_article(sections, img_prefix: str) -> str:
    parts = []
    for key in ("foreword", "city", "race", "post"):
        title, place, paragraphs = ENGLISH_COPY[key]
        parts.append(f"<h2>{escape(title)}</h2>")
        parts.append(f'<p class="place">{escape(place)}</p>')
        for paragraph in paragraphs:
            parts.append(f"<p>{escape(paragraph)}</p>")
        figures = render_figures(sections[key], img_prefix, "San Antonio Marathon photo")
        if figures:
            parts.append(figures)
    return "\n      ".join(parts)


def render_facebook_article(sections):
    story_prefix = "../stories/chinese/Run50-San-Antonio-Marathon-clean_files/"
    parts = [
        "<h2>The race first: San Antonio made the Rock 'n' Roll label feel literal</h2>",
        "<p>Race date: Dec 3, 2023. State 14 of Run50 came at the end of a long year, on a San Antonio course that mixed downtown blocks, live bands, Fort Sam Houston, greenway miles, and one very badly timed hill in the Texas sun.</p>",
        "<p>I started near City Hall in a later corral, ran the early miles in a Ginobili Spurs jersey, crossed through a military base, then spent the last stretch bargaining with a long climb before finishing in 4:12.</p>",
        render_figures(sections["race"], story_prefix, "Rock 'n' Roll San Antonio Marathon photo"),
        "<h2>Why San Antonio in the first place</h2>",
        "<p>The trip began as a Spurs idea. I wanted to see Victor Wembanyama after San Antonio drafted him No. 1, but the team happened to be on the road during marathon weekend. So the basketball plan quietly turned into a city-and-marathon trip.</p>",
        render_figures(sections["foreword"], story_prefix, "Spurs and San Antonio marathon photo"),
        "<h2>The Texas story around the race</h2>",
        "<p>San Antonio gave the weekend its real shape: the Alamo, the Lone Star mythology, the River Walk, Mexican music and food, Main Plaza's projection show, the Tower of the Americas, and that easy December tourist glow along the river.</p>",
        "<p>If Texas needed an introduction, this city had plenty of it: old Spanish missions, Mexican warmth, a river under the streets, and a marathon route that stitched the pieces together.</p>",
        render_figures(sections["city"], story_prefix, "San Antonio city photo"),
        "<h2>After the finish</h2>",
        "<p>The medal was bright and festive, built around Mexican Jarabe dance colors. We ate, stretched, took medal photos at the McNay Art Museum, then flew home under a Texas sky that felt like the closing credits for 2023.</p>",
        render_figures(sections["post"], story_prefix, "Texas post-race photo"),
    ]
    return "\n      ".join(part for part in parts if part)


def page_css() -> str:
    return """
    :root {
      --paper: #edf3f7;
      --surface: #ffffff;
      --ink: #20242b;
      --muted: #667085;
      --line: #d0dfe8;
      --river: #0b67c2;
      --brick: #9f3a2d;
      --gold: #b7892f;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      background: linear-gradient(180deg, #eef5f6 0, var(--paper) 320px);
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
    .kicker { margin: 0 0 14px; color: var(--river); font-size: 14px; font-weight: 850; }
    h1 {
      margin: 0;
      max-width: 820px;
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
    .meta span {
      display: inline-flex;
      align-items: center;
      min-height: 30px;
      padding: 3px 10px;
      border: 1px solid var(--line);
      border-radius: 999px;
      background: rgba(255, 255, 255, .72);
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
    .article-body h2:not(:first-child) { margin-top: 54px; }
    .article-body h2::before {
      content: "";
      width: 34px;
      height: 3px;
      border-radius: 999px;
      background: var(--gold);
      flex: 0 0 auto;
    }
    .article-body h3 { margin: 36px 0 16px; color: #111827; font-size: 22px; line-height: 1.3; font-weight: 800; }
    .article-body .section-label { color: #111827; font-size: 28px; letter-spacing: 0; text-transform: none; }
    .article-body p { margin: 0 0 17px; font-size: 17px; line-height: 1.86; }
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
    .end-mark, .credit-line { text-align: center; color: var(--muted); }
    .page-footer { max-width: 860px; margin: 0 auto; padding: 0 22px 44px; color: var(--muted); text-align: center; font-size: 14px; }
    @media (max-width: 640px) {
      .story-nav { flex-wrap: wrap; }
      .page-header { padding: 30px 18px 20px; }
      h1 { font-size: 26px; }
      .article-body { padding: 34px 18px 44px; }
      .article-body h2, .article-body .section-label { font-size: 24px; }
      .article-body p { font-size: 16px; }
      .article-body figure { margin-left: -2px; margin-right: -2px; }
    }
    """


def facebook_css() -> str:
    return """
    :root {
      --blue: #0b67c2;
      --ink: #111111;
      --muted: #666666;
      --line: #dddddd;
      --soft: #f0f4f8;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      color: var(--ink);
      background: #ffffff;
      font-family: Arial, Helvetica, sans-serif;
      letter-spacing: 0;
    }
    .topbar {
      background: var(--blue);
      color: #ffffff;
      min-height: 38px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      padding: 8px 18px;
      font-size: 13px;
      font-weight: 800;
      letter-spacing: .08em;
      text-transform: uppercase;
    }
    .brand {
      padding: 18px;
      border-bottom: 1px solid var(--line);
    }
    .brand h1 {
      margin: 0 0 14px;
      color: var(--blue);
      font-size: clamp(30px, 6vw, 54px);
      line-height: .96;
      letter-spacing: 0;
      text-transform: uppercase;
    }
    .brand nav { display: flex; flex-wrap: wrap; gap: 18px; font-size: 13px; font-weight: 800; text-transform: uppercase; }
    .brand a { color: #222222; text-decoration: none; }
    main { max-width: 1060px; margin: 0 auto; padding: 34px 18px 60px; }
    .label {
      display: inline-block;
      margin: 0 0 18px;
      padding: 7px 10px;
      background: var(--blue);
      color: #ffffff;
      font-size: 13px;
      font-weight: 900;
      letter-spacing: .08em;
      text-transform: uppercase;
    }
    .headline {
      max-width: 900px;
      margin: 0;
      font-size: clamp(38px, 7vw, 72px);
      line-height: .95;
      letter-spacing: 0;
      font-weight: 900;
    }
    .standfirst {
      max-width: 820px;
      margin: 18px 0 22px;
      color: #333333;
      font-size: 20px;
      line-height: 1.45;
    }
    .byline { display: flex; flex-wrap: wrap; gap: 8px; margin: 22px 0 34px; color: #444444; font-size: 13px; font-weight: 900; text-transform: uppercase; }
    .byline span { background: #f1f1f1; padding: 8px 10px; }
    .lead-media { margin: 0 0 32px; border-top: 8px solid var(--blue); }
    .lead-media img { display: block; width: 100%; height: auto; }
    .lead-media figcaption { margin-top: 8px; color: var(--muted); font-size: 13px; }
    .brief {
      margin: 0 0 34px;
      padding: 20px 22px;
      background: var(--soft);
      border-top: 6px solid var(--blue);
      display: grid;
      grid-template-columns: 160px 1fr;
      gap: 10px 18px;
      color: #222222;
      font-size: 15px;
      line-height: 1.5;
    }
    .brief strong { color: var(--blue); font-size: 12px; text-transform: uppercase; letter-spacing: .08em; }
    .story {
      max-width: 820px;
      margin: 0 auto;
      font-family: Georgia, "Times New Roman", serif;
      font-size: 19px;
      line-height: 1.7;
    }
    .story h2 {
      margin: 44px 0 16px;
      font-family: Arial, Helvetica, sans-serif;
      font-size: clamp(26px, 4vw, 42px);
      line-height: 1.08;
      letter-spacing: 0;
    }
    .story p { margin: 0 0 18px; }
    .story figure { margin: 28px 0 32px; }
    .story img { display: block; width: 100%; height: auto; }
    .story figcaption { margin-top: 7px; color: var(--muted); font-family: Arial, Helvetica, sans-serif; font-size: 12px; line-height: 1.45; }
    @media (max-width: 700px) {
      .topbar { align-items: flex-start; flex-direction: column; }
      .brief { grid-template-columns: 1fr; }
      main { padding-top: 26px; }
    }
    """


def engagement_block(locale: str, page_key: str, comment_id: str, rel: str) -> str:
    if locale == "zh-CN":
        kicker = "留言 / 阅读"
        heading = "跑完以后，说两句"
        note = "不用登录也可以留言。新留言会直接显示。"
        views = "阅读"
        loading = "评论加载中..."
    else:
        kicker = "Comments / Views"
        heading = "Say something after the run"
        note = "No account is needed to submit a comment. New comments appear right away."
        views = "Views"
        loading = "Loading comments..."
    return f"""
    <section class="zz-engagement" data-zz-engagement data-locale="{locale}" data-page-key="{page_key}">
      <div class="zz-engagement-shell">
        <div>
          <p class="zz-engagement-kicker">{kicker}</p>
          <h2>{heading}</h2>
          <p class="zz-engagement-note">{note}</p>
          <div class="zz-engagement-stats">
            <span class="zz-engagement-stat" id="busuanzi_container_page_pv">
              <span>{views}</span>
              <strong id="busuanzi_value_page_pv" data-zz-view-count>--</strong>
            </span>
          </div>
        </div>
        <div class="zz-engagement-card">
          <div id="{comment_id}" data-zz-supabase-comments></div>
          <p class="zz-engagement-status" data-zz-engagement-status>{loading}</p>
        </div>
      </div>
    </section>
    <script src="{rel}/zz-engagement-config.js?v={ENGAGEMENT_VERSION}"></script>
    <script src="{rel}/zz-engagement.js?v={ENGAGEMENT_VERSION}"></script>
    """


def story_page(lang: str, article: str) -> str:
    is_zh = lang == "zh"
    title = TITLE_ZH if is_zh else TITLE_EN
    html_lang = "zh-CN" if is_zh else "en"
    kicker = "Run50 Stories · Texas" if not is_zh else "Run50 Stories · 德克萨斯"
    dek = (
        "这是 Run50 的第14州，也是2023年的收官马拉松：从马刺和文班亚马的念头出发，最后在圣安东尼奥跑过阿拉莫、河畔步道、Fort Sam Houston、绿道和一段德州热坡。"
        if is_zh
        else "State 14 of Run50 and the 2023 season finale: a Spurs-inspired trip to San Antonio, an Alamo/River Walk weekend, and a 4:12 marathon through Fort Sam Houston, park greenways, music blocks, and a late Texas hill."
    )
    nav = (
        '<a href="./index.html">← 中文故事</a><a href="../english/san-antonio-marathon.html">English</a><a href="../../facebook/san-antonio-marathon.html">Facebook</a><a href="../../index.html">Run50</a>'
        if is_zh
        else '<a href="./index.html">← English Stories</a><a href="../chinese/san-antonio-marathon.html">中文</a><a href="../../facebook/san-antonio-marathon.html">Facebook</a><a href="../../index.html">Run50</a>'
    )
    meta = (
        '<span>圣安东尼奥</span><span>2023.12.03</span><span>Run50 #14</span><span>4小时12分</span>'
        if is_zh
        else '<span>San Antonio, Texas</span><span>Dec 3, 2023</span><span>Run50 #14</span><span>4:12 finish</span>'
    )
    page_key = f"run50-{SLUG}-zh" if is_zh else f"run50-{SLUG}-en"
    comment_id = "supabase-comments-san-antonio-zh" if is_zh else "supabase-comments-san-antonio-en"
    return f"""<!DOCTYPE html>
<html lang="{html_lang}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{escape(title)}</title>
  <meta name="description" content="{escape(dek)}">
  <meta property="og:type" content="article">
  <meta property="og:title" content="{escape(title)}">
  <meta property="og:description" content="{escape(dek)}">
  <meta property="og:image" content="{SITE}/assets/og-run50-san-antonio-marathon-icons.png?v={VERSION}">
  <meta property="og:url" content="{SITE}/run50/stories/{'chinese' if is_zh else 'english'}/san-antonio-marathon.html">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:image" content="{SITE}/assets/og-run50-san-antonio-marathon-icons.png?v={VERSION}">
  <link rel="stylesheet" href="../../../assets/zz-engagement.css?v={ENGAGEMENT_VERSION}">
  <style>{page_css()}</style>
</head>
<body>
  <nav class="story-nav">{nav}</nav>
  <header class="page-header">
    <p class="kicker">{escape(kicker)}</p>
    <h1>{escape(title)}</h1>
    <div class="meta">{meta}</div>
    <p class="dek">{escape(dek)}</p>
  </header>
  <main class="article-shell">
    <article class="article-body">
      {article}
    </article>
    {engagement_block('zh-CN' if is_zh else 'en', page_key, comment_id, '../../../assets')}
  </main>
  <footer class="page-footer">Run50 · Texas · San Antonio Rock 'n' Roll Marathon</footer>
</body>
</html>
"""


def facebook_page(article: str) -> str:
    standfirst = "Race date: Dec 3, 2023. State 14 of Run50: San Antonio, a Spurs-inspired trip, a Rock 'n' Roll course through Fort Sam Houston and greenways, and a 4:12 finish under the Texas sun."
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>San Antonio Marathon | Run50 Facebook</title>
  <meta name="description" content="{escape(standfirst)}">
  <meta property="og:type" content="article">
  <meta property="og:title" content="{escape(TITLE_FB)}">
  <meta property="og:description" content="{escape(standfirst)}">
  <meta property="og:image" content="{SITE}/assets/og-run50-san-antonio-marathon-icons.png?v={VERSION}">
  <meta property="og:url" content="{SITE}/run50/facebook/san-antonio-marathon.html">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:image" content="{SITE}/assets/og-run50-san-antonio-marathon-icons.png?v={VERSION}">
  <link rel="stylesheet" href="../../assets/zz-engagement.css?v={ENGAGEMENT_VERSION}">
  <style>{facebook_css()}</style>
</head>
<body>
  <div class="topbar"><span>Run50 Facebook</span><span>Race date: Dec 3, 2023</span></div>
  <header class="brand">
    <h1>Run50 USA</h1>
    <nav>
      <a href="../index.html">Run50</a>
      <a href="../stories/english/san-antonio-marathon.html">Full English Story</a>
      <a href="../stories/chinese/san-antonio-marathon.html">Chinese Original</a>
    </nav>
  </header>
  <main>
    <p class="label">USA / Texas / Marathon</p>
    <h1 class="headline">{escape(TITLE_FB)}</h1>
    <p class="standfirst">{escape(standfirst)}</p>
    <div class="byline"><span>By Arsenan</span><span>Run50 #14</span><span>San Antonio, Texas</span><span>4:12 finish</span></div>
    <figure class="lead-media">
      <img src="../../assets/og-run50-san-antonio-marathon-icons.png?v={VERSION}" alt="San Antonio icon cover with Alamo, River Walk, Tower of the Americas, guitar, and Run50 Texas badge">
      <figcaption>San Antonio icon cover with the Alamo, River Walk, Tower of the Americas, rock music and Run50 Texas badge.</figcaption>
    </figure>
    <section class="brief" aria-label="At a glance">
      <strong>Race</strong><span>Rock 'n' Roll San Antonio Marathon, State 14 of Run50.</span>
      <strong>Course</strong><span>City Hall start, Broadway, Brackenridge Park, Fort Sam Houston, Salado Creek Greenway, Hemisfair finish.</span>
      <strong>Result</strong><span>4 hours 12 minutes, after a late exposed Texas climb.</span>
      <strong>Why Texas</strong><span>A Spurs/Wembanyama idea that became an Alamo, River Walk and marathon weekend.</span>
    </section>
    <article class="story">
      {article}
    </article>
    {engagement_block('en', f'run50-{SLUG}-facebook-en', 'supabase-comments-san-antonio-facebook', '../../assets')}
  </main>
</body>
</html>
"""


def write_clean(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    cleaned = "\n".join(line.rstrip() for line in text.strip().splitlines()) + "\n"
    path.write_text(cleaned, encoding="utf-8")


def load_font(size: int, bold: bool = True):
    candidates = [
        r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\segoeuib.ttf" if bold else r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\calibrib.ttf" if bold else r"C:\Windows\Fonts\calibri.ttf",
    ]
    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default()


def fit_font(draw, text: str, max_width: int, start_size: int, min_size: int, bold: bool = True):
    size = start_size
    while size >= min_size:
        font = load_font(size, bold)
        bbox = draw.textbbox((0, 0), text, font=font)
        if bbox[2] - bbox[0] <= max_width:
            return font
        size -= 2
    return load_font(min_size, bold)


def draw_cover(draw, scale: float = 1.0):
    def s(v):
        return int(round(v * scale))

    ink = "#20242b"
    blue = "#0b67c2"
    muted = "#667085"
    river = "#2f8fa3"
    clay = "#ba4a2b"
    tan = "#d7b98b"
    gold = "#f5b32f"
    green = "#5a8f67"

    title_font = load_font(s(66), True)
    subtitle_font = load_font(s(26), True)
    badge_font = load_font(s(40), True)
    badge_city_font = fit_font(draw, "TEXAS", s(302), s(54), s(38), True)

    draw.text((s(64), s(56)), "SAN ANTONIO", font=title_font, fill=ink)
    draw.text((s(66), s(136)), "ALAMO, RIVER WALK, ROCK'N'ROLL", font=subtitle_font, fill=muted)

    draw.rounded_rectangle([s(760), s(64), s(1122), s(228)], radius=s(22), fill="#ffffff", outline=ink, width=s(7))
    draw.text((s(790), s(92)), "Run50 #14", font=badge_font, fill=ink)
    draw.text((s(790), s(144)), "TEXAS", font=badge_city_font, fill=blue)

    # River Walk bands.
    draw.polygon([(s(0), s(505)), (s(160), s(468)), (s(350), s(490)), (s(520), s(458)), (s(760), s(485)), (s(1200), s(438)), (s(1200), s(630)), (s(0), s(630))], fill="#b8d0c3")
    draw.polygon([(s(0), s(550)), (s(170), s(522)), (s(355), s(540)), (s(590), s(515)), (s(790), s(545)), (s(1200), s(498)), (s(1200), s(630)), (s(0), s(630))], fill="#7aa782")
    draw.polygon([(s(0), s(590)), (s(230), s(555)), (s(470), s(578)), (s(710), s(548)), (s(1200), s(582)), (s(1200), s(630)), (s(0), s(630))], fill=river)
    draw.line([(s(20), s(580)), (s(230), s(546)), (s(470), s(568)), (s(710), s(538)), (s(1180), s(570))], fill="#ffffff", width=s(5))

    # Alamo facade.
    draw.rectangle([s(95), s(392), s(360), s(552)], fill=clay)
    draw.rectangle([s(72), s(360), s(384), s(402)], fill="#8d2f26")
    draw.rectangle([s(115), s(312), s(190), s(360)], fill=clay)
    draw.rectangle([s(266), s(312), s(340), s(360)], fill=clay)
    draw.rectangle([s(132), s(430), s(175), s(552)], fill="#f7efe1")
    draw.rectangle([s(282), s(430), s(322), s(552)], fill="#f7efe1")
    draw.arc([s(198), s(410), s(266), s(548)], 180, 360, fill="#f7efe1", width=s(16))
    draw.rectangle([s(206), s(478), s(258), s(552)], fill="#f7efe1")
    draw.rectangle([s(115), s(312), s(190), s(344)], fill=tan)
    draw.rectangle([s(266), s(312), s(340), s(344)], fill=tan)

    # Tower of the Americas.
    draw.rectangle([s(612), s(330), s(632), s(552)], fill="#a05a25")
    draw.ellipse([s(575), s(280), s(670), s(375)], fill=gold, outline="#a05a25", width=s(6))
    draw.line([s(622), s(250), s(622), s(300)], fill="#a05a25", width=s(8))
    draw.line([s(580), s(326), s(668), s(326)], fill="#a05a25", width=s(6))

    # Rock music guitar.
    draw.ellipse([s(850), s(416), s(980), s(546)], fill="#f6c86a", outline=ink, width=s(7))
    draw.ellipse([s(890), s(456), s(940), s(506)], fill="#ffffff", outline=ink, width=s(4))
    draw.polygon([(s(956), s(430)), (s(1075), s(340)), (s(1098), s(366)), (s(986), s(466))], fill="#8d2f26", outline=ink)
    draw.line([(s(970), s(446)), (s(1085), s(354))], fill=ink, width=s(4))
    draw.line([(s(980), s(456)), (s(1094), s(363))], fill=ink, width=s(3))

    # Lone star sun.
    cx, cy, r1, r2 = s(1040), s(292), s(52), s(22)
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        r = r1 if i % 2 == 0 else r2
        pts.append((cx + int(math.cos(ang) * r), cy + int(math.sin(ang) * r)))
    draw.polygon(pts, fill="#ffffff", outline=blue)


def write_png():
    im = Image.new("RGB", (1200, 630), "#edf3f7")
    draw = ImageDraw.Draw(im)
    draw_cover(draw, 1.0)
    im.save(OG_PATH)


def write_svg():
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 750" role="img" aria-label="San Antonio Texas icon cover">
  <rect width="1200" height="750" fill="#edf3f7"/>
  <text x="70" y="104" font-family="Arial, Helvetica, sans-serif" font-size="66" font-weight="900" fill="#20242b">SAN ANTONIO</text>
  <text x="72" y="150" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="800" fill="#667085">ALAMO, RIVER WALK, ROCK'N'ROLL</text>
  <rect x="758" y="62" width="364" height="166" rx="22" fill="#ffffff" stroke="#20242b" stroke-width="8"/>
  <text x="790" y="122" font-family="Arial, Helvetica, sans-serif" font-size="41" font-weight="900" fill="#20242b">Run50 #14</text>
  <text x="790" y="182" font-family="Arial, Helvetica, sans-serif" font-size="52" font-weight="900" fill="#0b67c2">TEXAS</text>
  <path d="M0 590 C160 552 350 578 520 545 C760 583 930 515 1200 495 L1200 750 L0 750 Z" fill="#b8d0c3"/>
  <path d="M0 650 C170 620 355 645 590 610 C790 645 1000 590 1200 575 L1200 750 L0 750 Z" fill="#7aa782"/>
  <path d="M0 710 C230 670 470 705 710 668 C895 640 1045 675 1200 695 L1200 750 L0 750 Z" fill="#2f8fa3"/>
  <path d="M20 698 C230 658 470 693 710 656 C895 628 1045 663 1180 683" fill="none" stroke="#ffffff" stroke-width="6"/>
  <rect x="95" y="470" width="265" height="168" fill="#ba4a2b"/>
  <rect x="72" y="432" width="312" height="46" fill="#8d2f26"/>
  <rect x="115" y="372" width="75" height="60" fill="#ba4a2b"/>
  <rect x="266" y="372" width="74" height="60" fill="#ba4a2b"/>
  <rect x="132" y="512" width="43" height="126" fill="#f7efe1"/>
  <rect x="282" y="512" width="40" height="126" fill="#f7efe1"/>
  <path d="M206 638 V552 A34 70 0 0 1 258 552 V638" fill="#f7efe1"/>
  <rect x="612" y="400" width="20" height="238" fill="#a05a25"/>
  <circle cx="622" cy="350" r="47" fill="#f5b32f" stroke="#a05a25" stroke-width="6"/>
  <line x1="622" y1="305" x2="622" y2="245" stroke="#a05a25" stroke-width="8"/>
  <line x1="580" y1="350" x2="668" y2="350" stroke="#a05a25" stroke-width="6"/>
  <ellipse cx="915" cy="548" rx="70" ry="66" fill="#f6c86a" stroke="#20242b" stroke-width="8"/>
  <circle cx="915" cy="548" r="26" fill="#ffffff" stroke="#20242b" stroke-width="4"/>
  <path d="M958 505 L1075 410 L1100 438 L988 540 Z" fill="#8d2f26" stroke="#20242b" stroke-width="5"/>
  <polygon points="1040,285 1055,327 1100,327 1064,353 1078,396 1040,371 1002,396 1016,353 980,327 1025,327" fill="#ffffff" stroke="#0b67c2" stroke-width="6"/>
</svg>'''
    write_clean(THUMB_PATH, svg)


def update_file(path: Path, updater):
    text = path.read_text(encoding="utf-8")
    new = updater(text)
    if new != text:
        path.write_text(new, encoding="utf-8")


def update_indexes():
    thumb = f"../../../assets/thumb-run50-san-antonio-marathon-icons.svg?v={VERSION}"
    root_thumb = f"assets/thumb-run50-san-antonio-marathon-icons.svg?v={VERSION}"

    zh_card = f'''      <a class="story-card run-50" href="./san-antonio-marathon.html">
        <img src="{thumb}" alt="圣安东尼奥摇滚马拉松城市图标封面" loading="lazy" decoding="async">
        <div class="story-copy">
          <p class="story-meta">德克萨斯圣安东尼奥 · 2023.12.03</p>
          <h2 class="story-title">Run50 #第14州｜圣安东尼奥摇滚马拉松</h2>
          <p class="story-desc">因为马刺和文班亚马来到圣安东尼奥，结果球没看成，却跑完了2023收官马。阿拉莫、River Walk、Fort Sam Houston、墨西哥风情和4小时12分的德州热坡。</p>
          <div class="story-foot">
            <span>长文图记</span>
            <span>阅读 →</span>
          </div>
        </div>
      </a>
'''
    en_card = f'''      <a class="story-card run-50" href="./san-antonio-marathon.html">
        <img src="{thumb}" alt="Icon cover for San Antonio Marathon" />
        <div class="story-card-content">
          <div class="meta">Texas · San Antonio · 2023.12.03</div>
          <h2>San Antonio Rock 'n' Roll Marathon: the Spurs trip that became State 14</h2>
          <p>A Spurs-inspired Texas weekend with the Alamo, River Walk, Fort Sam Houston, live bands, a late hill, and a 4:12 finish to close out 2023.</p>
        </div>
      </a>
'''
    fb_card = f'''    <a class="story-card run-50" href="./san-antonio-marathon.html">
      <div>
        <p class="eyebrow">World / USA / Marathon</p>
        <h2>San Antonio turned a Spurs trip into my Texas marathon story</h2>
        <p>Race date: December 3, 2023. State 14 of Run50, from the Alamo and River Walk to Fort Sam Houston, greenway miles, one late Texas hill and a 4:12 finish.</p>
        <div class="meta">
          <span>San Antonio, Texas</span>
          <span>4:12 finish</span>
          <span>Run50 Facebook</span>
        </div>
      </div>
      <img src="../../assets/thumb-run50-san-antonio-marathon-icons.svg?v={VERSION}" alt="Icon-style San Antonio Marathon cover">
    </a>
'''

    def insert_before_miami(text, card):
        if "san-antonio-marathon.html" in text:
            return text
        marker = '      <a class="story-card run-50" href="./miami-marathon.html">'
        if marker not in text:
            raise RuntimeError("Could not find Miami card marker")
        return text.replace(marker, card + marker, 1)

    update_file(REPO / "run50" / "stories" / "chinese" / "index.html", lambda t: insert_before_miami(t, zh_card))
    update_file(REPO / "run50" / "stories" / "english" / "index.html", lambda t: insert_before_miami(t, en_card))

    def update_fb_index(text):
        if "san-antonio-marathon.html" in text:
            return text
        marker = '    <a class="story-card run-50" href="./miami-marathon.html">'
        if marker not in text:
            raise RuntimeError("Could not find Facebook Miami card marker")
        return text.replace(marker, fb_card + marker, 1)

    update_file(REPO / "run50" / "facebook" / "index.html", update_fb_index)

    def update_run50_index(text):
        return text.replace("6 stories", "7 stories")

    update_file(REPO / "run50" / "index.html", update_run50_index)

    def update_root(text):
        text = text.replace(
            'data-title="Run50 Chinese Stories Xiangyang Guilin Hong Kong Pisa Marathon"',
            'data-title="Run50 Chinese Stories Xiangyang Guilin Hong Kong Pisa Texas San Antonio Marathon"',
        )
        text = text.replace(
            'data-title="Run50 English Stories Xiangyang Guilin Hong Kong Pisa Marathon"',
            'data-title="Run50 English Stories Xiangyang Guilin Hong Kong Pisa Texas San Antonio Marathon"',
        )
        text = text.replace(
            'data-title="Run50 Facebook Xiangyang Guilin Hong Kong Pisa Marathon"',
            'data-title="Run50 Facebook Xiangyang Guilin Hong Kong Pisa Texas San Antonio Marathon"',
        )
        text = text.replace('assets/thumb-run50-guilin-icons.svg?v=20260604-8" alt="Run50 Chinese Stories Guilin cover"', f'{root_thumb}" alt="Run50 Chinese Stories San Antonio cover"')
        text = text.replace('assets/thumb-run50-hong-kong-icons.svg?v=20260604-8" alt="Run50 English Stories Hong Kong cover"', f'{root_thumb}" alt="Run50 English Stories San Antonio cover"')
        text = text.replace('assets/thumb-run50-miami-icons.svg?v=20260605-1" alt="Run50 Facebook Miami cover"', f'{root_thumb}" alt="Run50 Facebook San Antonio cover"')
        text = text.replace("Run50 &middot; Xiangyang + Guilin + Hong Kong + Pisa", "Run50 &middot; Texas + Xiangyang + Guilin + more")
        return text

    update_file(REPO / "index.html", update_root)

    keys = [
        "run50-san-antonio-marathon-facebook-en",
        "run50-san-antonio-marathon-en",
        "run50-san-antonio-marathon-zh",
    ]

    def update_sql(text):
        if keys[0] in text:
            return text
        insert = "\n      " + ",\n      ".join(f"'{key}'" for key in keys) + ","
        return text.replace("'run50-south-carolina-marathon-zh',", "'run50-south-carolina-marathon-zh'," + insert)

    update_file(REPO / "supabase" / "run50-comments.sql", update_sql)


def main():
    indexed = extract_story()
    image_count = copy_story_images(indexed)
    sections = split_sections(indexed)

    chinese_article = render_chinese_article(indexed)
    english_article = render_english_article(sections, "../chinese/Run50-San-Antonio-Marathon-clean_files/")
    fb_article = render_facebook_article(sections)

    write_clean(REPO / "run50" / "stories" / "chinese" / "san-antonio-marathon.html", story_page("zh", chinese_article))
    write_clean(REPO / "run50" / "stories" / "english" / "san-antonio-marathon.html", story_page("en", english_article))
    write_clean(REPO / "run50" / "facebook" / "san-antonio-marathon.html", facebook_page(fb_article))
    write_png()
    write_svg()
    update_indexes()
    print(f"built Texas story: events={len(indexed)} images={image_count}")


if __name__ == "__main__":
    main()
