from pathlib import Path
from html import escape
from lxml import html
from PIL import Image, ImageDraw, ImageFont, ImageOps
import re


REPO = Path(__file__).resolve().parents[1]
SOURCE_BASE = Path(r"Z:\ZhennanZ Folder\000-Marathon-Story-2024-2025\20230000-Marathons\2023-State-12-IL")
SOURCE_HTML = next(p for p in SOURCE_BASE.iterdir() if p.suffix.lower() == ".html")
SOURCE_FILES = next(p for p in SOURCE_BASE.iterdir() if p.is_dir() and p.name.endswith("_files"))
SITE = "https://arsenanzz.github.io/ZZ"
SLUG = "chicago-marathon"
VERSION = "20260605-1"
ENGAGEMENT_VERSION = "20260605"
OUT_IMG_DIR = REPO / "run50" / "stories" / "chinese" / "Run50-Chicago-Marathon-clean_files"
OG_PATH = REPO / "assets" / "og-run50-chicago-marathon-icons.png"
THUMB_PATH = REPO / "assets" / "thumb-run50-chicago-marathon-icons.svg"

TITLE_ZH = "Run50 #第12州｜伊利诺伊：芝加哥马拉松｜45周年打卡，我们的第二个大满贯"
TITLE_EN = "Run50 #12 | Illinois: 45th Chicago Marathon"
TITLE_FB = "Chicago turned a World Marathon Major into State 12 of Run50"
DATE_ZH = "2023.10.08"
DATE_EN = "Oct 8, 2023"
RACE_NAME = "45th Chicago Marathon"


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


def should_skip_text(text: str) -> bool:
    return text in {"★", "★★", "★★★", "★★★★", "\u200d"} or not text.strip("\u200d").strip()


def extract_story():
    source = SOURCE_HTML.read_text(encoding="utf-8", errors="replace")
    doc = html.fromstring(source)
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

    start = 0
    for pos, (_, event) in enumerate(clean):
        if event["type"] == "text" and event["text"] == "前言":
            start = pos
            break

    end = len(clean)
    for pos, (_, event) in enumerate(clean):
        if event["type"] == "text" and event["text"].startswith("设计"):
            end = pos + 1
            break
    return clean[start:end]


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


def copy_story_images(indexed):
    OUT_IMG_DIR.mkdir(parents=True, exist_ok=True)
    image_total = sum(1 for _, event in indexed if event["type"] == "img")
    existing = sorted(OUT_IMG_DIR.glob("img-*.webp"))
    if len(existing) == image_total:
        count = 0
        for _, event in indexed:
            if event["type"] != "img":
                continue
            count += 1
            event["out"] = f"img-{count:03d}.webp"
        return count

    for old in OUT_IMG_DIR.glob("img-*.webp"):
        old.unlink()

    count = 0
    for _, event in indexed:
        if event["type"] != "img":
            continue
        count += 1
        out_name = f"img-{count:03d}.webp"
        with Image.open(local_source_path(event["src"])) as im:
            im = ImageOps.exif_transpose(im)
            if im.mode != "RGB":
                im = im.convert("RGB")
            im.save(OUT_IMG_DIR / out_name, "WEBP", quality=88, method=4)
        event["out"] = out_name
    return count


def clean_caption(text: str) -> str:
    caption = text.lstrip("▲").strip()
    replacements = {
        "Offical": "Official",
        "Vechile": "Vehicle",
        "20km": "20 km",
        "10000km": "10000 km",
        "Chinatown Food": "Chinatown Food",
        "Passionate Uncle": "Passionate Uncle",
    }
    for old, new in replacements.items():
        caption = caption.replace(old, new)
    return caption


def figure_html(src: str, caption: str, alt_base: str) -> str:
    alt = caption or alt_base
    figcaption = f"<figcaption>{escape(caption)}</figcaption>" if caption else ""
    return f'<figure><img src="{escape(src)}" alt="{escape(alt)}" loading="lazy" decoding="async">{figcaption}</figure>'


def render_zh_text(text: str) -> str:
    if should_skip_text(text) or is_caption(text):
        return ""
    if text in ("前言", "后记"):
        return f'<h2 class="section-label">{escape(text)}</h2>'
    if text.startswith("# "):
        return f"<h2>{escape(text[2:])}</h2>"
    if text.startswith("## "):
        return f"<h3>{escape(text[3:])}</h3>"
    if text.startswith(("🚃", "📍", "🎽")):
        return f'<p class="place">{escape(text)}</p>'
    if text.startswith("- "):
        return f'<p class="end-mark">{escape(text)}</p>'
    if text.startswith(("文字", "摄影", "设计")):
        return f'<p class="credit-line">{escape(text)}</p>'
    return f"<p>{escape(text)}</p>"


def render_en_text(idx: int, source_text: str) -> str:
    if should_skip_text(source_text) or is_caption(source_text):
        return ""
    text = EN_BY_INDEX.get(idx)
    if text is None:
        raise KeyError(f"Missing English translation for source index {idx}: {source_text}")
    if text in ("Preface", "Postscript"):
        return f'<h2 class="section-label">{escape(text)}</h2>'
    if text.startswith("# "):
        return f"<h2>{escape(text[2:])}</h2>"
    if source_text.startswith(("🚃", "📍", "🎽")):
        return f'<p class="place">{escape(text)}</p>'
    if text.startswith("- "):
        return f'<p class="end-mark">{escape(text)}</p>'
    if text.startswith(("Words |", "Photos |", "Design |")):
        return f'<p class="credit-line">{escape(text)}</p>'
    return f"<p>{escape(text)}</p>"


def render_article(indexed, lang: str, img_prefix: str, alt_base: str) -> str:
    parts = []
    pending_caption = ""
    for idx, event in indexed:
        if event["type"] == "text":
            if is_caption(event["text"]):
                pending_caption = clean_caption(event["text"])
                continue
            html_text = render_zh_text(event["text"]) if lang == "zh" else render_en_text(idx, event["text"])
            if html_text:
                parts.append(html_text)
            continue
        if event["type"] == "img":
            parts.append(figure_html(img_prefix + event["out"], pending_caption, alt_base))
            pending_caption = ""
    return "\n      ".join(parts)


def find_pos(indexed, needle: str) -> int:
    for pos, (_, event) in enumerate(indexed):
        if event["type"] == "text" and event["text"] == needle:
            return pos
    raise RuntimeError(f"Could not find section marker: {needle}")


