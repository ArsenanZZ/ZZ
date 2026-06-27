from __future__ import annotations

import html
import json
import os
import re
import textwrap
import time
import urllib.parse
import urllib.request
from pathlib import Path

from lxml import html as lxml_html
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

from normalize_arizona_run50_style import normalize_arizona_story_style


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = Path(r"Z:\ZhennanZ Folder\0-Running Story Web\Run50 #第29州｜亚利桑那：凤凰城马拉松｜沙漠·仙人掌·干冷清晨｜二〇二六·第一跑·破4_files")
SOURCE_HTML = SOURCE_DIR / "Run50 #第29州｜亚利桑那：凤凰城马拉松｜沙漠·仙人掌·干冷清晨｜二〇二六·第一跑·破4.html"

SLUG = "arizona-phoenix-marathon"
IMAGE_DIR = ROOT / "run50" / "stories" / "chinese" / f"Run50-Arizona-Phoenix-Marathon-clean_files"
SITE = "https://zhennanzhang.com"
CANONICAL_ZH = f"{SITE}/run50/stories/chinese/{SLUG}.html"
CANONICAL_EN = f"{SITE}/run50/stories/english/{SLUG}.html"
CANONICAL_FB = f"{SITE}/run50/facebook/{SLUG}.html"

VERSION = "20260626-arizona"
DATE_ZH = "2026.01.10"
DATE_EN = "Jan 10, 2026"
KEY_ZH = "run50-arizona-phoenix-marathon-zh"
KEY_EN = "run50-arizona-phoenix-marathon-en"
KEY_FB = "run50-arizona-phoenix-marathon-facebook-en"

FONT_DIR = Path("C:/Windows/Fonts")
FONT_REGULAR = FONT_DIR / "msyh.ttc"
FONT_BOLD = FONT_DIR / "msyhbd.ttc"
FONT_EN_BOLD = FONT_DIR / "arialbd.ttf"
FONT_EN = FONT_DIR / "arial.ttf"


CAPTIONS = [
    ("Buckeye Marathon Vlog 封面", "Buckeye Marathon weekend vlog cover", "@Arsenan"),
    ("飞往亚利桑那途中的云海与荒漠", "Clouds and desert on the way to Arizona", "@Arsenan"),
    ("Buckeye Race to the Runway 号码布", "Buckeye Race to the Runway bib pickup", "@Arsenan"),
    ("North Mountain Park 的山路和巨人柱", "Cactus-lined climb at North Mountain Park", "@Arsenan"),
    ("Dobbins Lookout 的石屋与凤凰城夜色", "Stone lookout and Phoenix lights at Dobbins", "@Arsenan"),
    ("南山高处看凤凰城夜景", "Phoenix glowing below South Mountain", "@Arsenan"),
    ("Dobbins Lookout 日落前的山脊", "The ridge before sunset at Dobbins Lookout", "@Arsenan"),
    ("日落后的沙漠山线", "Desert ridgelines after sunset", "@Arsenan"),
    ("南山观景台的城市光", "City lights from the South Mountain overlook", "@Arsenan"),
    ("山顶石屋旁的晚风", "Evening wind beside the stone shelter", "@Arsenan"),
    ("亚利桑那第一晚的红色山坡", "Red slopes on the first Arizona evening", "@Arsenan"),
    ("Dobbins Lookout 的停车场与暮色", "Dusk at the Dobbins Lookout parking area", "@Arsenan"),
    ("车窗外的凤凰城余晖", "Phoenix afterglow through the car window", "@Arsenan"),
    ("沙漠城市的黄昏剪影", "Twilight silhouettes over the desert city", "@Arsenan"),
    ("酒店窗外的清晨天色", "Early morning light outside the hotel", "@Arsenan"),
    ("比赛日清晨开向 Buckeye", "Driving toward Buckeye before sunrise", "@Arsenan"),
    ("天亮前的高速路和山影", "Highway shadows before daybreak", "@Arsenan"),
    ("Race to the Runway 起点的冷空气", "Cold air at the Race to the Runway start", "@Arsenan"),
    ("起点拱门前的赛前人群", "Pre-race crowd under the start arch", "@Arsenan"),
    ("Festival Foothills 小学外的起跑区", "Start area outside Festival Foothills Elementary", "@Arsenan"),
    ("起跑前最后一张清晨自拍", "One last chilly pre-start photo", "@Arsenan"),
    ("亚利桑那冬晨的起点线", "The Arizona winter morning start line", "@Arsenan"),
    ("赛前补给和跑者队伍", "Pre-race supplies and runners lining up", "@Arsenan"),
    ("Phoenix Race to the Runway 起跑拱门", "Phoenix Race to the Runway start arch", "@Arsenan"),
    ("冷清晨里的起跑人群", "Runners gathering in the cold morning", "@Arsenan"),
    ("Sun City Festival 旁的沙漠道路", "Desert road beside Sun City Festival", "@Arsenan"),
    ("起跑后的第一段宽路", "The first wide stretch after the start", "@Arsenan"),
    ("亚利桑那蓝天下的赛道", "The course under a clean Arizona sky", "@Arsenan"),
    ("公路尽头的山和跑者", "Runners and mountains at the end of the road", "@Arsenan"),
    ("赛道边的巨人柱和土坡", "Saguaros and dirt slopes beside the course", "@Arsenan"),
    ("清晨阳光落在沙漠公路上", "Morning sun across the desert road", "@Arsenan"),
    ("向 Buckeye 机场方向一路下坡", "Rolling downhill toward Buckeye airport", "@Arsenan"),
    ("沙漠风景里的补给站", "Aid station in the desert landscape", "@Arsenan"),
    ("长直路上的跑者节奏", "Finding rhythm on the long straight road", "@Arsenan"),
    ("赛道旁的荒漠和远山", "Open desert and distant mountains", "@Arsenan"),
    ("巨人柱在赛道边排队", "Saguaros lining the edge of the course", "@Arsenan"),
    ("冷空气里的阳光越来越亮", "The sun warming up the cold air", "@Arsenan"),
    ("Buckeye 公路段的蓝天", "Blue sky over the Buckeye road section", "@Arsenan"),
    ("赛道转弯处的荒漠视野", "Desert view around a course bend", "@Arsenan"),
    ("后半程的长路和山影", "Long road and mountain shadows in the second half", "@Arsenan"),
    ("路边加油牌和跑者", "Course signs and runners along the road", "@Arsenan"),
    ("沙漠公路上的官方赛照", "Official course photo on the desert road", "赛事摄影"),
    ("靠近机场终点的最后几英里", "The final miles toward the airport finish", "@Arsenan"),
    ("Race to the Runway 终点方向", "Heading toward the Race to the Runway finish", "@Arsenan"),
    ("Buckeye Municipal Airport 终点拱门", "Finish arch at Buckeye Municipal Airport", "赛事摄影"),
    ("冲过机场跑道旁的终点线", "Across the finish line by the runway", "赛事摄影"),
    ("3:58 到手的终点瞬间", "A 3:58 finish, finally in hand", "赛事摄影"),
    ("终点后的奖牌和笑容", "Medal and a grin after the finish", "赛事摄影"),
    ("机场终点区的赛后合影", "Post-race photo at the airport finish", "赛事摄影"),
    ("Buckeye 机场的完赛拱门", "The finish arch at Buckeye Municipal Airport", "@Arsenan"),
    ("终点区的跑者和志愿者", "Runners and volunteers in the finish area", "@Arsenan"),
    ("奖牌、号码布和 3:58 的证据", "Medal, bib, and proof of 3:58", "@Arsenan"),
    ("跑道旁的赛后补给区", "Post-race food area beside the runway", "@Arsenan"),
    ("机场终点的蓝天和帐篷", "Blue sky and tents at the airport finish", "@Arsenan"),
    ("飞行主题的 Race to the Runway 奖牌", "A flight-themed Race to the Runway medal", "@Arsenan"),
    ("赛后餐盘里的补给", "The post-race plate that hit the spot", "@Arsenan"),
    ("沙漠边缘卷起的小尘旋", "A little dust swirl on the desert edge", "@Arsenan"),
    ("Race to the Runway 奖牌特写", "Close-up of the Race to the Runway medal", "@Arsenan"),
    ("凤凰城街头的赛后下午", "Post-race afternoon back in Phoenix", "@Arsenan"),
    ("Papago Park 红岩入口", "Red rocks at the entrance to Papago Park", "@Arsenan"),
    ("Hole-in-the-Rock 的洞口", "The opening at Hole-in-the-Rock", "@Arsenan"),
    ("红岩窗口里的 Tempe 天光", "Tempe light through the red-rock window", "@Arsenan"),
    ("Papago Park 小路和红砂岩", "Red sandstone trail at Papago Park", "@Arsenan"),
    ("岩洞里看出去的城市", "Looking out from inside the rock opening", "@Arsenan"),
    ("Hole-in-the-Rock 的游客剪影", "Visitors silhouetted at Hole-in-the-Rock", "@Arsenan"),
    ("红岩顶上的凤凰城午后", "Phoenix afternoon from the top of the red rocks", "@Arsenan"),
    ("奖牌和 Papago Park 红岩", "Medal against Papago Park red rocks", "@Arsenan"),
    ("Hole-in-the-Rock 前的完赛照", "Finishers' photo at Hole-in-the-Rock", "@Arsenan"),
    ("Papago Park 的沙漠植物", "Desert plants at Papago Park", "@Arsenan"),
    ("红岩上的风和太阳", "Wind and sun on the red rocks", "@Arsenan"),
    ("赛后继续在凤凰城散步", "A post-race walk through Phoenix", "@Arsenan"),
    ("Papago Park 的红岩层次", "Layers of red rock at Papago Park", "@Arsenan"),
    ("巨人柱、红岩和一枚奖牌", "Saguaros, red rock, and a medal", "@Arsenan"),
    ("Papago Park 山坡上的小路", "A small trail up the Papago Park slope", "@Arsenan"),
    ("Tempe Town Lake 的桥和水面", "Bridge and water at Tempe Town Lake", "@Arsenan"),
    ("Tempe 湖边的夕阳", "Sunset by Tempe Town Lake", "@Arsenan"),
    ("傍晚的 Tempe 城市线", "Tempe skyline in the evening", "@Arsenan"),
    ("巨人柱旁的 Race to the Runway 奖牌", "Race to the Runway medal beside a saguaro", "@Arsenan"),
    ("奖牌和亚利桑那仙人掌", "Medal with Arizona cactus", "@Arsenan"),
    ("沙漠上空的无人机视角", "Drone view above the desert", "@Arsenan"),
    ("日落前的巨人柱剪影", "Saguaro silhouette before sunset", "@Arsenan"),
    ("亚利桑那沙漠里的最后一束光", "The last light in the Arizona desert", "@Arsenan"),
    ("巨人柱和蓝天给这站收尾", "Saguaros and blue sky to close the chapter", "@Arsenan"),
    ("无人机镜头里的仙人柱阵列", "Saguaros lined up in the drone frame", "@Arsenan"),
    ("沙地、远山和低空视角", "Sand, distant hills, and a low drone angle", "@Arsenan"),
    ("临走前再看一眼亚利桑那", "One more look at Arizona before leaving", "@Arsenan"),
    ("凤凰城沙漠周末的最后画面", "The closing frame of a Phoenix desert weekend", "@Arsenan"),
]


