from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

TAB_CSS = """
  <style id="run50-global-tabs-style">
    .run50-global-tabs {
      max-width: 1120px;
      margin: 0 auto;
      padding: 18px 22px 0;
      display: grid !important;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 14px;
      align-items: center;
      color: #53647c;
      font-size: 15px;
      font-weight: 650;
      letter-spacing: 0;
    }
    .run50-global-tabs a {
      color: inherit;
      text-decoration: none;
      text-align: center;
      border-bottom: 1px solid transparent;
      padding: 4px 0;
    }
    .run50-global-tabs a:first-child { text-align: left; }
    .run50-global-tabs a:last-child { text-align: right; }
    .run50-global-tabs a:hover { border-color: currentColor; }
    @media (max-width: 640px) {
      .run50-global-tabs {
        grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
        padding: 14px 18px 0;
        row-gap: 8px;
      }
      .run50-global-tabs a,
      .run50-global-tabs a:first-child,
      .run50-global-tabs a:last-child {
        text-align: left;
      }
    }
  </style>
"""


def tabs_for(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    slug = path.stem

    if rel == "run50/stories/chinese/index.html":
        links = [
            ("../../index.html", "← Run50"),
            ("../english/", "English Stories"),
            ("./", "Chinese Stories"),
            ("../../facebook/", "Facebook"),
        ]
    elif rel == "run50/stories/english/index.html":
        links = [
            ("../../index.html", "← Run50"),
            ("./", "English Stories"),
            ("../chinese/", "Chinese Stories"),
            ("../../facebook/", "Facebook"),
        ]
    elif rel == "run50/facebook/index.html":
        links = [
            ("../index.html", "← Run50"),
            ("../stories/english/", "English Stories"),
            ("../stories/chinese/", "Chinese Stories"),
            ("./", "Facebook"),
        ]
    elif rel.startswith("run50/stories/chinese/"):
        links = [
            ("../../index.html", "← Run50"),
            (f"../english/{slug}.html" if (ROOT / "run50" / "stories" / "english" / f"{slug}.html").exists() else "../english/", "English Stories"),
            ("./index.html", "Chinese Stories"),
            (f"../../facebook/{slug}.html" if (ROOT / "run50" / "facebook" / f"{slug}.html").exists() else "../../facebook/", "Facebook"),
        ]
    elif rel.startswith("run50/stories/english/"):
        links = [
            ("../../index.html", "← Run50"),
            ("./index.html", "English Stories"),
            (f"../chinese/{slug}.html" if (ROOT / "run50" / "stories" / "chinese" / f"{slug}.html").exists() else "../chinese/", "Chinese Stories"),
            (f"../../facebook/{slug}.html" if (ROOT / "run50" / "facebook" / f"{slug}.html").exists() else "../../facebook/", "Facebook"),
        ]
    elif rel.startswith("run50/facebook/"):
        links = [
            ("../index.html", "← Run50"),
            (f"../stories/english/{slug}.html" if (ROOT / "run50" / "stories" / "english" / f"{slug}.html").exists() else "../stories/english/", "English Stories"),
            (f"../stories/chinese/{slug}.html" if (ROOT / "run50" / "stories" / "chinese" / f"{slug}.html").exists() else "../stories/chinese/", "Chinese Stories"),
            ("./index.html", "Facebook"),
        ]
    else:
        raise ValueError(f"Unsupported page: {path}")

    body = "".join(f'<a href="{href}">{label}</a>' for href, label in links)
    return f'  <nav class="run50-global-tabs" aria-label="Run50 story sections">{body}</nav>'


def remove_old_top_navs(text: str) -> str:
    text = re.sub(
        r"\s*<nav\b[^>]*class=\"[^\"]*\btopline\b[^\"]*\"[^>]*>.*?</nav>",
        "",
        text,
        count=1,
        flags=re.S,
    )
    text = re.sub(
        r"\s*<nav\b[^>]*class=\"[^\"]*\bstory-nav\b[^\"]*\"[^>]*>.*?</nav>",
        "",
        text,
        count=1,
        flags=re.S,
    )
    text = re.sub(
        r"\s*<nav\b[^>]*class=\"[^\"]*\bnav\b[^\"]*\"[^>]*>.*?</nav>",
        "",
        text,
        count=1,
        flags=re.S,
    )
    text = re.sub(
        r"\s*<nav\b(?![^>]*\brun50-global-tabs\b)[^>]*>\s*<a\b[^>]*>(?:←\s*)?(?:中文故事|English Stories|English|Facebook|Run50).*?</nav>",
        "",
        text,
        count=1,
        flags=re.S,
    )
    text = re.sub(
        r"\s*<header class=\"site-head\"><div class=\"site-head-inner\"><div class=\"wordmark\">Run50</div><nav\b[^>]*class=\"[^\"]*\bsection-nav\b[^\"]*\"[^>]*>.*?</nav></div></header>",
        "",
        text,
        count=1,
        flags=re.S,
    )
    text = re.sub(
        r"\s*<nav\b[^>]*class=\"[^\"]*\brun50-global-tabs\b[^\"]*\"[^>]*>.*?</nav>",
        "",
        text,
        count=1,
        flags=re.S,
    )
    return text


def normalize_page(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"\s*<style id=\"run50-global-tabs-style\">.*?</style>", "", text, flags=re.S)
    if "</head>" not in text or "<body" not in text:
        return
    text = text.replace("</head>", f"{TAB_CSS}\n</head>", 1)
    text = remove_old_top_navs(text)
    nav = tabs_for(path)
    text = re.sub(r"(<body\b[^>]*>)", rf"\1\n{nav}", text, count=1)
    text = re.sub(r"\n{3,}", "\n\n", text)
    path.write_text(text, encoding="utf-8", newline="\r\n")


def main() -> None:
    pages = [
        ROOT / "run50" / "stories" / "chinese" / "index.html",
        ROOT / "run50" / "stories" / "english" / "index.html",
        ROOT / "run50" / "facebook" / "index.html",
    ]
    pages.extend(sorted((ROOT / "run50" / "stories" / "chinese").glob("*.html")))
    pages.extend(sorted((ROOT / "run50" / "stories" / "english").glob("*.html")))
    pages.extend(sorted((ROOT / "run50" / "facebook").glob("*.html")))
    seen: set[Path] = set()
    for page in pages:
        if page.name == "index.html" and page not in pages[:3]:
            continue
        if page in seen:
            continue
        seen.add(page)
        normalize_page(page)


if __name__ == "__main__":
    main()