def split_sections(indexed):
    city = find_pos(indexed, "# 芝加哥，这个城市")
    travel = find_pos(indexed, "# 出发，飞去芝加哥")
    race = find_pos(indexed, "# 开跑！45周年芝加哥马拉松")
    post = find_pos(indexed, "后记")
    return {
        "foreword": indexed[:city],
        "city": indexed[city:travel],
        "travel": indexed[travel:race],
        "race": indexed[race:post],
        "post": indexed[post:],
    }


EN_BY_INDEX = {
    4: "Preface",
    5: "Last year in Honolulu, Hawaii, 47 and I received our Chicago Marathon lottery emails almost at the same time.",
    6: "It felt oddly magical. Yes, compared with other World Marathon Majors, Chicago is supposed to be a little easier to get into, but only relatively. For both of us to land that luck at the same time was still pretty rare.",
    7: "The 45th anniversary number was also one I liked. But this would be 47's first World Marathon Major and her first marathon with a strict cutoff time, so I was a little worried. Not everyone is like me - lihai, you know. For normal humans, running a full marathon is still a real challenge.",
    8: "After the emails arrived, I took 47 to Hawaii and we finished her first full marathon: the 50th Honolulu Marathon. We walked for most of it, but after finishing she looked completely fine. Apparently she had some talent. So Chicago seemed like it might be possible without dropping out.",
    11: "Just like that, ten months passed. We kept working out, and 47 got a lot stronger. Very impressive. For the upcoming 2023 Chicago Marathon, I would not say we were sure to win, but we definitely were not short on confidence.",
    15: "# Chicago, the city",
    16: "Chicago, Illinois",
    17: "Compared with the Chicago Marathon itself, I actually did not have huge expectations for the city. We had already driven there once in 2021. It is not far, about five hours by car, and I had connected through Chicago countless times. Flying there takes less than two hours.",
    22: "After coming back from Chicago that time, I wrote a post called 'Chicago, Parallel World.' Since I also ran a half marathon then, I wrote a race story called 'Chicago, Windy City Half Marathon' too.",
    27: "Writing a post is a bit like writing a paper: you still need to do some literature review. So I may know more about Chicago than most people. With less mystery and unfamiliarity, naturally there was a little less anticipation.",
    28: "But I still want to talk about Chicago.",
    29: "Chicago is Norman Mailer's 'last great American city,' and the rhythmic, music-and-dance city in Rob Marshall's films. It is the center of the Midwest, the third-largest city in the United States, and after the Great Fire of 1871, it rose again and drew architects and artists from around the world.",
    34: "In the 18th century, the Chicago area was Potawatomi land. In 1779, Jean Baptiste Point DuSable, a Black trader from Haiti, settled in Chicago, married a Potawatomi woman, and opened the area's first trading post on the north bank of the Chicago River.",
    35: "The Chicago of the 21st century is far from the place Kipling once passed through. It is no longer the world's pork shop. Replacing the old smoke and grayness are some of the finest public gardens since the Babylonians built the Hanging Gardens.",
    40: "With a bit of magic, more than 26 miles of lakefront now sits beside architectural wonders, forming Chicago's brilliant skyline.",
    45: "For many people, the big bean in Millennium Park, the deep and serious Art Institute of Chicago, and the desire-filled Magnificent Mile are all must-see Chicago stops.",
    52: "Do you like the Bulls? Do you like Jordan? That is one of Chicago's calling cards. In front of the United Center, the greatest player in NBA history, Air Jordan, and his No. 23 jersey are permanently honored there.",
    53: "Do you like Hemingway? Whether or not you have been to Idaho in the northwest or Key West in the southeast, you eventually need to come to Oak Park in Chicago. Hemingway was born here.",
    54: "Chicago also gave birth to many world firsts: the first pair of roller skates in 1884, popcorn in the modern sense in 1893, Judson's zipper in 1896, and the first transparent-window envelope mailed from here in 1902.",
    59: "Rumble, rumble, rumble - that is another unmistakable Chicago sound. In 1892, to solve three-dimensional urban transportation, Chicago built the world's first elevated railway. It still runs through the old city today, making me think of the drifting gaze of the male lead in 'Shall We Dance' as he looks out the train window.",
    64: "After four years in the United States and visiting quite a few places, I feel Chicago resembles China in certain ways: skyscrapers everywhere, a lively Chinatown, and genuinely good Chinese food.",
    67: "Even though I have gotten used to eating salad, I still have a stomach from Heilongjiang in China's northeast. Chicago has the liveliest Chinatown in the eastern half of the U.S.",
    72: "Walking from Wentworth Avenue into Chinatown, you can see a Chinese-style building. On the front are Sun Yat-sen's words 'The world belongs to all,' and on the back are the characters for propriety, righteousness, integrity, and shame.",
    74: "# Off we go, flying to Chicago",
    75: "Chicago, Illinois",
    76: "The Chicago Marathon is held on the second Sunday of October, so 47 and I booked Saturday morning flights. What I did not expect was how crowded Louisville airport would be a little after 6 a.m.",
    77: "We stood in line watching time slip away, getting more and more anxious. Even though we eventually got into the fast security lane, we still missed the flight at the very last moment.",
    80: "Looking through the big airport glass at the plane to Chicago parked outside felt a little heartbreaking. The plane was right there, and we still could not get on it.",
    81: "The airport staff were very nice and helped move us to a noon flight. The timing was still workable and would not delay packet pickup. Best arrangement possible.",
    82: "I opened my laptop and calmly organized photos and text for the Kentucky Derby Marathon. It was a little cold, but I was surprisingly efficient and almost finished another post.",
    83: "Finally, at noon, we boarded the flight to Chicago. 47 gave me the window seat, and we were about to fly over Indiana and into Illinois.",
    84: "Outside the window were white clouds, and below them one yellow-green farm field after another.",
    89: "A little over an hour later, we were above Chicago. Lake Michigan appeared below the clouds, broad as the sea, then the city shoreline cut it cleanly apart: on the left, the shimmering Great Lake; on the right, downtown Chicago packed with towers.",
    96: "After landing in Chicago, banners were already up at the metro entrance welcoming runners from around the world. It really felt like we had arrived somewhere that wanted us there.",
    99: "After dropping our luggage at the hotel, we went to the Chicago Marathon expo near the hotel to pick up our gear. The expo was huge, and you could see lots of Chicago touches there: the Chinatown gate, the CTA train cars, and more.",
    108: "Just like at the New York Marathon, if you tell the cashier after shopping that this is your first full marathon, they announce it loudly and everyone cheers.",
    117: "After the expo, we planned to go to Chinatown for good food. Our hotel was in a great spot, right between the expo and Chinatown. But Chicago really is the Windy City. It was so windy outside that when we passed the hotel halfway, I went back up to grab another layer.",
    120: "On the way to Chinatown, I saw an AR running crew sticker on a pole. It instantly pulled me back to the days training with AR in Shanghai. But after looking closely, I realized this AR sticker was from Berlin.",
    125: "In Chinatown, we found a Lanzhou noodle place and ordered a few big buns, two bowls of noodles, and smashed cucumber. The food came quickly and tasted good. Other than having almost nothing to do with Lanzhou noodles, everything was great.",
    134: "Across from our table sat a large group of runners from China. I listened to familiar Chinese voices and their plans to break three hours the next day.",
    141: "After dinner, we walked around Chinatown for a while. It was lively. The neighborhood is not big, but it felt very familiar. For a moment, I almost forgot I was in a foreign country.",
    142: "Fed and happy, we walked back to the hotel, passing lots of runners carrying race bags. The Chicago evening wind was a little chilly. I hoped tomorrow would bring good weather so everyone could enjoy this big party.",
    144: "# Race day: the 45th Chicago Marathon",
    145: "Chicago, Illinois",
    146: "Before September 26, 2023, Berlin and Chicago each held a world record. But after Tigst Assefa ran 2:11:53 in Berlin, Berlin became the unquestioned fastest course in the world. Still, Chicago was not without the ability to strike back.",
    147: "The Chicago Marathon on October 8 might have been preparing a world-shaking performance. The Windy City has never lacked speed or drama, and we were lucky enough to be part of it.",
    150: "The first Chicago Marathon dates back to 1905, but the modern Chicago Marathon truly began in 1977, originally called the Mayor Daley Marathon. It now has 45 years of history, is one of the World Marathon Majors, and is a World Athletics Gold Label race.",
    155: "Race morning was still dark when we got ready to go. At the metro station, we met two runners who had flown in from China, and we added each other on WeChat.",
    162: "The start was in Grant Park, and there really were a lot of people. After 47 and I wished each other luck, I squeezed into the crowd. Before officially entering Grant Park, security checked everyone, though compared with New York, Chicago felt a bit more relaxed.",
    175: "At that moment, sunrise had just risen over Lake Michigan, painting a thin blue edge in the distant sky. The clouds over the lake grew bluer too, echoing the pale blue water.",
    180: "Since there was still some time before the race began, I wandered around the bag check area and the big fountain near the start. I also went to the restroom. Chicago had plenty of portable toilets, and the lines were not too bad.",
    187: "My start was in Corral H. A lot of runners had already gathered there, and the fence beside us was piled with clothes. Clearly everyone was warmed up and ready to go.",
    192: "Near the start, I was pleasantly surprised to find photographers taking photos for runners. Naturally, I shamelessly got myself into quite a few shots, adding a few jacket-on images to the archive.",
    201: "There was also a big screen showing the lead pack live, and Kelvin Kiptum was in it. At that moment, we did not yet know we were witnessing history. A world record was being born in real time.",
    210: "Finally, our Corral H group started moving. We could still see runners from later lettered corrals waiting on the side road behind us. I looked carefully to see if I could spot 47.",
    217: "I followed the crowd forward little by little. The START arch got closer and closer. With cheers from the starting pack and the crowds on both sides, my second World Marathon Major officially began.",
    230: "The first mile ran north along Columbus Drive. Then we turned left onto Grand Avenue, passed Cloud Gate, and continued along the Riverwalk and the Wrigley Building.",
    235: "The William P. Fahey Bridge was covered with a red carpet. It was not slippery to run on. As expected from a major marathon, the details were handled well.",
    242: "The race then continued west on Grand, turned south onto State Street, and crossed back to the other side of the river. Before crossing, we passed Chicago's corn-cob towers, Marina Towers, whose shape is incredibly distinctive. The Marina City complex is a residential tower complex on the north bank of the Chicago River, made up of two identical honeycomb-like apartment towers.",
    251: "Before Mile 2, I saw two runners in Argentina jerseys and even Santa Claus. Pretty fun.",
    260: "Next we moved west together to Jackson Boulevard, then north to LaSalle Street, reaching the end of LaSalle around Mile 5 before turning along West LaSalle Drive to Stockton Drive. Here we passed through Lincoln Park and ran alongside the Lincoln Park Zoo.",
    265: "Around 8 kilometers, there was a green Irish-style cheering group. I stopped there for a restroom break, then ran lightly to 10K. The Chicago Marathon is excellent; maybe to take care of runners from all over the world, the bibs show both miles and kilometers.",
    272: "The spectators on both sides of the course were incredibly enthusiastic, and the stream of runners was nonstop. But that did create trouble for pedestrians and pedicabs, because crossing the road was genuinely difficult.",
    277: "Still, some pedicabs forced their way across despite the risk of being roasted by runners, adding some very unhelpful uncertainty to the course. I had to change my running rhythm because of a pedicab cutting across, and many runners complained after the race too.",
    284: "Around Mile 8, we reached Diversey Parkway, then turned north onto Sheridan Road. This section was extremely lively. I saw a blade runner flying along the course, plus proud LGBTQ performances. A very diverse community, and in many ways a small portrait of Chicago itself.",
    293: "After Mile 9, we drifted southeast toward Chicago's Broadway and reached Sedgwick Street around Mile 10.",
    298: "Here we saw a Japanese support drum team, and for a second I flashed back to the big bald-head mountain in Hawaii.",
    303: "At 20K, I stepped through the roadside barrier and asked a volunteer to take a photo of me with the 20K marker. The race was almost halfway.",
    306: "After 20K, Willis Tower was not far away. Willis Tower is one of Chicago's landmarks. It was once the tallest building in the world until Malaysia's Petronas Twin Towers surpassed it in 1998. Visitors can take a high-speed elevator to the skydeck for sweeping views of downtown Chicago and the lake.",
    311: "Next, we turned right onto West Adams Street and passed Heritage Green Park, Mary Bartelme Park, Skinner Park, and the United Center. Then we turned back around Mile 15.",
    324: "Along the way, you could see flags from many countries - Portugal, Brazil, South Africa. It felt very international.",
    333: "Running east after the turnaround, we faced Willis Tower head-on. Then a right turn south brought us to the University of Illinois Chicago. After 29K, we passed a Mexican-flavored street and saw an excellent Mexican folklorico skirt dance.",
    346: "After crossing the Chicago River, we entered Chinatown. Seeing Chinese characters everywhere felt very comforting. Passing through Chinatown, I even went by the Lanzhou noodle place we had eaten at the day before.",
    357: "At the end of Chinatown, I asked an Asian uncle who did not speak English to help take a few photos. He was very warm and kept gesturing to ask if the photos were good, and if not, he could take more. Truly kind.",
    364: "Coming out of Chinatown, we reached Mile 22. A 4:20 pacer passed me, so I followed for a while, then realized this pacer was not from my starting corral. I figured 4:30 was probably not happening either, so I stopped chasing and decided to run-walk comfortably to the finish.",
    373: "For the final stretch, we ran toward the Chicago skyline. The finish area was roaring with people and music, with photographers everywhere. I turned running mode back on, mostly to collect a few more good official photos.",
    390: "Final 200 meters, final 100 meters... Finish. Across the line. My second World Marathon Major was done, but the voices of volunteers and roadside spectators were still rising and falling in my head. I was not ready for it to be over.",
    399: "After collecting my medal and finisher beer, I stretched while calling 47 to check how she was doing. To my surprise, she sounded great, far beyond my expectations, and she was not far from finishing. I glanced at my watch and thought she might get a huge PR this time. Compared with Honolulu, her time should be much better, and finishing was basically locked in. Pretty impressive.",
    424: "After a short rest, I planned to loop from the post-race party area back to the course to find 47. On the way, I passed the many-legged Agora sculpture group, which looked pretty distinctive.",
    431: "I passed through the cheering crowd and walked back along the sidewalk beside the course, watching the course-closing vehicle slowly roll by. But I was not worried, because there were still so many participants on the course. Finally, after walking about two miles, I saw 47 coming toward me with all her bags, looking pretty good.",
    438: "Then I joined the race too. 47 and I became a two-person squad, walking toward the finish in infantry mode. When we saw photographers, we would pretend to run a little.",
    439: "Finally, after one turn, the Chicago skyline appeared in front of us. The finish was right there.",
    440: "In the final few hundred meters, we saw a couple ahead of us fly across the finish in airplane mode for the camera. They were moving pretty fast.",
    455: "47 and I were clearly more low-key, crossing the line in a much less exaggerated pose. Seven full hours - and 47 was now a World Marathon Major finisher too. Siqi was a serious runner now. Please congratulate her immediately.",
    456: "After crossing for the second time, I did not take a second medal or another finisher beer. As a high-quality runner, I crossed twice and still quietly got a ton of official photos. More quantity, same price. I am grateful to the Chicago Marathon for that.",
    459: "By then, the finish area was much quieter than when I had finished, but some photographers were still holding their ground in the strong wind to shoot finishers. 47 and I took plenty of photos together.",
    466: "On the way to the metro station, we also passed the Field Museum. It is one of the largest and most prestigious museums in the world, with huge collections related to natural history and anthropology.",
    469: "47 even suggested going inside to walk around and loosen up. For someone who had just finished a marathon, her energy was honestly impressive. But later we decided time was tight and it was a bit cold, so we took the metro straight back to the hotel.",
    470: "Then we ordered a big takeout meal and ended the Chicago city-walk day beautifully with good food. After the race, I checked Moments and saw that 'Teacher Da' had also run a big PR in Chicago, which gave me a lot of motivation to occasionally switch back from Buddhist runner mode to serious runner mode.",
    475: "On the way home, at the Chicago airport, we saw travelers wearing Chicago finisher medals everywhere. I think this trip will leave many people with lifelong memories, and I hope this piece can keep some of those fleeting moments.",
    480: "Postscript",
    481: "After finishing Chicago, I officially stepped into the gate of becoming a 10000-kilometer runner. Since I started running marathons in 2017, seven years have passed in a blur. Across these 32 full marathons, every kilometer is an extremely precious memory to me.",
    484: "Fifteen marathons in mainland China, fifteen in the United States, plus one each in Singapore and Thailand. I think of them as wonderful social-practice classes. Touching each city with my own feet always feels the most grounded.",
    485: "I used to be used to traveling alone, carrying a big backpack, going to Ordos, Guang'an, Bangkok, Singapore...",
    486: "Now, with Siqi joining in, the journey has become even more interesting. Whether it is '50th Anniversary Check-in: Our Honolulu Marathon' or '45th Anniversary Check-in: Our Chicago Marathon,' I always believe beautiful stories are about to happen - or rather, they are already happening.",
    487: "- End -",
    488: "Words | Arsenan",
    489: "Photos | Arsenan",
    490: "Design | Arsenan",
}


