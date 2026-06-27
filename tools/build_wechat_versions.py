from __future__ import annotations

from dataclasses import dataclass
from html import escape
from html.parser import HTMLParser
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
SLUG = "michigan-meadows-marathon"
SOURCE = ROOT / "run50" / "stories" / "chinese" / f"{SLUG}.html"
OUT_DIR = ROOT / "run50" / "wechat"


@dataclass
class Block:
    kind: str
    text: str = ""
    src: str = ""
    alt: str = ""


class StoryParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title_parts: list[str] = []
        self.dek_parts: list[str] = []
        self.meta_parts: list[str] = []
        self.blocks: list[Block] = []
        self.in_title = False
        self.in_dek = False
        self.in_meta = False
        self.meta_depth = 0
        self.in_article = False
        self.article_depth = 0
        self.current: dict[str, object] | None = None

    def handle_starttag(self, tag: str, attrs_list: list[tuple[str, str | None]]) -> None:
        attrs = {k: v or "" for k, v in attrs_list}
        cls = attrs.get("class", "")
        if tag == "h1":
            self.in_title = True
        if "dek" in cls.split():
            self.in_dek = True
        if "meta" in cls.split():
            self.in_meta = True
            self.meta_depth = 1
        elif self.in_meta:
            self.meta_depth += 1
        if tag == "article" and "article-body" in cls.split():
            self.in_article = True
            self.article_depth = 1
        elif self.in_article:
            self.article_depth += 1

        if self.in_article:
            if tag in {"p", "h2", "h3", "figcaption"}:
                self.current = {"kind": tag, "parts": []}
            elif tag == "img":
                self.blocks.append(
                    Block(
                        "img",
                        src=attrs.get("src", ""),
                        alt=attrs.get("alt", ""),
                    )
                )

    def handle_endtag(self, tag: str) -> None:
        if tag == "h1":
            self.in_title = False
        if self.in_dek and tag == "div":
            self.in_dek = False
        if self.current and tag == self.current["kind"]:
            text = normalize_text("".join(self.current["parts"]))  # type: ignore[index]
            if text:
                self.blocks.append(Block(str(self.current["kind"]), text=text))
            self.current = None
        if self.in_meta:
            self.meta_depth -= 1
            if self.meta_depth <= 0:
                self.in_meta = False
        if self.in_article:
            self.article_depth -= 1
            if self.article_depth <= 0:
                self.in_article = False

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title_parts.append(data)
        if self.in_dek:
            self.dek_parts.append(data)
        if self.in_meta:
            text = normalize_text(data)
            if text:
                self.meta_parts.append(text)
        if self.current:
            self.current["parts"].append(data)  # type: ignore[index]


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def clean_title(title: str) -> str:
    title = normalize_text(title)
    title = title.replace("｜密歇根梅多马拉松", "｜密歇根｜梅多马拉松")
    title = title.replace("梅多马拉松在", "梅多马拉松｜在")
    return title


def split_title(title: str) -> str:
    title = clean_title(title)
    parts = title.split("｜")
    if len(parts) >= 4:
        return "<br>".join(escape(part) for part in parts[:3]) + "<br>" + escape("｜".join(parts[3:]))
    return escape(title)


def caption_text(text: str) -> str:
    text = normalize_text(text)
    text = text.replace("@阿森南", "@Arsenan")
    return text


def image_src(src: str) -> str:
    return "../stories/chinese/" + src


def parse_source() -> tuple[str, str, list[str], list[Block]]:
    parser = StoryParser()
    parser.feed(SOURCE.read_text(encoding="utf-8"))
    title = clean_title("".join(parser.title_parts))
    dek = normalize_text("".join(parser.dek_parts))
    meta = []
    for item in parser.meta_parts:
        if item not in meta:
            meta.append(item)
    return title, dek, meta, parser.blocks


def paired_blocks(blocks: list[Block]) -> list[Block | tuple[Block, str]]:
    result: list[Block | tuple[Block, str]] = []
    i = 0
    while i < len(blocks):
        block = blocks[i]
        if block.kind == "img":
            cap = ""
            if i + 1 < len(blocks) and blocks[i + 1].kind == "figcaption":
                cap = caption_text(blocks[i + 1].text)
                i += 2
            else:
                i += 1
            result.append((block, cap))
        elif block.kind == "figcaption":
            i += 1
        else:
            result.append(block)
            i += 1
    return result


