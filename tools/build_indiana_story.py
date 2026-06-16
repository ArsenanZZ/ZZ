from pathlib import Path
from html import escape
from lxml import html
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps
import re
import shutil


REPO = Path(__file__).resolve().parents[1]
SOURCE_BASE = Path(
    r"Z:\ZhennanZ Folder\000-Marathon-Story-2024-2025\20230000-Marathons\2022-State-05-IN"
)
SOURCE_HTML = next(SOURCE_BASE.glob("*.html"))
SOURCE_FILES = next(p for p in SOURCE_BASE.iterdir() if p.is_dir() and p.name.endswith("_files"))

SITE = "https://arsenanzz.github.io/ZZ"
SLUG = "indianapolis-monumental-marathon"
VERSION = "20260615-5"
ENGAGEMENT_VERSION = "20260615"

OUT_IMG_DIR = (
    REPO
    / "run50"
    / "stories"
    / "chinese"
    / "Run50-Indianapolis-Monumental-Marathon-clean_files"
)
OG_PATH = REPO / "assets" / "og-run50-indianapolis-monumental-marathon-icons.png"
THUMB_PATH = REPO / "assets" / "thumb-run50-indianapolis-monumental-marathon-icons.svg"
FB_THUMB_PATH = REPO / "assets" / "facebook" / THUMB_PATH.name
MEDAL_COVER_PATH = REPO / "assets" / "cover-medal-in.jpg"

TITLE_ZH = "Run50 #第5州｜印第安纳：印第安纳波利斯纪念碑马拉松｜一日狂飙"
TITLE_EN = "Run50 #5 | Indiana: Indianapolis Monumental Marathon in One Day"
TITLE_FB = "Indianapolis turned a rainy one-day marathon into a way back to running"
DATE_ZH = "2022.11.05"
DATE_EN = "Nov 5, 2022"
RACE_NAME = "15th CNO Financial Indianapolis Monumental Marathon"

SKIP_TEXTS = {
    "▲ Indy Monumental Marathon @Arsenan",
    "- Indianapolis -",
    "印地秋天，全马再出发",
}


