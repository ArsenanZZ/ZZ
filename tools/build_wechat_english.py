#!/usr/bin/env python3
"""Build the Run50 WeChat English edition from existing English story pages.

The generator keeps the WeChat/new story order, uses the Facebook English
articles as idiomatic source copy, and reuses the article map snapshots from
the Chinese WeChat article pages.
"""

from __future__ import annotations

import html
import json
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
RUN50 = ROOT / "run50"
WECHAT = RUN50 / "wechat"
WECHAT_NEW = RUN50 / "wechat-new"
FACEBOOK = RUN50 / "facebook"
STORIES_EN = RUN50 / "stories" / "english"
PRACTICE = RUN50
OUT = RUN50 / "wechat-en"
VERSION = "20260706-wechat-en"


SPECIAL_SOURCE = {
    "hatfield-mccoy-marathon": "hatfield-mccoy-english-practice.html",
    "pittsburgh-marathon": "pittsburgh-english-practice.html",
}

SPECIAL_COVERS = {
    "green-bay-marathon": "../../assets/cover-medal-en-index-green-bay-wechat.png?v=20260706-wechat-en",
    "kentucky-derby-marathon-2021": "../../assets/cover-medal-en-index-kentucky-derby-2021-v2.png?v=20260706-wechat-en",
}

SERIES_LABEL = {
    "run-50": ("RUN50 DISPATCH", "Run50 · U.S. Marathon Stories"),
    "run-cn": ("RUNCN DISPATCH", "RunCN · China Marathon Stories"),
    "run-world": ("RUNWORLD DISPATCH", "RunWorld · Global Marathon Stories"),
}

STATE_BY_SLUG = {
    "louisville-marathon": ("Kentucky", "KY", "Louisville, Kentucky"),
    "kentucky-derby-marathon-2021": ("Kentucky", "KY", "Louisville, Kentucky"),
    "cleveland-marathon": ("Ohio", "OH", "Cleveland, Ohio"),
    "new-york-city-marathon": ("New York", "NY", "New York City, New York"),
    "san-francisco-marathon": ("California", "CA", "San Francisco, California"),
    "indianapolis-monumental-marathon": ("Indiana", "IN", "Indianapolis, Indiana"),
    "honolulu-marathon": ("Hawaii", "HI", "Honolulu, Hawaii"),
    "atlanta-marathon": ("Georgia", "GA", "Atlanta, Georgia"),
    "kentucky-derby-marathon-2023": ("Kentucky", "KY", "Louisville, Kentucky"),
    "kentucky-derby-marathon": ("Kentucky", "KY", "Louisville, Kentucky"),
    "hatfield-mccoy-marathon": ("Kentucky", "KY", "Williamson, Kentucky"),
    "cincinnati-flying-pig-marathon": ("Ohio", "OH", "Cincinnati, Ohio"),
    "denver-colfax-marathon": ("Colorado", "CO", "Denver, Colorado"),
    "anchorage-marathon": ("Alaska", "AK", "Anchorage, Alaska"),
    "st-joseph-marathon": ("Missouri", "MO", "St. Joseph, Missouri"),
    "chicago-marathon": ("Illinois", "IL", "Chicago, Illinois"),
    "nashville-marathon": ("Tennessee", "TN", "Nashville, Tennessee"),
    "west-virginia-marathon": ("West Virginia", "WV", "Huntington, West Virginia"),
    "san-antonio-marathon": ("Texas", "TX", "San Antonio, Texas"),
    "disney-marathon": ("Florida", "FL", "Orlando, Florida"),
    "miami-marathon": ("Florida", "FL", "Miami, Florida"),
    "north-carolina-oak-island-marathon": ("North Carolina", "NC", "Oak Island, North Carolina"),
    "little-rock-marathon": ("Arkansas", "AR", "Little Rock, Arkansas"),
    "south-carolina-marathon": ("South Carolina", "SC", "Greer, South Carolina"),
    "pittsburgh-marathon": ("Pennsylvania", "PA", "Pittsburgh, Pennsylvania"),
    "green-bay-marathon": ("Wisconsin", "WI", "Green Bay, Wisconsin"),
    "michigan-meadows-marathon": ("Michigan", "MI", "Grand Rapids, Michigan"),
    "new-hampshire-clarence-demar-marathon": ("New Hampshire", "NH", "Keene, New Hampshire"),
    "louisville-marathon-2024": ("Kentucky", "KY", "Louisville, Kentucky"),
    "louisiana-marathon": ("Louisiana", "LA", "Baton Rouge, Louisiana"),
    "blue-ridge-marathon": ("Virginia", "VA", "Roanoke, Virginia"),
    "kentucky-derby-marathon-2025": ("Kentucky", "KY", "Louisville, Kentucky"),
    "fargo-marathon": ("North Dakota", "ND", "Fargo, North Dakota"),
    "hell-on-gravel-marathon": ("Kansas", "KS", "El Dorado, Kansas"),
    "mad-marathon": ("Vermont", "VT", "Waitsfield, Vermont"),
    "rocket-city-marathon": ("Alabama", "AL", "Huntsville, Alabama"),
    "arizona-phoenix-marathon": ("Arizona", "AZ", "Phoenix, Arizona"),
}


@dataclass
class Card:
    slug: str
    source_slug: str
    href: str
    image: str
    image_alt: str
    title: str
    desc: str
    meta: str
    series_class: str
    section: str


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = "\n".join(line.rstrip() for line in text.splitlines()) + "\n"
    path.write_text(text, encoding="utf-8", newline="\n")


def clean_text_artifacts(value: str) -> str:
    replacements = {
        "\u00c2\u00b7": "\u00b7",
        "\u00c2": "",
        "\u00e2\u20ac\u2122": "'",
        "\u00e2\u20ac\u02dc": "'",
        "\u00e2\u20ac\u0153": '"',
        "\u00e2\u20ac\ufffd": '"',
        "\u00e2\u20ac\u009d": '"',
        "\u00e2\u20ac\u201d": "-",
        "\u00e2\u20ac\u201c": "-",
        "\u00e2\u20ac\u00a6": "...",
        "\u00ef\u00bd\u0153": "|",
        "\ufffd": "",
    }
    for old, new in replacements.items():
        value = value.replace(old, new)
    return value


def strip_tags(value: str) -> str:
    value = re.sub(r"<script\b.*?</script>", "", value, flags=re.I | re.S)
    value = re.sub(r"<style\b.*?</style>", "", value, flags=re.I | re.S)
    value = re.sub(r"<[^>]+>", " ", value)
    return clean_text_artifacts(re.sub(r"\s+", " ", html.unescape(value)).strip())


def attr(block: str, name: str) -> str:
    match = re.search(rf"\b{name}\s*=\s*(['\"])(.*?)\1", block, flags=re.I | re.S)
    return clean_text_artifacts(html.unescape(match.group(2).strip())) if match else ""


def slug_from_href(href: str) -> str | None:
    file_name = href.split("?")[0].rstrip("/").split("/")[-1]
    if not file_name.endswith(".html"):
        return None
    stem = file_name[:-5]
    return stem.removesuffix("-modern-rail")


def card_blocks(index_html: str) -> Iterable[tuple[str, str]]:
    pattern = re.compile(r"<a\b([^>]*\bstory-card\b[^>]*)>(.*?)</a>", re.I | re.S)
    return pattern.findall(index_html)


def parse_fb_cards() -> dict[str, Card]:
    index_html = read(FACEBOOK / "index.html")
    cards: dict[str, Card] = {}
    for attrs, body in card_blocks(index_html):
        href = attr(attrs, "href")
        slug = slug_from_href(href)
        if not slug:
            continue
        klass = attr(attrs, "class")
        series_class = "run-world" if "run-world" in klass else "run-cn" if "run-cn" in klass else "run-50"
        image_tag = re.search(r"<img\b[^>]*>", body, re.I | re.S)
        image = attr(image_tag.group(0), "src") if image_tag else ""
        image_alt = attr(image_tag.group(0), "alt") if image_tag else ""
        title_match = re.search(r"<h[23][^>]*class=\"story-title\"[^>]*>(.*?)</h[23]>", body, re.I | re.S)
        title = strip_tags(title_match.group(1)) if title_match else ""
        desc = strip_tags(re.search(r"<p[^>]*class=\"story-desc\"[^>]*>(.*?)</p>", body, re.I | re.S).group(1)) if re.search(r"<p[^>]*class=\"story-desc\"[^>]*>(.*?)</p>", body, re.I | re.S) else ""
        meta = strip_tags(re.search(r"<p[^>]*class=\"story-meta\"[^>]*>(.*?)</p>", body, re.I | re.S).group(1)) if re.search(r"<p[^>]*class=\"story-meta\"[^>]*>(.*?)</p>", body, re.I | re.S) else ""
        cards[slug] = Card(slug, slug, href, image, image_alt, title, desc, meta, series_class, "")
    return cards


