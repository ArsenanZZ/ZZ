from __future__ import annotations

import re
from html import escape
from pathlib import Path

from lxml import html


REPO = Path(__file__).resolve().parents[1]
SOURCE = REPO / "run50" / "stories" / "chinese" / "cleveland-marathon.html"
TARGET = REPO / "run50" / "wechat" / "cleveland-marathon-modern-rail.html"
INDEX = REPO / "run50" / "wechat-new" / "index.html"
VERSION = "20260706-cleveland-zh-complete"

P_STYLE = (
    "margin: 0 0 18px; line-height: 1.95; text-align: justify; "
    "font-size: 16px; letter-spacing: 0.2px; color: #26343f; "
    "font-family: -apple-system, BlinkMacSystemFont, 'Helvetica Neue', "
    "'PingFang SC', 'Microsoft YaHei', Arial, sans-serif;"
)

PART_STYLE = (
    "margin: 6px 0 15px; padding: 8px 11px; line-height: 1.65; "
    "font-size: 15px; letter-spacing: 0.3px; color: #c05621; "
    "background: #f4f8fb; border-left: 3px solid #d4a669; "
    "font-family: Georgia, 'Times New Roman', 'PingFang SC', serif; "
    "font-style: italic;"
)

CAPTION_STYLE = (
    "margin: 9px 0 0; padding-left: 10px; border-left: 3px solid #d4a669; "
    "font-size: 12px; line-height: 1.6; letter-spacing: 0.2px; "
    "color: #6f7d89; font-family: Optima-Regular, 'PingFang SC', serif;"
)


def text_content(node) -> str:
    return re.sub(r"\s+", " ", "".join(node.itertext())).strip()


def plain_paragraph(text: str) -> str:
    return f'<p style="{P_STYLE}">{escape(text)}</p>'


def part_label(text: str) -> str:
    return f'<p style="{PART_STYLE}">{escape(text)}</p>'


def heading(title: str, note: str = "比赛篇") -> str:
    return f"""
<section style="margin: 44px 0 18px; padding: 0 0 0 14px; border-left: 5px solid #c05621;">
  <p style="margin: 0 0 5px; font-size: 11px; line-height: 1.4; letter-spacing: 1.6px; color: #8a9bad; font-weight: 800;">FIELD NOTE 00</p>
  <h2 style="margin: 0; font-size: 20px; line-height: 1.45; font-weight: 900; color: #162636; letter-spacing: 0;">{escape(title)}</h2>
  <p style="margin: 7px 0 0; font-size: 12px; line-height: 1.6; color: #b98735;">{escape(note)}</p>
</section>""".strip()


def render_figure(node) -> str:
    img = node.find(".//img")
    if img is None:
        return ""
    src = img.get("src", "")
    src = "../stories/chinese/" + src.lstrip("./")
    alt = img.get("alt", "克利夫兰马拉松照片")
    caption = text_content(node.find(".//figcaption")) if node.find(".//figcaption") is not None else ""
    caption = caption.replace(" @ ", " @")
    caption_html = (
        f'\n  <p style="{CAPTION_STYLE}">{escape(caption)}</p>'
        if caption
        else ""
    )
    return f"""
<section style="margin: 28px 0 30px;">
  <img src="{escape(src)}" alt="{escape(alt)}" style="width: 100%; height: auto; display: block; margin: 0 auto; border-radius: 6px;">{caption_html}
</section>""".strip()


def race_article_html() -> str:
    source = SOURCE.read_text(encoding="utf-8")
    match = re.search(
        r'<p class="part-label">比赛篇｜克利夫兰，燃情42\.195</p>\s*<article>(.*?)</article>',
        source,
        re.S,
    )
    if not match:
        raise RuntimeError("Could not find the Cleveland race article in the source page.")
    root = html.fragment_fromstring(f"<div>{match.group(1)}</div>")
    output: list[str] = [
        part_label("比赛篇｜克利夫兰，燃情42.195"),
    ]
    skipped_title = False
    for child in root:
        if child.tag == "p":
            text = text_content(child)
            if not text:
                continue
            if not skipped_title and text == "克利夫兰，燃情42.195":
                skipped_title = True
                continue
            output.append(plain_paragraph(text))
        elif child.tag == "h2":
            output.append(heading(text_content(child)))
        elif child.tag == "figure":
            rendered = render_figure(child)
            if rendered:
                output.append(rendered)
    return "\n".join(output).strip() + "\n\n"


def renumber_field_notes(text: str) -> str:
    counter = 0

    def repl(_: re.Match[str]) -> str:
        nonlocal counter
        counter += 1
        return f"FIELD NOTE {counter:02d}"

    return re.sub(r"FIELD NOTE \d{2}", repl, text)


def main() -> None:
    page = TARGET.read_text(encoding="utf-8")
    if "img-030.webp" not in page:
        hot = page.find("Hot in Cleveland")
        if hot < 0:
            raise RuntimeError("Could not locate the start of the current Cleveland city article.")
        insert_at = page.rfind('<p style="margin: 6px 0 15px;', 0, hot)
        if insert_at < 0:
            raise RuntimeError("Could not locate the insertion point before the city article.")
        page = page[:insert_at] + race_article_html() + page[insert_at:]

    page = page.replace(
        "城市篇与比赛篇合并：摇滚名人堂、骑士主场、伊利湖和清晨冷风中的克利夫兰马拉松。",
        "先跑一场清晨冷风中的克利夫兰马拉松，再回头看摇滚名人堂、骑士主场和伊利湖边的这座铁锈州城市。",
    )
    page = page.replace(
        '城市篇与比赛篇合并：摇滚名人堂、骑士主场、<strong style="color: #356f8c; font-weight: 800;">伊利湖</strong>和清晨冷风中的克利夫兰马拉松。',
        '先跑一场清晨冷风中的克利夫兰马拉松，再回头看摇滚名人堂、骑士主场和<strong style="color: #356f8c; font-weight: 800;">伊利湖</strong>边的这座铁锈州城市。',
    )
    page = page.replace(
        "先看一段克利夫兰",
        "先跑一场克利夫兰",
    )
    page = renumber_field_notes(page)
    TARGET.write_text(page, encoding="utf-8")

    index = INDEX.read_text(encoding="utf-8")
    index = re.sub(
        r"(wechat/cleveland-marathon-modern-rail\.html\?v=)[^\"']+",
        rf"\g<1>{VERSION}",
        index,
    )
    INDEX.write_text(index, encoding="utf-8")
    print(f"Updated {TARGET} and {INDEX} with {VERSION}.")


if __name__ == "__main__":
    main()
