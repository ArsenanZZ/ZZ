# Run50 Story Workflow Reference

## Repository Map

- Default repo: `C:\Users\ZZ\Documents\Github\ZZ`
- Public site: `https://arsenanzz.github.io/ZZ/`
- Chinese stories: `run50/stories/chinese/`
- English stories: `run50/stories/english/`
- Facebook stories: `run50/facebook/`
- Shared assets: `assets/`
- Story builders and cover tools: `tools/`
- Supabase SQL: `supabase/run50-comments.sql`

## Source Import

For a new RunCN export, expect one of these forms:

- `RunCN ... .html` plus a sibling `RunCN ... _files/` directory.
- `RunCN ... .html` plus a zipped `_files.zip`.

Use a structured HTML parser when practical. Extract only meaningful story content: headings, paragraphs, figures, captions, and race metadata. Remove platform-specific wrappers, duplicated intro cards, empty blocks, reactions, share prompts, and unrelated script/style debris.

Convert images to `.webp` if needed and store them once under:

`run50/stories/chinese/RunCN-{City}-Marathon-clean_files/`

Name images sequentially:

`img-001.webp`, `img-002.webp`, ...

Use image markup like:

```html
<figure>
  <img src="RunCN-City-Marathon-clean_files/img-001.webp" alt="City Marathon photo 1" loading="lazy" decoding="async">
  <figcaption>Caption @Credit</figcaption>
</figure>
```

For English and Facebook pages, reference the Chinese image folder instead of duplicating images:

```html
<img src="../chinese/RunCN-City-Marathon-clean_files/img-001.webp" alt="City Marathon photo 1" loading="lazy" decoding="async">
```

For Facebook pages under `run50/facebook/`, use the correct relative depth:

```html
<img src="../stories/chinese/RunCN-City-Marathon-clean_files/img-001.webp" alt="City Marathon photo 1" loading="lazy" decoding="async">
```

## Three Page Outputs

### Chinese Original

Target:

`run50/stories/chinese/{slug}.html`

Requirements:

- Clean Chinese title, metadata, date, location, race name, and navigation.
- Preserve the original story voice.
- Start from the real foreword/content if the source has a messy exported cover or reaction section.
- Include Open Graph tags pointing to `assets/og-run50-{slug}-icons.png`.
- Include engagement section with `data-locale="zh-CN"` and `data-page-key="run50-{slug}-zh"`.

### English Story

Target:

`run50/stories/english/{slug}.html`

Requirements:

- Translate idiomatically and conversationally.
- Keep travel detours, family moments, jokes, and race details.
- Avoid literal Chinglish and avoid sounding like a summary.
- Preserve all meaningful photos and captions.
- Include engagement section with `data-locale="en"` and `data-page-key="run50-{slug}-en"`.

### Facebook Edition

Target:

`run50/facebook/{slug}.html`

Requirements:

- Use an editorial/news-like layout inspired by CNN World: strong masthead, red/black accents, article rail, brief box, large readable story column.
- Do not include public copy that reveals the editing process, such as "Facebook edition", "same full text", or "re-ordered for a stronger share opening".
- Use the marathon hook early, but add a short context paragraph first: date, race, city, and why this story matters.
- Move race-day report before slower backstory when useful for sharing.
- Add transitions when moving to wedding, Wuhan/travel, packet pickup, old city, family, or postscript sections.
- Keep the full English text and all photos unless the user asks for a shorter share version.
- Include engagement section with `data-locale="en"` and `data-page-key="run50-{slug}-facebook-en"`.

## Visual Channel Themes

Apply the same visual language across story indexes and cards so readers can recognize each channel quickly.

### RunCN Area

Use for China race stories such as Xiangyang, Guilin, and Hong Kong.

- Series label: `RunCN #N`
- Card class: `run-cn`
- Cover badge city color: red `#cc0000`
- Background family: warm peach/ivory
- Cover title: top-left city name only, no subtitle
- Cover badge: fixed top-right benchmark box and fixed text positions

```css
.story-card.run-cn {
  background: #faf2ee;
  border-color: #ebdcd6;
}
.story-card.run-cn:hover {
  border-color: #dfbeaf;
}
```

### Run50 Area

Use for U.S. state marathon stories.

- Series label: `Run50 #N`
- Card class: `run-50`
- Cover badge city color: blue `#0b67c2`
- Background family: cool glacier blue
- Cover title: top-left city/state/race name only, no subtitle
- Cover badge: same fixed benchmark geometry as RunCN; shrink long second-line text to fit

