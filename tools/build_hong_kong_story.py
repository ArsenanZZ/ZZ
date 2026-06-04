from pathlib import Path
from lxml import html
from html import escape
from PIL import Image, ImageDraw, ImageFont
import re


REPO = Path(r"C:\Users\ZZ\Documents\Github\ZZ")
SOURCE_BASE = Path(r"Z:\ZhennanZ Folder\000-Marathon-Story-2024-2025\20251123-Hong Kong Marathon\55-Web")
SOURCE_HTML = next(p for p in SOURCE_BASE.iterdir() if p.suffix.lower() == ".html")
SOURCE_FILES = next(p for p in SOURCE_BASE.iterdir() if p.is_dir() and p.name.endswith("_files"))
SITE = "https://arsenanzz.github.io/ZZ"
OUT_IMG_DIR = REPO / "run50" / "stories" / "chinese" / "RunCN-Hong-Kong-Marathon-clean_files"


EN_BY_INDEX = {
    0: "Preface",
    1: "# Wrapping up the trip with a run in Hong Kong",
    2: "Hong Kong, China",
    3: "My two-and-a-half-month trip in China was getting close to the end.",
    4: "During that final week, my father-in-law, mother-in-law, and Third Uncle were incredibly warm. They took my parents and my aunt around a few places near Foshan.",
    7: "That weekend, I would be flying back to the United States from Hong Kong, so crossing from Shenzhen into Hong Kong made sense. With my father-in-law leading the way, we also stopped by Window of the World, a light little ending to a long trip.",
    10: "Early the next morning, I officially entered Hong Kong through Shenzhen Bay Port. Since I already had a flight ticket to the United States, I did not need a Hong Kong and Macau travel permit.",
    13: "Of course, there was another important reason for the trip: I was going to run the Kerry Hong Kong Streetathon. The timing was almost too perfect. It felt like a memorable closing note for this long, full China trip.",
    17: "# Hong Kong, the old Pearl of the Orient",
    18: "To be honest, people from my generation have a bit of a filter for Hong Kong. We grew up on Hong Kong movies, TV dramas, and Cantopop: Stephen Chow's nonsense comedy, Andy Lau's heroic cool, all of it.",
    19: "From the cassette tapes of the Four Heavenly Kings to TVB theme songs, from neon-lit Kowloon to the skyline around Victoria Harbour, Hong Kong felt like the definition of modern, stylish, fast-moving city life.",
    22: "If you zoom out a little, Hong Kong's history and culture really are special. It went through a colonial period and then a long stretch of fast development.",
    25: "Chinese and Western cultures mixed here. The language, buildings, and way of living all carry that unmistakable Hong Kong flavor. Looking at the city now, the old filter has faded a bit, and what is left feels more real after the spell breaks.",
    26: "This was my first proper visit to Hong Kong. Passing through before did not count. I used this very niche Kerry Hong Kong Streetathon as a way to finally get to know the city a little.",
    29: "Why do I call it niche? Before the race, I asked a local Hong Kong running expert about it, and even she had never heard of the event.",
    31: "# Tsim Sha Tsui, Causeway Bay, and Victoria Harbour",
    32: "The bus from Shenzhen Bay to K11 in Tsim Sha Tsui took about forty minutes. As soon as I got off, I realized something: Hong Kong streets are narrow, and my two huge suitcases plus one giant backpack looked painfully out of place. I dragged everything toward the capsule hotel in Windsor Mansion.",
    35: "Windsor Mansion was covered in bamboo scaffolding and under renovation, which did not exactly inspire confidence. The entrance was so small I almost missed it. Inside, the building felt so old that I immediately thought of Chungking Mansions, with a group of South Asian guys gathered near the elevators.",
    36: "The capsule hotel would not let me check in until after four. Luckily, a kind Spanish guy helped me open the door, so I could finally put down all that oversized luggage.",
    41: "After dropping my stuff, I took the MTR to Kwun Tong Promenade for packet pickup. You can use Alipay directly on the Hong Kong subway, which is pretty convenient. I also bought an Octopus card as a backup and exchanged a little Hong Kong cash, so I was basically covered for every payment situation.",
    46: "My first impression of Kwun Tong Promenade was really good: dense office towers on one side, runners and walkers on the road, people strolling along the water, and a sea breeze coming through.",
    53: "There was graffiti on a lot of the walls, and the race expo was set up under the elevated road. The atmosphere was lively. The volunteers were efficient, I had booked a pickup time in advance, and there was almost no line. Some volunteers could speak Mandarin too, so the whole process was smooth.",
    58: "After picking up my race packet, I figured the next day's start was at Victoria Park, so I went to scout it on the way. From Kwun Tong I took the MTR to Causeway Bay and passed Tin Hau Station. For a second, my brain automatically started playing Next Stop, Tin Hau, and scenes from Young and Dangerous flashed back too. Very much an era thing.",
    61: "Coming out of Causeway Bay Station, I was right at Hong Kong's Times Square, and the crowd was honestly a bit much. When I looked up, the narrow triangular old building glowing in the sunset was right there. That is the Lee Garden Road tong lau, a classic symbol of Hong Kong's dense urban look because it is so thin and sharp that tourists always photograph it.",
    64: "I found a McDonald's to fill my stomach first. I was worried I might not have enough cash, so I went back to the Bank of China ATM in the station and took out a little more. In reality, most places in Hong Kong now take Alipay, which is both easy and painless.",
    69: "Walking from Times Square to Victoria Park, the city was loud, but the park suddenly got quiet. It felt like a smaller version of New York's Central Park. Traffic and crowds were only a few steps away, yet inside people were strolling, walking dogs, and running slowly. Hong Kong people really know how to find their rhythm.",
    78: "Keep walking toward the water and you reach East Coast Park Precinct. This place has become pretty popular in the last couple of years. The waterfront path gives you a clear view of the Kowloon skyline.",
    83: "The spiral-looking structure by the water is called The Lookout. Planning started in 2015, and later it became a landmark in the Kwun Tong waterfront redevelopment. This used to be an industrial pier area, now turned into public waterfront space. The tower is meant to suggest setting sail, and it showed up several times in The Queen of News 2.",
    90: "The evening light was beautiful. The whole coastline turned golden. People were walking dogs, pushing kids, taking photos. I also met a few guys who were running the marathon the next day, and we helped each other take pictures.",
    97: "After packet pickup, I took the MTR back through the Cross-Harbour Tunnel area. When I entered the station it was not dark yet, but by the time I came out at Tsim Sha Tsui, Hong Kong had fully switched into night mode.",
    100: "Right in front of me was the Avenue of Stars. The wind from Victoria Harbour carried a little salty smell. I had barely walked two steps before I realized how crowded it was. Everyone had their phones up taking photos.",
    103: "The Avenue of Stars is where Hong Kong shows the world its golden age of cinema. The waterfront sculptures, celebrity handprints, and giant Hong Kong Film Awards statue all say the same thing: this city once built one of Asia's most brilliant film industries.",
    106: "The color of the sky slowly moved from gold to orange-red, then into purple, and finally deep blue. Across the water, Central and Admiralty had already lit up.",
    113: "Lit-up boats drifted slowly through Victoria Harbour: sailboats, small yachts, and one red-lit junk that looked like it had sailed straight out of a Hong Kong movie.",
    120: "I stood by the railing, surrounded by tourists taking photos. On the way back to the capsule hotel, I crossed Nathan Road.",
    123: "That road feels like it never ends, stretching straight ahead forever. It was full of car lights, shadows of pedestrians, and neon that kept flashing until your eyes got tired.",
    124: "Back at Windsor Mansion, the style switched again. The building was still old and narrow. Once I pushed open the capsule hotel's door, though, it became quiet again.",
    127: "I ordered curry rice at a small shop in Tsim Sha Tsui and added a mango juice, a bit of pre-race fuel. After eating, I crawled into my tiny capsule and pulled the curtain shut. Outside, Hong Kong was still blazing with lights. Inside, I had to start mentally preparing for a 5 a.m. start.",
    131: "# Kerry Hong Kong Streetathon, a fight with tunnels and elevated roads",
    132: "The full marathon at the Kerry Hong Kong Streetathon started at 5 a.m., which is early even by marathon standards. I got out of the capsule at three and ate a little bread just to put something in my stomach. Most people in the capsule hotel were foreigners, and the Austrian woman I had met the day before was also up early. Seeing me fully geared up, she offered to take a pre-race photo for me, a small bit of encouragement before heading out.",
    135: "Once I left Windsor Mansion, the street was much quieter, though there were still taxis looking for passengers.",
    138: "Hong Kong's MTR opened unusually early that day, apparently for the marathon. Once I got on, I realized the train had basically become a race train. The whole car was full of runners. Some were sleeping, some were staring quietly into space, and colorful carbon-plated shoes were flashing everywhere.",
    143: "At Tin Hau Station, I followed the crowd toward the start. Because I have run so many races in the United States, I rarely check a bag anymore. This time, by accident, that helped me avoid one of the big pain points of the race.",
    144: "Near the start there was a small area where volunteers were painting designs on runners, which was pretty fun. Several Hong Kong volunteers were busy and cheerful there.",
    147: "The start was on the elevated road near North Point in East Coast Park Precinct, so we had to climb a bit before reaching the start line.",
    150: "The approach to the start required a detour. Technically you could cut through the middle barrier, but Hong Kong people felt pretty disciplined. Most runners just followed the signs and went around properly. It reminded me of how orderly people were with elevators and trains in Singapore.",
    153: "Not long after the start, the course sent us into the Central-Wan Chai Bypass.",
    158: "It is an important express route on Hong Kong Island. Cars usually fly through it, and people normally never get to go inside.",
    159: "Inside the tunnel, it was stuffy. The air did not move much, and the temperature felt higher than outside. It was like running through a long pipe that never seemed to end.",
    164: "Once we came out, wind rushed in and everyone immediately felt lighter. Looking left, I could see the Hong Kong Observation Wheel. It is one of the most visible landmarks on the Central waterfront, lit in red and blue, only a few dozen meters from the water.",
    167: "From there, the route ran along Victoria Harbour and the Central Harbourfront. The night view opened up beautifully: Kowloon's towers across the water, small boats moving on the harbor, and air that felt much better than inside the tunnel. Going from the stuffy underground city to an open waterfront wind tunnel was a clear switch, and one of the most memorable parts of the Streetathon course.",
    170: "After turning around near the Ferris wheel, the route sent us back into the Wan Chai bypass tunnel. It was basically the same tunnel again. The air was still stuffy.",
    173: "After coming out, we ran east along the elevated road by the Wan Chai North waterfront. The sky was slowly getting brighter. I used the bathroom around this stretch, then kept going and watched the light across Victoria Harbour begin to soften.",
    178: "Next, the course took us into the Eastern Harbour Crossing. This tunnel is pretty long, a little over two kilometers, and it was tough. The grade changes a bit, the air is not exactly fresh, and once you get out, you are in Kowloon.",
    183: "By the time I came out of the Eastern Harbour Crossing, the sky had brightened a lot. The road opened up, with towers from Kowloon Bay and Kwun Tong ahead. The road was wide, and the aid station was waiting. The 14.8 km marathon marker was right there. Without paying much attention, I had already reached around 15K.",
    190: "By this point it was fully light. The bridge ahead was the Tseung Kwan O Cross Bay Bridge, one of Hong Kong's newest cable-stayed bridges. Usually only vehicles can use it, but that day it belonged to us runners for the first time. Running into the sea breeze on the bridge, with a golden sky on the left and the morning bay on the right, felt pretty special.",
    197: "After crossing the bridge, we turned around near the Tseung Kwan O industrial area. Right there, I spotted another runner wearing an Arsenal jersey.",
    202: "After the turnaround, we ran back toward the city along the water. The pretty view did not last long before another dark section took over: the Tseung Kwan O Tunnel. It was not short, and the air was stuffy again. I counted the overhead lights as I ran, using that tiny ritual to keep my rhythm.",
    205: "Inside the tunnel, we met the half-marathon runners. Some were wearing cosplay outfits, and the red and green colors looked especially bright against the gray tunnel.",
    208: "The moment we burst out of the tunnel, sunlight hit us again. We were already close to 25K.",
    209: "Around East Coast Park, we finally reached the Streetathon's famous mega aid station. It was almost a small food market: bread, fruit, energy soup, soy milk, so many options that if you stopped too long you might start wondering whether you were still in a race.",
    214: "No one seemed in a rush there. People lined up for food, chatted, and took photos. This was probably the part of the whole race that felt most like a real street marathon.",
    215: "After leaving the aid station, the route followed the Kwun Tong waterfront, then passed a riverside stretch before slowly climbing back onto an elevated road.",
    218: "In the distance, I could see a very futuristic blue oval building. That is Kai Tak Sports Park, still under construction at the time. It will become Hong Kong's largest integrated sports venue and a new base for international events.",
    223: "There was almost no shade on this elevated section. Once the sun came out, the heat pushed right up. The elevated road was also long, with that feeling that no matter how much you ran, it would not end. Luckily, around 33K there was another aid station holding everyone together. A lot of runners stopped there to drink and reset.",
    230: "After that, we finally came down from the elevated road, and the route suddenly became more interesting, with a more genuine Hong Kong city feel. Especially when we returned to Kwun Tong Promenade, where I had picked up my packet the day before, the scene was lively. There were booths, music, and a girl group handing water to runners and cheering.",
    235: "Farther ahead, the route finally moved into the neighborhood streets. Buildings got denser and there were more pedestrians. The big sign reading Dai Keung Godown really stood out. It had that very local Hong Kong look.",
    242: "This was a turnaround. After turning back, the route took us onto elevated roads again, getting closer and closer to Kai Tak Sports Park.",
    247: "Then came the highlight from the race promotion: the Yau Ma Tei section of the Central Kowloon Route tunnel. This tunnel is one of Hong Kong's major recent infrastructure projects. It had not officially opened to traffic yet, so getting to run inside before cars could use it was the most special experience of the race.",
    252: "The tunnel was long. The lighting and ventilation were decent, but the feeling of running into the inside of a future city was unique. The good part did not last long, though. The final test arrived right before the finish. The tunnel itself rolled gently, but as soon as we came out, we hit a long climb. You had to survive that unreasonable hill before you could see the finish arch.",
    259: "When I crossed the finish line, my watch stopped just over five hours. All the fatigue turned into one simple thought: finally done. For a course with this much difficulty, finishing was the win.",
    264: "At the finish, the medal was handed to me by local students in neat blue uniforms. They were all very serious and very cute.",
    267: "Walking toward the exit, I saw a lot of people lining up for massage. Even more dramatic was the bag-check area. I heard the system had problems, and everyone was searching for their bags like a giant live-action lost-and-found experience. The whole scene was chaotic.",
    272: "Luckily, the route back to the MTR was smooth, with clear signs the whole way. Back at the capsule hotel, I ran into the Spanish guy from the day before, and he congratulated me on finishing.",
    273: "After a quick shower, I dozed off in the capsule for a while. When I opened my eyes again, it was time to go to the airport. The marathon was still sitting in my legs, Hong Kong's wind was already receding behind me, and my two-and-a-half-month China trip was coming to an end.",
    276: "Postscript",
    277: "# From the Pearl of the Orient to life on the other side",
    278: "Hong Kong, China",
    279: "That night on the Airport Express, I felt a little dazed. Outside the window, Hong Kong slowly moved away behind me. The high-rises were still packed tight, and the subway, footbridges, tunnels, and elevated roads stacked over one another like a machine that never shuts down.",
    280: "I was carrying the medal I had just earned, and I started replaying the past two and a half months in China. The clearest feeling from that trip was this: China is developing incredibly fast.",
    281: "In mainland cities, new subway lines, high-speed rail, shopping malls, and apartment blocks keep appearing one after another. Scan a phone and you can handle food, housing, transport, and daily life. The efficiency is maxed out.",
    282: "Hong Kong is still prosperous, and the Victoria Harbour night view is still beautiful. But the childhood movie filter has definitely faded a little. I noticed more old buildings, crowded trains, and narrow streets.",
    283: "Thinking about flying back to the United States gave me a subtle sense of switching worlds. Infrastructure there is honestly not that advanced: older subways, older highways, slower paperwork. But there is also more blank space, more room to breathe.",
    284: "When the plane took off, my China trip officially pressed pause. The roads I had run, the subways I had taken, the wind over Victoria Harbour, the meals around the table in Shunde, and the way my family waved goodbye at the border all got packed away in my luggage for now.",
    289: "After landing in Chicago for my connection, the trip gave me one small surprise: I ran into Cindy and Jim at the airport. After crossing half the world back from Asia, seeing familiar family in the terminal felt like the journey and daily life had quietly connected in a circle.",
    290: "Siqi came to the airport to pick us up and take us home. Next, I would return to another rhythm of life. But I know these two and a half months will keep coming back in many small moments later, replaying bit by bit.",
    291: "- The end -",
    292: "Words | Arsenan",
    293: "Photos | Arsenan",
    294: "Design | Arsenan",
}


