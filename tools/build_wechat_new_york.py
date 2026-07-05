from __future__ import annotations

from dataclasses import dataclass
from html import escape
import os
from pathlib import Path
import re

import lxml.html
from PIL import Image, ImageOps


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = Path(
    os.environ.get(
        "RUN50_NY_SOURCE_DIR",
        r"Z:\ZhennanZ Folder\000-Marathon-Story-2024-2025\20230000-Marathons\2021-State-03-NY",
    )
)
IMAGE_DIR = ROOT / "run50" / "stories" / "chinese" / "Run50-NewYorkCity-Marathon-clean_files"
OUT = ROOT / "run50" / "wechat" / "new-york-city-marathon-modern-rail.html"

PUBLIC_TITLE = "Run50 #第3州｜纽约：纽约马拉松｜50周年打卡"
STORY_IMAGE_PREFIX = "../stories/chinese/Run50-NewYorkCity-Marathon-clean_files"


@dataclass
class Block:
    kind: str
    text: str = ""
    caption: str = ""
    image_no: int = 0


SKIP_EXACT = {
    "丨NYC丨",
    "继续观看",
    "搜索「」网络结果",
    "暂无留言",
    "Scan to Follow",
    "当前内容可能存在未经审核的第三方商业营销信息，请确认是否继续访问。",
    "微信扫一扫可打开此内容，使用完整服务",
    "北美故事",
    "确认提交投诉",
    "你可以补充投诉原因（选填）",
    "文字丨Arsenan",
    "摄影丨Arsenan",
    "设计丨Arsenan",
    "纽约，赛博朋克",
    "50周年打卡：我的纽约马拉松",
    "出发去纽约",
    "漫长的等待",
    "第一个大满贯",
}

SKIP_CONTAINS = (
    "已关注 Follow",
    "Replay Share",
    "进度条",
    ":host {",
)


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def clean_caption(text: str) -> str:
    text = normalize_text(text).lstrip("\u25b2").strip()
    text = text.replace("@ Arsenan", "@Arsenan")
    text = text.replace("@ MarathonFoto", "@MarathonFoto")
    text = text.replace("@ LeRoy", "@LeRoy")
    text = text.replace("@ 官方", "@官方")
    return text


def is_boilerplate(text: str) -> bool:
    if not text or text in SKIP_EXACT:
        return True
    return any(marker in text for marker in SKIP_CONTAINS)


def find_source(name_part: str) -> Path:
    matches = [path for path in SOURCE_DIR.glob("*.html") if name_part in path.stem]
    if not matches:
        raise FileNotFoundError(f"Could not find source html containing {name_part!r} in {SOURCE_DIR}")
    return matches[0]


def parse_source(path: Path, image_offset: int) -> tuple[list[Block], list[Path]]:
    doc = lxml.html.fromstring(path.read_text(encoding="utf-8", errors="replace"))
    blocks: list[Block] = []
    images: list[Path] = []
    pending_images: list[Path] = []
    stopped = False

    for el in doc.iter():
        if stopped:
            break
        tag = el.tag.lower() if isinstance(el.tag, str) else ""
        if tag == "img" and "rich_pages" in el.get("class", ""):
            src = el.get("src") or ""
            if src:
                pending_images.append((path.parent / src).resolve())
            continue
        if tag not in {"p", "h1", "h2", "h3"}:
            continue

        text = normalize_text(el.text_content())
        if not text or is_boilerplate(text):
            continue
        if text == "- 本文完 -":
            stopped = True
            break
        if text.lstrip().startswith("\u25b2"):
            if pending_images:
                images.append(pending_images.pop(0))
                blocks.append(
                    Block(
                        "figure",
                        caption=clean_caption(text),
                        image_no=image_offset + len(images),
                    )
                )
            continue

        if blocks and blocks[-1].kind == "p" and blocks[-1].text == text:
            continue
        blocks.append(Block("p", text=text))

    for image in pending_images:
        images.append(image)
        blocks.append(Block("figure", caption="", image_no=image_offset + len(images)))

    return blocks, images