def page_css() -> str:
    return """
    :root {
      --paper: #edf3f7;
      --surface: #ffffff;
      --ink: #20242b;
      --muted: #667085;
      --line: #d0dfe8;
      --river: #0b67c2;
      --brick: #8f3b2f;
      --gold: #b7892f;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      background: linear-gradient(180deg, #eef5f6 0, var(--paper) 320px);
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
    .story-nav a { color: inherit; text-decoration: none; border-bottom: 1px solid transparent; }
    .story-nav a:hover { border-color: currentColor; }
    .page-header { max-width: 860px; margin: 0 auto; padding: 42px 22px 24px; }
    .kicker { margin: 0 0 14px; color: var(--river); font-size: 14px; font-weight: 850; }
    h1 {
      margin: 0;
      max-width: 820px;
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
    .meta span {
      display: inline-flex;
      align-items: center;
      min-height: 30px;
      padding: 3px 10px;
      border: 1px solid var(--line);
      border-radius: 999px;
      background: rgba(255, 255, 255, .72);
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
    .article-body h3 { margin: 36px 0 16px; color: #111827; font-size: 22px; line-height: 1.3; font-weight: 800; }
    .article-body .section-label { color: #111827; font-size: 28px; letter-spacing: 0; text-transform: none; }
    .article-body p { margin: 0 0 17px; font-size: 17px; line-height: 1.86; }
    .place { margin: -8px 0 24px; color: var(--muted); font-size: 15px; font-weight: 700; }
    .article-body figure { margin: 28px 0 30px; }
    .article-body img {
      display: block;
      width: 100%;
      max-width: 100%;
      height: auto;
      border-radius: 8px;
      background: #dceaf2;
      box-shadow: 0 16px 40px rgba(15, 23, 42, .12);
    }
    figcaption { margin-top: 9px; color: #7a828c; font-size: 13px; line-height: 1.55; text-align: center; }
    .end-mark, .credit-line { text-align: center; color: var(--muted); }
    .page-footer { max-width: 860px; margin: 0 auto; padding: 0 22px 44px; color: var(--muted); text-align: center; font-size: 14px; }
    @media (max-width: 640px) {
      .story-nav { flex-wrap: wrap; }
      .page-header { padding: 30px 18px 20px; }
      h1 { font-size: 26px; }
      .article-body { padding: 34px 18px 44px; }
      .article-body h2, .article-body .section-label { font-size: 24px; }
      .article-body p { font-size: 16px; }
      .article-body figure { margin-left: -2px; margin-right: -2px; }
    }
    """


