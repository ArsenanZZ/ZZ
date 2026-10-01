# Run50 transparent opening animation

Original robot: `assets/bio/favicon.png`. Five-second loop, 720 × 480, 20 fps, transparent outer canvas. The HTML contains the HyperFrames timeline; `DESIGN.md` records the supplied reference and palette.

Check with `pnpm dlx hyperframes check tools/run50-intro` from the repository root. The single-scene nested-container warning is intentional; runtime, motion and layout checks must pass.

Serve the repository locally, then run `node tools/render_run50_intro.cjs <frames-directory> <composition-URL>`. The default URL is `http://127.0.0.1:8765/tools/run50-intro/index.html`. Playwright must be available in the Node package search path.

Encode with FFmpeg using a transparent palette:

```
ffmpeg -y -framerate 20 -i <frames-directory>/frame-%03d.png -filter_complex "[0:v]split[a][b];[a]palettegen=reserve_transparent=1:stats_mode=full[p];[b][p]paletteuse=dither=none:alpha_threshold=128" -loop 0 assets/run50-robot-intro.gif
```

The article selects the still PNG when reduced motion is requested. Do not matte the GIF against white or black. Verify both themes before replacing the asset.

The running update articulates a vector tracing of the original robot. Leg pivot-drift warnings are intentional: legs rotate around the hip, not their bounding-box center. The original bitmap is retained as the design reference.
