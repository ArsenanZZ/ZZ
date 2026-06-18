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
from PIL import Image, ImageDraw, ImageFont, ImageOps


REPO = Path(__file__).resolve().parents[1]
SOURCE_ROOT = Path(r"Z:\ZhennanZ Folder\0-Running Story Web")
SITE = "https://arsenanzz.github.io/ZZ"
VERSION = "20260618-medal-uploaded"
ENGAGEMENT_VERSION = "20260617"
TRANSLATION_CACHE = Path(tempfile.gettempdir()) / "zz_running_story_web_translation_cache.json"
FONT_DIR = Path(r"C:\Windows\Fonts")
PRESERVE_MEDAL_COVER_SLUGS = {"xiamen-marathon", "shanghai-vertical-marathon"}


@dataclass(frozen=True)
class SourcePart:
    source_name: str
    source_subdir: str | None = None
    heading_zh: str | None = None


@dataclass(frozen=True)
class StoryConfig:
    source_name: str
    slug: str
    image_dir: str
    channel: str
    series: str
    card_class: str
    location_zh: str
    location_en: str
    date_zh: str
    date_en: str
    title_zh: str
    title_en: str
    title_fb: str
    deck_zh: str
    deck_en: str
    card_desc_zh: str
    card_desc_en: str
    cover_title: str
    cover_subtitle: str
    badge_text: str
    badge_color: str
    palette: tuple[str, str, str, str]
    motifs: tuple[str, ...]
    source_subdir: str | None = None
    map_x: int | None = None
    map_y: int | None = None
    map_color: str | None = None
    show_in_indexes: bool = True
    source_parts: tuple[SourcePart, ...] = ()

    @property
    def source_path(self) -> Path:
        return self._source_path(SourcePart(self.source_name, self.source_subdir))

    @property
    def source_files(self) -> Path:
        return self.source_path.with_name(self.source_path.stem + "_files")

    @property
    def source_paths(self) -> tuple[Path, ...]:
        parts = self.source_parts or (SourcePart(self.source_name, self.source_subdir),)
        return tuple(self._source_path(part) for part in parts)

    @property
    def source_files_list(self) -> tuple[Path, ...]:
        return tuple(path.with_name(path.stem + "_files") for path in self.source_paths)

    def _source_path(self, part: SourcePart) -> Path:
        base = SOURCE_ROOT / part.source_subdir if part.source_subdir else SOURCE_ROOT
        return base / part.source_name