EN_TSV = r"""
丨Indy丨	| Indy |
前言	Preface
印地安娜波利斯的Monumental“牦牛”马拉松在我们路村可以说是鼎鼎大名，每次和美国朋友聊天，他们都会兴致勃勃的讨论这项赛事，可以说是有口皆碑，路线平坦并且离我们也近。	The Monumental "Yak" Marathon in Indianapolis is famous around our Louisville village. Every time I chatted with American friends, they would talk about it with real excitement. It has a great reputation: flat course, and not far from us.
我其实一直在犹豫要不要去，主要是担心2022下半年跑量不太够，自从旧金山马拉松回来之后，我基本就处于半退役状态了。	I had actually been hesitating about whether to go, mostly because I was worried my mileage in the second half of 2022 was not enough. Ever since coming back from the San Francisco Marathon, I had basically been in semi-retirement.
所以，我确实需要一个跑步来激励一下，“牦牛”马就很合适，因为赛道平很快速，还可以帮我再点亮一个全马州。临近比赛两个星期，错过了早鸟价，犹豫了一会，最后还是决定报个名。	So I really needed a run to motivate myself, and the "Yak" Marathon was a good fit. The course is flat and fast, and it could help me light up another full-marathon state. Two weeks before the race, after missing the early-bird price and hesitating a little, I finally decided to sign up.
报名界面和芝加哥马拉松很像，一看就很高端，再仔细瞅瞅这个马，瞬间又觉得很值得，“牦牛”马还是美国最大的15个马拉松赛事之一，起点和终点都在印第安纳波利斯市中心。并且2022年还是整15届，我喜欢跑在市中心的大型马拉松，这绝对是近距离体验一座城市的绝佳方式；15届的数字也很好，值得一去！	The registration page looked a lot like the Chicago Marathon's, very polished at first glance. Then I looked more carefully at this race and instantly felt it was worth it. The "Yak" Marathon is also one of the 15 largest marathons in the U.S., with both start and finish in downtown Indianapolis. And 2022 was its 15th running. I like big downtown marathons; they are an excellent way to experience a city up close. The number 15 felt good too. Worth going.
这次47去加州开会，所以不能同行，我就压缩了行程，把开车去印城和跑马放在一天，两个多小时的车程并不会很辛苦，就是需要早起，因为起跑在8点，我要保证在这之前到达印城，找到车位，完成包裹领取和热身。	This time 47 was going to California for a conference, so she could not come with me. I compressed the itinerary and put the drive to Indy and the marathon into one day. The drive was only a little over two hours, so it would not be too tiring, but I did need to get up early. The race started at 8:00, and before that I had to arrive in Indy, find parking, pick up my packet, and warm up.
所以比赛日，11月5号这天，我凌晨三点多就出发了，路上车不多，开的挺轻松，很顺利地就抵达了起点边的停车场，还有很多车位。	So on race day, November 5, I set out a little after 3 a.m. There were not many cars on the road, so the drive was easy, and I smoothly reached a parking lot near the start with plenty of spaces left.
到的有点早，我也去旁边的市政厅和纪念碑广场转了转，上次是白天来的，印象深刻。这次天光未亮，纪念碑又有了不一样的风貌。	I arrived a little early, so I walked around the nearby statehouse and Monument Circle. I had been here during the day before and remembered it clearly. This time, before dawn, the monument had a different look.
士兵和水手纪念碑，是印第安纳州的标志性建筑之一。它是为了纪念美国内战中牺牲的印第安纳州士兵和水手而建造的，高达86米，是世界上最高的纪念碑之一。纪念碑对面就可以看到市政厅。	The Soldiers and Sailors Monument is one of Indiana's landmark buildings. It was built to honor Indiana soldiers and sailors who died in the American Civil War. At 86 meters tall, it is one of the tallest monuments in the world. Across from it, you can see the statehouse.
快到7点，人渐渐多了起来，我也很顺利的领取了装备，这次因为没有去Expo，所以我选择了当日领取包裹，“牦牛”马这点做的很周到。	As it got close to 7:00, more people gradually arrived, and I picked up my gear very smoothly. Because I did not go to the expo, I chose race-day packet pickup, and the "Yak" Marathon handled this very thoughtfully.
领完号码簿后，秋雨来袭，我就躲回了车里，等待起跑，虽然下着雨，但起点边的厕所还是排起了长队，秋雨不凉，还很舒服，这是很棒的跑马温度。	After picking up my bib, autumn rain arrived, so I hid back in the car and waited for the start. Even though it was raining, the toilets near the start still had long lines. The autumn rain was not cold; it actually felt comfortable. This was great marathon weather.
开跑	Start
雨渐渐变小，我也不想躲雨了，这不是跑马者该有的态度，我也加入大部队，在起点等待开跑。	The rain gradually got lighter, and I did not want to keep hiding from it. That was not the attitude a marathon runner should have. I joined the crowd and waited at the start.
人群喧闹，大家都跃跃欲试，天也开始慢慢变亮。终于，期待已久的时刻到来了！开跑！	The crowd was noisy and everyone was eager to go. The sky slowly began to brighten. Finally, the long-awaited moment arrived. Start!
再次跑马总是让人兴奋，但我心里也在打鼓，毕竟快半年没跑这样的距离了。	Running a marathon again is always exciting, but I was also nervous. After all, it had been almost half a year since I had run this distance.
好在印地的秋天很舒服，秋雨很清新，秋色很美丽。跑起来很容易就进入状态，步伐也不沉重，没有负担，完赛就好。	Fortunately, autumn in Indy was comfortable, the autumn rain was fresh, and the fall colors were beautiful. Once I started running, it was easy to get into rhythm. My steps did not feel heavy, there was no burden, and finishing would be enough.
起始的路线基本都在市区里，跑到2 miles的时候，我们就跑到了士兵和水手纪念碑，这绝对是赛事的亮点，大家都边跑边拿手机拍照，这会儿天亮了很多，和刚才看到的很不样。	The opening part of the course was basically all downtown. Around mile 2, we reached the Soldiers and Sailors Monument, definitely a highlight of the race. Everyone ran while taking phone photos. By then it was much brighter, and the scene looked very different from what I had just seen before dawn.
这边还有摄影师，我也摆了个pose，但是赛后查询，估计是没拍到，有点遗憾。	There were photographers there too, and I struck a pose, but when I checked after the race, I probably was not captured. A little regret.
跑过纪念碑，我们就跑进了当地的街区，我停在了一座教堂边的补给点上了个厕所，吃了点能量胶，继续开跑。跑马多了就知道，能量胶绝对是个好东西。	After passing the monument, we ran into local neighborhoods. I stopped at an aid station beside a church to use the bathroom, ate some energy gel, and kept running. Once you have run enough marathons, you know energy gels are absolutely good stuff.
秋天里的街区很好看，金黄色的落叶在树上，在地上，和秋雨融为一体，踩在上面不会沙沙作响，但也没有很滑。	The neighborhoods in autumn looked beautiful. Golden leaves were on the trees and on the ground, blending with the autumn rain. Stepping on them did not make a crisp rustling sound, but they were not very slippery either.
中途路过一个华人补给站，让我印象深刻，很有秩序，也很干净，我用中文向他们表示感谢，志愿者们也给我回了一句“加油！“	Midway through, I passed a Chinese aid station that left a strong impression on me. It was orderly and clean. I thanked them in Chinese, and the volunteers answered, "Jiayou!"
这会儿我跟着430的队伍一起，大家互相护理，跑起来很有劲，领头的兔子姐一直在和大家互动，最后还让我们互相自我介绍，来自哪里，跑了多少个马拉松。	At this point I was running with the 4:30 group. Everyone looked after each other, and running felt powerful. The lead pacer kept interacting with us, and in the end she even had us introduce ourselves: where we were from, and how many marathons we had run.
当轮到我，我说出了自己彪炳的战绩，不装了，我摊牌了，大家都是一阵欢呼。虽然那会儿体重超标，没有个传奇的样子，但心里还是不由得窃喜，也立志要好好锻炼身体。	When it was my turn, I laid out my glorious record. No more pretending, I showed my cards, and everyone burst into cheers. Although my weight was over the limit at the time and I did not exactly look legendary, I still felt secretly delighted and resolved to train properly again.
430的队伍不好跟，最后我还是不得不和大家说了再见。半马过后，明显感觉到体力没有之前强悍。	The 4:30 group was not easy to follow, and in the end I had to say goodbye to everyone. After the half marathon mark, I clearly felt my stamina was not as strong as before.
在一个公园的路线，我就突然想到47经常用到的间歇跑法。随即在谷歌市场下了一个app，临时制定了一个跑2走1的计划。	On a park section of the route, I suddenly thought of the run-walk interval method 47 often uses. I immediately downloaded an app from the Google Play Store and made a temporary plan: run 2 minutes, walk 1 minute.
没想到，这个方法还真管用。跑跑走走很舒服，感谢47给的灵感。	I did not expect it to work so well. Running and walking felt comfortable. Thanks to 47 for the inspiration.
不一会445的兔子追上了我，我觉得自己状态还行，就想跟一跟，不过我确实还是高估了自己，那就Let pacer go！	Before long, the 4:45 pacer caught up with me. I felt I was still doing all right and wanted to follow for a while, but I had definitely overestimated myself. So, let pacer go!
终于回到市区了，看到一个补给点，我赶紧补充一下能量饮料，为最后的冲线做准备。 再次和纪念碑重逢，我知道终点就在不远处了！	At last I was back downtown. Seeing an aid station, I quickly took some sports drink to prepare for the final push. When I met the monument again, I knew the finish was not far away.
很惊喜的是在冲线前我还遇见了Fleet Feet的老朋友Myrdin和Justin，搞了一张合影，准备完赛。	To my surprise, before the finish I ran into my old Fleet Feet friends Myrdin and Justin. We took a group photo, and I got ready to finish.
终点近了，我一看手表，这次能进5个小时，虽然放在几年前，这绝对不是个让我满意的成绩，但这一年来，破5似乎已经是个让我难以企及的高度。	The finish was close. I looked at my watch and saw I could finish under five hours. A few years ago, that definitely would not have been a satisfying result for me, but this past year, breaking five had almost become something out of reach.
特别是最近训练一般，体重飙升，4小时55分钟12秒，挺好的。	Especially with mediocre training recently and my weight shooting up, 4:55:12 was pretty good.
后记	Postscript
奖牌还挺好看的，主体元素是印城的市政厅。还有给完赛跑者的纪念品，全马是蓝色的毛线帽，半马是红色，我给47也要了一个。	The medal was actually pretty good-looking, with the Indianapolis statehouse as the main element. There were also finisher gifts: blue knit hats for full marathoners and red ones for half marathoners. I asked for one for 47 too.
跑完简单拉伸了一下，开车去Planet Fitness洗了个澡，又去中餐馆吃了个自助，然后回家，开车途中挺困的，大风又呜呜的吹，我就把车停到了一个加油站，在车里眯了一会儿，就又精神饱满了，顺利回到了路城。	After the race, I stretched briefly, drove to Planet Fitness for a shower, then went to a Chinese restaurant for buffet before heading home. I got pretty sleepy while driving, and the strong wind kept howling, so I pulled into a gas station and napped in the car for a bit. Then I was full of energy again and made it back to Louisville smoothly.
一日风尘，浓缩的单日跑马旅程。时间虽不长，但时隔接近一年来写这个文，还是意犹未尽。更重要的是，在”牦牛”马，我又找到了坚持跑步的方法，至今依旧受用。	One dusty day on the road, a compressed single-day marathon trip. It was not long, but writing this almost a year later, I still feel there is more to say. More importantly, at the "Yak" Marathon, I found a way to keep running again, and it still works for me now.
- 本文完 -	- End -
文字丨Arsenan	Words | Arsenan
摄影丨Arsenan	Photos | Arsenan
设计丨Arsenan	Design | Arsenan
"""


EN_BY_ZH = {}
for line in EN_TSV.strip().splitlines():
    zh, en = line.split("\t", 1)
    EN_BY_ZH[zh] = en


def norm(value: str) -> str:
    return re.sub(r"\s+", " ", value.replace("\xa0", " ")).strip()


def cleanup_story_text(text: str) -> str:
    text = norm(text).replace("\u200d", "").strip()
    text = text.replace("Captial", "Capitol")
    text = text.replace("Run in Indy@ Arsenan", "Run in Indy @Arsenan")
    text = text.replace("13.1 and 26.2", "13.1 and 26.2")
    return text.strip()


def is_styleish(value: str) -> bool:
    return ":host {" in value or "--weui-" in value or len(value) > 1200


def has_desc_leaf_container(el) -> bool:
    for desc in el.iterdescendants():
        if desc.tag in ("p", "section"):
            text = norm("".join(desc.itertext()))
            if text and not is_styleish(text):
                return True
    return False


