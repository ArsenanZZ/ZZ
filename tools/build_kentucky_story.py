from pathlib import Path
from html import escape
from lxml import html
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps
import re


REPO = Path(__file__).resolve().parents[1]


SOURCE_BASE = Path(
    r"Z:\ZhennanZ Folder\000-Marathon-Story-2024-2025\20230000-Marathons\2020-State-01-KY"
)
SOURCE_HTML = next(p for p in SOURCE_BASE.iterdir() if p.suffix.lower() == ".html")
SOURCE_FILES = next(p for p in SOURCE_BASE.iterdir() if p.is_dir() and p.name.endswith("_files"))
SITE = "https://arsenanzz.github.io/ZZ"
SLUG = "louisville-marathon"
VERSION = "20260615-2"
ENGAGEMENT_VERSION = "20260615"
OUT_IMG_DIR = (
    REPO
    / "run50"
    / "stories"
    / "chinese"
    / "Run50-Louisville-Marathon-clean_files"
)
OG_PATH = REPO / "assets" / "og-run50-louisville-marathon-icons.png"
THUMB_PATH = REPO / "assets" / "thumb-run50-louisville-marathon-icons.svg"
FB_THUMB_PATH = REPO / "assets" / "facebook" / THUMB_PATH.name
MEDAL_COVER_PATH = REPO / "assets" / "cover-medal-ky.jpg"

TITLE_ZH = "Run50 #第1州｜肯塔基：路易斯维尔马拉松｜北美的第一个全马"
TITLE_EN = "Run50 #1 | Kentucky: My First Marathon in North America"
TITLE_FB = "My first North American marathon came in a locked-down Kentucky autumn"
DATE_ZH = "2020.11.08"
DATE_EN = "Nov 8, 2020"
RACE_NAME = "Louisville Marathon, Half Marathon & 10K"