def facebook_css() -> str:
    return """
    :root {
      --red: #cc0000;
      --ink: #101214;
      --muted: #5f6672;
      --line: #d8dde3;
      --soft: #f3f5f7;
      --blue: #0b67c2;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      background: #ffffff;
      color: var(--ink);
      font-family: Arial, Helvetica, sans-serif;
      letter-spacing: 0;
      overflow-x: hidden;
    }
    a { color: inherit; }
    .topbar {
      min-height: 42px;
      padding: 0 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 18px;
      background: #111111;
      color: #ffffff;
      font-size: 13px;
      font-weight: 800;
      text-transform: uppercase;
    }
    .masthead {
      width: min(1120px, calc(100% - 36px));
      margin: 0 auto;
      padding: 36px 0 28px;
      border-bottom: 1px solid var(--line);
    }
    .brand {
      display: inline-flex;
      align-items: center;
      gap: 10px;
      color: var(--red);
      font-size: 13px;
      font-weight: 900;
      letter-spacing: .12em;
      text-transform: uppercase;
    }
    .brand::before { content: ""; width: 36px; height: 9px; background: var(--red); }
    h1 {
      max-width: 950px;
      margin: 16px 0 16px;
      font-size: clamp(2.35rem, 6.4vw, 5.4rem);
      line-height: .96;
      letter-spacing: 0;
      overflow-wrap: anywhere;
    }
    .summary {
      max-width: 780px;
      margin: 0;
      color: #30343b;
      font-size: 1.08rem;
      line-height: 1.7;
      overflow-wrap: anywhere;
    }
    .meta-row {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-top: 20px;
      color: var(--muted);
      font-size: 12px;
      font-weight: 800;
      text-transform: uppercase;
    }
    .meta-row span { padding: 6px 9px; background: var(--soft); }
    .content-grid {
      width: min(1120px, calc(100% - 36px));
      margin: 0 auto;
      display: grid;
      grid-template-columns: minmax(0, 730px) minmax(230px, 1fr);
      gap: 34px;
      padding: 32px 0 64px;
    }
    .article-body {
      max-width: 730px;
      min-width: 0;
      overflow-wrap: anywhere;
    }
    .article-body .lede, .bridge-note {
      padding: 18px 20px;
      margin: 0 0 22px;
      background: #edf3f7;
      border-left: 5px solid var(--blue);
      color: #26323e;
      font-size: 18px;
      line-height: 1.65;
      font-weight: 700;
    }
    .article-body h2 {
      margin: 46px 0 18px;
      border-top: 6px solid #111111;
      padding-top: 12px;
      font-size: 34px;
      line-height: 1.06;
      letter-spacing: 0;
    }
    .article-body h2:first-child { margin-top: 0; }
    .article-body .section-label {
      border-color: var(--blue);
      color: #111111;
    }
    .article-body p {
      margin: 0 0 17px;
      color: #242830;
      font-size: 17px;
      line-height: 1.82;
    }
    .place {
      margin-top: -8px;
      color: var(--muted);
      font-size: 14px;
      font-weight: 800;
      text-transform: uppercase;
    }
    figure { margin: 28px 0 30px; }
    figure img {
      display: block;
      width: 100%;
      height: auto;
      border-radius: 2px;
      background: #e6eef4;
    }
    figcaption {
      margin-top: 8px;
      color: var(--muted);
      font-size: 12px;
      text-align: center;
      line-height: 1.45;
    }
    .end-mark, .credit-line { text-align: center; color: var(--muted); }
    .rail {
      position: sticky;
      top: 24px;
      align-self: start;
      border-top: 6px solid var(--red);
      padding-top: 14px;
      color: #30343b;
      font-size: 14px;
      line-height: 1.6;
    }
    .rail h2 {
      margin: 0 0 10px;
      font-size: 22px;
      line-height: 1.1;
    }
    .rail p { margin: 0 0 12px; }
    .rail a {
      display: inline-block;
      margin-top: 4px;
      color: var(--red);
      font-weight: 800;
      text-decoration: none;
      border-bottom: 1px solid currentColor;
    }
    @media (max-width: 860px) {
      .topbar { padding: 0 18px; }
      .content-grid { grid-template-columns: 1fr; }
      .rail { position: static; order: -1; }
      .article-body h2 { font-size: 28px; }
    }
    @media (max-width: 560px) {
      .masthead, .content-grid {
        width: 100%;
        max-width: 390px;
        margin-left: 0;
        margin-right: 0;
        padding-left: 14px;
        padding-right: 14px;
      }
      .content-grid {
        display: block;
      }
      .article-body, .rail, .summary, h1 {
        width: 100%;
        max-width: 100%;
        min-width: 0;
      }
      .meta-row span {
        max-width: 100%;
        overflow-wrap: anywhere;
      }
      .topbar {
        min-height: 0;
        padding: 10px 14px;
        flex-wrap: wrap;
        justify-content: flex-start;
        line-height: 1.25;
      }
      h1 {
        font-size: 1.75rem;
        line-height: 1.03;
        word-break: break-word;
      }
      .article-body p { font-size: 16px; }
      .article-body .lede, .bridge-note { font-size: 16px; padding: 16px; }
    }
    """


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
    """


def story_page(lang: str, article: str) -> str:
    is_zh = lang == "zh"
    title = TITLE_ZH if is_zh else TITLE_EN
    description = (
        "2023年10月8日的第45届芝加哥马拉松：第二个世界大满贯、Run50第12州、基普图姆世界纪录诞生的一天，以及Siqi的第一个大满贯完赛。"
        if is_zh
        else "State 12 of Run50 and my second World Marathon Major: missing the first flight, eating in Chinatown, starting in Grant Park, witnessing Kelvin Kiptum's world record day, and walking Siqi into her first Major finish."
    )
    nav = (
        '<a href="./index.html">← 中文故事</a><a href="../english/chicago-marathon.html">English</a><a href="../../facebook/chicago-marathon.html">Facebook</a><a href="../../index.html">Run50</a>'
        if is_zh
        else '<a href="./index.html">← English Stories</a><a href="../chinese/chicago-marathon.html">中文</a><a href="../../facebook/chicago-marathon.html">Facebook</a><a href="../../index.html">Run50</a>'
    )
    meta = (
        '<span>芝加哥 · 伊利诺伊</span><span>2023.10.08</span><span>Run50 #第12州</span><span>第二个世界大满贯</span>'
        if is_zh
        else '<span>Chicago, Illinois</span><span>Oct 8, 2023</span><span>Run50 #12</span><span>World Major #2</span>'
    )
    kicker = "Run50 Stories · 伊利诺伊" if is_zh else "Run50 Stories · Illinois"
    lang_attr = "zh-CN" if is_zh else "en"
    page_key = f"run50-{SLUG}-zh" if is_zh else f"run50-{SLUG}-en"
    comment_id = "supabase-comments-chicago-zh" if is_zh else "supabase-comments-chicago-en"
    filename = "chinese/chicago-marathon.html" if is_zh else "english/chicago-marathon.html"
    footer = "Run50 · 伊利诺伊 · 芝加哥马拉松" if is_zh else "Run50 · Illinois · Chicago Marathon"
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
  <meta property="og:image" content="{SITE}/assets/og-run50-chicago-marathon-icons.png?v={VERSION}">
  <meta property="og:url" content="{SITE}/run50/stories/{filename}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:image" content="{SITE}/assets/og-run50-chicago-marathon-icons.png?v={VERSION}">
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
    description = "A Facebook-ready full English story about the 45th Chicago Marathon: race day first, with the full travel, city, packet pickup, Chinatown, and postscript story preserved after it."
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
  <meta property="og:image" content="{SITE}/assets/og-run50-chicago-marathon-icons.png?v={VERSION}">
  <meta property="og:url" content="{SITE}/run50/facebook/chicago-marathon.html">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:image" content="{SITE}/assets/og-run50-chicago-marathon-icons.png?v={VERSION}">
  <link rel="stylesheet" href="../../assets/zz-engagement.css?v={ENGAGEMENT_VERSION}">
  <style>{facebook_css()}</style>
</head>
<body>
  <div class="topbar"><span>Run50 Facebook</span><span>Race date: Oct 8, 2023</span></div>
  <header class="masthead">
    <div class="brand">Run50 / USA / Marathon</div>
    <h1>{escape(TITLE_FB)}</h1>
    <p class="summary">On October 8, 2023, the 45th Chicago Marathon became my second World Marathon Major, State 12 in the Run50 map, and the day Kelvin Kiptum rewrote the marathon world record. It was also the day Siqi became a Major finisher.</p>
    <div class="meta-row"><span>Chicago, Illinois</span><span>World Major #2</span><span>Run50 #12</span><span>Full story</span></div>
  </header>
  <main class="content-grid">
    <article class="article-body">
      {article}
    </article>
    <aside class="rail">
      <h2>Why this one matters</h2>
      <p>Chicago is one of the World Marathon Majors, a fast course with huge crowds and a huge city personality.</p>
      <p>This version opens with race day, then rewinds to the lottery, the city, the travel mess, the expo, Chinatown, and the postscript.</p>
      <a href="../stories/english/chicago-marathon.html">Read the original order</a>
    </aside>
    {engagement_block('en', f'run50-{SLUG}-facebook-en', 'supabase-comments-chicago-facebook', '../../assets')}
  </main>
</body>
</html>
"""