SPECIAL_TRANSLATIONS = {
    "- Run50 #第29州｜亚利桑那 -": "- Run50 State #29 | Arizona -",
    "📍地点丨凤凰城 Phoenix, Arizona": "Place | Phoenix, Arizona",
    "🎽赛事丨2026年1月10日 Buckeye Marathon": "Race | Buckeye Marathon, January 10, 2026",
    "📸图文丨Arsenan | ZhennanZhang.com": "Words and photos | Arsenan | ZhennanZhang.com",
    "前言": "Prologue",
    "后记": "Postscript",
    "- 本文完 -": "- The end -",
    "文字丨Arsenan": "Words | Arsenan",
    "摄影丨Arsenan": "Photos | Arsenan",
    "设计丨Arsenan": "Design | Arsenan",
    "# 沙漠方向的第一跑": "First run toward the desert",
    "# 第二十九个州 · 亚利桑那｜沙漠与 UFO 目击": "State #29: Arizona, desert roads and UFO lore",
    "# 第一章｜落地沙漠，日落之前": "Chapter 1 | Landing in the desert before sunset",
    "# 第二章｜干冷沙漠清晨，马拉松一路向西": "Chapter 2 | A cold, dry desert morning, running west",
    "# 第三章｜红岩一洞、仙人柱起飞": "Chapter 3 | Red rocks, Hole-in-the-Rock, and saguaros from above",
    "# 回到路城，跑进新一年": "Postscript | Back to Louisville, running into the new year",
}


def natural_key(path: Path) -> tuple[int, int]:
    name = path.name
    if name == "640":
        return (0, 0)
    match = re.fullmatch(r"640\((\d+)\)", name)
    if match:
        return (0, int(match.group(1)))
    return (1, 0)