TRANSLATIONS = {
    "▲ 北美第一马 by ACE": "▲ My first marathon in North America by ACE",
    "前言": "Preface",
    "2020年的第一个马拉松，比预想中来的晚了一些了，入坑四年多，回头一看，跑步200周了，也算是完成了一个不大不小的成就。": "My first marathon of 2020 came a little later than expected. I had been hooked on running for more than four years, and looking back, I had now run for 200 straight weeks. That felt like a modest but meaningful achievement.",
    "每年跑个马总是个很令人期待的事，因为2020年的无比魔幻，所以能一直keep这样节奏，就显得更加特别，虽然这个过程并不轻松。": "Running at least one marathon every year is always something I look forward to. Because 2020 had been so surreal, keeping that rhythm going felt especially meaningful, even though getting there was not easy.",
    "▲200周 by Joyrun": "▲ 200 weeks by Joyrun",
    "跑马": "The Marathon",
    "路易斯维尔马拉松是路城的第二大马拉松，也是波马的标准赛事，因为疫情的原因，比赛地点从原本的市区，挪到了几十公里外的Beckley Creek Park，其实为了这个全马，几个月前我就已经准备好了电动自行车，又买个备用电池，刚好可以cover来回的里程。": "The Louisville Marathon is the city's second-largest marathon and a Boston qualifier. Because of the pandemic, the race was moved from downtown to Beckley Creek Park, dozens of kilometers away. A few months earlier, I had actually prepared an electric bicycle for this marathon and bought a spare battery, just enough to cover the round trip.",
    "▲Beckley Creek Park by Arsenan": "▲ Beckley Creek Park by Arsenan",
    "但最近车没了，所以只好打Lyft和Uber，车费就接近100刀。另外最近也刚刚买了车，可是驾照一直没搞定，只能停在家门口，天天干瞪眼。": "But the bicycle was gone by race week, so I had to use Lyft and Uber instead. The rides cost close to $100. I had also just bought a car, but I still had not managed to get my driver's license, so it could only sit outside my home while I stared at it every day.",
    "▲Social distance by Arsenan": "▲ Social distance by Arsenan",
    "去的时候打了Lyft，司机师傅是个黑大哥，英语不咋地，也就没多聊，确实打车去跑步可比骑车轻松多了。黑大哥给我放到停车场，不用看地图，寻着马拉松起点处的音乐，就可以轻松定位。": "I took a Lyft there. The driver was a Black guy whose English was not great, so we did not talk much. Taking a car to a race was definitely easier than riding a bicycle. He dropped me in the parking lot, and I did not even need a map. I just followed the music from the marathon start.",
    "▲ 间隔起跑 by ACE": "▲ Staggered start by ACE",
    "起点处换了衣服，然后把包扔给了美国大兵，虽然这个比赛并没存包处，但大兵们还是答应帮着保管。": "I changed clothes near the start and left my bag with a few American service members. The race did not officially offer bag check, but they still agreed to look after it for me.",
    "起点是间隔起跑，人群聚集处都要戴口罩，我被分到8点24分出发，大家排着队，人和人之间都要6 feet的social distance，毕竟在疫情破千万的美国，能在这个时候举办马拉松已经很难得了。": "The race used staggered starts, and masks were required anywhere people gathered. My assigned start time was 8:24. Everyone stood in line with six feet of social distance between us. With U.S. COVID cases already past ten million, simply being able to hold a marathon at that moment was remarkable.",
    "▲ 又能跑步乐坏了 by ACE": "▲ Thrilled to be racing again by ACE",
    "明显跑者们也都憋坏了，那股兴奋劲是藏不住的。": "The runners had clearly been cooped up for too long. Nobody could hide the excitement.",
    "我这个队排的是真不错，轮到我出发刚好8点24，小风一吹，小腿一迈，这个马拉松算是跑起来了。": "My line moved with impressive precision. My turn came at exactly 8:24. A light breeze blew, I took the first step, and the marathon was finally underway.",
    "▲ 我前面的小伙 by ACE": "▲ The guy in front of me by ACE",
    "▲ 出发 by ACE": "▲ Starting out by ACE",
    "天气很棒，温度20℃上下，很适合跑步，除了没啥观众，一切都挺好，前几公里是一段水泥路，由于远离市区，基本没车，刚起跑很轻松，我甚至抽空去了趟厕所。": "The weather was excellent, around 20°C, just right for running. Other than the lack of spectators, everything felt good. The first few kilometers followed a paved road with almost no traffic because we were far from downtown. The opening felt easy enough that I even took time for a bathroom stop.",
    "▲ 飒 by ACE": "▲ Looking sharp by ACE",
    "水泥路之后进入小树林，跑步这天刚好是中国农历的立冬，路城也过了TA最美的时候，树的叶子也都快掉没了。我跟在一美国大叔后面，储存体力，虽然状态还行，但是毕竟好久没有跑全马，后面才是真正的考验。": "After the paved road, the course entered a small forest. Race day happened to be Lidong, the traditional Chinese beginning of winter. Louisville had already passed its prettiest autumn moment, and most of the leaves were nearly gone. I followed an older American runner and conserved energy. I felt all right, but I had not run a full marathon in a long time. The real test would come later.",
    "▲ 温馨 by ACE": "▲ A warm little scene by ACE",
    "10公里处我补了一条能量胶，这个活动补给点还真不少，虽然和国内那种流水席一样的补给比，确实寒酸了不少，只有水和饮料，偶尔有能量胶，但对我来说也足够了。": "At 10 kilometers, I took an energy gel. The race actually had plenty of aid stations. Compared with the banquet-like spreads at races in China, they were undeniably sparse: just water and sports drink, with an occasional gel. Still, that was enough for me.",
    "▲ 补给点 by Arsenan": "▲ Aid station by Arsenan",
    "公园里的风景比较单一，并没有太多的点值得停下拍照，偶尔路过不算精致的水塘和铁桥，也没有太大的吸引力让人回头多看一眼。": "The park scenery was fairly repetitive, with few places worth stopping to photograph. An ordinary pond or iron bridge appeared now and then, but nothing really made me turn around for another look.",
    "▲ 补水塘 by Arsenan": "▲ A little watering hole by Arsenan",
    "状态很平稳的接近半程终点，前面是一段很长的上坡，明显感觉腿很重，有点吃力。但这时，突然听到有人给我鼓劲，回头一看是一华人阿姨，旁边应该是她的美国老公，瞬间油箱又有油了。": "I approached the halfway point in a steady rhythm. A long uphill stretch appeared ahead, and my legs suddenly felt heavy. Then I heard someone cheering for me. I turned and saw a Chinese auntie with what was probably her American husband beside her. My fuel tank instantly felt full again.",
    "▲ 接近半程的森林 by Arsenan": "▲ Forest near halfway by Arsenan",
    "半程折返，有一个补给点，没什么特别的仪式，我一口气吃了两条能量胶，真正的考验才开始。": "There was an aid station at the halfway turnaround, with no special ceremony. I ate two gels in one go. The real test was only beginning.",
    "经历了刚才的爬坡，刚回去那会儿还真挺舒服，赛道穿梭在小森林里，不冷不热，太阳也不晃眼，舒舒服服的来到25公里。": "After the climb, the first part of the return felt genuinely comfortable. The course wound through the woods, neither cold nor hot, and the sun was not glaring. I reached 25 kilometers feeling relaxed.",
    "▲ 回程正午大太阳 by Arsenan": "▲ Bright noon sun on the way back by Arsenan",
    "一般来说25公里到35公里算是马拉松里最艰难的时候，我这会儿状态还行，耳机里是康姆士的《你要如何我们就如何》，听着主唱永驻的塑料普通话，瞬间似乎回到了那段在新加坡曼谷跑马的经历，我以为只是我脑路清奇，穿越了一下。": "The stretch from 25 to 35 kilometers is usually the hardest part of a marathon, but I was still doing all right. In my headphones was Kangmushi's song \"However You Want Us to Be.\" Hearing the singer's permanently charming, slightly offbeat Mandarin suddenly took me back to running marathons in Singapore and Bangkok. I thought it was just my strange brain traveling through time for a moment.",
    "▲ 回程拍的一个还不错的照片 by Arsenan": "▲ A pretty decent photo from the return by Arsenan",
    "但当我回过神来才发现这不仅仅是穿越，跑出了阴凉地带，正午温度直线上升，还真有点东南亚跑马的感觉，终于在30公里处，我的参赛模式从跑变成了走。": "But when I came back to the present, I realized it was more than a memory. Once I left the shade, the noon temperature climbed quickly, and it really did feel a little like racing in Southeast Asia. At 30 kilometers, my race mode finally changed from running to walking.",
    "▲ 小绿和铁桥 by Arsenan": "▲ A runner in green and the iron bridge by Arsenan",
    "好久没跑这个距离，后面十几公里确实挺艰难的，我跟在两个小绿女生后面，跑跑走走，我们就这样一会我超过了她们，一会她们又超过了我，大家都快没油了，只能勉强一路向前。": "I had not covered this distance in a long time, and the final dozen kilometers were genuinely hard. I followed two women in green, alternating between running and walking. Sometimes I passed them, then they passed me again. All of us were nearly out of fuel and could only keep inching forward.",
    "▲ 两个美国女孩 by Arsenan": "▲ Two American women by Arsenan",
    "35公里多，两个美国女孩给我加油，说我可以跟着她们，我也做了尝试，但是真是跑不动，挥手表达感谢，继续向前走，这会太阳很大，立冬还这么热，真的没想到。": "After 35 kilometers, the two American women encouraged me and said I could stay with them. I tried, but I truly could not keep running. I waved my thanks and continued walking. The sun was intense by then. I had never expected the beginning of winter to feel this hot.",
    "▲ 给妈妈加油的标语 by ACE": "▲ A cheer sign for Mom by ACE",
    "40公里，遇到一个亚裔小哥和一个美国大妈，大家互相鼓励着跑跑走走来到终点。音乐声很大，但因为疫情，也并不热烈。": "At 40 kilometers, I met a young Asian runner and an older American woman. We encouraged one another and alternated running and walking until the finish. The music was loud, but because of the pandemic, the atmosphere was not especially lively.",
    "▲ 亚裔小哥 by ACE": "▲ The young Asian runner by ACE",
    "奖牌很好看，回去找包发现美国大兵已经撤退了，不过我的包还在，之后帮着大妈拍了几个照片，算是完成了这场并不轻松的全马。": "The medal looked great. When I went back for my bag, the service members had already left, but the bag was still there. I then helped the older woman take a few photos. With that, this difficult marathon was complete.",
    "▲ 跑到模糊 by ACE": "▲ Running myself into a blur by ACE",
    "▲ 奖牌 by Arsenan": "▲ Medal by Arsenan",
    "简单拉伸之后，我躺在草坪上看着天，虽然身体到处酸痛，但倍儿满足，在2020年，这样一个特殊的年份，还可以坚持每年跑个全马的小目标，也是一件值得骄傲的事。": "After a little stretching, I lay on the grass and looked at the sky. My whole body ached, but I felt deeply satisfied. In a year as unusual as 2020, keeping my small goal of running a marathon every year was something worth being proud of.",
    "▲ 赛后 by Arsenan": "▲ After the race by Arsenan",
    "后记": "Postscript",
    "等了半个小时的Uber，终于可以回家了，车窗外面偶尔晃过Biden&Harris的竞选标语，第一次以亲历者的身份感受美国的election day，一切都很新鲜，我经历过川普时期政策的打压，真切感受到小人物在大时代背景下深深的无力感，所以也会感叹自己足够幸运，还有机会经历这个节点下美国的社会变革。": "After waiting half an hour for an Uber, I could finally go home. Biden and Harris campaign signs occasionally passed outside the window. Experiencing a U.S. election as someone actually living here was completely new to me. I had felt the pressure of Trump-era policies and understood how powerless an ordinary person could feel against the background of a much larger era. I also felt fortunate to have the chance to witness American society changing at this particular moment.",
    "▲ 跑者：Dr. Jill Biden by Rebecca": "▲ Runner: Dr. Jill Biden by Rebecca",
    "作为跑步爱好者，我对准first lady充满好感，最后还是想说，不论新政怎样，都希望一切会越来越好。": "As a fellow runner, I already felt warmly toward the soon-to-be First Lady. In the end, whatever the new administration might bring, I simply hoped things would keep getting better.",
    "- 本文完 -": "- End -",
    "文字丨Arsenan": "Words | Arsenan",
    "摄影丨Arsenan": "Photos | Arsenan",
    "设计丨Arsenan": "Design | Arsenan",
}


