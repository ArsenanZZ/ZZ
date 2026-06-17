from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


REPO = Path(__file__).resolve().parents[1]
ASSETS = REPO / "assets"


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


def fit_font(draw, text, max_width, start_size, bold=False, min_size=20):
    size = start_size
    while size >= min_size:
        candidate = font(size, bold)
        width = draw.textbbox((0, 0), text, font=candidate)[2]
        if width <= max_width:
            return candidate
        size -= 2
    return font(min_size, bold)


def draw_badge(draw, box, stop, city, accent):
    x1, y1, x2, y2 = box
    draw.rounded_rectangle(box, radius=22, fill="#ffffff", outline="#20242b", width=7)
    draw.text((x1 + 28, y1 + 26), stop, font=font(40, True), fill="#20242b")
    city_font = fit_font(draw, city, x2 - x1 - 56, 54, True, 34)
    draw.text((x1 + 28, y1 + 78), city, font=city_font, fill=accent)


def write_guilin_png():
    image = Image.new("RGB", (1200, 630), "#f6f8f3")
    draw = ImageDraw.Draw(image)
    draw.text((64, 62), "Guilin Marathon", font=font(62, True), fill="#20242b")
    draw.text((68, 132), "Li River - Karst hills - Heat wave - Family finish", font=font(29), fill="#667085")
    draw_badge(draw, (790, 64, 1110, 206), "RunCN #2", "GUILIN", "#cc0000")
    draw.ellipse((1034, 244, 1126, 336), fill="#f2b441")

    # Mountains stay below the text zone.
    for points, color in [
        ([(42, 474), (132, 258), (246, 474)], "#1f6f5b"),
        ([(214, 480), (360, 226), (536, 480)], "#2f855a"),
        ([(500, 484), (640, 292), (806, 484)], "#236b56"),
        ([(792, 478), (902, 292), (1038, 478)], "#2f855a"),
    ]:
        draw.polygon(points, fill=color)

    draw.polygon(
        [(0, 486), (155, 452), (315, 504), (478, 468), (650, 432), (822, 498), (990, 462), (1110, 474), (1200, 430), (1200, 630), (0, 630)],
        fill="#0f766e",
    )
    draw.polygon(
        [(0, 536), (160, 502), (336, 548), (522, 514), (712, 548), (920, 502), (1104, 516), (1200, 492), (1200, 630), (0, 630)],
        fill="#65b8b2",
    )
    draw.line([(108, 452), (420, 452), (512, 378), (606, 452), (1042, 452)], fill="#7a4f2a", width=20)
    draw.arc((448, 382, 576, 506), 200, 340, fill="#f6f8f3", width=25)
    draw.arc((468, 402, 556, 496), 200, 340, fill="#2f855a", width=18)

    draw.ellipse((238, 505, 342, 609), fill="#d9a441", outline="#8b5e20", width=8)
    draw.ellipse((266, 533, 314, 581), fill="#f6f8f3")
    draw.line([(258, 504), (290, 464), (322, 504)], fill="#8b5e20", width=7)
    image.save(ASSETS / "og-run50-guilin-icons.png", "PNG")