def parse_wechat_order() -> list[tuple[str, str]]:
    html_text = read(WECHAT_NEW / "index.html")
    order: list[tuple[str, str]] = []
    section = "run50"
    last_pos = 0
    section_marks = [
        ("run50", html_text.find('id="run50-series"')),
        ("runcn", html_text.find('id="runcn-series"')),
        ("runworld", html_text.find('id="runworld-series"')),
    ]
    section_marks = [(name, pos) for name, pos in section_marks if pos >= 0]
    section_marks.sort(key=lambda item: item[1])
    for match in re.finditer(r'<a\b([^>]*\bstory-card\b[^>]*)>', html_text, re.I | re.S):
        pos = match.start()
        for name, mark in section_marks:
            if mark <= pos:
                section = name
        attrs = match.group(1)
        href = attr(attrs, "href")
        slug = slug_from_href(href)
        if slug:
            order.append((slug, section))
        last_pos = pos
    seen: set[str] = set()
    unique: list[tuple[str, str]] = []
    for slug, section in order:
        if slug not in seen:
            seen.add(slug)
            unique.append((slug, section))
    return unique


def parse_meta_from_article(path: Path) -> dict[str, str]:
    text = read(path)
    title = strip_tags(re.search(r"<h1[^>]*>(.*?)</h1>", text, re.I | re.S).group(1)) if re.search(r"<h1[^>]*>(.*?)</h1>", text, re.I | re.S) else ""
    desc = attr(re.search(r"<meta\b[^>]*name=[\"']description[\"'][^>]*>", text, re.I | re.S).group(0), "content") if re.search(r"<meta\b[^>]*name=[\"']description[\"'][^>]*>", text, re.I | re.S) else ""
    image = attr(re.search(r"<meta\b[^>]*property=[\"']og:image[\"'][^>]*>", text, re.I | re.S).group(0), "content") if re.search(r"<meta\b[^>]*property=[\"']og:image[\"'][^>]*>", text, re.I | re.S) else ""
    if image.startswith("https://zhennanzhang.com/"):
        image = "../.." + image.removeprefix("https://zhennanzhang.com")
    elif image.startswith("https://arsenanzz.github.io/ZZ/"):
        image = "../.." + image.removeprefix("https://arsenanzz.github.io/ZZ")
    return {"title": title, "desc": desc, "image": image}


def extract_article_body(path: Path) -> str:
    text = read(path)
    match = re.search(r"<article\b[^>]*>(.*?)</article>", text, re.I | re.S)
    if not match:
        match = re.search(r"<main\b[^>]*>(.*?)</main>", text, re.I | re.S)
    if not match:
        return "<p>Story copy is being prepared.</p>"
    body = match.group(1)
    body = re.sub(r"<script\b.*?</script>", "", body, flags=re.I | re.S)
    body = re.sub(r"\s*class=\"(?:section-label|lede|end-mark|credit-line|story-kicker-line)\"", "", body)
    body = re.sub(r"\s*style=\"[^\"]*\"", "", body)
    body = re.sub(r"<p>\s*Race day\s*</p>", "", body, flags=re.I)
    body = re.sub(r"<p>\s*-\s*End\s*-\s*</p>", "", body, flags=re.I)
    body = re.sub(r"<p>\s*(Words|Photos|Design)\s*\|\s*Arsenan\s*</p>", "", body, flags=re.I)
    body = re.sub(r"<h2>\s*Chapter\s+(\d+)\s*\|\s*(.*?)</h2>", r"<h2>\2</h2>", body, flags=re.I | re.S)
    body = normalize_relative_paths(body)
    body = remove_decorative_figures(body)
    body = polish_html_copy(body)
    body = transform_h2_to_field_notes(body)
    body = add_wechat_emphasis(body)
    return clean_text_artifacts(body).strip()


def normalize_relative_paths(body: str) -> str:
    body = body.replace('src="../chinese/', 'src="../stories/chinese/')
    body = body.replace("src='../chinese/", "src='../stories/chinese/")
    body = body.replace('href="../chinese/', 'href="../stories/chinese/')
    body = body.replace('src="../../../assets/', 'src="../../assets/')
    body = body.replace("src='../../../assets/", "src='../../assets/")
    return body


def local_image_path(src: str) -> Path | None:
    clean = html.unescape(src or "").split("#")[0].split("?")[0].strip()
    if not clean or clean.startswith(("http://", "https://", "data:")):
        return None
    return (OUT / clean).resolve()


def is_decorative_image(src: str) -> bool:
    path = local_image_path(src)
    if not path or not path.exists():
        return False
    try:
        with Image.open(path) as image:
            width, height = image.size
    except Exception:
        return False
    # The old WeChat exports include thin divider strips, tiny icon tiles, and
    # low-resolution map/watermark fragments. In English articles they become
    # full-width blurry blocks, so keep only real photo-scale images.
    if width < 320 or height < 140:
        return True
    if width / max(height, 1) > 4.2:
        return True
    return False


def remove_decorative_figures(body: str) -> str:
    def replace_figure(match: re.Match[str]) -> str:
        figure = match.group(0)
        image = re.search(r"<img\b[^>]*>", figure, flags=re.I | re.S)
        src = attr(image.group(0), "src") if image else ""
        return "" if is_decorative_image(src) else figure

    body = re.sub(r"<figure\b[^>]*>\s*<img\b[^>]*>\s*(?:<figcaption\b[^>]*>.*?</figcaption>\s*)?</figure>", replace_figure, body, flags=re.I | re.S)
    return re.sub(r"\n{3,}", "\n\n", body)


def polish_html_copy(body: str) -> str:
    replacements = {
        "horse racing expo": "marathon expo",
        "Horse racing expo": "Marathon expo",
        "horse expo": "race expo",
        "Horse expo": "Race expo",
        "no horse racing": "no marathon",
        "No horse racing": "No marathon",
        "horse racing": "marathon running",
        "Horse racing": "Marathon running",
        "horse race": "marathon",
        "Horse race": "Marathon",
        "running horses": "running marathons",
        "Running horses": "Running marathons",
        "run horses": "run marathons",
        "Run horses": "Run marathons",
        "came to race": "came to run the marathon",
        "came to run a horse": "came to run a marathon",
        "I was here for marathon running": "I was in town for the marathon",
        "the road was specially closed to free up the area": "the street had been closed off for vendors",
        "I went to Nanyang twice": "I had traveled through Southeast Asia twice",
        "understand the warmth and warmth of human beings": "feel the warmth and rough edges of ordinary life",
    }
    for old, new in replacements.items():
        body = body.replace(old, new)
    return body


def transform_h2_to_field_notes(body: str) -> str:
    counter = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal counter
        counter += 1
        title = strip_tags(match.group(1))
        return (
            f'<section class="field-note-head">'
            f'<p>FIELD NOTE {counter:02d}</p>'
            f'<h2>{html.escape(title)}</h2>'
            f'</section>'
        )

    return re.sub(r"<h2[^>]*>(.*?)</h2>", repl, body, flags=re.I | re.S)


def renumber_field_notes(body: str) -> str:
    counter = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal counter
        counter += 1
        return f"FIELD NOTE {counter:02d}"

    return re.sub(r"FIELD NOTE\s+\d{2}", repl, body)


