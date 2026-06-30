import asyncio
import html
import json
import re
from pathlib import Path

import edge_tts


ROOT = Path(__file__).resolve().parents[1]
RUN50 = ROOT / "run50"
VERSION = "20260630-multivoice-v2"

VOICES = [
    ("en-US-BrianNeural", "Brian - casual male"),
    ("en-US-AndrewNeural", "Andrew - warm male"),
    ("en-US-AvaNeural", "Ava - friendly female"),
    ("en-US-EmmaNeural", "Emma - clear female"),
]


def strip_emoji(value: str) -> str:
    return re.sub(r"[\U0001F300-\U0001FAFF\u2600-\u27BF\ufe0f]", "", value).strip()


def tip_for(text: str) -> str:
    words = re.findall(r"[A-Za-z][A-Za-z'-]{3,}", text)
    stop = {
        "that",
        "this",
        "with",
        "from",
        "there",
        "were",
        "have",
        "about",
        "would",
        "could",
        "just",
        "into",
        "your",
        "then",
        "than",
    }
    picks = []
    for word in words:
        clean = word.strip("'").upper()
        if clean.lower() not in stop and clean not in picks:
            picks.append(clean)
        if len(picks) == 3:
            break
    return "重音: " + " · ".join(picks or ["RUN", "RACE", "STATE"])


