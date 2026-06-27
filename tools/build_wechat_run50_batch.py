from __future__ import annotations

from dataclasses import dataclass
from html import escape
from html.parser import HTMLParser
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "run50" / "wechat"
VERSION = "20260627-wechat-batch"


@dataclass(frozen=True)
class StoryConfig:
    slug: str
    state_en: str
    series: str
    place: str
    public_title: str
    summary: str
    stat_one: str
    stat_two: str
    stat_three: str
    accent: str = "#2d6f9f"
    gold: str = "#b98735"
    generate: bool = True


CONFIGS: list[StoryConfig] = [
    StoryConfig(
        "michigan-meadows-marathon",
        "MICHIGAN",
        "第21州 · 密歇根 · Meadow Marathon",
        "密歇根大急流城 · 2024.08.25",
        "Run50 #第21州 密歇根 梅多马拉松 在大急流城数圈，6次穿越千禧公园！",
        "在大急流城千禧公园跑六圈全马：Parkrun 开头、车祸小插曲、Grand River 日出、六道轮回和 4 小时 44 分的三味真火。",
        "21", "6", "4:44",
        generate=False,
    ),
    StoryConfig(
        "new-hampshire-clarence-demar-marathon",
        "NEW HAMPSHIRE",
        "第22州 · 新罕布什尔 · Clarence DeMar Marathon",
        "新罕布什尔基恩 · 2024.09.28",
        "Run50 #第22州｜新罕布什尔：克拉伦斯·德马尔马拉松｜跑进新英格兰小镇，穿越秋色森林与墓地！",
        "从尼亚加拉瀑布一路开进新英格兰秋色，在基恩的小镇清晨、山林赛道和校园终点里完成第22州。",
        "22", "KEENE", "FALL",
        "#2f855a",
    ),
    StoryConfig(
        "louisville-marathon-2024",
        "KENTUCKY",
        "第1州番外 · 肯塔基#3 · Louisville Marathon",
        "肯塔基路易斯维尔 · 2024.11.03",
        "Run50 #第1州番外｜肯塔基#3：路易斯维尔马拉松｜博士收官战，送我一朵小红花",
        "回到美国跑马起点，在 Floyds Fork 的秋色里把博士生涯跑成一个完整的 loop。",
        "KY", "PhD", "LOOP",
        "#6f4aa8",
    ),
    StoryConfig(
        "louisiana-marathon",
        "LOUISIANA",
        "第23州 · 路易斯安那 · Louisiana Marathon",
        "路易斯安那巴吞鲁日 · 2025.01.19",
        "Run50 #第23州｜路易斯安那：巴吞鲁日马拉松｜法兰西底色，2025 第一跑",
        "新年第一跑，从达拉斯转机到新奥尔良，再开进巴吞鲁日，把南方湿地、LSU 紫金色和 Finish Fest 串在一起。",
        "23", "LSU", "2025",
        "#6f4aa8",
    ),
    StoryConfig(
        "blue-ridge-marathon",
        "VIRGINIA",
        "第24州 · 弗吉尼亚 · Blue Ridge Marathon",
        "弗吉尼亚罗阿诺克 · 2025.04.12",
        "Run50 #第24州｜弗吉尼亚：蓝岭山马拉松｜全美最虐赛道，3,564英尺的暴力美学",
        "America's Toughest Road Marathon，把马拉松跑成登山赛，也把蓝岭山脉的硬派风光跑进腿里。",
        "24", "3,564 ft", "CLIMB",
        "#294f7a",
    ),
    StoryConfig(
        "kentucky-derby-marathon-2025",
        "KENTUCKY",
        "第1州番外 · 肯塔基#4 · Derby Marathon",
        "肯塔基路易斯维尔 · 2025.04.26",
        "Run50 #第1州番外｜肯塔基#4：德比马拉松｜三个奖牌，一块蛋糕，我的第50场马拉松！",
        "工作后的第一场德比马拉松，也是个人第50场全马：周五 5K、周六全马、三块奖牌和一块蛋糕。",
        "50", "3", "CAKE",
        "#6f4aa8",
    ),
    StoryConfig(
        "fargo-marathon",
        "NORTH DAKOTA",
        "第25州 · 北达科他 · Fargo Marathon",
        "北达科他法戈 · 2025.05.31",
        "Run50 #第25州｜北达科他州：法戈马拉松｜跑进美剧小镇，踏上50州跑马的“半程分水岭”！",
        "从蓝草州一路开到大平原，在粉色天空、玉米地、热浪和破4里完成 Run50 半程分水岭。",
        "25", "FARGO", "HALF",
        "#d08a28",
    ),
    StoryConfig(
        "hell-on-gravel-marathon",
        "KANSAS",
        "第26州 · 堪萨斯 · Hell on Gravel",
        "堪萨斯埃尔多拉多 · 2025.06.28",
        "Run50 #第26州｜堪萨斯：地狱砂石马拉松｜冠军就是冠军，哪怕全马只有十个人！",
        "风、牛群、麦田和砂石路，把一场小到只有十个人的全马跑成了冠军故事。",
        "26", "10", "CHAMP",
        "#b7791f",
    ),
    StoryConfig(
        "mad-marathon",
        "VERMONT",
        "第27州 · 佛蒙特 · Mad Marathon",
        "佛蒙特沃伦 · 2025.07.17",
        "Run50 #第27州｜佛蒙特：疯河谷马拉松｜绿山之州的夏天，跑进乡村油画里",
        "开进新英格兰腹地，在绿山、谷仓、国旗和乡村小路中，跑进一幅夏天的油画。",
        "27", "GREEN", "VALLEY",
        "#2f855a",
    ),
    StoryConfig(
        "rocket-city-marathon",
        "ALABAMA",
        "第28州 · 阿拉巴马 · Rocket City Marathon",
        "阿拉巴马亨茨维尔 · 2025.12.12",
        "Run50 #第28州｜阿拉巴马：火箭城马拉松｜寒流来袭，南方跑马也得穿秋裤",
        "在寒流里的火箭城起跑，把南方州、航天工业、大火箭和路村朋友们一起跑进 2025 收官。",
        "28", "ROCKET", "COLD",
        "#c05621",
    ),
    StoryConfig(
        "arizona-phoenix-marathon",
        "ARIZONA",
        "第29州 · 亚利桑那 · Buckeye Marathon",
        "亚利桑那巴克艾 · 2026.01.10",
        "Run50 #第29州｜亚利桑那 Buckeye Marathon：沙漠清晨，机场终点，2026 第一跑破4",
        "沙漠清晨、巨人柱、Buckeye 机场终点，还有二〇二六第一场意外破四。",
        "29", "DESERT", "SUB4",
        "#d97706",
    ),
]


