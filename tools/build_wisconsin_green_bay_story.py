from __future__ import annotations

import html
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


REPO = Path(__file__).resolve().parents[1]
SITE = "https://arsenanzz.github.io/ZZ"
SLUG = "green-bay-marathon"
VERSION = "20260701-wi-green-bay"
SERIES = "Run50 #20"
DATE_ZH = "2024.05.20"
DATE_EN = "May 20, 2024"
SRC_PHOTOS = Path(r"Z:\ZhennanZ Folder\000-Marathon-Story-2024-2025\20240520-WI-Cellcome Green Bay-Marathon\4-WI-Polished Photos")
SRC_TEXT = Path(r"C:\Users\ZZ\.codex\attachments\ec03be16-1a40-4c56-a9cd-dcfec3f82488\pasted-text.txt")
ASSET_DIR_NAME = "Run50-Green-Bay-Marathon-clean_files"
ASSET_DIR = REPO / "run50" / "stories" / "chinese" / ASSET_DIR_NAME


EN_SECTIONS = [
    (
        "Preface | Crossing the Windy City, heading for the Cheese State",
        [
            "I had only been at my internship for one week, but Run50 was already pulling me back onto the road. On May 20, Siqi and I decided to drive north to Wisconsin for my 20th state: the Cellcom Green Bay Marathon.",
            "We left on Friday evening, with the sunset turning farms and grain silos gold. The car felt like it was moving through an oil painting.",
            "The next morning, after a simple American breakfast in Lafayette, we kept driving north.",
            "The road took us past wind farms, fields, and the Chicago skyline. A red navigation warning trapped us in Windy City traffic, crawling forward on the highway.",
            "Once we finally broke through, the northern sky opened up again.",
            "Our first Wisconsin stop was Milwaukee, home of the NBA's Bucks. Yi Jianlian was drafted by Milwaukee with the sixth pick in 2007. I had heard that he was not exactly thrilled at first about going to this cold northern city.",
            "But later he still had some good moments here, and now Milwaukee's signature is Giannis.",
            "To us, Milwaukee did not feel small at all. We found a very good Indian buffet, ate a weekend feast, and even had mango ice cream.",
            "After that we walked along Lake Michigan. The wind off the lake was strong, the water and sky were clean and high, and the Milwaukee skyline sat in the distance.",
            "Then we continued toward Green Bay.",
        ],
    ),
    (
        "State 20: Wisconsin | Cheese, football, and the Packers",
        [
            "Wisconsin is called America's Dairyland, famous for cheese and the Cheesehead hats worn by Packers fans.",
            "Green Bay is not a big city, but the Green Bay Packers make it known across the country. Lambeau Field is almost the heart of the city.",
            "For runners, the special hook of this marathon was simple: before the finish, the course ran into Lambeau Field.",
            "This was the 25th Cellcom Green Bay Marathon, and also the final edition. After this year, the race would be gone.",
            "The surprise was the weather. I thought a northern race would be cool. Instead, race day came with heat.",
        ],
    ),
    (
        "Chapter 1 | Arriving in Green Bay",
        [
            "Green Bay felt clean, quiet, and very Packers. Even small details around town seemed to point back to football.",
            "Packet pickup was easy and relaxed. Volunteers handed out bibs and shirts, and the race had that small-city friendliness that makes a weekend feel less rushed.",
            "Before race day we settled in, looked around the town, and prepared for what was supposed to be a northern spring marathon.",
        ],
    ),
    (
        "Chapter 2 | Race morning: the heat arrives",
        [
            "On race morning the start area was already bright and warm. Runners gathered under the banner, trying to look fresh before the sun fully took over.",
            "The course first moved through neighborhood roads and open streets. Mile signs came one by one, and the crowd support was friendly and close.",
            "By the early miles, I could tell this would not be the cool Wisconsin run I had imagined. The sun was sharp, and the heat kept building.",
        ],
    ),
    (
        "Chapter 3 | Lakeside roads and a hot northern test",
        [
            "The middle miles mixed residential roads, river and lake views, volunteers, families cheering from lawns, and the occasional patch of shade.",
            "Wisconsin may be known for snow, cheese, and winter football, but that day felt like an oven. Down by the water and open road, even the geese seemed to know it was hot.",
            "I kept moving, switching between running and walking when needed. The race was no longer about pace; it was about reaching Lambeau Field.",
        ],
    ),
    (
        "Chapter 4 | Lambeau Field and the finish",
        [
            "Near the end, the course finally entered the Packers' holy ground: Lambeau Field.",
            "Running through the stadium felt surreal. The stands, the turf, the yellow-and-green seats, and the tunnel all turned the final miles into a football pilgrimage.",
            "I crossed the finish in about four and a half hours. It was my first and last Green Bay Marathon, and my 20th state was done.",
            "After the race, Siqi and I took medal photos, ate, recovered, and started the long drive home.",
        ],
    ),
    (
        "Postscript | State 20, a milestone",
        [
            "Run50 had reached state number twenty. From Louisville to Lafayette, from Chicago traffic to Milwaukee's lakeshore, from cheese-state football faith to a hot marathon finish at Lambeau Field, this trip felt like a real milestone.",
            "Not every race has to be fast. Some races are remembered because of where they take you. Green Bay gave me exactly that: a finish line inside an NFL shrine, and another state colored in on the Run50 map.",
        ],
    ),
]


