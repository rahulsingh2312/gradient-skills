# The Haze recipe, by hand

Use this when the gradient has to live inside the user's own codebase (React, Tailwind, Svelte, plain CSS)
rather than as a file the script produced. `python3 scripts/haze.py --blank --format css` prints a
ready-made block; this document explains what's in it so you can adapt it.

## 1. Anatomy

```
┌────────────────────────────────────────────┐
│ base paper colour   (#f6f5f1)              │  ← background-color
│  + 8 radial-gradient blobs, stacked        │  ← background-image, bottom layers
│  + 1 white light-leak ellipse on top       │  ← background-image, first (top) layer
│  ::before  dot grid, masked to fade out    │
│  ::after   optional SVG grain, multiply    │
│  content   position:relative; z-index:1    │
└────────────────────────────────────────────┘
```

Blobs are `radial-gradient(ellipse RX% RY% at X% Y%, colour 0%, colour@55% 32%, transparent 68%)`.
Percent sizes make it responsive — the ellipse scales with the box. Eight blobs and one leak is the
sweet spot; fewer looks flat, more looks muddy.

## 2. Minimal plain-CSS version (the reference look)

```css
.haze {
  position: relative; overflow: hidden; isolation: isolate;
  background-color: #f6f5f1;
  background-image:
    radial-gradient(ellipse 34% 75% at 52% 30%, rgba(255,255,255,.95) 0%, rgba(255,255,255,.55) 38%, rgba(255,255,255,0) 72%),
    radial-gradient(ellipse 42% 55% at  6%  8%, rgba(182,240,220,.95) 0%, rgba(182,240,220,.52) 32%, rgba(182,240,220,0) 68%),
    radial-gradient(ellipse 40% 60% at 28% 42%, rgba(207,225,255,.85) 0%, rgba(207,225,255,.47) 32%, rgba(207,225,255,0) 68%),
    radial-gradient(ellipse 44% 50% at 14% 66%, rgba(215,205,247,.85) 0%, rgba(215,205,247,.47) 32%, rgba(215,205,247,0) 68%),
    radial-gradient(ellipse 46% 40% at 22% 96%, rgba(243,196,230,.90) 0%, rgba(243,196,230,.50) 32%, rgba(243,196,230,0) 68%),
    radial-gradient(ellipse 44% 60% at 94%  6%, rgba(242,219,149,.90) 0%, rgba(242,219,149,.50) 32%, rgba(242,219,149,0) 68%),
    radial-gradient(ellipse 40% 55% at 70% 26%, rgba(249,239,198,.80) 0%, rgba(249,239,198,.44) 32%, rgba(249,239,198,0) 68%),
    radial-gradient(ellipse 40% 60% at 96% 60%, rgba(248,214,192,.85) 0%, rgba(248,214,192,.47) 32%, rgba(248,214,192,0) 68%),
    radial-gradient(ellipse 48% 44% at 78% 100%, rgba(248,226,220,.90) 0%, rgba(248,226,220,.50) 32%, rgba(248,226,220,0) 68%);
  background-repeat: no-repeat; background-size: 100% 100%;
  color: #121212;
}
.haze::before {              /* dot grid */
  content: ""; position: absolute; inset: 0; pointer-events: none;
  background-image: radial-gradient(rgba(15,15,15,.09) .9px, transparent 1.1px);
  background-size: 22px 22px;
  mask-image: radial-gradient(ellipse 90% 90% at 50% 50%, #000 40%, transparent 100%);
}
.haze > * { position: relative; z-index: 1; }
```

## 3. Tailwind

Put the palette in `tailwind.config` as a `backgroundImage` entry, or use arbitrary values inline:

```jsx
<section className="relative isolate overflow-hidden bg-[#f6f5f1] text-[#121212]
  bg-[radial-gradient(ellipse_34%_75%_at_52%_30%,rgba(255,255,255,.95),rgba(255,255,255,0)_72%),radial-gradient(ellipse_42%_55%_at_6%_8%,rgba(182,240,220,.95),rgba(182,240,220,0)_68%),...]">
  <div className="pointer-events-none absolute inset-0
    bg-[radial-gradient(rgba(15,15,15,.09)_.9px,transparent_1.1px)] [background-size:22px_22px]
    [mask-image:radial-gradient(ellipse_90%_90%_at_50%_50%,#000_40%,transparent_100%)]" />
  {children}
</section>
```

Tailwind arbitrary values can't contain spaces — use `_`. For anything longer than two blobs, a
`@layer utilities { .bg-haze { ... } }` block in the global CSS is cleaner.

## 4. React component (drop-in)

```tsx
export function Haze({ children, className = "" }: { children: React.ReactNode; className?: string }) {
  return <section className={`haze ${className}`}>{children}</section>;
}
```
…with the CSS from §2 in a global stylesheet. Keep it a plain CSS class rather than inline styles so the
blob list isn't re-serialised on every render.

## 5. Type stack

```css
.serif { font-family: "Instrument Serif", "Iowan Old Style", Georgia, serif; font-weight: 400; }
.mono  { font-family: "JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, monospace; }
h1.display { font-size: clamp(56px, 7.6vw, 128px); line-height: .92; letter-spacing: -.025em; }
h1.display em { font-style: italic; }
.eyebrow { font-size: 11px; letter-spacing: .38em; text-transform: uppercase; opacity: .5; }
.pill { font-size: 10px; letter-spacing: .3em; text-transform: uppercase; padding: 8px 16px;
        border-radius: 999px; border: 1px solid rgba(0,0,0,.15); background: rgba(255,255,255,.5); }
```
Google Fonts link: `family=Instrument+Serif:ital@0;1&family=Inter:wght@400;500&family=JetBrains+Mono:wght@400;500`.
Alternatives with the same feel: Fraunces (softer), Newsreader (more bookish), Playfair Display (more fashion).

## 6. Optional: slow drift animation

```css
@keyframes haze-drift {
  0%   { background-position: 0% 0%,  0% 0%,  0% 0%,  0% 0%,  0% 0%,  0% 0%,  0% 0%,  0% 0%,  0% 0%; }
  50%  { background-position: 0% 0%, -3% 2%,  2% -2%, -2% 3%,  3% 1%, -2% -3%,  2% 2%, -3% 1%,  1% -2%; }
  100% { background-position: 0% 0%,  0% 0%,  0% 0%,  0% 0%,  0% 0%,  0% 0%,  0% 0%,  0% 0%,  0% 0%; }
}
.haze.animated { background-size: 110% 110%; animation: haze-drift 48s ease-in-out infinite; }
@media (prefers-reduced-motion: reduce) { .haze.animated { animation: none; } }
```
Set `background-size` above 100% so there is slack to move. Keep cycles ≥ 40 s; fast drift looks like a
loading screen.

## 7. Dark variant

Same structure with `base: #0d0e12`, blob colours around 20–30% lightness (`#1f3a4a`, `#2a2f5c`,
`#4a3a1e`, `#5a2e3a` …), leak `#1c1d24`, dot grid `rgba(255,255,255,.10)`, grain with
`mix-blend-mode: screen`. Ink `#f2f0ea`. `--palette ink` in the script produces exactly this.

## 8. Things that break it

- Blobs under 35% of the box → visible circles.
- Hard stops (anything ending above ~75%) → visible edges.
- Saturated colours (`#ff00aa`) → neon, not haze. Lift lightness first.
- Pure black text or 1px borders around content → the softness collapses.
- A dot grid you can count → halve the opacity.
- `filter: blur()` on the whole section → blurs the text too; keep blur inside `background-image` (radial
  gradients are already soft) or on an absolutely-positioned child.