STORY_EXTRAS = {
    "new-hampshire-clarence-demar-marathon": {
        "map_asset": "wechat-run50-map-new-hampshire-22.png",
        "map_caption": "第22州，新罕布什尔点亮；星标落在 Keene，秋色和小镇终点都在这里。",
        "finish": "这一站最好的地方，不是它有多快，而是新英格兰的小镇、树林和校园终点，把一场全马跑得很有季节感。",
        "chat": "如果你也喜欢这种小镇比赛，可以在留言里讲讲：是秋色更迷人，还是赛后热汤更救命。",
    },
    "louisville-marathon-2024": {
        "map_asset": "wechat-run50-map-kentucky-extra-louisville-2024.png",
        "map_caption": "番外回到肯塔基。地图已经往前走了很多州，星标还是落回 Louisville。",
        "finish": "博士收官这一跑，像给肯塔基这条老线又补了一枚书签：不是第一次来，却刚好卡在一个人生章节的结尾。",
        "chat": "这一篇适合聊一点人生节点：毕业、搬家、告别，或者某场刚好卡在转折点上的比赛。",
    },
    "louisiana-marathon": {
        "map_asset": "wechat-run50-map-louisiana-23.png",
        "map_caption": "第23州路易斯安那点亮，星标落在 Baton Rouge。",
        "finish": "这站有点南方口味：湿地、紫金色、Finish Fest，还有年初第一场把身体重新叫醒的长跑。",
        "chat": "如果你跑过南方湿热的比赛，欢迎来吐槽一下：到底是风景先到，还是汗先到。",
    },
    "blue-ridge-marathon": {
        "map_asset": "wechat-run50-map-virginia-24.png",
        "map_caption": "第24州弗吉尼亚点亮，星标落在 Roanoke，蓝岭山的爬升也一起写进地图。",
        "finish": "蓝岭山这一跑不像普通城市马，更像一次把腿借给山路的旅行。痛是真的，风景也是真的。",
        "chat": "这一站可以聊爬坡。你跑过最狠的一段坡是哪儿？我很想听听大家的腿是怎么被教育的。",
    },
    "kentucky-derby-marathon-2025": {
        "map_asset": "wechat-run50-map-kentucky-extra-derby-2025.png",
        "map_caption": "又一次回到肯塔基 Louisville。这一次，地图外还有第50场全马这个私人坐标。",
        "finish": "三块奖牌和一块蛋糕，听着有点夸张，但刚好适合第50场：郑重一点，也好笑一点。",
        "chat": "如果你也有一个私人的整数纪念场，欢迎留言。第10场、第42场、第50场，都算数。",
    },
    "fargo-marathon": {
        "map_asset": "wechat-run50-map-north-dakota-25.png",
        "map_caption": "第25州北达科他点亮，Run50 的半程分水岭落在 Fargo。",
        "finish": "跑到第25州，数字突然有了重量。Fargo 不只是一个美剧名字，也成了这张地图的中点。",
        "chat": "半程分水岭这种东西，跑的时候没感觉，回头看才有点重。你也可以留言讲讲自己的 halfway moment。",
    },
    "hell-on-gravel-marathon": {
        "map_asset": "wechat-run50-map-kansas-26.png",
        "map_caption": "第26州堪萨斯点亮，星标落在 El Dorado 的砂石路边。",
        "finish": "这场小比赛的妙处就在于它不装大。十个人的全马，风、牛、砂石路都是真的，冠军也是真的。",
        "chat": "这一篇欢迎聊小比赛。人少、路野、补给随缘，但有时候记得最牢的就是这种。",
    },
    "mad-marathon": {
        "map_asset": "wechat-run50-map-vermont-27.png",
        "map_caption": "第27州佛蒙特点亮，星标落在 Warren 和 Mad River Valley。",
        "finish": "佛蒙特这一站像夏天慢慢展开的一张明信片：绿山、谷仓、乡村路，跑得不急，但很留人。",
        "chat": "如果你也有一场像明信片一样的比赛，可以留言丢给我。好看的乡村路永远不嫌多。",
    },
    "rocket-city-marathon": {
        "map_asset": "wechat-run50-map-alabama-28.png",
        "map_caption": "第28州阿拉巴马点亮，星标落在 Huntsville 的火箭城。",
        "finish": "南方也会冷得很认真。火箭城这一跑，把航天、寒流和路村朋友们都收进了 2025 的尾声。",
        "chat": "这一站欢迎讨论低温跑马装备：穿少了是勇敢，穿多了是智慧，我现在越来越尊重后者。",
    },
    "arizona-phoenix-marathon": {
        "map_asset": "wechat-run50-map-arizona-29.png",
        "map_caption": "第29州亚利桑那点亮，星标落在 Buckeye，沙漠公路一路通向机场终点。",
        "finish": "新年的第一场，没有硬追，反而破了4。沙漠很空，路很直，这种顺下来的状态最难得。",
        "chat": "如果你也有过一次“没想破，结果破了”的比赛，欢迎留言。我觉得这种惊喜比计划表更有意思。",
    },
}


