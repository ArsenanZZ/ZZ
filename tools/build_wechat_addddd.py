from __future__ import annotations

from dataclasses import dataclass, field
from html import escape, unescape
from html.parser import HTMLParser
from pathlib import Path
import json
import re

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = Path(r"Z:\ZhennanZ Folder\0-Running Story Web\ADDDDD")
OUT_DIR = ROOT / "run50" / "wechat"
VERSION = "20260628-addddd-wechat"


@dataclass
class Block:
    kind: str
    text: str = ""
    src: str = ""
    alt: str = ""
    source_index: int | None = None


@dataclass(frozen=True)
class AdddddConfig:
    slug: str
    title: str
    state_en: str
    series: str
    place: str
    summary: str
    opening: str
    stats: tuple[str, str, str]
    accent: str
    gold: str
    source_html: str | None = None
    source_story: str | None = None
    polished_photos: str | None = None
    start_phrase: str = ""
    first_heading: str = "出发"
    map_asset: str = ""
    map_caption: str = ""
    cover_asset: str = ""
    cover_state: str = ""
    cover_city: str = ""
    cover_year: str = "2024"
    cover_series: str = "RUN50"
    cover_palette: tuple[str, str, str] = ("#edf3f7", "#0b67c2", "#132535")
    finish: str = ""
    chat: str = ""
    caption_rules: tuple[tuple[str, str], ...] = field(default_factory=tuple)


CONFIGS = [
    AdddddConfig(
        slug="kentucky-derby-marathon",
        source_story="run50/stories/chinese/kentucky-derby-marathon.html",
        title="Run50 #第1州｜肯塔基：赛马节马拉松｜四刷主场，蓝草州终破4！",
        state_en="KENTUCKY",
        series="第1州 · 肯塔基 · Derby Festival Marathon",
        place="肯塔基路易斯维尔 · 2024.04.27",
        summary="第四次回到主场跑 Derby Festival Marathon，这一次终于把蓝草州正式点进 Run50 地图，也在熟悉的赛道上跑进 4 小时。",
        opening="四刷 Louisville Derby，热气球、Churchill Downs、Iroquois Park 和一次久等的破四，终于把第1州写成了真正的 Run50 开篇。",
        stats=("01", "LOU", "SUB4"),
        accent="#2f7d57",
        gold="#b98735",
        map_asset="wechat-run50-map-kentucky-1-derby-2024.png",
        map_caption="第1州 · Louisville",
        cover_asset="cover-medal-zh-kentucky-derby.jpg",
        finish="第1州不是最远的一站，却是最像主场的一站。熟悉的街道、赛马节的热闹、Churchill Downs 的马蹄声和最后那个破四，把这场跑成了一个真正的起点。",
        chat="有些比赛跑很多次，意义反而会变。第一次是完成，第二次是熟悉，到了第四次，终于像是在自己的城市里给自己补上一枚迟到的徽章。",
    ),
    AdddddConfig(
        slug="hatfield-mccoy-marathon",
        source_html="Run50 #第1州｜肯塔基#2：哈特菲尔德–麦考伊马拉松｜阿巴拉契亚山谷的脚步声与枪声.html",
        polished_photos=r"Run50 #第1州｜肯塔基#2：哈特菲尔德–麦考伊马拉松｜阿巴拉契亚山谷的脚步声与枪声_files\2-Polished Photos",
        title="Run50 #第1州｜肯塔基#2：哈特菲尔德–麦考伊马拉松｜阿巴拉契亚山谷的脚步声与枪声",
        state_en="KENTUCKY",
        series="第1州 · 肯塔基#2 · Hatfield-McCoy Marathon",
        place="肯塔基 / 西弗吉尼亚边境 · 2024.06.08",
        summary="从蓝草州开进阿巴拉契亚山谷，在 Williamson 的边境小镇和家族传奇里，跑一场人情味很重的小众马拉松。",
        opening="这不是大城市马拉松的声浪，而是一条穿过山谷、河流、煤矿小镇和百年仇怨传说的路。",
        stats=("KY#2", "4.7/5", "VALLEY"),
        accent="#7c5a2c",
        gold="#b98735",
        start_phrase="在威斯康辛被热得够呛",
        first_heading="穿过群岭，奔向边境小镇",
        map_asset="wechat-run50-map-kentucky-extra-hatfield-2024.png",
        map_caption="第1州#2 · Williamson",
        cover_asset="cover-medal-hatfield-mccoy-marathon.jpg",
        cover_state="KY",
        cover_city="WILLIAMSON",
        cover_year="2024",
        cover_series="RUN50 01+",
        cover_palette=("#efe7da", "#7c5a2c", "#20332a"),
        finish="Hatfield-McCoy 这场不像是在城市里刷成绩，更像是把脚步放进一段山谷传说。人少、路安静，但记忆点很密。",
        chat="小比赛有小比赛的好：没有那么多仪式感，却常常有更具体的人和更真切的路。跑完之后想起的不是规模，而是那些递水、挥手、拿着猎枪扮演传说的人。",
        caption_rules=(
            ("阿巴拉契亚", "阿巴拉契亚山谷"),
            ("Williamson", "Williamson 小镇"),
            ("边境", "肯塔基与西弗吉尼亚边境"),
            ("Hatfield", "Hatfield-McCoy 赛道"),
            ("山", "群山之间的赛道"),
        ),
    ),
    AdddddConfig(
        slug="pittsburgh-marathon",
        source_html="Run50 #第19州｜宾夕法尼亚：匹兹堡马拉松｜钢铁之心，拿下摇摆州！.html",
        title="Run50 #第19州｜宾夕法尼亚：匹兹堡马拉松｜钢铁之心，拿下摇摆州！",
        state_en="PENNSYLVANIA",
        series="第19州 · 宾夕法尼亚 · Pittsburgh Marathon",
        place="宾夕法尼亚匹兹堡 · 2024.05.05",
        summary="从赛马节的路易斯维尔开到钢铁城，在桥梁、三河、坡路和摇摆州的政治底色里，完成 Run50 第19州。",
        opening="从蓝草州的赛马场到宾州的钢铁城，这一站把公路清晨、金色田野、桥梁城市和一场硬朗的大赛串了起来。",
        stats=("19", "STEEL", "BRIDGES"),
        accent="#a33a2b",
        gold="#b98735",
        start_phrase="前一周我们才刚刚在",
        first_heading="从赛马场到钢铁城",
        map_asset="wechat-run50-map-pennsylvania-19.png",
        map_caption="第19州 · Pittsburgh",
        cover_asset="cover-medal-pittsburgh-marathon.jpg",
        cover_state="PA",
        cover_city="PITTSBURGH",
        cover_year="2024",
        cover_series="RUN50 19",
        cover_palette=("#e8edf1", "#a33a2b", "#162332"),
        finish="匹兹堡这站有一种很硬的城市质感：桥、河、坡、钢铁史，还有摇摆州的现实感。跑完它，第19州不是一个数字，而是一座城市的重量。",
        chat="有些城市适合用脚去认识。匹兹堡不是那种一眼明亮的地方，但跑过它的桥和坡之后，会慢慢知道为什么它叫钢铁城。",
        caption_rules=(
            ("油菜花", "高速边的金色田野"),
            ("田野", "开往宾州的清晨田野"),
            ("匹兹堡", "抵达匹兹堡"),
            ("Pittsburgh", "Pittsburgh 城市片段"),
            ("桥", "钢铁城的桥"),
            ("三河", "三河交汇的城市"),
            ("起点", "匹兹堡马拉松起点"),
            ("终点", "匹兹堡马拉松终点"),
            ("坡", "匹兹堡的坡路"),
            ("钢铁", "钢铁城路上"),
        ),
    ),
]


class StoryParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.blocks: list[Block] = []
        self.in_article = False
        self.article_depth = 0
        self.current: dict[str, object] | None = None

    def handle_starttag(self, tag: str, attrs_list: list[tuple[str, str | None]]) -> None:
        attrs = {k: v or "" for k, v in attrs_list}
        cls = attrs.get("class", "")
        if tag == "article" and (not cls or "article-body" in cls.split()):
            self.in_article = True
            self.article_depth = 1
        elif self.in_article:
            self.article_depth += 1
        if not self.in_article:
            return
        if tag in {"p", "h2", "h3", "figcaption"}:
            kind = "label" if "section-label" in cls.split() else tag
            self.current = {"kind": kind, "tag": tag, "parts": []}
        elif tag == "img":
            self.blocks.append(Block("img", src=attrs.get("src", ""), alt=attrs.get("alt", "")))

    def handle_endtag(self, tag: str) -> None:
        if self.current and tag == self.current.get("tag", self.current["kind"]):
            text = normalize_text("".join(self.current["parts"]))  # type: ignore[index]
            if text:
                self.blocks.append(Block(str(self.current["kind"]), text=text))
            self.current = None
        if self.in_article:
            self.article_depth -= 1
            if self.article_depth <= 0:
                self.in_article = False

    def handle_data(self, data: str) -> None:
        if self.current:
            self.current["parts"].append(data)  # type: ignore[index]


class ExportContentParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.blocks: list[Block] = []
        self.current: list[str] | None = None
        self.current_tag: str | None = None
        self.img_index = 0

    def handle_starttag(self, tag: str, attrs_list: list[tuple[str, str | None]]) -> None:
        attrs = {k: v or "" for k, v in attrs_list}
        if tag == "p":
            self.current = []
            self.current_tag = tag
        elif tag == "br" and self.current is not None:
            self.current.append("\n")
        elif tag == "img":
            src = attrs.get("data-src") or attrs.get("src", "")
            self.blocks.append(Block("img", src=src, alt=attrs.get("alt", ""), source_index=self.img_index))
            self.img_index += 1

    def handle_endtag(self, tag: str) -> None:
        if self.current is not None and tag == self.current_tag:
            text = normalize_text("".join(self.current))
            if text:
                self.blocks.append(Block("p", text=text))
            self.current = None
            self.current_tag = None

    def handle_data(self, data: str) -> None:
        if self.current is not None:
            self.current.append(data)


def normalize_text(text: str) -> str:
    text = unescape(text).replace("\xa0", " ")
    text = text.replace("Pittsburge", "Pittsburgh")
    return re.sub(r"\s+", " ", text).strip()


