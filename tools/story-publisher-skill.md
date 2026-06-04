# Story Publishing Skill & Workflow Guide

This skill guide documents the complete step-by-step workflow for importing, styling, translating, and deploying new running story articles (RunCN / Run50) on the ZZ portal.

---

## 1. Content Extraction & HTML Sanitation

When importing a new story (e.g., from WeChat, Word, or Markdown):
1. **Clean Markup**: Remove proprietary CSS styles and empty blocks. Standardize on clean HTML5 semantic tags (`<article>`, `<section>`, `<figure>`, `<figcaption>`, `<p>`, `<h2>`).
2. **Media Optimization**:
   - Save image assets inside a dedicated directory: `RunCN-[City]-Marathon-clean_files/`.
   - Use clean, sequential filenames (`img-001.webp`, `img-002.webp`, etc.).
   - All `<img>` tags must include:
     ```html
     <img src="RunCN-City-Marathon-clean_files/img-001.webp" alt="Description" loading="lazy" decoding="async">
     ```
3. **Typography**: Ensure proper chapter breaks using `<h2>` headers paired with a styling separator (`<hr>`).

---

## 2. Generating the 3 Page Portals

Every race story requires three separate HTML page integrations:

### A. Chinese Original (`run50/stories/chinese/[slug].html`)
- **Metadata**: Set appropriate `<title>`, `<meta name="description">`, and Open Graph tags (pointing to the respective `og-run50-*.png` cover in assets).
- **Core Elements**: Set navigation bar (`← 中文故事`, `English`, `Run50`), title section, byline meta block, and full Chinese text.

### B. English Translation (`run50/stories/english/[slug].html`)
- **Tone**: Keep a conversational voice, maintaining travel detours and finish-line notes.
- **Paths**: Keep paths consistent. Images should reference `../chinese/RunCN-[City]-Marathon-clean_files/...` directly to avoid duplicating file storage.

### C. Facebook Edition (`run50/facebook/[slug].html`)
- **Structure**: Uses a special grid layout featuring a `<span class="label">` category, a `<figure class="lead-media">` with the SVG cover, a sidebar `<aside class="rail">` with a "Brief box" key statistics table, and the English text.
- **Engagement**: Ensure the Supabase comments section container `<section data-zz-comments></section>` is correctly configured.

---

## 3. Card Visual Styling & Branding Colors

Maintain editorial, premium desaturated backgrounds and interactive hover styles for story listing cards:

### Warm Theme (Chinese RunCN Stories)
Apply the `.run-cn` class to the `.story-card` element:
```css
.story-card.run-cn {
  background: #faf2ee;      /* Soft warm peach-ivory */
  border: 1px solid #ebdcd6; /* Matching warm border */
}
.story-card.run-cn:hover {
  border-color: #dfbeaf;    /* Darker warm hover border */
}
```

### Cool Theme (US Run50 Stories)
Apply the `.run-50` class to the `.story-card` element:
```css
.story-card.run-50 {
  background: #edf3f7;      /* Soft cool slate-blue */
  border: 1px solid #d0dfe8; /* Matching cool border */
}
.story-card.run-50:hover {
  border-color: #acc4d3;    /* Darker cool hover border */
}
```

### Eucalyptus Theme (World RunWorld Stories)
Apply the `.run-world` class to the `.story-card` element:
```css
.story-card.run-world {
  background: #f1f6f2;      /* Soft sage-white */
  border: 1px solid #d0dfd4; /* Matching cool green-gray border */
}
.story-card.run-world:hover {
  border-color: #abc4b1;    /* Sage-green hover border */
}
```

### Transitions and Interactivity
Ensure all listing indexes have interactive transitions and card lift:
```css
.story-card {
  transition: transform .18s ease, box-shadow .18s ease, border-color .18s ease;
}
.story-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 24px 54px rgba(15, 23, 42, .12);
}
```

---

## 4. SVG Cover Badge Alignment & Dimensions

When generating or updating city icon cover SVGs, the top-right badge box (`RunCN #` or `Run50 #` and city name) must be mathematically sized and shifted to prevent text-border interference.

### A. 1200x750 Canvas (Guilin, Hong Kong, Miami)
```xml
<rect x="750" y="62" width="370" height="146" rx="22" fill="#ffffff" stroke="#20242b" stroke-width="8"/>
<text x="780" y="114" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="900" fill="#20242b">RunCN #[Num]</text>
<text x="780" y="168" font-family="Arial, Helvetica, sans-serif" font-size="44" font-weight="900" fill="#cc0000">[CITY_NAME]</text>
```

### B. 1600x1000 Canvas (Xiangyang)
Scaled up by 1.33x proportionally to match display sizing:
```xml
<rect x="993" y="83" width="500" height="195" rx="29" fill="#ffffff" stroke="#20242b" stroke-width="11"/>
<text x="1033" y="152" font-family="Arial, sans-serif" font-size="45" font-weight="900" fill="#20242b">RunCN #[Num]</text>
<text x="1033" y="224" font-family="Arial, sans-serif" font-size="59" font-weight="900" fill="#cc0000">[CITY_NAME]</text>
```

---

## 5. Supabase Engagement System Configuration

Every individual story page must load page views and comments. Inject the following scripts before `</body>`:

```html
<!-- Engagement Configuration & Library -->
<script src="[relative_path_to_assets]/zz-engagement-config.js" defer></script>
<script src="[relative_path_to_assets]/zz-engagement.js" defer></script>
<link rel="stylesheet" href="[relative_path_to_assets]/zz-engagement.css">

<!-- Container for comments -->
<section data-zz-comments></section>
```

---

## 6. Homepage & Listing Index Updates (Deploying)

To make the new story visible and guarantee the display is updated immediately without browser caching issues:

1. **Root index.html**:
   - Link the channel entries in the `.video-grid` to their listing subfolders.
   - Use distinctive, unique thumbnails representing each channel to ensure visual recognition (e.g. Guilin cover for Chinese stories, Hong Kong for English, Miami for Facebook).
2. **Cache Invalidation (Cache Busting)**:
   - Always append a version parameter query string `?v=YYYYMMDD-X` (where X is a sequence number) to all SVG cover image tags:
     ```html
     <img src="assets/thumb-run50-guilin-icons.svg?v=20260604-9" alt="Guilin cover">
     ```
3. **Commit & Push**:
   - Run `git add .`, commit with description, and push to main. GitHub Pages Actions will build and deploy the changes within 2 minutes.