def add_wechat_emphasis(body: str) -> str:
    keywords = [
        "Run50", "RunCN", "RunWorld", "marathon", "half marathon", "finish line",
        "race day", "course", "runner", "runners", "Boston", "Chicago", "Cleveland", "Ohio", "Lake Erie",
        "NYC Marathon", "Central Park", "Times Square", "Flushing", "Hudson River",
        "Kentucky", "Louisville", "Derby", "Churchill Downs", "Florida", "Disney",
        "Miami", "Arizona", "Phoenix", "Hawaii", "Honolulu", "China", "Wuhan",
        "Guang'an", "Guangan", "Yichang", "Changsha", "Hubei", "Sichuan", "Hunan",
        "Hong Kong", "Singapore", "Bangkok", "Mexico City", "Pisa",
    ]
    keyword_pattern = re.compile(
        r"(?<![\w-])(" + "|".join(re.escape(k) for k in sorted(keywords, key=len, reverse=True)) + r")(?![\w-])",
        re.I,
    )
    number_pattern = re.compile(r"\b(\d+(?:\.\d+)?(?:K| miles?| hours?| minutes?|:\d{2}|-\d+)?|\d{4})\b", re.I)

    def emphasize_text(text: str, limit: int = 2) -> str:
        if "<" in text or "&lt;" in text:
            return text
        used = 0

        def repl_keyword(match: re.Match[str]) -> str:
            nonlocal used
            if used >= limit:
                return match.group(0)
            used += 1
            return f'<strong class="auto-emphasis accent-{(used - 1) % 5}">{match.group(0)}</strong>'

        text = keyword_pattern.sub(repl_keyword, text, count=limit)
        if used == 0:
            def repl_number(match: re.Match[str]) -> str:
                nonlocal used
                if used >= limit:
                    return match.group(0)
                used += 1
                return f'<strong class="auto-emphasis accent-{(used - 1) % 5}">{match.group(0)}</strong>'
            text = number_pattern.sub(repl_number, text, count=limit)
        return text

    def repl_paragraph(match: re.Match[str]) -> str:
        attrs, inner = match.group(1), match.group(2)
        if strip_tags(inner).upper().startswith("FIELD NOTE"):
            return match.group(0)
        if "auto-caption" in attrs or "note-label" in attrs or "<strong" in inner or "<img" in inner:
            return match.group(0)
        return f"<p{attrs}>{emphasize_text(inner)}</p>"

    return re.sub(r"<p([^>]*)>(.*?)</p>", repl_paragraph, body, flags=re.I | re.S)


def cleveland_race_body() -> str:
    def fig(number: int, caption: str = "") -> str:
        cap = f"<figcaption>{html.escape(caption)}</figcaption>" if caption else ""
        return (
            f'<figure><img src="../stories/chinese/Run50-Cleveland-Marathon-clean_files/img-{number:03d}.webp" '
            f'alt="Cleveland Marathon photo {number:03d}" loading="lazy" decoding="async">{cap}</figure>'
        )

    raw = f"""
<p>Run first. Then the city can explain itself.</p>
<h2>Why Cleveland still happened</h2>
<p>The 2021 Cleveland Marathon was supposed to be in May, but COVID pushed it into October. I was still deciding whether to go when I saw that the Wuhan Marathon was scheduled for the same day. The idea of running a marathon at the same time as old friends back in Wuhan suddenly made the trip feel necessary.</p>
<p>Then the plot twisted. Wuhan was canceled the day before race day. Cleveland still happened. It lost a little of the long-distance ritual I had imagined, but the run itself turned out to be deeply satisfying.</p>
{fig(30, "Course map @ Google")}
<h2>A start line in the dark</h2>
<p>The start was near Tower City Center. I walked out before dawn, still in the dark, and the red tower above the start area looked unexpectedly dramatic.</p>
{fig(31, "Start area @ Arsenan")}
<p>Cleveland at daybreak was cold enough to make everyone shiver. Starting in darkness was not new to me. Singapore and Bangkok had done that too, but those races run from midnight into humid morning air. Cleveland was different: the sun simply rose late, and the cold was several levels sharper.</p>
{fig(32)}
<p>I wore a thin long-sleeve shirt and thought I would peel it off once I warmed up. Then the race started, and I realized I was not taking it off at all.</p>
{fig(33, "Starting out @ Arsenan")}
<p>After the gun, everyone began moving with real urgency, partly because standing still was miserable. We headed southwest along Detroit Road, legs finally doing what they were supposed to do.</p>
{fig(34, "Out on the course @ Arsenan")}
<p>Only later did I learn Cleveland has not just Detroit Road but also a Detroit Shoreway. Cleveland and Detroit, two Great Lakes Rust Belt cities, seem to have found a strange kind of warmth in each other's industrial afterlife. But that morning, none of that mattered much. I was there to run.</p>
{fig(35, "Into the city @ Arsenan")}
{fig(36)}
<h2>The hard-looking miles back downtown</h2>
<p>After 25th Street, 48th Street, and a loop through Franklin Boulevard, we returned to Detroit Road, this time pointed back toward downtown.</p>
{fig(37)}
{fig(38)}
<p>The sky was still not fully bright. In the distance, the towers stood firm against the morning clouds. That stretch had a tough, industrial beauty to it. Of the whole weekend, it is one of the parts I remember most clearly.</p>
{fig(39, "Veterans Memorial Bridge @ Arsenan")}
{fig(40)}
<p>We crossed the Veterans Memorial Bridge and a hard concrete stretch downtown, then turned toward the long elevated road by Lake Erie.</p>
{fig(41, "Right side @ Arsenan")}
{fig(42, "Left side @ Arsenan")}
<h2>Lake Erie, sunrise, and the quarter turn</h2>
<p>On the right, a train moved along Lake Erie, with blue water and pink clouds layered together. On the left, the sun was just coming up, and the city skyline sharpened in the morning light.</p>
{fig(43, "Cleveland skyline @ Arsenan")}
{fig(44)}
{fig(45, "Runners @ Photographer")}
<p>After the elevated section, we reached the waterfront park. By then daylight had arrived, I felt good, and the race was giving out enough gels to keep me calm.</p>
{fig(46, "Coming off the elevated road @ Arsenan")}
<p>Past the park, the course moved through a lakeside neighborhood. Adults and kids came out to cheer, and there were unofficial aid tables too. The road was narrow, which made the neighborhood feel close and warm.</p>
{fig(47, "Quarter turnaround @ Arsenan")}
<p>At the end of that neighborhood, the course turned back. Roughly a quarter of the marathon was done.</p>
{fig(48, "Return tunnel @ Arsenan")}
<h2>The view only a marathon gives you</h2>
<p>The way back was similar to the way out, so the novelty faded a little. But once I returned to the blue bridge by the lake and saw downtown from a different angle, the city changed completely.</p>
{fig(49, "Blue bridge @ Arsenan")}
{fig(50, "Back toward downtown @ Arsenan")}
<p>The hard lines of the city and its industrial character were all there at once. In front of the buildings, the Cuyahoga River moved slowly, looking as if it had already washed away some of its old industrial scars.</p>
{fig(51, "Cleveland @ Arsenan")}
{fig(52)}
<p>If not for the marathon, I probably never would have seen Cleveland from that angle. We crossed back toward the city, turned again, and the second half began.</p>
{fig(53, "Near 20K @ Arsenan")}
<h2>Gels, a banana, and getting through it</h2>
<p>There were noticeably fewer runners in the second half, and the scenery repeated enough that I stopped thinking about photos and settled into the work of running.</p>
{fig(54, "Return miles @ Arsenan")}
<p>Downtown, I grabbed a pile of gels. My thinking was simple: gels in hand, panic out of mind. It worked. I took one at nearly every aid station, and at least delayed the wall.</p>
{fig(55)}
<p>Later, back in the neighborhood, I grabbed a banana and finally got through the roughest patch. After that, the race hurt less. I could actually enjoy the final miles.</p>
{fig(56, "Return miles @ Photographer")}
<h2>Finish, medal, Public Square</h2>
<p>I finished Cleveland in under five hours, which was my best recent result at the time. Since moving to the U.S., I had become embarrassingly rusty, so this one felt good.</p>
{fig(57, "Finish @ Photographer")}
{fig(58, "Finish @ Arsenan")}
<p>47 had been waiting at the finish for quite a while and caught the moment after I crossed the line.</p>
{fig(59, "Finish @ 47")}
{fig(60, "Medal @ Arsenan")}
<p>The Cleveland medal was genuinely beautiful: openwork design, metallic weight, and a very industrial feel. Very Cleveland.</p>
{fig(61)}
{fig(62)}
<p>With the medal on, I took a lot of photos around Public Square. In the dark before the start I had not really seen the place. After the race, I finally realized how polished it was.</p>
{fig(63)}
{fig(64)}
{fig(65, "Public Square @ Arsenan")}
<h2>Back through Ohio</h2>
<p>After the race I showered at Planet Fitness. That national gym chain is honestly useful, and compared with Chicago, the Cleveland location felt much better.</p>
<p>Refreshed, we started the drive back to Louisville, nearly six hours away. On the way, we crossed an Ohio rainstorm, then stopped in Cincinnati after the weather cleared for a Chinese buffet before getting home.</p>
<p>Looking back, it was a dusty, hurried weekend by car across Ohio. But those 42.195 kilometers gave me a kind of satisfaction that made the whole trip worth it.</p>
"""
    return add_wechat_emphasis(transform_h2_to_field_notes(raw)).strip()