def read_source_events() -> list[dict[str, str]]:
    doc = lxml_html.fromstring(SOURCE_HTML.read_bytes())
    main = doc.xpath('//*[@id="js_content"]')
    if not main:
        main = doc.xpath('//*[contains(concat(" ", normalize-space(@class), " "), " rich_media_content ")]')
    if not main:
        raise RuntimeError("Could not find story content in exported HTML")
    events: list[dict[str, str]] = []
    for node in main[0].iter():
        tag = node.tag.lower() if isinstance(node.tag, str) else ""
        if tag == "img":
            src = node.get("data-src") or node.get("src") or ""
            name = Path(urllib.parse.urlparse(src).path).name
            if name.startswith("640"):
                events.append({"type": "image", "src": name})
        elif tag in {"p", "section"}:
            if any(isinstance(child.tag, str) and child.tag.lower() == "img" for child in node.iterdescendants()):
                continue
            text = " ".join(node.text_content().split())
            if text:
                events.append({"type": "text", "text": text})

    start = next(i for i, item in enumerate(events) if item.get("text") == "- Run50 #第29州｜亚利桑那 -")
    end = next(i for i, item in enumerate(events[start:], start) if item.get("text") == "设计丨Arsenan")
    deduped: list[dict[str, str]] = []
    for item in events[start : end + 1]:
        if deduped and deduped[-1] == item:
            continue
        deduped.append(item)
    return clean_events(deduped)


def clean_events(events: list[dict[str, str]]) -> list[dict[str, str]]:
    cleaned: list[dict[str, str]] = []
    skip_next: set[int] = set()
    for i, item in enumerate(events):
        if i in skip_next:
            continue
        if item["type"] == "image":
            cleaned.append(item)
            continue

        text = item["text"].strip()
        if not text or text in {"★", "★★", "★★★"}:
            continue
        if text.startswith("▲"):
            continue
        if text.startswith("★#") or text.startswith("★★#") or text.startswith("★★★#"):
            continue
        if re.fullmatch(r"(前言|后记)# .+🌵 .+", text):
            continue
        if text.startswith("# ") and "🌵" in text:
            continue
        cleaned.append({"type": "text", "text": text})
    return cleaned


def cache_path() -> Path:
    return ROOT / ".cache_arizona_translate.json"


def translate_text(text: str, cache: dict[str, str]) -> str:
    if text in SPECIAL_TRANSLATIONS:
        return SPECIAL_TRANSLATIONS[text]
    key = text
    if key in cache:
        return polish_translation(cache[key])
    params = urllib.parse.urlencode({"client": "gtx", "sl": "zh-CN", "tl": "en", "dt": "t", "q": text})
    url = f"https://translate.googleapis.com/translate_a/single?{params}"
    for attempt in range(3):
        try:
            with urllib.request.urlopen(url, timeout=20) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            translated = "".join(part[0] for part in data[0] if part and part[0])
            translated = polish_translation(translated)
            cache[key] = translated
            time.sleep(0.05)
            return translated
        except Exception:
            if attempt == 2:
                return text
            time.sleep(0.5)
    return text