def extract_story():
    source = SOURCE_HTML.read_text(encoding="utf-8", errors="replace")
    doc = html.fromstring(source)
    roots = doc.xpath('//*[@id="js_content"]')
    root = roots[0] if roots else doc
    events = []

    def walk(el):
        if not isinstance(el.tag, str):
            return
        if el.tag == "img":
            src = el.get("src") or el.get("data-src") or ""
            if src:
                events.append({"type": "img", "src": src})
            return
        if el.tag in ("p", "section"):
            text = norm("".join(el.itertext()))
            if text and not is_styleish(text) and not has_desc_leaf_container(el):
                if text not in ["，赞"] and not text.startswith("鲜花"):
                    events.append({"type": "text", "text": text})
                for img in el.xpath(".//img"):
                    src = img.get("src") or img.get("data-src") or ""
                    if src:
                        events.append({"type": "img", "src": src})
                return
        for child in el:
            walk(child)

    for child in root:
        walk(child)

    clean = []
    for idx, event in enumerate(events):
        key = (event["type"], event.get("text") or event.get("src"))
        prev = (clean[-1][1]["type"], clean[-1][1].get("text") or clean[-1][1].get("src")) if clean else None
        if prev != key:
            clean.append((idx, event))

    story = []
    for idx, event in clean:
        if event["type"] == "text":
            text = cleanup_story_text(event["text"])
            if not text or text in SKIP_TEXTS:
                continue
            story.append((idx, {"type": "text", "text": text}))
        else:
            story.append((idx, event))
    return story


def local_source_path(src: str) -> Path:
    src = src.split("#", 1)[0].split("?", 1)[0].replace("\\", "/")
    name = Path(src).name
    path = SOURCE_FILES / name
    if path.exists():
        return path
    raise FileNotFoundError(f"Could not map image source: {src}")


def copy_story_images(indexed):
    OUT_IMG_DIR.mkdir(parents=True, exist_ok=True)
    for old in OUT_IMG_DIR.glob("img-*.webp"):
        old.unlink()
    count = 0
    for _, event in indexed:
        if event["type"] != "img":
            continue
        count += 1
        out_name = f"img-{count:03d}.webp"
        with Image.open(local_source_path(event["src"])) as image:
            image = ImageOps.exif_transpose(image)
            if image.mode != "RGB":
                image = image.convert("RGB")
            image.save(OUT_IMG_DIR / out_name, "WEBP", quality=88, method=6)
        event["out"] = out_name
    return count


def is_caption(text: str) -> bool:
    return text.startswith("▲")


def clean_caption(text: str) -> str:
    text = cleanup_story_text(text)
    text = re.sub(r"^▲\s*", "▲ ", text)
    text = re.sub(r"\s+", " ", text)
    text = text.replace("430 Team", "4:30 Team")
    text = text.replace("445 Pacer", "4:45 Pacer")
    return text


def translate_caption(text: str) -> str:
    caption = clean_caption(text)
    replacements = {
        "▲ Indy @Google": "▲ Indy @Google",
        "▲ Run Indy @Google": "▲ Run Indy @Google",
        "▲ State Capitol @Arsenan": "▲ State Capitol @Arsenan",
        "▲ Back to State Capitol @Arsenan": "▲ Back to State Capitol @Arsenan",
        "▲ Soldiers and Sailors Monument @Arsenan": "▲ Soldiers and Sailors Monument @Arsenan",
        "▲ Bib Number @Arsenan": "▲ Bib Number @Arsenan",
        "▲ Marathon Start @Arsenan": "▲ Marathon Start @Arsenan",
        "▲ Wave A @Arsenan": "▲ Wave A @Arsenan",
        "▲ PANG @Arsenan": "▲ PANG @Arsenan",
        "▲ Run in Indy @Arsenan": "▲ Run in Indy @Arsenan",
        "▲ 2 miles @Arsenan": "▲ 2 miles @Arsenan",
        "▲ Run near Monument @Arsenan": "▲ Run near Monument @Arsenan",
        "▲ Water Station @Arsenan": "▲ Water Station @Arsenan",
        "▲ 13.1 and 26.2 @Arsenan": "▲ 13.1 and 26.2 @Arsenan",
        "▲ Chinese Water Station @Arsenan": "▲ Chinese Water Station @Arsenan",
        "▲ 4:30 Team @Arsenan": "▲ 4:30 Team @Arsenan",
        "▲ Park Run @Arsenan": "▲ Park Run @Arsenan",
        "▲ 4:45 Pacer @Arsenan": "▲ 4:45 Pacer @Arsenan",
        "▲ Back to Downtown @Arsenan": "▲ Back to Downtown @Arsenan",
        "▲ Back to Monument @Arsenan": "▲ Back to Monument @Arsenan",
        "▲ Myrdin and Justin @Arsenan": "▲ Myrdin and Justin @Arsenan",
        "▲ Almost There @MaraFoto": "▲ Almost There @MaraFoto",
        "▲ Finish @Arsenan": "▲ Finish @Arsenan",
        "▲ Medal Time @Arsenan": "▲ Medal Time @Arsenan",
        "▲ Photo Time @Arsenan": "▲ Photo Time @Arsenan",
        "▲ Medal @Arsenan": "▲ Medal @Arsenan",
        "▲ Medal and Hats @Arsenan": "▲ Medal and Hats @Arsenan",
        "▲ China Buffet @Arsenan": "▲ China Buffet @Arsenan",
    }
    return replacements.get(caption, caption)


def translate_text(text: str) -> str:
    text = cleanup_story_text(text)
    if is_caption(text):
        return translate_caption(text)
    if text in EN_BY_ZH:
        return EN_BY_ZH[text]
    if re.fullmatch(r"[\w\s|#.,:;!?'\"()&/@+\-]+", text):
        return text
    raise KeyError(f"Missing English translation for: {text}")


def render_text_block(text: str, lang: str) -> str:
    value = text if lang == "zh" else translate_text(text)
    if text in {"前言", "开跑", "后记"}:
        return f"<h2>{escape(value)}</h2>"
    if text == "丨Indy丨":
        return f'<p class="story-kicker-line">{escape(value)}</p>'
    if text == "- 本文完 -":
        return f'<p class="end-mark">{escape(value)}</p>'
    if text in {"文字丨Arsenan", "摄影丨Arsenan", "设计丨Arsenan"}:
        return f'<p class="credit-line">{escape(value)}</p>'
    return f"<p>{escape(value)}</p>"


def render_article(indexed, lang: str, img_prefix: str, alt_base: str) -> str:
    out = []
    pending = None

    def flush(caption=None):
        nonlocal pending
        if not pending:
            return
        img_num = pending["out"].split("-")[-1].split(".")[0]
        cap_html = ""
        if caption:
            cap_text = clean_caption(caption) if lang == "zh" else translate_caption(caption)
            cap_html = f"<figcaption>{escape(cap_text)}</figcaption>"
        out.append(
            f'<figure><img src="{img_prefix}{pending["out"]}" alt="{escape(alt_base)} {img_num}" '
            f'loading="lazy" decoding="async">{cap_html}</figure>'
        )
        pending = None

    for _, event in indexed:
        if event["type"] == "img":
            flush()
            pending = event
            continue
        text = cleanup_story_text(event["text"])
        if is_caption(text):
            if pending:
                flush(text)
            else:
                caption = clean_caption(text) if lang == "zh" else translate_caption(text)
                out.append(f'<p class="caption-line">{escape(caption)}</p>')
            continue
        flush()
        out.append(render_text_block(text, lang))
    flush()
    return "\n".join(out)