def clean_name(path: Path) -> str:
    return re.sub(r"^Copy #\d+ of\s+", "", path.name)


def natural_key(path: Path) -> list[object]:
    clean = clean_name(path)
    return [int(part) if part.isdigit() else part.lower() for part in re.split(r"(\d+)", clean)]


def photo_files() -> list[Path]:
    return sorted(
        [p for p in SRC_PHOTOS.iterdir() if p.suffix.lower() in {".png", ".jpg", ".jpeg"} and p.name.lower() != "desktop.ini"],
        key=natural_key,
    )


def extract_chinese_sections() -> list[tuple[str, list[str]]]:
    lines = SRC_TEXT.read_text(encoding="utf-8").splitlines()
    start = next(i for i, line in enumerate(lines) if "前言" in line and "跨过" in line)
    end = next((i for i in range(start + 1, len(lines)) if "终极口播" in lines[i]), len(lines))
    story_lines = lines[start:end]
    sections: list[tuple[str, list[str]]] = []
    title = ""
    blocks: list[str] = []
    for raw in story_lines:
        line = raw.strip()
        if not line or line == "---":
            continue
        if line.startswith("###"):
            if title:
                sections.append((title, blocks))
            title = re.sub(r"^#+\s*", "", line).strip()
            title = title.strip("* ")
            blocks = []
        else:
            line = re.sub(r"\*\*(.*?)\*\*", r"\1", line)
            blocks.append(line)
    if title:
        sections.append((title, blocks))
    return sections[:7]


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/georgiab.ttf" if bold else "C:/Windows/Fonts/georgia.ttf",
    ]
    for item in candidates:
        path = Path(item)
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def convert_photos() -> list[str]:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    paths = photo_files()
    names: list[str] = []
    for idx, src in enumerate(paths, 1):
        out_name = f"img-{idx:03d}.webp"
        out = ASSET_DIR / out_name
        im = Image.open(src)
        im = ImageOps.exif_transpose(im).convert("RGB")
        im.save(out, "WEBP", quality=86, method=6)
        names.append(out_name)
    return names