STORIES: list[StoryConfig] = [
    StoryConfig(
        source_name="Run50 #第16州 ｜北卡罗莱纳：橡树岛马拉松｜冲向大西洋，奖牌比脸还大！.html",
        slug="north-carolina-oak-island-marathon",
        image_dir="Run50-North-Carolina-Oak-Island-Marathon-clean_files",
        channel="Run50",
        series="Run50 #16",
        card_class="run-50",
        location_zh="北卡罗莱纳橡树岛",
        location_en="Oak Island, North Carolina",
        date_zh="2025 归档",
        date_en="2025 archive",
        title_zh="Run50 #第16州｜北卡罗莱纳：橡树岛马拉松",
        title_en="Run50 #16 | North Carolina: Oak Island Marathon",
        title_fb="Oak Island sent Run50 toward the Atlantic with a medal bigger than my face",
        deck_zh="从深冬训练出发，奔向北卡海岸线和大西洋，把第16州签收在一块大得离谱的奖牌里。",
        deck_en="A winter-training check-in on the North Carolina coast, running toward the Atlantic and signing off Run50 State 16 with a gloriously oversized medal.",
        card_desc_zh="北卡橡树岛的海边全马：深冬训练、海风、大西洋和一块比脸还大的奖牌。",
        card_desc_en="A North Carolina coast marathon with winter legs, ocean wind, Atlantic light, and a medal that refused to be subtle.",
        cover_title="OAK ISLAND",
        cover_subtitle="ATLANTIC COAST · BIG MEDAL · RUN50",
        badge_text="NORTH CAROLINA",
        badge_color="#0b67c2",
        palette=("#edf7fb", "#2c7da0", "#f2c14e", "#d1495b"),
        motifs=("ocean waves", "lighthouse", "big medal", "finish flag"),
        map_x=509,
        map_y=280,
        map_color="#ff4040",
    ),
    StoryConfig(
        source_name="以最难忘的出场，享拥每一句赞扬 ——记录我的厦马故事.html",
        slug="xiamen-marathon",
        image_dir="RunCN-Xiamen-Marathon-clean_files",
        channel="RunCN",
        series="RunCN #5",
        card_class="run-cn",
        location_zh="福建厦门",
        location_en="Xiamen, Fujian",
        date_zh="2018 归档",
        date_en="2018 archive",
        title_zh="RunCN #第5站｜厦门马拉松：以最难忘的出场，享拥每一句赞扬",
        title_en="RunCN #5 | Xiamen Marathon: the most unforgettable entrance",
        title_fb="Xiamen gave my 2018 season a rain-soaked, unforgettable opening",
        deck_zh="2018年的首马，在厦门的雨里开场：曾厝垵、兄弟重逢、赛道掌声和一个惊艳自己的开局。",
        deck_en="My first marathon of 2018 opened in Xiamen rain, with Zengcuo'an, a reunion on the road, finish-line applause, and a start that surprised me.",
        card_desc_zh="厦门雨战、曾厝垵、跑友重逢，以及2018年开年的第一场全马。",
        card_desc_en="A rainy Xiamen Marathon, a Zengcuo'an reunion, and the first full-marathon chapter of 2018.",
        cover_title="XIAMEN",
        cover_subtitle="RAIN · ISLAND ROAD · 2018 OPENER",
        badge_text="XIAMEN",
        badge_color="#cc0000",
        palette=("#faf2ee", "#1f8a8a", "#f6bd60", "#cc0000"),
        motifs=("island road", "rain", "seaside", "finish applause"),
        map_x=1490,
        map_y=328,
        map_color="#d4614a",
    ),
    StoryConfig(
        source_name="在上海，我爬上了中国最高的 Building.html",
        slug="shanghai-vertical-marathon",
        image_dir="RunCN-Shanghai-Vertical-Marathon-clean_files",
        channel="RunCN",
        series="RunCN #4",
        card_class="run-cn",
        location_zh="上海",
        location_en="Shanghai, China",
        date_zh="2019.11.24",
        date_en="Nov 24, 2019",
        title_zh="RunCN #第4站｜上海中心垂直马拉松",
        title_en="RunCN #4 | Shanghai Tower Vertical Marathon",
        title_fb="Climbing 3,398 steps to the top of China's tallest skyscraper",
        deck_zh="在签证等待的特殊时期，爬上119层、3398级台阶，在632米高处俯瞰浦江两岸。",
        deck_en="During a strange visa waiting period, I climbed 119 floors and 3,398 steps to look over Shanghai from 632 meters up.",
        card_desc_zh="上海中心垂直马拉松：119层、3398级台阶，和一段特殊时期里的魔都记忆。",
        card_desc_en="A vertical marathon up Shanghai Tower: 119 floors, 3,398 steps, and a strange season of life in the Magic City.",
        cover_title="SHANGHAI",
        cover_subtitle="VERTICAL MARATHON · 3398 STEPS",
        badge_text="SHANGHAI",
        badge_color="#cc0000",
        palette=("#eef5f6", "#1b3a4b", "#c09030", "#cc0000"),
        motifs=("Shanghai Tower", "Oriental Pearl", "stairs", "skyline"),
        map_x=1507,
        map_y=294,
        map_color="#d4614a",
        show_in_indexes=False,
    ),
    StoryConfig(
        source_name="我去西湖跑半马，偶遇跑者施一公.html",
        slug="west-lake-half-marathon",
        image_dir="RunCN-West-Lake-Half-Marathon-clean_files",
        channel="RunCN",
        series="RunCN #6",
        card_class="run-cn",
        location_zh="浙江杭州",
        location_en="Hangzhou, Zhejiang",
        date_zh="2019 归档",
        date_en="2019 archive",
        title_zh="RunCN #第6站｜西湖半马：我去西湖跑半马，偶遇跑者施一公",
        title_en="RunCN #6 | West Lake Half Marathon and a surprise encounter",
        title_fb="A West Lake half marathon turned into a lakeside reset and an unexpected encounter",
        deck_zh="从上海到杭州，去西湖边甩肉，跑一场半马，也偶遇了跑者施一公。",
        deck_en="A short trip from Shanghai to Hangzhou for a West Lake half marathon, a reset run, and an unexpected encounter with Shi Yigong.",
        card_desc_zh="西湖、青芝坞、西湖大学和一场重新找回状态的半马。",
        card_desc_en="West Lake, Qingzhiwu, Westlake University, and a half marathon that helped me restart.",
        cover_title="HANGZHOU",
        cover_subtitle="WEST LAKE · HALF MARATHON",
        badge_text="WEST LAKE",
        badge_color="#cc0000",
        palette=("#f2f7ee", "#3a7d44", "#9cc5a1", "#cc0000"),
        motifs=("West Lake", "bridge", "willows", "university"),
        map_x=1501,
        map_y=299,
        map_color="#d4614a",
    ),
    StoryConfig(
        source_name="曼谷，昼夜不停.html",
        slug="bangkok-marathon",
        image_dir="RunWorld-Bangkok-Marathon-clean_files",
        channel="RunWorld",
        series="RunWorld #3",
        card_class="run-world",
        location_zh="泰国曼谷",
        location_en="Bangkok, Thailand",
        date_zh="2019 归档",
        date_en="2019 archive",
        title_zh="RunWorld #第3站｜曼谷马拉松：昼夜不停",
        title_en="RunWorld #3 | Bangkok Marathon: day and night, nonstop",
        title_fb="Bangkok kept moving from temple light to marathon night",
        deck_zh="去泰国跑马，不囧，反而意犹未尽：寺庙、夜色、四面佛和一个昼夜不停的曼谷。",
        deck_en="A Thailand marathon trip that was not awkward at all: temples, night streets, the Erawan Shrine, and a Bangkok that never stopped moving.",
        card_desc_zh="曼谷跑马、寺庙夜色、四面佛许愿和微笑国度的热烈周末。",
        card_desc_en="A Bangkok running weekend through temple light, night streets, the Erawan Shrine, and the warmth of Thailand.",
        cover_title="BANGKOK",
        cover_subtitle="TEMPLES · NIGHT RUN · THAILAND",
        badge_text="BANGKOK",
        badge_color="#2f855a",
        palette=("#f1f6f2", "#6a4c93", "#f4a261", "#2f855a"),
        motifs=("temple", "tuk-tuk", "river", "night lights"),
        map_x=1402,
        map_y=381,
        map_color="#2f855a",
    ),
    StoryConfig(
        source_name="毕业图话，迟到了两年.html",
        slug="wuhan-graduation",
        image_dir="RunCN-Wuhan-Graduation-clean_files",
        channel="RunCN",
        series="RunCN Archive",
        card_class="run-cn",
        location_zh="湖北武汉",
        location_en="Wuhan, Hubei",
        date_zh="2019 归档",
        date_en="2019 archive",
        title_zh="RunCN 归档｜毕业图话，迟到了两年",
        title_en="RunCN Archive | Graduation photos, two years late",
        title_fb="A delayed Wuhan graduation album became a time capsule",
        deck_zh="迟到两年的毕业图话，把爸妈、武大、东湖、毕业典礼和那段武汉时光收进同一篇回忆。",
        deck_en="A graduation album two years late, keeping my parents, Wuhan University, East Lake, commencement, and that Wuhan season in one place.",
        card_desc_zh="武大毕业、爸妈来武汉、东湖和一组迟到两年的照片回忆。",
        card_desc_en="Wuhan University graduation, family visiting Wuhan, East Lake, and a photo album that arrived two years late.",
        cover_title="WUHAN",
        cover_subtitle="GRADUATION · WHU · EAST LAKE",
        badge_text="WUHAN",
        badge_color="#cc0000",
        palette=("#faf2ee", "#6f8f72", "#b56576", "#cc0000"),
        motifs=("Wuhan University", "cherry blossoms", "East Lake", "graduation"),
        map_x=1472,
        map_y=297,
        map_color="#d4614a",
    ),
    StoryConfig(
        source_name="河西走廊东边的野望与奔腾——兰州Strong.html",
        slug="lanzhou-marathon",
        image_dir="RunCN-Lanzhou-Marathon-clean_files",
        channel="RunCN",
        series="RunCN #7",
        card_class="run-cn",
        location_zh="甘肃兰州",
        location_en="Lanzhou, Gansu",
        date_zh="2018 归档",
        date_en="2018 archive",
        title_zh="RunCN #第7站｜兰州马拉松：河西走廊东边的野望与奔腾",
        title_en="RunCN #7 | Lanzhou Marathon on the eastern edge of the Hexi Corridor",
        title_fb="Lanzhou Strong: a marathon at the edge of the Yellow River and the Hexi dream",
        deck_zh="一碗面、一条河、一本书、一座城，把兰马写进河西走廊东边的风与奔腾。",
        deck_en="A bowl of noodles, a river, a book, and a city: Lanzhou Marathon as wind and momentum on the eastern edge of the Hexi Corridor.",
        card_desc_zh="黄河、牛肉面、中山桥、皋兰山和热情到炸的兰州马拉松。",
        card_desc_en="The Yellow River, beef noodles, Zhongshan Bridge, Gaolan Mountain, and a Lanzhou Marathon with roaring local energy.",
        cover_title="LANZHOU",
        cover_subtitle="YELLOW RIVER · HEXI CORRIDOR",
        badge_text="LANZHOU",
        badge_color="#cc0000",
        palette=("#fff3d8", "#b7791f", "#2f6f73", "#cc0000"),
        motifs=("Yellow River", "Zhongshan Bridge", "noodles", "mountains"),
        map_x=1419,
        map_y=269,
        map_color="#d4614a",
    ),
    StoryConfig(
        source_name="海口的诗和远方与星沉大海.html",
        slug="haikou-marathon",
        image_dir="RunCN-Haikou-Marathon-clean_files",
        channel="RunCN",
        series="RunCN #8",
        card_class="run-cn",
        location_zh="海南海口",
        location_en="Haikou, Hainan",
        date_zh="2019 归档",
        date_en="2019 archive",
        title_zh="RunCN #第8站｜海口：诗和远方与星沉大海",
        title_en="RunCN #8 | Haikou: poetry, distance, and a sea full of stars",
        title_fb="Haikou became an unfinished running story by the sea",
        deck_zh="错过三亚，又跑丢海口，但骑楼老街、海风、芳华小院和2019的开篇仍然值得留下。",
        deck_en="After missing Sanya and losing the Haikou race, the old arcades, sea wind, Fanghua courtyard, and the start of 2019 still deserved to be saved.",
        card_desc_zh="海口骑楼、海南海风、未完赛的遗憾和一篇仍要留下的城市故事。",
        card_desc_en="Haikou arcades, Hainan sea wind, an unfinished race, and a city story still worth keeping.",
        cover_title="HAIKOU",
        cover_subtitle="HAINAN · ARCADES · SEA WIND",
        badge_text="HAIKOU",
        badge_color="#cc0000",
        palette=("#fef7e5", "#00a6a6", "#f4a261", "#cc0000"),
        motifs=("arcade street", "palm trees", "sea", "old town"),
        map_x=1452,
        map_y=350,
        map_color="#d4614a",
    ),
    StoryConfig(
        source_name="独家记忆 _ 武汉，汉马.html",
        slug="wuhan-han-marathon",
        image_dir="RunCN-Wuhan-Han-Marathon-clean_files",
        channel="RunCN",
        series="RunCN #9",
        card_class="run-cn",
        location_zh="湖北武汉",
        location_en="Wuhan, Hubei",
        date_zh="2019 归档",
        date_en="2019 archive",
        title_zh="RunCN #第9站｜武汉汉马：独家记忆",
        title_en="RunCN #9 | Wuhan Han Marathon: a private memory",
        title_fb="Wuhan and the Han Marathon became my private memory of leaving home",
        deck_zh="即将离开武汉的人，也会有乡愁。汉马、武大和江城三年的断片，被拼成一篇独家记忆。",
        deck_en="Can someone about to leave Wuhan feel homesick already? Han Marathon, Wuhan University, and three years of city fragments became a private memory.",
        card_desc_zh="汉马、武大、江城、毕业前的乡愁和一场属于武汉的独家记忆。",
        card_desc_en="Han Marathon, Wuhan University, River City, pre-graduation homesickness, and a private Wuhan memory.",
        cover_title="WUHAN",
        cover_subtitle="HAN MARATHON · RIVER CITY",
        badge_text="WUHAN",
        badge_color="#cc0000",
        palette=("#faf2ee", "#2a9d8f", "#e76f51", "#cc0000"),
        motifs=("Yangtze River", "Wuhan University", "bridge", "marathon"),
        map_x=1472,
        map_y=297,
        map_color="#d4614a",
    ),
    StoryConfig(
        source_name="越过山丘，在大连.html",
        slug="dalian-trail",
        image_dir="RunCN-Dalian-Trail-clean_files",
        channel="RunCN",
        series="RunCN Trail",
        card_class="run-cn",
        location_zh="辽宁大连",
        location_en="Dalian, Liaoning",
        date_zh="2019 归档",
        date_en="2019 archive",
        title_zh="RunCN 越野｜越过山丘，在大连",
        title_en="RunCN Trail | Over the hills in Dalian",
        title_fb="Dalian turned my first real trail race into a Northeastern coming-of-age story",
        deck_zh="第一场真正意义上的越野赛，去大连西海岸，越过山丘，也看见东北的自由与斑驳。",
        deck_en="My first real trail race took me to Dalian's west coast, over the hills, and into a Northeastern story of freedom and weathered beauty.",
        card_desc_zh="大连西海岸、黄渤海分界线、越野赛和一篇写给东北的山丘故事。",
        card_desc_en="Dalian's west coast, the Yellow Sea and Bohai Sea divide, a trail race, and a hill story for the Northeast.",
        cover_title="DALIAN",
        cover_subtitle="TRAIL · COAST · NORTHEAST",
        badge_text="DALIAN",
        badge_color="#cc0000",
        palette=("#eef7fb", "#0f766e", "#f59e0b", "#cc0000"),
        motifs=("coastline", "hills", "trail", "sea boundary"),
        map_x=1508,
        map_y=256,
        map_color="#d4614a",
    ),
    StoryConfig(
        source_name="连接百年的奔跑，燃到炸的热血江城 ——FIR IN 大武汉.html",
        slug="wuhan-marathon-2018",
        image_dir="RunCN-Wuhan-Marathon-2018-clean_files",
        channel="RunCN",
        series="RunCN #10",
        card_class="run-cn",
        location_zh="湖北武汉",
        location_en="Wuhan, Hubei",
        date_zh="2018 归档",
        date_en="2018 archive",
        title_zh="RunCN #第10站｜武汉马拉松：连接百年的奔跑",
        title_en="RunCN #10 | Wuhan Marathon: a century-spanning run",
        title_fb="Wuhan Marathon connected a century of city fire and running energy",
        deck_zh="想读懂汉马，先读懂武汉。从辛亥、东湖到赛道热浪，把江城的体育基因写进一场马拉松。",
        deck_en="To understand Han Marathon, first understand Wuhan: from 1911 and East Lake to race-day heat, the city's sporting DNA runs through the course.",
        card_desc_zh="辛亥、东湖、汉马志愿者和燃到炸的大武汉。",
        card_desc_en="1911 memory, East Lake, Han Marathon volunteers, and Wuhan at full volume.",
        cover_title="WUHAN",
        cover_subtitle="HAN MARATHON · CITY FIRE",
        badge_text="WUHAN",
        badge_color="#cc0000",
        palette=("#fff1e6", "#d9480f", "#1f7a8c", "#cc0000"),
        motifs=("Yellow Crane Tower", "East Lake", "bridge", "flames"),
        map_x=1472,
        map_y=297,
        map_color="#d4614a",
    ),
    StoryConfig(
        source_name="那年，我在东北老家跑哈马.html",
        slug="harbin-marathon",
        image_dir="RunCN-Harbin-Marathon-clean_files",
        channel="RunCN",
        series="RunCN #11",
        card_class="run-cn",
        location_zh="黑龙江哈尔滨",
        location_en="Harbin, Heilongjiang",
        date_zh="2019 归档",
        date_en="2019 archive",
        title_zh="RunCN #第11站｜哈尔滨马拉松：那年，我在东北老家跑哈马",
        title_en="RunCN #11 | Harbin Marathon: running back home in the Northeast",
        title_fb="Harbin Marathon brought me back to the black soil and Songhua River",
        deck_zh="因为 check 多跑了一次哈马。松花江、黑土地、老家和疫情前那些快活的流浪日子，都在这篇里。",
        deck_en="A visa check gave me one more Harbin Marathon: Songhua River, black soil, home, and the wandering days before everything paused.",
        card_desc_zh="松花江、黑土地、东北老家和一次迟来的哈马回忆。",
        card_desc_en="Songhua River, black soil, Northeastern home, and a delayed Harbin Marathon memory.",
        cover_title="HARBIN",
        cover_subtitle="SONGHUA RIVER · BLACK SOIL",
        badge_text="HARBIN",
        badge_color="#cc0000",
        palette=("#eef6ff", "#2563eb", "#94a3b8", "#cc0000"),
        motifs=("Songhua River", "ice", "bridge", "home"),
        map_x=1533,
        map_y=221,
        map_color="#d4614a",
    ),
    StoryConfig(
        source_name="钢铁战车的故事.html",
        slug="steel-tank-story",
        image_dir="RunCN-Steel-Tank-Story-clean_files",
        channel="RunCN",
        series="RunCN Origin",
        card_class="run-cn",
        location_zh="哈尔滨 / 武汉",
        location_en="Harbin / Wuhan",
        date_zh="2017 归档",
        date_en="2017 archive",
        title_zh="RunCN 起点｜钢铁战车的故事",
        title_en="RunCN Origin | The story of the steel tank",
        title_fb="The steel tank story: how a heavy football kid found marathons",
        deck_zh="半年，6座城，3半马，3全马。从胖纸、足球后腰到跑马的人，钢铁战车的起点在这里。",
        deck_en="Six months, six cities, three half marathons, three full marathons: from a heavy football midfielder to someone who could run marathons.",
        card_desc_zh="从足球场上的钢铁战车，到哈尔滨马拉松终点线上的骄傲儿子。",
        card_desc_en="From the steel tank on the football field to a proud son at the Harbin Marathon finish.",
        cover_title="STEEL TANK",
        cover_subtitle="ORIGIN · FOOTBALL · MARATHON",
        badge_text="ORIGIN",
        badge_color="#cc0000",
        palette=("#f7f3e8", "#374151", "#ef4444", "#cc0000"),
        motifs=("football", "running shoes", "medal", "transformation"),
        map_x=1533,
        map_y=221,
        map_color="#d4614a",
    ),
    StoryConfig(
        source_name="飘落的“三月雪”｜樱花树下绽放——武汉，无锡三马笔记.html",
        slug="wuhan-wuxi-marathon-notes",
        image_dir="RunCN-Wuhan-Wuxi-Marathon-Notes-clean_files",
        channel="RunCN",
        series="RunCN Notes",
        card_class="run-cn",
        location_zh="武汉 / 无锡",
        location_en="Wuhan / Wuxi",
        date_zh="2018 归档",
        date_en="2018 archive",
        title_zh="RunCN 笔记｜武汉、无锡三马笔记：樱花树下绽放",
        title_en="RunCN Notes | Wuhan and Wuxi: three races under cherry blossoms",
        title_fb="Three spring races bloomed under cherry trees in Wuhan and Wuxi",
        deck_zh="三月，奔跑与樱花不期而遇。东湖岸边、蠡湖水畔，三场比赛写成一篇真实的跑马笔记。",
        deck_en="In March, running met cherry blossoms: East Lake, Lihu Lake, and three races became one honest set of notes.",
        card_desc_zh="武汉、无锡、樱花、大学生马拉松和三场春天里的跑步笔记。",
        card_desc_en="Wuhan, Wuxi, cherry blossoms, a college marathon, and three spring race notes.",
        cover_title="SPRING RUNS",
        cover_subtitle="WUHAN · WUXI · CHERRY BLOSSOMS",
        badge_text="WUHAN WUXI",
        badge_color="#cc0000",
        palette=("#fff1f5", "#db2777", "#22c55e", "#cc0000"),
        motifs=("cherry blossoms", "East Lake", "Lihu Lake", "campus"),
        map_x=1502,
        map_y=292,
        map_color="#d4614a",
    ),
    StoryConfig(
        source_subdir="迪士尼马拉松",
        source_name="2-美国50州挑战 ｜第15州：佛罗里达 奥兰多 “迪士尼马拉松”｜ Run50 系列更新.html",
        slug="disney-marathon",
        image_dir="Run50-Disney-Marathon-clean_files",
        channel="Run50",
        series="Run50 #15",
        card_class="run-50",
        location_zh="佛罗里达基韦斯特 / 奥兰多",
        location_en="Key West / Orlando, Florida",
        date_zh="2025 归档",
        date_en="2025 archive",
        title_zh="Run50 #第15州｜佛罗里达：基韦斯特、奥兰多与迪士尼马拉松",
        title_en="Run50 #15 | Florida: Key West, Orlando, and Disney Marathon",
        title_fb="A Florida week from Key West beaches to Disney Marathon",
        deck_zh="把基韦斯特跨年、奥兰多乐园速通和迪士尼马拉松合成一篇完整的佛州第15州故事。",
        deck_en="A complete Run50 State 15 story: New Year's in Key West, an Orlando park speedrun, and the Disney Marathon.",
        card_desc_zh="佛罗里达第15州完整篇：基韦斯特跨年、奥兰多速通、环球影城和迪士尼马拉松。",
        card_desc_en="Run50 State 15 as one Florida arc: Key West New Year, Orlando speedrun, Universal, and Disney Marathon.",
        cover_title="FLORIDA",
        cover_subtitle="KEY WEST · ORLANDO · DISNEY MARATHON",
        badge_text="FLORIDA",
        badge_color="#0b67c2",
        palette=("#edf3f7", "#2563eb", "#fbbf24", "#0b67c2"),
        motifs=("castle silhouette", "palm trees", "roller coaster", "fireworks"),
        map_x=493,
        map_y=307,
        map_color="#ff4040",
        source_parts=(
            SourcePart(
                source_subdir="迪士尼马拉松",
                source_name="0-美国小海南「基韦斯特🥥」， 跨年不冻手🥶 短袖沙滩走🥻 烦恼全溜走🥳.html",
                heading_zh="# 01｜基韦斯特：美国小海南",
            ),
            SourcePart(
                source_subdir="迪士尼马拉松",
                source_name="1-奥兰多速通计划｜迪士尼 「呆呆挑战」，环球影城，过山车真香！哎～.html",
                heading_zh="# 02｜奥兰多速通计划：迪士尼挑战与环球影城",
            ),
            SourcePart(
                source_subdir="迪士尼马拉松",
                source_name="2-美国50州挑战 ｜第15州：佛罗里达 奥兰多 “迪士尼马拉松”｜ Run50 系列更新.html",
                heading_zh="# 03｜Run50 第15州：奥兰多迪士尼马拉松",
            ),
        ),
    ),
]