```css
.story-card.run-50 {
  background: #edf3f7;
  border-color: #d0dfe8;
}
.story-card.run-50:hover {
  border-color: #acc4d3;
}
```

### RunWorld Area

Use for international stories outside the U.S. and China, such as Pisa and Mexico.

- Series label: `RunWorld #N`
- Card class: `run-world`
- Cover badge city color: green `#2f855a`
- Background family: soft sage
- Cover title: top-left city/country race name only, no subtitle
- Cover badge: same fixed benchmark geometry as RunCN; icon art stays below the title/badge zone

```css
.story-card.run-world {
  background: #f1f6f2;
  border-color: #d0dfd4;
}
.story-card.run-world:hover {
  border-color: #abc4b1;
}
```

Cards should keep a subtle lift interaction:

```css
.story-card {
  transition: transform .18s ease, box-shadow .18s ease, border-color .18s ease;
}
.story-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 24px 54px rgba(15, 23, 42, .12);
}
```

## Engagement Block

Pages should load:

```html
<link rel="stylesheet" href="../../../assets/zz-engagement.css?v=YYYYMMDD">
```

Use the correct relative path for the page depth.

Near the bottom of each page:

```html
<section class="zz-engagement" data-zz-engagement data-locale="en" data-page-key="run50-city-marathon-en">
  <div class="zz-engagement-shell">
    <div>
      <p class="zz-engagement-kicker">Comments / Views</p>
      <h2>Say something after the run</h2>
      <p class="zz-engagement-note">No account is needed to submit a comment. New comments appear right away.</p>
      <div class="zz-engagement-stats">
        <span class="zz-engagement-stat" id="busuanzi_container_page_pv">
          <span>Views</span>
          <strong id="busuanzi_value_page_pv" data-zz-view-count>--</strong>
        </span>
      </div>
    </div>
    <div class="zz-engagement-card">
      <div id="supabase-comments-city-en" data-zz-supabase-comments></div>
      <p class="zz-engagement-status" data-zz-engagement-status>Loading comments...</p>
    </div>
  </div>
</section>
<script src="../../../assets/zz-engagement-config.js?v=YYYYMMDD"></script>
<script src="../../../assets/zz-engagement.js?v=YYYYMMDD"></script>
```

For Chinese pages, use Chinese labels and `data-locale="zh-CN"`.

When adding a new story, update `supabase/run50-comments.sql` with the three new page keys in both the whitelist constraint and insert policy. The current model is public anonymous `select` and `insert`, no approval workflow; `is_hidden` is only for hiding abusive comments later.

## Cover Assets

Generate both:

- `assets/og-run50-{slug}-icons.png`: `1200x630`, RGB PNG, for Open Graph/Facebook previews.
- `assets/thumb-run50-{slug}-icons.svg`: `viewBox="0 0 1200 750"`, for list cards.

Design rules:

- City icon style, not a photo.
- Xiangyang, Guilin, and Hong Kong are the baseline cover family: top-left city/race name, top-right series badge, city icons below the text zone.
- The top-left has only the city or race name. Do not add a subtitle under it.
- RunCN/Run50/RunWorld badge stays in the fixed top-right zone.
- Main city icons stay in the lower half, normally starting below `y=245` on `1200x630` PNGs and below `y=280` on `1200x750` SVG thumbnails.
- Keep enough clear space between title, badge, skyline/mountains/bridges/medals.
- Use a real visual check with `view_image` for PNGs. For SVGs, open a local preview page or inspect in browser if needed.
- If text may be long, fit the city name into the badge instead of letting it collide with the border. Do not let the badge box press against, cover, or visually trap the text.

Fixed Open Graph PNG benchmark for `1200x630`:

- Canvas: `1200x630`, RGB.
- Top-left title text top-left: `x=64`, `y=64`, font `66px`, bold, fill `#20242b`.
- Badge box: `x=760`, `y=64`, `width=362`, `height=164`, radius `22`, fill `#ffffff`, stroke `#20242b`, stroke width `7`.
- Badge first line: `x=790`, `y=112`, font `40px`, bold, fill `#20242b`, text `RunCN #N`, `Run50 #N`, or `RunWorld #N`.
- Badge second line: `x=790`, `y=166`, font up to `50px`, bold, fit to max width `302px`.
- Badge city color: RunCN red `#cc0000`, Run50 blue `#0b67c2`, RunWorld green `#2f855a`.

Fixed thumbnail SVG benchmark for `1200x750`:

