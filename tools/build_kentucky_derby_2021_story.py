from __future__ import annotations

from dataclasses import dataclass
from html import escape, unescape
from pathlib import Path
import re
import textwrap

from lxml import html
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SOURCE_BASE = Path(r"Z:\ZhennanZ Folder\0-Running Story Web\ADDDDD")
SOURCE_HTML = next(SOURCE_BASE.glob("*传奇跑者*.html"))
SOURCE_ASSETS = next(p for p in SOURCE_BASE.glob("*传奇跑者*") if p.is_dir())

SLUG = "kentucky-derby-marathon-2021"
ASSET_DIR = ROOT / "run50" / "stories" / "chinese" / "Run50-Kentucky-Derby-Marathon-2021-clean_files"
VERSION = "20260703-ky-derby-2021"

ZH_TITLE = "Run50 #第1州｜肯塔基第二篇：Derby 全马｜“传奇跑者”的半年流水账"
EN_TITLE = "Run50 State 1, Kentucky Story 2: Derby Marathon and a half-year journal"
FB_TITLE = "A rainy Derby Marathon, then a city opening back up"
ZH_DESC = "从搬家、Waverly 半马，到 2021 年阴雨大风里的 Kentucky Derby Festival Marathon，再到疫苗、驾照、local running 和重新打开的美国。"
EN_DESC = "Moving, a lonely Waverly half, the rainy 2021 Kentucky Derby Festival Marathon, vaccines, a driver's license, local runs, and an America that slowly opened back up."

PAGE_KEYS = [
    f"run50-{SLUG}-en",
    f"run50-{SLUG}-facebook-en",
    f"run50-{SLUG}-zh",
]


