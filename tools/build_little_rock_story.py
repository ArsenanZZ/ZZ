from pathlib import Path
from lxml import html
from html import escape
from PIL import Image, ImageDraw, ImageFont, ImageOps
import re

REPO = Path(__file__).resolve().parents[1]
SOURCE_BASE = Path(r"Z:\ZhennanZ Folder\000-Marathon-Story-2024-2025\20240303-AR-Little Rock Marathon\0000-Web")
SOURCE_HTML = next(p for p in SOURCE_BASE.iterdir() if p.suffix.lower() == ".html")
SOURCE_FILES = next(p for p in SOURCE_BASE.iterdir() if p.is_dir() and p.name.endswith("_files"))
SITE = "https://arsenanzz.github.io/ZZ"
SLUG = "little-rock-marathon"
VERSION = "20260605-1"
OUT_IMG_DIR = REPO / "run50" / "stories" / "chinese" / "Run50-Little-Rock-Marathon-clean_files"

EN_BY_INDEX = {
    0: "Arkansas",
    2: "Run50 #17 U.S. State Marathon",
    3: "Location: Little Rock, Arkansas",
    4: "Race: Little Rock Marathon",
    5: "Preface",
    6: "# Out of deep winter, into spring: running toward the middle of the map",
    7: "By early March, the weather was finally starting to warm up. I had just locked in my internship offer, and my mind was feeling a bit lighter.",
    8: "This marathon was actually planned long ago, registered together with the Oak Island run. One was on the North Carolina coast, the other in Little Rock, the capital of Arkansas.",
    9: "I chose Little Rock entirely for the massive medal. This year's design featured a menacing dinosaur with a heavy metallic feel — I have absolutely no resistance when it comes to cool stuff like this.",
    12: "Starting from Kentucky, we drove all the way south. The route took us through Tennessee, then Mississippi, and finally into Arkansas. The most immediate feeling along the way was not the scenery changing, but the highway quality.",
    13: "The highways in Tennessee are fantastic — wide lanes, clear markings, solid road feel, and high speed limits. Driving there was incredibly smooth.",
    16: "But the moment we crossed into Mississippi, the road started rattling, as if to remind you not to get too ahead of yourself.",
    17: "Once in Arkansas, the road bumps practically shouted \"Welcome to the South\" with potholed asphalt, faded lane lines, and heavy truck traffic that made the narrow lanes feel even tighter.",
    18: "But the sun was wonderful. Spring in the South was free from damp cold; outside the car window was a soft golden glow, and the breeze was calm.",
    19: "Though the road quality was questionable, we were in good spirits. We successfully arrived in Little Rock, the home of President Clinton and the 17th state of my 50-state marathon quest.",
    23: "# State 17: Arkansas | A presidential home and a quiet running destination",
    24: "🦖 Little Rock, AR",
    25: "Arkansas sits in the south-central United States. While not completely isolated, it's certainly not a major tourist destination.",
    26: "Its capital, Little Rock, is small but has some fame — after all, it's the home of President Bill Clinton.",
    29: "Built along the Arkansas River and surrounded by hills and forests, the city has its share of ups and downs. Walking around, you realize it's a bit quiet — not bustling, yet not entirely desolate. There just aren't many people.",
    32: "But apparently, dogs are everywhere, to the point of being a bit overwhelming. I'd call it the \"few people, many dogs\" state. It's not necessarily good or bad, but it gives the place a distinct Southern vibe.",
    33: "Arkansas indeed has a quiet profile, but it has its own character:",
    34: "It's one of the most naturally rich states in the U.S., with plenty of mountains, lakes, and state parks;",
    35: "It serves as a key logistics corridor, with the headquarters of J.B. Hunt, the largest trucking company in the U.S., located nearby;",
    36: "It has witnessed major historical events, such as the 1957 Little Rock Crisis when federal troops were sent in to desegregate the high school.",
    37: "Running a marathon in this city leaves you with a quiet, unique, and slightly gritty memory of the American South.",
    39: "# Arriving in Little Rock: stepping into spring",
    40: "🦖 Little Rock, AR",
    41: "We arrived in Little Rock just after 3 p.m. The sun was bright, the city was quiet, and the air already carried a hint of spring.",
    46: "We originally planned to go straight downtown for packet pickup. But driving past a white-domed building, we were captivated by a pink magnolia tree in full bloom, with sunlight filtering through the branches as if spotlighting the structure.",
    49: "We got out of the car immediately. This was the Arkansas State Capitol, one of Little Rock's most iconic landmarks. Built to resemble a miniature U.S. Capitol, the white marble structure with its grand dome looks exactly like a state capital should.",
    54: "The trees in front of the Capitol were blooming beautifully — likely saucer magnolias. The massive pink blossoms hanging from the branches under the sunlight made for perfect pictures.",
    57: "So we started shooting, posing in front of the flowers, framing them against the building, and taking endless selfies. It felt like we were doing a wedding shoot for the Capitol.",
    58: "# Packet Pickup | A dinosaur playground on Main Street",
    59: "After taking enough photos, we drove on to the city center for packet pickup.",
    60: "The pickup location was near Main Street downtown, set up in a convention hall and parking garage combo. When we arrived, balloons were hanging at the entrance, and the parking structure featured a massive, colorful mural spelling out \"MAIN STREET.\"",
    65: "Stepping inside felt like walking into a cartoon theme park, complete with balloon arches, dinosaur figures, colorful flags, and cartoon backdrops.",
    66: "The Little Rock Marathon is famous for its massive, quirky medals. This year's theme was \"Runosaurs,\" and the medals, shirts, and mascots were entirely dinosaur-themed.",
    71: "# City Stroll | Rivers, bridges, a submarine, and a selfie sign",
    72: "With packet pickup done and plenty of time left, we went for a stroll along the riverfront.",
    73: "The Arkansas River, a major tributary of the Mississippi, flows right through Little Rock, serving as the city's geographical center line.",
    80: "Several bridges span the river, from modern expressways to historic railway crossings.",
    81: "One bridge caught our attention with its hybrid look — half modern, half rusted, looking like two different eras spliced together.",
    82: "It turns out this is Junction Bridge. Originally a railway bridge, it was later retired, and a section was converted into a pedestrian skyway that is now a popular scenic spot.",
    89: "Looking back from the bridge, the sunset painted the city in gold. With the skyline in the distance and light reflecting off the water, Little Rock looked surprisingly majestic — very different from the \"dilapidated and chaotic\" rumors.",
    94: "Even more surprising, a decommissioned submarine (USS Razorback, SS-394) was docked along the shore. Now a naval museum, it allows visitors to climb aboard and tour the decks.",
    95: "Half-submerged and bathed in the sunset glow, its weathered iron hull looked like a physical piece of history.",
    102: "Walking further along the bank, we spotted a large photo-op sign that read:",
    103: "“I’M BIG ON LITTLE ROCK”",
    104: "We couldn't resist striking a few poses and snapping some selfies with the bridge and the fading sky behind us.",
    105: "A quick flight with the Hover X1 pocket drone, and we had some great aerial shots.",
    106: "Little Rock wasn't as quiet as we had imagined. Its charm is something you discover only when you slow down and explore.",
    110: "# Race Day | Running through Clinton's hometown at dawn",
    111: "🦖 Little Rock, AR",
    112: "Race Morning: The Start Line Under the Spotlights",
    113: "Before dawn, we drove ten minutes to the River Market Pavilion, the start area for the Little Rock Marathon.",
    114: "The full marathon was scheduled to start at 6 a.m. When we arrived, the sky was pitch black, but the starting corral was brilliantly lit by floodlights, buzzing with energy.",
    119: "Before I could even process it, the full marathon pack was off. Adjusting my gear on the run, I quietly blended into the crowd and started jogging forward.",
    122: "Starting near the River Market, the course wound through the downtown streets before crossing the Clinton Presidential Park Bridge over the Arkansas River.",
    125: "Next, it entered North Little Rock on the other side of the river, looped through the east bank, and crossed back over the bridge to the main city.",
    126: "From there, the route pushed west through green parks, residential neighborhoods, and rolling hills, before finishing at the War Memorial Stadium on the city's west side.",
    127: "The elevation changes weren't too severe — just a couple of hills in the second half — making for a solid course overall.",
    128: "Running in the dark at the start, I was wearing a retro deep-red Arsenal jersey, which clashed with the neon streetlights to give off a distinct \"nightclub runner\" vibe.",
    133: "The passing police cruisers flashed their blue lights, throwing a neon-blue glow over my face. It looked like a low-budget AAA video game effect — as if I was about to release my Avatar and awaken my blue face. I almost stopped to strike a dramatic pose.",
    138: "Running in the dark, we hit the bridge around Mile 1. The dim yellow streetlights felt like a vintage film filter, framing my retro red Arsenal shirt like a late-night training session in North London.",
    139: "The other side of the bridge led into North Little Rock, the city's northern suburb.",
    140: "Coming off the bridge, the course threaded through tree-lined streets in North Little Rock.",
    141: "The white-flowered trees along the road were in full bloom, looking like rows of exploding cotton candy.",
    144: "Just then, a runner in a purple-and-gold Lakers #24 jersey appeared ahead, shining bright in the morning mist.",
    145: "With a golden headwrap, his silhouette carried a strong \"Mamba Mentality.\" From behind, it looked like Kobe Bryant out for a dawn practice session.",
    146: "For a second, I felt like I was in that famous 4 a.m. Los Angeles dawn.",
    147: "But this was 6:30 a.m. in Little Rock. Kobe is gone, but the Mamba spirit he left behind continues to march forward under the feet of runners.",
    148: "I ran behind him for a few hundred meters, feeling the quiet pull of that legacy. Respect!",
    149: "By Mile 3, we doubled back across the bridge as the horizon began to brighten.",
    150: "It was like a movie transitioning from black-and-white to full color.",
    151: "A headwind blew off the river, not too strong, but enough to slap me awake from my morning haze.",
    154: "I sped up slightly and passed a runner wearing a Hawaiian shirt over a purple singlet — not sure if he was here for a marathon or a tropical vacation, but it felt classic for Little Rock.",
    155: "Heading back into downtown, the streets had a clean, \"faded elegance\" to them. The buildings weren't new, but the streetscape felt wonderfully historic.",
    156: "Spring flowers were popping up — clusters of yellow and pink blossoms smiling along the curbs, which was a nice boost.",
    161: "The weather was a perfect overcast gray — cool, not cold, with the sun hidden, making for comfortable running conditions.",
    162: "After Mile 5, the route branched west, leaving the downtown core behind to weave through parks and residential areas.",
    163: "Around Mile 6, the half and full marathon courses split.",
    164: "The full marathoners headed toward the airport, looping around a landmark display plane in front of the Dassault Falcon Jet facility.",
    169: "Yes, that Dassault. The French aerospace giant is famous for business jets and fighter planes (like the Rafale), as well as engineering software like CATIA and ABAQUS. Passing their corporate offices was a cool highlight.",
    170: "Kids lined the curbs at the aid stations, handing out gels and cheering wildly: \"You got this! Let's goooo!\"",
    175: "Coming back from the loop, we merged with the half-marathoners again around Mile 7, though I couldn't spot Siqi in the crowd.",
    176: "Along the way, I saw a grandmother wearing a \"50 States\" shirt with a colorful map of the U.S. on her back, most of the states checked off.",
    181: "At Mile 8, a guy wearing a wig rode a red inflatable T-Rex by the curb, cheering us on. I wasn't sure if he was an official volunteer, but I'd give that outfit a perfect score.",
    186: "Running along, a man ahead of me had a blue shirt that read:",
    187: "“I RUN SO I CAN EAT.”",
    188: "I beg to differ — running hasn't made me lose any weight, probably because I take the eating part a little too seriously.",
    189: "After some rolling hills downtown, the Arkansas Museum of Fine Arts appeared — a sleek white modern structure set against a sandy grass lawn.",
    190: "Reopened in 2023 after a major renovation, the museum is a local cultural hub featuring American modern art, contemporary pottery, and a sculpture garden.",
    197: "At Mile 9, the aid station style shifted completely into a dinosaur theme.",
    204: "Giant pterodactyl models hung from the trees, and a volunteer was dressed as a purple-and-orange dragon. It was awesome.",
    205: "Leaving the dinosaur station behind, the course entered a very residential, lived-in part of town.",
    206: "This stretch wound through a humbler neighborhood, with weathered brick houses, chipped pickup trucks, and a faded \"57\" painted on a wall.",
    211: "The houses were simple, some windows boarded up, and rusted trucks parked in front yards.",
    212: "It wasn't a tourist zone or a commercial hub, but it was raw and real — a true glimpse of the city's other side.",
    215: "There weren't many spectators here, save for a few locals sitting on porches shouting encouragement.",
    216: "Approaching Mile 14, the white dome of the Arkansas State Capitol finally came back into view.",
    217: "Seeing photographers ahead, I quickly adjusted my hair and tried to look as smooth as possible passing by.",
    226: "The Mile 15 station kept the dinosaur theme going, featuring a massive inflatable T-Rex waving by the road while kids screamed \"Gatorade! Water!\"",
    233: "But my brain had only one word on repeat: hills.",
    234: "From here on, the hills were relentless — one roller after another. Not steep, but they wore you down, pulling you upward like an invisible string.",
    239: "Past Mile 16, the course quietly shifted tone. The urban noise faded, the crowds thinned, and all that remained was my breathing and the rhythm of shoes hitting the asphalt as I ran into a quiet forest.",
    242: "This was Allsopp Park, the city's wooded green lung, featuring winding paths under thick trees.",
    243: "By Mile 18, a peaceful, zen-like mood took over. Fewer runners, softer light, and a quiet mind.",
    246: "Just before Mile 19, I saw a row of grey sculptures that looked like they were practicing tai chi or martial arts, one frozen mid-punch. Next to them stood the sleek white building of the Arkansas Regional Innovation Hub.",
    253: "Exiting the park, the course wound past small bridges, warehouses, and industrial blocks. The trees receded, and the city took back the stage.",
    254: "By Mile 21, we rejoined the main roads, entering familiar Little Rock neighborhoods.",
    255: "The spectators returned in full force, and the energy was electric.",
    262: "From Miles 22 to 25, the historic red brick buildings and blooming wayside flowers gave the city a retro Southern feel — a warm, down-home welcome.",
    263: "My legs were heavy, but my spirit was light, knowing the finish was just around the corner.",
    264: "In the final mile, I saw a classic American roadside fixture: an older gentleman waving a giant U.S. flag, wearing a tall Uncle Sam hat and full red-white-and-blue gear, cheering us on with old-school patriotism.",
    271: "A light rain started to fall as I crossed the line. Finish time: 3 hours and 51 minutes!",
    272: "Almost identical to my time at Oak Island. Considering the rolling hills in the second half of Little Rock, this run was a major win.",
    281: "After crossing, I headed inside the Little Rock Convention Center to claim the legendary, massive dinosaur medal. It was incredibly heavy!",
    282: "This year's medal was a giant green T-Rex, beautifully crafted with a heavy metallic weight. The dinosaur's gaping jaws and fierce eyes looked like they were roaring in celebration of my finish.",
    287: "After securing the medal, professional photographers were waiting. I struck a few poses and got some great commemorative photos.",
    288: "By this time, Siqi had finished her race and was already resting.",
    291: "The indoor post-race area was huge and warm. Stepping in from the cold wind and rain felt like entering heaven.",
    292: "We sat down with a table of fellow runners, eating, drinking, and doing some much-needed stretching.",
    297: "After stretching, Siqi and I took a photo together in front of the finisher backdrop.",
    298: "Near the exit stood a striking Asian-style gate that read \"Songahm Gate.\"",
    299: "This gate commemorates Eternal Grand Master H.U. Lee, founder of the American Taekwondo Association (ATA). It was donated by his family, and Little Rock is actually home to the ATA world headquarters.",
    304: "Before leaving the venue, we used the pocket drone to take a photo in front of a rainbow mural in the parking lot — a routine that felt exactly like our finish at Oak Island.",
    309: "Postscript",
    310: "# After the Run | Leaving Arkansas with two medals",
    311: "After the race, we drove back to Louisville in high spirits.",
    312: "On the highway, it was the same familiar sight: endless convoys of massive trucks, like mechanical beasts roaring down the lanes.",
    315: "But this time was different. We had a massive green T-Rex medal sitting in the car like a heavy metal talisman, giving us a quiet sense of accomplishment.",
    316: "I joked that Little Rock was a place of \"few people and many dogs,\" but that was just banter. The crowd support was warm and the volunteers were lovely.",
    317: "Even with the gray sky and light rain, the smiles along the course were bright. As for the dogs — I actually didn't see a single one.",
    320: "This trip gave us a fresh perspective on Little Rock. Arkansas's capital may be small, but it hides some wonderful spots:",
    321: "The Arkansas State Capitol, with its movie-like white marble dome;",
    322: "Allsopp Park, wrapped in a peaceful, zen-like forest;",
    323: "The culturally rich Arkansas Museum of Fine Arts and the Innovation Hub;",
    324: "And most of all, the dinosaurs, the sculptures, the kids, and the flag-waving grandfathers that made this simple Southern race so memorable.",
    325: "State 17, Arkansas: Little Rock Marathon. Checked in, done.",
    326: "- End -",
    327: "Words | Arsenan",
    328: "Photos | Arsenan",
    329: "Design | Arsenan",
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
        "Run50#17 AR Vlog @Arsenan": "Run50 #17 AR Vlog @Arsenan",
        "Little Rock Marathon @Siqi": "Little Rock Marathon @Siqi",
        "State 17-Arkansas @Arsenan": "State 17 - Arkansas @Arsenan",
        "Little Rock Marathon @Photographer": "Little Rock Marathon @Photographer",
        "Arkansas @Google": "Arkansas @Google",
        "Arkansas State Capitol @Arsenan": "Arkansas State Capitol @Arsenan",
        "Spring in bloom @Siqi": "Spring in bloom @Siqi",
        "Magnolia flowers @Arsenan": "Magnolia flowers @Arsenan",
        "Downtown Little Rock @Arsenan": "Downtown Little Rock @Arsenan",
        "Expo @Siqi": "Expo @Siqi",
        "Expo @Volunteer": "Expo @Volunteer",
        "Junction Bridge @Arsenan": "Junction Bridge @Arsenan",
        "Arkansas River @Arsenan": "Arkansas River @Arsenan",
        "Miami Bus @DJI Mini 4": "Arkansas River @DJI Mini 4",
        "I'm big on Little Rock @Hover X1": "I'm big on Little Rock @Hover X1",
        "Marathon Start @Arsenan": "Marathon Start @Arsenan",
        "Marathon Start @Photographer": "Marathon Start @Photographer",
        "Marathon Course @Arsenan": "Marathon Course @Arsenan",
        "Running in LR Downtown @Arsenan": "Running in LR Downtown @Arsenan",
        "Running in LR Downtown @Photographer": "Running in LR Downtown @Photographer",
        "Chasing the Mamba Spirit At Dawn @Arsenan": "Chasing the Mamba Spirit At Dawn @Arsenan",
        "Back to Downtown @Arsenan": "Back to Downtown @Arsenan",
        "Mile-5 @Arsenan": "Mile 5 @Arsenan",
        "7：00 Pacer @Arsenan": "7:00 Pacer @Arsenan",
        "Mile-6 @Arsenan": "Mile 6 @Arsenan",
        "Dassault @Arsenan": "Dassault @Arsenan",
        "You got this @Arsenan": "You got this @Arsenan",
        "Mile-7 @Arsenan": "Mile 7 @Arsenan",
        "Turn About1 @Arsenan": "Turn Around @Arsenan",
        "50 States @Arsenan": "50 States @Arsenan",
        "Mile-8 @Arsenan": "Mile 8 @Arsenan",
        "I RUN SO I CAN EAT @Arsenan": "I RUN SO I CAN EAT @Arsenan",
        "Mile-9 @Arsenan": "Mile 9 @Arsenan",
        "Arkansas Museum of Fine Arts @Arsenan": "Arkansas Museum of Fine Arts @Arsenan",
        "Miami Bus @Arsenan": "Aid Station @Arsenan",
        "Dragon-Powered Aid Station @Arsenan": "Dragon-Powered Aid Station @Arsenan",
        "Through a Rougher Neighborhood @Arsenan": "Through a Rougher Neighborhood @Arsenan",
        "Towards Arkansas State Capitol @Arsenan": "Towards Arkansas State Capitol @Arsenan",
        "Arkansas State Capitol @Photographer": "Arkansas State Capitol @Photographer",
        "Mile-15 @Arsenan": "Mile 15 @Arsenan",
        "Allsopp Park @Arsenan": "Allsopp Park @Arsenan",
        "Allsopp Park @Photographer": "Allsopp Park @Photographer",
        "Mile-18 @Arsenan": "Mile 18 @Arsenan",
        "Mile-19 @Arsenan": "Mile 19 @Arsenan",
        "Mile-20 @Arsenan": "Mile 20 @Arsenan",
        "Towards Finish @Arsenan": "Towards Finish @Arsenan",
        "Mile-25 @Arsenan": "Mile 25 @Arsenan",
        "Mile 25.5 @Arsenan": "Mile 25.5 @Arsenan",
        "Old School Patriot @Arsenan": "Old School Patriot @Arsenan",
        "Final Mile, Powered by Cheers @Arsenan": "Final Mile, Powered by Cheers @Arsenan",
        "Final Mile, Powered by Cheers @Photographer": "Final Mile, Powered by Cheers @Photographer",
        "Finish @Arsenan": "Finish @Arsenan",
        "Finish @Photographer": "Finish @Photographer",
        "Medal Time @Arsenan": "Medal Time @Arsenan",
        "Big Medal Energy🦖 @Arsenan": "Big Medal Energy 🦖 @Arsenan",
        "State 17. Medal Secured @Photographer": "State 17. Medal Secured @Photographer",
        "Earned The Dinosaur @Arsenan": "Earned The Dinosaur @Arsenan",
        "Siqi @Arsenan": "Siqi @Arsenan",
        "Post-race Stretch Mode @Arsenan": "Post-race Stretch Mode @Arsenan",
        "We Made It @Spectator": "We Made It @Spectator",
        "Songahm Gate · Little Rock, AR @Arsenan": "Songahm Gate · Little Rock, AR @Arsenan",
        "Medals on, Memories Made @Hover X1": "Medals on, Memories Made @Hover X1",
        "Medal Bigger than Face @Siqi": "Medal Bigger than Face @Siqi",
        "Medal Heavier than My Smile @Siqi": "Medal Heavier than My Smile @Siqi",
        "Back KY @Arsenan": "Driving Back to KY @Arsenan",
        "Home Road @Arsenan": "Home Road @Arsenan",
    }
    for old, new in replacements.items():
        caption = caption.replace(old, new)
    return caption


