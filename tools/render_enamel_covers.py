from __future__ import annotations

from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"


def text_lines(lines: list[str], x: int, y: int, size: int, gap: int, fill: str = "#fff") -> str:
    parts: list[str] = []
    for i, line in enumerate(lines):
        parts.append(
            f'<text x="{x}" y="{y + i * gap}" text-anchor="middle" '
            f'font-size="{size}" font-weight="900" fill="{fill}" '
            f'letter-spacing="1">{escape(line)}</text>'
        )
    return "\n".join(parts)


def scene_water(cfg: dict[str, str]) -> str:
    return f"""
    <g transform="translate(420 130)" filter="url(#softShadow)">
      <path d="M188 20 C188 20 334 200 334 318 C334 430 264 502 188 502 C112 502 42 430 42 318 C42 200 188 20 188 20 Z" fill="url(#glass)" stroke="#eefcff" stroke-width="10"/>
      <path d="M151 303 C151 252 188 184 188 184 C188 184 225 252 225 303 C225 354 210 385 188 385 C166 385 151 354 151 303 Z" fill="#f8ffff" opacity=".58"/>
      <rect x="-154" y="248" width="188" height="54" rx="27" fill="#d9fbff" opacity=".92" stroke="#ffffff" stroke-width="6"/>
      <rect x="342" y="248" width="182" height="54" rx="27" fill="#d9fbff" opacity=".92" stroke="#ffffff" stroke-width="6"/>
      <path d="M-92 276 C42 246 97 342 188 300 C282 256 354 267 470 276" fill="none" stroke="{cfg['accent']}" stroke-width="12" stroke-linecap="round" opacity=".9"/>
      <g opacity=".92">
        <path d="M-74 348 h78 v92 h-78 z" fill="#e9ffff" opacity=".72" stroke="#fff" stroke-width="6"/>
        <path d="M-58 348 v-42 h46 v42" fill="none" stroke="#fff" stroke-width="8"/>
        <circle cx="-35" cy="394" r="18" fill="{cfg['light']}"/>
        <rect x="420" y="344" width="72" height="112" rx="18" fill="#dffcff" opacity=".74" stroke="#fff" stroke-width="6"/>
        <circle cx="456" cy="382" r="15" fill="{cfg['light']}"/>
        <circle cx="456" cy="420" r="20" fill="{cfg['accent']}" opacity=".72"/>
      </g>
    </g>
    """


def scene_nsf(cfg: dict[str, str]) -> str:
    return f"""
    <g transform="translate(355 120)" filter="url(#softShadow)">
      <rect x="70" y="30" width="360" height="430" rx="28" fill="#f6fbf1" stroke="#ffffff" stroke-width="10"/>
      <rect x="112" y="88" width="276" height="44" rx="12" fill="{cfg['accent']}" opacity=".85"/>
      <rect x="112" y="166" width="94" height="24" rx="10" fill="{cfg['primary']}" opacity=".5"/>
      <rect x="112" y="222" width="228" height="24" rx="10" fill="{cfg['primary']}" opacity=".42"/>
      <rect x="112" y="278" width="176" height="24" rx="10" fill="{cfg['primary']}" opacity=".38"/>
      <circle cx="398" cy="332" r="106" fill="{cfg['title']}" stroke="#ffffff" stroke-width="9"/>
      <circle cx="398" cy="332" r="74" fill="none" stroke="{cfg['light']}" stroke-width="8" opacity=".8"/>
      <path d="M354 333 l29 31 l63 -79" fill="none" stroke="#ffffff" stroke-width="18" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M0 270 C94 214 158 274 250 238 C356 197 445 232 546 172" fill="none" stroke="{cfg['light']}" stroke-width="13" stroke-linecap="round"/>
      <circle cx="74" cy="248" r="18" fill="{cfg['accent']}"/>
      <circle cx="224" cy="242" r="13" fill="#ffffff"/>
      <circle cx="494" cy="194" r="18" fill="{cfg['accent']}"/>
    </g>
    """


