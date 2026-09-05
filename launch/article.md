# X Article — paste-ready

**Cover:** upload `images/article-cover-x.png` (1920×768, sized for the article editor crop). Timeline card: `images/article-thumb.png`. Wide banner fallback: `images/article-banner.png`.
**Post text that carries the article** (pick one, the article card sits under it):

> A · 111,000 people laughed at a screenshot of a gradient last month. they all recognised it.
> i spent a weekend figuring out why the good ones look different, then made it a slash command. free.

> B · every AI ships the same blue-to-pink gradient. i wrote down the six rules the good landing pages follow and turned them into a Claude Code skill. one line to install.

> C · not that gradient. (article)

X shows the title, the cover, and roughly the first two lines of the body in the timeline. The first
two lines below are written for that preview.

---

## Title

Not that gradient.

## Subtitle

Every AI reaches for the same blue-to-pink. Here's why the good landing pages look like light instead, and the one-line skill that does it for you.

---

Last month a tweet with 111,000 views was just a screenshot of a gradient. Blue on the left, purple in the middle, pink on the right. The caption said "pov you are about to look at the worst code ever generated."

Nobody needed the code. Everyone already knew.

That gradient is the sound of an AI saying "make it look modern." It's in the Tailwind docs, it's in ten thousand tutorials, it's the first thing every model reaches for when nobody tells it what beautiful means. `from-blue-500 via-purple-500 to-pink-500`. You've shipped it. I've shipped it.

*[image: images/article-thumb.png]*

Meanwhile the landing pages people actually screenshot and send each other look nothing like that. Linear. Arc. Raycast. Half the good YC pages this year. Same trick every time: a sheet of near-white paper with soft pools of colour bleeding in from the edges, a dot grid you can barely see, one serif headline, second line in italic.

I wanted that for my own site. So I did what everyone does. Opened DevTools on a page I liked, copied nine radial gradients, and spent forty minutes moving numbers around until it stopped looking like a bruise.

Then I needed it again for an OG image. Then for a second product. Then a friend asked how I did it.

That's the point where a thing should stop being a trick and become a tool.

## Why yours looks like a bruise and theirs looks like light

The gradient itself is easy. Nine radial gradients stacked in one background. The hard part is that ninety percent of attempts look wrong, and for a while I couldn't say why. So I broke it on purpose until I could.

**The colours are barely colours.** Every blob sits above 82% lightness. None of them is loud. The contrast comes from temperature: cool hues on one side, warm on the other. The moment you push saturation it turns into 2012. This is the whole difference between the tweet gradient and the good ones. Same hues, wildly different lightness.

**The blobs are huge.** Each one spans 40 to 60 percent of the canvas and fades to nothing by two-thirds of its radius. Small blobs read as spots. Hard stops read as circles. Both kill the illusion that you're looking at light instead of paint.

**The white patch is the hero.** There's a big white ellipse where the headline goes and it's the brightest thing on the page. Text over colour looks like a poster. Text over that white leak looks like print. One layer. It's the "why does this feel expensive" layer.

**The grid is texture, not decoration.** Nine percent opacity, 22px apart, fading out at the edges. If you can count the dots it's too strong.

**Pure black text ruins it.** Near-black sits in the light. Pure black punches a hole in it.

**Nothing has a border.** Cards, shadows, outlines, all of them fight the softness. The one bordered thing is the small uppercase badge, and it earns it.

Six rules. Steal them. You don't need the skill to use them.

*[image: images/palettes.png]*

## So I wrote them down for Claude

A Claude Code skill is a folder with a SKILL.md and whatever scripts you want. The script is the boring part. The interesting part is that the markdown explains the six rules above and *why* they matter, so Claude can bend the look without breaking it.

Give it a brand colour and it derives a palette that keeps the temperature split. Ask for "softer" and it drops intensity before it touches the colours. Ask for dark mode and the dot grid flips to white on its own. Ask for "moving like water" and every blob gets its own slow drift.

The script underneath is plain Python, no packages, and it outputs whatever you actually need:

- a responsive hero page (HTML)
- a CSS block for the codebase you already have, plus Tailwind and React snippets
- an SVG if there's no browser around
- PNGs at any size, for OG images, X cards, wallpapers

Twenty palettes are built in, sixteen light and four dark, and any of them has a dark twin. Give it a brand colour and it derives one that keeps the temperature split.

*[image: images/one-prompt.png]*

## Using it

One line:

```
curl -fsSL gradient.skin/install | sh
```

Then, in Claude Code:

```
/gradient-skin launch hero, palette meadow, animated, export OG + X images
```

You get the page, the CSS, and the images from the same sentence. If you'd rather skip Claude, the script runs on its own and prints the CSS.

## The part I actually care about

A template gives you one result. A skill gives Claude taste in one narrow area, and taste generalises. The same six sentences produce a fintech hero, a wellness app, a dark dashboard header, and an OG image for a blog post. None of them look like each other. All of them look right.

I think this is what design tooling looks like for a while: not components, not templates. Small files that say "here's why this works, now go make a hundred of them."

Taste you can install.

## Get it

gradient.skin. Free, MIT, source on GitHub.

If you make something with it, reply with a screenshot. I'll share the good ones.

And if you hand-tuned one of these gradients last week: I'm sorry. You can stop now.
