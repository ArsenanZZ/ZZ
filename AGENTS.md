# Marathon article visual rules

User-confirmed article requirements, 2026-10-25:
- Every Run50 article needs a conversational introduction to its state: geography, distinctive local character, and how these relate to this trip. Place it early and interleave relevant existing photos; verify factual additions with primary sources.
- Avoid generic lyrical summaries such as “装进这一个周末”, “把一天串起来”, or “留下来的东西是真的多”. Prefer concrete events, the author's recorded observations and jokes, and plain chapter titles.

User-confirmed preferences, 2026-10-10. Apply when creating or changing RunCN / Run50 marathon story visuals. Do not silently restyle existing unrelated articles.

- **Homepage cover and in-article poster are two separate assets. Never reuse one file for both roles.**
- Homepage/index cover: rounded rectangular, layered plaque/license-plate rim. Chuxiong approved example: `assets/runcn-chuxiong-poster-framed-v3-20261010.jpg`.
- Article image immediately below the map: flat paper/screenprint poster, plain thin rectangular print border, no thick rounded metallic plaque rim. The user explicitly rejected stepped/notched outer corners: use ordinary 90-degree joins, no corner ornaments or detached corner squares.
- Preserve the same subject, local symbols, text and palette between cover and poster; change the framing/treatment rather than redesigning the scene.
- References: Liupanshui, Nebraska and New England article posters; user's `Z:/ZhennanZ Folder/ZZ-Z-others/2026-Website/RunCN-Homepage-16x9-Previews-20260716` folder for cover family and restrained border ideas.
- Do not default every province title to white or every year panel to yellow. Coordinate distinct title, year-panel, city-panel and series-panel colors while keeping strong contrast.
- Keep cover and poster paths explicitly separate in builders (`COVER_SRC`, `POSTER_SRC`); index and Open Graph use cover, map-adjacent figure uses poster. Verify these references before publishing.
- Opening photo GIFs: actual square crops, no gray padding, preserve faces, gestures and complete medals. Add/remove only requested frames; keep body photographs unless user requests body removal.

User-confirmed refinements, 2026-10-11:

- RunCN covers use the approximately **16:10** plaque proportions of the Liupanshui benchmark, with a large upper-left province title and a tall three-panel year/city/RUNCN rail. Do not default to 16:9 or shrink these letters.
- Article China maps use the current `build_lhasa_map.cjs` family: province names in KaiTi, a heavier Song-style dispatch title/current province, labels placed inside the actual province shapes, and external leaders for dense coastal municipalities. Use subdued completed-region colors and a stronger current-region color.
- Align both the outer image edges and visible artwork edges of map/poster pairs. Any map inset must have a paper-colored backing within the full-width image box; verify white and black themes and preserve that treatment in the WeChat copy exporter.
- Add image-specific photo captions and photography credits. Author photographs use `Arsenan`; event photographer images use `官方摄影` unless the source identifies a specific author. Never invent a photographer name. Preserve the user's actual spoken opinions and jokes when preparing articles from Vlogs.

User-confirmed RunCN map and WeChat requirements, 2026-10-22:

- All RunCN article maps use the Liupanshui paper-map standard. Generate them with `tools/build_runcn_article_maps.cjs` and `tools/data/runcn-map-timeline.json`; preserve the shared geography, KaiTi labels, subdued historical colors, current province emphasis, city star and local landmark leader.
- Color only provinces actually visited by that article's last numbered station. Never inherit today's homepage completion map. Combined articles use their final station as the historical cutoff; later provinces and city dots remain absent.
- Map and poster boxes use identical width and no asymmetric padding, including the WeChat copy export.
- Updated user preference, 2026-10-22: WeChat copying must preserve fetched image bytes without additional resizing or JPEG compression, including all photos and animated GIFs. Show actual clipboard size. Allow original-quality copy; if it reaches 10 MB, advise using the existing chapter-copy selector. Image quality takes priority over the earlier automatic 9 MB compression target.
- Copied chapter numbers must be native text with theme-appropriate ink and no background, never full-width number PNGs: WeChat can show those images as white bars in dark mode. Keep the website's outlined numbers unchanged. This applies to every numbered chapter, not only 01 and 02.
