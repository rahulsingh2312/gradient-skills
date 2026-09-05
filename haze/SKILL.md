---
name: haze
description: Generate soft pastel "mesh" gradient backgrounds and editorial hero sections in the "editorial fintech launch page" style — blurred colour blobs (mint, lavender, pink fading into cream and gold), a white light-leak, a faint dot grid, optional film grain, and big serif display type with an italic second line. Use this whenever someone asks for a gradient background, a mesh/aurora/blurred/pastel/dreamy/holographic gradient, a "soft" or "glowy" hero, a landing page hero, an OG image, an X/Twitter or social card, a wallpaper, or says they want something that looks like Linear, Vercel, Arc, or Raycast launch pages. Also use it when they only want the CSS for such a background, or a quick PNG. Outputs HTML, CSS, SVG, or PNG.
---

# Haze — pastel mesh gradients that look like light on paper

The look this skill produces: a near-white sheet of paper with big, very soft pools of colour bleeding in
from the edges — cool ones (mint, sky, lavender, pink) on one side, warm ones (cream, gold, peach) on the
other — a bright white "light-leak" between them, a barely-there dot grid, and calm editorial type.
Think Linear's launch art, or a Dribbble "aurora" shot, minus the neon.

Everything is in `scripts/haze.py` (stdlib Python, no packages). Read this file, then run the script.
Only open the references when you need them:

- `references/recipe.md` — the CSS anatomy explained, for hand-writing it into React/Tailwind/Svelte/plain CSS
  without the script. Read when the user wants it *inside their own codebase* rather than a file.
- `references/palettes.md` — every built-in palette with swatches and when to use each, plus how to derive
  a palette from a brand colour.

## Quick start

```bash
S=<path-to-this-skill>/scripts/haze.py

# 1. A finished hero as a standalone HTML page (Google Fonts, responsive)
python3 $S --responsive --wordmark "Acme." --eyebrow "Beta" \
  --headline "Ship the" --italic "boring parts." \
  --sub "Infra that stays out of your way." --badge "Live" --cta "Get started" --out hero.html

# 2. Just the background CSS to paste into an existing site
python3 $S --blank --palette dusk --format css > haze.css

# 3. A PNG for X / OG / a wallpaper (needs Node + Playwright, see "Rendering PNGs")
python3 $S --palette sorbet --seed 4 --size 1200x630 --headline "Launch" --italic "day." --out og.png

# 4. Full control (two panels side by side, footer, black top bar): write a spec JSON
python3 $S --spec spec.json --size 2000x1300 --out site.png
```

`--format` is inferred from the `--out` extension: `.html`, `.png`, `.svg`, or `--format css` to stdout.

## The knobs that matter

| Flag | What it does | Good values |
|---|---|---|
| `--palette` | colour family | `dawn` (reference), `sorbet`, `glacier`, `dusk`, `meadow`, `ember`, `ink` (dark) |
| `--layout` | where the blobs sit | `split` (cool left / warm right, white seam), `corners`, `wash`, `halo` |
| `--seed` | jitters blob positions | try 1–20; pick the one you like, then keep it fixed |
| `--intensity` | colour strength | `0.6` whisper, `1.0` reference, `1.3` punchy |
| `--colors` | your own 8 hex colours (4 cool, 4 warm) | see palettes.md for how to pick them |
| `--grain 0.06` | film grain overlay | 0.04–0.1; off by default |
| `--no-grid` / `--grid-size` | the dot grid | 22px default; 28–32px on very large canvases |
| `--fonts` | `google` (html default), `local` (png default, vendored), `embed` (self-contained), `system` | |
| `--responsive` | HTML fills the viewport instead of fixed `--size` | use for real pages |
| `--scale 2` | PNG device pixel ratio | 2 for retina, 1 for quick previews |

Sizes worth remembering: X/Twitter card `1600x900`, OG image `1200x630`, Instagram `1080x1080`,
desktop wallpaper `2560x1440`, full-bleed landing page `2000x1300`.

## Spec file (for multi-panel layouts)