DEPRECATED_REDIRECTS = {
    "key-west-florida": "disney-marathon",
    "orlando-disney-challenge": "disney-marathon",
}


SPECIAL_TRANSLATIONS = {
    "前言": "Preface",
    "前记": "Preface",
    "后记": "Postscript",
    "- 本文完 -": "- The end -",
    "文字丨Arsenan": "Words | Arsenan",
    "摄影丨Arsenan": "Photos | Arsenan",
    "设计丨Arsenan": "Design | Arsenan",
    "# 01｜基韦斯特：美国小海南": "# 01 | Key West: America's little Hainan",
    "# 02｜奥兰多速通计划：迪士尼挑战与环球影城": "# 02 | Orlando speedrun: Disney challenge and Universal",
    "# 03｜Run50 第15州：奥兰多迪士尼马拉松": "# 03 | Run50 State 15: Orlando Disney Marathon",
}


def norm(value: str) -> str:
    return re.sub(r"\s+", " ", value.replace("\xa0", " ")).strip()


def is_styleish(value: str) -> bool:
    return ":host {" in value or "--weui-" in value or len(value) > 1100


def has_desc_leaf_container(el) -> bool:
    for desc in el.iterdescendants():
        if desc.tag in ("p", "section"):
            text = norm("".join(desc.itertext()))
            if text and not is_styleish(text):
                return True
    return False


def is_platform_text(text: str) -> bool:
    junk = {
        "+",
        "0/0",
        "继续观看",
        "Thumbplayer 离线日志上报",
        "，赞",
    }
    if text in junk:
        return True
    return text.startswith(("鲜花", "微信扫一扫", "Read more", "继续滑动看下一个"))


def extract_source_events(source_path: Path, source_files: Path) -> list[dict]:
    source = source_path.read_text(encoding="utf-8", errors="replace")
    doc = html.fromstring(source)
    roots = doc.xpath('//*[@id="js_content"]')
    root = roots[0] if roots else doc
    events: list[dict] = []

    def should_keep_image(src: str) -> bool:
        if not src or src.startswith("data:"):
            return False
        parsed = urllib.parse.urlparse(src)
        return not (parsed.netloc == "mp.weixin.qq.com" and parsed.path.startswith("/s/"))

    def walk(el) -> None:
        if el.tag == "img":
            src = el.get("src") or el.get("data-src") or ""
            if should_keep_image(src):
                events.append({"type": "image", "src": src, "source_files": source_files})
            return
        if el.tag in ("p", "section"):
            text = norm("".join(el.itertext()))
            if text and not is_styleish(text) and not has_desc_leaf_container(el):
                if not is_platform_text(text):
                    events.append({"type": "text", "text": text})
                for img in el.xpath(".//img"):
                    src = img.get("src") or img.get("data-src") or ""
                    if should_keep_image(src):
                        events.append({"type": "image", "src": src, "source_files": source_files})
                return
        for child in el:
            walk(child)

    for child in root:
        walk(child)

    deduped: list[dict] = []
    for event in events:
        key = (event["type"], event.get("text") or event.get("src"))
        prev = (deduped[-1]["type"], deduped[-1].get("text") or deduped[-1].get("src")) if deduped else None
        if key != prev:
            deduped.append(event)

    end = len(deduped)
    for idx, event in enumerate(deduped):
        if event["type"] == "text" and event["text"].startswith("设计丨"):
            end = idx + 1
            break
    return deduped[:end]


def extract_story(config: StoryConfig) -> list[dict]:
    if not config.source_parts:
        return extract_source_events(config.source_path, config.source_files)
    combined: list[dict] = []
    for part, source_path, source_files in zip(config.source_parts, config.source_paths, config.source_files_list):
        if part.heading_zh:
            combined.append({"type": "text", "text": part.heading_zh})
        combined.extend(extract_source_events(source_path, source_files))
    return combined


def load_translation_cache() -> dict[str, str]:
    if TRANSLATION_CACHE.exists():
        return json.loads(TRANSLATION_CACHE.read_text(encoding="utf-8"))
    return {}


def save_translation_cache(cache: dict[str, str]) -> None:
    TRANSLATION_CACHE.parent.mkdir(parents=True, exist_ok=True)
    TRANSLATION_CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")


def translation_key(text: str) -> str:
    return text[2:].strip() if text.startswith("# ") else text


def needs_translation(text: str) -> bool:
    if text in SPECIAL_TRANSLATIONS:
        return False
    if re.fullmatch(r"\d{1,2}", text):
        return False
    return True


