# X Article: paste-ready

**Cover image:** `images/article-thumb-before-after.png` (highest click-through) or `images/article-thumb-hook.png` (cleaner as a cover).
**Working name in this draft:** gradient.skin. Find-and-replace it if you pick something else.

---

## Title

I turned the internet's favourite gradient into a Claude Code skill

## Subtitle

The soft pastel "light on paper" look from every good landing page this year, reverse-engineered, written down, and made into one prompt. Free, open source.

---

Every landing page I liked this year had the same background.

Mint fading into lavender on the left. Cream fading into gold on the right. A bright white patch in the middle where the headline sits. A dot grid you can barely see. One serif headline, second line in italic. Linear had a version. So did Arc, Raycast, half of the YC batch, and every tasteful crypto project that wasn't trying to look like a casino.

I wanted it for my own site. So I did what everyone does: opened DevTools on a page I liked, copied nine radial gradients, and spent forty minutes moving numbers around until it stopped looking like a bruise.

Then I wanted it again for an OG image. Then for a second product. Then a friend asked how I did it.

That's the moment a thing should become a skill.

*[image: images/hero-x.png]*

## What I actually learned by copying it badly

The gradient itself is easy. Nine `radial-gradient()` layers stacked in `background-image`. The hard part is that ninety percent of attempts look wrong, and for a while I couldn't say why. Here's what I found by breaking it on purpose.

**The colours are barely colours.** Every blob is above 82% lightness. The contrast doesn't come from any single colour being loud. It comes from the temperature split: cool hues on one side, warm on the other. The moment you push saturation, it turns into a 2012 web gradient. Lift the lightness first, always.

**The blobs have to be huge.** Each ellipse spans 40 to 60 percent of the canvas and fades to nothing by about two-thirds of its radius. Smaller blobs read as spots. Harder stops read as circles. Both kill the illusion that you're looking at light instead of paint.

**The white patch is the hero.** There's a big white ellipse where the text goes, and it's the brightest thing on the page. Text over a wash of colour looks like a poster. Text over that white leak looks like print. This one thing is the difference between "nice gradient" and "why does this feel expensive."

**The dot grid is texture, not decoration.** Nine percent opacity, 22px pitch, fading out toward the edges. If you can count the dots, it's too strong.

**Pure black text ruins it.** Near-black, `#121212`, sits in the light. `#000` punches a hole in it.

**Nothing has a border except the pill.** Cards, shadows, outlines: all of them fight the softness. The one bordered element is the little uppercase badge, and it earns it.

*[image: images/palettes.png]*

## So I wrote it down for Claude

A Claude Code skill is just a folder with a `SKILL.md` and whatever scripts you want. The interesting part isn't the script. It's that the markdown file explains the six rules above, and *why* they matter, so Claude can bend the look without breaking it. Give it a brand colour and it derives a palette that keeps the temperature split. Ask for "softer" and it drops intensity before it touches the palette. Ask for dark mode and the dot grid flips to white by itself.

The script underneath is plain Python with no dependencies. It outputs whatever you actually need:

- an HTML hero page, responsive, with Google Fonts wired up
- a CSS block you paste into your existing codebase, plus Tailwind and React snippets
- an SVG if you don't have a browser around
- PNGs at any size, for OG images, X cards, or wallpapers

Seven palettes are built in. `dawn` is the reference look. `sorbet`, `glacier`, `dusk`, `meadow`, `ember` are variations on the same rules. `ink` is the dark version.

*[image: images/one-prompt.png]*

## What it looks like to use

Install is two lines:

```
git clone https://github.com/rahulsingh2312/gradient-skills
cp -r gradient-skills/gradient-skin ~/.claude/skills/gradient-skin
```

Then in Claude Code:

```
/gradient-skin launch hero for Acme, brand #5B4BFF, a bit punchier, export OG + X images
```

You get a hero page, the CSS, and two PNGs, all from the same words. If you want to skip Claude entirely, the script runs on its own:

```
python3 gradient-skin/scripts/gradient-skin.py --palette sorbet --seed 4 --headline "Launch" --italic "day." --out og.png
```

*[image: images/article-thumb-before-after.png]*

## Why bother making it a skill instead of a template

A template gives you one result. A skill gives Claude taste in one narrow area, and taste generalises. Once the rules are written down, the same six sentences produce a fintech hero, a wellness app, a dark-mode dashboard header, and an OG image for a blog post. None of them look like each other, and all of them look right.

I think this is what a lot of design skills will look like: not "here's a component," but "here's why this thing works, now go make a hundred of them."

## Get it

It's free and MIT licensed. The repo is at github.com/rahulsingh2312/gradient-skills. If you make something with it, reply with a screenshot. I'll share the good ones.

If you have a landing page that uses this look and you hand-tuned it: I'm sorry, and also, you can stop now.
