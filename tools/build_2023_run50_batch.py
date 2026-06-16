from __future__ import annotations

from dataclasses import dataclass
from html import escape
from pathlib import Path
import json
import re
import shutil
import tempfile
import time
import urllib.parse
import urllib.request

from lxml import html
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps


REPO = Path(__file__).resolve().parents[1]
SOURCE_ROOT = Path(r"Z:\ZhennanZ Folder\000-Marathon-Story-2024-2025\20230000-Marathons")
SITE = "https://arsenanzz.github.io/ZZ"
VERSION = "20260616-2"
ENGAGEMENT_VERSION = "20260616"
TRANSLATION_CACHE = Path(tempfile.gettempdir()) / "zz_run50_2023_batch_translation_cache.json"
FONT_DIR = Path(r"C:\Windows\Fonts")


@dataclass(frozen=True)
class StoryConfig:
    folder: str
    slug: str
    image_dir: str
    medal_name: str
    run_no: str
    state_abbr: str
    state_en: str
    state_zh: str
    city_en: str
    city_zh: str
    race_en: str
    race_zh: str
    date_iso: str
    date_en: str
    date_zh: str
    title_zh: str
    title_en: str
    title_fb: str
    deck_zh: str
    deck_en: str
    fb_dek: str
    cover_title: str
    cover_subtitle: str
    card_title_en: str
    card_desc_en: str
    card_title_zh: str
    card_desc_zh: str
    fb_card_desc: str
    fb_meta_note: str
    root_marker: str
    scene: str
    route_memory: str
    medal_hint: str | None = None


STORIES = [
    StoryConfig(
        folder="2023-State-01-KY",
        slug="kentucky-derby-marathon",
        image_dir="Run50-Kentucky-Derby-Marathon-clean_files",
        medal_name="cover-medal-ky-derby.jpg",
        run_no="01+",
        state_abbr="KY",
        state_en="Kentucky",
        state_zh="肯塔基",
        city_en="Louisville",
        city_zh="路易斯维尔",
        race_en="Kentucky Derby Festival Marathon",
        race_zh="肯塔基德比马拉松",
        date_iso="2023.04.29",
        date_en="Apr 29, 2023",
        date_zh="2023.04.29",
        title_zh="Run50 #第1州番外｜肯塔基：路易斯维尔德比马拉松｜赛马城最大的跑步 Party",
        title_en="Run50 #1 Revisit | Kentucky: Louisville's Derby Marathon",
        title_fb="Louisville turned Derby season into the city's biggest running party",
        deck_zh="回到自己的城市，补上肯塔基德比马拉松这一篇：赛马、Twin Spires、市中心、朋友们和路城最大的跑步 Party。",
        deck_en="Back in my own city for the Kentucky Derby Festival Marathon: horse-racing season, Twin Spires, downtown Louisville, running friends, and the city's biggest running party.",
        fb_dek="On April 29, 2023, Louisville's Derby season became a marathon morning: a hometown course, Churchill Downs energy, friends on the road, and a reminder that Run50 also has local chapters worth saving.",
        cover_title="LOUISVILLE",
        cover_subtitle="DERBY CITY · TWIN SPIRES · RUNNING PARTY",
        card_title_en="Kentucky Derby Marathon: Louisville's biggest running party",
        card_desc_en="A hometown Run50 revisit through Derby season, downtown Louisville, Churchill Downs spirit, old friends, and a city that knows how to turn race weekend into a party.",
        card_title_zh="Run50 #第1州番外｜肯塔基德比马拉松",
        card_desc_zh="回到路易斯维尔自己的主场，补上德比马拉松这一篇：赛马城、Twin Spires、市中心、朋友们和一场真正属于本地人的跑步 Party。",
        fb_card_desc="Race date: April 29, 2023. A hometown Derby-season marathon in Louisville, with horse-racing energy, city streets, friends, and one more Kentucky chapter.",
        fb_meta_note="Derby season",
        root_marker="Kentucky Derby 2023 Run50 story",
        scene="derby",
        route_memory="Louisville streets, Derby season, Churchill Downs motifs, and the city's running community.",
        medal_hint="640(95)",
    ),
    StoryConfig(
        folder="2023-State-02-OH",
        slug="cincinnati-flying-pig-marathon",
        image_dir="Run50-Cincinnati-Flying-Pig-Marathon-clean_files",
        medal_name="cover-medal-oh-flying-pig.jpg",
        run_no="02+",
        state_abbr="OH",
        state_en="Ohio",
        state_zh="俄亥俄",
        city_en="Cincinnati",
        city_zh="辛辛那提",
        race_en="Flying Pig Marathon",
        race_zh="辛辛那提飞猪马拉松",
        date_iso="2023.05.07",
        date_en="May 7, 2023",
        date_zh="2023.05.07",
        title_zh="Run50 #第2州番外｜俄亥俄：辛辛那提飞猪马拉松｜飞猪变飞鱼",
        title_en="Run50 #2 Revisit | Ohio: Cincinnati Flying Pig Marathon",
        title_fb="Cincinnati's Flying Pig turned into a Flying Fish in the rain",
        deck_zh="第二次在俄亥俄跑全马，这次来到皇后城辛辛那提：桥、河、坡、雨水，以及从 Flying Pig 变成 Flying Fish 的一天。",
        deck_en="A second Ohio marathon, this time in Cincinnati: Queen City bridges, river hills, heavy rain, and the day the Flying Pig became a Flying Fish.",
        fb_dek="On May 7, 2023, Cincinnati's Flying Pig Marathon delivered the kind of wet, hilly, full-city race that makes a brand stick: bridge crossings, Queen City climbs, and rain that turned the pig into a fish.",
        cover_title="CINCINNATI",
        cover_subtitle="FLYING PIG · QUEEN CITY · RIVER BRIDGES",
        card_title_en="Flying Pig Marathon: Queen City bridges and a rain-soaked finish",
        card_desc_en="A second Ohio marathon through Cincinnati's river city: flying-pig branding, bridges, hills, rain, and a race that somehow became even more memorable when it got wet.",
        card_title_zh="Run50 #第2州番外｜辛辛那提飞猪马拉松",
        card_desc_zh="在皇后城再跑一次俄亥俄：飞猪、俄亥俄河、城市坡道和一场湿透的比赛，让 Flying Pig 变成了 Flying Fish。",
        fb_card_desc="Race date: May 7, 2023. Cincinnati's Flying Pig Marathon brought bridges, hills, rain and a full Queen City tour.",
        fb_meta_note="Flying Pig",
        root_marker="Cincinnati Flying Pig 2023 Run50 story",
        scene="pig",
        route_memory="Queen City streets, Ohio River bridges, rolling climbs, and a rainy Flying Pig finish.",
        medal_hint="640(84)",
    ),
    StoryConfig(
        folder="2023-State-07-GA",
        slug="atlanta-marathon",
        image_dir="Run50-Atlanta-Marathon-clean_files",
        medal_name="cover-medal-ga.jpg",
        run_no="07",
        state_abbr="GA",
        state_en="Georgia",
        state_zh="佐治亚",
        city_en="Atlanta",
        city_zh="亚特兰大",
        race_en="Publix Atlanta Marathon",
        race_zh="亚特兰大马拉松",
        date_iso="2023.02.26",
        date_en="Feb 26, 2023",
        date_zh="2023.02.26",
        title_zh="Run50 #第7州｜佐治亚：亚特兰大马拉松｜跑过奥运五环",
        title_en="Run50 #7 | Georgia: Atlanta Marathon and the Olympic Rings",
        title_fb="Atlanta made 26.2 miles feel like an Olympic city walk",
        deck_zh="Run50 第7州来到亚特兰大：96奥运、可口可乐、CNN、城市坡道，以及我和47各自的26.2与13.1。",
        deck_en="Run50 State 7 in Atlanta: the 1996 Olympics, Coca-Cola, CNN, city hills, and a 26.2-plus-13.1 weekend for me and 47.",
        fb_dek="On February 26, 2023, Atlanta gave Run50 State 7 a full-city feel: Olympic rings, Coca-Cola and CNN landmarks, rolling streets, and a weekend road trip built around 26.2 and 13.1 miles.",
        cover_title="ATLANTA",
        cover_subtitle="OLYMPIC RINGS · PEACHTREE · CNN",
        card_title_en="Atlanta Marathon: Olympic rings, hills, and a 16-hour road trip",
        card_desc_en="A Georgia marathon weekend with Chattanooga on the way, Olympic city landmarks, Coca-Cola, CNN, rolling Atlanta streets, and the shared rhythm of 26.2 and 13.1.",
        card_title_zh="Run50 #第7州｜亚特兰大马拉松",
        card_desc_zh="为了点亮佐治亚，自驾16小时往返亚特兰大：96奥运之城、CNN、可口可乐、城市坡道，以及26.2和13.1的周末。",
        fb_card_desc="Race date: February 26, 2023. State 7 of Run50 in Atlanta: Olympic rings, Coca-Cola, CNN, hills, and a long road-trip weekend.",
        fb_meta_note="Olympic city",
        root_marker="Atlanta 2023 Run50 story",
        scene="atlanta",
        route_memory="Centennial Olympic Park, downtown Atlanta, rolling streets, and a city built around Olympic memory.",
    ),
    StoryConfig(
        folder="2023-State-08-CO",
        slug="denver-colfax-marathon",
        image_dir="Run50-Denver-Colfax-Marathon-clean_files",
        medal_name="cover-medal-co.jpg",
        run_no="08",
        state_abbr="CO",
        state_en="Colorado",
        state_zh="科罗拉多",
        city_en="Denver",
        city_zh="丹佛",
        race_en="Denver Colfax Marathon",
        race_zh="丹佛 Colfax 马拉松",
        date_iso="2023.05.21",
        date_en="May 21, 2023",
        date_zh="2023.05.21",
        title_zh="Run50 #第8州｜科罗拉多：丹佛 Colfax 马拉松｜里高城的26.2英里",
        title_en="Run50 #8 | Colorado: Denver Colfax Marathon in the Mile High City",
        title_fb="Denver gave me 26.2 Mile High miles, stadium grass and mountain light",
        deck_zh="生日后的第一个周末，去丹佛点亮科罗拉多：老同学、阳光、雪山、球场，以及里高城的26.2英里。",
        deck_en="The first weekend after my birthday became a Colorado trip: an old classmate, Denver sunshine, mountain light, stadium grass, and 26.2 Mile High miles.",
        fb_dek="On May 21, 2023, Denver's Colfax Marathon turned Run50 State 8 into a high-altitude city tour: sunshine, mountain views, stadium grass, long avenues, and a birthday-adjacent Colorado weekend.",
        cover_title="DENVER",
        cover_subtitle="MILE HIGH · COLFAX · ROCKY MOUNTAINS",
        card_title_en="Denver Colfax Marathon: 26.2 Mile High miles",
        card_desc_en="A Colorado weekend built around old friends, Denver sun, Rocky Mountain light, stadium miles, and the thin-air rhythm of the Colfax Marathon.",
        card_title_zh="Run50 #第8州｜丹佛 Colfax 马拉松",
        card_desc_zh="生日后的周末去里高城点亮科罗拉多：老同学请饭、丹佛阳光、雪山远景、球场草地和高海拔的26.2英里。",
        fb_card_desc="Race date: May 21, 2023. State 8 of Run50 in Denver: Colfax, stadium grass, mountain light and Mile High air.",
        fb_meta_note="Mile High",
        root_marker="Denver Colfax 2023 Run50 story",
        scene="denver",
        route_memory="Colfax Avenue, Denver sunshine, stadium grass, mountain light, and high-altitude miles.",
        medal_hint="640(137)",
    ),
    StoryConfig(
        folder="2023-State-09-AK",
        slug="anchorage-marathon",
        image_dir="Run50-Anchorage-Marathon-clean_files",
        medal_name="cover-medal-ak.jpg",
        run_no="09",
        state_abbr="AK",
        state_en="Alaska",
        state_zh="阿拉斯加",
        city_en="Anchorage",
        city_zh="安克雷奇",
        race_en="Anchorage Mayor's Marathon",
        race_zh="安克雷奇市长马拉松",
        date_iso="2023.06.17",
        date_en="Jun 17, 2023",
        date_zh="2023.06.17",
        title_zh="Run50 #第9州｜阿拉斯加：安克雷奇马拉松｜去没有极光的阿拉斯加",
        title_en="Run50 #9 | Alaska: Anchorage Marathon Without the Aurora",
        title_fb="Alaska had no aurora, but Anchorage still gave me a wild 26.2 miles",
        deck_zh="Run50 第9州飞到阿拉斯加：没有极光，却有雪山、海湾、野性、夏至前后的长日照和安克雷奇的26.2英里。",
        deck_en="Run50 State 9 in Alaska: no aurora this time, but mountains, water, wild edges, solstice light, and 26.2 miles through Anchorage.",
        fb_dek="On June 17, 2023, Anchorage made Run50 State 9 feel far from ordinary: no northern lights, but long summer daylight, Alaska mountains, coastal trails, wild scenery and a marathon that felt bigger than the city.",
        cover_title="ANCHORAGE",
        cover_subtitle="ALASKA · COASTAL TRAIL · MIDNIGHT SUN",
        card_title_en="Anchorage Marathon: Alaska without the aurora",
        card_desc_en="A summer-solstice Alaska story: no northern lights, but mountains, coastal trails, wild scenery, long daylight, local runners and the kind of trip that makes the map feel larger.",
        card_title_zh="Run50 #第9州｜安克雷奇马拉松",
        card_desc_zh="去没有极光的阿拉斯加，跑一次安克雷奇马拉松：雪山、海湾、野性、长日照，以及一次把地图拉得更远的旅行。",
        fb_card_desc="Race date: June 17, 2023. State 9 of Run50 in Anchorage: no aurora, but Alaska mountains, coastal trails and summer-solstice light.",
        fb_meta_note="Alaska light",
        root_marker="Anchorage 2023 Run50 story",
        scene="alaska",
        route_memory="Anchorage trails, coastal views, summer light, mountains, and Alaska's wild edge.",
        medal_hint="640(166)",
    ),
    StoryConfig(
        folder="2023-State-10-MO",
        slug="st-joseph-marathon",
        image_dir="Run50-St-Joseph-Marathon-clean_files",
        medal_name="cover-medal-mo.jpg",
        run_no="10",
        state_abbr="MO",
        state_en="Missouri",
        state_zh="密苏里",
        city_en="St. Joseph",
        city_zh="圣约瑟夫",
        race_en="St. Joseph Missouri Marathon",
        race_zh="圣约瑟夫马拉松",
        date_iso="2023.09.23",
        date_en="Sep 23, 2023",
        date_zh="2023.09.23",
        title_zh="Run50 #第10州｜密苏里：圣约瑟夫马拉松｜第一届，不一般",
        title_en="Run50 #10 | Missouri: The Inaugural St. Joseph Marathon",
        title_fb="St. Joseph made Missouri feel like a first-edition marathon road trip",
        deck_zh="穿越密苏里，来到西北角的圣约瑟夫：第一届赛事、公园道路、坡、热浪、婚礼，以及芝加哥前的一次长距离训练。",
        deck_en="Crossing Missouri to St. Joseph: an inaugural race, parkways, hills, heat, a wedding, and one long-distance tune-up before Chicago.",
        fb_dek="On September 23, 2023, the inaugural St. Joseph Missouri Marathon became Run50 State 10: a cross-Missouri drive, civic-park start, rolling parkways, late heat, and a weekend folded into friends and wedding memories.",
        cover_title="ST. JOSEPH",
        cover_subtitle="MISSOURI · PARKWAYS · INAUGURAL RACE",
        card_title_en="St. Joseph Marathon: the first edition across Missouri",
        card_desc_en="A Missouri road-trip marathon before Chicago: long drive, inaugural race energy, parkways, heat, hills, friends, and a wedding weekend at the end.",
        card_title_zh="Run50 #第10州｜圣约瑟夫马拉松",
        card_desc_zh="穿越密苏里去跑第一届圣约瑟夫马拉松：公园道路、坡、热浪、婚礼，以及芝加哥前的一次长距离训练。",
        fb_card_desc="Race date: September 23, 2023. State 10 of Run50 at the inaugural St. Joseph Missouri Marathon: parkways, heat, hills and a wedding weekend.",
        fb_meta_note="Inaugural race",
        root_marker="St Joseph 2023 Run50 story",
        scene="missouri",
        route_memory="St. Joseph parkways, civic center start, rolling hills, late heat, and inaugural-race energy.",
        medal_hint="640(118)",
    ),
]