@dataclass
class Block:
    kind: str
    text: str = ""
    src: str = ""
    caption: str = ""


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        Path(r"C:\Windows\Fonts\msyhbd.ttc") if bold else Path(r"C:\Windows\Fonts\msyh.ttc"),
        Path(r"C:\Windows\Fonts\simhei.ttf"),
        Path(r"C:\Windows\Fonts\arialbd.ttf") if bold else Path(r"C:\Windows\Fonts\arial.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default()


def text_width(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.FreeTypeFont) -> int:
    box = draw.textbbox((0, 0), text, font=fnt)
    return box[2] - box[0]


def fit_text(draw: ImageDraw.ImageDraw, text: str, start_size: int, max_width: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    for size in range(start_size, 18, -2):
        fnt = font(size, bold=bold)
        if text_width(draw, text, fnt) <= max_width:
            return fnt
    return font(18, bold=bold)


def draw_cover(path: Path, *, chinese: bool, og: bool = False) -> None:
    w, h = (1200, 630) if og else (1200, 750)
    img = Image.new("RGB", (w, h), "#edf3f7")
    d = ImageDraw.Draw(img)

    # Background fields.
    d.rectangle([0, 0, w, h], fill="#edf3f7")
    d.polygon([(0, int(h * .54)), (w, int(h * .45)), (w, h), (0, h)], fill="#6fa65d")
    d.polygon([(0, int(h * .62)), (w, int(h * .52)), (w, int(h * .68)), (0, int(h * .78))], fill="#d79a3a")
    d.rectangle([0, int(h * .70), w, h], fill="#1f7a78")
    d.rectangle([0, int(h * .76), w, h], fill="#f4efe5")

    title = "肯塔基" if chinese else "KENTUCKY"
    subtitle = "DERBY 全马 · 2021 · 第二篇" if chinese else "DERBY · 2021 · STORY 2"
    title_font = fit_text(d, title, 70, 620, bold=True)
    subtitle_font = fit_text(d, subtitle, 30, 620, bold=True)
    d.text((64, 58), title, font=title_font, fill="#20242b")
    d.text((66, 138), subtitle, font=subtitle_font, fill="#5f6f76")

    # Fixed Run50 badge.
    bx, by, bw, bh = 760, 64, 362, 164
    d.rounded_rectangle([bx, by, bx + bw, by + bh], radius=22, fill="#ffffff", outline="#20242b", width=7)
    d.text((790, 106), "Run50 #1", font=font(40, bold=True), fill="#20242b")
    badge_text = "STORY 2" if not chinese else "第二篇"
    d.text((790, 162), badge_text, font=fit_text(d, badge_text, 52, 302, bold=True), fill="#0b67c2")

    # Louisville/Derby motifs: bridge, rain, medal, river road.
    base_y = int(h * .58)
    for x in range(95, 1120, 110):
        d.line([(x, base_y + 55), (x + 70, base_y - 24)], fill="#314453", width=8)
        d.line([(x + 70, base_y - 24), (x + 140, base_y + 55)], fill="#314453", width=8)
    d.line([(70, base_y + 55), (1130, base_y + 55)], fill="#314453", width=12)
    d.arc([430, base_y - 30, 775, base_y + 315], 200, 340, fill="#c96e30", width=26)
    d.ellipse([540, base_y + 108, 670, base_y + 238], fill="#f2d88a", outline="#8a5a21", width=12)
    d.ellipse([575, base_y + 145, 635, base_y + 205], fill="#ffffff", outline="#d4b056", width=6)
    d.line([(118, base_y + 185), (420, base_y + 140), (720, base_y + 188), (1084, base_y + 132)], fill="#ffffff", width=16)
    d.line([(118, base_y + 185), (420, base_y + 140), (720, base_y + 188), (1084, base_y + 132)], fill="#0b67c2", width=5)
    for x in range(125, 1110, 85):
        d.line([(x, 240), (x - 14, 278)], fill="#5f8795", width=5)

    # Bottom label for index cards.
    if not og:
        d.rounded_rectangle([265, 598, 935, 695], radius=28, fill="#114f68", outline="#f8e9bd", width=6)
        bottom = "传奇跑者 · DERBY" if chinese else "LEGENDARY RUNNER"
        bottom_font = fit_text(d, bottom, 58, 610, bold=True)
        tw = text_width(d, bottom, bottom_font)
        d.text(((w - tw) / 2, 615), bottom, font=bottom_font, fill="#fff5d6")
        d.rounded_rectangle([58, 620, 230, 696], radius=22, fill="#b96b2c", outline="#f8e9bd", width=5)
        d.text((92, 638), "2021", font=font(34, bold=True), fill="#fff5d6")
        d.rounded_rectangle([970, 620, 1144, 696], radius=22, fill="#0b67c2", outline="#f8e9bd", width=5)
        d.text((1006, 638), "RUN50", font=font(30, bold=True), fill="#fff5d6")

    path.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix.lower() in {".jpg", ".jpeg"}:
        img.save(path, quality=92)
    else:
        img.save(path)


def write_svg_cover() -> None:
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 750" width="1200" height="750">
  <rect width="1200" height="750" fill="#edf3f7"/>
  <path d="M0 392 C250 320 420 340 600 300 C780 260 940 295 1200 235 L1200 750 L0 750Z" fill="#77aa64"/>
  <path d="M0 470 C220 430 395 450 615 410 C835 370 1040 365 1200 330 L1200 540 L0 590Z" fill="#d99637"/>
  <rect y="552" width="1200" height="198" fill="#1f7a78"/>
  <rect y="618" width="1200" height="132" fill="#f4efe5"/>
  <text x="70" y="104" font-family="Arial, Helvetica, sans-serif" font-size="66" font-weight="900" fill="#20242b">LOUISVILLE</text>
  <text x="72" y="150" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="800" fill="#667085">DERBY · RAIN · REOPENING</text>
  <rect x="758" y="62" width="364" height="166" rx="22" fill="#ffffff" stroke="#20242b" stroke-width="8"/>
  <text x="790" y="122" font-family="Arial, Helvetica, sans-serif" font-size="41" font-weight="900" fill="#20242b">Run50 #1</text>
  <text x="790" y="182" font-family="Arial, Helvetica, sans-serif" font-size="48" font-weight="900" fill="#0b67c2">STORY 2</text>
  <g stroke="#314453" stroke-width="9" fill="none">
    <path d="M82 480 L170 388 L258 480 M258 480 L346 388 L434 480 M434 480 L522 388 L610 480 M610 480 L698 388 L786 480 M786 480 L874 388 L962 480 M962 480 L1050 388 L1138 480"/>
    <path d="M72 480 H1140" stroke-width="13"/>
  </g>
  <path d="M124 650 C278 588 410 582 550 626 C710 676 892 610 1088 572" fill="none" stroke="#ffffff" stroke-width="18" stroke-linecap="round"/>
  <path d="M124 650 C278 588 410 582 550 626 C710 676 892 610 1088 572" fill="none" stroke="#0b67c2" stroke-width="6" stroke-linecap="round"/>
  <path d="M450 404 C455 590 720 590 724 404" fill="none" stroke="#c96e30" stroke-width="28" stroke-linecap="round"/>
  <circle cx="588" cy="548" r="70" fill="#f2d88a" stroke="#8a5a21" stroke-width="14"/>
  <circle cx="588" cy="548" r="32" fill="#ffffff" stroke="#d4b056" stroke-width="6"/>
  <g stroke="#5f8795" stroke-width="5">
    <path d="M130 240 l-18 42"/><path d="M218 228 l-18 42"/><path d="M306 236 l-18 42"/><path d="M394 224 l-18 42"/><path d="M482 232 l-18 42"/><path d="M570 220 l-18 42"/><path d="M658 230 l-18 42"/><path d="M746 222 l-18 42"/><path d="M834 238 l-18 42"/><path d="M922 226 l-18 42"/><path d="M1010 234 l-18 42"/>
  </g>
</svg>
"""
    (ROOT / "assets" / f"thumb-run50-{SLUG}-icons.svg").write_text(svg, encoding="utf-8")


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", unescape(s or "")).strip()


def join_parts(parts: list[str]) -> str:
    out = ""
    for part in parts:
        if not out:
            out = part
        elif part.startswith("by "):
            out += " " + part
        elif part in "，。！？；：、）】》" or out.endswith(("（", "《", "“", '"')):
            out += part
        elif re.search(r"[A-Za-z0-9)]$", out) and re.search(r'^[A-Za-z0-9("“]', part):
            out += " " + part
        else:
            out += part
    return out.replace("B road Run Park", "Broad Run Park")


def extract_blocks() -> list[Block]:
    text = SOURCE_HTML.read_text(encoding="utf-8", errors="replace")
    doc = html.fromstring(text)
    root = doc.xpath('//*[contains(concat(" ", normalize-space(@class), " "), " rich_media_content ")]')[0]
    events: list[tuple[str, str]] = []
    img_re = re.compile(r"/([^/]*640(?:\(\d+\))?)$")

    def add_text(value: str | None) -> None:
        value = norm(value or "")
        if value:
            events.append(("text", value))

    for el in root.iter():
        add_text(el.text)
        if isinstance(el.tag, str) and el.tag.lower() == "img":
            src = el.get("src") or el.get("data-src") or ""
            match = img_re.search(src)
            if match:
                events.append(("img", match.group(1)))
        add_text(el.tail)

    start = next(i for i, event in enumerate(events) if event == ("text", "前言"))
    blocks: list[Block] = []
    para: list[str] = []

    def flush() -> None:
        nonlocal para
        if para:
            blocks.append(Block("p", text=join_parts(para)))
            para = []

    i = start
    while i < len(events):
        kind, value = events[i]
        if kind == "img":
            flush()
            cap: list[str] = []
            j = i + 1
            if j < len(events) and events[j] == ("text", "▲"):
                j += 1
            while j < len(events) and events[j][0] == "text":
                cap.append(events[j][1])
                j += 1
                if cap[-1].startswith("by "):
                    break
            blocks.append(Block("figure", src=value, caption=join_parts([c for c in cap if c != "▲"])))
            i = j
            continue
        if kind == "text":
            if value in {"前言", "后记"}:
                flush()
                blocks.append(Block("h2", text=value))
                i += 1
                continue
            if value in {"01", "02", "03"}:
                flush()
                heading = events[i + 1][1] if i + 1 < len(events) and events[i + 1][0] == "text" else ""
                blocks.append(Block("h2", text=f"{value} {heading}"))
                i += 2
                continue
            if value == "- 本文完 -":
                flush()
                blocks.append(Block("end", text=value))
                i += 1
                continue
            if value.startswith(("文字丨", "摄影丨", "设计丨")):
                flush()
                blocks.append(Block("credit", text=value))
                i += 1
                continue
            if value != "▲" and not value.startswith("by "):
                para.append(value)
        i += 1
    flush()
    return blocks


EN = {
    "前言": "Foreword",
    "01 Waverly半马": "01 Waverly Half Marathon",
    "02 Derby全马": "02 Derby Marathon",
    "03 美国也还行，没那么凑活": "03 America Wasn't So Bad After All",
    "后记": "Postscript",
    "- 本文完 -": "- End -",
    "文字丨Arsenan": "Words | Arsenan",
    "摄影丨Arsenan": "Photos | Arsenan",
    "设计丨Arsenan": "Design | Arsenan",
    "在美国呆了一年，感觉挺无聊的，更甭提又赶上疫情弗洛伊德大选寒流，听很多人说，国外就是好山好水好无聊，但我觉得不对，因为这山这水，我也没觉得有多好。": "After a year in the States, I honestly felt pretty bored. Add the pandemic, George Floyd, the election, and the winter storm, and it got even harder to pretend otherwise. A lot of people say life abroad means nice mountains, nice water, and a whole lot of boredom. I did not quite buy that. The mountains and water did not feel that amazing to me either.",
    "2021这半年应该是从搬家开始的，房东是个倔老头，听说很不好对付。和老头交涉了两次，感觉有点像《海蒂和爷爷》里刚出场的老爷子，总之就是很生硬。": "The first half of 2021 probably began with moving. My landlord was a stubborn old man, and people said he was not easy to deal with. After talking to him twice, he reminded me a bit of the grandfather when he first appears in Heidi. In short, very stiff.",
    "搬了新家，也冬眠挺久的了，正好跑个步熟悉熟悉环境，一路沿着街道跑到了downtown，天气阴沉沉的，疫情里的城市也没多少活力，偶尔跑过街边的桥洞，总会被一群流浪汉盯的不寒而栗。": "After moving into the new place and hibernating for a while, I figured I should go for a run and get to know the neighborhood. I followed the streets all the way downtown. The sky was gray, the city had little energy during the pandemic, and every now and then, when I passed under a bridge, a group of unhoused people would stare at me in a way that gave me chills.",
    "没跑多远，累够呛，完全没有巅峰时候的风采，作为传奇跑者，其实我也没那么佛系。": "I did not run far before I was completely worn out. None of my peak-era swagger was left. As a legendary runner, I was apparently not that zen after all.",
    "就这样，我赶紧报名个半马，提醒自己，我可是跑圈传奇，可不能这么油腻。疫情里比赛少的可怜，仅有的几个能跑的都在几十公里外的公园trail，也只能割肉打车了。": "So I quickly signed up for a half marathon, mostly to remind myself that I was, allegedly, a legend in the running world and could not keep getting this out of shape. Races were painfully rare during the pandemic, and the few that were happening were on park trails dozens of kilometers away, so I had to bite the bullet and pay for a ride.",
    "Broad Run Park的小半马，没几个人，因为疫情，大家分开起跑，所以就让这段路显得更加孤单，伴随着一月底的冬雨和冷风，走走跑跑的完赛。": "The little half marathon at Broad Run Park had very few people. Because of COVID, everyone started separately, which made the road feel even lonelier. In the cold rain and wind at the end of January, I half-ran, half-walked my way to the finish.",
    "惊喜也有，公园里的黄色silo，像极了武汉的失落之塔，让人眼前一亮。": "There were surprises too. The yellow silo in the park looked so much like Wuhan's Lost Tower that it instantly caught my eye.",
    "赛后，当我发现自己跑个半马都这么费劲了，这让我认识到问题的严重性，得抓紧时间锻炼身体。": "After the race, realizing that even a half marathon felt this hard made the problem very clear. I needed to get serious about training again.",
    "一晃两个月，Derby来了，肯塔基州最大的马拉松，不过今年因为疫情，分天分时起跑，所以并不热烈。": "Two months went by, and Derby arrived. It is Kentucky's biggest marathon, but this year, because of the pandemic, runners started across different days and time slots, so the atmosphere was not exactly lively.",
    "跑步日，又是个阴天，赛前天气预报说，我注定要被淋成落汤鸡。": "Race day was cloudy again. The forecast had already told me I was destined to get soaked like a drenched chicken.",
    "前三十公里其实还好，雨不大，跑起来还挺舒服，是传奇跑者喜欢的节奏，不过后面十几公里确实艰难，和去年的Louisville全马简直是两个极端，大风吹的我打晃，大雨淋的我打颤。": "The first 30 kilometers were actually fine. The rain was light, and the rhythm felt comfortable, exactly the kind of pace a legendary runner likes. But the final dozen kilometers were genuinely rough, the total opposite of last year's Louisville Marathon. The wind pushed me around, and the heavy rain made me shiver.",
    "温暖也有，旁边的赛道工作人员，一直骑着自行车和救助包跟着我，不时过来问一下\"You good?\"，我会假笑一下然后竖起大拇指，表示OK，这是传奇跑者最后的倔强。": "There was warmth too. A race volunteer rode nearby with a bicycle and a medical bag, checking on me every so often with, \"You good?\" I would force a smile, give a thumbs-up, and signal that I was OK. That was the legendary runner's last bit of stubborn pride.",
    "费了挺大劲，终于回到了终点，雨下得更大了，也没个地躲雨，也不给口热汤，今年的补给确实不太行。": "It took a lot of effort, but I finally made it back to the finish. By then the rain was heavier, there was nowhere to hide from it, and not even a cup of hot soup. The support this year really was not great.",
    "赛后花了40多刀，买了跑步照片，回头去看，虽然狼狈，但至少照片里，我还是挺enjoy的，算是挺有趣的回忆，至少又完成了一场全马，还可以自称是传奇。": "After the race I spent more than forty dollars on race photos. Looking back at them, I looked rough, but at least in the photos I still seemed to be enjoying myself. That made it a pretty funny memory. At the very least, I had finished another marathon and could still call myself a legend.",
    "三四月份扎了两针辉瑞，晕了两天，四月底拿到正式驾照，开车自由。感觉一下子就打开了我的任督二脉，生活一下子精彩了起来。": "In March and April I got two Pfizer shots, felt dizzy for two days, and by the end of April finally got my proper driver's license. Freedom to drive. It felt like some hidden channel in my life suddenly opened, and things became a lot more interesting.",
    "美国，其实也没那么凑活，好像还行。": "America, as it turned out, was not that make-do after all. It seemed kind of okay.",
    "去个几十公里外的公园打卡，放飞机。": "I could check in at parks dozens of kilometers away and fly the drone.",
    "参加各种local的小跑步，再也不用担心丢自行车了。": "I joined all kinds of small local runs and no longer had to worry about losing my bike.",
    "和Cindy一家去Red River Gorge Hiking，吃BBQ看音乐会，家里坐客。": "I went hiking at Red River Gorge with Cindy's family, ate BBQ, watched a concert, and visited their home.",
    "最开心的是，美国正常的大马拉松马上要回来了，确实有点迫不及待。当然作为\"传奇跑者”，还是要先减下去十几斤肉，总有那么一天我这个传奇跑者可以名副其实，不仅仅是调侃。": "The happiest part was that normal big American marathons were about to come back. I really could not wait. Of course, as a \"legendary runner,\" I still had to lose more than ten pounds first. One day, this legendary runner would live up to the name, not just use it as a joke.",
    "今年因为寒流，Louisville的雪下的很大，有点一夜回到东北的感觉。房东老爷子请我帮忙扫雪，简单聊了下，才知道他竟然去过哈尔滨，还show他一直track哈尔滨的天气。": "Because of the cold wave this year, Louisville got a lot of snow. It felt a bit like being transported back to Northeast China overnight. The old landlord asked me to help shovel snow, and after chatting a little, I found out he had actually been to Harbin. He even showed me that he still tracked Harbin's weather.",
    "其实老头也没那么生硬，有时候也挺好玩的。": "The old man was not actually that stiff. Sometimes he was pretty fun.",
    "前几天看朋友晒黄石公园的风景，好像美国这山山水水也没那么不堪。": "A few days ago I saw a friend post photos from Yellowstone, and suddenly America's mountains and water did not seem so bad.",
    "最近健身房的口罩禁令解除，跑步也慢慢开始找到状态，停滞的时间又开始流动起来。": "Recently the gym lifted its mask requirement, and my running slowly started to come back. Time, which had been stuck, began to move again.",
    "2021这半年，看到大地从寒冬走向了盛夏，城市也从lockdown回到了open，街上人也多了起来。": "In the first half of 2021, I watched the world move from deep winter into full summer, and the city move from lockdown back to open. There were more people on the streets again.",
    "好像是又来了一次美国，突然就觉得，城市可以lockdown，但人真不该lockdown，毕竟作为\"传奇跑者”，应该是不断拓展认知边界的。": "It felt like arriving in America all over again. Suddenly I thought: a city can be locked down, but people really should not be. After all, as a \"legendary runner,\" I should be constantly expanding the borders of what I know.",
}

CAPTIONS = {
    "搬家 by Arsenan": "Moving by Arsenan",
    "起跑点 by Arsenan": "Start area by Arsenan",
    "奖牌 by Arsenan": "Medal by Arsenan",
    "起点涂鸦 by Arsenan": "Start-line graffiti by Arsenan",
    "起点 by Arsenan": "Start line by Arsenan",
    "壮胖子 by marathonfoto": "Chubby runner by marathonfoto",
    "壮子 by marathonfoto": "The runner by marathonfoto",
    "雨里摄影师 by Arsenan": "Photographer in the rain by Arsenan",
    "壮子傻笑 by marathonfoto": "Awkward smile by marathonfoto",
    "大雨 by marathonfoto": "Heavy rain by marathonfoto",
    "Derby 奖牌 by Arsenan": "Derby medal by Arsenan",
    "疫苗 by Arsenan": "Vaccine by Arsenan",
    "买了两个专辑(减肥) by Santosh": "Bought two albums (weight loss) by Santosh",
    "Hiking (Zoe&胖子&Santosh&Siqi) by Cindy": "Hiking (Zoe, Pangzi, Santosh and Siqi) by Cindy",
    "国际跑步日奖牌 by Arsenan": "Global Running Day medal by Arsenan",
    "冬天 by Arsenan": "Winter by Arsenan",
    "城市又运转了 by Arsenan": "The city started moving again by Arsenan",
    "春天 by Arsenan": "Spring by Arsenan",
    "夏天 by Arsenan": "Summer by Arsenan",
    "城市夜景 by Arsenan": "City night view by Arsenan",
}


def translate_text(value: str) -> str:
    if value in EN:
        return EN[value]
    if value in CAPTIONS:
        return CAPTIONS[value]
    return value


def copy_images() -> None:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    for i in range(40):
        name = "640" if i == 0 else f"640({i})"
        src = SOURCE_ASSETS / name
        dest = ASSET_DIR / f"img-{i + 1:03d}.webp"
        with Image.open(src) as im:
            im = im.convert("RGB")
            im.save(dest, "WEBP", quality=92)


def src_for(original_name: str, prefix: str) -> str:
    index = 0 if original_name == "640" else int(re.search(r"\((\d+)\)", original_name).group(1))
    return f"{prefix}/img-{index + 1:03d}.webp"


def render_blocks(blocks: list[Block], *, lang: str, img_prefix: str) -> str:
    out: list[str] = []
    for block in blocks:
        if block.kind == "h2":
            out.append(f"<h2>{escape(translate_text(block.text) if lang == 'en' else block.text)}</h2>")
        elif block.kind == "p":
            txt = translate_text(block.text) if lang == "en" else block.text
            out.append(f"<p>{escape(txt)}</p>")
        elif block.kind == "figure":
            cap = translate_text(block.caption) if lang == "en" else block.caption
            src = src_for(block.src, img_prefix)
            out.append(
                f'<figure><img src="{escape(src)}" alt="{escape(cap)}" loading="lazy" decoding="async">'
                f"<figcaption>{escape(cap)}</figcaption></figure>"
            )
        elif block.kind == "end":
            txt = translate_text(block.text) if lang == "en" else block.text
            out.append(f'<p class="end-mark">{escape(txt)}</p>')
        elif block.kind == "credit":
            txt = translate_text(block.text) if lang == "en" else block.text
            out.append(f'<p class="credit-line">{escape(txt)}</p>')
    return "\n      ".join(out)


def split_sections(blocks: list[Block]) -> dict[str, list[Block]]:
    sections: dict[str, list[Block]] = {}
    current = "front"
    for block in blocks:
        if block.kind == "h2":
            current = block.text
            sections[current] = [block]
        else:
            sections.setdefault(current, []).append(block)
    return sections


BASE_CSS = """
    :root { color-scheme: light; --ink:#20242b; --muted:#667085; --paper:#edf3f7; --line:#d0dfe8; --blue:#0b67c2; --gold:#b7791f; }
    * { box-sizing: border-box; }
    body { margin:0; font-family: Inter, "Segoe UI", Arial, "PingFang SC", "Microsoft YaHei", sans-serif; background:#f6f9fb; color:var(--ink); line-height:1.78; letter-spacing:0; }
    a { color:inherit; text-underline-offset:4px; }
    nav { max-width:1080px; margin:0 auto; padding:22px 20px; display:flex; gap:18px; justify-content:flex-end; font-weight:800; color:#526170; flex-wrap:wrap; }
    nav a { text-decoration:none; }
    .hero { background:linear-gradient(180deg,#e7f1f6,#f6f9fb); border-bottom:1px solid var(--line); }
    .hero-inner { max-width:1080px; margin:0 auto; padding:54px 20px 46px; display:grid; grid-template-columns:minmax(0,1.05fr) minmax(300px,.95fr); gap:34px; align-items:center; }
    .kicker { margin:0 0 12px; color:var(--blue); font-size:13px; font-weight:900; letter-spacing:1.6px; text-transform:uppercase; }
    h1 { margin:0; font-size:clamp(34px,5vw,62px); line-height:1.05; letter-spacing:0; }
    .dek { margin:20px 0 0; max-width:690px; color:#526170; font-size:19px; }
    .stats { display:flex; flex-wrap:wrap; gap:10px; margin-top:24px; }
    .stat { border:1px solid var(--line); border-radius:999px; padding:8px 13px; background:#fff; color:#344054; font-weight:800; font-size:13px; }
    .hero-card { overflow:hidden; border-radius:8px; border:1px solid var(--line); background:#fff; box-shadow:0 24px 60px rgba(28,56,80,.14); }
    .hero-card img { display:block; width:100%; height:auto; }
    .article-shell { max-width:850px; margin:0 auto; padding:46px 20px 20px; }
    .article-body { font-size:18px; }
    .article-body h2 { margin:46px 0 18px; padding-top:16px; border-top:1px solid var(--line); color:#16324c; font-size:28px; line-height:1.25; letter-spacing:0; }
    .article-body p { margin:18px 0; }
    figure { margin:28px 0; }
    figure img { display:block; width:100%; height:auto; border-radius:8px; background:#e8eef2; }
    figcaption { margin-top:9px; color:#667085; font-size:13px; text-align:center; }
    .end-mark { text-align:center; color:#8a5b22; font-weight:900; }
    .credit-line { margin:5px 0; color:#667085; font-size:14px; text-align:center; }
    .zz-engagement { margin-top:28px; }
    @media (max-width:760px) { nav { justify-content:flex-start; } .hero-inner { grid-template-columns:1fr; padding-top:34px; } .article-body { font-size:17px; } }
"""


def engagement(locale: str, page_key: str, depth: str) -> str:
    zh = locale == "zh-CN"
    kicker = "留言 / 阅读" if zh else "Comments / Views"
    title = "跑完也说两句" if zh else "Say something after the run"
    note = "不用登录，留下名字就能留言；新留言会直接显示。" if zh else "No account is needed to submit a comment. New comments appear right away."
    views = "阅读" if zh else "Views"
    loading = "评论加载中..." if zh else "Loading comments..."
    return f"""
  <section class="zz-engagement" data-zz-engagement data-locale="{locale}" data-page-key="{page_key}">
    <div class="zz-engagement-shell">
      <div>
        <p class="zz-engagement-kicker">{kicker}</p>
        <h2>{title}</h2>
        <p class="zz-engagement-note">{note}</p>
        <div class="zz-engagement-stats">
          <span class="zz-engagement-stat" id="busuanzi_container_page_pv"><span>{views}</span><strong id="busuanzi_value_page_pv" data-zz-view-count>--</strong></span>
        </div>
      </div>
      <div class="zz-engagement-card">
        <div id="supabase-comments-{SLUG}-{locale.lower().replace('-', '')}" data-zz-supabase-comments></div>
        <p class="zz-engagement-status" data-zz-engagement-status>{loading}</p>
      </div>
    </div>
  </section>
  <script src="{depth}/assets/zz-engagement-config.js?v=20260616"></script>
  <script src="{depth}/assets/zz-engagement.js?v=20260616"></script>"""


def story_page(*, lang: str, title: str, desc: str, body: str, page_key: str, canonical: str, img_depth: str) -> str:
    zh = lang == "zh-CN"
    nav = (
        '<a href="../../../run50/">Run50</a><a href="./">中文目录</a><a href="../english/kentucky-derby-marathon-2021.html">English</a><a href="../../facebook/kentucky-derby-marathon-2021.html">Facebook</a>'
        if zh
        else '<a href="../../../run50/">Run50</a><a href="./">English Index</a><a href="../chinese/kentucky-derby-marathon-2021.html">Chinese</a><a href="../../facebook/kentucky-derby-marathon-2021.html">Facebook</a>'
    )
    og = f"https://arsenanzz.github.io/ZZ/assets/og-run50-{SLUG}-icons.png?v={VERSION}"
    return f"""<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)}</title>
  <meta name="description" content="{escape(desc)}">
  <meta property="og:title" content="{escape(title)}">
  <meta property="og:description" content="{escape(desc)}">
  <meta property="og:image" content="{og}">
  <meta property="og:url" content="https://arsenanzz.github.io/ZZ/{canonical}">
  <meta property="og:type" content="article">
  <link rel="stylesheet" href="../../../assets/zz-engagement.css?v=20260616">
  <style>{BASE_CSS}</style>
</head>
<body>
  <nav>{nav}</nav>
  <header class="hero">
    <div class="hero-inner">
      <div>
        <p class="kicker">Run50 · State 1 · Kentucky Story 2</p>
        <h1>{escape(title)}</h1>
        <p class="dek">{escape(desc)}</p>
        <div class="stats">
          <span class="stat">Kentucky · Louisville</span>
          <span class="stat">Derby Marathon · 2021.04.24</span>
          <span class="stat">40 photos</span>
        </div>
      </div>
      <figure class="hero-card"><img src="{img_depth}/assets/og-run50-{SLUG}-icons.png?v={VERSION}" alt="{escape(title)} cover"></figure>
    </div>
  </header>
  <main class="article-shell">
    <article class="article-body">
      {body}
    </article>
    {engagement('zh-CN' if zh else 'en', page_key, '../../..')}
  </main>
</body>
</html>
"""


def facebook_page(blocks: list[Block]) -> str:
    sections = split_sections(blocks)
    fb_blocks: list[Block] = []
    fb_blocks.extend(sections.get("02 Derby全马", []))
    fb_blocks.append(Block("h2", text="前言"))
    fb_blocks.append(Block("p", text="这篇原本是一篇 2021 上半年的流水账。Derby 是中间最硬的一段：一场疫情下分散起跑、阴雨大风、补给很冷清的肯塔基全马。跑完这段，再回头看搬家、Waverly 半马、疫苗、驾照和城市重新打开，整篇故事才有了一个完整的方向。"))
    for key in ["前言", "01 Waverly半马", "03 美国也还行，没那么凑活", "后记"]:
        fb_blocks.extend(sections.get(key, []))
    body = render_blocks(fb_blocks, lang="en", img_prefix="../stories/chinese/Run50-Kentucky-Derby-Marathon-2021-clean_files")
    # Translate the editorial bridge that only exists in the Facebook edition.
    body = body.replace(
        escape("这篇原本是一篇 2021 上半年的流水账。Derby 是中间最硬的一段：一场疫情下分散起跑、阴雨大风、补给很冷清的肯塔基全马。跑完这段，再回头看搬家、Waverly 半马、疫苗、驾照和城市重新打开，整篇故事才有了一个完整的方向。"),
        "This was originally a half-year journal from 2021. Derby is the hardest section in the middle: a Kentucky marathon with pandemic staggered starts, gray skies, wind, rain, and sparse race support. Once that race is up front, the rest of the story has a cleaner arc: moving, Waverly, vaccines, a driver's license, and a city slowly opening again.",
    )
    css = BASE_CSS + """
    body { background:#f4f6f8; }
    .masthead { background:#101820; color:#fff; border-bottom:5px solid #0b67c2; }
    .masthead-inner { max-width:1120px; margin:0 auto; padding:18px 20px; display:flex; justify-content:space-between; gap:16px; align-items:center; flex-wrap:wrap; }
    .brand { font-size:22px; font-weight:950; letter-spacing:1.2px; }
    .edition { color:#b8c4d2; font-size:13px; font-weight:800; text-transform:uppercase; letter-spacing:1.4px; }
    .content-grid { max-width:1120px; margin:0 auto; padding:42px 20px; display:grid; grid-template-columns:minmax(0,760px) 280px; gap:34px; align-items:start; }
    .rail { position:sticky; top:18px; background:#fff; border:1px solid var(--line); border-radius:8px; padding:18px; color:#344054; }
    .rail h2 { margin:0 0 12px; font-size:18px; }
    .rail p { margin:10px 0; color:#667085; font-size:14px; line-height:1.55; }
    .lede { font-size:21px; line-height:1.62; color:#263747; font-weight:700; }
    @media (max-width:900px) { .content-grid { grid-template-columns:1fr; } .rail { position:static; } }
"""
    og = f"https://arsenanzz.github.io/ZZ/assets/og-run50-{SLUG}-icons.png?v={VERSION}"
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(FB_TITLE)}</title>
  <meta name="description" content="{escape(EN_DESC)}">
  <meta property="og:title" content="{escape(FB_TITLE)}">
  <meta property="og:description" content="{escape(EN_DESC)}">
  <meta property="og:image" content="{og}">
  <meta property="og:url" content="https://arsenanzz.github.io/ZZ/run50/facebook/{SLUG}.html">
  <meta property="og:type" content="article">
  <link rel="stylesheet" href="../../assets/zz-engagement.css?v=20260616">
  <style>{css}</style>
</head>
<body>
  <header class="masthead"><div class="masthead-inner"><div class="brand">RUN50 WORLD DESK</div><div class="edition">Kentucky · Story 2 · Derby Marathon</div></div></header>
  <section class="hero">
    <div class="hero-inner">
      <div>
        <p class="kicker">Run50 · State 1 · Kentucky Story 2</p>
        <h1>{escape(FB_TITLE)}</h1>
        <p class="dek">{escape(EN_DESC)}</p>
      </div>
      <figure class="hero-card"><img src="../../assets/og-run50-{SLUG}-icons.png?v={VERSION}" alt="{escape(FB_TITLE)} cover"></figure>
    </div>
  </section>
  <main class="content-grid">
    <article class="article-body">
      <p class="lede">On April 24, 2021, the Kentucky Derby Festival Marathon came back in a pandemic format: staggered starts, a quieter course, and a runner who was still trying to earn back the word “legendary.”</p>
      {body}
    </article>
    <aside class="rail">
      <h2>Story Card</h2>
      <p><strong>Race:</strong> Kentucky Derby Festival Marathon</p>
      <p><strong>Date:</strong> Apr 24, 2021</p>
      <p><strong>Series:</strong> Run50 State 1 · Kentucky Story 2</p>
      <p><strong>Photos:</strong> 40 original images preserved from the source export.</p>
    </aside>
    {engagement('en', f'run50-{SLUG}-facebook-en', '../..')}
  </main>
</body>
</html>
"""


def wechat_page(blocks: list[Block]) -> str:
    body = render_blocks(blocks, lang="zh", img_prefix="../stories/chinese/Run50-Kentucky-Derby-Marathon-2021-clean_files")
    css = """
    * { box-sizing:border-box; } body { margin:0; background:#f3f7f8; color:#20242b; font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif; line-height:1.85; }
    .page { max-width:780px; margin:0 auto; padding:28px 18px 54px; background:#fff; }
    .cover { margin:0 -18px 28px; background:#edf3f7; border-bottom:1px solid #d0dfe8; }
    .cover img { display:block; width:100%; height:auto; }
    .meta { color:#0b67c2; font-weight:900; letter-spacing:1.4px; font-size:12px; text-transform:uppercase; }
    h1 { margin:10px 0 14px; font-size:32px; line-height:1.22; letter-spacing:0; }
    .dek { color:#667085; font-size:16px; }
    h2 { margin:40px 0 16px; padding-top:14px; border-top:1px solid #d0dfe8; font-size:24px; color:#16324c; }
    p { margin:16px 0; font-size:17px; }
    figure { margin:25px 0; }
    figure img { display:block; width:100%; height:auto; border-radius:8px; }
    figcaption { margin-top:8px; text-align:center; color:#667085; font-size:13px; }
    .end-mark,.credit-line { text-align:center; color:#8a5b22; font-weight:800; }
    """
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(ZH_TITLE)}</title>
  <style>{css}</style>
</head>
<body>
  <main class="page">
    <figure class="cover"><img src="../../assets/cover-medal-zh-index-kentucky-derby-2021-cn-flat.jpg?v={VERSION}" alt="{escape(ZH_TITLE)}封面"></figure>
    <p class="meta">RUN50 DISPATCH · KENTUCKY · STORY 2</p>
    <h1>{escape(ZH_TITLE)}</h1>
    <p class="dek">{escape(ZH_DESC)}</p>
    {body}
  </main>
</body>
</html>
"""


def write_pages(blocks: list[Block]) -> None:
    zh_body = render_blocks(blocks, lang="zh", img_prefix="Run50-Kentucky-Derby-Marathon-2021-clean_files")
    en_body = render_blocks(blocks, lang="en", img_prefix="../chinese/Run50-Kentucky-Derby-Marathon-2021-clean_files")

    (ROOT / "run50" / "stories" / "chinese" / f"{SLUG}.html").write_text(
        story_page(
            lang="zh-CN",
            title=ZH_TITLE,
            desc=ZH_DESC,
            body=zh_body,
            page_key=f"run50-{SLUG}-zh",
            canonical=f"run50/stories/chinese/{SLUG}.html",
            img_depth="../../..",
        ),
        encoding="utf-8",
    )
    (ROOT / "run50" / "stories" / "english" / f"{SLUG}.html").write_text(
        story_page(
            lang="en",
            title=EN_TITLE,
            desc=EN_DESC,
            body=en_body,
            page_key=f"run50-{SLUG}-en",
            canonical=f"run50/stories/english/{SLUG}.html",
            img_depth="../../..",
        ),
        encoding="utf-8",
    )
    (ROOT / "run50" / "facebook" / f"{SLUG}.html").write_text(facebook_page(blocks), encoding="utf-8")
    (ROOT / "run50" / "wechat" / f"{SLUG}-modern-rail.html").write_text(wechat_page(blocks), encoding="utf-8")


def remove_card(text: str, slug: str) -> str:
    card_re = re.compile(r"\n\s*<a class=\"(?:story-card|card)\"[\s\S]*?</a>", flags=re.S)
    return card_re.sub(lambda match: "" if slug in match.group(0) else match.group(0), text)


def insert_after(text: str, anchor: str, addition: str) -> str:
    if addition.strip() in text:
        return text
    pos = text.find(anchor)
    if pos == -1:
        raise RuntimeError(f"Anchor not found: {anchor}")
    end = text.find("</a>", pos)
    if end == -1:
        raise RuntimeError(f"Anchor end not found: {anchor}")
    end += len("</a>")
    return text[:end] + "\n" + addition + text[end:]


def update_indexes() -> None:
    zh_cover = f"../../../assets/cover-medal-zh-index-kentucky-derby-2021-cn-flat.jpg?v={VERSION}"
    en_cover = f"../../../assets/cover-medal-en-index-kentucky-derby-2021.png?v={VERSION}"
    fb_cover = f"../../assets/cover-medal-en-index-kentucky-derby-2021.png?v={VERSION}"
    wechat_cover = f"../../assets/cover-medal-zh-index-kentucky-derby-2021-cn-flat.jpg?v={VERSION}"

    chinese_card = f"""
        <a class="story-card run-50" href="./{SLUG}.html">
          <img src="{zh_cover}" alt="肯塔基 Derby 2021 传奇跑者半年流水账奖牌封面" loading="lazy" decoding="async">
          <div class="story-copy">
            <p class="story-meta">肯塔基路易斯维尔 · 2021.04.24</p>
            <h2 class="story-title">肯塔基第二篇：Derby 全马｜“传奇跑者”的半年流水账</h2>
            <p class="story-desc">搬家、Waverly 半马、阴雨里的 Derby 全马、疫苗和驾照，把 2021 上半年重新跑开。</p>
            <div class="story-foot"><span>Run50 · 第1州</span><span>阅读 →</span></div>
          </div>
        </a>"""
    english_card = f"""
        <a class="story-card run-50" href="./{SLUG}.html" data-map-meta="Kentucky · Louisville · 2021.04.24">
          <img src="{en_cover}" alt="Kentucky Derby Marathon 2021 medal cover" loading="lazy" decoding="async">
          <div class="story-card-body">
            <span class="story-tag">Run50 #1 · Kentucky Story 2</span>
            <h2 class="story-title">Derby Marathon and a half-year journal from Louisville</h2>
            <p class="story-desc">A rainy 2021 Derby Marathon, a lonely Waverly half, vaccines, a driver's license, and a city opening back up.</p>
            <p class="story-meta">Louisville · Kentucky · Apr 24, 2021</p>
          </div>
        </a>"""
    facebook_card = f"""
        <a class="story-card run-50" href="./{SLUG}.html">
          <img src="{fb_cover}" alt="Kentucky Derby Marathon 2021 Facebook cover" loading="lazy" decoding="async">
          <div class="story-card-body">
            <span class="story-tag">Run50 #1 · Kentucky Story 2</span>
            <h2 class="story-title">A rainy Derby Marathon, then a city opening back up</h2>
            <p class="story-desc">Race day comes first, then the half-year journal: moving, Waverly, vaccines, local runs, and a less locked-down America.</p>
            <p class="story-meta">Louisville · Kentucky · Facebook</p>
          </div>
        </a>"""
    wechat_card = f"""
      <a class="card" href="{SLUG}-modern-rail.html?v={VERSION}">
        <img class="cover" src="{wechat_cover}" alt="{ZH_TITLE}奖牌封面">
        <div class="body">
          <p class="meta">RUN50 DISPATCH · KENTUCKY · STORY 2</p>
          <h2>{ZH_TITLE}</h2>
          <p class="place">肯塔基路易斯维尔 · 2021.04.24</p>
          <p class="summary">搬家、Waverly 半马、阴雨里的 Derby 全马、疫苗和驾照，把 2021 上半年重新跑开。</p>
          <span class="button">Open WeChat Edition →</span>
        </div>
      </a>"""
    wechat_new_card = f"""
          <a class="story-card" href="https://zhennanzhang.com/run50/wechat/{SLUG}-modern-rail.html?v={VERSION}">
            <img src="../../assets/cover-medal-zh-index-kentucky-derby-2021-cn-flat.jpg?v={VERSION}" alt="{ZH_TITLE}封面">
            <div class="story-body">
              <span class="story-number">Run50 · 01B</span>
              <div class="eyebrow">RUN50 DISPATCH · KENTUCKY</div>
              <h3>{ZH_TITLE}</h3>
              <div class="meta">肯塔基路易斯维尔 · 2021.04.24</div>
              <p class="desc">Derby 是这篇半年流水账里最硬的一段：疫情分散起跑、阴雨大风、冷清补给，以及重新找回跑步状态的开头。</p>
              <span class="story-cta">Open WeChat Edition</span>
            </div>
          </a>"""

    targets = [
        (ROOT / "run50" / "stories" / "chinese" / "index.html", "louisville-marathon.html", chinese_card),
        (ROOT / "run50" / "stories" / "english" / "index.html", "louisville-marathon.html", english_card),
        (ROOT / "run50" / "facebook" / "index.html", "louisville-marathon.html", facebook_card),
        (ROOT / "run50" / "wechat" / "index.html", "louisville-marathon-modern-rail.html", wechat_card),
        (ROOT / "run50" / "wechat-new" / "index.html", "louisville-marathon-modern-rail.html", wechat_new_card),
    ]
    for path, anchor, card in targets:
        text = path.read_text(encoding="utf-8")
        text = remove_card(text, SLUG)
        text = insert_after(text, anchor, textwrap.dedent(card).rstrip())
        if path == ROOT / "run50" / "wechat-new" / "index.html":
            text = text.replace('<div class="stat-card"><b>57</b><span>公众号版文章</span></div>', '<div class="stat-card"><b>58</b><span>公众号版文章</span></div>')
            text = text.replace('<div class="stat-card"><b>34</b><span>Run50 故事</span></div>', '<div class="stat-card"><b>35</b><span>Run50 故事</span></div>')
        path.write_text(text, encoding="utf-8")

    run50_index = ROOT / "run50" / "index.html"
    text = run50_index.read_text(encoding="utf-8")
    new_race = "      ['Kentucky Derby Marathon', '2021.04.24', './stories/english/kentucky-derby-marathon-2021.html'],\n"
    if "kentucky-derby-marathon-2021.html" not in text:
        anchor = "      ['Louisville Marathon', '2020.11.08', './stories/english/louisville-marathon.html'],\n"
        text = text.replace(anchor, anchor + new_race)
        run50_index.write_text(text, encoding="utf-8")


def update_supabase() -> None:
    path = ROOT / "supabase" / "run50-comments.sql"
    text = path.read_text(encoding="utf-8")
    if PAGE_KEYS[0] in text:
        return
    anchor = "      'run50-kentucky-derby-marathon-2025-zh',\n"
    addition = "".join(f"      '{key}',\n" for key in PAGE_KEYS)
    if anchor not in text:
        raise RuntimeError("Supabase whitelist anchor not found")
    text = text.replace(anchor, anchor + addition)
    path.write_text(text, encoding="utf-8")


def validate(blocks: list[Block]) -> None:
    figures = sum(1 for block in blocks if block.kind == "figure")
    if figures != 40:
        raise RuntimeError(f"Expected 40 figures, got {figures}")
    missing = [block.text for block in blocks if block.kind in {"p", "h2", "end", "credit"} and block.text not in EN]
    missing += [block.caption for block in blocks if block.kind == "figure" and block.caption not in CAPTIONS and not re.match(r"^(Downtown|Ohio river|Broad Run Park|Silo|20 mile|New Albany|Bernheim Arboretum|Snow running group|FF running group|Hiking|Mike Mains|Paul)", block.caption)]
    if missing:
        print("Translation fallback entries:")
        for item in missing:
            print(" -", item)


def main() -> None:
    blocks = extract_blocks()
    validate(blocks)
    copy_images()
    draw_cover(ROOT / "assets" / "cover-medal-zh-index-kentucky-derby-2021-cn-flat.jpg", chinese=True)
    draw_cover(ROOT / "assets" / "cover-medal-en-index-kentucky-derby-2021.png", chinese=False)
    draw_cover(ROOT / "assets" / f"og-run50-{SLUG}-icons.png", chinese=False, og=True)
    write_svg_cover()
    write_pages(blocks)
    update_indexes()
    update_supabase()
    print(f"Built {SLUG}: {len(blocks)} blocks, 40 images")


if __name__ == "__main__":
    main()
