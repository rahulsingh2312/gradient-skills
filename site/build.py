#!/usr/bin/env python3
"""Builds site/index.html from the gradient-skin generator so the site is always the real skill output."""
import importlib.util, os, random, sys
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("skin", os.path.join(HERE, "..", "gradient-skin", "scripts", "skin.py"))
skin = importlib.util.module_from_spec(spec); spec.loader.exec_module(skin)

REPO = "https://github.com/rahulsingh2312/gradient-skills"
PALS = ["dawn", "sorbet", "glacier", "dusk", "meadow", "ember", "ink"]

def gradient(pal_name, seed, animate=False, cls=None, intensity=1.0):
    pal = dict(skin.PALETTES[pal_name])
    blobs, leak = skin.make_blobs(pal, "split", random.Random(seed), intensity)
    css = skin.build_css(pal, blobs, leak, dict(grid=True, grid_size=22, grain=0, dark=pal_name == "ink", animate=animate))
    markup = skin.blobs_html(pal, blobs, leak, seed) if animate else ""
    if cls:
        css = css.replace(".skin", "." + cls)
    return css, markup

hero_css, hero_blobs = gradient("dawn", 3, animate=True)
after_css, after_blobs = gradient("dawn", 3, animate=True, cls="after-skin", intensity=1.15)
after_css = after_css.replace("skin-blobs", "after-blobs").replace("skin-blob", "after-blob").replace("skin-leak", "after-leak").replace("skin-drift", "after-drift").replace("skin-content", "after-content")
after_blobs = after_blobs.replace("skin-blobs", "after-blobs").replace("skin-blob", "after-blob").replace("skin-leak", "after-leak")
tiles_css = "".join(gradient(p, 2, cls=f"sk-{p}")[0] for p in PALS)
tiles = "".join(f'<a class="tile sk-{p}" href="#install"><span class="mono">--palette {p}</span></a>' for p in PALS)

html = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>gradient.skin — gradients that feel like light</title>
<meta name="description" content="A Claude Code skill that generates soft pastel mesh gradient heroes: HTML, CSS, SVG or PNG from one prompt.">
<meta property="og:title" content="gradient.skin — gradients that feel like light"><meta property="og:description" content="A Claude Code skill. One prompt → hero page, CSS, SVG or PNG."><meta property="og:image" content="og.png"><meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Inter:wght@400;500;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
html,body{{margin:0}} body{{font-family:Inter,ui-sans-serif,system-ui,sans-serif;-webkit-font-smoothing:antialiased;color:#121212;background:#f6f5f1}}
.serif{{font-family:"Instrument Serif",Georgia,serif;font-weight:400}} .mono{{font-family:"JetBrains Mono",ui-monospace,monospace}}
{hero_css}
.skin{{min-height:100vh}}
.wrap{{position:relative;z-index:2;min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:120px 6vw 96px}}
.wordmark{{position:absolute;top:34px;left:0;right:0;text-align:center;font-size:26px;letter-spacing:-.01em}}
.eyebrow{{font-size:11px;letter-spacing:.38em;text-transform:uppercase;opacity:.5;margin-bottom:22px}}
h1{{font-size:clamp(56px,7.6vw,128px);line-height:.92;letter-spacing:-.025em;margin:0 0 22px}} h1 em{{font-style:italic}}
.sub{{font-size:19px;line-height:1.5;opacity:.62;max-width:36ch;margin:0 0 30px}}
.cmd{{display:inline-flex;align-items:center;gap:14px;max-width:100%;box-sizing:border-box;font-size:14px;padding:12px 18px;border-radius:999px;border:1px solid rgba(0,0,0,.14);background:rgba(255,255,255,.55);backdrop-filter:blur(6px);cursor:pointer;color:inherit}}
.cmd span{{min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
.cmd small{{flex-shrink:0;white-space:nowrap;opacity:.5;font-size:11px;letter-spacing:.2em;text-transform:uppercase}}
.cmd:hover{{background:rgba(255,255,255,.8)}}
.links{{margin-top:28px;font-size:15px;font-weight:500}} .links a{{color:inherit;text-decoration:none;margin:6px 12px;display:inline-block;white-space:nowrap}} .links a:hover{{text-decoration:underline}}
.foot{{position:absolute;bottom:22px;left:0;right:0;text-align:center;font-size:10px;letter-spacing:.32em;text-transform:uppercase;opacity:.42}}
section.plain{{max-width:1100px;margin:0 auto;padding:96px 6vw}}
h2{{font-size:clamp(36px,4.5vw,56px);letter-spacing:-.02em;line-height:1;margin:0 0 12px}} .lede{{opacity:.6;font-size:17px;max-width:52ch;margin:0 0 40px;line-height:1.55}}

/* ---- before / after slider ---- */
.compare{{position:relative;aspect-ratio:16/9;border-radius:18px;overflow:hidden;user-select:none;-webkit-user-select:none;touch-action:pan-y;box-shadow:0 1px 0 rgba(0,0,0,.06),0 24px 60px -30px rgba(0,0,0,.25)}}
.layer{{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:0 8%;box-sizing:border-box}}
.before{{background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);color:#fff}}
.before h3{{font:700 clamp(34px,6vw,84px)/1 Inter,sans-serif;letter-spacing:-.03em;margin:0 0 14px;text-shadow:0 2px 12px rgba(0,0,0,.25)}}
.before p{{font:400 clamp(13px,1.6vw,20px)/1.4 Inter,sans-serif;opacity:.9;margin:0 0 22px;max-width:30ch}}
.before .btn{{background:linear-gradient(#fff,#e8e8f5);color:#5b4bd6;font:700 clamp(12px,1.4vw,17px) Inter,sans-serif;padding:.8em 1.6em;border-radius:8px;box-shadow:0 4px 14px rgba(0,0,0,.25)}}
.after{{clip-path:inset(0 0 0 var(--cut,50%));overflow:hidden}}
{after_css}
.after-skin{{position:absolute;inset:0}}
.after-content{{position:relative;z-index:2;display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%;padding:0 8%;box-sizing:border-box;text-align:center}}
.after h3{{font-size:clamp(38px,6.6vw,96px);line-height:.92;letter-spacing:-.03em;margin:0 0 14px}} .after h3 em{{font-style:italic}}
.after p{{font-size:clamp(13px,1.6vw,19px);line-height:1.45;opacity:.62;margin:0 0 22px;max-width:32ch}}
.after .cta{{font-weight:500;font-size:clamp(13px,1.4vw,18px)}}
.tag{{position:absolute;z-index:3;top:18px;font-size:10px;letter-spacing:.32em;text-transform:uppercase;padding:6px 12px;border-radius:999px;background:rgba(255,255,255,.55);color:#121212;backdrop-filter:blur(6px)}}
.tag.l{{left:18px;background:rgba(0,0,0,.25);color:#fff}} .tag.r{{right:18px}} .tag b{{font-weight:inherit}}
.handle{{position:absolute;top:0;bottom:0;left:var(--cut,50%);width:0;pointer-events:none;z-index:3}}
.handle::before{{content:"";position:absolute;top:0;bottom:0;left:-1px;width:2px;background:#fff;box-shadow:0 0 0 1px rgba(0,0,0,.12)}}
.handle span{{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:48px;height:48px;border-radius:50%;background:#121212;color:#fff;display:flex;align-items:center;justify-content:center;font:500 18px "JetBrains Mono",monospace;box-shadow:0 8px 24px rgba(0,0,0,.3);letter-spacing:-.05em}}
.range{{position:absolute;inset:0;width:100%;height:100%;margin:0;opacity:0;cursor:ew-resize;z-index:4;-webkit-appearance:none;appearance:none;background:transparent}}
.range::-webkit-slider-thumb{{-webkit-appearance:none;width:64px;height:100%}} .range::-moz-range-thumb{{width:64px;height:100%;border:0;background:transparent}}
.hint{{margin-top:14px;font-size:11px;letter-spacing:.3em;text-transform:uppercase;opacity:.45;text-align:center}}

.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:16px}}
.tile{{display:flex;align-items:flex-end;aspect-ratio:16/10;border-radius:14px;padding:14px;text-decoration:none;font-size:12px;color:inherit;overflow:hidden;transition:transform .2s}} .tile:hover{{transform:translateY(-2px)}}
{tiles_css}
.sk-ink{{color:#f2f0ea}}
.steps{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:32px}} .step h3{{font-size:28px;margin:0 0 8px;letter-spacing:-.02em}} .step p{{opacity:.62;line-height:1.55;margin:0 0 10px}}
pre{{background:#121212;color:#f2f0ea;border-radius:12px;padding:18px 20px;font-size:13px;line-height:1.6;overflow-x:auto;margin:0}}
footer{{text-align:center;padding:48px 6vw 64px;font-size:12px;opacity:.5}} footer a{{color:inherit}}
@media (max-width:760px){{
  h1{{font-size:clamp(48px,14vw,96px)}} .wrap{{padding:100px 6vw 80px}}
  .cmd{{font-size:12px;padding:11px 14px;gap:10px}}
  section.plain{{padding:72px 6vw}} .tile{{aspect-ratio:16/9}} .steps{{gap:36px}}
  .compare{{aspect-ratio:4/5;border-radius:14px}} .tag{{font-size:9px;letter-spacing:.22em;padding:5px 9px;top:12px}} .tag.l{{left:12px}} .tag.r{{right:12px}} .tag b{{display:none}}
  pre{{white-space:pre-wrap;word-break:break-all;font-size:12px;padding:14px 16px}}
}}
</style></head>
<body>
<section class="skin">{hero_blobs}<div class="wrap">
  <div class="wordmark serif">gradient.skin</div>
  <div class="eyebrow mono">Claude Code skill</div>
  <h1 class="serif">Gradients that<br><em>feel like light.</em></h1>
  <p class="sub">Soft mesh backgrounds, a dot grid, editorial type. One prompt. Any palette. HTML, CSS, SVG or PNG.</p>
  <button class="cmd mono" onclick="navigator.clipboard.writeText(this.dataset.c);this.querySelector('small').textContent='copied'" data-c="git clone {REPO} && cp -r gradient-skills/gradient-skin ~/.claude/skills/gradient-skin"><span>git clone rahulsingh2312/gradient-skills</span><small>copy install</small></button>
  <div class="links"><a href="{REPO}">GitHub →</a><a href="#compare">Before / after →</a><a href="#palettes">Palettes →</a></div>
  <div class="foot mono">Open source · MIT · gradient.skin</div>
</div></section>

<section class="plain" id="compare">
  <h2 class="serif">The one you copied, <em>and the one you wanted.</em></h2>
  <p class="lede">Left: the gradient every template ships with. Right: the same page after one prompt. Drag the handle.</p>
  <div class="compare" id="cmp" style="--cut:55%">
    <div class="layer before"><h3>Ship faster.</h3><p>The all-in-one platform for modern teams to build, deploy and scale.</p><span class="btn">Get started</span></div>
    <div class="layer after"><div class="after-skin">{after_blobs}<div class="after-content"><h3 class="serif">Ship the<br><em>quiet part.</em></h3><p>Infra that stays out of your way. Built for teams who read the docs.</p><span class="cta">Get started →</span></div></div></div>
    <span class="tag mono l">Before</span><span class="tag mono r">After<b> · one prompt</b></span>
    <div class="handle"><span>&lt;&gt;</span></div>
    <input class="range" type="range" min="2" max="98" value="55" aria-label="Compare before and after">
  </div>
  <div class="hint mono">drag · or just watch it breathe</div>
</section>

<section class="plain" id="palettes">
  <h2 class="serif">Seven palettes, <em>plus yours.</em></h2>
  <p class="lede">Every tile below is the same CSS recipe with a different colour set. Pass a brand hex and gradient.skin derives the eighth.</p>
  <div class="grid">{tiles}</div>
</section>

<section class="plain" id="install">
  <h2 class="serif">Three steps.</h2>
  <p class="lede">A folder with a SKILL.md and a Python script. No packages, no build.</p>
  <div class="steps">
    <div class="step"><h3 class="serif">1. Install</h3><p>Drop the skill in your Claude Code skills folder.</p><pre>git clone {REPO}
cp -r gradient-skills/gradient-skin ~/.claude/skills/gradient-skin</pre></div>
    <div class="step"><h3 class="serif">2. Ask</h3><p>Describe the hero. Mention a palette, a brand colour, or nothing.</p><pre>/gradient-skin launch hero for Acme,
brand #5B4BFF, animated, export OG + X images</pre></div>
    <div class="step"><h3 class="serif">3. Ship</h3><p>Get a responsive page, a CSS block for your codebase, an SVG, or PNGs.</p><pre>hero.html  skin.css
og.png     hero-x.png</pre></div>
  </div>
</section>
<footer class="mono">GRADIENT.SKIN · A CLAUDE CODE SKILL · <a href="{REPO}">github.com/rahulsingh2312/gradient-skills</a></footer>
<script>
(function(){{
  var box=document.getElementById('cmp'), r=box.querySelector('.range'), touched=false;
  function set(v){{ box.style.setProperty('--cut', v+'%'); }}
  r.addEventListener('input', function(){{ touched=true; set(r.value); }});
  r.addEventListener('pointerdown', function(){{ touched=true; }});
  // gentle sweep until the user grabs it, so the page shows what it does at rest
  if(!matchMedia('(prefers-reduced-motion: reduce)').matches){{
    var t0=performance.now();
    (function tick(now){{ if(touched) return; var p=(now-t0)/9000; var v=55+22*Math.sin(p*Math.PI*2); r.value=v; set(v); requestAnimationFrame(tick); }})(t0);
  }}
}})();
</script>
</body></html>'''
open(os.path.join(HERE, "index.html"), "w").write(html)
print("wrote site/index.html", len(html), "bytes")
