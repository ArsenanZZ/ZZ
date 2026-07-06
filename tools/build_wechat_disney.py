from __future__ import annotations

from html import escape
from pathlib import Path
import re

import lxml.html


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "run50" / "stories" / "chinese" / "disney-marathon.html"
OUT = ROOT / "run50" / "wechat" / "disney-marathon-modern-rail.html"

PUBLIC_TITLE = "Run50 #第15州｜佛罗里达：奥兰多迪士尼马拉松｜从5K到全马的Dopey周末"
CACHE = "20260706-disney-run-first"


ACCENTS = [
    "Disney Marathon",
    "Disney Marathon Weekend",
    "Dopey Challenge",
    "EPCOT",
    "Magic Kingdom",
    "Animal Kingdom",
    "Hollywood Studios",
    "Epcot",
    "迪士尼马拉松",
    "迪士尼",
    "全马",
    "半马",
    "10K",
    "5K",
    "奥兰多",
    "佛罗里达",
    "Key West",
    "基韦斯特",
    "Magic Kingdom",
    "Run50",
]


def clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def accent_inline(text: str) -> str:
    html = escape(text)
    colors = ["#356f8c", "#b7791f", "#74576d"]
    for index, phrase in enumerate(ACCENTS):
        target = escape(phrase)
        html = html.replace(
            target,
            f'<strong style="color: {colors[index % len(colors)]}; font-weight: 850;">{target}</strong>',
            1,
        )
    return html


def paragraph(text: str) -> str:
    text = clean_text(text)
    if not text:
        return ""
    if len(text) <= 42 and (
        text.startswith(("🏰", "🌴", "🏝", "🎢", "🏃", "🎆", "🧢", "🏅", "🌊"))
        or text.endswith(("：", "！"))
    ):
        return (
            '<p style="margin: 6px 0 15px; padding: 8px 11px; line-height: 1.65; '
            "font-size: 15px; letter-spacing: 0; color: #b7791f; background: #f4f8fb; "
            "border-left: 3px solid #d4a669; font-family: Georgia, 'Times New Roman', "
            "'PingFang SC', serif; font-style: italic;\">"
            f"{accent_inline(text)}</p>"
        )
    return (
        '<p style="margin: 0 0 18px; line-height: 1.95; text-align: justify; '
        "font-size: 16px; letter-spacing: 0; color: #26343f; "
        "font-family: -apple-system, BlinkMacSystemFont, 'Helvetica Neue', 'PingFang SC', "
        "'Microsoft YaHei', Arial, sans-serif;\">"
        f"{accent_inline(text)}</p>"
    )


def section_heading(number: int, title: str, label: str) -> str:
    return f"""
<section style="margin: 44px 0 18px; padding: 0 0 0 14px; border-left: 5px solid #b7791f;">
  <p style="margin: 0 0 5px; font-size: 11px; line-height: 1.4; letter-spacing: 1.6px; color: #8a9bad; font-weight: 800;">FIELD NOTE {number:02d}</p>
  <h2 style="margin: 0; font-size: 20px; line-height: 1.45; font-weight: 900; color: #162636; letter-spacing: 0;">{escape(title)}</h2>
  <p style="margin: 7px 0 0; font-size: 12px; line-height: 1.6; color: #b98735;">{escape(label)}</p>
</section>"""


def figure(el: lxml.html.HtmlElement, image_no: int) -> str:
    img = el.xpath(".//img")[0] if el.xpath(".//img") else None
    if img is None:
        return ""
    src = img.get("src") or ""
    if src.startswith("Run50-Disney-Marathon-clean_files/"):
        src = "../stories/chinese/" + src
    caption = clean_text(el.xpath("string(.//figcaption)"))
    if not caption:
        caption = clean_text(img.get("alt") or f"Disney Marathon photo {image_no:03d}")
    caption = caption.replace(" · 2", "").replace(" · 3", "").replace(" · 4", "")
    return f"""
<section style="margin: 28px 0 30px;">
  <img src="{escape(src)}" alt="奥兰多迪士尼马拉松照片 {image_no:03d}" loading="lazy" decoding="async" style="width: 100%; height: auto; display: block; margin: 0 auto; border-radius: 6px;">
  <p style="margin: 9px 0 0; padding-left: 10px; border-left: 3px solid #d4a669; font-size: 12px; line-height: 1.6; letter-spacing: 0; color: #6f7d89; font-family: Optima-Regular, 'PingFang SC', serif;">{escape(caption)}</p>
</section>"""


