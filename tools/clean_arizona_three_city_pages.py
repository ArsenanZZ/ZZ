from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERSION = "20260627-run50-clean"

ARIZONA = ROOT / "run50" / "stories" / "chinese" / "arizona-phoenix-marathon.html"
NORTH_CAROLINA = ROOT / "run50" / "stories" / "chinese" / "north-carolina-oak-island-marathon.html"

THREE_CITY_PAGES = [
    ROOT / "run50" / "stories" / "chinese" / "three-city-pilgrimage.html",
    ROOT / "run50" / "stories" / "english" / "three-city-pilgrimage.html",
    ROOT / "run50" / "facebook" / "three-city-pilgrimage.html",
]

THREE_CITY_JUNK_IMAGES = {
    "img-001.webp",
    "img-002.webp",
    "img-003.webp",
    "img-004.webp",
    "img-005.webp",
    "img-009.webp",
    "img-011.webp",
    "img-012.webp",
    "img-013.webp",
    "img-017.webp",
    "img-019.webp",
    "img-020.webp",
    "img-024.webp",
    "img-026.webp",
    "img-027.webp",
    "img-028.webp",
    "img-029.webp",
    "img-030.webp",
    "img-031.webp",
    "img-032.webp",
    "img-033.webp",
    "img-034.webp",
    "img-035.webp",
    "img-036.webp",
}


def extract_style(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    match = re.search(r"<style>\s*(.*?)\s*</style>", text, flags=re.S)
    if not match:
        raise RuntimeError(f"Could not find <style> in {path}")
    return match.group(1)


def clean_arizona_chinese_page() -> None:
    text = ARIZONA.read_text(encoding="utf-8")
    reference_style = extract_style(NORTH_CAROLINA)
    text = re.sub(r"<style>\s*.*?\s*</style>", f"<style>\n{reference_style}\n  </style>", text, flags=re.S)

    text = re.sub(
        r'<div class="meta">\s*<span>By Arsenan</span>\s*<span>Race: 2026\.01\.10</span>\s*'
        r"<span>Buckeye / Phoenix, Arizona</span>\s*<span>Buckeye Marathon</span>\s*</div>",
        '<div class="meta"><span>Arsenan</span><span>2026.01.10</span><span>Run50 #29</span></div>',
        text,
        flags=re.S,
    )
    text = text.replace(
        '<div class="dek">二〇二六第一跑，落地凤凰城，跑过 Buckeye 的沙漠公路、巨人柱、机场终点和一场意外的 3:58。</div>',
        '<p class="dek">二〇二六第一跑，落地凤凰城，跑过 Buckeye 的沙漠公路、巨人柱、机场终点和一场意外的 3:58。</p>\n'
        f'    <img class="cover" src="../../../assets/cover-medal-arizona-phoenix-marathon.jpg?v={VERSION}" '
        'alt="Run50 #第29州｜亚利桑那：Buckeye Marathon 奖牌封面" loading="eager" decoding="async">',
    )

    # Remove repetitive self-credit from every personal photo caption; keep non-self source labels.
    text = re.sub(r"\s*<span>@Arsenan</span>", "", text)
    text = re.sub(r"\s*<span>(赛事摄影|Official|Photographer|Google|Drone)</span>", r" · \1", text)
    text = text.replace("?v=20260627-run50-style", f"?v={VERSION}")
    text = text.replace(
        "og-run50-arizona-phoenix-marathon-icons.png?v=20260627-run50-style",
        f"og-run50-arizona-phoenix-marathon-icons.png?v={VERSION}",
    )
    ARIZONA.write_text(text, encoding="utf-8", newline="\r\n")


def clean_three_city_pages() -> None:
    for path in THREE_CITY_PAGES:
        text = path.read_text(encoding="utf-8")
        if path.name == "three-city-pilgrimage.html" and "\\chinese\\" in str(path):
            text = re.sub(
                r"(<h1>RunCN #第7-9站｜鲜衣怒马，烈焰红花：三座城的朝圣之旅</h1>)\s*"
                r"2017\.10\.15-11\.18</span><span>RunCN #第7-9站</span></div>",
                r'\1\n    <div class="meta"><span>Arsenan</span><span>2017.10.15-11.18</span><span>RunCN #第7-9站</span></div>',
                text,
                flags=re.S,
            )

        for image_name in THREE_CITY_JUNK_IMAGES:
            text = remove_figure_by_image(text, image_name)

        text = re.sub(r"\n{3,}", "\n\n", text)
        path.write_text(text, encoding="utf-8", newline="\r\n")


def remove_figure_by_image(text: str, image_name: str) -> str:
    escaped = re.escape(image_name)
    patterns = [
        rf"\n\s*<figure>\s*<img\b[^>]*{escaped}[^>]*>\s*(?:<figcaption>.*?</figcaption>)?\s*</figure>",
        rf"\n\s*<figure[^>]*>.*?<img\b[^>]*{escaped}[^>]*>.*?</figure>",
    ]
    for pattern in patterns:
        text = re.sub(pattern, "", text, flags=re.S)
    return text


def main() -> None:
    clean_arizona_chinese_page()
    clean_three_city_pages()


if __name__ == "__main__":
    main()
