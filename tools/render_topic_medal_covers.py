from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
W, H = 1200, 750
S = 2


def hx(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))


def rgba(value: str, alpha: int = 255) -> tuple[int, int, int, int]:
    return hx(value) + (alpha,)


def blend(a: str, b: str, t: float) -> tuple[int, int, int]:
    ca, cb = hx(a), hx(b)
    return tuple(round(ca[i] * (1 - t) + cb[i] * t) for i in range(3))


FONT_SETS = {
    "slab": [
        r"C:\Windows\Fonts\ROCKEB.TTF",
        r"C:\Windows\Fonts\ROCKB.TTF",
        r"C:\Windows\Fonts\georgiab.ttf",
        r"C:\Windows\Fonts\cambriab.ttf",
        r"C:\Windows\Fonts\arialbd.ttf",
    ],
    "serif": [
        r"C:\Windows\Fonts\georgiab.ttf",
        r"C:\Windows\Fonts\cambriab.ttf",
        r"C:\Windows\Fonts\ROCKB.TTF",
        r"C:\Windows\Fonts\arialbd.ttf",
    ],
    "sans": [
        r"C:\Windows\Fonts\bahnschrift.ttf",
        r"C:\Windows\Fonts\arialbd.ttf",
        r"C:\Windows\Fonts\segoeuib.ttf",
    ],
}


def font(size: int, kind: str = "slab") -> ImageFont.FreeTypeFont:
    for item in FONT_SETS.get(kind, FONT_SETS["slab"]):
        try:
            return ImageFont.truetype(item, size * S)
        except OSError:
            continue
    return ImageFont.load_default()


def fit_font(
    draw: ImageDraw.ImageDraw,
    text: str,
    max_w: int,
    max_h: int,
    start: int,
    kind: str = "slab",
    min_size: int = 20,
) -> ImageFont.FreeTypeFont:
    for size in range(start, min_size - 1, -2):
        candidate = font(size, kind)
        box = draw.textbbox((0, 0), text, font=candidate, stroke_width=3 * S)
        if box[2] - box[0] <= max_w * S and box[3] - box[1] <= max_h * S:
            return candidate
    return font(min_size, kind)


def scale_box(box: tuple[float, float, float, float]) -> tuple[int, int, int, int]:
    return tuple(round(v * S) for v in box)


def scaled(points: list[tuple[float, float]]) -> list[tuple[int, int]]:
    return [(round(x * S), round(y * S)) for x, y in points]


def rect(
    draw: ImageDraw.ImageDraw,
    box: tuple[float, float, float, float],
    fill: str | tuple[int, int, int, int] | None,
    outline: str | tuple[int, int, int, int] | None = None,
    width: int = 1,
    radius: int = 0,
) -> None:
    draw.rounded_rectangle(
        scale_box(box),
        radius=radius * S,
        fill=fill,
        outline=outline,
        width=width * S,
    )


def ellipse(
    draw: ImageDraw.ImageDraw,
    box: tuple[float, float, float, float],
    fill: str | tuple[int, int, int, int] | None,
    outline: str | tuple[int, int, int, int] | None = None,
    width: int = 1,
) -> None:
    draw.ellipse(scale_box(box), fill=fill, outline=outline, width=width * S)


def line(
    draw: ImageDraw.ImageDraw,
    points: list[tuple[float, float]],
    fill: str | tuple[int, int, int, int],
    width: int = 1,
    joint: str = "curve",
) -> None:
    draw.line(scaled(points), fill=fill, width=width * S, joint=joint)


def polygon(
    draw: ImageDraw.ImageDraw,
    points: list[tuple[float, float]],
    fill: str | tuple[int, int, int, int],
    outline: str | tuple[int, int, int, int] | None = None,
    width: int = 1,
) -> None:
    draw.polygon(scaled(points), fill=fill)
    if outline:
        draw.line(scaled(points + [points[0]]), fill=outline, width=width * S, joint="curve")


def draw_gradient(im: Image.Image, top: str, bottom: str, box: tuple[int, int, int, int]) -> None:
    x0, y0, x1, y1 = [v * S for v in box]
    draw = ImageDraw.Draw(im)
    for y in range(y0, y1):
        t = (y - y0) / max(1, y1 - y0)
        draw.line((x0, y, x1, y), fill=blend(top, bottom, t))


def text_relief(
    draw: ImageDraw.ImageDraw,
    xy: tuple[float, float],
    text: str,
    fnt: ImageFont.FreeTypeFont,
    fill: str,
    stroke: str = "#f8ecd4",
    shadow: str = "#111722",
    sw: int = 3,
    anchor: str | None = None,
) -> None:
    x, y = xy[0] * S, xy[1] * S
    draw.text(
        (x + 6 * S, y + 7 * S),
        text,
        font=fnt,
        fill=shadow,
        stroke_width=sw * S,
        stroke_fill="#514b42",
        anchor=anchor,
    )
    draw.text(
        (x, y),
        text,
        font=fnt,
        fill=fill,
        stroke_width=sw * S,
        stroke_fill=stroke,
        anchor=anchor,
    )
    draw.text(
        (x + 2 * S, y + 2 * S),
        text,
        font=fnt,
        fill="#fff8e7",
        stroke_width=1 * S,
        stroke_fill=fill,
        anchor=anchor,
    )


