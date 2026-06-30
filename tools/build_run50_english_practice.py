import asyncio
import html
import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

import edge_tts


ROOT = Path(__file__).resolve().parents[1]
RUN50 = ROOT / "run50"
SOURCE = RUN50 / "run50.html"
CACHE_PATH = ROOT / "work" / "run50-english-practice-translation-cache.json"

VOICE = "en-US-BrianNeural"
VERSION = "20260630-brian-batch-v1"

TARGETS = [
    {
        "id": "script-ky",
        "slug": "hatfield-mccoy-english-practice",
        "audio": "hatfield-mccoy-english-practice",
        "title": "#01 Kentucky | Hatfield-McCoy Marathon",
        "tag": "RUN50 #01 | READ-ALONG",
        "stats": ["Kentucky", "Williamson", "4h20m", "25th | Feud"],
        "stats_sub": ["State", "Town", "Finish time", "Race note"],
        "color": "#1a2a3a",
        "accent": "#8aa3bd",
    },
    {
        "id": "script-ky-derby",
        "slug": "louisville-derby-english-practice",
        "audio": "louisville-derby-english-practice",
        "title": "#01+ Kentucky | Louisville Derby Marathon",
        "tag": "RUN50 #01+ | READ-ALONG",
        "stats": ["Kentucky", "Louisville", "3h57m", "Sub-4"],
        "stats_sub": ["State", "City", "Finish time", "Race note"],
        "color": "#8B2027",
        "accent": "#d4a373",
    },
    {
        "id": "script-ky-grad",
        "slug": "louisville-2024-english-practice",
        "audio": "louisville-2024-english-practice",
        "title": "#01++ Kentucky | Louisville Marathon",
        "tag": "RUN50 #01++ | READ-ALONG",
        "stats": ["Kentucky", "Louisville", "Black-gold medal", "PhD finish"],
        "stats_sub": ["State", "City", "Record", "Race note"],
        "color": "#1C4A2A",
        "accent": "#c9a44d",
    },
    {
        "id": "script-fl",
        "slug": "miami-english-practice",
        "audio": "miami-english-practice",
        "title": "#15 Florida | Miami Marathon",
        "tag": "RUN50 #15 | READ-ALONG",
        "stats": ["Florida", "Miami", "2024.01.28", "Messi's town"],
        "stats_sub": ["State", "City", "Race date", "Theme"],
        "color": "#006272",
        "accent": "#f6b44b",
    },
    {
        "id": "script-nc",
        "slug": "north-carolina-oak-island-english-practice",
        "audio": "north-carolina-oak-island-english-practice",
        "title": "#16 North Carolina | Oak Island Marathon",
        "tag": "RUN50 #16 | READ-ALONG",
        "stats": ["North Carolina", "Oak Island", "2024.02.18", "Atlantic PB"],
        "stats_sub": ["State", "Town", "Race date", "Theme"],
        "color": "#13294B",
        "accent": "#56b5e8",
    },
    {
        "id": "script-ar",
        "slug": "little-rock-english-practice",
        "audio": "little-rock-english-practice",
        "title": "#17 Arkansas | Little Rock Marathon",
        "tag": "RUN50 #17 | READ-ALONG",
        "stats": ["Arkansas", "Little Rock", "2024.03.03", "Big medal"],
        "stats_sub": ["State", "City", "Race date", "Theme"],
        "color": "#9D2235",
        "accent": "#d9a441",
    },
    {
        "id": "script-sc",
        "slug": "south-carolina-english-practice",
        "audio": "south-carolina-english-practice",
        "title": "#18 South Carolina | 2Slow4Boston",
        "tag": "RUN50 #18 | READ-ALONG",
        "stats": ["South Carolina", "Greer", "2024.04.14", "20 loops"],
        "stats_sub": ["State", "Town", "Race date", "Theme"],
        "color": "#003087",
        "accent": "#79b38a",
    },
    {
        "id": "script-pa",
        "slug": "pittsburgh-english-practice",
        "audio": "pittsburgh-english-practice",
        "title": "#19 Pennsylvania | Pittsburgh Marathon",
        "tag": "RUN50 #19 | READ-ALONG",
        "stats": ["Pennsylvania", "Pittsburgh", "2024.05.04", "Bridges"],
        "stats_sub": ["State", "City", "Race date", "Theme"],
        "color": "#1C2951",
        "accent": "#ffb612",
    },
    {
        "id": "script-mi",
        "slug": "michigan-english-practice",
        "audio": "michigan-english-practice",
        "title": "#21 Michigan | Grand Rapids Marathon",
        "tag": "RUN50 #21 | READ-ALONG",
        "stats": ["Michigan", "Grand Rapids", "2024.08.25", "Hot comeback"],
        "stats_sub": ["State", "City", "Race date", "Theme"],
        "color": "#00274C",
        "accent": "#ffcb05",
    },
    {
        "id": "script-nh",
        "slug": "new-hampshire-english-practice",
        "audio": "new-hampshire-english-practice",
        "title": "#22 New Hampshire | Clarence DeMar Marathon",
        "tag": "RUN50 #22 | READ-ALONG",
        "stats": ["New Hampshire", "Keene", "2024.09.28", "Fall colors"],
        "stats_sub": ["State", "City", "Race date", "Theme"],
        "color": "#1B3A2D",
        "accent": "#d97845",
    },
]


