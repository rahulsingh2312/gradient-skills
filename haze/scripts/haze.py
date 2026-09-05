#!/usr/bin/env python3
"""
haze.py — generate soft pastel "mesh" gradient backgrounds and editorial hero
sections (the soft "light on paper" look): blurred colour blobs, a white light-leak, a faint
dot grid, optional film grain, and serif display type.

Pure standard library. PNG export shells out to render.mjs (Playwright/Chromium).

Quick examples
  python3 haze.py --out hero.html
  python3 haze.py --palette sorbet --seed 7 --size 1600x900 --format png --out hero.png
  python3 haze.py --blank --palette glacier --format css            # just the CSS
  python3 haze.py --spec spec.json --format png --out og.png        # full control

Run with --help for every flag, or read ../SKILL.md for the design rules.
"""
import argparse, json, os, random, shutil, subprocess, sys, tempfile

# --------------------------------------------------------------------------- palettes
# Each palette: a cool cluster, a warm cluster, a base paper colour and a light-leak.
# Keep every blob colour above ~82% lightness; saturation lives in the *hue contrast*
# between cool and warm, not in any single colour. That is what makes it feel like
# light on paper instead of a 2012 "web 2.0" gradient.
PALETTES = {
    "dawn": {  # the reference look: mint/lavender/pink on the left, cream/gold on the right
        "cool": ["#b6f0dc", "#cfe1ff", "#d7cdf7", "#f3c4e6"],
        "warm": ["#f9efc6", "#f2db95", "#f8d6c0", "#f8e2dc"],
        "base": "#f6f5f1", "leak": "#ffffff", "ink": "#121212",
    },
    "sorbet": {  # peach / raspberry / lemon
        "cool": ["#f8c9d9", "#f6b8c9", "#ffd9e8", "#fbe2f0"],
        "warm": ["#ffe3b3", "#ffd08a", "#fff3c4", "#ffd7b0"],
        "base": "#fff8f3", "leak": "#ffffff", "ink": "#1a1215",
    },
    "glacier": {  # mint / ice blue / lilac, very cold
        "cool": ["#c8f4ec", "#c9e4ff", "#dad4ff", "#e6f6ff"],
        "warm": ["#eef3ff", "#f4f0ff", "#e4f8f3", "#ffffff"],
        "base": "#f3f6fa", "leak": "#ffffff", "ink": "#0e1420",
    },
    "dusk": {  # lavender / rose / apricot, evening light
        "cool": ["#cfc4f7", "#e0c6f2", "#bfd0ff", "#f0c9ea"],
        "warm": ["#ffd9c2", "#ffc9b8", "#ffe7d1", "#ffd6dd"],
        "base": "#f7f3f5", "leak": "#fffaf5", "ink": "#16101c",
    },
    "meadow": {  # sage / lemon / sky, fresh
        "cool": ["#cdeedb", "#bfe9d4", "#cfe6ff", "#e2f3e8"],
        "warm": ["#f7f4b8", "#fff0a8", "#eef7c8", "#fffbe0"],
        "base": "#f5f8f2", "leak": "#ffffff", "ink": "#0f1a12",
    },
    "ember": {  # warm all over: apricot / coral / honey (single-temperature)
        "cool": ["#ffd6c9", "#ffc2b3", "#ffe1cf", "#ffd0d0"],
        "warm": ["#ffe6b0", "#ffd48c", "#fff0cf", "#ffdcae"],
        "base": "#fff6ef", "leak": "#fffaf2", "ink": "#1c120c",
    },
    "ink": {  # dark mode: charcoal with dim aurora
        "cool": ["#1f3a4a", "#2a2f5c", "#1e4a3f", "#3b2a55"],
        "warm": ["#4a3a1e", "#5a2e3a", "#3e3320", "#4b2b2b"],
        "base": "#0d0e12", "leak": "#1c1d24", "ink": "#f2f0ea",
    },
}

LAYOUTS = ("split", "corners", "wash", "halo")

