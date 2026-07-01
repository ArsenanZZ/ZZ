from __future__ import annotations

from html import unescape
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
INDEX_PATH = ROOT / "run50" / "wechat-new" / "index.html"
ARTICLE_DIR = ROOT / "run50" / "wechat"
ARTICLE_VERSION = "20260630-wechat-emphasis"

BLUE = "#356f8c"
GOLD = "#876633"
PLUM = "#74576d"
COLORS = (BLUE, GOLD, PLUM)
VLOG_RESPONSIVE_STYLE = """  <style>
    @media (max-width: 520px) {
      .wechat-vlog-frame { padding-top: 72% !important; }
      .wechat-vlog-panel { padding: 18px !important; }
      .wechat-vlog-title { font-size: 22px !important; line-height: 1.28 !important; }
      .wechat-vlog-summary { padding-right: 58px; font-size: 13px !important; line-height: 1.55 !important; }
      .wechat-vlog-meta {
        left: 18px !important;
        right: 82px;
        bottom: 16px !important;
        overflow: hidden;
        white-space: nowrap;
        text-overflow: ellipsis;
      }
      .wechat-vlog-play {
        right: 18px !important;
        bottom: 16px !important;
        width: 52px !important;
        height: 52px !important;
      }
      .wechat-vlog-play-icon {
        left: 20px !important;
        top: 14px !important;
        border-top-width: 12px !important;
        border-bottom-width: 12px !important;
        border-left-width: 19px !important;
      }
    }
  </style>
"""

LINK_RE = re.compile(
    r'href="https://zhennanzhang\.com/run50/wechat/([^"?]+-modern-rail\.html)',
    flags=re.I,
)
STRONG_RE = re.compile(
    r'<strong\s+style="color:\s*#[0-9a-fA-F]{6};\s*font-weight:\s*(?:800|900);">(.*?)</strong>',
    flags=re.S,
)
NUMBER_BADGE_RE = re.compile(
    r'<span\s+style="display:\s*inline-block;\s*padding:\s*0 3px;\s*margin:\s*0 1px;'
    r'\s*border-radius:\s*3px;\s*background:\s*rgba\(185,135,53,0\.16\);'
    r'\s*color:\s*#[0-9a-fA-F]{6};\s*font-weight:\s*900;">(.*?)</span>',
    flags=re.S,
)
BODY_PARAGRAPH_RE = re.compile(
    r'(<p\s+style="(?=[^"]*font-size:\s*(?:15|16)px;)(?=[^"]*text-align:\s*justify;)[^"]*">)'
    r"(.*?)"
    r"(</p>)",
    flags=re.S,
)
SERIES_SECTION_RE = re.compile(
    r'(<section class="story-section [^"]*" id="(?P<id>run50-series|runcn-series|runworld-series)">)'
    r"(?P<body>.*?)"
    r"(?=      <section class=\"story-section|      <section class=\"stats\")",
    flags=re.S,
)
CARD_OPEN_RE = re.compile(
    r'(<a class="story-card" href="[^"]+">\s*)'
    r'(?:<span class="story-number">.*?</span>\s*)?',
    flags=re.S,
)

BLUE_PATTERNS = [
    re.compile(
        r"[A-Z][A-Za-z0-9'.-]*(?:\s+(?:[A-Z][A-Za-z0-9'.-]*|of|the|and|on|to)){0,4}"
    ),
    re.compile(r"[\u4e00-\u9fff]{2,10}(?:公园|小镇|大学|机场|体育场|河|湖|山|桥)"),
    re.compile(r"(?:马拉松|赛道|起点|补给站|跑者)"),
]
GOLD_PATTERNS = [
    re.compile(
        r"(?:\d+(?::\d+)?(?:\.\d+)?\s*(?:小时|分钟|英里|英尺|公里|场|州|K|k|人|圈|次|年|月|日)?)"
    ),
    re.compile(r"(?:破\s?4|Sub\s?4|sub\s?4|冠军|终点|冲线|奖牌|全马|半马|PB)"),
]
PLUM_PATTERNS = [
    re.compile(
        r"(?:没想到|最难|第一次|终于|遗憾|惊喜|坚持|放弃|害怕|幸运|感动|"
        r"崩溃|痛苦|开心|快乐|挑战|意外|疯狂|孤独|热爱|人生|梦想|回忆|"
        r"告别|重逢|自由|勇气|满足|骄傲|难忘)"
    ),
    re.compile(r"[\u4e00-\u9fff]{2,8}(?:时刻|瞬间|故事|旅程|记忆|心情)"),
]


def linked_articles() -> list[Path]:
    html = INDEX_PATH.read_text(encoding="utf-8")
    names = list(dict.fromkeys(LINK_RE.findall(html)))
    return [ARTICLE_DIR / name for name in names]


def number_story_cards() -> None:
    html = INDEX_PATH.read_text(encoding="utf-8")
    html = re.sub(
        r"(\-modern\-rail\.html)\?v=[^\"']+",
        rf"\1?v={ARTICLE_VERSION}",
        html,
    )
    html = re.sub(
        r"(const WECHAT_STORY_VERSION = '\?v=)[^']+",
        lambda match: f"{match.group(1)}{ARTICLE_VERSION}",
        html,
    )
    labels = {
        "run50-series": "Run50",
        "runcn-series": "RunCN",
        "runworld-series": "RunWorld",
    }

    def number_section(match: re.Match[str]) -> str:
        series_id = match.group("id")
        counter = 0

        def number_card(card_match: re.Match[str]) -> str:
            nonlocal counter
            counter += 1
            badge = f'<span class="story-number">{labels[series_id]} · {counter:02d}</span>\n            '
            return f"{card_match.group(1)}{badge}"

        body = CARD_OPEN_RE.sub(number_card, match.group("body"))
        return f"{match.group(1)}{body}"

    numbered, section_count = SERIES_SECTION_RE.subn(number_section, html)
    if section_count != 3:
        raise RuntimeError(f"Expected 3 story sections, found {section_count}")
    INDEX_PATH.write_text(numbered, encoding="utf-8", newline="\n")


