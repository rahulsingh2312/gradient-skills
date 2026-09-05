#!/usr/bin/env python3
"""Compose the article image that pairs the original post with ours.

The original post lives on X and cannot be downloaded from here, so save a
screenshot of it locally and pass the path:

    python3 launch/compose.py --shot ~/Downloads/ryan.png
    python3 launch/compose.py --shot ~/Downloads/ryan.png --layout stacked

Without --shot it falls back to a quote card that credits the post and shows
its permalink, so the image still builds.
"""
import argparse, base64, mimetypes, os, random, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "gradient-skin", "scripts"))
import skin  # noqa: E402

SOURCE_URL = "https://x.com/ryandavogel/status/1956365206147244167"
SOURCE_CAPTION = "@ryandavogel · aug 15 · 111K views"
SOURCE_TEXT = "pov you are about to look at the worst code ever generated:"
FONTS = os.path.join(ROOT, "gradient-skin", "assets", "fonts")


def face(family, file, style="normal", weight="400"):
    return (f'@font-face{{font-family:"{family}";font-style:{style};font-weight:{weight};'
            f'src:url("file://{FONTS}/{file}") format("woff2")}}')


FONT_CSS = "".join([
    face("Instrument Serif", "InstrumentSerif-400.woff2"),
    face("Instrument Serif", "InstrumentSerif-400i.woff2", style="italic"),
    face("Inter", "Inter-400.woff2"),
    face("Inter", "Inter-500.woff2", weight="500"),
    face("Inter", "Inter-500.woff2", weight="700"),
    face("JetBrains Mono", "JetBrainsMono-400.woff2"),
])


def palette_css(name, cls, seed):
    pal = skin.PALETTES[name]
    rng = random.Random(seed)
    blobs, leak = skin.make_blobs(pal, "split", rng)
    css = skin.build_css(pal, blobs, leak, {"grid": True})
    return css.replace(".skin", "." + cls)


def data_uri(path):
    mime = mimetypes.guess_type(path)[0] or "image/png"
    with open(path, "rb") as fh:
        return f"data:{mime};base64," + base64.b64encode(fh.read()).decode()


TICK = ('<svg viewBox="0 0 24 24" width="22" height="22"><circle cx="12" cy="12" r="11" fill="#00b96b"/>'
        '<path d="M7 12.5l3.2 3.2L17 9" stroke="#fff" stroke-width="2.6" fill="none" '
        'stroke-linecap="round" stroke-linejoin="round"/></svg>')
XLOGO = ('<svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor"><path d="M18.9 2H22l-7.4 '
         '8.5L23 22h-6.8l-5.3-6.9L4.8 22H1.7l7.9-9L0 2h7l4.8 6.3L18.9 2z"/></svg>')


def their_card(shot):
    if shot:
        return (f'<div class="card shot"><div class="tag">{SOURCE_CAPTION}</div>'
                f'<img src="{data_uri(shot)}" alt="the original post">'
                f'<div class="meta link">{SOURCE_URL.replace("https://", "")}</div></div>')
    return (f'<div class="card q"><div class="tag">{SOURCE_CAPTION}</div>'
            f'<div class="txt">{SOURCE_TEXT}</div><div class="img ugly"></div>'
            f'<div class="meta link">{SOURCE_URL.replace("https://", "")}</div></div>')


OUR_CARD = f'''<div class="card">
  <div class="head"><div class="meadow avatar"></div><b>gradient.skin</b>{TICK}<span>@gradientskin</span><span class="x">{XLOGO}</span></div>
  <div class="txt">pov you are about to look at the <b>best</b> gradient ever generated:</div>
  <div class="img meadow inner"><span class="serif">Not that <em>gradient.</em></span></div>
  <div class="meta"><b>one prompt</b> · open source claude code skill · gradient.skin</div>
</div>'''