def build_facebook_article(sections) -> str:
    race = render_article(sections["race"], "en", "../stories/chinese/Run50-Chicago-Marathon-clean_files/", "Chicago Marathon photo")
    foreword = render_article(sections["foreword"], "en", "../stories/chinese/Run50-Chicago-Marathon-clean_files/", "Chicago Marathon photo")
    city = render_article(sections["city"], "en", "../stories/chinese/Run50-Chicago-Marathon-clean_files/", "Chicago Marathon photo")
    travel = render_article(sections["travel"], "en", "../stories/chinese/Run50-Chicago-Marathon-clean_files/", "Chicago Marathon photo")
    post = render_article(sections["post"], "en", "../stories/chinese/Run50-Chicago-Marathon-clean_files/", "Chicago Marathon photo")
    intro = """
      <p class="lede">Chicago did not feel like just another race on the calendar. It was the 45th Chicago Marathon, my second World Marathon Major, State 12 of Run50, and a course famous for speed, architecture, neighborhoods, and noise. So before rewinding to the lottery email and the messy travel day, let me start where the story really hits hardest: race morning in Grant Park.</p>
    """
    transition = """
      <p class="bridge-note">To understand why that finish meant so much, we need to rewind to the beginning: two lottery emails, one first-Major anxiety, and a city I thought I already knew.</p>
    """
    return intro + "\n      " + race + "\n      " + transition + "\n      " + foreword + "\n      " + city + "\n      " + travel + "\n      " + post