def source_file_for_image(folder: Path, index: int) -> Path:
    return folder / ("640" if index == 0 else f"640({index})")


def extract_app_msg_info(path: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="replace")
    key = "wx.cgiData.app_msg_info = "
    start = text.find(key)
    if start < 0:
        raise RuntimeError(f"Could not find app_msg_info in {path}")
    end = text.find("};", start)
    if end < 0:
        raise RuntimeError(f"Could not find app_msg_info end in {path}")
    data = json.loads(text[start + len(key) : end + 1])
    return data["item"][0]


def parse_export(cfg: AdddddConfig) -> list[Block]:
    assert cfg.source_html
    source_path = SOURCE_ROOT / cfg.source_html
    info = extract_app_msg_info(source_path)
    content = unescape(info.get("content", ""))
    parser = ExportContentParser()
    parser.feed(content)
    blocks = parser.blocks
    if cfg.start_phrase:
        start_idx = next(
            (i for i, b in enumerate(blocks) if b.kind == "p" and cfg.start_phrase in b.text),
            0,
        )
        blocks = blocks[start_idx:]
    cleaned: list[Block] = []
    for block in blocks:
        if block.kind == "p":
            text = clean_export_text(block.text)
            if not text:
                continue
            if "- 本文完 -" in text:
                break
            cleaned.append(Block("p", text=text))
        else:
            cleaned.append(block)
    return pair_export_captions(cleaned)


def clean_export_text(text: str) -> str:
    text = normalize_text(text)
    text = text.strip(" \u200b")
    drop_exact = {
        "Miami",
        "Orlando",
        "Arsenan",
        "runDisney Vlog",
        "Run50",
        "#第1州",
        "un50#",
        "Pittsburgh, PA",
        "Louisville, KY",
        "Williamson , KY",
        "Williamson, KY",
    }
    if text in drop_exact:
        return ""
    if text.startswith("#DopeyChallenge") or "data-nonceid" in text:
        return ""
    if text.startswith("丨"):
        return ""
    if text.startswith("📍地点") or text.startswith("🎽赛事"):
        return ""
    if text.startswith("文字丨") or text.startswith("摄影丨") or text.startswith("设计丨"):
        return ""
    if text.startswith("▲") and "Miami" in text:
        return ""
    return text


def looks_like_caption(text: str) -> bool:
    if not text:
        return False
    if text in {"Miami", "Orlando"}:
        return True
    if text.startswith("▲"):
        return True
    if "@Arsenan" in text or "@阿森南" in text:
        return True
    return False


def pair_export_captions(blocks: list[Block]) -> list[Block]:
    paired: list[Block] = []
    i = 0
    while i < len(blocks):
        block = blocks[i]
        if block.kind == "img" and i + 1 < len(blocks) and blocks[i + 1].kind == "p" and looks_like_caption(blocks[i + 1].text):
            i += 2
            paired.append(block)
        else:
            paired.append(block)
            i += 1
    return paired


def parse_story_page(cfg: AdddddConfig) -> list[Block]:
    assert cfg.source_story
    parser = StoryParser()
    parser.feed((ROOT / cfg.source_story).read_text(encoding="utf-8"))
    result: list[Block] = []
    i = 0
    while i < len(parser.blocks):
        block = parser.blocks[i]
        if block.kind == "img":
            cap = ""
            if i + 1 < len(parser.blocks) and parser.blocks[i + 1].kind == "figcaption":
                cap = parser.blocks[i + 1].text
                i += 1
            result.append(Block("img", src="../stories/chinese/" + block.src, alt=block.alt, text=caption_clean(cap)))
        elif block.kind != "figcaption":
            if block.kind == "p" and ("留言 / 阅读" in block.text or "不用登录" in block.text):
                break
            if block.kind in {"h2", "h3"} and ("跑完以后" in block.text or "后记" in block.text):
                break
            if block.kind == "label":
                i += 1
                continue
            result.append(Block(block.kind, text=block.text))
        i += 1
    return result


def caption_clean(text: str) -> str:
    text = normalize_text(re.sub(r"<[^>]+>", "", text))
    text = text.replace("@阿森南", "@Arsenan")
    return text


def ensure_export_images(cfg: AdddddConfig, blocks: list[Block]) -> None:
    if not cfg.source_html:
        return
    source_folder = SOURCE_ROOT / cfg.source_html.replace(".html", "_files")
    target = ROOT / "run50" / "stories" / "chinese" / f"Run50-{title_slug(cfg.slug)}-clean_files"
    target.mkdir(parents=True, exist_ok=True)
    for out_index, block in enumerate([b for b in blocks if b.kind == "img"], start=1):
        if block.source_index is None:
            continue
        source = source_file_for_image(source_folder, block.source_index)
        if not source.exists():
            print(f"missing source image for {cfg.slug}: {source}")
            block.src = ""
            continue
        out = target / f"img-{out_index:03d}.webp"
        if not out.exists():
            with Image.open(source) as img:
                img = img.convert("RGB")
                img.save(out, "WEBP", quality=88, method=6)
        block.src = f"../stories/chinese/{target.name}/{out.name}"