def text_for(idx: int, text: str, lang: str) -> str:
    if lang == "zh":
        if text == "装备领取｜一座“Main Street”的恐龙乐园":
            return "# 装备领取｜一座“Main Street”的恐龙乐园"
        if text == "城市漫步｜河、桥、潜水艇和一块自拍牌子":
            return "# 城市漫步｜河、桥、潜水艇和一块自拍牌子"
        if text == "比赛日早晨：灯光下的起跑仪式":
            return "## 比赛日早晨：灯光下的起跑仪式"
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
    if idx in (3, 4) or text.startswith(("📍", "🎽", "🦖")) or value.startswith("🦖"):
        return f'<p class="place">{escape(value)}</p>'
    if value.startswith("- "):
        return f'<p class="end-mark">{escape(value)}</p>'
    if idx in (327, 328, 329):
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
            alt = caption or ("Little Rock Marathon photo" if lang == "en" else "小石城马拉松照片")
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
    title = "Run50 #第17州｜阿肯色：小石城马拉松｜奖牌第一大，克林顿老家也没那么荒！" if is_zh else "Run50 #17 | Arkansas: Little Rock Marathon"
    short = "Run50 #17 | Little Rock Marathon"
    desc = (
        "三月初的小石城马拉松，为了那块巨大的绿色暴龙奖牌驱车向南。跑过市中心、达索公司和奥索普森林公园，冲线克林顿总统的故乡。"
        if is_zh
        else "Race date: March 3, 2024. Running U.S. State 17: Little Rock Marathon in Arkansas, from the State Capitol and the Arkansas River to Allsopp Park forest, with a giant green T-Rex finisher medal."
    )
    canonical = f"{SITE}/run50/stories/{'chinese' if is_zh else 'english'}/{SLUG}.html"
    other = f"../{'english' if is_zh else 'chinese'}/{SLUG}.html"
    fb = f"../../facebook/{SLUG}.html"
    nav = (
        f'<a href="./index.html">← 中文故事</a><a href="{other}">English</a><a href="{fb}">Facebook</a><a href="../../index.html">Run50</a>'
        if is_zh
        else f'<a href="./index.html">← English Stories</a><a href="{other}">中文</a><a href="{fb}">Facebook</a><a href="../../index.html">Run50</a>'
    )
    kicker = "Run50 #第17州 · 阿肯色" if is_zh else "Run50 #17 · Arkansas"
    footer = "© 2024-2026 ArsenanZZ. Built with love."
    locale = "zh-CN" if is_zh else "en"
    key = f"run50-{SLUG}-zh" if is_zh else f"run50-{SLUG}-en"
    mount = f"supabase-comments-little-rock-zh" if is_zh else f"supabase-comments-little-rock-en"
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
  <meta property="og:image:alt" content="Little Rock Marathon cover with State Capitol, Junction Bridge and T-Rex dinosaur.">
  <meta property="article:author" content="Arsenan">
  <meta property="article:published_time" content="2024-03-03T06:00:00-06:00">
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
      <span>Race: March 3, 2024</span>
      <a href="https://mp.weixin.qq.com/s/9_2_L_h1R0kYm2o-W_files" target="_blank" rel="noopener">Original WeChat &nearr;</a>
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
    title = "I ran Little Rock's marathon for the massive dinosaur medal, and the old South surprised me"
    desc = "Race date: March 3, 2024. Running U.S. State 17: Little Rock Marathon in Arkansas, featuring a giant green T-Rex medal, a dawn run over the Clinton Bridge, and a peaceful stroll along the Arkansas River."
    canonical = f"{SITE}/run50/facebook/{SLUG}.html"
    locale = "en"
    key = f"run50-{SLUG}-facebook-en"
    mount = f"supabase-comments-little-rock-facebook-en"
    og_image = f"{SITE}/assets/og-run50-{SLUG}-icons.png?v={VERSION}"
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Little Rock Marathon | Run50 Facebook</title>
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
  <meta property="og:image:alt" content="Little Rock Marathon cover with State Capitol, Junction Bridge and T-Rex dinosaur.">
  <meta property="article:author" content="Arsenan">
  <meta property="article:published_time" content="2024-03-03T06:00:00-06:00">
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
      <span>Race date: March 3, 2024</span>
    </div>
  </div>
  <header class="site-head">
    <div class="site-head-inner">
      <a class="wordmark" href="./index.html" aria-label="Run50 Facebook home">RUN50 WORLD</a>
      <nav class="section-nav" aria-label="Story navigation">
        <a href="../index.html">Run50</a>
        <a href="../stories/english/{SLUG}.html">Full English Story</a>
        <a href="../stories/chinese/{SLUG}.html">Chinese Original</a>
      </nav>
    </div>
  </header>
  <article class="article">
    <section class="hero">
      <span class="label">World / USA / Marathon</span>
      <h1>{escape(title)}</h1>
      <p class="dek">{escape(desc)}</p>
      <div class="byline">
        <span>By Arsenan</span>
        <span>Race: March 3, 2024</span>
        <span>Little Rock, AR</span>
        <span>Run50 #17</span>
      </div>
      <figure class="lead-media"><img src="../../assets/og-run50-{SLUG}-icons.png?v={VERSION}" alt="Icon-style Little Rock Marathon cover"><figcaption>Little Rock icon cover with the Arkansas State Capitol dome, Junction Bridge, and a T-Rex dinosaur silhouette.</figcaption></figure>
    </section>
    <section class="story-grid">
      <aside class="rail">
        <section class="brief-box"><h2>At a glance</h2><dl><div><dt>Race</dt><dd>Little Rock Marathon, Run50 State 17.</dd></div><div><dt>Course</dt><dd>Downtown Little Rock, Clinton Presidential Park Bridge, North Little Rock, Dassault Jet facility, and Allsopp Park forest trails.</dd></div><div><dt>What stayed with me</dt><dd>Giant green dinosaur medal, misty dawn over the Arkansas River, Mamba runner tribute, and rolling hills of Allsopp Park.</dd></div></dl></section>
        <section class="share-note"><strong>Notes</strong>Comments and page views are tracked below the story.</section>
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
<title id="title">Little Rock Marathon icon cover</title>
<desc id="desc">Icon style cover with Little Rock title, Run50 badge, Arkansas State Capitol dome, Junction Bridge, and dinosaur.</desc>
<rect width="1200" height="750" fill="#edf3f7"/>
<g transform="translate(70 104)">
  <text x="0" y="0" font-family="Arial, Helvetica, sans-serif" font-size="66" font-weight="900" fill="#20242b">LITTLE ROCK</text>
  <text x="0" y="46" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="700" fill="#0b67c2">CAPITOL · CLINTON · DINOSAUR</text>