def maybe_write_images(images: list[Path]) -> None:
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    force = os.environ.get("RUN50_FORCE_IMAGES") == "1"
    for index, src in enumerate(images, start=1):
        out = IMAGE_DIR / f"img-{index:03d}.webp"
        if out.exists() and not force:
            continue
        with Image.open(src) as image:
            image = ImageOps.exif_transpose(image)
            if image.mode not in {"RGB", "RGBA"}:
                image = image.convert("RGB")
            if image.mode == "RGBA":
                background = Image.new("RGB", image.size, "#ffffff")
                background.paste(image, mask=image.getchannel("A"))
                image = background
            image.save(out, "WEBP", quality=88, method=6)


def accent_inline(text: str) -> str:
    html = escape(text)
    accents = [
        "纽约马拉松",
        "中央公园",
        "时代广场",
        "哈德逊河",
        "自由女神",
        "布鲁克林",
        "曼哈顿",
        "法拉盛",
        "Run50",
        "Finisher",
        "五座桥",
        "50周年",
        "42.195公里",
    ]
    colors = ["#356f8c", "#876633", "#74576d"]
    for index, phrase in enumerate(accents):
        escaped = escape(phrase)
        html = html.replace(
            escaped,
            f'<strong style="color: {colors[index % len(colors)]}; font-weight: 800;">{escaped}</strong>',
            1,
        )
    return html


def section_heading(number: int, title: str, label: str) -> str:
    return f"""
<section style="margin: 44px 0 18px; padding: 0 0 0 14px; border-left: 5px solid #2f855a;">
  <p style="margin: 0 0 5px; font-size: 11px; line-height: 1.4; letter-spacing: 1.6px; color: #8a9bad; font-weight: 800;">FIELD NOTE {number:02d}</p>
  <h2 style="margin: 0; font-size: 20px; line-height: 1.45; font-weight: 900; color: #162636; letter-spacing: 0;">{escape(title)}</h2>
  <p style="margin: 7px 0 0; font-size: 12px; line-height: 1.6; color: #b98735;">{escape(label)}</p>
</section>"""


def paragraph(text: str) -> str:
    return (
        '<p style="margin: 0 0 18px; line-height: 1.95; text-align: justify; '
        "font-size: 16px; letter-spacing: 0.2px; color: #26343f; "
        "font-family: -apple-system, BlinkMacSystemFont, 'Helvetica Neue', 'PingFang SC', "
        "'Microsoft YaHei', Arial, sans-serif;\">"
        f"{accent_inline(text)}</p>"
    )


def figure(block: Block) -> str:
    src = f"{STORY_IMAGE_PREFIX}/img-{block.image_no:03d}.webp"
    cap = escape(block.caption)
    return f"""
<section style="margin: 28px 0 30px;">
  <img src="{src}" alt="纽约马拉松照片 {block.image_no:03d}" loading="lazy" decoding="async" style="width: 100%; height: auto; display: block; margin: 0 auto; border-radius: 6px;">
  <p style="margin: 9px 0 0; padding-left: 10px; border-left: 3px solid #d4a669; font-size: 12px; line-height: 1.6; letter-spacing: 0.2px; color: #6f7d89; font-family: Optima-Regular, 'PingFang SC', serif;">{cap}</p>
</section>"""


def render_blocks(blocks: list[Block], section_plan: list[tuple[str, str, str]]) -> str:
    rendered: list[str] = []
    section_index = 0
    active_title = ""

    def add_heading(title: str, label: str) -> None:
        nonlocal section_index, active_title
        if active_title == title:
            return
        section_index += 1
        active_title = title
        rendered.append(section_heading(section_index, title, label))

    if section_plan:
        first_trigger, first_title, first_label = section_plan[0]
        add_heading(first_title, first_label)

    used = {section_plan[0][1]} if section_plan else set()
    for block in blocks:
        if block.kind == "p":
            for trigger, title, label in section_plan[1:]:
                if title not in used and block.text.startswith(trigger):
                    add_heading(title, label)
                    used.add(title)
                    break
            rendered.append(paragraph(block.text))
        elif block.kind == "figure":
            rendered.append(figure(block))
    return "\n".join(rendered)


