from pathlib import Path
from lxml import html
from html import escape
from PIL import Image, ImageDraw, ImageFont, ImageOps
import math
import re

REPO = Path(__file__).resolve().parents[1]
SOURCE_BASE = Path(r"Z:\ZhennanZ Folder\000-Marathon-Story-2024-2025\20230000-Marathons\2023-State-14-TX")
SOURCE_HTML = next(p for p in SOURCE_BASE.iterdir() if p.suffix.lower() == ".html")
SOURCE_FILES = next(p for p in SOURCE_BASE.iterdir() if p.is_dir() and p.name.endswith("_files"))
SITE = "https://arsenanzz.github.io/ZZ"
SLUG = "san-antonio-marathon"
VERSION = "20260605-2"
ENGAGEMENT_VERSION = "20260605"
OUT_IMG_DIR = REPO / "run50" / "stories" / "chinese" / "Run50-San-Antonio-Marathon-clean_files"
OG_PATH = REPO / "assets" / "og-run50-san-antonio-marathon-icons.png"
THUMB_PATH = REPO / "assets" / "thumb-run50-san-antonio-marathon-icons.svg"

TITLE_ZH = "Run50 #第14州｜德克萨斯：圣安东尼奥摇滚马拉松｜没有马刺，也没有文班亚马"
TITLE_EN = "Run50 #14 | Texas: San Antonio Rock 'n' Roll Marathon"
TITLE_FB = "I went to San Antonio for the Spurs and ended up running Texas"
DATE_ZH = "2023.12.03"
DATE_EN = "Dec 3, 2023"
RACE_NAME = "Rock 'n' Roll San Antonio Marathon"


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
    normalized = src[2:] if src.startswith("./") else src
    return SOURCE_BASE / normalized


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
        src_path = local_source_path(event["src"])
        with Image.open(src_path) as im:
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
        "Bulding": "Building",
        "Kng": "King",
        "Rock'n Roll": "Rock 'n' Roll",
        "Rock'n' Roll": "Rock 'n' Roll",
        "Rock 'n' Roll Start": "Rock 'n' Roll Start",
        "Qingting": "Dragonfly",
        "India Food": "Indian Food",
        "Korea Food": "Korean Food",
        "Paopao": "Bubbles",
    }
    for old, new in replacements.items():
        caption = caption.replace(old, new)
    return caption


def figure_html(src: str, caption: str, alt_base: str) -> str:
    alt = caption or alt_base
    figcaption = f"<figcaption>{escape(caption)}</figcaption>" if caption else ""
    return f'<figure><img src="{escape(src)}" alt="{escape(alt)}" loading="lazy" decoding="async">{figcaption}</figure>'


def render_figures(indexed, img_prefix: str, alt_base: str) -> str:
    parts = []
    pending_caption = ""
    for _, event in indexed:
        if event["type"] == "text":
            if is_caption(event["text"]):
                pending_caption = clean_caption(event["text"])
            continue
        if event["type"] == "img":
            parts.append(figure_html(img_prefix + event["out"], pending_caption, alt_base))
            pending_caption = ""
    return "\n      ".join(parts)


def render_zh_text(idx: int, text: str) -> str:
    if should_skip_text(text) or is_caption(text):
        return ""
    if text in ("前言", "后记"):
        return f'<h2 class="section-label">{escape(text)}</h2>'
    if text.startswith("# "):
        return f"<h2>{escape(text[2:])}</h2>"
    if text.startswith("## "):
        return f"<h3>{escape(text[3:])}</h3>"
    if text.startswith(("🏀", "📍", "🎽")):
        return f'<p class="place">{escape(text)}</p>'
    if text.startswith("- "):
        return f'<p class="end-mark">{escape(text)}</p>'
    if text.startswith(("文字", "摄影", "设计")):
        return f'<p class="credit-line">{escape(text)}</p>'
    return f"<p>{escape(text)}</p>"


def render_chinese_article(indexed):
    parts = []
    pending_caption = ""
    for idx, event in indexed:
        if event["type"] == "text":
            if is_caption(event["text"]):
                pending_caption = clean_caption(event["text"])
                continue
            html_text = render_zh_text(idx, event["text"])
            if html_text:
                parts.append(html_text)
            continue
        if event["type"] == "img":
            parts.append(figure_html("Run50-San-Antonio-Marathon-clean_files/" + event["out"], pending_caption, "圣安东尼奥摇滚马拉松照片"))
            pending_caption = ""
    return "\n      ".join(parts)


def find_pos(indexed, needle: str) -> int:
    for pos, (_, event) in enumerate(indexed):
        if event["type"] == "text" and event["text"] == needle:
            return pos
    raise RuntimeError(f"Could not find section marker: {needle}")


def split_sections(indexed):
    city = find_pos(indexed, "# 圣安东尼奥：墨味儿十足")
    race = find_pos(indexed, "# 圣安东尼奥：「25周年」摇滚马拉松")
    post = find_pos(indexed, "后记")
    return {
        "foreword": indexed[:city],
        "city": indexed[city:race],
        "race": indexed[race:post],
        "post": indexed[post:],
    }


