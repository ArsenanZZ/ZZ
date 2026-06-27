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


def split_section(text: str) -> tuple[str, str]:
    if "｜" in text:
        label, rest = text.split("｜", 1)
        return label.strip(), rest.strip()
    return "Run50", text.strip()


def section_number(index: int) -> str:
    return f"{index:02d}"


def variant_section_heading(text: str, index: int, variant: str) -> str:
    label, rest = split_section(text)
    number = section_number(index)
    if variant == "rail":
        return f"""
<section style="margin: 44px 0 18px; padding: 0 0 0 14px; border-left: 5px solid #2d6f9f;">
  <p style="margin: 0 0 5px; font-size: 11px; line-height: 1.4; letter-spacing: 1.6px; color: #8a9bad; font-weight: 800;">FIELD NOTE {number}</p>
  <h2 style="margin: 0; font-size: 20px; line-height: 1.45; font-weight: 900; color: #162636; letter-spacing: 0;">{escape(rest or text)}</h2>
  <p style="margin: 7px 0 0; font-size: 12px; line-height: 1.6; color: #9b6d24;">{escape(label)}</p>
</section>"""
    if variant == "badge":
        return f"""
<section style="margin: 46px 0 20px; padding: 16px 16px 15px; background: #f1f7fa; border: 1px solid #d8e7ef; border-radius: 7px;">
  <p style="margin: 0 0 10px; font-size: 12px; line-height: 1; color: #2d6f9f; font-weight: 900; letter-spacing: 1.2px;"><span style="display: inline-block; padding: 5px 8px; background: #2d6f9f; color: #ffffff; border-radius: 999px;">{number}</span> <span style="color: #8a6a2f;">{escape(label)}</span></p>
  <h2 style="margin: 0; font-size: 20px; line-height: 1.5; font-weight: 900; color: #182635; letter-spacing: 0;">{escape(rest or text)}</h2>
</section>"""
    if variant == "stamp":
        return f"""
<section style="margin: 48px 0 22px; text-align: center;">
  <p style="margin: 0 auto 10px; display: inline-block; padding: 4px 12px; border-top: 1px solid #d4a669; border-bottom: 1px solid #d4a669; font-size: 11px; line-height: 1.6; letter-spacing: 1.8px; color: #9b6d24; font-weight: 800;">RUN50 · {number}</p>
  <h2 style="margin: 0; font-size: 20px; line-height: 1.55; font-weight: 900; color: #17212b; letter-spacing: 0;">{escape(label)}</h2>
  <p style="margin: 7px 0 0; font-size: 14px; line-height: 1.8; color: #53616f;">{escape(rest)}</p>
</section>"""
    if variant == "timeline":
        return f"""
<section style="margin: 44px 0 20px; display: table; width: 100%; border-collapse: collapse;">
  <section style="display: table-cell; width: 42px; vertical-align: top;">
    <span style="display: inline-block; width: 30px; height: 30px; border-radius: 50%; background: #d4a669; color: #ffffff; text-align: center; line-height: 30px; font-size: 12px; font-weight: 900;">{number}</span>
  </section>
  <section style="display: table-cell; vertical-align: top; padding-left: 4px; border-bottom: 1px solid #e7edf1; padding-bottom: 12px;">
    <p style="margin: 0 0 4px; font-size: 11px; line-height: 1.4; color: #2d6f9f; letter-spacing: 1.4px; font-weight: 800;">{escape(label)}</p>
    <h2 style="margin: 0; font-size: 19px; line-height: 1.5; font-weight: 900; color: #17212b; letter-spacing: 0;">{escape(rest or text)}</h2>
  </section>
</section>"""
    return modern_section_heading(text)


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


def accent_inline(text: str) -> str:
    escaped = escape(text)
    blue = "#2d6f9f"
    gold = "#9b6d24"
    terms = [
        ("Grand Rapids", blue),
        ("Millennium Park", blue),
        ("Parkrun", gold),
        ("六圈", gold),
        ("4 小时 44 分", blue),
        ("三味真火", gold),
        ("Mile ", blue),
        ("大急流城", blue),
        ("千禧公园", blue),
        ("密歇根", blue),
    ]
    for term, color in terms:
        escaped = escaped.replace(
            escape(term),
            f'<strong style="color: {color}; font-weight: 800;">{escape(term)}</strong>',
        )
    return escaped