def polish_translation(text: str) -> str:
    replacements = {
        "competition day": "race day",
        "Competition Day": "Race day",
        "game": "race",
        "number plate": "bib",
        "entry package": "race packet",
        "receiving package": "packet pickup",
        "horse pull loose": "marathon",
        "half horse": "half marathon",
        "full horse": "full marathon",
        "Run Fifty": "Run50",
        "West Lake University": "Westlake University",
        "Xiamen Horse": "Xiamen Marathon",
        "Hanma": "Han Marathon",
        "Hama": "Harbin Marathon",
        "Disney Horse": "Disney Marathon",
        "Oak Island Horse": "Oak Island Marathon",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = text.replace(" ,", ",").replace(" .", ".").replace(" !", "!").replace(" ?", "?")
    return re.sub(r"\s+", " ", text).strip()


def google_translate_joined(texts: list[str]) -> list[str]:
    if not texts:
        return []
    separators = [f"ZZSEP{i:04d}ZZ" for i in range(1, len(texts))]
    joined = texts[0]
    for sep, text in zip(separators, texts[1:]):
        joined += f"\n{sep}\n{text}"
    query = urllib.parse.urlencode({"client": "gtx", "sl": "zh-CN", "tl": "en", "dt": "t", "q": joined})
    with urllib.request.urlopen("https://translate.googleapis.com/translate_a/single?" + query, timeout=60) as response:
        data = json.loads(response.read().decode("utf-8"))
    translated = "".join(part[0] for part in data[0])
    pieces = [translated]
    for sep in separators:
        next_pieces: list[str] = []
        for piece in pieces:
            next_pieces.extend(piece.split(sep))
        pieces = next_pieces
    if len(pieces) != len(texts):
        raise RuntimeError("Translation separator split mismatch")
    return [polish_translation(piece) for piece in pieces]


def safe_translate_batch(texts: list[str]) -> list[str]:
    try:
        return google_translate_joined(texts)
    except Exception:
        translated: list[str] = []
        for text in texts:
            translated.extend(google_translate_joined([text]))
            time.sleep(0.1)
        return translated


def ensure_translations(all_events: list[list[dict]]) -> dict[str, str]:
    cache = load_translation_cache()
    missing: list[str] = []
    for events in all_events:
        for event in events:
            if event["type"] == "text" and needs_translation(event["text"]):
                key = translation_key(event["text"])
                if key not in cache:
                    missing.append(key)
    missing = list(dict.fromkeys(missing))
    print(f"translation cache: {len(cache)} existing, {len(missing)} missing")
    batch: list[str] = []
    chars = 0
    for key in missing:
        if batch and chars + len(key) > 1200:
            for src, dst in zip(batch, safe_translate_batch(batch)):
                cache[src] = dst
            save_translation_cache(cache)
            batch = []
            chars = 0
            time.sleep(0.08)
        batch.append(key)
        chars += len(key)
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
    value = cache.get(translation_key(text), text)
    return polish_translation(value)


def font(size: int, bold: bool = False):
    names = ["arialbd.ttf", "msyhbd.ttc", "simhei.ttf"] if bold else ["arial.ttf", "msyh.ttc", "simhei.ttf"]
    for name in names:
        path = FONT_DIR / name
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def fit_font(draw: ImageDraw.ImageDraw, text: str, max_width: int, start: int, minimum: int, bold: bool = True):
    for size in range(start, minimum - 1, -2):
        candidate = font(size, bold)
        bbox = draw.textbbox((0, 0), text, font=candidate)
        if bbox[2] - bbox[0] <= max_width:
            return candidate
    return font(minimum, bold)


def local_image_path(config: StoryConfig, event: dict) -> Path | None:
    src = event["src"]
    parsed = urllib.parse.urlparse(src)
    name = Path(urllib.parse.unquote(parsed.path)).name
    if "_files/" in src:
        name = urllib.parse.unquote(src.split("_files/", 1)[1].split("?", 1)[0].split("#", 1)[0])
    source_files = event.get("source_files") or config.source_files
    candidates = [
        source_files / name,
        source_files / name.replace("%28", "(").replace("%29", ")"),
    ]
    for candidate in candidates:
        if candidate.exists() and candidate.is_file():
            return candidate
    return None


def copy_story_images(config: StoryConfig, events: list[dict]) -> int:
    out_dir = REPO / "run50" / "stories" / "chinese" / config.image_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    for old in out_dir.glob("img-*.webp"):
        old.unlink()
    count = 0
    missing: list[str] = []
    for event in events:
        if event["type"] != "image":
            continue
        src_path = local_image_path(config, event)
        if not src_path:
            missing.append(event["src"])
            event["skip"] = True
            continue
        count += 1
        out_name = f"img-{count:03d}.webp"
        out_path = out_dir / out_name
        with Image.open(src_path) as image:
            image = ImageOps.exif_transpose(image)
            if image.mode != "RGB":
                image = image.convert("RGB")
            image.save(out_path, "WEBP", quality=88, method=6)
        event["out"] = out_name
    if missing:
        print(f"warning: {config.slug} skipped {len(missing)} missing images")
    return count


def is_caption(text: str) -> bool:
    return text.startswith("▲")


def clean_caption(text: str) -> str:
    text = re.sub(r"^▲\s*", "", text).strip()
    return text


def render_text(config: StoryConfig, text: str, lang: str, cache: dict[str, str]) -> str:
    value = text if lang == "zh" else translate_text(text, cache)
    clean = value[2:].strip() if value.startswith("# ") else value
    original = text[2:].strip() if text.startswith("# ") else text
    if text.startswith("# "):
        return f"<h2>{escape(clean)}</h2>"
    if original in {"前言", "前记", "后记", "赛前", "赛中", "赛后"}:
        return f'<h2 class="section-label">{escape(clean)}</h2>'
    if re.fullmatch(r"\d{1,2}", original):
        return f"<h3>{escape(clean)}</h3>"
    if original == "- 本文完 -":
        return f'<p class="end-mark">{escape(clean)}</p>'
    if original.startswith(("文字丨", "摄影丨", "设计丨")):
        return f'<p class="credit-line">{escape(clean)}</p>'
    if original.startswith("丨") and original.endswith("丨"):
        return f'<p class="place">{escape(clean)}</p>'
    if len(original) <= 18 and not original.endswith(("。", "，", "！", "？", ".", ",")) and any(ch in original for ch in "：·丨"):
        return f'<p class="place">{escape(clean)}</p>'
    return f"<p>{escape(clean)}</p>"


def render_events(config: StoryConfig, events: list[dict], lang: str, image_prefix: str, cache: dict[str, str]) -> str:
    parts: list[str] = []
    pending_caption: str | None = None
    for event in events:
        if event["type"] == "image":
            if event.get("skip"):
                continue
            number = int(event["out"].split("-")[1].split(".")[0])
            alt = f"{config.location_en} story photo {number}" if lang == "en" else f"{config.location_zh}故事照片 {number}"
            figure = (
                f'<figure><img src="{image_prefix}{event["out"]}" alt="{escape(alt)}" '
                f'loading="lazy" decoding="async">'
            )
            if pending_caption:
                figure += f"<figcaption>{escape(pending_caption)}</figcaption>"
                pending_caption = None
            figure += "</figure>"
            parts.append(figure)
            continue

        text = event["text"]
        if is_caption(text):
            caption = clean_caption(text if lang == "zh" else translate_text(text, cache))
            if parts and parts[-1].endswith("</figure>") and "<figcaption>" not in parts[-1]:
                parts[-1] = parts[-1].replace("</figure>", f"<figcaption>{escape(caption)}</figcaption></figure>")
            else:
                pending_caption = caption
            continue
        if pending_caption:
            parts.append(f'<p class="caption-line">{escape(pending_caption)}</p>')
            pending_caption = None
        parts.append(render_text(config, text, lang, cache))
    if pending_caption:
        parts.append(f'<p class="caption-line">{escape(pending_caption)}</p>')
    return "\n      ".join(parts)


def engagement(config: StoryConfig, lang: str, fb: bool = False) -> str:
    suffix = "facebook-en" if fb else ("zh" if lang == "zh" else "en")
    page_key = f"run50-{config.slug}-{suffix}"
    locale = "zh-CN" if lang == "zh" else "en"
    if lang == "zh":
        heading = "跑完也说两句"
        kicker = "留言 / 访问次数"
        note = "不用注册账号即可提交留言，提交后会直接显示。"
        status = "留言区加载中..."
        views = "访问"
    else:
        heading = "Say something after the run"
        kicker = "Comments / Views"
        note = "No account is needed to submit a comment. New comments appear right away."
        status = "Loading comments..."
        views = "Views"
    return f"""
  <section class="zz-engagement" data-zz-engagement data-locale="{locale}" data-page-key="{page_key}">
    <div class="zz-engagement-shell">
      <div>
        <p class="zz-engagement-kicker">{kicker}</p>
        <h2>{heading}</h2>
        <p class="zz-engagement-note">{note}</p>
        <div class="zz-engagement-stats"><span class="zz-engagement-stat" id="busuanzi_container_page_pv"><span>{views}</span><strong id="busuanzi_value_page_pv" data-zz-view-count>--</strong></span></div>
      </div>
      <div class="zz-engagement-card"><div id="supabase-comments-{config.slug}-{suffix}" data-zz-supabase-comments></div><p class="zz-engagement-status" data-zz-engagement-status>{status}</p></div>
    </div>
  </section>"""


STORY_CSS = """
    :root {
      --paper:#f6f9fb; --surface:#ffffff; --ink:#20242b; --muted:#667085; --line:#d8e2ea;
      --accent:#0b67c2; --soft:#edf3f7;
    }
    * { box-sizing: border-box; }
    body { margin:0; background:linear-gradient(180deg,var(--soft),var(--paper) 330px); color:var(--ink); font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif; line-height:1.78; letter-spacing:0; }
    a { color:inherit; text-underline-offset:4px; }
    .story-nav { max-width:960px; margin:0 auto; padding:18px 22px 0; display:flex; gap:14px; justify-content:space-between; flex-wrap:wrap; color:var(--muted); font-size:14px; font-weight:750; }
    .story-nav a { text-decoration:none; border-bottom:1px solid transparent; }
    .story-nav a:hover { border-color:currentColor; }
    .page-header { max-width:960px; margin:0 auto; padding:42px 22px 28px; }
    .kicker { margin:0 0 14px; color:var(--accent); font-size:14px; font-weight:900; letter-spacing:.08em; text-transform:uppercase; }
    h1 { margin:0; max-width:850px; color:#111827; font-size:clamp(30px,5vw,58px); line-height:1.08; letter-spacing:0; font-weight:900; }
    .meta { display:flex; flex-wrap:wrap; gap:10px; margin-top:18px; color:var(--muted); font-size:14px; }
    .meta span,.meta a { display:inline-flex; align-items:center; min-height:30px; padding:3px 10px; border:1px solid var(--line); border-radius:999px; background:rgba(255,255,255,.74); color:var(--muted); text-decoration:none; }
    .dek { margin:22px 0 0; padding-left:16px; border-left:4px solid var(--accent); color:#344054; font-size:16px; max-width:760px; }
    .cover { width:100%; max-width:900px; margin:28px 0 0; display:block; border-radius:8px; border:1px solid var(--line); box-shadow:0 22px 56px rgba(15,23,42,.12); background:#e8edf1; }
    .article-shell { background:var(--surface); border-top:1px solid var(--line); border-bottom:1px solid var(--line); box-shadow:0 24px 60px rgba(15,23,42,.06); }
    .article-body { max-width:780px; margin:0 auto; padding:44px 22px 56px; overflow-wrap:anywhere; }
    .article-body h2 { margin:38px 0 16px; color:#111827; font-size:28px; line-height:1.25; font-weight:900; }
    .article-body h3 { margin:32px 0 12px; color:var(--accent); font-size:18px; letter-spacing:.08em; font-weight:900; }
    .article-body p { margin:0 0 17px; font-size:17px; line-height:1.86; }
    .section-label { color:var(--accent); letter-spacing:.08em; text-transform:uppercase; }
    .place { color:#334155; font-weight:850; }
    .credit-line,.end-mark { text-align:center; color:var(--muted); font-weight:850; }
    figure { margin:28px 0 30px; }
    figure img { display:block; width:100%; max-width:100%; height:auto; border-radius:8px; background:#e8edf1; box-shadow:0 16px 40px rgba(15,23,42,.12); }
    figcaption,.caption-line { margin-top:9px; color:#7a828c; font-size:13px; line-height:1.55; text-align:center; }
    .page-footer { max-width:960px; margin:0 auto; padding:22px 22px 48px; color:var(--muted); font-size:13px; }
    @media (max-width:640px) {
      .story-nav { justify-content:flex-start; }
      .page-header { padding:30px 18px 22px; }
      .article-body { padding:34px 18px 44px; }
      .article-body p { font-size:16px; }
      figure { margin-left:-2px; margin-right:-2px; }
    }
"""


FB_CSS = """
    :root { --red:#cc2424; --ink:#111111; --muted:#666666; --line:#d9d9d9; --soft:#f4f4f4; --paper:#ffffff; }
    * { box-sizing:border-box; }
    body { margin:0; background:var(--paper); color:var(--ink); font-family:Arial,Helvetica,sans-serif; line-height:1.62; letter-spacing:0; }
    a { color:inherit; text-decoration-thickness:1px; text-underline-offset:3px; }
    img { max-width:100%; height:auto; }
    .breaking { background:var(--red); color:#fff; font-size:13px; font-weight:900; letter-spacing:.08em; text-transform:uppercase; }
    .breaking-inner { width:min(1180px,calc(100% - 32px)); margin:0 auto; min-height:38px; display:flex; align-items:center; justify-content:space-between; gap:18px; flex-wrap:wrap; }
    .breaking a { color:#fff; text-decoration:none; }
    .site-head { border-bottom:1px solid var(--line); background:#fff; }
    .site-head-inner { width:min(1180px,calc(100% - 32px)); margin:0 auto; min-height:68px; display:flex; align-items:center; justify-content:space-between; gap:18px; flex-wrap:wrap; }
    .wordmark { color:var(--red); font-size:30px; line-height:1; font-weight:950; letter-spacing:0; }
    .section-nav { display:flex; flex-wrap:wrap; justify-content:flex-end; gap:14px; color:#333; font-size:13px; font-weight:800; text-transform:uppercase; }
    .section-nav a { text-decoration:none; }
    .article { width:min(1180px,calc(100% - 32px)); margin:0 auto; }
    .hero { padding:34px 0 26px; border-bottom:1px solid var(--line); }
    .label { display:inline-flex; align-items:center; min-height:28px; padding:4px 9px; background:var(--red); color:#fff; font-size:12px; font-weight:900; letter-spacing:.08em; text-transform:uppercase; }
    h1 { max-width:980px; margin:18px 0 14px; font-size:clamp(2.35rem,7vw,5.3rem); line-height:.96; letter-spacing:0; }
    .dek { max-width:850px; margin:0; color:#333; font-size:clamp(1.05rem,2vw,1.32rem); line-height:1.55; }
    .byline { display:flex; flex-wrap:wrap; gap:8px; margin-top:18px; color:var(--muted); font-size:13px; font-weight:800; text-transform:uppercase; }
    .byline span,.byline a { min-height:30px; display:inline-flex; align-items:center; padding:4px 9px; background:var(--soft); text-decoration:none; }
    .lead-media { margin:26px 0 0; border-top:6px solid var(--red); }
    .lead-media img { display:block; width:100%; aspect-ratio:1200/630; object-fit:cover; background:var(--soft); }
    figcaption { margin-top:8px; color:var(--muted); font-size:12px; line-height:1.4; }
    .story-grid { display:grid; grid-template-columns:minmax(220px,300px) minmax(0,720px); gap:34px; align-items:start; padding:34px 0 12px; }
    .rail { position:sticky; top:16px; display:grid; gap:18px; }
    .brief-box { border-top:5px solid var(--red); background:var(--soft); padding:16px; }
    .brief-box h2 { margin:0 0 12px; font-size:19px; line-height:1.1; }
    .brief-box dl { margin:0; display:grid; gap:12px; }
    .brief-box dt { color:var(--red); font-size:11px; font-weight:900; letter-spacing:.08em; text-transform:uppercase; }
    .brief-box dd { margin:2px 0 0; color:#222; font-size:14px; line-height:1.45; }
    .story-body { min-width:0; }
    .story-body p { margin:0 0 18px; font-size:18px; line-height:1.75; }
    .story-body h2 { margin:36px 0 14px; font-size:30px; line-height:1.18; }
    .story-body h3 { margin:30px 0 10px; color:var(--red); font-size:18px; letter-spacing:.08em; }
    .story-body figure { margin:28px 0 30px; }
    .story-body figure img { display:block; width:100%; height:auto; border-radius:0; box-shadow:none; background:var(--soft); }
    .story-body figcaption,.caption-line { margin-top:8px; color:var(--muted); font-size:13px; text-align:center; }
    .end-mark,.credit-line { text-align:center; color:var(--muted); font-weight:800; }
    @media (max-width:900px){ .story-grid{grid-template-columns:1fr;} .rail{position:static; order:2;} }
    @media (max-width:620px){ .site-head-inner{align-items:flex-start;} .story-body p{font-size:17px;} }
"""


def render_page(config: StoryConfig, article: str, lang: str) -> str:
    is_zh = lang == "zh"
    title = config.title_zh if is_zh else config.title_en
    deck = config.deck_zh if is_zh else config.deck_en
    nav = (
        f'<a href="./index.html">← {"中文故事" if is_zh else "English Stories"}</a>'
        f'<a href="../{"english" if is_zh else "chinese"}/{config.slug}.html">{"English" if is_zh else "中文"}</a>'
        f'<a href="../../facebook/{config.slug}.html">Facebook</a><a href="../../index.html">Run50</a>'
    )
    hero_image = f"cover-medal-{config.slug}.jpg" if is_zh else f"og-run50-{config.slug}-icons.png"
    og = f"{SITE}/assets/{hero_image}"
    accent = config.badge_color
    soft = "#faf2ee" if config.card_class == "run-cn" else ("#f1f6f2" if config.card_class == "run-world" else "#edf3f7")
    return f"""<!doctype html>
<html lang="{'zh-CN' if is_zh else 'en'}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)}</title>
  <meta name="description" content="{escape(deck)}">
  <link rel="canonical" href="{SITE}/run50/stories/{'chinese' if is_zh else 'english'}/{config.slug}.html">
  <meta property="og:title" content="{escape(title)}">
  <meta property="og:description" content="{escape(deck)}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="{SITE}/run50/stories/{'chinese' if is_zh else 'english'}/{config.slug}.html">
  <meta property="og:site_name" content="ArsenanZZ">
  <meta property="og:image" content="{og}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:image" content="{og}">
  <link rel="stylesheet" href="../../../assets/zz-engagement.css?v={ENGAGEMENT_VERSION}">
  <style>{STORY_CSS}
    :root {{ --accent:{accent}; --soft:{soft}; }}
  </style>
</head>
<body>
  <nav class="story-nav" aria-label="Page navigation">{nav}</nav>
  <header class="page-header">
    <p class="kicker">{escape(config.series)} · {escape(config.location_zh if is_zh else config.location_en)}</p>
    <h1>{escape(title)}</h1>
    <div class="meta"><span>Arsenan</span><span>{escape(config.date_zh if is_zh else config.date_en)}</span><span>{escape(config.channel)}</span></div>
    <p class="dek">{escape(deck)}</p>
    <img class="cover" src="../../../assets/{hero_image}?v={VERSION}" alt="{escape(title)} cover" loading="eager" decoding="async">
  </header>
  <main class="article-shell"><article class="article-body">
      {article}
    </article></main>
  {engagement(config, lang)}
  <footer class="page-footer">© ArsenanZZ · Run50</footer>
  <script src="../../../assets/zz-engagement-config.js?v={ENGAGEMENT_VERSION}"></script>
  <script src="../../../assets/zz-engagement.js?v={ENGAGEMENT_VERSION}"></script>
</body>
</html>
"""


def render_facebook_page(config: StoryConfig, article: str) -> str:
    og = f"{SITE}/assets/og-run50-{config.slug}-icons.png"
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(config.title_fb)} | Run50</title>
  <meta name="description" content="{escape(config.deck_en)}">
  <link rel="canonical" href="{SITE}/run50/facebook/{config.slug}.html">
  <meta property="og:title" content="{escape(config.title_fb)}">
  <meta property="og:description" content="{escape(config.deck_en)}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="{SITE}/run50/facebook/{config.slug}.html">
  <meta property="og:site_name" content="ArsenanZZ">
  <meta property="og:image" content="{og}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:image" content="{og}">
  <link rel="stylesheet" href="../../assets/zz-engagement.css?v={ENGAGEMENT_VERSION}">
  <style>{FB_CSS}
    :root {{ --red:{config.badge_color}; }}
  </style>
