from __future__ import annotations

import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "wechat-run50-map-michigan-21.png"
TMP_HTML = ROOT / "tmp" / "wechat-run50-map-michigan-21.html"
CHROME = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")

STATE_PATHS = {
    "KY": ["Georgia_1_", "Kentucky"],
    "OH": ["Ohio", "West_Virginia_1_"],
    "NY": ["Rhode_Island_1_", "New_York"],
    "CA": ["Arizona"],
    "IN": ["Indiana", "Ohio_1_"],
    "HI": ["ocean_2_"],
    "GA": ["Georgia", "Florida_1_"],
    "CO": ["Texas_1_", "Colorado"],
    "AK": ["ocean_3_"],
    "MO": ["Iowa_1_", "Missouri"],
    "IL": ["Illinois", "Kentucky_1_"],
    "TN": ["Alabama"],
    "WV": ["West_Virginia", "Virginia_1_"],
    "TX": ["Kansas_1_"],
    "FL": ["South_Carolina_1_"],
    "NC": ["Maryland"],
    "AR": ["Tennessee", "Arkansas"],
    "SC": ["South_Carolina", "Indiana_1_"],
    "PA": ["Pensilvania", "New_Jersey_1_"],
    "WI": ["Wisconsin", "Illinois_1_"],
    "MI": ["Michigan", "Ocean"],
}

RUN50_FIRST_21 = [
    "KY",
    "OH",
    "NY",
    "CA",
    "IN",
    "HI",
    "GA",
    "CO",
    "AK",
    "MO",
    "IL",
    "TN",
    "WV",
    "TX",
    "FL",
    "NC",
    "AR",
    "SC",
    "PA",
    "WI",
    "MI",
]


def css_ids(ids: list[str]) -> str:
    return ",".join(f"#us-map-master #map_{item}" for item in ids)


def read_us_svg() -> str:
    text = (ROOT / "run50" / "us-map-svg.js").read_text(encoding="utf-8")
    match = re.search(r"`([\s\S]*)`", text)
    if not match:
        raise RuntimeError("Could not extract US_MAP_SVG")
    return match.group(1)


def build_html() -> str:
    svg = read_us_svg()
    completed_paths = [path for abbr in RUN50_FIRST_21 for path in STATE_PATHS[abbr]]
    michigan_paths = STATE_PATHS["MI"]
    completed_selector = css_ids(completed_paths)
    michigan_selector = css_ids(michigan_paths)
    grand_rapids_x, grand_rapids_y = 1170.64, 387.84

    css = f"""
      html, body {{
        width: 1200px;
        height: 760px;
        margin: 0;
        overflow: hidden;
        background: #f6fbfe;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
      }}
      .canvas {{
        width: 1200px;
        height: 760px;
        box-sizing: border-box;
        padding: 46px 58px 38px;
        background:
          linear-gradient(180deg, rgba(255,255,255,.96), rgba(239,249,253,.98));
      }}
      .eyebrow {{
        margin: 0 0 8px;
        color: #2d6f9f;
        font-size: 24px;
        line-height: 1.2;
        font-weight: 900;
        letter-spacing: 3px;
      }}
      .title {{
        margin: 0;
        color: #12283b;
        font-size: 48px;
        line-height: 1.12;
        font-weight: 900;
        letter-spacing: 0;
      }}
      .subtitle {{
        margin: 13px 0 18px;
        color: #647887;
        font-size: 22px;
        line-height: 1.35;
        font-weight: 600;
        letter-spacing: 0;
      }}
      .map-wrap {{
        position: relative;
        width: 100%;
        height: 505px;
        border-top: 1px solid #d6e7ef;
        padding-top: 14px;
      }}
      svg {{
        width: 100%;
        height: 100%;
        display: block;
      }}
      #us-map-master path[id^="map_"] {{
        fill: #dce8ef !important;
        stroke: #ffffff !important;
        stroke-width: 1.25 !important;
      }}
      #map_USA {{
        fill: #eaf3f8 !important;
        stroke: none !important;
      }}
      {completed_selector} {{
        fill: #69abc9 !important;
        stroke: #ffffff !important;
        stroke-width: 1.45 !important;
        opacity: 1 !important;
      }}
      {michigan_selector} {{
        fill: #1f6f9e !important;
        stroke: #ffffff !important;
        stroke-width: 1.75 !important;
        opacity: 1 !important;
      }}
      .legend {{
        position: absolute;
        left: 18px;
        bottom: 16px;
        display: flex;
        gap: 22px;
        align-items: center;
        color: #5d7080;
        font-size: 18px;
        font-weight: 700;
      }}
      .swatch {{
        display: inline-block;
        width: 20px;
        height: 12px;
        margin-right: 8px;
        border-radius: 999px;
        vertical-align: 1px;
      }}
    """

    overlay = f"""
      <g id="wechat-mi-callout">
        <circle cx="{grand_rapids_x}" cy="{grand_rapids_y}" r="19" fill="rgba(45,111,159,.22)" />
        <circle cx="{grand_rapids_x}" cy="{grand_rapids_y}" r="8.5" fill="#d4a669" stroke="#ffffff" stroke-width="4" />
        <path d="M1195 374 C1243 342 1290 326 1338 318" fill="none" stroke="#2d6f9f" stroke-width="4" stroke-linecap="round" />
        <rect x="1346" y="268" width="248" height="84" rx="18" fill="#ffffff" stroke="#c8dce8" stroke-width="2" />
        <text x="1372" y="303" fill="#2d6f9f" font-size="24" font-weight="900">#21 MICHIGAN</text>
        <text x="1372" y="332" fill="#667a89" font-size="18" font-weight="700">Grand Rapids · Aug 2024</text>
      </g>
    """
    svg = svg.replace("</svg>", overlay + "</svg>")

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<style>{css}</style>
</head>
<body>
  <main class="canvas">
    <p class="eyebrow">RUN50 MAP · STATE 21</p>
    <h1 class="title">Michigan Lights Up the Map</h1>
    <p class="subtitle">21 states completed from Kentucky to Grand Rapids</p>
    <section class="map-wrap">
      {svg}
      <div class="legend">
        <span><span class="swatch" style="background:#69abc9"></span>Completed before/through #21</span>
        <span><span class="swatch" style="background:#1f6f9e"></span>Michigan</span>
      </div>
    </section>
  </main>
</body>
</html>
"""


def main() -> None:
    if not CHROME.exists():
        raise RuntimeError(f"Chrome not found at {CHROME}")
    TMP_HTML.parent.mkdir(parents=True, exist_ok=True)
    TMP_HTML.write_text(build_html(), encoding="utf-8", newline="\n")
    subprocess.run(
        [
            str(CHROME),
            "--headless=new",
            "--disable-gpu",
            "--hide-scrollbars",
            "--allow-file-access-from-files",
            "--window-size=1200,760",
            f"--screenshot={OUT}",
            TMP_HTML.resolve().as_uri(),
        ],
        check=True,
    )
    print(f"generated {OUT}")


if __name__ == "__main__":
    main()