def centered_relief(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    text: str,
    max_size: int,
    fill: str,
    stroke: str = "#f6e8ca",
    kind: str = "slab",
) -> None:
    x0, y0, x1, y1 = box
    fnt = fit_font(draw, text, x1 - x0 - 28, y1 - y0 - 12, max_size, kind)
    bbox = draw.textbbox((0, 0), text, font=fnt, stroke_width=2 * S)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (x0 * S + x1 * S - tw) // 2
    y = (y0 * S + y1 * S - th) // 2 - 2 * S
    text_relief(draw, (x / S, y / S), text, fnt, fill, stroke, sw=2)


def shadow_shape(im: Image.Image, draw_fn, blur: int = 12, alpha: int = 95) -> None:
    layer = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    draw_fn(d, (0, 0, 0, alpha))
    layer = layer.filter(ImageFilter.GaussianBlur(blur * S))
    im.alpha_composite(layer)


def texture(im: Image.Image, seed: str) -> None:
    rng = random.Random(seed)
    overlay = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    for _ in range(1900):
        x = rng.randrange(58 * S, 1142 * S)
        y = rng.randrange(58 * S, 704 * S)
        alpha = rng.randrange(9, 28)
        color = (255, 255, 255, alpha) if rng.random() < 0.54 else (25, 30, 36, alpha)
        d.point((x, y), fill=color)
    for _ in range(95):
        x = rng.randrange(80, 1110)
        y = rng.randrange(82, 545)
        r = rng.randrange(18, 74)
        ellipse(d, (x, y, x + r, y + r / 2), (255, 255, 255, rng.randrange(5, 14)))
    im.alpha_composite(overlay)


def draw_frame(draw: ImageDraw.ImageDraw, cfg: dict[str, object]) -> None:
    rect(draw, (16, 16, 1184, 734), "#0a0e12", radius=42)
    rect(draw, (23, 22, 1177, 728), "#242832", "#05070a", 4, 38)
    rect(draw, (33, 32, 1167, 718), "#dfe5ea", "#737c87", 4, 32)
    rect(draw, (43, 42, 1157, 708), "#9c7a3f", "#fff2c8", 3, 27)
    rect(draw, (53, 52, 1147, 698), "#18202a", "#11151b", 4, 23)
    rect(draw, (64, 63, 1136, 687), cfg["paper"], "#f8efd7", 3, 18)
    rect(draw, (72, 71, 1128, 679), None, "#202733", 2, 13)

    for cx, cy in [(49, 47), (1151, 47), (49, 703), (1151, 703)]:
        ellipse(draw, (cx - 17, cy - 17, cx + 17, cy + 17), "#f8f4e8", "#222a34", 4)
        ellipse(draw, (cx - 8, cy - 8, cx + 8, cy + 8), "#737d88", "#fff8e8", 2)

    for mirror_x, mirror_y in [(1, 1), (-1, 1), (1, -1), (-1, -1)]:
        ox = 84 if mirror_x == 1 else 1116
        oy = 88 if mirror_y == 1 else 662
        pts = [
            (ox, oy),
            (ox + mirror_x * 40, oy + mirror_y * 18),
            (ox + mirror_x * 70, oy),
            (ox + mirror_x * 28, oy + mirror_y * 42),
            (ox, oy + mirror_y * 72),
        ]
        line(draw, pts, "#c6b28d", 4)
        line(draw, [(x + mirror_x * 8, y) for x, y in pts[:4]], "#fff4d8", 2)


def scene_backdrop(im: Image.Image, cfg: dict[str, object]) -> ImageDraw.ImageDraw:
    draw_gradient(im, cfg["sky1"], cfg["sky2"], (72, 72, 1128, 548))
    d = ImageDraw.Draw(im)
    for y in range(105, 534, 44):
        line(d, [(92, y), (240, y - 12), (392, y + 6), (550, y - 10), (736, y + 5), (912, y - 8), (1110, y + 8)], "#ffffff", 2)
    return d


def draw_clouds(draw: ImageDraw.ImageDraw) -> None:
    for cx, cy, s in [(210, 130, 1.0), (560, 104, 0.82), (910, 142, 0.95)]:
        ellipse(draw, (cx, cy, cx + 72 * s, cy + 36 * s), "#fff4d6", None)
        ellipse(draw, (cx + 35 * s, cy - 18 * s, cx + 112 * s, cy + 32 * s), "#fff8e6", None)
        rect(draw, (cx + 24 * s, cy + 15 * s, cx + 126 * s, cy + 38 * s), "#fff4d6", radius=8)


def draw_flow_route(draw: ImageDraw.ImageDraw, cfg: dict[str, object], points: list[tuple[int, int]] | None = None) -> None:
    pts = points or cfg.get("route", [(120, 498), (285, 452), (455, 500), (625, 438), (792, 498), (948, 445), (1060, 488)])
    color = cfg["route_color"]
    line(draw, [(x + 3, y + 7) for x, y in pts], "#111722", 18)
    line(draw, pts, "#f5e5c2", 23)
    line(draw, pts, color, 15)
    line(draw, pts, "#fff8d8", 4)
    for i, (x, y) in enumerate(pts[1:-1], start=1):
        if i % 2:
            ellipse(draw, (x - 12, y - 12, x + 12, y + 12), "#fff7dc", color, 4)