def polish_translation(text: str) -> str:
    replacements = [
        ("Buck Eye", "Buckeye"),
        ("Buck Ai", "Buckeye"),
        ("Buckai", "Buckeye"),
        ("Buckai Marathon", "Buckeye Marathon"),
        ("Barkai", "Buckeye"),
        ("Lucheng", "Louisville"),
        ("Road City", "Louisville"),
        ("road city", "Louisville"),
        ("Hongyan", "red rocks"),
        ("Immortal Pillar", "saguaro"),
        ("immortal pillar", "saguaro"),
        ("Giant Pillar", "saguaro"),
        ("giant pillar", "saguaro"),
        ("Saguaro (giant column)", "saguaro cactus"),
        ("Saguaro (giant pillar)", "saguaro cactus"),
        ("Saguaro, with a large cactus", "saguaros, with big cacti"),
        ("like a watcher", "like sentries"),
        ("break 4", "go sub-four"),
        ("Breaking 4", "Going sub-four"),
        ("broken 4", "gone sub-four"),
        ("breaking 4", "going sub-four"),
        ("breaking 4.", "going sub-four."),
        ("broke 4", "went sub-four"),
        ("Sqi", "Siqi"),
        ("Siki", "Siqi"),
        ("Tianpu", "Tempe"),
        ("Pappago", "Papago"),
        ("Dobbins Observation Deck", "Dobbins Lookout"),
        ("Hole in the Rock", "Hole-in-the-Rock"),
        ("Hole-in-the-rock", "Hole-in-the-Rock"),
        ("Buckeye Municipal Airport", "Buckeye Municipal Airport"),
        ("Festival Foothills Elementary School", "Festival Foothills Elementary School"),
        ("Pre-flight", "PreFlight"),
        ("TownePlace Suitess", "TownePlace Suites"),
        ("TownePlace Suitesss", "TownePlace Suites"),
        ("towards", "toward"),
        ("competition", "race"),
        ("Competition", "Race"),
        ("such a niche game", "such a small race"),
        ("number cloth", "bib"),
        ("Number cloth", "Bib"),
        ("The entry package", "The race packet"),
        ("After receiving the equipment", "After packet pickup"),
        ("receiving the equipment", "packet pickup"),
        ("There was no fuss about eating, so we went directly to Golden Corral.", "We kept food simple and went straight to Golden Corral."),
        ("Typical American buffet, no surprises.", "Classic American buffet, no surprises."),
        ("In the afternoon, go to TownePlace Suites by Marriott (Buckeye) to pick up equipment.", "In the afternoon, we went to TownePlace Suites by Marriott in Buckeye for packet pickup."),
        ("At first glance, it looks like a small race.", "You could tell right away it was a small race."),
        ("I drove directly to North Mountain Park.", "We drove straight to North Mountain Park."),
        ("What I was given was a 2023 Tesla Model Y.", "They gave us a 2023 Tesla Model Y."),
        ("it can actually drive automatically", "it even had Autopilot"),
        ("Although it is an old version", "It was an older version"),
        ("It was an older version, it is sufficient. Siqi and I didn’t have to worry about driving just now.", "It was an older version, but good enough. At least Siqi and I did not have to stress about the drive."),
        ("gained an hour in vain", "got an extra hour for free"),
        ("new atmosphere", "fresh start"),
        ("I don’t want to fall behind on this big plan of Run50.", "I didn’t want the big Run50 plan to sit still either."),
        ("was taught a positive lesson by the cold wave", "got thoroughly humbled by the cold front"),
        ("Starting below zero and facing the wind", "Starting below freezing and fighting the wind"),
        ("So my eyes fell on Arizona.", "So I started looking at Arizona."),
        ("This time the race was small", "This time, the race was small"),
        ("it’s not stressful, so it’s good.", "no pressure, which sounded perfect."),
        ("it’s not stressful, so it’s good, it’s good.", "no pressure, which sounded perfect."),
        ("bifurcated", "branching"),
        ("supply point", "aid station"),
        ("supply points", "aid stations"),
        ("Someone kept shouting \"Come on\"", "Someone kept yelling \"you got this\""),
        ("The marathon starts at 8am. Before dawn, Siqi sent me to the starting point. Start at Festival Foothills Elementary School", "The marathon started at 8 a.m. Before dawn, Siqi drove me to the start at Festival Foothills Elementary School."),
        ("waiting for the gun to be fired", "waiting for the start"),
        ("There was no obstruction, no trees", "There was no shade, no trees"),
        ("The pace of the aid station is very good", "The aid stations were well spaced"),
        ("The aid stations were well spaced, and the water and drinks are all ice cold.", "The aid stations were well spaced, and the water and sports drinks were ice cold."),
        ("There is also energy gel on the table, you can tear it open and take it.", "There were gels on the tables too, easy to grab and tear open."),
        ("The volunteers are very enthusiastic.", "The volunteers were great."),
        ("someone handed the cup to your hand with very focused eyes, as if they were seriously completing something important.", "someone placed a cup right in your hand with the focus of someone doing something that mattered."),
        ("The light began to harden.", "The light got harsher."),
        ("I continued to run forward and began to take supplies more seriously.", "I kept moving and started respecting the aid stations."),
        ("I packed every stop with water, drinks, and energy gels.", "I started taking every aid station seriously: water, sports drink, gels."),
        ("I kept moving and started respecting the aid stations. I started taking every aid station seriously: water, sports drink, gels.", "I kept moving, and I started respecting every aid station: water, sports drink, gels."),
        ("I ate and drank a little, not because I was hungry, but because I wanted to leave room for the road ahead.", "I ate a little and drank a little, not because I was hungry, but to leave something for the miles ahead."),
        ("The half-way time was about 1 hour and 55 minutes.", "My half-marathon split was about 1:55."),
        ("I looked at my watch and had an idea.", "I glanced at my watch and knew where I was."),
        ("not bad.", "Not bad."),
        ("straight downhill track", "straight, gently downhill course"),
        ("there is no need to repeatedly pull the rhythm", "there was no constant rhythm-breaking"),
        ("the legs only need to keep moving forward", "my legs only needed to keep moving forward"),
        ("rushing.", "pushing."),
        ("cool and very dry", "cool and very dry"),
        ("not hot and very dry", "cool and very dry"),
        ("Pulled my legs at the finish line.", "My legs tightened up after the finish."),
        ("aesthetics are on the line", "the aesthetics were on point"),
        ("\"the aesthetics were on point\"", "the aesthetics were on point"),
        ("race organization is very simple", "race setup was simple"),
        ("are all not perfunctory", "were anything but perfunctory"),
        ("before the game", "before the race"),
        ("mini tornado", "tiny dust devil"),
        ("a small column of sand", "a small column of dust"),
        ("I'm still a little unwilling to do it. I have the drone on my back and I always want to show off my skills.", "I still wasn’t ready to give up on the drone. I had carried it all this way and wanted to make it count."),
        ("where there is a real saguaros, with big cacti standing upright in the sand, like sentries", "where real saguaros stood upright in the sand like sentries"),
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    text = re.sub(r"\bsub 4\b", "sub-four", text, flags=re.I)
    text = re.sub(r"\b4 hours\b", "four hours", text)
    text = text.replace("I and Siqi", "Siqi and I")
    text = text.replace("｜", " | ")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def load_translation_cache() -> dict[str, str]:
    path = cache_path()
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def save_translation_cache(cache: dict[str, str]) -> None:
    cache_path().write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")


def copy_images() -> list[Path]:
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    sources = sorted([p for p in SOURCE_DIR.iterdir() if p.name == "640" or re.fullmatch(r"640\(\d+\)", p.name)], key=natural_key)
    if len(sources) != len(CAPTIONS):
        raise RuntimeError(f"Expected {len(CAPTIONS)} images, found {len(sources)}")
    out_paths: list[Path] = []
    for idx, src in enumerate(sources, start=1):
        out = IMAGE_DIR / f"{idx:02d}-{SLUG}.webp"
        with Image.open(src) as im:
            im = ImageOps.exif_transpose(im).convert("RGB")
            im.save(out, "WEBP", quality=90, method=6)
        out_paths.append(out)
    return out_paths


def web_path(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def rel_from(target_dir: Path, asset: Path) -> str:
    return Path(path_rel(target_dir, asset)).as_posix()


def path_rel(from_dir: Path, to_path: Path) -> str:
    return os.path.relpath(to_path, from_dir)


def attrs(**kwargs: str) -> str:
    return " ".join(f'{k}="{html.escape(v, quote=True)}"' for k, v in kwargs.items() if v)


def render_body(events: list[dict[str, str]], images: list[Path], lang: str, cache: dict[str, str], base_dir: Path) -> str:
    output: list[str] = []
    img_idx = 0
    for item in events:
        if item["type"] == "image":
            img_path = images[img_idx]
            zh, en, credit = CAPTIONS[img_idx]
            cap_text = zh if lang == "zh" else en
            cap_credit = credit if lang == "zh" else ("Race photographer" if credit == "赛事摄影" else credit)
            output.append(
                f'''<figure class="story-photo">
  <img src="{rel_from(base_dir, img_path)}?v={VERSION}" alt="{html.escape(cap_text, quote=True)}" loading="lazy">
  <figcaption>{html.escape(cap_text)} <span>{html.escape(cap_credit)}</span></figcaption>
</figure>'''
            )
            img_idx += 1
            continue

        raw = item["text"]
        text = raw if lang == "zh" else translate_text(raw, cache)
        tag = classify_text(raw)
        if tag == "h2":
            output.append(f"<h2>{html.escape(text.lstrip('# ').strip())}</h2>")
        elif tag == "meta":
            output.append(f'<p class="story-meta-line">{html.escape(text)}</p>')
        elif tag == "end":
            output.append(f'<p class="story-end">{html.escape(text)}</p>')
        elif tag == "credit":
            output.append(f'<p class="story-credit">{html.escape(text)}</p>')
        else:
            output.append(f"<p>{html.escape(text)}</p>")
    return "\n".join(output)


def classify_text(text: str) -> str:
    if text in {"前言", "后记"} or text.startswith("# "):
        return "h2"
    if text.startswith(("📍", "🎽", "📸")) or text.startswith("- Run50"):
        return "meta"
    if text == "- 本文完 -":
        return "end"
    if re.match(r"^(文字|摄影|设计)丨", text):
        return "credit"
    return "p"


def base_css() -> str:
    return """
:root{color-scheme:light;--ink:#182026;--muted:#69737d;--paper:#fbfaf6;--line:#e5ded2;--accent:#c45b34;--blue:#1b688a;--green:#4c7c59}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;line-height:1.78}
a{color:inherit}.site-nav{position:sticky;top:0;z-index:20;background:rgba(251,250,246,.92);backdrop-filter:blur(16px);border-bottom:1px solid var(--line)}
.site-nav-inner{max-width:1120px;margin:0 auto;padding:12px 20px;display:flex;justify-content:space-between;gap:16px;align-items:center;font-size:14px}
.site-nav a{text-decoration:none;color:#34414c}.site-nav a:hover{color:var(--accent)}
.hero{min-height:92vh;display:grid;align-items:end;background:linear-gradient(180deg,rgba(0,0,0,.16),rgba(0,0,0,.58)),url("../../assets/og-run50-arizona-phoenix-marathon-icons.png?v=20260626-arizona") center/cover no-repeat;color:white}
.hero-inner{width:min(1120px,100%);margin:0 auto;padding:72px 20px 76px}.kicker{font-size:14px;letter-spacing:.14em;text-transform:uppercase;font-weight:800;color:#f7d3a1}
h1{max-width:940px;margin:12px 0 18px;font-size:clamp(36px,7vw,82px);line-height:1.04;letter-spacing:0}.deck{max-width:760px;margin:0;font-size:clamp(18px,2.4vw,25px);line-height:1.5;color:#fff4e7}
.stats{display:flex;flex-wrap:wrap;gap:10px;margin-top:28px}.stat{border:1px solid rgba(255,255,255,.44);padding:8px 12px;border-radius:6px;background:rgba(0,0,0,.18);font-size:14px}
main{max-width:880px;margin:0 auto;padding:54px 20px 76px}.lead-card{border-left:5px solid var(--accent);padding:18px 22px;background:#fff;border-radius:6px;margin-bottom:34px;box-shadow:0 12px 32px rgba(45,34,20,.08)}
.lead-card p{margin:4px 0;color:#3a4650}.story-meta-line{color:var(--blue);font-weight:700;margin:.45rem 0}.article p{font-size:18px;margin:1.1rem 0}
h2{font-size:clamp(26px,4.8vw,42px);line-height:1.18;margin:58px 0 20px;color:#1c2a33}
h2::after{content:"";display:block;width:58px;height:4px;background:linear-gradient(90deg,var(--accent),#e5a64e);margin-top:12px;border-radius:10px}
.story-photo{margin:34px auto}.story-photo img{display:block;width:100%;height:auto;border-radius:8px;box-shadow:0 14px 38px rgba(42,31,19,.16);background:#eee}
figcaption{margin-top:10px;color:#5f6b73;font-size:14px;line-height:1.5}figcaption span{color:#9a5c33}
.story-end{text-align:center;font-weight:800;letter-spacing:.08em;margin-top:46px}.story-credit{color:#7b604c;text-align:center;margin:.35rem 0!important}
.engagement{margin-top:64px;padding-top:28px;border-top:1px solid var(--line)}
.comments-frame{width:100%;min-height:540px;border:0;border-radius:8px;background:#fff;box-shadow:0 12px 32px rgba(45,34,20,.08)}
.footer-links{margin-top:40px;display:flex;flex-wrap:wrap;gap:12px}.footer-links a{padding:10px 13px;border:1px solid var(--line);border-radius:6px;text-decoration:none;background:#fff}
@media(max-width:700px){.site-nav-inner{align-items:flex-start;flex-direction:column}.hero{min-height:88vh}.hero-inner{padding-bottom:48px}main{padding-top:36px}.article p{font-size:17px}.story-photo{margin-left:-6px;margin-right:-6px}figcaption{padding:0 6px}}
""".strip()


def page(title: str, deck: str, lang: str, body_html: str, key: str, canonical: str, og: str, title_short: str) -> str:
    back_text = "Run50 中文目录" if lang == "zh" else "Run50 English Index"
    back_href = "./index.html"
    switch_href = f"../{'english' if lang == 'zh' else 'chinese'}/{SLUG}.html"
    switch_text = "English" if lang == "zh" else "中文"
    fb_href = f"../../facebook/{SLUG}.html"
    locale = "zh-CN" if lang == "zh" else "en"
    engagement_title = "留言 / 浏览" if lang == "zh" else "Comments / Views"
    engagement_heading = "在路边留一句" if lang == "zh" else "Leave a note from the road"
    engagement_note = "不用登录。新的留言会直接显示在页面里。" if lang == "zh" else "No login needed. New comments appear directly on the page."
    engagement_status = "留言区加载中..." if lang == "zh" else "Loading comments..."
    views_label = "浏览" if lang == "zh" else "Views"
    story_css = base_css().replace("../../assets/", "../../../assets/")
    return f"""<!doctype html>
<html lang="{locale}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(deck, quote=True)}">
  <link rel="canonical" href="{canonical}">
  <meta property="og:type" content="article">
  <meta property="og:title" content="{html.escape(title_short, quote=True)}">
  <meta property="og:description" content="{html.escape(deck, quote=True)}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{SITE}/{og}">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="stylesheet" href="../../../assets/zz-engagement.css?v=20260605-1">
  <style>{story_css}</style>
</head>
<body data-story-key="{key}">
  <nav class="site-nav">
    <div class="site-nav-inner">
      <a href="{back_href}">{back_text}</a>
      <div><a href="{switch_href}">{switch_text}</a> · <a href="{fb_href}">Facebook</a> · <a href="../../index.html">Run50</a></div>
    </div>
  </nav>
  <header class="hero">
    <div class="hero-inner">
      <div class="kicker">RUN50 · STATE 29 · ARIZONA</div>
      <h1>{html.escape(title)}</h1>
      <p class="deck">{html.escape(deck)}</p>
      <div class="stats">
        <span class="stat">Buckeye Marathon</span>
        <span class="stat">{DATE_EN if lang == 'en' else DATE_ZH}</span>
        <span class="stat">Buckeye / Phoenix, AZ</span>
        <span class="stat">3:58</span>
      </div>
    </div>
  </header>
  <main>
    <section class="lead-card">
      <p>{'2026 年第一跑：沙漠清晨、机场终点、巨人柱和一场意外的破四。' if lang == 'zh' else 'The first race of 2026: a cold desert morning, an airport finish, saguaros, and a surprise sub-four.'}</p>
      <p>{'官方赛事信息显示，2026 年 Buckeye Marathon 于 1 月 10 日在 Festival Foothills Elementary 起跑，并在 Buckeye Municipal Airport 完赛。' if lang == 'zh' else 'Official race information lists the 2026 Buckeye Marathon on January 10, starting at Festival Foothills Elementary and finishing at Buckeye Municipal Airport.'}</p>
    </section>
    <article class="article">
{body_html}
    </article>
    <section class="zz-engagement" data-zz-engagement data-locale="{locale}" data-page-key="{key}">
      <div class="zz-engagement-shell">
        <div>
          <p class="zz-engagement-kicker">{engagement_title}</p>
          <h2>{engagement_heading}</h2>
          <p class="zz-engagement-note">{engagement_note}</p>
          <div class="zz-engagement-stats"><span class="zz-engagement-stat" id="busuanzi_container_page_pv"><span>{views_label}</span><strong id="busuanzi_value_page_pv" data-zz-view-count>--</strong></span></div>
        </div>
        <div class="zz-engagement-card"><div id="supabase-comments-{key.replace('run50-', '')}" data-zz-supabase-comments></div><p class="zz-engagement-status" data-zz-engagement-status>{engagement_status}</p></div>
      </div>
    </section>
    <div class="footer-links">
      <a href="{back_href}">{back_text}</a>
      <a href="{switch_href}">{switch_text}</a>
      <a href="{fb_href}">Facebook Edition</a>
    </div>
  </main>
  <script src="../../../assets/zz-engagement-config.js?v=20260605-1"></script>
  <script src="../../../assets/zz-engagement.js?v=20260605-1"></script>
</body>
</html>
"""


def facebook_page(body_html: str) -> str:
    title = "Arizona turned a cold desert runway race into my first sub-four of 2026"
    deck = "Buckeye Marathon started in the Phoenix desert and ended beside a runway, with saguaros, dry air, and a finish time I did not see coming."
    css = base_css()
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(deck, quote=True)}">
  <link rel="canonical" href="{CANONICAL_FB}">
  <meta property="og:type" content="article">
  <meta property="og:title" content="{html.escape(title, quote=True)}">
  <meta property="og:description" content="{html.escape(deck, quote=True)}">
  <meta property="og:url" content="{CANONICAL_FB}">
  <meta property="og:image" content="{SITE}/assets/cover-medal-fb-arizona-phoenix-marathon.jpg">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="stylesheet" href="../../assets/zz-engagement.css?v=20260605-1">
  <style>{css}</style>
</head>
<body data-story-key="{KEY_FB}">
  <nav class="site-nav">
    <div class="site-nav-inner">
      <a href="./index.html">Run50 Facebook Stories</a>
      <div><a href="../stories/english/{SLUG}.html">English</a> · <a href="../stories/chinese/{SLUG}.html">中文</a> · <a href="../index.html">Run50</a></div>
    </div>
  </nav>
  <header class="hero">
    <div class="hero-inner">
      <div class="kicker">RUN50 · STATE 29 · ARIZONA</div>
      <h1>{html.escape(title)}</h1>
      <p class="deck">{html.escape(deck)}</p>
      <div class="stats">
        <span class="stat">Buckeye Marathon</span>
        <span class="stat">{DATE_EN}</span>
        <span class="stat">Buckeye / Phoenix, AZ</span>
        <span class="stat">3:58</span>
      </div>
    </div>
  </header>
  <main>
    <section class="lead-card">
      <p>Cold desert air, one long road toward an airport, and the kind of race where your watch says “maybe” until the final turn.</p>
      <p>This is the Facebook-friendly cut of my Arizona chapter: same story, a little tighter, built for sharing.</p>
    </section>
    <article class="article">
{body_html}
    </article>
    <section class="zz-engagement" data-zz-engagement data-locale="en" data-page-key="{KEY_FB}">
      <div class="zz-engagement-shell">
        <div>
          <p class="zz-engagement-kicker">Comments / Views</p>
          <h2>Leave a note from the road</h2>
          <p class="zz-engagement-note">No login needed. New comments appear directly on the page.</p>
          <div class="zz-engagement-stats"><span class="zz-engagement-stat" id="busuanzi_container_page_pv"><span>Views</span><strong id="busuanzi_value_page_pv" data-zz-view-count>--</strong></span></div>
        </div>
        <div class="zz-engagement-card"><div id="supabase-comments-arizona-phoenix-marathon-facebook-en" data-zz-supabase-comments></div><p class="zz-engagement-status" data-zz-engagement-status>Loading comments...</p></div>
      </div>
    </section>
    <div class="footer-links">
      <a href="./index.html">Facebook Stories</a>
      <a href="../stories/english/{SLUG}.html">Full English Story</a>
      <a href="../stories/chinese/{SLUG}.html">Chinese Original</a>
    </div>
  </main>
  <script src="../../assets/zz-engagement-config.js?v=20260605-1"></script>
  <script src="../../assets/zz-engagement.js?v=20260605-1"></script>
</body>
</html>
"""


def make_covers() -> None:
    assets = ROOT / "assets"
    assets.mkdir(exist_ok=True)
    make_og_cover(assets / f"og-run50-{SLUG}-icons.png")
    make_medal_cover(assets / f"cover-medal-{SLUG}.jpg", fb=False)
    make_medal_cover(assets / f"cover-medal-fb-{SLUG}.jpg", fb=True)
    make_thumb_svg(assets / f"thumb-run50-{SLUG}-icons.svg")


def font(path: Path, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(path), size)


def make_og_cover(path: Path) -> None:
    w, h = 1200, 630
    img = Image.new("RGB", (w, h), "#f5d6a2")
    draw = ImageDraw.Draw(img)
    for y in range(h):
        r = int(239 - y * 0.08)
        g = int(192 - y * 0.10)
        b = int(125 - y * 0.06)
        draw.line([(0, y), (w, y)], fill=(r, g, b))
    draw.ellipse((780, 64, 1020, 304), fill="#e7733b")
    draw.polygon([(0, 348), (250, 245), (520, 350), (800, 230), (1200, 360), (1200, 630), (0, 630)], fill="#8f6d55")
    draw.polygon([(0, 406), (340, 300), (645, 430), (920, 305), (1200, 420), (1200, 630), (0, 630)], fill="#c07c4f")
    draw.rectangle((0, 455, w, h), fill="#d7a35b")
    draw.polygon([(535, 630), (620, 455), (675, 455), (800, 630)], fill="#2e3438")
    draw.line((640, 470, 665, 620), fill="#f6e9c4", width=8)
    for x, scale in [(160, 1.05), (250, .72), (930, 1.15), (1035, .82)]:
        cactus(draw, x, 350, scale)
    draw.rounded_rectangle((70, 74, 530, 198), radius=18, fill="#1f2c32")
    draw.text((96, 88), "RUN50 29", font=font(FONT_EN_BOLD, 56), fill="#fff4dd")
    draw.text((96, 150), "ARIZONA", font=font(FONT_EN_BOLD, 26), fill="#f4ba66")
    draw.text((70, 240), "BUCKEYE", font=font(FONT_EN_BOLD, 92), fill="#ffffff")
    draw.text((76, 334), "Race to the Runway", font=font(FONT_EN_BOLD, 42), fill="#1f2c32")
    draw.text((78, 388), "Phoenix desert · Jan 10, 2026 · 3:58", font=font(FONT_EN, 30), fill="#28343a")
    img.save(path)


def cactus(draw: ImageDraw.ImageDraw, x: int, ground: int, scale: float) -> None:
    trunk_h = int(170 * scale)
    trunk_w = int(26 * scale)
    fill = "#37785f"
    draw.rounded_rectangle((x, ground - trunk_h, x + trunk_w, ground), radius=trunk_w // 2, fill=fill)
    arm_w = int(18 * scale)
    draw.rounded_rectangle((x - int(48 * scale), ground - int(120 * scale), x - int(30 * scale), ground - int(58 * scale)), radius=arm_w // 2, fill=fill)
    draw.rounded_rectangle((x - int(48 * scale), ground - int(135 * scale), x - int(10 * scale), ground - int(118 * scale)), radius=arm_w // 2, fill=fill)
    draw.rounded_rectangle((x + int(28 * scale), ground - int(98 * scale), x + int(46 * scale), ground - int(38 * scale)), radius=arm_w // 2, fill=fill)
    draw.rounded_rectangle((x + int(28 * scale), ground - int(112 * scale), x + int(70 * scale), ground - int(96 * scale)), radius=arm_w // 2, fill=fill)


def make_medal_cover(path: Path, fb: bool) -> None:
    w, h = 1200, 750
    img = Image.new("RGB", (w, h), "#ead3a3")
    draw = ImageDraw.Draw(img)
    for i in range(18):
        inset = 18 + i * 3
        col = (110 + i * 4, 80 + i * 3, 52 + i * 2)
        draw.rounded_rectangle((inset, inset, w - inset, h - inset), radius=42, outline=col, width=3)
    draw.rounded_rectangle((70, 70, w - 70, h - 70), radius=26, fill="#f6e5bd", outline="#74543b", width=5)
    draw.rectangle((95, 508, w - 95, 664), fill="#29363b")
    draw.text((122, 96), "AZ", font=font(FONT_EN_BOLD, 145), fill="#b64f31")
    draw.text((350, 112), "RUN50", font=font(FONT_EN_BOLD, 58), fill="#2c373a")
    draw.text((354, 178), "STATE 29", font=font(FONT_EN_BOLD, 36), fill="#a55d37")
    draw.ellipse((715, 94, 935, 314), fill="#d96a36")
    draw.polygon([(120, 478), (360, 300), (570, 450), (780, 286), (1088, 482)], fill="#b46c43")
    draw.polygon([(100, 508), (390, 352), (605, 500), (790, 348), (1100, 506)], fill="#d8984d")
    for x, scale in [(286, .86), (642, .72), (1005, .93)]:
        cactus(draw, x, 510, scale)
    draw.polygon([(520, 664), (590, 510), (622, 510), (710, 664)], fill="#242c30")
    draw.line((608, 528, 620, 646), fill="#fff0c7", width=7)
    draw.text((128, 532), "BUCKEYE", font=font(FONT_EN_BOLD, 74), fill="#fff4dc")
    draw.text((132, 608), "RACE TO THE RUNWAY · JAN 10, 2026", font=font(FONT_EN_BOLD, 27), fill="#f5c56b")
    medal = Image.new("RGBA", (260, 260), (0, 0, 0, 0))
    md = ImageDraw.Draw(medal)
    md.ellipse((32, 32, 228, 228), fill="#c89336", outline="#f8e4a4", width=8)
    md.ellipse((66, 66, 194, 194), outline="#7b5325", width=8)
    md.text((82, 85), "3:58", font=font(FONT_EN_BOLD, 44), fill="#fff6d3")
    md.text((78, 136), "2026", font=font(FONT_EN_BOLD, 34), fill="#55361c")
    medal = medal.rotate(-10, resample=Image.Resampling.BICUBIC, expand=True)
    img.paste(medal, (880, 368), medal)
    draw.text((822, 104 if fb else 686), "PHOENIX DESERT", font=font(FONT_EN_BOLD, 28), fill="#39454a")
    if fb:
        draw.text((790, 684), "COLD START · AIRPORT FINISH", font=font(FONT_EN_BOLD, 26), fill="#39454a")
    img = img.filter(ImageFilter.UnsharpMask(radius=1.2, percent=110))
    img.save(path, quality=92)


def make_thumb_svg(path: Path) -> None:
    path.write_text(
        f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 750">
  <rect width="1200" height="750" fill="#f1c982"/>
  <circle cx="884" cy="175" r="110" fill="#df6b37"/>
  <path d="M0 520 280 310 530 486 782 280 1200 520v230H0z" fill="#b87043"/>
  <path d="M500 750 590 520h48l122 230z" fill="#273034"/>
  <text x="92" y="178" font-family="Arial Black,Arial,sans-serif" font-size="120" fill="#b74f31">AZ</text>
  <text x="92" y="616" font-family="Arial Black,Arial,sans-serif" font-size="92" fill="#243136">BUCKEYE</text>
  <text x="98" y="666" font-family="Arial,sans-serif" font-size="34" fill="#243136">RUN50 29 · RACE TO THE RUNWAY</text>
</svg>
""",
        encoding="utf-8",
    )


