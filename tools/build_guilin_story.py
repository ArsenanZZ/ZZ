from pathlib import Path
from lxml import html
from html import escape
from PIL import Image, ImageDraw, ImageFont
import re


REPO = Path(r"C:\Users\ZZ\Documents\Github\ZZ")
SOURCE_BASE = Path(r"Z:\ZhennanZ Folder\000-Marathon-Story-2024-2025\20251116-Guilin Marathon")
SOURCE_HTML = next(p for p in SOURCE_BASE.iterdir() if p.suffix.lower() == ".html")
SOURCE_FILES = next(p for p in SOURCE_BASE.iterdir() if p.is_dir() and p.name.endswith("_files"))
SITE = "https://arsenanzz.github.io/ZZ"
OUT_IMG_DIR = REPO / "run50" / "stories" / "chinese" / "RunCN-Guilin-Marathon-clean_files"


EN_BY_INDEX = {
    0: "Preface",
    1: "# A marathon family meet-up",
    2: "In my last week in China, I had hoped to squeeze in a couple more runs. Instead, I spent most of the month dealing with dental work, so it turned into an involuntary break from running. Luckily, by the time I was about to leave, I was mostly fine again. Guilin Marathon landed at just the right moment, so I treated it as a last-minute comeback.",
    5: "My parents had recently been traveling with my cousin, and we planned to meet up in Guilin. After I finished the race, they could head back to Foshan with me and stay for another week. After that, I would be flying back across the ocean for work again, and who knows when the next trip home would happen.",
    6: "So for me, this Guilin race had a nice little mix to it: part comeback run, part family meet-up.",
    10: "# The marathon expo and Two Rivers and Four Lakes",
    11: "I arrived in Guilin one day before my parents. The first thing I noticed after getting off the train was the heat. It honestly felt even hotter than Guangdong. I dropped my luggage at the Airbnb and went straight to Central Square to pick up my race packet.",
    14: "Guilin has a lot of electric scooters. Crossing the street takes some awareness, because they are constantly moving through the city and testing your reaction time a little.",
    17: "The volunteers were wearing blue shirts, and most of them looked pretty young. They were warm and efficient. Packet pickup was quick: bib, race bag, and then a photographer nearby taking pictures of runners.",
    24: "As evening settled in, the “Guilin Marathon welcomes you” display was still lit up. A lot of runners were taking photos there, and the race mood was already in the air.",
    27: "I had some congee to put something in my stomach, then decided to walk toward the river. There were race-themed decorations for “Run Guilin Marathon, tour Two Rivers and Four Lakes,” and I saw local girls wearing ethnic silver jewelry taking photos with their families.",
    32: "Behind them were the Sun and Moon Twin Pagodas: the gold one is the Sun Pagoda, the silver one is the Moon Pagoda. They stand on Shan Lake and are probably the most recognizable landmark in the Two Rivers and Four Lakes area. Along the water, people could also rent ethnic costumes for photos, and quite a few people were livestreaming. It was lively.",
    33: "Since it was still early, I bought a ticket for the Two Rivers and Four Lakes night cruise. There was a guide on the boat, and we slowly moved across the water under the lights. The scenery was beautiful. Some buildings had a Southeast Asian feel, while others looked more like little bridges, pavilions, courtyards and gardens.",
    40: "Out on the water, there were also fishermen performing with cormorants. It was clearly more of a show than real fishing, but it was still fun to see for the first time. There were dance performances on the pavilions too, and once the lights hit the stage, it looked pretty good.",
    47: "The cruise also passes through a lock. The water levels between the four lakes and the two rivers are different, so the boat has to rise once and drop once. It was my first time taking a city cruise through a lock like that, and it felt surprisingly novel. The two rivers are the Li River and the Taohua River; the four lakes are Shan, Rong, Gui and Mulong.",
    50: "As the boat kept going, the famous Elephant Trunk Hill suddenly appeared. The lights were shining on the hill and through the arch, with reflections on the water. By the time we got back to the dock, it was almost nine. The area was still busy, and there happened to be a Guilin rice noodle festival nearby with rows of food stalls.",
    53: "I did not get back to the Airbnb until around ten. I was already thinking about going out the next morning for sunrise.",
    55: "# Sunrise at Chuanshan Park, then Elephant Trunk Hill with my parents",
    56: "On Saturday, I woke up early, a little after four. I wanted to go to Chuanshan Pavilion in Chuanshan Park to watch the sunrise.",
    57: "I found the spot through Xiaohongshu. Someone said the view was good. It is definitely not as famous as those big sunrise spots in Yangshuo, but inside Guilin city, it seemed like a solid choice.",
    60: "Around five, it was still dark when I reached the entrance to Chuanshan Park. Finding the trail took some effort. There were not many lights, so I used my phone as a flashlight and climbed the stone steps. Early-morning hill climbing is no joke. It felt harder than running.",
    63: "By the time I reached Chuanshan Pavilion halfway up the hill, quite a few people were already holding spots for sunrise. The view was wide open: Guilin city below, and rings of karst peaks in the distance. These are what people call peak forest landforms, limestone hills rising one by one, the kind of layered mountains you see in ink paintings.",
    68: "As dawn came in, the mountains slowly changed color, from dark blue to pale blue and then a little purple. The sun was shy that morning, with thick clouds blocking the clean “jumping over the peak” moment. When it finally showed itself, it was already a bit higher, but the light landing on the hills and the small houses below still looked beautiful.",
    77: "Once it was bright, the dense city below became clear too. Off to the right there was a stretch of water, part of the Yijiang river channel area in Guilin, shining gold in the morning light. Farther away, I could also see a tower on a hill. That is Tashan Pagoda near Chuanshan Park, an old local landmark.",
    84: "On the way down, I saw the well-known “Three Friends” sculpture: Xu Beihong, Liu Yazi and Xiong Foxi. They all lived in Guilin at one point and left behind work and stories here. Standing near the sculpture under the trees felt a bit like stepping back into that era.",
    87: "I went back to the Airbnb and took a nap. Around noon, I went to the airport to pick up my parents and my aunt. They had flown in from Chengdu. We ate some dumplings together, and when the sun was less brutal, we walked around Elephant Trunk Hill in the evening.",
    90: "Elephant Trunk Hill really is Guilin’s signature landmark. It is famous because the cave in the hill looks like an elephant stretching its trunk into the river to drink.",
    97: "It sits where the Li River and Taohua River meet. Poets and painters have written about it and painted it for ages, so its fame has kept building. The scenic area is also pretty accessible now. It is the kind of place almost everyone visits when they come to Guilin.",
    104: "Seeing Elephant Trunk Hill during the day is one thing; seeing it lit up at night is another. My dad said he had heard my grandfather talk about it when he was young, and that it had appeared in old picture books. So this trip was finally seeing the real thing.",
    111: "After the scenic area, it was getting dark, so we ate at a northeastern Chinese restaurant nearby. The taste was normal enough, but the portion size and the price reminded me very clearly that we were eating northeastern food in a southern tourist city.",
    115: "# Guilin Marathon, starting in the heat",
    116: "Race day finally arrived. The start was not until 8 a.m., so I did not leave the Airbnb until just before seven. My parents were still on the balcony waving and cheering for me. That felt pretty warm.",
    119: "The start was at Guilin Central Square, and it was packed. I was in Zone D and had to walk almost a kilometer around the crowd. Because my corral was farther back, I did not officially start until 8:20. The sun was already very present. It was hot.",
    126: "In the first three kilometers, we reached Binjiang Road. This section runs right along the Li River. There was a bit of cool wind, and the scenery immediately started to feel like Guilin. In the distance, the karst peaks poked up behind the buildings with sharp little outlines. It was pretty special.",
    135: "There were lots of photographers too. I was wearing a red Arsenal jersey in a sea of yellow Guilin Marathon shirts, so I looked like the one red tomato piece in a plate of fried rice with egg.",
    142: "From kilometer six to twelve, the course went north through the space between city and mountains. Ludi Road is near Reed Flute Cave, one of Guilin’s older famous sights. Taohua River Road follows the Taohua River; the water is a bit wider there, with hills and buildings on both sides, and it felt comfortable to run through.",
    147: "There were also cheer squads in ethnic costumes along the road. The colors were bright, and under that strong sun they stood out even more.",
    154: "The water station volunteers were in blue, and just seeing them from a distance made me feel cooler. It was also the first time I got caught by a photographer at a water station, which was kind of funny.",
    157: "Around 10K, we passed Guilin Library. The building has a distinctive look, with a roof that feels a little traditional, and it came out well in photos.",
    162: "Around kilometer 13, we reached Victory Bridge. It is a pretty noticeable old bridge in Guilin’s urban area, painted orange, and because the view opens up there, it is one of those spots where photographers can frame runners and mountains together.",
    167: "When we crossed, the sun was blasting right onto the bridge deck. The colors were bright, but it was also a bit blinding. After Victory Bridge, we entered Zhongyin Road. The view opened even more, but there was very little shade. That was the official start of the direct-sunlight zone.",
    170: "Around 20K, I stopped and asked a man in a reflective vest to help me take a few photos. He was really nice and even taught me how to pose.",
    173: "After that came the main city roads. The course would gradually move toward Chuanshan Park, where the mountains get closer and the scenery improves again. The sunlight, though, was another story.",
    175: "# Run-walk through Chuanshan, and even the spray trucks could not beat the heat",
    176: "Soon after halfway, the route entered the classic Chuanshan and Seven Star area of Guilin. Chuanshan Park was right next to us, and Seven Star Park was not far away either.",
    177: "This is the stretch a lot of runners call the prettiest part of Guilin Marathon. The roadside is full of those typical karst peaks, with almost nothing blocking them. The mountains stand right in front of you.",
    182: "As I kept running, I saw a tower standing clearly on a hill. That is Chuanshan East Pagoda, one of the easiest landmarks to capture in race photos on this section. Behind it, layers of mountains stack up, and it looks pretty grand.",
    187: "To be honest, by then I was not fully in sightseeing mode anymore. My phone was almost dead, my earbuds had gone silent, and without my audiobook, my mindset got very Buddhist. Mostly, it was just too hot. The sun was annoying.",
    190: "I shifted into run-walk mode. With the temperature at this race, plenty of runners were doing the same. This stretch had a big out-and-back, with the turnaround near Lushan Road, and it was widely seen as one of the mental checkpoints of the full marathon.",
    191: "There was barely any shade. The road was wide and straight, and the sun was shining right in front of us. A road that seems to go on forever, plus that heat, can really loosen your willpower. I definitely put on the pain face.",
    196: "There were lots of spray trucks along the road, shooting water like little fountains. Running through one felt cool for about three seconds, and then I was hot again.",
    197: "You could tell everyone was trying anything to cool down: drinking, pouring water over the head, pressing sponges onto the face. Everything was in use.",
    203: "# Finishing with Fat Messi, with my parents waiting at the end",
    204: "After the turnaround, we crossed Li River Bridge again and returned to Chuanshan Road. The city feeling came back, the roadside got livelier, and there were more spectators.",
    205: "That was when I saw a guy ahead of me with little braids wearing a Miami Messi No. 10 jersey. From behind, he looked intimidating, and I thought he might be foreign. When I caught up, I realized he was Chinese, so we chatted a little.",
    210: "The braided guy was from Weihai. I told him I was from the Northeast, and he said no wonder, because someone from the Northeast would definitely struggle more with the Guilin sun.",
    211: "As we were talking, he suggested running a bit more. Then before long, he pulled far ahead. I thought, okay, this will not do, so I took it a bit more seriously. In the end, we crossed the line almost in the same stride.",
    214: "The photographers even got close-up shots of us. I suspect one of them might have been a Messi fan. My Arsenal jersey is not something many people recognize on the road in China, so I just borrowed a little Messi traffic.",
    217: "My parents and my aunt had waited at the finish for hours. I picked up my finisher bag. The Guilin medal was very distinctive: gold, with a rotating piece, and very photogenic.",
    228: "I walked out around the sports center and met up with my parents. We took a few photos together, just to keep the memory.",
    229: "On the way back, we saw a long line of electric scooters stuck behind the road closure. That is how city marathons are: some people enjoy them, some people get trapped by them. Different perspectives, hard to fully reconcile.",
    236: "In the end, we flagged down a three-wheeler back to the Airbnb. I ordered delivery, and my parents, my aunt and I had a simple takeout meal together. I did not run fast in Guilin, but I got way more photos than usual. Under the big sun, the pictures turned out surprisingly well.",
    241: "After one night of rest, I was ready to head back to Foshan. This Guilin trip was slow on the running side, but so what?",
    244: "Postscript",
    245: "# From the textbook to the course",
    246: "When I was little, our textbooks always said, “Guilin’s scenery is the finest under heaven.” Back then, I only remembered it as a slogan.",
    247: "Now, after running this loop, that line has turned from text into something real: the mountains were right there, the river was beside the road, and the route connected one scene after another like the whole city had become a long running course.",
    248: "The marathon route went from the city to the Li River, then into the arms of the karst peaks, across bridges, around turnarounds, and back through Chuanshan Road.",
    249: "The mountains that used to exist only in photos when I was a kid became the backdrop I could look up and see while running. The mountains stood still; I was moving. It felt like slowly running open a geography textbook.",
    250: "The stranger and sweeter part was that my northeastern family had all come down to the far south of China to cheer for me. That was a pretty special experience.",
    251: "In another week, I would be flying back to the United States, so I am leaving these words and photos here as a small freeze-frame.",
    252: "- The end -",
    253: "Words | Arsenan",
    254: "Photos | Arsenan",
    255: "Design | Arsenan",
}