CAPTION_OVERRIDES = {
    "Shenzhen Bay Port @WoMa": "Shenzhen Bay Port @Mom",
    "Window of the World @Father in Law": "Window of the World @Father-in-law",
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
        "在那是排队按摩": "在那里排队按摩",
        "Siqi来机场接我们一起回家": "Siqi 来机场接我们一起回家",
        "所以能在还没开放给车辆之前先进去跑一回": "所以能在还没开放给车辆之前先进去跑一回",
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


def is_place_line(value: str) -> bool:
    stripped = value.strip()
    return stripped in {"💎香港，中国", "Hong Kong, China"}


def render_article(events, lang: str, rel_img_prefix: str) -> str:
    parts = []
    pending_img = None

    def flush(caption=""):
        nonlocal pending_img
        if not pending_img:
            return
        alt_base = "Hong Kong Streetathon photo" if lang == "en" else "香港嘉里街道马拉松照片"
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
        if is_place_line(value):
            continue
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
            parts.append('<p class="place">Hong Kong, China</p>' if lang == "en" else '<p class="place">💎 香港，中国</p>')
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
        title = "RunCN #第3站｜香港：嘉里街道马拉松｜穿梭在昔日“东方之珠”的隧道与高桥"
        short = "RunCN #第3站｜香港嘉里街道马拉松"
        desc = "这是我跑中国的第三站，香港嘉里街道马拉松。凌晨五点从东岸公园出发，穿过中环湾仔绕道、东隧、将军澳跨湾大桥和中九龙干线隧道，在高架、海风和城市街区里完成这趟收尾跑。"
        canonical = f"{SITE}/run50/stories/chinese/hong-kong-marathon.html"
        nav = '<a href="./index.html">← 中文故事</a><a href="../english/hong-kong-marathon.html">English</a><a href="../../index.html">Run50</a>'
        meta = '<span>阿森男</span><span>比赛日期：2025年11月23日</span><span>发布：2026年1月30日</span><a href="https://mp.weixin.qq.com/s/z_hKWEO0zVdIA8FoVvlmUg" target="_blank" rel="noopener noreferrer">原文链接</a>'
        kicker = "RunCN #第3站 · 香港"
        footer = "静态整理版：正文从“前言”开始，已移除公众号导出页的顶部杂项，原始保存文件未修改。"
        engage = engagement("zh-CN", "run50-hong-kong-marathon-zh", "supabase-comments-hong-kong-zh")
        og_locale = "zh_CN"
        alt_locale = "en_US"
    else:
        page_lang = "en"
        title = "RunCN Stop 3 | Kerry Hong Kong Streetathon"
        short = "Hong Kong Streetathon: tunnels, bridges, and a 5 a.m. start"
        desc = "A conversational English version of Arsenan's third RunCN story: Kerry Hong Kong Streetathon, Victoria Harbour, tunnels, elevated roads, Tseung Kwan O Bridge, and the last stop of a long China trip."
        canonical = f"{SITE}/run50/stories/english/hong-kong-marathon.html"
        nav = '<a href="./index.html">← English Stories</a><a href="../chinese/hong-kong-marathon.html">中文</a><a href="../../index.html">Run50</a>'
        meta = '<span>Arsenan</span><span>Race date: November 23, 2025</span><span>Published: January 30, 2026</span><a href="../chinese/hong-kong-marathon.html">Original Chinese</a>'
        kicker = "RunCN Stop 3 · Hong Kong"
        footer = "English version of the Hong Kong Streetathon story. Original Chinese page is linked above."
        engage = engagement("en", "run50-hong-kong-marathon-en", "supabase-comments-hong-kong-en")
        og_locale = "en_US"
        alt_locale = "zh_CN"

    og_img = f"{SITE}/assets/og-run50-hong-kong-icons.png"
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
  <meta property="article:published_time" content="2025-11-23T05:00:00+08:00">
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
    desc = "Race date: November 23, 2025. Kerry Hong Kong Streetathon started before dawn and sent runners through tunnels, elevated roads, Victoria Harbour views, Tseung Kwan O Bridge, and a late uphill finish."
    og_img = f"{SITE}/assets/og-run50-hong-kong-icons.png"
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Hong Kong Streetathon | Run50 Facebook</title>
  <meta name="description" content="{escape(desc)}">
  <link rel="canonical" href="{SITE}/run50/facebook/hong-kong-marathon.html">
  <meta property="og:title" content="Hong Kong turned a marathon into a tunnel-and-bridge city tour">
  <meta property="og:description" content="{escape(desc)}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="{SITE}/run50/facebook/hong-kong-marathon.html">
  <meta property="og:site_name" content="ArsenanZZ">
  <meta property="og:locale" content="en_US">
  <meta property="og:image" content="{og_img}">
  <meta property="og:image:secure_url" content="{og_img}">
  <meta property="og:image:type" content="image/png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="article:author" content="Arsenan">
  <meta property="article:published_time" content="2025-11-23T05:00:00+08:00">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Hong Kong turned a marathon into a tunnel-and-bridge city tour">
  <meta name="twitter:description" content="{escape(desc)}">
  <meta name="twitter:image" content="{og_img}">
  <link rel="stylesheet" href="../../assets/zz-engagement.css">
  <style>{css}</style>
</head>
<body>
  <div class="breaking"><div class="breaking-inner"><a href="./index.html">Run50 Facebook</a><span>Hong Kong / China / Marathon</span></div></div>
  <header class="site-head"><div class="site-head-inner"><div class="wordmark">Run50</div><nav class="section-nav" aria-label="Story links"><a href="../stories/english/hong-kong-marathon.html">Full English</a><a href="../stories/chinese/hong-kong-marathon.html">中文原文</a><a href="../index.html">Run50</a></nav></div></header>
  <article class="article">
    <section class="hero">
      <span class="label">World / China / Marathon</span>
      <h1>Hong Kong turned a marathon into a tunnel-and-bridge city tour</h1>
      <p class="dek">Before dawn on November 23, 2025, the Kerry Hong Kong Streetathon sent runners into expressway tunnels, onto elevated roads, across a sea bridge, and through a city still carrying the old Pearl of the Orient filter.</p>
      <div class="byline"><span>By Arsenan</span><span>Hong Kong, China</span><span>November 23, 2025</span></div>
      <figure class="lead-media"><img src="../../assets/og-run50-hong-kong-icons.png" alt="Icon-style Hong Kong Streetathon cover"><figcaption>Hong Kong skyline, tunnel, bridge, Ferris wheel, harbor and race bib.</figcaption></figure>
    </section>
    <section class="story-grid">
      <aside class="rail">
        <section class="brief-box"><h2>At a glance</h2><dl><div><dt>Race</dt><dd>Kerry Hong Kong Streetathon, RunCN Stop 3</dd></div><div><dt>Course</dt><dd>East Coast Park, Central-Wan Chai Bypass, Eastern Harbour Crossing, Tseung Kwan O Bridge and Central Kowloon Route tunnel.</dd></div><div><dt>What stayed with me</dt><dd>A 5 a.m. start, tunnel heat, harbor wind, a massive aid station and a chaotic bag area I luckily avoided.</dd></div></dl></section>
        <section class="share-note"><strong>Notes</strong>The comments box is below the story. New comments appear right away.</section>
      </aside>
      <div class="copy full-story">
        {article}
      </div>
    </section>
  </article>
  {engagement("en", "run50-hong-kong-marathon-facebook-en", "supabase-comments-hong-kong-facebook-en")}
  <script src="../../assets/zz-engagement-config.js?v=20260604"></script>
  <script src="../../assets/zz-engagement.js?v=20260604"></script>
</body>
</html>
'''


def write_cover_assets():
    assets = REPO / "assets"
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 750" role="img" aria-labelledby="title desc">
<title id="title">Hong Kong Streetathon icon cover</title>
<desc id="desc">Icon style cover with Hong Kong skyline, harbor, bridge, tunnel, Ferris wheel, race bib and medal.</desc>
<rect width="1200" height="750" fill="#f7f7f2"/>
<rect x="0" y="520" width="1200" height="230" fill="#1f6f8b"/>
<path d="M0 560 C150 515 300 590 450 545 C620 495 760 585 930 532 C1040 500 1120 522 1200 485 L1200 750 L0 750 Z" fill="#3fb5c4" opacity=".88"/>
<circle cx="990" cy="140" r="76" fill="#f7b733"/>
<rect x="90" y="300" width="80" height="225" fill="#22324d"/>
<rect x="185" y="235" width="95" height="290" fill="#31496d"/>
<rect x="300" y="270" width="72" height="255" fill="#22324d"/>
<rect x="392" y="205" width="115" height="320" fill="#405a7e"/>
<rect x="535" y="330" width="80" height="195" fill="#22324d"/>
<rect x="640" y="255" width="95" height="270" fill="#31496d"/>
<path d="M765 520 C835 378 970 378 1040 520" fill="none" stroke="#c33b2b" stroke-width="18"/>
<line x1="765" y1="520" x2="1040" y2="520" stroke="#c33b2b" stroke-width="18" stroke-linecap="round"/>
<path d="M120 545 C250 438 430 438 560 545" fill="none" stroke="#f7f7f2" stroke-width="24"/>
<path d="M145 545 C265 472 415 472 535 545" fill="none" stroke="#22324d" stroke-width="10"/>
<rect x="760" y="323" width="260" height="158" rx="18" fill="#ffffff" stroke="#20242b" stroke-width="8"/>
<text x="790" y="376" font-family="Arial, Helvetica, sans-serif" font-size="35" font-weight="900" fill="#20242b">RunCN #3</text>
<text x="790" y="427" font-family="Arial, Helvetica, sans-serif" font-size="51" font-weight="900" fill="#cc0000">HONG KONG</text>
<circle cx="624" cy="230" r="72" fill="none" stroke="#cc0000" stroke-width="14"/>
<line x1="624" y1="158" x2="624" y2="302" stroke="#cc0000" stroke-width="9"/>
<line x1="552" y1="230" x2="696" y2="230" stroke="#cc0000" stroke-width="9"/>
<text x="70" y="100" font-family="Arial, Helvetica, sans-serif" font-size="58" font-weight="900" fill="#20242b">Hong Kong Streetathon</text>
<text x="74" y="154" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="700" fill="#667085">Tunnels · Harbour · High bridges · 5 a.m. start</text>
</svg>'''
    (assets / "thumb-run50-hong-kong-icons.svg").write_text(svg, encoding="utf-8", newline="\n")

    width, height = 1200, 630
    image = Image.new("RGB", (width, height), "#f7f7f2")
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

    draw.rectangle((0, 450, 1200, 630), fill="#1f6f8b")
    draw.polygon([(0, 496), (150, 454), (300, 510), (450, 476), (610, 440), (760, 510), (930, 462), (1090, 474), (1200, 430), (1200, 630), (0, 630)], fill="#3fb5c4")
    draw.ellipse((920, 52, 1070, 202), fill="#f7b733")
    for x, y, w, h, color in [
        (80, 260, 82, 225, "#22324d"),
        (182, 192, 98, 293, "#31496d"),
        (304, 232, 72, 253, "#22324d"),
        (398, 168, 112, 317, "#405a7e"),
        (538, 296, 82, 189, "#22324d"),
        (646, 222, 96, 263, "#31496d"),
    ]:
        draw.rectangle((x, y, x + w, y + h), fill=color)
        for wx in range(x + 14, x + w - 12, 24):
            for wy in range(y + 24, y + h - 18, 34):
                draw.rectangle((wx, wy, wx + 8, wy + 14), fill="#f7d06a")
    draw.arc((540, 140, 700, 300), 0, 360, fill="#cc0000", width=12)
    draw.line((620, 140, 620, 300), fill="#cc0000", width=8)
    draw.line((540, 220, 700, 220), fill="#cc0000", width=8)
    draw.arc((120, 396, 560, 590), 195, 345, fill="#f7f7f2", width=24)
    draw.arc((140, 424, 540, 575), 200, 340, fill="#22324d", width=10)
    draw.arc((750, 330, 1050, 586), 190, 350, fill="#c33b2b", width=18)
    draw.line((750, 480, 1050, 480), fill="#c33b2b", width=18)
    draw.rounded_rectangle((735, 286, 1030, 435), radius=18, fill="#ffffff", outline="#20242b", width=7)
    draw.text((766, 325), "RunCN #3", font=font(37, True), fill="#20242b")
    draw.text((766, 376), "HONG KONG", font=font(50, True), fill="#cc0000")
    draw.text((64, 72), "Hong Kong Streetathon", font=font(62, True), fill="#20242b")
    draw.text((68, 136), "Tunnels - Harbour - High bridges - 5 a.m. start", font=font(28), fill="#667085")
    image.save(assets / "og-run50-hong-kong-icons.png", "PNG")


def main():
    story = extract_story()
    polish_chinese(story)
    image_count = copy_story_images(story)
    indexed = list(enumerate(story))

    normal_css = extract_style(REPO / "run50" / "stories" / "english" / "xiangyang-marathon.html")
    normal_css = normal_css.replace("#0e7490", "#1f6f8b").replace("#a33a2b", "#b6282f").replace("#b7892f", "#b8860b")
    fb_css = extract_style(REPO / "run50" / "facebook" / "xiangyang-marathon.html")

    zh_article = render_article(indexed, "zh", "RunCN-Hong-Kong-Marathon-clean_files/")
    en_article = render_article(indexed, "en", "../chinese/RunCN-Hong-Kong-Marathon-clean_files/")

    race_start, post_start = 131, 276
    race_events = [(i, e) for i, e in indexed if race_start <= i < post_start]
    backstory_events = [(i, e) for i, e in indexed if i < race_start]
    post_events = [(i, e) for i, e in indexed if i >= post_start]
    fb_article = "\n        ".join([
        '<section class="context-note"><p>Kerry Hong Kong Streetathon is a smaller, stranger kind of city marathon. It starts at 5 a.m., sends runners through expressway tunnels usually reserved for cars, opens briefly onto Victoria Harbour, crosses a sea bridge, then finishes with one more tunnel and a late uphill punch.</p><p>For me, it was also the final race-sized stop of a two-and-a-half-month China trip before flying back to the United States from Hong Kong that night.</p></section>',
        render_article(race_events, "en", "../stories/chinese/RunCN-Hong-Kong-Marathon-clean_files/"),
        '<section class="section-bridge"><h2>Before the 5 a.m. start</h2><p>The race day was the headline, but Hong Kong had already been working on me the day before: crossing from Shenzhen, dragging huge suitcases through Tsim Sha Tsui, picking up the race packet in Kwun Tong, then walking through Causeway Bay, Victoria Park and Victoria Harbour at night.</p></section>',
        render_article(backstory_events, "en", "../stories/chinese/RunCN-Hong-Kong-Marathon-clean_files/"),
        render_article(post_events, "en", "../stories/chinese/RunCN-Hong-Kong-Marathon-clean_files/"),
    ])

    (REPO / "run50" / "stories" / "chinese" / "hong-kong-marathon.html").write_text(normal_page("zh", zh_article, normal_css), encoding="utf-8", newline="\n")
    (REPO / "run50" / "stories" / "english" / "hong-kong-marathon.html").write_text(normal_page("en", en_article, normal_css), encoding="utf-8", newline="\n")
    (REPO / "run50" / "facebook" / "hong-kong-marathon.html").write_text(facebook_page(fb_article, fb_css), encoding="utf-8", newline="\n")
    write_cover_assets()
    print(f"story_events={len(story)} images={image_count}")


if __name__ == "__main__":
    main()