def write_pages(events: list[dict[str, str]], images: list[Path]) -> None:
    cache = load_translation_cache()
    zh_body = render_body(events, images, "zh", cache, ROOT / "run50" / "stories" / "chinese")
    en_body = render_body(events, images, "en", cache, ROOT / "run50" / "stories" / "english")
    fb_body = render_body(events, images, "en", cache, ROOT / "run50" / "facebook")
    save_translation_cache(cache)
    (ROOT / "run50" / "stories" / "chinese" / f"{SLUG}.html").write_text(
        page(
            "Run50 #第29州｜亚利桑那：凤凰城马拉松｜沙漠、仙人掌、干冷清晨",
            "二〇二六第一跑，落地凤凰城，跑过 Buckeye 的沙漠公路、巨人柱、机场终点和一场意外的 3:58。",
            "zh",
            zh_body,
            KEY_ZH,
            CANONICAL_ZH,
            f"assets/cover-medal-{SLUG}.jpg",
            "Run50 #第29州｜亚利桑那：凤凰城马拉松",
        ),
        encoding="utf-8",
    )
    (ROOT / "run50" / "stories" / "english" / f"{SLUG}.html").write_text(
        page(
            "Run50 State #29 | Arizona: Buckeye Marathon",
            "My first race of 2026 started in the Phoenix desert: Buckeye’s downhill road, saguaro silhouettes, an airport finish, and a surprise 3:58.",
            "en",
            en_body,
            KEY_EN,
            CANONICAL_EN,
            f"assets/cover-medal-{SLUG}.jpg",
            "Run50 State #29 | Arizona: Buckeye Marathon",
        ),
        encoding="utf-8",
    )
    (ROOT / "run50" / "facebook" / f"{SLUG}.html").write_text(facebook_page(fb_body), encoding="utf-8")