def engagement(lang: str, rel_assets: str, page_key: str, comment_id: str) -> str:
    is_zh = lang == "zh"
    kicker = "留言 / 阅读" if is_zh else "Comments / Views"
    heading = "跑完也说两句" if is_zh else "Say something after the run"
    note = "不用登录，留下名字就能留言。新留言会直接显示。" if is_zh else "No account is needed to submit a comment. New comments appear right away."
    views = "阅读次数" if is_zh else "Views"
    loading = "评论加载中..." if is_zh else "Loading comments..."
    locale = "zh-CN" if is_zh else "en"
    return f"""
    <section class="zz-engagement" data-zz-engagement data-locale="{locale}" data-page-key="{page_key}">
      <div class="zz-engagement-shell">
        <div>
          <p class="zz-engagement-kicker">{escape(kicker)}</p>
          <h2>{escape(heading)}</h2>
          <p class="zz-engagement-note">{escape(note)}</p>
          <div class="zz-engagement-stats">
            <span class="zz-engagement-stat" id="busuanzi_container_page_pv">
              <span>{escape(views)}</span>
              <strong id="busuanzi_value_page_pv" data-zz-view-count>--</strong>
            </span>
          </div>
        </div>
        <div class="zz-engagement-card">
          <div id="{comment_id}" data-zz-supabase-comments></div>
          <p class="zz-engagement-status" data-zz-engagement-status>{escape(loading)}</p>
        </div>
      </div>
    </section>
    <script src="{rel_assets}/zz-engagement-config.js?v={ENGAGEMENT_VERSION}"></script>
    <script src="{rel_assets}/zz-engagement.js?v={ENGAGEMENT_VERSION}"></script>
"""


def normal_page(lang: str, article: str) -> str:
    is_zh = lang == "zh"
    title = TITLE_ZH if is_zh else TITLE_EN
    description = (
        "Run50第5州印第安纳：2022年11月5日印第安纳波利斯纪念碑马拉松，一场清晨出发、秋雨开跑、最终4小时55分12秒完赛的单日跑马旅程。"
        if is_zh
        else "Run50 State 5 in Indiana: the November 5, 2022 Indianapolis Monumental Marathon, a one-day trip through autumn rain, Monument Circle, run-walk intervals, and a 4:55:12 finish."
    )
    nav = (
        f'<a href="./index.html">← 中文故事</a><a href="../english/{SLUG}.html">English</a><a href="../../facebook/{SLUG}.html">Facebook</a><a href="../../index.html">Run50</a>'
        if is_zh
        else f'<a href="./index.html">← English Stories</a><a href="../chinese/{SLUG}.html">中文</a><a href="../../facebook/{SLUG}.html">Facebook</a><a href="../../index.html">Run50</a>'
    )
    eyebrow = "Run50 #第5州 · 印第安纳" if is_zh else "Run50 #5 · Indiana"
    dek = description
    meta = (
        f"<span>印第安纳波利斯，印第安纳</span><span>{DATE_ZH}</span><span>Run50 #5</span><span>{RACE_NAME}</span>"
        if is_zh
        else f"<span>Indianapolis, Indiana</span><span>{DATE_EN}</span><span>Run50 #5</span><span>{RACE_NAME}</span>"
    )
    cover_alt = "印第安纳波利斯图标封面" if is_zh else "Indianapolis Marathon icon cover"
    part_label = "印地秋天，全马再出发" if is_zh else "A rainy one-day marathon in Indy"
    page_key = f"run50-{SLUG}-zh" if is_zh else f"run50-{SLUG}-en"
    comment_id = "supabase-comments-indianapolis-zh" if is_zh else "supabase-comments-indianapolis-en"
    canonical_dir = "chinese" if is_zh else "english"
    lang_attr = "zh-Hans" if is_zh else "en"

    return f"""<!doctype html>
<html lang="{lang_attr}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)}</title>
  <meta name="description" content="{escape(description)}">
  <link rel="canonical" href="{SITE}/run50/stories/{canonical_dir}/{SLUG}.html">
  <meta property="og:type" content="article">
  <meta property="og:title" content="{escape(title)}">
  <meta property="og:description" content="{escape(description)}">
  <meta property="og:image" content="{SITE}/assets/{OG_PATH.name}?v={VERSION}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:image" content="{SITE}/assets/{OG_PATH.name}?v={VERSION}">
  <link rel="stylesheet" href="../../../assets/zz-engagement.css?v={ENGAGEMENT_VERSION}">
  <style>
    :root {{ --bg:#edf3f7; --paper:#fff; --ink:#20242b; --muted:#667085; --line:#d0dfe8; --accent:#0b67c2; --soft:#f8fbfd; }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; background:var(--bg); color:var(--ink); font-family:Inter, "Segoe UI", Arial, "Microsoft YaHei", sans-serif; line-height:1.78; }}
    a {{ color:inherit; }}
    .nav {{ position:sticky; top:0; z-index:10; display:flex; gap:14px; flex-wrap:wrap; justify-content:center; padding:13px 18px; background:rgba(237,243,247,.92); backdrop-filter:blur(12px); border-bottom:1px solid var(--line); }}
    .nav a {{ text-decoration:none; color:#475467; font-size:14px; font-weight:800; }}
    .hero {{ max-width:1120px; margin:0 auto; padding:54px 20px 20px; }}
    .hero-card {{ display:grid; grid-template-columns:minmax(0,1fr) minmax(260px,430px); gap:28px; align-items:center; }}
    .eyebrow {{ margin:0 0 12px; color:var(--accent); text-transform:uppercase; letter-spacing:.08em; font-size:13px; font-weight:900; }}
    h1 {{ margin:0; font-family:Georgia, "Times New Roman", "Microsoft YaHei", serif; font-size:clamp(34px,5vw,64px); line-height:1.05; letter-spacing:0; }}
    .dek {{ margin:18px 0 0; color:#475467; font-size:18px; max-width:760px; }}
    .cover {{ width:100%; border:1px solid var(--line); border-radius:8px; box-shadow:0 24px 60px rgba(15,23,42,.13); background:#fff; }}
    .meta-row {{ display:flex; gap:10px; flex-wrap:wrap; margin-top:22px; }}
    .meta-row span {{ border:1px solid var(--line); background:rgba(255,255,255,.78); color:#475467; padding:7px 11px; border-radius:999px; font-size:13px; font-weight:800; }}
    main {{ max-width:860px; margin:0 auto; padding:20px 20px 64px; }}
    .part-label {{ margin:52px 0 20px; padding-top:26px; border-top:1px solid var(--line); color:var(--accent); font-size:15px; font-weight:900; letter-spacing:.04em; text-transform:uppercase; }}
    article {{ background:var(--paper); border:1px solid var(--line); border-radius:8px; padding:clamp(22px,4vw,46px); box-shadow:0 18px 50px rgba(15,23,42,.08); }}
    article p {{ margin:0 0 18px; font-size:17px; }}
    article h2 {{ margin:34px 0 16px; font-size:26px; line-height:1.25; }}
    .story-kicker-line {{ color:#6b7a86; font-weight:900; text-align:center; }}
    .end-mark, .credit-line {{ text-align:center; color:#6b7a86; font-weight:800; }}
    figure {{ margin:28px 0; }}
    figure img {{ display:block; width:100%; height:auto; border-radius:8px; border:1px solid #e5edf3; background:#f8fafc; }}
    figcaption, .caption-line {{ margin-top:8px; color:#667085; text-align:center; font-size:13px; line-height:1.5; }}
    @media (max-width:760px) {{
      .hero-card {{ grid-template-columns:1fr; }}
      .hero {{ padding-top:36px; }}
      .cover {{ max-width:520px; }}
      article {{ padding:22px; }}
      article p {{ font-size:16px; }}
    }}
  </style>
</head>
<body>
  <nav class="nav">{nav}</nav>
  <header class="hero">
    <div class="hero-card">
      <div>
        <p class="eyebrow">{escape(eyebrow)}</p>
        <h1>{escape(title)}</h1>
        <p class="dek">{escape(dek)}</p>
        <div class="meta-row">{meta}</div>
      </div>
      <img class="cover" src="../../../assets/{THUMB_PATH.name}?v={VERSION}" alt="{escape(cover_alt)}">
    </div>
  </header>
  <main>
    <p class="part-label">{escape(part_label)}</p>
    <article>
{article}
    </article>
{engagement("zh" if is_zh else "en", "../../../assets", page_key, comment_id)}
  </main>
</body>
</html>
"""