def draw_checkered_tab(draw: ImageDraw.ImageDraw, x: int = 988, y: int = 360, scale: float = 1.0) -> None:
    line(draw, [(x, y + 126 * scale), (x, y - 12 * scale)], "#1f2630", 6)
    w, h = 130 * scale, 88 * scale
    for r in range(4):
        for c in range(4):
            fill = "#fbf6e6" if (r + c) % 2 == 0 else "#1d2530"
            rect(draw, (x + c * w / 4, y + r * h / 4, x + (c + 1) * w / 4, y + (r + 1) * h / 4), fill)
    rect(draw, (x, y, x + w, y + h), None, "#f4e8ca", 3, 4)


def draw_water_scene(draw: ImageDraw.ImageDraw, im: Image.Image, cfg: dict[str, object]) -> None:
    draw_clouds(draw)
    rect(draw, (72, 402, 1128, 548), cfg["water"], radius=0)
    for y in range(424, 545, 28):
        line(draw, [(92, y), (230, y - 18), (382, y + 5), (540, y - 12), (720, y + 7), (900, y - 8), (1108, y + 5)], "#baf8ef", 4)
    # Main droplet with chrome edge.
    pts = [(470, 124), (610, 294), (610, 388), (560, 460), (470, 476), (382, 460), (330, 388), (330, 294)]
    polygon(draw, pts, "#f7ffff", "#f4e8ca", 8)
    polygon(draw, [(470, 156), (574, 302), (556, 388), (500, 431), (442, 431), (384, 386), (366, 302)], cfg["accent"], "#ffffff", 5)
    ellipse(draw, (430, 250, 506, 334), "#f8ffff", None)
    # Canisters and pipes.
    for x, h, col in [(690, 250, "#e7fbff"), (780, 210, "#cbf3f1"), (870, 260, "#f6f0d8")]:
        rect(draw, (x, 250, x + 70, 250 + h), col, "#ffffff", 5, 24)
        rect(draw, (x + 11, 278, x + 59, 302), cfg["accent"], None, 0, 9)
    line(draw, [(650, 358), (690, 358), (690, 325), (905, 325), (905, 388), (970, 388)], "#f5ead0", 16)
    line(draw, [(650, 358), (690, 358), (690, 325), (905, 325), (905, 388), (970, 388)], cfg["route_color"], 7)
    draw_flow_route(draw, cfg)
    draw_checkered_tab(draw)


def draw_nsf_scene(draw: ImageDraw.ImageDraw, im: Image.Image, cfg: dict[str, object]) -> None:
    draw_clouds(draw)
    draw_flow_route(draw, cfg, [(128, 502), (298, 468), (448, 504), (594, 456), (744, 500), (910, 448), (1050, 486)])
    rect(draw, (368, 120, 695, 482), "#fbf7e9", "#f7e9c7", 8, 24)
    rect(draw, (408, 166, 655, 205), cfg["accent"], None, 0, 10)
    for y, w in [(245, 204), (294, 238), (344, 176)]:
        rect(draw, (412, y, 412 + w, y + 18), "#758861", None, 0, 7)
    ellipse(draw, (638, 302, 820, 484), cfg["badge"], "#f7e9c7", 8)
    ellipse(draw, (670, 334, 788, 452), None, "#dceea4", 7)
    line(draw, [(690, 396), (728, 430), (778, 356)], "#fff8e8", 18)
    rect(draw, (820, 196, 1006, 410), "#e4f0d0", "#fff6d6", 7, 20)
    centered_relief(draw, (832, 220, 994, 292), "ANSI", 44, "#566f36", "#fff5ce")
    centered_relief(draw, (838, 306, 990, 374), "58/53", 40, "#183b36", "#fff5ce")
    draw_checkered_tab(draw, 1000, 372, 0.86)


def draw_ro_scene(draw: ImageDraw.ImageDraw, im: Image.Image, cfg: dict[str, object]) -> None:
    draw_clouds(draw)
    draw_flow_route(draw, cfg, [(118, 505), (275, 450), (440, 506), (594, 456), (746, 500), (910, 444), (1060, 488)])
    rect(draw, (310, 208, 890, 388), "#effcff", "#ffffff", 9, 74)
    ellipse(draw, (284, 214, 376, 382), "#aeeeff", "#ffffff", 7)
    ellipse(draw, (826, 214, 918, 382), "#16466d", "#ffffff", 7)
    rect(draw, (430, 250, 770, 346), "#143c60", "#ffffff", 5, 18)
    for x in range(458, 748, 48):
        line(draw, [(x, 258), (x + 34, 338)], cfg["accent"], 6)
    for x in [202, 960]:
        ellipse(draw, (x, 190, x + 82, 272), "#fff8e9", "#f1dfb8", 7)
        line(draw, [(x + 41, 231), (x + 62, 212)], "#102640", 6)
        line(draw, [(x + 42, 272), (x + 42, 330)], "#f5ead0", 10)
    line(draw, [(152, 300), (292, 300), (292, 298)], "#effcff", 34)
    line(draw, [(910, 300), (1052, 300)], "#effcff", 34)
    line(draw, [(152, 300), (292, 300), (292, 298)], cfg["route_color"], 10)
    line(draw, [(910, 300), (1052, 300)], cfg["route_color"], 10)
    draw_checkered_tab(draw, 1002, 376, 0.82)


