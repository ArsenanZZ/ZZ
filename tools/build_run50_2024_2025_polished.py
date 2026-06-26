from __future__ import annotations

import hashlib
import html
import io
import json
import math
import os
import re
import shutil
import time
import urllib.parse
import urllib.request
import zipfile
from dataclasses import dataclass, field
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps


REPO_ROOT = Path(__file__).resolve().parents[1]
CHINESE_DIR = REPO_ROOT / "run50" / "stories" / "chinese"
ENGLISH_DIR = REPO_ROOT / "run50" / "stories" / "english"
FACEBOOK_DIR = REPO_ROOT / "run50" / "facebook"
ASSETS_DIR = REPO_ROOT / "assets"
TRANSLATION_CACHE = REPO_ROOT.parent / "run50_2024_2025_translation_cache.json"
REPORT_PATH = REPO_ROOT.parent / "run50_2024_2025_publish_report.json"
SITE_BASE = "https://arsenanzz.github.io/ZZ"


@dataclass
class Story:
    key: str
    source: Path
    slug: str
    asset_dir: str
    run_no: str
    state_code: str
    state_zh: str
    state_en: str
    city_zh: str
    city_en: str
    race_zh: str
    race_en: str
    race_date: str
    card_date: str
    title_zh: str
    title_en: str
    subtitle_zh: str
    subtitle_en: str
    accent: str
    accent2: str
    emoji: str
    script_id: str
    lat: float
    lon: float
    max_images: int = 72
    start_marker: str | None = None
    stop_markers: tuple[str, ...] = ("Outline", "Draft", "文章大纲草案")
    skip_stop_marker_once: str | None = None
    cover_hint: str | None = None
    state_story: bool = True
    extra_label_zh: str | None = None

    @property
    def page_name(self) -> str:
        return f"{self.slug}.html"

    @property
    def page_key_zh(self) -> str:
        return f"run50-{self.slug}-zh"

    @property
    def page_key_en(self) -> str:
        return f"run50-{self.slug}-en"

    @property
    def page_key_fb(self) -> str:
        return f"run50-{self.slug}-facebook-en"

    @property
    def cover_zh(self) -> str:
        return f"cover-medal-zh-{self.slug}.jpg"

    @property
    def cover_en(self) -> str:
        return f"cover-medal-{self.slug}.jpg"

    @property
    def cover_fb(self) -> str:
        return f"cover-medal-fb-{self.slug}.jpg"

    @property
    def cover_city(self) -> str:
        return f"cover-city-{self.slug}.jpg"

    @property
    def og_icon(self) -> str:
        return f"og-run50-{self.slug}-icons.png"

    @property
    def thumb_icon(self) -> str:
        return f"thumb-run50-{self.slug}-icons.svg"