def scene_ro(cfg: dict[str, str]) -> str:
    return f"""
    <g transform="translate(270 164)" filter="url(#softShadow)">
      <path d="M20 245 C158 186 276 210 404 254 C520 294 598 286 720 220" fill="none" stroke="{cfg['light']}" stroke-width="34" stroke-linecap="round" opacity=".7"/>
      <path d="M24 255 C164 204 270 220 398 260 C518 298 610 286 716 228" fill="none" stroke="#ffffff" stroke-width="7" stroke-linecap="round" opacity=".8"/>
      <g transform="translate(218 18)">
        <rect x="0" y="78" width="360" height="240" rx="96" fill="url(#tube)" stroke="#f6ffff" stroke-width="12"/>
        <ellipse cx="38" cy="198" rx="46" ry="112" fill="#77e3ff" opacity=".55" stroke="#ffffff" stroke-width="8"/>
        <ellipse cx="322" cy="198" rx="46" ry="112" fill="#092e4f" opacity=".52" stroke="#ffffff" stroke-width="8"/>
        <rect x="86" y="128" width="196" height="140" rx="22" fill="#e9fdff" opacity=".28" stroke="#ffffff" stroke-width="5"/>
        <path d="M111 144 h152 M111 178 h152 M111 212 h152 M111 246 h152" stroke="{cfg['accent']}" stroke-width="8" stroke-linecap="round" opacity=".9"/>
        <path d="M-104 198 H72 M288 198 H480" stroke="#dffcff" stroke-width="44" stroke-linecap="round"/>
        <path d="M-90 198 H76 M290 198 H472" stroke="{cfg['light']}" stroke-width="13" stroke-linecap="round"/>
      </g>
      <circle cx="158" cy="146" r="38" fill="#e9ffff" stroke="#ffffff" stroke-width="7"/>
      <path d="M158 146 l22 -20" stroke="{cfg['title']}" stroke-width="7" stroke-linecap="round"/>
      <path d="M637 268 C705 300 760 328 825 302" fill="none" stroke="{cfg['accent']}" stroke-width="24" stroke-linecap="round" opacity=".8"/>
      <path d="M640 269 C707 297 760 318 819 299" fill="none" stroke="#fff5c8" stroke-width="7" stroke-linecap="round"/>
    </g>
    """


def scene_softener(cfg: dict[str, str]) -> str:
    beads = []
    for i, (x, y, r) in enumerate([(55, 80, 15), (96, 110, 20), (140, 82, 13), (185, 126, 22), (235, 88, 16), (280, 132, 13), (324, 96, 19)]):
        color = cfg["accent"] if i % 2 else cfg["light"]
        beads.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}" stroke="#ffffff" stroke-width="5" opacity=".93"/>')
    return f"""
    <g transform="translate(330 112)" filter="url(#softShadow)">
      <path d="M-120 306 C38 250 102 308 240 286 C356 268 420 214 608 250" fill="none" stroke="#d8fbff" stroke-width="40" stroke-linecap="round" opacity=".7"/>
      <path d="M-112 306 C42 268 108 318 242 292 C362 270 420 232 600 254" fill="none" stroke="{cfg['light']}" stroke-width="12" stroke-linecap="round"/>
      <rect x="188" y="24" width="248" height="468" rx="72" fill="url(#tube)" stroke="#f6ffff" stroke-width="12"/>
      <rect x="224" y="-6" width="176" height="86" rx="22" fill="#dffbff" stroke="#ffffff" stroke-width="9"/>
      <rect x="260" y="18" width="104" height="26" rx="9" fill="{cfg['title']}" opacity=".75"/>
      <rect x="232" y="162" width="160" height="214" rx="28" fill="#102c3a" stroke="#ffffff" stroke-width="7" opacity=".82"/>
      <g transform="translate(206 184)">
        {"".join(beads)}
      </g>
      <path d="M312 158 v214" stroke="#ffffff" stroke-width="8" opacity=".75"/>
      <path d="M282 252 l30 -38 l30 38" fill="none" stroke="{cfg['light']}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>
    </g>
    """


def scene_valve(cfg: dict[str, str]) -> str:
    return f"""
    <g transform="translate(296 128)" filter="url(#softShadow)">
      <path d="M-76 286 C72 226 186 284 310 252 C430 221 548 232 708 182" fill="none" stroke="#d8fbff" stroke-width="38" stroke-linecap="round" opacity=".72"/>
      <path d="M-62 286 C84 246 184 296 312 260 C432 228 550 246 698 194" fill="none" stroke="{cfg['light']}" stroke-width="12" stroke-linecap="round"/>
      <rect x="168" y="104" width="356" height="246" rx="42" fill="url(#tube)" stroke="#f6ffff" stroke-width="12"/>
      <rect x="218" y="150" width="256" height="80" rx="22" fill="#102c3a" stroke="#ffffff" stroke-width="8" opacity=".88"/>
      <rect x="258" y="174" width="118" height="32" rx="10" fill="{cfg['light']}" opacity=".72"/>
      <circle cx="412" cy="190" r="17" fill="{cfg['accent']}" stroke="#ffffff" stroke-width="5"/>
      <circle cx="452" cy="190" r="17" fill="{cfg['primary']}" stroke="#ffffff" stroke-width="5"/>
      <g stroke="#ffffff" stroke-width="9" stroke-linecap="round" opacity=".92">
        <path d="M168 226 H30"/>
        <path d="M524 226 H670"/>
        <path d="M346 350 V464"/>
      </g>
      <rect x="262" y="360" width="168" height="118" rx="38" fill="{cfg['title']}" stroke="#ffffff" stroke-width="9" opacity=".82"/>
      <path d="M302 420 h88 M346 382 v76" stroke="{cfg['light']}" stroke-width="9" stroke-linecap="round"/>
      <circle cx="136" cy="226" r="28" fill="#effcff" stroke="#ffffff" stroke-width="7"/>
      <path d="M136 226 l16 -17" stroke="{cfg['title']}" stroke-width="6" stroke-linecap="round"/>
      <circle cx="558" cy="226" r="28" fill="#effcff" stroke="#ffffff" stroke-width="7"/>
      <path d="M558 226 l18 14" stroke="{cfg['title']}" stroke-width="6" stroke-linecap="round"/>
      <g opacity=".88">
        <circle cx="162" cy="384" r="14" fill="{cfg['accent']}" stroke="#ffffff" stroke-width="5"/>
        <circle cx="202" cy="412" r="18" fill="{cfg['light']}" stroke="#ffffff" stroke-width="5"/>
        <circle cx="536" cy="376" r="16" fill="{cfg['accent']}" stroke="#ffffff" stroke-width="5"/>
        <circle cx="580" cy="408" r="13" fill="{cfg['light']}" stroke="#ffffff" stroke-width="5"/>
      </g>
    </g>
    """


