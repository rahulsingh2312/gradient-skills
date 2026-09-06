# gradient.skin — X launch copy

Everything below is ready to paste. Pick one main post, attach the image named next to it, and post the
thread as replies to yourself. Swap `<link>` for the GitHub URL (or the domain once you have one).

Voice rules used throughout: no hashtags, no "excited to announce", no emoji walls, one idea per post,
the image does the selling. Lowercase is fine on X; the serif in the image carries the polish.

---

## Main post (pick ONE)

**A — the flex** · image: `images/hero-x.png`

> i got tired of hand-tuning radial gradients to get that soft "light on paper" look every good landing page has right now
>
> so i turned it into a Claude Code skill. one prompt → hero page, css, svg, or png
>
> it's called gradient.skin. open source. <link>

**B — the demo** · image: `images/one-prompt.png`

> `/gradient-skin launch hero, palette meadow, animated, export OG + X images`
>
> that's the whole workflow now. Claude Code skill, free, link below

**C — the contrarian** · image: `images/hero-x.png`

> every "beautiful" landing page in 2026 is the same 4 things:
> pastel mesh gradient, dot grid, one serif headline, an italic second line
>
> so i made it a one-liner. /gradient-skin. steal it. <link>

**D — the short one** · image: `images/hero-x.png`

> made a Claude Code skill that generates these. free. <link>

---

## Thread (reply to the main post, in order)

**2/** · image: `images/palettes.png`

> twenty-one palettes built in, sixteen light and five dark, and every one has a dark twin.
> or give it your brand hex and it derives one. `--from-brand` does the rest

**3/** · image: `images/one-prompt.png`

> it doesn't just make a picture. same prompt gives you:
> • a responsive hero page (html)
> • a css block for your existing codebase (tailwind + react snippets included)
> • svg if you have no browser around
> • png for OG / X / wallpapers

**4/** · no image, or a screenshot of your terminal

> install:
> ```
> curl -fsSL gradient.skin/install | sh
> ```
> then in Claude Code: `/gradient-skin make me a hero for <your product>`
> png export needs playwright (`npm i -g playwright && npx playwright install chromium`), html/css/svg need nothing

**5/**

> the part i'm proudest of is the SKILL.md. it explains *why* the look works — blob size, the white light-leak, why pure black kills it, why the dot grid should be almost invisible — so Claude can bend it without breaking it. not a template, a taste

**6/** · image: `images/wallpaper.png`

> also makes a decent wallpaper. 2560x1440 in the repo if you want it

**7/**

> repo: <link>
> if you build something with it, reply with a screenshot — i'll RT the good ones

---

## Alt hooks (for a second post 2–3 days later, or if the first one flops)

- "designers spend 40 minutes on this gradient. it's now 4 seconds and a slash command"
- "the gradient from every YC landing page, as a Claude Code skill"
- "you know the one. mint on the left, gold on the right, dot grid, serif. now it's `/gradient-skin`"
- "i reverse-engineered the pastel mesh gradient look and put it in a skill so i never have to do it again"
- "stop screenshotting linear's hero for reference. run /gradient-skin"

## Reply-guy answers (have these ready)

- *"isn't this just css radial gradients?"* → "yes, nine of them, in the right order, with the right falloffs, and a light-leak where the text goes. the point is not having to find that by hand every time"
- *"why not a figma plugin?"* → "because you also want the css. figma gives you a png; this gives you the css, the html, and the png from the same words"
- *"does it work with Cursor / other agents?"* → "it's a folder with a SKILL.md and a python script. anything that reads markdown and runs python can use it"
- *"dark mode?"* → "`--palette ink`" + attach the ink tile

## Quote posts

### Quoting the 111K gradient post

Quote https://x.com/ryandavogel/status/1956365206147244167 — it is the reference everyone already
knows, and quoting is friendlier than screenshotting. Credit, never dunk: the joke is the model's
default taste, not the person who posted it.

**A — the answer** · image: `images/article-two-tweets.png`

> the reason every model writes this exact gradient is that nobody ever told it what the good ones do
> differently. turns out it's six rules, mostly about lightness. i put them in a claude code skill

**B — the diagnosis** · no image, let the quote carry it

> this is the most recognisable image in software right now and there's no code in it
>
> the fix isn't "less gradient", it's lightness above 82% and one white patch where the headline goes.
> wrote up why: <article link>

**C — the short one** · image: `images/hero-x.png`

> fixed it. one prompt, free skill → gradient.skin

**D — the receipt** · image: `images/covers/crossed-card.png`

> left: what every model reaches for. right: same nine radial gradients with the lightness fixed.
> one prompt apart. gradient.skin

### Quoting your own launch post when the article goes live

> wrote the long version of this — the six rules, why the white light-leak does most of the work, and
> what breaks when you push saturation
>
> <article link>

### When someone posts a result

> this is what gradient.skin looks like in someone else's hands. 10/10 palette choice <quote>

### Day 3, if it has legs

> <n> installs since tuesday. the most used palette is meadow, which surprised me — i built the whole
> thing around dawn <quote your launch post>

---

## Posts that carry the article

The article card renders under the post, so the text has to earn the click on its own. First two
lines are what shows in the timeline.

**A — the number** · cover does the work

> 111,000 people laughed at a screenshot of a gradient last month. they all recognised it instantly
>
> i spent a weekend figuring out why the good landing pages look different, then turned it into a
> slash command. the rules are in here, free to steal

**B — the rules teaser**

> six things separate the AI gradient from the linear/arc one:
>
> lightness above 82%. blobs at half the canvas. one white patch behind the headline. a dot grid you
> can barely see. near-black text, never pure. no borders anywhere
>
> the long version:

**C — the flat one**

> not that gradient.
>
> (an article about why every model writes the same blue-to-pink, and the six rules the good pages
> follow instead)

**D — the builder angle**

> i wrote down why a gradient looks expensive, then made it a claude code skill so i never have to
> think about it again. both are in here — the reasoning first, the one-line install at the end

**Reply under whichever you post** · image: `images/one-prompt.png`

> the whole thing is one line:
> ```
> curl -fsSL gradient.skin/install | sh
> ```
> then `/gradient-skin make me a hero, palette meadow`

## Timing

- Post Tue–Thu, 8–10am PT (US design/dev crowd) or 6–8pm IST if your audience is India-heavy.
- Reply to your own post within 5 minutes with 2/ — the algorithm reads early replies as engagement.
- Don't edit the post after 10 minutes; edits reset distribution on some clients.
- Pin it for a week.

## Who to tag (in a reply, not the main post)

People who amplify Claude Code skills and design-dev crossover: the Claude Code / Anthropic devrel
accounts, whoever runs the "skills" directory you list it in, and 2–3 design-engineer accounts whose
launch pages use this look. Tagging in the main post reads as begging; in a reply it reads as credit.
