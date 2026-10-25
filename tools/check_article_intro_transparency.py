"""Check every referenced magazine brand intro, including all animation frames."""
from pathlib import Path
from urllib.parse import urlsplit
from bs4 import BeautifulSoup
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]

def main():
    assets, pages = set(), 0
    for page in (ROOT / 'run50').rglob('*.html'):
        soup = BeautifulSoup(page.read_text(encoding='utf8'), 'html.parser')
        brands = soup.select('.brand-intro')
        pages += bool(brands)
        for brand in brands:
            for tag in brand.select('img,source'):
                for attr in ('src', 'srcset', 'data-light-src', 'data-dark-src'):
                    path = urlsplit(tag.get(attr, '')).path
                    if path.startswith('/assets/') and path.endswith(('.gif', '.png')):
                        assets.add(path)
    failures, frames = [], 0
    for asset in sorted(assets):
        with Image.open(ROOT / asset.lstrip('/')) as image:
            for index in range(getattr(image, 'n_frames', 1)):
                image.seek(index)
                alpha = image.convert('RGBA').getchannel('A')
                w, h = image.size
                edges = [(0, 0, w, 1), (0, h-1, w, h), (0, 0, 1, h), (w-1, 0, w, h)]
                if any(alpha.crop(box).getextrema()[1] for box in edges):
                    failures.append((asset, index))
                frames += 1
    print(f'{pages} pages; {len(assets)} assets; {frames} frames; {len(failures)} opaque borders')
    for failure in failures:
        print(failure)
    if failures:
        raise SystemExit(1)

if __name__ == '__main__':
    main()