def font(size: int, bold: bool = False):
    font_name = "arialbd.ttf" if bold else "arial.ttf"
    for base in [Path("C:/Windows/Fonts"), Path("C:/Windows/Fonts/Arial")]:
        path = base / font_name
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def draw_badge(draw, x, y, w, h, line1, line2):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=26, fill="#ffffff", outline="#a9bfd0", width=3)
    draw.text((x + w / 2, y + 37), line1, fill="#1f2937", font=font(34, True), anchor="mm")
    second_font = font(33, True)
    while draw.textlength(line2, font=second_font) > w - 48:
        second_font = font(max(18, second_font.size - 2), True)
    draw.text((x + w / 2, y + 86), line2, fill="#0b67c2", font=second_font, anchor="mm")


def generate_cover_png():
    img = Image.new("RGB", (1200, 630), "#edf3f7")
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 390, 1200, 630], fill="#6aa9bd")
    draw.rectangle([0, 444, 1200, 630], fill="#477f92")
    draw.rectangle([0, 540, 1200, 630], fill="#d7c592")
    draw.text((74, 78), "CHICAGO", fill="#22313d", font=font(82, True))
    draw.text((78, 158), "LAKE, L TRAIN, WORLD MAJOR", fill="#5f6f7d", font=font(27, True))
    draw_badge(draw, 844, 62, 278, 118, "Run50 #12", "ILLINOIS")

    rail_y = 250
    draw.line([92, rail_y, 1110, rail_y - 40], fill="#2a3138", width=12)
    draw.line([92, rail_y + 30, 1110, rail_y - 10], fill="#2a3138", width=7)
    for x in range(120, 1070, 88):
        draw.line([x, rail_y - 8, x + 16, rail_y + 34], fill="#2a3138", width=4)

    skyline = [
        (120, 335, 174, 520), (188, 300, 246, 520), (266, 372, 325, 520),
        (342, 245, 394, 520), (414, 310, 466, 520), (485, 210, 530, 520),
        (548, 360, 612, 520), (635, 285, 686, 520), (704, 340, 770, 520),
        (790, 260, 842, 520), (864, 375, 920, 520), (940, 330, 1000, 520),
    ]
    colors = ["#dfe9ef", "#cddde7", "#e7eef2", "#bed4e2"]
    for i, box in enumerate(skyline):
        draw.rounded_rectangle(box, radius=5, fill=colors[i % len(colors)], outline="#6f8491", width=2)
        x0, y0, x1, y1 = box
        for wx in range(x0 + 10, x1 - 8, 18):
            for wy in range(y0 + 18, y1 - 18, 28):
                draw.rectangle([wx, wy, wx + 6, wy + 10], fill="#8eb8c8")
    draw.rectangle([505, 176, 513, 210], fill="#6f8491")

    draw.ellipse([514, 414, 706, 510], fill="#c7d5dc", outline="#5c6b73", width=4)
    draw.ellipse([548, 428, 690, 493], fill="#edf3f7")
    draw.arc([514, 414, 706, 510], 190, 350, fill="#ffffff", width=5)
    draw.rounded_rectangle([132, 510, 640, 566], radius=27, fill="#cc2f2f")
    draw.text((386, 538), "45th CHICAGO MARATHON", fill="#ffffff", font=font(26, True), anchor="mm")
    draw.ellipse([868, 492, 946, 570], fill="#ffd45a", outline="#94671e", width=6)
    draw.text((907, 531), "26.2", fill="#1f2937", font=font(24, True), anchor="mm")
    OG_PATH.parent.mkdir(parents=True, exist_ok=True)
    img.save(OG_PATH, "PNG")


