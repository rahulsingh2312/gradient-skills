# gradient-skills

Claude Code skills for gradients. Currently one: **Haze**.

<p align="center"><img src="launch/images/hero-x.png" width="800" alt="Haze hero"></p>

## Haze

Soft pastel "mesh" gradient backgrounds and editorial hero sections: blurred colour blobs, a white
light-leak, a faint dot grid, optional grain, and serif display type with an italic second line.
One prompt gives you HTML, CSS, SVG, or PNG.

<p align="center"><img src="launch/images/palettes.png" width="800" alt="Seven palettes"></p>

### Install

```bash
git clone https://github.com/rahulsingh2312/gradient-skills
cp -r gradient-skills/haze ~/.claude/skills/haze        # personal
# or: cp -r gradient-skills/haze .claude/skills/haze     # per project
```

Or drop `haze.skill` from this repo into Claude (the file card shows a **Save skill** button).

Then in Claude Code:

```
/haze launch hero for Acme, brand #5B4BFF, a bit punchier, export OG + X images
```

### Use the script directly

```bash
python3 haze/scripts/haze.py --palette sorbet --seed 4 --headline "Launch" --italic "day." --out og.png
python3 haze/scripts/haze.py --blank --palette dusk --format css   # CSS to stdout
python3 haze/scripts/haze.py --responsive --out hero.html          # standalone page
```

Pure standard-library Python. PNG export needs Node + Playwright once:
`npm i -g playwright && npx playwright install chromium`. HTML, CSS, and SVG need nothing.

Palettes: `dawn` `sorbet` `glacier` `dusk` `meadow` `ember` `ink` (dark), or `--colors` with your own.
Layouts: `split` `corners` `wash` `halo`. See `haze/SKILL.md` for the full set of flags and the design
rules, `haze/references/recipe.md` for hand-writing it into React/Tailwind.

### Repo layout

```
haze/            the skill (SKILL.md, scripts/, references/, assets/fonts/)
haze.skill       packaged skill, importable into Claude
launch/          X posts, domain shortlist, launch images and the spec that made them
site/            single-file landing page (index.html + og.png), deploy anywhere static
```

## License

MIT for the code and docs. Bundled fonts (Instrument Serif, Inter, JetBrains Mono) are under the
SIL Open Font License, see `haze/assets/fonts/OFL.txt`.
