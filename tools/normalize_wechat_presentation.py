"""Keep WeChat reader-safe logos and one shared credit per connected photo group.

Run after article builders, and before publishing. Uses only the standard library.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

def normalize(html):
    counts = [0, 0]
    def brand(match):
        original = match[0]
        # RunCN uses a separate mountain wordmark with opaque themed backgrounds.
        # Keep its theme pair; this fix is for the transparent Run50 robot.
        if 'RunCN' in original:
            return original
        def media(m):
            tag = m[0]
            dark = re.search(r'data-dark-src="([^"]+)"', tag)
            url = dark[1] if dark else ('/assets/run50-cutout-intro-dark-still.png' if tag.startswith('<source') else '/assets/run50-cutout-intro-dark.gif')
            return re.sub(r'((?:data-light-src|data-dark-src|src|srcset)=)"[^"]*"', lambda a: a[1]+'"'+url+'"', tag)
        updated = re.sub(r'<(?:img|source)\b[^>]*>', media, original)
        counts[0] += updated != original
        return updated
    html = re.sub(r'<picture\b[^>]*class="brand-intro"[^>]*>.*?</picture>', brand, html, flags=re.S)
    def figure(match):
        original = match[0]
        if len(re.findall(r'<img\b', original)) < 2:
            return original
        def caption(m):
            lines = re.split(r'<br\s*/?>', m[2])
            parts = [re.fullmatch(r'(.*?)\s*[·|]\s*(摄影\s*[/|]\s*[^<>]+?)\s*', line, re.S) for line in lines]
            if len(parts)<2 or not all(parts) or len({p[2].strip() for p in parts})!=1:
                return m[0]
            counts[1] += 1
            return m[1]+'<br>'.join([p[1].rstrip() for p in parts]+[parts[0][2].strip()])+m[3]
        return re.sub(r'(<figcaption\b[^>]*>)(.*?)(</figcaption>)', caption, original, flags=re.S)
    html = re.sub(r'<figure\b[^>]*>.*?</figure>', figure, html, flags=re.S)
    return html, counts

if __name__ == '__main__':
    totals = [0, 0, 0]
    for folder in ['wechat', 'wechat-new']:
        for path in sorted((ROOT/'run50'/folder).glob('*.html')):
            original = path.read_text(encoding='utf-8')
            updated, counts = normalize(original)
            if updated != original:
                path.write_text(updated, encoding='utf-8')
                totals = [totals[0]+1, totals[1]+counts[0], totals[2]+counts[1]]
                print(path.relative_to(ROOT), counts)
    print('Changed pages, logos, photo groups:', totals)