EN_BY_INDEX = {
    5: "Preface",
    6: "This year, the Spurs somehow earned themselves the No. 1 pick. I have always been a Spurs fan. Back then I really loved Manu Ginobili, Tony Parker, and Tim Duncan - the Argentine blade, the French sports car, and the stone-faced big fundamental. The Spurs' steady, grounded temperament, mixed with Popovich's wild imagination, has always felt weirdly close to my own style.",
    9: "When San Antonio won that No. 1 pick, everyone knew the French spider-man, Victor Wembanyama, was heading there. I like watching aliens, and I have always felt Wemby is basically an alien. So when the Spurs drafted him, I thought: one way or another, I need to go see this living alien play. And if I could run a marathon while I was there, even better.",
    14: "So that was the motivation for going to San Antonio. Now for the result: during marathon weekend, the Spurs were all on the road. No game.",
    15: "But we still ran a very solid San Antonio Rock 'n' Roll Marathon, and we also got to explore a San Antonio that felt wonderfully full of Mexican flavor.",
    18: "And considering the Spurs were in the middle of a double-digit losing streak, and Wemby's alien identity still needed a little more testing, I honestly did not feel too regretful. If anything, it gave me something to look forward to. I can wait until the alien takes off another layer of disguise, then go see him properly.",
    22: "# San Antonio: full of Mexican soul",
    23: "Texas, San Antonio",
    24: "Besides the Spurs, San Antonio is also a really distinctive travel city. I remember Yao Ming once said in an interview that among American cities, his favorite was San Antonio, Texas.",
    33: "San Antonio absolutely deserves Yao's high praise. It is the Venice of America. Conde Nast Traveler once called it one of the most popular travel cities in the United States, and even among the top cities globally.",
    42: "San Antonio is loved for its deep history and layered culture: traces of Spanish influence and war are everywhere, Mexican character is impossible to miss, and Native American traditions are also part of the mix. All of that blends together in this pleasant waterside city.",
    45: "We left Louisville, connected through Dallas, took off and landed under a spectacular Texas sunset, and arrived smoothly in San Antonio just after dark.",
    50: "After leaving the airport and dropping our things at the Airbnb, we could not wait to take a bus downtown for food. The Latino driver smiled and told us, \"Free!\"",
    53: "Not long after getting off the bus, we ran into the Alamo by chance. Americans often say, \"If you have not been to the Alamo, you have not really been to Texas.\" The Alamo, originally expanded from a mission into a fortress in downtown San Antonio, is a household name in Texas. Its place in American history carries a symbolic weight similar to Pearl Harbor in 1941.",
    56: "On March 2, 1836, Texas declared independence from Mexico, partly over the issue of slavery, and was soon surrounded by the Mexican army. Around 200 defenders held the Alamo for 13 days against thousands of Mexican troops. In the end, all of the male defenders were killed.",
    59: "Three weeks later, \"Remember the Alamo!\" became the rallying cry for Texas independence. The main Texan force won at the San Jacinto River, Texas remained independent for several years, and nine years later it joined the United States. That is where the idea of the Lone Star Republic comes from.",
    64: "But San Antonio never abandoned its original Mexican cultural color. Even today, those traditional Mexican elements have already merged naturally into modern Texan life.",
    69: "A short walk from the Alamo brings you to the River Walk. It is lively, beautiful, and especially magical near Christmas, with lights shimmering on the water, tourist boats passing back and forth, and even Santa posing with visitors from a platform in the river.",
    80: "We found a pretty good Indian restaurant, sat by the river, felt the breeze coming off the River Walk, and ate naan and curry with the night view right beside us.",
    93: "People say that in energetic San Antonio, the one thing you should not miss at night - besides the River Walk - is The Saga, the visual art projection show at Main Plaza. So after eating our fill, we decided to go check it out.",
    94: "Since its debut in June 2014, this free projection show has run year-round. It starts on Friday and Saturday nights at 9:00, 9:30, and 10:00, and on Sunday and Tuesday nights at 7:30, 8:00, and 8:30. Each show lasts 24 minutes.",
    96: "With dramatic music in the background, the old and majestic facade of San Fernando Cathedral becomes the perfect canvas. One vivid scene after another unfolds across it, telling the history of San Antonio. The Roman Catholic San Fernando Cathedral is the burial place of Alamo heroes, the spiritual heart of the city, and one of the oldest cathedrals in the United States.",
    101: "With brilliant color, precise projection, powerful music, and constantly shifting imagery, this show - designed specifically around the shape of the cathedral facade - has become one of San Antonio's most attractive sights. Through architectural projection art, it tells the story of the city's discovery, settlement, and rise, along with the larger legend of the Lone Star State.",
    106: "From the earliest Native peoples to faces familiar to Spurs fans, the show becomes a dazzling kaleidoscope of city history: ancestral caves, sacred and everyday oil wells dug from underground, Indigenous people and Spaniards, Native communities and colonists, the Mexican Revolution, the Battle of the Alamo, and modern San Antonio.",
    109: "The music of San Antonio folk singer Tish Hinojosa, conjunto legend Flaco Jimenez, Scottish folk singer Donovan, and others blends beautifully with the sound and visuals, pulling the audience into the legendary history of the Alamo City.",
    114: "The artist behind this gorgeous projection show, Xavier de Richemont, is a French painter who has become one of the world's most popular visual artists. Over the past 20-plus years, he has designed major visual art works around the world.",
    119: "Twenty-four minutes to tell the history of a city in such a beautiful form - it was honestly wonderful. It is the kind of immersive audio-visual experience you really have to see in person. We watched it twice in one go.",
    134: "The next day in San Antonio started with American-style Chinese food at Ming's. After that, we followed the River Walk and a small stretch of downtown to Arsenal Bridge, which Siqi strongly recommended. With my Arsenal jacket and my \"Arsenal guy\" nickname, it turned into a once-in-a-century photo session.",
    151: "After picking up our race gear, we went to the highest point in San Antonio: the Tower of the Americas. It is one of the city's landmarks and shows off San Antonio's modern side.",
    156: "The Tower of the Americas sits in Hemisfair Park in southern San Antonio. It is 750 feet tall and was built in 1968 to celebrate the city's 250th anniversary.",
    161: "From 1968 to 1996, this tower was the tallest observation tower in the United States, and it was also a central feature of the 1968 World's Fair.",
    168: "Today, visitors can take an elevator to the top and look out over the whole city. You can also go up around sunset, eat in the rotating restaurant, enjoy the view, and get a relaxed taste of modern city life.",
    177: "The 4D theater below the tower is also pretty fun, and the graphics near the entrance show many of the city's different landmarks.",
    186: "Leaving the Tower of the Americas, we followed the paths through Hemisfair Park toward the River Walk to take a night boat ride on the San Antonio River. We had taken boats before in New York and Hawaii, and both were easy with barely any wait. But the River Walk was completely different. The line looked like it stretched for kilometers. I could hardly believe it, so I asked a party-going visitor nearby and confirmed that yes, they were all waiting for the boat.",
    195: "We did not really want to stand there forever. There were three boarding points total, so we optimistically thought maybe the other two would not be too crowded. We practically ran to check both of them, and finally gave up completely. At least we could sit down and eat some snacks in peace.",
    202: "Later that night, we went back to the dock. The line was finally shorter, and after waiting about half an hour, we got on the boat. The female captain was cool and decisive. When she saw some noisy kids causing trouble, she spoke to their parents and had them leave the boat.",
    209: "At last, we could properly enjoy the River Walk. Under the Christmas lights, it was almost unreal.",
    210: "People say that San Antonio's modern life and its unique urban spirit are concentrated in this bustling riverside walkway. Many cities in the world call themselves some version of Venice, but San Antonio stands apart. No one really competes with it for the title of the Venice of America.",
    215: "The reason is the river. The San Antonio River runs through central Texas and passes right through downtown. The River Walk stretches for 4.5 kilometers and has become the city's most important leisure and entertainment space, lined with restaurants and performance venues. It is where the Spurs hold championship parades, and it is one of Texas's top entertainment destinations, drawing millions of visitors every year.",
    218: "The River Walk was developed in the 1920s, originally as a way to prevent flooding. Downtown streets seem to float above the riverbanks, and modern stairways at street corners lead down to the water. Once you step below street level, the city suddenly opens up. The river winds back and forth, and every few dozen meters, stone arch bridges cross over it like something from a Suzhou garden.",
    223: "Riding the boat, looking at both banks, feeling the balance of nature and city life, and listening to the Latina captain introduce the history of the River Walk - it all had a uniquely Mexican romance. People moved along the walkway, black ducks played in the water, and for a moment it felt like the American version of a dream water town.",
    226: "After the boat ride, it was finally time to head back to the Airbnb. We had been out all day and were honestly tired. We sat on a city street waiting for a Lyft while familiar Latino faces, colorful horse-drawn carriages, and glowing snowmen passed by.",
    234: "# San Antonio: the 25th anniversary Rock 'n' Roll Marathon",
    235: "Texas, San Antonio",
    236: "The Rock 'n' Roll Marathon Series is one of the largest marathon series in the world. It began in 1998 with a simple idea: make running more fun. The series has now reached its 25th anniversary. Its signature feature is live rock bands placed along the course, using rock music to cheer runners on.",
    237: "The San Antonio Rock 'n' Roll race we ran was celebrating its 15th year. In 2023, the marathon course started at City Hall, continued north toward Broadway and Brackenridge Park, then entered Joint Base San Antonio-Fort Sam Houston at Mile 5 and ran through the base for three miles.",
    238: "Both the marathon and half marathon finished in front of UTSA's downtown campus. The course passed many landmarks, including the Tower of the Americas, the River Walk, and the Torch of Friendship. It also crossed city neighborhoods, with live music around every corner.",
    243: "The pre-race expo was large. People said it matched the usual Rock 'n' Roll scale, and honestly it felt no less grand than a major marathon. Packet pickup was extremely efficient.",
    248: "After getting the gear, you could walk into the exhibition area behind it. There were tons of Rock 'n' Roll photo boards, plenty of running-related vendors, and even free beef sticks and yogurt.",
    255: "There were a lot of people and the atmosphere was lively, but it was not crowded, because the expo space itself was huge. It really did feel like a race with production value.",
    260: "The race started at 7:00 in the morning. We took a taxi to the area near San Antonio City Hall an hour early. When we arrived, it was still dark, and we still had to walk a short distance with the other runners.",
    267: "The sky was not fully bright yet, but the start corrals were already stretched into long lines. The organizers assigned runners to different areas based on pace, and each corral had toilets, which was very thoughtful.",
    278: "At exactly 7:00 a.m., runners began to start one group after another. Since I was in a later corral, I did not actually pass under the arch until almost 7:20. By then the sky had brightened. I saw many runners leaving their extra warm clothes beside the flower beds near the start, and the DJ was full of energy.",
    283: "After starting, we first ran east along Travis Street. There were graffiti walls and cosplay runners along the way. The early San Antonio temperature was comfortable, the weather was good, and I thought this was destined to be a happy city run.",
    298: "Around Mile 1, we reached Broadway. I took off my red jacket and revealed my Spurs Ginobili jersey underneath. Transformation complete.",
    309: "The morning sun was lovely and not harsh. Half of my face was lit up by the light, which felt great. I also saw a runner in a Cristiano Ronaldo Al Nassr jersey ahead of me, which made me feel oddly at home.",
    316: "After Mile 2, we ran through Brackenridge Park. This park sits in the heart of San Antonio, has a long history, and is genuinely scenic. But what caught me most was one Mexican-style band after another. The atmosphere was excellent.",
    325: "The biggest surprise for me was the Mexican big-skirt dance. Later I learned it was Jarabe, Mexico's national dance. Locals call it Jarabe: a dance blending Indigenous and Spanish culture. The women wear bright dresses with skirts more than 50 feet wide, lifting and spinning the fabric into flying flowers, while the men wear black outfits, wide-brimmed hats, and boots, kicking rhythmically as if the stage were a drum. Clapping, whistles, and footwork combine into a magnificent Mexican folk scene. Clearly, my casual nickname, \"big-skirt dance,\" was a bit rude.",
    330: "Those flying skirt flowers and bright, fiery steps sketch out the passionate character of Mexican culture. Mexicans love to dance; in streets, alleys, even on buses, you can hear energetic Mexican music, and people dance when the music starts. Wherever there is music, there seems to be a charming Mexican dance nearby. This was the second time after Chicago that I had seen a roadside performance like this, and it left a deep impression.",
    341: "Before leaving Brackenridge Park, there was a memorial portrait route for fallen soldiers, followed by American flags waving on both sides. It looked pretty grand.",
    350: "After Mile 4, Santa Claus was greeting people along the road. I smiled and said, \"Merry Christmas!\"",
    355: "Ahead was San Antonio Country Club. Of course there was another band, plus cheering spectators and gentle sunshine.",
    364: "I also ran into a fellow Arsenal veteran, though I had no idea who his No. 13 shirt was supposed to be. A spectator brought her kid to blow bubbles by the road too, which was very cheerful.",
    371: "Starting at Mile 5, we ran three miles through a U.S. military base. Joint Base San Antonio is made up of Fort Sam Houston, Randolph Air Force Base, and Lackland Air Force Base. It belongs to the U.S. Air Force's 502nd Air Base Wing, and U.S. Army South is headquartered at Fort Sam Houston.",
    378: "Our marathon route went straight through Fort Sam Houston. The white castle-like Fort Sam Houston Theater was beautiful. Along the road were armored vehicles, different aircraft, soldiers cheering and handing out supplies, and of course, more bands.",
    387: "At that point I kept thinking: I am actually running through a U.S. military base. What a strange and novel experience, another weird little running route unlocked. Of course, if the marathon course had not been routed through here, I would never have dared to come check in on my own.",
    396: "After leaving the military base, just past Mile 8, we reached the Quadrangle at Fort Sam Houston, which is also a well-known spot.",
    399: "Built in 1876, it is said to be a historic landmark and strategic site, with a clock tower, another tower, and a historic oak tree inside. What impressed me most was still the clock tower. The Quadrangle and museum are open to the public, but non-military visitors need a pass.",
    418: "The next stretch went through a series of residential neighborhoods. The kids along the road were adorable. A priest sprinkled water on runners, there were street performers dressed up with signs, a green pain-relief squad, a second bearded Santa, and even a Smile unicorn lady. Every mile had a different bit of fun. San Antonio's local warmth showed up fully in the Rock 'n' Roll Marathon.",
    425: "Finally the half and full marathons split. My half marathon time was just under two hours. If I could keep that rhythm, going under four hours again looked possible.",
    434: "Entering the second half, I still felt pretty good. We also happened to be running into the park green space, and this section felt totally different from the first half.",
    441: "From Miles 13 to 20, we first passed Lincoln Park, then followed Salado Creek Greenway through Martin Luther King Park, Covington Park, and Southside Lions Park.",
    448: "The greenway scenery was beautiful, and bands and volunteers kept cheering everyone on. Here I also saw a wheelchair athlete struggling up a hill. No runners deliberately stepped in to help him. That, too, is sportsmanship - and the greatest respect for him.",
    459: "Lions Park Lake inside Southside Lions Park marked the southernmost point of the race. After that, it was time to turn back.",
    470: "Leaving the chain of park roads, we headed north through exposed streets. By then, San Antonio was getting close to noon, the temperature was rising, and the worst part was a long uphill stretch.",
    479: "This race did have some rolling hills. The first half had three, but my legs were fresh and the weather was cool, so they were manageable. The second half only had one, but it was in the worst possible place: a 4.5-mile continuous climb between Miles 20 and 25, with grades up to 11 percent. That part was hard, and I fell off pace.",
    496: "The sky was very blue, the grade was very real, and the temperature was a little high. So I strategically gave up on breaking four hours and switched to a run-walk plan. After Mile 23, the Tower of the Americas was clearly right in front of me.",
    501: "We turned left in front of Hemisfair, where the Tower of the Americas stands, and entered the final mile-plus.",
    535: "The finish was almost there. Both sides of the course were packed with people, everyone eager and ready, probably waiting to welcome their family and friends back. I have seen scenes like this countless times, but every time they still move me. My final time stopped at 4 hours and 12 minutes.",
    540: "The finish line was at the University of Texas at San Antonio downtown campus. The medal theme was the Mexican Jarabe dance, and the tomato-and-egg color scheme felt very festive.",
    547: "It was pretty hot. I saw volunteers pulling bottle after bottle of water out of a little ice hill and tossing them into buckets. Somehow just watching that felt cooling.",
    554: "The post-race party area also had live bands. People sat on the grass, listened to music, and stretched. Siqi had finished long before me. We took a photo together in front of the big flower wall, took a bunch of medal photos, and happily called a taxi back to the Airbnb.",
    565: "On the way, we ordered a big Korean meal for delivery. We had wanted Chinese food, but San Antonio did not seem to have many good Chinese options. Korean food, though, had plenty of highly rated restaurants.",
    570: "After eating, we went to the McNay Art Museum near our Airbnb to absorb some art bacteria and loosen up the legs.",
    579: "The museum is free on the first Sunday of every month. Perfectly enough, marathon day was the first Sunday of December. The biggest surprise was that it actually had real works by Monet and Picasso, plus all kinds of colorful paintings and sculptures.",
    584: "So of course we took out the medals and posed with the masterpieces. Medal plus artwork - not awkward at all.",
    589: "Postscript",
    590: "The next day, before heading home, we cleaned the Airbnb extremely well. The host later left a comment: \"Extreme clean!\"",
    591: "The Texas sky was still beautiful. From inside the plane, I watched the colors outside the window shift from orange to deep blue, like time passing right in front of me.",
    600: "This was our final marathon of 2023, and also our tenth marathon of the year. Calling it a perfect ten does not feel exaggerated at all.",
    601: "In 2023, I ran some marathons and published some papers. I learned a lot that year, and the work that once felt impossible to start gradually became more manageable. I guess I was finally getting a little bit of a PhD student's rhythm - though I was also getting close to graduation.",
    602: "In daily life, Siqi and I started sticking to a 5 a.m. wake-up, 10 p.m. sleep schedule at the beginning of the year, and I felt much more energetic. Recently I have also been learning about the 16/8 eating window and the 25-minute Pomodoro method, both of which have helped me.",
    603: "Also, this year I watched a ridiculous number of documentaries and films about aliens and the universe, and I even had a chance to talk about UFOs with a scholar from Los Alamos. All of that made me even more curious about the world.",
    604: "Writing this, all of my 2023 running stories are finally complete. One more thing off my mind. Nice.",
    605: "At the end here, for some reason, I could not help adding this tiny personal summary. I honestly have not done this kind of year-end reflection in many years. Maybe because it feels way too sentimental, or maybe because there usually is not much worth getting excited about. But for 2023, it was worth it.",
    606: "2024 is almost here. Siqi and I are both full of expectations for the new life ahead, even a little excited. My request is not high: graduate smoothly and find a good job...",
    607: "Should be fine, right?",
    608: "- End -",
    609: "Words | Arsenan",
    610: "Photos | Arsenan",
    611: "Design | Arsenan",
}