def caption_en(idx: int) -> str:
    ranges = [
        (4, "Run50 map and Wisconsin route planning"),
        (8, "Rolling north through farm country and sunset light"),
        (14, "Wind farms, Chicago traffic, and the drive into Wisconsin"),
        (21, "Milwaukee, Lake Michigan, skyline views, and a very good Indian buffet"),
        (35, "Green Bay arrival, packet pickup, Airbnb, and small-city details"),
        (55, "Race morning, neighborhood miles, and the heat building on course"),
        (72, "Lakeside paths, river light, volunteers, and mile markers"),
        (96, "The long hot middle miles toward Lambeau Field"),
        (112, "Lambeau Field, finish-line energy, and medal moments"),
        (121, "Post-race food, finish data, and the long road home"),
    ]
    for end, text in ranges:
        if idx <= end:
            return f"{text} #{idx:03d} @Arsenan"
    return f"Green Bay Marathon weekend #{idx:03d} @Arsenan"


def caption_zh(idx: int) -> str:
    ranges = [
        (4, "Run50 地图与威斯康辛路线规划"),
        (8, "一路北上，农田和夕阳把周末拉开"),
        (14, "风车、芝加哥车流和进入威斯康辛的路上"),
        (21, "密尔沃基、密歇根湖、城市天际线和印度自助"),
        (35, "抵达绿湾、取号码布、Airbnb 和小城细节"),
        (55, "比赛日清晨、社区赛道和逐渐升温的太阳"),
        (72, "湖边小路、河面光影、志愿者和英里牌"),
        (96, "通往兰博球场前的漫长炎热中段"),
        (112, "兰博球场、终点气氛和奖牌时刻"),
        (121, "赛后吃饭、完赛数据和回程路上"),
    ]
    for end, text in ranges:
        if idx <= end:
            return f"{text} #{idx:03d} @Arsenan"
    return f"绿湾马拉松周末 #{idx:03d} @Arsenan"


IMAGE_SPLITS = [21, 35, 55, 72, 96, 112, 121]


def render_figures(names: list[str], start: int, end: int, locale: str, rel_prefix: str) -> str:
    parts = []
    for idx in range(start, end + 1):
        cap = caption_zh(idx) if locale == "zh" else caption_en(idx)
        alt = "绿湾马拉松照片" if locale == "zh" else "Green Bay Marathon photo"
        parts.append(
            f'      <figure><img src="{rel_prefix}{ASSET_DIR_NAME}/{names[idx-1]}" alt="{html.escape(alt)} {idx}" loading="lazy" decoding="async"><figcaption>{html.escape(cap)}</figcaption></figure>'
        )
    return "\n".join(parts)


STYLE = """
  <style id="run50-global-tabs-style">
    .run50-global-tabs{max-width:1120px;margin:0 auto;padding:18px 22px 0;display:grid!important;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px;font-family:Arial,Helvetica,sans-serif}
    .run50-global-tabs a{display:block;border:1px solid rgba(148,163,184,.45);border-radius:8px;padding:10px 12px;text-align:center;text-decoration:none;color:#1f2937;background:rgba(255,255,255,.72);font-size:13px;font-weight:800}
    .run50-global-tabs a:first-child{text-align:left}.run50-global-tabs a:last-child{text-align:right}.run50-global-tabs a:hover{border-color:currentColor}
    @media(max-width:640px){.run50-global-tabs{grid-template-columns:repeat(2,minmax(0,1fr))!important;padding:14px 18px 0;row-gap:8px}.run50-global-tabs a{font-size:12px;padding:9px 10px}}
  </style>
  <style>
    :root{--paper:#edf3f7;--ink:#1f2937;--muted:#667085;--line:#d5e1ea;--blue:#0b67c2;--green:#164e3f}
    *{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font-family:Arial,Helvetica,sans-serif;line-height:1.78}
    .page-header{max-width:1120px;margin:0 auto;padding:44px 22px 28px}.kicker{margin:0 0 12px;color:var(--blue);font-weight:900;letter-spacing:.08em;text-transform:uppercase;font-size:13px}
    h1{margin:0;max-width:900px;font-family:Georgia,serif;font-size:clamp(36px,6vw,70px);line-height:1.05;letter-spacing:0}
    .subtitle{max-width:780px;margin:18px 0 0;color:#344054;font-size:18px}.meta{display:flex;flex-wrap:wrap;gap:10px;margin-top:20px}.meta span{border:1px solid var(--line);background:#fff;border-radius:999px;padding:6px 11px;font-size:13px;font-weight:800;color:#475467}
    .article-shell{max-width:860px;margin:0 auto;padding:8px 22px 64px}.article-shell h2{font-family:Georgia,serif;font-size:clamp(26px,4vw,40px);line-height:1.2;margin:54px 0 18px;color:#152033}.article-shell p{font-size:18px;margin:0 0 18px}
    figure{margin:30px 0;background:#fff;border:1px solid var(--line);border-radius:8px;overflow:hidden;box-shadow:0 18px 44px rgba(15,23,42,.08)}figure img{display:block;width:100%;height:auto}figcaption{padding:10px 14px;color:#475467;font-size:14px;line-height:1.55;background:#fff}
    .zz-engagement{max-width:960px;margin:30px auto 64px;padding:0 22px}.zz-engagement-shell{border:1px solid var(--line);border-radius:8px;background:#fff;padding:22px}.zz-engagement-kicker{font-weight:900;color:var(--blue);margin:0 0 6px}.zz-engagement h2{margin:0 0 8px;font-family:Georgia,serif}.zz-engagement-note{color:var(--muted)}
    @media(max-width:640px){.page-header{padding-top:30px}.article-shell p{font-size:16px}.article-shell{padding-inline:18px}figure{margin:24px 0}}
  </style>
"""