</g>
<rect x="758" y="62" width="364" height="166" rx="22" fill="#ffffff" stroke="#20242b" stroke-width="8"/>
<text x="790" y="122" font-family="Arial, Helvetica, sans-serif" font-size="41" font-weight="900" fill="#20242b">Run50 #17</text>
<text x="790" y="182" font-family="Arial, Helvetica, sans-serif" font-size="52" font-weight="900" fill="#0b67c2">ARKANSAS</text>
<circle cx="1052" cy="352" r="62" fill="#fbbf24"/>
<path d="M0 612 C190 540 330 590 500 538 C690 480 830 590 1000 545 C1100 518 1168 515 1200 498 L1200 750 L0 750 Z" fill="#b0cddb"/>
<path d="M0 682 C180 620 370 705 560 650 C760 592 930 690 1200 620 L1200 750 L0 750 Z" fill="#84acc3"/>
<rect x="50" y="580" width="1100" height="16" fill="#334155"/>
<path d="M100 580 Q250 500 400 580" stroke="#334155" stroke-width="12" fill="none"/>
<path d="M400 580 Q550 500 700 580" stroke="#334155" stroke-width="12" fill="none"/>
<path d="M700 580 Q850 500 1000 580" stroke="#334155" stroke-width="12" fill="none"/>
<rect x="385" y="580" width="30" height="120" fill="#475569"/>
<rect x="685" y="580" width="30" height="120" fill="#475569"/>
<g>
  <rect x="150" y="440" width="180" height="140" fill="#cbd5e1" stroke="#334155" stroke-width="5"/>
  <line x1="180" y1="440" x2="180" y2="580" stroke="#475569" stroke-width="4"/>
  <line x1="210" y1="440" x2="210" y2="580" stroke="#475569" stroke-width="4"/>
  <line x1="240" y1="440" x2="240" y2="580" stroke="#475569" stroke-width="4"/>
  <line x1="270" y1="440" x2="270" y2="580" stroke="#475569" stroke-width="4"/>
  <line x1="300" y1="440" x2="300" y2="580" stroke="#475569" stroke-width="4"/>
  <rect x="180" y="380" width="120" height="60" fill="#cbd5e1" stroke="#334155" stroke-width="5"/>
  <line x1="200" y1="380" x2="200" y2="440" stroke="#475569" stroke-width="3"/>
  <line x1="220" y1="380" x2="220" y2="440" stroke="#475569" stroke-width="3"/>
  <line x1="240" y1="380" x2="240" y2="440" stroke="#475569" stroke-width="3"/>
  <line x1="260" y1="380" x2="260" y2="440" stroke="#475569" stroke-width="3"/>
  <line x1="280" y1="380" x2="280" y2="440" stroke="#475569" stroke-width="3"/>
  <path d="M195 380 C195 310 305 310 305 380 Z" fill="#94a3b8" stroke="#334155" stroke-width="5"/>
  <rect x="245" y="290" width="10" height="20" fill="#64748b"/>
  <line x1="250" y1="290" x2="250" y2="250" stroke="#334155" stroke-width="4"/>