def write_hong_kong_png():
    image = Image.new("RGB", (1200, 630), "#f7f7f2")
    draw = ImageDraw.Draw(image)
    draw.text((64, 58), "Hong Kong Streetathon", font=font(60, True), fill="#20242b")
    draw.text((68, 126), "Tunnels - Harbour - High bridges - 5 a.m. start", font=font(28), fill="#667085")
    draw_badge(draw, (760, 64, 1122, 206), "RunCN #3", "HONG KONG", "#cc0000")
    draw.ellipse((1018, 244, 1110, 336), fill="#f7b733")

    # Skyline, wheel and bridge are anchored below the title zone.
    buildings = [
        (70, 286, 154, 488, "#22324d"),
        (184, 218, 282, 488, "#31496d"),
        (306, 264, 378, 488, "#22324d"),
        (402, 196, 512, 488, "#405a7e"),
        (540, 326, 624, 488, "#22324d"),
        (652, 252, 746, 488, "#31496d"),
    ]
    for x1, y1, x2, y2, color in buildings:
        draw.rectangle((x1, y1, x2, y2), fill=color)
        for wx in range(x1 + 16, x2 - 12, 24):
            for wy in range(y1 + 26, y2 - 18, 34):
                draw.rectangle((wx, wy, wx + 8, wy + 14), fill="#f7d06a")

    draw.ellipse((560, 214, 704, 358), outline="#cc0000", width=12)
    draw.line((632, 214, 632, 358), fill="#cc0000", width=8)
    draw.line((560, 286, 704, 286), fill="#cc0000", width=8)
    draw.arc((110, 392, 560, 590), 195, 345, fill="#f7f7f2", width=24)
    draw.arc((132, 420, 538, 574), 200, 340, fill="#22324d", width=10)
    draw.arc((780, 352, 1080, 588), 190, 350, fill="#c33b2b", width=18)
    draw.line((780, 486, 1080, 486), fill="#c33b2b", width=18)
    draw.polygon([(0, 452), (1200, 452), (1200, 630), (0, 630)], fill="#1f6f8b")
    draw.polygon(
        [(0, 498), (150, 456), (300, 512), (450, 478), (610, 442), (760, 512), (930, 464), (1090, 476), (1200, 432), (1200, 630), (0, 630)],
        fill="#3fb5c4",
    )
    image.save(ASSETS / "og-run50-hong-kong-icons.png", "PNG")