STORIES: list[Story] = [
    Story(
        key="nh",
        source=Path(r"Y:\ZhennanZ Folder\000-Marathon-Story-2024-2025\20240928-NH-New Hampshire Marathon\4-Polished"),
        slug="new-hampshire-clarence-demar-marathon",
        asset_dir="Run50-New-Hampshire-Clarence-DeMar-Marathon-clean_files",
        run_no="#22",
        state_code="NH",
        state_zh="新罕布什尔",
        state_en="New Hampshire",
        city_zh="基恩",
        city_en="Keene",
        race_zh="克拉伦斯·德马尔马拉松",
        race_en="Clarence DeMar Marathon",
        race_date="2024-09-28",
        card_date="2024.09.28",
        title_zh="Run50 #第22州｜新罕布什尔：克拉伦斯·德马尔马拉松｜跑进新英格兰小镇，穿越秋色森林与墓地！",
        title_en="Run50 State #22 | New Hampshire: Clarence DeMar Marathon",
        subtitle_zh="从尼亚加拉瀑布一路开进新英格兰秋色，在基恩的小镇清晨、山林赛道和校园终点里完成第22州。",
        subtitle_en="From Niagara Falls into New England foliage, this was a small-town marathon through Keene, quiet roads, autumn forests, and a campus finish.",
        accent="#1B3A2D",
        accent2="#C97A2B",
        emoji="🍂",
        script_id="script-nh",
        lat=42.9337,
        lon=-72.2781,
        max_images=54,
        start_marker="前言｜秋假没假",
        cover_hint="NH",
    ),
    Story(
        key="ky_grad",
        source=Path(r"Y:\ZhennanZ Folder\000-Marathon-Story-2024-2025\20241103-KY-Louisville-Marathon\4-Polished-Run"),
        slug="louisville-marathon-2024",
        asset_dir="Run50-Louisville-Marathon-2024-clean_files",
        run_no="#1州番外",
        state_code="KY",
        state_zh="肯塔基",
        state_en="Kentucky",
        city_zh="路易斯维尔",
        city_en="Louisville",
        race_zh="路易斯维尔马拉松",
        race_en="Louisville Marathon",
        race_date="2024-11-03",
        card_date="2024.11.03",
        title_zh="Run50 #第1州番外｜肯塔基#3：路易斯维尔马拉松｜博士收官战，送我一朵小红花",
        title_en="Run50 Kentucky Extra | Louisville Marathon 2024: A Doctoral Finish Line",
        subtitle_zh="回到美国跑马起点，在 Floyds Fork 的秋色里把博士生涯跑成一个完整的 loop。",
        subtitle_en="Four years after my first U.S. marathon, I returned to Floyds Fork for a hometown loop that closed the PhD chapter.",
        accent="#1C4A2A",
        accent2="#C44B43",
        emoji="🎓",
        script_id="script-ky-grad",
        lat=38.214,
        lon=-85.480,
        max_images=72,
        cover_hint="KY",
        state_story=False,
        extra_label_zh="博士收官战",
    ),
    Story(
        key="la",
        source=Path(r"Y:\ZhennanZ Folder\000-Marathon-Story-2024-2025\20250119-LA-Louisiana Marathon\1-Polished Vlog"),
        slug="louisiana-marathon",
        asset_dir="Run50-Louisiana-Marathon-clean_files",
        run_no="#23",
        state_code="LA",
        state_zh="路易斯安那",
        state_en="Louisiana",
        city_zh="巴吞鲁日",
        city_en="Baton Rouge",
        race_zh="路易斯安那马拉松",
        race_en="Louisiana Marathon",
        race_date="2025-01-19",
        card_date="2025.01.19",
        title_zh="Run50 #第23州｜路易斯安那：巴吞鲁日马拉松｜法兰西底色，2025 第一跑",
        title_en="Run50 State #23 | Louisiana Marathon: Baton Rouge and the French South",
        subtitle_zh="新年第一跑，从达拉斯转机到新奥尔良，再开进巴吞鲁日，把南方湿地、LSU 紫金色和 Finish Fest 串在一起。",
        subtitle_en="The first race of 2025 stitched together a Dallas layover, New Orleans, Baton Rouge, LSU purple-and-gold, and a warm Finish Fest.",
        accent="#4A1C6F",
        accent2="#D8A72D",
        emoji="🎷",
        script_id="script-la",
        lat=30.4515,
        lon=-91.1871,
        max_images=70,
        cover_hint="LA",
    ),
    Story(
        key="va",
        source=Path(r"Y:\ZhennanZ Folder\000-Marathon-Story-2024-2025\20250412-VA-Blue Ridge Marathon\5-Polished Photos"),
        slug="blue-ridge-marathon",
        asset_dir="Run50-Blue-Ridge-Marathon-clean_files",
        run_no="#24",
        state_code="VA",
        state_zh="弗吉尼亚",
        state_en="Virginia",
        city_zh="罗阿诺克",
        city_en="Roanoke",
        race_zh="蓝岭山马拉松",
        race_en="Blue Ridge Marathon",
        race_date="2025-04-12",
        card_date="2025.04.12",
        title_zh="Run50 #第24州｜弗吉尼亚：蓝岭山马拉松｜全美最虐赛道，3,564英尺的暴力美学",
        title_en="Run50 State #24 | Virginia: Blue Ridge Marathon",
        subtitle_zh="America's Toughest Road Marathon，把马拉松跑成登山赛，也把蓝岭山脉的硬派风光跑进腿里。",
        subtitle_en="America's Toughest Road Marathon turned 26.2 miles into a mountain fight through Roanoke and the Blue Ridge.",
        accent="#1B4332",
        accent2="#B55C2A",
        emoji="🏔️",
        script_id="script-va",
        lat=37.271,
        lon=-79.9414,
        max_images=84,
        cover_hint="VA",
    ),
    Story(
        key="ky_50",
        source=Path(r"Y:\ZhennanZ Folder\000-Marathon-Story-2024-2025\20250426-KY-Derby Marathon-My 50th\3-Polished"),
        slug="kentucky-derby-marathon-2025",
        asset_dir="Run50-Kentucky-Derby-Marathon-2025-clean_files",
        run_no="#50马拉松",
        state_code="KY",
        state_zh="肯塔基",
        state_en="Kentucky",
        city_zh="路易斯维尔",
        city_en="Louisville",
        race_zh="肯塔基德比马拉松",
        race_en="Kentucky Derby Marathon",
        race_date="2025-04-26",
        card_date="2025.04.26",
        title_zh="Run50 #第1州番外｜肯塔基#4：德比马拉松｜三个奖牌，一块蛋糕，我的第50场马拉松！",
        title_en="Run50 Kentucky Extra | Derby Marathon 2025: My 50th Marathon",
        subtitle_zh="工作后的第一场德比马拉松，也是个人第50场全马：周五 5K、周六全马、三块奖牌和一块蛋糕。",
        subtitle_en="A hometown Derby weekend with a Friday 5K, Saturday marathon, three medals, one cake, and my 50th marathon finish.",
        accent="#6B2D8B",
        accent2="#E2B44F",
        emoji="🏇",
        script_id="script-ky-50",
        lat=38.2527,
        lon=-85.7585,
        max_images=76,
        cover_hint="Derby",
        state_story=False,
        extra_label_zh="第50场全马",
    ),
    Story(
        key="nd",
        source=Path(r"Y:\ZhennanZ Folder\000-Marathon-Story-2024-2025\20250529-ND-Fargo Marathon-25st\4-Polished Photos"),
        slug="fargo-marathon",
        asset_dir="Run50-Fargo-Marathon-clean_files",
        run_no="#25",
        state_code="ND",
        state_zh="北达科他",
        state_en="North Dakota",
        city_zh="法戈",
        city_en="Fargo",
        race_zh="法戈马拉松",
        race_en="Fargo Marathon",
        race_date="2025-05-31",
        card_date="2025.05.31",
        title_zh="Run50 #第25州｜北达科他州：法戈马拉松｜跑进美剧小镇，踏上50州跑马的“半程分水岭”！",
        title_en="Run50 State #25 | North Dakota: Fargo Marathon",
        subtitle_zh="从蓝草州一路开到大平原，在粉色天空、玉米地、热浪和破4里完成 Run50 半程分水岭。",
        subtitle_en="A long drive to the northern plains, a pink-sky start, cornfields, heat, and the halfway mark of the Run50 quest.",
        accent="#8B4513",
        accent2="#D8B15F",
        emoji="🌾",
        script_id="script-nd",
        lat=46.8772,
        lon=-96.7898,
        max_images=76,
        cover_hint="ND",
    ),
    Story(
        key="ks",
        source=Path(r"Y:\ZhennanZ Folder\000-Marathon-Story-2024-2025\20250628-KS-Gravel on the hell-St26\6-Polished Photos"),
        slug="hell-on-gravel-marathon",
        asset_dir="Run50-Hell-On-Gravel-Marathon-clean_files",
        run_no="#26",
        state_code="KS",
        state_zh="堪萨斯",
        state_en="Kansas",
        city_zh="埃尔多拉多",
        city_en="El Dorado",
        race_zh="地狱砂石马拉松",
        race_en="Hell on Gravel Marathon",
        race_date="2025-06-28",
        card_date="2025.06.28",
        title_zh="Run50 #第26州｜堪萨斯：地狱砂石马拉松｜冠军就是冠军，哪怕全马只有十个人！",
        title_en="Run50 State #26 | Kansas: Hell on Gravel Marathon",
        subtitle_zh="风、牛群、麦田和砂石路，把一场小到只有十个人的全马跑成了冠军故事。",
        subtitle_en="Wind, cattle, wheat fields, and gravel roads turned a tiny ten-runner marathon into a champion's story.",
        accent="#5C4033",
        accent2="#C2A254",
        emoji="🪨",
        script_id="script-ks",
        lat=37.8172,
        lon=-96.8623,
        max_images=70,
        skip_stop_marker_once="Outline",
        cover_hint="KS",
    ),
    Story(
        key="vt",
        source=Path(r"Y:\ZhennanZ Folder\000-Marathon-Story-2024-2025\20250717-VT-Mad Marathon-St27\4-Polished Photos"),
        slug="mad-marathon",
        asset_dir="Run50-Mad-Marathon-clean_files",
        run_no="#27",
        state_code="VT",
        state_zh="佛蒙特",
        state_en="Vermont",
        city_zh="沃伦",
        city_en="Warren",
        race_zh="疯河谷马拉松",
        race_en="Mad Marathon",
        race_date="2025-07-17",
        card_date="2025.07.17",
        title_zh="Run50 #第27州｜佛蒙特：疯河谷马拉松｜绿山之州的夏天，跑进乡村油画里",
        title_en="Run50 State #27 | Vermont: Mad Marathon",
        subtitle_zh="开进新英格兰腹地，在绿山、谷仓、国旗和乡村小路中，跑进一幅夏天的油画。",
        subtitle_en="A drive into Vermont's Green Mountains for a summer race of barns, flags, village roads, and rolling countryside.",
        accent="#2D6A2D",
        accent2="#D15B43",
        emoji="🍁",
        script_id="script-vt",
        lat=44.112,
        lon=-72.855,
        max_images=86,
        cover_hint="VT",
    ),
    Story(
        key="al",
        source=Path(r"Y:\ZhennanZ Folder\000-Marathon-Story-2024-2025\20251212-AL-Rocket City Marathon\00-Polished Photos"),
        slug="rocket-city-marathon",
        asset_dir="Run50-Rocket-City-Marathon-clean_files",
        run_no="#28",
        state_code="AL",
        state_zh="阿拉巴马",
        state_en="Alabama",
        city_zh="亨茨维尔",
        city_en="Huntsville",
        race_zh="火箭城马拉松",
        race_en="Rocket City Marathon",
        race_date="2025-12-12",
        card_date="2025.12.12",
        title_zh="Run50 #第28州｜阿拉巴马：火箭城马拉松｜寒流来袭，南方跑马也得穿秋裤",
        title_en="Run50 State #28 | Alabama: Rocket City Marathon",
        subtitle_zh="在寒流里的火箭城起跑，把南方州、航天工业、大火箭和路村朋友们一起跑进 2025 收官。",
        subtitle_en="A cold-weather Rocket City run through Huntsville, aerospace history, a giant rocket, and a year-end reunion with friends.",
        accent="#1A3A6B",
        accent2="#D8D6C7",
        emoji="🚀",
        script_id="script-al",
        lat=34.7304,
        lon=-86.5861,
        max_images=78,
        cover_hint="AL",
        start_marker="公众号文章",
    ),
]


TRANSLATION_CACHE_DATA: dict[str, str] = {}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def safe_remove_generated_dir(path: Path) -> None:
    resolved = path.resolve()
    root = CHINESE_DIR.resolve()
    if os.path.commonpath([str(root), str(resolved)]) != str(root):
        raise RuntimeError(f"Refusing to remove outside Chinese stories dir: {path}")
    if not path.name.startswith("Run50-") or not path.name.endswith("-clean_files"):
        raise RuntimeError(f"Refusing to remove unexpected asset dir: {path}")
    if path.exists():
        shutil.rmtree(path)


def load_translation_cache() -> None:
    global TRANSLATION_CACHE_DATA
    if TRANSLATION_CACHE.exists():
        try:
            TRANSLATION_CACHE_DATA = json.loads(TRANSLATION_CACHE.read_text(encoding="utf-8"))
        except Exception:
            TRANSLATION_CACHE_DATA = {}