def split_article_sections() -> list[dict]:
    doc = lxml.html.fromstring(SOURCE.read_text(encoding="utf-8"))
    article = doc.xpath("//article")[0]
    sections: list[dict] = []
    current: dict | None = None
    for child in article:
        if child.tag == "h2":
            title = clean_text(child.text_content())
            if current:
                sections.append(current)
            current = {"title": title, "nodes": []}
        elif current:
            current["nodes"].append(child)
    if current:
        sections.append(current)
    return sections


def section_label(title: str) -> str:
    if "03｜" in title or "Run50" in title:
        return "Run50 State 15"
    if "EPCOT" in title or "Epcot" in title:
        return "Race Day"
    if "Magic Kingdom" in title or "Animal Kingdom" in title or "Hollywood" in title:
        return "Course"
    if "奖牌" in title or "跑完" in title:
        return "Finish Line"
    if "5K" in title or "10K" in title or "半马" in title:
        return "Race Weekend"
    if "环球" in title or "奥兰多" in title:
        return "Orlando"
    if "Key West" in title or "基韦斯特" in title or "迈阿密" in title:
        return "Florida Trip"
    return "Field Notes"


def normalize_title(title: str) -> str:
    title = re.sub(r"^\d+｜", "", title).strip()
    if title == "前言":
        return "从乐园周末回到马拉松起点"
    if title == "后记":
        return "跑完之后，把故事继续讲完"
    return title


def ordered_sections(sections: list[dict]) -> list[dict]:
    race_start = next(
        index for index, section in enumerate(sections)
        if section["title"].startswith("03｜")
    )
    weekend_start = next(
        index for index, section in enumerate(sections)
        if section["title"].startswith("02｜")
    )
    race = sections[race_start:]
    weekend = sections[weekend_start:race_start]
    travel = sections[:weekend_start]
    return race + weekend + travel


def render_content() -> str:
    output: list[str] = []
    image_no = 0
    for number, section in enumerate(ordered_sections(split_article_sections()), start=1):
        output.append(section_heading(number, normalize_title(section["title"]), section_label(section["title"])))
        for node in section["nodes"]:
            if node.tag == "p":
                text = clean_text(node.text_content())
                compact_text = text.replace(" ", "")
                if compact_text in {
                    "-\u672c\u6587\u5b8c-",
                    "\u6587\u5b57\u4e28Arsenan",
                    "\u6587\u5b57|Arsenan",
                    "\u6444\u5f71\u4e28Arsenan",
                    "\u6444\u5f71|Arsenan",
                    "\u8bbe\u8ba1\u4e28Arsenan",
                    "\u8bbe\u8ba1|Arsenan",
                }:
                    continue
                if text:
                    output.append(paragraph(text))
            elif node.tag == "figure":
                image_no += 1
                output.append(figure(node, image_no))
    return "\n".join(part for part in output if part)


