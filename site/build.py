#!/usr/bin/env python3
"""Builds site/index.html from the gradient-skin generator so the site is always the real skill output."""
import importlib.util, os, random, sys
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("skin", os.path.join(HERE, "..", "gradient-skin", "scripts", "skin.py"))
skin = importlib.util.module_from_spec(spec); spec.loader.exec_module(skin)

REPO = "https://github.com/rahulsingh2312/gradient-skills"
SITE = "https://gradient-skin.vercel.app"   # switch to https://gradient.skin once the domain resolves
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
after_css, after_blobs = gradient("dawn", 3, animate=True, intensity=1.15)
for a, b in (("skin-blobs", "after-blobs"), ("skin-blob", "after-blob"), ("skin-leak", "after-leak"),
             ("skin-drift", "after-drift"), ("skin-content", "after-content"), (".skin", ".after-skin")):
    after_css = after_css.replace(a, b)
    after_blobs = after_blobs.replace(a, b)
tiles_css = "".join(gradient(p, 2, cls=f"sk-{p}")[0] for p in PALS)
tiles = "".join(f'<a class="tile sk-{p}" href="#install"><span class="mono">--palette {p}</span></a>' for p in PALS)

html = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>gradient.skin — not that gradient</title>
<meta name="description" content="Soft mesh gradient heroes for your landing page. One prompt.">
<meta property="og:type" content="website"><meta property="og:url" content="{SITE}/"><meta property="og:site_name" content="gradient.skin">
<meta property="og:title" content="Not that gradient."><meta property="og:description" content="Soft mesh gradient heroes for your landing page. One prompt."><meta property="og:image" content="{SITE}/og.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="Not that gradient. A soft pastel mesh gradient hero.">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="Not that gradient."><meta name="twitter:description" content="Soft mesh gradient heroes for your landing page. One prompt."><meta name="twitter:image" content="{SITE}/og.png">
<meta name="theme-color" content="#f6f5f1"><link rel="canonical" href="{SITE}/">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 64 64%27%3E%3Cdefs%3E%3ClinearGradient id=%27g%27 x1=%270%27 y1=%270%27 x2=%271%27 y2=%271%27%3E%3Cstop offset=%270%27 stop-color=%27%23b6f0dc%27/%3E%3Cstop offset=%27.5%27 stop-color=%27%23fbfaf6%27/%3E%3Cstop offset=%271%27 stop-color=%27%23f2db95%27/%3E%3C/linearGradient%3E%3C/defs%3E%3Crect width=%2764%27 height=%2764%27 rx=%2716%27 fill=%27url(%23g)%27/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Inter:wght@400;500;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
html,body{{margin:0}} body{{font-family:Inter,ui-sans-serif,system-ui,sans-serif;-webkit-font-smoothing:antialiased;color:#121212;background:#f6f5f1}}
.serif{{font-family:"Instrument Serif",Georgia,serif;font-weight:400}} .mono{{font-family:"JetBrains Mono",ui-monospace,monospace}}
{hero_css}

/* ---- hero = the comparison. Same words on both layers; only the skin changes. ---- */
.hero{{position:relative;min-height:100vh;overflow:hidden;user-select:none;-webkit-user-select:none}}
.layer{{position:absolute;inset:0;isolation:isolate}} .ugly{{z-index:1}} .good{{z-index:2}}
.ugly{{background:linear-gradient(90deg,#3b82f6 0%,#a855f7 50%,#ec4899 100%);color:#fff}}
.good{{clip-path:inset(0 0 0 var(--cut,92%))}}
.good .skin{{position:absolute;inset:0;min-height:0}}
.wrap{{position:relative;z-index:2;min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:120px 6vw 96px;box-sizing:border-box}}
.wordmark{{position:absolute;top:34px;left:0;right:0;text-align:center;font-size:26px;letter-spacing:-.01em}}
.ugly .wordmark{{font-weight:700;letter-spacing:-.02em}}
.eyebrow{{font-size:11px;letter-spacing:.38em;text-transform:uppercase;opacity:.5;margin-bottom:22px;height:14px}}
.ugly .eyebrow{{opacity:.85}}
h1{{font-size:clamp(56px,7.6vw,128px);line-height:.92;letter-spacing:-.025em;margin:0 0 22px;height:calc(2 * .92em)}} h1 em{{font-style:italic}}
.ugly h1{{font-weight:700;letter-spacing:-.045em;text-shadow:0 2px 18px rgba(0,0,0,.25)}} .ugly h1 em{{font-style:normal}}
.sub{{font-size:19px;line-height:1.5;opacity:.62;max-width:36ch;margin:0 0 30px;min-height:calc(3 * 1.5em)}}
.ugly .sub{{opacity:.92}}
.cmd{{display:inline-flex;align-items:center;gap:14px;max-width:100%;box-sizing:border-box;height:44px;font-size:14px;padding:0 18px;border-radius:10px;border:1px solid rgba(0,0,0,.14);background:rgba(255,255,255,.55);backdrop-filter:blur(6px);cursor:pointer;color:inherit;font-family:inherit}}
.cmd span{{min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
.cmd small{{flex-shrink:0;white-space:nowrap;opacity:.5;font-size:11px;letter-spacing:.2em;text-transform:uppercase}}
.cmd:hover{{background:rgba(255,255,255,.8)}}
.ugly .cmd{{background:#fff;color:#7c3aed;border-color:transparent;box-shadow:0 8px 24px rgba(0,0,0,.25);font-weight:700}} .ugly .cmd small{{opacity:.6}}
.links{{margin-top:28px;font-size:15px;font-weight:500;height:28px}} .links a{{color:inherit;text-decoration:none;margin:6px 12px;display:inline-block;white-space:nowrap}} .links a:hover{{text-decoration:underline}}
.foot{{position:absolute;bottom:22px;left:0;right:0;text-align:center;font-size:10px;letter-spacing:.32em;text-transform:uppercase;opacity:.42}}
.ugly .foot{{opacity:.8}}
.tag{{position:absolute;z-index:4;top:22px;font-size:10px;letter-spacing:.32em;text-transform:uppercase;padding:7px 12px;border-radius:7px;pointer-events:none;transition:opacity .3s}}
.tag b{{font-weight:inherit}} .tag.l{{left:22px;background:rgba(0,0,0,.28);color:#fff}} .tag.r{{right:22px;background:rgba(255,255,255,.6);color:#121212;backdrop-filter:blur(6px)}}
.hero[data-cut="0"] .tag.l{{opacity:0}} .hero[data-cut="100"] .tag.r{{opacity:0}}
.grip{{position:absolute;z-index:5;top:0;bottom:0;left:var(--cut,92%);width:0;cursor:ew-resize;touch-action:pan-y;outline:none}}
.grip::before{{content:"";position:absolute;top:0;bottom:0;left:-1px;width:2px;background:#1c1c21}}
.grip::after{{content:"";position:absolute;top:0;bottom:0;left:-32px;width:64px}}
.grip i{{position:absolute;top:50%;left:0;transform:translate(-50%,-50%);width:40px;height:40px;border-radius:50%;background:#1c1c21;color:#fff;display:flex;align-items:center;justify-content:center;box-shadow:0 6px 18px rgba(0,0,0,.28);font-style:normal;transition:transform .2s}}
.grip i svg{{width:18px;height:18px;display:block;transition:transform .2s}}
.grip:hover i,.grip:focus-visible i{{transform:translate(-50%,-50%) scale(1.08)}}
.grip:focus-visible i{{box-shadow:0 0 0 2px #fff,0 6px 18px rgba(0,0,0,.28)}}
/* parked at an edge: half the circle is off-screen, so it reads as a tab with one chevron */
.hero[data-cut="0"] .grip::before,.hero[data-cut="100"] .grip::before{{opacity:0}}
.hero[data-cut="0"] .grip i svg{{transform:translateX(6px)}} .hero[data-cut="0"] .grip i svg .l{{display:none}}
.hero[data-cut="100"] .grip i svg{{transform:translateX(-6px)}} .hero[data-cut="100"] .grip i svg .r{{display:none}}
@media (prefers-reduced-motion:reduce){{.grip i{{transition:none}}}}

section.plain{{max-width:1100px;margin:0 auto;padding:96px 6vw}}
h2{{font-size:clamp(36px,4.5vw,56px);letter-spacing:-.02em;line-height:1;margin:0 0 12px}} .lede{{opacity:.6;font-size:17px;max-width:52ch;margin:0 0 40px;line-height:1.55}}
.grid{{display:grid;grid-template-columns:repeat(2,1fr);gap:20px}}
.tile{{display:flex;align-items:flex-end;aspect-ratio:16/10;border-radius:18px;padding:18px;text-decoration:none;font-size:14px;color:inherit;overflow:hidden;transition:transform .2s}} .tile:hover{{transform:translateY(-2px)}}
{tiles_css}
.sk-ink{{color:#f2f0ea}}
.steps{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:32px}} .step h3{{font-size:28px;margin:0 0 8px;letter-spacing:-.02em}} .step p{{opacity:.62;line-height:1.55;margin:0 0 12px}}
pre{{background:#121212;color:#f2f0ea;border-radius:12px;padding:18px 20px;font-size:13px;line-height:1.9;overflow-x:auto;margin:0;white-space:pre}} pre.soft{{white-space:pre-wrap}}
footer{{text-align:center;padding:48px 6vw 64px;font-size:12px;opacity:.5}} footer a{{color:inherit}}
@media (max-width:760px){{
  h1{{font-size:clamp(38px,11.5vw,96px)}} .wrap{{padding:100px 6vw 80px}} .sub{{font-size:17px;max-width:34ch}}
  .cmd{{font-size:12px;padding:0 14px;gap:10px}}
  section.plain{{padding:72px 6vw}}
  .grid{{grid-template-columns:1fr;gap:16px}} .tile{{aspect-ratio:16/10;border-radius:14px}}
  .steps{{gap:36px}} pre{{font-size:12px;padding:16px 16px;line-height:2}}
  .tag{{top:14px;font-size:9px;letter-spacing:.22em;padding:5px 9px}} .tag.l{{left:14px}} .tag.r{{right:14px}} .tag b{{display:none}} .wordmark{{top:48px;font-size:22px}}
}}
</style></head>
<body>
<section class="hero" id="hero" style="--cut:92%">
  <div class="layer ugly"><div class="wrap">
    <div class="wordmark">gradient.skin</div>
    <div class="eyebrow mono">Claude Code skill</div>
    <h1>Not that<br><em>gradient.</em></h1>
    <p class="sub">The blue-to-pink one every AI reaches for. One prompt swaps it for soft light on paper. HTML, CSS, SVG or PNG.</p>
    <button class="cmd mono" data-copy><span>curl -fsSL gradient.skin/install | sh</span><small>copy</small></button>
    <div class="links"><a href="{REPO}">GitHub →</a><a href="#palettes">Palettes →</a></div>
    <div class="foot mono">Open source · MIT · gradient.skin</div>
  </div></div>
  <div class="layer good"><section class="skin">{hero_blobs}<div class="wrap">
    <div class="wordmark serif">gradient.skin</div>
    <div class="eyebrow mono">Claude Code skill</div>
    <h1 class="serif">Not that<br><em>gradient.</em></h1>
    <p class="sub">The blue-to-pink one every AI reaches for. One prompt swaps it for soft light on paper. HTML, CSS, SVG or PNG.</p>
    <button class="cmd mono" data-copy><span>curl -fsSL gradient.skin/install | sh</span><small>copy</small></button>
    <div class="links"><a href="{REPO}">GitHub →</a><a href="#palettes">Palettes →</a></div>
    <div class="foot mono">Open source · MIT · gradient.skin</div>
  </div></section></div>
  <span class="tag mono l">Before</span><span class="tag mono r">After<b> · one prompt</b></span>
  <div class="grip" role="slider" tabindex="0" aria-label="Compare the template gradient with gradient.skin" aria-valuemin="0" aria-valuemax="100" aria-valuenow="92"><i><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path class="l" d="M9 7l-5 5 5 5"/><path class="r" d="M15 7l5 5-5 5"/></svg></i></div>
</section>

<section class="plain" id="palettes">
  <h2 class="serif">Seven palettes, <em>plus yours.</em></h2>
  <p class="lede">Every tile below is the same CSS recipe with a different colour set. Pass a brand hex and gradient.skin derives the eighth.</p>
  <div class="grid">{tiles}</div>
</section>

<section class="plain" id="install">
  <h2 class="serif">Three steps.</h2>
  <p class="lede">A folder with a SKILL.md and a Python script. No packages, no build. Prefer files? <a href="/skill" style="color:inherit">Download the .skill</a> or grab it on <a href="{REPO}" style="color:inherit">GitHub</a>.</p>
  <div class="steps">
    <div class="step"><h3 class="serif">1. Install</h3><p>One line. Puts the skill in your Claude Code skills folder.</p><pre>curl -fsSL gradient.skin/install | sh</pre></div>
    <div class="step"><h3 class="serif">2. Ask</h3><p>Describe the hero. Mention a palette, a brand colour, or nothing.</p><pre class="soft">/gradient-skin launch hero,
palette meadow, animated,
export OG + X images</pre></div>
    <div class="step"><h3 class="serif">3. Ship</h3><p>Get a responsive page, a CSS block for your codebase, an SVG, or PNGs.</p><pre>hero.html
skin.css
og.png
hero-x.png</pre></div>
  </div>
</section>
<footer class="mono">GRADIENT.SKIN · A CLAUDE CODE SKILL · <a href="{REPO}">github.com/rahulsingh2312/gradient-skills</a></footer>
<script>
(function(){{
  var hero=document.getElementById('hero'), grip=hero.querySelector('.grip'), cut=92, touched=false, raf;
  function set(v){{ cut=Math.max(0,Math.min(100,v)); hero.style.setProperty('--cut',cut+'%'); grip.setAttribute('aria-valuenow',Math.round(cut)); hero.dataset.cut=cut<=0.5?'0':cut>=99.5?'100':''; }}
  // 1.2 s pause, then the good skin sweeps across and becomes the whole background
  var reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
  if(reduce){{ set(0); hero.classList.add('settled'); }}
  else {{
    var t0=null, from=92, dur=2600, delay=1200;
    (function tick(now){{ if(touched) return; if(t0===null) t0=now; var t=(now-t0-delay)/dur; if(t<0){{raf=requestAnimationFrame(tick);return;}}
      var e=t>=1?1:1-Math.pow(1-t,3); set(from*(1-e)); if(t<1) raf=requestAnimationFrame(tick); else hero.classList.add('settled'); }})(performance.now());
  }}
  // drag the grip
  var dragging=false;
  function pos(e){{ var r=hero.getBoundingClientRect(); return (e.clientX-r.left)/r.width*100; }}
  grip.addEventListener('pointerdown',function(e){{ touched=true; cancelAnimationFrame(raf); hero.classList.add('settled'); dragging=true; grip.setPointerCapture(e.pointerId); set(pos(e)); e.preventDefault(); }});
  grip.addEventListener('pointermove',function(e){{ if(dragging) set(pos(e)); }});
  grip.addEventListener('pointerup',function(){{ dragging=false; }}); grip.addEventListener('pointercancel',function(){{ dragging=false; }});
  grip.addEventListener('keydown',function(e){{ var d=e.key==='ArrowLeft'?-4:e.key==='ArrowRight'?4:0; if(d){{ touched=true; cancelAnimationFrame(raf); set(cut+d); e.preventDefault(); }} }});
  // copy buttons (both layers)
  document.querySelectorAll('[data-copy]').forEach(function(b){{ b.addEventListener('click',function(){{ navigator.clipboard.writeText('curl -fsSL gradient.skin/install | sh'); document.querySelectorAll('[data-copy] small').forEach(function(s){{s.textContent='copied';}}); }}); }});
}})();
</script>
</body></html>'''
open(os.path.join(HERE, "index.html"), "w").write(html)
import shutil
src = os.path.join(HERE, "..", "gradient-skin.skill")
if os.path.exists(src): shutil.copy(src, os.path.join(HERE, "gradient-skin.skill"))
print("wrote site/index.html", len(html), "bytes")