@dataclass
class Block:
    kind: str
    text: str = ""
    src: str = ""
    alt: str = ""


class StoryParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title_parts: list[str] = []
        self.dek_parts: list[str] = []
        self.blocks: list[Block] = []
        self.in_title = False
        self.in_dek = False
        self.dek_tag: str | None = None
        self.in_article = False
        self.article_depth = 0
        self.current: dict[str, object] | None = None

    def handle_starttag(self, tag: str, attrs_list: list[tuple[str, str | None]]) -> None:
        attrs = {k: v or "" for k, v in attrs_list}
        cls = attrs.get("class", "")
        if tag == "h1":
            self.in_title = True
        if "dek" in cls.split():
            self.in_dek = True
            self.dek_tag = tag
        if tag == "article" and "article-body" in cls.split():
            self.in_article = True
            self.article_depth = 1
        elif self.in_article:
            self.article_depth += 1
        if self.in_article:
            if tag in {"p", "h2", "h3", "figcaption"}:
                self.current = {"kind": tag, "parts": []}
            elif tag == "img":
                self.blocks.append(Block("img", src=attrs.get("src", ""), alt=attrs.get("alt", "")))

    def handle_endtag(self, tag: str) -> None:
        if tag == "h1":
            self.in_title = False
        if self.in_dek and tag == self.dek_tag:
            self.in_dek = False
            self.dek_tag = None
        if self.current and tag == self.current["kind"]:
            text = normalize_text("".join(self.current["parts"]))  # type: ignore[index]
            if text:
                self.blocks.append(Block(str(self.current["kind"]), text=text))
            self.current = None
        if self.in_article:
            self.article_depth -= 1
            if self.article_depth <= 0:
                self.in_article = False

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title_parts.append(data)
        if self.in_dek:
            self.dek_parts.append(data)
        if self.current:
            self.current["parts"].append(data)  # type: ignore[index]


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


TAIL_MARKERS = (
    "- \u672c\u6587\u5b8c -",
    "\u6587\u5b57\u4e28Arsenan",
    "\u6444\u5f71\u4e28Arsenan",
    "\u8bbe\u8ba1\u4e28Arsenan",
    "\u7559\u8a00 / \u6d4f\u89c8",
    "\u7559\u8a00/\u6d4f\u89c8",
    "\u7559\u8a00\uff0f\u6d4f\u89c8",
    "\u4e0d\u7528\u767b\u5f55",
    "\u7559\u8a00\u533a\u52a0\u8f7d\u4e2d",
    "supabase",
)


