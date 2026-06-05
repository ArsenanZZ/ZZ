from pathlib import Path
from lxml import html
from html import escape
from PIL import Image, ImageDraw, ImageFont, ImageOps
import re


REPO = Path(__file__).resolve().parents[1]
SOURCE_BASE = Path(r"Z:\ZhennanZ Folder\000-Marathon-Story-2024-2025\20251221-Italy-Pisa Marathon\000-Web")
SOURCE_HTML = next(p for p in SOURCE_BASE.iterdir() if p.suffix.lower() == ".html")
SOURCE_FILES = next(p for p in SOURCE_BASE.iterdir() if p.is_dir() and p.name.endswith("_files"))
SITE = "https://arsenanzz.github.io/ZZ"
SLUG = "pisa-marathon"
VERSION = "20260604-1"
OUT_IMG_DIR = REPO / "run50" / "stories" / "chinese" / "RunWorld-Pisa-Marathon-clean_files"


EN_BY_INDEX = {
    5: "Preface",
    6: "# Italy | Why Pisa",
    7: "Pisa, Italy",
    8: "Christmas break at the end of the year, plus New Year's, gave us a nice little stack of days off.",
    9: "If we did nothing with it, it felt like we would be letting the calendar down. The problem was that late December, especially around Christmas, is not exactly marathon season.",
    10: "I scrolled through race calendars for a while. Most of the big ones were already over. Right when I was about to give up, World's Marathons showed me one more option: Pisa Marathon.",
    13: "The timing was perfect, the weekend right before Christmas. And the Leaning Tower of Pisa needs no introduction. It is one of those landmarks everyone recognizes even if they have never been there, the kind of place that lives permanently in school textbooks.",
    14: "Siqi and I talked it over. The dates worked, the city sounded good, and we could use it as an excuse to wander through Italy. Italy has too much culture to go wrong with; in Europe, it is one of those places you can choose with your eyes closed.",
    15: "So the logic became very simple: first Pisa, then Italy. Use a marathon as the excuse, and pick up a little taste, beauty and art education along the way.",
    16: "So what were we waiting for? Visa, flights, hotels. Let's go.",
    20: "# A quick sketch of Italy | Renaissance, football, and pickpockets",
    21: "When people think of Italy, three things usually show up pretty quickly: the Renaissance, football, and... pickpockets.",
    24: "First, the Renaissance.",
    25: "This one does not need much explanation. History books, museums and travel brochures have repeated it a thousand times: Leonardo da Vinci, Michelangelo, Raphael.",
    26: "Stone can become a human body; a ceiling can turn into a universe. Italy feels like this: you walk into almost any city, history is under your feet, and when you look up, art class is already in session.",
    29: "Then there is football.",
    30: "Serie A was once called the little World Cup. It was the era of packed superstar lineups, heavy tactics, big names and serious physical battles.",
    31: "The first European league Chinese TV broadcast in a real systematic way was Serie A. For a lot of Chinese families, weekend nights with the TV on and the commentator shouting a string of hard-to-pronounce names are a very familiar memory.",
    32: "That was my father's generation's memory, and it was also one of my earliest introductions to football.",
    33: "As for the third keyword: pickpockets.",
    34: "That topic is a little delicate. Almost every friend who has been to Italy will warn you before you leave, with the seriousness of someone passing down family wisdom:",
    35: '"Watch your bag." "Zip it up." "Be careful around the metro."',
    36: "I do not love that kind of constant alertness. But it has somehow become part of Italy's texture too. Life still feels loose, normal and lively. People still drink coffee standing up, stroll through streets slowly, and sunlight still lands beautifully on old stone walls.",
    37: "Pisa is a perfect little sample of that feeling. The tower leans, the city does not hurry, tourists keep coming, and life goes on.",
    41: "# Arriving in Pisa | Picking up the bib under the Leaning Tower",
    42: "Getting to Italy, and then to Pisa, was honestly not as easy as the idea sounded. A direct flight was unrealistic and not friendly to the wallet. Siqi checked route after route.",
    43: "In the end we settled on a route that already sounded tiring on paper: Louisville to Chicago, Chicago to Frankfurt, Frankfurt to Florence.",
    44: "By the time we reached Florence it was night, so we stayed there first and took the train to Pisa the next day. On the walk to the station, we took one wrong turn and accidentally ran into a wedding car outside a church: an old car, white flowers, a bride, a church.",
    47: "The train ride was quick. Florence to Pisa felt like a blink. Neither station was huge, and from Pisa Centrale we walked straight to the hotel, less than two kilometers.",
    48: "My first impression of Pisa was that it felt deeply medieval. The streets were not wide, the buildings were not tall, and everywhere there were stones, arches and old window frames. There were even horse carriages in town, as if time had been saved here in one piece.",
    53: "Pisa's beauty is hard to separate from the Arno. The river runs down from the Tuscan hills, through Florence and Pisa, then toward the sea. For hundreds of years, trade, wealth and the city's growth all followed this water.",
    54: "At dusk, when the old buildings reflected on the river, the scene needed no filter to look Italian. Our hotel was right next to the Leaning Tower. More precisely, it was near Piazza dei Miracoli, the Square of Miracles.",
    61: "This area is more than just the tower. Beside it stand the cathedral, the baptistery and a wide green lawn. The buildings line up without fighting for attention, but the tower is always the character you recognize first.",
    68: "The marathon expo was here too. It was small and simple, but the location did all the heavy lifting. You could stand in line for your bib and look up at the Leaning Tower at the same time. During the day it was crowded with tourists; at night, once the crowd thinned and the lights came on, the tower somehow became even more charming.",
    71: "That night we had a proper Italian meal. If you are in Pisa, how could you not eat pizza? Simple toppings, nothing fancy. As for carb strategy, that evening it did not matter.",
    75: "# Pisa Marathon | Under the Tuscan winter sun",
    76: "Pisa Marathon started at 9 a.m. Tuscany in December did not feel as cold as winter is supposed to feel. Once the sun came out, the temperature was just right: short sleeves plus arm sleeves, perfect.",
    79: "The start was around Largo Cocco Griffi, not far from Piazza dei Miracoli. The starting area was not big, and yellow balloons swayed above everyone.",
    80: "Every bib had the runner's national flag printed on it. I looked around on purpose: Japan, Spain, France, the UK, Czechia...",
    83: "It is a smaller marathon, but the field really did come from all over the world. It was not huge either: roughly three thousand for the full, four to five thousand for the half. In a medieval town, that felt like the right limit: lively, but not crushed.",
    88: "Not long after the gun, the pack ran through an old city-wall passage. Ahead was Piazza dei Miracoli: grass, white marble, and in the distance that tower leaning with absolutely no intention of behaving.",
    93: "One turn later, the race officially entered the small city of Pisa. On the right was the Arno; on the left, rows of old buildings. People leaned out from balconies, kids waved, and older residents stood by windows applauding.",
    98: "Soon we crossed the most famous bridge over the Arno here, Ponte Solferino. It was not wide. With enough runners on it, the sound of footsteps bounced off the stone.",
    99: "On the other side of the river stood a small church full of sharp little spires: Chiesa di Santa Maria della Spina. The church is not large, but the details are almost outrageous, as if someone lifted a complete medieval model and set it on the riverbank.",
    102: "Pisa is actually a small city. By around five kilometers, we were already outside the center. The houses got lower, the roads opened up, and murals suddenly appeared on roadside walls.",
    107: "At that moment a sentence popped into my head: Italian artists really did have stars and galaxies inside their heads.",
    112: "The aid stations were straightforward: water, wafers and a little fruit. Nothing stunning, but enough. The volunteers were older on average and not especially fast, but every one of them was serious. This kind of race does not rush you or push you. You just run your own pace, slowly.",
    119: "Farther on, the route went straight into villages and farmland. This was the Piana di Pisa area, the classic Tuscan countryside. Golden straw moved in the wind, the land was flat, and the view opened wide. Honestly, for a second, it reminded me of certain plain-country villages back home in China.",
    126: "There were photographers along the road, and ahead of me some runners were wearing football jerseys. I could not tell which clubs they were, but in Italy, running a marathon in a football shirt makes perfect sense.",
    131: "Around 21K, after passing through a village near Marina di Pisa, we finished a turnaround. Then the road suddenly opened up.",
    132: "A wide stretch of water appeared in front of me. At first I thought it was a large lake. After running a little longer, I realized: wait, this is the sea.",
    135: "In the Middle Ages, Pisa was a major port. It was one of Italy's four great maritime republics, along with Venice, Genoa and Amalfi.",
    136: "Later, as the river silted up and both the Arno and the important Serchio waterway changed course or dried out, the port gradually lost its role. Pisa's power at sea faded with it.",
    141: "Now, running along the coast, the sea was on my left and bright white breakwater stones flashed under the sun. On my right were low buildings and quiet restaurants. In peak season this place is probably lively, but in winter, the whole coastline seemed to belong to the runners.",
    146: "After that we left the seaside and the course brought us inland again. Boat yards, farmland and ponds appeared one after another, so it never felt boring. The Tuscan countryside has a clean, comfortable rhythm.",
    151: "Running through all of this, I suddenly felt that Tuscany's colors matched my red Arsenal shirt really well. It is one of my favorite kits. Back then, the young captain Cesc Fabregas wore it when he first broke through.",
    154: "Now he is a bearded middle-aged manager in Italy, coaching Como, and I am no longer under his spell. But I still love this shirt.",
    157: "When we ran back into Pisa, the medieval buildings returned. We crossed the Arno again, ran along an old riverside street, then turned into a narrow lane in the Borgo Stretto area, one of Pisa's most typical old quarters.",
    164: "At the end of the lane, above a cluster of low buildings, the Leaning Tower suddenly peeked out. Not the whole tower yet, just the first little reveal. The finish was right beside Piazza dei Miracoli.",
    171: "The photographers were very professional. They managed to catch me and the Leaning Tower in the same frame, and no, the tower was not perfectly balanced on top of my head.",
    180: "To be honest, I have always felt that the Leaning Tower of Pisa represents Italy even better than the Colosseum. The Colosseum is power, conquest and cruelty. Pisa is where Galileo dropped iron balls, where human reason began pushing back against authority.",
    181: "One is a bloody spectacle. The other is a turning point of intelligence.",
    182: "The medal this time was gold. On the front, Galileo holds a telescope, with the Leaning Tower and a starry sky behind him. It is not flashy, but it rewards a second look.",
    189: "Siqi waited a long time at the finish, and she got a PR, so congratulations to her. The weather felt perfect while running; once I stopped, it became a little cold. We took a few tourist photos pretending to hold up the tower, took medal photos, and quickly went back to the hotel. Luckily, the hotel really was close.",
    198: "That night we came out for another Italian dinner. The tower still looked steady in the dark, and we even found an angle where it looked even more tilted.",
    204: "# Tourist mode | Learning culture with a medal",
    205: "After Pisa Marathon, we chose the least brain-powered way to handle the rest of Italy: a group tour.",
    206: "We got on the bus in Venice and entered the classic travel mode: sleep on the bus, get off and take photos. To be honest, I usually look down on this mode a little.",
    215: "But mixing it in once in a while is not too bad. Northern Italy cooled down, with gray rain for days. Venice was wet, gray and cold, but still beautiful. Gondolas moved slowly on the water, houses seemed to grow straight out of the canals, and we walked an absurd amount that day. The only mistake was forgetting to take the medal out for photos.",
    224: "Next stop: Milan. Even in rainy weather, the Duomo di Milano still dominated everything. We climbed to the roof. Spires, flying buttresses and white marble filled the view, with the city spread out below. In that moment I suddenly felt that Europeans built churches by turning the act of looking upward into architecture.",
    227: "From the city we returned to the west coast and reached Cinque Terre. Colorful houses stacked along the cliffs, the sea right below. This place is perfect for checking in; beyond that, there is honestly not much else to do.",
    228: "If everything before this was travel, then once we returned to Florence, the real study-abroad mode began: three museums in a row.",
    229: 'I used to be fairly indifferent toward museums. My style was: "walk around, take two photos, done." But these Florence museums hit me hard.',
    232: "Museo Nazionale del Bargello. It is small and not crowded, but its centerpiece is fierce: Donatello's David. Not the later version with explosive muscles, but a boy who has not fully grown yet. The body is not exaggerated, the posture is loose, but the confidence and tension are already there.",
    235: "Galleria dell'Accademia. No need to explain too much: everyone is there for the same person, Michelangelo's David. Only on site did I understand that photos are not even good enough to be a trailer. The proportions, muscles, gaze, that feeling that he is about to move.",
    240: "Galleria degli Uffizi. From the windows of the Uffizi, you can see the dome of Santa Maria del Fiore and the Ponte Vecchio almost perfectly framed.",
    245: "This place is basically the table of contents for the Renaissance. The Birth of Venus and Primavera, two of Botticelli's masterworks and two pillars of Renaissance art, are in the same room. Nearby is Leonardo da Vinci's unfinished Adoration of the Magi.",
    248: "From this point on, art began to move away from a single religious narrative and started talking about humans, nature and thought itself. That is the real force of the Renaissance. At that moment, Siqi and I looked at each other and realized we did not have enough culture loaded. All we could say was: this painting is huge, that sculpture is tall. But we were very sure of one thing: humans really do need art.",
    249: "I still cannot explain clearly how art should be defined, or whose judgment gets to be authoritative. I only felt it directly: beauty.",
    256: "Postscript",
    257: "# New Year's in Rome | Running past the Colosseum",
    258: "Rome, Italy",
    259: "We left the tour in Rome. This was also the final stop of the Italy trip.",
    260: "The line for the Mouth of Truth was long. The influencer-style photo guy working there was extremely skilled, knew exactly how to pose, and could even throw out a few lines in Chinese.",
    265: "As the sun went down, ancient Rome started changing color. The Colosseum area had a powerful sense of fate at dusk. The Colosseum is worth seeing during the day, but at night it becomes a different thing.",
    280: "Birds were not afraid of people. They landed on statues, stone walls and railings as if they had always belonged there, stitching ancient Rome, present-day Rome and tourists into the same frame.",
    291: "The real highlight was the New Year's Rome 10K. The classic routes that are usually packed with tourists were handed over to runners for the day. Siqi and I ran together, past the Colosseum, the Spanish Steps and several obelisks.",
    300: "There were lots of photographers. Having the Colosseum as a running backdrop is not an angle everyone gets. Rome is great; it is just hard to stop worrying about being pickpocketed or getting trapped by bracelet sellers.",
    311: "We walked all over Rome for several days. On the last day of 2025, we somehow had a northeastern Chinese meal in Rome. The restaurant was called Xiao Shenyang. It was not expensive and tasted solid. I even left the owner a good review on Google Maps, and he cheerfully gave us two oranges.",
    316: "On January 1, 2026, we left Rome, connected through Frankfurt, and returned to the United States. That was how the new year began. 2025 was good. 2026 should be even better.",
    317: "- The end -",
    318: "Words | Arsenan",
    319: "Photos | Arsenan",
    320: "Design | Arsenan",
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
        "比萨马拉松 Vlog @Arsenan": "Pisa Marathon Vlog @Arsenan",
        "Pisa Marathon@Photographer": "Pisa Marathon @Photographer",
        "Coloseum": "Colosseum",
    }
    for old, new in replacements.items():
        caption = caption.replace(old, new)
    return caption