def vlog_opening() -> str:
    return """
<section style="margin: 24px 0 30px;">
  <section class="wechat-vlog-frame" style="position: relative; width: 100%; padding-top: 56.25%; border-radius: 8px; overflow: hidden; background: #12384a; border: 1px solid #d5e4eb; box-shadow: 0 16px 36px rgba(20, 52, 68, 0.16);">
    <section class="wechat-vlog-panel" style="position: absolute; inset: 0; padding: 24px 26px; box-sizing: border-box; background: linear-gradient(135deg, #12384a 0%, #2f855a 58%, #0f2634 100%); color: #ffffff;">
      <p style="margin: 0 0 10px; font-size: 12px; line-height: 1.3; letter-spacing: 2.2px; font-weight: 900; color: #ffdd75;">RUN50 VLOG · NEW YORK</p>
      <p class="wechat-vlog-title" style="margin: 0; max-width: 430px; font-size: 28px; line-height: 1.25; font-weight: 900; letter-spacing: 0;">先看一段纽约</p>
      <p class="wechat-vlog-summary" style="margin: 10px 0 0; max-width: 460px; font-size: 15px; line-height: 1.75; color: rgba(255,255,255,0.86);">城市篇与比赛篇合并：赛博朋克纽约、法拉盛、时代广场、哈德逊河夜航，再跑进50周年纽约马拉松的五个城区。</p>
      <section class="wechat-vlog-meta" style="position: absolute; left: 26px; bottom: 22px; display: inline-block; padding: 7px 12px; border-radius: 999px; background: rgba(255,255,255,0.14); color: rgba(255,255,255,0.9); font-size: 12px; line-height: 1.4; letter-spacing: 0.5px;">New York · 2021.11.07 · 16:9 Vlog</section>
      <section class="wechat-vlog-play" style="position: absolute; right: 30px; bottom: 26px; width: 64px; height: 64px; border-radius: 50%; background: #ffcc00; box-shadow: 0 10px 24px rgba(0,0,0,0.22);">
        <span class="wechat-vlog-play-icon" style="position: absolute; left: 25px; top: 18px; width: 0; height: 0; border-top: 14px solid transparent; border-bottom: 14px solid transparent; border-left: 22px solid #12384a;"></span>
      </section>
    </section>
  </section>
  <p style="margin: 9px 0 0; padding-left: 10px; border-left: 3px solid #b98735; font-size: 12px; line-height: 1.65; letter-spacing: 0.2px; color: #6f7d89; font-family: Optima-Regular, 'PingFang SC', serif;">Vlog 开场位｜New York</p>
</section>"""


def opening_panels() -> str:
    note = "这篇把两篇旧文并成一条纽约长线：先写城市的混乱、漂亮和赛博朋克，再写50周年纽约马拉松从领物、等起跑到冲线的完整一天。"
    summary = "法拉盛、时代广场、中央公园、哈德逊河夜航，是纽约的城市底色；Verrazano Bridge、布鲁克林、皇后区、曼哈顿和中央公园，则把这座城市变成一条42.195公里的赛道。"
    return f"""
<section style="margin: 0 0 28px; padding: 16px 18px; background: #edf5f8; border-radius: 6px;"><p style="margin: 0 0 6px; font-size: 12px; line-height: 1.5; letter-spacing: 1px; color: #2f855a; font-weight: 800;">OPENING NOTE</p><p style="margin: 0; font-size: 15px; line-height: 1.9; color: #26343f; text-align: justify;">{accent_inline(note)}</p></section>
<section style="margin: 0 0 28px; display: block;"><p style="margin: 0 0 8px; font-size: 14px; line-height: 1.8; color: #b98735; font-weight: 800;">本文速记</p><p style="margin: 0; font-size: 14px; line-height: 1.9; color: #53616f;">{accent_inline(summary)}</p></section>

<section style="margin: 24px 0 28px;">
  <img src="../../assets/cover-medal-zh-index-new-york-cn-flat.jpg?v=20260629-cn-flat-v3" alt="Run50 #第3州｜纽约：纽约马拉松｜50周年打卡封面" style="width: 100%; height: auto; display: block; margin: 0 auto; border-radius: 7px;">
  <p style="margin: 9px 0 0; padding-left: 10px; border-left: 3px solid #b98735; font-size: 12px; line-height: 1.65; letter-spacing: 0.2px; color: #6f7d89; font-family: Optima-Regular, 'PingFang SC', serif;">奖牌质感封面｜New York</p>
</section>
<section class="article-map-panel" aria-label="Article map">
  <div class="article-map-window" data-map-kind="us" data-region="NY" data-short-label="NY" data-label="Run50 Map - New York"></div>
  <p class="article-map-caption">Run50 Map - New York @Arsenan</p>
</section>"""


