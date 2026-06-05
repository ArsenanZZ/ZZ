from pathlib import Path
from lxml import html
from html import escape
from PIL import Image, ImageDraw, ImageFont, ImageOps
import re


REPO = Path(__file__).resolve().parents[1]
SOURCE_BASE = Path(r"Z:\ZhennanZ Folder\000-Marathon-Story-2024-2025\20230000-Marathons\2023-State-13-WV")
SOURCE_HTML = next(p for p in SOURCE_BASE.iterdir() if p.suffix.lower() == ".html")
SOURCE_FILES = next(p for p in SOURCE_BASE.iterdir() if p.is_dir() and p.name.endswith("_files"))
SITE = "https://arsenanzz.github.io/ZZ"
SLUG = "west-virginia-marathon"
VERSION = "20260605-1"
OUT_IMG_DIR = REPO / "run50" / "stories" / "chinese" / "Run50-West-Virginia-Marathon-clean_files"


EN_BY_INDEX = {
    0: "丨WEST VIRGINIA丨",
    2: "Preface",
    3: "I have listened to the song 'Take Me Home, Country Roads' since I was a child. The first line of the lyrics, 'almost heaven West Virginia,' made me fall in love with it. Back in middle school during English class, I would sneakily listen to it on my player. Country Roads was my initiation to American country music. As for West Virginia itself, back then it felt too distant. Now, it is just a three-hour drive from our home.",
    4: "This song was written and performed by the famous American singer John Denver in 1971. The melody is light and brisk, sketching the beautiful scenery of West Virginia in the eastern United States. While writing this story, I collected several versions of the song, and it remains as beautiful as ever...",
    5: '"Almost heaven, West Virginia, Blue Ridge Mountains, Shenandoah River. Life is old there, older than the trees, younger than the mountains, growing like a breeze. Country roads, take me home to the place I belong, West Virginia, mountain mama, take me home country roads..."',
    7: "▲ Take Me Home, Country Roads @YT",
    8: "▲ Marshall University Marathon @MUM",
    10: "★",
    11: "# West Virginia: Huntington 🏈 Tri-State Confluence",
    12: "Compared to the song, the state of West Virginia doesn't seem to have a strong presence. On the marathon map, it is even more obscure.",
    13: "▲ West Virginia @Google",
    15: "▲ Coopers Rock State Forest @Google",
    17: "However, West Virginia's landscape can truly be described as spectacular. Although it is close to Kentucky, the terrain is completely different. Because West Virginia is entirely covered by mountains and plateaus with no plains, it is also known as the Mountain State. In the Potomac Highlands, the peaks reach nearly 1,500 meters, hosting many ski resorts, state parks, waterfalls, and winding trails.",
    18: "▲ Grandview National Park @Google",
    20: "▲ Grandview National Park @Google",
    22: "▲ West Virginia @Google",
    24: "Due to its unique geography, West Virginians developed a sense of independence early on. The Appalachian and Blue Ridge mountains separated this area from the rest of Virginia, so they did not feel a strong connection to that state. In fact, West Virginia is the only state born out of the American Civil War.",
    25: "▲ West Virginia @Google",
    27: "▲ New River Gorge Bridge Archival @Google",
    29: "▲ New River Gorge Bridge Archival @Google",
    31: "As for Huntington, where we were heading, it isn't very famous either—it is a tiny city. However, its location is quite unique: right at the tri-state junction of Kentucky, Ohio, and West Virginia, and at the confluence of the Ohio River and the Guyandotte River.",
    32: "▲ Huntington, WV @Google",
    34: "The junction location is great because it means it's very close to us. Along the way, we would pass Lexington, which is a one-hour drive away. Lexington has our favorite Chinese buffet, offering Saturday specials like Di San Xian (sauteed potato, eggplant, and green pepper), boiled fish, pork trotter, and various Sichuan dishes. On this trip, we naturally wouldn't miss it.",
    35: "▲ Panda Cuisine, Lexington @Google",
    37: "▲ 41st Ave and 10th Street, Huntington @Google",
    39: "After eating our fill, we drove for another two hours and arrived in Huntington. The city is small, with a reported population of about 50,000. The outskirts as we entered looked a bit rundown.",
    40: "▲ Huntington, WV @Arsenan",
    42: "We came to Huntington to run the Marshall University Marathon. This is a race where you get to cross the finish line holding a football. It's very unique, and runners love it.",
    43: "▲ Expo @Arsenan",
    45: "▲ Expo @Arsenan",
    47: "Upon arriving in Huntington, we went straight to the expo to pick up our gear. The expo was held in a church next to the green football stadium. The setup was simple, focusing on efficiency.",
    48: "▲ Expo @Siqi",
    50: "▲ Expo @Siqi",
    52: "After grabbing our packets, we had some time, so we decided to stroll around Marshall University. It was my first time seeing a marathon named directly after a university, and I was curious to see what made this place special.",
    53: "▲ Marshall University @Arsenan",
    55: "▲ Marshall University @Arsenan",
    57: "▲ Marshall University @Arsenan",
    59: "▲ Marshall University @Arsenan",
    61: "When we first arrived at Marshall University, I habitually searched for the school's ranking. Seeing it wasn't very high, I was a bit puzzled. If it isn't a prestigious university, why does the whole town seem so proud of it? They even named the marathon after it. Later, when we visited Kroger, we saw school-branded souvenirs everywhere.",
    62: "▲ Marshall University @Arsenan",
    64: "▲ Marshall University @Arsenan",
    66: "Suddenly, I realized I had fallen into the trap of Chinese-style thinking. Our education overemphasizes academic rankings and test scores, so I was used to analyzing things through that lens.",
    67: "Marshall University's greatest pride is its football team, the Thundering Herd. This team has won three national championships, including NCAA Division I-AA titles in 1992 and 1996, and finished as runner-up in 1991, 1993, and 1995. Even though the town has only 50,000 residents, a single game can draw over 38,000 fans!",
    68: "Considering that American society is practically built on sports, the residents' pride is not surprising. I hope China will have a sports culture like this one day, so no one will say I'm wasting my life by running marathons.",
    69: "When I was a kid, I loved playing soccer and thought I was pretty good. But my homeroom teacher would always pull me aside, warning that running around would deform my legs. Now that I run marathons, my family and friends constantly warn me that my knees will be ruined. It feels like an endless loop.",
    70: "▲ Marshall University @Arsenan",
    72: "▲ Marshall University @Arsenan",
    74: "Anyway, back to Marshall University. The campus slogans reflect this pride everywhere. The green signs paired with the golden autumn foliage create a very refreshing atmosphere.",
    75: "▲ Memorial Fountain @Arsenan",
    77: "▲ Memorial Fountain @Arsenan",
    79: "▲ Memorial Fountain @Siqi",
    81: "As we walked, we reached a fountain outside the Memorial Student Center. This fountain was built to honor the 75 victims of the 1970 plane crash. On November 14, 1970, the deadliest single-tragedy aviation crash in NCAA sports history occurred, claiming 75 lives. The crash on a rainy hillside in Wayne County, West Virginia, wiped out almost the entire Marshall University football team, along with coaches, crew, and many dedicated fans.",
    82: "▲ Football Team (1970) @Google",
    84: "The monument was created by sculptor Harry Bertoia, standing 13 feet tall and weighing 6,500 pounds. He designed the fountain to 'commemorate the living, not the dead—on the waters of life, rising, receding, surging, to express upward growth, immortality, and eternity.'",
    85: "For Marshall students and alumni, this team is the city's pride and its eternal scar. The Memorial Fountain stands as a symbol of resilience, eternal spirit, and looking forward.",
    86: "▲ Marshall University @Arsenan",
    88: "▲ Marshall University @Siqi",
    90: "▲ Marshall University @Arsenan",
    92: "We took a lot of photos around the campus, which was beautiful. Later, we bought some breakfast at the supermarket and headed back to our motel. This was my first time staying in a motel, and it exceeded my expectations—very convenient, clean, and comfortable.",
    93: "▲ Motel @Arsenan",
    95: "We watched some episodes of 'Divas Hit the Road' and Siqi worked for a bit before we went to bed early. The motel had decent soundproofing. They supposedly offered breakfast the next morning, but we had to leave too early to catch it.",
    96: "★★",
    97: "# Marshall University Marathon: 19th Anniversary 🏈 Huntington, West Virginia",
    98: "This is West Virginia's largest marathon, but it must be said that the Marshall University Marathon and Half Marathon is still a relatively small race (with just over 1,800 participants across both distances in 2023). The course is a 13.1-mile loop, which marathon runners complete twice.",
    99: "▲ Course Map @Google",
    101: "The start and finish lines are at Marshall University's Joan C. Edwards Stadium. The course loops through downtown Huntington, Pullman Square, several parks, and a straight stretch through a light industrial area.",
    102: "▲ Joan C Edward @Arsenan",
    104: "▲ Joan C Edward @Arsenan",
    106: "I enjoyed running through the neighborhoods and looking at the houses. We ran a short stretch through Harris Riverfront Park along the river (I wish this section had been longer), looped through the larger Ritter Park, ran past the campus, and finished on the field of Joan C. Edwards Stadium.",
    107: "▲ Start @Arsenan",
    109: "▲ Start @Siqi",
    111: "For me, the first highlight of the day was that before running through the Marshall campus for the second time, we were handed a white flower to place on the 1970 football team memorial.",
    112: "Another highlight: just before the finish line, volunteers hand a football to the marathon runners, allowing them to cross the line in a 'touchdown' style. That is truly unique.",
    113: "▲ Start @Arsenan",
    115: "▲ Start @Arsenan",
    117: "▲ Start @Arsenan",
    119: "▲ Start @Arsenan",
    121: "▲ Start @Arsenan",
    123: "On race day, we arrived at the starting area next to the green football field right on time. A large crowd of runners had already gathered, and the energetic announcer led the crowd in chanting: 'We are—' 'Marshall!' 'Marshall!'...",
    124: "▲ 《We Are Marshall》 @Google",
    126: "'We Are Marshall' is a 2006 sports drama film based on a true story. It tells the story of the 1971 Marshall University football team's struggle to rebuild after all 75 members of the 1970 team perished in the plane crash.",
    127: "▲ Start @Arsenan",
    129: "▲ Start @Arsenan",
    131: "▲ Start @Arsenan",
    133: "▲ Start @Arsenan",
    135: "▲ Go @Arsenan",
    137: "The race finally started, and our field of 1,800 runners headed west under the morning sunrise. The initial route followed 3rd Avenue. There weren't many houses, and the sunrise cast a beautiful, gentle light.",
    138: "▲ Sunrise Morning @Arsenan",
    140: "▲ Sunrise Morning @Arsenan",
    142: "▲ Sunrise Morning @Arsenan",
    144: "▲ 50State Club @Arsenan",
    146: "I spotted a runner wearing a 50 States Marathon Club shirt. I knew many runners choose this race to check off West Virginia. Before the race, I had seen recommendations for this event on the 50 States Club homepage.",
    147: "▲ Downtown @Arsenan",
    149: "▲ Downtown @Arsenan",
    151: "▲ Mile-2 @Arsenan",
    153: "▲ Stadium @Arsenan",
    155: "▲ Marshall University @Arsenan",
    157: "▲ Marshall University @Arsenan",
    159: "During this stretch, we ran through the university area. Families dressed in Marshall green sat along the curbs, reminding me of our childhood school field trips.",
    160: "▲ 430 Pacer @Arsenan",
    162: "▲ Harris Riverfront Park @Arsenan",
    164: "▲ Harris Riverfront Park @Arsenan",
    166: "▲ Harris Riverfront Park @Arsenan",
    168: "▲ Harris Riverfront Park @MUM",
    170: "▲ Harris Riverfront Park @MUM",
    172: "▲ Harris Riverfront Park @MUM",
    174: "▲ Harris Riverfront Park @MUM",
    176: "▲ Harris Riverfront Park @Arsenan",
    178: "▲ Harris Riverfront Park @Arsenan",
    180: "Around Mile 3, we reached Harris Riverfront Park. I absolutely loved this section. The college student volunteers were incredibly enthusiastic, making me feel almost guilty if I didn't grab a few cups of water.",
    181: "▲ Harris Riverfront Park @Arsenan",
    183: "▲ Harris Riverfront Park @Arsenan",
    185: "On our right was the Ohio River. It felt different from the view in Louisville. This stretch was very pleasant, just too short. But that was fine, as we would run it three more times.",
    186: "▲ Mile-4 @Arsenan",
    188: "▲ Restroom @Arsenan",
    190: "▲ Virginia St @Arsenan",
    192: "▲ Mile-5 @Arsenan",
    194: "Exiting the park, we ran onto the straight Virginia Avenue. This section felt a bit desolate and quiet, but the road was wide, and the sun remained gentle. I took the opportunity to make a quick restroom stop.",
    195: "▲ Old Central City Gazebo @Arsenan",
    197: "▲ Old Central City Gazebo @Arsenan",
    199: "▲ Old Central City Gazebo @Arsenan",
    201: "▲ Mile-6 @Arsenan",
    203: "▲ Central City @ 14 STW @Arsenan",
    205: "Around Mile 5, we turned left onto 14th Street. The route looped around the Old Central City Gazebo to add some distance, then passed through Central City at 14th Street West, which had a bit more crowd energy.",
    206: "▲ Chad Pennington @Arsenan",
    208: "▲ Chad Pennington @Arsenan",
    210: "Further ahead stood a beautiful red brick building named after Chad Pennington, carrying a vintage aesthetic.",
    211: "▲ Kiwanis Park @Arsenan",
    213: "▲ Kiwanis Park @Arsenan",
    215: "▲ Kiwanis Park @Arsenan",
    217: "▲ Memorial Blvd @Arsenan",
    219: "Next, we ran a short stretch through Kiwanis Park, then followed Memorial Boulevard and Fourpole Creek to the dirt paths of Ritter Park. Although the organizers described this as a fast trail, it felt a bit slippery, making it hard to push off.",
    220: "▲ Ritter Park @Arsenan",
    222: "▲ Mile-8 @Arsenan",
    224: "▲ Ritter Park @Arsenan",
    226: "▲ Ritter Park @Arsenan",
    228: "The park scenery was beautiful and refreshing. After crossing a wooden bridge, we finally finished the slippery gravel path.",
    229: "▲ Ritter Park @Arsenan",
    231: "▲ Mile-9 @Arsenan",
    233: "Now we reached 13th Street. After passing the Mile 9 marker, there was an Army aid station. The volunteers saw me wearing my Arsenal shirt and booed, saying Arsenal was no good and Chelsea was much better.",
    234: "▲ Army Supply @Arsenan",
    236: "▲ Chelsea Guy @Arsenan",
    238: "The guy who booed me was caught red-handed by my camera. Buddy, I'll remember you!",
    239: "▲ Turn Around @Arsenan",
    241: "▲ Rose Tunnel @Arsenan",
    243: "▲ Rose Tunnel @Arsenan",
    245: "▲ Rose Tunnel @Arsenan",
    247: "▲ Mile-10 @Arsenan",
    249: "▲ Back Harris Riverfront @Arsenan",
    251: "▲ Back Harris Riverfront @Arsenan",
    253: "Just past the Army station was a sharp turn. We ran through the Rose Tunnel to 8th Street, then headed north back to Harris Riverfront Park.",
    254: "▲ Harris Riverfront Park @MUM",
    256: "▲ Harris Riverfront Park @MUM",
    258: "▲ Harris Riverfront Park @MUM",
    260: "▲ Harris Riverfront Park @MUM",
    262: "▲ Harris Riverfront Park @MUM",
    264: "▲ Harris Riverfront Park @Arsenan",
    266: "▲ Harris Riverfront Park @Arsenan",
    268: "▲ Harris Riverfront Park @Arsenan",
    270: "▲ Harris Riverfront Park @Arsenan",
    272: "Running in the opposite direction through Harris Riverfront Park made the scenery feel completely different. The volunteers were still there, and the lively atmosphere hadn't faded at all.",
    273: "▲ Marshsall University @Arsenan",
    275: "Returning to the city streets, the marathon and half-marathon runners split up. The full marathon pack headed through the Marshall University campus—a path Siqi and I knew well from our photoshoot the day before.",
    276: "▲ Left Marshsall University @Arsenan",
    278: "▲ Back Stadium @Arsenan",
    280: "Leaving campus, the stadium stood right before us. But unlike the half-marathoners, we had to wave goodbye to it, as we still had more than half the distance left.",
    281: "▲ Mile-13 @Arsenan",
    283: "▲ Marshsall University @Arsenan",
    285: "Looping back to the start, we repeated the first-lap route. I checked my watch: less than two hours for the half. This was better than expected, and since I hadn't pushed myself too hard in the first half, I felt my Nashville flag could finally stand.",
    286: "▲ Harris Riverfront Park @Arsenan",
    288: "Returning to the city streets, the familiar route gave me confidence. I knew the terrain inside out. However, there were some changes: by the third time we reached Harris Riverfront Park, the volunteers' energy had noticeably dropped. But as long as the supplies were there, it was fine.",
    289: "▲ Mile-19 @Arsenan",
    291: "By then, my projected finish time was ahead of the 4-hour pacer. I decided to stick to the sub-4 goal and give it a push.",
    292: "▲ Chad Pennington @Arsenan",
    294: "▲ Chad Pennington @Arsenan",
    296: "▲ Chad Pennington @Arsenan",
    298: "My pace was steady, and in a flash, I reached Mile 19. The red brick building looked different under the stronger sunlight. The sun lit up my face, and I looked in good shape.",
    300: "▲ Kiwanis Park @Arsenan",
    302: "I made sure to grab supplies; you can't skip aid stations just to save a few seconds. I realized it had been a while since I ran so seriously. I kept calculating the time: Mile 20, Mile 21...",
    303: "▲ Mile-20 @Arsenan",
    305: "▲ Mile-21 @Arsenan",
    307: "▲ Fourpole Creek @Arsenan",
    309: "When I returned to the Army aid station, I had another friendly battle with the Chelsea guy. I yelled that Arsenal was the best. By then, they were already packing up.",
    310: "▲ Army Water Station @Arsenan",
    312: "▲ Army Water Station @Arsenan",
    314: "Returning to the Rose Tunnel, the downhill slope wasn't easy, and the uphill climb was even tougher. As the miles piled up, fatigue began to set in.",
    315: "▲ Turn Around @Arsenan",
    317: "▲ Rose Tunnel @Arsenan",
    319: "▲ Back @Arsenan",
    321: "I didn't miss a single aid station, calculating my time and gel intake. As we neared Harris Riverfront Park on 1st Street, I grabbed a cup of Coke.",
    322: "▲ Cole Station @Arsenan",
    324: "By now, Harris Riverfront Park was nearly empty of spectators, but there was still water left for us. The sun had grown intense, and my pace dropped a bit. However, I had built up enough of a cushion earlier to afford a slight slowdown. The hope of breaking 4 hours was still very strong.",
    325: "▲ Harris Riverfront @Arsenan",
    327: "▲ Mile-25 @Arsenan",
    329: "▲ Back @Arsenan",
    331: "Entering the Marshall campus for the second time, volunteers at the gate handed each runner a flower to honor the 1970 victims. I didn't fully grasp the depth of the gesture at the time, and being exhausted, I didn't know where to put it. Finding it inconvenient, I gave it to a volunteer along the road. Looking back, that was a real regret of this race.",
    332: "▲ Marshall University @Arsenan",
    334: "▲ Marshall University @MUM",
    336: "▲ Marshall University @MUM",
    338: "▲ Marshall University @MUM",
    340: "▲ Marshall University @MUM",
    342: "▲ Marshall University @MUM",
    344: "▲ Marshall University @MUM",
    346: "▲ Marshall University @MUM",
    348: "▲ Marshall University @MUM",
    350: "▲ Marshall University @MUM",
    352: "▲ Marshall University @MUM",
    354: "▲ Marshall University @MUM",
    356: "▲ Marshall University @MUM",
    358: "▲ Marshall University @MUM",
    360: "Leaving the campus, we were about to run back onto the turf of Joan C. Edwards Stadium. I kept staring at my watch; breaking 4 hours was down to a split-second decision. I decided to sprint—the atmosphere was set.",
    361: "▲ Joan C Edward Stadium @Arsenan",
    363: "▲ Touchdown @Arsenan",
    365: "▲ Touchdown @Arsenan",
    367: "▲ Touchdown @Arsenan",
    369: "Just as I entered the stadium, a volunteer handed me a football. The runner in blue next to me was sprinting with his football, which triggered my competitive spirit. While he paused to pose near the finish line, I easily passed him, gaining one last position.",
    370: "▲ Touchdown @MUM",
    372: "▲ Touchdown @MUM",
    374: "▲ Touchdown @MUM",
    376: "▲ Touchdown @MUM",
    379: "▲ Touchdown @MUM",
    380: "▲ Touchdown @MUM",
    382: "▲ Touchdown @MUM",
    384: "I looked at my watch: 3 hours and 58 minutes. Later, the official results confirmed I had successfully broken 4 hours. Honestly, it was a pleasant surprise.",
    385: "▲ Return Ball @Arsenan",
    387: "▲ Medal Time @Arsenan",
    389: "▲ Done @Arsenan",
    391: "▲ Finish @Arsenan",
    393: "▲ Medal Time @Arsenan",
    395: "▲ Medal Time @Arsenan",
    397: "After returning the football and receiving my medal, I stood by the stadium billboard watching other runners score their 'touchdowns.' I didn't feel too exhausted, and even a butterfly hovered around to congratulate me. I felt extremely happy.",
    398: "▲ Medal Time @Arsenan",
    400: "▲ Medal Time @Arsenan",
    402: "▲ Runner @Arsenan",
    404: "▲ Medal Time @Runner Above",
    406: "▲ Medal Time @Runner",
    408: "Siqi finished the race as well and was outside eating some treats. She was surprised that I finished so quickly. We took some photos in the stadium, and I queued at the recovery area to get stretched by a volunteer, which was great. Then we took some photos outside the stadium and headed happily to Planet Fitness to shower.",
    409: "▲ Massage @Siqi",
    411: "▲ Massage @Siqi",
    413: "▲ Massage @Siqi",
    415: "▲ Leave @Siqi",
    417: "▲ Medal Time @Runner",
    419: "▲ Medal Time @Siqi",
    421: "▲ Medal Time @Siqi",
    423: "▲ Medal Time @Siqi",
    425: "▲ Medal Time @Siqi",
    427: "▲ Siqi @Arsenan",
    429: "▲ Stadium @Arsenan",
    431: "▲ Stadium @Arsenan",
    433: "▲ Medal Time @Arsenan",
    435: "▲ Medal Time @Siqi",
    437: "▲ Medal Time @Siqi",
    439: "▲ Medal Time @Siqi",
    441: "▲ Medal Time @Arsenan",
    443: "The stadium DJ's music echoed in waves, and runners were still crossing the finish line. But as our car drove away, the sounds grew fainter until everything went silent. The car drove further and further, but the impact of this marathon remained incredibly strong.",
    444: "▲ Arsenal @Arsenan",
    446: "▲ Huntington @Arsenan",
    448: "▲ Huntington @Arsenan",
    450: "▲ Planet Fitness @Arsenan",
    453: "后记",
    454: "On the way back, we stopped in Lexington again. Siqi treated me to a Korean hotpot buffet at K-Pot to celebrate my sub-4 finish. The hotpot tasted great, and I heard they are planning to open a location in Louisville.",
    455: "▲ K-Pot @Arsenan",
    457: "▲ K-Pot @Arsenan",
    459: "▲ K-Pot @Arsenan",
    461: "▲ K-Pot @Arsenan",
    463: "As we headed home, the evening glow painted the horizon along I-64. It was beautiful. I felt a bit proud, thinking: it had been a long time since I ran seriously, and yet with just a little effort, I broke 4 hours. It seems I am a talented and capable runner after all, and qualifying for Boston is only a matter of time. (You can get faster, or you can get older.)",
    464: "▲ I-64 @Arsenan",
    466: "Of course, having confidence is good, but I don't want to go all out every time. Fast running has its thrill, while slow running has its own charm. This shifting rhythm is probably more interesting.",
    467: "More importantly, I want to stay healthy and disciplined. I don't want to get injured. Having run for so many years, I know my body better than anyone. Running is a lifelong journey, so there is no rush.",
    468: "- The end -",
    469: "Words | Arsenan",
    470: "Photos | Arsenan",
    471: "Design | Arsenan"
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

    return clean


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
            im.save(OUT_IMG_DIR / out_name, "WEBP", quality=82)
    return count


def render_article(indexed, lang, img_prefix):
    is_zh = lang == "zh"
    blocks = []
    img_idx = 0
    for idx, event in indexed:
        if event["type"] == "img":
            img_idx += 1
            # For en/facebook, references chinese image folder relative to their location
            src = f"{img_prefix}img-{img_idx:03d}.webp"
            # look ahead for caption
            caption = ""
            for next_idx in range(indexed.index((idx, event)) + 1, len(indexed)):
                next_event = indexed[next_idx][1]
                if next_event["type"] == "text":
                    if is_caption(next_event["text"]):
                        txt = next_event["text"]
                        if not is_zh and indexed[next_idx][0] in EN_BY_INDEX:
                            txt = EN_BY_INDEX[indexed[next_idx][0]]
                        caption = txt
                    break
                elif next_event["type"] == "img":
                    break
            
            blocks.append(f'''      <figure>
        <img src="{src}" alt="West Virginia Marathon image {img_idx}" loading="lazy" decoding="async">''')
            if caption:
                blocks.append(f'        <figcaption>{escape(caption)}</figcaption>')
            blocks.append('      </figure>')
        
        elif event["type"] == "text":
            txt = event["text"]
            if not is_zh and idx in EN_BY_INDEX:
                txt = EN_BY_INDEX[idx]
            
            if is_caption(event["text"]) or should_skip_text(event["text"]):
                continue
            
            if txt.startswith("丨"):
                # Channel title tag
                continue
            elif txt.startswith("# "):
                # Heading 1
                blocks.append(f'      <h2 class="section-label">{escape(txt[2:])}</h2>')
            elif txt.startswith("## "):
                # Heading 2
                blocks.append(f'      <h3>{escape(txt[3:])}</h3>')
            elif txt.startswith("- 本文完 -") or txt.startswith("- The end -"):
                blocks.append(f'      <p class="end-mark">{escape(txt)}</p>')
            elif txt.startswith("文字丨") or txt.startswith("摄影丨") or txt.startswith("设计丨") or txt.startswith("Words |") or txt.startswith("Photos |") or txt.startswith("Design |"):
                blocks.append(f'      <p class="credit-line">{escape(txt)}</p>')
            else:
                blocks.append(f'      <p>{escape(txt)}</p>')
                
    return "\n".join(blocks)


def page_css() -> str:
    return """
    :root {
      --paper: #f4f6f7;
      --surface: #ffffff;
      --ink: #20242b;
      --muted: #667085;
      --line: #dde5ec;
      --river: #0e7490;
      --brick: #a33a2b;
      --gold: #b7892f;
      --soft: #edf3f7;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      background: linear-gradient(180deg, #eef5f6 0, var(--paper) 320px);
      color: var(--ink);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
      line-height: 1.7;
    }
    a { color: var(--river); text-decoration-thickness: 1px; text-underline-offset: 4px; }
    .story-nav {
      max-width: 860px;
      margin: 0 auto;
      padding: 18px 22px 0;
      display: flex;
      gap: 14px;
      justify-content: space-between;
      color: var(--muted);
      font-size: 14px;
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
    }
    .article-body {
      max-width: 720px;
      margin: 0 auto;
      padding: 54px 22px 64px;
    }
    .article-body p {
      margin: 0 0 22px;
      font-size: 17.5px;
      line-height: 1.8;
      color: #2c323f;
    }
    .article-body h2.section-label {
      margin: 48px 0 20px;
      padding-top: 24px;
      border-top: 1px solid var(--line);
      color: var(--brick);
      font-size: 21px;
      font-weight: 800;
    }
    .article-body h3 {
      margin: 32px 0 16px;
      color: #111827;
      font-size: 19px;
      font-weight: 800;
    }
    figure {
      margin: 32px 0;
    }
    figure img {
      display: block;
      width: 100%;
      height: auto;
      border: 1px solid var(--line);
      border-radius: 4px;
    }
    figcaption {
      margin-top: 8px;
      color: var(--muted);
      font-size: 13px;
      text-align: center;
    }
    .end-mark,
    .credit-line {
      text-align: center;
      color: var(--muted);
      font-size: 14px;
    }
    .end-mark {
      margin: 48px 0 12px;
      font-weight: 700;
    }
    .credit-line { margin: 6px 0; }
    .page-footer {
      max-width: 860px;
      margin: 0 auto;
      padding: 42px 22px 64px;
      color: var(--muted);
      font-size: 14px;
      text-align: center;
    }
    """


def facebook_css() -> str:
    return """
    :root {
      --ink: #0f172a;
      --muted: #475569;
      --line: #cbd5e1;
      --red: #0b67c2;
      --soft: #edf3f7;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      background: #f8fafc;
      color: var(--ink);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      line-height: 1.62;
    }
    a { color: var(--red); text-decoration: none; }
    .breaking {
      background: var(--ink);
      color: #ffffff;
      padding: 10px 22px;
      font-size: 12px;
      font-weight: 900;
      text-transform: uppercase;
      letter-spacing: .08em;
    }
    .breaking-inner {
      max-width: 1180px;
      margin: 0 auto;
      display: flex;
      justify-content: space-between;
    }
    .breaking-inner a { color: inherit; }
    .site-head {
      background: #ffffff;
      border-bottom: 3px solid var(--red);
    }
    .site-head-inner {
      max-width: 1180px;
      margin: 0 auto;
      padding: 24px 22px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .wordmark {
      font-size: 28px;
      font-weight: 900;
      color: var(--ink);
      letter-spacing: -.03em;
      text-decoration: none;
    }
    .section-nav {
      display: flex;
      gap: 18px;
      font-size: 13px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: .05em;
    }
    .section-nav a { color: var(--muted); }
    .section-nav a:hover { color: var(--red); }
    .article {
      max-width: 1180px;
      margin: 0 auto;
      padding: 42px 22px 64px;
    }
    .hero {
      margin-bottom: 34px;
      border-bottom: 1px solid var(--line);
      padding-bottom: 34px;
    }
    .label {
      color: var(--red);
      font-size: 12px;
      font-weight: 900;
      text-transform: uppercase;
      letter-spacing: .08em;
    }
    h1 {
      margin: 12px 0 16px;
      font-size: clamp(30px, 5vw, 48px);
      line-height: 1.1;
      font-weight: 900;
      letter-spacing: -.02em;
    }
    .dek {
      margin: 0 0 24px;
      font-size: clamp(17px, 3vw, 21px);
      line-height: 1.45;
      color: var(--muted);
    }
    .byline {
      display: flex;
      flex-wrap: wrap;
      gap: 14px;
      color: var(--muted);
      font-size: 13px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: .05em;
    }
    .lead-media {
      margin: 30px 0 0;
    }
    .lead-media img {
      display: block;
      width: 100%;
      height: auto;
      border: 1px solid var(--line);
    }
    .lead-media figcaption {
      margin-top: 10px;
      color: var(--muted);
      font-size: 13px;
      font-style: italic;
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
    title = "Run50 #第13州｜西弗吉尼亚：马歇尔大学马拉松｜抱着橄榄球达阵，在乡村路跑进四小时！" if is_zh else "Run50 #13 | West Virginia: Marshall University Marathon"
    short = "Run50 #13 | Marshall University Marathon"
    desc = (
        "十一月初的西弗吉尼亚亨廷顿，在秋高气爽的马歇尔大学校园，将一朵花送给1970年空难的离世队员们；在终点抱着橄榄球“达阵”冲线，成功破4！"
        if is_zh
        else "Race date: November 5, 2023. Running U.S. State 13: Marshall University Marathon in Huntington, West Virginia, featuring a stadium finish with a football touchdown, placing a white flower on the 1970 sports tragedy memorial, and achieving a sub-4 hour PR."
    )
    canonical = f"{SITE}/run50/stories/{'chinese' if is_zh else 'english'}/{SLUG}.html"
    other = f"../{'english' if is_zh else 'chinese'}/{SLUG}.html"
    fb = f"../../facebook/{SLUG}.html"
    nav = (
        f'<a href="./index.html">← 中文故事</a><a href="{other}">English</a><a href="{fb}">Facebook</a><a href="../../index.html">Run50</a>'
        if is_zh
        else f'<a href="./index.html">← English Stories</a><a href="{other}">中文</a><a href="{fb}">Facebook</a><a href="../../index.html">Run50</a>'
    )
    kicker = "Run50 #第13州 · 西弗吉尼亚" if is_zh else "Run50 #13 · West Virginia"
    footer = "© 2023-2026 ArsenanZZ. Built with love."
    locale = "zh-CN" if is_zh else "en"
    key = f"run50-{SLUG}-zh" if is_zh else f"run50-{SLUG}-en"
    mount = f"supabase-comments-west-virginia-zh" if is_zh else f"supabase-comments-west-virginia-en"
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
  <meta property="og:image:alt" content="West Virginia Marathon cover with Appalachian mountains, country road and a football.">
  <meta property="article:author" content="Arsenan">
  <meta property="article:published_time" content="2023-11-05T07:00:00-05:00">
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
      <span>Race: November 5, 2023</span>
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
    title = "I ran West Virginia's university marathon for a stadium finish, scored a touchdown to break 4 hours, and paid my respects to a local tragedy"
    desc = "Race date: November 5, 2023. Running U.S. State 13: Marshall University Marathon in Huntington, West Virginia, featuring a stadium finish with a football touchdown, placing a white flower on the 1970 sports tragedy memorial, and achieving a sub-4 hour PR."
    canonical = f"{SITE}/run50/facebook/{SLUG}.html"
    locale = "en"
    key = f"run50-{SLUG}-facebook-en"
    mount = f"supabase-comments-west-virginia-facebook-en"
    og_image = f"{SITE}/assets/og-run50-{SLUG}-icons.png?v={VERSION}"
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Marshall University Marathon | Run50 Facebook</title>
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
  <meta property="og:image:alt" content="West Virginia Marathon cover with Appalachian mountains, country road and a football.">
  <meta property="article:author" content="Arsenan">
  <meta property="article:published_time" content="2023-11-05T07:00:00-05:00">
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
      <span>Race date: November 5, 2023</span>
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
        <span>Race: November 5, 2023</span>
        <span>Huntington, WV</span>
        <span>Run50 #13</span>
      </div>
      <figure class="lead-media"><img src="../../assets/og-run50-{SLUG}-icons.png?v={VERSION}" alt="Icon-style West Virginia Marathon cover"><figcaption>West Virginia icon cover with Appalachian mountains, winding country road and a football.</figcaption></figure>
    </section>
    <section class="story-grid">
      <aside class="rail">
        <section class="brief-box"><h2>At a glance</h2><dl><div><dt>Race</dt><dd>Marshall University Marathon, Run50 State 13.</dd></div><div><dt>Course</dt><dd>Huntington downtown, Ohio riverfront paths, central neighborhoods, and a stadium finish inside the Joan C. Edwards Stadium.</dd></div><div><dt>What stayed with me</dt><dd>Country Roads morning sunrise, the 1970 football team memorial flower tribute, running past local homes, and carrying a football touchdown at the finish line to secure a sub-4 hour PR.</dd></div></dl></section>
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
<title id="title">West Virginia Marathon icon cover</title>
<desc id="desc">Icon style cover with West Virginia title, Run50 badge, Appalachian mountains, winding country road, and football.</desc>
<rect width="1200" height="750" fill="#edf3f7"/>
<g transform="translate(70 104)">
  <text x="0" y="0" font-family="Arial, Helvetica, sans-serif" font-size="66" font-weight="900" fill="#20242b">W. VIRGINIA</text>
  <text x="0" y="46" font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="700" fill="#0b67c2">MOUNTAINS · COUNTRY ROADS · FOOTBALL</text>
</g>
<rect x="758" y="62" width="364" height="166" rx="22" fill="#ffffff" stroke="#20242b" stroke-width="8"/>
<text x="790" y="122" font-family="Arial, Helvetica, sans-serif" font-size="41" font-weight="900" fill="#20242b">Run50 #13</text>
<text x="790" y="182" font-family="Arial, Helvetica, sans-serif" font-size="52" font-weight="900" fill="#0b67c2">W. VIRGINIA</text>

<!-- Sky Sunset Warmth -->
<rect x="50" y="260" width="1100" height="320" rx="10" fill="#fffbeb" stroke="#20242b" stroke-width="5"/>

<!-- Sun -->
<circle cx="250" cy="350" r="45" fill="#f97316"/>

<!-- Layered Appalachian Mountains -->
<path d="M50 540 Q200 440 450 510 T900 480 T1150 500 L1150 580 L50 580 Z" fill="#a7f3d0"/>
<path d="M50 560 Q300 470 650 550 T1150 520 L1150 580 L50 580 Z" fill="#34d399"/>
<path d="M50 580 L1150 580 L1150 720 L50 720 Z" fill="#047857"/>
<path d="M50 570 Q450 490 850 570 T1150 550 L1150 580 L50 580 Z" fill="#10b981"/>

<!-- Winding Country Road -->
<polygon points="500 720, 700 720, 610 570, 590 570" fill="#374151" stroke="#20242b" stroke-width="4"/>
<path d="M600 720 L600 570" stroke="#fbbf24" stroke-dasharray="15 10" stroke-width="4"/>

<g transform="translate(860, 540) rotate(15)">
  <ellipse cx="50" cy="50" rx="90" ry="60" fill="#78350f" stroke="#20242b" stroke-width="7"/>
  <!-- Laces -->
  <line x1="-15" y1="50" x2="115" y2="50" stroke="#ffffff" stroke-width="8"/>
  <line x1="10" y1="35" x2="10" y2="65" stroke="#ffffff" stroke-width="6"/>
  <line x1="30" y1="35" x2="30" y2="65" stroke="#ffffff" stroke-width="6"/>
  <line x1="50" y1="35" x2="50" y2="65" stroke="#ffffff" stroke-width="6"/>
  <line x1="70" y1="35" x2="70" y2="65" stroke="#ffffff" stroke-width="6"/>
  <line x1="90" y1="35" x2="90" y2="65" stroke="#ffffff" stroke-width="6"/>
  <!-- End stripes -->
  <path d="M-10 20 Q-25 50 -10 80" fill="none" stroke="#ffffff" stroke-width="8"/>
  <path d="M110 20 Q125 50 110 80" fill="none" stroke="#ffffff" stroke-width="8"/>
</g>
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
    draw.text((64, 64), "W. VIRGINIA", font=font(66, True), fill=text_color)
    draw.text((66, 136), "MOUNTAINS · COUNTRY ROADS · FOOTBALL", font=font(26, True), fill=blue)
    
    # Badge Box
    draw.rounded_rectangle((760, 64, 1122, 228), radius=22, fill="#ffffff", outline=text_color, width=7)
    draw.text((790, 112), "Run50 #13", font=font(40, True), fill=text_color)
    draw.text((790, 166), "W. VIRGINIA", font=font(50, True), fill=blue)
    
    # Sunset Sky Area
    draw.rectangle((50, 260, 1150, 580), fill="#fffbeb", outline=text_color, width=5)
    
    # Sun
    draw.ellipse((205, 305, 295, 395), fill="#f97316")
    
    # Layered Mountains
    draw.polygon([(50, 580), (200, 480), (450, 550), (700, 490), (950, 560), (1150, 520), (1150, 580)], fill="#a7f3d0")
    draw.polygon([(50, 580), (300, 510), (650, 570), (900, 520), (1150, 550), (1150, 580)], fill="#34d399")
    draw.polygon([(50, 580), (450, 530), (850, 580), (1150, 560), (1150, 580)], fill="#10b981")
    draw.rectangle((50, 570, 1150, 580), fill="#047857")
    
    # Road
    draw.polygon([(500, 580), (700, 580), (610, 510), (590, 510)], fill="#374151", outline=text_color, width=2)
    # dashed yellow center line
    draw.line((600, 580, 600, 510), fill="#fbbf24", width=3)
    
    # Football
    # Create a sub-image to draw a rotated football
    fb_img = Image.new("RGBA", (200, 200), (0, 0, 0, 0))
    fb_draw = ImageDraw.Draw(fb_img)
    fb_draw.ellipse((10, 40, 190, 160), fill="#78350f", outline="#20242b", width=7)
    # Laces
    fb_draw.line((10, 100, 190, 100), fill="#ffffff", width=8)
    for lx in range(40, 170, 24):
        fb_draw.line((lx, 80, lx, 120), fill="#ffffff", width=6)
    # Stripes
    fb_draw.arc((10, 50, 60, 150), 90, 270, fill="#ffffff", width=8)
    fb_draw.arc((140, 50, 190, 150), 270, 90, fill="#ffffff", width=8)
    
    # Rotate football by 15 degrees
    rotated_fb = fb_img.rotate(15, resample=Image.Resampling.BICUBIC)
    image.paste(rotated_fb, (840, 420), rotated_fb)
    
    image.save(REPO / "assets" / f"og-run50-{SLUG}-icons.png", "PNG")


def update_indexes():
    new_card_zh = f'''      <a class="story-card run-50" href="./{SLUG}.html">
        <img src="../../../assets/thumb-run50-{SLUG}-icons.svg?v={VERSION}" alt="西弗吉尼亚马拉松城市图标封面" loading="lazy" decoding="async">
        <div class="story-copy">
          <p class="story-meta">西弗吉尼亚亨廷顿 · 2023.11.05</p>
          <h2 class="story-title">Run50 #第13州｜西弗吉尼亚马拉松</h2>
          <p class="story-desc">十一月初的西弗吉尼亚亨廷顿，在秋高气爽的马歇尔大学校园，将一朵花送给1970年空难的离世队员们；在终点抱着橄榄球“达阵”冲线，成功破4！</p>
          <div class="story-foot">
            <span>长文图记</span>
            <span>阅读 →</span>
          </div>
        </div>
      </a>
    </section>'''

    new_card_en = f'''      <a class="story-card run-50" href="./{SLUG}.html">
        <img src="../../../assets/thumb-run50-{SLUG}-icons.svg?v={VERSION}" alt="Icon cover for West Virginia Marathon" />
        <div class="story-card-content">
          <div class="meta">West Virginia · Huntington · 2023.11.05</div>
          <h2>Marshall University Marathon: scoring a football touchdown in West Virginia</h2>
          <p>Running U.S. State 13 quest under the autumn sunshine, honoring the 1970 sports plane tragedy memorial on campus, and scoring a touchdown at the finish line inside the football stadium to break 4 hours.</p>
        </div>
      </a>
    </section>'''

    new_card_fb = f'''    <a class="story-card run-50" href="./{SLUG}.html">
      <div>
        <p class="eyebrow">World / USA / Marathon</p>
        <h2>West Virginia gave me a touchdown stadium finish to break 4 hours</h2>
        <p>Race date: November 5, 2023. Running U.S. State 13 at Marshall University in Huntington, WV. A beautiful autumn loop race with a football stadium finish, placing a flower on the 1970 team plane crash memorial, and a PR.</p>
        <div class="meta">
          <span>Huntington, WV</span>
          <span>touchdown secured</span>
          <span>Run50 Facebook</span>
        </div>
      </div>
      <img src="../../assets/thumb-run50-{SLUG}-icons.svg?v={VERSION}" alt="Icon-style West Virginia Marathon cover">
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
    zh_article = render_article(indexed_story, "zh", f"Run50-West-Virginia-Marathon-clean_files/")
    write_clean(zh_path, normal_page("zh", zh_article))

    print("Rendering English Page...")
    en_article = render_article(indexed_story, "en", f"../chinese/Run50-West-Virginia-Marathon-clean_files/")
    write_clean(en_path, normal_page("en", en_article))

    print("Rendering Facebook Page...")
    fb_article = render_article(indexed_story, "en", f"../stories/chinese/Run50-West-Virginia-Marathon-clean_files/")
    write_clean(fb_path, facebook_page(fb_article))

    print("Generating SVG Thumbnail Cover...")
    write_svg()

    print("Generating PNG OpenGraph Cover...")
    write_png()

    print("Registering cards on Listing Indexes...")
    update_indexes()

    print("Done! West Virginia Marathon story successfully published.")


if __name__ == "__main__":
    main()
