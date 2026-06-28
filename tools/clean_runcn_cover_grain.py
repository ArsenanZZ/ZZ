from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"

RUNCN_COVER_STEMS = [
    "steel-tank-story",
    "three-city-pilgrimage",
    "xiamen-marathon",
    "wuhan-wuxi-marathon-notes",
    "wuhan-marathon-2018",
    "xian-city-wall-marathon",
    "lanzhou-marathon",
    "guiyang-marathon-climb",
    "haikou-marathon",
    "wuhan-han-marathon",
    "dalian-trail",
    "wuhan-graduation",
    "harbin-marathon",
    "west-lake-half-marathon",
    "shanghai-vertical-marathon",
    "ningbo-dongqian-lake-marathon",
    "xiangyang",
    "guilin",
    "hk",
]

RUNCN_COVERS = [
    *(f"cover-medal-{stem}.jpg" for stem in RUNCN_COVER_STEMS),
    "cover-medal-fb-steel-tank-story.jpg",
    "cover-medal-fb-three-city-pilgrimage.jpg",
    "cover-medal-fb-xiamen-marathon.jpg",
    "cover-medal-fb-wuhan-wuxi-marathon-notes.jpg",
    "cover-medal-fb-wuhan-marathon-2018.jpg",
    "cover-medal-fb-xian-city-wall-marathon.jpg",
    "cover-medal-fb-lanzhou-marathon.jpg",
    "cover-medal-fb-guiyang-marathon-climb.jpg",
    "cover-medal-fb-haikou-marathon.jpg",
    "cover-medal-fb-wuhan-han-marathon.jpg",
    "cover-medal-fb-dalian-trail.jpg",
    "cover-medal-fb-wuhan-graduation.jpg",
    "cover-medal-fb-harbin-marathon.jpg",
    "cover-medal-fb-west-lake-half-marathon.jpg",
    "cover-medal-fb-shanghai-vertical-marathon.jpg",
    "cover-medal-fb-ningbo-dongqian-lake-marathon.jpg",
    "cover-medal-fb-xiangyang.jpg",
    "cover-medal-fb-guilin.jpg",
    "cover-medal-fb-hk.jpg",
]


def clean_cover(image: Image.Image) -> Image.Image:
    image = image.convert("RGB")
    median3 = image.filter(ImageFilter.MedianFilter(3))
    cleaned = image.copy()
    src = image.load()
    med = median3.load()
    dst = cleaned.load()
    width, height = image.size

    for y in range(height):
        for x in range(width):
            r, g, b = src[x, y]
            mr, mg, mb = med[x, y]
            lum = 0.2126 * r + 0.7152 * g + 0.0722 * b
            median_lum = 0.2126 * mr + 0.7152 * mg + 0.0722 * mb
            saturation = max(r, g, b) - min(r, g, b)
            if lum > 95 and lum - median_lum > 10 and saturation < 150:
                amount = min(0.90, 0.55 + (lum - median_lum) / 80)
                dst[x, y] = (
                    int(r * (1 - amount) + mr * amount),
                    int(g * (1 - amount) + mg * amount),
                    int(b * (1 - amount) + mb * amount),
                )

    edges = (
        cleaned.convert("L")
        .filter(ImageFilter.FIND_EDGES)
        .filter(ImageFilter.GaussianBlur(1.0))
    )
    edge_mask = edges.point(lambda p: max(0, min(255, int((p - 10) * 5.0))))
    flat_clean = Image.blend(
        cleaned.filter(ImageFilter.MedianFilter(5)),
        cleaned.filter(ImageFilter.GaussianBlur(1.15)),
        0.55,
    )
    result = Image.composite(cleaned, flat_clean, edge_mask)
    result = ImageEnhance.Color(result).enhance(1.08)
    result = ImageEnhance.Contrast(result).enhance(1.10)
    return result.filter(ImageFilter.UnsharpMask(radius=1.25, percent=130, threshold=6))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--family",
        choices=("base", "fb", "all"),
        default="all",
        help="Which RunCN cover family to clean.",
    )
    args = parser.parse_args()

    if args.family == "base":
        filenames = [f"cover-medal-{stem}.jpg" for stem in RUNCN_COVER_STEMS]
    elif args.family == "fb":
        filenames = [f"cover-medal-fb-{stem}.jpg" for stem in RUNCN_COVER_STEMS]
    else:
        filenames = RUNCN_COVERS

    for filename in filenames:
        path = ASSETS / filename
        with Image.open(path) as image:
            cleaned = clean_cover(image)
        cleaned.save(path, quality=95, subsampling=1, optimize=True)
        print(f"cleaned {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