def draw_softener_scene(draw: ImageDraw.ImageDraw, im: Image.Image, cfg: dict[str, object], valve: bool = False) -> None:
    draw_clouds(draw)
    draw_flow_route(draw, cfg)
    if valve:
        rect(draw, (382, 202, 786, 392), "#dff7f6", "#ffffff", 8, 38)
        rect(draw, (440, 244, 648, 314), "#172834", "#ffffff", 6, 18)
        rect(draw, (472, 266, 562, 290), cfg["accent"], None, 0, 8)
        for x, col in [(678, cfg["route_color"]), (724, cfg["accent"])]:
            ellipse(draw, (x, 262, x + 36, 298), col, "#ffffff", 4)
        line(draw, [(220, 296), (382, 296)], "#f5ead0", 26)
        line(draw, [(786, 296), (988, 296)], "#f5ead0", 26)
        line(draw, [(220, 296), (382, 296)], cfg["route_color"], 9)
        line(draw, [(786, 296), (988, 296)], cfg["route_color"], 9)
        rect(draw, (522, 392, 646, 505), cfg["badge"], "#ffffff", 7, 34)
        line(draw, [(584, 412), (584, 486)], cfg["accent"], 8)
        line(draw, [(548, 448), (620, 448)], cfg["accent"], 8)
    else:
        for x, h, col in [(380, 330, "#e3fbff"), (534, 360, "#d0f6ed")]:
            rect(draw, (x, 172, x + 112, 172 + h), col, "#ffffff", 8, 42)
            rect(draw, (x + 20, 132, x + 92, 196), "#f8f1d9", "#ffffff", 7, 18)
            rect(draw, (x + 28, 312, x + 84, 440), "#12303e", "#ffffff", 4, 20)
        rng = random.Random(str(cfg["file"]))
        for _ in range(50):
            x = rng.randint(388, 628)
            y = rng.randint(330, 454)
            r = rng.randint(8, 16)
            fill = cfg["accent"] if rng.random() < 0.5 else cfg["route_color"]
            ellipse(draw, (x - r, y - r, x + r, y + r), fill, "#ffffff", 2)
        rect(draw, (734, 286, 904, 502), "#f7ecd0", "#ffffff", 7, 24)
        centered_relief(draw, (756, 320, 882, 390), "SALT", 42, cfg["badge"], "#fff6dc")
    draw_checkered_tab(draw, 1002, 376, 0.82)


def draw_reading_scene(draw: ImageDraw.ImageDraw, im: Image.Image, cfg: dict[str, object], atomic: bool = False) -> None:
    draw_clouds(draw)
    if atomic:
        for angle, col in [(-18, cfg["route_color"]), (28, cfg["accent"]), (72, "#fff4da")]:
            bbox = scale_box((338, 150, 822, 390))
            draw.arc(bbox, angle, angle + 300, fill=col, width=7 * S)
        for x, y in [(796, 194), (388, 342), (720, 378)]:
            ellipse(draw, (x - 14, y - 14, x + 14, y + 14), cfg["accent"], "#ffffff", 4)
    rect(draw, (306, 230, 584, 490), "#fff2dd", "#ffffff", 8, 18)
    polygon(draw, [(445, 228), (586, 268), (586, 490), (445, 450)], "#f1d3ad", "#ffffff", 8)
    line(draw, [(445, 238), (445, 456)], cfg["accent"], 6)
    for y in [282, 322, 362]:
        line(draw, [(338, y), (416, y)], "#80644a", 5)
        line(draw, [(486, y), (544, y)], "#80644a", 5)
    for i, (x, y, col) in enumerate([(650, 238, cfg["accent"]), (704, 278, "#fff2dd"), (760, 228, cfg["route_color"])]):
        rect(draw, (x, y, x + 148, y + 202), col, "#ffffff", 7, 18)
        line(draw, [(x + 22, y + 52), (x + 112, y + 52)], "#533443", 5)
        line(draw, [(x + 22, y + 84), (x + 88, y + 84)], "#533443", 5)
    draw_flow_route(draw, cfg, [(132, 504), (296, 466), (454, 506), (622, 458), (784, 506), (936, 454), (1060, 488)])
    draw_checkered_tab(draw, 1000, 374, 0.84)


def draw_nano_scene(draw: ImageDraw.ImageDraw, im: Image.Image, cfg: dict[str, object], reader: bool = False) -> None:
    draw_clouds(draw)
    ellipse(draw, (350, 110, 780, 540), "#e9f7ff", "#ffffff", 9)
    for r, col in [(360, "#b8fcff"), (300, cfg["route_color"]), (220, cfg["accent"]), (148, "#ffffff")]:
        bbox = scale_box((565 - r / 2, 325 - r / 2, 565 + r / 2, 325 + r / 2))
        draw.arc(bbox, 20, 330, fill=col, width=4 * S)
    rect(draw, (488, 244, 650, 406), "#172044", "#ffffff", 8, 22)
    rect(draw, (522, 278, 616, 372), cfg["route_color"], cfg["accent"], 5, 12)
    for y in [268, 304, 340, 376]:
        line(draw, [(488, y), (430, y)], "#ffffff", 6)
        line(draw, [(650, y), (710, y)], "#ffffff", 6)
    for x in [516, 552, 588, 624]:
        line(draw, [(x, 244), (x, 192)], "#ffffff", 6)
        line(draw, [(x, 406), (x, 456)], "#ffffff", 6)
    for pts in [
        [(160, 448), (262, 448), (262, 382), (386, 382)],
        [(816, 198), (930, 198), (930, 284), (1030, 284)],
        [(788, 466), (896, 466), (896, 408), (1040, 408)],
    ]:
        line(draw, pts, cfg["accent"], 7)
        ellipse(draw, (pts[-1][0] - 9, pts[-1][1] - 9, pts[-1][0] + 9, pts[-1][1] + 9), "#fff7de", cfg["accent"], 3)
    if reader:
        rect(draw, (722, 330, 910, 490), "#fff4dd", "#ffffff", 7, 18)
        polygon(draw, [(816, 332), (912, 362), (912, 490), (816, 462)], "#d7d8ff", "#ffffff", 7)
        line(draw, [(816, 336), (816, 462)], cfg["accent"], 5)
    draw_flow_route(draw, cfg, [(128, 504), (282, 460), (430, 505), (598, 454), (760, 508), (926, 452), (1060, 488)])
    draw_checkered_tab(draw, 1000, 374, 0.84)