GOOGLE_LINK = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1'
    '&family=Inter:wght@400;500&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">'
)
FONT_FILES = [  # (family, style, weight, file) — OFL fonts vendored in ../assets/fonts
    ("Instrument Serif", "normal", 400, "InstrumentSerif-400.woff2"),
    ("Instrument Serif", "italic", 400, "InstrumentSerif-400i.woff2"),
    ("Inter", "normal", 400, "Inter-400.woff2"),
    ("Inter", "normal", 500, "Inter-500.woff2"),
    ("JetBrains Mono", "normal", 400, "JetBrainsMono-400.woff2"),
    ("JetBrains Mono", "normal", 500, "JetBrainsMono-500.woff2"),
]
FONT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "fonts")

def font_head(mode):
    """google: <link> to Google Fonts (needs network at view time).
       local:  @font-face pointing at the vendored files (file:// — for PNG rendering, offline-safe).
       embed:  @font-face with base64 data URIs (self-contained HTML, ~270 KB heavier).
       system: no webfonts, fall back to Georgia / system-ui."""
    if mode == "google":
        return GOOGLE_LINK
    if mode == "system":
        return ""
    faces = []
    for fam, style, weight, fn in FONT_FILES:
        path = os.path.abspath(os.path.join(FONT_DIR, fn))
        if not os.path.exists(path):
            return GOOGLE_LINK  # vendored fonts missing; degrade to Google
        if mode == "embed":
            import base64
            with open(path, "rb") as f:
                src = "data:font/woff2;base64," + base64.b64encode(f.read()).decode()
        else:
            src = "file://" + path
        faces.append(f"@font-face{{font-family:'{fam}';font-style:{style};font-weight:{weight};font-display:block;src:url('{src}') format('woff2');}}")
    return "<style>" + "".join(faces) + "</style>"

# --------------------------------------------------------------------------- helpers
def hex_to_rgb(h):
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

def rgba(h, a):
    r, g, b = hex_to_rgb(h)
    return f"rgba({r},{g},{b},{a:.2f})"

def parse_size(s):
    w, h = s.lower().split("x")
    return int(w), int(h)

def parse_colors(s):
    return [c.strip() for c in s.split(",") if c.strip()]

# --------------------------------------------------------------------------- blobs
def make_blobs(pal, layout, rng, intensity=1.0):
    """Return a list of blob dicts: x,y (%), rx,ry (% of box), color, alpha."""
    cool, warm = pal["cool"], pal["warm"]
    j = lambda amt: rng.uniform(-amt, amt)
    blobs = []

    def add(x, y, rx, ry, color, alpha):
        blobs.append(dict(x=x + j(5), y=y + j(5), rx=rx + j(6), ry=ry + j(6),
                          color=color, alpha=min(1.0, alpha * intensity)))

    if layout == "split":
        # cool cluster left, warm cluster right, white seam up the middle (the reference)
        add(6, 8, 42, 55, cool[0], .95)
        add(28, 42, 40, 60, cool[1], .85)
        add(14, 66, 44, 50, cool[2], .85)
        add(22, 96, 46, 40, cool[3], .90)
        add(94, 6, 44, 60, warm[1], .90)
        add(70, 26, 40, 55, warm[0], .80)
        add(96, 60, 40, 60, warm[2], .85)
        add(78, 100, 48, 44, warm[3], .90)
        leak = (52, 30, 34, 75)
    elif layout == "corners":
        add(0, 0, 55, 55, cool[0], .95)
        add(100, 0, 55, 55, warm[1], .90)
        add(0, 100, 55, 55, cool[3], .90)
        add(100, 100, 55, 55, warm[2], .90)
        add(50, 100, 45, 40, cool[2], .55)
        add(50, 0, 45, 40, warm[0], .55)
        leak = (50, 50, 42, 48)
    elif layout == "wash":
        # everything mixed, gentle; good behind long text
        cs = cool + warm
        for i in range(8):
            add(rng.uniform(0, 100), rng.uniform(0, 100), 38, 46, cs[i % len(cs)], .70)
        leak = (50, 45, 40, 50)
    else:  # halo: a ring of colour around a bright centre — great for a single centred headline
        ring = cool[:2] + warm[:2] + cool[2:] + warm[2:]
        import math
        for i, c in enumerate(ring):
            a = i / len(ring) * 2 * math.pi
            add(50 + 58 * math.cos(a), 50 + 62 * math.sin(a), 40, 46, c, .85)
        leak = (50, 48, 36, 42)

    return blobs, leak