ENGLISH_COPY = {
    "foreword": (
        "Preface: the Spurs trip that became a marathon",
        "Texas · San Antonio",
        [
            "The whole idea started with basketball. I have been a Spurs fan for years, the Ginobili-Parker-Duncan era kind of Spurs: calm, stubborn, disciplined, and somehow a little magical.",
            "When San Antonio landed the No. 1 pick and Victor Wembanyama arrived, I figured I should go see this living alien in person. And if there happened to be a marathon in town, even better.",
            "The joke, of course, was that the Spurs were away during marathon weekend. No Wemby, no live Spurs game. But we still got a terrific Rock 'n' Roll marathon and a deeply Mexican-flavored San Antonio weekend. State 14 was checked off after all.",
        ],
    ),
    "city": (
        "State 14: Texas, the Alamo, and San Antonio's Mexican soul",
        "Texas · San Antonio",
        [
            "San Antonio is not just a Spurs city. It is one of the most distinctive travel cities in the United States, shaped by Spanish missions, Mexican culture, Indigenous history, Texas independence, and that soft water-city romance around the River Walk.",
            "The Alamo gives the place its Texas mythology. The phrase 'Remember the Alamo' still sits at the center of how the Lone Star story is told, and standing there downtown makes the history feel less like a textbook and more like a street corner.",
            "But what I loved more was how San Antonio never really let go of its Mexican texture: music, food, lights, colors, churches, the River Walk, the Main Plaza projection show, and that easy mix of tourist bustle and local life.",
            "We flew in through Dallas under a huge Texas sunset, walked into the Alamo almost by accident, ate by the river, watched The Saga light up San Fernando Cathedral, took photos on Arsenal Bridge, climbed toward the Tower of the Americas, and eventually picked up our race gear.",
            "So if the article needed a Texas introduction, San Antonio already wrote one for us: Lone Star history on one side, Mexican warmth on the other, and a river running right through the middle.",
        ],
    ),
    "race": (
        "Race day: bands, Fort Sam Houston, greenways, and one brutal late hill",
        "Rock 'n' Roll San Antonio Marathon · Dec 3, 2023",
        [
            "The race started at 7 a.m. near San Antonio City Hall. Because I was in a later corral, I crossed the start closer to 7:20, just as the sky was finally brightening and the DJ was waking everyone up properly.",
            "The first miles felt exactly like a happy city run. We rolled through downtown, onto Broadway, into Brackenridge Park, past murals, costumes, live bands, Santa sightings, Mexican dance performances, and a surprising number of little street moments that made the Rock 'n' Roll name feel earned.",
            "Around Mile 5, the course entered Joint Base San Antonio-Fort Sam Houston. Running through a U.S. military base, past aircraft, armored vehicles, old theater buildings, and uniformed volunteers, was one of those odd marathon-only experiences I never would have planned on my own.",
            "After the half/full split, the course changed tone. The second half moved through Lincoln Park, Salado Creek Greenway, Martin Luther King Park, Covington Park, and Southside Lions Park. It was greener and quieter, with bands and volunteers still keeping the road alive.",
            "Then Texas reminded me it had hills. From roughly Mile 20 to Mile 25, there was a long exposed climb under stronger sun, with grades that felt rude for that stage of a marathon. I let go of the sub-four idea and switched into survival mode.",
            "The Tower of the Americas eventually came back into view, the crowd thickened, and I crossed the line in 4 hours and 12 minutes. Not the cleanest finish, but for State 14 and the final marathon of 2023, it felt just right.",
            "The medal carried the bright colors of Mexican Jarabe dance, and the post-race area turned into a small music-and-medal picnic. We ate Korean food, visited the McNay Art Museum with the medal, and somehow made the whole day feel like one long San Antonio afterparty.",
        ],
    ),
    "post": (
        "Postscript: closing out 2023 with State 14",
        "Texas sky · 2023 finale",
        [
            "On the flight home, the Texas sky shifted from orange to deep blue, which felt like the right closing image for the year.",
            "This was our final marathon of 2023, and our tenth marathon of the year. Ten races, papers, PhD work, early mornings, new habits, a lot of alien documentaries, and a slowly clearer sense that I was finally getting the hang of things.",
            "State 14, Texas: San Antonio Rock 'n' Roll Marathon. No Spurs game, no Wembanyama sighting, but a full Texas story anyway.",
        ],
    ),
}


