from pathlib import Path
from math import sin, pi

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"

TEXT = "#20242b"
SUBTITLE = "#667085"
RUN50_BLUE = "#0b67c2"
WATER_DARK = "#0f766e"
WATER_LIGHT = "#65b8b2"
SAND = "#f2d2a4"
SUN = "#f2b441"
PALM = "#2f855a"
TRUNK = "#7a4f2a"


def font(size, bold=False):
    fonts = [
        "arialbd.ttf" if bold else "arial.ttf",
        "seguisb.ttf" if bold else "segoeui.ttf",
        "calibrib.ttf" if bold else "calibri.ttf",
    ]
    for name in fonts:
        path = Path("C:/Windows/Fonts") / name
        if path.exists():
            return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default()


def fit_font(draw, text, start_size, max_width, bold=True, min_size=28):
    size = start_size
    while size >= min_size:
        candidate = font(size, bold=bold)
        width = draw.textbbox((0, 0), text, font=candidate)[2]
        if width <= max_width:
            return candidate
        size -= 2
    return font(min_size, bold=bold)


def draw_text(draw, xy, text, fnt, fill):
    draw.text(xy, text, font=fnt, fill=fill)


def draw_badge(draw):
    x, y, w, h = 760, 64, 362, 164
    draw.rounded_rectangle((x, y, x + w, y + h), radius=22, fill="white", outline=TEXT, width=7)
    draw_text(draw, (790, 112), "Run50 #15", font(40, bold=True), TEXT)
    city_font = fit_font(draw, "MIAMI", 50, 302, bold=True, min_size=36)
    draw_text(draw, (790, 166), "MIAMI", city_font, RUN50_BLUE)


def wave_points(width, height, base_y, amp, period, phase=0):
    points = [(0, height)]
    for x in range(0, width + 24, 24):
        y = base_y + amp * sin((x / period) * 2 * pi + phase)
        points.append((x, y))
    points.append((width, height))
    return points


def draw_skyline(draw):
    buildings = [
        (320, 292, 58, 218, "#1e293b"),
        (396, 248, 78, 262, "#2d3748"),
        (494, 322, 70, 188, "#1e3a8a"),
        (584, 286, 56, 224, "#334155"),
        (658, 336, 64, 174, "#1f2937"),
    ]
    for x, y, w, h, color in buildings:
        draw.rectangle((x, y, x + w, y + h), fill=color)
        if x == 396:
            draw.polygon([(x, y), (x + w, y - 38), (x + w, y)], fill=color)
        for wx in range(x + 13, x + w - 10, 25):
            for wy in range(y + 22, y + h - 22, 34):
                draw.rectangle((wx, wy, wx + 11, wy + 16), fill="#f8fafc" if x == 396 else SUN)


def draw_ship(draw):
    draw.polygon([(775, 456), (956, 456), (925, 500), (794, 500)], fill=TEXT)
    draw.rectangle((798, 414, 920, 456), fill="white")
    draw.rectangle((832, 382, 894, 414), fill="white")
    draw.rectangle((852, 358, 875, 382), fill="white")
    draw.rectangle((862, 326, 878, 358), fill=RUN50_BLUE)
    draw.rectangle((862, 326, 878, 334), fill=TEXT)
    for x in (822, 852, 882):
        draw.ellipse((x, 432, x + 8, 440), fill=SUN)


def draw_palm(draw, root, top, scale=1.0):
    rx, ry = root
    tx, ty = top
    draw.line((rx, ry, tx, ty), fill=TRUNK, width=max(6, int(12 * scale)))
    leaves = [
        (-100, -34),
        (-68, -88),
        (-14, -116),
        (50, -106),
        (96, -52),
        (68, 36),
        (-50, 58),
    ]
    for dx, dy in leaves:
        end = (tx + dx * scale, ty + dy * scale)
        ctrl = ((tx + end[0]) / 2, ty + dy * 0.35 * scale)
        draw.line((tx, ty, ctrl[0], ctrl[1], end[0], end[1]), fill=PALM, width=max(5, int(9 * scale)))


def draw_medal(draw):
    cx, cy = 302, 570
    star1 = [(cx - 50, cy), (cx - 16, cy - 16), (cx, cy - 50), (cx + 16, cy - 16), (cx + 50, cy), (cx + 16, cy + 16), (cx, cy + 50), (cx - 16, cy + 16)]
    star2 = [(cx - 36, cy - 36), (cx, cy - 18), (cx + 36, cy - 36), (cx + 18, cy), (cx + 36, cy + 36), (cx, cy + 18), (cx - 36, cy + 36), (cx - 18, cy)]
    draw.polygon(star1, fill="#d9a441", outline="#8b5e20")
    draw.line(star1 + [star1[0]], fill="#8b5e20", width=5)
    draw.polygon(star2, fill="#d9a441", outline="#8b5e20")
    draw.line(star2 + [star2[0]], fill="#8b5e20", width=5)
    draw.ellipse((cx - 27, cy - 27, cx + 27, cy + 27), fill="#f6f8f3", outline="#8b5e20", width=4)
    draw.line((cx, cy + 15, cx, cy - 2), fill=TRUNK, width=3)
    for end in [(cx - 12, cy - 2), (cx - 4, cy - 14), (cx + 12, cy - 2), (cx + 5, cy - 14)]:
        draw.line((cx, cy - 2, end[0], end[1]), fill=PALM, width=3)