def insert_card(text: str, href: str, new_card: str) -> str:
    text = re.sub(rf"\n\s*<a class=\"story-card[^\"]*\" href=\"\./{re.escape(SLUG)}\.html\">.*?</a>\s*", "\n", text, flags=re.S)
    marker = f'href="{href}"'
    pos = text.find(marker)
    if pos == -1:
        raise RuntimeError(f"Could not find card marker {href}")
    start = text.rfind("<a class=\"story-card", 0, pos)
    end = text.find("</a>", pos)
    if start == -1 or end == -1:
        raise RuntimeError(f"Could not locate full card for {href}")
    end += len("</a>")
    updated = text[:end] + "\n" + textwrap.indent(new_card.strip(), "        ") + text[end:]
    return updated.replace("\n<!-- END RUN50 2024-2025 POLISHED STORIES -->", "\n\n        <!-- END RUN50 2024-2025 POLISHED STORIES -->")


def update_indexes() -> None:
    zh_card = f"""
<a class="story-card run-50" href="./{SLUG}.html">
  <img src="../../../assets/cover-medal-{SLUG}.jpg?v={VERSION}" alt="Run50 #第29州｜亚利桑那：凤凰城马拉松奖牌封面">
  <div class="story-copy">
    <span class="story-tag">Run50 #第29州 · 2026</span>
    <h2>亚利桑那：凤凰城马拉松</h2>
    <p>沙漠清晨、巨人柱、Buckeye 机场终点，还有二〇二六第一场意外破四。</p>
  </div>
</a>"""
    en_card = f"""
<a class="story-card run-50" href="./{SLUG}.html">
  <img src="../../../assets/cover-medal-{SLUG}.jpg?v={VERSION}" alt="Run50 State 29 Arizona Buckeye Marathon medal cover">
  <div class="story-copy">
    <span class="story-tag">Run50 State #29 · 2026</span>
    <h2>Arizona: Buckeye Marathon</h2>
    <p>A cold Phoenix desert morning, saguaros, an airport finish, and the first sub-four of 2026.</p>
  </div>
</a>"""
    fb_card = f"""
<a class="story-card run-50" href="./{SLUG}.html">
  <img src="../../assets/cover-medal-fb-{SLUG}.jpg?v={VERSION}" alt="Arizona Buckeye Marathon Facebook story cover">
  <div class="story-copy">
    <span class="story-tag">Run50 State #29 · Arizona</span>
    <h2>Arizona turned a cold desert runway race into my first sub-four of 2026</h2>
    <p>Buckeye Marathon, the Phoenix desert, and a finish line beside the airport runway.</p>
  </div>
</a>"""

    files = [
        (ROOT / "run50" / "stories" / "chinese" / "index.html", './rocket-city-marathon.html', zh_card),
        (ROOT / "run50" / "stories" / "english" / "index.html", './rocket-city-marathon.html', en_card),
        (ROOT / "run50" / "facebook" / "index.html", './rocket-city-marathon.html', fb_card),
    ]
    for path, marker, card in files:
        text = path.read_text(encoding="utf-8")
        text = insert_card(text, marker, card)
        path.write_text(text, encoding="utf-8")

    update_text_file(ROOT / "run50" / "index.html", [
        ("['Buckeye Marathon', '2026.01.10', '']", "['Buckeye Marathon', '2026.01.10', './stories/english/arizona-phoenix-marathon.html']"),
    ])
    update_text_file(ROOT / "run50" / "stories" / "chinese" / "index.html", [
        ("[{city: '巴基', raceName: 'Buckeye Marathon', date: '2026.01.10', emoji: '🌵', num: '#29', isPlaceholder: true}]", "[{city: '巴基', raceName: 'Buckeye Marathon', date: '2026.01.10', emoji: '🌵', num: '#29', url: './arizona-phoenix-marathon.html'}]"),
    ])
    update_text_file(ROOT / "run50" / "stories" / "english" / "index.html", [
        ("[{city: 'Buckeye', raceName: 'Buckeye Marathon', date: '2026.01.10', emoji: '🌵', num: '#29', isPlaceholder: true}]", "[{city: 'Buckeye', raceName: 'Buckeye Marathon', date: '2026.01.10', emoji: '🌵', num: '#29', url: './arizona-phoenix-marathon.html'}]"),
    ])
    update_hub()
    update_run50_archive()