def text_for(idx: int, text: str, lang: str) -> str:
    if lang == "zh":
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
    if idx in (7, 258) or text.startswith(("🍕", "🏛️")):
        return f'<p class="place">{escape(value)}</p>'
    if value.startswith("- "):
        return f'<p class="end-mark">{escape(value)}</p>'
    if idx in (318, 319, 320):
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
            alt = caption or ("Pisa Marathon photo" if lang == "en" else "比萨马拉松照片")
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
      --paper: #f3f6ef;
      --surface: #ffffff;
      --ink: #20242b;
      --muted: #667085;
      --line: #d5dfd0;
      --sage: #6f8f71;
      --terracotta: #b24a33;
      --gold: #b7892f;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      background: linear-gradient(180deg, #eaf2e8 0, var(--paper) 360px);
      color: var(--ink);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, "PingFang SC", "Microsoft YaHei", sans-serif;
      line-height: 1.75;
      letter-spacing: 0;
    }
    a { color: inherit; }
    .story-nav {
      max-width: 980px;
      margin: 0 auto;
      padding: 22px 22px 0;
      display: flex;
      justify-content: space-between;
      gap: 12px;
      color: var(--muted);
      font-size: 14px;
    }
    .story-nav a { text-decoration: none; border-bottom: 1px solid transparent; }
    .story-nav a:hover { border-color: currentColor; }
    .page-header {
      max-width: 980px;
      margin: 0 auto;
      padding: 58px 22px 30px;
    }
    .kicker {
      margin: 0 0 14px;
      color: var(--terracotta);
      font-weight: 850;
      font-size: 13px;
      letter-spacing: .12em;
      text-transform: uppercase;
    }
    h1 {
      margin: 0;
      max-width: 850px;
      font-size: clamp(34px, 7vw, 66px);
      line-height: 1;
      letter-spacing: 0;
    }
    .meta {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin: 20px 0 0;
      color: var(--muted);
      font-size: 13px;
      font-weight: 750;
      text-transform: uppercase;
    }
    .meta span {
      padding: 5px 8px;
      background: rgba(255,255,255,.72);
      border: 1px solid var(--line);
    }
    .dek {
      max-width: 720px;
      margin: 22px 0 0;
      color: #344054;
      font-size: 18px;
    }
    .article-shell {
      max-width: 860px;
      margin: 0 auto;
      padding: 4px 22px 44px;
    }
    .article-body {
      max-width: 720px;
      margin: 0 auto;
      font-size: 18px;
    }
    .article-body h2 {
      margin: 42px 0 16px;
      color: #18212b;
      font-size: clamp(25px, 5vw, 38px);
      line-height: 1.18;
      letter-spacing: 0;
    }
    .article-body .section-label {
      color: var(--terracotta);
      font-size: 15px;
      letter-spacing: .12em;
      text-transform: uppercase;
      border-top: 1px solid var(--line);
      padding-top: 24px;
    }
    .article-body p { margin: 0 0 18px; }
    .place {
      color: var(--sage);
      font-weight: 850;
    }
    .article-body figure {
      margin: 28px 0;
    }
    .article-body img {
      display: block;
      width: 100%;
      height: auto;
      border-radius: 8px;
      background: #e1e8dc;
      box-shadow: 0 18px 42px rgba(35, 49, 39, .12);
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
      .page-header { padding-top: 40px; }
      .article-body { font-size: 17px; }
    }
    """


def facebook_css() -> str:
    return """
    :root {
      --red: #cc0000;
      --ink: #111111;
      --muted: #666666;
      --line: #dddddd;
      --soft: #f4f6f0;
      --paper: #ffffff;
      --sage: #6f8f71;
      --terracotta: #b24a33;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      background: var(--paper);
      color: var(--ink);
      font-family: Arial, Helvetica, sans-serif;
      letter-spacing: 0;
    }
    a { color: inherit; }
    .breaking {
      background: #111111;
      color: #ffffff;
      font-size: 13px;
      font-weight: 700;
    }
    .breaking-inner,
    .site-head-inner,
    .article {
      width: min(1120px, calc(100% - 32px));
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
    }
    .site-head-inner {
      min-height: 72px;
    }
    .wordmark {
      color: var(--red);
      font-size: 28px;
      font-weight: 900;
      letter-spacing: 0;
    }
    .section-nav {
      display: flex;
      flex-wrap: wrap;
      gap: 14px;
      color: var(--muted);
      font-size: 13px;
      font-weight: 700;
    }
    .hero {
      padding: 34px 0 22px;
      border-bottom: 1px solid var(--line);
    }
    .label {
      display: inline-flex;
      align-items: center;
      gap: 10px;
      color: var(--red);
      font-size: 13px;
      font-weight: 900;
      letter-spacing: .08em;
      text-transform: uppercase;
    }
    .label::before {
      content: "";
      width: 38px;
      height: 9px;
      background: var(--red);
    }
    h1 {
      margin: 18px 0 14px;
      max-width: 980px;
      font-size: clamp(2.4rem, 7vw, 5.6rem);
      line-height: .92;
      letter-spacing: 0;
    }
    .dek {
      max-width: 760px;
      margin: 0;
      color: #333333;
      font-size: 1.15rem;
      line-height: 1.65;
    }
    .byline {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin-top: 18px;
      color: var(--muted);
      font-size: 13px;
      font-weight: 700;
      text-transform: uppercase;
    }
    .lead-media {
      margin: 28px 0 0;
    }
    .lead-media img {
      display: block;
      width: 100%;
      border-radius: 6px;
      background: var(--soft);
    }
    figcaption {
      margin-top: 8px;
      color: var(--muted);
      font-size: 12px;
    }
    .story-grid {
      display: grid;
      grid-template-columns: 300px minmax(0, 1fr);
      gap: 36px;
      align-items: start;
      padding: 30px 0 50px;
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
      background: #f7f8f4;
      padding: 18px;
      border-radius: 8px;
    }
    .brief-box h2,
    .section-bridge h2 {
      margin: 0 0 12px;
      font-size: 20px;
    }
    dl { margin: 0; display: grid; gap: 16px; }
    dt {
      color: var(--red);
      font-size: 12px;
      font-weight: 900;
      text-transform: uppercase;
      letter-spacing: .08em;
    }
    dd {
      margin: 4px 0 0;
      color: #333333;
      font-size: 14px;
      line-height: 1.55;
    }
    .share-note {
      color: #333333;
      font-size: 14px;
      line-height: 1.6;
    }
    .share-note strong {
      display: block;
      color: var(--red);
      text-transform: uppercase;
      font-size: 12px;
      letter-spacing: .08em;
      margin-bottom: 6px;
    }
    .copy {
      max-width: 760px;
      font-size: 18px;
      line-height: 1.75;
    }
    .copy p { margin: 0 0 18px; }
    .copy h2 {
      margin: 42px 0 16px;
      font-size: clamp(26px, 4vw, 42px);
      line-height: 1.08;
      letter-spacing: 0;
    }
    .copy .section-label {
      color: var(--red);
      font-size: 13px;
      text-transform: uppercase;
      letter-spacing: .12em;
      border-top: 1px solid var(--line);
      padding-top: 24px;
    }
    .copy .place {
      color: var(--sage);
      font-weight: 850;
    }
    .copy figure {
      margin: 28px 0;
    }
    .copy figure img {
      width: 100%;
      display: block;
      border-radius: 6px;
      background: var(--soft);
    }
    .context-note,
    .section-bridge {
      margin: 0 0 28px;
    }
    .context-note p:last-child,
    .section-bridge p:last-child {
      margin-bottom: 0;
    }
    .end-mark,
    .credit-line {
      text-align: center;
      color: var(--muted);
    }
    @media (max-width: 820px) {
      .story-grid { grid-template-columns: 1fr; }
      .rail { position: static; }
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
    title = "RunWorld #第6国｜意大利：比萨马拉松｜在亚平宁上艺术课，在斜塔前锻炼身体" if is_zh else "RunWorld #6 | Italy: Pisa Marathon"
    short = "RunWorld #6 | Pisa Marathon"
    desc = (
        "圣诞假期前的比萨马拉松，穿过斜塔、阿诺河、托斯卡纳乡村和利古里亚海，再一路把奖牌带去威尼斯、米兰、佛罗伦萨和罗马。"
        if is_zh
        else "Race date: December 21, 2025. Pisa Marathon under the Tuscan winter sun, from the Leaning Tower and the Arno to countryside roads, the Ligurian Sea, and an Italy trip through Venice, Milan, Florence and Rome."
    )
    canonical = f"{SITE}/run50/stories/{'chinese' if is_zh else 'english'}/{SLUG}.html"
    other = f"../{'english' if is_zh else 'chinese'}/{SLUG}.html"
    fb = f"../../facebook/{SLUG}.html"
    nav = (
        f'<a href="./index.html">← 中文故事</a><a href="{other}">English</a><a href="{fb}">Facebook</a><a href="../../index.html">Run50</a>'
        if is_zh
        else f'<a href="./index.html">← English Stories</a><a href="{other}">中文</a><a href="{fb}">Facebook</a><a href="../../index.html">Run50</a>'
    )
    meta = (
        "<span>意大利比萨</span><span>2025.12.21</span><span>RunWorld #6</span>"
        if is_zh
        else "<span>Pisa, Italy</span><span>Dec 21, 2025</span><span>RunWorld #6</span>"
    )
    kicker = "RunWorld Stories · Italy" if not is_zh else "RunWorld Stories · 意大利"
    footer = "中文原文页面，英文和 Facebook 版已链接在顶部。" if is_zh else "English version of the Pisa Marathon story. Original Chinese page is linked above."
    locale = "zh-CN" if is_zh else "en"
    page_key = f"run50-pisa-marathon-{'zh' if is_zh else 'en'}"
    mount = f"supabase-comments-pisa-{'zh' if is_zh else 'en'}"
    og_img = f"{SITE}/assets/og-run50-pisa-icons.png"
    return f'''<!doctype html>
<html lang="{'zh-CN' if is_zh else 'en'}">
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
  <meta property="og:locale" content="{'zh_CN' if is_zh else 'en_US'}">
  <meta property="og:locale:alternate" content="{'en_US' if is_zh else 'zh_CN'}">
  <meta property="og:image" content="{og_img}">
  <meta property="og:image:secure_url" content="{og_img}">
  <meta property="og:image:type" content="image/png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="article:author" content="Arsenan">
  <meta property="article:published_time" content="2025-12-21T09:00:00+01:00">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{escape(short)}">
  <meta name="twitter:description" content="{escape(desc)}">
  <meta name="twitter:image" content="{og_img}">
  <link rel="stylesheet" href="../../../assets/zz-engagement.css?v=20260604">
  <style>{page_css()}</style>
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
  {engagement(locale, page_key, mount)}
  <footer class="page-footer">{escape(footer)}</footer>
  <script src="../../../assets/zz-engagement-config.js?v=20260604"></script>
  <script src="../../../assets/zz-engagement.js?v=20260604"></script>
</body>
</html>
'''


def facebook_page(article: str) -> str:
    title = "Pisa turned a marathon into a Tuscan art-school road trip"
    desc = "Race date: December 21, 2025. A Pisa Marathon story that starts at the Leaning Tower, runs through Tuscan countryside and the Ligurian Sea, then keeps going through Venice, Milan, Florence and Rome."
    og_img = f"{SITE}/assets/og-run50-pisa-icons.png"
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Pisa Marathon | Run50 Facebook</title>
  <meta name="description" content="{escape(desc)}">
  <link rel="canonical" href="{SITE}/run50/facebook/{SLUG}.html">
  <meta property="og:title" content="{escape(title)}">
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
  <meta property="article:published_time" content="2025-12-21T09:00:00+01:00">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{escape(title)}">
  <meta name="twitter:description" content="{escape(desc)}">
  <meta name="twitter:image" content="{og_img}">
  <link rel="stylesheet" href="../../assets/zz-engagement.css?v=20260604">
  <style>{facebook_css()}</style>
</head>
<body>
  <div class="breaking"><div class="breaking-inner"><a href="./index.html">Run50 Facebook</a><span>Italy / Pisa / Marathon</span></div></div>
  <header class="site-head"><div class="site-head-inner"><div class="wordmark">Run50</div><nav class="section-nav" aria-label="Story links"><a href="../stories/english/{SLUG}.html">Full English</a><a href="../stories/chinese/{SLUG}.html">中文原文</a><a href="../index.html">Run50</a></nav></div></header>
  <article class="article">
    <section class="hero">
      <span class="label">World / Italy / Marathon</span>
      <h1>{escape(title)}</h1>
      <p class="dek">{escape(desc)}</p>
      <div class="byline"><span>By Arsenan</span><span>Pisa, Italy</span><span>December 21, 2025</span></div>
      <figure class="lead-media"><img src="../../assets/og-run50-pisa-icons.png" alt="Icon-style Pisa Marathon cover"><figcaption>Pisa icon cover with the Leaning Tower, Arno River, Tuscan hills, sea and medal.</figcaption></figure>
    </section>
    <section class="story-grid">
      <aside class="rail">
        <section class="brief-box"><h2>At a glance</h2><dl><div><dt>Race</dt><dd>Pisa Marathon, RunWorld country 6</dd></div><div><dt>Course</dt><dd>Leaning Tower, Arno River, Tuscan villages, Marina di Pisa and the Ligurian Sea, then back to Piazza dei Miracoli.</dd></div><div><dt>What stayed with me</dt><dd>Winter sun, a small international field, the sea appearing halfway through, and a medal that followed us to Venice, Milan, Florence and Rome.</dd></div></dl></section>
        <section class="share-note"><strong>Notes</strong>The comments box is below the story. New comments appear right away.</section>
      </aside>
      <div class="copy full-story">
        {article}
      </div>
    </section>
  </article>
  {engagement("en", "run50-pisa-marathon-facebook-en", "supabase-comments-pisa-facebook-en")}
  <script src="../../assets/zz-engagement-config.js?v=20260604"></script>
  <script src="../../assets/zz-engagement.js?v=20260604"></script>
</body>
</html>
'''


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


def fit_font(draw, text, max_width, start_size, bold=False, min_size=24):
    size = start_size
    while size >= min_size:
        candidate = font(size, bold)
        if draw.textbbox((0, 0), text, font=candidate)[2] <= max_width:
            return candidate
        size -= 2
    return font(min_size, bold)


def write_pisa_png():
    image = Image.new("RGB", (1200, 630), "#eef5ec")
    draw = ImageDraw.Draw(image)
    draw.text((64, 58), "Pisa Marathon", font=font(66, True), fill="#20242b")
    draw.text((68, 132), "Leaning Tower - Tuscan roads - Ligurian Sea", font=font(28), fill="#667085")
    draw.rounded_rectangle((774, 64, 1122, 224), radius=22, fill="#ffffff", outline="#20242b", width=7)
    draw.text((804, 112), "RunWorld #6", font=font(38, True), fill="#20242b")
    draw.text((804, 166), "PISA", font=font(50, True), fill="#b24a33")

    draw.ellipse((1015, 250, 1118, 353), fill="#f2b441")
    draw.rectangle((0, 472, 1200, 630), fill="#5c8d94")
    draw.polygon([(0, 500), (170, 450), (330, 522), (510, 474), (680, 428), (850, 508), (1030, 464), (1200, 430), (1200, 630), (0, 630)], fill="#89b58a")
    draw.polygon([(0, 555), (230, 500), (430, 566), (640, 520), (850, 570), (1040, 518), (1200, 492), (1200, 630), (0, 630)], fill="#d8c78f")
    draw.rectangle((0, 540, 1200, 630), fill="#3f8fa0")
    draw.arc((702, 370, 1084, 618), 192, 350, fill="#ffffff", width=22)
    draw.arc((726, 400, 1060, 610), 200, 340, fill="#b24a33", width=12)

    tower = [(226, 230), (356, 212), (412, 520), (270, 540)]
    draw.polygon(tower, fill="#f7f2df", outline="#20242b")
    for y in [270, 322, 374, 426, 478]:
        draw.line((245, y, 386, y - 18), fill="#b24a33", width=6)
    for x in [265, 300, 335]:
        draw.line((x, 238, x + 52, 528), fill="#20242b", width=3)
    draw.polygon([(206, 530), (436, 502), (454, 536), (224, 564)], fill="#b24a33")
    draw.ellipse((214, 510, 314, 610), fill="#d9a441", outline="#8b5e20", width=8)
    draw.ellipse((244, 540, 284, 580), fill="#eef5ec")
    draw.line((238, 510, 264, 470, 292, 510), fill="#8b5e20", width=7)
    image.save(REPO / "assets" / "og-run50-pisa-icons.png", "PNG")


def write_pisa_svg():
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 750" role="img" aria-labelledby="title desc">
<title id="title">Pisa Marathon icon cover</title>
<desc id="desc">Icon style cover with Pisa title, RunWorld badge, Leaning Tower, Tuscan hills, sea, bridge, sun and medal.</desc>
<rect width="1200" height="750" fill="#eef5ec"/>
<text x="70" y="104" font-family="Arial, Helvetica, sans-serif" font-size="66" font-weight="900" fill="#20242b">Pisa Marathon</text>
<text x="74" y="160" font-family="Arial, Helvetica, sans-serif" font-size="29" font-weight="700" fill="#667085">Leaning Tower - Tuscan roads - Ligurian Sea</text>
<rect x="774" y="62" width="348" height="162" rx="22" fill="#ffffff" stroke="#20242b" stroke-width="8"/>
<text x="804" y="122" font-family="Arial, Helvetica, sans-serif" font-size="41" font-weight="900" fill="#20242b">RunWorld #6</text>
<text x="804" y="176" font-family="Arial, Helvetica, sans-serif" font-size="52" font-weight="900" fill="#b24a33">PISA</text>
<circle cx="1072" cy="292" r="58" fill="#f2b441"/>
<path d="M0 580 C170 530 340 620 510 560 C690 500 850 610 1030 548 C1115 520 1160 520 1200 498 L1200 750 L0 750 Z" fill="#89b58a"/>
<path d="M0 650 C230 590 430 675 640 620 C850 575 1040 640 1200 590 L1200 750 L0 750 Z" fill="#d8c78f"/>
<path d="M0 650 L1200 596 L1200 750 L0 750 Z" fill="#3f8fa0"/>
<path d="M700 648 Q892 500 1084 648" stroke="#ffffff" stroke-width="26" fill="none"/>
<path d="M728 648 Q894 535 1060 648" stroke="#b24a33" stroke-width="13" fill="none"/>
<path d="M230 278 L360 258 L420 638 L270 656 Z" fill="#f7f2df" stroke="#20242b" stroke-width="6"/>
<path d="M246 326 L386 306 M256 386 L396 366 M266 446 L406 426 M276 506 L416 486 M286 566 L426 546" stroke="#b24a33" stroke-width="7"/>
<path d="M268 292 L324 648 M306 286 L366 642 M344 280 L408 638" stroke="#20242b" stroke-width="4"/>
<path d="M206 636 L438 608 L458 646 L224 678 Z" fill="#b24a33"/>
<circle cx="286" cy="654" r="55" fill="#d9a441" stroke="#8b5e20" stroke-width="8"/>
<circle cx="286" cy="654" r="24" fill="#eef5ec"/>
<path d="M254 628 L286 588 L318 628" stroke="#8b5e20" stroke-width="8" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
</svg>'''
    (REPO / "assets" / "thumb-run50-pisa-icons.svg").write_text(svg, encoding="utf-8", newline="\n")


def write_cover_assets():
    write_pisa_svg()
    write_pisa_png()


def main():
    indexed = extract_story()
    image_count = copy_story_images(indexed)

    missing = [
        (idx, event["text"])
        for idx, event in indexed
        if event["type"] == "text"
        and not is_caption(event["text"])
        and not should_skip_text(event["text"])
        and idx not in EN_BY_INDEX
    ]
    if missing:
        raise RuntimeError(f"Missing English translations: {missing[:5]}")

    zh_article = render_article(indexed, "zh", "RunWorld-Pisa-Marathon-clean_files/")
    en_article = render_article(indexed, "en", "../chinese/RunWorld-Pisa-Marathon-clean_files/")

    race_events = [(idx, event) for idx, event in indexed if 75 <= idx < 203]
    backstory_events = [(idx, event) for idx, event in indexed if idx not in {5} and idx < 75]
    post_events = [(idx, event) for idx, event in indexed if idx >= 203]
    fb_article = "\n        ".join([
        '<section class="context-note"><p>Pisa Marathon was the race that made the whole Italy trip happen. On December 21, 2025, a small international field started near the Leaning Tower, crossed the Arno, ran through Tuscan villages, opened suddenly onto the Ligurian Sea, and came back to finish beside Piazza dei Miracoli.</p><p>The rest of the trip became the bonus lap: Venice, Milan, Cinque Terre, Florence museums, Rome at sunset, and one more 10K past the Colosseum on New Year&apos;s Eve.</p></section>',
        render_article(race_events, "en", "../stories/chinese/RunWorld-Pisa-Marathon-clean_files/"),
        '<section class="section-bridge"><h2>How Pisa became the excuse</h2><p>The race was the headline, but the choice started with a very practical December problem: there are not many marathons left around Christmas. Pisa solved the calendar problem and gave us a reason to turn a race weekend into an Italy art lesson.</p></section>',
        render_article(backstory_events, "en", "../stories/chinese/RunWorld-Pisa-Marathon-clean_files/"),
        '<section class="section-bridge"><h2>The medal kept traveling</h2><p>After the marathon, the finisher medal became the prop for the rest of the trip. We carried it through rainy Venice, Milan&apos;s cathedral roof, Florence&apos;s museums, and Rome&apos;s New Year streets.</p></section>',
        render_article(post_events, "en", "../stories/chinese/RunWorld-Pisa-Marathon-clean_files/"),
    ])

    (REPO / "run50" / "stories" / "chinese" / f"{SLUG}.html").write_text(normal_page("zh", zh_article), encoding="utf-8", newline="\n")
    (REPO / "run50" / "stories" / "english" / f"{SLUG}.html").write_text(normal_page("en", en_article), encoding="utf-8", newline="\n")
    (REPO / "run50" / "facebook" / f"{SLUG}.html").write_text(facebook_page(fb_article), encoding="utf-8", newline="\n")
    write_cover_assets()
    print(f"story_events={len(indexed)} images={image_count}")


if __name__ == "__main__":
    main()