</head>
<body>
  <div class="breaking"><div class="breaking-inner"><span>{escape(config.channel)} / Longform</span><a href="../stories/chinese/{config.slug}.html">中文原文</a></div></div>
  <header class="site-head"><div class="site-head-inner"><div class="wordmark">Run50</div><nav class="section-nav"><a href="./index.html">Facebook Stories</a><a href="../stories/english/{config.slug}.html">English</a><a href="../stories/chinese/{config.slug}.html">中文</a><a href="../index.html">Run50</a></nav></div></header>
  <main class="article">
    <section class="hero">
      <span class="label">{escape(config.series)}</span>
      <h1>{escape(config.title_fb)}</h1>
      <p class="dek">{escape(config.deck_en)}</p>
      <div class="byline"><span>By Arsenan</span><span>{escape(config.location_en)}</span><span>{escape(config.date_en)}</span></div>
      <figure class="lead-media"><img src="../../assets/og-run50-{config.slug}-icons.png?v={VERSION}" alt="{escape(config.title_fb)} cover"><figcaption>{escape(config.location_en)} · {escape(config.channel)}</figcaption></figure>
    </section>
    <section class="story-grid">
      <aside class="rail">
        <div class="brief-box"><h2>Story Brief</h2><dl><div><dt>Place</dt><dd>{escape(config.location_en)}</dd></div><div><dt>Series</dt><dd>{escape(config.series)}</dd></div><div><dt>Route Memory</dt><dd>{escape(config.cover_subtitle.title())}</dd></div></dl></div>
      </aside>
      <article class="story-body">
        <p class="place"><strong>{escape(config.location_en)}.</strong> {escape(config.deck_en)}</p>
        {article}
      </article>
    </section>
  </main>
  {engagement(config, "en", fb=True)}
  <script src="../../assets/zz-engagement-config.js?v={ENGAGEMENT_VERSION}"></script>
  <script src="../../assets/zz-engagement.js?v={ENGAGEMENT_VERSION}"></script>