def text_for(idx: int, text: str, lang: str) -> str:
    if lang == "zh":
        return text
    if is_caption(text):
        return clean_caption(text)
    if should_skip_text(text):
        return ""
    try:
        return EN_BY_INDEX[idx]
    except KeyError as exc:
        raise RuntimeError(f"Missing English translation for index {idx}: {text}") from exc


def render_text(idx: int, text: str, lang: str) -> str:
    value = text_for(idx, text, lang)
    if not value or is_caption(text):
        return ""
    if text in ("前言", "后记") or value in ("Preface", "Postscript"):
        return f'<h2 class="section-label">{escape(value)}</h2>'
    if value.startswith("# "):
        return f"<h2>{escape(value[2:])}</h2>"
    if value.startswith("## "):
        return f"<h3>{escape(value[3:])}</h3>"
    if text.startswith(("🏀", "📍", "🎽")) or idx in (23, 235):
        return f'<p class="place">{escape(value)}</p>'
    if value.startswith("- "):
        return f'<p class="end-mark">{escape(value)}</p>'
    if idx in (609, 610, 611):
        return f'<p class="credit-line">{escape(value)}</p>'
    return f"<p>{escape(value)}</p>"


def render_ordered_article(indexed, lang: str, img_prefix: str, alt_base: str) -> str:
    parts = []
    pending_caption = ""
    for idx, event in indexed:
        if event["type"] == "text":
            if is_caption(event["text"]):
                pending_caption = text_for(idx, event["text"], lang)
                continue
            html_text = render_text(idx, event["text"], lang)
            if html_text:
                parts.append(html_text)
            continue
        if event["type"] == "img":
            parts.append(figure_html(img_prefix + event["out"], pending_caption, alt_base))
            pending_caption = ""
    return "\n      ".join(parts)


