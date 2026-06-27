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
        "map_caption": "第22州 · Keene",
        "finish": "这一站最好的地方，不是它有多快，而是新英格兰的小镇、树林和校园终点，把一场全马跑得很有季节感。",
        "chat": "这类小镇比赛很适合慢慢回味：赛道不一定热闹，但路边的树、学校终点和赛后那碗热东西，会把人留住。你要是也跑过类似的新英格兰小城马，可以留言告诉我是哪一场。",
    },
    "louisville-marathon-2024": {
        "map_asset": "wechat-run50-map-kentucky-extra-louisville-2024.png",
        "map_caption": "番外 · Louisville",
        "finish": "博士收官这一跑，像给肯塔基这条老线又补了一枚书签：不是第一次来，却刚好卡在一个人生章节的结尾。",
        "chat": "有些比赛的意义不在配速，而在它刚好卡在人生节点上。毕业、搬家、换工作、告别一座城，如果你也有这种带着时间戳的比赛，留言区很适合慢慢讲。",
    },
    "louisiana-marathon": {
        "map_asset": "wechat-run50-map-louisiana-23.png",
        "map_caption": "第23州 · Baton Rouge",
        "finish": "这站有点南方口味：湿地、紫金色、Finish Fest，还有年初第一场把身体重新叫醒的长跑。",
        "chat": "南方比赛有一种很直接的身体记忆：空气、湿度、音乐和赛后食物都一起上来。跑过湿热赛道的人，应该都懂那种一边嫌弃一边又记很久的感觉。",
    },
    "blue-ridge-marathon": {
        "map_asset": "wechat-run50-map-virginia-24.png",
        "map_caption": "第24州 · Roanoke",
        "finish": "蓝岭山这一跑不像普通城市马，更像一次把腿借给山路的旅行。痛是真的，风景也是真的。",
        "chat": "爬坡赛道很公平，它不会跟你讲道理，只会一点点把腿里的存货掏出来。你跑过最狠的坡在哪儿？我很想知道大家都是在哪一段被教育的。",
    },
    "kentucky-derby-marathon-2025": {
        "map_asset": "wechat-run50-map-kentucky-extra-derby-2025.png",
        "map_caption": "第50场 · Louisville",
        "finish": "三块奖牌和一块蛋糕，听着有点夸张，但刚好适合第50场：郑重一点，也好笑一点。",
        "chat": "整数场次不一定非要隆重，但它确实会让人忍不住回头数一数。第10场、第42场、第50场，或者任何一个你自己在意的数字，都值得被认真记一下。",
    },
    "fargo-marathon": {
        "map_asset": "wechat-run50-map-north-dakota-25.png",
        "map_caption": "第25州 · Fargo",
        "finish": "跑到第25州，数字突然有了重量。Fargo 不只是一个美剧名字，也成了这张地图的中点。",
        "chat": "半程分水岭这种东西，站在当下未必觉得多宏大，回头看才发现它真的把前后分开了。跑步、旅行、读书、工作，好像很多事情都有一个自己的 halfway moment。",
    },
    "hell-on-gravel-marathon": {
        "map_asset": "wechat-run50-map-kansas-26.png",
        "map_caption": "第26州 · El Dorado",
        "finish": "这场小比赛的妙处就在于它不装大。十个人的全马，风、牛、砂石路都是真的，冠军也是真的。",
        "chat": "小比赛常常没有大场面的声浪，但会留下很多奇怪又鲜活的细节。人少、路野、补给随缘，偏偏就是这种比赛，最容易在很久以后还被想起来。",
    },
    "mad-marathon": {
        "map_asset": "wechat-run50-map-vermont-27.png",
        "map_caption": "第27州 · Warren",
        "finish": "佛蒙特这一站像夏天慢慢展开的一张明信片：绿山、谷仓、乡村路，跑得不急，但很留人。",
        "chat": "有些比赛不是靠成绩留下来的，而是靠颜色、风和路边房子的样子。要是你也跑过那种像明信片一样的乡村赛道，可以留言把名字丢给我。",
    },
    "rocket-city-marathon": {
        "map_asset": "wechat-run50-map-alabama-28.png",
        "map_caption": "第28州 · Huntsville",
        "finish": "南方也会冷得很认真。火箭城这一跑，把航天、寒流和路村朋友们都收进了 2025 的尾声。",
        "chat": "低温跑马这件事，年轻时总想证明自己不怕冷，后来才发现穿对衣服也是一种能力。火箭城提醒我：南方不等于暖和，起跑线也不负责照顾嘴硬的人。",
    },
    "arizona-phoenix-marathon": {
        "map_asset": "wechat-run50-map-arizona-29.png",
        "map_caption": "第29州 · Buckeye",
        "finish": "新年的第一场，没有硬追，反而破了4。沙漠很空，路很直，这种顺下来的状态最难得。",
        "chat": "有时候最舒服的破4，不是赛前写在计划表上的那种，而是一路跑着跑着发现身体愿意给你。沙漠很空，路很直，这种意外顺下来的比赛，比硬追更让人开心。",
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


CAPTION_REWRITES = {
    "Keene State Colleg 2": "Keene State 赛后合影",
    "Keene State Colleg": "Keene State 校园终点",
    "跑进 Keene State Col": "跑进 Keene State",
    "挂满 Clarence DeMar": "Clarence DeMar 旗帜",
    "Clarence DeMar 奖牌特": "Clarence DeMar 奖牌",
    "路边展开的 Surry Mounta": "Surry Mountain 路段",
    "距离 Keene State 终点只": "接近 Keene State 终点",
    "Buckeye Race to the Runway 号码布": "Buckeye 号码布",
    "Phoenix Race to the Runway 起跑拱门": "Phoenix 起跑拱门",
    "Race to the Runway 起点的冷空气": "起点冷空气",
    "Race to the Runway 终点方向": "机场终点方向",
    "飞行主题的 Race to the Runway 奖牌": "飞行主题奖牌",
    "Race to the Runway 奖牌特写": "奖牌特写",
    "巨人柱旁的 Race to the Runway 奖牌": "巨人柱旁奖牌",
    "接近 Surry Mountain": "接近萨里山湖",
    "沿着 Surry Mountain": "沿着萨里山路",
    "Surry Mountain 路段": "萨里山湖路段",
}


TAIL_MARKERS = (
    "- \u672c\u6587\u5b8c -",
    "\u6587\u5b57\u4e28Arsenan",
    "\u6444\u5f71\u4e28Arsenan",
    "\u8bbe\u8ba1\u4e28Arsenan",
    "\u7559\u8a00 / \u6d4f\u89c8",
    "\u7559\u8a00/\u6d4f\u89c8",
    "\u7559\u8a00\uff0f\u6d4f\u89c8",
    "\u7559\u8a00 / \u9605\u8bfb",
    "\u7559\u8a00/\u9605\u8bfb",
    "\u7559\u8a00\uff0f\u9605\u8bfb",
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
    is_external = bool(re.search(r"网络|资料图|航拍资料|赛事资料|Photo by|摄影师|Wikipedia|Unsplash|赛事方|Google|地图", text, flags=re.I))
    external_label = "资料图"
    if re.search(r"航拍资料", text):
        external_label = "航拍资料"
    elif re.search(r"赛事资料|赛事方", text):
        external_label = "赛事资料"
    text = text.replace("@阿森南", "").replace("@Arsenan", "")
    text = re.sub(r"\bOfficial race photo\b|\bOfficial photo\b|赛事摄影|官方摄影|资料图|航拍资料|赛事资料", "", text, flags=re.I)
    text = re.sub(r"\s+", " ", text)
    text = text.strip(" ·｜|-")
    for old, new in CAPTION_REWRITES.items():
        if old in text:
            text = text.replace(old, new)
    text = compact_caption_base(text, is_official)
    if is_official:
        return f"{text} · 赛事摄影" if text else "赛事摄影"
    if is_external:
        return f"{text} · {external_label}" if text else external_label
    if text:
        return f"{text} @Arsenan"
    return text


def compact_caption_base(text: str, is_official: bool = False) -> str:
    text = normalize_text(text).strip(" ·｜|-")
    if not text:
        return text
    official_map = [
        (r"pink|粉", "粉色球衣"),
        (r"first miles|early", "前半程赛照"),
        (r"pack|crew", "队伍中奔跑"),
        (r"finish|final|终点|冲线", "终点瞬间"),
        (r"arms up|庆祝", "举手庆祝"),
        (r"Churchill|Louisville logo", "路易斯维尔赛照"),
        (r"green hills|blue kit", "山谷赛道"),
    ]
    if is_official:
        for pattern, replacement in official_map:
            if re.search(pattern, text, re.I):
                return replacement
        return english_caption_to_chinese(text, fallback="官方赛照")
    if re.search(r"[A-Za-z]", text) and len(text) > 18:
        return english_caption_to_chinese(text)
    if len(text) <= 18:
        return text
    for sep in ["，", "；", "：", " · ", "｜", "和", "与", "里的", "旁的", "前的", "后的"]:
        if sep in text:
            candidate = text.split(sep, 1)[0].strip()
            if 5 <= len(candidate) <= 18:
                return candidate
    for suffix in ["介绍牌", "英里牌", "起跑区", "终点线", "补给站", "停车场", "观景台", "合影", "自拍", "奖牌", "赛道"]:
        index = text.find(suffix)
        if 0 <= index <= 16:
            return text[: index + len(suffix)]
    return text[:18].rstrip("的和与，；：")


def english_caption_to_chinese(text: str, fallback: str = "路上片刻") -> str:
    raw = normalize_text(text)
    lower = raw.lower()
    replacements = [
        (r"blue ridge marathon finish", "蓝岭山终点标识"),
        (r"downtown roanoke street", "Roanoke 赛前街景"),
        (r"pre-race buffet", "赛前自助餐"),
        (r"steel bridge", "进山路上的钢桥"),
        (r"foggy highway", "山间雾路"),
        (r"tesla navigation", "弗吉尼亚导航"),
        (r"roanoke skyline", "Roanoke 天际线"),
        (r"fog settling", "蓝岭山雾气"),
        (r"art-covered building", "市中心壁画楼"),
        (r"quiet roanoke street", "清晨街道"),
        (r"start-line selfie|pink kit selfie", "起点自拍"),
        (r"volunteers and tents|aid station|water stop", "补给站"),
        (r"gravel path", "爬坡前的砂石路"),
        (r"roanoke star", "Roanoke Star 合影"),
        (r"old brick building", "赛道旁砖楼"),
        (r"empty finish chute", "空荡终点通道"),
        (r"roanoke finish arch", "Roanoke 终点拱门"),
        (r"distance signs", "终点区距离牌"),
        (r"blue ridge medal|full marathon medal|post-race medal", "蓝岭山奖牌"),
        (r"cooling down", "赛后市中心放松"),
        (r"medal pose", "街角奖牌照"),
        (r"storm clouds", "北上路上的风暴云"),
        (r"colorful overpass", "彩色天桥下"),
        (r"red sunset|sunset stripe", "州际公路落日"),
        (r"wind turbines", "平原风车"),
        (r"exit sign", "北达科他出口牌"),
        (r"dark highway", "夜色高速路"),
        (r"campsite|campground", "营地一角"),
        (r"road-trip snacks", "路上零食"),
        (r"car lunch", "车上午餐"),
        (r"flat prairie", "车窗外的大平原"),
        (r"quiet field", "营地后的田野"),
        (r"dusty gravel road", "农田砂石路"),
        (r"fargodome", "FargoDome 起点"),
        (r"fargo marathon start", "Fargo 起跑牌"),
        (r"runners heading out", "跑者冲出场馆"),
        (r"early miles", "前半程清晨"),
        (r"turning through fargo", "Fargo 街区转弯"),
        (r"mile \d+", "英里牌"),
        (r"vintage red truck", "复古红色卡车"),
        (r"two-lane road", "通往火箭城的公路"),
        (r"utility poles", "冬日路边电线杆"),
        (r"morning mist", "清晨薄雾"),
        (r"rocket city course", "Rocket City 路线图"),
        (r"siqi posing", "Siqi 赛前留影"),
        (r"sunlit creek", "阳光下的小溪"),
        (r"final aid area", "最后补给区"),
        (r"blue-kit selfie", "蓝色跑衣自拍"),
        (r"final sunny selfie", "赛后阳光自拍"),
        (r"cincinnati skyline", "辛辛那提天际线"),
        (r"hot-air balloon", "热气球拖车"),
        (r"orange sunset", "橙色落日"),
        (r"night highway", "夜色高速"),
        (r"covered bridge", "乡村廊桥"),
        (r"small boat", "湖上的小船"),
        (r"cyclists climbing", "绿坡上的骑行者"),
        (r"farm lane", "谷仓旁小路"),
        (r"red b", "红色谷仓"),
        (r"thumbs-up", "路边竖起大拇指"),
        (r"shadow selfie", "烈日下的影子自拍"),
        (r"park gazebo", "公园凉亭自拍"),
        (r"hotel hallway", "酒店走廊"),
        (r"long evening shadow", "傍晚长影"),
        (r"pond", "池塘边"),
        (r"campground road", "营地小路"),
        (r"pouring water", "浇水降温"),
        (r"friday 5k", "周五 5K 起点"),
        (r"ohio river sunset", "俄亥俄河落日"),
        (r"big .*bridge|bridge deck", "雨中的大桥"),
        (r"mile 3 sign", "5K 三英里牌"),
        (r"mile 22 sign|mile 25 sign", "马拉松英里牌"),
        (r"runner raising", "跑者举手瞬间"),
        (r"turn-around sign", "折返点标识"),
        (r"underpass shade", "桥下阴影"),
        (r"sunrise haze", "清晨霞光"),
        (r"bayous|brown water", "湾流与褐色水面"),
        (r"seatback map|in-flight map", "飞行地图"),
        (r"korean lunch", "转机韩餐"),
        (r"bib", "号码布"),
        (r"baton rouge mural", "Baton Rouge 壁画"),
        (r"lsu tiger", "LSU 虎队吉祥物"),
        (r"finish fest", "Finish Fest"),
        (r"hydration", "赛道补水"),
        (r"buckeye marathon vlog", "Buckeye Vlog 封面"),
        (r"race to the runway", "Race to the Runway"),
        (r"north mountain park", "North Mountain 山路"),
        (r"dobbins lookout", "Dobbins Lookout"),
        (r"festival foothills", "Festival Foothills 起点"),
        (r"sun city festival", "Sun City 赛道路段"),
        (r"papago park", "Papago Park 红岩"),
        (r"hole-in-the-rock", "Hole-in-the-Rock"),
    ]
    for pattern, label in replacements:
        if re.search(pattern, lower, re.I):
            return label
    generic = [
        (r"selfie", "路上自拍"),
        (r"medal", "奖牌照"),
        (r"start|corral", "起点现场"),
        (r"finish|chute", "终点现场"),
        (r"runners|runner", "赛道跑者"),
        (r"aid|water|hydration", "补给站"),
        (r"sunset", "落日时分"),
        (r"sunrise|morning", "清晨风景"),
        (r"road|highway|interstate", "路上风景"),
        (r"bridge", "桥上风景"),
        (r"downtown|street", "城市街景"),
        (r"field|farm|prairie|corn", "田野风景"),
        (r"mountain|hill|ridge", "山路风景"),
        (r"creek|lake|river", "水边风景"),
        (r"sign", "路边标识"),
    ]
    for pattern, label in generic:
        if re.search(pattern, lower, re.I):
            return label
    words = re.sub(r"[^A-Za-z0-9 ]+", " ", raw).split()
    if words:
        return " ".join(words[:2])
    return fallback


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
    seen_captions: dict[str, int] = {}
    i = 0
    while i < len(blocks):
        block = blocks[i]
        if block.kind == "img":
            cap = ""
            if i + 1 < len(blocks) and blocks[i + 1].kind == "figcaption":
                cap = caption_text(blocks[i + 1].text)
                original_cap = cap
                count = seen_captions.get(original_cap, 0)
                cap = uniquify_caption(original_cap, count)
                seen_captions[original_cap] = count + 1
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


def uniquify_caption(caption: str, count: int) -> str:
    if count <= 0 or not caption:
        return caption
    source = ""
    base = caption
    for marker in [" @Arsenan", " · 赛事摄影", " · 航拍资料", " · 赛事资料", " · 资料图"]:
        if caption.endswith(marker):
            base = caption[: -len(marker)]
            source = marker
            break
    variants = {
        "终点瞬间": ["冲线瞬间", "终点挥手", "终点近照", "终点回望", "终点蓝衣"],
        "山路风景": ["山路转弯", "山顶视野", "林间山路", "下坡路段", "山城远景"],
        "营地一角": ["营地车位", "营地黄昏", "营地清晨", "树边营位"],
        "路上风景": ["路边远景", "车窗风景", "前方长路", "转场路上"],
        "城市街景": ["街角一幕", "市中心路口", "赛前街道", "城市立面"],
        "桥上风景": ["桥面路段", "过桥瞬间", "桥下阴影", "桥边视角"],
        "落日时分": ["落日公路", "傍晚天色", "夕阳余光", "天边橙光"],
        "起点现场": ["起点人群", "起跑拱门", "出发前一刻", "起点队伍"],
        "赛道跑者": ["路上跑者", "转弯跑者", "队伍中段", "赛道节奏"],
        "补给站": ["补给桌前", "志愿者补给", "水站一角", "赛道补水"],
        "英里牌": ["里程标识", "路边英里牌", "后半程英里牌", "关键里程"],
        "路边标识": ["路牌细节", "赛道指示牌", "路口标识", "方向牌"],
        "FargoDome 起点": ["FargoDome 外场", "场馆起跑线", "冲出 FargoDome"],
        "红色谷仓": ["谷仓侧影", "乡村红屋", "田野谷仓"],
        "Dobbins Lookout": ["Dobbins 石屋", "Dobbins 山脊", "Dobbins 暮色"],
        "Hole-in-the-Rock": ["红岩洞口", "岩洞窗口", "红岩观景点"],
        "Race to the Runway": ["机场赛道", "飞行主题赛道", "跑道方向"],
        "蓝岭山奖牌": ["蓝岭山奖牌近照", "完赛奖牌", "赛后奖牌"],
        "街角奖牌照": ["阳光奖牌照", "赛后街角", "市中心奖牌照"],
        "飞行地图": ["转机航线图", "落地前地图", "机上路线图"],
        "号码布": ["号码布近照", "Expo 号码布", "赛前号码布"],
    }
    options = variants.get(base)
    if options:
        if count - 1 < len(options):
            return f"{options[count - 1]}{source}"
        return f"{base} · {count + 1}{source}"
    return f"{base} · {count + 1}{source}"


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
    escaped = re.sub(
        r"(3:58|4:44|Sub4|sub4|\d+(?:\.\d+)?\s?(?:小时|分钟|英里|英尺|场|州|K|k)?)",
        lambda m: f'<span style="display: inline-block; padding: 0 3px; margin: 0 1px; border-radius: 3px; background: rgba(185,135,53,0.16); color: {cfg.gold}; font-weight: 900;">{m.group(1)}</span>',
        escaped,
    )
    underline_terms = [
        "第22州", "第23州", "第24州", "第25州", "第26州", "第27州", "第28州", "第29州",
        "半程分水岭", "全美最虐赛道", "冠军就是冠军", "第50场马拉松", "2025 第一跑",
        "二〇二六第一跑", "机场终点", "博士收官", "第50场", "破 4", "破4",
    ]
    for term in underline_terms:
        escaped = escaped.replace(
            escape(term),
            f'<span style="border-bottom: 2px solid {cfg.gold}; color: #162636; font-weight: 800; padding-bottom: 1px;">{escape(term)}</span>',
        )
    italic_terms = [
        "Run50", "Parkrun", "Finish Fest", "America's Toughest Road Marathon",
        "Buckeye", "Floyds Fork", "loop", "sub4", "Sub4", "Race to the Runway",
        "Halfway", "halfway moment", "Vlog",
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
        "Grand River", "LSU", "大火箭", "巨人柱", "机场终点", "凤凰城",
        "Roanoke", "Baton Rouge", "Fargo", "Huntsville", "Warren",
        "4 小时", "破4", "秋色", "热浪", "寒流", "砂石路", "绿山",
        "沙漠", "湿地", "谷仓", "玉米地", "蛋糕", "冠军", "UFO",
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
  <p style="margin: 9px 0 0; padding-left: 10px; border-left: 3px solid #d4a669; font-size: 12px; line-height: 1.6; letter-spacing: 0.2px; color: #6f7d89; font-family: Optima-Regular, 'PingFang SC', serif;">{cap}</p>
</section>"""


def paragraph(text: str, cfg: StoryConfig) -> str:
    if len(text) <= 18 and not text.endswith("。"):
        return (
            '<p style="margin: 6px 0 15px; padding: 8px 11px; line-height: 1.65; '
            f"font-size: 15px; letter-spacing: 0.3px; color: {cfg.accent}; "
            "background: #f4f8fb; border-left: 3px solid #d4a669; "
            "font-family: Georgia, 'Times New Roman', 'PingFang SC', serif; font-style: italic;\">"
            f"{accent_inline(text, cfg)}</p>"
        )
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
    pending_label = ""
    section_labels = {"前言", "后记", "楔子", "尾声"}

    def flush_section() -> None:
        for item in interleave_section_items(section_items):
            if isinstance(item, tuple):
                rendered.append(figure(item[0], item[1]))
            elif item.kind == "p":
                rendered.append(paragraph(item.text, cfg))

    items = paired_blocks(blocks)
    for index, item in enumerate(items):
        if not isinstance(item, tuple) and item.kind in {"h2", "h3"}:
            if item.text in section_labels:
                flush_section()
                section_items.clear()
                pending_label = item.text
                continue
            flush_section()
            section_items.clear()
            section_index += 1
            heading_text = f"{pending_label}｜{item.text}" if pending_label else item.text
            pending_label = ""
            rendered.append(section_heading(heading_text, section_index, cfg))
        else:
            if (
                pending_label
                and not isinstance(item, tuple)
                and item.kind == "p"
                and item.text.strip() in {"Run50", "RUN50"}
            ):
                continue
            section_items.append(item)
    flush_section()
    return rendered


def normalize_existing_page(cfg: StoryConfig) -> None:
    path = OUT_DIR / f"{cfg.slug}-modern-rail.html"
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")

    def normalize_caption(match: re.Match[str]) -> str:
        prefix, body, suffix = match.groups()
        plain = re.sub(r"<[^>]+>", "", body)
        plain = normalize_text(plain)
        if (
            not plain
            or "@Arsenan" in plain
            or "赛事摄影" in plain
            or "官方" in plain
            or "网络" in plain
            or "奖牌质感封面" in plain
            or "Vlog" in plain
            or "地图" in plain
            or "第21州" in plain
        ):
            return match.group(0)
        return f"{prefix}{body} @Arsenan{suffix}"

    text = re.sub(
        r'(<p style="[^"]*border-left: 3px solid[^"]*">)(.*?)(</p>)',
        normalize_caption,
        text,
        flags=re.S,
    )
    text = text.replace(
        "Vlog \u5f00\u573a\u4f4d\uff5c\u4ece\u80af\u5854\u57fa\u5317\u4e0a\u5bc6\u6b47\u6839\uff0c\u628a Run50 \u7b2c21\u5dde\u70b9\u4eae\u3002",
        "Vlog \u5f00\u573a\u4f4d\uff5cMichigan",
    )
    text = text.replace(
        "\u4ece\u80af\u5854\u57fa\u5230\u5bc6\u6b47\u6839\uff0cRun50 \u5df2\u70b9\u4eae\u524d 21 \u4e2a\u5dde\u3002 @Arsenan",
        "\u7b2c21\u5dde \u00b7 Michigan",
    )
    text = text.replace(
        "跑完以后也可以聊两句。如果你也跑过绕圈赛道，或者也有一次“看起来不顺、回头却很难忘”的比赛，欢迎在公众号留言区见。",
        "绕圈赛道很容易让人精神出走，但也最容易把一场比赛的细节钉进脑子里。如果你也跑过这种“绕到怀疑人生”的路线，欢迎在留言里互相取暖。",
    )
    text = text.replace("文字 / 摄影 / 设计 · Arsenan", "文字 / 编辑 / 排版 · Arsenan")
    path.write_text(text, encoding="utf-8", newline="\n")


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
  <p style="margin: 9px 0 0; padding-left: 10px; border-left: 3px solid {cfg.gold}; font-size: 12px; line-height: 1.65; letter-spacing: 0.2px; color: #6f7d89; font-family: Optima-Regular, 'PingFang SC', serif;">Vlog 开场位｜{escape(cfg.state_en.title())}</p>
</section>"""


def medal_figure(cfg: StoryConfig) -> str:
    return f"""
<section style="margin: 24px 0 28px;">
  <img src="../../assets/cover-medal-{escape(cfg.slug)}.jpg" alt="{escape(cfg.public_title)}奖牌封面" style="width: 100%; height: auto; display: block; margin: 0 auto; border-radius: 7px;">
  <p style="margin: 9px 0 0; padding-left: 10px; border-left: 3px solid {cfg.gold}; font-size: 12px; line-height: 1.65; letter-spacing: 0.2px; color: #6f7d89; font-family: Optima-Regular, 'PingFang SC', serif;">奖牌质感封面｜{escape(cfg.state_en.title())}</p>
</section>"""


def map_figure(cfg: StoryConfig) -> str:
    extra = STORY_EXTRAS.get(cfg.slug)
    if not extra:
        return ""
    return f"""
<section style="margin: 12px 0 30px;">
  <img src="../../assets/{escape(str(extra['map_asset']))}" alt="{escape(str(extra['map_caption']))}" style="width: 100%; height: auto; display: block; margin: 0 auto; border-radius: 7px;">
  <p style="margin: 9px 0 0; padding-left: 10px; border-left: 3px solid {cfg.gold}; font-size: 12px; line-height: 1.65; letter-spacing: 0.2px; color: #6f7d89; font-family: Optima-Regular, 'PingFang SC', serif;">{escape(str(extra['map_caption']))}</p>
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
        else:
            normalize_existing_page(cfg)
    (OUT_DIR / "index.html").write_text(render_index(), encoding="utf-8", newline="\n")
    print(f"generated {len(generated)} WeChat pages")
    for path in generated:
        print(path)
    print(OUT_DIR / "index.html")


if __name__ == "__main__":
    main()