def build(shot, layout, w, h):
    stacked = layout == "stacked"
    flow = "column" if stacked else "row"
    card_w = 900 if stacked else 640
    return f'''<html><head><meta charset="utf-8"><style>
{FONT_CSS}
html,body{{margin:0;height:100%;overflow:hidden}}
body{{font-family:Inter,sans-serif;-webkit-font-smoothing:antialiased;color:#121212}}
.c{{position:relative;width:{w}px;height:{h}px;overflow:hidden}}
{palette_css("dawn", "bg", 7)}
{palette_css("meadow", "meadow", 3)}
.bg{{position:absolute;inset:0}}
.z{{position:relative;z-index:2;height:100%;display:flex;flex-direction:{flow};align-items:center;
   justify-content:center;gap:{34 if stacked else 40}px;padding:{46 if stacked else 0}px 70px;box-sizing:border-box}}
.card{{width:{card_w}px;background:#fff;border-radius:22px;padding:30px 34px;box-sizing:border-box;
   box-shadow:0 30px 80px -30px rgba(0,0,0,.28);display:flex;flex-direction:column;gap:14px}}
.card.q,.card.shot{{background:rgba(255,255,255,.72);backdrop-filter:blur(8px)}}
.card.shot img{{width:100%;border-radius:14px;display:block;object-fit:contain;
   max-height:{620 if stacked else 660}px}}
.head{{display:flex;align-items:center;gap:10px;font-size:22px}}
.head b{{font-weight:700}} .head span{{opacity:.5}} .head .x{{margin-left:auto;opacity:.55}}
.avatar{{position:relative;width:44px;height:44px;border-radius:50%;flex:none}}
.tag{{font:500 11px "JetBrains Mono",monospace;letter-spacing:.32em;text-transform:uppercase;color:rgba(0,0,0,.5)}}
.txt{{font-size:26px;line-height:1.3}} .txt b{{font-weight:700}}
.img{{height:{300 if stacked else 270}px;border-radius:14px;overflow:hidden;position:relative;
   display:flex;align-items:center;justify-content:center}}
.ugly{{background:linear-gradient(90deg,#3b82f6,#a855f7,#ec4899)}}
.inner{{position:relative}}
.meta{{font-size:14px;color:rgba(0,0,0,.45)}} .meta b{{color:#121212;font-weight:700}}
.meta.link{{font:500 13px "JetBrains Mono",monospace;color:rgba(0,0,0,.42)}}
.serif{{font-family:"Instrument Serif",serif;font-weight:400;font-size:64px;letter-spacing:-.03em;color:#121212}}
.arrow{{font:400 {54 if stacked else 60}px "Instrument Serif",serif;color:#121212;opacity:.7}}
</style></head><body><div class="c"><div class="bg"></div><div class="z">
{their_card(shot)}
<div class="arrow">{'↓' if stacked else '→'}</div>
{OUR_CARD}
</div></div></body></html>'''


def main():
    ap = argparse.ArgumentParser(description="Compose the two-post article image.")
    ap.add_argument("--shot", help="path to a screenshot of the original post")
    ap.add_argument("--layout", choices=["side", "stacked"], default="side")
    ap.add_argument("--out", default=os.path.join(HERE, "images", "article-two-tweets.png"))
    ap.add_argument("--size", default=None, help="WxH, defaults to 1600x900 (side) / 1200x1500 (stacked)")
    ap.add_argument("--scale", type=float, default=1.0)
    a = ap.parse_args()
    if a.shot and not os.path.exists(a.shot):
        sys.exit(f"no such screenshot: {a.shot}")
    w, h = skin.parse_size(a.size) if a.size else ((1600, 900) if a.layout == "side" else (1200, 1500))
    html = build(a.shot, a.layout, w, h)
    html_path = os.path.splitext(a.out)[0] + ".html"
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    with open(html_path, "w") as fh:
        fh.write(html)
    skin.render_png(html_path, a.out, w, h, a.scale)
    os.remove(html_path)
    print(a.out)


if __name__ == "__main__":
    main()