def update_text_file(path: Path, replacements: list[tuple[str, str]]) -> None:
    text = path.read_text(encoding="utf-8")
    for old, new in replacements:
        if old not in text and new not in text:
            raise RuntimeError(f"Missing pattern in {path}: {old}")
        text = text.replace(old, new)
    path.write_text(text, encoding="utf-8")


def update_hub() -> None:
    path = ROOT / "run50" / "hub.html"
    text = path.read_text(encoding="utf-8")
    if "'Buckeye':{lat:33.3703,lon:-112.5838}" not in text:
        text = text.replace(
            "'Burlington':{lat:44.4759,lon:-73.2121},",
            "'Burlington':{lat:44.4759,lon:-73.2121},\n  'Buckeye':{lat:33.3703,lon:-112.5838},",
        )
    az_entry = "'AZ':[{city:'Buckeye',date:'2026.01.10',story:'stories/english/arizona-phoenix-marathon.html',fb:'facebook/arizona-phoenix-marathon.html'}],"
    if az_entry not in text:
        text = text.replace(
            "'AL':[{city:'Huntsville',date:'2025.12.12',story:'stories/english/rocket-city-marathon.html',fb:'facebook/rocket-city-marathon.html'}],",
            "'AL':[{city:'Huntsville',date:'2025.12.12',story:'stories/english/rocket-city-marathon.html',fb:'facebook/rocket-city-marathon.html'}],\n  " + az_entry,
        )
    path.write_text(text, encoding="utf-8")


