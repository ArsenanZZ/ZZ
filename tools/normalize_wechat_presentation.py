"""Keep WeChat reader-safe logos and one shared credit per connected photo group.

Run after article builders, and before publishing. Uses only the standard library.
"""
from pathlib import Path
import re,json

ROOT = Path(__file__).resolve().parents[1]

def normalize(html, page_name=''):
    counts = [0, 0]
    palette_file=ROOT/'tools/data/run50-shirt-palettes.json'
    palettes=json.loads(palette_file.read_text(encoding='utf-8')) if palette_file.exists() else {}
    slug_match=re.search(r'data-edition="([^"]+)"',html)
    shirt_slug=None
    if page_name:
        shirt_slug=next((s for s in sorted(palettes,key=len,reverse=True) if page_name.startswith(s+'-')),None)
    if slug_match and not shirt_slug:
        shirt_slug=next((s for s in sorted(palettes,key=len,reverse=True) if slug_match[1].startswith(s)),None)
    # Some older builders use short edition IDs; match their canonical metadata.
    if not shirt_slug:
        shirt_slug=next((s for s in sorted(palettes,key=len,reverse=True) if re.search(re.escape(s)+r'-(?:editorial|modern-rail|d-rail)\.html',html)),None)
    def brand(match):
        original = match[0]
        if 'RunCN' in original or 'RunWorld' in original:
            return original
        if shirt_slug:
            base='/assets/run50-shirt-intros/'+shirt_slug+'/'
            return '<picture class="brand-intro" data-logo-theme="shirt"><source media="(prefers-reduced-motion: reduce)" srcset="'+base+'light-still.png" data-light-src="'+base+'light-still.png" data-dark-src="'+base+'dark-still.png"><img src="'+base+'light.gif" data-light-src="'+base+'light.gif" data-dark-src="'+base+'dark.gif" alt="Run50 机器人片头" width="280" height="350"></picture>'
        # RunCN uses a separate mountain wordmark with opaque themed backgrounds.
        # Keep its theme pair; this fix is for the transparent Run50 robot.
        if 'RunCN' in original or 'data-logo-theme="paired"' in original:
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
        def official(m):
            caption=re.sub(r'(?:@|\bby\s+)Photographer(?:\s*·\s*\d+)?', ' · 摄影 / 官方摄影',m[2],flags=re.I)
            caption=re.sub(r'^\s*·\s*','',caption)
            return m[1]+caption+m[3]
        original=re.sub(r'(<figcaption\b[^>]*>)(.*?)(</figcaption>)',official,original,flags=re.S)
        if len(re.findall(r'<img\b', original)) < 2:
            return original
        def caption(m):
            lines = re.split(r'<br\s*/?>', m[2])
            parts = [re.fullmatch(r'(.*?)\s*[·|]\s*(摄影\s*[/|]\s*[^<>]+?)\s*', line, re.S) for line in lines]
            credited = [p for p in parts if p]
            if len(credited)<2 or len({p[2].strip() for p in credited})!=1:
                return m[0]
            # An uncredited photo must not inherit its neighbours' attribution.
            if not all(parts):
                labels = ['上', '下'] if len(parts)==2 else ['上', '中', '下'] if len(parts)==3 else [str(i+1) for i in range(len(parts))]
                credit = '、'.join(labels[i] for i,p in enumerate(parts) if p)+'图：'+credited[0][2].strip()
            else:
                credit = credited[0][2].strip()
            counts[1] += 1
            return m[1]+'<br>'.join([v for p,line in zip(parts,lines) if (v := (p[1].rstrip() if p else line)) not in ['', '上：', '中：', '下：']]+[credit])+m[3]
        return re.sub(r'(<figcaption\b[^>]*>)(.*?)(</figcaption>)', caption, original, flags=re.S)
    html = re.sub(r'<figure\b[^>]*>.*?</figure>', figure, html, flags=re.S)
    return html, counts

if __name__ == '__main__':
    totals = [0, 0, 0]
    for folder in ['wechat', 'wechat-new']:
        for path in sorted((ROOT/'run50'/folder).glob('*.html')):
            original = path.read_text(encoding='utf-8')
            updated, counts = normalize(original,path.name)
            if updated != original:
                path.write_text(updated, encoding='utf-8')
                totals = [totals[0]+1, totals[1]+counts[0], totals[2]+counts[1]]
                print(path.relative_to(ROOT), counts)
    print('Changed pages, logos, photo groups:', totals)