def strip_tags(value: str) -> str:
    value = re.sub(r"<br\s*/?>", " ", value, flags=re.I)
    value = re.sub(r"<[^>]+>", "", value)
    value = html.unescape(value)
    value = re.sub(r"[\U0001F300-\U0001FAFF\u2600-\u27BF]", "", value)
    value = value.replace("(环境音：模拟踩在落叶上的碎裂声)", "")
    value = re.sub(r"\([^)]*BGM[^)]*\)", "", value, flags=re.I)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def strip_emoji(value: str) -> str:
    return re.sub(r"[\U0001F300-\U0001FAFF\u2600-\u27BF\ufe0f]", "", value)


def split_sentences(text: str) -> list[str]:
    text = strip_emoji(text)
    pieces = re.split(r"(?<=[。！？!?])\s*", text)
    out = []
    for piece in pieces:
        piece = piece.strip()
        if not piece or not re.search(r"[\w\u4e00-\u9fff]", piece):
            continue
        if len(piece) > 90:
            halves = re.split(r"[；;]", piece)
            out.extend([h.strip() for h in halves if re.search(r"[\w\u4e00-\u9fff]", h)])
        else:
            out.append(piece)
    return out


def extract_block(source: str, script_id: str) -> str:
    start = source.index(f'id="{script_id}"')
    next_match = re.search(r'\n\s*<div id="script-', source[start + 10 :])
    end = start + 10 + next_match.start() if next_match else source.index("<link ", start)
    return source[start:end]


def extract_rows(source: str, script_id: str) -> list[dict]:
    block = extract_block(source, script_id)
    rows = []
    for match in re.finditer(
        r'<div class="cue-tag">(?P<cue>.*?)</div>\s*<div class="script-text">(?P<text>.*?)</div>',
        block,
        re.S,
    ):
        cue = strip_tags(match.group("cue"))
        text = strip_tags(match.group("text"))
        for idx, sentence in enumerate(split_sentences(text)):
            sentence = strip_emoji(sentence).strip()
            if not re.search(r"[\w\u4e00-\u9fff]", sentence):
                continue
            cue_label = cue if idx == 0 else cue + f".{idx + 1}"
            rows.append({"cue": cue_label, "zh": sentence})
    return rows


def load_cache() -> dict:
    if CACHE_PATH.exists():
        return json.loads(CACHE_PATH.read_text(encoding="utf-8"))
    return {}


def save_cache(cache: dict) -> None:
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CACHE_PATH.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")


def translate_one(text: str, cache: dict) -> str:
    key = "zh-en:" + text
    if key in cache:
        cleaned = polish_translation(cache[key])
        cache[key] = cleaned
        return cleaned
    params = urllib.parse.urlencode(
        {"client": "gtx", "sl": "zh-CN", "tl": "en", "dt": "t", "q": text}
    )
    url = "https://translate.googleapis.com/translate_a/single?" + params
    for attempt in range(5):
        try:
            with urllib.request.urlopen(url, timeout=20) as response:
                payload = json.loads(response.read().decode("utf-8"))
            translated = "".join(part[0] for part in payload[0] if part[0]).strip()
            translated = polish_translation(translated)
            cache[key] = translated
            save_cache(cache)
            time.sleep(0.08)
            return translated
        except Exception:
            if attempt == 4:
                raise
            time.sleep(1.5 + attempt)
    raise RuntimeError("unreachable")