def cleveland_article_body(source_path: Path) -> tuple[dict[str, str], str]:
    meta = {
        "title": "Run50 #2 | Ohio: Cleveland Marathon, From Night to Daylight",
        "desc": "A complete two-part Cleveland story: the cold dawn marathon first, then Rock Hall, Cavaliers, Lake Erie, and the Rust Belt city around it.",
        "image": "../../assets/cover-medal-en-index-cleveland.png?v=20260702-en-index-v1",
    }
    city = extract_article_body(source_path)
    city_start = city.find("<h2>Melancholy Cleveland</h2>")
    if city_start >= 0:
        section_start = city.rfind('<section class="field-note-head">', 0, city_start)
        if section_start >= 0:
            city = city[section_start:]
    intro = """
<section class="field-note-head"><p>FIELD NOTE 00</p><h2>After the race, the city</h2></section>
<p>Once the marathon was in the body, Cleveland made more sense: Lake Erie, old industry, rock and roll, basketball, and a city still carrying itself with stubborn pride.</p>
"""
    body = cleveland_race_body() + "\n" + add_wechat_emphasis(intro).strip() + "\n" + city
    return meta, renumber_field_notes(body)


def extract_practice_article(slug: str, file_name: str) -> tuple[dict[str, str], str]:
    path = PRACTICE / file_name
    text = read(path)
    title = strip_tags(re.search(r"<h1[^>]*>(.*?)</h1>", text, re.I | re.S).group(1)) if re.search(r"<h1[^>]*>(.*?)</h1>", text, re.I | re.S) else slug.replace("-", " ").title()
    title = re.sub(r"^#?\d+\s+[^|]+\|\s*", "", title)
    raw = re.search(r"const\s+DATA\s*=\s*(\[.*?\]);", text, re.S)
    items = json.loads(raw.group(1)) if raw else []
    paragraphs: list[str] = []
    current: list[str] = []
    last_cue = ""
    for item in items:
        cue = re.sub(r"\.\d+$", "", item.get("cue", ""))
        en = item.get("en", "").strip()
        if not en:
            continue
        en = polish_practice_sentence(en)
        cue_label = re.sub(r"^\d+:\d+\s*", "", cue).strip()
        if re.search(r"[\u4e00-\u9fff]", cue_label):
            cue_label = ""
        if cue_label and cue_label != last_cue:
            if current:
                paragraphs.append("<p>" + " ".join(current) + "</p>")
                current = []
            paragraphs.append(
                f'<section class="field-note-head"><p>FIELD NOTE {len([p for p in paragraphs if "field-note-head" in p]) + 1:02d}</p><h2>{html.escape(cue_label.title())}</h2></section>'
            )
            last_cue = cue_label
        current.append(html.escape(en))
        if len(" ".join(current)) > 360:
            if not current[:-1]:
                paragraphs.append(
                    f'<section class="field-note-head"><p>FIELD NOTE {len([p for p in paragraphs if "field-note-head" in p]) + 1:02d}</p><h2>Story Beat {len([p for p in paragraphs if "field-note-head" in p]) + 1:02d}</h2></section>'
                )
            paragraphs.append("<p>" + " ".join(current) + "</p>")
            current = []
    if current:
        paragraphs.append("<p>" + " ".join(current) + "</p>")
    meta = {
        "title": title,
        "desc": "A conversational English edition prepared from the Run50 read-along script.",
        "image": "",
    }
    return meta, "\n".join(paragraphs)


def polish_practice_sentence(sentence: str) -> str:
    replacements = {
        "Which is the most swing state": "Which state swings the hardest",
        "running a marathon with many bridges and steep slopes": "running a marathon packed with bridges and steep climbs",
        "the track": "the course",
        "Not only is the state shaking": "It is not just the state that swings",
        "started from Kentucky and ran towards": "left Kentucky and headed toward",
    }
    for old, new in replacements.items():
        sentence = sentence.replace(old, new)
    return sentence


def extract_map_panel(slug: str) -> str:
    for base in (WECHAT, WECHAT_NEW):
        path = base / f"{slug}-modern-rail.html"
        if path.exists():
            text = read(path)
            match = re.search(r'<section class="article-map-panel"[^>]*>.*?</section>', text, re.I | re.S)
            if match:
                panel = match.group(0)
                panel = re.sub(r"v=20\d+[-\w]*", f"v={VERSION}", panel)
                panel = re.sub(
                    r'(<div\b(?![^>]*\bdata-map-locale=)(?=[^>]*\bclass="[^"]*\barticle-map-window\b))',
                    r'\1 data-map-locale="en"',
                    panel,
                )
                return panel
    return ""


def normalize_asset_path(path: str) -> str:
    if not path:
        return ""
    if path.startswith("http"):
        return path
    path = path.replace("\\", "/")
    if path.startswith("../../"):
        return path
    if path.startswith("../"):
        return "../" + path
    if path.startswith("./"):
        return path[2:]
    return path


def source_article_path(slug: str) -> Path | None:
    story = STORIES_EN / f"{slug}.html"
    if story.exists():
        return story
    fb = FACEBOOK / f"{slug}.html"
    if fb.exists():
        return fb
    special = SPECIAL_SOURCE.get(slug)
    if special and (PRACTICE / special).exists():
        return PRACTICE / special
    return None


def build_cards() -> list[Card]:
    fb_cards = parse_fb_cards()
    cards: list[Card] = []
    for slug, section in parse_wechat_order():
        source_slug = slug
        card = fb_cards.get(slug)
        if not card and slug in SPECIAL_SOURCE:
            label, series_text = SERIES_LABEL["run-50"]
            state = STATE_BY_SLUG.get(slug, ("", "", ""))[0]
            meta, _ = extract_practice_article(slug, SPECIAL_SOURCE[slug])
            image = f"../../assets/cover-medal-en-index-{slug.replace('marathon', '').strip('-')}.png"
            if slug == "hatfield-mccoy-marathon":
                image = "../../assets/cover-medal-en-index-williamson.png?v=20260702-en-index-v3"
            if slug == "pittsburgh-marathon":
                image = "../../assets/cover-medal-en-index-pittsburgh.png?v=20260702-en-index-v2"
            card = Card(slug, slug, "", image, meta["title"], meta["title"], meta["desc"], f"{label} · {state}".strip(), "run-50", section)
        if not card:
            continue
        if slug in SPECIAL_COVERS:
            card.image = SPECIAL_COVERS[slug]
        card.section = section
        card.href = f"./{slug}-modern-rail.html?v={VERSION}"
        cards.append(card)
    return cards