def generate_cover_svg():
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 750" role="img" aria-labelledby="title desc">
  <title id="title">Chicago Marathon Run50 icon cover</title>
  <desc id="desc">Icon cover with Chicago skyline, elevated train rail, Lake Michigan, Cloud Gate and a Run50 Illinois badge.</desc>
  <rect width="1200" height="750" fill="#edf3f7"/>
  <text x="74" y="112" fill="#22313d" font-family="Arial, Helvetica, sans-serif" font-size="82" font-weight="900">CHICAGO</text>
  <text x="78" y="160" fill="#5f6f7d" font-family="Arial, Helvetica, sans-serif" font-size="27" font-weight="800">LAKE, L TRAIN, WORLD MAJOR</text>
  <rect x="844" y="62" width="278" height="118" rx="26" fill="#ffffff" stroke="#a9bfd0" stroke-width="3"/>
  <text x="983" y="104" text-anchor="middle" fill="#1f2937" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="900">Run50 #12</text>
  <text x="983" y="153" text-anchor="middle" fill="#0b67c2" font-family="Arial, Helvetica, sans-serif" font-size="33" font-weight="900">ILLINOIS</text>
  <rect x="0" y="460" width="1200" height="290" fill="#6aa9bd"/>
  <rect x="0" y="520" width="1200" height="230" fill="#477f92"/>
  <rect x="0" y="646" width="1200" height="104" fill="#d7c592"/>
  <line x1="92" y1="282" x2="1110" y2="242" stroke="#2a3138" stroke-width="12" stroke-linecap="round"/>
  <line x1="92" y1="312" x2="1110" y2="272" stroke="#2a3138" stroke-width="7" stroke-linecap="round"/>
  <g stroke="#2a3138" stroke-width="4">'''
    for x in range(120, 1070, 88):
        svg += f'<line x1="{x}" y1="274" x2="{x + 16}" y2="316"/>'
    svg += '''</g>
  <g stroke="#6f8491" stroke-width="2">'''
    skyline = [
        (120, 395, 54, 230), (188, 356, 58, 269), (266, 440, 59, 185),
        (342, 292, 52, 333), (414, 372, 52, 253), (485, 250, 45, 375),
        (548, 430, 64, 195), (635, 332, 51, 293), (704, 402, 66, 223),
        (790, 310, 52, 315), (864, 444, 56, 181), (940, 388, 60, 237),
    ]
    colors = ["#dfe9ef", "#cddde7", "#e7eef2", "#bed4e2"]
    for i, (x, y, w, h) in enumerate(skyline):
        svg += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" fill="{colors[i % len(colors)]}"/>'
        for wx in range(x + 10, x + w - 8, 18):
            for wy in range(y + 18, y + h - 18, 28):
                svg += f'<rect x="{wx}" y="{wy}" width="6" height="10" fill="#8eb8c8"/>'
    svg += '''</g>
  <rect x="505" y="216" width="8" height="40" fill="#6f8491"/>
  <ellipse cx="610" cy="552" rx="96" ry="48" fill="#c7d5dc" stroke="#5c6b73" stroke-width="4"/>
  <ellipse cx="619" cy="560" rx="71" ry="32" fill="#edf3f7"/>
  <path d="M525 552 C570 506 664 506 699 552" fill="none" stroke="#ffffff" stroke-width="6" stroke-linecap="round"/>
  <rect x="132" y="608" width="508" height="56" rx="28" fill="#cc2f2f"/>
  <text x="386" y="644" text-anchor="middle" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="900">45th CHICAGO MARATHON</text>
  <circle cx="907" cy="634" r="39" fill="#ffd45a" stroke="#94671e" stroke-width="6"/>
  <text x="907" y="643" text-anchor="middle" fill="#1f2937" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="900">26.2</text>
</svg>
'''
    THUMB_PATH.write_text(svg, encoding="utf-8")


def remove_existing_card(text: str, href: str) -> str:
    pattern = re.compile(rf"\n\s*<a class=\"story-card [^\"]+\" href=\"{re.escape(href)}\">.*?</a>", re.S)
    return pattern.sub("", text)


def update_story_indexes():
    zh_path = REPO / "run50" / "stories" / "chinese" / "index.html"
    en_path = REPO / "run50" / "stories" / "english" / "index.html"
    fb_path = REPO / "run50" / "facebook" / "index.html"

    zh_card = f'''      <a class="story-card run-50" href="./chicago-marathon.html">
        <img src="../../../assets/thumb-run50-chicago-marathon-icons.svg?v={VERSION}" alt="芝加哥马拉松城市图标封面" loading="lazy" decoding="async">
        <div class="story-copy">
          <p class="story-meta">伊利诺伊芝加哥 · 2023.10.08</p>
          <h2 class="story-title">Run50 #第12州｜芝加哥马拉松</h2>
          <p class="story-desc">45周年芝加哥马拉松，也是我的第二个世界大满贯。错过早班飞机、唐人街补给、格兰特公园起跑、见证基普图姆世界纪录诞生，再陪Siqi七小时冲线。</p>
          <div class="story-foot">
            <span>长文图记</span>
            <span>阅读 →</span>
          </div>
        </div>
      </a>