def scene_reading(cfg: dict[str, str], atomic: bool = False) -> str:
    orbit = (
        f'<ellipse cx="332" cy="204" rx="190" ry="78" fill="none" stroke="{cfg["light"]}" stroke-width="8" opacity=".8" transform="rotate(-18 332 204)"/>'
        f'<ellipse cx="332" cy="204" rx="190" ry="78" fill="none" stroke="{cfg["accent"]}" stroke-width="6" opacity=".7" transform="rotate(28 332 204)"/>'
        f'<circle cx="498" cy="150" r="15" fill="{cfg["accent"]}" stroke="#fff" stroke-width="5"/>'
    )
    cards = (
        f'<rect x="406" y="246" width="210" height="128" rx="18" fill="#fff6e5" stroke="#ffffff" stroke-width="8" transform="rotate(7 511 310)"/>'
        f'<rect x="372" y="218" width="210" height="128" rx="18" fill="{cfg["light"]}" stroke="#ffffff" stroke-width="8" transform="rotate(-5 477 282)"/>'
        f'<path d="M408 280 h108 M408 314 h80" stroke="{cfg["title"]}" stroke-width="9" stroke-linecap="round" opacity=".45"/>'
    )
    book = (
        f'<path d="M120 156 C190 116 256 124 328 168 v250 C252 378 190 372 120 414 Z" fill="#fff1dc" stroke="#ffffff" stroke-width="9"/>'
        f'<path d="M328 168 C404 124 472 116 546 156 v258 C474 372 404 378 328 418 Z" fill="#f9dfc3" stroke="#ffffff" stroke-width="9"/>'
        f'<path d="M328 170 v246" stroke="{cfg["accent"]}" stroke-width="7" opacity=".75"/>'
        f'<path d="M166 210 h110 M166 246 h92 M378 210 h120 M378 246 h82" stroke="{cfg["title"]}" stroke-width="7" stroke-linecap="round" opacity=".32"/>'
    )
    return f"""
    <g transform="translate(300 128)" filter="url(#softShadow)">
      {orbit if atomic else ""}
      {book}
      {cards if atomic else '<rect x="456" y="266" width="134" height="170" rx="18" fill="' + cfg["accent"] + '" stroke="#ffffff" stroke-width="8" transform="rotate(10 523 351)"/>'}
      <path d="M110 450 C216 406 312 470 420 424 C496 392 560 408 662 372" fill="none" stroke="{cfg['light']}" stroke-width="13" stroke-linecap="round" opacity=".75"/>
    </g>
    """


def scene_nano(cfg: dict[str, str], reader: bool = False) -> str:
    book = ""
    if reader:
        book = f"""
        <path d="M108 250 C176 218 240 222 306 260 v160 C240 390 176 386 108 420 Z" fill="#f2f5ff" stroke="#ffffff" stroke-width="8"/>
        <path d="M306 260 C378 222 444 218 514 250 v170 C444 386 378 390 306 420 Z" fill="#e8dbff" stroke="#ffffff" stroke-width="8"/>
        <path d="M306 260 v160" stroke="{cfg['accent']}" stroke-width="7"/>
        """
    return f"""
    <g transform="translate(290 112)" filter="url(#softShadow)">
      <circle cx="332" cy="238" r="186" fill="url(#wafer)" stroke="#ffffff" stroke-width="11"/>
      <path d="M180 116 C284 220 380 176 490 306" fill="none" stroke="#ffffff" stroke-width="9" opacity=".65"/>
      <path d="M190 344 C292 256 400 310 502 188" fill="none" stroke="{cfg['light']}" stroke-width="8" opacity=".85"/>
      <g stroke="{cfg['accent']}" stroke-width="6" stroke-linecap="round" opacity=".78">
        <path d="M180 238 h86 v-62 h86"/>
        <path d="M246 342 v-66 h132"/>
        <path d="M384 126 v70 h96"/>
        <path d="M418 392 v-72 h92"/>
      </g>
      <rect x="254" y="162" width="164" height="164" rx="22" fill="#161b48" stroke="#ffffff" stroke-width="9"/>
      <rect x="288" y="196" width="96" height="96" rx="12" fill="{cfg['primary']}" opacity=".78" stroke="{cfg['light']}" stroke-width="6"/>
      <g stroke="#ffffff" stroke-width="7" opacity=".88">
        <path d="M252 190 h-34 M252 224 h-34 M252 258 h-34 M252 292 h-34"/>
        <path d="M420 190 h34 M420 224 h34 M420 258 h34 M420 292 h34"/>
        <path d="M284 160 v-34 M318 160 v-34 M352 160 v-34 M386 160 v-34"/>
        <path d="M284 328 v34 M318 328 v34 M352 328 v34 M386 328 v34"/>
      </g>
      {book}
      <path d="M70 470 C214 418 322 480 468 420 C560 382 626 402 720 360" fill="none" stroke="{cfg['light']}" stroke-width="13" stroke-linecap="round" opacity=".8"/>
    </g>
    """