def save_translation_cache() -> None:
    TRANSLATION_CACHE.write_text(
        json.dumps(TRANSLATION_CACHE_DATA, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def translate_google(text: str) -> str:
    clean = re.sub(r"\s+", " ", text).strip()
    if not clean:
        return ""
    key = hashlib.sha1(clean.encode("utf-8")).hexdigest()
    if key in TRANSLATION_CACHE_DATA:
        return TRANSLATION_CACHE_DATA[key]
    # The public endpoint handles short text reliably. Keep each call small.
    url = (
        "https://translate.googleapis.com/translate_a/single?client=gtx&sl=zh-CN&tl=en&dt=t&q="
        + urllib.parse.quote(clean)
    )
    try:
        with urllib.request.urlopen(url, timeout=18) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        translated = "".join(part[0] for part in data[0] if part and part[0]).strip()
        if not translated or translated.count("?") > max(8, len(translated) // 2):
            translated = clean
    except Exception:
        translated = clean
    TRANSLATION_CACHE_DATA[key] = translated
    time.sleep(0.04)
    return translated


def read_notion_markdown(source: Path) -> tuple[str, str]:
    zips = sorted(source.glob("*.zip"))
    if not zips:
        raise FileNotFoundError(f"No Notion export zip found in {source}")
    with zipfile.ZipFile(zips[0]) as outer:
        md_names = [name for name in outer.namelist() if name.lower().endswith(".md")]
        if md_names:
            name = md_names[0]
            return name, outer.read(name).decode("utf-8", "replace")
        inner_names = [name for name in outer.namelist() if name.lower().endswith(".zip")]
        if not inner_names:
            raise FileNotFoundError(f"No inner zip or markdown found in {zips[0]}")
        with zipfile.ZipFile(io.BytesIO(outer.read(inner_names[0]))) as inner:
            md_names = [name for name in inner.namelist() if name.lower().endswith(".md")]
            if not md_names:
                raise FileNotFoundError(f"No markdown found in {inner_names[0]}")
            name = md_names[0]
            return name, inner.read(name).decode("utf-8", "replace")


def clean_heading(text: str) -> str:
    text = text.strip().strip("#").strip()
    text = re.sub(r"^\*+|\*+$", "", text).strip()
    text = text.replace("｜", "｜").replace("**", "")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def strip_inline_markdown(text: str) -> str:
    text = re.sub(r"!\[[^\]]*]\([^)]*\)", "", text)
    text = re.sub(r"\[([^\]]+)]\(([^)]+)\)", r"\1", text)
    text = text.replace("**", "")
    text = text.replace("__", "")
    text = text.replace("`", "")
    return text.strip()


def markdown_inline_to_html(text: str) -> str:
    text = html.escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"__(.+?)__", r"<strong>\1</strong>", text)
    return text


def clean_blocks(story: Story, markdown: str) -> list[dict[str, str]]:
    lines = markdown.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    start = 0
    if story.start_marker:
        matches = [i for i, line in enumerate(lines) if story.start_marker in line]
        if matches:
            start = matches[-1] if story.key == "nh" else matches[0] + 1
    elif lines and lines[0].lstrip().startswith("#"):
        start = 1

    blocks: list[dict[str, str]] = []
    skipped_once = False
    for line in lines[start:]:
        raw = line.strip()
        if not raw:
            continue
        if raw.startswith("!") or raw.startswith("---"):
            continue
        if "📸" in raw or raw.startswith("对应照片"):
            continue
        if re.match(r"^#+\s*$", raw):
            continue
        heading_match = re.match(r"^(#{1,6})\s*(.+)$", raw)
        if heading_match:
            heading = clean_heading(heading_match.group(2))
            if not heading:
                continue
            if story.skip_stop_marker_once and story.skip_stop_marker_once.lower() in heading.lower() and not skipped_once:
                skipped_once = True
                continue
            if any(marker.lower() in heading.lower() for marker in story.stop_markers):
                break
            if heading in {"公众号文章"}:
                continue
            kind = "h2" if len(heading_match.group(1)) <= 3 else "h3"
            blocks.append({"type": kind, "text": heading})
            continue
        paragraph = strip_inline_markdown(raw)
        if not paragraph:
            continue
        if any(marker.lower() == paragraph.lower() for marker in story.stop_markers):
            break
        paragraph = re.sub(r"^-+\s*", "", paragraph).strip()
        if paragraph:
            blocks.append({"type": "p", "text": paragraph})
    return blocks


def natural_key(path: Path) -> tuple:
    rel = str(path).lower()
    nums = tuple(int(n) for n in re.findall(r"\d+", path.stem))
    if nums:
        return (path.parent.as_posix().lower(), nums, rel)
    return (path.parent.as_posix().lower(), (999999,), rel)


def iter_image_sources(source: Path) -> list[Path]:
    exts = {".jpg", ".jpeg", ".png", ".webp"}
    paths: list[Path] = []
    for path in source.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in exts:
            continue
        if path.name.startswith(".") or path.name.lower() in {"thumbs.db"}:
            continue
        try:
            if path.stat().st_size <= 0:
                continue
        except OSError:
            continue
        paths.append(path)
    return sorted(paths, key=natural_key)


def dhash(image: Image.Image) -> int:
    img = ImageOps.exif_transpose(image).convert("L").resize((9, 8), Image.Resampling.LANCZOS)
    pixels = list(img.getdata())
    bits = 0
    for row in range(8):
        for col in range(8):
            bits = (bits << 1) | (1 if pixels[row * 9 + col] > pixels[row * 9 + col + 1] else 0)
    return bits


def hamming(a: int, b: int) -> int:
    return (a ^ b).bit_count()


@dataclass
class SelectedImage:
    source: Path
    dest_name: str
    width: int
    height: int
    section_hint: str = ""


def load_image_for_rgb(path: Path) -> Image.Image:
    img = Image.open(path)
    img = ImageOps.exif_transpose(img)
    if img.mode in {"RGBA", "LA", "P"}:
        bg = Image.new("RGB", img.size, "white")
        if img.mode == "P":
            img = img.convert("RGBA")
        bg.paste(img, mask=img.split()[-1] if img.mode in {"RGBA", "LA"} else None)
        return bg
    return img.convert("RGB")


def select_and_convert_images(story: Story) -> tuple[list[SelectedImage], dict[str, int | list[str]]]:
    dest_dir = CHINESE_DIR / story.asset_dir
    safe_remove_generated_dir(dest_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)

    all_sources = iter_image_sources(story.source)
    selected: list[SelectedImage] = []
    exact_hashes: set[str] = set()
    recent_hashes: list[int] = []
    skipped = {"invalid": 0, "exact_duplicate": 0, "near_duplicate": 0, "over_cap": 0}

    for source in all_sources:
        if len(selected) >= story.max_images:
            skipped["over_cap"] += 1
            continue
        try:
            data_hash = hashlib.sha1(source.read_bytes()).hexdigest()
            if data_hash in exact_hashes:
                skipped["exact_duplicate"] += 1
                continue
            img = load_image_for_rgb(source)
            image_hash = dhash(img)
        except Exception:
            skipped["invalid"] += 1
            continue

        if any(hamming(image_hash, old) <= 3 for old in recent_hashes[-26:]):
            skipped["near_duplicate"] += 1
            continue

        exact_hashes.add(data_hash)
        recent_hashes.append(image_hash)
        width, height = img.size
        max_side = max(width, height)
        if max_side > 1800:
            scale = 1800 / max_side
            img = img.resize((int(width * scale), int(height * scale)), Image.Resampling.LANCZOS)
            width, height = img.size
        dest_name = f"img-{len(selected) + 1:03d}.webp"
        img.save(dest_dir / dest_name, "WEBP", quality=84, method=6)
        selected.append(SelectedImage(source=source, dest_name=dest_name, width=width, height=height))

    return selected, {
        "source_images": len(all_sources),
        "selected_images": len(selected),
        "skipped": skipped,
        "sample_skipped_note": "Duplicates use exact hash plus conservative perceptual hash against nearby images.",
    }


def find_font(candidates: list[str], size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            try:
                return ImageFont.truetype(str(path), size=size)
            except Exception:
                continue
    return ImageFont.load_default()


FONT_ZH = [
    r"C:\Windows\Fonts\msyh.ttc",
    r"C:\Windows\Fonts\simhei.ttf",
    r"C:\Windows\Fonts\simsun.ttc",
]
FONT_EN = [
    r"C:\Windows\Fonts\segoeui.ttf",
    r"C:\Windows\Fonts\arial.ttf",
]
FONT_BOLD = [
    r"C:\Windows\Fonts\msyhbd.ttc",
    r"C:\Windows\Fonts\seguisb.ttf",
    r"C:\Windows\Fonts\arialbd.ttf",
]


def wrap_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, width: int) -> list[str]:
    words = text.split(" ") if re.search(r"[A-Za-z]", text) else list(text)
    lines: list[str] = []
    current = ""
    joiner = " " if re.search(r"[A-Za-z]", text) else ""
    for word in words:
        candidate = word if not current else current + joiner + word
        if draw.textbbox((0, 0), candidate, font=font)[2] <= width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines[:5]


def crop_cover(img: Image.Image, size: tuple[int, int]) -> Image.Image:
    target_w, target_h = size
    img = ImageOps.exif_transpose(img).convert("RGB")
    w, h = img.size
    scale = max(target_w / w, target_h / h)
    resized = img.resize((math.ceil(w * scale), math.ceil(h * scale)), Image.Resampling.LANCZOS)
    left = (resized.width - target_w) // 2
    top = (resized.height - target_h) // 2
    return resized.crop((left, top, left + target_w, top + target_h))


def pick_cover_source(story: Story, selected: list[SelectedImage]) -> Path | None:
    if not selected:
        return None
    keywords = [story.cover_hint or "", "medal", "finish", "award", "podium", "goal", "end"]
    best: tuple[int, int, Path] | None = None
    for i, item in enumerate(selected):
        name = item.source.name.lower()
        score = 0
        for keyword in keywords:
            if keyword and keyword.lower() in name:
                score += 6
        if item.width > item.height:
            score += 4
        if len(selected) > 12 and int(len(selected) * 0.22) <= i <= int(len(selected) * 0.86):
            score += 8
        score += min(i, 50) // 12
        candidate = (score, i, item.source)
        if best is None or candidate > best:
            best = candidate
    return best[2] if best else selected[0].source


def draw_cover(story: Story, selected: list[SelectedImage], variant: str) -> None:
    cover_source = pick_cover_source(story, selected)
    if cover_source:
        base = crop_cover(load_image_for_rgb(cover_source), (1200, 750))
    else:
        base = Image.new("RGB", (1200, 750), story.accent)
    base = ImageEnhance.Color(base).enhance(0.92)
    overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    for y in range(750):
        alpha = int(20 + 165 * (y / 750) ** 1.7)
        draw.line([(0, y), (1200, y)], fill=(0, 0, 0, alpha))
    draw.rectangle((0, 0, 1200, 750), outline=story.accent2, width=12)
    base = Image.alpha_composite(base.convert("RGBA"), overlay)
    draw = ImageDraw.Draw(base)

    if variant == "zh":
        title = f"{story.run_no}｜{story.state_zh}：{story.race_zh}"
        cover_name = story.cover_zh
        label = f"Run50 {story.run_no} · {story.state_zh}"
        subtitle = story.subtitle_zh
        title_font = find_font(FONT_BOLD + FONT_ZH, 48)
        small_font = find_font(FONT_ZH, 26)
        label_font = find_font(FONT_BOLD + FONT_ZH, 28)
    elif variant == "fb":
        title = f"{story.run_no} | {story.state_en}: {story.race_en}"
        cover_name = story.cover_fb
        label = f"RUN50 PHOTO STORY · {story.state_en.upper()}"
        subtitle = story.subtitle_en
        title_font = find_font(FONT_BOLD + FONT_EN, 48)
        small_font = find_font(FONT_EN, 25)
        label_font = find_font(FONT_BOLD + FONT_EN, 28)
    else:
        title = f"{story.run_no} | {story.state_en}: {story.race_en}"
        cover_name = story.cover_en
        label = f"Run50 {story.run_no} · {story.state_en}"
        subtitle = story.subtitle_en
        title_font = find_font(FONT_BOLD + FONT_EN, 48)
        small_font = find_font(FONT_EN, 25)
        label_font = find_font(FONT_BOLD + FONT_EN, 28)

    draw.rounded_rectangle((54, 58, 364, 116), radius=7, fill=story.accent)
    draw.text((78, 72), label, font=label_font, fill="white")
    draw.text((70, 402), f"{story.emoji} {story.city_en if variant != 'zh' else story.city_zh} · {story.card_date}", font=small_font, fill=(245, 245, 245, 235))
    y = 458
    for line in wrap_text(draw, title, title_font, 1040):
        draw.text((70, y), line, font=title_font, fill="white")
        y += 58
    if y < 665:
        for line in wrap_text(draw, subtitle, small_font, 1040)[:2]:
            draw.text((72, y + 4), line, font=small_font, fill=(235, 238, 240, 230))
            y += 32
    base.convert("RGB").save(ASSETS_DIR / cover_name, "JPEG", quality=90, optimize=True)


def run50_badge_text(story: Story) -> str:
    if story.key == "ky_grad":
        return "Run50 EXTRA"
    if story.key == "ky_50":
        return "Run50 #50"
    match = re.search(r"#(\d+)", story.run_no)
    return f"Run50 #{match.group(1)}" if match else "Run50"


def fit_font(draw: ImageDraw.ImageDraw, text: str, candidates: list[str], start: int, minimum: int, max_width: int) -> ImageFont.ImageFont:
    for size in range(start, minimum - 1, -2):
        font = find_font(candidates, size)
        if draw.textbbox((0, 0), text, font=font)[2] <= max_width:
            return font
    return find_font(candidates, minimum)


def draw_state_scene(draw: ImageDraw.ImageDraw, story: Story, width: int, height: int) -> None:
    accent = hex_to_rgb(story.accent)
    accent2 = hex_to_rgb(story.accent2)
    dark = (32, 36, 43)
    sky = (237, 243, 247)
    ridge1 = tuple(int(c * 0.55 + 245 * 0.45) for c in accent)
    ridge2 = tuple(int(c * 0.78 + 245 * 0.22) for c in accent)
    y0 = int(height * 0.54)
    draw.rectangle((0, 0, width, height), fill=sky)
    draw.ellipse((-180, -210, 540, 260), fill=(255, 255, 255))
    draw.polygon([(0, y0 + 60), (190, y0 - 60), (360, y0 + 35), (520, y0 - 25), (720, y0 + 75), (width, y0 - 35), (width, height), (0, height)], fill=ridge1)
    draw.polygon([(0, y0 + 145), (240, y0 + 15), (500, y0 + 115), (745, y0 + 10), (980, y0 + 130), (width, y0 + 50), (width, height), (0, height)], fill=ridge2)
    draw.polygon([(460, height), (588, y0 + 120), (705, height)], fill=(220, 229, 236))
    draw.line((588, y0 + 120, 575, height), fill=(248, 250, 252), width=4)
    draw.line((588, y0 + 120, 646, height), fill=(248, 250, 252), width=4)

    key = story.key
    if key in {"nh", "vt", "va"}:
        draw.polygon([(70, height - 82), (230, y0 + 48), (390, height - 82)], fill=(54, 88, 93))
        draw.polygon([(180, height - 82), (365, y0 + 12), (555, height - 82)], fill=(68, 112, 112))
        draw.polygon([(330, height - 82), (545, y0 + 68), (760, height - 82)], fill=(94, 132, 120))
        if key == "va":
            cx, cy = 870, height - 170
            points = []
            for i in range(10):
                ang = -math.pi / 2 + i * math.pi / 5
                r = 66 if i % 2 == 0 else 27
                points.append((cx + math.cos(ang) * r, cy + math.sin(ang) * r))
            draw.polygon(points, fill=story.accent2)
        elif key == "vt":
            draw.rectangle((790, height - 188, 1050, height - 86), fill=(125, 55, 45), outline=dark, width=5)
            draw.polygon([(760, height - 188), (920, height - 278), (1080, height - 188)], fill=(98, 38, 35), outline=dark)
            draw.rectangle((850, height - 150, 990, height - 86), fill=(238, 244, 239), outline=dark, width=4)
        else:
            draw.arc((760, height - 250, 1090, height - 40), 8, 170, fill=story.accent2, width=18)
            draw.line((770, height - 122, 1090, height - 122), fill=story.accent2, width=10)
    elif key in {"ky_grad", "ky_50"}:
        draw.ellipse((690, height - 240, 1110, height - 44), outline=story.accent2, width=18)
        draw.line((810, height - 252, 810, height - 116), fill=dark, width=9)
        draw.line((990, height - 252, 990, height - 116), fill=dark, width=9)
        draw.polygon([(765, height - 252), (810, height - 330), (855, height - 252)], fill=(248, 250, 252), outline=dark)
        draw.polygon([(945, height - 252), (990, height - 330), (1035, height - 252)], fill=(248, 250, 252), outline=dark)
        draw.line((720, height - 102, 1090, height - 102), fill=dark, width=7)
    elif key == "la":
        for x in range(650, 1110, 85):
            draw.line((x, height - 105, x + 34, height - 255), fill=dark, width=5)
        draw.arc((620, height - 275, 1120, height - 35), 190, 350, fill=story.accent2, width=16)
        draw.rectangle((0, height - 102, width, height), fill=(105, 154, 177))
    elif key == "nd":
        draw.rectangle((0, height - 108, width, height), fill=(176, 197, 167))
        for x in range(650, 1090, 96):
            draw.arc((x - 84, height - 230, x + 112, height - 40), 200, 338, fill=story.accent2, width=11)
        draw.line((610, height - 110, 1120, height - 110), fill=dark, width=8)
    elif key == "ks":
        draw.rectangle((0, height - 118, width, height), fill=(218, 205, 143))
        for x in range(700, 1100, 42):
            draw.line((x, height - 82, x + 18, height - 198), fill=(164, 120, 42), width=5)
            draw.line((x + 18, height - 198, x - 12, height - 230), fill=(164, 120, 42), width=4)
            draw.line((x + 18, height - 198, x + 48, height - 230), fill=(164, 120, 42), width=4)
    elif key == "al":
        draw.rectangle((0, height - 110, width, height), fill=(207, 224, 229))
        draw.polygon([(860, height - 345), (930, height - 470), (1000, height - 345)], fill=(238, 243, 246), outline=dark)
        draw.rectangle((846, height - 345, 1014, height - 88), fill=(238, 243, 246), outline=dark, width=6)
        draw.polygon([(846, height - 170), (770, height - 88), (846, height - 88)], fill=story.accent2, outline=dark)
        draw.polygon([(1014, height - 170), (1090, height - 88), (1014, height - 88)], fill=story.accent2, outline=dark)
        draw.ellipse((900, height - 316, 960, height - 256), fill=(97, 150, 178), outline=dark, width=5)


def draw_icon_cover_png(story: Story, size: tuple[int, int]) -> Image.Image:
    canvas = Image.new("RGB", size, "#edf3f7")
    draw = ImageDraw.Draw(canvas)
    draw_state_scene(draw, story, *size)

    title = story.city_en.upper()
    subtitle = story.race_en
    title_font = fit_font(draw, title, FONT_BOLD + FONT_EN, 66, 42, 640)
    subtitle_font = fit_font(draw, subtitle, FONT_BOLD + FONT_EN, 28, 22, 640)
    draw.text((64, 64), title, font=title_font, fill="#20242b")
    draw.text((66, 136), subtitle, font=subtitle_font, fill="#667085")

    draw.rounded_rectangle((760, 64, 1122, 228), radius=22, fill="#ffffff", outline="#20242b", width=7)
    badge_font = fit_font(draw, run50_badge_text(story), FONT_BOLD + FONT_EN, 40, 30, 300)
    state_font = fit_font(draw, story.state_en.upper(), FONT_BOLD + FONT_EN, 50, 30, 302)
    draw.text((790, 112), run50_badge_text(story), font=badge_font, fill="#20242b")
    draw.text((790, 166), story.state_en.upper(), font=state_font, fill="#0b67c2")
    return canvas


def svg_scene(story: Story) -> str:
    accent = story.accent
    accent2 = story.accent2
    common = f"""
  <path d="M0 520 L190 380 L360 500 L540 420 L740 535 L980 410 L1200 500 L1200 750 L0 750 Z" fill="#d9e7ee"/>
  <path d="M0 630 L245 470 L500 595 L745 465 L980 615 L1200 540 L1200 750 L0 750 Z" fill="{accent}"/>
  <path d="M450 750 L588 548 L715 750 Z" fill="#dce5ec"/>
  <path d="M588 548 L575 750 M588 548 L650 750" stroke="#f8fafc" stroke-width="5" fill="none"/>
"""
    if story.key in {"nh", "vt", "va"}:
        extra = f"""
  <path d="M70 668 L230 488 L390 668 Z" fill="#36585d"/>
  <path d="M180 668 L365 452 L555 668 Z" fill="#447070"/>
  <path d="M330 668 L545 528 L760 668 Z" fill="#5e8478"/>
"""
        if story.key == "vt":
            extra += """
  <rect x="790" y="562" width="260" height="102" fill="#7d372d" stroke="#20242b" stroke-width="5"/>
  <path d="M760 562 L920 472 L1080 562 Z" fill="#622623" stroke="#20242b" stroke-width="5"/>
  <rect x="850" y="600" width="140" height="64" fill="#eef4ef" stroke="#20242b" stroke-width="4"/>
"""
        elif story.key == "va":
            extra += f"""
  <polygon points="870,500 888,555 946,555 899,589 917,644 870,610 823,644 841,589 794,555 852,555" fill="{accent2}"/>
"""
        else:
            extra += f"""
  <path d="M760 610 C850 500 1000 505 1090 610" stroke="{accent2}" stroke-width="18" fill="none"/>
  <path d="M770 628 L1090 628" stroke="{accent2}" stroke-width="10"/>
"""
        return common + extra
    if story.key in {"ky_grad", "ky_50"}:
        return common + f"""
  <ellipse cx="900" cy="610" rx="210" ry="98" fill="none" stroke="{accent2}" stroke-width="18"/>
  <path d="M810 498 L810 632 M990 498 L990 632" stroke="#20242b" stroke-width="9"/>
  <path d="M765 498 L810 420 L855 498 Z M945 498 L990 420 L1035 498 Z" fill="#f8fafc" stroke="#20242b" stroke-width="5"/>
  <path d="M720 648 L1090 648" stroke="#20242b" stroke-width="7"/>
"""
    if story.key == "la":
        return common + f"""
  <rect x="0" y="646" width="1200" height="104" fill="#699ab1"/>
  <path d="M620 625 C770 500 980 500 1120 625" stroke="{accent2}" stroke-width="16" fill="none"/>
  <path d="M650 645 L684 495 M735 645 L769 495 M820 645 L854 495 M905 645 L939 495 M990 645 L1024 495" stroke="#20242b" stroke-width="5"/>
"""
    if story.key == "nd":
        return common + f"""
  <rect x="0" y="642" width="1200" height="108" fill="#b0c5a7"/>
  <path d="M566 645 C620 525 730 525 790 645 M662 645 C716 525 826 525 886 645 M758 645 C812 525 922 525 982 645 M854 645 C908 525 1018 525 1078 645" stroke="{accent2}" stroke-width="11" fill="none"/>
  <path d="M610 642 L1120 642" stroke="#20242b" stroke-width="8"/>
"""
    if story.key == "ks":
        wheat = "".join(
            f'<path d="M{x} 668 L{x+18} 552 M{x+18} 552 L{x-12} 520 M{x+18} 552 L{x+48} 520" stroke="#a4782a" stroke-width="5" fill="none"/>'
            for x in range(700, 1100, 42)
        )
        return common + f'<rect x="0" y="632" width="1200" height="118" fill="#dacd8f"/>{wheat}'
    if story.key == "al":
        return common + f"""
  <rect x="0" y="640" width="1200" height="110" fill="#cfe0e5"/>
  <path d="M860 405 L930 280 L1000 405 Z" fill="#eef3f6" stroke="#20242b" stroke-width="6"/>
  <rect x="846" y="405" width="168" height="257" fill="#eef3f6" stroke="#20242b" stroke-width="6"/>
  <path d="M846 580 L770 662 L846 662 Z M1014 580 L1090 662 L1014 662 Z" fill="{accent2}" stroke="#20242b" stroke-width="5"/>
  <circle cx="930" cy="435" r="30" fill="#6196b2" stroke="#20242b" stroke-width="5"/>
"""
    return common


def draw_city_cover(story: Story, selected: list[SelectedImage]) -> None:
    og = draw_icon_cover_png(story, (1200, 630))
    og.save(ASSETS_DIR / story.og_icon, "PNG", optimize=True)

    card = Image.new("RGB", (1200, 750), "#edf3f7")
    card.paste(draw_icon_cover_png(story, (1200, 630)), (0, 0))
    draw = ImageDraw.Draw(card)
    draw.rectangle((0, 630, 1200, 750), fill="#f8fafc")
    draw.line((0, 630, 1200, 630), fill=story.accent2, width=8)
    card.save(ASSETS_DIR / story.cover_city, "JPEG", quality=92, optimize=True)

    title = html.escape(story.city_en.upper())
    subtitle = html.escape(story.race_en)
    state = html.escape(story.state_en.upper())
    badge = html.escape(run50_badge_text(story))
    state_size = max(32, min(52, int(660 / max(12, len(state)))))
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 750" role="img" aria-label="{title} Run50 icon cover">
  <rect width="1200" height="750" fill="#edf3f7"/>
  <circle cx="180" cy="40" r="260" fill="#ffffff" opacity=".78"/>
{svg_scene(story)}
  <text x="70" y="104" font-family="Arial, Helvetica, sans-serif" font-size="66" font-weight="900" fill="#20242b">{title}</text>
  <text x="72" y="150" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="800" fill="#667085">{subtitle}</text>
  <rect x="758" y="62" width="364" height="166" rx="22" fill="#ffffff" stroke="#20242b" stroke-width="8"/>
  <text x="790" y="122" font-family="Arial, Helvetica, sans-serif" font-size="41" font-weight="900" fill="#20242b">{badge}</text>
  <text x="790" y="182" font-family="Arial, Helvetica, sans-serif" font-size="{state_size}" font-weight="900" fill="#0b67c2">{state}</text>
</svg>
"""
    write_text(ASSETS_DIR / story.thumb_icon, svg)


def hex_to_rgb(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))


def nearest_heading(blocks: list[dict[str, str]], index: int) -> str:
    for block in reversed(blocks[: index + 1]):
        if block["type"] in {"h2", "h3"}:
            return block["text"]
    return "路途与比赛"


def distribute_images(blocks: list[dict[str, str]], images: list[SelectedImage]) -> dict[int, list[SelectedImage]]:
    if not images:
        return {}
    eligible = [i for i, block in enumerate(blocks) if block["type"] == "p"]
    if not eligible:
        eligible = list(range(len(blocks)))
    result: dict[int, list[SelectedImage]] = {}
    for n, image in enumerate(images):
        pos_index = min(len(eligible) - 1, round((n + 0.5) * (len(eligible) - 1) / max(1, len(images))))
        pos = eligible[pos_index]
        result.setdefault(pos, []).append(image)
    return result


def caption_for(story: Story, heading: str, index: int, lang: str) -> str:
    clean = re.sub(r"^(Chapter|章节|第[一二三四五六七八九十0-9]+章)[^｜|]*[｜|]?", "", heading).strip()
    clean = clean.replace("·", " · ")
    if lang == "zh":
        place = f"{story.state_zh} · {story.city_zh}"
        return f"{place}｜{clean}"
    heading_en = translate_google(clean) if re.search(r"[\u4e00-\u9fff]", clean) else clean
    return f"{story.city_en}, {story.state_en} | {heading_en}"


def render_figure(story: Story, item: SelectedImage, index: int, heading: str, lang: str) -> str:
    if lang == "zh":
        src = f"{story.asset_dir}/{item.dest_name}"
    elif lang == "en":
        src = f"../chinese/{story.asset_dir}/{item.dest_name}"
    else:
        src = f"../stories/chinese/{story.asset_dir}/{item.dest_name}"
    cap = caption_for(story, heading, index, "zh" if lang == "zh" else "en")
    alt = f"{story.race_en} photo {index}" if lang != "zh" else f"{story.race_zh}照片 {index}"
    return (
        "      <figure>\n"
        f'        <img src="{html.escape(src)}" alt="{html.escape(alt)}" loading="lazy" decoding="async">\n'
        f"        <figcaption>{html.escape(cap)} <span>@Arsenan</span></figcaption>\n"
        "      </figure>\n"
    )


def translated_blocks(blocks: list[dict[str, str]]) -> list[dict[str, str]]:
    output: list[dict[str, str]] = []
    for block in blocks:
        if re.search(r"[\u4e00-\u9fff]", block["text"]):
            output.append({"type": block["type"], "text": translate_google(block["text"])})
        else:
            output.append(block.copy())
    return output


def render_article(story: Story, blocks: list[dict[str, str]], images: list[SelectedImage], lang: str, facebook: bool = False) -> str:
    distributed = distribute_images(blocks, images)
    parts: list[str] = []
    if facebook:
        parts.append(
            f'      <p class="fb-lede"><strong>{html.escape(story.city_en)}, {html.escape(story.state_en)}</strong> — {html.escape(story.subtitle_en)}</p>\n'
        )
    for i, block in enumerate(blocks):
        text = block["text"]
        if block["type"] == "h2":
            parts.append(f'      <h2 class="section-label">{markdown_inline_to_html(text)}</h2>\n')
        elif block["type"] == "h3":
            parts.append(f"      <h3>{markdown_inline_to_html(text)}</h3>\n")
        else:
            parts.append(f"      <p>{markdown_inline_to_html(text)}</p>\n")
        for image in distributed.get(i, []):
            heading = nearest_heading(blocks, i)
            figure_index = images.index(image) + 1
            parts.append(render_figure(story, image, figure_index, heading, lang))
    if lang == "zh":
        parts.append('      <p class="end-mark">- 本文完 -</p>\n')
        parts.append('      <p class="credit-line">文字丨Arsenan</p>\n')
        parts.append('      <p class="credit-line">摄影丨Arsenan</p>\n')
        parts.append('      <p class="credit-line">设计丨Arsenan</p>\n')
    else:
        parts.append('      <p class="end-mark">- End -</p>\n')
        parts.append('      <p class="credit-line">Words, photos, and layout by Arsenan</p>\n')
    return "".join(parts)


def story_css(story: Story, facebook: bool = False) -> str:
    paper = "#f6f7f4" if not facebook else "#f4f7fb"
    return f"""
    :root {{
      --paper: {paper};
      --surface: #ffffff;
      --ink: #20242b;
      --muted: #667085;
      --line: #dde5ec;
      --accent: {story.accent};
      --accent2: {story.accent2};
      --soft: #edf3f7;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: linear-gradient(180deg, color-mix(in srgb, var(--accent) 12%, #ffffff) 0, var(--paper) 340px);
      color: var(--ink);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
      line-height: 1.75;
    }}
    a {{ color: var(--accent); text-decoration-thickness: 1px; text-underline-offset: 4px; }}
    .story-nav {{
      max-width: 900px;
      margin: 0 auto;
      padding: 18px 22px 0;
      display: flex;
      gap: 14px;
      justify-content: space-between;
      color: var(--muted);
      font-size: 14px;
    }}
    .story-nav a {{ color: inherit; text-decoration: none; border-bottom: 1px solid transparent; }}
    .story-nav a:hover {{ border-color: currentColor; }}
    .page-header {{
      max-width: 900px;
      margin: 0 auto;
      padding: 42px 22px 24px;
    }}
    .kicker {{ margin: 0 0 14px; color: var(--accent); font-size: 14px; font-weight: 850; }}
    h1 {{
      margin: 0;
      max-width: 820px;
      color: #111827;
      font-size: clamp(29px, 4vw, 42px);
      line-height: 1.18;
      font-weight: 900;
      letter-spacing: 0;
    }}
    .meta {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      align-items: center;
      margin-top: 18px;
      color: var(--muted);
      font-size: 14px;
    }}
    .meta span, .meta a {{
      display: inline-flex;
      align-items: center;
      min-height: 30px;
      padding: 3px 10px;
      border: 1px solid var(--line);
      border-radius: 999px;
      background: rgba(255, 255, 255, .76);
      color: var(--muted);
      text-decoration: none;
    }}
    .dek {{
      margin: 22px 0 0;
      padding-left: 16px;
      border-left: 4px solid var(--accent);
      color: #344054;
      font-size: 16px;
    }}
    .article-shell {{
      background: var(--surface);
      border-top: 1px solid var(--line);
      border-bottom: 1px solid var(--line);
    }}
    .article-body {{
      max-width: 760px;
      margin: 0 auto;
      padding: 54px 22px 64px;
    }}
    .article-body p {{
      margin: 0 0 22px;
      font-size: 17.5px;
      line-height: 1.82;
      color: #2c323f;
    }}
    .article-body p.fb-lede {{
      padding: 18px 20px;
      border-left: 4px solid var(--accent2);
      background: #f7f9fb;
      color: #182230;
      font-size: 18px;
    }}
    .article-body h2.section-label {{
      margin: 50px 0 20px;
      padding-top: 24px;
      border-top: 1px solid var(--line);
      color: var(--accent);
      font-size: 22px;
      font-weight: 850;
    }}
    .article-body h3 {{
      margin: 32px 0 16px;
      color: #111827;
      font-size: 19px;
      font-weight: 850;
    }}
    figure {{ margin: 32px 0; }}
    figure img {{
      display: block;
      width: 100%;
      height: auto;
      border: 1px solid var(--line);
      border-radius: 4px;
      background: #f3f4f6;
    }}
    figcaption {{
      margin-top: 8px;
      color: var(--muted);
      font-size: 13px;
      text-align: center;
    }}
    figcaption span {{ color: #98a2b3; }}
    .end-mark, .credit-line {{
      text-align: center;
      color: var(--muted);
      font-size: 14px;
    }}
    .end-mark {{ margin: 48px 0 12px; font-weight: 800; }}
    .credit-line {{ margin: 6px 0; }}
    .page-footer {{
      max-width: 900px;
      margin: 0 auto;
      padding: 42px 22px 64px;
      color: var(--muted);
      font-size: 14px;
      text-align: center;
    }}
    @media (max-width: 640px) {{
      .story-nav {{ flex-wrap: wrap; }}
      .page-header {{ padding-top: 32px; }}
      .article-body p {{ font-size: 16.5px; }}
    }}
    """


def engagement_html(story: Story, lang: str, depth: str) -> str:
    locale = "zh-CN" if lang == "zh" else "en"
    page_key = story.page_key_zh if lang == "zh" else story.page_key_fb if lang == "fb" else story.page_key_en
    suffix = "zh" if lang == "zh" else "fb" if lang == "fb" else "en"
    if lang == "zh":
        kicker, title, note, loading = "留言 / 阅读", "跑完也可以聊两句", "不用登录就可以留言，新留言会直接显示。", "留言区加载中..."
        read = "阅读"
    else:
        kicker, title, note, loading = "Comments / Views", "Leave a note from the road", "No login needed. New comments appear directly on the page.", "Loading comments..."
        read = "Views"
    return f"""
  <section class="zz-engagement" data-zz-engagement data-locale="{locale}" data-page-key="{html.escape(page_key)}">
    <div class="zz-engagement-shell">
      <div>
        <p class="zz-engagement-kicker">{kicker}</p>
        <h2>{title}</h2>
        <p class="zz-engagement-note">{note}</p>
        <div class="zz-engagement-stats"><span class="zz-engagement-stat" id="busuanzi_container_page_pv"><span>{read}</span><strong id="busuanzi_value_page_pv" data-zz-view-count>--</strong></span></div>
      </div>
      <div class="zz-engagement-card"><div id="supabase-comments-{html.escape(story.slug)}-{suffix}" data-zz-supabase-comments></div><p class="zz-engagement-status" data-zz-engagement-status>{loading}</p></div>
    </div>
  </section>
  <footer class="page-footer">© 2023-2026 ArsenanZZ. Built with love.</footer>
  <script src="{depth}assets/zz-engagement-config.js?v=20260605-1"></script>
  <script src="{depth}assets/zz-engagement.js?v=20260605-1"></script>
"""


def render_page(story: Story, blocks_zh: list[dict[str, str]], blocks_en: list[dict[str, str]], images: list[SelectedImage], lang: str) -> str:
    if lang == "zh":
        title = story.title_zh
        subtitle = story.subtitle_zh
        html_lang = "zh"
        depth = "../../../"
        cover = story.cover_zh
        article = render_article(story, blocks_zh, images, "zh")
        nav = f'<a href="./index.html">← 中文故事</a><a href="../english/{story.page_name}">English</a><a href="../../facebook/{story.page_name}">Facebook</a><a href="../../index.html">Run50</a>'
        kicker = f"Run50 {story.run_no} · {story.state_zh}"
        twitter_title = story.title_en
        locale = "zh-CN"
        canonical_path = f"run50/stories/chinese/{story.page_name}"
    elif lang == "fb":
        title = story.title_en + " | Facebook Edition"
        subtitle = story.subtitle_en
        html_lang = "en"
        depth = "../../"
        cover = story.cover_fb
        article = render_article(story, blocks_en, images, "fb", facebook=True)
        nav = f'<a href="./index.html">← Facebook</a><a href="../stories/english/{story.page_name}">English</a><a href="../stories/chinese/{story.page_name}">中文</a><a href="../index.html">Run50</a>'
        kicker = f"Run50 Photo Story · {story.state_en}"
        twitter_title = story.title_en
        locale = "en_US"
        canonical_path = f"run50/facebook/{story.page_name}"
    else:
        title = story.title_en
        subtitle = story.subtitle_en
        html_lang = "en"
        depth = "../../../"
        cover = story.cover_en
        article = render_article(story, blocks_en, images, "en")
        nav = f'<a href="./index.html">← English Stories</a><a href="../chinese/{story.page_name}">中文</a><a href="../../facebook/{story.page_name}">Facebook</a><a href="../../index.html">Run50</a>'
        kicker = f"Run50 {story.run_no} · {story.state_en}"
        twitter_title = story.title_en
        locale = "en_US"
        canonical_path = f"run50/stories/english/{story.page_name}"

    cover_url = f"{SITE_BASE}/assets/{story.og_icon}?v=20260626-run50-2024-2025"
    canonical = f"{SITE_BASE}/{canonical_path}"
    return f"""<!doctype html>
<html lang="{html_lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(subtitle)}">
  <link rel="canonical" href="{html.escape(canonical)}">
  <meta property="og:title" content="{html.escape(title)}">
  <meta property="og:description" content="{html.escape(subtitle)}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="{html.escape(canonical)}">
  <meta property="og:site_name" content="ArsenanZZ">
  <meta property="og:locale" content="{locale}">
  <meta property="og:image" content="{html.escape(cover_url)}">
  <meta property="og:image:secure_url" content="{html.escape(cover_url)}">
  <meta property="og:image:type" content="image/png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="{html.escape(title)} cover">
  <meta property="article:author" content="Arsenan">
  <meta property="article:published_time" content="{story.race_date}T07:00:00-05:00">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{html.escape(twitter_title)}">
  <meta name="twitter:description" content="{html.escape(subtitle)}">
  <meta name="twitter:image" content="{html.escape(cover_url)}">
  <link rel="stylesheet" href="{depth}assets/zz-engagement.css?v=20260605-1">
  <style>{story_css(story, facebook=(lang == "fb"))}</style>
</head>
<body>
  <nav class="story-nav" aria-label="Page navigation">
    {nav}
  </nav>
  <header class="page-header">
    <p class="kicker">{html.escape(kicker)}</p>
    <h1>{html.escape(title)}</h1>
    <div class="meta">
      <span>By Arsenan</span>
      <span>Race: {html.escape(story.card_date)}</span>
      <span>{html.escape(story.city_en if lang != "zh" else story.city_zh)}, {html.escape(story.state_en if lang != "zh" else story.state_zh)}</span>
    </div>
    <div class="dek">{html.escape(subtitle)}</div>
  </header>
  <main class="article-shell">
    <article class="article-body">
{article}    </article>
  </main>
{engagement_html(story, lang, depth)}</body>
</html>
"""


def generate_pages(story: Story, blocks_zh: list[dict[str, str]], images: list[SelectedImage]) -> dict[str, int]:
    blocks_en = translated_blocks(blocks_zh)
    write_text(CHINESE_DIR / story.page_name, render_page(story, blocks_zh, blocks_en, images, "zh"))
    write_text(ENGLISH_DIR / story.page_name, render_page(story, blocks_zh, blocks_en, images, "en"))
    write_text(FACEBOOK_DIR / story.page_name, render_page(story, blocks_zh, blocks_en, images, "fb"))
    return {"blocks_zh": len(blocks_zh), "blocks_en": len(blocks_en)}


def card_html(story: Story, variant: str) -> str:
    if variant == "zh":
        href = f"./{story.page_name}"
        img = f"../../../assets/{story.cover_en}?v=20260626-medal-polish"
        meta = f"{story.state_zh}{story.city_zh} · {story.card_date}"
        title = story.title_zh
        desc = story.subtitle_zh
        foot1, foot2 = "长文图记", "阅读 →"
    elif variant == "fb":
        href = f"./{story.page_name}"
        img = f"../../assets/{story.cover_fb}?v=20260626-medal-polish"
        meta = f"{story.city_en}, {story.state_en} · {story.card_date}"
        title = story.title_en
        desc = story.subtitle_en
        foot1, foot2 = "Facebook edition", "Open →"
    else:
        href = f"./{story.page_name}"
        img = f"../../../assets/{story.cover_en}?v=20260626-medal-polish"
        meta = f"{story.city_en}, {story.state_en} · {story.card_date}"
        title = story.title_en
        desc = story.subtitle_en
        foot1, foot2 = "English story", "Read →"
    return f"""
        <a class="story-card run-50" href="{href}">
          <img src="{img}" alt="{html.escape(title)} cover" loading="lazy" decoding="async">
          <div class="story-copy">
            <p class="story-meta">{html.escape(meta)}</p>
            <h2 class="story-title">{html.escape(title)}</h2>
            <p class="story-desc">{html.escape(desc)}</p>
            <div class="story-foot"><span>{foot1}</span><span>{foot2}</span></div>
          </div>
        </a>
"""


def replace_generated_block(text: str, marker: str, block: str, insert_before: str) -> str:
    begin = f"<!-- BEGIN {marker} -->"
    end = f"<!-- END {marker} -->"
    wrapped = f"{begin}\n{block}\n        {end}\n"
    pattern = re.compile(re.escape(begin) + r".*?" + re.escape(end) + r"\n?", re.S)
    if pattern.search(text):
        return pattern.sub(wrapped, text)
    idx = text.find(insert_before)
    if idx == -1:
        raise RuntimeError(f"Insert marker not found for {marker}")
    return text[:idx] + wrapped + text[idx:]


def update_story_indexes() -> None:
    marker = "RUN50 2024-2025 POLISHED STORIES"
    chinese = read_text(CHINESE_DIR / "index.html")
    english = read_text(ENGLISH_DIR / "index.html")
    facebook = read_text(FACEBOOK_DIR / "index.html")

    zh_block = "".join(card_html(story, "zh") for story in STORIES)
    en_block = "".join(card_html(story, "en") for story in STORIES)
    fb_block = "".join(card_html(story, "fb") for story in STORIES)

    insert_ch = '      </div>\n    </section>\n\n    <section class="story-section run-cn-zone"'
    insert_en = insert_ch
    insert_fb = '      </div>\n    </section>'
    chinese = replace_generated_block(chinese, marker, zh_block, insert_ch)
    english = replace_generated_block(english, marker, en_block, insert_en)
    facebook = replace_generated_block(facebook, marker, fb_block, insert_fb)
    write_text(CHINESE_DIR / "index.html", chinese)
    write_text(ENGLISH_DIR / "index.html", english)
    write_text(FACEBOOK_DIR / "index.html", facebook)


def patch_story_mapping_object(text: str) -> str:
    additions = {
        "NH-基恩": "new-hampshire-clarence-demar-marathon.html",
        "LA-巴吞鲁日": "louisiana-marathon.html",
        "VA-罗阿诺克": "blue-ridge-marathon.html",
        "ND-法戈": "fargo-marathon.html",
        "KS-Gravel": "hell-on-gravel-marathon.html",
        "KS-埃尔多拉多": "hell-on-gravel-marathon.html",
        "VT-沃伦": "mad-marathon.html",
        "AL-亨茨维尔": "rocket-city-marathon.html",
    }
    match = re.search(r"const _STORY_MAPPING = \{(.*?)\n\};", text, flags=re.S)
    if not match:
        return text
    body = match.group(1)
    existing = dict(re.findall(r"'([^']+)'\s*:\s*'([^']+)'", body))
    existing.update(additions)
    lines = [f"  '{key}': '{value}'" for key, value in sorted(existing.items())]
    replacement = "const _STORY_MAPPING = {\n" + ",\n".join(lines) + "\n};"
    return text[: match.start()] + replacement + text[match.end() :]


def update_run50_home() -> None:
    path = REPO_ROOT / "run50" / "run50.html"
    text = read_text(path)
    text = patch_story_mapping_object(text)

    for story in STORIES:
        pattern = re.compile(
            r"<div class=\"race-card(?: placeholder)?\"(?: data-story-file=\"[^\"]+\")? onclick=\"switchScript\('"
            + re.escape(story.script_id)
            + r"'\)\""
        )
        replacement = (
            f'<div class="race-card" data-story-file="{story.page_name}" '
            f'onclick="switchScript(\'{story.script_id}\')"'
        )
        text = pattern.sub(replacement, text)

    text = re.sub(
        r"const isPlaceholder = card\.classList\.contains\('placeholder'\);",
        "const isPlaceholder = card.classList.contains('placeholder') && !card.dataset.storyFile;",
        text,
    )
    if "const storyFileAttr = card.dataset.storyFile || '';" not in text:
        text = re.sub(
            r"const date = card\.querySelector\('\.rc-date'\)\?\.textContent \|\| '';",
            "const date = card.querySelector('.rc-date')?.textContent || '';\n    const storyFileAttr = card.dataset.storyFile || '';",
            text,
            count=1,
        )
    text = re.sub(
        r"_STATE_RACES\[abbr\]\.push\(\{\n        city, raceName, date, emoji, num, isPlaceholder, cardId: card\.id\n      \}\);",
        "_STATE_RACES[abbr].push({\n        city, raceName, date, emoji, num, isPlaceholder, cardId: card.id, storyFile: storyFileAttr\n      });",
        text,
        count=1,
    )
    text = text.replace("const storyFile = _STORY_MAPPING[storyKey];", "const storyFile = r.storyFile || _STORY_MAPPING[storyKey];")
    text = text.replace("'LA', 'VA', 'ND', 'KS', 'VT', 'AL', 'AZ'", "'AZ'")
    write_text(path, text)


def update_hub() -> None:
    path = REPO_ROOT / "run50" / "hub.html"
    if not path.exists():
        return
    text = read_text(path)
    race_lines: dict[str, list[str]] = {}
    base = {
        "KY": [
            "{city:'Louisville',date:'Nov 8, 2020',story:'stories/english/louisville-marathon.html',fb:'facebook/louisville-marathon.html'}",
            "{city:'Louisville',date:'Apr 27, 2024',story:'stories/english/kentucky-derby-marathon.html',fb:'facebook/kentucky-derby-marathon.html'}",
        ],
        "OH": ["{city:'Cleveland',date:'Oct 24, 2021',story:'stories/english/cleveland-marathon.html',fb:'facebook/cleveland-marathon.html'}"],
        "IL": ["{city:'Chicago',date:'Oct 2023',story:'stories/english/chicago-marathon.html',fb:'facebook/chicago-marathon.html'}"],
        "AR": ["{city:'Little Rock',date:'Mar 2025',story:'stories/english/little-rock-marathon.html',fb:'facebook/little-rock-marathon.html'}"],
        "FL": ["{city:'Miami',date:'Jan 2025',story:'stories/english/miami-marathon.html',fb:'facebook/miami-marathon.html'}"],
        "TN": ["{city:'Nashville',date:'Apr 2025',story:'stories/english/nashville-marathon.html',fb:'facebook/nashville-marathon.html'}"],
        "TX": ["{city:'San Antonio',date:'Dec 2024',story:'stories/english/san-antonio-marathon.html',fb:'facebook/san-antonio-marathon.html'}"],
        "SC": ["{city:'Greer',date:'Feb 2025',story:'stories/english/south-carolina-marathon.html',fb:'facebook/south-carolina-marathon.html'}"],
        "WV": ["{city:'Huntington',date:'May 2025',story:'stories/english/west-virginia-marathon.html',fb:'facebook/west-virginia-marathon.html'}"],
        "MI": ["{city:'Grand Rapids',date:'Aug 2024',story:'stories/english/michigan-meadows-marathon.html',fb:'facebook/michigan-meadows-marathon.html'}"],
    }
    for code, entries in base.items():
        race_lines.setdefault(code, []).extend(entries)
    for story in STORIES:
        race_lines.setdefault(story.state_code, []).append(
            "{city:'%s',date:'%s',story:'stories/english/%s',fb:'facebook/%s'}"
            % (story.city_en, story.card_date, story.page_name, story.page_name)
        )
    object_lines = ["const _RACES = {"]
    for code in sorted(race_lines):
        object_lines.append(f"  '{code}':[{','.join(race_lines[code])}],")
    object_lines[-1] = object_lines[-1].rstrip(",")
    object_lines.append("};")
    text = re.sub(r"const _RACES = \{.*?\n\};", "\n".join(object_lines), text, flags=re.S)

    # Add missing city coordinates to the inline map if they are not already present.
    city_insert = ""
    for story in STORIES:
        if f"'{story.city_en}':" not in text:
            city_insert += f"  '{story.city_en}':{{lat:{story.lat},lon:{story.lon}}},\n"
    if city_insert:
        text = text.replace("};\n\nconst _RACES = {", city_insert + "};\n\nconst _RACES = {")

    write_text(path, text)


def update_supabase_sql() -> None:
    path = REPO_ROOT / "supabase" / "run50-comments.sql"
    if not path.exists():
        return
    text = read_text(path)
    new_ids: list[str] = []
    for story in STORIES:
        new_ids.extend([story.page_key_fb, story.page_key_en, story.page_key_zh])

    def repl(match: re.Match[str]) -> str:
        block = match.group(1)
        ids = re.findall(r"'([^']+)'", block)
        merged = sorted(set(ids + new_ids))
        formatted = "\n".join(f"      '{page_id}'," for page_id in merged)
        formatted = formatted.rstrip(",")
        return "page_id in (\n" + formatted + "\n    )"

    text = re.sub(r"page_id in \(\n(.*?)\n\s*\)", repl, text, flags=re.S)
    write_text(path, text)


def process_story(story: Story) -> dict[str, object]:
    print(f"[story] {story.slug}")
    md_name, markdown = read_notion_markdown(story.source)
    blocks = clean_blocks(story, markdown)
    images, image_report = select_and_convert_images(story)
    draw_cover(story, images, "zh")
    draw_cover(story, images, "en")
    draw_cover(story, images, "fb")
    draw_city_cover(story, images)
    page_report = generate_pages(story, blocks, images)
    return {
        "slug": story.slug,
        "markdown": md_name,
        "blocks": len(blocks),
        "pages": page_report,
        "images": image_report,
    }


def main() -> None:
    load_translation_cache()
    requested = {
        item.strip().lower()
        for item in os.environ.get("RUN50_STORIES", "").replace(";", ",").split(",")
        if item.strip()
    }
    selected_stories = [
        story
        for story in STORIES
        if not requested or story.key.lower() in requested or story.slug.lower() in requested
    ]
    if requested and not selected_stories:
        raise RuntimeError(f"No stories matched RUN50_STORIES={sorted(requested)}")
    report: list[dict[str, object]] = []
    for story in selected_stories:
        report.append(process_story(story))
        save_translation_cache()
    update_story_indexes()
    update_run50_home()
    update_hub()
    update_supabase_sql()
    save_translation_cache()
    REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print(f"[done] report: {REPORT_PATH}")


if __name__ == "__main__":
    main()