def article_page(card: Card) -> str:
    source_path = source_article_path(card.slug)
    if not source_path:
        meta = {"title": card.title, "desc": card.desc, "image": card.image}
        body = "<p>Story copy is being prepared.</p>"
    elif source_path.name.endswith("-english-practice.html"):
        meta, body = extract_practice_article(card.slug, source_path.name)
    elif card.slug == "cleveland-marathon":
        meta, body = cleveland_article_body(source_path)
    else:
        meta = parse_meta_from_article(source_path)
        body = extract_article_body(source_path)
    title = meta.get("title") or card.title
    desc = meta.get("desc") or card.desc
    cover = SPECIAL_COVERS.get(card.slug) or card.image or meta.get("image", "")
    cover = normalize_asset_path(cover)
    map_panel = extract_map_panel(card.slug)
    state_name, state_abbr, place = STATE_BY_SLUG.get(card.slug, ("", "", ""))
    series_title = SERIES_LABEL.get(card.series_class, SERIES_LABEL["run-50"])[0]
    section_line = clean_text_artifacts(card.meta or f"{series_title} \u00b7 {state_name or 'Marathon'}")
    finish_region = place or state_name or card.meta or "Run50"
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)} | Run50 WeChat English</title>
  <meta name="description" content="{html.escape(desc)}">
  <script>
    (function () {{
      try {{
        var saved = localStorage.getItem('run50-wechat-article-theme');
        document.documentElement.dataset.theme = saved === 'light' ? 'light' : 'dark';
      }} catch (error) {{
        document.documentElement.dataset.theme = 'dark';
      }}
    }})();
  </script>
  <link rel="stylesheet" href="../wechat-article-theme.css?v={VERSION}">
  <link rel="stylesheet" href="./wechat-en.css?v={VERSION}">
</head>
<body>
<button class="article-theme-toggle" type="button" aria-label="Toggle theme">Light</button>
<script src="../us-map-svg.js?v={VERSION}"></script>
<script src="../china-map-svg.js?v={VERSION}"></script>
<script src="../world-geo-data.js?v={VERSION}"></script>
<script src="../wechat-article-map.js?v={VERSION}"></script>
<script src="../wechat-article-theme.js?v={VERSION}"></script>
<main class="wechat-en-page">
  <nav class="wechat-en-nav">
    <a href="../index.html">Run50</a>
    <a href="./index.html">WeChat English</a>
    <a href="../wechat-new/?v=20260630-rail-align">Chinese Edition</a>
    <a href="../facebook/">Facebook</a>
  </nav>
  <header class="wechat-en-header">
    <p class="kicker">{html.escape(section_line)}</p>
    <h1>{html.escape(title)}</h1>
    <p class="dek">{html.escape(desc)}</p>
    <div class="meta-row">
      <span>{html.escape(place or state_name or 'Run50')}</span>
      <span>{html.escape(series_title)}</span>
      <span>WeChat English</span>
    </div>
  </header>
  <section class="opening-note">
    <p class="note-label">OPENING NOTE</p>
    <p>This English edition keeps the race story up front and lets the travel notes breathe around it. It is written for American friends: conversational, direct, and naturally about running marathons.</p>
  </section>
  <section class="cover-block">
    <img src="{html.escape(cover)}" alt="{html.escape(title)} cover" loading="lazy" decoding="async">
    <p class="auto-caption">Run50 English cover · {html.escape(state_abbr or card.section.upper())} @Arsenan</p>
  </section>
  {map_panel}
  <article class="wechat-en-article">
    {body}
    <section class="wechat-en-credits" aria-label="Credits">
      <p>- End -</p>
      <p>Words · Arsenan</p>
      <p>Photos · Arsenan</p>
      <p>Design · Arsenan</p>
    </section>
  </article>
  <section class="wechat-finish-line" aria-label="Run50 finish line">
    <p class="finish-kicker">RUN50 FINISH LINE</p>
    <h2>One more mile saved for the story.</h2>
    <div class="finish-chips">
      <span>{html.escape(series_title)}</span>
      <span>{html.escape(finish_region)}</span>
      <span>WeChat English</span>
    </div>
    <p>This edition keeps the running up front, then lets the city, the food, the weather, and the small human details settle in around it.</p>
    <p class="finish-note">Thanks for reading. The Chinese WeChat edition carries the original voice; this English version keeps the same route, just in a language that feels natural to American friends.</p>
  </section>
</main>
<script src="../../assets/zz-home-button.js?v=20260703-home" defer></script>
</body>
</html>
"""


def render_card(card: Card) -> str:
    image = normalize_asset_path(card.image)
    series_label = SERIES_LABEL.get(card.series_class, SERIES_LABEL["run-50"])[0]
    return f"""
      <a class="story-card {card.series_class}" href="{html.escape(card.href)}">
        <img src="{html.escape(image)}" alt="{html.escape(card.image_alt or card.title)}" loading="lazy" decoding="async">
        <div class="story-card-body">
          <p class="story-meta">{html.escape(card.meta or series_label)}</p>
          <h3 class="story-title">{html.escape(card.title)}</h3>
          <p class="story-desc">{html.escape(card.desc)}</p>
          <p class="story-foot">Open WeChat English →</p>
        </div>
      </a>"""


def story_number(card: Card, fallback: int) -> str:
    meta = card.meta or ""
    match = re.search(r"(Run(?:50|CN|World)\s*#?\s*[0-9A-Z+\-]+)", meta, re.I)
    if match:
        value = match.group(1)
        value = re.sub(r"RunCN\s*#?", "RunCN · ", value, flags=re.I)
        value = re.sub(r"RunWorld\s*#?", "RunWorld · ", value, flags=re.I)
        value = re.sub(r"Run50\s*#?", "Run50 · ", value, flags=re.I)
        return value.replace("  ", " ")
    if card.series_class == "run-cn":
        return f"RunCN · {fallback:02d}"
    if card.series_class == "run-world":
        return f"RunWorld · {fallback:02d}"
    return f"Run50 · {fallback:02d}"


def render_wechat_new_card(card: Card, index: int) -> str:
    image = normalize_asset_path(card.image)
    href = f"https://zhennanzhang.com/run50/wechat-en/{card.slug}-modern-rail.html?v={VERSION}"
    series_label = SERIES_LABEL.get(card.series_class, SERIES_LABEL["run-50"])[0]
    region = ""
    if card.series_class == "run-50":
        region = STATE_BY_SLUG.get(card.slug, ("", "", ""))[0].upper()
    elif card.series_class == "run-cn":
        region = (card.meta.split("·")[0] if card.meta else "CHINA").strip().upper()
    else:
        region = (card.meta.split("·")[0] if card.meta else "WORLD").strip().upper()
    return f"""
          <a class="story-card" href="{html.escape(href)}">
            <img src="{html.escape(image)}" alt="{html.escape(card.image_alt or card.title)}">
            <div class="story-body">
              <span class="story-number">{html.escape(story_number(card, index))}</span>
              <div class="eyebrow">{html.escape(series_label)} · {html.escape(region)}</div>
              <h3>{html.escape(card.title)}</h3>
              <div class="meta">{html.escape(card.meta or series_label)}</div>
              <p class="desc">{html.escape(card.desc)}</p>
              <div class="open">Open WeChat English →</div>
            </div>
          </a>"""


def render_wechat_new_section(cards: list[Card], key: str, title: str, eyebrow: str, count_label: str) -> str:
    body = "\n".join(render_wechat_new_card(card, i + 1) for i, card in enumerate(cards))
    zone = "run-50-zone" if key == "run50" else "run-cn-zone" if key == "runcn" else "run-world-zone"
    aria = {
        "run50": "Run50 U.S. marathon WeChat English stories",
        "runcn": "RunCN China marathon WeChat English stories",
        "runworld": "RunWorld global marathon WeChat English stories",
    }[key]
    return f"""      <section class="story-section {zone}" id="{key}-series">
        <div class="section-head">
          <div>
            <div class="eyebrow">{eyebrow}</div>
            <h2>{title}</h2>
          </div>
          <p>{count_label}</p>
        </div>

        <div class="stories" aria-label="{aria}">{body}
        </div>
      </section>