</body>
</html>
"""


def render_redirect_page(title: str, target: str) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta http-equiv="refresh" content="0; url={escape(target)}">
  <link rel="canonical" href="{escape(target)}">
  <title>{escape(title)}</title>
  <style>
    body {{ margin:0; min-height:100vh; display:grid; place-items:center; font-family:Arial, Helvetica, sans-serif; background:#edf3f7; color:#20242b; }}
    main {{ width:min(560px, calc(100% - 40px)); }}
    a {{ color:#0b67c2; font-weight:800; }}
  </style>
</head>
<body>
  <main>
    <h1>{escape(title)}</h1>
    <p>This story has been merged into the full Florida Disney Marathon page.</p>
    <p><a href="{escape(target)}">Open the merged story</a></p>
  </main>
  <script>location.replace({json.dumps(target)});</script>
</body>
</html>
"""


def write_deprecated_redirects() -> None:
    for old_slug, target_slug in DEPRECATED_REDIRECTS.items():
        targets = [
            (REPO / "run50" / "stories" / "chinese" / f"{old_slug}.html", f"./{target_slug}.html"),
            (REPO / "run50" / "stories" / "english" / f"{old_slug}.html", f"./{target_slug}.html"),
            (REPO / "run50" / "facebook" / f"{old_slug}.html", f"./{target_slug}.html"),
        ]
        for path, target in targets:
            path.write_text(render_redirect_page("Story merged", target), encoding="utf-8", newline="\n")