def draw_scene(draw: ImageDraw.ImageDraw, im: Image.Image, cfg: dict[str, object]) -> None:
    scene = cfg["scene"]
    if scene == "water":
        draw_water_scene(draw, im, cfg)
    elif scene == "nsf":
        draw_nsf_scene(draw, im, cfg)
    elif scene == "ro":
        draw_ro_scene(draw, im, cfg)
    elif scene == "valve":
        draw_softener_scene(draw, im, cfg, valve=True)
    elif scene == "softener":
        draw_softener_scene(draw, im, cfg)
    elif scene == "atomic":
        draw_reading_scene(draw, im, cfg, atomic=True)
    elif scene == "reading":
        draw_reading_scene(draw, im, cfg)
    elif scene == "nano-reader":
        draw_nano_scene(draw, im, cfg, reader=True)
    else:
        draw_nano_scene(draw, im, cfg)


def draw_badge(draw: ImageDraw.ImageDraw, cfg: dict[str, object]) -> None:
    rect(draw, (820, 86, 1114, 168), "#17202a", "#f3e4bf", 5, 15)
    rect(draw, (832, 98, 1102, 156), cfg["badge"], "#ffffff", 2, 10)
    centered_relief(draw, (842, 101, 1092, 154), cfg["tag"], 32, "#fff0d2", "#2a2220", "sans")


def draw_bottom(draw: ImageDraw.ImageDraw, cfg: dict[str, object]) -> None:
    bar = cfg["bar"]
    shape = cfg.get("bar_shape", "straight")
    if shape == "step":
        pts = [(64, 548), (172, 530), (1028, 530), (1136, 548), (1112, 642), (88, 642)]
    elif shape == "ribbon":
        pts = [(64, 566), (132, 538), (1068, 538), (1136, 566), (1088, 642), (112, 642)]
    else:
        pts = [(64, 548), (1136, 548), (1136, 642), (64, 642)]

    polygon(draw, [(x + 5, y + 7) for x, y in pts], "#0b1017")
    polygon(draw, pts, bar, "#f4e6c4", 7)
    if shape != "straight":
        line(draw, [(142, 557), (1058, 557)], "#ffffff", 3)
    else:
        rect(draw, (82, 562, 1118, 628), None, "#ffffff", 2, 12)

    fnt = fit_font(draw, cfg["bottom"], 775, 72, cfg.get("bottom_size", 66), "slab")
    text_relief(draw, (600, 580), cfg["bottom"], fnt, "#f7ead0", "#9c7a3f", "#101620", 2, anchor="ma")

    rect(draw, (78, 648, 284, 706), cfg["left_fill"], "#f4e7c8", 5, 10)
    centered_relief(draw, (78, 648, 284, 706), cfg["left"], 36, "#fff0d2", "#2b2520", "sans")
    rect(draw, (914, 648, 1124, 706), cfg["right_fill"], "#f4e7c8", 5, 10)
    centered_relief(draw, (914, 648, 1124, 706), cfg["right"], 32, "#fff0d2", "#2b2520", "sans")

    motifs = cfg.get("motifs", ["dot", "dot", "dot"])
    x = 390
    for motif in motifs:
        if motif == "drop":
            polygon(draw, [(x, 653), (x + 22, 682), (x, 699), (x - 22, 682)], cfg["accent"], "#fff2d5", 3)
        elif motif == "chip":
            rect(draw, (x - 18, 664, x + 18, 700), cfg["accent"], "#fff2d5", 3, 6)
            for dx in [-30, 30]:
                line(draw, [(x + dx, 673), (x + dx / 2, 673)], "#fff2d5", 3)
                line(draw, [(x + dx, 690), (x + dx / 2, 690)], "#fff2d5", 3)
        elif motif == "book":
            rect(draw, (x - 24, 662, x + 8, 700), "#fff2d5", cfg["accent"], 3, 5)
            rect(draw, (x + 8, 662, x + 40, 700), "#e7c28b", cfg["accent"], 3, 5)
        elif motif == "bead":
            for r, col in [(18, cfg["accent"]), (10, cfg["route_color"])]:
                ellipse(draw, (x - r, 681 - r, x + r, 681 + r), col, "#fff2d5", 3)
        else:
            ellipse(draw, (x - 18, 663, x + 18, 699), cfg["accent"], "#fff2d5", 4)
        x += 72
    line(draw, [(330, 676), (x + 20, 676)], "#f6e5c0", 3)