def facebook_page(article: str) -> str:
    description = (
        "On November 5, 2022, Run50 State 5 went to the 15th Indianapolis Monumental Marathon: a fast, flat downtown race in autumn rain, finished in 4:55:12."
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(TITLE_FB)}</title>
  <meta name="description" content="{escape(description)}">
  <link rel="canonical" href="{SITE}/run50/facebook/{SLUG}.html">
  <meta property="og:type" content="article">
  <meta property="og:title" content="{escape(TITLE_FB)}">
  <meta property="og:description" content="{escape(description)}">
  <meta property="og:image" content="{SITE}/assets/{OG_PATH.name}?v={VERSION}">
  <meta property="og:url" content="{SITE}/run50/facebook/{SLUG}.html">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:image" content="{SITE}/assets/{OG_PATH.name}?v={VERSION}">
  <link rel="stylesheet" href="../../assets/zz-engagement.css?v={ENGAGEMENT_VERSION}">
  <style>
    :root {{ --bg:#f5f7fa; --paper:#fff; --ink:#101828; --muted:#667085; --line:#d0dfe8; --accent:#0b67c2; }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; background:var(--bg); color:var(--ink); font-family:Inter, "Segoe UI", Arial, sans-serif; line-height:1.72; }}
    a {{ color:inherit; }}
    .topbar {{ background:#0b1018; color:#fff; border-bottom:4px solid var(--accent); }}
    .topbar-inner {{ max-width:1180px; margin:0 auto; padding:14px 18px; display:flex; justify-content:space-between; gap:14px; align-items:center; flex-wrap:wrap; }}
    .brand {{ font-weight:950; letter-spacing:.08em; text-transform:uppercase; }}
    .brand span {{ color:#8ab4f8; }}
    .topbar nav {{ display:flex; gap:14px; flex-wrap:wrap; }}
    .topbar a {{ color:#dbe7ff; text-decoration:none; font-size:13px; font-weight:800; }}
    .hero {{ background:#fff; border-bottom:1px solid var(--line); }}
    .hero-inner {{ max-width:1180px; margin:0 auto; padding:42px 18px 30px; display:grid; grid-template-columns:minmax(0,1.08fr) minmax(280px,.72fr); gap:30px; align-items:center; }}
    .section-label {{ margin:0 0 12px; color:var(--accent); text-transform:uppercase; letter-spacing:.08em; font-size:13px; font-weight:950; }}
    h1 {{ margin:0; font-family:Georgia, "Times New Roman", serif; font-size:clamp(36px,5.2vw,72px); line-height:1; letter-spacing:0; }}
    .dek {{ max-width:780px; margin:18px 0 0; color:#475467; font-size:19px; }}
    .hero img {{ width:100%; border:1px solid var(--line); border-radius:8px; box-shadow:0 28px 70px rgba(15,23,42,.16); background:#fff; }}
    .meta-row {{ margin-top:22px; display:flex; gap:10px; flex-wrap:wrap; }}
    .meta-row span {{ background:#eef5fb; border:1px solid #cddfec; color:#344054; border-radius:999px; padding:7px 11px; font-size:13px; font-weight:850; }}
    .layout {{ max-width:1180px; margin:0 auto; padding:32px 18px 66px; display:grid; grid-template-columns:minmax(0,780px) minmax(230px,1fr); gap:32px; align-items:start; }}
    article {{ background:var(--paper); border:1px solid var(--line); border-radius:8px; padding:clamp(22px,4vw,44px); box-shadow:0 20px 52px rgba(15,23,42,.08); }}
    article p {{ margin:0 0 18px; font-size:17px; }}
    article h2 {{ margin:36px 0 16px; font-size:28px; line-height:1.22; }}
    .story-kicker-line {{ color:#667085; font-weight:900; text-align:center; }}
    .end-mark, .credit-line {{ text-align:center; color:#667085; font-weight:800; }}
    figure {{ margin:28px 0; }}
    figure img {{ display:block; width:100%; height:auto; border-radius:8px; border:1px solid #e5edf3; }}
    figcaption, .caption-line {{ margin-top:8px; color:#667085; text-align:center; font-size:13px; line-height:1.45; }}
    .rail {{ position:sticky; top:18px; display:grid; gap:16px; }}
    .brief {{ background:#101828; color:#fff; border-radius:8px; padding:18px; }}
    .brief h2 {{ margin:0 0 12px; font-size:18px; }}
    .brief dl {{ display:grid; gap:12px; margin:0; }}
    .brief dt {{ color:#9ec5ff; font-size:12px; font-weight:900; text-transform:uppercase; letter-spacing:.08em; }}
    .brief dd {{ margin:2px 0 0; color:#eef4ff; font-size:14px; line-height:1.45; }}
    .related {{ background:#fff; border:1px solid var(--line); border-radius:8px; padding:18px; }}
    .related a {{ display:block; color:#0b67c2; font-weight:900; text-decoration:none; margin-top:10px; }}
    .transition {{ margin:42px 0 22px; padding-top:24px; border-top:1px solid var(--line); color:#475467; font-weight:850; }}
    @media (max-width:860px) {{
      .hero-inner, .layout {{ grid-template-columns:1fr; }}
      .rail {{ position:static; }}
      article p {{ font-size:16px; }}
    }}
  </style>
</head>
<body>
  <header class="topbar">
    <div class="topbar-inner">
      <div class="brand">Run50 <span>Facebook</span></div>
      <nav><a href="../hub.html">Run50 Hub</a><a href="../stories/english/{SLUG}.html">English</a><a href="../stories/chinese/{SLUG}.html">中文</a></nav>
    </div>
  </header>
  <section class="hero">
    <div class="hero-inner">
      <div>
        <p class="section-label">World / USA / Marathon</p>
        <h1>{escape(TITLE_FB)}</h1>
        <p class="dek">On November 5, 2022, I drove from Louisville before dawn for the 15th Indianapolis Monumental Marathon, a fast and flat downtown race that became Run50 State 5 and quietly gave me a running method I still use.</p>
        <div class="meta-row"><span>Indianapolis, IN</span><span>{DATE_EN}</span><span>Run50 #5</span><span>4:55:12 finish</span></div>
      </div>
      <img src="../../assets/{THUMB_PATH.name}?v={VERSION}" alt="Indianapolis Monumental Marathon icon cover">
    </div>
  </section>
  <main class="layout">
    <article>
      <p class="section-label">Race day</p>
      <p>The Indianapolis Monumental Marathon is exactly the kind of race that tempts a half-retired runner back out the door: big enough to feel like a city event, flat enough to feel possible, and close enough to turn into one compressed, slightly ridiculous one-day trip.</p>
{article}
    </article>
    <aside class="rail">
      <div class="brief">
        <h2>Race Brief</h2>
        <dl>
          <div><dt>Race</dt><dd>{RACE_NAME}</dd></div>
          <div><dt>Date</dt><dd>{DATE_EN}</dd></div>
          <div><dt>State</dt><dd>Indiana · Run50 #5</dd></div>
          <div><dt>Route memory</dt><dd>Downtown Indianapolis, Monument Circle, autumn rain, neighborhood aid stations, pacers, run-walk intervals and a sub-5 finish.</dd></div>
        </dl>
      </div>
      <div class="related">
        <strong>More versions</strong>
        <a href="../stories/english/{SLUG}.html">Read in original order</a>
        <a href="../stories/chinese/{SLUG}.html">中文原文整理版</a>
      </div>
    </aside>
  </main>
{engagement("en", "../../assets", f"run50-{SLUG}-facebook-en", "supabase-comments-indianapolis-facebook")}
</body>
</html>
"""


FONT_DIR = Path(r"C:\Windows\Fonts")


def font(size: int, bold: bool = False):
    names = ["arialbd.ttf", "Arial Bold.ttf"] if bold else ["arial.ttf", "Arial.ttf"]
    for name in names:
        path = FONT_DIR / name
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def draw_badge(draw, x, y, w, h):
    draw.rounded_rectangle((x, y, x + w, y + h), radius=22, fill="#ffffff", outline="#20242b", width=7)
    draw.text((x + 30, y + 48), "Run50 #05", fill="#20242b", font=font(38, True))
    draw.text((x + 30, y + 102), "INDIANA", fill="#0b67c2", font=font(48, True))


def draw_indy_scene(draw, height: int):
    scale = height / 630

    def p(x, y):
        return (int(x * scale), int(y * scale))

    sky = "#cfe9f4"
    road = "#46505c"
    grass = "#78bb61"
    gold = "#f7bc3b"
    brick = "#c65f3e"
    stone = "#e8dcc9"
    dark = "#20242b"

    draw.rectangle((0, 0, int(1200 * scale), height), fill=sky)
    draw.ellipse((p(925, 108), p(1016, 199)), fill=gold)
    draw.polygon([p(0, 430), p(320, 360), p(680, 395), p(1200, 340), p(1200, 630), p(0, 630)], fill="#9ad06d")
    draw.polygon([p(0, 470), p(520, 410), p(1200, 462), p(1200, 630), p(0, 630)], fill=grass)

    # Rain streaks stay low so the title and badge remain clear.
    for x in range(80, 1120, 95):
        draw.line((p(x, 255), p(x - 22, 330)), fill="#7aa9bd", width=max(1, int(3 * scale)))

    # Statehouse dome.
    draw.rectangle((p(118, 386), p(332, 535)), fill="#d7c5ad", outline=dark, width=max(2, int(4 * scale)))
    draw.rectangle((p(96, 535), p(354, 565)), fill="#b99068", outline=dark, width=max(2, int(4 * scale)))
    draw.pieslice((p(142, 285), p(308, 455)), 180, 360, fill="#d8b46e", outline=dark, width=max(2, int(4 * scale)))
    draw.rectangle((p(215, 264), p(235, 320)), fill="#b99068", outline=dark, width=max(2, int(3 * scale)))
    draw.polygon([p(214, 264), p(225, 238), p(236, 264)], fill=gold, outline=dark)
    for x in (140, 178, 255, 293):
        draw.rectangle((p(x, 418), p(x + 24, 526)), fill="#efe6d7", outline="#84674b", width=max(1, int(2 * scale)))

    # Soldiers and Sailors Monument.
    cx = 610
    draw.rectangle((p(cx - 42, 300), p(cx + 42, 540)), fill=stone, outline=dark, width=max(2, int(4 * scale)))
    draw.polygon([p(cx - 54, 300), p(cx, 210), p(cx + 54, 300)], fill="#d7c5ad", outline=dark)
    draw.rectangle((p(cx - 78, 535), p(cx + 78, 575)), fill="#b99068", outline=dark, width=max(2, int(4 * scale)))
    draw.ellipse((p(cx - 66, 472), p(cx + 66, 552)), fill="#efdfc7", outline=dark, width=max(2, int(4 * scale)))
    draw.text(p(cx - 24, 498), "INDY", fill=dark, font=font(max(16, int(24 * scale)), True))

    # Downtown blocks.
    for x, y, w, h, c in [
        (760, 350, 62, 160, "#b7d7e5"),
        (835, 315, 74, 195, "#f5d66c"),
        (925, 380, 54, 130, "#a7dccd"),
        (995, 340, 72, 170, "#d2c2ee"),
    ]:
        draw.rectangle((p(x, y), p(x + w, 510)), fill=c, outline="#6b7280", width=max(1, int(2 * scale)))
        for wx in range(x + 12, x + w - 8, 22):
            for wy in range(y + 18, 500, 34):
                draw.rectangle((p(wx, wy), p(wx + 9, wy + 13)), fill="#fff6bf")

    # Road and runner.
    draw.polygon([p(310, 630), p(535, 474), p(710, 474), p(970, 630)], fill=road)
    draw.line((p(621, 490), p(621, 630)), fill="#f7d35b", width=max(2, int(4 * scale)))
    x, y = 705, 470
    draw.ellipse((p(x, y), p(x + 26, y + 26)), fill="#0b67c2")
    draw.line((p(x + 13, y + 26), p(x + 8, y + 70)), fill=dark, width=max(3, int(5 * scale)))
    draw.line((p(x + 10, y + 42), p(x - 20, y + 58)), fill=dark, width=max(3, int(5 * scale)))
    draw.line((p(x + 9, y + 70), p(x - 14, y + 104)), fill=dark, width=max(3, int(5 * scale)))
    draw.line((p(x + 9, y + 70), p(x + 42, y + 96)), fill=dark, width=max(3, int(5 * scale)))


def generate_cover_png():
    image = Image.new("RGB", (1200, 630), "#cfe9f4")
    draw = ImageDraw.Draw(image)
    draw_indy_scene(draw, 630)
    draw.text((64, 64), "INDIANAPOLIS", fill="#20242b", font=font(66, True))
    draw.text((66, 136), "MONUMENT CIRCLE · FAST & FLAT", fill="#667085", font=font(26, True))
    draw_badge(draw, 760, 64, 362, 164)
    image.save(OG_PATH)


def generate_cover_svg():
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 750" width="1200" height="750" role="img" aria-labelledby="title desc">
  <title id="title">Indianapolis Monumental Marathon Run50 icon cover</title>
  <desc id="desc">Icon cover with Indianapolis monument, statehouse dome, autumn rain, downtown blocks and a Run50 Indiana badge.</desc>
  <rect width="1200" height="750" fill="#cfe9f4"/>
  <circle cx="945" cy="132" r="58" fill="#f7bc3b"/>
  <path d="M0 515 L320 435 L680 485 L1200 420 L1200 750 L0 750Z" fill="#9ad06d"/>
  <path d="M0 570 L520 500 L1200 555 L1200 750 L0 750Z" fill="#78bb61"/>
  <g stroke="#7aa9bd" stroke-width="3" opacity=".85">
    <line x1="80" y1="305" x2="55" y2="392"/><line x1="180" y1="305" x2="155" y2="392"/><line x1="280" y1="305" x2="255" y2="392"/>
    <line x1="840" y1="305" x2="815" y2="392"/><line x1="940" y1="305" x2="915" y2="392"/><line x1="1040" y1="305" x2="1015" y2="392"/>
  </g>
  <g stroke="#20242b" stroke-width="4">
    <rect x="118" y="460" width="214" height="180" fill="#d7c5ad"/>
    <rect x="96" y="640" width="258" height="36" fill="#b99068"/>
    <path d="M142 460 Q225 315 308 460Z" fill="#d8b46e"/>
    <rect x="215" y="315" width="20" height="70" fill="#b99068"/>
    <path d="M214 315 L225 285 L236 315Z" fill="#f7bc3b"/>
    <rect x="140" y="500" width="24" height="128" fill="#efe6d7" stroke="#84674b" stroke-width="2"/>
    <rect x="178" y="500" width="24" height="128" fill="#efe6d7" stroke="#84674b" stroke-width="2"/>
    <rect x="255" y="500" width="24" height="128" fill="#efe6d7" stroke="#84674b" stroke-width="2"/>
    <rect x="293" y="500" width="24" height="128" fill="#efe6d7" stroke="#84674b" stroke-width="2"/>
  </g>
  <g stroke="#20242b" stroke-width="5">
    <rect x="568" y="358" width="84" height="286" fill="#e8dcc9"/>
    <path d="M556 358 L610 250 L664 358Z" fill="#d7c5ad"/>
    <rect x="532" y="640" width="156" height="48" fill="#b99068"/>
    <ellipse cx="610" cy="606" rx="66" ry="46" fill="#efdfc7"/>
    <text x="610" y="615" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="900" fill="#20242b" stroke="none">INDY</text>
  </g>
  <g stroke="#6b7280" stroke-width="2">
    <rect x="760" y="420" width="62" height="190" fill="#b7d7e5"/><rect x="835" y="380" width="74" height="230" fill="#f5d66c"/>
    <rect x="925" y="455" width="54" height="155" fill="#a7dccd"/><rect x="995" y="408" width="72" height="202" fill="#d2c2ee"/>
  </g>
  <path d="M310 750 L535 565 L710 565 L970 750Z" fill="#46505c"/>
  <line x1="621" y1="585" x2="621" y2="750" stroke="#f7d35b" stroke-width="5"/>
  <g stroke="#20242b" stroke-width="6" fill="none">
    <circle cx="718" cy="560" r="14" fill="#0b67c2" stroke="none"/>
    <line x1="718" y1="574" x2="713" y2="630"/>
    <line x1="715" y1="594" x2="684" y2="614"/>
    <line x1="713" y1="630" x2="690" y2="675"/>
    <line x1="713" y1="630" x2="750" y2="666"/>
  </g>
  <text x="70" y="104" font-family="Arial, Helvetica, sans-serif" font-size="66" font-weight="900" fill="#20242b">INDIANAPOLIS</text>
  <text x="72" y="150" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="800" fill="#667085">MONUMENT CIRCLE · FAST &amp; FLAT</text>
  <rect x="758" y="62" width="364" height="166" rx="22" fill="#ffffff" stroke="#20242b" stroke-width="8"/>
  <text x="790" y="122" font-family="Arial, Helvetica, sans-serif" font-size="41" font-weight="900" fill="#20242b">Run50 #05</text>
  <text x="790" y="182" font-family="Arial, Helvetica, sans-serif" font-size="52" font-weight="900" fill="#0b67c2">INDIANA</text>
</svg>
'''
    THUMB_PATH.write_text(svg, encoding="utf-8")
    FB_THUMB_PATH.parent.mkdir(parents=True, exist_ok=True)
    FB_THUMB_PATH.write_text(svg, encoding="utf-8")


def generate_medal_cover():
    source = SOURCE_FILES / "640(51)"
    if not source.exists():
        source = SOURCE_FILES / "640(52)"
    with Image.open(source) as image:
        image = ImageOps.exif_transpose(image).convert("RGB")
        bg = ImageOps.fit(image, (1200, 750), method=Image.LANCZOS, centering=(0.5, 0.5))
        bg = bg.filter(ImageFilter.GaussianBlur(18))
        overlay = Image.new("RGB", (1200, 750), "#edf3f7")
        bg = Image.blend(bg, overlay, 0.2)
        fg = image.copy()
        fg.thumbnail((1080, 700), Image.LANCZOS)
        x = (1200 - fg.width) // 2
        y = (750 - fg.height) // 2
        bg.paste(fg, (x, y))
        bg.save(MEDAL_COVER_PATH, quality=92)


def clean_text(text: str) -> str:
    return "\n".join(line.rstrip() for line in text.splitlines()) + "\n"


def remove_existing_card(text: str, href: str) -> str:
    pattern = re.compile(rf'\n\s*<a class="story-card [^"]+" href="{re.escape(href)}">.*?</a>', re.S)
    return pattern.sub("", text)


def insert_after_card(text: str, target_href: str, card: str, fallback_marker: str) -> str:
    pattern = re.compile(rf'(\n\s*<a class="story-card [^"]+" href="{re.escape(target_href)}">.*?</a>\s*)', re.S)
    if pattern.search(text):
        return pattern.sub(lambda m: m.group(1) + "\n" + card, text, count=1)
    return text.replace(fallback_marker, fallback_marker + "\n" + card, 1)


def update_mapping(text: str, new_line: str, after_line: str) -> str:
    key = new_line.strip().split(":", 1)[0]
    text = re.sub(rf"\n\s*{re.escape(key)}: '.*?',", "", text)
    if new_line in text:
        return text
    return text.replace(after_line, after_line + "\n" + new_line, 1)


def update_story_indexes():
    zh_path = REPO / "run50" / "stories" / "chinese" / "index.html"
    en_path = REPO / "run50" / "stories" / "english" / "index.html"
    fb_path = REPO / "run50" / "facebook" / "index.html"

    zh_card = f"""      <a class="story-card run-50" href="./{SLUG}.html">
        <img src="../../../assets/{MEDAL_COVER_PATH.name}?v={VERSION}" alt="印第安纳波利斯纪念碑马拉松奖牌封面" loading="lazy" decoding="async">
        <div class="story-copy">
          <p class="story-meta">印第安纳印第安纳波利斯 · {DATE_ZH}</p>
          <h2 class="story-title">Run50 #第5州｜印第安纳波利斯纪念碑马拉松</h2>
          <p class="story-desc">一日狂飙去印城跑“牦牛”马：凌晨出发、秋雨开跑、纪念碑广场、430和445兔子、跑走策略，以及4小时55分12秒的回归。</p>
          <div class="story-foot"><span>长文图记</span><span>阅读 →</span></div>
        </div>
      </a>
"""
    en_card = f"""      <a class="story-card run-50" href="./{SLUG}.html">
        <img src="../../../assets/{THUMB_PATH.name}?v={VERSION}" alt="Icon cover for Indianapolis Monumental Marathon" loading="lazy" decoding="async">
        <div class="story-card-content">
          <div class="meta">Indiana · Indianapolis · {DATE_ZH}</div>
          <h2>Indianapolis Monumental Marathon: a rainy one-day run back under five</h2>
          <p>A pre-dawn drive from Louisville, autumn rain downtown, Monument Circle, pacer groups, run-walk intervals, and a 4:55:12 finish that made running feel possible again.</p>
        </div>
      </a>
"""
    fb_card = f"""    <a class="story-card run-50" href="./{SLUG}.html">
      <div>
        <p class="eyebrow">World / USA / Marathon</p>
        <h2>{escape(TITLE_FB)}</h2>
        <p>Race date: November 5, 2022. Run50 State 5 at the 15th Indianapolis Monumental Marathon: autumn rain, Monument Circle, run-walk intervals, and a 4:55:12 finish.</p>
        <div class="meta"><span>Indianapolis, IN</span><span>Run50 #5</span><span>4:55:12 finish</span></div>
      </div>
      <img src="../../assets/facebook/{THUMB_PATH.name}?v={VERSION}" alt="Icon-style Indianapolis Monumental Marathon cover">
    </a>
"""

    text = remove_existing_card(zh_path.read_text(encoding="utf-8"), f"./{SLUG}.html")
    text = insert_after_card(text, "./san-francisco-marathon.html", zh_card, '<section class="story-grid"')
    text = update_mapping(
        text,
        f"      'IN-印第安纳波利斯': '{SLUG}.html',",
        "      'CA-旧金山': 'san-francisco-marathon.html',",
    )
    text = re.sub(
        r"'IN': \[\{city: '.*?', raceName: '.*?', date: '.*?', emoji: '.*?', num: '#05', isPlaceholder: false\}\],",
        "'IN': [{city: '印第安纳波利斯', raceName: '第15届印第安纳波利斯纪念碑马拉松', date: '2022.11.05', emoji: '🏎️', num: '#05', isPlaceholder: false}],",
        text,
    )
    zh_path.write_text(clean_text(text), encoding="utf-8")

    text = remove_existing_card(en_path.read_text(encoding="utf-8"), f"./{SLUG}.html")
    text = insert_after_card(text, "./san-francisco-marathon.html", en_card, '<section class="story-grid"')
    text = update_mapping(
        text,
        f"      'IN-Indianapolis': '{SLUG}.html',",
        "      'CA-San Francisco': 'san-francisco-marathon.html',",
    )
    text = re.sub(
        r"'IN': \[\{city: 'Indianapolis', raceName: '.*?', date: '.*?', emoji: '.*?', num: '#05', isPlaceholder: false\}\],",
        "'IN': [{city: 'Indianapolis', raceName: '15th Indianapolis Monumental', date: '2022.11.05', emoji: '🏎️', num: '#05', isPlaceholder: false}],",
        text,
    )
    en_path.write_text(clean_text(text), encoding="utf-8")

    text = remove_existing_card(fb_path.read_text(encoding="utf-8"), f"./{SLUG}.html")
    text = insert_after_card(text, "./san-francisco-marathon.html", fb_card, '<main class="shell">')
    fb_path.write_text(clean_text(text), encoding="utf-8")


def update_root_home():
    path = REPO / "index.html"
    text = path.read_text(encoding="utf-8")
    text = re.sub(
        r"\n\s*<!-- Indiana Run50 story -->.*?<!-- /Indiana Run50 story -->\n",
        "\n",
        text,
        flags=re.S,
    )
    card = f"""
      <!-- Indiana Run50 story -->
      <article class="video-card" data-section="run50" data-category="run50 facebook" data-title="{escape(TITLE_FB)}">
        <a class="thumb" href="run50/facebook/{SLUG}.html">
          <img src="assets/facebook/{THUMB_PATH.name}?v={VERSION}" alt="Icon-style Indianapolis Monumental Marathon cover">
          <span class="duration">Story</span>
        </a>
        <div class="meta">
          <span class="avatar run50">50</span>
          <div>
            <a class="video-title" href="run50/facebook/{SLUG}.html">{escape(TITLE_FB)}</a>
            <p class="video-sub">Indianapolis, IN &middot; Nov 5, 2022</p>
          </div>
        </div>
      </article>
      <!-- /Indiana Run50 story -->
"""
    text = text.replace("      <!-- /San Francisco Run50 story -->\n", "      <!-- /San Francisco Run50 story -->\n" + card, 1)
    path.write_text(clean_text(text), encoding="utf-8")


def update_landing_counts():
    path = REPO / "run50" / "index.html"
    text = path.read_text(encoding="utf-8")
    text = text.replace(" 16 stories", " 17 stories")
    text = text.replace("<strong>16</strong> stories", "<strong>17</strong> stories")
    path.write_text(clean_text(text), encoding="utf-8")


def update_hub():
    path = REPO / "run50" / "hub.html"
    text = path.read_text(encoding="utf-8")
    if "'Indianapolis':{lat:39.7684,lon:-86.1581}" not in text:
        text = text.replace(
            "'San Francisco':{lat:37.7749,lon:-122.4194},'Cincinnati'",
            "'San Francisco':{lat:37.7749,lon:-122.4194},'Indianapolis':{lat:39.7684,lon:-86.1581},'Cincinnati'",
            1,
        )
    text = re.sub(r"^\s*'IN':\[\{city:'Indianapolis'.*?\}\],\n", "", text, flags=re.M)
    text = text.replace(
        "  'CA':[{city:'San Francisco',date:'Jul 24, 2022',story:'stories/english/san-francisco-marathon.html',fb:'facebook/san-francisco-marathon.html'}],",
        "  'CA':[{city:'San Francisco',date:'Jul 24, 2022',story:'stories/english/san-francisco-marathon.html',fb:'facebook/san-francisco-marathon.html'}],\n"
        "  'IN':[{city:'Indianapolis',date:'Nov 5, 2022',story:'stories/english/indianapolis-monumental-marathon.html',fb:'facebook/indianapolis-monumental-marathon.html'}],",
        1,
    )
    text = re.sub(
        r"\n\s*<!-- Indiana Indianapolis story dot -->.*?<!-- /Indiana Indianapolis story dot -->\n",
        "\n",
        text,
        flags=re.S,
    )
    dot = """
    <!-- Indiana Indianapolis story dot -->
    <circle cx="224" cy="145" r="10" fill="rgba(255,80,40,0.18)" pointer-events="none"/>
    <circle cx="224" cy="145" r="5" fill="#ff4040" stroke="#fff" stroke-width="1.6" class="wm-dot"
      data-city="Indianapolis, IN" data-date="Nov 5, 2022" data-story="stories/english/indianapolis-monumental-marathon.html"/>
    <!-- /Indiana Indianapolis story dot -->
"""
    text = text.replace("    <!-- /California San Francisco story dot -->\n", "    <!-- /California San Francisco story dot -->\n" + dot, 1)
    path.write_text(clean_text(text), encoding="utf-8")


def update_supabase_sql():
    path = REPO / "supabase" / "run50-comments.sql"
    text = path.read_text(encoding="utf-8")
    keys = [
        f"run50-{SLUG}-facebook-en",
        f"run50-{SLUG}-en",
        f"run50-{SLUG}-zh",
    ]
    for key in keys:
        text = re.sub(rf"^\s*'{re.escape(key)}',\n", "", text, flags=re.M)

    def add_keys(match):
        indent = match.group(1)
        return "".join(f"{indent}'{key}',\n" for key in keys) + match.group(0)

    text = re.sub(
        r"^(\s*)'run50-san-francisco-marathon-facebook-en',",
        add_keys,
        text,
        flags=re.M,
    )
    path.write_text(clean_text(text), encoding="utf-8")


def main():
    indexed = extract_story()
    image_count = copy_story_images(indexed)
    if image_count != 55:
        raise RuntimeError(f"Expected 55 story images, got {image_count}")

    zh_article = render_article(indexed, "zh", "Run50-Indianapolis-Monumental-Marathon-clean_files/", "印第安纳波利斯马拉松照片")
    en_article = render_article(indexed, "en", "../chinese/Run50-Indianapolis-Monumental-Marathon-clean_files/", "Indianapolis Monumental Marathon photo")
    fb_article = render_article(indexed, "en", "../stories/chinese/Run50-Indianapolis-Monumental-Marathon-clean_files/", "Indianapolis Monumental Marathon photo")

    (REPO / "run50" / "stories" / "chinese" / f"{SLUG}.html").write_text(normal_page("zh", zh_article), encoding="utf-8")
    (REPO / "run50" / "stories" / "english" / f"{SLUG}.html").write_text(normal_page("en", en_article), encoding="utf-8")
    (REPO / "run50" / "facebook" / f"{SLUG}.html").write_text(facebook_page(fb_article), encoding="utf-8")

    generate_cover_png()
    generate_cover_svg()
    shutil.copyfile(THUMB_PATH, FB_THUMB_PATH)
    generate_medal_cover()
    update_story_indexes()
    update_root_home()
    update_landing_counts()
    update_hub()
    update_supabase_sql()
    print(f"Built {SLUG}: {image_count} images, {len(indexed)} story events")


if __name__ == "__main__":
    main()