```json
{
  "wordmark": "Lumen.",
  "palette": "dawn", "layout": "split", "seed": 3, "topbar": true, "grain": 0,
  "footer": "Made with care. No cookies.",
  "panels": [
    {"eyebrow": "Studio", "headline": "Design the", "italic": "quiet part.",
     "sub": "Interfaces that get out of the way.", "badge": "Live", "cta": "Enter", "href": "/studio"},
    {"eyebrow": "Labs", "headline": "Same idea,", "italic": "gold leaf.",
     "sub": "Experiments, shipped weekly.", "badge": "Beta", "cta": "Enter"}
  ]
}
```

Every key is optional. One panel = a centred hero; two or three = columns (they stack on mobile).
CLI flags override the spec, so `--seed 9` on top of a spec is a cheap way to explore variants.

## Rendering PNGs

PNG export runs `scripts/render.mjs` (Playwright + Chromium). It looks for `playwright` locally, then in
the global npm root; if it can't find it, it falls back to a `chromium` binary on PATH, and if that is
missing too it leaves the `.html` beside the output and tells you. One-time setup on a fresh machine:

```bash
npm i -g playwright && npx playwright install chromium
```

PNG renders use the vendored fonts in `assets/fonts/` (Instrument Serif, Inter, JetBrains Mono — all
OFL) so they are identical offline and in CI. HTML output links Google Fonts by default; pass
`--fonts embed` when the HTML must be one self-contained file (email, a CMS field, an offline demo).

## Working with the user

1. Ask nothing you can infer. A bare "make me one of those soft gradient heroes" means: `dawn` palette, `split` layout,
   grid on, no grain. A brand colour in the request means derive a palette (palettes.md → "From a brand
   colour"). Dark UI means `ink`.
2. Render, then *look* at the result (open the PNG, or screenshot the HTML) before handing it over. Check:
   the white seam still exists, text sits on the calmest part of the canvas, no blob has a visible hard edge,
   the type is not fighting the colour. If it's off, change seed or intensity first — palette last.
3. Offer two or three seeds side by side when the user is choosing; people pick faster from options
   than from adjectives.
4. Ship what fits their stack: `.html` for a page, `--format css` for an existing codebase (and point them
   at `references/recipe.md` for Tailwind/React), `.png` for social, `.svg` when they need a vector or have
   no browser available.

## Why the look works (so you can bend it without breaking it)

- **Low saturation, high lightness.** Every blob is ≥ 82% lightness. The contrast comes from the hue
  *temperature* split (cool vs warm), not from any single loud colour. Push saturation and it turns into a
  2012 "web 2.0" gradient instantly.
- **Blobs are huge and soft.** Each radial ellipse spans 40–60% of the canvas and fades to transparent by
  ~68% of its radius. Small blobs read as spots; sharp stops read as circles. Both kill the "light" illusion.
- **The white light-leak is the hero.** It is the brightest thing on the canvas and it sits where the text
  goes. Type over a wash of colour looks like a poster; type over the light-leak looks like print.
- **The grid is texture, not decoration.** ~9% opacity, ~22px pitch, fading out toward the edges. If you can
  count the dots from across the room it's too strong.
- **Type is quiet.** One display serif with a true italic for the second line, tracking slightly negative,
  line-height under 1. Eyebrow and badges in a small tracked-out mono (uppercase, `letter-spacing: .3em+`).
  Ink is near-black (`#121212`), never pure black — pure black on pastel looks harsh.
- **Nothing has a border except the pill badge.** Cards, boxes, and drop shadows fight the softness.

## Common asks

- "Make it more dreamy / softer" → `--intensity 0.7`, maybe `--grain 0.05`.
- "More colour / punchier" → `--intensity 1.25`, or `--layout corners`.
- "Match our brand (#5B4BFF)" → palettes.md → "From a brand colour"; pass `--colors`.
- "Dark version" → `--palette ink` (dot grid flips to white automatically).
- "Animate it" → recipe.md has a 20-line keyframe drift that moves the blobs slowly; keep it under
  60 s per cycle and respect `prefers-reduced-motion`.
- "Put it behind my existing page" → recipe.md, the `.haze` class is designed to wrap any content.