def render_english_article(indexed) -> str:
    return render_ordered_article(indexed, "en", "../chinese/Run50-San-Antonio-Marathon-clean_files/", "San Antonio Marathon photo")


def render_facebook_article(sections):
    story_prefix = "../stories/chinese/Run50-San-Antonio-Marathon-clean_files/"
    parts = [
        "<p>On December 3, 2023, I ran State 14 of my Run50 project at the Rock 'n' Roll San Antonio Marathon. It started as a Spurs and Wembanyama excuse, turned into a full Texas weekend, and ended with a 4:12 finish after one very unfriendly late climb.</p>",
        render_ordered_article(sections["race"], "en", story_prefix, "Rock 'n' Roll San Antonio Marathon photo"),
        "<p>To explain why I was in San Antonio in the first place, we need to rewind from the finish chute back to basketball.</p>",
        render_ordered_article(sections["foreword"], "en", story_prefix, "Spurs and San Antonio marathon photo"),
        "<p>And around the race itself, San Antonio gave the trip its real texture: Alamo history, River Walk lights, Mexican music, city boats, projection art, and that soft December travel glow.</p>",
        render_ordered_article(sections["city"], "en", story_prefix, "San Antonio city photo"),
        "<p>After the medal photos and the flight home, this race also became the closing note of my 2023 running year.</p>",
        render_ordered_article(sections["post"], "en", story_prefix, "Texas post-race photo"),
    ]
    return "\n      ".join(part for part in parts if part)


def page_css() -> str:
    return """
    :root {
      --paper: #edf3f7;
      --surface: #ffffff;
      --ink: #20242b;
      --muted: #667085;
      --line: #d0dfe8;
      --river: #0b67c2;
      --brick: #9f3a2d;
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
      background: #e1e8dc;
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
      --blue: #0b67c2;
      --ink: #111111;
      --muted: #666666;
      --line: #dddddd;
      --soft: #f0f4f8;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      color: var(--ink);
      background: #ffffff;
      font-family: Arial, Helvetica, sans-serif;
      letter-spacing: 0;
      overflow-x: hidden;
    }
    .topbar {
      background: var(--blue);
      color: #ffffff;
      min-height: 38px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      padding: 8px 18px;
      font-size: 13px;
      font-weight: 800;
      letter-spacing: .08em;
      text-transform: uppercase;
    }
    .brand {
      padding: 18px;
      border-bottom: 1px solid var(--line);
    }
    .brand h1 {
      margin: 0 0 14px;
      color: var(--blue);
      font-size: clamp(30px, 6vw, 54px);
      line-height: .96;
      letter-spacing: 0;
      text-transform: uppercase;
    }
    .brand nav { display: flex; flex-wrap: wrap; gap: 18px; font-size: 13px; font-weight: 800; text-transform: uppercase; }
    .brand a { color: #222222; text-decoration: none; }
    main { max-width: 1060px; margin: 0 auto; padding: 34px 18px 60px; }
    .label {
      display: inline-block;
      margin: 0 0 18px;
      padding: 7px 10px;
      background: var(--blue);
      color: #ffffff;
      font-size: 13px;
      font-weight: 900;
      letter-spacing: .08em;
      text-transform: uppercase;
    }
    .headline {
      max-width: 900px;
      margin: 0;
      font-size: clamp(38px, 7vw, 72px);
      line-height: .95;
      letter-spacing: 0;
      font-weight: 900;
      overflow-wrap: anywhere;
    }
    .standfirst {
      max-width: 820px;
      margin: 18px 0 22px;
      color: #333333;
      font-size: 20px;
      line-height: 1.45;
    }
    .byline { display: flex; flex-wrap: wrap; gap: 8px; margin: 22px 0 34px; color: #444444; font-size: 13px; font-weight: 900; text-transform: uppercase; }
    .byline span { background: #f1f1f1; padding: 8px 10px; }
    .lead-media { margin: 0 0 32px; border-top: 8px solid var(--blue); }
    .lead-media img { display: block; width: 100%; height: auto; }
    .lead-media figcaption { margin-top: 8px; color: var(--muted); font-size: 13px; }
    .brief {
      margin: 0 0 34px;
      padding: 20px 22px;
      background: var(--soft);
      border-top: 6px solid var(--blue);
      display: grid;
      grid-template-columns: 160px 1fr;
      gap: 10px 18px;
      color: #222222;
      font-size: 15px;
      line-height: 1.5;
    }
    .brief strong { color: var(--blue); font-size: 12px; text-transform: uppercase; letter-spacing: .08em; }
    .story {
      max-width: 820px;
      margin: 0 auto;
      font-family: Georgia, "Times New Roman", serif;
      font-size: 19px;
      line-height: 1.7;
    }
    .story h2 {
      margin: 44px 0 16px;
      font-family: Arial, Helvetica, sans-serif;
      font-size: clamp(26px, 4vw, 42px);
      line-height: 1.08;
      letter-spacing: 0;
    }
    .story p { margin: 0 0 18px; }
    .story figure { margin: 28px 0 32px; }
    .story img { display: block; width: 100%; height: auto; }
    .story figcaption { margin-top: 7px; color: var(--muted); font-family: Arial, Helvetica, sans-serif; font-size: 12px; line-height: 1.45; }
    @media (max-width: 700px) {
      .topbar { align-items: flex-start; flex-direction: column; }
      .brief { grid-template-columns: 1fr; }
      main { width: 100vw; max-width: 100vw; padding: 26px 18px 60px; overflow: hidden; }
      .headline { width: min(100%, 320px); max-width: 320px; font-size: 30px; line-height: 1.08; white-space: normal; word-break: break-word; }
      .standfirst { width: min(320px, calc(100vw - 36px)); max-width: min(320px, calc(100vw - 36px)); font-size: 18px; overflow-wrap: anywhere; }
      .byline span { max-width: 100%; }
      .brand nav { width: min(320px, calc(100vw - 36px)); max-width: min(320px, calc(100vw - 36px)); gap: 10px 14px; }
      .byline, .lead-media, .brief, .story { width: min(320px, calc(100vw - 36px)); max-width: min(320px, calc(100vw - 36px)); overflow-wrap: anywhere; }
    }
    """