def norm(value: str) -> str:
    return re.sub(r"\s+", " ", value.replace("\xa0", " ")).strip()


def is_styleish(value: str) -> bool:
    return ":host {" in value or "--weui-" in value or len(value) > 1200


def has_desc_leaf_container(el) -> bool:
    for desc in el.iterdescendants():
        if desc.tag in ("p", "section"):
            text = norm("".join(desc.itertext()))
            if text and not is_styleish(text):
                return True
    return False


def is_caption(text: str) -> bool:
    return text.startswith("▲")


def extract_story():
    doc = html.fromstring(SOURCE_HTML.read_text(encoding="utf-8", errors="replace"))
    roots = doc.xpath('//*[@id="js_content"]')
    root = roots[0] if roots else doc
    events = []

    def walk(el):
        if el.tag == "img":
            src = el.get("src") or el.get("data-src") or ""
            if src:
                events.append({"type": "img", "src": src})
            return
        if el.tag in ("p", "section"):
            text = norm("".join(el.itertext()))
            if text and not is_styleish(text) and not has_desc_leaf_container(el):
                if text != "，赞" and not text.startswith("鲜花"):
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
    for event in events:
        key = (event["type"], event.get("text") or event.get("src"))
        previous = (
            (clean[-1]["type"], clean[-1].get("text") or clean[-1].get("src"))
            if clean
            else None
        )
        if previous != key:
            clean.append(event)

    start = next(
        (i for i, event in enumerate(clean) if event["type"] == "img"),
        0,
    )
    end = next(
        (
            i + 1
            for i, event in enumerate(clean)
            if event["type"] == "text" and event["text"] == "设计丨Arsenan"
        ),
        len(clean),
    )
    story = clean[start:end]
    source_texts = [event["text"] for event in story if event["type"] == "text"]
    missing = sorted({text for text in source_texts if text not in TRANSLATIONS})
    if missing:
        raise RuntimeError("Missing English translations:\n" + "\n".join(missing))
    return story


def local_source_path(src: str) -> Path:
    normalized = src.split("?", 1)[0]
    if normalized.startswith("./"):
        normalized = normalized[2:]
    candidate = SOURCE_BASE / normalized
    if candidate.exists():
        return candidate
    fallback = SOURCE_FILES / Path(normalized).name
    if fallback.exists():
        return fallback
    raise FileNotFoundError(f"Missing image source: {src}")


def copy_story_images(events):
    OUT_IMG_DIR.mkdir(parents=True, exist_ok=True)
    for old in OUT_IMG_DIR.glob("img-*.webp"):
        old.unlink()
    count = 0
    for event in events:
        if event["type"] != "img":
            continue
        count += 1
        out_name = f"img-{count:03d}.webp"
        with Image.open(local_source_path(event["src"])) as image:
            image = ImageOps.exif_transpose(image)
            if image.mode != "RGB":
                image = image.convert("RGB")
            image.save(OUT_IMG_DIR / out_name, "WEBP", quality=90, method=4)
        event["out"] = out_name
    return count


def clean_caption(text: str, lang: str) -> str:
    value = TRANSLATIONS[text] if lang == "en" else text
    return value.lstrip("▲").strip()


def figure_html(src: str, caption: str, alt_base: str) -> str:
    alt = caption or alt_base
    figcaption = f"<figcaption>{escape(caption)}</figcaption>" if caption else ""
    return (
        f'<figure><img src="{escape(src)}" alt="{escape(alt)}" '
        f'loading="lazy" decoding="async">{figcaption}</figure>'
    )


def render_text(text: str, lang: str) -> str:
    value = TRANSLATIONS[text] if lang == "en" else text
    if value in ("Preface", "Postscript", "前言", "后记"):
        return f'<h2 class="section-label">{escape(value)}</h2>'
    if value in ("The Marathon", "跑马"):
        return f"<h2>{escape(value)}</h2>"
    if value.startswith("- "):
        return f'<p class="end-mark">{escape(value)}</p>'
    if value.startswith(("Words |", "Photos |", "Design |", "文字丨", "摄影丨", "设计丨")):
        return f'<p class="credit-line">{escape(value)}</p>'
    return f"<p>{escape(value)}</p>"