def voice_for(index: int) -> tuple[str, str]:
    # Keep one voice for a short scene so it sounds like narration, not a random splice.
    return VOICES[(index // 6) % len(VOICES)]


def native_polish(text: str) -> str:
    replacements = {
        "Hey everyone, this is - Asen Man.": "Hey everyone, I'm Asennan.",
        "Hey everyone, this is - Asennan.": "Hey everyone, I'm Asennan.",
        "Hello everyone, this is - Asen Man.": "Hey everyone, I'm Asennan.",
        "This time, Run50 comes to": "This time, Run50 takes us to",
        "This time Run50 comes to": "This time, Run50 takes us to",
        "Run50 comes to": "Run50 takes us to",
        "I want to talk about": "we're talking about",
        "the United States -": "the U.S.:",
        "United States -": "the U.S.:",
        "This is a state that doesn’t have a strong presence": "This state tends to fly under the radar",
        "This is a state that doesn't have a strong presence": "This state tends to fly under the radar",
        "the gang leader Capone": "mob boss Al Capone",
        "gang leader Capone": "mob boss Al Capone",
        "Indian language": "Native American language",
        "The genes of the Boston Marathon grew out of here.": "You can feel the roots of the Boston Marathon around here.",
        "Moreover, there were volunteers cheering on both sides.": "And yes, volunteers were cheering on both sides.",
        "This was definitely the most awesome marathon I’ve ever run.": "This might be the most over-the-top marathon I've ever run.",
        "This is the marathon I have ever run - the biggest medal.": "This race had the biggest medal I've ever seen at a marathon.",
        "the second Florida, Miami Marathon": "state number fifteen, Florida: the Miami Marathon",
        "on the front lines of frequent hurricanes": "right in hurricane country",
        "This is the hometown of Disney": "It's home to Disney",
        "is surrounded by sea on three sides": "is wrapped by water on three sides",
        "It is the inspiration city of GTA6": "It's the city that inspired GTA 6",
        "an Native American language": "a Native American language",
        "For this Run50 episode, we're talking about the 15th state I ran in the U.S.: state number fifteen, Florida: the Miami Marathon.": "For this Run50 episode, we're in my 15th U.S. state: Florida, for the Miami Marathon.",
        "New England includes Maine, Vermont, New Hampshire, Massachusetts, Connecticut and Rhode Island. It is the earliest colony in the United States, with a rich history and beautiful autumn colors.": "New England includes Maine, Vermont, New Hampshire, Massachusetts, Connecticut, and Rhode Island. The region has some of America's earliest colonial history, plus gorgeous fall colors.",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = re.sub(r"\bThis time I return to the Run50 series and ", "For this Run50 episode, ", text)
    text = re.sub(r"\blocated in the ([^,]+),", r"in the \1,", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract_data_array(source: str) -> tuple[str, str] | None:
    match = re.search(r"const DATA = (\[[\s\S]*?\n\]);", source)
    if not match:
        return None
    return match.group(1), match.group(0)


def update_json_data(source: str) -> tuple[str, list[str], list[str]] | None:
    extracted = extract_data_array(source)
    if not extracted:
        return None
    raw_array, full_decl = extracted
    try:
        rows = json.loads(raw_array)
    except json.JSONDecodeError:
        return None

    spoken_texts = []
    voice_names = []
    for index, row in enumerate(rows):
        if "en" not in row:
            continue
        row["en"] = native_polish(row["en"])
        row["tip"] = tip_for(row["en"])
        voice, label = voice_for(len(spoken_texts))
        row["voice"] = label
        spoken_texts.append(row["en"])
        voice_names.append(voice)

    new_decl = "const DATA = " + json.dumps(rows, ensure_ascii=False, indent=2) + ";"
    return source.replace(full_decl, new_decl), spoken_texts, voice_names


def extract_spoken_texts_fallback(source: str) -> tuple[list[str], list[str]]:
    spoken = []
    for match in re.finditer(r'en:"((?:\\.|[^"\\])*)"', source):
        text = match.group(1)
        text = bytes(text, "utf-8").decode("unicode_escape")
        spoken.append(html.unescape(native_polish(text)))
    voices = [voice_for(i)[0] for i in range(len(spoken))]
    return spoken, voices


def update_version_and_labels(source: str) -> str:
    source = re.sub(
        r"HUMAN_AUDIO_VERSION = '[^']+'",
        f"HUMAN_AUDIO_VERSION = '{VERSION}'",
        source,
    )
    source = source.replace(
        "English script for read-along practice · Natural voice audio · 中英对照逐句跟读",
        "English script for read-along practice · Multi-voice natural audio · 中英对照逐句跟读",
    )
    source = source.replace(
        "自然人声音频",
        "多音色自然人声音频",
    )
    return source


async def synthesize(text: str, voice: str, out: Path) -> None:
    clean = strip_emoji(text)
    if not clean:
        raise ValueError(f"Empty audio text for {out}")
    tmp = out.with_suffix(".tmp.mp3")
    if tmp.exists():
        tmp.unlink()
    for attempt in range(5):
        try:
            communicate = edge_tts.Communicate(clean, voice, rate="+2%")
            await communicate.save(str(tmp))
            if tmp.stat().st_size <= 1000:
                raise RuntimeError("Generated audio was too small")
            tmp.replace(out)
            return
        except Exception:
            if tmp.exists():
                tmp.unlink()
            if attempt == 4:
                raise
            await asyncio.sleep(2 + attempt * 2)


async def refresh_page(page: Path) -> tuple[str, int]:
    source = page.read_text(encoding="utf-8")
    updated = update_json_data(source)
    if updated:
        source, spoken_texts, voice_names = updated
    else:
        spoken_texts, voice_names = extract_spoken_texts_fallback(source)
    source = update_version_and_labels(source)
    page.write_text(source, encoding="utf-8", newline="\n")

    slug = page.stem
    audio_dir = RUN50 / "audio" / slug
    audio_dir.mkdir(parents=True, exist_ok=True)
    for stale in audio_dir.glob("*.mp3"):
        stale.unlink()
    for index, (text, voice) in enumerate(zip(spoken_texts, voice_names), start=1):
        await synthesize(text, voice, audio_dir / f"{index:02d}.mp3")
    (audio_dir / "README.md").write_text(
        "# Multi-Voice Read-Along Audio\n\n"
        f"Generated for `{page.name}` with {', '.join(label for _, label in VOICES)}.\n"
        f"Cache version: `{VERSION}`.\n",
        encoding="utf-8",
    )
    return slug, len(spoken_texts)


async def main() -> None:
    pages = sorted(RUN50.glob("*-english-practice.html"))
    for page in pages:
        slug, count = await refresh_page(page)
        print(f"{slug}: {count} clips")


if __name__ == "__main__":
    asyncio.run(main())