"""


def translate_wechat_new_script_text(page: str) -> str:
    replacements = {
        "下方故事待补": "Story pending below",
        "点击定位到下方故事": "Click to jump to the story below",
        "点击选择": "click to choose",
        "待补": "pending",
        "篇故事": " stories",
        " 篇": " stories",
        "篇：": " stories: ",
        "点击打开完整互动地图": "Click to open the full interactive map",
        "请在下方故事中选择": "choose from the stories below",
        "已定位：": "selected: ",
        "已定位到下方故事": "selected the story below",
    }
    for old, new in replacements.items():
        page = page.replace(old, new)
    china_label_replacements = {
        "黑龙江": "Heilongjiang",
        "湖北": "Hubei",
        "四川": "Sichuan",
        "内蒙古": "Inner Mongolia",
        "山西": "Shanxi",
        "湖南": "Hunan",
        "福建": "Fujian",
        "甘肃": "Gansu",
        "江苏": "Jiangsu",
        "贵州": "Guizhou",
        "陕西": "Shaanxi",
        "浙江": "Zhejiang",
        "海南": "Hainan",
        "辽宁": "Liaoning",
        "上海": "Shanghai",
        "广西": "Guangxi",
        "香港": "Hong Kong",
        "北京": "Beijing",
        "哈尔滨": "Harbin",
        "鄂尔多斯": "Ordos",
        "长治": "Changzhi",
        "武汉": "Wuhan",
        "宜昌": "Yichang",
        "襄阳": "Xiangyang",
        "广安": "Guangan",
        "长沙": "Changsha",
        "厦门": "Xiamen",
        "兰州": "Lanzhou",
        "无锡": "Wuxi",
        "贵阳": "Guiyang",
        "西安": "Xian",
        "杭州": "Hangzhou",
        "海口": "Haikou",
        "大连": "Dalian",
        "宁波": "Ningbo",
        "桂林": "Guilin",
    }
    for old, new in china_label_replacements.items():
        page = page.replace(old, new)
    page = re.sub(r"<footer>.*?</footer>", "<footer>WeChat English follows the same layout as the Chinese WeChat New edition.</footer>", page, flags=re.S)
    page = page.replace("切换到亮色模式", "Switch to light mode")
    page = page.replace("切换到暗色模式", "Switch to dark mode")
    page = page.replace("切换明暗主题", "Toggle theme")
    page = page.replace("https://zhennanzhang.com/run50/wechat/';", "https://zhennanzhang.com/run50/wechat-en/';")
    page = page.replace("?v=20260630-wechat-emphasis';", f"?v={VERSION}';")
    page = page.replace(
        "return `${label} · ${titles.length} stories: ${titles.slice(0, 3).join(' / ')}${titles.length > 3 ? ' / ...' : ''}`;",
        "return `${label} · ${titles.length === 1 ? '1 story' : `${titles.length} stories`}: ${titles.slice(0, 3).join(' / ')}${titles.length > 3 ? ' / ...' : ''}`;",
    )
    page = page.replace(
        "heading.textContent = `${label} · ${rows.length || 0}  stories · click to choose`;",
        "heading.textContent = `${label} · ${rows.length === 1 ? '1 story' : `${rows.length || 0} stories`} · click to choose`;",
    )
    page = page.replace(
        "count.textContent = rows.length ? `${rows.length} stories` : 'pending';",
        "count.textContent = rows.length ? (rows.length === 1 ? '1 story' : `${rows.length} stories`) : 'pending';",
    )
    return page


def english_mini_map_localizer_script() -> str:
    return """  <script>
    (() => {
      const labelMap = {
        '南海': 'South China Sea',
        '蒙古': 'Mongolia',
        '韩国': 'South Korea',
        '日本': 'Japan',
        '渤海': 'Bohai Sea',
        '黄海': 'Yellow Sea',
        '东海': 'East China Sea',
        '黑龙江': 'Heilongjiang',
        '湖北': 'Hubei',
        '四川': 'Sichuan',
        '内蒙古': 'Inner Mongolia',
        '山西': 'Shanxi',
        '湖南': 'Hunan',
        '福建': 'Fujian',
        '甘肃': 'Gansu',
        '江苏': 'Jiangsu',
        '贵州': 'Guizhou',
        '陕西': 'Shaanxi',
        '浙江': 'Zhejiang',
        '海南': 'Hainan',
        '辽宁': 'Liaoning',
        '广西': 'Guangxi',
        '香港': 'Hong Kong',
        '北京': 'Beijing'
      };
      function localizeMiniChinaMap() {
        document.querySelectorAll('#runcn-china-map-mini text').forEach((text) => {
          const value = (text.textContent || '').trim();
          if (labelMap[value]) text.textContent = labelMap[value];
          else if (/[\u4e00-\u9fff]/.test(value)) text.textContent = '';
        });
      }
      localizeMiniChinaMap();
      const target = document.getElementById('runcn-china-map-mini');
      if (target) new MutationObserver(localizeMiniChinaMap).observe(target, { childList: true, subtree: true });
    })();
  </script>
"""


def index_page(cards: list[Card]) -> str:
    base = read(WECHAT_NEW / "index.html")
    buckets = {
        "run50": [c for c in cards if c.section == "run50"],
        "runcn": [c for c in cards if c.section == "runcn"],
        "runworld": [c for c in cards if c.section == "runworld"],
    }
    sections = (
        render_wechat_new_section(
            buckets["run50"],
            "run50",
            "U.S. Marathon Stories",
            "Run50 · U.S. States",
            f"{len(buckets['run50'])} stories · ordered by race timeline",
        )
        + render_wechat_new_section(
            buckets["runcn"],
            "runcn",
            "China Marathon Stories",
            "RunCN · China Routes",
            f"{len(buckets['runcn'])} stories · cities, regions, and race years",
        )
        + render_wechat_new_section(
            buckets["runworld"],
            "runworld",
            "World Marathon Stories",
            "RunWorld · Global Routes",
            f"{len(buckets['runworld'])} stories · outside the U.S. and China",
        )
    )
    hero_and_ticker = f"""      <section class="hero hero-board" id="score">
        <div class="scorecard intro-card">
          <div class="eyebrow">Run50 Coverage</div>
          <h1>WeChat English Edition</h1>
          <p class="lead">A WeChat-style English edition for American friends: race day first, travel notes after, natural marathon language, and the same browsing rhythm as the Chinese WeChat New index.</p>
          <div class="series-strip" aria-label="Run50 story families">
            <div class="series-chip">
              <strong>Run50</strong>
              <span>U.S. state-by-state marathon stories, organized by race and place.</span>
            </div>
            <div class="series-chip">
              <strong>RunCN</strong>
              <span>China marathon travel stories, connected through region maps and city dots.</span>
            </div>
            <div class="series-chip">
              <strong>RunWorld</strong>
              <span>Global marathon routes outside the U.S. and mainland China.</span>
            </div>
          </div>
        </div>

        <div class="map-board" aria-label="Run50 and RunCN maps">
          <a class="run-map-card" href="#run50-series">
            <div>
              <div class="eyebrow">Interactive Map</div>
              <h2>Run50 · U.S. 50 States Map</h2>
              <p>The same U.S. story map from the Chinese edition, with completed states, city dots, and English story links in one place.</p>
            </div>
            <div class="map-window" id="run50-us-map-mini" aria-label="Run50 U.S. map"></div>
            <div class="map-foot"><span id="us-map-mini-status">Click a state or city dot to choose a story</span><b>35 States</b></div>
          </a>

          <a class="run-map-card" id="runcn-map" href="#runcn-series">
            <div>
              <div class="eyebrow">Interactive Map</div>
              <h2>RunCN · China Marathon Map</h2>
              <p>China marathon stories collected on one map, with highlighted provinces, regions, and city markers.</p>
            </div>
            <div class="map-window" id="runcn-china-map-mini" aria-label="RunCN China map" data-map-locale="en"></div>
            <div class="map-foot"><span id="cn-map-mini-status">Click a region or city dot to choose a story</span><b>18 Regions</b></div>
          </a>
        </div>
      </section>

      <section class="ticker" id="featured" aria-label="Featured Run50 stories">
        {''.join(f'<a class="ticker-item" href="https://zhennanzhang.com/run50/wechat-en/{card.slug}-modern-rail.html?v={VERSION}"><small>{html.escape(story_number(card, i + 1))}</small><b>{html.escape(card.title)}</b></a>' for i, card in enumerate((buckets["run50"][:1] + buckets["run50"][18:20] + buckets["run50"][24:25])[:4]))}
      </section>

"""
    stats = f"""      <section class="stats" id="stats" aria-label="Run50 statistics">
        <div class="stat-card"><b>{len(cards)}</b><span>Total stories</span></div>
        <div class="stat-card"><b>{len(buckets['run50'])}</b><span>Run50 stories</span></div>
        <div class="stat-card"><b>{len(buckets['runcn'])}</b><span>RunCN stories</span></div>
        <div class="stat-card"><b>{len(buckets['runworld'])}</b><span>RunWorld stories</span></div>
      </section>
