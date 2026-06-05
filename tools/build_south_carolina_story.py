from pathlib import Path
from lxml import html
from html import escape
from PIL import Image, ImageDraw, ImageFont, ImageOps
import re

REPO = Path(__file__).resolve().parents[1]
SOURCE_BASE = Path(r"Z:\ZhennanZ Folder\000-Marathon-Story-2024-2025\20240414-SC-2skow4boston-Marathon\0000-Web")
SOURCE_HTML = next(p for p in SOURCE_BASE.iterdir() if p.suffix.lower() == ".html")
SOURCE_FILES = next(p for p in SOURCE_BASE.iterdir() if p.is_dir() and p.name.endswith("_files"))
SITE = "https://arsenanzz.github.io/ZZ"
SLUG = "south-carolina-marathon"
VERSION = "20260605-2"
OUT_IMG_DIR = REPO / "run50" / "stories" / "chinese" / "Run50-South-Carolina-Marathon-clean_files"

EN_BY_INDEX = {
    0: "South Carolina",
    2: "Run50 #18 U.S. State Marathon",
    3: "Location: Greer, SC",
    4: "Race: Too Slow for Boston",
    5: "Preface",
    6: "# From North Carolina to South Carolina: A Springtime Marathon Relay",
    7: "🏝️ Greer, SC",
    8: "Just after charging into the Atlantic at Oak Island in North Carolina in February, as soon as the April spring breeze blew, South Carolina was easily added to the schedule.",
    9: "Actually, marathons in South Carolina are really hard to find. We scrolled through running websites back and forth, and finally stumbled upon a very interesting name: '2Slow4Boston'.",
    12: "At first glance, it looked like a 'meme' race, with puns flying everywhere (Too Slow for Boston, meaning you can't qualify for the Boston Marathon).",
    13: "But once I looked into it, it turned out they weren't joking at all. This race actually has some substance:",
    14: "It's specially designed for 'people who can't qualify for Boston,' going against the norm—the slower you run, the more glorious it is. They even award trophies to the final three finishers.",
    15: "The core theme is to slow down, enjoy, and stop stressing. To be honest, I hesitated for a long time at first, feeling that this race might be too 'boring'.",
    16: "Running a marathon here means looping around a residential neighborhood 20 times, with the scenery of trees, houses, and lawns playing on a continuous loop.",
    17: "But since I had to run the Derby Marathon in Kentucky at the end of April, I decided to treat it as pre-race training. Keep it easy, don't worry about pace, and check off South Carolina for my Run50 quest at the same time. And so, we set off.",
    21: "# State 18: South Carolina | Quiet, Low-key, and an Old Historical Soul",
    22: "🌿 Greer, SC",
    23: "South Carolina, State 18 of Run50. On the map, it borders North Carolina and is tucked into the southeastern corner of the United States.",
    24: "The state is small and quiet today, but don't let that fool you—it was anything but quiet in history. The first shot of the Civil War was fired here, and it was the first state to secede from the Union.",
    27: "You could say it's like that student in US history who always wants to be the first to speak up:",
    28: "The capital, Columbia, is not very famous and has few tourists;",
    29: "The largest city, Charleston, is an old port town with a charming, historic vibe;",
    30: "Greer, where we stayed this time, is a small town right on the North Carolina border, neither near the ocean nor close to the bustle.",
    31: "In short, South Carolina doesn't have the blazing sunshine of Florida or the poetic coastline of North Carolina, but as State 18 of Run50, it carries its own weight.",
    33: "# Passing the Great Smoky Mountains: An RV as our Airbnb!",
    34: "🌿 Greer, SC",
    35: "Driving all the way from North Carolina to South Carolina, as we passed the foothills of the Great Smoky Mountains, we stopped at a sunny town called Pigeon Forge and had a meal at a classic American buffet, Golden Corral.",
    44: "We arrived in the town of Greer in the afternoon, which is the site of the 2Slow4Boston Marathon. The packet pickup was very unique—not in a convention center, but right on the race organizer's front porch.",
    45: "As we walked up, we saw the organizer wearing a tie-dye t-shirt, sitting behind a high-top table covered with a pile of yellow shirts and bibs. Beside her was an elderly man, and their house was right behind them.",
    46: "The whole atmosphere felt less like a race expo and more like a neighborhood block party, where locals just decided to hold a running event.",
    55: "The shirts were in the striking Boston Marathon colors: yellow and blue. The graphic on the chest featured a guy dragging a stubborn mule that refused to budge, making the theme crystal clear: Too Slow 4 Boston!",
    56: "After picking up our gear, we drove to our Airbnb. Honestly, this place was way cooler than I expected: a large travel trailer (RV) parked on the grass.",
    57: "This kind of trailer RV doesn't have a driver's cab and is usually towed by a pickup truck. Americans absolutely love them. They tow their home across the country, park it, and once expanded, it's bigger than the apartment I rent—complete with a shower, kitchen, and TV.",
    66: "I really love the Oscar-winning film 'Nomadland,' which tells the story of nomads who live in RVs and work temporary jobs across America. They have it a bit hard and lonely, but they are incredibly free.",
    67: "I often think how cool it would be to buy an RV in the future, finish the 50 states with Siqi, and go camping in national parks. (Though with an RV, it's not really camping anymore; it's more like driving a mini-villa through the wilderness.)",
    76: "This RV had everything, but the toilet got clogged at night. The two of us worked on it for a long time but couldn't fix it, so we had to call the host.",
    77: "The host came over from the huge house next door and fixed it in no time, which gave us a chance to meet them face-to-face.",
    78: "This night before the race felt like living in a mobile home, turning South Carolina into our own backyard.",
    80: "# Trophies for the Slowest: A Marathon That Goes Backwards!",
    81: "🌿 Greer, SC",
    82: "In the marathon world, speed is always worshipped. Running fast represents strength, honor, and is a badge of merit for those chosen by Boston.",
    83: "But in the small South Carolina town of Greer, the 2Slow4Boston Marathon goes completely against the grain. It doesn't worship speed; it pays tribute to 'slowness'. It even explicitly states that runners who are too fast are disqualified from winning trophies.",
    84: "The symbol of the race is not a unicorn, but a stubborn mule, because this race is not about speed, but about stubborn determination.",
    87: "The origin of this marathon is also very unique. It was originally a spin-off of another race series called the B. Marathon.",
    88: "The founder came up with a fun idea: 'Since Boston is everyone's goal, why don't we host a reverse one? How about a Too Slow for Boston race?'",
    89: "That's how today's 2S4B was born—a small-loop marathon that is both funny and deeply meaningful.",
    92: "The tone of the entire race is completely different from traditional marathons. The official website states plainly: 'We believe that spending 6, 7, or 8 hours completing a marathon, with that refusal to give up, is also worthy of applause.'",
    93: "The aid station is also very 'community block party' style: there is only one station, offering potato chips, sandwiches, sodas, and pizza for lunch.",
    94: "So this might be one of the most boring marathons in the world! But the more you learn about it, the more you feel: this quirky race actually has a lot of character.",
    96: "# Half an Hour Late? No Problem! We're Here to Take It Slow",
    97: "🌿 Greer, SC",
    98: "On the morning of the race, we set off from the RV and headed back to the neighborhood where we picked up our gear, ready to start today's 'looping' challenge.",
    99: "The race format is simple and hardcore: a neighborhood loop of 1.31 miles, run 20 times, and you're done.",
    100: "The sun wasn't blazing yet, but the South Carolina morning was already getting warm. As we chatted and strolled to the starting line, we suddenly noticed quite a few runners already running back and forth.",
    103: "I thought to myself: these people are way too eager, their warm-up looks like an actual race!",
    104: "But looking closer, the race had already started!",
    105: "We were actually half an hour late! But honestly, nobody cares when you start. After all, this race is called 'Too Slow for Boston'—slowness is a virtue here, and running fast is just awkward.",
    110: "I took my time going to the restroom, then leisurely set off from the only green arch. The whole vibe felt exactly like going for a morning run in your own neighborhood, completely stress-free.",
    111: "The neighborhood isn't big, but the road isn't flat either—it has some rolling elevation changes.",
    116: "There weren't many runners, and barely any residents in sight. The atmosphere was so quiet you could hear footsteps and your own breathing.",
    117: "The most enthusiastic spectator was actually a dog. It stood behind the fence, watching us run back and forth with longing eyes.",
    120: "There was only one aid station, and the organizers encouraged everyone to bring their own cups—eco-friendly and self-disciplined.",
    121: "Since I didn't bring a water hydration pack, I sheepishly asked for several plastic bottles. Each lap I passed by, I placed them in a shady corner, turning it into my exclusive 'secret aid station'.",
    122: "As the laps added up, the weather began to get brutal. The South Carolina sun is no joke, and within a few laps, I could feel my skin starting to roast.",
    129: "Siqi was in excellent form today, running steadily and patiently, taking it slow and easy.",
    130: "Every time I ran through the green arch, a volunteer with a clicker counter would check me off, just like punching in at work.",
    135: "There was also a very eye-catching guy on the course, wearing a US flag bandanna and running shirtless with ripped muscles, looking like the second coolest runner out there.",
    136: "But from my 'data observations,' the main force of this starting field was mostly elderly runners. You really can't out-slow them. Respect!",
    145: "We could catch some shade occasionally, but most of the course was exposed to the scorching sun, which could bake you in just a few laps.",
    146: "My 'secret aid station' began accumulating spoils of war, with plastic bottles lining up one by one, looking like a beverage exhibition corner.",
    155: "I bet the lady at the aid station would have been completely exasperated if she saw it, probably muttering under her breath: 'Didn't we tell you to bring your own cups? What is this, a plastic bottle self-service station?'",
    156: "Electrolyte drinks were served in rotation—purple, pink, yellow, a colorful bombardment. The taste was a bit like the bubblegum water from childhood,",
    157: "but honestly, on such a boring and quiet course, this little bit of color and artificial flavor added some welcome fun.",
    164: "The sun grew fiercer, casting straight shadows onto the road. Looking down, I felt like my face was almost fully cooked.",
    165: "During the final few miles, I met Siqi at the aid station. She was in good spirits, smiling and taking photos as she walked.",
    172: "An organizer came over to chat, saw the camera in my hand and asked, 'Is that a GoPro?' I said, 'No, it's a DJI.' He scratched his head and smiled, 'My old camera is practically an antique, probably not as good as yours.'",
    173: "Siqi also helped carry the camera for a while, which made things a lot easier for me.",
    182: "By the time we met again, she had already finished and was holding a 'Slow Award' trophy.",
    183: "Not bad at all—perfectly fitting for Siqi's personality.",
    188: "I finally reached my last loop. As a well-behaved runner, I didn't leave a messy 'exhibition' of plastic bottles. I went back to the corner, cleaned up all the bottles, and tossed them into the trash bin.",
    189: "At the finish line, the organizer wearing glasses was waiting under the arch. She hung the medal around my neck herself, patted my shoulder, and said, 'Nice job!'",
    200: "At that moment, I realized I had underestimated this small race before starting—it wasn't easy to finish at all.",
    201: "Later we ran into her again at another marathon—truly, runners meet everywhere.",
    212: "The post-race weather was brutally hot. I chugged water, ate two slices of pizza, and took plenty of photos with Siqi, feeling like a dried fish brought back to life by the medal.",
    213: "The medal looked very similar to the golden Boston Marathon unicorn, but looking closer, it wasn't a unicorn—it was a bearded man pulling a stubborn mule that refused to move!",
    222: "It's quite interesting—some run marathons like stallions, while others drag a mule to reach the finish line. We were the latter, but we made it too!",
    223: "Postscript",
    224: "# What Are You Looking At? What's Wrong With Going Slow?!",
    225: "🌿 Greer, SC",
    226: "Right after the race, we drove back to Kentucky without stopping, enjoying a K-Pot Korean BBQ and Hot Pot buffet along the way.",
    229: "Looking back, this was probably the most laid-back marathon I've ever run: no starting gun, no pacers, no cheering crowds, and no pre-finish line sprint tension.",
    230: "Just a small neighborhood loop, round and round, in an infinite loop.",
    231: "Sometimes, running is like spiritual practice: you can't rush, you can't take shortcuts, and you can't worry too much about others' speeds.",
    232: "This race called 2Slow4Boston sounds like a joke,",
    233: "but its core is actually very serious. It tells ordinary runners like us: 'It doesn't matter if you run slow, what matters is that you are still running.'",
    234: "State 18 - South Carolina - Checked!",
    235: "From South Carolina to Kentucky, we drove along sun-dappled highways.",
    236: "Outside the car window was the typical South Carolina countryside; inside the car was the small medal hanging around our necks. It wasn't the Boston unicorn, but it shone just as bright, as if to say:",
    237: "There isn't just one path to Boston for runners. Sometimes, a neighborhood loop of twenty laps can bring its own rhythm and glory.",
    239: "- End -",
    240: "Words | Arsenan",
    241: "Photos | Arsenan",
    242: "Design | Arsenan",
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
    return text.startswith("▲") or "@" in text

def should_skip_text(text: str) -> bool:
    return text in {"★", "★★", "★★★", "★★★★"}

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
    for idx, event in enumerate(events):
        key = (event["type"], event.get("text") or event.get("src"))
        prev = (clean[-1][1]["type"], clean[-1][1].get("text") or clean[-1][1].get("src")) if clean else None
        if prev != key:
            clean.append((idx, event))

    story = [(idx, event) for idx, event in clean if idx >= 5]
    for pos, (_, event) in enumerate(story):
        if event["type"] == "text" and event["text"].startswith("设计"):
            return story[: pos + 1]
    return story

def local_source_path(src: str) -> Path:
    normalized = src[2:] if src.startswith("./") else src
    return SOURCE_BASE / normalized

def copy_story_images(indexed):
    OUT_IMG_DIR.mkdir(parents=True, exist_ok=True)
    count = 0
    for _, event in indexed:
        if event["type"] != "img":
            continue
        count += 1
        out_name = f"img-{count:03d}.webp"
        src_path = local_source_path(event["src"])
        with Image.open(src_path) as im:
            im = ImageOps.exif_transpose(im)
            if im.mode not in ("RGB", "L"):
                im = im.convert("RGB")
            elif im.mode == "L":
                im = im.convert("RGB")
            im.save(OUT_IMG_DIR / out_name, "WEBP", quality=88, method=6)
        event["out"] = out_name
    return count

def translate_caption(text: str) -> str:
    caption = text.lstrip("▲").strip()
    replacements = {
        "Run50-18 SC Vlog @Arsenan": "Run50-18 SC Vlog @Arsenan",
        "State-18 SC @Arsenan": "State-18 SC @Arsenan",
        "State-18 SC @Siqi": "State-18 SC @Siqi",
        "State-18 SC@Siqi": "State-18 SC @Siqi",
        "Pigeon Forge @Arsenan": "Pigeon Forge @Arsenan",
        "Golden Corral @Arsenan": "Golden Corral @Arsenan",
        "Greer @Arsenan": "Greer @Arsenan",
        "Jersey @Arsenan": "Jersey @Arsenan",
        "Expo @Arsenan": "Expo @Arsenan",
        "RV Airbnb @Arsenan": "RV Airbnb @Arsenan",
        "RV Airbnb @Hover": "RV Airbnb @Hover",
        "2Slow4Boston @Arsenan": "2Slow4Boston @Arsenan",
        "2Slow4Boston @Google": "2Slow4Boston @Google",
        "2Slow4Boston @DaMa": "2Slow4Boston @DaMa",
        "Miami Bus @Arsenan": "Aid Station @Arsenan",
        "Siqi @Arsenan": "Siqi @Arsenan",
        "Slow Slow Slow @Arsenan": "Slow Slow Slow @Arsenan",
        "K-Pot @Arsenan": "K-Pot @Arsenan",
    }
    for old, new in replacements.items():
        caption = caption.replace(old, new)
    return caption

def text_for(idx: int, text: str, lang: str) -> str:
    if lang == "zh":
        if text == "最慢才有奖：这场马拉松，有点反着来！":
            return "# 最慢才有奖：这场马拉松，有点反着来！"
        if text == "迟到半小时也没事，反正主打一个慢！":
            return "# 迟到半小时也没事，反正主打一个慢！"
        if text == "比赛日早晨：从房车出发":
            return "## 比赛日早晨：从房车出发"
        return text
    if is_caption(text):
        return translate_caption(text)
    if should_skip_text(text):
        return ""
    try:
        return EN_BY_INDEX[idx]
    except KeyError as exc:
        raise RuntimeError(f"Missing English translation for index {idx}: {text}") from exc

def render_text(idx: int, text: str, lang: str) -> str:
    value = text_for(idx, text, lang)
    if not value:
        return ""
    if text in ("前言", "后记") or value in ("Preface", "Postscript"):
        return f'<h2 class="section-label">{escape(value)}</h2>'
    if value.startswith("# "):
        return f"<h2>{escape(value[2:])}</h2>"
    if value.startswith("## "):
        return f"<h3>{escape(value[3:])}</h3>"
    if idx in (3, 4) or text.startswith(("📍", "🎽", "🦖", "🌿")) or value.startswith("🌿"):
        return f'<p class="place">{escape(value)}</p>'
    if value.startswith("- "):
        return f'<p class="end-mark">{escape(value)}</p>'
    if idx in (240, 241, 242):
        return f'<p class="credit-line">{escape(value)}</p>'
    return f"<p>{escape(value)}</p>"

def render_article(indexed, lang: str, img_prefix: str) -> str:
    parts = []
    skip_next = False
    for pos, (idx, event) in enumerate(indexed):
        if skip_next:
            skip_next = False
            continue
        if event["type"] == "img":
            caption = ""
            if pos + 1 < len(indexed):
                next_idx, next_event = indexed[pos + 1]
                if next_event["type"] == "text" and is_caption(next_event["text"]):
                    caption = text_for(next_idx, next_event["text"], lang)
                    skip_next = True
            src = img_prefix + event["out"]
            alt = caption or ("South Carolina Marathon photo" if lang == "en" else "南卡罗莱纳马拉松照片")
            figcaption = f"<figcaption>{escape(caption)}</figcaption>" if caption else ""
            parts.append(
                f'<figure><img src="{escape(src)}" alt="{escape(alt)}" loading="lazy" decoding="async">{figcaption}</figure>'
            )
            continue
        html_text = render_text(idx, event["text"], lang)
        if html_text:
            parts.append(html_text)
    return "\n      ".join(parts)

def page_css() -> str:
    return """
    :root {
      --paper: #edf3f7; /* Soft cool slate-blue */
      --surface: #ffffff;
      --ink: #20242b;
      --muted: #667085;
      --line: #d0dfe8; /* Matching border */
      --river: #0b67c2; /* Run50 blue */
      --brick: #a33a2b; /* Accent terracotta red */
      --gold: #b7892f;
      --leaf: #2f855a;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      background: linear-gradient(180deg, #eef5f6 0, var(--paper) 300px);
      color: var(--ink);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
      line-height: 1.78;
      letter-spacing: 0;
    }
    a { color: var(--river); text-decoration-thickness: 1px; text-underline-offset: 4px; }
    .story-nav {
      max-width: 860px;
      margin: 0 auto;
      padding: 18px 22px 0;
      display: flex;
      gap: 14px;
      color: var(--muted);
      font-size: 14px;
      justify-content: space-between;
    }
    .story-nav a {
      color: inherit;
      text-decoration: none;
      border-bottom: 1px solid transparent;
    }
    .story-nav a:hover { border-color: currentColor; }
    .page-header {
      max-width: 860px;
      margin: 0 auto;
      padding: 42px 22px 24px;
    }
    .kicker { margin: 0 0 14px; color: var(--brick); font-size: 14px; font-weight: 800; }
    h1 {
      margin: 0;
      max-width: 780px;
      color: #111827;
      font-size: 34px;
      line-height: 1.22;
      font-weight: 850;
      letter-spacing: 0;
    }
    .meta {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      align-items: center;
      margin-top: 18px;
      color: var(--muted);
      font-size: 14px;
    }
    .meta span,
    .meta a {
      display: inline-flex;
      align-items: center;
      min-height: 30px;
      padding: 3px 10px;
      border: 1px solid var(--line);
      border-radius: 999px;
      background: rgba(255, 255, 255, .72);
      color: var(--muted);
      text-decoration: none;
    }
    .dek {
      margin: 22px 0 0;
      padding-left: 16px;
      border-left: 4px solid var(--river);
      color: #344054;
      font-size: 15px;
    }
    .article-shell {
      background: var(--surface);
      border-top: 1px solid var(--line);
      border-bottom: 1px solid var(--line);
      box-shadow: 0 24px 60px rgba(15, 23, 42, .06);
    }
    .article-body {
      max-width: 760px;
      margin: 0 auto;
      padding: 44px 22px 56px;
      overflow-wrap: anywhere;
    }
    .article-body h2 {
      display: flex;
      align-items: center;
      gap: 12px;
      margin: 0 0 26px;
      color: #111827;
      font-size: 28px;
      line-height: 1.25;
      font-weight: 850;
      letter-spacing: 0;
    }
    .article-body h2:not(:first-child) { margin-top: 54px; }
    .article-body h2::before {
      content: "";
      width: 34px;
      height: 3px;
      border-radius: 999px;
      background: var(--gold);
      flex: 0 0 auto;
    }
    .article-body h3 {
      margin: 36px 0 16px;
      color: #111827;
      font-size: 22px;
      line-height: 1.3;
      font-weight: 800;
    }
    .article-body .section-label {
      color: #111827;
      font-size: 28px;
      letter-spacing: 0;
      text-transform: none;
      border-top: 0;
      padding-top: 0;
    }
    .article-body p { margin: 0 0 17px; font-size: 17px; line-height: 1.86; }
    .place {
      margin: -8px 0 24px;
      color: var(--muted);
      font-size: 15px;
      font-weight: 700;
    }
    .article-body figure { margin: 28px 0 30px; }
    .article-body img {
      display: block;
      width: 100%;
      max-width: 100%;
      height: auto;
      border-radius: 8px;
      background: #e1e8dc;
      box-shadow: 0 16px 40px rgba(15, 23, 42, .12);
    }
    figcaption {
      margin-top: 9px;
      color: #7a828c;
      font-size: 13px;
      line-height: 1.55;
      text-align: center;
    }
    .article-body hr { width: 72px; height: 1px; margin: 34px auto; border: 0; background: var(--line); }
    .end-mark,
    .credit-line {
      text-align: center;
      color: var(--muted);
    }
    .page-footer {
      max-width: 860px;
      margin: 0 auto;
      padding: 0 22px 44px;
      color: var(--muted);
      text-align: center;
      font-size: 14px;
    }
    @media (max-width: 640px) {
      .story-nav { flex-wrap: wrap; }
      .page-header { padding: 30px 18px 20px; }
      h1 { font-size: 26px; }
      .article-body { padding: 34px 18px 44px; }
      .article-body h2,
      .article-body .section-label { font-size: 24px; }
      .article-body p { font-size: 16px; }
      .article-body figure { margin-left: -2px; margin-right: -2px; }
    }
    """

def facebook_css() -> str:
    return """
    :root {
      --red: #0b67c2; /* Run50 blue for accents */
      --ink: #111111;
      --muted: #666666;
      --line: #dddddd;
      --soft: #f0f4f8;
      --paper: #ffffff;
      --slate: #64748b;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      background: var(--paper);
      color: var(--ink);
      font-family: Arial, Helvetica, sans-serif;
      line-height: 1.6;
      letter-spacing: 0;
    }
    a { color: inherit; text-decoration-thickness: 1px; text-underline-offset: 3px; }
    img { max-width: 100%; height: auto; }
    .breaking {
      background: var(--red);
      color: #ffffff;
      font-size: 13px;
      font-weight: 900;
      letter-spacing: .08em;
      text-transform: uppercase;
    }
    .breaking-inner,
    .site-head-inner,
    .article {
      width: min(1180px, calc(100% - 32px));
      margin: 0 auto;
    }
    .breaking-inner,
    .site-head-inner {
      min-height: 38px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
    }
    .breaking a,
    .section-nav a { color: inherit; text-decoration: none; }
    .site-head {
      border-bottom: 1px solid var(--line);
      background: #ffffff;
    }
    .site-head-inner {
      min-height: 72px;
    }
    .wordmark {
      color: var(--red);
      font-size: 28px;
      font-weight: 900;
      letter-spacing: 0;
      text-decoration: none;
    }
    .section-nav {
      display: flex;
      flex-wrap: wrap;
      justify-content: flex-end;
      gap: 14px;
      color: #333333;
      font-size: 13px;
      font-weight: 800;
      text-transform: uppercase;
    }
    .hero {
      padding: 34px 0 22px;
      border-bottom: 1px solid var(--line);
    }
    .label {
      display: inline-flex;
      align-items: center;
      min-height: 28px;
      padding: 4px 9px;
      background: var(--red);
      color: #ffffff;
      font-size: 12px;
      font-weight: 900;
      letter-spacing: .08em;
      text-transform: uppercase;
    }
    h1 {
      margin: 18px 0 14px;
      max-width: 980px;
      font-size: clamp(2.4rem, 7vw, 5.6rem);
      line-height: .92;
      letter-spacing: 0;
    }
    .dek {
      max-width: 820px;
      margin: 0;
      color: #333333;
      font-size: clamp(1.08rem, 2vw, 1.32rem);
      line-height: 1.55;
    }
    .byline {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-top: 18px;
      color: var(--muted);
      font-size: 13px;
      font-weight: 800;
      text-transform: uppercase;
    }
    .byline span,
    .byline a {
      min-height: 30px;
      display: inline-flex;
      align-items: center;
      padding: 4px 9px;
      background: var(--soft);
      text-decoration: none;
    }
    .lead-media {
      margin: 26px 0 0;
      border-top: 6px solid var(--red);
    }
    .lead-media img {
      display: block;
      width: 100%;
      aspect-ratio: 1200 / 630;
      object-fit: cover;
      background: var(--soft);
    }
    figcaption {
      margin-top: 8px;
      color: var(--muted);
      font-size: 12px;
    }
    .story-grid {
      display: grid;
      grid-template-columns: minmax(220px, 300px) minmax(0, 720px);
      gap: 34px;
      align-items: start;
      padding: 34px 0 12px;
    }
    .rail {
      position: sticky;
      top: 18px;
      display: grid;
      gap: 18px;
    }
    .brief-box,
    .share-note,
    .context-note,
    .section-bridge {
      border: 1px solid var(--line);
      padding: 18px;
    }
    .brief-box {
      border: 0;
      border-top: 5px solid var(--red);
      background: var(--soft);
      padding: 16px;
    }
    .brief-box h2,
    .section-bridge h2 {
      margin: 0 0 12px;
      font-size: 19px;
      line-height: 1.1;
    }
    dl { margin: 0; display: grid; gap: 12px; }
    dt {
      color: var(--red);
      font-size: 12px;
      font-weight: 900;
      text-transform: uppercase;
      letter-spacing: .08em;
    }
    dd {
      margin: 2px 0 0;
      color: #222222;
      font-size: 14px;
      line-height: 1.45;
    }
    .share-note {
      color: #333333;
      font-size: 14px;
      line-height: 1.6;
    }
    .share-note strong {
      display: block;
      color: var(--ink);
      text-transform: uppercase;
      font-size: 12px;
      letter-spacing: .08em;
      margin-bottom: 6px;
    }
    .copy {
      min-width: 0;
    }
    .copy p {
      margin: 0 0 19px;
      font-family: Georgia, "Times New Roman", serif;
      font-size: 19px;
      line-height: 1.72;
    }
    .copy h2 {
      margin: 36px 0 16px;
      padding-top: 20px;
      border-top: 1px solid var(--line);
      font-size: 30px;
      line-height: 1.1;
      letter-spacing: 0;
    }
    .copy h3 {
      margin: 24px 0 12px;
      font-size: 22px;
      line-height: 1.25;
      font-weight: 800;
    }
    .copy .section-label {
      color: var(--red);
      font-size: 13px;
      font-family: Arial, Helvetica, sans-serif;
      font-weight: 900;
      text-transform: uppercase;
      letter-spacing: .08em;
      border-top: 1px solid var(--line);
      padding-top: 24px;
    }
    .copy .place {
      margin: 0 0 18px;
      color: var(--red);
      font-family: Arial, Helvetica, sans-serif;
      font-size: 13px;
      font-weight: 900;
      letter-spacing: .08em;
      text-transform: uppercase;
    }
    .copy figure {
      margin: 25px 0 30px;
    }
    .copy figure img {
      display: block;
      width: 100%;
      border: 1px solid var(--line);
      background: var(--soft);
    }
    .context-note,
    .section-bridge {
      margin: 0 0 28px;
    }
    .context-note {
      padding: 18px 0 18px 18px;
      border: 0;
      border-left: 7px solid var(--red);
      background: #fafafa;
    }
    .context-note p,
    .section-bridge p {
      font-family: Arial, Helvetica, sans-serif;
      font-size: 16px;
      line-height: 1.65;
    }
    .section-bridge {
      margin: 40px 0 26px;
      border: 0;
      border-top: 5px solid var(--red);
      background: #f7f7f7;
    }
    .section-bridge h2 {
      margin: 0 0 10px;
      padding: 0;
      border: 0;
      font-size: 24px;
    }
    .context-note p:last-child,
    .section-bridge p:last-child {
      margin-bottom: 0;
    }
    .copy hr {
      width: 74px;
      height: 5px;
      margin: 34px 0;
      border: 0;
      background: var(--red);
    }
    .end-mark,
    .credit-line {
      text-align: center;
      color: var(--muted);
    }
    .zz-engagement {
      max-width: 1180px;
      padding-left: 0;
      padding-right: 0;
    }
    .zz-engagement-kicker,
    .zz-engagement h2 {
      color: var(--red);
    }
    @media (max-width: 820px) {
      .story-grid { grid-template-columns: 1fr; }
      .rail { position: static; }
    }
    @media (max-width: 860px) {
      .site-head-inner {
        align-items: flex-start;
        flex-direction: column;
        padding: 16px 0;
      }
      .section-nav {
        justify-content: flex-start;
      }
    }
    """

def engagement(locale: str, page_key: str, mount_id: str) -> str:
    is_zh = locale == "zh-CN"
    kicker = "留言 / 阅读" if is_zh else "Comments / Views"
    title = "跑完也可以聊两句" if is_zh else "Say something after the run"
    note = "不用登录就可以留言，新留言会直接显示。" if is_zh else "No account is needed to submit a comment. New comments appear right away."
    loading = "留言区加载中..." if is_zh else "Loading comments..."
    views = "阅读" if is_zh else "Views"
    return f'''
  <section class="zz-engagement" data-zz-engagement data-locale="{locale}" data-page-key="{page_key}">
    <div class="zz-engagement-shell">
      <div>
        <p class="zz-engagement-kicker">{escape(kicker)}</p>
        <h2>{escape(title)}</h2>
        <p class="zz-engagement-note">{escape(note)}</p>
        <div class="zz-engagement-stats"><span class="zz-engagement-stat" id="busuanzi_container_page_pv"><span>{escape(views)}</span><strong id="busuanzi_value_page_pv" data-zz-view-count>--</strong></span></div>
      </div>
      <div class="zz-engagement-card"><div id="{mount_id}" data-zz-supabase-comments></div><p class="zz-engagement-status" data-zz-engagement-status>{escape(loading)}</p></div>
    </div>
  </section>'''

def normal_page(lang: str, article: str) -> str:
    is_zh = lang == "zh"
    title = "Run50 #第18州｜南卡罗莱纳：反“波士顿”马拉松｜小区绕圈20，世界上最无聊42公里？" if is_zh else "Run50 #18 | South Carolina: Too Slow for Boston Marathon"
    short = "Run50 #18 | South Carolina Marathon"
    desc = (
        "南卡罗莱纳小镇Greer的2Slow4Boston马拉松，一个专为跑不进波马的人准备的反向比赛。在宁静的小区里绕圈20次，收获一块骡子拉大叔的奇特奖牌。"
        if is_zh
        else "Race date: April 14, 2024. Running U.S. State 18: Too Slow for Boston Marathon in Greer, South Carolina, featuring a 20-lap neighborhood loop challenge, trailer RV camping, and a stubborn mule finisher medal."
    )
    canonical = f"{SITE}/run50/stories/{'chinese' if is_zh else 'english'}/{SLUG}.html"
    other = f"../{'english' if is_zh else 'chinese'}/{SLUG}.html"
    fb = f"../../facebook/{SLUG}.html"
    nav = (
        f'<a href="./index.html">← 中文故事</a><a href="{other}">English</a><a href="{fb}">Facebook</a><a href="../../index.html">Run50</a>'
        if is_zh
        else f'<a href="./index.html">← English Stories</a><a href="{other}">中文</a><a href="{fb}">Facebook</a><a href="../../index.html">Run50</a>'
    )
    kicker = "Run50 #第18州 · 南卡罗莱纳" if is_zh else "Run50 #18 · South Carolina"
    footer = "© 2024-2026 ArsenanZZ. Built with love."
    locale = "zh-CN" if is_zh else "en"
    key = f"run50-{SLUG}-zh" if is_zh else f"run50-{SLUG}-en"
    mount = f"supabase-comments-south-carolina-zh" if is_zh else f"supabase-comments-south-carolina-en"
    og_image = f"{SITE}/assets/og-run50-{SLUG}-icons.png?v={VERSION}"
    return f'''<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)}</title>
  <meta name="description" content="{escape(desc)}">
  <link rel="canonical" href="{canonical}">
  <meta property="og:title" content="{escape(title)}">
  <meta property="og:description" content="{escape(desc)}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="{canonical}">
  <meta property="og:site_name" content="ArsenanZZ">
  <meta property="og:locale" content="{locale}">
  <meta property="og:image" content="{og_image}">
  <meta property="og:image:secure_url" content="{og_image}">
  <meta property="og:image:type" content="image/png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="South Carolina Marathon cover with RV caravan, pine trees and stubborn mule.">
  <meta property="article:author" content="Arsenan">
  <meta property="article:published_time" content="2024-04-14T07:00:00-05:00">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{escape(short)}">
  <meta name="twitter:description" content="{escape(desc)}">
  <meta name="twitter:image" content="{og_image}">
  <link rel="stylesheet" href="../../../assets/zz-engagement.css?v={VERSION}">
  <style>{page_css()}</style>
</head>
<body>
  <nav class="story-nav" aria-label="页面导航">
    {nav}
  </nav>
  <header class="page-header">
    <p class="kicker">{escape(kicker)}</p>
    <h1>{escape(title)}</h1>
    <div class="meta">
      <span>By Arsenan</span>
      <span>Race: April 14, 2024</span>
      <a href="https://mp.weixin.qq.com/s/7n-M3508Ww7k5e2o-W_files" target="_blank" rel="noopener">Original WeChat &nearr;</a>
    </div>
    <div class="dek">{escape(desc)}</div>
  </header>
  <main class="article-shell">
    <article class="article-body">
      {article}
    </article>
  </main>
  {engagement(locale, key, mount)}
  <footer class="page-footer">{escape(footer)}</footer>
  <script src="../../../assets/zz-engagement-config.js?v={VERSION}"></script>
  <script src="../../../assets/zz-engagement.js?v={VERSION}"></script>
</body>
</html>
'''

def facebook_page(content: str) -> str:
    title = "I ran South Carolina's most boring marathon to check off State 18, and it completely won me over"
    desc = "Race date: April 14, 2024. Running U.S. State 18: Too Slow for Boston Marathon in Greer, South Carolina, featuring a 20-lap neighborhood loop challenge, trailer RV camping, and a stubborn mule finisher medal."
    canonical = f"{SITE}/run50/facebook/{SLUG}.html"
    locale = "en"
    key = f"run50-{SLUG}-facebook-en"
    mount = f"supabase-comments-south-carolina-facebook-en"
    og_image = f"{SITE}/assets/og-run50-{SLUG}-icons.png?v={VERSION}"
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Too Slow for Boston Marathon | Run50 Facebook</title>
  <meta name="description" content="{escape(desc)}">
  <link rel="canonical" href="{canonical}">
  <meta property="og:title" content="{escape(title)}">
  <meta property="og:description" content="{escape(desc)}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="{canonical}">
  <meta property="og:site_name" content="ArsenanZZ">
  <meta property="og:locale" content="en_US">
  <meta property="og:image" content="{og_image}">
  <meta property="og:image:secure_url" content="{og_image}">
  <meta property="og:image:type" content="image/png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="South Carolina Marathon cover with RV caravan, pine trees and stubborn mule.">
  <meta property="article:author" content="Arsenan">
  <meta property="article:published_time" content="2024-04-14T07:00:00-05:00">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{escape(title)}">
  <meta name="twitter:description" content="{escape(desc)}">
  <meta name="twitter:image" content="{og_image}">
  <link rel="stylesheet" href="../../assets/zz-engagement.css?v={VERSION}">
  <style>{facebook_css()}</style>
</head>
<body>
  <div class="breaking">
    <div class="breaking-inner">
      <a href="./index.html">Run50 Facebook</a>
      <span>Race date: April 14, 2024</span>
    </div>
  </div>
  <header class="site-head">
    <div class="site-head-inner">
      <a class="wordmark" href="./index.html" aria-label="Run50 Facebook home">RUN50 WORLD</a>
      <nav class="section-nav" aria-label="Story navigation">
        <a href="../index.html">Run50</a>
        <a href="../stories/english/{SLUG}.html">Full English Story</a>
        <a href="../stories/chinese/{SLUG}.html" style="display:none;">Chinese Original</a>
        <a href="../stories/chinese/{SLUG}.html">Chinese Original</a>
      </nav>
    </div>
  </header>
  <article class="article">
    <section class="hero">
      <span class="label">World / USA / Marathon / South Carolina</span>
      <h1>{escape(title)}</h1>
      <p class="dek">{escape(desc)}</p>
      <div class="byline">
        <span>By Arsenan</span>
        <span>Race: April 14, 2024</span>
        <span>Greer, SC</span>
        <span>Run50 #18</span>
      </div>
      <figure class="lead-media"><img src="../../assets/og-run50-{SLUG}-icons.png?v={VERSION}" alt="Icon-style South Carolina Marathon cover"><figcaption>South Carolina icon cover with travel trailer RV caravan, pine trees, and stubborn mule silhouette.</figcaption></figure>
    </section>
    <section class="story-grid">
      <aside class="rail">
        <section class="brief-box"><h2>At a glance</h2><dl><div><dt>Race</dt><dd>Too Slow for Boston Marathon (2Slow4Boston), Run50 State 18.</dd></div><div><dt>Course</dt><dd>A 20-lap neighborhood road loop (1.31 miles per loop) in Greer, South Carolina.</dd></div><div><dt>What stayed with me</dt><dd>Living in a trailer RV, the friendly neighborhood vibes, clicker lap-counting system, and the humor of "Too Slow for Boston".</dd></div></dl></section>
      </aside>
      <div class="copy full-story">
        {content}
      </div>
    </section>
  </article>
  {engagement("en", key, mount)}
  <script src="../../assets/zz-engagement-config.js?v={VERSION}"></script>
  <script src="../../assets/zz-engagement.js?v={VERSION}"></script>
</body>
</html>
'''

SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 750" role="img" aria-labelledby="title desc">
<title id="title">Greer 2Slow4Boston icon cover</title>
<desc id="desc">Icon style cover with Greer title, Run50 South Carolina badge, caravan RV trailer, pine trees, and stubborn mule.</desc>
<rect width="1200" height="750" fill="#bae6fd"/>
<g transform="translate(70 104)">
  <text x="0" y="0" font-family="Arial, Helvetica, sans-serif" font-size="66" font-weight="900" fill="#20242b">GREER</text>
  <text x="0" y="46" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="700" fill="#0b67c2">2SLOW4BOSTON · RV LOOP</text>
</g>
<rect x="758" y="62" width="364" height="166" rx="22" fill="#ffffff" stroke="#20242b" stroke-width="8"/>
<text x="790" y="122" font-family="Arial, Helvetica, sans-serif" font-size="41" font-weight="900" fill="#20242b">Run50 #18</text>
<text x="790" y="182" font-family="Arial, Helvetica, sans-serif" font-size="46" font-weight="900" fill="#0b67c2">S. CAROLINA</text>
<circle cx="1052" cy="352" r="62" fill="#fbbf24"/>
<path d="M0 612 C190 540 330 590 500 538 C690 480 830 590 1000 545 C1100 518 1168 515 1200 498 L1200 750 L0 750 Z" fill="#86efac"/>
<path d="M0 682 C180 620 370 705 560 650 C760 592 930 690 1200 620 L1200 750 L0 750 Z" fill="#4ade80"/>

<!-- Pine Trees -->
<g>
  <rect x="540" y="300" width="20" height="200" fill="#78350f"/>
  <polygon points="470,360 630,360 550,240" fill="#15803d"/>
  <polygon points="490,280 610,280 550,180" fill="#15803d"/>
  <polygon points="510,200 590,200 550,120" fill="#15803d"/>
</g>

<!-- Caravan RV Trailer -->
<g transform="translate(30, 20)">
  <rect x="150" y="340" width="300" height="150" rx="20" fill="#cbd5e1" stroke="#334155" stroke-width="6"/>
  <rect x="200" y="370" width="80" height="50" rx="5" fill="#e2e8f0" stroke="#334155" stroke-width="4"/>
  <rect x="340" y="370" width="50" height="120" fill="#94a3b8" stroke="#334155" stroke-width="4"/>
  <circle cx="300" cy="490" r="30" fill="#334155" stroke="#1e293b" stroke-width="4"/>
  <line x1="150" y1="470" x2="100" y2="490" stroke="#334155" stroke-width="8"/>
</g>

<!-- Stubborn Mule Mascot -->
<g transform="translate(-10, 0)">
  <polygon points="840,380 870,350 890,410 860,430" fill="#27272a"/>
  <ellipse cx="840" cy="345" rx="30" ry="25" fill="#27272a"/>
  <ellipse cx="805" cy="352" rx="25" ry="17" fill="#27272a"/>
  <polygon points="840,325 835,280 855,300" fill="#27272a"/>
  <polygon points="850,325 855,280 865,305" fill="#27272a"/>
  <ellipse cx="910" cy="440" rx="50" ry="40" fill="#27272a"/>
  <line x1="880" y1="450" x2="880" y2="540" stroke="#27272a" stroke-width="12"/>
  <line x1="900" y1="450" x2="900" y2="540" stroke="#27272a" stroke-width="12"/>
  <line x1="930" y1="450" x2="930" y2="540" stroke="#27272a" stroke-width="12"/>
  <line x1="950" y1="450" x2="950" y2="540" stroke="#27272a" stroke-width="12"/>
  <line x1="955" y1="420" x2="985" y2="480" stroke="#27272a" stroke-width="8"/>
</g>

<path d="M0 702 C180 675 340 720 520 695 C720 668 900 720 1200 678 L1200 750 L0 750 Z" fill="#16a34a"/>
</svg>
"""

def font(size, bold=False):
    name = "arialbd.ttf" if bold else "arial.ttf"
    try:
        return ImageFont.truetype(name, size)
    except IOError:
        try:
            return ImageFont.truetype("LiberationSans-Bold.ttf" if bold else "LiberationSans-Regular.ttf", size)
        except IOError:
            return ImageFont.load_default()

def write_clean(path: Path, text: str):
    path.write_text(text, encoding="utf-8", newline="\n")

def write_svg():
    write_clean(REPO / "assets" / f"thumb-run50-{SLUG}-icons.svg", SVG)

def write_png():
    image = Image.new("RGB", (1200, 630), "#bae6fd")
    draw = ImageDraw.Draw(image)
    text_color = "#20242b"
    blue = "#0b67c2"
    
    # Title
    draw.text((64, 64), "GREER", font=font(66, True), fill=text_color)
    draw.text((66, 142), "2SLOW4BOSTON, RV LOOP", font=font(25, True), fill=blue)
    
    # Badge Box
    draw.rounded_rectangle((760, 64, 1122, 228), radius=22, fill="#ffffff", outline=text_color, width=7)
    draw.text((790, 112), "Run50 #18", font=font(40, True), fill=text_color)
    draw.text((790, 166), "S. CAROLINA", font=font(46, True), fill=blue)
    
    # Sun
    draw.ellipse((980, 260, 1078, 358), fill="#fbbf24")
    
    # Hills
    draw.polygon([(0, 515), (160, 455), (330, 520), (515, 465), (710, 420), (900, 510), (1080, 460), (1200, 438), (1200, 630), (0, 630)], fill="#86efac")
    draw.polygon([(0, 584), (190, 535), (380, 596), (560, 545), (770, 598), (980, 548), (1200, 516), (1200, 630), (0, 630)], fill="#4ade80")
    draw.rectangle((0, 592, 1200, 630), fill="#16a34a")
    
    # Pine Tree Background
    draw.rectangle((540, 280, 560, 480), fill="#78350f")
    draw.polygon([(470, 340), (630, 340), (550, 220)], fill="#15803d")
    draw.polygon([(490, 260), (610, 260), (550, 160)], fill="#15803d")
    draw.polygon([(510, 180), (590, 180), (550, 100)], fill="#15803d")
    
    # RV Caravan
    # rounded rect: x=180, y=360, w=300, h=150
    draw.rounded_rectangle((180, 360, 480, 510), radius=20, fill="#cbd5e1", outline="#334155", width=6)
    draw.rounded_rectangle((230, 390, 310, 440), radius=5, fill="#e2e8f0", outline="#334155", width=4)
    draw.rectangle((370, 390, 420, 510), fill="#94a3b8", outline="#334155", width=4)
    draw.ellipse((300, 480, 360, 540), fill="#334155", outline="#1e293b", width=4)
    draw.line((180, 490, 130, 510), fill="#334155", width=8)
 
    # Stubborn Mule Mascot
    draw.polygon([(830, 380), (860, 350), (880, 410), (850, 430)], fill="#27272a") # neck
    draw.ellipse((800, 320, 860, 370), fill="#27272a") # head
    draw.ellipse((770, 327, 820, 361), fill="#27272a") # snout
    draw.polygon([(830, 325), (825, 280), (845, 300)], fill="#27272a") # ear 1
    draw.polygon([(840, 325), (845, 280), (855, 305)], fill="#27272a") # ear 2
    draw.ellipse((870, 390, 970, 470), fill="#27272a") # body
    draw.line((890, 440, 890, 530), fill="#27272a", width=12) # leg 1
    draw.line((910, 440, 910, 530), fill="#27272a", width=12) # leg 2
    draw.line((940, 440, 940, 530), fill="#27272a", width=12) # leg 3
    draw.line((960, 440, 960, 530), fill="#27272a", width=12) # leg 4
    draw.line((950, 410, 980, 470), fill="#27272a", width=8) # tail
 
    image.save(REPO / "assets" / f"og-run50-{SLUG}-icons.png", "PNG")

def update_indexes():
    new_card_zh = f'''      <a class="story-card run-50" href="./{SLUG}.html">
        <img src="../../../assets/thumb-run50-{SLUG}-icons.svg?v={VERSION}" alt="南卡罗莱纳马拉松城市图标封面" loading="lazy" decoding="async">
        <div class="story-copy">
          <p class="story-meta">南卡罗莱纳Greer · 2024.04.14</p>
          <h2 class="story-title">Run50 #第18州｜南卡罗莱纳马拉松</h2>
          <p class="story-desc">南卡罗莱纳小镇Greer的2Slow4Boston马拉松，一个专为跑不进波马的人准备的反向比赛。在宁静的小区里绕圈20次，收获一块骡子拉大叔的奇特奖牌。</p>
          <div class="story-foot">
            <span>长文图记</span>
            <span>阅读 →</span>
          </div>
        </div>
      </a>
    </section>'''

    new_card_en = f'''      <a class="story-card run-50" href="./{SLUG}.html">
        <img src="../../../assets/thumb-run50-{SLUG}-icons.svg?v={VERSION}" alt="Icon cover for South Carolina Marathon" />
        <div class="story-card-content">
          <div class="meta">South Carolina · Greer · 2024.04.14</div>
          <h2>Too Slow for Boston Marathon: loops, RV camping, and the stubborn mule</h2>
          <p>A U.S. State 18 quest going against the speed-worshipping norm, completing 20 neighborhood loops under the sun, and celebrating with local block-party volunteers.</p>
        </div>
      </a>
    </section>'''

    new_card_fb = f'''    <a class="story-card run-50" href="./{SLUG}.html">
      <div>
        <p class="eyebrow">World / USA / Marathon</p>
        <h2>Too Slow for Boston gave me a 26.2-mile run with the stubborn mule medal</h2>
        <p>Race date: April 14, 2024. A neighborhood loop road race designed for those who can't qualify for Boston—featuring trailer RV camping, a clicker lap-counting system, and a trophy for the slowest.</p>
        <div class="meta">
          <span>Greer, SC</span>
          <span>Stubborn Mule secured</span>
          <span>Run50 Facebook</span>
        </div>
      </div>
      <img src="../../assets/thumb-run50-{SLUG}-icons.svg?v={VERSION}" alt="Icon-style South Carolina Marathon cover">
    </a>
  </main>'''

    # Update Chinese index
    zh_idx_path = REPO / "run50" / "stories" / "chinese" / "index.html"
    zh_text = zh_idx_path.read_text(encoding="utf-8")
    if f"{SLUG}.html" not in zh_text:
        zh_text = zh_text.replace("    </section>", new_card_zh)
        write_clean(zh_idx_path, zh_text)

    # Update English index
    en_idx_path = REPO / "run50" / "stories" / "english" / "index.html"
    en_text = en_idx_path.read_text(encoding="utf-8")
    if f"{SLUG}.html" not in en_text:
        en_text = en_text.replace("    </section>", new_card_en)
        write_clean(en_idx_path, en_text)

    # Update Facebook index
    fb_idx_path = REPO / "run50" / "facebook" / "index.html"
    fb_text = fb_idx_path.read_text(encoding="utf-8")
    if f"{SLUG}.html" not in fb_text:
        fb_text = fb_text.replace("  </main>", new_card_fb)
        write_clean(fb_idx_path, fb_text)

def main():
    zh_path = REPO / "run50" / "stories" / "chinese" / f"{SLUG}.html"
    en_path = REPO / "run50" / "stories" / "english" / f"{SLUG}.html"
    fb_path = REPO / "run50" / "facebook" / f"{SLUG}.html"

    print("Extracting raw story blocks...")
    indexed_story = extract_story()
    
    print("Processing and copying WebP images...")
    img_count = copy_story_images(indexed_story)
    print(f"Copied {img_count} optimized WebP images.")

    print("Rendering Chinese Page...")
    zh_article = render_article(indexed_story, "zh", f"Run50-South-Carolina-Marathon-clean_files/")
    write_clean(zh_path, normal_page("zh", zh_article))

    print("Rendering English Page...")
    en_article = render_article(indexed_story, "en", f"../chinese/Run50-South-Carolina-Marathon-clean_files/")
    write_clean(en_path, normal_page("en", en_article))

    print("Rendering Facebook Page...")
    fb_article = render_article(indexed_story, "en", f"../stories/chinese/Run50-South-Carolina-Marathon-clean_files/")
    write_clean(fb_path, facebook_page(fb_article))

    print("Generating SVG Thumbnail Cover...")
    write_svg()

    print("Generating PNG OpenGraph Cover...")
    write_png()

    print("Registering cards on Listing Indexes...")
    update_indexes()

    print("Done! South Carolina Marathon story successfully published.")

if __name__ == "__main__":
    main()
