from pathlib import Path
from lxml import html
import re

SOURCE_BASE = Path(r"Z:\ZhennanZ Folder\000-Marathon-Story-2024-2025\20240303-AR-Little Rock Marathon\0000-Web")
SOURCE_HTML = next(p for p in SOURCE_BASE.iterdir() if p.suffix.lower() == ".html")

def norm(value: str) -> str:
    return re.sub(r"\s+", " ", value.replace("\xa0", " ")).strip()

def is_styleish(value: str) -> bool:
    return ":host {" in value or "--weui-" in value or len(value) > 1200

def has_desc_leaf_container(el) -> bool:
    for desc in el.iterdescendants():
        if desc.tag in ("p", "section"):
            text = norm("".join(desc.itertext()))
            if text and not is_styleish(text):
                return True
    return False

def extract_story():
    source = SOURCE_HTML.read_text(encoding="utf-8", errors="replace")
    doc = html.fromstring(source)
    root = doc.xpath('//*[@id="js_content"]')[0]
    events = []

    def walk(el):
        if el.tag == "img":
            src = el.get("src") or el.get("data-src") or ""
            if src:
                events.append({"type": "img", "src": src})
            return
        if el.tag in ("p", "section"):
            text = norm("".join(el.itertext()))
            if text and not is_styleish(text) and not has_desc_leaf_container(el):
                if text not in ["，赞"] and not text.startswith("鲜花"):
                    events.append({"type": "text", "text": text})
                for img in el.xpath(".//img"):
                    src = img.get("src") or img.get("data-src") or ""
                    if src:
                        events.append({"type": "img", "src": src})
                return
        for child in el:
            walk(child)

    for child in root:
        walk(child)

    clean = []
    for idx, event in enumerate(events):
        key = (event["type"], event.get("text") or event.get("src"))
        prev = (clean[-1][1]["type"], clean[-1][1].get("text") or clean[-1][1].get("src")) if clean else None
        if prev != key:
            clean.append((idx, event))

    # We start from index 5 or when the real content begins
    story = clean
    return story

def main():
    story = extract_story()
    out_lines = []
    for idx, event in story:
        if event["type"] == "text":
            out_lines.append(f"{idx}: {event['text']}")
        else:
            out_lines.append(f"{idx}: [IMAGE] {event['src']}")
    
    Path("tools/little_rock_raw_blocks.txt").write_text("\n".join(out_lines), encoding="utf-8")
    print(f"Dumped {len(story)} blocks to tools/little_rock_raw_blocks.txt")

if __name__ == "__main__":
    main()