"""
    start = base.find('      <section class="hero hero-board" id="score">')
    end = base.find('      <section class="stats" id="stats"', start)
    stats_end = base.find('  <footer>', end)
    if start >= 0 and end >= 0 and stats_end >= 0:
        base = base[:start] + hero_and_ticker + sections + stats + base[stats_end:]
    base = re.sub(r'<html lang="zh-CN">', '<html lang="en">', base, count=1)
    base = re.sub(r"<title>.*?</title>", "<title>Run50 WeChat English</title>", base, count=1, flags=re.S)
    base = base.replace("Run50 微信故事新版", "Run50 WeChat English")
    base = base.replace("微信公众号版", "WeChat English")
    base = base.replace("美国50州", "U.S. States")
    base = base.replace("中国马拉松", "China Marathons")
    base = base.replace("世界跑旅", "Global Routes")
    base = base.replace("文章与进度", "Stories & Progress")
    base = base.replace('href="https://zhennanzhang.com/run50/wechat/">WeChat</a>', 'href="https://zhennanzhang.com/run50/wechat/">Chinese WeChat</a>')
    base = base.replace('href="https://zhennanzhang.com/run50/wechat-new/"><span class="dot"></span>微信故事新版</a>', f'href="https://zhennanzhang.com/run50/wechat-en/?v={VERSION}"><span class="dot"></span>WeChat English</a>')
    base = base.replace("Chinese Stories", "Chinese Stories")
    base = base.replace("English Stories", "English Stories")
    base = base.replace("Facebook", "Facebook")
    base = base.replace("../us-map-svg.js?v=20260630-mini-maps", f"../us-map-svg.js?v={VERSION}")
    base = base.replace("../china-map-svg.js?v=20260630-mini-maps", f"../china-map-svg.js?v={VERSION}")
    base = base.replace('<!-- saved from url=(0055)#score -->\n', "")
    base = translate_wechat_new_script_text(base)
    base = base.replace("</body>", english_mini_map_localizer_script() + "</body>")
    return "\n".join(line.rstrip() for line in base.splitlines()) + "\n"

    # Legacy standalone English layout kept below as reference. The function
    # returns earlier so the public page uses the WeChat New layout exactly.
    def section(key: str, kicker: str, title: str, intro: str) -> str:
        body = "\n".join(render_card(c) for c in buckets[key])
        return f"""
    <section class="story-section {key}-zone" id="{key}-series">
      <div class="section-head">
        <p class="section-kicker">{kicker}</p>
        <h2>{title}</h2>
        <p>{intro}</p>
      </div>
      <div class="story-grid">{body}
      </div>
    </section>"""
    return f"""<!doctype html>
<html lang="en" data-theme="dark">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Run50 WeChat English | Arsenan</title>
  <meta name="description" content="Conversational English WeChat-style editions of the Run50, RunCN, and RunWorld marathon stories.">
  <script>
    try {{
      if (localStorage.getItem('run50-wechat-en-theme') === 'light') {{
        document.documentElement.dataset.theme = 'light';
      }}
    }} catch (error) {{}}
  </script>
  <link rel="stylesheet" href="./wechat-en.css?v={VERSION}">
</head>
<body>
  <button class="theme-toggle" type="button" aria-label="Toggle theme">Light</button>
  <header class="masthead">
    <nav class="top-nav">
      <a href="../index.html">Run50</a>
      <a href="../wechat-new/?v=20260630-rail-align">Chinese Edition</a>
      <a href="../facebook/">Facebook</a>
      <a href="../stories/english/">English Stories</a>
    </nav>
    <p class="brand">RUN50 · WECHAT ENGLISH</p>
    <h1>Marathon stories, rewritten for American friends.</h1>
    <p class="intro">A conversational English edition of the WeChat series: race-day first, travel notes after, with local phrasing that reads naturally in the U.S.</p>
    <div class="quick-links">
      <a href="#run50-series">Run50</a>
      <a href="#runcn-series">RunCN</a>
      <a href="#runworld-series">RunWorld</a>
    </div>
  </header>
  <main class="shell">
{section("run50", "RUN50 · U.S. STATES", "U.S. Marathon Series", "The state-by-state Run50 marathon stories, in the same order as the WeChat Chinese edition.")}
{section("runcn", "RUNCN · CHINA ROUTES", "China Marathon Series", "RunCN stories with English covers, English copy, and China-map snapshots for each province or region.")}
{section("runworld", "RUNWORLD · GLOBAL ROUTES", "World Marathon Series", "Runs outside the U.S. and mainland China, kept in the same card layout as the other sections.")}
  </main>
  <script>
    const button = document.querySelector('.theme-toggle');
    function syncThemeButton() {{
      button.textContent = document.documentElement.dataset.theme === 'light' ? 'Dark' : 'Light';
    }}
    syncThemeButton();
    button.addEventListener('click', () => {{
      const next = document.documentElement.dataset.theme === 'light' ? 'dark' : 'light';
      document.documentElement.dataset.theme = next;
      localStorage.setItem('run50-wechat-en-theme', next);
      syncThemeButton();
    }});
  </script>