def css_blob(b):
    return (f"radial-gradient(ellipse {b['rx']:.0f}% {b['ry']:.0f}% at {b['x']:.0f}% {b['y']:.0f}%, "
            f"{rgba(b['color'], b['alpha'])} 0%, {rgba(b['color'], b['alpha'] * .55)} 32%, "
            f"{rgba(b['color'], 0)} 68%)")

def css_leak(pal, leak):
    x, y, rx, ry = leak
    return (f"radial-gradient(ellipse {rx}% {ry}% at {x}% {y}%, "
            f"{rgba(pal['leak'], .95)} 0%, {rgba(pal['leak'], .55)} 38%, {rgba(pal['leak'], 0)} 72%)")

GRAIN_SVG = ("data:image/svg+xml;utf8,"
             "<svg xmlns='http://www.w3.org/2000/svg' width='240' height='240'>"
             "<filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/>"
             "<feColorMatrix values='0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .6 0'/></filter>"
             "<rect width='100%25' height='100%25' filter='url(%23n)'/></svg>")

# --------------------------------------------------------------------------- css
def build_css(pal, blobs, leak, opts):
    layers = [css_leak(pal, leak)] + [css_blob(b) for b in blobs]
    dark = pal is PALETTES.get("ink") or opts.get("dark")
    dot = "rgba(255,255,255,.10)" if dark else "rgba(15,15,15,.09)"
    grid = ""
    if opts.get("grid", True):
        grid = f"""
.haze::before {{
  content:""; position:absolute; inset:0; pointer-events:none;
  background-image: radial-gradient({dot} 0.9px, transparent 1.1px);
  background-size: {opts.get('grid_size', 22)}px {opts.get('grid_size', 22)}px;
  mask-image: radial-gradient(ellipse 90% 90% at 50% 50%, #000 40%, transparent 100%);
}}"""
    grain = ""
    if opts.get("grain", 0) > 0:
        grain = f"""
.haze::after {{
  content:""; position:absolute; inset:0; pointer-events:none;
  background-image: url("{GRAIN_SVG}");
  opacity:{opts['grain']:.2f}; mix-blend-mode:{'screen' if dark else 'multiply'};
}}"""
    return f"""
.haze {{
  --haze-base: {pal['base']};
  --haze-ink: {pal['ink']};
  position:relative; overflow:hidden; isolation:isolate;
  background-color: var(--haze-base);
  background-image:
    {(',' + chr(10) + '    ').join(layers)};
  background-repeat:no-repeat; background-size:100% 100%;
  color: var(--haze-ink);
}}{grid}{grain}
"""

TYPE_CSS = """
.haze { font-family: "Inter", ui-sans-serif, system-ui, -apple-system, "Segoe UI", Helvetica, Arial, sans-serif; -webkit-font-smoothing:antialiased; }
.haze .serif { font-family: "Instrument Serif", "Iowan Old Style", "Playfair Display", Georgia, "Times New Roman", serif; font-weight:400; }
.haze .mono  { font-family: "JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }
.haze-content { position:relative; z-index:1; min-height:100%; display:flex; flex-direction:column; }
.haze-wordmark { position:absolute; top:34px; left:0; right:0; text-align:center; font-size:28px; letter-spacing:-.01em; }
.haze-panels { flex:1; display:grid; grid-template-columns: repeat(var(--n,1), 1fr); align-items:center; padding: 120px 6vw 96px; gap: 4vw; }
.haze-panel { text-align:center; display:flex; flex-direction:column; align-items:center; }
.haze-eyebrow { font-size:11px; letter-spacing:.38em; text-transform:uppercase; opacity:.5; margin-bottom:22px; }
.haze-h1 { font-size: clamp(56px, 7.6vw, 128px); line-height:.92; letter-spacing:-.025em; margin:0 0 22px; }
.haze-h1 em { font-style:italic; letter-spacing:-.02em; }
.haze-sub { font-size: 19px; line-height:1.5; opacity:.62; max-width: 34ch; margin:0 0 26px; }
.haze-badge { display:inline-block; font-size:10px; letter-spacing:.3em; text-transform:uppercase; padding:8px 16px; border-radius:999px; border:1px solid color-mix(in srgb, currentColor 18%, transparent); background: color-mix(in srgb, var(--haze-base) 55%, transparent); margin-bottom:30px; }
.haze-cta { font-size:17px; font-weight:500; text-decoration:none; color:inherit; }
.haze-cta span { display:inline-block; margin-left:.45em; transition:transform .2s; }
.haze-cta:hover span { transform:translateX(3px); }
.haze-footer { position:absolute; bottom:22px; left:0; right:0; text-align:center; font-size:10px; letter-spacing:.32em; text-transform:uppercase; opacity:.42; }
.haze-topbar { height:44px; background:#000; }
.haze-topbar + .haze-wordmark { top:78px; }
@media (max-width: 760px) { .haze-panels { grid-template-columns:1fr; padding:110px 8vw 80px; gap:64px; } .haze-h1 { font-size: clamp(52px, 15vw, 96px); } }
"""