def bottom_ornament(cfg: dict[str, str]) -> str:
    kind = cfg.get("ornament", "wave")
    if kind == "circuit":
        return f"""
        <g stroke="{cfg['light']}" stroke-width="5" stroke-linecap="round" opacity=".7">
          <path d="M198 640 h96 v-34 h82"/>
          <path d="M826 640 h-96 v-34 h-82"/>
          <path d="M360 663 h112 M728 663 h112"/>
          <circle cx="376" cy="606" r="9" fill="{cfg['accent']}" stroke="#fff" stroke-width="4"/>
          <circle cx="648" cy="606" r="9" fill="{cfg['accent']}" stroke="#fff" stroke-width="4"/>
        </g>
        """
    if kind == "cards":
        return f"""
        <g opacity=".78">
          <rect x="190" y="626" width="70" height="44" rx="8" fill="{cfg['accent']}" stroke="#fff" stroke-width="4" transform="rotate(-8 225 648)"/>
          <rect x="284" y="628" width="70" height="44" rx="8" fill="{cfg['light']}" stroke="#fff" stroke-width="4" transform="rotate(6 319 650)"/>
          <rect x="850" y="626" width="70" height="44" rx="8" fill="{cfg['accent']}" stroke="#fff" stroke-width="4" transform="rotate(8 885 648)"/>
          <path d="M386 652 h112 M702 652 h112" stroke="#fff" stroke-width="5" stroke-linecap="round" opacity=".6"/>
        </g>
        """
    if kind == "beads":
        circles = []
        for i, x in enumerate([205, 244, 284, 896, 936, 976]):
            circles.append(f'<circle cx="{x}" cy="650" r="{13 + (i % 3) * 3}" fill="{cfg["accent"] if i % 2 else cfg["light"]}" stroke="#fff" stroke-width="4" opacity=".86"/>')
        return f'<g>{"".join(circles)}<path d="M350 652 h156 M694 652 h156" stroke="#fff" stroke-width="5" stroke-linecap="round" opacity=".56"/></g>'
    return f"""
    <g opacity=".75">
      <path d="M178 650 C250 624 318 674 392 646 C472 616 524 662 602 636 C678 610 724 662 804 638 C882 614 934 654 1020 626" fill="none" stroke="{cfg['light']}" stroke-width="8" stroke-linecap="round"/>
      <circle cx="338" cy="646" r="10" fill="{cfg['accent']}" stroke="#fff" stroke-width="4"/>
      <circle cx="862" cy="638" r="10" fill="{cfg['accent']}" stroke="#fff" stroke-width="4"/>
    </g>
    """