```xml
<text x="70" y="104" font-family="Arial, Helvetica, sans-serif" font-size="66" font-weight="900" fill="#20242b">CITY NAME</text>
<rect x="758" y="62" width="364" height="166" rx="22" fill="#ffffff" stroke="#20242b" stroke-width="8"/>
<text x="790" y="122" font-family="Arial, Helvetica, sans-serif" font-size="41" font-weight="900" fill="#20242b">RunCN #N</text>
<text x="790" y="182" font-family="Arial, Helvetica, sans-serif" font-size="52" font-weight="900" fill="#cc0000">CITY NAME</text>
```

Use the same SVG badge geometry for every channel. Change only the series label and second-line city color:

- RunCN city text: `#cc0000`.
- Run50 city text: `#0b67c2`.
- RunWorld city text: `#2f855a`.

For longer city names, keep `x`, `y`, box size, and safe zone fixed, then reduce the second-line font size until the text fits inside the badge. Keep the badge in the top-right visual zone and city icons in the lower half.

For larger `1600x1000` icon art, scale this system proportionally, roughly `1.33x`, while preserving safe margins:

```xml
<text x="93" y="138" font-family="Arial, Helvetica, sans-serif" font-size="88" font-weight="900" fill="#20242b">CITY NAME</text>
<rect x="1008" y="83" width="484" height="221" rx="29" fill="#ffffff" stroke="#20242b" stroke-width="11"/>
<text x="1051" y="162" font-family="Arial, Helvetica, sans-serif" font-size="55" font-weight="900" fill="#20242b">RunCN #N</text>
<text x="1051" y="242" font-family="Arial, Helvetica, sans-serif" font-size="69" font-weight="900" fill="#cc0000">CITY NAME</text>
```

## Index Updates

Update the relevant index pages:

- root `index.html` or root Run50 card entry when the public homepage should surface the channel/story.
- `run50/stories/chinese/index.html`
- `run50/stories/english/index.html`
- `run50/facebook/index.html`
- `run50/index.html` if the top-level Run50 navigation/card set should expose the new story or channel.

Use class themes consistently:

- `run-cn` for China RunCN stories.
- `run-50` for U.S. Run50 stories.
- `run-world` for international RunWorld stories.

Add cache-busting to thumbnail URLs:

```html
<img src="../../../assets/thumb-run50-city-icons.svg?v=YYYYMMDD-X" alt="City Marathon icon cover">
```

Use a fresh suffix whenever covers or thumbnails change. If only copy changes, cache-bust affected HTML-linked assets when previews or cards may otherwise stay stale.

## Local Verification

Recommended checks:

```powershell
$env:Path="C:\Program Files\Git\cmd;C:\Program Files\Git\bin;$env:Path"
git status --short
```

Run the relevant builder:

```powershell
& 'C:\Users\ZZ\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' tools/build_city_story.py
```

Check generated images:

```powershell
@'
from PIL import Image
from pathlib import Path
for path in Path("assets").glob("og-run50-*-icons.png"):
    im = Image.open(path)
    print(path, im.size, im.mode)
'@ | python -
```

Serve locally if needed:

```powershell
python -m http.server 43210 --bind 127.0.0.1
```

Open local URLs in the in-app browser:

- `http://127.0.0.1:43210/run50/stories/chinese/{slug}.html`
- `http://127.0.0.1:43210/run50/stories/english/{slug}.html`
- `http://127.0.0.1:43210/run50/facebook/{slug}.html`

Verify:

- no text overlap
- images load
- comments UI appears
- view placeholder appears
- mobile width does not break
- OG tags point to absolute live URLs where appropriate

## Deploy Verification

Commit only relevant files. Do not include temporary server pid files, local preview files, or Python `__pycache__`.

Push to `main`, then check Pages:

```powershell
$headers = @{ 'User-Agent' = 'Codex' }
Invoke-RestMethod -Uri 'https://api.github.io/repos/ArsenanZZ/ZZ/actions/runs?per_page=5' -Headers $headers
```

After the matching `head_sha` completes with `success`, verify live URLs with cache busting:

- `https://arsenanzz.github.io/ZZ/run50/stories/chinese/{slug}.html?v=TIMESTAMP`
- `https://arsenanzz.github.io/ZZ/run50/stories/english/{slug}.html?v=TIMESTAMP`
- `https://arsenanzz.github.io/ZZ/facebook/{slug}.html?v=TIMESTAMP`
- `https://arsenanzz.github.io/ZZ/assets/og-run50-{slug}-icons.png?v=TIMESTAMP`
- `https://arsenanzz.github.io/ZZ/assets/thumb-run50-{slug}-icons.svg?v=TIMESTAMP`

Final response should be concise and include published URLs, verification status, and commit hash.
