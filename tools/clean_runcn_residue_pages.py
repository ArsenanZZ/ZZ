from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

PAGE_ROOTS = [
    ROOT / "run50" / "stories" / "chinese",
    ROOT / "run50" / "stories" / "english",
    ROOT / "run50" / "facebook",
]

JUNK_IMAGE_PATHS = {
    "RunCN-Dalian-Trail-clean_files/img-003.webp",
    "RunCN-Dalian-Trail-clean_files/img-005.webp",
    "RunCN-Dalian-Trail-clean_files/img-021.webp",
    "RunCN-Dalian-Trail-clean_files/img-048.webp",
    "RunCN-Haikou-Marathon-clean_files/img-002.webp",
    "RunCN-Haikou-Marathon-clean_files/img-054.webp",
    "RunCN-Haikou-Marathon-clean_files/img-078.webp",
    "RunCN-Xiamen-Marathon-clean_files/img-001.webp",
    "RunCN-Xiamen-Marathon-clean_files/img-002.webp",
    "RunCN-Xiamen-Marathon-clean_files/img-003.webp",
}


def fix_missing_header_meta(text: str) -> str:
    def repl(match: re.Match[str]) -> str:
        heading, date_text, series = match.groups()
        return f'{heading}\n    <div class="meta"><span>Arsenan</span><span>{date_text.strip()}</span><span>{series.strip()}</span></div>'

    return re.sub(
        r"(<h1>[^<]+</h1>)\s*([^<>\n]*\d{4}[^<]*)</span><span>(RunCN #第[^<]+)</span></div>",
        repl,
        text,
        flags=re.S,
    )


def remove_figure_by_image(text: str, image_path: str) -> str:
    if image_path not in text:
        return text
    escaped = re.escape(image_path)
    return re.sub(
        rf"^\s*<figure\b[^>]*>.*?<img\b[^>]*{escaped}(?:\?[^\"'>]*)?[^>]*>.*?</figure>\s*$\r?\n?",
        "",
        text,
        flags=re.M,
    )


def remove_star_only_paragraphs(text: str) -> str:
    return re.sub(r"\n\s*<p>\s*(?:\*{5,}|[★☆]{1,12})\s*</p>", "", text)


def remove_wechat_caption_prefix(text: str) -> str:
    triangle = "\u25b2"
    text = text.replace(f'alt="{triangle}', 'alt="')
    text = text.replace(f"<figcaption>{triangle}", "<figcaption>")
    text = text.replace(triangle, " / ")
    text = re.sub(r"<figcaption>\s+", "<figcaption>", text)
    return text


def clean_pages() -> None:
    for root in PAGE_ROOTS:
        for path in root.glob("*.html"):
            if path.name == "index.html":
                continue
            text = path.read_text(encoding="utf-8")
            new_text = fix_missing_header_meta(text)
            new_text = remove_star_only_paragraphs(new_text)
            new_text = remove_wechat_caption_prefix(new_text)
            for image_path in JUNK_IMAGE_PATHS:
                new_text = remove_figure_by_image(new_text, image_path)
                if root.name != "chinese":
                    new_text = remove_figure_by_image(new_text, f"../chinese/{image_path}")
                    new_text = remove_figure_by_image(new_text, f"../stories/chinese/{image_path}")
            new_text = re.sub(r"\n{3,}", "\n\n", new_text)
            if new_text != text:
                path.write_text(new_text, encoding="utf-8", newline="\r\n")


if __name__ == "__main__":
    clean_pages()