def vlog_opening() -> str:
    return f"""
<section style="margin: 24px 0 30px;">
  <section class="wechat-vlog-frame" style="position: relative; width: 100%; padding-top: 56.25%; border-radius: 8px; overflow: hidden; background: #12384a; border: 1px solid #d5e4eb; box-shadow: 0 16px 36px rgba(20, 52, 68, 0.16);">
    <section class="wechat-vlog-panel" style="position: absolute; inset: 0; padding: 24px 26px; box-sizing: border-box; background: linear-gradient(135deg, #12384a 0%, #b7791f 58%, #0f2634 100%); color: #ffffff;">
      <p style="margin: 0 0 10px; font-size: 12px; line-height: 1.3; letter-spacing: 2.2px; font-weight: 900; color: #ffdd75;">RUN50 VLOG · FLORIDA</p>
      <p class="wechat-vlog-title" style="margin: 0; max-width: 430px; font-size: 28px; line-height: 1.25; font-weight: 900; letter-spacing: 0;">先跑一场迪士尼</p>
      <p class="wechat-vlog-summary" style="margin: 10px 0 0; max-width: 460px; font-size: 15px; line-height: 1.75; color: rgba(255,255,255,0.86);">从凌晨的EPCOT起点，到Magic Kingdom城堡、动物王国、好莱坞影城和终点奖牌，把佛州第15州先跑完整，再回看这趟奥兰多与Key West旅行。</p>
      <section class="wechat-vlog-meta" style="position: absolute; left: 26px; bottom: 22px; display: inline-block; padding: 7px 12px; border-radius: 999px; background: rgba(255,255,255,0.14); color: rgba(255,255,255,0.9); font-size: 12px; line-height: 1.4; letter-spacing: 0;">Orlando · 2024.01.07 · 16:9 Vlog</section>
      <section class="wechat-vlog-play" style="position: absolute; right: 30px; bottom: 26px; width: 64px; height: 64px; border-radius: 50%; background: #ffcc00; box-shadow: 0 10px 24px rgba(0,0,0,0.22);">
        <span class="wechat-vlog-play-icon" style="position: absolute; left: 25px; top: 18px; width: 0; height: 0; border-top: 14px solid transparent; border-bottom: 14px solid transparent; border-left: 22px solid #12384a;"></span>
      </section>
    </section>
  </section>
  <p style="margin: 9px 0 0; padding-left: 10px; border-left: 3px solid #b98735; font-size: 12px; line-height: 1.65; letter-spacing: 0; color: #6f7d89; font-family: Optima-Regular, 'PingFang SC', serif;">Vlog 开场位｜Disney Marathon Weekend</p>
</section>"""


def opening_note() -> str:
    return f"""
<section style="margin: 0 0 28px; padding: 16px 18px; background: #edf5f8; border-radius: 6px;">
  <p style="margin: 0 0 6px; font-size: 12px; line-height: 1.5; letter-spacing: 1px; color: #b7791f; font-weight: 800;">OPENING NOTE</p>
  <p style="margin: 0; font-size: 15px; line-height: 1.9; color: #26343f; text-align: justify;">这版把跑步线提前：先写<strong style="color:#356f8c;">迪士尼马拉松</strong>的凌晨起跑、四大园区、EPCOT冲刺和奖牌，再把5K、10K、半马、环球影城、Key West与迈阿密放回后半段，像纽约那篇一样，把比赛作为主轴，旅行作为注脚。</p>
</section>
<section style="margin: 0 0 28px; display: block;">
  <p style="margin: 0 0 8px; font-size: 14px; line-height: 1.8; color: #b98735; font-weight: 800;">本文速记</p>
  <p style="margin: 0; font-size: 14px; line-height: 1.9; color: #53616f;">Run50第15州，佛罗里达。EPCOT外摸黑开跑，穿过Magic Kingdom、Animal Kingdom、Hollywood Studios，再回到Epcot终点。前面是全马，后面是Dopey周末和佛州旅行。</p>
</section>"""


def cover_and_maps() -> str:
    return f"""
<section style="margin: 24px 0 28px;">
  <img src="../../assets/cover-medal-zh-index-disney-cn-flat.jpg?v=20260701-artfix-v1" alt="{escape(PUBLIC_TITLE)}封面" style="width: 100%; height: auto; display: block; margin: 0 auto; border-radius: 7px;">
  <p style="margin: 9px 0 0; padding-left: 10px; border-left: 3px solid #b98735; font-size: 12px; line-height: 1.65; letter-spacing: 0; color: #6f7d89; font-family: Optima-Regular, 'PingFang SC', serif;">奖牌质感封面｜Florida</p>
</section>
<section class="article-map-panel" aria-label="Article map">
  <div class="article-map-window article-map-snapshot article-map-snapshot-dark" data-map-kind="us" data-map-theme="dark" data-region="FL" data-short-label="FL" data-label="Run50 Map - Florida"></div>
  <p class="article-map-caption">Run50 Map - Florida · Dark @Arsenan</p>
  <div class="article-map-window article-map-snapshot article-map-snapshot-light" data-map-kind="us" data-map-theme="light" data-region="FL" data-short-label="FL" data-label="Run50 Map - Florida"></div>
  <p class="article-map-caption">Run50 Map - Florida · Light @Arsenan</p>
</section>"""