CAPTION_OVERRIDES = {
    "Wo @WoBa": "Me @Dad",
    "WoBa and WoMa @Arsenan": "Dad and Mom @Arsenan",
    "WoMan and DaNing @Arsenan": "Mom and Aunt @Arsenan",
    "WoMa and WoBa @Arsenan": "Mom and Dad @Arsenan",
    "WoMa#DaNiang @Arsenan": "Mom and Aunt @Arsenan",
    "WoBa @Arsenan": "Dad @Arsenan",
    "Finish @WoMa": "Finish @Mom",
    "20KM @DaShu": "20KM @Kind stranger",
    "Finish @DaNiang": "Finish @Aunt",
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

    story = clean[5:]
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
            raise FileNotFoundError(source_path)
        out_name = f"img-{count:03d}.webp"
        out_path = OUT_IMG_DIR / out_name
        with Image.open(source_path) as im:
            if im.mode not in ("RGB", "RGBA"):
                im = im.convert("RGB")
            if im.mode == "RGBA":
                bg = Image.new("RGB", im.size, "white")
                bg.paste(im, mask=im.getchannel("A"))
                im = bg
            im.save(out_path, "WEBP", quality=88, method=6)
        event["file"] = out_name
    return count


def polish_chinese(story):
    fixes = {
        "好在临走前好差不多了": "好在临走前好得差不多了",
        "最后我们几户以相同的步伐冲线": "最后我们几乎以相同的步伐冲线",
    }
    for event in story:
        if event["type"] == "text":
            for old, new in fixes.items():
                event["text"] = event["text"].replace(old, new)


def clean_caption(value: str) -> str:
    caption = value.lstrip("▲").strip()
    return CAPTION_OVERRIDES.get(caption, caption)


def translated_text(index: int, value: str) -> str:
    if value.startswith("▲"):
        return "▲" + clean_caption(value)
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
        alt_base = "Guilin Marathon photo" if lang == "en" else "桂林马拉松照片"
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
            flush(clean_caption(value) if lang == "en" else value.lstrip("▲").strip())
            continue
        flush()
        if set(value) <= {"★"}:
            parts.append("<hr>")
        elif value in ("前言", "后记", "Preface", "Postscript"):
            parts.append(f"<h2>{escape(value)}</h2>")
        elif value.startswith("# "):
            parts.append(f'<p class="chapter-title">{escape(value[2:].strip())}</p>')
            parts.append('<p class="place">Guilin, Guangxi</p>' if lang == "en" else '<p class="place">⛰️ 桂林，广西</p>')
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
        title = "RunCN #第2站｜广西：桂林马拉松｜热浪滚滚，爸妈也来助威了"
        short = "RunCN #第2站｜桂林马拉松"
        desc = "这是我跑中国的第二站，广西桂林马拉松。比赛从中心广场出发，赛道贴着漓江，一路跑进穿山和七星一带。前半程风景很好，后半程暴晒明显，爸妈和大娘也在终点等我。"
        canonical = f"{SITE}/run50/stories/chinese/guilin-marathon.html"
        nav = '<a href="./index.html">← 中文故事</a><a href="../english/guilin-marathon.html">English</a><a href="../../index.html">Run50</a>'
        meta = '<span>阿森男</span><span>比赛日期：2025年11月16日</span><span>发布：2026年1月24日</span><a href="https://mp.weixin.qq.com/s/aiLzgB9klRuemRYtlFWOKg" target="_blank" rel="noopener noreferrer">原文链接</a>'
        kicker = "RunCN #第2站 · 广西桂林"
        footer = "静态整理版：正文从“前言”开始，已移除公众号导出页的顶部杂项，原始保存文件未修改。"
        engage = engagement("zh-CN", "run50-guilin-marathon-zh", "supabase-comments-guilin-zh")
        og_locale = "zh_CN"
        alt_locale = "en_US"
    else:
        page_lang = "en"
        title = "RunCN Stop 2 | Guilin Marathon"
        short = "Guilin Marathon: heat, karst hills, and family at the finish"
        desc = "A conversational English version of Arsenan's second RunCN story: Guilin Marathon, Li River views, karst hills, heavy heat, a run-walk second half, and family waiting at the finish."
        canonical = f"{SITE}/run50/stories/english/guilin-marathon.html"
        nav = '<a href="./index.html">← English Stories</a><a href="../chinese/guilin-marathon.html">中文</a><a href="../../index.html">Run50</a>'
        meta = '<span>Arsenan</span><span>Race date: November 16, 2025</span><span>Published: January 24, 2026</span><a href="../chinese/guilin-marathon.html">Original Chinese</a>'
        kicker = "RunCN Stop 2 · Guilin, Guangxi"
        footer = "English version of the Guilin Marathon story. Original Chinese page is linked above."
        engage = engagement("en", "run50-guilin-marathon-en", "supabase-comments-guilin-en")
        og_locale = "en_US"
        alt_locale = "zh_CN"

    og_img = f"{SITE}/assets/og-run50-guilin-icons.png"
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
  <meta property="article:published_time" content="2025-11-16T08:00:00+08:00">
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
  <script src="../../../assets/zz-engagement-config.js?v=20260604"></script>
  <script src="../../../assets/zz-engagement.js?v=20260604"></script>
</body>
</html>
'''


def facebook_page(article: str, css: str) -> str:
    desc = "Race date: November 16, 2025. Guilin Marathon through the Li River, karst hills, bridges, heavy heat and a finish line where family was waiting."
    og_img = f"{SITE}/assets/og-run50-guilin-icons.png"
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Guilin Marathon | Run50 Facebook</title>
  <meta name="description" content="{escape(desc)}">
  <link rel="canonical" href="{SITE}/run50/facebook/guilin-marathon.html">
  <meta property="og:title" content="Guilin turned a marathon into a heat test with mountains on every side">
  <meta property="og:description" content="{escape(desc)}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="{SITE}/run50/facebook/guilin-marathon.html">
  <meta property="og:site_name" content="ArsenanZZ">
  <meta property="og:locale" content="en_US">
  <meta property="og:image" content="{og_img}">
  <meta property="og:image:secure_url" content="{og_img}">
  <meta property="og:image:type" content="image/png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="article:author" content="Arsenan">
  <meta property="article:published_time" content="2025-11-16T08:00:00+08:00">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Guilin turned a marathon into a heat test with mountains on every side">
  <meta name="twitter:description" content="{escape(desc)}">
  <meta name="twitter:image" content="{og_img}">
  <link rel="stylesheet" href="../../assets/zz-engagement.css">
  <style>{css}</style>
</head>
<body>
  <div class="breaking"><div class="breaking-inner"><a href="./index.html">Run50 Facebook</a><span>Guilin / Guangxi / Marathon</span></div></div>
  <header class="site-head"><div class="site-head-inner"><div class="wordmark">Run50</div><nav class="section-nav" aria-label="Story links"><a href="../stories/english/guilin-marathon.html">Full English</a><a href="../stories/chinese/guilin-marathon.html">中文原文</a><a href="../index.html">Run50</a></nav></div></header>
  <article class="article">
    <section class="hero">
      <span class="label">World / China / Marathon</span>
      <h1>Guilin turned a marathon into a heat test with mountains on every side</h1>
      <p class="dek">Guilin is famous for karst hills and the Li River. On November 16, 2025, its marathon put those postcard views on the course, then added a second-half wall of heat.</p>
      <div class="byline"><span>By Arsenan</span><span>Guilin, Guangxi</span><span>November 16, 2025</span></div>
      <figure class="lead-media"><img src="../../assets/og-run50-guilin-icons.png" alt="Icon-style Guilin Marathon cover"><figcaption>Guilin karst hills, Li River, bridge, sun, bib and medal.</figcaption></figure>
    </section>
    <section class="story-grid">
      <aside class="rail">
        <section class="brief-box"><h2>At a glance</h2><dl><div><dt>Race</dt><dd>Guilin Marathon, RunCN Stop 2</dd></div><div><dt>Course</dt><dd>Central Square, Li River, Victory Bridge, Chuanshan and Seven Star</dd></div><div><dt>What stayed with me</dt><dd>Heat, karst hills, a run-walk second half and family waiting at the finish.</dd></div></dl></section>
        <section class="share-note"><strong>Notes</strong>The comments box is below the story. New comments appear right away.</section>
      </aside>
      <div class="copy full-story">
        {article}
      </div>
    </section>
  </article>
  {engagement("en", "run50-guilin-marathon-facebook-en", "supabase-comments-guilin-facebook-en")}
  <script src="../../assets/zz-engagement-config.js?v=20260604"></script>
  <script src="../../assets/zz-engagement.js?v=20260604"></script>
</body>
</html>
'''


def write_cover_assets():
    assets = REPO / "assets"
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 750" role="img" aria-labelledby="title desc">
<title id="title">Guilin Marathon icon cover</title>
<desc id="desc">Icon style cover with Guilin karst hills, Li River, bridge, sun, race bib and medal.</desc>
<rect width="1200" height="750" fill="#f4f7f4"/>
<circle cx="982" cy="135" r="76" fill="#f4b642"/>
<path d="M0 570 C180 518 308 602 470 552 C620 506 736 544 890 520 C1015 500 1102 518 1200 486 L1200 750 L0 750 Z" fill="#0f766e" opacity=".88"/>
<path d="M68 502 C140 270 250 270 322 502 Z" fill="#1f6f5b"/>
<path d="M254 504 C350 214 490 212 584 504 Z" fill="#2f855a"/>
<path d="M514 510 C610 252 744 252 838 510 Z" fill="#236b56"/>
<path d="M768 506 C854 278 988 276 1078 506 Z" fill="#2f855a"/>
<path d="M0 610 C150 560 260 640 420 594 C594 544 760 628 930 572 C1042 536 1130 560 1200 532 L1200 750 L0 750 Z" fill="#65b8b2" opacity=".78"/>
<path d="M135 525 L420 525 M420 525 L520 435 M520 435 L620 525 M620 525 L1030 525" stroke="#7a4f2a" stroke-width="22" stroke-linecap="round" fill="none"/>
<path d="M450 525 Q520 455 590 525" stroke="#f4f7f4" stroke-width="30" fill="none"/>
<rect x="760" y="318" width="250" height="160" rx="18" fill="#ffffff" stroke="#20242b" stroke-width="8"/>
<text x="785" y="374" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="900" fill="#20242b">RunCN #2</text>
<text x="785" y="426" font-family="Arial, Helvetica, sans-serif" font-size="54" font-weight="900" fill="#cc0000">GUILIN</text>
<circle cx="260" cy="630" r="52" fill="#d9a441" stroke="#8b5e20" stroke-width="8"/>
<circle cx="260" cy="630" r="24" fill="#f4f7f4"/>
<path d="M230 604 L260 566 L290 604" stroke="#8b5e20" stroke-width="8" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
<text x="70" y="105" font-family="Arial, Helvetica, sans-serif" font-size="58" font-weight="900" fill="#20242b">Guilin Marathon</text>
<text x="74" y="158" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="700" fill="#667085">Li River · Karst hills · Heat wave · Family finish</text>
</svg>'''
    (assets / "thumb-run50-guilin-icons.svg").write_text(svg, encoding="utf-8", newline="\n")

    width, height = 1200, 630
    image = Image.new("RGB", (width, height), "#f4f7f4")
    draw = ImageDraw.Draw(image)

    def font(size, bold=False):
        candidates = [
            r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
            r"C:\Windows\Fonts\segoeuib.ttf" if bold else r"C:\Windows\Fonts\segoeui.ttf",
        ]
        for candidate in candidates:
            try:
                return ImageFont.truetype(candidate, size)
            except Exception:
                pass
        return ImageFont.load_default()

    draw.ellipse((920, 58, 1070, 208), fill="#f4b642")
    for points, color in [
        ([(50, 438), (132, 210), (252, 438)], "#1f6f5b"),
        ([(230, 442), (350, 172), (520, 442)], "#2f855a"),
        ([(500, 448), (628, 218), (798, 448)], "#236b56"),
        ([(748, 444), (872, 218), (1040, 444)], "#2f855a"),
    ]:
        draw.polygon(points, fill=color)
    draw.polygon([(0, 486), (150, 452), (310, 506), (465, 468), (620, 442), (760, 500), (930, 464), (1100, 440), (1200, 420), (1200, 630), (0, 630)], fill="#0f766e")
    draw.polygon([(0, 535), (160, 500), (330, 548), (520, 514), (710, 548), (920, 500), (1100, 516), (1200, 490), (1200, 630), (0, 630)], fill="#65b8b2")
    draw.line([(120, 450), (410, 450), (510, 370), (610, 450), (1040, 450)], fill="#7a4f2a", width=20)
    draw.arc((445, 380, 575, 510), 200, 340, fill="#f4f7f4", width=26)
    draw.rounded_rectangle((735, 275, 1010, 430), radius=18, fill="#ffffff", outline="#20242b", width=7)
    draw.text((765, 318), "RunCN #2", font=font(38, True), fill="#20242b")
    draw.text((765, 370), "GUILIN", font=font(58, True), fill="#cc0000")
    draw.ellipse((230, 500, 334, 604), fill="#d9a441", outline="#8b5e20", width=8)
    draw.ellipse((258, 528, 306, 576), fill="#f4f7f4")
    draw.line([(250, 500), (282, 462), (314, 500)], fill="#8b5e20", width=7)
    draw.text((64, 78), "Guilin Marathon", font=font(62, True), fill="#20242b")
    draw.text((68, 142), "Li River - Karst hills - Heat wave - Family finish", font=font(28), fill="#667085")
    image.save(assets / "og-run50-guilin-icons.png", "PNG")


def main():
    story = extract_story()
    polish_chinese(story)
    image_count = copy_story_images(story)
    indexed = list(enumerate(story))

    normal_css = extract_style(REPO / "run50" / "stories" / "english" / "xiangyang-marathon.html")
    normal_css = normal_css.replace("#0e7490", "#0f766e").replace("#a33a2b", "#a45625").replace("#b7892f", "#a47c2a")
    fb_css = extract_style(REPO / "run50" / "facebook" / "xiangyang-marathon.html")

    zh_article = render_article(indexed, "zh", "RunCN-Guilin-Marathon-clean_files/")
    en_article = render_article(indexed, "en", "../chinese/RunCN-Guilin-Marathon-clean_files/")

    race_start, post_start = 115, 244
    race_events = [(i, e) for i, e in indexed if race_start <= i < post_start]
    backstory_events = [(i, e) for i, e in indexed if i < race_start]
    post_events = [(i, e) for i, e in indexed if i >= post_start]
    fb_article = "\n        ".join([
        '<section class="context-note"><p>Guilin Marathon is not just a race with pretty mountains on the side. The course starts in the city, runs along the Li River, opens onto bridges and karst hills, then throws runners into a hot, exposed second half.</p><p>For me, it was also the last marathon-sized thing I did before heading back to the United States: a comeback run after dental trouble, with my parents and aunt waiting at the finish.</p></section>',
        render_article(race_events, "en", "../stories/chinese/RunCN-Guilin-Marathon-clean_files/"),
        '<section class="section-bridge"><h2>How Guilin became a family stop</h2><p>The race day was the headline, but the trip started earlier: packet pickup, a night cruise through Two Rivers and Four Lakes, sunrise at Chuanshan Park, and my parents arriving in Guilin before the race.</p></section>',
        render_article(backstory_events, "en", "../stories/chinese/RunCN-Guilin-Marathon-clean_files/"),
        render_article(post_events, "en", "../stories/chinese/RunCN-Guilin-Marathon-clean_files/"),
    ])

    (REPO / "run50" / "stories" / "chinese" / "guilin-marathon.html").write_text(normal_page("zh", zh_article, normal_css), encoding="utf-8", newline="\n")
    (REPO / "run50" / "stories" / "english" / "guilin-marathon.html").write_text(normal_page("en", en_article, normal_css), encoding="utf-8", newline="\n")
    (REPO / "run50" / "facebook" / "guilin-marathon.html").write_text(facebook_page(fb_article, fb_css), encoding="utf-8", newline="\n")
    write_cover_assets()
    from redesign_run50_covers import main as redesign_run50_covers
    redesign_run50_covers()
    print(f"story_events={len(story)} images={image_count}")


if __name__ == "__main__":
    main()