def render_cover(cfg: dict[str, str | list[str]]) -> str:
    c = cfg  # short alias
    palette = {
        "primary": c["primary"],
        "secondary": c["secondary"],
        "title": c["title_color"],
        "title2": c["title_color2"],
        "accent": c["accent"],
        "light": c["light"],
    }
    scene_kind = str(c["scene"])
    if scene_kind == "water":
        scene = scene_water(palette)
    elif scene_kind == "nsf":
        scene = scene_nsf(palette)
    elif scene_kind == "ro":
        scene = scene_ro(palette)
    elif scene_kind == "softener":
        scene = scene_softener(palette)
    elif scene_kind == "valve":
        scene = scene_valve(palette)
    elif scene_kind == "reading":
        scene = scene_reading(palette, atomic=False)
    elif scene_kind == "atomic":
        scene = scene_reading(palette, atomic=True)
    elif scene_kind == "nano-reader":
        scene = scene_nano(palette, reader=True)
    else:
        scene = scene_nano(palette, reader=False)

    title_lines = c["title_lines"]
    assert isinstance(title_lines, list)
    title_size = 66 if len(max(title_lines, key=len)) <= 13 else 56
    line_gap = 68 if title_size >= 64 else 58
    title_y = 592 if len(title_lines) == 1 else 566
    code = escape(str(c["code"]))
    tag = escape(str(c["tag"]))
    subtitle = escape(str(c["subtitle"]))
    desc = escape(str(c["desc"]))
    title_desc = escape(" ".join(title_lines))
    panel_path = str(c.get("panel_path", "M104 524 L252 496 H948 L1096 524 L1052 696 H148 Z"))

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 750" role="img" aria-labelledby="title desc">
  <title id="title">{title_desc}</title>
  <desc id="desc">{desc}</desc>
  <defs>
    <linearGradient id="metal" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#fff6d4"/>
      <stop offset="18%" stop-color="#9c7a3d"/>
      <stop offset="36%" stop-color="#f9f2df"/>
      <stop offset="58%" stop-color="#706041"/>
      <stop offset="80%" stop-color="#f6f7f4"/>
      <stop offset="100%" stop-color="#886b36"/>
    </linearGradient>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{c['bg1']}"/>
      <stop offset="56%" stop-color="{c['bg2']}"/>
      <stop offset="100%" stop-color="{c['bg3']}"/>
    </linearGradient>
    <linearGradient id="titleGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{c['title_color']}"/>
      <stop offset="100%" stop-color="{c['title_color2']}"/>
    </linearGradient>
    <linearGradient id="glass" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="48%" stop-color="{c['light']}"/>
      <stop offset="100%" stop-color="{c['primary']}"/>
    </linearGradient>
    <linearGradient id="tube" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#f6ffff"/>
      <stop offset="45%" stop-color="{c['light']}"/>
      <stop offset="100%" stop-color="{c['primary']}"/>
    </linearGradient>
    <radialGradient id="wafer" cx="42%" cy="32%" r="68%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="28%" stop-color="{c['light']}"/>
      <stop offset="58%" stop-color="{c['secondary']}"/>
      <stop offset="100%" stop-color="{c['primary']}"/>
    </radialGradient>
    <filter id="shadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="18" stdDeviation="18" flood-color="#000000" flood-opacity=".34"/>
    </filter>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="12" stdDeviation="10" flood-color="#000000" flood-opacity=".24"/>
    </filter>
    <pattern id="pinstripe" width="44" height="44" patternUnits="userSpaceOnUse" patternTransform="rotate(24)">
      <path d="M0 0 H44" stroke="#ffffff" stroke-width="3" opacity=".08"/>
    </pattern>
  </defs>
  <style>
    text {{ font-family: Inter, "Segoe UI", Arial, sans-serif; }}
  </style>
  <rect width="1200" height="750" fill="#090f12"/>
  <rect x="26" y="24" width="1148" height="702" rx="48" fill="url(#metal)" filter="url(#shadow)"/>
  <rect x="42" y="40" width="1116" height="670" rx="40" fill="#111817"/>
  <rect x="61" y="59" width="1078" height="632" rx="32" fill="url(#bg)"/>
  <rect x="61" y="59" width="1078" height="632" rx="32" fill="url(#pinstripe)"/>
  <path d="M92 102 C248 52 394 88 548 126 C734 172 872 128 1100 80 L1100 260 C912 302 754 276 586 234 C382 184 224 202 92 260 Z" fill="#ffffff" opacity=".08"/>
  <path d="M82 468 C214 418 354 484 496 444 C664 396 836 432 1114 348 L1114 672 H82 Z" fill="#000000" opacity=".14"/>

  <g transform="translate(90 86)" filter="url(#softShadow)">
    <path d="M0 0 H246 L276 36 V144 L246 180 H0 Z" fill="{c['code_fill']}" stroke="url(#metal)" stroke-width="9"/>
    <text x="132" y="116" text-anchor="middle" font-size="{c['code_size']}" font-weight="950" fill="#fff8df" stroke="#0b1114" stroke-width="4" paint-order="stroke">{code}</text>
  </g>

  <g transform="translate(928 92)" opacity=".96">
    <path d="M34 0 H150 L184 34 V116 L150 150 H34 L0 116 V34 Z" fill="{c['badge_fill']}" stroke="url(#metal)" stroke-width="7"/>
    <circle cx="92" cy="56" r="28" fill="{c['accent']}" opacity=".9" stroke="#fff" stroke-width="5"/>
    <path d="M76 56 h32 M92 40 v32" stroke="#0c1214" stroke-width="7" stroke-linecap="round" opacity=".54"/>
    <text x="92" y="120" text-anchor="middle" font-size="21" font-weight="900" fill="#fff8df">{tag}</text>
  </g>

  {scene}

  <g filter="url(#softShadow)">
    <path d="{panel_path}" fill="url(#titleGrad)" stroke="url(#metal)" stroke-width="10" stroke-linejoin="round"/>
    <path d="M168 538 C308 510 418 548 560 528 C720 506 832 524 1032 508" fill="none" stroke="#ffffff" stroke-width="5" opacity=".22"/>
    {text_lines(title_lines, 600, title_y, title_size, line_gap)}
    <text x="600" y="646" text-anchor="middle" font-size="23" font-weight="850" fill="{c['subtitle_color']}" letter-spacing="3">{subtitle}</text>
    {bottom_ornament({**palette, "ornament": str(c.get("ornament", "wave"))})}
  </g>
  <rect x="61" y="59" width="1078" height="632" rx="32" fill="none" stroke="#ffffff" stroke-width="3" opacity=".24"/>
  <rect x="34" y="32" width="1132" height="686" rx="44" fill="none" stroke="#ffffff" stroke-width="4" opacity=".58"/>