</g>
<g>
  <path d="M880 580 L900 520 Q910 490 890 470 Q870 450 850 460 L830 470 L830 450 L860 430 Q880 410 910 420 L930 440 Q950 420 970 390 L980 400 Q970 420 950 450 L940 480 Q950 490 970 500 L990 495 Q1010 490 1030 510 L1060 540 Q1080 550 1110 560 L1120 580 L1080 580 Q1040 570 1010 550 L980 540 L960 580 Z" fill="#166534"/>
</g>
<path d="M0 702 C180 675 340 720 520 695 C720 668 900 720 1200 678 L1200 750 L0 750 Z" fill="#0f766e"/>
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
    image = Image.new("RGB", (1200, 630), "#edf3f7")
    draw = ImageDraw.Draw(image)
    text_color = "#20242b"
    blue = "#0b67c2"
    
    # Title
    draw.text((64, 64), "LITTLE ROCK", font=font(66, True), fill=text_color)
    
    # Badge Box
    draw.rounded_rectangle((760, 64, 1122, 228), radius=22, fill="#ffffff", outline=text_color, width=7)
    draw.text((790, 112), "Run50 #17", font=font(40, True), fill=text_color)
    draw.text((790, 166), "ARKANSAS", font=font(50, True), fill=blue)
    
    # Sun
    draw.ellipse((980, 260, 1078, 358), fill="#fbbf24")
    
    # Hills
    draw.polygon([(0, 515), (160, 455), (330, 520), (515, 465), (710, 420), (900, 510), (1080, 460), (1200, 438), (1200, 630), (0, 630)], fill="#b0cddb")
    draw.polygon([(0, 584), (190, 535), (380, 596), (560, 545), (770, 598), (980, 548), (1200, 516), (1200, 630), (0, 630)], fill="#84acc3")
    draw.rectangle((0, 592, 1200, 630), fill="#0f766e")
    
    # Bridge Truss & Piers
    draw.rectangle((50, 480, 1150, 493), fill="#334155")
    draw.rectangle((385, 490, 415, 592), fill="#475569")
    draw.rectangle((685, 490, 715, 592), fill="#475569")
    
    # Capitol Dome Left
    draw.rectangle((150, 370, 330, 490), fill="#cbd5e1", outline="#334155", width=4)
    for cx in range(180, 310, 30):
        draw.line((cx, 370, cx, 490), fill="#475569", width=3)
    draw.rectangle((180, 320, 300, 370), fill="#cbd5e1", outline="#334155", width=4)
    for cx in range(200, 290, 20):
        draw.line((cx, 320, cx, 370), fill="#475569", width=2)
    draw.ellipse((195, 260, 305, 370), fill="#94a3b8", outline="#334155", width=4)
    draw.rectangle((245, 240, 255, 260), fill="#64748b")
    draw.line((250, 240, 250, 210), fill="#334155", width=3)
    
    # Dinosaur T-Rex Right
    # Use simple shapes for dinosaur: head oval, body oval, tail polygon, legs lines
    draw.ellipse((830, 360, 890, 410), fill="#166534") # head
    draw.polygon([(830, 385), (800, 395), (840, 405)], fill="#166534") # mouth
    draw.ellipse((860, 390, 950, 500), fill="#166534") # body
    draw.polygon([(930, 460), (1080, 510), (940, 490)], fill="#166534") # tail
    draw.line((910, 480, 930, 540), fill="#166534", width=16) # leg 1
    draw.line((940, 480, 960, 540), fill="#166534", width=16) # leg 2
    draw.line((870, 420, 855, 435), fill="#166534", width=6) # arm
    
    image.save(REPO / "assets" / f"og-run50-{SLUG}-icons.png", "PNG")