# --------------------------------------------------------------------------- html
def esc(s):
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def panel_html(p):
    h = ""
    if p.get("eyebrow"):
        h += f'<div class="haze-eyebrow mono">{esc(p["eyebrow"])}</div>'
    if p.get("headline") or p.get("italic"):
        h += '<h1 class="haze-h1 serif">'
        if p.get("headline"):
            h += esc(p["headline"])
        if p.get("italic"):
            h += ('<br>' if p.get("headline") else '') + f'<em>{esc(p["italic"])}</em>'
        h += '</h1>'
    if p.get("sub"):
        h += f'<p class="haze-sub">{esc(p["sub"])}</p>'
    if p.get("badge"):
        h += f'<div class="haze-badge mono">{esc(p["badge"])}</div>'
    if p.get("cta"):
        h += f'<a class="haze-cta" href="{esc(p.get("href", "#"))}">{esc(p["cta"])}<span>&rarr;</span></a>'
    return f'<div class="haze-panel">{h}</div>'

def build_html(spec, css, w, h, standalone_size=True):
    fonts = font_head(spec.get("fonts") or "google")
    panels = spec.get("panels") or []
    content = ""
    if not spec.get("blank"):
        if spec.get("topbar"):
            content += '<div class="haze-topbar"></div>'
        if spec.get("wordmark"):
            content += f'<div class="haze-wordmark serif">{esc(spec["wordmark"])}</div>'
        if panels:
            content += f'<div class="haze-panels" style="--n:{len(panels)}">' + "".join(panel_html(p) for p in panels) + "</div>"
        if spec.get("footer"):
            content += f'<div class="haze-footer mono">{esc(spec["footer"])}</div>'
    size_css = f"html,body{{margin:0;height:100%}} .haze{{width:{w}px;height:{h}px}}" if standalone_size else "html,body{margin:0;height:100%} .haze{min-height:100vh}"
    title = esc(spec.get("title") or spec.get("wordmark") or "Haze")
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
{fonts}
<style>
{size_css}
{css}
{TYPE_CSS}
</style></head>
<body><section class="haze"><div class="haze-content">{content}</div></section></body></html>
"""

# --------------------------------------------------------------------------- svg (no browser needed)
def build_svg(pal, blobs, leak, spec, w, h):
    defs, shapes = [], []
    x, y, rx, ry = leak
    for i, b in enumerate([dict(x=x, y=y, rx=rx, ry=ry, color=pal["leak"], alpha=.95)] + blobs):
        r, g, bb = hex_to_rgb(b["color"])
        defs.append(f'<radialGradient id="g{i}"><stop offset="0" stop-color="rgb({r},{g},{bb})" stop-opacity="{b["alpha"]:.2f}"/>'
                    f'<stop offset=".45" stop-color="rgb({r},{g},{bb})" stop-opacity="{b["alpha"]*.5:.2f}"/>'
                    f'<stop offset="1" stop-color="rgb({r},{g},{bb})" stop-opacity="0"/></radialGradient>')
        shapes.append(f'<ellipse cx="{b["x"]/100*w:.0f}" cy="{b["y"]/100*h:.0f}" rx="{b["rx"]/100*w:.0f}" ry="{b["ry"]/100*h:.0f}" fill="url(#g{i})"/>')
    grid = ""
    if spec.get("grid", True):
        dark = spec.get("dark")
        grid = (f'<pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r=".9" fill="{"#fff" if dark else "#000"}" fill-opacity=".11"/></pattern>'
                f'<rect width="100%" height="100%" fill="url(#dots)"/>')
    text = ""
    if not spec.get("blank") and spec.get("panels"):
        p = spec["panels"][0]
        ink = pal["ink"]
        cy = h * .46
        if p.get("eyebrow"):
            text += f'<text x="50%" y="{cy - h*.13:.0f}" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="{h*.014:.0f}" letter-spacing="{h*.005:.1f}" fill="{ink}" fill-opacity=".5">{esc(p["eyebrow"].upper())}</text>'
        fs = h * .13
        if p.get("headline"):
            text += f'<text x="50%" y="{cy:.0f}" text-anchor="middle" font-family="Instrument Serif, Georgia, serif" font-size="{fs:.0f}" letter-spacing="{-fs*.025:.1f}" fill="{ink}">{esc(p["headline"])}</text>'
        if p.get("italic"):
            text += f'<text x="50%" y="{cy + fs*.95:.0f}" text-anchor="middle" font-family="Instrument Serif, Georgia, serif" font-style="italic" font-size="{fs:.0f}" letter-spacing="{-fs*.02:.1f}" fill="{ink}">{esc(p["italic"])}</text>'
        if p.get("sub"):
            text += f'<text x="50%" y="{cy + fs*1.55:.0f}" text-anchor="middle" font-family="Inter, system-ui, sans-serif" font-size="{h*.024:.0f}" fill="{ink}" fill-opacity=".62">{esc(p["sub"])}</text>'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f'<defs>{"".join(defs)}<filter id="blur"><feGaussianBlur stdDeviation="{min(w,h)*.04:.0f}"/></filter></defs>'
            f'<rect width="100%" height="100%" fill="{pal["base"]}"/>'
            f'<g filter="url(#blur)">{"".join(shapes)}</g>{grid}{text}</svg>')

# --------------------------------------------------------------------------- png
def render_png(html_path, out, w, h, scale):
    here = os.path.dirname(os.path.abspath(__file__))
    renderer = os.path.join(here, "render.mjs")
    env = dict(os.environ)
    if not env.get("NODE_PATH"):
        try:
            env["NODE_PATH"] = subprocess.check_output(["npm", "root", "-g"], text=True).strip()
        except Exception:
            pass
    cmd = ["node", renderer, html_path, out, f"{w}x{h}", str(scale)]
    r = subprocess.run(cmd, env=env, capture_output=True, text=True)
    if r.returncode != 0:
        sys.stderr.write(r.stderr)
        # fallback: bare chromium headless screenshot
        chrome = shutil.which("chromium") or shutil.which("chromium-browser") or shutil.which("google-chrome")
        if chrome:
            subprocess.run([chrome, "--headless=new", "--hide-scrollbars", f"--window-size={w},{h}",
                            f"--screenshot={out}", "--virtual-time-budget=4000", f"file://{html_path}"], check=True)
        else:
            sys.exit("PNG export needs Node + Playwright (npm i -g playwright && npx playwright install chromium) "
                     "or a chromium binary on PATH. The HTML was still written next to the output.")

# --------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default="haze.html")
    ap.add_argument("--format", choices=["html", "png", "svg", "css"], default=None, help="inferred from --out extension if omitted")
    ap.add_argument("--size", default="1600x900", help="WxH px, e.g. 1200x630 (OG), 1600x900 (X), 1080x1080")
    ap.add_argument("--scale", type=float, default=2, help="device pixel ratio for PNG (2 = retina)")
    ap.add_argument("--palette", choices=sorted(PALETTES), default="dawn")
    ap.add_argument("--colors", help="custom comma list of 8 hex colours: first 4 cool, last 4 warm")
    ap.add_argument("--base", help="paper colour override, e.g. #f7f6f2")
    ap.add_argument("--layout", choices=LAYOUTS, default="split")
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--intensity", type=float, default=1.0, help="0.6 = whisper, 1.0 = reference, 1.3 = punchy")
    ap.add_argument("--no-grid", action="store_true")
    ap.add_argument("--grid-size", type=int, default=22)
    ap.add_argument("--grain", type=float, default=0.0, help="0–0.2; 0.06 is a nice film feel")
    ap.add_argument("--fonts", choices=["google", "local", "embed", "system"], default=None,
                    help="google (default for html), local (default for png; vendored files), embed (base64, self-contained), system")
    ap.add_argument("--topbar", action="store_true", help="44px black bar across the top")
    ap.add_argument("--blank", action="store_true", help="no text, just the background")
    ap.add_argument("--spec", help="JSON file with wordmark/panels/footer etc. (see SKILL.md)")
    # single-panel shortcuts
    ap.add_argument("--wordmark"); ap.add_argument("--eyebrow"); ap.add_argument("--headline")
    ap.add_argument("--italic", help="second headline line, set in italic"); ap.add_argument("--sub")
    ap.add_argument("--badge"); ap.add_argument("--cta"); ap.add_argument("--href"); ap.add_argument("--footer")
    ap.add_argument("--responsive", action="store_true", help="HTML fills the viewport instead of fixed WxH")
    a = ap.parse_args()

    spec = {}
    if a.spec:
        with open(a.spec) as f:
            spec = json.load(f)
    # CLI flags override spec
    for k in ("palette", "layout", "seed", "intensity", "grain", "fonts", "wordmark", "footer", "size", "base", "colors"):
        v = getattr(a, k)
        if v not in (None, ap.get_default(k)) or k not in spec:
            spec[k] = v if v is not None else spec.get(k)
    if a.blank: spec["blank"] = True
    if a.topbar: spec["topbar"] = True
    if a.no_grid: spec["grid"] = False
    spec.setdefault("grid", True)
    spec["grid_size"] = a.grid_size
    if any(getattr(a, k) for k in ("eyebrow", "headline", "italic", "sub", "badge", "cta")):
        spec["panels"] = [dict(eyebrow=a.eyebrow, headline=a.headline, italic=a.italic, sub=a.sub, badge=a.badge, cta=a.cta, href=a.href)]
    if not spec.get("panels") and not spec.get("blank"):
        spec["panels"] = [dict(eyebrow="Haze", headline="Soft light,", italic="on demand.", sub="A pastel mesh gradient with a dot grid and editorial type. Change the words, keep the glow.", badge="Live", cta="Enter")]
        spec.setdefault("wordmark", "Haze.")

    pal = dict(PALETTES[spec.get("palette") or "dawn"])
    if spec.get("colors"):
        cs = parse_colors(spec["colors"]) if isinstance(spec["colors"], str) else spec["colors"]
        if len(cs) < 2: sys.exit("--colors needs at least 2 hex colours")
        while len(cs) < 8: cs = cs + cs
        pal["cool"], pal["warm"] = cs[:4], cs[4:8]
    if spec.get("base"): pal["base"] = spec["base"]
    if spec.get("ink"): pal["ink"] = spec["ink"]
    if spec.get("palette") == "ink": spec["dark"] = True

    w, h = parse_size(spec.get("size") or a.size)
    rng = random.Random(int(spec.get("seed") or 1))
    blobs, leak = make_blobs(pal, spec.get("layout") or "split", rng, float(spec.get("intensity") or 1.0))
    css = build_css(pal, blobs, leak, dict(grid=spec["grid"], grid_size=a.grid_size, grain=float(spec.get("grain") or 0), dark=spec.get("dark")))

    fmt = a.format or os.path.splitext(a.out)[1].lstrip(".").lower() or "html"
    if not spec.get("fonts"):
        spec["fonts"] = "local" if fmt == "png" else "google"
    if fmt == "css":
        sys.stdout.write(css + ("\n/* type helpers */" + TYPE_CSS if not spec.get("blank") else ""))
        return
    if fmt == "svg":
        with open(a.out, "w") as f: f.write(build_svg(pal, blobs, leak, spec, w, h))
    elif fmt == "html":
        with open(a.out, "w") as f: f.write(build_html(spec, css, w, h, standalone_size=not a.responsive))
    elif fmt == "png":
        html_path = os.path.splitext(a.out)[0] + ".html"
        with open(html_path, "w") as f: f.write(build_html(spec, css, w, h))
        render_png(os.path.abspath(html_path), os.path.abspath(a.out), w, h, a.scale)
    print(f"wrote {a.out}  ({fmt}, {w}x{h}, palette={spec.get('palette')}, layout={spec.get('layout')}, seed={spec.get('seed')})")

if __name__ == "__main__":
    main()