def write_png():
    width, height = 1200, 630
    img = Image.new("RGB", (width, height), "#e8f4f8")
    draw = ImageDraw.Draw(img)

    draw_text(draw, (64, 64), "MIAMI", font(66, bold=True), TEXT)
    draw_text(draw, (66, 136), "OCEAN DRIVE TO DOWNTOWN", font(26, bold=True), SUBTITLE)
    draw_badge(draw)

    draw.ellipse((970, 250, 1086, 366), fill=SUN)
    draw.rectangle((0, 510, width, height), fill=SAND)
    draw_skyline(draw)
    draw_ship(draw)
    draw.line((215, 478, 1048, 478), fill=TRUNK, width=21)
    for x in (300, 500, 700, 900):
        draw.line((x, 478, x, 540), fill=TRUNK, width=10)
    draw.polygon(wave_points(width, height, 526, 18, 360, 0.2), fill=WATER_DARK)
    draw.polygon(wave_points(width, height, 578, 16, 330, 1.1), fill=WATER_LIGHT)
    draw_palm(draw, (122, 590), (188, 334), scale=0.9)
    draw_palm(draw, (1092, 596), (1030, 360), scale=0.75)
    draw_medal(draw)

    img.save(ASSETS / "og-run50-miami-icons.png", "PNG")


SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 750" role="img" aria-labelledby="title desc">
  <title id="title">Miami icon cover</title>
  <desc id="desc">Icon style cover with Miami title, fixed Run50 badge, skyline, palms, bridge, cruise ship, sun and medal.</desc>
  <rect width="1200" height="750" fill="#e8f4f8"/>
  <text x="70" y="104" font-family="Arial, Helvetica, sans-serif" font-size="66" font-weight="900" fill="#20242b">MIAMI</text>
  <text x="72" y="150" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="800" fill="#667085">OCEAN DRIVE TO DOWNTOWN</text>
  <rect x="758" y="62" width="364" height="166" rx="22" fill="#ffffff" stroke="#20242b" stroke-width="8"/>
  <text x="790" y="122" font-family="Arial, Helvetica, sans-serif" font-size="41" font-weight="900" fill="#20242b">Run50 #15</text>
  <text x="790" y="182" font-family="Arial, Helvetica, sans-serif" font-size="52" font-weight="900" fill="#0b67c2">MIAMI</text>

  <circle cx="1018" cy="350" r="68" fill="#f2b441"/>
  <rect x="0" y="618" width="1200" height="132" fill="#f2d2a4"/>

  <g>
    <rect x="320" y="340" width="60" height="260" fill="#1e293b"/>
    <rect x="400" y="290" width="82" height="310" fill="#2d3748"/>
    <path d="M400 290 L482 248 L482 290 Z" fill="#2d3748"/>
    <rect x="504" y="370" width="72" height="230" fill="#1e3a8a"/>
    <rect x="598" y="322" width="58" height="278" fill="#334155"/>
    <rect x="678" y="386" width="68" height="214" fill="#1f2937"/>
    <g fill="#f2b441">
      <rect x="334" y="365" width="12" height="18"/><rect x="354" y="365" width="12" height="18"/><rect x="334" y="405" width="12" height="18"/><rect x="354" y="405" width="12" height="18"/><rect x="334" y="445" width="12" height="18"/><rect x="354" y="445" width="12" height="18"/>
      <rect x="518" y="398" width="12" height="18"/><rect x="544" y="398" width="12" height="18"/><rect x="518" y="438" width="12" height="18"/><rect x="544" y="438" width="12" height="18"/>
      <rect x="612" y="350" width="12" height="18"/><rect x="636" y="350" width="12" height="18"/><rect x="612" y="390" width="12" height="18"/><rect x="636" y="390" width="12" height="18"/>
    </g>
    <g fill="#f8fafc" opacity=".9">
      <rect x="416" y="320" width="14" height="22"/><rect x="446" y="320" width="14" height="22"/><rect x="416" y="362" width="14" height="22"/><rect x="446" y="362" width="14" height="22"/><rect x="416" y="404" width="14" height="22"/><rect x="446" y="404" width="14" height="22"/>
    </g>
  </g>

  <g>
    <path d="M780 585 L955 585 L980 548 L760 548 Z" fill="#20242b"/>
    <rect x="795" y="506" width="142" height="42" fill="#ffffff"/>
    <rect x="830" y="472" width="84" height="34" fill="#ffffff"/>
    <rect x="854" y="446" width="44" height="26" fill="#ffffff"/>
    <rect x="872" y="412" width="16" height="34" fill="#0b67c2"/>
    <rect x="872" y="412" width="16" height="8" fill="#20242b"/>
    <circle cx="822" cy="530" r="5" fill="#f2b441"/><circle cx="855" cy="530" r="5" fill="#f2b441"/><circle cx="888" cy="530" r="5" fill="#f2b441"/>
  </g>

  <g>
    <path d="M220 590 L1046 590" stroke="#7a4f2a" stroke-width="23" stroke-linecap="round" fill="none"/>
    <line x1="300" y1="590" x2="300" y2="650" stroke="#7a4f2a" stroke-width="12"/>
    <line x1="500" y1="590" x2="500" y2="650" stroke="#7a4f2a" stroke-width="12"/>
    <line x1="700" y1="590" x2="700" y2="650" stroke="#7a4f2a" stroke-width="12"/>
    <line x1="900" y1="590" x2="900" y2="650" stroke="#7a4f2a" stroke-width="12"/>
  </g>

  <path d="M0 650 C160 610 330 676 500 630 C672 582 826 662 990 622 C1080 602 1140 602 1200 570 L1200 750 L0 750 Z" fill="#0f766e"/>
  <path d="M0 704 C190 652 340 720 530 678 C720 634 868 720 1040 670 C1115 650 1160 666 1200 642 L1200 750 L0 750 Z" fill="#65b8b2"/>

  <g>
    <path d="M120 705 C130 580 170 470 190 390" stroke="#7a4f2a" stroke-width="14" stroke-linecap="round" fill="none"/>
    <path d="M190 390 Q160 340 100 360" stroke="#2f855a" stroke-width="10" stroke-linecap="round" fill="none"/>
    <path d="M190 390 Q170 320 130 300" stroke="#2f855a" stroke-width="10" stroke-linecap="round" fill="none"/>
    <path d="M190 390 Q220 320 260 310" stroke="#2f855a" stroke-width="10" stroke-linecap="round" fill="none"/>
    <path d="M190 390 Q240 350 280 360" stroke="#2f855a" stroke-width="10" stroke-linecap="round" fill="none"/>
    <path d="M190 390 Q220 410 240 450" stroke="#2f855a" stroke-width="10" stroke-linecap="round" fill="none"/>
    <path d="M190 390 Q170 410 130 440" stroke="#2f855a" stroke-width="10" stroke-linecap="round" fill="none"/>
  </g>
  <g>
    <path d="M1090 710 C1080 590 1040 500 1020 430" stroke="#7a4f2a" stroke-width="12" stroke-linecap="round" fill="none"/>
    <path d="M1020 430 Q990 390 930 410" stroke="#2f855a" stroke-width="8" stroke-linecap="round" fill="none"/>
    <path d="M1020 430 Q1000 360 960 340" stroke="#2f855a" stroke-width="8" stroke-linecap="round" fill="none"/>
    <path d="M1020 430 Q1050 360 1090 350" stroke="#2f855a" stroke-width="8" stroke-linecap="round" fill="none"/>
    <path d="M1020 430 Q1070 390 1110 400" stroke="#2f855a" stroke-width="8" stroke-linecap="round" fill="none"/>
    <path d="M1020 430 Q1050 450 1070 490" stroke="#2f855a" stroke-width="8" stroke-linecap="round" fill="none"/>
  </g>

  <g transform="translate(300 690)">
    <path d="M-55 0 L-18 -18 L0 -55 L18 -18 L55 0 L18 18 L0 55 L-18 18 Z" fill="#d9a441" stroke="#8b5e20" stroke-width="7" stroke-linejoin="round"/>
    <path d="M-39 -39 L0 -18 L39 -39 L18 0 L39 39 L0 18 L-39 39 L-18 0 Z" fill="#d9a441" stroke="#8b5e20" stroke-width="7" stroke-linejoin="round"/>
    <circle cx="0" cy="0" r="28" fill="#f6f8f3" stroke="#8b5e20" stroke-width="5"/>
    <path d="M0 15 L0 -2" stroke="#7a4f2a" stroke-width="3" fill="none"/>
    <path d="M0 -2 Q-12 -9 -17 -2 M0 -2 Q-5 -14 0 -17 M0 -2 Q12 -9 17 -2 M0 -2 Q5 -14 0 -17" stroke="#2f855a" stroke-width="3.5" fill="none"/>
  </g>
</svg>
"""


def write_svg():
    (ASSETS / "thumb-run50-miami-icons.svg").write_text(SVG, encoding="utf-8")


def main():
    write_png()
    write_svg()


if __name__ == "__main__":
    main()