def nav(prefix: str, current: str) -> str:
    links = [
        ("Run50", f"{prefix}../index.html" if current == "fb" else f"{prefix}../../index.html"),
        ("English Stories", f"{prefix}../stories/english/" if current == "fb" else f"{prefix}../english/"),
        ("Chinese Stories", f"{prefix}../stories/chinese/" if current == "fb" else f"{prefix}../chinese/"),
        ("Facebook", f"{prefix}../facebook/" if current != "fb" else f"{prefix}./"),
    ]
    return '<nav class="run50-global-tabs" aria-label="Run50 navigation">' + "".join(f'<a href="{href}">{label}</a>' for label, href in links) + "</nav>"


def engagement(locale: str, page_key: str, rel: str) -> str:
    if locale == "zh":
        title = "跑完之后，说两句"
        note = "无需账号即可留言，新评论会立即显示。"
        kicker = "评论 / 浏览"
        loading = "评论加载中..."
    else:
        title = "Say something after the run"
        note = "No account is needed to submit a comment. New comments appear right away."
        kicker = "Comments / Views"
        loading = "Loading comments..."
    return f"""
  <section class="zz-engagement" data-zz-engagement data-locale="{locale}" data-page-key="{page_key}">
    <div class="zz-engagement-shell">
      <div>
        <p class="zz-engagement-kicker">{kicker}</p>
        <h2>{title}</h2>
        <p class="zz-engagement-note">{note}</p>
        <div class="zz-engagement-stats"><span class="zz-engagement-stat" id="busuanzi_container_page_pv"><span>Views</span> <strong id="busuanzi_value_page_pv" data-zz-view-count>--</strong></span></div>
      </div>
      <div class="zz-engagement-card"><div id="supabase-comments-{SLUG}-{locale}" data-zz-supabase-comments></div><p class="zz-engagement-status" data-zz-engagement-status>{loading}</p></div>
    </div>
  </section>
  <link rel="stylesheet" href="{rel}assets/zz-engagement.css?v=20260701">
  <script src="{rel}assets/zz-engagement-config.js?v=20260701"></script>
  <script src="{rel}assets/zz-engagement.js?v=20260701"></script>
"""