def write_svg_assets():
    (ASSETS / "thumb-run50-guilin-icons.svg").write_text(
        '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 750" role="img" aria-labelledby="title desc">
<title id="title">Guilin Marathon icon cover</title>
<desc id="desc">Icon style cover with Guilin title, RunCN badge, karst hills, Li River, bridge, sun and medal.</desc>
<rect width="1200" height="750" fill="#f6f8f3"/>
<text x="70" y="104" font-family="Arial, Helvetica, sans-serif" font-size="62" font-weight="900" fill="#20242b">Guilin Marathon</text>
<text x="74" y="158" font-family="Arial, Helvetica, sans-serif" font-size="29" font-weight="700" fill="#667085">Li River - Karst hills - Heat wave - Family finish</text>
<rect x="790" y="62" width="320" height="146" rx="22" fill="#ffffff" stroke="#20242b" stroke-width="8"/>
<text x="820" y="122" font-family="Arial, Helvetica, sans-serif" font-size="41" font-weight="900" fill="#20242b">RunCN #2</text>
<text x="820" y="178" font-family="Arial, Helvetica, sans-serif" font-size="55" font-weight="900" fill="#cc0000">GUILIN</text>
<circle cx="1080" cy="290" r="56" fill="#f2b441"/>
<path d="M48 580 C138 330 248 330 338 580 Z" fill="#1f6f5b"/>
<path d="M236 586 C382 274 558 274 704 586 Z" fill="#2f855a"/>
<path d="M582 590 C720 358 886 358 1028 590 Z" fill="#236b56"/>
<path d="M0 602 C160 560 330 626 500 580 C672 532 826 612 990 572 C1080 552 1140 552 1200 520 L1200 750 L0 750 Z" fill="#0f766e"/>
<path d="M0 654 C190 602 340 670 530 628 C720 584 868 670 1040 620 C1115 600 1160 616 1200 592 L1200 750 L0 750 Z" fill="#65b8b2"/>
<path d="M118 548 L430 548 L520 466 L614 548 L1046 548" stroke="#7a4f2a" stroke-width="23" stroke-linecap="round" fill="none"/>
<path d="M456 550 Q520 480 584 550" stroke="#f6f8f3" stroke-width="30" fill="none"/>
<circle cx="286" cy="652" r="55" fill="#d9a441" stroke="#8b5e20" stroke-width="8"/>
<circle cx="286" cy="652" r="25" fill="#f6f8f3"/>
<path d="M254 626 L286 586 L318 626" stroke="#8b5e20" stroke-width="8" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
</svg>''',
        encoding="utf-8",
        newline="\n",
    )
    (ASSETS / "thumb-run50-hong-kong-icons.svg").write_text(
        '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 750" role="img" aria-labelledby="title desc">
<title id="title">Hong Kong Streetathon icon cover</title>
<desc id="desc">Icon style cover with Hong Kong title, RunCN badge, skyline, harbor, bridge, tunnel and Ferris wheel.</desc>
<rect width="1200" height="750" fill="#f7f7f2"/>
<text x="70" y="102" font-family="Arial, Helvetica, sans-serif" font-size="61" font-weight="900" fill="#20242b">Hong Kong Streetathon</text>
<text x="74" y="156" font-family="Arial, Helvetica, sans-serif" font-size="29" font-weight="700" fill="#667085">Tunnels - Harbour - High bridges - 5 a.m. start</text>
<rect x="758" y="62" width="364" height="146" rx="22" fill="#ffffff" stroke="#20242b" stroke-width="8"/>
<text x="790" y="122" font-family="Arial, Helvetica, sans-serif" font-size="41" font-weight="900" fill="#20242b">RunCN #3</text>
<text x="790" y="178" font-family="Arial, Helvetica, sans-serif" font-size="49" font-weight="900" fill="#cc0000">HONG KONG</text>
<circle cx="1076" cy="292" r="56" fill="#f7b733"/>
<rect x="72" y="344" width="84" height="234" fill="#22324d"/>
<rect x="186" y="260" width="98" height="318" fill="#31496d"/>
<rect x="308" y="314" width="72" height="264" fill="#22324d"/>
<rect x="404" y="232" width="112" height="346" fill="#405a7e"/>
<rect x="540" y="388" width="84" height="190" fill="#22324d"/>
<rect x="652" y="306" width="96" height="272" fill="#31496d"/>
<g fill="#f7d06a"><rect x="94" y="374" width="10" height="18"/><rect x="122" y="374" width="10" height="18"/><rect x="214" y="294" width="10" height="18"/><rect x="242" y="294" width="10" height="18"/><rect x="430" y="270" width="10" height="18"/><rect x="462" y="270" width="10" height="18"/><rect x="682" y="340" width="10" height="18"/><rect x="712" y="340" width="10" height="18"/></g>
<circle cx="632" cy="332" r="74" fill="none" stroke="#cc0000" stroke-width="13"/>
<path d="M632 258 L632 406 M558 332 L706 332" stroke="#cc0000" stroke-width="9"/>
<path d="M0 584 L1200 536 L1200 750 L0 750 Z" fill="#1f6f8b"/>
<path d="M0 638 C150 588 300 662 450 620 C610 574 760 650 930 604 C1040 574 1120 590 1200 552 L1200 750 L0 750 Z" fill="#3fb5c4"/>
<path d="M110 600 Q332 486 558 600" stroke="#f7f7f2" stroke-width="27" fill="none"/>
<path d="M138 600 Q334 520 532 600" stroke="#22324d" stroke-width="11" fill="none"/>
<path d="M780 598 Q930 452 1080 598" stroke="#c33b2b" stroke-width="19" fill="none"/>
<path d="M780 598 L1080 598" stroke="#c33b2b" stroke-width="19" stroke-linecap="round"/>
</svg>''',
        encoding="utf-8",
        newline="\n",
    )
    (ASSETS / "thumb-run50-shanghai-vertical-marathon-icons.svg").write_text(
        '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 750" role="img" aria-labelledby="title desc">
<title id="title">Shanghai Tower Vertical Marathon icon cover</title>
<desc id="desc">Icon style cover with Shanghai title, RunCN badge, skyline, river and medal.</desc>
<rect width="1200" height="750" fill="#faf5f0"/>
<text x="70" y="104" font-family="Arial, Helvetica, sans-serif" font-size="62" font-weight="900" fill="#20242b">Shanghai Vertical Marathon</text>
<text x="74" y="158" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="700" fill="#667085">Shanghai Tower · 119 floors · 3,398 steps · 632m</text>
<rect x="790" y="62" width="320" height="146" rx="22" fill="#ffffff" stroke="#20242b" stroke-width="8"/>
<text x="820" y="122" font-family="Arial, Helvetica, sans-serif" font-size="41" font-weight="900" fill="#20242b">RunCN #4</text>
<text x="820" y="178" font-family="Arial, Helvetica, sans-serif" font-size="52" font-weight="900" fill="#cc0000">SHANGHAI</text>
<circle cx="1030" cy="290" r="56" fill="#f7b733"/>

<rect x="238" y="300" width="14" height="280" fill="#2c3e50"/>
<circle cx="245" cy="480" r="32" fill="#cc2424"/>
<circle cx="245" cy="380" r="18" fill="#cc2424"/>
<line x1="245" y1="200" x2="245" y2="300" stroke="#2c3e50" stroke-width="6"/>

<path d="M340 580 L370 280 L430 280 L460 580 Z" fill="#34495e"/>
<rect x="382" y="310" width="36" height="36" fill="#faf5f0"/>

<path d="M500 580 L510 320 L550 320 L560 580 Z" fill="#2c3e50"/>

<path d="M600 580 L640 210 L680 210 L720 580 Z" fill="#4a5e6a"/>
<path d="M600 580 Q660 380 680 210" stroke="#faf5f0" stroke-width="6" fill="none"/>
<path d="M720 580 Q660 380 640 210" stroke="#faf5f0" stroke-width="6" fill="none"/>

<path d="M0 580 L1200 580 L1200 750 L0 750 Z" fill="#2980b9"/>
<path d="M0 620 C200 580 400 660 600 600 C800 540 1000 640 1200 580 L1200 750 L0 750 Z" fill="#3498db"/>

<circle cx="286" cy="652" r="55" fill="#d9a441" stroke="#8b5e20" stroke-width="8"/>
<circle cx="286" cy="652" r="25" fill="#faf5f0"/>
<path d="M254 626 L286 586 L318 626" stroke="#8b5e20" stroke-width="8" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
</svg>''',
        encoding="utf-8",
        newline="\n",
    )


def write_shanghai_png():
    image = Image.new("RGB", (1200, 630), "#faf5f0")
    draw = ImageDraw.Draw(image)
    draw.text((64, 62), "Shanghai Vertical Marathon", font=font(58, True), fill="#20242b")
    draw.text((68, 132), "Shanghai Tower - 119 floors - 3,398 steps - 632m", font=font(28), fill="#667085")
    draw_badge(draw, (790, 64, 1110, 206), "RunCN #4", "SHANGHAI", "#cc0000")
    draw.ellipse((960, 244, 1060, 344), fill="#f7b733")

    # Oriental Pearl Tower
    draw.rectangle((238, 250, 252, 480), fill="#2c3e50")
    draw.ellipse((213, 380, 277, 444), fill="#cc2424")
    draw.ellipse((227, 300, 263, 336), fill="#cc2424")
    draw.line([(245, 170), (245, 250)], fill="#2c3e50", width=6)

    # SWFC
    draw.polygon([(340, 480), (370, 230), (430, 230), (460, 480)], fill="#34495e")
    draw.rectangle((382, 260, 418, 296), fill="#faf5f0")

    # Jin Mao
    draw.polygon([(500, 480), (510, 270), (550, 270), (560, 480)], fill="#2c3e50")

    # Shanghai Tower
    draw.polygon([(600, 480), (640, 160), (680, 160), (720, 480)], fill="#4a5e6a")
    draw.arc((570, 160, 750, 480), 200, 340, fill="#faf5f0", width=6)

    # Ground water
    draw.polygon([(0, 480), (1200, 480), (1200, 630), (0, 630)], fill="#2980b9")
    draw.polygon([(0, 520), (300, 480), (600, 540), (900, 500), (1200, 480), (1200, 630), (0, 630)], fill="#3498db")

    # Medal
    draw.ellipse((238, 505, 342, 609), fill="#d9a441", outline="#8b5e20", width=8)
    draw.ellipse((266, 533, 314, 581), fill="#faf5f0")
    draw.line([(258, 504), (290, 464), (322, 504)], fill="#8b5e20", width=7)

    image.save(ASSETS / "og-run50-shanghai-vertical-marathon-icons.png", "PNG")


def main():
    write_svg_assets()
    write_guilin_png()
    write_hong_kong_png()
    write_shanghai_png()


if __name__ == "__main__":
    main()