def render_article(events, lang: str, image_prefix: str, alt_base: str) -> str:
    parts = []
    i = 0
    pending_caption = ""
    while i < len(events):
        event = events[i]
        if event["type"] == "img":
            caption = pending_caption
            pending_caption = ""
            if (
                i + 1 < len(events)
                and events[i + 1]["type"] == "text"
                and is_caption(events[i + 1]["text"])
            ):
                caption = clean_caption(events[i + 1]["text"], lang)
                i += 1
            parts.append(
                figure_html(image_prefix + event["out"], caption, alt_base)
            )
        elif is_caption(event["text"]):
            if i + 1 < len(events) and events[i + 1]["type"] == "img":
                pending_caption = clean_caption(event["text"], lang)
        else:
            parts.append(render_text(event["text"], lang))
        i += 1
    return "\n      ".join(parts)


def split_sections(events):
    race = next(
        i
        for i, event in enumerate(events)
        if event["type"] == "text" and event["text"] == "跑马"
    )
    post = next(
        i
        for i, event in enumerate(events)
        if event["type"] == "text" and event["text"] == "后记"
    )
    return {
        "lead": events[:2],
        "foreword": events[2:race],
        "race": events[race:post],
        "post": events[post:],
    }


def existing_css(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    match = re.search(r"<style>(.*?)</style>", text, re.S)
    if not match:
        raise RuntimeError(f"Could not find inline CSS in {path}")
    return match.group(1)


def page_css() -> str:
    return existing_css(
        REPO / "run50" / "stories" / "english" / "chicago-marathon.html"
    )


def facebook_css() -> str:
    return existing_css(REPO / "run50" / "facebook" / "chicago-marathon.html")


def engagement_block(locale: str, page_key: str, comment_id: str, rel: str) -> str:
    if locale == "zh-CN":
        kicker = "留言 / 阅读"
        heading = "跑完以后，说两句"
        note = "不用登录也可以留言。新留言会直接显示。"
        views = "阅读"
        loading = "留言加载中..."
    else:
        kicker = "Comments / Views"
        heading = "Say something after the run"
        note = "No account is needed to submit a comment. New comments appear right away."
        views = "Views"
        loading = "Loading comments..."
    return f"""
    <section class="zz-engagement" data-zz-engagement data-locale="{locale}" data-page-key="{page_key}">
      <div class="zz-engagement-shell">
        <div>
          <p class="zz-engagement-kicker">{kicker}</p>
          <h2>{heading}</h2>
          <p class="zz-engagement-note">{note}</p>
          <div class="zz-engagement-stats">
            <span class="zz-engagement-stat" id="busuanzi_container_page_pv">
              <span>{views}</span>
              <strong id="busuanzi_value_page_pv" data-zz-view-count>--</strong>
            </span>
          </div>
        </div>
        <div class="zz-engagement-card">
          <div id="{comment_id}" data-zz-supabase-comments></div>
          <p class="zz-engagement-status" data-zz-engagement-status>{loading}</p>
        </div>
      </div>
    </section>
    <script src="{rel}/zz-engagement-config.js?v={ENGAGEMENT_VERSION}"></script>
    <script src="{rel}/zz-engagement.js?v={ENGAGEMENT_VERSION}"></script>
    """.strip()


def story_page(lang: str, article: str) -> str:
    is_zh = lang == "zh"
    title = TITLE_ZH if is_zh else TITLE_EN
    description = (
        "2020年11月8日，疫情中的路易斯维尔马拉松搬到Beckley Creek Park。间隔起跑、六英尺社交距离、正午高温，以及我在北美完成的第一个全马。"
        if is_zh
        else "On November 8, 2020, the pandemic-era Louisville Marathon moved to Beckley Creek Park: staggered starts, six feet of distance, a hot final 12 kilometers, and my first marathon in North America."
    )
    nav = (
        '<a href="./index.html">← 中文故事</a><a href="../english/louisville-marathon.html">English</a><a href="../../facebook/louisville-marathon.html">Facebook</a><a href="../../index.html">Run50</a>'
        if is_zh
        else '<a href="./index.html">← English Stories</a><a href="../chinese/louisville-marathon.html">中文</a><a href="../../facebook/louisville-marathon.html">Facebook</a><a href="../../index.html">Run50</a>'
    )
    meta = (
        '<span>路易斯维尔 · 肯塔基</span><span>2020.11.08</span><span>Run50 #第1州</span><span>北美第一个全马</span>'
        if is_zh
        else '<span>Louisville, Kentucky</span><span>Nov 8, 2020</span><span>Run50 #1</span><span>First North American marathon</span>'
    )
    kicker = "Run50 Stories · 肯塔基" if is_zh else "Run50 Stories · Kentucky"
    lang_attr = "zh-CN" if is_zh else "en"
    page_key = f"run50-{SLUG}-zh" if is_zh else f"run50-{SLUG}-en"
    comment_id = (
        "supabase-comments-louisville-zh"
        if is_zh
        else "supabase-comments-louisville-en"
    )
    filename = (
        "chinese/louisville-marathon.html"
        if is_zh
        else "english/louisville-marathon.html"
    )
    footer = (
        "Run50 · 肯塔基 · 路易斯维尔马拉松"
        if is_zh
        else "Run50 · Kentucky · Louisville Marathon"
    )
    return f"""<!DOCTYPE html>
<html lang="{lang_attr}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{escape(title)}</title>
  <meta name="description" content="{escape(description)}">
  <meta property="og:type" content="article">
  <meta property="og:title" content="{escape(title)}">
  <meta property="og:description" content="{escape(description)}">
  <meta property="og:image" content="{SITE}/assets/og-run50-louisville-marathon-icons.png?v={VERSION}">
  <meta property="og:url" content="{SITE}/run50/stories/{filename}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:image" content="{SITE}/assets/og-run50-louisville-marathon-icons.png?v={VERSION}">
  <link rel="stylesheet" href="../../../assets/zz-engagement.css?v={ENGAGEMENT_VERSION}">
  <style>{page_css()}</style>
</head>
<body>
  <nav class="story-nav">{nav}</nav>
  <header class="page-header">
    <p class="kicker">{kicker}</p>
    <h1>{escape(title)}</h1>
    <div class="meta">{meta}</div>
    <p class="dek">{escape(description)}</p>
  </header>
  <main class="article-shell">
    <article class="article-body">
      {article}
    </article>
    {engagement_block('zh-CN' if is_zh else 'en', page_key, comment_id, '../../../assets')}
  </main>
  <footer class="page-footer">{footer}</footer>
</body>
</html>
"""


def facebook_page(article: str) -> str:
    description = (
        "My first marathon in North America: a socially distanced Louisville race "
        "through Beckley Creek Park in November 2020, with the complete original story and photos."
    )
    fb_css = facebook_css().replace("--red: #cc0000;", "--red: #0b67c2;")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{escape(TITLE_FB)}</title>
  <meta name="description" content="{escape(description)}">
  <meta property="og:type" content="article">
  <meta property="og:title" content="{escape(TITLE_FB)}">
  <meta property="og:description" content="{escape(description)}">
  <meta property="og:image" content="{SITE}/assets/og-run50-louisville-marathon-icons.png?v={VERSION}">
  <meta property="og:url" content="{SITE}/run50/facebook/louisville-marathon.html">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:image" content="{SITE}/assets/og-run50-louisville-marathon-icons.png?v={VERSION}">
  <link rel="stylesheet" href="../../assets/zz-engagement.css?v={ENGAGEMENT_VERSION}">
  <style>{fb_css}</style>
</head>
<body>
  <div class="topbar"><span>Run50 Facebook</span><span>Race date: Nov 8, 2020</span></div>
  <header class="masthead">
    <div class="brand">Run50 / USA / Marathon</div>
    <h1>{escape(TITLE_FB)}</h1>
    <p class="summary">On November 8, 2020, I reached the start line at Beckley Creek Park for State 1 of Run50 and my first marathon in North America. Masks, staggered starts and six-foot gaps made it unmistakably 2020; the final miles under a surprisingly hot winter sun made it unmistakably a marathon.</p>
    <div class="meta-row"><span>Louisville, Kentucky</span><span>Run50 #1</span><span>First North American marathon</span><span>Full story</span></div>
  </header>
  <main class="content-grid">
    <article class="article-body">
      {article}
    </article>
    <aside class="rail">
      <h2>Why this one matters</h2>
      <p>This was the first state on my Run50 map and my first full marathon after moving to North America.</p>
      <p>The race left downtown during the pandemic and became a quiet out-and-back through Beckley Creek Park.</p>
      <a href="../stories/english/louisville-marathon.html">Read the story in its original order</a>
    </aside>
    {engagement_block('en', f'run50-{SLUG}-facebook-en', 'supabase-comments-louisville-facebook', '../../assets')}
  </main>
</body>
</html>
"""


def facebook_article(sections) -> str:
    prefix = "../stories/chinese/Run50-Louisville-Marathon-clean_files/"
    lead = render_article(sections["lead"], "en", prefix, "Louisville Marathon photo")
    race = render_article(sections["race"], "en", prefix, "Louisville Marathon photo")
    foreword = render_article(
        sections["foreword"], "en", prefix, "Louisville Marathon photo"
    )
    post = render_article(sections["post"], "en", prefix, "Louisville Marathon photo")
    return "\n      ".join(
        [
            '<p class="lede">The Louisville Marathon normally belongs to the city. In 2020, COVID pushed it out to Beckley Creek Park, where runners started one at a time behind masks and six-foot gaps. It was a strange setting for a milestone, but it became my first marathon in North America and the first state on my Run50 map.</p>',
            lead,
            race,
            '<p class="bridge-note">That finish carried more than 26.2 miles. It also completed a small promise I had been trying to keep through an impossible year, so the story now rewinds to the 200 weeks of running that brought me to the start.</p>',
            foreword,
            post,
        ]
    )


def font(size: int, bold: bool = False):
    name = "arialbd.ttf" if bold else "arial.ttf"
    path = Path("C:/Windows/Fonts") / name
    return ImageFont.truetype(str(path), size) if path.exists() else ImageFont.load_default()


def draw_badge(draw, x, y, w, h):
    draw.rounded_rectangle(
        [x, y, x + w, y + h],
        radius=26,
        fill="#ffffff",
        outline="#8fb2cc",
        width=3,
    )
    draw.text(
        (x + w / 2, y + 37),
        "Run50 #01",
        fill="#1f2937",
        font=font(34, True),
        anchor="mm",
    )
    draw.text(
        (x + w / 2, y + 86),
        "KENTUCKY",
        fill="#0b67c2",
        font=font(31, True),
        anchor="mm",
    )


def draw_louisville_scene(draw, height: int):
    scale = height / 630

    def point(x, y):
        return (int(x * scale), int(y * scale))

    width = int(1200 * scale)
    draw.rectangle([0, int(365 * scale), width, height], fill="#8fc8dc")
    draw.polygon(
        [
            point(0, 420),
            point(170, 348),
            point(340, 405),
            point(530, 330),
            point(740, 410),
            point(930, 340),
            point(1200, 410),
            point(1200, 630),
            point(0, 630),
        ],
        fill="#82b85a",
    )
    draw.rectangle([0, int(530 * scale), width, height], fill="#4c9ab5")
    draw.rectangle([0, int(580 * scale), width, height], fill="#367b96")

    bridge_y = int(420 * scale)
    draw.line([point(75, 455), point(1115, 420)], fill="#304454", width=max(3, int(10 * scale)))
    draw.line([point(75, 478), point(1115, 443)], fill="#304454", width=max(2, int(6 * scale)))
    for x in range(110, 1110, 100):
        draw.line(
            [point(x, 447), point(x + 18, 480)],
            fill="#304454",
            width=max(2, int(4 * scale)),
        )

    # Churchill Downs-inspired twin spires as the Louisville city signal.
    draw.rectangle([int(710 * scale), int(310 * scale), int(940 * scale), int(475 * scale)], fill="#f2eee6", outline="#6f7f89", width=max(2, int(3 * scale)))
    draw.rectangle([int(738 * scale), int(260 * scale), int(782 * scale), int(475 * scale)], fill="#f7f3ea", outline="#6f7f89", width=max(2, int(3 * scale)))
    draw.rectangle([int(868 * scale), int(260 * scale), int(912 * scale), int(475 * scale)], fill="#f7f3ea", outline="#6f7f89", width=max(2, int(3 * scale)))
    draw.polygon([point(734, 260), point(760, 214), point(786, 260)], fill="#c74d3d", outline="#6f3430")
    draw.polygon([point(864, 260), point(890, 214), point(916, 260)], fill="#c74d3d", outline="#6f3430")
    draw.ellipse([int(754 * scale), int(229 * scale), int(766 * scale), int(241 * scale)], fill="#e9c75e")
    draw.ellipse([int(884 * scale), int(229 * scale), int(896 * scale), int(241 * scale)], fill="#e9c75e")
    for x in (735, 790, 845, 900):
        draw.rectangle([int(x * scale), int(350 * scale), int((x + 22) * scale), int(385 * scale)], fill="#8fb8c8")

    # Running horse silhouette.
    draw.ellipse([int(230 * scale), int(365 * scale), int(440 * scale), int(455 * scale)], fill="#70452f")
    draw.polygon([point(382, 365), point(430, 338), point(462, 405), point(395, 432)], fill="#70452f")
    draw.ellipse([int(415 * scale), int(338 * scale), int(485 * scale), int(392 * scale)], fill="#70452f")
    draw.ellipse([int(464 * scale), int(359 * scale), int(510 * scale), int(389 * scale)], fill="#80523a")
    draw.polygon([point(432, 342), point(440, 318), point(452, 346)], fill="#70452f")
    draw.polygon([point(451, 340), point(462, 320), point(469, 350)], fill="#70452f")
    draw.line([point(260, 438), point(210, 515)], fill="#5a3425", width=max(4, int(13 * scale)))
    draw.line([point(320, 440), point(365, 520)], fill="#5a3425", width=max(4, int(13 * scale)))
    draw.line([point(390, 430), point(468, 492)], fill="#5a3425", width=max(4, int(13 * scale)))
    draw.line([point(275, 430), point(180, 460)], fill="#5a3425", width=max(4, int(11 * scale)))
    draw.arc([int(175 * scale), int(350 * scale), int(270 * scale), int(450 * scale)], 115, 265, fill="#4b2d20", width=max(3, int(10 * scale)))
    draw.ellipse([int(456 * scale), int(350 * scale), int(464 * scale), int(358 * scale)], fill="#111827")
    draw.rectangle([int(302 * scale), int(360 * scale), int(386 * scale), int(390 * scale)], fill="#0b67c2")
    draw.polygon([point(330, 365), point(350, 305), point(384, 312), point(382, 370)], fill="#205d8f")
    draw.ellipse([int(342 * scale), int(278 * scale), int(378 * scale), int(314 * scale)], fill="#d9a27d")
    draw.pieslice([int(337 * scale), int(270 * scale), int(383 * scale), int(307 * scale)], 180, 360, fill="#1f2937")
    draw.line([point(365, 325), point(420, 360)], fill="#d9a27d", width=max(3, int(8 * scale)))


def generate_cover_png():
    image = Image.new("RGB", (1200, 630), "#edf3f7")
    draw = ImageDraw.Draw(image)
    draw_louisville_scene(draw, 630)
    draw.rectangle([0, 0, 1200, 205], fill="#edf3f7")
    draw.text((64, 70), "LOUISVILLE", fill="#20303d", font=font(72, True))
    draw.text(
        (68, 148),
        "DERBY CITY · FIRST NORTH AMERICAN MARATHON",
        fill="#536a79",
        font=font(24, True),
    )
    draw_badge(draw, 844, 58, 278, 118)
    image.save(OG_PATH, "PNG")


def generate_cover_svg():
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 750" role="img" aria-labelledby="title desc">
  <title id="title">Louisville Marathon Run50 icon cover</title>
  <desc id="desc">Louisville icon cover with a running horse, twin spires, park hills, river bridge and a Kentucky Run50 badge.</desc>
  <rect width="1200" height="750" fill="#edf3f7"/>
  <rect y="420" width="1200" height="330" fill="#8fc8dc"/>
  <path d="M0 500 L170 414 L340 482 L530 390 L740 488 L930 404 L1200 492 V750 H0Z" fill="#82b85a"/>
  <rect y="626" width="1200" height="124" fill="#4c9ab5"/>
  <rect y="696" width="1200" height="54" fill="#367b96"/>
  <text x="64" y="112" fill="#20303d" font-family="Arial, Helvetica, sans-serif" font-size="72" font-weight="900">LOUISVILLE</text>
  <text x="68" y="160" fill="#536a79" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="800">DERBY CITY · FIRST NORTH AMERICAN MARATHON</text>
  <rect x="844" y="58" width="278" height="118" rx="26" fill="#fff" stroke="#8fb2cc" stroke-width="3"/>
  <text x="983" y="101" text-anchor="middle" fill="#1f2937" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="900">Run50 #01</text>
  <text x="983" y="150" text-anchor="middle" fill="#0b67c2" font-family="Arial, Helvetica, sans-serif" font-size="31" font-weight="900">KENTUCKY</text>
  <g stroke="#304454" stroke-linecap="round">
    <line x1="75" y1="540" x2="1115" y2="498" stroke-width="10"/>
    <line x1="75" y1="567" x2="1115" y2="525" stroke-width="6"/>
    <g stroke-width="4">
      <line x1="110" y1="530" x2="128" y2="570"/><line x1="210" y1="526" x2="228" y2="566"/>
      <line x1="310" y1="522" x2="328" y2="562"/><line x1="410" y1="518" x2="428" y2="558"/>
      <line x1="510" y1="514" x2="528" y2="554"/><line x1="610" y1="510" x2="628" y2="550"/>
      <line x1="710" y1="506" x2="728" y2="546"/><line x1="810" y1="502" x2="828" y2="542"/>
      <line x1="910" y1="498" x2="928" y2="538"/><line x1="1010" y1="494" x2="1028" y2="534"/>
    </g>
  </g>
  <g stroke="#6f7f89" stroke-width="3">
    <rect x="710" y="356" width="230" height="196" fill="#f2eee6"/>
    <rect x="738" y="296" width="44" height="256" fill="#f7f3ea"/>
    <rect x="868" y="296" width="44" height="256" fill="#f7f3ea"/>
  </g>
  <path d="M734 296 L760 240 L786 296Z" fill="#c74d3d" stroke="#6f3430" stroke-width="3"/>
  <path d="M864 296 L890 240 L916 296Z" fill="#c74d3d" stroke="#6f3430" stroke-width="3"/>
  <circle cx="760" cy="258" r="7" fill="#e9c75e"/><circle cx="890" cy="258" r="7" fill="#e9c75e"/>
  <g fill="#8fb8c8"><rect x="735" y="405" width="22" height="35"/><rect x="790" y="405" width="22" height="35"/><rect x="845" y="405" width="22" height="35"/><rect x="900" y="405" width="22" height="35"/></g>
  <g fill="#70452f" stroke="#5a3425" stroke-linecap="round">
    <ellipse cx="335" cy="504" rx="105" ry="45" stroke="none"/>
    <path d="M382 455 L430 420 L462 505 L395 532Z" stroke="none"/>
    <ellipse cx="450" cy="448" rx="36" ry="28" stroke="none"/>
    <ellipse cx="487" cy="468" rx="24" ry="15" fill="#80523a" stroke="none"/>
    <path d="M432 424 L440 394 L452 430Z" stroke="none"/><path d="M451 422 L462 397 L469 434Z" stroke="none"/>
    <line x1="260" y1="532" x2="210" y2="620" stroke-width="13"/>
    <line x1="320" y1="534" x2="365" y2="625" stroke-width="13"/>
    <line x1="390" y1="524" x2="478" y2="592" stroke-width="13"/>
    <line x1="275" y1="524" x2="180" y2="558" stroke-width="11"/>
    <path d="M242 476 Q185 438 190 520" fill="none" stroke="#4b2d20" stroke-width="10"/>
  </g>
  <circle cx="458" cy="444" r="4" fill="#111827"/>
  <rect x="302" y="451" width="84" height="30" fill="#0b67c2"/>
  <path d="M330 456 L350 382 L384 390 L382 462Z" fill="#205d8f"/>
  <circle cx="360" cy="365" r="18" fill="#d9a27d"/>
  <path d="M337 360 Q360 330 383 360Z" fill="#1f2937"/>
  <line x1="365" y1="402" x2="420" y2="446" stroke="#d9a27d" stroke-width="8" stroke-linecap="round"/>
</svg>
"""
    THUMB_PATH.write_text(svg, encoding="utf-8")
    FB_THUMB_PATH.parent.mkdir(parents=True, exist_ok=True)
    FB_THUMB_PATH.write_text(svg, encoding="utf-8")


def generate_medal_cover():
    source_path = OUT_IMG_DIR / "img-022.webp"
    with Image.open(source_path) as source:
        source = ImageOps.exif_transpose(source).convert("RGB")
        background = ImageOps.fit(
            source,
            (1200, 750),
            method=Image.Resampling.LANCZOS,
        ).filter(ImageFilter.GaussianBlur(28))
        background = Image.blend(
            background,
            Image.new("RGB", background.size, "#12304a"),
            0.32,
        )
        foreground = ImageOps.contain(
            source,
            (1080, 710),
            method=Image.Resampling.LANCZOS,
        )

    canvas = background.convert("RGBA")
    x = (canvas.width - foreground.width) // 2
    y = (canvas.height - foreground.height) // 2
    shadow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.rounded_rectangle(
        [x + 12, y + 16, x + foreground.width + 12, y + foreground.height + 16],
        radius=18,
        fill=(3, 12, 22, 115),
    )
    shadow = shadow.filter(ImageFilter.GaussianBlur(16))
    canvas.alpha_composite(shadow)
    canvas.paste(foreground, (x, y))
    canvas.convert("RGB").save(MEDAL_COVER_PATH, "JPEG", quality=92, optimize=True)


def remove_existing_card(text: str, href: str) -> str:
    pattern = re.compile(
        rf'\n\s*<a class="story-card [^"]+" href="{re.escape(href)}">.*?</a>',
        re.S,
    )
    return pattern.sub("", text)


def update_story_indexes():
    zh_path = REPO / "run50" / "stories" / "chinese" / "index.html"
    en_path = REPO / "run50" / "stories" / "english" / "index.html"
    fb_path = REPO / "run50" / "facebook" / "index.html"

    zh_card = f"""      <a class="story-card run-50" href="./{SLUG}.html">
        <img src="../../../assets/{MEDAL_COVER_PATH.name}?v={VERSION}" alt="路易斯维尔马拉松奖牌封面" loading="lazy" decoding="async">
        <div class="story-copy">
          <p class="story-meta">肯塔基路易斯维尔 · {DATE_ZH}</p>
          <h2 class="story-title">Run50 #第1州｜路易斯维尔马拉松</h2>
          <p class="story-desc">疫情中的间隔起跑、六英尺社交距离、Beckley Creek Park的秋日折返，以及我在北美完成的第一个全马。</p>
          <div class="story-foot"><span>长文图记</span><span>阅读 →</span></div>
        </div>
      </a>
"""
    en_card = f"""      <a class="story-card run-50" href="./{SLUG}.html">
        <img src="../../../assets/{THUMB_PATH.name}?v={VERSION}" alt="Icon cover for Louisville Marathon" loading="lazy" decoding="async">
        <div class="story-card-content">
          <div class="meta">Kentucky · Louisville · {DATE_ZH}</div>
          <h2>Louisville Marathon: my first marathon in North America</h2>
          <p>A pandemic-era out-and-back through Beckley Creek Park, with masks, staggered starts, six-foot gaps, a hot final stretch, and State 1 of Run50.</p>
        </div>
      </a>
"""
    fb_card = f"""    <a class="story-card run-50" href="./{SLUG}.html">
      <div>
        <p class="eyebrow">World / USA / Marathon</p>
        <h2>Kentucky gave me my first marathon in North America</h2>
        <p>Race date: November 8, 2020. A socially distanced Louisville Marathon moved into Beckley Creek Park, with staggered starts, a quiet forest course, and a hard final 12 kilometers.</p>
        <div class="meta"><span>Louisville, KY</span><span>Run50 #1</span><span>First North American marathon</span></div>
      </div>
      <img src="../../assets/facebook/{THUMB_PATH.name}?v={VERSION}" alt="Icon-style Louisville Marathon cover">
    </a>
"""

    for path, marker, card in [
        (zh_path, '<section class="story-grid" aria-label="中文故事列表">', zh_card),
        (en_path, '<section class="story-grid" aria-label="English story list">', en_card),
    ]:
        text = remove_existing_card(path.read_text(encoding="utf-8"), f"./{SLUG}.html")
        text = text.replace(marker, marker + "\n" + card, 1)
        path.write_text(text, encoding="utf-8")

    text = remove_existing_card(fb_path.read_text(encoding="utf-8"), f"./{SLUG}.html")
    text = text.replace('<main class="shell">', '<main class="shell">\n' + fb_card, 1)
    fb_path.write_text(text, encoding="utf-8")

    # A parsed story card already carries the exact 2020 date. Match both city and
    # date so later Louisville races do not inherit this story link.
    for path in (zh_path, en_path):
        text = path.read_text(encoding="utf-8")
        text = text.replace(
            "const match = parsedList.find(p => p.city === mr.city);",
            "const match = parsedList.find(p => p.city === mr.city && p.date === mr.date);",
        )
        path.write_text(text, encoding="utf-8")


def update_hub():
    path = REPO / "run50" / "hub.html"
    text = path.read_text(encoding="utf-8")

    text = re.sub(
        r"\s*'Louisville':\{lat:38\.2527,lon:-85\.7585\},?",
        "",
        text,
    )
    text = text.replace(
        "'Chicago':{lat:41.8781,lon:-87.6298},",
        "'Chicago':{lat:41.8781,lon:-87.6298},"
        "'Louisville':{lat:38.2527,lon:-85.7585},",
        1,
    )

    text = re.sub(
        r"^\s*'KY':\[\{city:'Louisville'.*?\}\],\n",
        "",
        text,
        flags=re.M,
    )
    text = text.replace(
        "const _RACES = {\n",
        "const _RACES = {\n"
        "  'KY':[{city:'Louisville',date:'Nov 8, 2020',"
        "story:'stories/english/louisville-marathon.html',"
        "fb:'facebook/louisville-marathon.html'}],\n",
        1,
    )

    text = re.sub(
        r"\n\s*<!-- Kentucky Louisville story dot -->.*?"
        r"<!-- /Kentucky Louisville story dot -->\n",
        "\n",
        text,
        flags=re.S,
    )
    world_dot = """
    <!-- Kentucky Louisville story dot -->
    <circle cx="234" cy="128" r="10" fill="rgba(255,80,40,0.18)" pointer-events="none"/>
    <circle cx="234" cy="128" r="5" fill="#ff4040" stroke="#fff" stroke-width="1.6" class="wm-dot"
      data-city="Louisville, KY" data-date="Nov 8, 2020" data-story="stories/english/louisville-marathon.html"/>
    <!-- /Kentucky Louisville story dot -->
"""
    chicago_dot = """    <circle cx="231" cy="121" r="5" fill="#ff4040" stroke="#fff" stroke-width="1.6" class="wm-dot"
      data-city="Chicago, IL" data-date="Oct 2024" data-story="stories/english/chicago-marathon.html"/>
"""
    text = text.replace(chicago_dot, chicago_dot + world_dot, 1)
    path.write_text(text, encoding="utf-8")


def update_root_home():
    path = REPO / "index.html"
    text = path.read_text(encoding="utf-8")
    text = re.sub(
        r"\n\s*<!-- Kentucky Run50 story -->.*?"
        r"<!-- /Kentucky Run50 story -->\n",
        "\n",
        text,
        flags=re.S,
    )
    card = f"""
      <!-- Kentucky Run50 story -->
      <article class="video-card" data-section="run50" data-category="run50 facebook" data-title="Kentucky gave me my first marathon in North America">
        <a class="thumb" href="run50/facebook/{SLUG}.html">
          <img src="assets/facebook/{THUMB_PATH.name}?v={VERSION}" alt="Icon-style Louisville Marathon cover">
          <span class="duration">Story</span>
        </a>
        <div class="meta">
          <span class="avatar run50">50</span>
          <div>
            <a class="video-title" href="run50/facebook/{SLUG}.html">Kentucky gave me my first marathon in North America</a>
            <p class="video-sub">Louisville, KY &middot; Nov 8, 2020</p>
          </div>
        </div>
      </article>
      <!-- /Kentucky Run50 story -->

"""
    text = text.replace("      <!-- Water Header -->", card + "      <!-- Water Header -->", 1)
    path.write_text(text, encoding="utf-8")


def update_landing_counts():
    path = REPO / "run50" / "index.html"
    text = path.read_text(encoding="utf-8")
    text = text.replace(" 8 stories", " 13 stories")
    text = text.replace("<strong>8</strong> stories", "<strong>13</strong> stories")
    path.write_text(text, encoding="utf-8")


def update_supabase_sql():
    path = REPO / "supabase" / "run50-comments.sql"
    text = path.read_text(encoding="utf-8")
    keys = [
        "run50-louisville-marathon-facebook-en",
        "run50-louisville-marathon-en",
        "run50-louisville-marathon-zh",
    ]
    for key in keys:
        text = re.sub(rf"^\s*'{re.escape(key)}',\n", "", text, flags=re.M)

    def add_keys(match):
        indent = match.group(1)
        return "".join(f"{indent}'{key}',\n" for key in keys) + match.group(0)

    text = re.sub(
        r"^(\s*)'run50-chicago-marathon-facebook-en',",
        add_keys,
        text,
        flags=re.M,
    )
    path.write_text(text, encoding="utf-8")


def main():
    events = extract_story()
    image_count = copy_story_images(events)
    sections = split_sections(events)

    zh_article = render_article(
        events,
        "zh",
        "Run50-Louisville-Marathon-clean_files/",
        "路易斯维尔马拉松照片",
    )
    en_article = render_article(
        events,
        "en",
        "../chinese/Run50-Louisville-Marathon-clean_files/",
        "Louisville Marathon photo",
    )
    fb_article = facebook_article(sections)

    (REPO / "run50" / "stories" / "chinese" / f"{SLUG}.html").write_text(
        story_page("zh", zh_article), encoding="utf-8"
    )
    (REPO / "run50" / "stories" / "english" / f"{SLUG}.html").write_text(
        story_page("en", en_article), encoding="utf-8"
    )
    (REPO / "run50" / "facebook" / f"{SLUG}.html").write_text(
        facebook_page(fb_article), encoding="utf-8"
    )

    generate_cover_png()
    generate_cover_svg()
    generate_medal_cover()
    update_story_indexes()
    update_hub()
    update_root_home()
    update_landing_counts()
    update_supabase_sql()

    text_count = sum(event["type"] == "text" for event in events)
    print(
        f"Built Kentucky story with {image_count} images, "
        f"{text_count} text blocks, and {len(events)} source events."
    )


if __name__ == "__main__":
    main()