def strip_tail_text(text: str) -> tuple[str, bool]:
    normalized = normalize_text(text)
    earliest: int | None = None
    for marker in TAIL_MARKERS:
        index = normalized.find(marker)
        if index >= 0 and (earliest is None or index < earliest):
            earliest = index
    if earliest is None:
        return normalized, False
    return normalize_text(normalized[:earliest]), True


def caption_text(text: str) -> str:
    text = normalize_text(text)
    is_official = bool(re.search(r"Official (race )?photo|赛事摄影|官方赛照|官方摄影", text, flags=re.I))
    text = text.replace("@阿森南", "").replace("@Arsenan", "")
    text = re.sub(r"\bOfficial race photo\b|\bOfficial photo\b|赛事摄影|官方赛照|官方摄影", "", text, flags=re.I)
    text = re.sub(r"\s+", " ", text)
    text = text.strip(" ·｜|-")
    if is_official:
        return f"{text} · 赛事摄影" if text else "赛事摄影"
    return text


def parse_source(slug: str) -> tuple[str, str, list[Block]]:
    parser = StoryParser()
    path = ROOT / "run50" / "stories" / "chinese" / f"{slug}.html"
    parser.feed(path.read_text(encoding="utf-8"))
    title = normalize_text("".join(parser.title_parts))
    dek = normalize_text("".join(parser.dek_parts))
    return title, dek, parser.blocks


def blocks_for_wechat(blocks: list[Block]) -> list[Block]:
    result: list[Block] = []
    for block in blocks:
        text, hit_tail = strip_tail_text(block.text)
        if hit_tail:
            if text:
                result.append(Block(block.kind, text=text, src=block.src, alt=block.alt))
            break
        if block.kind in {"h2", "h3"} and "\u8dd1\u5b8c\u4e5f\u53ef\u4ee5\u804a\u4e24\u53e5" in text:
            break
        result.append(Block(block.kind, text=text, src=block.src, alt=block.alt))
    credit_markers = {
        "- \u672c\u6587\u5b8c -",
        "\u6587\u5b57\u4e28Arsenan",
        "\u6444\u5f71\u4e28Arsenan",
        "\u8bbe\u8ba1\u4e28Arsenan",
    }
    while result and result[-1].kind == "p" and strip_tail_text(result[-1].text)[0] in credit_markers:
        result.pop()
    return result


def paired_blocks(blocks: list[Block]) -> list[Block | tuple[Block, str]]:
    result: list[Block | tuple[Block, str]] = []
    i = 0
    while i < len(blocks):
        block = blocks[i]
        if block.kind == "img":
            cap = ""
            if i + 1 < len(blocks) and blocks[i + 1].kind == "figcaption":
                cap = caption_text(blocks[i + 1].text)
                i += 2
            else:
                i += 1
            result.append((block, cap))
        elif block.kind == "figcaption":
            i += 1
        else:
            result.append(block)
            i += 1
    return result


def interleave_section_items(items: list[Block | tuple[Block, str]]) -> list[Block | tuple[Block, str]]:
    paragraphs = [item for item in items if not isinstance(item, tuple) and item.kind == "p"]
    figures = [item for item in items if isinstance(item, tuple)]
    if not paragraphs or not figures:
        return items
    first_figure = next((i for i, item in enumerate(items) if isinstance(item, tuple)), -1)
    last_paragraph = max(i for i, item in enumerate(items) if not isinstance(item, tuple) and item.kind == "p")
    if first_figure < last_paragraph:
        return items
    woven: list[Block | tuple[Block, str]] = []
    figure_index = 0
    for paragraph_index, paragraph in enumerate(paragraphs, start=1):
        woven.append(paragraph)
        target = round(paragraph_index * len(figures) / len(paragraphs))
        while figure_index < target:
            woven.append(figures[figure_index])
            figure_index += 1
    woven.extend(figures[figure_index:])
    return woven


def split_section(text: str) -> tuple[str, str]:
    if "｜" in text:
        label, rest = text.split("｜", 1)
        return label.strip(), rest.strip()
    if " · " in text:
        label, rest = text.split(" · ", 1)
        return label.strip(), rest.strip()
    return "Run50", text.strip()


def image_src(src: str) -> str:
    if src.startswith(("http://", "https://", "../", "./")):
        return src
    return "../stories/chinese/" + src