def render(cfg: dict[str, object]) -> Path:
    im = Image.new("RGBA", (W * S, H * S), rgba("#080c10"))
    draw = ImageDraw.Draw(im)
    shadow_shape(im, lambda d, fill: rect(d, (24, 22, 1176, 728), fill, radius=38), 18, 120)
    draw_frame(draw, cfg)
    texture(im, str(cfg["file"]))
    draw = scene_backdrop(im, cfg)
    draw_scene(draw, im, cfg)

    top = cfg["top"]
    top_font = fit_font(draw, top, 410, 118, cfg.get("top_size", 98), "slab", 38)
    text_relief(draw, (90, 86), top, top_font, cfg["top_color"], cfg["top_stroke"], "#101722", 4)
    subtitle = cfg["subtitle"]
    subtitle_font = fit_font(draw, subtitle, 650, 42, 29, "sans", 18)
    draw.text(
        (94 * S, 202 * S),
        subtitle,
        font=subtitle_font,
        fill=hx("#253142"),
        stroke_width=1 * S,
        stroke_fill=hx("#fff4dc"),
    )
    draw_badge(draw, cfg)
    draw_bottom(draw, cfg)
    rect(draw, (64, 63, 1136, 706), None, "#fff6dc", 3, 18)
    rect(draw, (35, 34, 1165, 716), None, "#ffffff", 2, 31)

    im = im.convert("RGB").resize((W, H), Image.Resampling.LANCZOS)
    out = ASSETS / str(cfg["file"])
    im.save(out, "JPEG", quality=94, optimize=True, progressive=True)
    return out


BASE = {
    "paper": "#f4ead8",
    "sky1": "#dff8f2",
    "sky2": "#69c6c0",
    "water": "#1d7f8c",
    "accent": "#efb84d",
    "route_color": "#0da6ad",
    "top_stroke": "#f7e7c8",
    "badge": "#154c57",
    "bar": "#0d2442",
    "left_fill": "#9b2428",
    "right_fill": "#17472f",
    "bar_shape": "straight",
    "motifs": ["drop", "dot", "drop"],
}