'''
    en_card = f'''      <a class="story-card run-50" href="./chicago-marathon.html">
        <img src="../../../assets/thumb-run50-chicago-marathon-icons.svg?v={VERSION}" alt="Icon cover for Chicago Marathon" />
        <div class="story-card-content">
          <div class="meta">Illinois · Chicago · 2023.10.08</div>
          <h2>Chicago Marathon: State 12 and a second World Marathon Major</h2>
          <p>Running the 45th Chicago Marathon, missing the first flight, eating in Chinatown, starting in Grant Park, witnessing Kelvin Kiptum's world record day, and walking Siqi into her first Major finish.</p>
        </div>
      </a>
'''
    fb_card = f'''    <a class="story-card run-50" href="./chicago-marathon.html">
      <div>
        <p class="eyebrow">World / USA / Marathon</p>
        <h2>Chicago gave me my second World Marathon Major and State 12 of Run50</h2>
        <p>Race date: October 8, 2023. The 45th Chicago Marathon: Grant Park, the L, Chinatown, roaring crowds, Kelvin Kiptum's world record day, and a second finish beside Siqi.</p>
        <div class="meta">
          <span>Chicago, IL</span>
          <span>World Major #2</span>
          <span>Run50 Facebook</span>
        </div>
      </div>
      <img src="../../assets/thumb-run50-chicago-marathon-icons.svg?v={VERSION}" alt="Icon-style Chicago Marathon cover">
    </a>
'''
    for path, marker, card in [
        (zh_path, '<section class="story-grid" aria-label="中文故事列表">', zh_card),
        (en_path, '<section class="story-grid" aria-label="English story list">', en_card),
    ]:
        text = remove_existing_card(path.read_text(encoding="utf-8"), "./chicago-marathon.html")
        text = text.replace(marker, marker + "\n" + card, 1)
        path.write_text(text, encoding="utf-8")

    text = remove_existing_card(fb_path.read_text(encoding="utf-8"), "./chicago-marathon.html")
    text = text.replace('<main class="shell">', '<main class="shell">\n' + fb_card, 1)
    fb_path.write_text(text, encoding="utf-8")


def update_root_and_landing():
    landing = REPO / "run50" / "index.html"
    text = landing.read_text(encoding="utf-8")
    text = text.replace("<span>7 stories · growing</span>", "<span>8 stories · growing</span>")
    text = text.replace("<span>7 stories &middot; growing</span>", "<span>8 stories &middot; growing</span>")
    text = text.replace("<span>7 stories &middot; live</span>", "<span>8 stories &middot; live</span>")
    text = text.replace("from China and Miami to Mexico City and Pisa's Tuscan winter sun", "from Chicago and Miami to Mexico City, China, and Pisa's Tuscan winter sun")
    landing.write_text(text, encoding="utf-8")

    root = REPO / "index.html"
    text = root.read_text(encoding="utf-8")
    text = text.replace("assets/thumb-run50-san-antonio-marathon-icons.svg?v=20260605-1", f"assets/thumb-run50-chicago-marathon-icons.svg?v={VERSION}")
    text = text.replace("assets/thumb-run50-san-antonio-marathon-icons.svg", f"assets/thumb-run50-chicago-marathon-icons.svg?v={VERSION}")
    text = text.replace("Run50 Chinese Stories Xiangyang Guilin Hong Kong Pisa Texas San Antonio Marathon", "Run50 Chinese Stories Chicago Illinois Xiangyang Guilin Hong Kong Pisa Texas San Antonio Marathon")
    text = text.replace("Run50 English Stories Xiangyang Guilin Hong Kong Pisa Texas San Antonio Marathon", "Run50 English Stories Chicago Illinois Xiangyang Guilin Hong Kong Pisa Texas San Antonio Marathon")
    text = text.replace("Run50 Facebook Xiangyang Guilin Hong Kong Pisa Texas San Antonio Marathon", "Run50 Facebook Chicago Illinois Xiangyang Guilin Hong Kong Pisa Texas San Antonio Marathon")
    text = text.replace("Run50 Chinese Stories San Antonio cover", "Run50 Chinese Stories Chicago cover")
    text = text.replace("Run50 English Stories San Antonio cover", "Run50 English Stories Chicago cover")
    text = text.replace("Run50 Facebook San Antonio cover", "Run50 Facebook Chicago cover")
    text = text.replace("Run50 &middot; Texas + Xiangyang + Guilin + more", "Run50 &middot; Chicago + Texas + Xiangyang + more")
    root.write_text(text, encoding="utf-8")


def update_supabase_sql():
    path = REPO / "supabase" / "run50-comments.sql"
    text = path.read_text(encoding="utf-8")
    keys = [
        "run50-chicago-marathon-facebook-en",
        "run50-chicago-marathon-en",
        "run50-chicago-marathon-zh",
    ]
    for key in keys:
        text = re.sub(rf"^\s*'{re.escape(key)}',\n", "", text, flags=re.M)

    def add_keys(match):
        indent = match.group(1)
        insert = "".join(f"{indent}'{key}',\n" for key in keys)
        return insert + match.group(0)

    text = re.sub(r"^(\s*)'run50-guilin-marathon-facebook-en',", add_keys, text, flags=re.M)
    path.write_text(text, encoding="utf-8")


def main():
    indexed = extract_story()
    count = copy_story_images(indexed)
    sections = split_sections(indexed)

    zh_article = render_article(indexed, "zh", "Run50-Chicago-Marathon-clean_files/", "芝加哥马拉松照片")
    en_article = render_article(indexed, "en", "../chinese/Run50-Chicago-Marathon-clean_files/", "Chicago Marathon photo")
    fb_article = build_facebook_article(sections)

    (REPO / "run50" / "stories" / "chinese" / "chicago-marathon.html").write_text(story_page("zh", zh_article), encoding="utf-8")
    (REPO / "run50" / "stories" / "english" / "chicago-marathon.html").write_text(story_page("en", en_article), encoding="utf-8")
    (REPO / "run50" / "facebook" / "chicago-marathon.html").write_text(facebook_page(fb_article), encoding="utf-8")

    generate_cover_png()
    generate_cover_svg()
    update_story_indexes()
    update_root_and_landing()
    update_supabase_sql()
    print(f"Built Chicago story with {count} images and {len(indexed)} story events.")


if __name__ == "__main__":
    main()