def classic_section_heading(text: str) -> str:
    label = text.split("｜", 1)[0].strip()
    if "·" in label:
        label = label.split("·", 1)[-1].strip()
    line = text
    return f"""
<section style="margin: 34px 0 14px; text-align: center;">
  <section style="display: inline-block; padding: 0 12px; line-height: 35px; font-size: 14px; letter-spacing: 1px; font-weight: bold; color: #202124;">
    <span style="font-size: 17px; font-weight: bold; text-decoration: none;">{escape(label)}</span>
  </section>
  <p style="margin: 0 0 16px; font-family: -apple-system, BlinkMacSystemFont, 'Helvetica Neue', 'PingFang SC', 'Microsoft YaHei', Arial, sans-serif; font-size: 14px; line-height: 2em; letter-spacing: 0.544px; text-align: center; color: #202124;">
    <span style="font-weight: 600;"># {escape(line)}</span>
  </p>
</section>"""


def modern_section_heading(text: str) -> str:
    label = text.split("｜", 1)[0].strip()
    return f"""
<section style="margin: 42px 0 18px; padding: 14px 0 10px; border-top: 1px solid #d9e4ec; border-bottom: 1px solid #edf3f6;">
  <p style="margin: 0 0 6px; font-size: 11px; line-height: 1.4; letter-spacing: 1.6px; text-transform: uppercase; color: #8a9bad;">RUN50 FIELD NOTE</p>
  <h2 style="margin: 0; font-size: 19px; line-height: 1.55; font-weight: 800; color: #1d2a35; letter-spacing: 0;">{escape(text)}</h2>
  <p style="margin: 6px 0 0; font-size: 12px; line-height: 1.6; color: #8a6a2f;">{escape(label)}</p>
</section>"""


def classic_paragraph(text: str) -> str:
    return (
        '<p style="margin: 0 0 16px; line-height: 2em; text-indent: 2em; '
        "text-align: justify; font-size: 15px; letter-spacing: 0.4px; "
        "color: #222222; font-family: -apple-system, BlinkMacSystemFont, "
        "'Helvetica Neue', 'PingFang SC', 'Microsoft YaHei', Arial, sans-serif;\">"
        f"{escape(text)}</p>"
    )


def modern_paragraph(text: str) -> str:
    return (
        '<p style="margin: 0 0 18px; line-height: 1.95; text-align: justify; '
        "font-size: 16px; letter-spacing: 0.2px; color: #26343f; "
        "font-family: -apple-system, BlinkMacSystemFont, 'Helvetica Neue', "
        "'PingFang SC', 'Microsoft YaHei', Arial, sans-serif;\">"
        f"{escape(text)}</p>"
    )


def classic_figure(img: Block, caption: str) -> str:
    cap = escape(caption)
    return f"""
<section style="margin: 24px 0 24px; text-align: center;">
  <img src="{escape(image_src(img.src))}" alt="{escape(img.alt)}" style="width: 100%; height: auto; display: block; margin: 0 auto;">
  <p style="margin: 7px 0 0; text-align: center; line-height: 2em;">
    <span style="font-size: 14px; color: #ffa900;">▲</span><span style="background: #ffffff; font-size: 12px; color: #888888; letter-spacing: 0.5px; font-family: Optima-Regular, PingFangTC-light, serif;">{cap}</span>
  </p>
</section>"""


def modern_figure(img: Block, caption: str) -> str:
    cap = escape(caption)
    return f"""
<section style="margin: 28px 0 30px;">
  <img src="{escape(image_src(img.src))}" alt="{escape(img.alt)}" style="width: 100%; height: auto; display: block; margin: 0 auto; border-radius: 6px;">
  <p style="margin: 9px 0 0; padding-left: 10px; border-left: 3px solid #d4a669; font-size: 12px; line-height: 1.8; letter-spacing: 0.4px; color: #6f7d89; font-family: Optima-Regular, 'PingFang SC', serif;">{cap}</p>
</section>"""


def render_classic(title: str, dek: str, blocks: list[Block]) -> str:
    body: list[str] = [
        '<section style="max-width: 677px; width: 100%; box-sizing: border-box; margin: 0 auto; padding: 26px 18px 56px; background: #ffffff;">',
        '<p style="text-align: center; margin: 0 0 10px; color: #d4a669; font-size: 13px; letter-spacing: 0.5px;">丨密歇根丨</p>',
        f'<h1 style="margin: 0 0 14px; text-align: center; font-size: 24px; line-height: 1.45; font-weight: 800; color: #202124; letter-spacing: 0;">{split_title(title)}</h1>',
        '<p style="margin: 0 0 18px; text-align: center; line-height: 2em;"><span style="font-size: 14px; color: #ffa900;">▲</span><span style="font-size: 12px; color: #888888; letter-spacing: 0.5px; font-family: Optima-Regular, PingFangTC-light, serif;">Meadow Marathon @Arsenan</span></p>',
        '<p style="margin: 15px 0 8px; text-align: center; color: #d4a669; font-size: 13px; letter-spacing: 0.5px;">- Run50 #第21州｜密歇根 -</p>',
        '<p style="margin: 0 0 8px; text-align: center; font-size: 15px; line-height: 1.9; color: #202124; font-weight: bold;">📍地点：Grand Rapids · Michigan</p>',
        '<p style="margin: 0 0 24px; text-align: center; font-size: 15px; line-height: 1.9; color: #202124; font-weight: bold;">🎽赛事：Meadow Marathon</p>',
    ]
    if dek:
        body.append(
            '<section style="margin: 0 0 28px; padding: 14px 18px; border-left: 3px solid #d4a669; background: #fbf8f2;">'
            f'<p style="margin: 0; font-size: 14px; line-height: 2; color: #5d5142; letter-spacing: 0.4px; text-align: justify;">{escape(dek)}</p>'
            "</section>"
        )
    for block in paired_blocks(blocks):
        if isinstance(block, tuple):
            body.append(classic_figure(block[0], block[1]))
        elif block.kind == "h2":
            body.append(classic_section_heading(block.text))
        elif block.kind == "h3":
            body.append(classic_section_heading(block.text))
        elif block.kind == "p":
            body.append(classic_paragraph(block.text))
    body.append('<p style="margin: 38px 0 0; text-align: center; color: #d4a669; font-size: 13px; letter-spacing: 1px;">- End -</p>')
    body.append("</section>")
    return page_shell(title + "｜微信公众号版", "\n".join(body))