def rounded_rectangle(draw: ImageDraw.ImageDraw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def draw_story_icon(draw: ImageDraw.ImageDraw, config: StoryConfig, cx: int, cy: int, scale: float = 1.0) -> None:
    s = scale
    ink = "#20242b"
    fill = "#ffffff"
    accent = config.badge_color

    def line(points, color=ink, width=5):
        draw.line([(int(x), int(y)) for x, y in points], fill=color, width=max(2, int(width * s)), joint="curve")

    def rect(box, color=fill, outline=ink, width=4):
        draw.rounded_rectangle(tuple(int(v) for v in box), radius=int(6 * s), fill=color, outline=outline, width=max(2, int(width * s)))

    def castle():
        rect((cx - 92 * s, cy - 42 * s, cx + 92 * s, cy + 48 * s))
        for dx, h in [(-66, 74), (0, 104), (66, 74)]:
            x = cx + dx * s
            rect((x - 22 * s, cy - h * s, x + 22 * s, cy + 48 * s))
            draw.polygon([(x - 27 * s, cy - h * s), (x, cy - (h + 32) * s), (x + 27 * s, cy - h * s)], fill=accent, outline=ink)
        draw.arc((cx - 28 * s, cy + 4 * s, cx + 28 * s, cy + 78 * s), 180, 360, fill=ink, width=max(3, int(5 * s)))

    def lighthouse():
        draw.polygon([(cx - 28 * s, cy + 58 * s), (cx + 28 * s, cy + 58 * s), (cx + 18 * s, cy - 74 * s), (cx - 18 * s, cy - 74 * s)], fill=fill, outline=ink)
        draw.rectangle((cx - 32 * s, cy - 98 * s, cx + 32 * s, cy - 74 * s), fill=accent, outline=ink, width=max(2, int(4 * s)))
        for yy in [-42, -6, 30]:
            line([(cx - 20 * s, cy + yy * s), (cx + 20 * s, cy + yy * s)], accent, 4)
        line([(cx - 76 * s, cy - 82 * s), (cx - 34 * s, cy - 70 * s)], "#ffffff", 4)
        line([(cx + 34 * s, cy - 70 * s), (cx + 76 * s, cy - 82 * s)], "#ffffff", 4)

    def tower():
        draw.polygon([(cx - 28 * s, cy + 62 * s), (cx + 28 * s, cy + 62 * s), (cx + 12 * s, cy - 112 * s), (cx - 12 * s, cy - 112 * s)], fill=fill, outline=ink)
        draw.ellipse((cx - 46 * s, cy - 12 * s, cx + 46 * s, cy + 40 * s), fill=accent, outline=ink, width=max(2, int(4 * s)))
        draw.ellipse((cx - 36 * s, cy - 90 * s, cx + 36 * s, cy - 44 * s), fill=accent, outline=ink, width=max(2, int(4 * s)))
        line([(cx - 86 * s, cy + 62 * s), (cx + 86 * s, cy + 62 * s)], ink, 5)

    def bridge():
        line([(cx - 105 * s, cy + 42 * s), (cx + 105 * s, cy + 42 * s)], ink, 6)
        draw.arc((cx - 96 * s, cy - 38 * s, cx + 96 * s, cy + 94 * s), 200, 340, fill=accent, width=max(3, int(8 * s)))
        for dx in [-66, -28, 28, 66]:
            line([(cx + dx * s, cy + 42 * s), (cx + dx * s, cy - 4 * s)], ink, 3)

    def palm():
        line([(cx - 10 * s, cy + 64 * s), (cx + 18 * s, cy - 46 * s)], ink, 7)
        for angle, dx, dy in [(0, 76, -76), (1, -72, -72), (2, 52, -112), (3, -46, -112), (4, 10, -124)]:
            line([(cx + 18 * s, cy - 46 * s), (cx + dx * s, cy + dy * s)], accent if angle % 2 else fill, 10)
        draw.ellipse((cx - 96 * s, cy - 104 * s, cx - 42 * s, cy - 50 * s), fill="#fbbf24", outline=ink, width=max(2, int(3 * s)))

    def temple():
        draw.polygon([(cx - 88 * s, cy - 8 * s), (cx, cy - 100 * s), (cx + 88 * s, cy - 8 * s)], fill=accent, outline=ink)
        rect((cx - 70 * s, cy - 8 * s, cx + 70 * s, cy + 62 * s))
        for dx in [-42, 0, 42]:
            rect((cx + dx * s - 12 * s, cy + 8 * s, cx + dx * s + 12 * s, cy + 62 * s), "#f8fafc", ink, 3)

    def snowflake():
        for a in range(0, 180, 30):
            import math
            rad = math.radians(a)
            dx = 82 * s * math.cos(rad)
            dy = 82 * s * math.sin(rad)
            line([(cx - dx, cy - dy), (cx + dx, cy + dy)], accent, 5)
        draw.ellipse((cx - 22 * s, cy - 22 * s, cx + 22 * s, cy + 22 * s), fill=fill, outline=ink, width=max(2, int(4 * s)))

    def football():
        draw.ellipse((cx - 94 * s, cy - 54 * s, cx + 94 * s, cy + 54 * s), fill=fill, outline=ink, width=max(2, int(5 * s)))
        line([(cx - 48 * s, cy), (cx + 48 * s, cy)], accent, 5)
        for dx in [-24, 0, 24]:
            line([(cx + dx * s, cy - 18 * s), (cx + dx * s, cy + 18 * s)], ink, 3)

    def pagoda():
        for i, width in enumerate([118, 92, 66]):
            y = cy + (i * 40 - 70) * s
            draw.polygon([(cx - width * s / 2, y), (cx + width * s / 2, y), (cx + (width - 22) * s / 2, y + 24 * s), (cx - (width - 22) * s / 2, y + 24 * s)], fill=accent if i == 0 else fill, outline=ink)
        line([(cx, cy - 108 * s), (cx, cy + 62 * s)], ink, 4)

    slug = config.slug
    if "disney" in slug or "orlando" in slug:
        castle()
    elif "key-west" in slug or "haikou" in slug:
        palm()
    elif "shanghai" in slug:
        tower()
    elif "north-carolina" in slug or "dalian" in slug:
        lighthouse()
    elif "bangkok" in slug:
        temple()
    elif "harbin" in slug:
        snowflake()
    elif "steel" in slug:
        football()
    elif "wuhan" in slug or "lanzhou" in slug:
        bridge()
    elif "xiamen" in slug or "west-lake" in slug:
        pagoda()
    else:
        bridge()


def draw_cover_png(config: StoryConfig) -> None:
    w, h = 1200, 630
    bg, primary, secondary, accent = config.palette
    image = Image.new("RGB", (w, h), bg)
    draw = ImageDraw.Draw(image)
    for y in range(h):
        blend = y / h
        r = int(int(bg[1:3], 16) * (1 - blend) + 255 * blend)
        g = int(int(bg[3:5], 16) * (1 - blend) + 250 * blend)
        b = int(int(bg[5:7], 16) * (1 - blend) + 235 * blend)
        draw.line([(0, y), (w, y)], fill=(r, g, b))
    draw.rectangle((0, 420, w, h), fill=primary)
    draw.arc((-80, 280, 460, 720), 190, 350, fill=secondary, width=22)
    draw.arc((760, 260, 1280, 730), 200, 345, fill=secondary, width=18)
    for i, x in enumerate(range(90, 1110, 135)):
        top = 290 - (i % 4) * 28
        draw.polygon([(x, 420), (x + 48, top), (x + 96, 420)], fill=secondary)
    draw_story_icon(draw, config, 610, 360, 0.9)
    route = [(120, 500), (250, 455), (380, 510), (520, 458), (680, 500), (840, 450), (1030, 500)]
    draw.line(route, fill=accent, width=12, joint="curve")
    for point in route[::2]:
        draw.ellipse((point[0] - 9, point[1] - 9, point[0] + 9, point[1] + 9), fill="#ffffff", outline=accent, width=4)
    draw.rectangle((820, 374, 968, 468), fill="#ffffff", outline="#20242b", width=5)
    for row in range(2):
        for col in range(4):
            if (row + col) % 2:
                draw.rectangle((824 + col * 35, 378 + row * 42, 859 + col * 35, 420 + row * 42), fill="#20242b")
    title_font = fit_font(draw, config.cover_title, 650, 66, 42, True)
    draw.text((64, 64), config.cover_title, font=title_font, fill="#20242b")
    sub_font = fit_font(draw, config.cover_subtitle, 640, 26, 18, True)
    draw.text((66, 136), config.cover_subtitle, font=sub_font, fill="#667085")
    rounded_rectangle(draw, (760, 64, 1122, 228), 22, "#ffffff", "#20242b", 7)
    draw.text((790, 112), config.series, font=fit_font(draw, config.series, 300, 40, 28, True), fill="#20242b")
    draw.text((790, 166), config.badge_text, font=fit_font(draw, config.badge_text, 302, 50, 26, True), fill=config.badge_color)
    image.save(REPO / "assets" / f"og-run50-{config.slug}-icons.png")


def draw_medal_jpg(config: StoryConfig) -> None:
    w, h = 1200, 750
    bg, primary, secondary, accent = config.palette
    image = Image.new("RGB", (w, h), "#f8fafc")
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((32, 32, w - 32, h - 32), radius=44, fill=bg, outline="#c8ced8", width=18)
    draw.rounded_rectangle((64, 64, w - 64, h - 64), radius=30, fill=bg, outline="#f8fafc", width=8)
    draw.rectangle((84, 520, w - 84, 655), fill="#10243f")
    for i, x in enumerate(range(130, 1050, 120)):
        top = 350 - (i % 5) * 22
        draw.polygon([(x, 520), (x + 55, top), (x + 110, 520)], fill=secondary)
    draw_story_icon(draw, config, 610, 430, 0.95)
    draw.line([(130, 570), (280, 505), (440, 552), (600, 500), (760, 558), (930, 500), (1060, 550)], fill=accent, width=13)
    draw.rectangle((892, 420, 1045, 518), fill="#ffffff", outline="#20242b", width=5)
    for row in range(2):
        for col in range(4):
            if (row + col) % 2:
                draw.rectangle((897 + col * 36, 425 + row * 43, 933 + col * 36, 468 + row * 43), fill="#20242b")
    draw.text((100, 100), config.badge_text, font=fit_font(draw, config.badge_text, 650, 84, 44, True), fill="#20242b")
    draw.text((104, 184), config.cover_subtitle, font=fit_font(draw, config.cover_subtitle, 720, 32, 20, True), fill="#667085")
    draw.text((110, 552), config.cover_title, font=fit_font(draw, config.cover_title, 760, 76, 40, True), fill="#ffffff")
    draw.text((940, 618), config.series.upper(), font=fit_font(draw, config.series.upper(), 180, 24, 16, True), fill="#ffffff")
    image.save(REPO / "assets" / f"cover-medal-{config.slug}.jpg", "JPEG", quality=92)


def svg_motif(config: StoryConfig) -> str:
    ink = "#20242b"
    accent = config.badge_color
    slug = config.slug
    if "disney" in slug or "orlando" in slug:
        return f'''  <g transform="translate(600 424)" stroke="{ink}" stroke-width="7" stroke-linejoin="round">
    <rect x="-92" y="-30" width="184" height="94" rx="8" fill="#fff"/>
    <rect x="-76" y="-86" width="40" height="150" rx="6" fill="#fff"/>
    <rect x="-20" y="-120" width="40" height="184" rx="6" fill="#fff"/>
    <rect x="36" y="-86" width="40" height="150" rx="6" fill="#fff"/>
    <path d="M-82 -86 L-56 -122 L-30 -86 M-26 -120 L0 -158 L26 -120 M30 -86 L56 -122 L82 -86" fill="{accent}"/>
  </g>'''
    if "key-west" in slug or "haikou" in slug:
        return f'''  <g transform="translate(600 420)" stroke="{ink}" stroke-width="8" stroke-linecap="round">
    <circle cx="-76" cy="-70" r="28" fill="#fbbf24"/>
    <path d="M-6 70 C8 18 16 -30 26 -78" fill="none"/>
    <path d="M26 -78 C76 -122 104 -112 122 -100 M26 -78 C-28 -124 -64 -116 -92 -100 M26 -78 C54 -154 86 -154 112 -144 M26 -78 C-8 -156 -44 -156 -78 -144" stroke="{accent}" stroke-width="13"/>
  </g>'''
    if "shanghai" in slug:
        return f'''  <g transform="translate(600 420)" stroke="{ink}" stroke-width="7" stroke-linejoin="round">
    <path d="M-26 78 L26 78 L12 -126 L-12 -126 Z" fill="#fff"/>
    <ellipse cx="0" cy="-58" rx="46" ry="24" fill="{accent}"/>
    <ellipse cx="0" cy="22" rx="56" ry="28" fill="{accent}"/>
    <path d="M-104 78 H104" fill="none"/>
  </g>'''
    if "north-carolina" in slug or "dalian" in slug:
        return f'''  <g transform="translate(600 420)" stroke="{ink}" stroke-width="7" stroke-linejoin="round">
    <path d="M-30 80 H30 L18 -92 H-18 Z" fill="#fff"/>
    <rect x="-36" y="-122" width="72" height="30" fill="{accent}"/>
    <path d="M-76 -100 L-38 -86 M38 -86 L76 -100" stroke="#fff"/>
    <path d="M-22 -44 H22 M-22 -2 H22 M-22 40 H22" stroke="{accent}"/>
  </g>'''
    if "bangkok" in slug or "xiamen" in slug or "west-lake" in slug:
        return f'''  <g transform="translate(600 428)" stroke="{ink}" stroke-width="7" stroke-linejoin="round">
    <path d="M-94 -8 L0 -112 L94 -8 Z" fill="{accent}"/>
    <rect x="-76" y="-8" width="152" height="82" rx="8" fill="#fff"/>
    <path d="M-44 74 V20 M0 74 V20 M44 74 V20"/>
  </g>'''
    if "harbin" in slug:
        return f'''  <g transform="translate(600 420)" stroke="{accent}" stroke-width="8" stroke-linecap="round">
    <path d="M-92 0 H92 M-66 -66 L66 66 M-66 66 L66 -66 M0 -92 V92"/>
    <circle cx="0" cy="0" r="24" fill="#fff" stroke="{ink}"/>
  </g>'''
    if "steel" in slug:
        return f'''  <g transform="translate(600 420)" stroke="{ink}" stroke-width="7">
    <ellipse cx="0" cy="0" rx="102" ry="58" fill="#fff"/>
    <path d="M-52 0 H52" stroke="{accent}" stroke-width="9"/>
    <path d="M-28 -20 V20 M0 -22 V22 M28 -20 V20"/>
  </g>'''
    return f'''  <g transform="translate(600 428)" stroke="{ink}" stroke-width="7" stroke-linecap="round">
    <path d="M-110 54 H110" fill="none"/>
    <path d="M-96 54 C-52 -58 52 -58 96 54" fill="none" stroke="{accent}" stroke-width="12"/>
    <path d="M-60 54 V0 M-24 54 V-24 M24 54 V-24 M60 54 V0" fill="none"/>
  </g>'''


def svg_cover(config: StoryConfig) -> str:
    bg, primary, secondary, accent = config.palette
    title_size = 66 if len(config.cover_title) <= 12 else 54
    badge_size = 52 if len(config.badge_text) <= 10 else 38
    motif_text = " · ".join(config.motifs[:3]).upper()
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 750" role="img" aria-label="{escape(config.title_en)} cover">
  <rect width="1200" height="750" fill="{bg}"/>
  <path d="M0 552 C180 500 255 590 420 535 S740 490 930 552 S1120 585 1200 540 L1200 750 L0 750 Z" fill="{primary}" opacity=".92"/>
  <path d="M116 580 C250 510 360 612 500 548 S790 502 1018 578" fill="none" stroke="{accent}" stroke-width="16" stroke-linecap="round"/>
  <g opacity=".86" fill="{secondary}">
    <polygon points="120,552 210,378 300,552"/>
    <polygon points="260,552 360,324 462,552"/>
    <polygon points="440,552 548,355 658,552"/>
    <polygon points="645,552 760,318 890,552"/>
    <polygon points="835,552 950,382 1070,552"/>
  </g>
{svg_motif(config)}
  <g transform="translate(884 432)">
    <rect width="162" height="102" fill="#fff" stroke="#20242b" stroke-width="6"/>
    <rect x="6" y="6" width="38" height="44" fill="#20242b"/>
    <rect x="82" y="6" width="38" height="44" fill="#20242b"/>
    <rect x="44" y="50" width="38" height="44" fill="#20242b"/>
    <rect x="120" y="50" width="36" height="44" fill="#20242b"/>
  </g>
  <text x="70" y="104" font-family="Arial, Helvetica, sans-serif" font-size="{title_size}" font-weight="900" fill="#20242b">{escape(config.cover_title)}</text>
  <text x="72" y="150" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="800" fill="#667085">{escape(config.cover_subtitle)}</text>
  <rect x="758" y="62" width="364" height="166" rx="22" fill="#ffffff" stroke="#20242b" stroke-width="8"/>
  <text x="790" y="122" font-family="Arial, Helvetica, sans-serif" font-size="41" font-weight="900" fill="#20242b">{escape(config.series)}</text>
  <text x="790" y="182" font-family="Arial, Helvetica, sans-serif" font-size="{badge_size}" font-weight="900" fill="{config.badge_color}">{escape(config.badge_text)}</text>
  <text x="82" y="690" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="900" fill="#fff">{escape(motif_text)}</text>
</svg>
'''


def write_covers(config: StoryConfig) -> None:
    assets = REPO / "assets"
    (assets / "facebook").mkdir(parents=True, exist_ok=True)
    draw_cover_png(config)
    medal_path = assets / f"cover-medal-{config.slug}.jpg"
    if config.slug not in PRESERVE_MEDAL_COVER_SLUGS or not medal_path.exists():
        draw_medal_jpg(config)
    svg = svg_cover(config)
    (assets / f"thumb-run50-{config.slug}-icons.svg").write_text(svg, encoding="utf-8", newline="\n")
    (assets / "facebook" / f"thumb-run50-{config.slug}-icons.svg").write_text(svg, encoding="utf-8", newline="\n")


def chinese_card(config: StoryConfig) -> str:
    return f'''        <a class="story-card {config.card_class}" href="./{config.slug}.html">
          <img src="../../../assets/cover-medal-{config.slug}.jpg?v={VERSION}" alt="{escape(config.title_zh)}封面" loading="lazy" decoding="async">
          <div class="story-copy">
            <p class="story-meta">{escape(config.location_zh)} · {escape(config.date_zh)}</p>
            <h2 class="story-title">{escape(config.title_zh)}</h2>
            <p class="story-desc">{escape(config.card_desc_zh)}</p>
            <div class="story-foot"><span>长文图记</span><span>阅读 →</span></div>
          </div>
        </a>'''


def english_card(config: StoryConfig) -> str:
    return f'''        <a class="story-card {config.card_class}" href="./{config.slug}.html">
          <img src="../../../assets/thumb-run50-{config.slug}-icons.svg?v={VERSION}" alt="Icon cover for {escape(config.title_en)}" />
          <div class="story-card-content">
            <div class="meta">{escape(config.location_en)} · {escape(config.date_en)}</div>
            <h2>{escape(config.title_en)}</h2>
            <p>{escape(config.card_desc_en)}</p>
          </div>
        </a>'''


def facebook_card(config: StoryConfig) -> str:
    return f'''        <a class="story-card {config.card_class}" href="./{config.slug}.html">
          <div>
            <p class="eyebrow">{escape(config.channel)} / Longform</p>
            <h2>{escape(config.title_fb)}</h2>
            <p>{escape(config.card_desc_en)}</p>
            <div class="meta"><span>{escape(config.location_en)}</span><span>{escape(config.series)}</span><span>Run50 Facebook</span></div>
          </div>
          <img src="../../assets/facebook/thumb-run50-{config.slug}-icons.svg?v={VERSION}" alt="Icon-style {escape(config.title_en)} cover">
        </a>'''


def marker_block(kind: str, cards_by_channel: dict[str, list[str]]) -> str:
    headings = {
        "zh": {
            "Run50": ("Run50 · 州挑战", "北卡第16州，以及基韦斯特、奥兰多速通和迪士尼马拉松合并后的佛州第15州故事"),
            "RunCN": ("RunCN · 中国马拉松系列", "上海、武汉、哈尔滨、无锡、杭州西湖、大连、兰州和钢铁战车等中国跑旅归类"),
            "RunWorld": ("RunWorld · 世界马拉松系列", "曼谷归入 RunWorld 第3站，美国和中国之外的跑旅故事"),
        },
        "en": {
            "Run50": ("Run50 / State Challenge", "North Carolina State 16 and the merged Florida State 15 story across Key West, Orlando, and Disney Marathon."),
            "RunCN": ("RunCN / China Marathon Series", "Shanghai, Wuhan, Harbin, Wuxi, West Lake, Dalian, Lanzhou, Steel Tank, and other China running stories."),
            "RunWorld": ("RunWorld / Global Marathon Series", "Bangkok is RunWorld stop 3, with running stories beyond the U.S. and China."),
        },
        "fb": {
            "Run50": ("Run50 / State Challenge", "North Carolina State 16 and the merged Florida State 15 story across Key West, Orlando, and Disney Marathon."),
            "RunCN": ("RunCN / China Marathon Series", "Shanghai, Wuhan, Harbin, Wuxi, West Lake, Dalian, Lanzhou, Steel Tank, and other China running stories."),
            "RunWorld": ("RunWorld / Global Marathon Series", "Bangkok is RunWorld stop 3, with running stories beyond the U.S. and China."),
        },
    }
    zone_class = {"Run50": "run-50-zone", "RunCN": "run-cn-zone", "RunWorld": "run-world-zone"}
    parts = [f"    <!-- running-story-web-batch:{kind}:start -->"]
    for channel in ("Run50", "RunCN", "RunWorld"):
        cards = cards_by_channel.get(channel, [])
        if not cards:
            continue
        title, desc = headings[kind][channel]
        parts.append(f'''    <section class="story-section {zone_class[channel]}" id="running-story-web-{kind}-{channel.lower()}">
      <div class="section-head">
        <p class="section-kicker">{escape(title.split(" · ")[0].split(" / ")[0])}</p>
        <h2>{escape(title)}</h2>
        <p>{escape(desc)}</p>
      </div>
      <div class="story-grid" aria-label="{escape(title)}">
{chr(10).join(cards)}
      </div>
    </section>''')
    parts.append(f"    <!-- running-story-web-batch:{kind}:end -->")
    return "\n\n".join(parts)


def replace_marker(html_text: str, kind: str, block: str) -> str:
    pattern = re.compile(rf"\n\s*<!-- running-story-web-batch:{kind}:start -->.*?<!-- running-story-web-batch:{kind}:end -->", re.S)
    html_text = pattern.sub("", html_text)
    return html_text.replace("\n  </main>", "\n" + block + "\n  </main>")


def update_indexes() -> None:
    visible = [s for s in STORIES if s.show_in_indexes]
    grouped_zh: dict[str, list[str]] = {}
    grouped_en: dict[str, list[str]] = {}
    grouped_fb: dict[str, list[str]] = {}
    for story in visible:
        grouped_zh.setdefault(story.channel, []).append(chinese_card(story))
        grouped_en.setdefault(story.channel, []).append(english_card(story))
        grouped_fb.setdefault(story.channel, []).append(facebook_card(story))
    files = [
        (REPO / "run50" / "stories" / "chinese" / "index.html", "zh", grouped_zh),
        (REPO / "run50" / "stories" / "english" / "index.html", "en", grouped_en),
        (REPO / "run50" / "facebook" / "index.html", "fb", grouped_fb),
    ]
    for path, kind, grouped in files:
        text = path.read_text(encoding="utf-8")
        text = replace_marker(text, kind, marker_block(kind, grouped))
        path.write_text(text, encoding="utf-8", newline="\n")


def update_cache_versions() -> None:
    for path in [REPO / "run50" / "index.html", REPO / "run50" / "hub.html", REPO / "index.html"]:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        text = re.sub(r"\?v=2026061[678][A-Za-z0-9._-]*", f"?v={VERSION}", text)
        path.write_text(text, encoding="utf-8", newline="\n")


def update_hub_world_dots() -> None:
    path = REPO / "run50" / "hub.html"
    text = path.read_text(encoding="utf-8")
    pattern = re.compile(r"\n\s*// running-story-web-batch:dots:start.*?// running-story-web-batch:dots:end", re.S)
    text = pattern.sub("", text)
    lines = []
    for story in STORIES:
        if story.map_x is None or story.map_y is None or not story.show_in_indexes:
            continue
        link = f"facebook/{story.slug}.html"
        color = story.map_color or ("cnCol" if story.channel == "RunCN" else ("itCol" if story.channel == "RunWorld" else "'#ff4040'"))
        color_expr = color if color in {"cnCol", "itCol", "mxCol"} else f"'{color}'"
        lines.append(f"   [{story.map_x}, {story.map_y}, {color_expr}, false, '{story.location_en}', '{story.date_en}', '{link}'],")
    block = "\n   // running-story-web-batch:dots:start\n" + "\n".join(lines) + "\n   // running-story-web-batch:dots:end"
    anchor = "   [1507, 294, cnCol,   false, 'Shanghai, China',  '2019',    'stories/chinese/shanghai-vertical-marathon.html'],"
    if anchor in text:
        text = text.replace(anchor, anchor + block)
    path.write_text(text, encoding="utf-8", newline="\n")


def update_sql() -> None:
    path = REPO / "supabase" / "run50-comments.sql"
    text = path.read_text(encoding="utf-8")
    original = text
    for slug in DEPRECATED_REDIRECTS:
        for suffix in ("facebook-en", "en", "zh"):
            key = f"run50-{slug}-{suffix}"
            text = re.sub(rf"\n\s*'{re.escape(key)}',?", "", text)
    keys: list[str] = []
    for story in STORIES:
        keys.extend([
            f"run50-{story.slug}-facebook-en",
            f"run50-{story.slug}-en",
            f"run50-{story.slug}-zh",
        ])
    missing = [key for key in keys if text.count(f"'{key}'") == 0]
    if not missing:
        if text != original:
            path.write_text(text, encoding="utf-8", newline="\n")
        return
    block = "".join(f"      '{key}',\n" for key in missing)
    text = text.replace("      'run50-shanghai-vertical-marathon-facebook-en',", block + "      'run50-shanghai-vertical-marathon-facebook-en',", 3)
    text = text.replace("    'run50-shanghai-vertical-marathon-facebook-en',", block.replace("      ", "    ") + "    'run50-shanghai-vertical-marathon-facebook-en',", 1)
    for key in missing:
        for indent in ("      ", "    "):
            target = f"{indent}'{key}',\n"
            while text.count(f"'{key}'") > 3 and target in text:
                text = text.replace(target, "", 1)
    path.write_text(text, encoding="utf-8", newline="\n")


def build() -> None:
    for config in STORIES:
        for source_path, source_files in zip(config.source_paths, config.source_files_list):
            if not source_path.exists():
                raise FileNotFoundError(source_path)
            if not source_files.exists():
                raise FileNotFoundError(source_files)
    all_events = [extract_story(story) for story in STORIES]
    for story, events in zip(STORIES, all_events):
        images = sum(1 for e in events if e["type"] == "image")
        texts = sum(1 for e in events if e["type"] == "text")
        print(f"{story.slug}: {texts} text blocks, {images} images")
    cache = ensure_translations(all_events)

    for story, events in zip(STORIES, all_events):
        count = copy_story_images(story, events)
        print(f"{story.slug}: copied {count} images")
        write_covers(story)
        zh_article = render_events(story, events, "zh", f"{story.image_dir}/", cache)
        en_article = render_events(story, events, "en", f"../chinese/{story.image_dir}/", cache)
        fb_article = render_events(story, events, "en", f"../stories/chinese/{story.image_dir}/", cache)
        (REPO / "run50" / "stories" / "chinese" / f"{story.slug}.html").write_text(render_page(story, zh_article, "zh"), encoding="utf-8", newline="\n")
        (REPO / "run50" / "stories" / "english" / f"{story.slug}.html").write_text(render_page(story, en_article, "en"), encoding="utf-8", newline="\n")
        (REPO / "run50" / "facebook" / f"{story.slug}.html").write_text(render_facebook_page(story, fb_article), encoding="utf-8", newline="\n")

    write_deprecated_redirects()
    update_indexes()
    update_cache_versions()
    update_hub_world_dots()
    update_sql()


if __name__ == "__main__":
    build()