</svg>
"""


COVERS: list[dict[str, str | list[str]]] = [
    {
        "file": "thumb-wqa-presentations.svg",
        "code": "WQA",
        "code_size": "76",
        "tag": "NOTES",
        "title_lines": ["WQA 2026", "PRESENTATIONS"],
        "subtitle": "FIELD NOTES • TECH TALKS",
        "desc": "Modern enamel plaque cover for WQA 2026 presentation notes.",
        "scene": "water",
        "ornament": "wave",
        "bg1": "#083436",
        "bg2": "#087f69",
        "bg3": "#17301f",
        "primary": "#18a58e",
        "secondary": "#0f6f7e",
        "light": "#8ef8e4",
        "accent": "#f0b84f",
        "title_color": "#0e7c66",
        "title_color2": "#214f39",
        "code_fill": "#0e554d",
        "badge_fill": "#174338",
        "subtitle_color": "#e6fff7",
    },
    {
        "file": "thumb-wqa-expo.svg",
        "code": "EXPO",
        "code_size": "64",
        "tag": "2026",
        "title_lines": ["WQA EXPO", "OBSERVATION"],
        "subtitle": "BOOTHS • PRODUCTS • FIELD REPORT",
        "desc": "Modern enamel plaque cover for the WQA expo observation report.",
        "scene": "water",
        "ornament": "wave",
        "bg1": "#102e38",
        "bg2": "#0c8f82",
        "bg3": "#5a3a1c",
        "primary": "#21b6a6",
        "secondary": "#0d6f85",
        "light": "#a4fff0",
        "accent": "#ffb35b",
        "title_color": "#b7602d",
        "title_color2": "#0e6b61",
        "code_fill": "#b7602d",
        "badge_fill": "#0d4f58",
        "subtitle_color": "#fff1d7",
    },
    {
        "file": "thumb-nsf-standards.svg",
        "code": "NSF",
        "code_size": "78",
        "tag": "ANSI",
        "title_lines": ["NSF/ANSI", "STANDARDS"],
        "subtitle": "DRINKING WATER • ENDPOINTS",
        "desc": "Modern enamel plaque cover for NSF ANSI drinking-water standards.",
        "scene": "nsf",
        "ornament": "wave",
        "bg1": "#17251d",
        "bg2": "#5f833e",
        "bg3": "#193328",
        "primary": "#7fae52",
        "secondary": "#246850",
        "light": "#c8f299",
        "accent": "#d8aa4a",
        "title_color": "#526d31",
        "title_color2": "#1d5c4f",
        "code_fill": "#536e33",
        "badge_fill": "#263f2e",
        "subtitle_color": "#f8f5d6",
    },
    {
        "file": "thumb-ro-guide.svg",
        "code": "RO",
        "code_size": "94",
        "tag": "GUIDE",
        "title_lines": ["REVERSE", "OSMOSIS"],
        "subtitle": "MEMBRANE • STAGES • MAINTENANCE",
        "desc": "Modern enamel plaque cover for reverse osmosis guide.",
        "scene": "ro",
        "ornament": "wave",
        "bg1": "#061f3b",
        "bg2": "#0b7fb5",
        "bg3": "#062a45",
        "primary": "#147eb8",
        "secondary": "#0d50a1",
        "light": "#7ee9ff",
        "accent": "#f0d56b",
        "title_color": "#07578f",
        "title_color2": "#052b5f",
        "code_fill": "#075b91",
        "badge_fill": "#092b54",
        "subtitle_color": "#e5fbff",
    },
    {
        "file": "thumb-ro-system.svg",
        "code": "RO",
        "code_size": "94",
        "tag": "FLOW",
        "title_lines": ["RO SYSTEM", "EXPLAINED"],
        "subtitle": "FLOW PATH • MEMBRANE CUTAWAY",
        "desc": "Modern enamel plaque cover for a reverse osmosis system explainer.",
        "scene": "ro",
        "ornament": "wave",
        "bg1": "#06223d",
        "bg2": "#0a97c9",
        "bg3": "#102c52",
        "primary": "#1596c4",
        "secondary": "#123d96",
        "light": "#8df4ff",
        "accent": "#ffcc64",
        "title_color": "#084e7d",
        "title_color2": "#0d4368",
        "code_fill": "#0a6b9d",
        "badge_fill": "#0a365a",
        "subtitle_color": "#e7fdff",
    },
    {
        "file": "thumb-softener.svg",
        "code": "SFT",
        "code_size": "78",
        "tag": "CALC",
        "title_lines": ["WATER", "SOFTENER"],
        "subtitle": "GUIDE • SIZING • CALCULATOR",
        "desc": "Modern enamel plaque cover for water softener guide and calculator.",
        "scene": "softener",
        "ornament": "beads",
        "bg1": "#0a3144",
        "bg2": "#269eb4",
        "bg3": "#204238",
        "primary": "#2aa6bd",
        "secondary": "#0b6f8f",
        "light": "#9cefff",
        "accent": "#d6a852",
        "title_color": "#287f8e",
        "title_color2": "#36562d",
        "code_fill": "#1d7382",
        "badge_fill": "#143a48",
        "subtitle_color": "#effcff",
    },
    {
        "file": "thumb-water-softener.svg",
        "code": "SFT",
        "code_size": "78",
        "tag": "STUDY",
        "title_lines": ["SOFTENER", "STUDY"],
        "subtitle": "ION EXCHANGE • VALVES",
        "desc": "Modern enamel plaque cover for water softener study hub.",
        "scene": "softener",
        "ornament": "beads",
        "bg1": "#123042",
        "bg2": "#3aa2a7",
        "bg3": "#4b3a23",
        "primary": "#2aa6bd",
        "secondary": "#0f7284",
        "light": "#b8f3ff",
        "accent": "#e2b75d",
        "title_color": "#2b7287",
        "title_color2": "#7b6131",
        "code_fill": "#277589",
        "badge_fill": "#173944",
        "subtitle_color": "#fff2d4",
    },
    {
        "file": "thumb-softener-valve-en.svg",
        "code": "VALVE",
        "code_size": "54",
        "tag": "EN",
        "title_lines": ["SOFTENER", "VALVES"],
        "subtitle": "FLECK • CLACK • RUNXIN",
        "desc": "Modern enamel plaque cover for softener valve analysis.",
        "scene": "valve",
        "ornament": "beads",
        "bg1": "#0f3245",
        "bg2": "#208aa2",
        "bg3": "#5e4524",
        "primary": "#249ab5",
        "secondary": "#166276",
        "light": "#9cecff",
        "accent": "#e0ad52",
        "title_color": "#8a6230",
        "title_color2": "#1e7284",
        "code_fill": "#8a6230",
        "badge_fill": "#183d4d",
        "subtitle_color": "#fff5d9",
    },
    {
        "file": "thumb-softener-valve-zh.svg",
        "code": "VALVE",
        "code_size": "54",
        "tag": "ZH",
        "title_lines": ["SOFTENER", "VALVES"],
        "subtitle": "ION EXCHANGE • COMPETITORS",
        "desc": "Modern enamel plaque cover for the Chinese softener valve analysis.",
        "scene": "valve",
        "ornament": "beads",
        "bg1": "#12313f",
        "bg2": "#2f9d98",
        "bg3": "#694829",
        "primary": "#2ea7b1",
        "secondary": "#0f7069",
        "light": "#b7fff1",
        "accent": "#f0bd62",
        "title_color": "#906433",
        "title_color2": "#176d69",
        "code_fill": "#906433",
        "badge_fill": "#173c42",
        "subtitle_color": "#fff2d2",
    },
    {
        "file": "thumb-ezsalt.svg",
        "code": "SALT",
        "code_size": "64",
        "tag": "RPT",
        "title_lines": ["EZSALT", "RESEARCH"],
        "subtitle": "SOFTENER SALT • PRODUCT STUDY",
        "desc": "Modern enamel plaque cover for EZsalt research report.",
        "scene": "softener",
        "ornament": "beads",
        "bg1": "#17324b",
        "bg2": "#08a49e",
        "bg3": "#6b4a24",
        "primary": "#0fa9b0",
        "secondary": "#15678a",
        "light": "#defcff",
        "accent": "#efc15f",
        "title_color": "#bc7b2e",
        "title_color2": "#12706b",
        "code_fill": "#bc7b2e",
        "badge_fill": "#173d4f",
        "subtitle_color": "#fff3d0",
    },
    {
        "file": "thumb-drop.svg",
        "code": "DROP",
        "code_size": "62",
        "tag": "IOT",
        "title_lines": ["SMART WATER", "PLATFORM"],
        "subtitle": "CONTROLS • SENSORS • FIELD REPORT",
        "desc": "Modern enamel plaque cover for connected smart water platform research.",
        "scene": "water",
        "ornament": "circuit",
        "bg1": "#102d2c",
        "bg2": "#1f9f7a",
        "bg3": "#1a3a46",
        "primary": "#1aa987",
        "secondary": "#127f93",
        "light": "#89f5ff",
        "accent": "#f1bd55",
        "title_color": "#247c68",
        "title_color2": "#1b4d67",
        "code_fill": "#247c68",
        "badge_fill": "#173b3e",
        "subtitle_color": "#ecfffb",
    },
    {
        "file": "thumb-reading-home.svg",
        "code": "READ",
        "code_size": "62",
        "tag": "HUB",
        "title_lines": ["READING", "STUDY"],
        "subtitle": "NOTES • BOOKS • CARDS",
        "desc": "Modern enamel plaque cover for reading and study hub.",
        "scene": "reading",
        "ornament": "cards",
        "bg1": "#281224",
        "bg2": "#9d3e50",
        "bg3": "#2b253c",
        "primary": "#a24351",
        "secondary": "#6a4a86",
        "light": "#f5c7ca",
        "accent": "#e8c66b",
        "title_color": "#8d2f42",
        "title_color2": "#50315e",
        "code_fill": "#893141",
        "badge_fill": "#3a233b",
        "subtitle_color": "#fff0d4",
    },
    {
        "file": "thumb-atomic-full.svg",
        "code": "ATOM",
        "code_size": "62",
        "tag": "BOOK",
        "title_lines": ["ATOMIC", "HABITS"],
        "subtitle": "FULL EDITION • NOTES",
        "desc": "Modern enamel plaque cover for Atomic Habits full edition.",
        "scene": "atomic",
        "ornament": "cards",
        "bg1": "#2b1228",
        "bg2": "#b24f54",
        "bg3": "#453057",
        "primary": "#b34f54",
        "secondary": "#6f4e8b",
        "light": "#ffd0d1",
        "accent": "#ffd36a",
        "title_color": "#9b2f3d",
        "title_color2": "#5a3468",
        "code_fill": "#9b2f3d",
        "badge_fill": "#41213c",
        "subtitle_color": "#fff2ce",
    },
    {
        "file": "thumb-atomic-cards.svg",
        "code": "CARD",
        "code_size": "60",
        "tag": "DECK",
        "title_lines": ["HABIT", "CARDS"],
        "subtitle": "BLOOM • STUDY DECK",
        "desc": "Modern enamel plaque cover for Atomic Habits study cards.",
        "scene": "atomic",
        "ornament": "cards",
        "bg1": "#301729",
        "bg2": "#bd5c57",
        "bg3": "#5b355f",
        "primary": "#b44d57",
        "secondary": "#7a5a98",
        "light": "#ffd8cf",
        "accent": "#f1c95f",
        "title_color": "#803448",
        "title_color2": "#7b4069",
        "code_fill": "#803448",
        "badge_fill": "#472340",
        "subtitle_color": "#fff1cc",
    },
    {
        "file": "thumb-nano-ic-prep.svg",
        "code": "NANO",
        "code_size": "62",
        "tag": "FLOW",
        "title_lines": ["NANO IC", "STUDY"],
        "subtitle": "EQUIPMENT • PROCESS FLOW",
        "desc": "Modern enamel plaque cover for nano-scale IC manufacturing study notes.",
        "scene": "nano",
        "ornament": "circuit",
        "bg1": "#0b1133",
        "bg2": "#214eb9",
        "bg3": "#42206d",
        "primary": "#245dd6",
        "secondary": "#6a4ad8",
        "light": "#79f1ff",
        "accent": "#f0c85c",
        "title_color": "#263e91",
        "title_color2": "#4a297d",
        "code_fill": "#3d3697",
        "badge_fill": "#171947",
        "subtitle_color": "#e8fbff",
    },
    {
        "file": "thumb-nano-ic-handbook.svg",
        "code": "IC",
        "code_size": "92",
        "tag": "REF",
        "title_lines": ["EQUIPMENT", "HANDBOOK"],
        "subtitle": "DETAILED REFERENCE",
        "desc": "Modern enamel plaque cover for the nano equipment detailed handbook.",
        "scene": "nano",
        "ornament": "circuit",
        "bg1": "#101239",
        "bg2": "#5a38b0",
        "bg3": "#1b506e",
        "primary": "#5634bd",
        "secondary": "#1673b7",
        "light": "#8bf3ff",
        "accent": "#f3c460",
        "title_color": "#3d2f83",
        "title_color2": "#135f7f",
        "code_fill": "#3d2f83",
        "badge_fill": "#171947",
        "subtitle_color": "#effcff",
    },
    {
        "file": "thumb-nano-ic-reader.svg",
        "code": "PAGE",
        "code_size": "60",
        "tag": "488",
        "title_lines": ["NANO IC", "READER"],
        "subtitle": "PAGE IMAGE DIRECTORY",
        "desc": "Modern enamel plaque cover for the Nano IC illustrated reader and page directory.",
        "scene": "nano-reader",
        "ornament": "circuit",
        "bg1": "#121338",
        "bg2": "#7045b8",
        "bg3": "#23486f",
        "primary": "#684bd4",
        "secondary": "#1382b2",
        "light": "#96f5ff",
        "accent": "#e9c769",
        "title_color": "#543184",
        "title_color2": "#165c83",
        "code_fill": "#543184",
        "badge_fill": "#191946",
        "subtitle_color": "#f0fbff",
    },
]


def main() -> None:
    for cfg in COVERS:
        target = ASSETS / str(cfg["file"])
        svg = "\n".join(line.rstrip() for line in render_cover(cfg).splitlines()) + "\n"
        target.write_text(svg, encoding="utf-8", newline="\n")
        print(f"wrote {target.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