def polished_photo_paths(cfg: AdddddConfig) -> list[Path]:
    if not cfg.polished_photos:
        return []
    folder = SOURCE_ROOT / cfg.polished_photos
    if not folder.exists():
        return []
    paths = []
    for path in folder.glob("Copy #1 of M*.png"):
        match = re.search(r"M(\d+)(?:-\d+)?\.png$", path.name)
        if not match:
            continue
        if "-" in path.stem:
            continue
        paths.append(path)
    def key(path: Path) -> tuple[int, str]:
        match = re.search(r"M(\d+)", path.name)
        return (int(match.group(1)) if match else 9999, path.name)
    return sorted(paths, key=key)


def add_polished_photos(cfg: AdddddConfig, blocks: list[Block]) -> list[Block]:
    paths = polished_photo_paths(cfg)
    if not paths:
        return blocks
    target = ROOT / "run50" / "stories" / "chinese" / f"Run50-{title_slug(cfg.slug)}-clean_files"
    target.mkdir(parents=True, exist_ok=True)
    photo_blocks: list[Block] = []
    for idx, source in enumerate(paths, start=1):
        out = target / f"img-{idx:03d}.webp"
        if not out.exists():
            with Image.open(source) as img:
                img = img.convert("RGB")
                img.save(out, "WEBP", quality=88, method=6)
        photo_blocks.append(Block("img", src=f"../stories/chinese/{target.name}/{out.name}", alt=f"{cfg.title} 图片 {idx}", source_index=idx - 1))
    text_blocks = [b for b in blocks if b.kind != "img"]
    if not text_blocks:
        return photo_blocks
    woven: list[Block] = []
    photo_index = 0
    paragraph_seen = 0
    total_paragraphs = max(1, sum(1 for b in text_blocks if b.kind == "p"))
    total_photos = len(photo_blocks)
    for block in text_blocks:
        woven.append(block)
        if block.kind != "p":
            continue
        paragraph_seen += 1
        target_count = round(paragraph_seen * total_photos / total_paragraphs)
        while photo_index < target_count:
            woven.append(photo_blocks[photo_index])
            photo_index += 1
    woven.extend(photo_blocks[photo_index:])
    return woven


def title_slug(slug: str) -> str:
    return "-".join(part.capitalize() for part in slug.split("-"))