def finish_card() -> str:
    return """
<section style="margin: 46px 0 0; padding: 22px 18px 20px; border-radius: 8px; background: linear-gradient(135deg, #132535 0%, #205f87 58%, #d1a35f 100%); color: #ffffff; box-shadow: 0 14px 32px rgba(19, 37, 53, 0.18);">
  <p style="margin: 0 0 10px; font-size: 11px; line-height: 1.4; letter-spacing: 2.2px; font-weight: 900; color: rgba(255,255,255,0.78);">RUN50 FINISH LINE</p>
  <h2 style="margin: 0 0 12px; font-size: 24px; line-height: 1.35; font-weight: 900; color: #ffffff; letter-spacing: 0;">第3州，纽约点亮。</h2>
  <p style="margin: 0; font-size: 15px; line-height: 1.9; color: rgba(255,255,255,0.92); text-align: justify;">从赛博朋克式的城市漫游，到50周年纽约马拉松的五区奔跑，这一站不像只是完成一场比赛，更像把纽约从地下铁、游船、街区、桥梁和中央公园里重新走读了一遍。</p>
  <section style="margin: 18px 0 0; display: table; width: 100%; border-collapse: collapse;">
    <section style="display: table-cell; width: 33.33%; padding: 10px 6px; border-right: 1px solid rgba(255,255,255,0.18); text-align: center;">
      <p style="margin: 0; font-size: 18px; line-height: 1.2; font-weight: 900; color: #ffffff;">3</p>
      <p style="margin: 5px 0 0; font-size: 11px; line-height: 1.4; color: rgba(255,255,255,0.74); letter-spacing: 0.8px;">STATE</p>
    </section>
    <section style="display: table-cell; width: 33.33%; padding: 10px 6px; border-right: 1px solid rgba(255,255,255,0.18); text-align: center;">
      <p style="margin: 0; font-size: 18px; line-height: 1.2; font-weight: 900; color: #ffffff;">50th</p>
      <p style="margin: 5px 0 0; font-size: 11px; line-height: 1.4; color: rgba(255,255,255,0.74); letter-spacing: 0.8px;">NYC</p>
    </section>
    <section style="display: table-cell; width: 33.33%; padding: 10px 6px; text-align: center;">
      <p style="margin: 0; font-size: 18px; line-height: 1.2; font-weight: 900; color: #ffffff;">5</p>
      <p style="margin: 5px 0 0; font-size: 11px; line-height: 1.4; color: rgba(255,255,255,0.74); letter-spacing: 0.8px;">BOROUGHS</p>
    </section>
  </section>
</section>
<section style="margin: 16px 0 0; padding: 15px 16px; border-left: 4px solid #d1a35f; background: #f4f8fb; border-radius: 7px;">
  <p style="margin: 0; font-size: 14px; line-height: 1.9; color: #314657; text-align: justify;">跑完以后也可以聊两句。如果你也有一座爱恨交织的城市，或者也有一次“大满贯第一站”的记忆，欢迎在公众号留言区见。</p>
</section>
<p style="margin: 24px 0 0; text-align: center; color: #8a9bad; font-size: 12px; line-height: 1.8; letter-spacing: 1.2px;">文字 / 摄影 / 设计 · Arsenan</p>"""


def page_shell(content: str) -> str:
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(PUBLIC_TITLE)}</title>
  <style>
    @media (max-width: 520px) {{
      .wechat-vlog-frame {{ padding-top: 72% !important; }}
      .wechat-vlog-panel {{ padding: 18px !important; }}
      .wechat-vlog-title {{ font-size: 22px !important; line-height: 1.28 !important; }}
      .wechat-vlog-summary {{ padding-right: 58px; font-size: 13px !important; line-height: 1.55 !important; }}
      .wechat-vlog-meta {{
        left: 18px !important;
        right: 82px;
        bottom: 16px !important;
        overflow: hidden;
        white-space: nowrap;
        text-overflow: ellipsis;
      }}
      .wechat-vlog-play {{
        right: 18px !important;
        bottom: 16px !important;
        width: 52px !important;
        height: 52px !important;
      }}
      .wechat-vlog-play-icon {{
        left: 20px !important;
        top: 14px !important;
        border-top-width: 12px !important;
        border-bottom-width: 12px !important;
        border-left-width: 19px !important;
      }}
    }}
  </style>
  <script>
    (function () {{
      try {{
        var saved = localStorage.getItem('run50-wechat-article-theme');
        document.documentElement.dataset.theme = saved === 'light' ? 'light' : 'dark';
      }} catch (error) {{
        document.documentElement.dataset.theme = 'dark';
      }}
    }})();
  </script>
  <link rel="stylesheet" href="../wechat-article-theme.css?v=20260705-ny-merge">