def page(title: str, subtitle: str, sections: list[tuple[str, list[str]]], names: list[str], locale: str, current: str) -> str:
    rel_asset = "" if current == "zh" else ("../stories/chinese/" if current == "fb" else "../chinese/")
    rel_root = "../../../" if current in {"zh", "en"} else "../../"
    page_key = f"run50-{SLUG}-{'zh' if locale == 'zh' else ('facebook-en' if current == 'fb' else 'en')}"
    parts = [
        "<!doctype html>",
        f'<html lang="{"zh-CN" if locale == "zh" else "en"}">',
        "<head>",
        '  <meta charset="utf-8">',
        '  <meta name="viewport" content="width=device-width, initial-scale=1">',
        f"  <title>{html.escape(title)} | Arsenan</title>",
        f'  <meta name="description" content="{html.escape(subtitle)}">',
        f'  <meta property="og:title" content="{html.escape(title)}">',
        f'  <meta property="og:description" content="{html.escape(subtitle)}">',
        '  <meta property="og:type" content="article">',
        f'  <meta property="og:image" content="{SITE}/assets/og-run50-{SLUG}-icons.png">',
        STYLE,
        "</head>",
        "<body>",
        nav("", current),
        '  <header class="page-header">',
        f"    <p class=\"kicker\">{SERIES} · Wisconsin · Green Bay</p>",
        f"    <h1>{html.escape(title)}</h1>",
        f"    <p class=\"subtitle\">{html.escape(subtitle)}</p>",
        f"    <div class=\"meta\"><span>{DATE_ZH if locale == 'zh' else DATE_EN}</span><span>Green Bay, Wisconsin</span><span>Cellcom Green Bay Marathon</span><span>121 photos</span></div>",
        "  </header>",
        '  <main class="article-shell">',
    ]
    start = 1
    for i, (heading, blocks) in enumerate(sections):
        parts.append(f"    <h2>{html.escape(heading)}</h2>")
        for block in blocks:
            parts.append(f"    <p>{html.escape(block)}</p>")
        end = IMAGE_SPLITS[min(i, len(IMAGE_SPLITS) - 1)]
        parts.append(render_figures(names, start, end, locale, rel_asset))
        start = end + 1
    parts.extend(["  </main>", engagement(locale, page_key, rel_root), "</body>", "</html>"])
    return "\n".join(parts)


def write_pages(names: list[str]) -> None:
    zh_sections = extract_chinese_sections()
    zh_title = "Run50 #第20州｜威斯康辛：绿湾马拉松｜奶酪州的橄榄球信仰"
    zh_subtitle = "从路易斯维尔一路北上，穿过芝加哥和密尔沃基，最后在绿湾的热浪里跑进兰博球场。"
    en_title = "Run50 State #20 | Wisconsin: Green Bay Marathon"
    en_subtitle = "A northern road trip through Chicago and Milwaukee, ending with a hot marathon finish inside Lambeau Field."
    fb_title = "The Green Bay Marathon ended inside football's small-town cathedral"
    fb_subtitle = "Run50 State 20: cheese-state pride, unexpected heat, and the final Cellcom Green Bay Marathon."
    targets = [
        (REPO / "run50" / "stories" / "chinese" / f"{SLUG}.html", page(zh_title, zh_subtitle, zh_sections, names, "zh", "zh")),
        (REPO / "run50" / "stories" / "english" / f"{SLUG}.html", page(en_title, en_subtitle, EN_SECTIONS, names, "en", "en")),
        (REPO / "run50" / "facebook" / f"{SLUG}.html", page(fb_title, fb_subtitle, EN_SECTIONS, names, "en", "fb")),
    ]
    for path, content in targets:
        path.write_text(content, encoding="utf-8")