</body>
</html>
"""


def css_text() -> str:
    return """*{box-sizing:border-box}html{color-scheme:dark}html[data-theme=light]{color-scheme:light}body{margin:0;background:#0b1020;color:#dbe7f6;font-family:Inter,"Segoe UI",Arial,sans-serif;line-height:1.72;letter-spacing:0}a{color:inherit}.theme-toggle{position:fixed;right:16px;top:14px;z-index:20;border:1px solid rgba(255,255,255,.18);border-radius:999px;padding:8px 12px;background:rgba(15,23,42,.82);color:#f8fbff;font-weight:850;font-size:12px;box-shadow:0 10px 28px rgba(0,0,0,.28);cursor:pointer}.masthead{width:min(1180px,calc(100% - 32px));margin:0 auto;padding:28px 0 38px}.top-nav{display:flex;gap:12px;justify-content:flex-end;flex-wrap:wrap;margin:0 0 38px}.top-nav a,.quick-links a,.wechat-en-nav a{border:1px solid rgba(148,163,184,.28);border-radius:999px;padding:8px 12px;text-decoration:none;color:#c9d7eb;background:rgba(255,255,255,.05);font-size:13px;font-weight:800}.brand,.section-kicker,.kicker,.note-label{margin:0 0 10px;color:#7dd3fc;font-size:13px;font-weight:950;letter-spacing:.1em;text-transform:uppercase}.masthead h1{max-width:900px;margin:0;font-family:Georgia,"Times New Roman",serif;font-size:clamp(42px,7vw,88px);line-height:.95;letter-spacing:0}.intro{max-width:780px;margin:20px 0 0;color:#b6c5d8;font-size:20px}.quick-links{display:flex;gap:10px;flex-wrap:wrap;margin-top:26px}.shell{width:min(1180px,calc(100% - 32px));margin:0 auto;padding:0 0 80px}.story-section{margin-top:58px}.story-section:first-child{margin-top:0}.section-head{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:18px;align-items:end;margin:0 0 22px;padding:0 0 18px;border-bottom:1px solid rgba(148,163,184,.22)}.section-head h2{grid-column:1;margin:0;color:#f8fbff;font-size:clamp(26px,4vw,42px);line-height:1.05}.section-head p:last-child{grid-column:1/-1;max-width:760px;margin:0;color:#a8b7cc}.story-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:24px;align-items:stretch}.story-card{display:grid;grid-template-rows:auto 1fr;overflow:hidden;min-height:100%;border:1px solid rgba(148,163,184,.22);border-radius:8px;background:#1b2437;text-decoration:none;box-shadow:0 18px 44px rgba(0,0,0,.22);transition:transform .18s ease,border-color .18s ease,box-shadow .18s ease}.story-card:hover{transform:translateY(-3px);border-color:rgba(248,220,138,.7);box-shadow:0 24px 60px rgba(0,0,0,.32)}.story-card img{display:block;width:100%;aspect-ratio:16/10;object-fit:cover;background:#10192c}.story-card-body{padding:18px 18px 20px;display:grid;align-content:start}.story-meta{margin:0 0 8px;color:#9ddfbd;font-size:12px;font-weight:900;letter-spacing:.08em;text-transform:uppercase}.story-title{margin:0;color:#f8fbff;font-size:20px;line-height:1.28}.story-desc{margin:12px 0 0;color:#b6c5d8;font-size:15px;line-height:1.62}.story-foot{margin:18px 0 0;color:#f8dc8a;font-weight:900}.run-cn .story-meta{color:#a7f3d0}.run-world .story-meta{color:#7dd3fc}html[data-theme=light] body{background:#f5f7fb;color:#17212b}html[data-theme=light] .masthead h1,html[data-theme=light] .section-head h2,html[data-theme=light] .story-title{color:#101828}html[data-theme=light] .intro,html[data-theme=light] .section-head p:last-child,html[data-theme=light] .story-desc{color:#526170}html[data-theme=light] .story-card{background:#fff;border-color:#d9e2ec;box-shadow:0 18px 44px rgba(15,23,42,.08)}html[data-theme=light] .top-nav a,html[data-theme=light] .quick-links a,html[data-theme=light] .wechat-en-nav a{color:#344054;background:#fff;border-color:#d9e2ec}.wechat-en-page{width:min(677px,100%);margin:0 auto;padding:28px 18px 58px;background:#0b1020}.wechat-en-nav{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 22px}.wechat-en-header{padding:16px 0 18px;border-top:4px solid #2f855a;border-bottom:1px solid rgba(125,211,252,.34)}.wechat-en-header h1{margin:0;color:#f8fbff;font-size:clamp(30px,7vw,46px);line-height:1.12;letter-spacing:0}.dek{margin:14px 0 0;color:#b6c5d8;font-size:16px;line-height:1.7}.meta-row{display:flex;gap:8px;flex-wrap:wrap;margin-top:15px}.meta-row span{border:1px solid rgba(125,211,252,.26);border-radius:999px;padding:6px 10px;color:#a8b7cc;font-size:12px;font-weight:800}.opening-note{margin:24px 0 28px;padding:16px 18px;border:1px solid rgba(248,220,138,.42);border-radius:6px;background:#131d31}.opening-note p:last-child{margin:0;color:#dbe7f6}.cover-block{margin:24px 0 30px}.cover-block img,.wechat-en-article figure img{display:block;width:100%;height:auto;border-radius:7px}.wechat-en-article{background:transparent;color:#dbe7f6}.wechat-en-article p{margin:0 0 18px;font-size:16px;line-height:1.95;text-align:left}.wechat-en-article figure{margin:28px 0 30px}.wechat-en-article figcaption{margin:9px 0 0;padding-left:10px;border-left:3px solid #d4a669;color:#a8b7cc;font:italic 12px/1.65 Optima,Georgia,serif}.field-note-head{margin:44px 0 18px;padding:0 0 0 14px;border-left:5px solid #2f855a}.field-note-head p{margin:0 0 5px!important;color:#8a9bad!important;font-size:11px!important;line-height:1.4!important;letter-spacing:1.6px;font-weight:900;text-align:left}.field-note-head h2{margin:0;color:#f8fbff;font-size:22px;line-height:1.35;letter-spacing:0}.wechat-en-credits{margin:34px 0 0;text-align:center}.wechat-en-credits p{margin:10px 0!important;text-align:center!important;color:#c8d5e7!important;font-weight:800}.zz-engagement{margin:32px 0 0}.zz-engagement-shell{border:1px solid rgba(148,163,184,.25);border-radius:8px;background:#10192c;padding:18px}.zz-engagement-kicker{margin:0 0 6px;color:#7dd3fc;font-weight:900}.zz-engagement h2{margin:0 0 8px}.zz-engagement-note{color:#a8b7cc}.zz-engagement-stats{display:flex;gap:10px;flex-wrap:wrap}.zz-engagement-stat{display:inline-flex;gap:8px;align-items:center;border:1px solid rgba(148,163,184,.25);border-radius:999px;padding:7px 11px;color:#c8d5e7}html[data-theme=light] .wechat-en-page{background:#fff}html[data-theme=light] .wechat-en-header h1,html[data-theme=light] .field-note-head h2{color:#162636}html[data-theme=light] .dek,html[data-theme=light] .meta-row span,html[data-theme=light] .wechat-en-article p{color:#26343f}html[data-theme=light] .opening-note{background:#edf5f8;border-color:#d8e6ee}html[data-theme=light] .opening-note p:last-child{color:#26343f}html[data-theme=light] .zz-engagement-shell{background:#fff;border-color:#d9e2ec}@media(max-width:700px){.section-head{grid-template-columns:1fr}.story-grid{grid-template-columns:1fr}.masthead{padding-top:22px}.top-nav{justify-content:flex-start;margin-bottom:26px}.wechat-en-page{padding-inline:16px}.wechat-en-article p{font-size:16px;line-height:1.86}}"""


def article_extra_css() -> str:
    return """
.wechat-en-article strong.auto-emphasis{font-weight:900;padding:0 .05em;border-radius:4px;text-shadow:0 0 16px color-mix(in srgb,var(--emphasis-color,#f8dc8a) 24%,transparent)}
.wechat-en-article strong.auto-emphasis.accent-0{--emphasis-color:#7dd3fc;color:#7dd3fc}
.wechat-en-article strong.auto-emphasis.accent-1{--emphasis-color:#f8dc8a;color:#f8dc8a}
.wechat-en-article strong.auto-emphasis.accent-2{--emphasis-color:#a7f3d0;color:#a7f3d0}
.wechat-en-article strong.auto-emphasis.accent-3{--emphasis-color:#f0a6ca;color:#f0a6ca}
.wechat-en-article strong.auto-emphasis.accent-4{--emphasis-color:#c4f08a;color:#c4f08a}
html[data-theme=light] .wechat-en-article strong.auto-emphasis.accent-0{color:#0b67c2}
html[data-theme=light] .wechat-en-article strong.auto-emphasis.accent-1{color:#8a5a00}
html[data-theme=light] .wechat-en-article strong.auto-emphasis.accent-2{color:#087857}
html[data-theme=light] .wechat-en-article strong.auto-emphasis.accent-3{color:#9b2f62}
html[data-theme=light] .wechat-en-article strong.auto-emphasis.accent-4{color:#437314}
.wechat-finish-line{margin:36px 0 0;padding:20px 18px 22px;border:1px solid rgba(248,220,138,.35);border-radius:8px;background:linear-gradient(135deg,#10192c 0,#16233a 62%,#10192c 100%);box-shadow:0 18px 44px rgba(0,0,0,.22)}
.finish-kicker{margin:0 0 8px;color:#f8dc8a;font-size:12px;font-weight:950;letter-spacing:.12em;text-transform:uppercase}
.wechat-finish-line h2{margin:0;color:#f8fbff;font-size:24px;line-height:1.25}
.finish-chips{display:flex;flex-wrap:wrap;gap:8px;margin:14px 0}
.finish-chips span{border:1px solid rgba(125,211,252,.24);border-radius:999px;padding:6px 10px;color:#b6c5d8;font-size:12px;font-weight:850}
.wechat-finish-line p{margin:12px 0 0;color:#dbe7f6;line-height:1.75}
.wechat-finish-line .finish-note{color:#a8b7cc;font-style:italic}
html[data-theme=light] .wechat-finish-line{background:#edf5f8;border-color:#d8e6ee;box-shadow:0 18px 44px rgba(15,23,42,.08)}
html[data-theme=light] .wechat-finish-line h2{color:#162636}
html[data-theme=light] .wechat-finish-line p{color:#26343f}
html[data-theme=light] .finish-chips span{color:#526170;border-color:#d0dbe8}
"""


def main() -> None:
    cards = build_cards()
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    write(OUT / "wechat-en.css", css_text() + article_extra_css())
    write(OUT / "index.html", index_page(cards))
    for card in cards:
        write(OUT / f"{card.slug}-modern-rail.html", article_page(card))
    print(f"Built {len(cards)} WeChat English articles in {OUT}")


if __name__ == "__main__":
    main()