def update_indexes():
    new_card_zh = f'''      <a class="story-card run-50" href="./{SLUG}.html">
        <img src="../../../assets/thumb-run50-{SLUG}-icons.svg?v={VERSION}" alt="小石城马拉松城市图标封面" loading="lazy" decoding="async">
        <div class="story-copy">
          <p class="story-meta">阿肯色小石城 · 2024.03.03</p>
          <h2 class="story-title">Run50 #第17州｜小石城马拉松</h2>
          <p class="story-desc">三月初的小石城马拉松，为了那块巨大的绿色暴龙奖牌驱车向南。跑过市中心、达索公司和奥索普森林公园，冲线克林顿总统的故乡。</p>
          <div class="story-foot">
            <span>长文图记</span>
            <span>阅读 →</span>
          </div>
        </div>
      </a>
    </section>'''

    new_card_en = f'''      <a class="story-card run-50" href="./{SLUG}.html">
        <img src="../../../assets/thumb-run50-{SLUG}-icons.svg?v={VERSION}" alt="Icon cover for Little Rock Marathon" />
        <div class="story-card-content">
          <div class="meta">Arkansas · Little Rock · 2024.03.03</div>
          <h2>Little Rock Marathon: running in President Clinton's backyard</h2>
          <p>A U.S. State 17 quest under the dawn lights, crossing the Clinton Presidential Bridge, loop around the Dassault Jet center, and climbing rolling hills of Allsopp Park.</p>
        </div>
      </a>
    </section>'''

    new_card_fb = f'''    <a class="story-card run-50" href="./{SLUG}.html">
      <div>
        <p class="eyebrow">World / USA / Marathon</p>
        <h2>Little Rock gave me a 26.2-mile run with the massive dinosaur medal</h2>
        <p>Race date: March 3, 2024. A Southern weekend road trip down to Arkansas for the legendary dinosaur medal, looping the aviation giants and wooded forest parks.</p>
        <div class="meta">
          <span>Little Rock, AR</span>
          <span>Dinosaur Medal secured</span>
          <span>Run50 Facebook</span>
        </div>
      </div>
      <img src="../../assets/thumb-run50-{SLUG}-icons.svg?v={VERSION}" alt="Icon-style Little Rock Marathon cover">
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
    zh_article = render_article(indexed_story, "zh", f"Run50-Little-Rock-Marathon-clean_files/")
    write_clean(zh_path, normal_page("zh", zh_article))

    print("Rendering English Page...")
    en_article = render_article(indexed_story, "en", f"../chinese/Run50-Little-Rock-Marathon-clean_files/")
    write_clean(en_path, normal_page("en", en_article))

    print("Rendering Facebook Page...")
    fb_article = render_article(indexed_story, "en", f"../stories/chinese/Run50-Little-Rock-Marathon-clean_files/")
    write_clean(fb_path, facebook_page(fb_article))

    print("Generating SVG Thumbnail Cover...")
    write_svg()

    print("Generating PNG OpenGraph Cover...")
    write_png()

    print("Registering cards on Listing Indexes...")
    update_indexes()

    print("Done! Little Rock Marathon story successfully published.")


if __name__ == "__main__":
    main()