def accent_inline(text: str, cfg: StoryConfig) -> str:
    escaped = escape(text)
    underline_terms = [
        "第22州", "第23州", "第24州", "第25州", "第26州", "第27州", "第28州", "第29州",
        "半程分水岭", "全美最虐赛道", "冠军就是冠军", "第50场马拉松", "2025 第一跑",
    ]
    for term in underline_terms:
        escaped = escaped.replace(
            escape(term),
            f'<span style="border-bottom: 2px solid {cfg.gold}; color: #162636; font-weight: 800; padding-bottom: 1px;">{escape(term)}</span>',
        )
    italic_terms = [
        "Run50", "Parkrun", "Finish Fest", "America's Toughest Road Marathon",
        "Buckeye", "Floyds Fork", "loop", "sub4", "Sub4",
    ]
    for term in italic_terms:
        escaped = escaped.replace(
            escape(term),
            f'<em style="font-family: Georgia, Times, serif; color: {cfg.accent}; font-style: italic;">{escape(term)}</em>',
        )
    terms = [
        cfg.series.split("·")[0].strip(),
        cfg.place.split("·")[0].strip(),
        "新英格兰", "基恩", "路易斯维尔", "巴吞鲁日", "蓝岭山", "罗阿诺克",
        "法戈", "堪萨斯", "佛蒙特", "火箭城", "亚利桑那", "大平原",
        "Grand River", "LSU", "大火箭", "巨人柱", "机场终点",
        "4 小时", "破4", "秋色", "热浪", "寒流", "砂石路", "绿山",
    ]
    for term in terms:
        if term:
            escaped = escaped.replace(
                escape(term),
                f'<strong style="color: {cfg.accent}; font-weight: 800;">{escape(term)}</strong>',
            )
    return escaped


def figure(img: Block, caption: str) -> str:
    cap = escape(caption)
    return f"""
<section style="margin: 28px 0 30px;">
  <img src="{escape(image_src(img.src))}" alt="{escape(img.alt)}" style="width: 100%; height: auto; display: block; margin: 0 auto; border-radius: 6px;">
  <p style="margin: 9px 0 0; padding-left: 10px; border-left: 3px solid #d4a669; font-size: 12px; line-height: 1.8; letter-spacing: 0.4px; color: #6f7d89; font-family: Optima-Regular, 'PingFang SC', serif;">{cap}</p>
</section>"""


def paragraph(text: str, cfg: StoryConfig) -> str:
    if text.endswith("：") and len(text) <= 14:
        return (
            '<p style="margin: 4px 0 14px; line-height: 1.7; text-align: left; '
            f"font-size: 15px; letter-spacing: 0.6px; color: {cfg.gold}; "
            "font-style: italic; font-family: Georgia, 'Times New Roman', 'PingFang SC', serif;\">"
            f"{escape(text)}</p>"
        )
    return (
        '<p style="margin: 0 0 18px; line-height: 1.95; text-align: justify; '
        "font-size: 16px; letter-spacing: 0.2px; color: #26343f; "
        "font-family: -apple-system, BlinkMacSystemFont, 'Helvetica Neue', "
        "'PingFang SC', 'Microsoft YaHei', Arial, sans-serif;\">"
        f"{accent_inline(text, cfg)}</p>"
    )


def section_heading(text: str, index: int, cfg: StoryConfig) -> str:
    label, rest = split_section(text)
    return f"""
<section style="margin: 44px 0 18px; padding: 0 0 0 14px; border-left: 5px solid {cfg.accent};">
  <p style="margin: 0 0 5px; font-size: 11px; line-height: 1.4; letter-spacing: 1.6px; color: #8a9bad; font-weight: 800;">FIELD NOTE {index:02d}</p>
  <h2 style="margin: 0; font-size: 20px; line-height: 1.45; font-weight: 900; color: #162636; letter-spacing: 0;">{escape(rest or text)}</h2>
  <p style="margin: 7px 0 0; font-size: 12px; line-height: 1.6; color: {cfg.gold};">{escape(label)}</p>
</section>"""


def render_story_blocks(blocks: list[Block], cfg: StoryConfig) -> list[str]:
    rendered: list[str] = []
    section_items: list[Block | tuple[Block, str]] = []
    section_index = 0

    def flush_section() -> None:
        for item in interleave_section_items(section_items):
            if isinstance(item, tuple):
                rendered.append(figure(item[0], item[1]))
            elif item.kind == "p":
                rendered.append(paragraph(item.text, cfg))

    for item in paired_blocks(blocks):
        if not isinstance(item, tuple) and item.kind in {"h2", "h3"}:
            flush_section()
            section_items.clear()
            section_index += 1
            rendered.append(section_heading(item.text, section_index, cfg))
        else:
            section_items.append(item)
    flush_section()
    return rendered