</head>
<body style="margin: 0; padding: 0; background: #ffffff; font-family: -apple-system, BlinkMacSystemFont, 'Helvetica Neue', 'PingFang SC', 'Microsoft YaHei', Arial, sans-serif;">
<button class="article-theme-toggle" type="button" aria-label="Toggle theme">Light</button>
  <script src="../us-map-svg.js?v=20260705-ny-merge"></script>
  <script src="../china-map-svg.js?v=20260705-ny-merge"></script>
  <script src="../wechat-article-map.js?v=20260705-ny-merge"></script>
  <script src="../wechat-article-theme.js?v=20260705-ny-merge"></script>

<section style="max-width: 677px; width: 100%; box-sizing: border-box; margin: 0 auto; padding: 28px 18px 58px; background: #ffffff;">
<section style="margin: 0 0 22px; padding: 16px 0 18px; border-top: 4px solid #2f855a; border-bottom: 1px solid #dfe9ef;">
<p style="margin: 0 0 8px; font-size: 12px; line-height: 1.4; letter-spacing: 2px; color: #2f855a; font-weight: 800;">RUN50 DISPATCH · NEW YORK</p>
<p style="margin: 0; font-size: 20px; line-height: 1.55; font-weight: 900; color: #17212b; letter-spacing: 0;">Run50 第3州 · 纽约 · 纽约马拉松</p>
<p style="margin: 14px 0 0; font-size: 13px; line-height: 1.7; color: #6f7d89;">纽约 · 纽约州 · 2021.11.07</p>
</section>
{content}
</section>
</body>
</html>
"""


def build() -> None:
    city_path = find_source("赛博朋克")
    race_path = find_source("马拉松")
    city_blocks, city_images = parse_source(city_path, 0)
    race_blocks, race_images = parse_source(race_path, len(city_images))
    images = city_images + race_images
    if len(images) != 130:
        raise RuntimeError(f"Expected 130 story images, got {len(images)}")
    maybe_write_images(images)

    city_sections = [
        ("站在世界的十字路口", "纽约，赛博朋克", "City"),
        ("都说纽约是", "出发去纽约", "Arrival"),
        ("挑选了一家韩国自助", "法拉盛", "Flushing"),
        ("晚上下楼探索时代广场", "时代广场", "Times Square"),
        ("第二天上午吃了个天津大包子", "中央公园", "Central Park"),
        ("出了中央公园", "哈德逊河游船", "Hudson River"),
        ("跑步后的第二天", "洛克菲勒中心与告别", "After the race"),
    ]
    race_sections = [
        ("从鱼龙混杂", "第一个大满贯", "NYC Marathon"),
        ("马拉松的前一天", "马博会与中央公园", "Expo"),
        ("跑步日的清晨", "漫长的等待", "Start Village"),
        ("马拉松是一道饕餮大餐", "五区奔跑", "Five Boroughs"),
        ("跑进中央公园", "冲向中央公园", "Central Park"),
        ("冲过终点", "Finisher", "Finish"),
        ("纽约的故事还远没有结束", "赛后纽约", "Postscript"),
    ]

    content = "\n".join(
        [
            vlog_opening(),
            opening_panels(),
            render_blocks(city_blocks, city_sections),
            '<section style="margin: 42px 0 24px; padding: 16px 18px; border-radius: 7px; background: #fff7e7; border-left: 4px solid #d1a35f;"><p style="margin: 0; font-size: 14px; line-height: 1.9; color: #5e4a2b; text-align: justify;">城市的底色铺好之后，故事转到这次纽约之行真正的主线：50周年纽约马拉松。</p></section>',
            render_blocks(race_blocks, race_sections),
            finish_card(),
        ]
    )
    OUT.write_text(page_shell(content), encoding="utf-8", newline="\n")
    print(f"wrote {OUT}")
    print(f"images {len(images)}")
    print(f"city blocks {len(city_blocks)} race blocks {len(race_blocks)}")


if __name__ == "__main__":
    build()