def polish_translation(text: str) -> str:
    replacements = {
        "Hello everyone": "Hey everyone",
        "I am Asennan": "I'm Asennan",
        "here is-Asennan": "this is Asennan",
        "Run50 came to": "Run50 takes us to",
        "marathon": "marathon",
        "Siqi": "Siqi",
        "Louisville": "Louisville",
        "Green Bay": "Green Bay",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = strip_emoji(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


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


def page_html(target: dict, rows: list[dict]) -> str:
    data = []
    for row in rows:
        data.append(
            {
                "cue": row["cue"],
                "en": row["en"],
                "zh": row["zh"],
                "tip": tip_for(row["en"]),
            }
        )
    color = target["color"]
    accent = target["accent"]
    stats = "".join(
        f'<div class="stat"><div class="v">{html.escape(v)}</div><div class="t">{html.escape(t)}</div></div>'
        for v, t in zip(target["stats"], target["stats_sub"])
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(target["title"])} — English Read-Along</title>
<style>
  :root{{--green:{color};--green2:{color};--gold:{accent};--paper:#f5f8f7;--ink:#1f2d27;--muted:#6b7d75;--line:#dfeae4}}
  *{{box-sizing:border-box}} body{{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,"PingFang SC","Microsoft YaHei",sans-serif;background:#e9efeb;color:var(--ink);line-height:1.6}}
  .wrap{{max-width:880px;margin:0 auto;padding:0 0 80px}} .banner{{background:var(--green);color:#fff;border-bottom:6px solid var(--gold);padding:28px 26px 24px;position:relative}}
  .tag{{display:inline-block;background:var(--gold);color:var(--green);font-weight:800;font-size:12px;letter-spacing:.5px;padding:4px 10px;border-radius:5px}}
  .banner h1{{margin:12px 0 6px;font-size:24px;line-height:1.3}} .banner .sub{{color:rgba(255,255,255,.72);font-size:14px}}
  .backbtn{{position:absolute;top:14px;right:16px;background:rgba(255,255,255,.18);color:#fff;border:none;border-radius:6px;padding:6px 12px;font-size:13px;cursor:pointer;text-decoration:none;backdrop-filter:blur(4px)}} .backbtn:hover{{background:rgba(255,255,255,.3)}}
  .controls{{background:#fff;position:sticky;top:0;z-index:30;border-bottom:1px solid var(--line);padding:12px 18px;display:flex;flex-wrap:wrap;gap:10px 16px;align-items:center;box-shadow:0 2px 10px rgba(0,0,0,.05)}}
  .controls .grp{{display:flex;align-items:center;gap:8px}} .controls label{{font-size:13px;color:var(--muted);white-space:nowrap}} select,button{{font-family:inherit}} select{{padding:6px 8px;border:1px solid var(--line);border-radius:6px;background:#fff;font-size:13px;max-width:200px}}
  .btn{{background:var(--green);color:#fff;border:none;border-radius:8px;padding:8px 14px;font-size:14px;font-weight:700;cursor:pointer;display:inline-flex;align-items:center;gap:6px}} .btn:hover{{filter:brightness(1.08)}} .btn.ghost{{background:#eef4f1;color:var(--green)}} .btn.ghost:hover{{background:#e0ece6}} .btn:disabled{{opacity:.5;cursor:not-allowed}} input[type=range]{{accent-color:var(--green)}} .rateval{{font-weight:800;color:var(--green);font-size:13px;min-width:38px;text-align:center}}
  .hint{{background:#fffbe9;border-left:4px solid var(--gold);color:#6a5a1e;margin:18px;padding:12px 14px;border-radius:8px;font-size:13.5px}} .hint b{{color:#8a6d14}} .hint code{{background:rgba(255,255,255,.65);border:1px solid rgba(138,109,20,.18);border-radius:5px;padding:1px 5px;font-family:ui-monospace,SFMono-Regular,Consolas,monospace;font-size:12px}}
  .stats{{display:flex;flex-wrap:wrap;gap:10px;padding:0 18px;margin:16px 0 4px}} .stat{{flex:1;min-width:120px;background:#fff;border:1px solid var(--line);border-radius:10px;padding:10px 12px;text-align:center}} .stat .v{{font-weight:800;color:var(--green);font-size:16px}} .stat .t{{font-size:11px;color:var(--muted);margin-top:2px}}
  .list{{padding:8px 18px}} .row{{background:#fff;border:1px solid var(--line);border-radius:12px;padding:14px 14px 14px 16px;margin:12px 0;display:flex;gap:12px;align-items:flex-start;transition:.15s;position:relative;border-left:4px solid transparent}} .row.active{{border-left-color:var(--gold);box-shadow:0 4px 16px rgba(18,70,52,.12);background:#fcfffe}} .row .num{{font-size:11px;color:#fff;background:var(--green);border-radius:5px;padding:2px 7px;font-weight:800;white-space:nowrap;margin-top:3px}} .row .body{{flex:1;min-width:0}} .row .cue{{font-size:11px;color:var(--muted);margin-bottom:4px}} .row .en{{font-size:18px;line-height:1.55;color:var(--ink)}} .row.active .en{{color:var(--green)}} .row .zh{{font-size:13.5px;color:var(--muted);margin-top:6px;display:none}} .row.show-zh .zh{{display:block}} .row .tip{{font-size:12.5px;color:#7a5a00;background:#fff8e1;border:1px dashed #e7c66b;border-radius:8px;padding:6px 10px;margin-top:8px;line-height:1.7;display:none}} .row.show-tip .tip{{display:block}} .row .ops{{display:flex;flex-direction:column;gap:6px;align-items:center}} .iconbtn{{width:38px;height:38px;border-radius:50%;border:none;cursor:pointer;font-size:15px;display:flex;align-items:center;justify-content:center;background:#eef4f1;color:var(--green)}} .iconbtn:hover{{background:var(--green);color:#fff}} .iconbtn.on{{background:var(--gold);color:var(--green)}}
  .rec{{background:#fff;border:1px solid var(--line);border-radius:12px;margin:18px;padding:16px}} .rec h3{{margin:0 0 4px;color:var(--green);font-size:16px}} .rec p{{margin:0 0 12px;font-size:13px;color:var(--muted)}} .rec .recrow{{display:flex;flex-wrap:wrap;gap:10px;align-items:center}} .dot{{width:10px;height:10px;border-radius:50%;background:#cdd;display:inline-block;margin-right:6px}} .dot.live{{background:#e23;animation:pulse 1s infinite}} @keyframes pulse{{50%{{opacity:.3}}}} audio{{height:34px}} .foot{{text-align:center;color:var(--muted);font-size:12px;padding:24px}} @media(max-width:600px){{.banner h1{{font-size:20px}}.row .en{{font-size:16px}}.controls{{gap:8px 10px}}}}
</style>
</head>
<body>
<div class="wrap">
  <div class="banner">
    <span class="tag">{html.escape(target["tag"])}</span>
    <h1>{html.escape(target["title"])}</h1>
    <div class="sub">English script for read-along practice · Natural voice audio · 中英对照逐句跟读</div>
    <a class="backbtn" href="run50.html">← 返回口播稿</a>
  </div>
  <div class="controls">
    <div class="grp"><button class="btn" id="playAll">▶ 全文连读</button><button class="btn ghost" id="stopBtn">■ 停止</button></div>
    <div class="grp"><label>语速</label><input type="range" id="rate" min="0.5" max="1.1" step="0.05" value="1"><span class="rateval" id="rateval">1.00x</span></div>
    <div class="grp"><label>备用发音</label><select id="voice"></select></div>
    <div class="grp"><button class="btn ghost" id="toggleTip">🗣 发音提示</button><button class="btn ghost" id="toggleZh">显示中文</button></div>
  </div>
  <div class="hint"><b>🔊 使用提示：</b>点每句右边的 <b>▶</b> 听自然人声音频；点 <b>🔁</b> 循环跟读。缺少对应 mp3 时才会临时回退到浏览器备用发音。</div>
  <div class="hint"><b>🎧 人声音频模式：</b>音频文件位于 <code>run50/audio/{html.escape(target["audio"])}/01.mp3</code> 起，逐句对应本页文本。</div>
  <div class="stats">{stats}</div>
  <div class="list" id="list"></div>
  <div class="rec"><h3>🎙️ 录音对比练习</h3><p>先选上面任意一句，再录下自己的发音，对比原句。</p><div class="recrow"><button class="btn" id="recBtn"><span class="dot" id="recDot"></span>开始录音</button><button class="btn ghost" id="playOrig" disabled>▶ 听原句</button><button class="btn ghost" id="playMine" disabled>▶ 听我的录音</button><button class="btn ghost" id="playCompare" disabled>⇄ 原句→我的 对比</button></div><p id="recStatus" style="margin-top:10px">当前选中：<b id="selText">（未选择，点上面任意一句）</b></p><audio id="myAudio" controls style="display:none;width:100%;margin-top:6px"></audio></div>
  <div class="foot">© Run50 · English Read-Along · 愿每一双跑鞋都不被辜负</div>
</div>
<script>
const DATA = {json.dumps(data, ensure_ascii=False, indent=2)};
const listEl = document.getElementById('list');
const rows = [];
DATA.forEach((d) => {{
  const idx = rows.length;
  const row = document.createElement('div');
  row.className = 'row';
  row.innerHTML = '<div class="num">'+(idx+1)+'</div><div class="body"><div class="cue">'+d.cue+'</div><div class="en">'+d.en+'</div>'+(d.tip ? '<div class="tip">🗣 '+d.tip+'</div>' : '')+'<div class="zh">'+d.zh+'</div></div><div class="ops"><button class="iconbtn play" title="朗读这一句">▶</button><button class="iconbtn loop" title="循环这一句">🔁</button></div>';
  listEl.appendChild(row);
  const rec = {{el:row, idx:idx, data:d}};
  rows.push(rec);
  row.querySelector('.play').addEventListener('click', e=>{{ e.stopPropagation(); selectRow(idx); speakOne(idx); }});
  row.querySelector('.loop').addEventListener('click', e=>{{ e.stopPropagation(); toggleLoop(idx, e.currentTarget); }});
  row.addEventListener('click', ()=> selectRow(idx));
}});
const synth = window.speechSynthesis;
const voiceSel = document.getElementById('voice');
const rateEl = document.getElementById('rate');
const ratevalEl = document.getElementById('rateval');
const humanAudio = new Audio();
const HUMAN_AUDIO_BASE = 'audio/{target["audio"]}';
const HUMAN_AUDIO_VERSION = '{VERSION}';
let voices = [], chosenVoice = null, loopIdx = -1, playingAll = false, selected = -1, playToken = 0;
rateEl.addEventListener('input', ()=> ratevalEl.textContent = (+rateEl.value).toFixed(2)+'x');
function isUS(v){{ return /en[-_]US/i.test(v.lang) || /English.*United States/i.test(v.name); }}
function isEN(v){{ return /^en/i.test(v.lang) || /\\bEnglish\\b/i.test(v.name); }}
function loadVoices(){{ const all = synth.getVoices(); if(!all.length) return false; const us = all.filter(isUS); const en = all.filter(v => isEN(v) && !isUS(v)); voices = (us.length ? us.concat(en) : en.length ? en : all); voiceSel.innerHTML=''; voices.forEach((v,i)=>{{ const o=document.createElement('option'); o.value=i; o.textContent=v.name+' ('+v.lang+')'; voiceSel.appendChild(o); }}); chosenVoice=voices[0]||null; return true; }}
voiceSel.addEventListener('change', ()=> chosenVoice = voices[+voiceSel.value]); if(synth.onvoiceschanged !== undefined) synth.onvoiceschanged = loadVoices; (function tryLoad(n){{ if(loadVoices()) return; if(n>0) setTimeout(()=>tryLoad(n-1), 300); }})(10);
function makeUtter(text){{ const u = new SpeechSynthesisUtterance(text); if(chosenVoice) u.voice = chosenVoice; u.lang = (chosenVoice && chosenVoice.lang) || 'en-US'; u.rate = +rateEl.value; return u; }}
function humanAudioSrc(idx){{ return HUMAN_AUDIO_BASE + '/' + String(idx + 1).padStart(2, '0') + '.mp3?v=' + HUMAN_AUDIO_VERSION; }}
function stopCurrentVoice(){{ playToken++; synth.cancel(); humanAudio.pause(); humanAudio.removeAttribute('src'); humanAudio.load(); }}
function selectRow(idx){{ selected = idx; rows.forEach((r,i)=> r.el.classList.toggle('active', i===idx)); document.getElementById('selText').textContent = rows[idx].data.en; document.getElementById('playOrig').disabled = false; refreshCompareBtns(); }}
function speakOne(idx, after){{ const token = ++playToken; synth.cancel(); humanAudio.pause(); const done = ()=>{{ if(token !== playToken) return; if(loopIdx===idx){{ setTimeout(()=>{{ if(loopIdx===idx) speakOne(idx); }}, 500); return; }} if(after) after(); }}; const fallbackToTts = ()=>{{ if(token !== playToken) return; humanAudio.onerror = null; const u = makeUtter(rows[idx].data.en); u.onend = done; synth.speak(u); }}; let fellBack = false; const fallbackOnce = ()=>{{ if(fellBack) return; fellBack = true; fallbackToTts(); }}; humanAudio.onended = done; humanAudio.onerror = fallbackOnce; humanAudio.src = humanAudioSrc(idx); humanAudio.currentTime = 0; humanAudio.playbackRate = +rateEl.value; humanAudio.play().catch(fallbackOnce); }}
function toggleLoop(idx, btn){{ document.querySelectorAll('.iconbtn.loop').forEach(b=>b.classList.remove('on')); if(loopIdx===idx){{ loopIdx=-1; stopCurrentVoice(); return; }} loopIdx = idx; btn.classList.add('on'); playingAll = false; selectRow(idx); speakOne(idx); }}
document.getElementById('playAll').addEventListener('click', ()=>{{ loopIdx = -1; document.querySelectorAll('.iconbtn.loop').forEach(b=>b.classList.remove('on')); stopCurrentVoice(); playingAll = true; let i = 0; const step = ()=>{{ if(!playingAll || i>=rows.length){{ playingAll=false; rows.forEach(r=>r.el.classList.remove('active')); return; }} selectRow(i); rows[i].el.scrollIntoView({{behavior:'smooth', block:'center'}}); speakOne(i, ()=>{{ i++; step(); }}); }}; step(); }});
document.getElementById('stopBtn').addEventListener('click', ()=>{{ playingAll=false; loopIdx=-1; document.querySelectorAll('.iconbtn.loop').forEach(b=>b.classList.remove('on')); stopCurrentVoice(); }});
let showTip = false; document.getElementById('toggleTip').addEventListener('click', e=>{{ showTip=!showTip; rows.forEach(r=>r.el.classList.toggle('show-tip', showTip)); e.currentTarget.textContent = showTip ? '🗣 隐藏提示' : '🗣 发音提示'; }});
let showZh = false; document.getElementById('toggleZh').addEventListener('click', e=>{{ showZh=!showZh; rows.forEach(r=>r.el.classList.toggle('show-zh', showZh)); e.currentTarget.textContent = showZh ? '隐藏中文' : '显示中文'; }});
let mediaRec=null, chunks=[], myURL=null, recording=false; const recBtn=document.getElementById('recBtn'), recDot=document.getElementById('recDot'), myAudio=document.getElementById('myAudio');
function refreshCompareBtns(){{ const has=!!myURL, sel=selected>=0; document.getElementById('playMine').disabled=!has; document.getElementById('playCompare').disabled=!(has&&sel); }}
recBtn.addEventListener('click', async ()=>{{ if(recording){{ mediaRec.stop(); return; }} try{{ const stream=await navigator.mediaDevices.getUserMedia({{audio:true}}); mediaRec=new MediaRecorder(stream); chunks=[]; mediaRec.ondataavailable=e=>chunks.push(e.data); mediaRec.onstop=()=>{{ const blob=new Blob(chunks, {{type:'audio/webm'}}); if(myURL) URL.revokeObjectURL(myURL); myURL=URL.createObjectURL(blob); myAudio.src=myURL; myAudio.style.display='block'; recording=false; recDot.classList.remove('live'); recBtn.lastChild.textContent='重新录音'; stream.getTracks().forEach(t=>t.stop()); refreshCompareBtns(); }}; mediaRec.start(); recording=true; recDot.classList.add('live'); recBtn.lastChild.textContent='停止录音'; }}catch(err){{ alert('无法访问麦克风：'+err.message+'\\n请在浏览器允许麦克风权限后重试。'); }} }});
document.getElementById('playOrig').addEventListener('click', ()=>{{ if(selected>=0) speakOne(selected); }}); document.getElementById('playMine').addEventListener('click', ()=>{{ if(myURL){{ myAudio.currentTime=0; myAudio.play(); }} }}); document.getElementById('playCompare').addEventListener('click', ()=>{{ if(selected<0 || !myURL) return; stopCurrentVoice(); speakOne(selected, ()=> setTimeout(()=>{{ myAudio.currentTime=0; myAudio.play(); }}, 400)); }}); window.addEventListener('beforeunload', ()=> stopCurrentVoice());
</script>
</body>
</html>
"""


async def make_audio(target: dict, rows: list[dict]) -> None:
    out_dir = RUN50 / "audio" / target["audio"]
    out_dir.mkdir(parents=True, exist_ok=True)
    for i, row in enumerate(rows, start=1):
        out = out_dir / f"{i:02d}.mp3"
        if out.exists() and out.stat().st_size > 1000:
            continue
        text = strip_emoji(row["en"])
        for attempt in range(5):
            try:
                communicate = edge_tts.Communicate(text, VOICE, rate="+2%")
                await communicate.save(str(out))
                break
            except Exception:
                if out.exists():
                    out.unlink()
                if attempt == 4:
                    raise
                await asyncio.sleep(2 + attempt * 2)
        print(f"  audio {target['slug']} {i:02d}/{len(rows)}")
    (out_dir / "README.md").write_text(
        f"# {target['title']} Voice Audio\n\nGenerated with `{VOICE}` for `{target['slug']}.html`.\n",
        encoding="utf-8",
    )


def update_run50_links(source: str) -> str:
    for target in TARGETS:
        script_id = target["id"]
        href = f'{target["slug"]}.html'
        source = re.sub(
            rf'<a href="{re.escape(href)}" style="[^"]+">🎧 英文跟读</a>\s*',
            "",
            source,
        )
        marker = f'<div id="{script_id}"'
        start = source.index(marker)
        button_start = source.index('<button onclick="showWelcome()"', start)
        button = (
            f'<a href="{href}" style="position:absolute;top:12px;right:90px;background:{target["accent"]};'
            f'color:{target["color"]};font-weight:700;border:none;border-radius:6px;padding:4px 10px;'
            f'font-size:12px;cursor:pointer;text-decoration:none">🎧 英文跟读</a>\n            '
        )
        source = source[:button_start] + button + source[button_start:]
    return source


async def main() -> None:
    source = SOURCE.read_text(encoding="utf-8")
    cache = load_cache()
    generated = []
    for target in TARGETS:
        print(f"Building {target['slug']}...")
        rows = extract_rows(source, target["id"])
        for row in rows:
            row["en"] = translate_one(row["zh"], cache)
        page_path = RUN50 / f"{target['slug']}.html"
        page_path.write_text(page_html(target, rows), encoding="utf-8", newline="\n")
        await make_audio(target, rows)
        generated.append((target["slug"], len(rows)))
    updated = update_run50_links(source)
    SOURCE.write_text(updated, encoding="utf-8", newline="\n")
    print("Generated pages:")
    for slug, count in generated:
        print(f"  {slug}.html ({count} rows)")


if __name__ == "__main__":
    asyncio.run(main())