def finish_line() -> str:
    return """
<p style="margin: 46px 0 10px; font-size: 16px; line-height: 1.8; color: #d7e0ea; text-align: center;">- &#26412;&#25991;&#23436; -</p>
<p style="margin: 0 0 26px; font-size: 15px; line-height: 1.9; color: #d7e0ea; text-align: center; letter-spacing: .2px;">&#25991;&#23383; | Arsenan&nbsp;&nbsp;&middot;&nbsp;&nbsp;&#25668;&#24433; | Arsenan&nbsp;&nbsp;&middot;&nbsp;&nbsp;&#35774;&#35745; | Arsenan</p>
<section style="margin: 48px 0 0; padding: 18px 18px 20px; border-radius: 8px; background: linear-gradient(135deg, #14283a, #263f56); color: #f8fbff;">
  <p style="margin: 0 0 8px; font-size: 12px; line-height: 1.5; letter-spacing: 1.6px; color: #f8dc8a; font-weight: 900;">RUN50 FINISH LINE</p>
  <p style="margin: 0 0 12px; font-size: 18px; line-height: 1.55; font-weight: 900;">第15州，佛罗里达点亮。</p>
  <section style="display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 8px; margin: 12px 0 14px;">
    <span style="padding: 8px 6px; border-radius: 6px; background: rgba(255,255,255,.10); font-size: 12px; text-align: center;">State 15</span>
    <span style="padding: 8px 6px; border-radius: 6px; background: rgba(255,255,255,.10); font-size: 12px; text-align: center;">Orlando</span>
    <span style="padding: 8px 6px; border-radius: 6px; background: rgba(255,255,255,.10); font-size: 12px; text-align: center;">26.2 mi</span>
  </section>
  <p style="margin: 0; font-size: 14px; line-height: 1.8; color: rgba(248,251,255,.84);">这不是一篇单纯的乐园游记，也不是一场单纯刷成绩的比赛。它更像一个跑步周末：用四天把身体放进童话、排队、烟花和长距离里，最后带着一串奖牌走出Magic Kingdom。</p>
</section>
<p style="margin: 18px 0 0; font-size: 12px; line-height: 1.8; color: #7a8794; text-align: center;">欢迎在微信留言区继续补充你的迪士尼跑马故事。</p>"""


def render() -> str:
    content = render_content()
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
      .wechat-vlog-meta {{ left: 18px !important; right: 82px; bottom: 16px !important; overflow: hidden; white-space: nowrap; text-overflow: ellipsis; }}
      .wechat-vlog-play {{ right: 18px !important; bottom: 16px !important; width: 52px !important; height: 52px !important; }}
      .wechat-vlog-play-icon {{ left: 20px !important; top: 14px !important; border-top-width: 12px !important; border-bottom-width: 12px !important; border-left-width: 19px !important; }}
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
  <link rel="stylesheet" href="../wechat-article-theme.css?v={CACHE}">
</head>
<body style="margin: 0; padding: 0; background: #ffffff; font-family: -apple-system, BlinkMacSystemFont, 'Helvetica Neue', 'PingFang SC', 'Microsoft YaHei', Arial, sans-serif;">
<button class="article-theme-toggle" type="button" aria-label="Toggle theme">Light</button>
  <script src="../us-map-svg.js?v={CACHE}"></script>
  <script src="../china-map-svg.js?v={CACHE}"></script>
  <script src="../wechat-article-map.js?v={CACHE}"></script>
  <script src="../wechat-article-theme.js?v={CACHE}"></script>

<section style="max-width: 677px; width: 100%; box-sizing: border-box; margin: 0 auto; padding: 28px 18px 58px; background: #ffffff;">
<section style="margin: 0 0 22px; padding: 16px 0 18px; border-top: 4px solid #b7791f; border-bottom: 1px solid #dfe9ef;">
  <p style="margin: 0 0 8px; font-size: 12px; line-height: 1.4; letter-spacing: 2px; color: #b7791f; font-weight: 800;">RUN50 DISPATCH · FLORIDA</p>
  <p style="margin: 0; font-size: 20px; line-height: 1.55; font-weight: 900; color: #17212b; letter-spacing: 0;">Run50 第15州 · 佛罗里达 · 奥兰多迪士尼马拉松</p>
  <p style="margin: 14px 0 0; font-size: 13px; line-height: 1.7; color: #6f7d89;">奥兰多 · 佛罗里达 · 2024.01.07</p>
</section>
{vlog_opening()}
{opening_note()}
{cover_and_maps()}
{content}
{finish_line()}
</section>
</body>
</html>
"""


def main() -> None:
    OUT.write_text(render(), encoding="utf-8", newline="\n")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