def vlog_card(cfg: StoryConfig) -> str:
    return f"""
<section style="margin: 24px 0 30px;">
  <section style="position: relative; width: 100%; padding-top: 56.25%; border-radius: 8px; overflow: hidden; background: #12384a; border: 1px solid #d5e4eb; box-shadow: 0 16px 36px rgba(20, 52, 68, 0.16);">
    <section style="position: absolute; inset: 0; padding: 24px 26px; box-sizing: border-box; background: linear-gradient(135deg, #12384a 0%, {cfg.accent} 58%, #0f2634 100%); color: #ffffff;">
      <p style="margin: 0 0 10px; font-size: 12px; line-height: 1.3; letter-spacing: 2.2px; font-weight: 900; color: #ffdd75;">RUN50 VLOG · {escape(cfg.state_en)}</p>
      <p style="margin: 0; max-width: 430px; font-size: 28px; line-height: 1.25; font-weight: 900; letter-spacing: 0;">先看一段{escape(cfg.place.split('·')[0].strip())}</p>
      <p style="margin: 10px 0 0; max-width: 460px; font-size: 15px; line-height: 1.75; color: rgba(255,255,255,0.86);">{escape(cfg.summary)}</p>
      <section style="position: absolute; left: 26px; bottom: 22px; display: inline-block; padding: 7px 12px; border-radius: 999px; background: rgba(255,255,255,0.14); color: rgba(255,255,255,0.9); font-size: 12px; line-height: 1.4; letter-spacing: 0.5px;">{escape(cfg.place)} · 16:9 Vlog</section>
      <section style="position: absolute; right: 30px; bottom: 26px; width: 64px; height: 64px; border-radius: 50%; background: #ffcc00; box-shadow: 0 10px 24px rgba(0,0,0,0.22);">
        <span style="position: absolute; left: 25px; top: 18px; width: 0; height: 0; border-top: 14px solid transparent; border-bottom: 14px solid transparent; border-left: 22px solid #12384a;"></span>
      </section>
    </section>
  </section>
  <p style="margin: 9px 0 0; padding-left: 10px; border-left: 3px solid {cfg.gold}; font-size: 12px; line-height: 1.8; letter-spacing: 0.4px; color: #6f7d89; font-family: Optima-Regular, 'PingFang SC', serif;">Vlog 开场位｜{escape(cfg.summary)}</p>
</section>"""


def medal_figure(cfg: StoryConfig) -> str:
    return f"""
<section style="margin: 24px 0 28px;">
  <img src="../../assets/cover-medal-{escape(cfg.slug)}.jpg" alt="{escape(cfg.public_title)}奖牌封面" style="width: 100%; height: auto; display: block; margin: 0 auto; border-radius: 7px;">
  <p style="margin: 9px 0 0; padding-left: 10px; border-left: 3px solid {cfg.gold}; font-size: 12px; line-height: 1.8; letter-spacing: 0.4px; color: #6f7d89; font-family: Optima-Regular, 'PingFang SC', serif;">{escape(cfg.public_title)}奖牌质感封面。</p>
</section>"""


def map_figure(cfg: StoryConfig) -> str:
    extra = STORY_EXTRAS.get(cfg.slug)
    if not extra:
        return ""
    return f"""
<section style="margin: 12px 0 30px;">
  <img src="../../assets/{escape(str(extra['map_asset']))}" alt="{escape(str(extra['map_caption']))}" style="width: 100%; height: auto; display: block; margin: 0 auto; border-radius: 7px;">
  <p style="margin: 9px 0 0; padding-left: 10px; border-left: 3px solid {cfg.gold}; font-size: 12px; line-height: 1.8; letter-spacing: 0.4px; color: #6f7d89; font-family: Optima-Regular, 'PingFang SC', serif;">{escape(str(extra['map_caption']))}</p>
</section>"""