def render_modern(title: str, dek: str, blocks: list[Block]) -> str:
    body: list[str] = [
        '<section style="max-width: 677px; width: 100%; box-sizing: border-box; margin: 0 auto; padding: 28px 18px 58px; background: #ffffff;">',
        '<section style="margin: 0 0 22px; padding: 16px 0 18px; border-top: 4px solid #2d6f9f; border-bottom: 1px solid #dfe9ef;">',
        '<p style="margin: 0 0 8px; font-size: 12px; line-height: 1.4; letter-spacing: 2px; color: #2d6f9f; font-weight: 800;">RUN50 DISPATCH · MICHIGAN</p>',
        f'<h1 style="margin: 0; font-size: 26px; line-height: 1.38; font-weight: 900; color: #17212b; letter-spacing: 0;">{split_title(title)}</h1>',
        '<p style="margin: 14px 0 0; font-size: 13px; line-height: 1.7; color: #6f7d89;">Grand Rapids · Millennium Park · Meadow Marathon</p>',
        "</section>",
    ]
    if dek:
        body.append(
            '<section style="margin: 0 0 28px; padding: 16px 18px; background: #edf5f8; border-radius: 6px;">'
            '<p style="margin: 0 0 6px; font-size: 12px; line-height: 1.5; letter-spacing: 1px; color: #2d6f9f; font-weight: 800;">OPENING NOTE</p>'
            f'<p style="margin: 0; font-size: 15px; line-height: 1.9; color: #26343f; text-align: justify;">{escape(dek)}</p>'
            "</section>"
        )
    body.append(
        '<section style="margin: 0 0 28px; display: block;">'
        '<p style="margin: 0 0 8px; font-size: 14px; line-height: 1.8; color: #8a6a2f; font-weight: 800;">本文速记</p>'
        '<p style="margin: 0; font-size: 14px; line-height: 1.9; color: #53616f;">从肯塔基北上大急流城，先用 Parkrun 热身，再在 Millennium Park 绕六圈完成密歇根州。不是最快的一场，但很有夏天、湿地和重复路线的味道。</p>'
        "</section>"
    )
    for block in paired_blocks(blocks):
        if isinstance(block, tuple):
            body.append(modern_figure(block[0], block[1]))
        elif block.kind in {"h2", "h3"}:
            body.append(modern_section_heading(block.text))
        elif block.kind == "p":
            body.append(modern_paragraph(block.text))
    body.append('<p style="margin: 42px 0 0; padding-top: 16px; border-top: 1px solid #dfe9ef; text-align: center; color: #8a9bad; font-size: 12px; letter-spacing: 1.6px;">RUN50 · MICHIGAN · END</p>')
    body.append("</section>")
    return page_shell(title + "｜微信公众号增强版", "\n".join(body))


def page_shell(title: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)}</title>
</head>
<body style="margin: 0; padding: 0; background: #ffffff; font-family: -apple-system, BlinkMacSystemFont, 'Helvetica Neue', 'PingFang SC', 'Microsoft YaHei', Arial, sans-serif;">
{body}
</body>
</html>
"""


def main() -> None:
    title, dek, _meta, blocks = parse_source()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / f"{SLUG}.html").write_text(render_classic(title, dek, blocks), encoding="utf-8", newline="\n")
    (OUT_DIR / f"{SLUG}-modern.html").write_text(render_modern(title, dek, blocks), encoding="utf-8", newline="\n")
    print(f"generated {OUT_DIR / (SLUG + '.html')}")
    print(f"generated {OUT_DIR / (SLUG + '-modern.html')}")


if __name__ == "__main__":
    main()