def cover(draw_zh: bool, out: Path, fb: bool = False) -> None:
    im = Image.new("RGB", (1200, 750), "#dcecf7")
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([24, 22, 1176, 728], radius=38, fill="#f5f7ef", outline="#233044", width=8)
    d.rounded_rectangle([46, 46, 1154, 704], radius=28, fill="#d5eef3", outline="#e9dcae", width=5)
    d.rectangle([60, 420, 1140, 590], fill="#1f6f5a")
    d.polygon([(46, 410), (260, 270), (560, 330), (780, 220), (1154, 360), (1154, 620), (46, 620)], fill="#74b8d8")
    d.rectangle([46, 500, 1154, 620], fill="#19613f")
    d.arc([170, 170, 1030, 665], 205, 355, fill="#f6c443", width=20)
    d.line([(190, 560), (350, 500), (520, 535), (695, 450), (880, 500), (1030, 430)], fill="#fff6d2", width=10)
    for x in [280, 430, 580, 730, 880]:
        d.rectangle([x, 235, x + 34, 420], fill="#f8d74e", outline="#0f5138", width=4)
        d.polygon([(x - 18, 420), (x + 52, 420), (x + 18, 455)], fill="#0f5138")
    d.ellipse([875, 120, 1110, 355], fill="#f3d36a", outline="#213147", width=7)
    d.polygon([(880, 235), (920, 150), (960, 235), (1000, 150), (1040, 235), (1080, 150), (1105, 235)], fill="#1b5c2e")
    if draw_zh:
        top = "威斯康辛"
        city = "绿湾马拉松"
        series = "RUN50 20"
    else:
        top = "WISCONSIN"
        city = "GREEN BAY"
        series = "RUN50 20"
    d.text((76, 72), top, font=font(70 if draw_zh else 64, True), fill="#0b5139", stroke_width=3, stroke_fill="#fff3d6")
    d.rounded_rectangle([255, 565, 945, 690], radius=26, fill="#113f67", outline="#fff0c2", width=6)
    city_font = font(64 if draw_zh else 76, True)
    bbox = d.textbbox((0, 0), city, font=city_font, stroke_width=2)
    d.text((600 - (bbox[2] - bbox[0]) / 2, 608), city, font=city_font, fill="#fff0c2", stroke_width=3, stroke_fill="#0f172a")
    d.rounded_rectangle([70, 625, 225, 700], radius=18, fill="#9b2f23", outline="#fff0c2", width=5)
    d.text((99, 646), "2024", font=font(38, True), fill="#fff0c2")
    d.rounded_rectangle([970, 625, 1130, 700], radius=18, fill="#0b67c2", outline="#fff0c2", width=5)
    d.text((986, 647), series, font=font(30, True), fill="#fff0c2")
    im.save(out, quality=92)
    if fb:
        return


def og_and_thumb() -> None:
    path = REPO / "assets" / f"og-run50-{SLUG}-icons.png"
    im = Image.new("RGB", (1200, 630), "#dcecf7")
    d = ImageDraw.Draw(im)
    d.rectangle([0, 390, 1200, 630], fill="#1f6f5a")
    d.rectangle([0, 0, 1200, 400], fill="#bddfed")
    d.arc([110, 120, 1110, 700], 205, 350, fill="#f6c443", width=22)
    d.text((64, 64), "GREEN BAY", font=font(66, True), fill="#20242b")
    d.text((66, 136), "Cellcom Green Bay Marathon", font=font(26, True), fill="#667085")
    d.rounded_rectangle([760, 64, 1122, 228], radius=22, fill="#ffffff", outline="#20242b", width=7)
    d.text((790, 112), "Run50 #20", font=font(40, True), fill="#20242b")
    d.text((790, 166), "WISCONSIN", font=font(48, True), fill="#0b67c2")
    for x in [240, 390, 540, 690]:
        d.rectangle([x, 250, x + 28, 390], fill="#f8d74e", outline="#0f5138", width=4)
    path.parent.mkdir(parents=True, exist_ok=True)
    im.save(path)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 750" role="img" aria-label="Green Bay Marathon Run50 cover">
