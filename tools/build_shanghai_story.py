from pathlib import Path
from lxml import html
from html import escape
from PIL import Image, ImageOps
import re

REPO = Path(__file__).resolve().parents[1]
SOURCE_BASE = Path(r"Z:\ZhennanZ Folder\0-Running Story Web")
SOURCE_HTML = SOURCE_BASE / "在上海，我爬上了中国最高的 Building.html"
SOURCE_FILES = SOURCE_BASE / "在上海，我爬上了中国最高的 Building_files"
SITE = "https://arsenanzz.github.io/ZZ"
SLUG = "shanghai-vertical-marathon"
OUT_IMG_DIR = REPO / "run50" / "stories" / "chinese" / "RunCN-Shanghai-Vertical-Marathon-clean_files"

EN_BY_INDEX = {
    0: "Adventure in the Magic City",
    2: "Reaching the top of Shanghai Tower @Arsenan",
    3: "- Message from Shanghai -",
    4: "Humanity in the Magic City",
    5: "Preface",
    6: "Last week, I had a Zoom call with my junior from Tongji University. That night, I actually dreamed of returning to those special days in Shanghai. In the dream, I was heavily pressured to drink, and ended up drinking quite a lot, leaving me feeling a bit dizzy the next day.",
    7: "As someone who left footprints in the Magic City, I still consider Shanghai to be my lucky city. Although I left a long time ago, I still miss those stories.",
    9: "The Magic City @Arsenan",
    10: "01",
    11: "# Drifting in Shanghai",
    12: "Because my U.S. visa had been stuck for so long, Professor Chen recommended that I go to Professor Zhuang's research group at Tongji University as a 'visiting scholar.' Although it was called an exchange, in reality, I felt more than anything a deep sense of unease. With tensions rising between China and the U.S., the future felt highly uncertain.",
    13: "My first impression of Shanghai was not friendly at all. The taxi driver had that typical arrogant, condescending attitude toward outsiders, using a sarcastic tone that made me want to resort to physical violence in a heartbeat. Then, the heavy-set lady living next door in the hostel would hog the washing machine with an aggressively hostile attitude; after a big shouting match, we just couldn't stand the sight of each other.",
    14: "The only thing that gave me some comfort was that the canteens at Tongji University were actually quite delicious.",
    16: "Braised noodles at Tongji canteen @Arsenan",
    17: "After National Day, autumn arrived in Shanghai. Six months had already slipped by since my first visa interview, and other students in the same boat were growing increasingly anxious. Feeling my expanding belly, I realized I had completely let my physical shape go. I would often joke about myself: fat and with no future, a total useless salted fish.",
    19: "Rice bowl at Tongji canteen @Arsenan",
    20: "So I would sigh occasionally, but immediately tell myself: ups and downs are all part of life, just stay busy, and the other side of the coin will eventually show.",
    21: "Learn new things, then get moving. The running tracks at Tongji and Fudan Universities started seeing my silhouette, and I became a regular at the Tongji gym. Yet, it still didn't feel intense enough.",
    23: "Tongji University running track @Arsenan",
    25: "Fudan University running track @Arsenan",
    26: "That was when AR (Adidas Runners) came into the picture. Having heard about this Adidas running club for a while, I rode my bicycle over to join them out of curiosity. The first time, trying to keep up for ten kilometers completely broke me—even though I was in the slowest pacer group.",
    28: "Running the Bund with AR @Arsenan",
    30: "Running the Bund with AR @Arsenan",
    32: "Running the Bund with AR @AR",
    33: "I refused to accept defeat; after all, I used to be a decent runner myself. Gradually, I found myself able to keep up with AR's 4:30/km group for a full 10K, and I slowly shed some weight.",
    34: "Night run with AR @AR",
    36: "Night run with AR @AR",
    39: "AR night run & birthday party @AR",
    41: "The Bund, the West Bund, Century Park—I ran through all of these iconic Shanghai running spots with AR. Sending all my love to AR.",
    43: "The trendy West Bund @Arsenan",
    45: "AR's special refreshments and Sister Bing @Arsenan",
    46: "With a solid community, I slowly integrated into life at Tongji. Qimin took me out to explore and eat, Bin dragged me to Hongkou Stadium to watch the Shenhua football match, I did research with my juniors, spent long hours in the library with Minjin, and even had the privilege of attending a public lecture by a prominent French professor organized by Professor Jin. As my schedule filled up, everything seemed to be looking up.",
    48: "Qimin, who took me to all kinds of food spots @Arsenan",
    49: "Watching Shenhua at Hongkou with Bin @Passerby",
    51: "Doing research with my junior @Passerby",
    53: "In late October, I booked my second visa interview in Shanghai, withdrawing my previous application in Beijing. The process was incredibly smooth. The U.S. consular officer was very polite, and with Halloween just around the corner, the atmosphere inside the consulate felt quite relaxed.",
    55: "Halloween celebration @Passerby",
    57: "02",
    58: "# Reaching the top of Shanghai Tower",
    59: "Things started to take a positive turn. The month following a visa interview is usually a happy window. I had the chance to visit Jing'an Temple with an old friend from Wuhan University to pray for my visa to be issued. I traveled to West Lake to see close friends and unexpectedly bumped into the renowned academic Shi Yigong. I left my most important wish of 2019 by the Chao Phraya River and in front of the Erawan Shrine in Bangkok. I even took a trip to Ningbo to say goodbye to that girl, drifting around like a hermit crab.",
    60: "Jing'an Temple @Arsenan",
    62: "Jing'an Temple @Arsenan",
    64: "Jing'an Temple @Arsenan",
    65: "I also signed up for the Shanghai Tower Vertical Marathon. The idea that climbing stairs could be called a 'marathon' sounded incredibly novel, so I wanted to experience it. Since such an opportunity is rare, especially in Shanghai, I naturally couldn't pass it up.",
    67: "Night view of the Magic City @Arsenan",
    69: "Night view of the Magic City @Arsenan",
    71: "Night view of the Magic City @Arsenan",
    72: "Shanghai Tower: 127 floors, with 119 floors in the main building structure, 3,398 steps, and a vertical height of 632 meters. This is the tallest skyscraper in Shanghai.",
    75: "Shanghai Tower (on the right) @Arsenan",
    76: "From 2008 to 2016, the 632-meter-tall Shanghai Tower grew steadily along the banks of the Huangpu River. Day by day, it evolved from its early 'eggbeater' construction look into the modern landmark of the Magic City, standing like an eternal, shimmering silver tree in Shanghai's night sky. No matter day or night, there are always people stopping to gaze at it. This is also the highest vertical marathon in the world.",
    77: "Shanghai Tower starting point @Arsenan",
    79: "Starting line (the chubby guy in white) @Photographer",
    81: "Entering the tower @Photographer",
    82: "On packet pickup day, I was completely captivated by Shanghai's night scenery. But when the next morning's start came around, I actually grew quite nervous. Although I was a veteran of road marathons, this was my absolute first time doing a vertical marathon. Everyone started in staggered time slots. I was mostly worried about the stuffy, hot air inside the stairwell. However, once I started climbing, I realized the exhaust and ventilation systems of Shanghai Tower were top-notch; on some floors, you could even feel a cool breeze.",
    84: "Climbing stairs @Photographer",
    86: "Climbing stairs @Photographer",
    88: "Climbing stairs @Photographer",
    89: "In a vertical marathon, you don't actually need to run; just taking large strides to climb is enough. I felt that trying to run might make me more prone to injury. Along the way, faster climbers were politely let through by those in front—it was very harmonious. With aid stations and evacuation refuge floors scattered throughout, there was no need for excessive worry; you could just focus on enjoying the race.",
    91: "Aid station @Arsenan",
    92: "The volunteers on the 90-something floor told us not to worry too much about finishing, as there was plenty of time, and suggested we take photos on that floor since the view was great. It was a very spacious floor with excellent visibility, offering a quite different perspective compared to the main observation deck at the very top.",
    94: "Jin Mao Tower @Arsenan",
    96: "Shanghai World Financial Center @Arsenan",
    97: "Before I knew it, I had reached the summit. Compared to a standard road marathon, the vertical marathon felt much easier. The observation deck was already filled with finishers. Looking through the glass windows and seeing the Jin Mao Tower and Oriental Pearl Tower standing beneath my feet, I think even the most reserved person would feel a surge of excitement.",
    99: "Summit finish @Photographer",
    101: "Summit finish @Photographer",
    102: "How high you stand is indeed important, but what matters even more is your curiosity. So today is another milestone.",
    103: "Having stood at the top of Shanghai Tower, my time in Shanghai has truly been worthwhile.",
    105: "Medal and Oriental Pearl Tower @Arsenan",
    107: "Medal and Huangpu River @Arsenan",
    109: "Medal and Shanghai World Financial Center @Arsenan",
    110: "There was an extra surprise afterward. During the post-race lucky draw, I was fortunate enough to win an American Heart Association first-aid certification course, which turned out to be a very engaging and useful training session.",
    112: "First-aid runner training class @Arsenan",
    113: "Before I realized it, winter arrived in Shanghai. I found another running group, Joy Run Shanghai, and met another wonderful crowd of friends.",
    115: "The new running community @Arsenan",
    116: "Postscript",
    117: "In mid-December, my visa was finally approved. My days in Shanghai were drawing to a close.",
    118: "Without realizing it, I had grown very fond of this university and this group of friends.",
    120: "Iron pot stew @Arsenan",
    121: "Before leaving, I took my friends from the Tongji lab out for a northeastern Chinese iron pot stew. I have to say, the flavor here in Shanghai was surprisingly authentic.",
    122: "Tongji University @Arsenan",
    124: "Tongji University @Arsenan",
    126: "Tongji University @Arsenan",
    128: "Tongji University @Arsenan",
    130: "Then I said goodbye to my friends at the hostel: Xia, Little Xia, and the girl from Shenyang. They were all incredibly nice people.",
    131: "My time in Shanghai was a special journey during a very unique period of my life. I believe that every experience has its purpose, so lately I often remind myself: even when being pushed hard, keep your energy high.",
    132: "- The end -",
    133: "Words | Arsenan",
    134: "Photos | Arsenan",
    135: "Design | Arsenan",
}