def engagement_block(locale: str, page_key: str, comment_id: str, rel: str) -> str:
    if locale == "zh-CN":
        kicker = "留言 / 阅读"
        heading = "跑完以后，说两句"
        note = "不用登录也可以留言。新留言会直接显示。"
        views = "阅读"
        loading = "评论加载中..."
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
    html_lang = "zh-CN" if is_zh else "en"
    kicker = "Run50 Stories · Texas" if not is_zh else "Run50 Stories · 德克萨斯"
    dek = (
        "这是 Run50 的第14州，也是2023年的收官马拉松：从马刺和文班亚马的念头出发，最后在圣安东尼奥跑过阿拉莫、河畔步道、Fort Sam Houston、绿道和一段德州热坡。"
        if is_zh
        else "State 14 of Run50 and the 2023 season finale: a Spurs-inspired trip to San Antonio, an Alamo/River Walk weekend, and a 4:12 marathon through Fort Sam Houston, park greenways, music blocks, and a late Texas hill."
    )
    nav = (
        '<a href="./index.html">← 中文故事</a><a href="../english/san-antonio-marathon.html">English</a><a href="../../facebook/san-antonio-marathon.html">Facebook</a><a href="../../index.html">Run50</a>'
        if is_zh
        else '<a href="./index.html">← English Stories</a><a href="../chinese/san-antonio-marathon.html">中文</a><a href="../../facebook/san-antonio-marathon.html">Facebook</a><a href="../../index.html">Run50</a>'
    )
    meta = (
        '<span>圣安东尼奥</span><span>2023.12.03</span><span>Run50 #14</span><span>4小时12分</span>'
        if is_zh
        else '<span>San Antonio, Texas</span><span>Dec 3, 2023</span><span>Run50 #14</span><span>4:12 finish</span>'
    )
    page_key = f"run50-{SLUG}-zh" if is_zh else f"run50-{SLUG}-en"
    comment_id = "supabase-comments-san-antonio-zh" if is_zh else "supabase-comments-san-antonio-en"
    return f"""<!DOCTYPE html>
<html lang="{html_lang}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{escape(title)}</title>
  <meta name="description" content="{escape(dek)}">
  <meta property="og:type" content="article">
  <meta property="og:title" content="{escape(title)}">
  <meta property="og:description" content="{escape(dek)}">
  <meta property="og:image" content="{SITE}/assets/og-run50-san-antonio-marathon-icons.png?v={VERSION}">
  <meta property="og:url" content="{SITE}/run50/stories/{'chinese' if is_zh else 'english'}/san-antonio-marathon.html">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:image" content="{SITE}/assets/og-run50-san-antonio-marathon-icons.png?v={VERSION}">
  <link rel="stylesheet" href="../../../assets/zz-engagement.css?v={ENGAGEMENT_VERSION}">
  <style>{page_css()}</style>
</head>
<body>
  <nav class="story-nav">{nav}</nav>
  <header class="page-header">
    <p class="kicker">{escape(kicker)}</p>
    <h1>{escape(title)}</h1>
    <div class="meta">{meta}</div>
    <p class="dek">{escape(dek)}</p>
  </header>
  <main class="article-shell">
    <article class="article-body">
      {article}
    </article>
    {engagement_block('zh-CN' if is_zh else 'en', page_key, comment_id, '../../../assets')}
  </main>
  <footer class="page-footer">Run50 · Texas · San Antonio Rock 'n' Roll Marathon</footer>
</body>
</html>
"""


def facebook_page(article: str) -> str:
    standfirst = "Race date: Dec 3, 2023. State 14 of Run50: San Antonio, a Spurs-inspired trip, a Rock 'n' Roll course through Fort Sam Houston and greenways, and a 4:12 finish under the Texas sun."
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>San Antonio Marathon | Run50 Facebook</title>
  <meta name="description" content="{escape(standfirst)}">
  <meta property="og:type" content="article">
  <meta property="og:title" content="{escape(TITLE_FB)}">
  <meta property="og:description" content="{escape(standfirst)}">
  <meta property="og:image" content="{SITE}/assets/og-run50-san-antonio-marathon-icons.png?v={VERSION}">
  <meta property="og:url" content="{SITE}/run50/facebook/san-antonio-marathon.html">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:image" content="{SITE}/assets/og-run50-san-antonio-marathon-icons.png?v={VERSION}">
  <link rel="stylesheet" href="../../assets/zz-engagement.css?v={ENGAGEMENT_VERSION}">
  <style>{facebook_css()}</style>
</head>
<body>
  <div class="topbar"><span>Run50 Facebook</span><span>Race date: Dec 3, 2023</span></div>
  <header class="brand">
    <h1>Run50 USA</h1>
    <nav>
      <a href="../index.html">Run50</a>
      <a href="../stories/english/san-antonio-marathon.html">Full English Story</a>
      <a href="../stories/chinese/san-antonio-marathon.html">Chinese Original</a>
    </nav>
  </header>
  <main>
    <p class="label">USA / Texas / Marathon</p>
    <h1 class="headline">{escape(TITLE_FB)}</h1>
    <p class="standfirst">{escape(standfirst)}</p>
    <div class="byline"><span>By Arsenan</span><span>Run50 #14</span><span>San Antonio, Texas</span><span>4:12 finish</span></div>
    <figure class="lead-media">
      <img src="../../assets/og-run50-san-antonio-marathon-icons.png?v={VERSION}" alt="San Antonio icon cover with Alamo, River Walk, Tower of the Americas, guitar, and Run50 Texas badge">
      <figcaption>San Antonio icon cover with the Alamo, River Walk, Tower of the Americas, rock music and Run50 Texas badge.</figcaption>
    </figure>
    <section class="brief" aria-label="At a glance">
      <strong>Race</strong><span>Rock 'n' Roll San Antonio Marathon, State 14 of Run50.</span>
      <strong>Course</strong><span>City Hall start, Broadway, Brackenridge Park, Fort Sam Houston, Salado Creek Greenway, Hemisfair finish.</span>
      <strong>Result</strong><span>4 hours 12 minutes, after a late exposed Texas climb.</span>
      <strong>Why Texas</strong><span>A Spurs/Wembanyama idea that became an Alamo, River Walk and marathon weekend.</span>
    </section>
    <article class="story">
      {article}
    </article>
    {engagement_block('en', f'run50-{SLUG}-facebook-en', 'supabase-comments-san-antonio-facebook', '../../assets')}
  </main>