def finish_card(cfg: StoryConfig) -> str:
    extra = STORY_EXTRAS.get(cfg.slug, {})
    finish = str(extra.get("finish", f"{cfg.summary} 跑完这一篇，Run50 的故事又多了一块颜色。"))
    chat = str(extra.get("chat", "如果这一站也勾起了你的某段跑步记忆，欢迎在公众号留言里接着聊。别太正式，像赛后坐下来喝一口水那样就行。"))
    return f"""
<section style="margin: 46px 0 0; padding: 22px 18px 20px; border-radius: 8px; background: linear-gradient(135deg, #132535 0%, {cfg.accent} 58%, {cfg.gold} 100%); color: #ffffff; box-shadow: 0 14px 32px rgba(19, 37, 53, 0.18);">
  <p style="margin: 0 0 10px; font-size: 11px; line-height: 1.4; letter-spacing: 2.2px; font-weight: 900; color: rgba(255,255,255,0.78);">RUN50 FINISH LINE</p>
  <h2 style="margin: 0 0 12px; font-size: 24px; line-height: 1.35; font-weight: 900; color: #ffffff; letter-spacing: 0;">这一站，收进地图。</h2>
  <p style="margin: 0; font-size: 15px; line-height: 1.9; color: rgba(255,255,255,0.92); text-align: justify;">{escape(finish)}</p>
  <section style="margin: 18px 0 0; display: table; width: 100%; border-collapse: collapse;">
    <section style="display: table-cell; width: 33.33%; padding: 10px 6px; border-right: 1px solid rgba(255,255,255,0.18); text-align: center;"><p style="margin: 0; font-size: 18px; line-height: 1.2; font-weight: 900; color: #ffffff;">{escape(cfg.stat_one)}</p><p style="margin: 5px 0 0; font-size: 11px; line-height: 1.4; color: rgba(255,255,255,0.74); letter-spacing: 0.8px;">RUN50</p></section>
    <section style="display: table-cell; width: 33.33%; padding: 10px 6px; border-right: 1px solid rgba(255,255,255,0.18); text-align: center;"><p style="margin: 0; font-size: 18px; line-height: 1.2; font-weight: 900; color: #ffffff;">{escape(cfg.stat_two)}</p><p style="margin: 5px 0 0; font-size: 11px; line-height: 1.4; color: rgba(255,255,255,0.74); letter-spacing: 0.8px;">MARK</p></section>
    <section style="display: table-cell; width: 33.33%; padding: 10px 6px; text-align: center;"><p style="margin: 0; font-size: 18px; line-height: 1.2; font-weight: 900; color: #ffffff;">{escape(cfg.stat_three)}</p><p style="margin: 5px 0 0; font-size: 11px; line-height: 1.4; color: rgba(255,255,255,0.74); letter-spacing: 0.8px;">NOTE</p></section>
  </section>
</section>
<section style="margin: 16px 0 0; padding: 15px 16px; border-left: 4px solid {cfg.gold}; background: #f4f8fb; border-radius: 7px;">
  <p style="margin: 0; font-size: 14px; line-height: 1.9; color: #314657; text-align: justify;">{escape(chat)}</p>
</section>
<p style="margin: 24px 0 0; text-align: center; color: #8a9bad; font-size: 12px; line-height: 1.8; letter-spacing: 1.2px;">文字 / 编辑 / 排版 · Arsenan</p>"""