def modern_paragraph_accent(text: str) -> str:
    return (
        '<p style="margin: 0 0 18px; line-height: 1.95; text-align: justify; '
        "font-size: 16px; letter-spacing: 0.2px; color: #26343f; "
        "font-family: -apple-system, BlinkMacSystemFont, 'Helvetica Neue', "
        "'PingFang SC', 'Microsoft YaHei', Arial, sans-serif;\">"
        f"{accent_inline(text)}</p>"
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


def render_modern_variant(title: str, dek: str, blocks: list[Block], variant: str, label: str) -> str:
    body: list[str] = [
        '<section style="max-width: 677px; width: 100%; box-sizing: border-box; margin: 0 auto; padding: 28px 18px 58px; background: #ffffff;">',
        '<section style="margin: 0 0 22px; padding: 16px 0 18px; border-top: 4px solid #2d6f9f; border-bottom: 1px solid #dfe9ef;">',
        f'<p style="margin: 0 0 8px; font-size: 12px; line-height: 1.4; letter-spacing: 2px; color: #2d6f9f; font-weight: 800;">RUN50 DISPATCH · MICHIGAN · {escape(label.upper())}</p>',
        f'<h1 style="margin: 0; font-size: 26px; line-height: 1.38; font-weight: 900; color: #17212b; letter-spacing: 0;">{split_title(title)}</h1>',
        '<p style="margin: 14px 0 0; font-size: 13px; line-height: 1.7; color: #6f7d89;">Grand Rapids · Millennium Park · Meadow Marathon</p>',
        "</section>",
    ]
    if dek:
        body.append(
            '<section style="margin: 0 0 28px; padding: 16px 18px; background: #edf5f8; border-radius: 6px;">'
            '<p style="margin: 0 0 6px; font-size: 12px; line-height: 1.5; letter-spacing: 1px; color: #2d6f9f; font-weight: 800;">OPENING NOTE</p>'
            f'<p style="margin: 0; font-size: 15px; line-height: 1.9; color: #26343f; text-align: justify;">{accent_inline(dek)}</p>'
            "</section>"
        )
    body.append(
        '<section style="margin: 0 0 28px; display: block;">'
        '<p style="margin: 0 0 8px; font-size: 14px; line-height: 1.8; color: #8a6a2f; font-weight: 800;">本文速记</p>'
        '<p style="margin: 0; font-size: 14px; line-height: 1.9; color: #53616f;">从肯塔基北上大急流城，先用 <strong style="color: #9b6d24; font-weight: 800;">Parkrun</strong> 热身，再在 <strong style="color: #2d6f9f; font-weight: 800;">Millennium Park</strong> 绕六圈完成密歇根州。不是最快的一场，但很有夏天、湿地和重复路线的味道。</p>'
        "</section>"
    )
    section_index = 0
    for block in paired_blocks(blocks):
        if isinstance(block, tuple):
            body.append(modern_figure(block[0], block[1]))
        elif block.kind in {"h2", "h3"}:
            section_index += 1
            body.append(variant_section_heading(block.text, section_index, variant))
        elif block.kind == "p":
            body.append(modern_paragraph_accent(block.text))
    body.append(f'<p style="margin: 42px 0 0; padding-top: 16px; border-top: 1px solid #dfe9ef; text-align: center; color: #8a9bad; font-size: 12px; letter-spacing: 1.6px;">RUN50 · MICHIGAN · {escape(label.upper())} · END</p>')
    body.append("</section>")
    return page_shell(title + f"｜微信公众号增强版｜{label}", "\n".join(body))


def render_title_lab(title: str, blocks: list[Block]) -> str:
    headings = [block.text for block in blocks if block.kind in {"h2", "h3"}][:4]
    descriptions = {
        "rail": "左侧杂志栏：最像新版公众号专栏，利落、现代，适合长期使用。",
        "badge": "编号章卡：信息感更强，适合 Run50 这种系列文章。",
        "stamp": "居中印章：保留一点旧公众号的仪式感，但比 Italy 版更干净。",
        "timeline": "路线时间线：有跑步路线和旅程推进感，章节感最强。",
    }
    body: list[str] = [
        '<section style="max-width: 677px; width: 100%; box-sizing: border-box; margin: 0 auto; padding: 28px 18px 58px; background: #ffffff;">',
        '<p style="margin: 0 0 8px; font-size: 12px; line-height: 1.4; letter-spacing: 2px; color: #2d6f9f; font-weight: 800;">RUN50 WECHAT TITLE LAB</p>',
        f'<h1 style="margin: 0 0 14px; font-size: 25px; line-height: 1.4; font-weight: 900; color: #17212b; letter-spacing: 0;">{split_title(title)}</h1>',
        '<p style="margin: 0 0 28px; font-size: 14px; line-height: 1.9; color: #53616f;">下面是四套小章标题风格。每套先给一句定位，再连续展示几个章节标题，方便比较它在长文里的节奏。</p>',
    ]
    for variant, label in [
        ("rail", "Version A · Rail"),
        ("badge", "Version B · Badge"),
        ("stamp", "Version C · Stamp"),
        ("timeline", "Version D · Timeline"),
    ]:
        body.append(
            f'<section style="margin: 34px 0 18px; padding: 12px 14px; background: #f7fafc; border-radius: 7px;">'
            f'<p style="margin: 0 0 5px; font-size: 13px; line-height: 1.6; color: #2d6f9f; font-weight: 900;">{escape(label)}</p>'
            f'<p style="margin: 0; font-size: 13px; line-height: 1.8; color: #53616f;">{escape(descriptions[variant])}</p>'
            "</section>"
        )
        for index, heading in enumerate(headings, start=1):
            body.append(variant_section_heading(heading, index, variant))
    body.append("</section>")
    return page_shell(title + "｜微信公众号标题样式对照", "\n".join(body))


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
    (OUT_DIR / f"{SLUG}-title-styles.html").write_text(render_title_lab(title, blocks), encoding="utf-8", newline="\n")
    for variant, label in [
        ("rail", "rail"),
        ("badge", "badge"),
        ("stamp", "stamp"),
        ("timeline", "timeline"),
    ]:
        (OUT_DIR / f"{SLUG}-modern-{variant}.html").write_text(
            render_modern_variant(title, dek, blocks, variant, label),
            encoding="utf-8",
            newline="\n",
        )
    print(f"generated {OUT_DIR / (SLUG + '.html')}")
    print(f"generated {OUT_DIR / (SLUG + '-modern.html')}")
    print("generated modern variants")


if __name__ == "__main__":
    main()