def strip_old_word_highlights(html: str) -> str:
    html = NUMBER_BADGE_RE.sub(lambda match: match.group(1), html)
    return STRONG_RE.sub(lambda match: match.group(1), html)


def make_vlog_responsive(html: str) -> str:
    if "wechat-vlog-frame" not in html:
        html = html.replace(
            '<section style="position: relative; width: 100%; padding-top: 56.25%;',
            '<section class="wechat-vlog-frame" style="position: relative; width: 100%; padding-top: 56.25%;',
            1,
        )
        html = html.replace(
            '<section style="position: absolute; inset: 0; padding: 24px 26px;',
            '<section class="wechat-vlog-panel" style="position: absolute; inset: 0; padding: 24px 26px;',
            1,
        )
        html = html.replace(
            '<p style="margin: 0; max-width: 430px; font-size: 28px;',
            '<p class="wechat-vlog-title" style="margin: 0; max-width: 430px; font-size: 28px;',
            1,
        )
        html = html.replace(
            '<p style="margin: 10px 0 0; max-width: 460px; font-size: 15px;',
            '<p class="wechat-vlog-summary" style="margin: 10px 0 0; max-width: 460px; font-size: 15px;',
            1,
        )
        html = html.replace(
            '<section style="position: absolute; left: 26px; bottom: 22px;',
            '<section class="wechat-vlog-meta" style="position: absolute; left: 26px; bottom: 22px;',
            1,
        )
        html = html.replace(
            '<section style="position: absolute; right: 30px; bottom: 26px;',
            '<section class="wechat-vlog-play" style="position: absolute; right: 30px; bottom: 26px;',
            1,
        )
        html = html.replace(
            '<span style="position: absolute; left: 25px; top: 18px;',
            '<span class="wechat-vlog-play-icon" style="position: absolute; left: 25px; top: 18px;',
            1,
        )
    if "wechat-vlog-frame { padding-top: 72%" not in html:
        html = html.replace("</head>", f"{VLOG_RESPONSIVE_STYLE}</head>", 1)
    return html


def plain_text(fragment: str) -> str:
    return unescape(re.sub(r"<[^>]+>", "", fragment))


def first_match(text: str, patterns: list[re.Pattern[str]]) -> str:
    for pattern in patterns:
        match = pattern.search(text)
        if not match:
            continue
        phrase = match.group(0).strip()
        if len(phrase) >= 2 and phrase.lower() not in {"run", "the", "and", "with"}:
            return phrase
    return ""


def fallback_phrase(text: str) -> str:
    clauses = [
        clause.strip()
        for clause in re.split(r"[，。！？；：]", text)
        if 5 <= len(clause.strip()) <= 18
    ]
    if not clauses:
        return ""
    with_self = [clause for clause in clauses if "我" in clause]
    return (with_self or clauses)[-1]


def candidate_for(text: str, color: str) -> str:
    if color == BLUE:
        return first_match(text, BLUE_PATTERNS)
    if color == GOLD:
        return first_match(text, GOLD_PATTERNS)
    return first_match(text, PLUM_PATTERNS)


def emphasize_articles(html: str) -> tuple[str, dict[str, int]]:
    html = make_vlog_responsive(strip_old_word_highlights(html))
    paragraphs = list(BODY_PARAGRAPH_RE.finditer(html))
    target_total = max(9, min(21, len(paragraphs) // 4))
    counts = {color: 0 for color in COLORS}
    inserted = 0
    cursor = 0
    parts: list[str] = []

    for match in paragraphs:
        parts.append(html[cursor : match.start()])
        opening, body, closing = match.groups()
        cursor = match.end()

        if inserted >= target_total or "<" in body:
            parts.append(match.group(0))
            continue

        text = plain_text(body).strip()
        if len(text) < 18:
            parts.append(match.group(0))
            continue

        preferred = COLORS[inserted % len(COLORS)]
        selected_color = min(COLORS, key=lambda color: (counts[color], color != preferred))
        phrase = candidate_for(text, selected_color)
        if not phrase:
            phrase = fallback_phrase(text)

        if not phrase or phrase not in body:
            parts.append(match.group(0))
            continue

        strong = f'<strong style="color: {selected_color}; font-weight: 800;">{phrase}</strong>'
        body = body.replace(phrase, strong, 1)
        counts[selected_color] += 1
        inserted += 1
        parts.append(f"{opening}{body}{closing}")

    parts.append(html[cursor:])
    polished = "".join(parts)

    if any(counts[color] < 3 for color in COLORS):
        raise RuntimeError(f"Could not place balanced emphasis: {counts}")
    return polished, counts


def main() -> None:
    paths = linked_articles()
    if not paths:
        raise RuntimeError("No linked WeChat articles found")

    for path in paths:
        if not path.exists():
            raise FileNotFoundError(path)
        html = path.read_text(encoding="utf-8")
        polished, counts = emphasize_articles(html)
        path.write_text(polished, encoding="utf-8", newline="\n")
        summary = ", ".join(f"{color}={counts[color]}" for color in COLORS)
        print(f"{path.relative_to(ROOT)}: {summary}")

    number_story_cards()
    print(f"polished {len(paths)} WeChat articles")
    print("numbered Run50, RunCN, and RunWorld cards from 01")


if __name__ == "__main__":
    main()