def ensure_cover(cfg: AdddddConfig) -> None:
    if not cfg.cover_state:
        return
    out = ROOT / "assets" / cfg.cover_asset
    if out.exists():
        return
    bg, accent, ink = cfg.cover_palette
    img = Image.new("RGB", (1200, 750), bg)
    draw = ImageDraw.Draw(img)
    font_dir = Path("C:/Windows/Fonts")
    def font(name: str, size: int) -> ImageFont.FreeTypeFont:
        for candidate in [name, "arialbd.ttf", "arial.ttf"]:
            p = font_dir / candidate
            if p.exists():
                return ImageFont.truetype(str(p), size)
        return ImageFont.load_default()
    title_font = font("georgiab.ttf", 118)
    city_font = font("arialbd.ttf", 96)
    small_font = font("arialbd.ttf", 34)
    label_font = font("arialbd.ttf", 42)
    draw.rounded_rectangle((28, 24, 1172, 726), radius=42, fill="#f7f0df", outline=ink, width=9)
    draw.rounded_rectangle((56, 54, 1144, 606), radius=28, fill=bg, outline="#d8c8a6", width=5)
    draw.text((82, 72), cfg.cover_state, font=title_font, fill=accent, stroke_width=3, stroke_fill="#fff7df")
    for x in range(120, 1110, 130):
        y = 430 + ((x // 130) % 2) * 28
        draw.line((x, y, x + 95, y - 48), fill=accent, width=9)
        draw.ellipse((x - 9, y - 9, x + 9, y + 9), fill="#fff3c4", outline=ink, width=2)
    if cfg.slug == "pittsburgh-marathon":
        for x in [510, 620, 730]:
            draw.arc((x - 90, 255, x + 90, 455), 180, 360, fill=ink, width=10)
        draw.rectangle((450, 455, 820, 480), fill=ink)
        draw.text((474, 214), "THREE RIVERS", font=small_font, fill=ink)
    else:
        for x in [520, 640, 760]:
            draw.polygon([(x, 250), (x + 80, 410), (x - 80, 410)], fill="#6f8f5f", outline=ink)
        draw.text((500, 214), "APPALACHIA", font=small_font, fill=ink)
    draw.polygon([(1010, 292), (1100, 328), (1010, 366)], fill="#ffffff", outline=ink)
    for n in range(3):
        draw.rectangle((1010 + n * 30, 292 + n * 12, 1040 + n * 30, 322 + n * 12), fill=ink)
    draw.rounded_rectangle((72, 550, 1128, 650), radius=18, fill=ink, outline="#f8e7bd", width=4)
    city = cfg.cover_city
    city_font_dynamic = city_font
    while draw.textbbox((0, 0), city, font=city_font_dynamic)[2] > 990:
        city_font_dynamic = font("arialbd.ttf", city_font_dynamic.size - 4)
    draw.text((600, 600), city, font=city_font_dynamic, fill="#fff4d0", anchor="mm")
    draw.rounded_rectangle((76, 660, 222, 710), radius=10, fill=accent, outline=ink, width=3)
    draw.text((149, 686), cfg.cover_year, font=label_font, fill="#fff6dc", anchor="mm")
    draw.rounded_rectangle((952, 660, 1128, 710), radius=10, fill=accent, outline=ink, width=3)
    draw.text((1040, 686), cfg.cover_series, font=small_font, fill="#fff6dc", anchor="mm")
    img.save(out, quality=92)
    print(f"generated {out}")


def paragraph_html(text: str, cfg: AdddddConfig) -> str:
    text = emphasize(text, cfg)
    return (
        '<p style="margin: 0 0 18px; line-height: 1.95; text-align: justify; '
        "font-size: 16px; letter-spacing: 0.2px; color: #26343f; "
        "font-family: -apple-system, BlinkMacSystemFont, 'Helvetica Neue', 'PingFang SC', "
        "'Microsoft YaHei', Arial, sans-serif;\">"
        f"{text}</p>"
    )


def emphasize(text: str, cfg: AdddddConfig) -> str:
    escaped = escape(text)
    keywords = [
        "Run50", "肯塔基", "宾夕法尼亚", "匹兹堡", "Pittsburgh", "Louisville",
        "Churchill Downs", "Iroquois Park", "Hatfield-McCoy", "Williamson",
        "阿巴拉契亚", "破4", "4:31 AM", "第19州", "第1州",
    ]
    for kw in keywords:
        e = escape(kw)
        escaped = escaped.replace(
            e,
            f"<strong style=\"color: {cfg.accent}; font-weight: 800;\">{e}</strong>",
        )
    return escaped


def heading_html(text: str, index: int, cfg: AdddddConfig) -> str:
    text = text.lstrip("# ").strip()
    return f"""
<section style="margin: 34px 0 18px; padding-left: 18px; border-left: 5px solid {cfg.accent};">
  <p style="margin: 0 0 5px; font-size: 11px; line-height: 1.4; letter-spacing: 1.6px; color: #8a9bad; font-weight: 800;">FIELD NOTE {index:02d}</p>
  <h2 style="margin: 0; font-size: 23px; line-height: 1.45; color: #102033; font-weight: 900; letter-spacing: 0;">{escape(text)}</h2>
  <p style="margin: 7px 0 0; font-size: 12px; line-height: 1.6; color: {cfg.gold};">{escape(text)}</p>
</section>"""


def figure_html(block: Block, caption: str) -> str:
    if not block.src:
        return ""
    return f"""
<section style="margin: 22px 0 24px;">
  <img src="{escape(block.src)}?v={VERSION}" alt="{escape(block.alt or caption)}" style="width: 100%; height: auto; display: block; margin: 0 auto; border-radius: 6px;">
  <p style="margin: 9px 0 0; padding-left: 10px; border-left: 3px solid #d4a669; font-size: 12px; line-height: 1.6; letter-spacing: 0.2px; color: #6f7d89; font-family: Optima-Regular, 'PingFang SC', serif;">{escape(caption)}</p>
</section>"""


def make_caption(cfg: AdddddConfig, block: Block, context: str, idx: int, used: dict[str, int]) -> str:
    if cfg.slug == "pittsburgh-marathon":
        base = indexed_caption(cfg, idx)
    elif block.text and not looks_like_caption(block.text):
        base = rewrite_caption(block.text)
    else:
        base = ""
        if cfg.polished_photos:
            base = indexed_caption(cfg, idx)
        else:
            for key, label in cfg.caption_rules:
                if key in context:
                    base = label
                    break
        if not base:
            base = indexed_caption(cfg, idx)
    base = normalize_text(base)
    base = re.sub(r"\s*@.*$", "", base)
    if len(base) > 24:
        base = base[:23].rstrip() + "…"
    n = used.get(base, 0) + 1
    used[base] = n
    if n > 1:
        base = f"{base} {n:02d}"
    if any(word in base for word in ["官方", "赛事", "Official"]):
        return f"{base} · 赛事官方"
    return f"{base} @Arsenan"


def rewrite_caption(text: str) -> str:
    replacements = {
        "Kentucky Derby Festival Race Expo": "Derby Expo 取包",
        "Derby Marathon 与 miniMarathon 号码布": "Derby 号码布",
        "Thunder Over Louisville 夜色里的俄亥俄河": "Thunder 烟花夜",
        "Louisville Slugger Field 附近的起点": "Slugger Field 起点",
        "Downtown Louisville 的半马冲线": "Downtown 半马冲线",
        "Urban Bourbon Half Marathon 官方照片": "Urban Bourbon 官方赛照",
        "Urban Bourbon Half Marathon 林荫赛道": "Urban Bourbon 林荫赛道",
        "Urban Bourbon Half Marathon 奖牌": "Urban Bourbon 奖牌",
        "Kentucky Derby Marathon 赛道图": "Derby 赛道图",
        "Kentucky Derby Marathon 完赛奖牌": "Derby 完赛奖牌",
        "赛道上遇见 Lynsey O'Donnell": "赛道上遇见 Lynsey",
    }
    text = normalize_text(text)
    return replacements.get(text, text)


def indexed_caption(cfg: AdddddConfig, idx: int) -> str:
    if cfg.slug == "pittsburgh-marathon":
        labels = [
            "凌晨离开肯塔基", "官方镜头里的奔跑", "第19州进度图", "三河边的钢铁城",
            "起点人潮压满街口", "Expo 号码布合影", "蓝桥下的居民区", "雨后坡上街区",
            "匹兹堡山城住宅", "赛前一顿热饭", "取到号码布", "Dick's 背板打卡",
            "Pittsburgh Marathon 墙", "黄桥和阴天河面", "山城观景台", "树林里的下坡路",
            "俯看 Downtown 天际线", "观景台游客照", "城市天际线合影", "欢迎来到 Pittsburgh",
            "彩色墙前打卡", "山坡上的民居", "阴天里的三河交汇", "桥城全景一眼收下",
            "起跑前的居民区", "低云压着山城", "起点前自拍", "市中心赛前集结",
            "雾气里的起点拱门", "刚开跑就很兴奋", "雨中冲出市中心", "湿漉漉的宽街",
            "第一英里标牌", "彩虹壁画旁经过", "第二英里补给口", "街角壁画和跑者",
            "高楼间的官方赛照", "第一座黄桥", "黄桥上的自拍", "第三英里上桥",
            "红砖街区转弯", "桥头湿地路面", "黄桥上继续前进", "雨后的河边赛道",
            "红色空中步道", "第九英里长街", "十英里街区", "路边餐馆和跑者",
            "小朋友递出加油牌", "路村朋友隔街加油", "击掌的一瞬间", "Run for Cakes 标语",
            "路边水站小摊", "第12英里的桥下", "匹大校园天桥", "Cathedral of Learning",
            "仰望匹大高塔", "第13英里长坡", "橙色花球加油", "教堂街区的缓坡",
            "独角兽也来助威", "社区补给站", "第16英里前后", "转进后半程",
            "后半程一个人顶住", "雨后空旷街道", "橙衣志愿者小队", "黄瓜补给太及时",
            "小朋友的 BAD DAD 牌", "终点前的城市街道", "市民热情击掌", "冲向 Finish Line",
            "官方镜头里的跑姿", "最后几公里的跟跑", "市中心官方赛照", "和帅哥跑友合影",
            "冲线后的第一口气", "奖牌到手的笑", "终点区举手庆祝", "完赛后官方照",
            "奖牌背板单人照", "I Smile for Miles", "赛后自拍还很嗨", "和跑友一起完赛",
            "朋友们的完赛合影", "终点后的市中心", "Bridges of Steel 背板", "喷泉边放松一下",
            "阴天喷泉前起飞", "远眺 Monongahela 斜坡", "奖牌和黄桥同框", "赛后补给路上",
            "回程车里的疲惫", "离开城市后的绿野",
        ]
        if idx <= len(labels):
            return labels[idx - 1]
    if cfg.slug == "hatfield-mccoy-marathon":
        labels = [
            "Hatfield 家族拱门前", "阿巴拉契亚山谷航拍", "山脊间的蜿蜒公路", "航拍看见整片绿",
            "清晨停车场醒来", "夜里开进木屋", "山里木屋亮着灯", "黑熊木屋装饰",
            "墙上的黑熊照片", "木屋客厅和行李", "雾气里的小木屋", "清晨山谷民宿",
            "车窗外的雾山", "Hatfield-McCoy 号码布", "起点前遇见跑友", "早餐店前集合",
            "山雾压着起点", "起跑后抬头看山", "清晨公路第一段", "第二英里路标",
            "第三英里继续上路", "穿过山谷小镇", "路边志愿者加油", "溪水贴着赛道流",
            "第五英里前的补给", "五英里水站很热闹", "加拿大海滩补给站", "阳光照进山谷",
            "晨光里的公路", "山谷里一束太阳", "第六英里路牌", "吃一口西瓜回血",
            "手表记录还很轻松", "第九英里的影子", "沿着溪水往前跑", "阿巴拉契亚长路",
            "路边高草和阳光", "第十英里消防站", "志愿者守着乡间路口", "第十一英里",
            "十二英里前的树荫", "溪边缓一口气", "山坡上的小屋", "小镇街道里的阳光",
            "街口的终点方向", "啦啦队在路边挥手", "山城小车队", "Tug Fork 河边",
            "河谷一片安静", "山路上挥手自拍", "第十四英里", "小路转进深绿",
            "Hatfield 墓地入口", "老房车停在路边", "桥下河水很安静", "树荫里继续跑",
            "ATV 从身边开过", "第十六英里", "碎石小路进林子", "林间窄路很野",
            "草地尽头又是山", "吊桥前的开阔地", "吊桥横跨山谷", "桥上自拍一张",
            "蓝天白云下的山坡", "铁路桥影", "河水绕过山脚", "阳光照在山谷里",
            "白房子旁的小路", "第十九英里", "二十英里补给棚", "补给站里聊两句",
            "Lucky Duck 加油牌", "你已经到这儿了", "第二十二英里", "第二十五英里",
            "烈日下的影子", "最后几英里的加油团", "彩球水站喝一口", "桥上回望山谷",
            "彩色壁画前自拍", "小镇楼梯壁画", "终点前的街道", "拱门下的 Finish",
            "和 Hatfield 老爷子合影", "小镇终点主持人", "举起完赛奖牌", "赛后和跑友自拍",
            "遇见开心的跑友", "终点帐篷下休息", "坐车回到起点", "赛后披萨补能",
            "车窗外的山路", "木屋外最后一眼", "赛后小店自拍", "跑完终于吃上饭",
            "离开前的肯塔基校园", "回程车上满脸疲惫",
        ]
        if idx <= len(labels):
            return labels[idx - 1]
    return f"{cfg.series.split('·')[-1].strip()} {idx:02d}"


def render_blocks(blocks: list[Block], cfg: AdddddConfig) -> str:
    first_is_heading = bool(blocks and blocks[0].kind in {"h2", "h3"})
    parts: list[str] = [] if first_is_heading else [heading_html(cfg.first_heading, 1, cfg)]
    field_index = 0 if first_is_heading else 1
    seen_headings: set[str] = set()
    if not first_is_heading:
        seen_headings.add(cfg.first_heading)
    last_context = cfg.first_heading
    img_index = 0
    used_caps: dict[str, int] = {}
    for block in blocks:
        if block.kind in {"h2", "h3"} or (block.kind == "p" and block.text.startswith("#")):
            text = block.text.lstrip("# ").strip()
            if "Run50#" in text:
                continue
            if text in seen_headings:
                continue
            if text:
                field_index += 1
                seen_headings.add(text)
                parts.append(heading_html(text, field_index, cfg))
                last_context = text
            continue
        if block.kind == "p":
            text = block.text
            if len(text) <= 26 and any(mark in text for mark in ["·", "｜"]) and not text.endswith("。"):
                if text in seen_headings:
                    continue
                field_index += 1
                seen_headings.add(text)
                parts.append(heading_html(text, field_index, cfg))
                last_context = text
            else:
                parts.append(paragraph_html(text, cfg))
                last_context = text
        elif block.kind == "img":
            img_index += 1
            caption = make_caption(cfg, block, last_context, img_index, used_caps)
            parts.append(figure_html(block, caption))
    return "\n".join(part for part in parts if part)


def split_title(title: str) -> str:
    parts = title.split("｜")
    if len(parts) >= 3:
        return "<br>".join(escape(p) for p in parts[:3]) + "<br>" + escape("｜".join(parts[3:]))
    return escape(title)


def finish_card(cfg: AdddddConfig) -> str:
    s1, s2, s3 = cfg.stats
    return f"""
<section style="margin: 46px 0 0; padding: 22px 18px 20px; border-radius: 8px; background: linear-gradient(135deg, #132535 0%, {cfg.accent} 58%, {cfg.gold} 100%); color: #ffffff; box-shadow: 0 14px 32px rgba(19, 37, 53, 0.18);">
  <p style="margin: 0 0 10px; font-size: 11px; line-height: 1.4; letter-spacing: 2.2px; font-weight: 900; color: rgba(255,255,255,0.78);">RUN50 FINISH LINE</p>
  <h2 style="margin: 0 0 12px; font-size: 24px; line-height: 1.35; font-weight: 900; color: #ffffff; letter-spacing: 0;">{escape(cfg.series.split('·')[0].strip())}，收下。</h2>
  <p style="margin: 0; font-size: 15px; line-height: 1.9; color: rgba(255,255,255,0.92); text-align: justify;">{escape(cfg.finish)}</p>
  <section style="margin: 18px 0 0; display: table; width: 100%; border-collapse: collapse;">
    <section style="display: table-cell; width: 33.33%; padding: 10px 6px; border-right: 1px solid rgba(255,255,255,0.18); text-align: center;"><p style="margin: 0; font-size: 18px; line-height: 1.2; font-weight: 900; color: #ffffff;">{escape(s1)}</p><p style="margin: 5px 0 0; font-size: 11px; line-height: 1.4; color: rgba(255,255,255,0.74); letter-spacing: 0.8px;">STATE</p></section>
    <section style="display: table-cell; width: 33.33%; padding: 10px 6px; border-right: 1px solid rgba(255,255,255,0.18); text-align: center;"><p style="margin: 0; font-size: 18px; line-height: 1.2; font-weight: 900; color: #ffffff;">{escape(s2)}</p><p style="margin: 5px 0 0; font-size: 11px; line-height: 1.4; color: rgba(255,255,255,0.74); letter-spacing: 0.8px;">PLACE</p></section>
    <section style="display: table-cell; width: 33.33%; padding: 10px 6px; text-align: center;"><p style="margin: 0; font-size: 18px; line-height: 1.2; font-weight: 900; color: #ffffff;">{escape(s3)}</p><p style="margin: 5px 0 0; font-size: 11px; line-height: 1.4; color: rgba(255,255,255,0.74); letter-spacing: 0.8px;">MEMO</p></section>
  </section>
</section>
<section style="margin: 16px 0 0; padding: 15px 16px; border-left: 4px solid {cfg.gold}; background: #f4f8fb; border-radius: 7px;">
  <p style="margin: 0; font-size: 14px; line-height: 1.9; color: #314657; text-align: justify;">{escape(cfg.chat)}</p>
</section>
<p style="margin: 24px 0 0; text-align: center; color: #8a9bad; font-size: 12px; line-height: 1.8; letter-spacing: 1.2px;">文字 / 摄影 / 设计 · Arsenan</p>"""


def render_page(cfg: AdddddConfig, blocks: list[Block]) -> str:
    body = render_blocks(blocks, cfg)
    title_body = split_title(cfg.title)
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(cfg.title)}</title>
</head>
<body style="margin:0; padding:0; background:#ffffff;">
<main style="max-width: 677px; margin: 0 auto; padding: 28px 18px 42px; box-sizing: border-box; color: #26343f;">
<section style="margin: 0 0 22px; padding-bottom: 18px; border-bottom: 4px solid {cfg.accent};">
  <p style="margin: 0 0 8px; font-size: 12px; line-height: 1.4; letter-spacing: 2px; color: {cfg.accent}; font-weight: 800;">RUN50 DISPATCH · {escape(cfg.state_en)}</p>
  <p style="margin: 0; font-size: 20px; line-height: 1.55; font-weight: 900; color: #17212b; letter-spacing: 0;">{escape(cfg.series)}</p>
</section>
<section style="margin: 0 0 26px; position: relative; width: 100%; aspect-ratio: 16 / 9; border-radius: 9px; overflow: hidden; background: linear-gradient(135deg, #122232, {cfg.accent}); box-shadow: 0 16px 32px rgba(15, 23, 42, .18);">
  <section style="position: absolute; inset: 0; padding: 26px; box-sizing: border-box; color: #fff;">
    <p style="margin: 0 0 12px; font-size: 12px; letter-spacing: 2.2px; font-weight: 900; color: rgba(255,255,255,.72);">16:9 VLOG</p>
    <h1 style="margin: 0; max-width: 510px; font-size: 30px; line-height: 1.28; font-weight: 900; letter-spacing: 0; color: #fff;">{title_body}</h1>
    <p style="margin: 10px 0 0; max-width: 480px; font-size: 15px; line-height: 1.75; color: rgba(255,255,255,.86);">{escape(cfg.summary)}</p>
    <section style="position: absolute; left: 26px; bottom: 22px; padding: 7px 12px; border-radius: 999px; background: rgba(255,255,255,.14); color: rgba(255,255,255,.9); font-size: 12px; line-height: 1.4;">{escape(cfg.place)} · Vlog</section>
  </section>
</section>
<section style="margin: 0 0 28px; padding: 16px 18px; background: #edf5f8; border-radius: 6px;">
  <p style="margin: 0 0 6px; font-size: 12px; line-height: 1.5; letter-spacing: 1px; color: {cfg.accent}; font-weight: 800;">OPENING NOTE</p>
  <p style="margin: 0; font-size: 15px; line-height: 1.9; color: #26343f; text-align: justify;">{emphasize(cfg.opening, cfg)}</p>
</section>
<section style="margin: 0 0 28px;">
  <p style="margin: 0 0 8px; font-size: 14px; line-height: 1.8; color: {cfg.gold}; font-weight: 800;">本文速记</p>
  <p style="margin: 0; font-size: 14px; line-height: 1.9; color: #53616f;">{emphasize(cfg.summary, cfg)}</p>
</section>
<section style="margin: 0 0 24px;">
  <img src="../../assets/{escape(cfg.cover_asset)}?v={VERSION}" alt="{escape(cfg.title)} 奖牌封面" style="width: 100%; height: auto; display: block; margin: 0 auto; border-radius: 7px;">
  <p style="margin: 9px 0 0; padding-left: 10px; border-left: 3px solid {cfg.gold}; font-size: 12px; line-height: 1.65; letter-spacing: 0.2px; color: #6f7d89; font-family: Optima-Regular, 'PingFang SC', serif;">奖牌质感封面 · {escape(cfg.state_en.title())}</p>
</section>
<section style="margin: 0 0 28px;">
  <img src="../../assets/{escape(cfg.map_asset)}?v={VERSION}" alt="{escape(cfg.map_caption)}" style="width: 100%; height: auto; display: block; margin: 0 auto; border-radius: 7px;">
  <p style="margin: 9px 0 0; padding-left: 10px; border-left: 3px solid {cfg.gold}; font-size: 12px; line-height: 1.65; letter-spacing: 0.2px; color: #6f7d89; font-family: Optima-Regular, 'PingFang SC', serif;">{escape(cfg.map_caption)}</p>
</section>
{body}
{finish_card(cfg)}
</main>
</body>
</html>
"""


def build() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for cfg in CONFIGS:
        ensure_cover(cfg)
        blocks = parse_story_page(cfg) if cfg.source_story else parse_export(cfg)
        ensure_export_images(cfg, blocks)
        blocks = add_polished_photos(cfg, blocks)
        out = OUT_DIR / f"{cfg.slug}-modern-rail.html"
        out.write_text(render_page(cfg, blocks), encoding="utf-8", newline="\n")
        images = sum(1 for b in blocks if b.kind == "img" and b.src)
        paragraphs = sum(1 for b in blocks if b.kind == "p")
        print(f"generated {out} paragraphs={paragraphs} images={images}")


if __name__ == "__main__":
    build()