</body>
</html>
"""


def write_clean(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    cleaned = "\n".join(line.rstrip() for line in text.strip().splitlines()) + "\n"
    path.write_text(cleaned, encoding="utf-8")


def load_font(size: int, bold: bool = True):
    candidates = [
        r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\segoeuib.ttf" if bold else r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\calibrib.ttf" if bold else r"C:\Windows\Fonts\calibri.ttf",
    ]
    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default()


def fit_font(draw, text: str, max_width: int, start_size: int, min_size: int, bold: bool = True):
    size = start_size
    while size >= min_size:
        font = load_font(size, bold)
        bbox = draw.textbbox((0, 0), text, font=font)
        if bbox[2] - bbox[0] <= max_width:
            return font
        size -= 2
    return load_font(min_size, bold)


def draw_cover(draw, scale: float = 1.0):
    def s(v):
        return int(round(v * scale))

    ink = "#20242b"
    blue = "#0b67c2"
    muted = "#667085"
    river = "#2f8fa3"
    clay = "#ba4a2b"
    tan = "#d7b98b"
    gold = "#f5b32f"
    green = "#5a8f67"

    title_font = load_font(s(66), True)
    subtitle_font = load_font(s(26), True)
    badge_font = load_font(s(40), True)
    badge_city_font = fit_font(draw, "TEXAS", s(302), s(54), s(38), True)

    draw.text((s(64), s(56)), "SAN ANTONIO", font=title_font, fill=ink)
    draw.text((s(66), s(136)), "ALAMO, RIVER WALK, ROCK 'N' ROLL", font=subtitle_font, fill=muted)

    draw.rounded_rectangle([s(760), s(64), s(1122), s(228)], radius=s(22), fill="#ffffff", outline=ink, width=s(7))
    draw.text((s(790), s(92)), "Run50 #14", font=badge_font, fill=ink)
    draw.text((s(790), s(144)), "TEXAS", font=badge_city_font, fill=blue)

    # River Walk bands.
    draw.polygon([(s(0), s(505)), (s(160), s(468)), (s(350), s(490)), (s(520), s(458)), (s(760), s(485)), (s(1200), s(438)), (s(1200), s(630)), (s(0), s(630))], fill="#b8d0c3")
    draw.polygon([(s(0), s(550)), (s(170), s(522)), (s(355), s(540)), (s(590), s(515)), (s(790), s(545)), (s(1200), s(498)), (s(1200), s(630)), (s(0), s(630))], fill="#7aa782")
    draw.polygon([(s(0), s(590)), (s(230), s(555)), (s(470), s(578)), (s(710), s(548)), (s(1200), s(582)), (s(1200), s(630)), (s(0), s(630))], fill=river)
    draw.line([(s(20), s(580)), (s(230), s(546)), (s(470), s(568)), (s(710), s(538)), (s(1180), s(570))], fill="#ffffff", width=s(5))

    # River Walk bridge and boat details.
    draw.arc([s(360), s(492), s(560), s(660)], 195, 345, fill="#f7efe1", width=s(10))
    draw.line([(s(380), s(552)), (s(540), s(532))], fill="#f7efe1", width=s(5))
    draw.rounded_rectangle([s(720), s(518), s(835), s(548)], radius=s(10), fill="#f7efe1", outline=ink, width=s(3))
    draw.rectangle([s(742), s(495), s(812), s(522)], fill="#0b67c2")
    draw.line([(s(752), s(505)), (s(802), s(505))], fill="#ffffff", width=s(3))
    draw.ellipse([s(702), s(532), s(722), s(552)], fill=gold, outline=ink, width=s(2))

    # Alamo facade.
    draw.rectangle([s(95), s(392), s(360), s(552)], fill=clay)
    draw.rectangle([s(72), s(360), s(384), s(402)], fill="#8d2f26")
    draw.rectangle([s(115), s(312), s(190), s(360)], fill=clay)
    draw.rectangle([s(266), s(312), s(340), s(360)], fill=clay)
    draw.rectangle([s(132), s(430), s(175), s(552)], fill="#f7efe1")
    draw.rectangle([s(282), s(430), s(322), s(552)], fill="#f7efe1")
    draw.arc([s(198), s(410), s(266), s(548)], 180, 360, fill="#f7efe1", width=s(16))
    draw.rectangle([s(206), s(478), s(258), s(552)], fill="#f7efe1")
    draw.rectangle([s(115), s(312), s(190), s(344)], fill=tan)
    draw.rectangle([s(266), s(312), s(340), s(344)], fill=tan)
    draw.arc([s(100), s(330), s(360), s(455)], 180, 360, fill="#f7efe1", width=s(6))
    draw.line([(s(95), s(392)), (s(360), s(392))], fill="#f7efe1", width=s(4))

    # Tower of the Americas.
    draw.rectangle([s(612), s(330), s(632), s(552)], fill="#a05a25")
    draw.ellipse([s(575), s(280), s(670), s(375)], fill=gold, outline="#a05a25", width=s(6))
    draw.line([s(622), s(250), s(622), s(300)], fill="#a05a25", width=s(8))
    draw.line([s(580), s(326), s(668), s(326)], fill="#a05a25", width=s(6))
    draw.line([s(602), s(374), s(602), s(552)], fill="#7c3f18", width=s(4))
    draw.line([s(642), s(374), s(642), s(552)], fill="#7c3f18", width=s(4))

    # Rock music guitar.
    draw.ellipse([s(850), s(416), s(980), s(546)], fill="#f6c86a", outline=ink, width=s(7))
    draw.ellipse([s(890), s(456), s(940), s(506)], fill="#ffffff", outline=ink, width=s(4))
    draw.polygon([(s(956), s(430)), (s(1075), s(340)), (s(1098), s(366)), (s(986), s(466))], fill="#8d2f26", outline=ink)
    draw.line([(s(970), s(446)), (s(1085), s(354))], fill=ink, width=s(4))
    draw.line([(s(980), s(456)), (s(1094), s(363))], fill=ink, width=s(3))

    # Lone star sun.
    cx, cy, r1, r2 = s(1040), s(292), s(52), s(22)
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        r = r1 if i % 2 == 0 else r2
        pts.append((cx + int(math.cos(ang) * r), cy + int(math.sin(ang) * r)))
    draw.polygon(pts, fill="#ffffff", outline=blue)


def write_png():
    im = Image.new("RGB", (1200, 630), "#edf3f7")
    draw = ImageDraw.Draw(im)
    draw_cover(draw, 1.0)
    im.save(OG_PATH)


def write_svg():
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 750" role="img" aria-label="San Antonio Texas icon cover">
  <rect width="1200" height="750" fill="#edf3f7"/>
  <text x="70" y="104" font-family="Arial, Helvetica, sans-serif" font-size="66" font-weight="900" fill="#20242b">SAN ANTONIO</text>
  <text x="72" y="150" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="800" fill="#667085">ALAMO, RIVER WALK, ROCK 'N' ROLL</text>
  <rect x="758" y="62" width="364" height="166" rx="22" fill="#ffffff" stroke="#20242b" stroke-width="8"/>
  <text x="790" y="122" font-family="Arial, Helvetica, sans-serif" font-size="41" font-weight="900" fill="#20242b">Run50 #14</text>
  <text x="790" y="182" font-family="Arial, Helvetica, sans-serif" font-size="52" font-weight="900" fill="#0b67c2">TEXAS</text>
  <path d="M0 590 C160 552 350 578 520 545 C760 583 930 515 1200 495 L1200 750 L0 750 Z" fill="#b8d0c3"/>
  <path d="M0 650 C170 620 355 645 590 610 C790 645 1000 590 1200 575 L1200 750 L0 750 Z" fill="#7aa782"/>
  <path d="M0 710 C230 670 470 705 710 668 C895 640 1045 675 1200 695 L1200 750 L0 750 Z" fill="#2f8fa3"/>
  <path d="M20 698 C230 658 470 693 710 656 C895 628 1045 663 1180 683" fill="none" stroke="#ffffff" stroke-width="6"/>
  <path d="M370 662 A105 86 0 0 1 558 640" fill="none" stroke="#f7efe1" stroke-width="12" stroke-linecap="round"/>
  <path d="M386 658 L542 638" stroke="#f7efe1" stroke-width="6" stroke-linecap="round"/>
  <rect x="720" y="618" width="116" height="34" rx="10" fill="#f7efe1" stroke="#20242b" stroke-width="4"/>
  <rect x="744" y="592" width="68" height="30" fill="#0b67c2"/>
  <line x1="754" y1="604" x2="802" y2="604" stroke="#ffffff" stroke-width="4"/>
  <circle cx="712" cy="642" r="12" fill="#f5b32f" stroke="#20242b" stroke-width="3"/>
  <rect x="95" y="470" width="265" height="168" fill="#ba4a2b"/>
  <rect x="72" y="432" width="312" height="46" fill="#8d2f26"/>
  <rect x="115" y="372" width="75" height="60" fill="#ba4a2b"/>
  <rect x="266" y="372" width="74" height="60" fill="#ba4a2b"/>
  <rect x="132" y="512" width="43" height="126" fill="#f7efe1"/>
  <rect x="282" y="512" width="40" height="126" fill="#f7efe1"/>
  <path d="M206 638 V552 A34 70 0 0 1 258 552 V638" fill="#f7efe1"/>
  <path d="M103 470 A132 70 0 0 1 357 470" fill="none" stroke="#f7efe1" stroke-width="7"/>
  <line x1="96" y1="470" x2="360" y2="470" stroke="#f7efe1" stroke-width="5"/>
  <rect x="612" y="400" width="20" height="238" fill="#a05a25"/>
  <circle cx="622" cy="350" r="47" fill="#f5b32f" stroke="#a05a25" stroke-width="6"/>
  <line x1="622" y1="305" x2="622" y2="245" stroke="#a05a25" stroke-width="8"/>
  <line x1="580" y1="350" x2="668" y2="350" stroke="#a05a25" stroke-width="6"/>
  <line x1="602" y1="398" x2="602" y2="638" stroke="#7c3f18" stroke-width="5"/>
  <line x1="642" y1="398" x2="642" y2="638" stroke="#7c3f18" stroke-width="5"/>
  <ellipse cx="915" cy="548" rx="70" ry="66" fill="#f6c86a" stroke="#20242b" stroke-width="8"/>
  <circle cx="915" cy="548" r="26" fill="#ffffff" stroke="#20242b" stroke-width="4"/>
  <path d="M958 505 L1075 410 L1100 438 L988 540 Z" fill="#8d2f26" stroke="#20242b" stroke-width="5"/>
  <polygon points="1040,285 1055,327 1100,327 1064,353 1078,396 1040,371 1002,396 1016,353 980,327 1025,327" fill="#ffffff" stroke="#0b67c2" stroke-width="6"/>
</svg>'''
    write_clean(THUMB_PATH, svg)


def update_file(path: Path, updater):
    text = path.read_text(encoding="utf-8")
    new = updater(text)
    if new != text:
        path.write_text(new, encoding="utf-8")


def update_indexes():
    thumb = f"../../../assets/thumb-run50-san-antonio-marathon-icons.svg?v={VERSION}"
    root_thumb = f"assets/thumb-run50-san-antonio-marathon-icons.svg?v={VERSION}"

    zh_card = f'''      <a class="story-card run-50" href="./san-antonio-marathon.html">
        <img src="{thumb}" alt="圣安东尼奥摇滚马拉松城市图标封面" loading="lazy" decoding="async">
        <div class="story-copy">
          <p class="story-meta">德克萨斯圣安东尼奥 · 2023.12.03</p>
          <h2 class="story-title">Run50 #第14州｜圣安东尼奥摇滚马拉松</h2>
          <p class="story-desc">因为马刺和文班亚马来到圣安东尼奥，结果球没看成，却跑完了2023收官马。阿拉莫、River Walk、Fort Sam Houston、墨西哥风情和4小时12分的德州热坡。</p>
          <div class="story-foot">
            <span>长文图记</span>
            <span>阅读 →</span>
          </div>
        </div>
      </a>
'''
    en_card = f'''      <a class="story-card run-50" href="./san-antonio-marathon.html">
        <img src="{thumb}" alt="Icon cover for San Antonio Marathon" />
        <div class="story-card-content">
          <div class="meta">Texas · San Antonio · 2023.12.03</div>
          <h2>San Antonio Rock 'n' Roll Marathon: the Spurs trip that became State 14</h2>
          <p>A Spurs-inspired Texas weekend with the Alamo, River Walk, Fort Sam Houston, live bands, a late hill, and a 4:12 finish to close out 2023.</p>
        </div>
      </a>
'''
    fb_card = f'''    <a class="story-card run-50" href="./san-antonio-marathon.html">
      <div>
        <p class="eyebrow">World / USA / Marathon</p>
        <h2>San Antonio turned a Spurs trip into my Texas marathon story</h2>
        <p>Race date: December 3, 2023. State 14 of Run50, from the Alamo and River Walk to Fort Sam Houston, greenway miles, one late Texas hill and a 4:12 finish.</p>
        <div class="meta">
          <span>San Antonio, Texas</span>
          <span>4:12 finish</span>
          <span>Run50 Facebook</span>
        </div>
      </div>
      <img src="../../assets/thumb-run50-san-antonio-marathon-icons.svg?v={VERSION}" alt="Icon-style San Antonio Marathon cover">
    </a>
'''

    def insert_before_miami(text, card):
        if "san-antonio-marathon.html" in text:
            return text
        marker = '      <a class="story-card run-50" href="./miami-marathon.html">'
        if marker not in text:
            raise RuntimeError("Could not find Miami card marker")
        return text.replace(marker, card + marker, 1)

    update_file(REPO / "run50" / "stories" / "chinese" / "index.html", lambda t: insert_before_miami(t, zh_card))
    update_file(REPO / "run50" / "stories" / "english" / "index.html", lambda t: insert_before_miami(t, en_card))

    def update_fb_index(text):
        if "san-antonio-marathon.html" in text:
            return text
        marker = '    <a class="story-card run-50" href="./miami-marathon.html">'
        if marker not in text:
            raise RuntimeError("Could not find Facebook Miami card marker")
        return text.replace(marker, fb_card + marker, 1)

    update_file(REPO / "run50" / "facebook" / "index.html", update_fb_index)

    def update_run50_index(text):
        return text.replace("6 stories", "7 stories")

    update_file(REPO / "run50" / "index.html", update_run50_index)

    def update_root(text):
        text = text.replace(
            'data-title="Run50 Chinese Stories Xiangyang Guilin Hong Kong Pisa Marathon"',
            'data-title="Run50 Chinese Stories Xiangyang Guilin Hong Kong Pisa Texas San Antonio Marathon"',
        )
        text = text.replace(
            'data-title="Run50 English Stories Xiangyang Guilin Hong Kong Pisa Marathon"',
            'data-title="Run50 English Stories Xiangyang Guilin Hong Kong Pisa Texas San Antonio Marathon"',
        )
        text = text.replace(
            'data-title="Run50 Facebook Xiangyang Guilin Hong Kong Pisa Marathon"',
            'data-title="Run50 Facebook Xiangyang Guilin Hong Kong Pisa Texas San Antonio Marathon"',
        )
        text = text.replace('assets/thumb-run50-guilin-icons.svg?v=20260604-8" alt="Run50 Chinese Stories Guilin cover"', f'{root_thumb}" alt="Run50 Chinese Stories San Antonio cover"')
        text = text.replace('assets/thumb-run50-hong-kong-icons.svg?v=20260604-8" alt="Run50 English Stories Hong Kong cover"', f'{root_thumb}" alt="Run50 English Stories San Antonio cover"')
        text = text.replace('assets/thumb-run50-miami-icons.svg?v=20260605-1" alt="Run50 Facebook Miami cover"', f'{root_thumb}" alt="Run50 Facebook San Antonio cover"')
        text = text.replace("Run50 &middot; Xiangyang + Guilin + Hong Kong + Pisa", "Run50 &middot; Texas + Xiangyang + Guilin + more")
        return text

    update_file(REPO / "index.html", update_root)

    keys = [
        "run50-san-antonio-marathon-facebook-en",
        "run50-san-antonio-marathon-en",
        "run50-san-antonio-marathon-zh",
    ]

    def update_sql(text):
        if keys[0] in text:
            return text
        insert = "\n      " + ",\n      ".join(f"'{key}'" for key in keys) + ","
        return text.replace("'run50-south-carolina-marathon-zh',", "'run50-south-carolina-marathon-zh'," + insert)

    update_file(REPO / "supabase" / "run50-comments.sql", update_sql)


def main():
    indexed = extract_story()
    image_count = copy_story_images(indexed)
    sections = split_sections(indexed)

    chinese_article = render_chinese_article(indexed)
    english_article = render_english_article(indexed)
    fb_article = render_facebook_article(sections)

    write_clean(REPO / "run50" / "stories" / "chinese" / "san-antonio-marathon.html", story_page("zh", chinese_article))
    write_clean(REPO / "run50" / "stories" / "english" / "san-antonio-marathon.html", story_page("en", english_article))
    write_clean(REPO / "run50" / "facebook" / "san-antonio-marathon.html", facebook_page(fb_article))
    write_png()
    write_svg()
    update_indexes()
    print(f"built Texas story: events={len(indexed)} images={image_count}")


if __name__ == "__main__":
    main()