COVERS: list[dict[str, object]] = [
    {
        **BASE,
        "file": "thumb-wqa-presentations.jpg",
        "top": "WQA",
        "top_size": 116,
        "top_color": "#0d7f74",
        "subtitle": "2026 PRESENTATIONS - FIELD NOTES - TECH TALKS",
        "tag": "WATER LAB",
        "bottom": "WQA PRESENTATIONS",
        "bottom_size": 58,
        "left": "2026",
        "right": "ZZ WATER",
        "scene": "water",
        "sky1": "#d6fff5",
        "sky2": "#4fb7b1",
        "route_color": "#0aa7b1",
        "accent": "#efb84d",
        "badge": "#0f4d55",
        "bar": "#0a2b42",
        "motifs": ["drop", "drop", "dot", "drop"],
    },
    {
        **BASE,
        "file": "thumb-wqa-expo.jpg",
        "top": "EXPO",
        "top_color": "#b7602d",
        "subtitle": "WQA 2026 - BOOTHS - PRODUCTS - FIELD REPORT",
        "tag": "SHOW FLOOR",
        "bottom": "WQA EXPO",
        "left": "2026",
        "right": "OBSERVE",
        "scene": "water",
        "paper": "#f7ead8",
        "sky1": "#ffe3b8",
        "sky2": "#4fc0b0",
        "water": "#138b92",
        "route_color": "#f07836",
        "accent": "#2bd0c2",
        "top_stroke": "#fff0cd",
        "badge": "#844527",
        "bar": "#103547",
        "left_fill": "#a34523",
        "right_fill": "#0e5b55",
        "bar_shape": "ribbon",
        "motifs": ["drop", "bead", "drop"],
    },
    {
        **BASE,
        "file": "thumb-nsf-standards.jpg",
        "top": "NSF",
        "top_color": "#5b7537",
        "subtitle": "DRINKING WATER - ENDPOINTS - STANDARD LIBRARY",
        "tag": "NSF / ANSI",
        "bottom": "NSF STANDARDS",
        "left": "ANSI",
        "right": "LIBRARY",
        "scene": "nsf",
        "paper": "#eef2d6",
        "sky1": "#eaf6d5",
        "sky2": "#86b46b",
        "water": "#6a9447",
        "route_color": "#e2ac43",
        "accent": "#8fbf55",
        "badge": "#5f773e",
        "bar": "#173826",
        "left_fill": "#7a4f28",
        "right_fill": "#376c35",
        "bar_shape": "step",
        "motifs": ["drop", "dot", "drop", "dot"],
    },
    {
        **BASE,
        "file": "thumb-ro-guide.jpg",
        "top": "RO",
        "top_size": 124,
        "top_color": "#0b67a8",
        "subtitle": "REVERSE OSMOSIS - MEMBRANE - MAINTENANCE",
        "tag": "MEMBRANE",
        "bottom": "REVERSE OSMOSIS",
        "bottom_size": 54,
        "left": "GUIDE",
        "right": "FLOW 01",
        "scene": "ro",
        "paper": "#e9f4ff",
        "sky1": "#d8f8ff",
        "sky2": "#5eafdc",
        "water": "#146c9d",
        "route_color": "#23c8ee",
        "accent": "#f5c85b",
        "top_stroke": "#fff3cf",
        "badge": "#0b4773",
        "bar": "#102844",
        "left_fill": "#0e5f8d",
        "right_fill": "#17513f",
        "bar_shape": "straight",
        "motifs": ["drop", "chip", "drop"],
    },
    {
        **BASE,
        "file": "thumb-ro-system.jpg",
        "top": "RO",
        "top_size": 124,
        "top_color": "#137fae",
        "subtitle": "SYSTEM EXPLAINED - STAGES - FLOW PATH",
        "tag": "CUTAWAY",
        "bottom": "RO SYSTEM",
        "left": "FLOW",
        "right": "WATER 02",
        "scene": "ro",
        "paper": "#e6f7ff",
        "sky1": "#d5fbff",
        "sky2": "#55b7d0",
        "route_color": "#f4c95d",
        "accent": "#63e8ff",
        "badge": "#0d5b7b",
        "bar": "#0c334f",
        "left_fill": "#9b6a25",
        "right_fill": "#11596b",
        "bar_shape": "ribbon",
        "motifs": ["drop", "drop", "chip"],
    },
    {
        **BASE,
        "file": "thumb-softener.jpg",
        "top": "SFT",
        "top_color": "#287f8e",
        "subtitle": "SOFTENER GUIDE - SIZING - CALCULATOR",
        "tag": "ION EXCH.",
        "bottom": "WATER SOFTENER",
        "bottom_size": 56,
        "left": "CALC",
        "right": "WATER 03",
        "scene": "softener",
        "paper": "#e9f2ef",
        "sky1": "#d8fff8",
        "sky2": "#61beb2",
        "water": "#1d8a98",
        "route_color": "#2bbbd0",
        "accent": "#d7a84d",
        "badge": "#1b6f76",
        "bar": "#143245",
        "left_fill": "#987029",
        "right_fill": "#155b62",
        "bar_shape": "step",
        "motifs": ["bead", "bead", "drop", "bead"],
    },
    {
        **BASE,
        "file": "thumb-water-softener.jpg",
        "top": "SFT",
        "top_color": "#2b7287",
        "subtitle": "SOFTENER STUDY - ION EXCHANGE - VALVES",
        "tag": "STUDY HUB",
        "bottom": "SOFTENER STUDY",
        "left": "STUDY",
        "right": "WATER 04",
        "scene": "softener",
        "paper": "#eaf1eb",
        "sky1": "#d8fff7",
        "sky2": "#6ab7b6",
        "water": "#27859b",
        "route_color": "#e4b455",
        "accent": "#62d8d8",
        "badge": "#226974",
        "bar": "#173747",
        "left_fill": "#91692b",
        "right_fill": "#1e5d5d",
        "bar_shape": "ribbon",
        "motifs": ["bead", "drop", "bead"],
    },
    {
        **BASE,
        "file": "thumb-softener-valve-en.jpg",
        "top": "VALVE",
        "top_size": 86,
        "top_color": "#8a6230",
        "subtitle": "FLECK - CLACK - RUNXIN - CONTROL HEADS",
        "tag": "ENGLISH",
        "bottom": "SOFTENER VALVES",
        "bottom_size": 55,
        "left": "EN",
        "right": "VALVE",
        "scene": "valve",
        "paper": "#efe8d8",
        "sky1": "#f1ead4",
        "sky2": "#6ab6b0",
        "route_color": "#2fc0d0",
        "accent": "#efb354",
        "badge": "#7a5528",
        "bar": "#203747",
        "left_fill": "#915c28",
        "right_fill": "#14616a",
        "bar_shape": "step",
        "motifs": ["bead", "chip", "bead"],
    },
    {
        **BASE,
        "file": "thumb-softener-valve-zh.jpg",
        "top": "VALVE",
        "top_size": 86,
        "top_color": "#926333",
        "subtitle": "ION EXCHANGE - COMPETITORS - CHINESE NOTES",
        "tag": "CHINESE",
        "bottom": "SOFTENER VALVES",
        "bottom_size": 55,
        "left": "ZH",
        "right": "VALVE",
        "scene": "valve",
        "paper": "#f1e8d7",
        "sky1": "#f2e0c4",
        "sky2": "#6dc4ae",
        "route_color": "#f0bd62",
        "accent": "#34c9bf",
        "badge": "#875b2e",
        "bar": "#173c42",
        "left_fill": "#946132",
        "right_fill": "#126861",
        "bar_shape": "ribbon",
        "motifs": ["bead", "drop", "chip"],
    },
    {
        **BASE,
        "file": "thumb-ezsalt.jpg",
        "top": "SALT",
        "top_color": "#bc7b2e",
        "subtitle": "EZSALT RESEARCH - PRODUCT STUDY - SOFTENER SALT",
        "tag": "PRODUCT",
        "bottom": "EZSALT RESEARCH",
        "left": "RPT",
        "right": "WATER 05",
        "scene": "softener",
        "paper": "#f4ead6",
        "sky1": "#ffe9c2",
        "sky2": "#61bfb1",
        "water": "#0f9a9c",
        "route_color": "#efc15f",
        "accent": "#34cbc1",
        "badge": "#9a642b",
        "bar": "#193c4d",
        "left_fill": "#a05d25",
        "right_fill": "#14645c",
        "bar_shape": "straight",
        "motifs": ["bead", "bead", "bead", "drop"],
    },
    {
        **BASE,
        "file": "thumb-drop.jpg",
        "top": "DROP",
        "top_color": "#247c68",
        "subtitle": "SMART WATER PLATFORM - CONTROLS - SENSORS",
        "tag": "IOT",
        "bottom": "SMART WATER",
        "left": "IOT",
        "right": "WATER 06",
        "scene": "water",
        "paper": "#e6f2ef",
        "sky1": "#d8fff8",
        "sky2": "#53bfa1",
        "water": "#177d82",
        "route_color": "#63e8ff",
        "accent": "#efba51",
        "badge": "#216b61",
        "bar": "#14363f",
        "left_fill": "#915f24",
        "right_fill": "#175a50",
        "bar_shape": "step",
        "motifs": ["chip", "drop", "chip"],
    },
    {
        **BASE,
        "file": "thumb-reading-home.jpg",
        "top": "READ",
        "top_color": "#8d2f42",
        "subtitle": "NOTES - BOOKS - CARDS - STUDY SYSTEM",
        "tag": "READING",
        "bottom": "READING STUDY",
        "left": "HUB",
        "right": "ZZ LIB",
        "scene": "reading",
        "paper": "#f6e6e1",
        "sky1": "#ffe0d7",
        "sky2": "#b46b82",
        "water": "#8b3f58",
        "route_color": "#8f5aa7",
        "accent": "#e7c565",
        "top_stroke": "#fff0d1",
        "badge": "#7c344d",
        "bar": "#3b233b",
        "left_fill": "#8d2f42",
        "right_fill": "#5a356b",
        "bar_shape": "ribbon",
        "motifs": ["book", "dot", "book"],
    },
    {
        **BASE,
        "file": "thumb-atomic-full.jpg",
        "top": "ATOM",
        "top_color": "#9b2f3d",
        "subtitle": "ATOMIC HABITS - FULL EDITION - NOTES",
        "tag": "BOOK",
        "bottom": "ATOMIC HABITS",
        "left": "FULL",
        "right": "BOOK",
        "scene": "atomic",
        "paper": "#f8e6e1",
        "sky1": "#ffe2d6",
        "sky2": "#bd6b76",
        "route_color": "#7c58a6",
        "accent": "#f3cc62",
        "top_stroke": "#fff2d0",
        "badge": "#8b3442",
        "bar": "#43233d",
        "left_fill": "#9b2f3d",
        "right_fill": "#603776",
        "bar_shape": "step",
        "motifs": ["book", "dot", "book", "dot"],
    },
    {
        **BASE,
        "file": "thumb-atomic-cards.jpg",
        "top": "CARD",
        "top_color": "#803448",
        "subtitle": "HABIT CARDS - BLOOM - STUDY DECK",
        "tag": "DECK",
        "bottom": "HABIT CARDS",
        "left": "DECK",
        "right": "CARDS",
        "scene": "atomic",
        "paper": "#f8e6e3",
        "sky1": "#ffe4dc",
        "sky2": "#b96482",
        "route_color": "#f0c75f",
        "accent": "#8560a7",
        "badge": "#803448",
        "bar": "#4a2842",
        "left_fill": "#7e384b",
        "right_fill": "#6b4578",
        "bar_shape": "straight",
        "motifs": ["book", "book", "dot"],
    },
    {
        **BASE,
        "file": "thumb-nano-ic-prep.jpg",
        "top": "NANO",
        "top_color": "#263e91",
        "subtitle": "IC MANUFACTURING - EQUIPMENT - PROCESS FLOW",
        "tag": "PROCESS",
        "bottom": "NANO IC STUDY",
        "left": "FLOW",
        "right": "SEMI 01",
        "scene": "nano",
        "paper": "#e9ecff",
        "sky1": "#dfe8ff",
        "sky2": "#5d72d8",
        "water": "#3954bd",
        "route_color": "#79f1ff",
        "accent": "#f0c85c",
        "badge": "#293b93",
        "bar": "#171947",
        "left_fill": "#2e3f95",
        "right_fill": "#0f6678",
        "bar_shape": "step",
        "motifs": ["chip", "chip", "dot", "chip"],
    },
    {
        **BASE,
        "file": "thumb-nano-ic-handbook.jpg",
        "top": "IC",
        "top_size": 122,
        "top_color": "#3d2f83",
        "subtitle": "EQUIPMENT HANDBOOK - DETAILED REFERENCE",
        "tag": "REFERENCE",
        "bottom": "EQUIPMENT HANDBOOK",
        "bottom_size": 48,
        "left": "REF",
        "right": "SEMI 02",
        "scene": "nano",
        "paper": "#ebe9ff",
        "sky1": "#eadfff",
        "sky2": "#5b69c7",
        "route_color": "#8bf3ff",
        "accent": "#f3c460",
        "badge": "#43328a",
        "bar": "#191c4b",
        "left_fill": "#43328a",
        "right_fill": "#14657e",
        "bar_shape": "ribbon",
        "motifs": ["chip", "dot", "chip"],
    },
    {
        **BASE,
        "file": "thumb-nano-ic-reader.jpg",
        "top": "PAGE",
        "top_color": "#543184",
        "subtitle": "NANO IC READER - PAGE IMAGE DIRECTORY",
        "tag": "488 PAGES",
        "bottom": "NANO IC READER",
        "left": "PAGE",
        "right": "SEMI 03",
        "scene": "nano-reader",
        "paper": "#ebe8ff",
        "sky1": "#eee0ff",
        "sky2": "#6679ca",
        "route_color": "#96f5ff",
        "accent": "#e9c769",
        "badge": "#543184",
        "bar": "#1d1d4f",
        "left_fill": "#543184",
        "right_fill": "#17627e",
        "bar_shape": "straight",
        "motifs": ["chip", "book", "chip"],
    },
]


def main() -> None:
    for cfg in COVERS:
        out = render(cfg)
        print(f"wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