def update_run50_archive() -> None:
    path = ROOT / "run50" / "run50.html"
    text = path.read_text(encoding="utf-8")
    text = text.replace(
        '<div class="race-card placeholder" onclick="switchScript(\'script-az\')"',
        '<div class="race-card" onclick="switchScript(\'script-az\')"',
    )
    text = text.replace(
        '<div class="rc-state">亚利桑那</div>',
        f'<a class="rc-state" href="./stories/chinese/{SLUG}.html">亚利桑那</a>',
    )
    text = text.replace(
        '<div class="rc-title">Phoenix Marathon</div>',
        f'<div class="rc-title"><a href="./stories/chinese/{SLUG}.html">Phoenix / Buckeye Marathon</a></div>',
    )
    path.write_text(text, encoding="utf-8")


def update_comment_whitelist() -> None:
    path = ROOT / "run50" / "tools" / "comments.html"
    text = path.read_text(encoding="utf-8")
    for key in [KEY_EN, KEY_FB, KEY_ZH]:
        text = re.sub(rf"\s*'{re.escape(key)}',\n", "\n", text)
    anchor = "'run50-rocket-city-marathon-en',"
    additions = f"{anchor}\n        '{KEY_EN}',\n        '{KEY_FB}',\n        '{KEY_ZH}',"
    text = text.replace(anchor, additions)
    if text.count(KEY_EN) != 3 or text.count(KEY_FB) != 3 or text.count(KEY_ZH) != 3:
        raise RuntimeError("Comment whitelist keys were not inserted in all three allowlists")
    path.write_text(text, encoding="utf-8")


def main() -> None:
    events = read_source_events()
    images = copy_images()
    make_covers()
    write_pages(events, images)
    update_indexes()
    normalize_arizona_story_style()
    print(f"Built {SLUG}: {len(events)} story events, {len(images)} images")


if __name__ == "__main__":
    main()