<rect width="1200" height="750" rx="36" fill="#dcecf7"/>
<rect x="34" y="34" width="1132" height="682" rx="30" fill="#f5f7ef" stroke="#20242b" stroke-width="8"/>
<path d="M60 500 C260 350 410 340 560 420 S860 560 1140 330 L1140 610 L60 610 Z" fill="#74b8d8"/>
<path d="M120 570 C330 505 480 535 650 462 S920 492 1080 430" fill="none" stroke="#f6c443" stroke-width="22" stroke-linecap="round"/>
<text x="70" y="104" font-family="Arial, Helvetica, sans-serif" font-size="66" font-weight="900" fill="#20242b">GREEN BAY</text>
<text x="72" y="150" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="800" fill="#667085">Cellcom Marathon</text>
<rect x="758" y="62" width="364" height="166" rx="22" fill="#ffffff" stroke="#20242b" stroke-width="8"/>
<text x="790" y="122" font-family="Arial, Helvetica, sans-serif" font-size="41" font-weight="900" fill="#20242b">Run50 #20</text>
<text x="790" y="182" font-family="Arial, Helvetica, sans-serif" font-size="48" font-weight="900" fill="#0b67c2">WISCONSIN</text>
<rect x="250" y="585" width="700" height="100" rx="24" fill="#113f67" stroke="#fff0c2" stroke-width="6"/>
<text x="600" y="654" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="62" font-weight="900" fill="#fff0c2">GREEN BAY</text>
</svg>'''
    (REPO / "assets" / f"thumb-run50-{SLUG}-icons.svg").write_text(svg, encoding="utf-8")


def write_covers() -> None:
    assets = REPO / "assets"
    cover(True, assets / f"cover-medal-zh-{SLUG}.jpg")
    cover(False, assets / f"cover-medal-{SLUG}.jpg")
    cover(False, assets / f"cover-medal-fb-{SLUG}.jpg", fb=True)
    og_and_thumb()


def insert_once(text: str, marker: str, block: str) -> str:
    if f'href="./{SLUG}.html"' in text or f'href="../../stories/chinese/{SLUG}.html"' in text:
        return text
    return text.replace(marker, block + "\n" + marker, 1)


def update_indexes() -> None:
    zh = REPO / "run50" / "stories" / "chinese" / "index.html"
    en = REPO / "run50" / "stories" / "english" / "index.html"
    fb = REPO / "run50" / "facebook" / "index.html"
    zh_block = f'''        <a class="story-card run-50" href="./{SLUG}.html">
          <img src="../../../assets/cover-medal-zh-{SLUG}.jpg?v={VERSION}" alt="威斯康辛绿湾马拉松奖牌封面" loading="lazy" decoding="async">
          <div class="story-copy">
            <p class="story-meta">威斯康辛绿湾 · 2024.05.20</p>
            <h2 class="story-title">Run50 #第20州｜威斯康辛：绿湾马拉松｜跑进兰博球场的最后一届</h2>
            <p class="story-desc">从风城和密歇根湖一路北上，在奶酪州的热浪里跑进 Green Bay Packers 的圣地兰博球场。</p>
            <div class="story-foot"><span>长文图记</span><span>阅读 →</span></div>
          </div>
        </a>'''
    en_block = f'''        <a class="story-card run-50" href="./{SLUG}.html" data-map-meta="Wisconsin · Green Bay · 2024.05.20">
          <img src="../../../assets/cover-medal-{SLUG}.jpg?v={VERSION}" alt="Green Bay Marathon medal cover" loading="lazy" decoding="async">
          <div class="story-copy">
            <p class="story-meta">Green Bay, WI · Lambeau finish</p>
            <h2 class="story-title">Wisconsin gave Run50 a hot finish inside Lambeau Field</h2>
            <p class="story-desc">Race date: May 20, 2024. Run50 State 20 at the final Cellcom Green Bay Marathon, with Milwaukee, Lake Michigan, cheese-state football faith, and 121 photos from the weekend.</p>
            <div class="story-foot"><span>Run50 Story</span><span>Read →</span></div>
          </div>
        </a>'''
    fb_block = f'''        <a class="story-card run-50" href="./{SLUG}.html">
          <img src="../../assets/cover-medal-fb-{SLUG}.jpg?v={VERSION}" alt="Green Bay Marathon medal cover" loading="lazy" decoding="async">
          <div class="story-copy">
            <p class="story-meta">Green Bay, WI · Lambeau finish</p>
            <h2 class="story-title">The Green Bay Marathon ended inside football's small-town cathedral</h2>
            <p class="story-desc">Run50 State 20: cheese-state pride, unexpected heat, and the final Cellcom Green Bay Marathon finishing through Lambeau Field.</p>
            <div class="story-foot"><span>Run50 Facebook</span><span>Read →</span></div>
          </div>
        </a>'''
    zh_text = insert_once(zh.read_text(encoding="utf-8"), '        <a class="story-card run-50" href="../../wechat/hatfield-mccoy-marathon-modern-rail.html">', zh_block)
    en_text = insert_once(en.read_text(encoding="utf-8"), '        <a class="story-card run-50" href="./michigan-meadows-marathon.html"', en_block)
    fb_text = insert_once(fb.read_text(encoding="utf-8"), '        <a class="story-card run-50" href="./michigan-meadows-marathon.html">', fb_block)
    zh_text = zh_text.replace("'MI-大急流城': 'michigan-meadows-marathon.html',", "'WI-绿湾': 'green-bay-marathon.html',\n      'MI-大急流城': 'michigan-meadows-marathon.html',")
    en_text = en_text.replace("'MI-Grand Rapids': 'michigan-meadows-marathon.html',", "'WI-Green Bay': 'green-bay-marathon.html',\n      'MI-Grand Rapids': 'michigan-meadows-marathon.html',")
    zh.write_text(zh_text, encoding="utf-8")
    en.write_text(en_text, encoding="utf-8")
    fb.write_text(fb_text, encoding="utf-8")


def update_hub() -> None:
    for rel in ["run50/index.html", "run50/hub.html"]:
        path = REPO / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        text = text.replace("['Green Bay Marathon', '2024.05.20', '']", "['Green Bay Marathon', '2024.05.20', 'stories/english/green-bay-marathon.html']")
        text = text.replace("['Green Bay Marathon', '2024.05.20', \"\"]", "['Green Bay Marathon', '2024.05.20', 'stories/english/green-bay-marathon.html']")
        if "'WI':[{city:'Green Bay'" not in text:
            text = text.replace(
                "  'MI':[{city:'Grand Rapids',date:'Aug 2024',story:'stories/english/michigan-meadows-marathon.html',fb:'facebook/michigan-meadows-marathon.html'}],",
                "  'WI':[{city:'Green Bay',date:'2024.05.20',story:'stories/english/green-bay-marathon.html',fb:'facebook/green-bay-marathon.html'}],\n  'MI':[{city:'Grand Rapids',date:'Aug 2024',story:'stories/english/michigan-meadows-marathon.html',fb:'facebook/michigan-meadows-marathon.html'}],",
            )
        path.write_text(text, encoding="utf-8")


def update_supabase() -> None:
    path = REPO / "supabase" / "run50-comments.sql"
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    keys = [f"run50-{SLUG}-zh", f"run50-{SLUG}-en", f"run50-{SLUG}-facebook-en"]
    if all(k in text for k in keys):
        return
    anchor = "'run50-michigan-meadows-marathon-zh',"
    if anchor in text:
        text = text.replace(anchor, anchor + "\n    " + ",\n    ".join(f"'{k}'" for k in keys) + ",", 1)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    names = convert_photos()
    if len(names) != 121:
        raise SystemExit(f"Expected 121 photos, got {len(names)}")
    write_pages(names)
    write_covers()
    update_indexes()
    update_hub()
    update_supabase()
    print(f"Built {SLUG}: {len(names)} photos")


if __name__ == "__main__":
    main()