SPECIAL_TRANSLATIONS = {
    "前言": "Preface",
    "后记": "Postscript",
    "- 本文完 -": "- End -",
    "文字丨Arsenan": "Words | Arsenan",
    "摄影丨Arsenan": "Photos | Arsenan",
    "设计丨Arsenan": "Design | Arsenan",
}


def norm(value: str) -> str:
    return re.sub(r"\s+", " ", value.replace("\xa0", " ").replace("\u200b", "").replace("\u200d", "")).strip()


def clean_story_text(text: str) -> str:
    text = norm(text)
    replacements = {
        "Offical": "Official",
        "Vechile": "Vehicle",
        "Menorial": "Memorial",
        "St Joseph": "St. Joseph",
        "St.Joseph": "St. Joseph",
        "Cincinnati Flying Pig Marathon": "Cincinnati Flying Pig Marathon",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


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


def is_story_image(src: str) -> bool:
    name = Path(src.split("#", 1)[0].split("?", 1)[0].replace("\\", "/")).name
    return name.startswith("640")


def local_source_path(path: Path, src: str) -> Path:
    normalized = src.split("#", 1)[0].split("?", 1)[0].replace("\\", "/")
    if normalized.startswith("./"):
        normalized = normalized[2:]
    candidate = path.parent / normalized
    if candidate.exists():
        return candidate
    candidate = files_dir_for(path) / Path(normalized).name
    if candidate.exists():
        return candidate
    raise FileNotFoundError(f"Could not map image source {src!r} for {path.name}")


def should_skip_text(text: str, source_stem: str) -> bool:
    if not text:
        return True
    if text in {"，赞", "0/0", "★", "★★", "★★★", "★★★★", "继续观看", source_stem}:
        return True
    if text.startswith("鲜花"):
        return True
    return False


def extract_story(config: StoryConfig) -> list[dict]:
    source_dir = SOURCE_ROOT / config.folder
    source_html = next(source_dir.glob("*.html"))
    doc = html.fromstring(source_html.read_text(encoding="utf-8", errors="replace"))
    roots = doc.xpath('//*[@id="js_content"]')
    root = roots[0] if roots else doc
    events: list[dict] = []

    def walk(el):
        if not isinstance(el.tag, str):
            return
        if el.tag == "img":
            src = el.get("src") or el.get("data-src") or ""
            if src and is_story_image(src):
                events.append({"type": "image", "source": local_source_path(source_html, src)})
            return
        if el.tag in ("p", "section"):
            text = clean_story_text("".join(el.itertext()))
            if text and not is_styleish(text) and not has_desc_leaf_container(el):
                if not should_skip_text(text, source_html.stem):
                    events.append({"type": "text", "text": text})
                for img in el.xpath(".//img"):
                    src = img.get("src") or img.get("data-src") or ""
                    if src and is_story_image(src):
                        events.append({"type": "image", "source": local_source_path(source_html, src)})
                return
        for child in el:
            walk(child)

    for child in root:
        walk(child)

    deduped = []
    for event in events:
        key = (event["type"], event.get("text") or str(event.get("source")))
        prev = (deduped[-1]["type"], deduped[-1].get("text") or str(deduped[-1].get("source"))) if deduped else None
        if key != prev:
            deduped.append(event)

    start = 0
    for idx, event in enumerate(deduped):
        if event["type"] == "text" and event["text"] == "前言":
            start = idx
            break

    end = len(deduped)
    for idx, event in enumerate(deduped):
        if event["type"] == "text" and event["text"].startswith("设计"):
            end = idx + 1
            break
    return deduped[start:end]


def load_translation_cache() -> dict[str, str]:
    if TRANSLATION_CACHE.exists():
        return json.loads(TRANSLATION_CACHE.read_text(encoding="utf-8"))
    return {}


def save_translation_cache(cache: dict[str, str]) -> None:
    TRANSLATION_CACHE.parent.mkdir(parents=True, exist_ok=True)
    TRANSLATION_CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")


def translation_key(text: str) -> str:
    return text[2:].strip() if text.startswith("# ") else text


def needs_machine_translation(text: str) -> bool:
    if text in SPECIAL_TRANSLATIONS:
        return False
    if re.fullmatch(r"\d{1,2}", text):
        return False
    return True


def polish_translation(text: str) -> str:
    replacements = {
        "competition day": "race day",
        "Competition Day": "Race day",
        "Before the game": "Before the race",
        "after the game": "after the race",
        "number plate": "bib",
        "number book": "bib",
        "entry package": "race packet",
        "receiving package": "packet pickup",
        "Flying Pig Horse": "Flying Pig Marathon",
        "Derby Horse Marathon": "Derby Marathon",
        "Colfax Horse": "Colfax Marathon",
        "Anchorage Horse": "Anchorage Marathon",
        "St. Joseph Horse": "St. Joseph Marathon",
        "horse pull loose": "marathon",
        "horse race runners": "marathon runners",
        "horse racing race": "marathon race",
        "half horse": "half marathon",
        "full horse": "full marathon",
        "Run Fifty": "Run50",
        "Route City": "Louisville",
        "Road City": "Louisville",
        "47": "47",
        "Cincinati": "Cincinnati",
        "Cininnati": "Cincinnati",
        "St Joseph": "St. Joseph",
        "St.Joseph": "St. Joseph",
        "Denfer": "Denver",
        "Ankrech": "Anchorage",
        "Atlanga": "Atlanta",
        "Chattanoaga": "Chattanooga",
        "KFC": "KFC",
        "CNN": "CNN",
        "NBA": "NBA",
        "IMDB": "IMDb",
        "Facebook": "Facebook",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = text.replace(" ,", ",").replace(" .", ".").replace(" !", "!").replace(" ?", "?")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def google_translate_joined(texts: list[str]) -> list[str]:
    if not texts:
        return []
    separators = [f"ZZSEP{i:04d}ZZ" for i in range(1, len(texts))]
    joined = texts[0]
    for sep, text in zip(separators, texts[1:]):
        joined += f"\n{sep}\n{text}"
    query = urllib.parse.urlencode({"client": "gtx", "sl": "zh-CN", "tl": "en", "dt": "t", "q": joined})
    with urllib.request.urlopen("https://translate.googleapis.com/translate_a/single?" + query, timeout=45) as response:
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


def safe_translate_batch(texts: list[str]) -> list[str]:
    try:
        return google_translate_joined(texts)
    except Exception:
        translated = []
        for text in texts:
            translated.extend(google_translate_joined([text]))
            time.sleep(0.15)
        return translated


def ensure_translations(all_events: list[list[dict]]) -> dict[str, str]:
    cache = load_translation_cache()
    missing = []
    for events in all_events:
        for event in events:
            if event["type"] != "text":
                continue
            text = event["text"]
            key = translation_key(text)
            if needs_machine_translation(text) and key not in cache:
                missing.append(key)
    missing = list(dict.fromkeys(missing))
    batch: list[str] = []
    batch_chars = 0
    for key in missing:
        if batch and batch_chars + len(key) > 1300:
            for src, dst in zip(batch, safe_translate_batch(batch)):
                cache[src] = dst
            save_translation_cache(cache)
            batch = []
            batch_chars = 0
            time.sleep(0.12)
        batch.append(key)
        batch_chars += len(key)
    if batch:
        for src, dst in zip(batch, safe_translate_batch(batch)):
            cache[src] = dst
        save_translation_cache(cache)
    return cache


def translate_text(text: str, cache: dict[str, str]) -> str:
    if text in SPECIAL_TRANSLATIONS:
        return SPECIAL_TRANSLATIONS[text]
    if re.fullmatch(r"\d{1,2}", text):
        return text
    value = polish_translation(cache[translation_key(text)])
    if text.startswith("▲") and not value.startswith("▲"):
        value = "▲ " + value.lstrip("▲").strip()
    return value


def is_caption(text: str) -> bool:
    return text.startswith("▲")


def clean_caption(text: str) -> str:
    text = clean_story_text(text)
    text = re.sub(r"^▲\s*", "▲ ", text)
    text = text.replace("@ ", "@")
    return re.sub(r"\s+", " ", text).strip()


def font(size: int, bold: bool = False):
    names = ["arialbd.ttf", "msyhbd.ttc", "simhei.ttf"] if bold else ["arial.ttf", "msyh.ttc"]
    for name in names:
        path = FONT_DIR / name
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def fit_font(draw: ImageDraw.ImageDraw, text: str, max_width: int, start_size: int, min_size: int, bold: bool = True):
    for size in range(start_size, min_size - 1, -2):
        candidate = font(size, bold)
        bbox = draw.textbbox((0, 0), text, font=candidate)
        if bbox[2] - bbox[0] <= max_width:
            return candidate
    return font(min_size, bold)


def copy_story_images(config: StoryConfig, events: list[dict]) -> int:
    out_dir = REPO / "run50" / "stories" / "chinese" / config.image_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    for old in out_dir.glob("img-*.webp"):
        old.unlink()
    image_index = 0
    for event in events:
        if event["type"] != "image":
            continue
        image_index += 1
        out_name = f"img-{image_index:03d}.webp"
        with Image.open(event["source"]) as image:
            image = ImageOps.exif_transpose(image)
            if image.mode != "RGB":
                image = image.convert("RGB")
            image.save(out_dir / out_name, "WEBP", quality=88, method=6)
        event["out"] = out_name
    return image_index


def render_text(text: str, lang: str, cache: dict[str, str]) -> str:
    original = text
    value = clean_story_text(text) if lang == "zh" else translate_text(text, cache)
    if original.startswith("# "):
        value = clean_story_text(original[2:]) if lang == "zh" else value
        return f"<h2>{escape(value)}</h2>"
    if original in {"前言", "后记"}:
        return f'<h2 class="section-label">{escape(value)}</h2>'
    if re.fullmatch(r"\d{1,2}", original):
        return f"<h3>{escape(value)}</h3>"
    if original == "- 本文完 -":
        return f'<p class="end-mark">{escape(value)}</p>'
    if original.startswith(("文字", "摄影", "设计")):
        return f'<p class="credit-line">{escape(value)}</p>'
    if original.startswith(("🏇", "🐠", "🏔", "🛣", "🎽", "📍")):
        return f'<p class="place">{escape(value)}</p>'
    return f"<p>{escape(value)}</p>"


def render_events(config: StoryConfig, events: list[dict], lang: str, image_prefix: str, cache: dict[str, str]) -> str:
    output: list[str] = []
    pending_caption = None
    for event in events:
        if event["type"] == "image":
            number = event["out"].split("-")[1].split(".")[0]
            alt = f"{config.city_en} marathon photo {number}" if lang == "en" else f"{config.city_zh}马拉松照片 {number}"
            figure = (
                f'<figure><img src="{image_prefix}{event["out"]}" alt="{escape(alt)}" '
                f'loading="lazy" decoding="async">'
            )
            if pending_caption:
                figure += f"<figcaption>{escape(pending_caption)}</figcaption>"
                pending_caption = None
            figure += "</figure>"
            output.append(figure)
            continue

        original = event["text"]
        if is_caption(original):
            caption = clean_caption(original) if lang == "zh" else clean_caption(translate_text(original, cache))
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
    return "\n      ".join(output)


BASE_STORY_CSS = """
  :root { color-scheme: light; --ink:#20242b; --muted:#667085; --paper:#edf3f7; --line:#d0dfe8; --blue:#0b67c2; }
  * { box-sizing: border-box; }
  body { margin:0; font-family: Inter, "Segoe UI", Arial, sans-serif; background:#f6f9fb; color:var(--ink); line-height:1.78; }
  a { color:inherit; }
  nav { max-width:1080px; margin:0 auto; padding:22px 20px; display:flex; gap:18px; justify-content:flex-end; font-weight:800; color:#526170; flex-wrap:wrap; }
  .hero { background:linear-gradient(180deg,#e7f1f6,#f6f9fb); border-bottom:1px solid var(--line); }
  .hero-inner { max-width:1080px; margin:0 auto; padding:34px 20px 42px; }
  .eyebrow { color:var(--blue); font-size:13px; font-weight:900; letter-spacing:.08em; text-transform:uppercase; }
  h1 { margin:10px 0 14px; font-family: Georgia, "Times New Roman", serif; font-size:clamp(34px,5vw,64px); line-height:1.04; letter-spacing:0; max-width:940px; }
  .deck { max-width:820px; color:#53606b; font-size:19px; margin:0 0 22px; }
  .meta-row { display:flex; flex-wrap:wrap; gap:10px; margin:22px 0 28px; }
  .meta-row span { border:1px solid var(--line); background:#fff; border-radius:999px; padding:8px 13px; font-size:13px; font-weight:800; color:#344252; }
  .cover { width:100%; max-width:980px; display:block; border-radius:8px; border:1px solid var(--line); box-shadow:0 24px 60px rgba(15,23,42,.12); background:#cfe9f4; }
  main { max-width:860px; margin:0 auto; padding:40px 20px 72px; }
  article { background:#fff; border:1px solid var(--line); border-radius:8px; padding:clamp(22px,4vw,44px); box-shadow:0 18px 48px rgba(15,23,42,.08); }
  article p { margin:0 0 18px; font-size:18px; }
  article h2 { margin:34px 0 14px; font-family: Georgia, "Times New Roman", serif; font-size:32px; line-height:1.2; }
  article h3 { margin:30px 0 10px; color:var(--blue); font-size:18px; letter-spacing:.08em; }
  .section-label { color:var(--blue); font-weight:900; letter-spacing:.08em; text-transform:uppercase; }
  .place { color:#334155; font-weight:800; }
  .credit-line, .end-mark { text-align:center; color:var(--muted); font-weight:800; }
  figure { margin:26px 0; }
  figure img { width:100%; height:auto; display:block; border-radius:8px; border:1px solid #d7e3ea; background:#f4f7f9; }
  figcaption, .caption-line { margin-top:8px; color:#6a7480; font-size:14px; text-align:center; }
  @media (max-width: 620px) {
    nav { justify-content:flex-start; }
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
  .lede { border-left:5px solid var(--blue); padding:14px 0 14px 18px; color:#334155; background:#f0f6fb; }
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


def engagement_block(config: StoryConfig, lang: str) -> str:
    page_key = f"run50-{config.slug}-zh" if lang == "zh" else f"run50-{config.slug}-en"
    comments_id = f"supabase-comments-{config.slug}-{'zh' if lang == 'zh' else 'en'}"
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


def facebook_engagement(config: StoryConfig) -> str:
    return f"""
  <section class="zz-engagement" data-zz-engagement data-locale="en" data-page-key="run50-{config.slug}-facebook-en">
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
        <div id="supabase-comments-{config.slug}-facebook" data-zz-supabase-comments></div>
        <p class="zz-engagement-status" data-zz-engagement-status>Loading comments...</p>
      </div>
    </div>
  </section>
  <script src="../../assets/zz-engagement-config.js?v={ENGAGEMENT_VERSION}"></script>
  <script src="../../assets/zz-engagement.js?v={ENGAGEMENT_VERSION}"></script>
"""


def story_page(config: StoryConfig, lang: str, article: str) -> str:
    is_zh = lang == "zh"
    title = config.title_zh if is_zh else config.title_en
    desc = config.deck_zh if is_zh else config.deck_en
    html_lang = "zh-Hans" if is_zh else "en"
    index_name = "中文故事" if is_zh else "English Stories"
    index_href = "./"
    other_href = f"../english/{config.slug}.html" if is_zh else f"../chinese/{config.slug}.html"
    other_label = "English" if is_zh else "中文"
    eyebrow = f"Run50 #{config.run_no} · {config.state_zh}" if is_zh else f"Run50 #{config.run_no} · {config.state_en}"
    return f"""<!doctype html>
<html lang="{html_lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)}</title>
  <meta name="description" content="{escape(desc)}">
  <meta property="og:title" content="{escape(title)}">
  <meta property="og:description" content="{escape(desc)}">
  <meta property="og:image" content="{SITE}/assets/og-run50-{config.slug}-icons.png?v={VERSION}">
  <meta property="og:type" content="article">
  <link rel="stylesheet" href="../../../assets/zz-engagement.css?v={ENGAGEMENT_VERSION}">
  <style>{BASE_STORY_CSS}</style>
</head>
<body>
  <nav>
    <a href="{index_href}">← {index_name}</a>
    <a href="{other_href}">{other_label}</a>
    <a href="../../facebook/{config.slug}.html">Facebook</a>
    <a href="../../index.html">Run50</a>
  </nav>
  <section class="hero">
    <div class="hero-inner">
      <p class="eyebrow">{escape(eyebrow)}</p>
      <h1>{escape(title)}</h1>
      <p class="deck">{escape(desc)}</p>
      <div class="meta-row"><span>{escape(config.city_en)}, {escape(config.state_en)}</span><span>{config.date_en}</span><span>Run50 #{escape(config.run_no)}</span><span>{escape(config.race_en)}</span></div>
      <img class="cover" src="../../../assets/thumb-run50-{config.slug}-icons.svg?v={VERSION}" alt="{escape(config.city_en)} Marathon icon cover">
    </div>
  </section>
  <main>
    <article>
{article}
    </article>
  </main>
{engagement_block(config, lang)}
</body>
</html>
"""


def facebook_page(config: StoryConfig, article: str) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(config.title_fb)}</title>
  <meta name="description" content="{escape(config.fb_dek)}">
  <meta property="og:title" content="{escape(config.title_fb)}">
  <meta property="og:description" content="{escape(config.fb_dek)}">
  <meta property="og:image" content="{SITE}/assets/og-run50-{config.slug}-icons.png?v={VERSION}">
  <meta property="og:type" content="article">
  <link rel="stylesheet" href="../../assets/zz-engagement.css?v={ENGAGEMENT_VERSION}">
  <style>{FB_CSS}</style>
</head>
<body>
  <header class="topbar">
    <div class="topbar-inner">
      <a class="brand" href="./">RUN50 <span>FACEBOOK</span></a>
      <nav><a href="../hub.html">Run50 Hub</a><a href="../stories/english/{config.slug}.html">English</a><a href="../stories/chinese/{config.slug}.html">中文</a></nav>
    </div>
  </header>
  <section class="hero">
    <p class="eyebrow">World / USA / Marathon</p>
    <h1>{escape(config.title_fb)}</h1>
    <p class="dek">{escape(config.fb_dek)}</p>
    <div class="meta-row"><span>{escape(config.city_en)}, {escape(config.state_abbr)}</span><span>{config.date_en}</span><span>Run50 #{escape(config.run_no)}</span><span>{escape(config.fb_meta_note)}</span></div>
    <img class="lead-cover" src="../../assets/thumb-run50-{config.slug}-icons.svg?v={VERSION}" alt="{escape(config.city_en)} Marathon icon cover">
  </section>
  <main class="layout">
    <article>
      <p class="section-label">Race story</p>
      <p class="lede">{escape(config.fb_dek)}</p>
{article}
    </article>
    <aside class="rail">
      <div class="brief">
        <h2>Race Brief</h2>
        <dl>
          <div><dt>Race</dt><dd>{escape(config.race_en)}</dd></div>
          <div><dt>Date</dt><dd>{escape(config.date_en)}</dd></div>
          <div><dt>State</dt><dd>{escape(config.state_en)} · Run50 #{escape(config.run_no)}</dd></div>
          <div><dt>Route memory</dt><dd>{escape(config.route_memory)}</dd></div>
        </dl>
      </div>
      <div class="related">
        <strong>More versions</strong>
        <a href="../stories/english/{config.slug}.html">Read in original order</a>
        <a href="../stories/chinese/{config.slug}.html">中文原文整理版</a>
      </div>
    </aside>
  </main>
{facebook_engagement(config)}
</body>
</html>
"""


def draw_badge(draw: ImageDraw.ImageDraw, config: StoryConfig, scale: float = 1.0) -> None:
    def s(v):
        return int(round(v * scale))

    draw.rounded_rectangle((s(760), s(64), s(1122), s(228)), radius=s(22), fill="#ffffff", outline="#20242b", width=s(7))
    draw.text((s(790), s(96)), f"Run50 #{config.run_no}", fill="#20242b", font=font(s(38), True))
    badge_font = fit_font(draw, config.state_en.upper(), s(302), s(50), s(30), True)
    draw.text((s(790), s(150)), config.state_en.upper(), fill="#0b67c2", font=badge_font)


def draw_scene(draw: ImageDraw.ImageDraw, config: StoryConfig, width: int = 1200, height: int = 630) -> None:
    scale = height / 630

    def p(x, y):
        return (int(x * scale), int(y * scale))

    ink = "#20242b"
    sky = "#cfe9f4"
    green = "#80bd5b"
    gold = "#f7b733"
    orange = "#f77f50"
    blue = "#0b67c2"
    draw.rectangle((0, 0, width, height), fill=sky)
    draw.ellipse((p(930, 82), p(1028, 180)), fill=gold)
    draw.polygon([p(0, 430), p(250, 370), p(520, 405), p(760, 350), p(1200, 410), p(1200, 630), p(0, 630)], fill="#9acb6e")
    draw.polygon([p(0, 510), p(360, 465), p(780, 500), p(1200, 462), p(1200, 630), p(0, 630)], fill=green)

    if config.scene == "derby":
        # Twin spires and a horse track.
        draw.ellipse((p(250, 455), p(640, 590)), fill="#f5efe1", outline="#ffffff", width=max(3, p(5, 0)[0]))
        draw.ellipse((p(330, 488), p(560, 560)), fill=green)
        for x in (820, 940):
            draw.rectangle((p(x, 265), p(x + 70, 470)), fill="#f8e2b8", outline=ink, width=max(2, int(3 * scale)))
            draw.polygon([p(x - 8, 265), p(x + 35, 205), p(x + 78, 265)], fill="#d35245", outline=ink)
        draw.rectangle((p(790, 470), p(1040, 505)), fill="#d35245", outline=ink, width=max(2, int(3 * scale)))
        draw.arc((p(852, 310), p(978, 490)), 180, 360, fill=ink, width=max(4, int(5 * scale)))
        draw.ellipse((p(390, 365), p(525, 438)), fill="#8d6a55")
        draw.ellipse((p(510, 342), p(558, 386)), fill="#8d6a55")
        draw.line((p(420, 430), p(405, 482)), fill=ink, width=max(4, int(5 * scale)))
        draw.line((p(492, 430), p(515, 482)), fill=ink, width=max(4, int(5 * scale)))
        draw.line((p(377, 392), p(340, 375)), fill=ink, width=max(4, int(5 * scale)))
    elif config.scene == "pig":
        # Flying pig over the Ohio River and Roebling-style bridge.
        draw.rectangle((p(0, 502), p(1200, 630)), fill="#3fb8ca")
        for x in (320, 850):
            draw.line((p(x, 265), p(x, 520)), fill=ink, width=max(5, int(7 * scale)))
            draw.arc((p(x - 86, 235), p(x + 86, 360)), 180, 360, fill=ink, width=max(5, int(7 * scale)))
        draw.line((p(235, 350), p(935, 350)), fill=ink, width=max(4, int(5 * scale)))
        for x in range(280, 900, 70):
            draw.line((p(x, 350), p(x + 20, 505)), fill="#5b6b7a", width=max(2, int(3 * scale)))
        draw.ellipse((p(515, 330), p(665, 420)), fill="#ff9fb5", outline=ink, width=max(2, int(3 * scale)))
        draw.ellipse((p(640, 348), p(700, 398)), fill="#ff9fb5", outline=ink, width=max(2, int(3 * scale)))
        draw.polygon([p(565, 335), p(520, 295), p(600, 320)], fill="#ffd2df", outline=ink)
        draw.polygon([p(580, 335), p(635, 292), p(620, 345)], fill="#ffd2df", outline=ink)
        draw.ellipse((p(684, 370), p(696, 382)), fill=ink)
        draw.arc((p(486, 350), p(520, 390)), 90, 290, fill=ink, width=max(3, int(4 * scale)))
    elif config.scene == "atlanta":
        # Olympic rings, skyline and peach.
        colors = ["#0085c7", "#f4c300", "#000000", "#009f3d", "#df0024"]
        centers = [(430, 390), (492, 435), (555, 390), (618, 435), (680, 390)]
        for (cx, cy), color in zip(centers, colors):
            draw.ellipse((p(cx - 48, cy - 48), p(cx + 48, cy + 48)), outline=color, width=max(6, int(10 * scale)))
        for x, h, c in [(770, 142, "#b7d7e5"), (838, 192, "#f5d66c"), (925, 165, "#d2c2ee")]:
            draw.rectangle((p(x, 470 - h), p(x + 58, 470)), fill=c, outline="#667085", width=max(1, int(2 * scale)))
        draw.ellipse((p(175, 340), p(300, 465)), fill="#f47f4b", outline=ink, width=max(2, int(3 * scale)))
        draw.polygon([p(245, 332), p(310, 300), p(285, 365)], fill="#4b9b54")
    elif config.scene == "denver":
        # Rocky Mountains and stadium.
        draw.polygon([p(0, 410), p(185, 235), p(360, 410)], fill="#9aa5b1")
        draw.polygon([p(135, 285), p(185, 235), p(236, 288)], fill="#ffffff")
        draw.polygon([p(300, 430), p(510, 190), p(740, 430)], fill="#7f8c98")
        draw.polygon([p(455, 252), p(510, 190), p(575, 270)], fill="#ffffff")
        draw.ellipse((p(742, 382), p(1030, 520)), fill="#ffffff", outline=ink, width=max(4, int(5 * scale)))
        draw.ellipse((p(800, 412), p(976, 493)), fill="#62a85f")
        draw.rectangle((p(840, 350), p(930, 420)), fill="#ef7d45", outline=ink, width=max(2, int(3 * scale)))
    elif config.scene == "alaska":
        # Mountains, coastal water and aurora-like summer light.
        draw.rectangle((p(0, 500), p(1200, 630)), fill="#3ba7ba")
        draw.polygon([p(40, 455), p(260, 175), p(500, 455)], fill="#6e7f8e")
        draw.polygon([p(200, 250), p(260, 175), p(332, 270)], fill="#ffffff")
        draw.polygon([p(420, 465), p(660, 145), p(920, 465)], fill="#5f7182")
        draw.polygon([p(595, 230), p(660, 145), p(742, 255)], fill="#ffffff")
        draw.arc((p(100, 90), p(1050, 270)), 190, 345, fill="#79d6a2", width=max(5, int(8 * scale)))
        draw.ellipse((p(870, 420), p(970, 472)), fill="#775b45", outline=ink, width=max(2, int(3 * scale)))
        draw.ellipse((p(942, 394), p(986, 436)), fill="#775b45", outline=ink, width=max(2, int(3 * scale)))
        for x in (895, 940):
            draw.line((p(x, 465), p(x - 10, 520)), fill=ink, width=max(4, int(5 * scale)))
        draw.line((p(990, 400), p(1030, 370)), fill=ink, width=max(3, int(4 * scale)))
        draw.line((p(985, 405), p(1030, 410)), fill=ink, width=max(3, int(4 * scale)))
    elif config.scene == "missouri":
        # Road, river, Pony Express hat and civic dome.
        draw.polygon([p(430, 630), p(555, 405), p(665, 405), p(820, 630)], fill="#4f5b66")
        draw.line((p(610, 430), p(620, 630)), fill="#f5d66c", width=max(4, int(5 * scale)))
        draw.rectangle((p(175, 372), p(450, 492)), fill="#f1e0c5", outline=ink, width=max(2, int(3 * scale)))
        draw.rectangle((p(210, 322), p(415, 372)), fill="#d7b98b", outline=ink, width=max(2, int(3 * scale)))
        draw.arc((p(242, 255), p(382, 390)), 180, 360, fill=ink, width=max(4, int(5 * scale)))
        draw.ellipse((p(835, 358), p(1000, 442)), fill="#b07a50", outline=ink, width=max(2, int(3 * scale)))
        draw.polygon([p(815, 442), p(1020, 442), p(940, 485)], fill="#b07a50", outline=ink)
        draw.line((p(875, 442), p(850, 510)), fill=ink, width=max(4, int(5 * scale)))
        draw.line((p(960, 442), p(985, 510)), fill=ink, width=max(4, int(5 * scale)))


def generate_cover_png(config: StoryConfig) -> None:
    path = REPO / "assets" / f"og-run50-{config.slug}-icons.png"
    image = Image.new("RGB", (1200, 630), "#cfe9f4")
    draw = ImageDraw.Draw(image)
    draw_scene(draw, config, 1200, 630)
    draw.text((64, 64), config.cover_title, fill="#20242b", font=fit_font(draw, config.cover_title, 650, 66, 44, True))
    draw.text((66, 136), config.cover_subtitle, fill="#667085", font=fit_font(draw, config.cover_subtitle, 640, 26, 18, True))
    draw_badge(draw, config, 1.0)
    image.save(path)


def svg_art(config: StoryConfig) -> str:
    if config.scene == "derby":
        return """
  <ellipse cx="455" cy="625" rx="225" ry="74" fill="#f5efe1" stroke="#fff" stroke-width="8"/>
  <ellipse cx="455" cy="625" rx="130" ry="39" fill="#80bd5b"/>
  <g fill="#f8e2b8" stroke="#20242b" stroke-width="4"><rect x="815" y="320" width="72" height="238"/><rect x="940" y="320" width="72" height="238"/></g>
  <g fill="#d35245" stroke="#20242b" stroke-width="4"><path d="M807 320 L851 250 L895 320Z"/><path d="M932 320 L976 250 L1020 320Z"/></g>
  <rect x="785" y="558" width="260" height="42" fill="#d35245" stroke="#20242b" stroke-width="4"/>
  <path d="M845 440 Q915 345 985 440" fill="none" stroke="#20242b" stroke-width="7"/>
  <ellipse cx="450" cy="475" rx="78" ry="42" fill="#8d6a55"/><ellipse cx="530" cy="455" rx="29" ry="25" fill="#8d6a55"/>
  <path d="M420 516 L405 585 M505 515 L532 585 M377 470 L335 448" stroke="#20242b" stroke-width="7" stroke-linecap="round"/>
"""
    if config.scene == "pig":
        return """
  <rect y="600" width="1200" height="150" fill="#3fb8ca"/>
  <g fill="none" stroke="#20242b" stroke-width="8"><path d="M320 315 V615 M850 315 V615"/><path d="M230 415 H940"/><path d="M234 405 Q320 250 406 405"/><path d="M764 405 Q850 250 936 405"/></g>
  <g stroke="#5b6b7a" stroke-width="4"> <path d="M280 415 L305 602"/><path d="M350 415 L375 602"/><path d="M420 415 L445 602"/><path d="M490 415 L515 602"/><path d="M560 415 L585 602"/><path d="M630 415 L655 602"/><path d="M700 415 L725 602"/><path d="M770 415 L795 602"/><path d="M840 415 L865 602"/></g>
  <ellipse cx="590" cy="452" rx="85" ry="50" fill="#ff9fb5" stroke="#20242b" stroke-width="4"/>
  <ellipse cx="676" cy="462" rx="35" ry="27" fill="#ff9fb5" stroke="#20242b" stroke-width="4"/>
  <path d="M560 452 L510 402 L610 428Z M590 448 L650 400 L632 465Z" fill="#ffd2df" stroke="#20242b" stroke-width="4"/>
  <circle cx="693" cy="460" r="6" fill="#20242b"/><path d="M507 448 Q482 465 502 490" fill="none" stroke="#20242b" stroke-width="5"/>
"""
    if config.scene == "atlanta":
        return """
  <g fill="none" stroke-width="11"><circle cx="430" cy="465" r="55" stroke="#0085c7"/><circle cx="500" cy="515" r="55" stroke="#f4c300"/><circle cx="570" cy="465" r="55" stroke="#000"/><circle cx="640" cy="515" r="55" stroke="#009f3d"/><circle cx="710" cy="465" r="55" stroke="#df0024"/></g>
  <g stroke="#667085" stroke-width="3"><rect x="780" y="395" width="62" height="170" fill="#b7d7e5"/><rect x="860" y="345" width="70" height="220" fill="#f5d66c"/><rect x="955" y="382" width="62" height="183" fill="#d2c2ee"/></g>
  <ellipse cx="235" cy="505" rx="70" ry="75" fill="#f47f4b" stroke="#20242b" stroke-width="4"/><path d="M275 430 L342 392 L318 470Z" fill="#4b9b54"/>
"""
    if config.scene == "denver":
        return """
  <path d="M0 495 L190 280 L375 495Z" fill="#9aa5b1"/><path d="M140 345 L190 280 L242 350Z" fill="#fff"/>
  <path d="M285 515 L525 215 L765 515Z" fill="#7f8c98"/><path d="M460 295 L525 215 L590 315Z" fill="#fff"/>
  <ellipse cx="895" cy="535" rx="160" ry="80" fill="#fff" stroke="#20242b" stroke-width="6"/><ellipse cx="895" cy="535" rx="95" ry="42" fill="#62a85f"/><rect x="850" y="438" width="96" height="85" fill="#ef7d45" stroke="#20242b" stroke-width="4"/>
"""
    if config.scene == "alaska":
        return """
  <rect y="595" width="1200" height="155" fill="#3ba7ba"/>
  <path d="M40 545 L265 205 L500 545Z" fill="#6e7f8e"/><path d="M205 292 L265 205 L340 322Z" fill="#fff"/>
  <path d="M420 560 L665 175 L930 560Z" fill="#5f7182"/><path d="M600 275 L665 175 L750 305Z" fill="#fff"/>
  <path d="M95 120 Q580 260 1055 140" fill="none" stroke="#79d6a2" stroke-width="12" opacity=".85"/>
  <ellipse cx="925" cy="515" rx="58" ry="30" fill="#775b45" stroke="#20242b" stroke-width="4"/><ellipse cx="985" cy="492" rx="28" ry="24" fill="#775b45" stroke="#20242b" stroke-width="4"/>
  <path d="M900 545 L888 610 M950 545 L975 610 M1010 490 L1050 458 M1008 497 L1054 505" stroke="#20242b" stroke-width="6" stroke-linecap="round"/>
"""
    return """
  <path d="M430 750 L555 480 H665 L825 750Z" fill="#4f5b66"/><path d="M610 510 L622 750" stroke="#f5d66c" stroke-width="7"/>
  <rect x="175" y="440" width="280" height="140" fill="#f1e0c5" stroke="#20242b" stroke-width="4"/><rect x="210" y="380" width="210" height="60" fill="#d7b98b" stroke="#20242b" stroke-width="4"/><path d="M248 390 Q315 310 385 390" fill="none" stroke="#20242b" stroke-width="6"/>
  <ellipse cx="920" cy="498" rx="90" ry="45" fill="#b07a50" stroke="#20242b" stroke-width="4"/><path d="M815 543 H1030 L940 600Z" fill="#b07a50" stroke="#20242b" stroke-width="4"/><path d="M875 543 L850 625 M960 543 L988 625" stroke="#20242b" stroke-width="6"/>
"""


def generate_cover_svg(config: StoryConfig) -> None:
    title_size = 66
    if len(config.cover_title) > 12:
        title_size = 58
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 750" width="1200" height="750" role="img" aria-labelledby="title desc">
  <title id="title">{escape(config.city_en)} Marathon Run50 icon cover</title>
  <desc id="desc">Icon cover for {escape(config.race_en)} with city motifs and a Run50 {escape(config.state_en)} badge.</desc>
  <rect width="1200" height="750" fill="#cfe9f4"/>
  <circle cx="965" cy="132" r="58" fill="#f7b733"/>
  <path d="M0 510 L250 440 L520 485 L760 420 L1200 490 L1200 750 L0 750Z" fill="#9acb6e"/>
  <path d="M0 615 L360 555 L780 602 L1200 552 L1200 750 L0 750Z" fill="#80bd5b"/>
{svg_art(config)}
  <text x="70" y="104" font-family="Arial, Helvetica, sans-serif" font-size="{title_size}" font-weight="900" fill="#20242b">{escape(config.cover_title)}</text>
  <text x="72" y="150" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="800" fill="#667085">{escape(config.cover_subtitle)}</text>
  <rect x="758" y="62" width="364" height="166" rx="22" fill="#ffffff" stroke="#20242b" stroke-width="8"/>
  <text x="790" y="122" font-family="Arial, Helvetica, sans-serif" font-size="41" font-weight="900" fill="#20242b">Run50 #{escape(config.run_no)}</text>
  <text x="790" y="182" font-family="Arial, Helvetica, sans-serif" font-size="{46 if len(config.state_en) > 8 else 52}" font-weight="900" fill="#0b67c2">{escape(config.state_en.upper())}</text>
</svg>
'''
    thumb_path = REPO / "assets" / f"thumb-run50-{config.slug}-icons.svg"
    fb_path = REPO / "assets" / "facebook" / thumb_path.name
    thumb_path.write_text(svg, encoding="utf-8")
    fb_path.parent.mkdir(parents=True, exist_ok=True)
    fb_path.write_text(svg, encoding="utf-8")


def choose_medal_source(config: StoryConfig, events: list[dict]) -> Path:
    if config.medal_hint:
        for event in events:
            if event["type"] == "image" and event["source"].name == config.medal_hint:
                return event["source"]
    image_indices = [idx for idx, event in enumerate(events) if event["type"] == "image"]
    for keywords in (("奖牌", "medal", "Medal"), ("完赛", "冲线", "终点", "finish", "Finish")):
        for idx, event in enumerate(events):
            if event["type"] != "text":
                continue
            if not any(keyword.lower() in event["text"].lower() for keyword in keywords):
                continue
            previous_images = [image_idx for image_idx in image_indices if image_idx < idx]
            if previous_images:
                return events[previous_images[-1]]["source"]
    return events[image_indices[-1]]["source"]


def draw_checkered_strip(draw: ImageDraw.ImageDraw, x: int, y: int, size: int = 16, cols: int = 8, rows: int = 3) -> None:
    for row in range(rows):
        for col in range(cols):
            fill = "#20242b" if (row + col) % 2 == 0 else "#ffffff"
            draw.rectangle((x + col * size, y + row * size, x + (col + 1) * size, y + (row + 1) * size), fill=fill)
    draw.rectangle((x, y, x + cols * size, y + rows * size), outline="#20242b", width=3)


def generate_medal_cover(config: StoryConfig, events: list[dict]) -> None:
    out = REPO / "assets" / config.medal_name
    canvas = Image.new("RGBA", (1200, 750), "#edf3f7")
    draw = ImageDraw.Draw(canvas)

    # A medal-art plaque instead of a cropped medal photo, matching the Chicago/Guilin card rhythm.
    for y in range(0, 750, 18):
        shade = 239 + ((y // 18) % 2) * 5
        draw.line((0, y, 1200, y), fill=(shade, shade + 3, shade + 5, 80), width=2)
    draw.rounded_rectangle((26, 24, 1174, 724), radius=38, fill="#c7b184", outline="#20242b", width=9)
    draw.rounded_rectangle((42, 40, 1158, 708), radius=28, outline="#f9edc5", width=8)
    draw.rounded_rectangle((56, 54, 1144, 694), radius=20, outline="#6e5932", width=5)

    scene = Image.new("RGB", (1200, 630), "#cfe9f4")
    scene_draw = ImageDraw.Draw(scene)
    draw_scene(scene_draw, config, 1200, 630)
    scene = ImageOps.fit(scene, (1076, 560), method=Image.LANCZOS, centering=(0.5, 0.55)).convert("RGBA")
    mask = Image.new("L", (1076, 560), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, 1075, 559), radius=16, fill=255)
    canvas.paste(scene, (62, 62), mask)

    overlay = Image.new("RGBA", (1200, 750), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.rounded_rectangle((82, 86, 515, 265), radius=20, fill=(255, 255, 255, 190), outline=(32, 36, 43, 210), width=4)
    od.rounded_rectangle((820, 88, 1104, 220), radius=18, fill=(255, 255, 255, 210), outline=(32, 36, 43, 220), width=5)
    od.rounded_rectangle((82, 542, 1118, 662), radius=18, fill=(32, 36, 43, 230), outline=(249, 237, 197, 230), width=4)
    od.rectangle((82, 622, 1118, 662), fill=(11, 103, 194, 230))
    canvas = Image.alpha_composite(canvas, overlay)
    draw = ImageDraw.Draw(canvas)

    state_font = fit_font(draw, config.state_abbr, 380, 112, 82, True)
    draw.text((108, 101), config.state_abbr, fill="#20242b", font=state_font, stroke_width=2, stroke_fill="#f9edc5")
    draw.text((112, 214), config.state_en.upper(), fill="#5b6774", font=fit_font(draw, config.state_en.upper(), 360, 28, 20, True))

    draw.text((848, 116), f"Run50 #{config.run_no}", fill="#20242b", font=fit_font(draw, f"Run50 #{config.run_no}", 220, 38, 28, True))
    draw.text((848, 166), config.date_iso, fill="#0b67c2", font=fit_font(draw, config.date_iso, 220, 34, 24, True))
    draw_checkered_strip(draw, 940, 232, size=14, cols=7, rows=3)

    title_font = fit_font(draw, config.cover_title, 840, 76, 48, True)
    draw.text((106, 558), config.cover_title, fill="#ffffff", font=title_font)
    draw.text((108, 626), config.race_en.upper(), fill="#ffffff", font=fit_font(draw, config.race_en.upper(), 840, 25, 17, True))

    for x, y in ((62, 62), (1138, 62), (62, 622), (1138, 622)):
        draw.ellipse((x - 14, y - 14, x + 14, y + 14), fill="#f8e7b3", outline="#20242b", width=4)
        draw.ellipse((x - 5, y - 5, x + 5, y + 5), fill="#6e5932")

    canvas.convert("RGB").save(out, quality=94)


def write_clean(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(line.rstrip() for line in text.strip().splitlines()) + "\n", encoding="utf-8")


def remove_existing_card(text: str, href: str) -> str:
    pattern = re.compile(rf'\n\s*<a class="story-card [^"]+" href="{re.escape(href)}">.*?</a>', re.S)
    return pattern.sub("", text)


def insert_after_card(text: str, target_href: str, card: str, fallback_marker: str) -> str:
    pattern = re.compile(rf'(\n\s*<a class="story-card [^"]+" href="{re.escape(target_href)}">.*?</a>\s*)', re.S)
    if pattern.search(text):
        return pattern.sub(lambda match: match.group(1) + "\n" + card, text, count=1)
    return text.replace(fallback_marker, fallback_marker + "\n" + card, 1)


def story_cards(config: StoryConfig) -> tuple[str, str, str]:
    zh_card = f"""      <a class="story-card run-50" href="./{config.slug}.html">
        <img src="../../../assets/{config.medal_name}?v={VERSION}" alt="{escape(config.race_zh)}奖牌封面" loading="lazy" decoding="async">
        <div class="story-copy">
          <p class="story-meta">{escape(config.state_zh)}{escape(config.city_zh)} · {config.date_zh}</p>
          <h2 class="story-title">{escape(config.card_title_zh)}</h2>
          <p class="story-desc">{escape(config.card_desc_zh)}</p>
          <div class="story-foot"><span>长文图记</span><span>阅读 →</span></div>
        </div>
      </a>
"""
    en_card = f"""      <a class="story-card run-50" href="./{config.slug}.html">
        <img src="../../../assets/thumb-run50-{config.slug}-icons.svg?v={VERSION}" alt="Icon cover for {escape(config.race_en)}" loading="lazy" decoding="async">
        <div class="story-card-content">
          <div class="meta">{escape(config.state_en)} · {escape(config.city_en)} · {config.date_iso}</div>
          <h2>{escape(config.card_title_en)}</h2>
          <p>{escape(config.card_desc_en)}</p>
        </div>
      </a>
"""
    fb_card = f"""    <a class="story-card run-50" href="./{config.slug}.html">
      <div>
        <p class="eyebrow">World / USA / Marathon</p>
        <h2>{escape(config.title_fb)}</h2>
        <p>{escape(config.fb_card_desc)}</p>
        <div class="meta"><span>{escape(config.city_en)}, {config.state_abbr}</span><span>Run50 #{escape(config.run_no)}</span><span>{escape(config.fb_meta_note)}</span></div>
      </div>
      <img src="../../assets/facebook/thumb-run50-{config.slug}-icons.svg?v={VERSION}" alt="Icon-style {escape(config.race_en)} cover">
    </a>
"""
    return zh_card, en_card, fb_card


def update_story_indexes() -> None:
    zh_path = REPO / "run50" / "stories" / "chinese" / "index.html"
    en_path = REPO / "run50" / "stories" / "english" / "index.html"
    fb_path = REPO / "run50" / "facebook" / "index.html"

    zh = zh_path.read_text(encoding="utf-8")
    en = en_path.read_text(encoding="utf-8")
    fb = fb_path.read_text(encoding="utf-8")
    for config in STORIES:
        zh = remove_existing_card(zh, f"./{config.slug}.html")
        en = remove_existing_card(en, f"./{config.slug}.html")
        fb = remove_existing_card(fb, f"./{config.slug}.html")

    target = "./honolulu-marathon.html"
    for config in reversed(STORIES):
        zh_card, en_card, fb_card = story_cards(config)
        zh = insert_after_card(zh, target, zh_card, '<section class="story-grid"')
        en = insert_after_card(en, target, en_card, '<section class="story-grid"')
        fb = insert_after_card(fb, target, fb_card, '<main class="shell">')

    zh = re.sub(
        r"'AK': \[\{city: '.*?', raceName: '.*?', date: '2023\.08\.20', emoji: '.*?', num: '#09', isPlaceholder: true\}\],",
        "'AK': [{city: '安克雷奇', raceName: '安克雷奇市长马拉松', date: '2023.06.17', emoji: '🏔️', num: '#09', isPlaceholder: false}],",
        zh,
    )
    en = re.sub(
        r"'AK': \[\{city: 'Anchorage', raceName: '4th Anchorage Marathon', date: '2023\.08\.20', emoji: '.*?', num: '#09', isPlaceholder: false\}\],",
        "'AK': [{city: 'Anchorage', raceName: \"Anchorage Mayor's Marathon\", date: '2023.06.17', emoji: '🏔️', num: '#09', isPlaceholder: false}],",
        en,
    )
    write_clean(zh_path, zh)
    write_clean(en_path, en)
    write_clean(fb_path, fb)


def root_card(config: StoryConfig) -> str:
    return f"""
      <!-- {config.root_marker} -->
      <article class="video-card" data-section="run50" data-category="run50 facebook" data-title="{escape(config.title_fb)}">
        <a class="thumb" href="run50/facebook/{config.slug}.html">
          <img src="assets/facebook/thumb-run50-{config.slug}-icons.svg?v={VERSION}" alt="Icon-style {escape(config.race_en)} cover">
          <span class="duration">Story</span>
        </a>
        <div class="meta">
          <span class="avatar run50">50</span>
          <div>
            <a class="video-title" href="run50/facebook/{config.slug}.html">{escape(config.title_fb)}</a>
            <p class="video-sub">{escape(config.city_en)}, {config.state_abbr} &middot; {escape(config.date_en)}</p>
          </div>
        </div>
      </article>
      <!-- /{config.root_marker} -->
"""


def update_root_home() -> None:
    path = REPO / "index.html"
    text = path.read_text(encoding="utf-8")
    for config in STORIES:
        text = re.sub(rf"\n\s*<!-- {re.escape(config.root_marker)} -->.*?<!-- /{re.escape(config.root_marker)} -->\n", "\n", text, flags=re.S)
    block = "".join(root_card(config) for config in STORIES)
    marker = "      <!-- /Hawaii Run50 story -->"
    if marker in text:
        text = text.replace(marker, marker + "\n" + block, 1)
    write_clean(path, text)


def update_landing_counts() -> None:
    path = REPO / "run50" / "index.html"
    text = path.read_text(encoding="utf-8")
    text = text.replace(" 18 stories", " 24 stories")
    text = text.replace("<strong>18</strong> stories", "<strong>24</strong> stories")
    write_clean(path, text)


def update_hub() -> None:
    path = REPO / "run50" / "hub.html"
    text = path.read_text(encoding="utf-8")
    if "'Anchorage':{lat:61.2181,lon:-149.9003}" not in text:
        text = text.replace(
            "'Atlanta':{lat:33.749,lon:-84.388},'Denver':{lat:39.7392,lon:-104.9903}",
            "'Atlanta':{lat:33.749,lon:-84.388},'Denver':{lat:39.7392,lon:-104.9903},'Anchorage':{lat:61.2181,lon:-149.9003},'St. Joseph':{lat:39.7675,lon:-94.8466}",
            1,
        )
    race_lines = {
        "KY": "  'KY':[{city:'Louisville',date:'Nov 8, 2020',story:'stories/english/louisville-marathon.html',fb:'facebook/louisville-marathon.html'},{city:'Louisville',date:'Apr 29, 2023',story:'stories/english/kentucky-derby-marathon.html',fb:'facebook/kentucky-derby-marathon.html'}],",
        "OH": "  'OH':[{city:'Cleveland',date:'Oct 24, 2021',story:'stories/english/cleveland-marathon.html',fb:'facebook/cleveland-marathon.html'},{city:'Cincinnati',date:'May 7, 2023',story:'stories/english/cincinnati-flying-pig-marathon.html',fb:'facebook/cincinnati-flying-pig-marathon.html'}],",
        "GA": "  'GA':[{city:'Atlanta',date:'Feb 26, 2023',story:'stories/english/atlanta-marathon.html',fb:'facebook/atlanta-marathon.html'}],",
        "CO": "  'CO':[{city:'Denver',date:'May 21, 2023',story:'stories/english/denver-colfax-marathon.html',fb:'facebook/denver-colfax-marathon.html'}],",
        "AK": "  'AK':[{city:'Anchorage',date:'Jun 17, 2023',story:'stories/english/anchorage-marathon.html',fb:'facebook/anchorage-marathon.html'}],",
        "MO": "  'MO':[{city:'St. Joseph',date:'Sep 23, 2023',story:'stories/english/st-joseph-marathon.html',fb:'facebook/st-joseph-marathon.html'}],",
    }
    for abbr in race_lines:
        text = re.sub(rf"^\s*'{abbr}':\[\{{.*?\}}\],\n", "", text, flags=re.M)
    anchor = "  'HI':[{city:'Honolulu',date:'Dec 11, 2022',story:'stories/english/honolulu-marathon.html',fb:'facebook/honolulu-marathon.html'}],"
    insert = anchor + "\n" + "\n".join(race_lines[abbr] for abbr in ["KY", "OH", "GA", "CO", "AK", "MO"])
    text = text.replace(anchor, insert, 1)

    text = re.sub(r"\n\s*<!-- 2023 batch Run50 story dots -->.*?<!-- /2023 batch Run50 story dots -->\n", "\n", text, flags=re.S)
    dots = """
    <!-- 2023 batch Run50 story dots -->
    <circle cx="236" cy="131" r="10" fill="rgba(255,80,40,0.18)" pointer-events="none"/>
    <circle cx="236" cy="131" r="5" fill="#ff4040" stroke="#fff" stroke-width="1.6" class="wm-dot"
      data-city="Louisville, KY" data-date="Apr 29, 2023" data-story="stories/english/kentucky-derby-marathon.html"/>
    <circle cx="238" cy="128" r="10" fill="rgba(255,80,40,0.18)" pointer-events="none"/>
    <circle cx="238" cy="128" r="5" fill="#ff4040" stroke="#fff" stroke-width="1.6" class="wm-dot"
      data-city="Cincinnati, OH" data-date="May 7, 2023" data-story="stories/english/cincinnati-flying-pig-marathon.html"/>
    <circle cx="239" cy="143" r="10" fill="rgba(255,80,40,0.18)" pointer-events="none"/>
    <circle cx="239" cy="143" r="5" fill="#ff4040" stroke="#fff" stroke-width="1.6" class="wm-dot"
      data-city="Atlanta, GA" data-date="Feb 26, 2023" data-story="stories/english/atlanta-marathon.html"/>
    <circle cx="204" cy="132" r="10" fill="rgba(255,80,40,0.18)" pointer-events="none"/>
    <circle cx="204" cy="132" r="5" fill="#ff4040" stroke="#fff" stroke-width="1.6" class="wm-dot"
      data-city="Denver, CO" data-date="May 21, 2023" data-story="stories/english/denver-colfax-marathon.html"/>
    <circle cx="162" cy="92" r="10" fill="rgba(255,80,40,0.18)" pointer-events="none"/>
    <circle cx="162" cy="92" r="5" fill="#ff4040" stroke="#fff" stroke-width="1.6" class="wm-dot"
      data-city="Anchorage, AK" data-date="Jun 17, 2023" data-story="stories/english/anchorage-marathon.html"/>
    <circle cx="217" cy="129" r="10" fill="rgba(255,80,40,0.18)" pointer-events="none"/>
    <circle cx="217" cy="129" r="5" fill="#ff4040" stroke="#fff" stroke-width="1.6" class="wm-dot"
      data-city="St. Joseph, MO" data-date="Sep 23, 2023" data-story="stories/english/st-joseph-marathon.html"/>
    <!-- /2023 batch Run50 story dots -->
"""
    text = text.replace("    <!-- Mexico -->", dots + "\n    <!-- Mexico -->", 1)
    write_clean(path, text)


def update_supabase_sql() -> None:
    path = REPO / "supabase" / "run50-comments.sql"
    text = path.read_text(encoding="utf-8")
    keys = []
    for config in STORIES:
        keys.extend([
            f"run50-{config.slug}-facebook-en",
            f"run50-{config.slug}-en",
            f"run50-{config.slug}-zh",
        ])
    for key in keys:
        text = re.sub(rf"\n\s*'{re.escape(key)}',", "", text)
    insertion = "".join(f"      '{key}',\n" for key in keys)
    text = text.replace("      'run50-honolulu-marathon-zh',\n", "      'run50-honolulu-marathon-zh',\n" + insertion, 1)
    text = text.replace("      'run50-honolulu-marathon-zh',\n", "      'run50-honolulu-marathon-zh',\n" + insertion, 1)
    text = text.replace("    'run50-honolulu-marathon-zh',\n", "    'run50-honolulu-marathon-zh',\n" + insertion.replace("      ", "    "), 1)
    write_clean(path, text)


def build_all() -> None:
    extracted = {config.slug: extract_story(config) for config in STORIES}
    cache = ensure_translations(list(extracted.values()))
    for config in STORIES:
        events = extracted[config.slug]
        count = copy_story_images(config, events)
        article_zh = render_events(config, events, "zh", f"{config.image_dir}/", cache)
        article_en = render_events(config, events, "en", f"../chinese/{config.image_dir}/", cache)
        article_fb = render_events(config, events, "en", f"../stories/chinese/{config.image_dir}/", cache)
        write_clean(REPO / "run50" / "stories" / "chinese" / f"{config.slug}.html", story_page(config, "zh", article_zh))
        write_clean(REPO / "run50" / "stories" / "english" / f"{config.slug}.html", story_page(config, "en", article_en))
        write_clean(REPO / "run50" / "facebook" / f"{config.slug}.html", facebook_page(config, article_fb))
        generate_cover_png(config)
        generate_cover_svg(config)
        generate_medal_cover(config, events)
        print(f"Built {config.slug}: {count} images, {sum(1 for e in events if e['type']=='text')} text blocks")
    update_story_indexes()
    update_root_home()
    update_landing_counts()
    update_hub()
    update_supabase_sql()


if __name__ == "__main__":
    build_all()
