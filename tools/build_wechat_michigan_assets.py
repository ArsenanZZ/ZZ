from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "wechat-run50-map-michigan-21.png"
TMP_HTML = ROOT / "tmp" / "wechat-run50-map-michigan-21.html"
CHROME = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")

STATE_PATHS = {
    "IL": ["Illinois", "Kentucky_1_"],
    "TN": ["Alabama"],
    "WV": ["West_Virginia", "Virginia_1_"],
    "TX": ["Kansas_1_"],
    "FL": ["South_Carolina_1_"],
    "NC": ["Maryland"],
    "AR": ["Tennessee", "Arkansas"],
    "SC": ["South_Carolina", "Indiana_1_"],
    "KY": ["Georgia_1_", "Kentucky"],
    "PA": ["Pensilvania", "New_Jersey_1_"],
    "WI": ["Wisconsin", "Illinois_1_"],
    "MI": ["Michigan", "Ocean"],
    "NH": ["New_Hampshire", "Maine_1_"],
    "LA": ["Arkansas_1_"],
    "VA": ["North_Carolina_1_", "Virginia"],
    "ND": ["South_Dakota_1_", "North_Dakota"],
    "KS": ["Kansas", "North_Dakota_1_"],
    "VT": ["New_Hampshire_1_", "Vermont"],
    "AL": ["alabama", "Missispi"],
    "AZ": ["Arizona_1_", "Utah"],
    "DE": ["Massachusets_1_"],
    "MN": ["Minnesotta", "Wisconsin_1_"],
    "CT": ["New_York_2_", "Connecticut"],
    "RI": ["Delaware", "Rhode_Island"],
    "MA": ["Vermont_1_", "Massachusets"],
    "ME": ["Michigan_1_", "Maine"],
    "OH": ["Ohio", "West_Virginia_1_"],
    "NY": ["Rhode_Island_1_", "New_York"],
    "CA": ["Arizona"],
    "IN": ["Indiana", "Ohio_1_"],
    "GA": ["Georgia", "Florida_1_"],
    "CO": ["Texas_1_", "Colorado"],
    "MO": ["Iowa_1_", "Missouri"],
    "HI": ["ocean_2_"],
    "AK": ["ocean_3_"],
    "ID": ["Idaho", "Wyoming"],
    "IA": ["Minessota", "Iowa"],
    "MS": ["Mossouri", "Missisppi"],
    "MT": ["Washington_1_", "Montana"],
    "NE": ["Nebraska", "Louisiana_1_"],
    "NV": ["Nevada_41_", "California"],
    "NJ": ["New_Jersey", "Connecticut_1_"],
    "NM": ["Idaho_1_", "New_Mexico_1_"],
    "OK": ["Oklahoma", "Colorado_1_"],
    "OR": ["Nevada_1_", "Oregon_41_"],
    "SD": ["South_Dakota", "Nebraska_1_"],
    "UT": ["Utah_1_", "New_Mexico"],
    "WY": ["Montana_1_", "Wyoming_1_"],
    "MD": ["Pensilvania_1_", "Oregon_1_"],
    "WA": ["Oklahoma_1_"],
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

COLORS = {
    "AK": "#d4614a",
    "AR": "#5ca860",
    "CA": "#d4614a",
    "CO": "#9068c0",
    "FL": "#d4614a",
    "GA": "#e89838",
    "HI": "#9068c0",
    "IL": "#9068c0",
    "IN": "#e89838",
    "KY": "#98c038",
    "MI": "#007f9f",
    "MO": "#e89838",
    "NC": "#98c038",
    "NY": "#e89838",
    "OH": "#5ca860",
    "PA": "#d4614a",
    "SC": "#9068c0",
    "TN": "#3898a8",
    "TX": "#9068c0",
    "WI": "#5ca860",
    "WV": "#e89838",
}

CITY_DOTS = [
    ("KY", "Louisville", 38.2527, -85.7585),
    ("KY", "Williamson", 37.6740, -82.2776),
    ("OH", "Cleveland", 41.4993, -81.6944),
    ("NY", "New York City", 40.7128, -74.0060),
    ("CA", "San Francisco", 37.7749, -122.4194),
    ("IN", "Indianapolis", 39.7684, -86.1581),
    ("HI", "Honolulu", 21.3069, -157.8583),
    ("GA", "Atlanta", 33.7490, -84.3880),
    ("CO", "Denver", 39.7392, -104.9903),
    ("AK", "Anchorage", 61.2181, -149.9003),
    ("MO", "St. Joseph", 39.7675, -94.8466),
    ("IL", "Chicago", 41.8781, -87.6298),
    ("TN", "Nashville", 36.1627, -86.7816),
    ("WV", "Huntington", 38.4192, -82.4453),
    ("TX", "San Antonio", 29.4241, -98.4936),
    ("FL", "Miami", 25.7617, -80.1918),
    ("FL", "Orlando", 28.5383, -81.3792),
    ("NC", "Oak Island", 33.9174, -78.1575),
    ("AR", "Little Rock", 34.7465, -92.2896),
    ("SC", "Greer", 34.9387, -82.2271),
    ("PA", "Pittsburgh", 40.4406, -79.9959),
    ("WI", "Green Bay", 44.5133, -88.0133),
    ("MI", "Grand Rapids", 42.9634, -85.6681),
]


def read_us_svg() -> str:
    text = (ROOT / "run50" / "us-map-svg.js").read_text(encoding="utf-8")
    match = re.search(r"`([\s\S]*)`", text)
    if not match:
        raise RuntimeError("Could not extract US_MAP_SVG")
    return match.group(1)


def js_literal(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def build_html() -> str:
    svg = read_us_svg()
    state_path_ids = sorted({path for paths in STATE_PATHS.values() for path in paths})
    hollow_cleanup = [
        "Arizona",
        "Michigan",
        "Oklahoma_1_",
        "Alabama",
        "Maryland",
        "ocean_3_",
        "Kansas_1_",
        "Arkansas_1_",
        "Illinois",
        "West_Virginia",
        "South_Carolina",
        "Pensilvania",
        "Wisconsin",
        "Vermont",
        "New_Hampshire",
        "Kansas",
        "alabama",
        "Arizona_1_",
        "Minnesotta",
        "Ohio",
        "New_York",
        "Indiana",
        "Georgia",
        "Alaska_1_",
        "Idaho",
        "Nebraska",
        "Nevada_41_",
        "Oklahoma",
        "South_Dakota",
        "Utah_1_",
        "Pensilvania_1_",
    ]

    script = f"""
      const STATE_PATHS = {js_literal(STATE_PATHS)};
      const RUN_STATES = {js_literal(RUN50_FIRST_21)};
      const COLORS = {js_literal(COLORS)};
      const STATE_PATH_IDS = {js_literal(state_path_ids)};
      const HOLLOW_CLEANUP = {js_literal(hollow_cleanup)};
      const CITY_DOTS = {js_literal(CITY_DOTS)};
      const SPECIAL_POSITIONS = {{
        "NY:New York City": {{ x: 1474.0, y: 418.0 }}
      }};
      const MUTED = "#dedad3";

      function projectAlbers(lat, lon) {{
        const lat0 = 37.5 * Math.PI / 180;
        const lon0 = -96 * Math.PI / 180;
        const lat1 = 29.5 * Math.PI / 180;
        const lat2 = 45.5 * Math.PI / 180;
        const n = 0.5 * (Math.sin(lat1) + Math.sin(lat2));
        const C = Math.cos(lat1) * Math.cos(lat1) + 2 * n * Math.sin(lat1);
        const rho0 = Math.sqrt(C - 2 * n * Math.sin(lat0)) / n;
        const latRad = lat * Math.PI / 180;
        const lonRad = lon * Math.PI / 180;
        const theta = n * (lonRad - lon0);
        const rho = Math.sqrt(C - 2 * n * Math.sin(latRad)) / n;
        return {{
          x: 1798.50 * rho * Math.sin(theta) + 935.11,
          y: -1851.29 * (rho0 - rho * Math.cos(theta)) + 579.07
        }};
      }}

      function splitPath(d) {{
        const parts = [];
        let last = 0;
        for (let i = 1; i < d.length; i++) {{
          if (d[i] === "M" && /\\s/.test(d[i - 1])) {{
            parts.push(d.slice(last, i).trim());
            last = i;
          }}
        }}
        parts.push(d.slice(last).trim());
        return parts;
      }}

      function bbox(part) {{
        const coords = part.match(/([\\d.]+),([\\d.]+)/g) || [];
        if (!coords.length) return {{ xMin: 0, xMax: 0, yMin: 0, yMax: 0, area: 0 }};
        const xs = coords.map(c => parseFloat(c.split(",")[0]));
        const ys = coords.map(c => parseFloat(c.split(",")[1]));
        const xMin = Math.min(...xs), xMax = Math.max(...xs), yMin = Math.min(...ys), yMax = Math.max(...ys);
        return {{ xMin, xMax, yMin, yMax, area: (xMax - xMin) * (yMax - yMin) }};
      }}

      function removeNestedSubpaths(id) {{
        const el = document.getElementById("map_" + id);
        if (!el) return;
        const d = el.getAttribute("d") || "";
        const parts = splitPath(d);
        const boxes = parts.map(bbox);
        const maxArea = Math.max(...boxes.map(b => b.area));
        if (!isFinite(maxArea) || maxArea <= 0) return;
        el.removeAttribute("fill-rule");
        el.setAttribute("d", parts.filter((_, i) => {{
          const b = boxes[i];
          if (b.area < maxArea * 0.05) return true;
          return !boxes.some((o, j) => j !== i && b.xMin >= o.xMin && b.xMax <= o.xMax && b.yMin >= o.yMin && b.yMax <= o.yMax);
        }}).join(" "));
      }}

      function starPoints(cx, cy, outer, inner) {{
        const points = [];
        for (let i = 0; i < 10; i++) {{
          const angle = -Math.PI / 2 + i * Math.PI / 5;
          const radius = i % 2 === 0 ? outer : inner;
          points.push(`${{cx + Math.cos(angle) * radius}},${{cy + Math.sin(angle) * radius}}`);
        }}
        return points.join(" ");
      }}

      function removeFloridaHoles() {{
        const el = document.getElementById("map_South_Carolina_1_");
        if (!el) return;
        const parts = splitPath(el.getAttribute("d") || "");
        const boxes = parts.map(bbox);
        const maxArea = Math.max(...boxes.map(b => b.area));
        const outerIdx = boxes.findIndex(b => b.area === maxArea);
        const outer = boxes[outerIdx];
        if (!outer || !isFinite(maxArea) || maxArea <= 0) return;
        el.setAttribute("d", parts.filter((_, i) => {{
          const b = boxes[i];
          const nested = b.xMin >= outer.xMin && b.xMax <= outer.xMax && b.yMin >= outer.yMin && b.yMax <= outer.yMax;
          return i === outerIdx || !nested || b.area < maxArea * 0.05;
        }}).join(" "));
      }}

      function renderMap() {{
        const slot = document.getElementById("map-slot");
        slot.innerHTML = {js_literal(svg)};
        const master = document.getElementById("us-map-master");
        master.style.width = "100%";
        master.style.height = "100%";
        master.style.display = "block";

        master.querySelectorAll("path").forEach(path => {{
          const id = path.id.replace("map_", "");
          if (!STATE_PATH_IDS.includes(id)) {{
            path.style.pointerEvents = "none";
            if (id !== "USA" && id !== "White" && id !== "exterior_2_") {{
              const fill = path.getAttribute("fill") || "";
              if (/^#[0-9a-fA-F]{{6}}$/.test(fill)) {{
                const r = parseInt(fill.slice(1, 3), 16), g = parseInt(fill.slice(3, 5), 16), b = parseInt(fill.slice(5, 7), 16);
                if (r * .299 + g * .587 + b * .114 >= 60) path.style.fill = "none";
              }}
            }}
          }}
        }});

        removeFloridaHoles();
        HOLLOW_CLEANUP.forEach(removeNestedSubpaths);
        STATE_PATH_IDS.forEach(id => {{
          const el = document.getElementById("map_" + id);
          if (el) el.style.fill = MUTED;
        }});
        RUN_STATES.forEach(abbr => {{
          (STATE_PATHS[abbr] || []).forEach(id => {{
            const el = document.getElementById("map_" + id);
            if (el) {{
              el.style.fill = COLORS[abbr] || "#3898a8";
              el.classList.add("run-state");
            }}
          }});
        }});
        const alaskaFrame = document.getElementById("map_exterior_2_");
        const hawaiiFrame = document.getElementById("map_hawaii_1_");
        if (alaskaFrame && hawaiiFrame) alaskaFrame.style.fill = getComputedStyle(hawaiiFrame).fill;

        const highlightGroup = document.createElementNS("http://www.w3.org/2000/svg", "g");
        highlightGroup.id = "mi-highlight-outline";
        master.appendChild(highlightGroup);
        (STATE_PATHS.MI || []).forEach(id => {{
          const source = document.getElementById("map_" + id);
          if (!source) return;
          const outline = source.cloneNode(false);
          outline.removeAttribute("id");
          outline.setAttribute("fill", "none");
          outline.setAttribute("stroke", "#ffcc00");
          outline.setAttribute("stroke-width", "4.2");
          outline.setAttribute("stroke-linejoin", "round");
          outline.setAttribute("stroke-linecap", "round");
          outline.setAttribute("opacity", "0.95");
          outline.style.pointerEvents = "none";
          highlightGroup.appendChild(outline);
        }});

        const dotGroup = document.createElementNS("http://www.w3.org/2000/svg", "g");
        dotGroup.id = "city-dots-group";
        master.appendChild(dotGroup);
        CITY_DOTS.forEach(([abbr, city, lat, lon]) => {{
          let x, y;
          const special = SPECIAL_POSITIONS[abbr + ":" + city];
          if (special) {{
            x = special.x; y = special.y;
          }} else if (abbr === "HI") {{
            x = 570.0; y = 933.0;
          }} else if (abbr === "AK") {{
            x = 275.0; y = 917.0;
          }} else {{
            const p = projectAlbers(lat, lon);
            x = p.x; y = p.y;
          }}
          const glow = document.createElementNS("http://www.w3.org/2000/svg", "circle");
          glow.setAttribute("cx", x);
          glow.setAttribute("cy", y);
          glow.setAttribute("r", 11);
          glow.setAttribute("fill", "rgba(255, 59, 48, 0.35)");
          dotGroup.appendChild(glow);
          if (abbr === "MI") {{
            const shadow = document.createElementNS("http://www.w3.org/2000/svg", "polygon");
            shadow.setAttribute("points", starPoints(x + 2.1, y + 2.6, 13.2, 5.8));
            shadow.setAttribute("fill", "#5f4500");
            shadow.setAttribute("opacity", "0.38");
            dotGroup.appendChild(shadow);
            const star = document.createElementNS("http://www.w3.org/2000/svg", "polygon");
            star.setAttribute("points", starPoints(x, y, 13, 5.7));
            star.setAttribute("fill", "#ffcc00");
            star.setAttribute("stroke", "#6b4d00");
            star.setAttribute("stroke-width", "1.9");
            star.setAttribute("stroke-linejoin", "round");
            dotGroup.appendChild(star);
            const shine = document.createElementNS("http://www.w3.org/2000/svg", "polygon");
            shine.setAttribute("points", starPoints(x - 2.4, y - 3.2, 5.2, 2.1));
            shine.setAttribute("fill", "#fff1a8");
            shine.setAttribute("opacity", "0.9");
            dotGroup.appendChild(shine);
            return;
          }}
          const dot = document.createElementNS("http://www.w3.org/2000/svg", "circle");
          dot.setAttribute("cx", x);
          dot.setAttribute("cy", y);
          dot.setAttribute("r", 4.5);
          dot.setAttribute("fill", "#ff3b30");
          dot.setAttribute("stroke", "#ffffff");
          dot.setAttribute("stroke-width", "1.5");
          dotGroup.appendChild(dot);
        }});
      }}

      renderMap();
    """

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<style>
  html, body {{
    width: 1200px;
    height: 704px;
    margin: 0;
    overflow: hidden;
    background: #ffffff;
  }}
  .frame {{
    width: 1200px;
    height: 704px;
    box-sizing: border-box;
    padding: 12px;
    background: #ffffff;
  }}
  #map-slot {{
    position: relative;
    width: 100%;
    aspect-ratio: 1722 / 989;
    background: #f4f6f7;
    border-radius: 10px;
    overflow: hidden;
    border: 1px solid #dde5ec;
    box-sizing: border-box;
  }}
  #us-map-master path {{
    transition: fill .2s ease, opacity .2s ease, stroke .2s ease;
  }}
</style>
</head>
<body>
  <main class="frame">
    <section id="map-slot"></section>
  </main>
  <script>{script}</script>
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
            "--window-size=1200,704",
            f"--screenshot={OUT}",
            TMP_HTML.resolve().as_uri(),
        ],
        check=True,
    )
    print(f"generated {OUT}")


if __name__ == "__main__":
    main()