def norm(value: str) -> str:
    return re.sub(r"\s+", " ", value.replace("\xa0", " ")).strip()

def is_styleish(value: str) -> bool:
    return ":host {" in value or "--weui-" in value or len(value) > 800

def has_desc_leaf_container(el) -> bool:
    for desc in el.iterdescendants():
        if desc.tag in ("p", "section"):
            text = norm("".join(desc.itertext()))
            if text and not is_styleish(text):
                return True
    return False

def extract_style(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    match = re.search(r"<style>(.*?)</style>", text, re.S)
    if not match:
        raise RuntimeError(f"No style block in {path}")
    return match.group(1)

def extract_story():
    source = SOURCE_HTML.read_text(encoding="utf-8", errors="replace")
    doc = html.fromstring(source)
    root = doc.xpath('//*[@id="js_content"]')[0]
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
    for event in events:
        key = (event["type"], event.get("text") or event.get("src"))
        prev = (clean[-1]["type"], clean[-1].get("text") or clean[-1].get("src")) if clean else None
        if prev != key:
            clean.append(event)

    story = clean
    for idx, event in enumerate(story):
        if event["type"] == "text" and event["text"].startswith("设计"):
            return story[: idx + 1]
    return story

def copy_story_images(story):
    OUT_IMG_DIR.mkdir(parents=True, exist_ok=True)
    count = 0
    for event in story:
        if event["type"] != "img":
            continue
        count += 1
        src = event["src"]
        local_name = src.split("_files/", 1)[1] if "_files/" in src else Path(src).name
        local_name = local_name.split("?", 1)[0].split("#", 1)[0]
        source_path = SOURCE_FILES / local_name
        if not source_path.exists():
            # Try parsing with parenthesis if (1) format is present
            source_path = SOURCE_FILES / local_name.replace("%28", "(").replace("%29", ")")
        if not source_path.exists():
            raise FileNotFoundError(source_path)
        out_name = f"img-{count:03d}.webp"
        out_path = OUT_IMG_DIR / out_name
        with Image.open(source_path) as im:
            im = ImageOps.exif_transpose(im)
            if im.mode not in ("RGB", "L"):
                im = im.convert("RGB")
            elif im.mode == "L":
                im = im.convert("RGB")
            im.save(out_path, "WEBP", quality=88, method=6)
        event["file"] = out_name
    return count

def clean_caption(value: str) -> str:
    caption = value.lstrip("▲").strip()
    return caption

def translated_text(index: int, value: str) -> str:
    if value.startswith("▲"):
        return "▲ " + clean_caption(value)
    if set(value) <= {"★"}:
        return value
    return EN_BY_INDEX.get(index, value)

def render_article(events, lang: str, rel_img_prefix: str) -> str:
    parts = []
    pending_img = None

    def flush(caption=""):
        nonlocal pending_img
        if not pending_img:
            return
        alt_base = "Shanghai Vertical Marathon photo" if lang == "en" else "上海中心垂直马拉松照片"
        img_num = int(pending_img[4:7])
        cap = f"<figcaption>{escape(caption)}</figcaption>" if caption else ""
        parts.append(
            f'<figure><img src="{rel_img_prefix}{pending_img}" alt="{alt_base} {img_num}" '
            f'loading="lazy" decoding="async">{cap}</figure>'
        )
        pending_img = None

    for index, event in events:
        if event["type"] == "img":
            flush()
            pending_img = event["file"]
            continue
        value = event["text"] if lang == "zh" else translated_text(index, event["text"])
        if value.startswith("▲"):
            caption_text = clean_caption(value)
            # Find matching overrides or translate
            if lang == "en":
                caption_text = EN_BY_INDEX.get(index, caption_text)
                if caption_text.endswith(" @Arsenan") or caption_text.endswith(" @AR") or caption_text.endswith(" @Photographer") or caption_text.endswith(" @Passerby"):
                    # keep the clean credit format
                    pass
                else:
                    # check if caption_text starts with ▲, if so strip it
                    caption_text = caption_text.lstrip("▲").strip()
            flush(caption_text)
            continue
        flush()
        if set(value) <= {"★"}:
            parts.append("<hr>")
        elif value in ("前言", "后记", "Preface", "Postscript"):
            parts.append(f'<h2 class="section-label">{escape(value)}</h2>')
        elif value.startswith("# "):
            parts.append(f"<h2>{escape(value[2:].strip())}</h2>")
            parts.append('<p class="place">Shanghai Tower, Shanghai</p>' if lang == "en" else '<p class="place">🏙️ 上海中心，上海</p>')
        elif value.startswith("- "):
            parts.append(f'<p class="end-mark">{escape(value)}</p>')
        elif value.startswith("文字") or value.startswith("摄影") or value.startswith("设计") or value.startswith("Words") or value.startswith("Photos") or value.startswith("Design"):
            parts.append(f'<p class="credit-line">{escape(value)}</p>')
        elif index == 0:
            parts.append(f'<p class="place">{escape(value)}</p>')
        elif index == 3:
            parts.append(f'<h2 class="section-label">{escape(value)}</h2>')
        elif index == 4:
            parts.append(f'<p class="place">{escape(value)}</p>')
        else:
            parts.append(f"<p>{escape(value)}</p>")
    flush()
    return "\n      ".join(parts)

def engagement(locale: str, key: str, ident: str) -> str:
    if locale == "zh-CN":
        return f'''<section class="zz-engagement" data-zz-engagement data-locale="zh-CN" data-page-key="{key}">
    <div class="zz-engagement-shell">
      <div>
        <p class="zz-engagement-kicker">留言 / 访问次数</p>
        <h2>跑完也可以聊两句</h2>
        <p class="zz-engagement-note">不用注册账号即可提交留言，提交后会直接显示。</p>
        <div class="zz-engagement-stats">
          <span class="zz-engagement-stat" id="busuanzi_container_page_pv"><span>访问</span><strong id="busuanzi_value_page_pv" data-zz-view-count>--</strong><span>次</span></span>
        </div>
      </div>
      <div class="zz-engagement-card"><div id="{ident}" data-zz-supabase-comments></div><p class="zz-engagement-status" data-zz-engagement-status>留言区加载中...</p></div>
    </div>
  </section>'''
    return f'''<section class="zz-engagement" data-zz-engagement data-locale="en" data-page-key="{key}">
    <div class="zz-engagement-shell">
      <div>
        <p class="zz-engagement-kicker">Comments / Views</p>
        <h2>Say something after the run</h2>
        <p class="zz-engagement-note">No account is needed to submit a comment. New comments appear right away.</p>
        <div class="zz-engagement-stats"><span class="zz-engagement-stat" id="busuanzi_container_page_pv"><span>Views</span><strong id="busuanzi_value_page_pv" data-zz-view-count>--</strong></span></div>
      </div>
      <div class="zz-engagement-card"><div id="{ident}" data-zz-supabase-comments></div><p class="zz-engagement-status" data-zz-engagement-status>Loading comments...</p></div>
    </div>
  </section>'''

def normal_page(lang: str, article: str, css: str) -> str:
    zh = lang == "zh"
    if zh:
        page_lang = "zh-CN"
        title = "RunCN #第4站｜上海中心垂直马拉松｜爬上中国最高的 Building，看东方明珠立在脚下"
        short = "RunCN #第4站｜上海中心垂直马拉松"
        desc = "这是我跑中国的第四站，上海中心大厦垂直马拉松。2019年冬，在签证等待的特殊时期里，我报名参加了这场世界最高的垂马比赛，爬完127层、3398个台阶，在632米之巅看浦江两岸。"
        canonical = f"{SITE}/run50/stories/chinese/{SLUG}.html"
        nav = f'<a href="./index.html">← 中文故事</a><a href="../english/{SLUG}.html">English</a><a href="../../facebook/{SLUG}.html">Facebook</a><a href="../../index.html">Run50</a>'
        meta = '<span>阿森男</span><span>比赛日期：2019年11月24日</span><span>发布：2026年6月17日</span>'
        kicker = "RunCN #第4站 · 上海中心垂马"
        footer = "静态整理版：正文从“前言”开始，已移除公众号导出页的顶部杂项，原始保存文件未修改。"
        engage = engagement("zh-CN", f"run50-{SLUG}-zh", f"supabase-comments-{SLUG}-zh")
        og_locale = "zh_CN"
        alt_locale = "en_US"
    else:
        page_lang = "en"
        title = "RunCN Stop 4 | Shanghai Tower Vertical Marathon"
        short = "Shanghai Tower Vertical Marathon: climbing 3,398 steps to the summit"
        desc = "A conversational English version of Arsenan's fourth RunCN story: The Shanghai Tower Vertical Marathon in 2019. Climbing 127 floors, 3,398 steps, and reaching 632m height during a special visa waiting period."
        canonical = f"{SITE}/run50/stories/english/{SLUG}.html"
        nav = f'<a href="./index.html">← English Stories</a><a href="../chinese/{SLUG}.html">中文</a><a href="../../facebook/{SLUG}.html">Facebook</a><a href="../../index.html">Run50</a>'
        meta = f'<span>Arsenan</span><span>Race date: November 24, 2019</span><span>Published: June 17, 2026</span><a href="../chinese/{SLUG}.html">Original Chinese</a>'
        kicker = "RunCN Stop 4 · Shanghai Tower"
        footer = "English version of the Shanghai Tower Vertical Marathon story. Original Chinese page is linked above."
        engage = engagement("en", f"run50-{SLUG}-en", f"supabase-comments-{SLUG}-en")
        og_locale = "en_US"
        alt_locale = "zh_CN"

    og_img = f"{SITE}/assets/og-run50-{SLUG}-icons.png"
    return f'''<!doctype html>
<html lang="{page_lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)}</title>
  <meta name="description" content="{escape(desc)}">
  <link rel="canonical" href="{canonical}">
  <meta property="og:title" content="{escape(short)}">
  <meta property="og:description" content="{escape(desc)}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="{canonical}">
  <meta property="og:site_name" content="ArsenanZZ">
  <meta property="og:locale" content="{og_locale}">
  <meta property="og:locale:alternate" content="{alt_locale}">
  <meta property="og:image" content="{og_img}">
  <meta property="og:image:secure_url" content="{og_img}">
  <meta property="og:image:type" content="image/png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="article:author" content="Arsenan">
  <meta property="article:published_time" content="2019-11-24T09:00:00+08:00">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{escape(short)}">
  <meta name="twitter:description" content="{escape(desc)}">
  <meta name="twitter:image" content="{og_img}">
  <link rel="stylesheet" href="../../../assets/zz-engagement.css">
  <style>{css}</style>
</head>
<body>
  <nav class="story-nav" aria-label="Page navigation">{nav}</nav>
  <header class="page-header">
    <p class="kicker">{escape(kicker)}</p>
    <h1>{escape(title)}</h1>
    <div class="meta">{meta}</div>
    <p class="dek">{escape(desc)}</p>
  </header>
  <main class="article-shell">
    <article class="article-body">
      {article}
    </article>
  </main>
  {engage}
  <footer class="page-footer">{escape(footer)}</footer>
  <script src="../../../assets/zz-engagement-config.js?v=20260617"></script>
  <script src="../../../assets/zz-engagement.js?v=20260617"></script>
</body>
</html>
'''

def facebook_page(article: str, css: str) -> str:
    desc = "Race date: November 24, 2019. Reaching 632m height at the Shanghai Tower Vertical Marathon—climbing 127 floors and 3,398 steps during a special visa waiting period."
    og_img = f"{SITE}/assets/og-run50-{SLUG}-icons.png"
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Shanghai Tower Vertical Marathon | Run50 Facebook</title>
  <meta name="description" content="{escape(desc)}">
  <link rel="canonical" href="{SITE}/run50/facebook/{SLUG}.html">
  <meta property="og:title" content="Climbing 3,398 steps to the top of China's tallest skyscraper">
  <meta property="og:description" content="{escape(desc)}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="{SITE}/run50/facebook/{SLUG}.html">
  <meta property="og:site_name" content="ArsenanZZ">
  <meta property="og:locale" content="en_US">
  <meta property="og:image" content="{og_img}">
  <meta property="og:image:secure_url" content="{og_img}">
  <meta property="og:image:type" content="image/png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="article:author" content="Arsenan">
  <meta property="article:published_time" content="2019-11-24T09:00:00+08:00">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Climbing 3,398 steps to the top of China's tallest skyscraper">
  <meta name="twitter:description" content="{escape(desc)}">
  <meta name="twitter:image" content="{og_img}">
  <link rel="stylesheet" href="../../assets/zz-engagement.css">
  <style>{css}</style>
</head>
<body>
  <div class="breaking"><div class="breaking-inner"><a href="./index.html">Run50 Facebook</a><span>Shanghai / China / Vertical Marathon</span></div></div>
  <header class="site-head"><div class="site-head-inner"><div class="wordmark">Run50</div><nav class="section-nav" aria-label="Story links"><a href="../stories/english/{SLUG}.html">Full English</a><a href="../stories/chinese/{SLUG}.html">中文原文</a><a href="../index.html">Run50</a></nav></div></header>
  <article class="article">
    <section class="hero">
      <span class="label">World / China / Vertical Marathon</span>
      <h1>Climbing 3,398 steps to the top of China's tallest skyscraper</h1>
      <p class="dek">Shanghai Tower stands 632 meters tall along the riverbank. In late 2019, during a long and tense wait for a U.S. visa, I signed up for the world's highest vertical marathon.</p>
      <div class="byline"><span>By Arsenan</span><span>Shanghai, China</span><span>November 24, 2019</span></div>
      <figure class="lead-media"><img src="../../assets/og-run50-{SLUG}-icons.png" alt="Icon-style Shanghai Vertical Marathon cover"><figcaption>Shanghai Tower, Oriental Pearl Tower, river, steps, and finisher medal.</figcaption></figure>
    </section>
    <section class="story-grid">
      <aside class="rail">
        <section class="brief-box"><h2>At a glance</h2><dl><div><dt>Race</dt><dd>Shanghai Tower Vertical Marathon, RunCN Stop 4</dd></div><div><dt>Height</dt><dd>632m vertical rise, 127 floors, 3,398 steps</dd></div><div><dt>What stayed with me</dt><dd>CAP group night runs, visa anxiety, and the city landscape below my feet.</dd></div></dl></section>
        <section class="share-note"><strong>Notes</strong>The comments box is below the story. New comments appear right away.</section>
      </aside>
      <div class="copy full-story">
        {article}
      </div>
    </section>
  </article>
  {engagement("en", f"run50-{SLUG}-facebook-en", f"supabase-comments-{SLUG}-facebook-en")}
  <script src="../../assets/zz-engagement-config.js?v=20260617"></script>
  <script src="../../assets/zz-engagement.js?v=20260617"></script>
</body>
</html>
'''

def main():
    story = extract_story()
    image_count = copy_story_images(story)
    indexed = list(enumerate(story))

    # Read Guilin style and customize slightly for Shanghai Tower theme
    normal_css = extract_style(REPO / "run50" / "stories" / "english" / "guilin-marathon.html")
    # Adapt color accents to Shanghai Tower theme (steel blue / gold)
    normal_css = normal_css.replace("#0f766e", "#1b3a4b").replace("#a45625", "#a43e25").replace("#a47c2a", "#c09030")
    
    fb_css = extract_style(REPO / "run50" / "facebook" / "guilin-marathon.html")
    fb_css = fb_css.replace("#cc0000", "#cc2424") # RunCN red accent

    zh_article = render_article(indexed, "zh", "RunCN-Shanghai-Vertical-Marathon-clean_files/")
    en_article = render_article(indexed, "en", f"../chinese/RunCN-Shanghai-Vertical-Marathon-clean_files/")

    # Facebook story: race first!
    # Race starts at block 65 (Vertical marathon signup/intro) to 112
    race_start, post_start = 65, 116
    race_events = [(i, e) for i, e in indexed if race_start <= i < post_start]
    backstory_events = [(i, e) for i, e in indexed if i < race_start]
    post_events = [(i, e) for i, e in indexed if i >= post_start]
    
    fb_article = "\n        ".join([
        '<section class="context-note"><p>The vertical marathon at Shanghai Tower is a unique challenge: 127 floors, 3,398 steps, climbing straight up into the sky. Unlike road races, it is an intense, vertical fight against gravity where you compete in staggered time slots.</p><p>For me, this 2019 climb was a milestone that came right in the middle of a stressful visa waiting period, bookended by lab life at Tongji University and group night runs along the Bund.</p></section>',
        render_article(race_events, "en", f"../stories/chinese/RunCN-Shanghai-Vertical-Marathon-clean_files/"),
        '<section class="section-bridge"><h2>Drifting on the Bund and campus life</h2><p>Before stepping into the stairwell, my weeks in Shanghai were shaped by campus canteens, visa anxiety, and joining the Adidas Runners (AR) community for night runs that eventually got me back into running shape.</p></section>',
        render_article(backstory_events, "en", f"../stories/chinese/RunCN-Shanghai-Vertical-Marathon-clean_files/"),
        render_article(post_events, "en", f"../stories/chinese/RunCN-Shanghai-Vertical-Marathon-clean_files/"),
    ])

    (REPO / "run50" / "stories" / "chinese" / f"{SLUG}.html").write_text(normal_page("zh", zh_article, normal_css), encoding="utf-8", newline="\n")
    (REPO / "run50" / "stories" / "english" / f"{SLUG}.html").write_text(normal_page("en", en_article, normal_css), encoding="utf-8", newline="\n")
    (REPO / "run50" / "facebook" / f"{SLUG}.html").write_text(facebook_page(fb_article, fb_css), encoding="utf-8", newline="\n")
    
    print(f"Shanghai Vertical Marathon story built successfully. story_events={len(story)} images={image_count}")

if __name__ == "__main__":
    main()