def page_shell(title: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)}</title>
</head>
<body style="margin: 0; padding: 0; background: #ffffff; font-family: -apple-system, BlinkMacSystemFont, 'Helvetica Neue', 'PingFang SC', 'Microsoft YaHei', Arial, sans-serif;">
{body}
</body>
</html>
"""


def render_page(cfg: StoryConfig) -> str:
    _title, dek, blocks = parse_source(cfg.slug)
    blocks = blocks_for_wechat(blocks)
    opening = dek or cfg.summary
    body: list[str] = [
        '<section style="max-width: 677px; width: 100%; box-sizing: border-box; margin: 0 auto; padding: 28px 18px 58px; background: #ffffff;">',
        f'<section style="margin: 0 0 22px; padding: 16px 0 18px; border-top: 4px solid {cfg.accent}; border-bottom: 1px solid #dfe9ef;">',
        f'<p style="margin: 0 0 8px; font-size: 12px; line-height: 1.4; letter-spacing: 2px; color: {cfg.accent}; font-weight: 800;">RUN50 DISPATCH · {escape(cfg.state_en)}</p>',
        f'<p style="margin: 0; font-size: 20px; line-height: 1.55; font-weight: 900; color: #17212b; letter-spacing: 0;">{escape(cfg.series)}</p>',
        f'<p style="margin: 14px 0 0; font-size: 13px; line-height: 1.7; color: #6f7d89;">{escape(cfg.place)}</p>',
        "</section>",
        vlog_card(cfg),
        f'<section style="margin: 0 0 28px; padding: 16px 18px; background: #edf5f8; border-radius: 6px;"><p style="margin: 0 0 6px; font-size: 12px; line-height: 1.5; letter-spacing: 1px; color: {cfg.accent}; font-weight: 800;">OPENING NOTE</p><p style="margin: 0; font-size: 15px; line-height: 1.9; color: #26343f; text-align: justify;">{accent_inline(opening, cfg)}</p></section>',
        '<section style="margin: 0 0 28px; display: block;">'
        f'<p style="margin: 0 0 8px; font-size: 14px; line-height: 1.8; color: {cfg.gold}; font-weight: 800;">本文速记</p>'
        f'<p style="margin: 0; font-size: 14px; line-height: 1.9; color: #53616f;">{accent_inline(cfg.summary, cfg)}</p>'
        "</section>",
        medal_figure(cfg),
        map_figure(cfg),
    ]
    body.extend(render_story_blocks(blocks, cfg))
    body.append(finish_card(cfg))
    body.append("</section>")
    return page_shell(cfg.public_title, "\n".join(body))


def render_index() -> str:
    cards = []
    for cfg in CONFIGS:
        cards.append(f"""
      <a class="card" href="{escape(cfg.slug)}-modern-rail.html?v={VERSION}">
        <img class="cover" src="../../assets/cover-medal-{escape(cfg.slug)}.jpg" alt="{escape(cfg.public_title)}奖牌封面">
        <div class="body">
          <p class="meta">RUN50 DISPATCH · {escape(cfg.state_en)}</p>
          <h2>{escape(cfg.public_title)}</h2>
          <p class="place">{escape(cfg.place)}</p>
          <p class="summary">{escape(cfg.summary)}</p>
          <span class="button">Open WeChat Edition →</span>
        </div>
      </a>""")
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Run50 WeChat Editions</title>
  <style>
    :root {{ --bg:#edf3f7; --paper:#fff; --ink:#17212b; --muted:#5e6c78; --line:#d9e4ec; --blue:#2d6f9f; --gold:#b98735; }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; background:var(--bg); color:var(--ink); font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",Arial,sans-serif; }}
    .tabs {{ max-width:1080px; margin:0 auto; padding:18px 20px; display:flex; gap:18px; flex-wrap:wrap; justify-content:center; font-size:14px; font-weight:800; }}
    .tabs a {{ color:#435569; text-decoration:none; }} .tabs a.active {{ color:var(--blue); }}
    main {{ max-width:1160px; margin:0 auto; padding:32px 20px 64px; }}
    .hero {{ padding:26px 0 24px; border-top:4px solid var(--blue); border-bottom:1px solid var(--line); }}
    .kicker {{ margin:0 0 10px; font-size:12px; letter-spacing:2px; color:var(--blue); font-weight:900; }}
    h1 {{ margin:0; font-size:clamp(32px,6vw,56px); line-height:1.05; letter-spacing:0; }}
    .dek {{ max-width:760px; margin:16px 0 0; color:var(--muted); font-size:17px; line-height:1.8; }}
    .grid {{ margin-top:30px; display:grid; grid-template-columns:repeat(auto-fit,minmax(280px,1fr)); gap:18px; }}
    .card {{ display:block; overflow:hidden; background:var(--paper); border:1px solid var(--line); border-radius:8px; text-decoration:none; color:inherit; box-shadow:0 16px 40px rgba(31,51,70,.08); }}
    .cover {{ width:100%; aspect-ratio:16/10; object-fit:cover; display:block; background:#dbe7ef; }}
    .body {{ padding:18px 18px 20px; }}
    .meta {{ margin:0 0 8px; color:var(--gold); font-size:12px; letter-spacing:1.1px; font-weight:900; }}
    h2 {{ margin:0; font-size:21px; line-height:1.38; letter-spacing:0; }}
    .place {{ margin:10px 0 0; color:#425466; font-size:13px; font-weight:800; }}
    .summary {{ margin:10px 0 0; color:var(--muted); font-size:15px; line-height:1.72; }}
    .button {{ display:inline-block; margin-top:16px; padding-bottom:3px; color:var(--blue); border-bottom:2px solid var(--gold); font-size:14px; font-weight:900; }}
    .note {{ margin:28px 0 0; padding:16px 18px; background:rgba(255,255,255,.72); border-left:4px solid var(--gold); color:var(--muted); line-height:1.75; border-radius:7px; font-size:14px; }}
  </style>
</head>
<body>
  <nav class="tabs" aria-label="Run50 story sections">
    <a href="../index.html">← Run50</a>
    <a href="../stories/chinese/">Chinese Stories</a>
    <a href="../stories/english/">English Stories</a>
    <a href="./" class="active">WeChat</a>
    <a href="../facebook/">Facebook</a>
  </nav>
  <main>
    <section class="hero">
      <p class="kicker">RUN50 WECHAT EDITIONS</p>
      <h1>微信公众号版</h1>
      <p class="dek">为公众号复制和发布准备的杂志版文章：Vlog 开场、图文穿插、精致图注、适合手机阅读的节奏。</p>
    </section>
    <section class="grid" aria-label="WeChat editions">
{''.join(cards)}
    </section>
    <p class="note">后续每一篇公众号杂志版都会放在这里，方便从 Run50 首页直接进入。</p>
  </main>
</body>
</html>
"""


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    generated = []
    for cfg in CONFIGS:
        if cfg.generate:
            path = OUT_DIR / f"{cfg.slug}-modern-rail.html"
            path.write_text(render_page(cfg), encoding="utf-8", newline="\n")
            generated.append(path)
    (OUT_DIR / "index.html").write_text(render_index(), encoding="utf-8", newline="\n")
    print(f"generated {len(generated)} WeChat pages")
    for path in generated:
        print(path)
    print(OUT_DIR / "index.html")


if __name__ == "__main__":
    main()
