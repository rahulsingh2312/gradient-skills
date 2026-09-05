# gradient-skills

Claude Code skills for gradients. Currently one: **gradient.skin**.

<p align="center"><img src="launch/images/hero-x.png" width="800" alt="gradient.skin hero"></p>

## gradient.skin

Soft pastel "mesh" gradient backgrounds and editorial hero sections: blurred colour blobs, a white
light-leak, a faint dot grid, optional grain, and serif display type with an italic second line.
One prompt gives you HTML, CSS, SVG, or PNG.

<p align="center"><img src="launch/images/palettes.png" width="800" alt="Seven palettes"></p>

### Install

```bash
git clone https://github.com/rahulsingh2312/gradient-skills
cp -r gradient-skills/gradient-skin ~/.claude/skills/gradient-skin        # personal
# or: cp -r gradient-skills/gradient-skin .claude/skills/gradient-skin     # per project
```

Or drop `gradient-skin.skill` from this repo into Claude (the file card shows a **Save skill** button).

Then in Claude Code:

```
/gradient-skin launch hero for Acme, brand #5B4BFF, a bit punchier, export OG + X images
```

### Use the script directly

```bash
python3 gradient-skin/scripts/skin.py --palette sorbet --seed 4 --headline "Launch" --italic "day." --out og.png
python3 gradient-skin/scripts/skin.py --blank --palette dusk --format css   # CSS to stdout
python3 gradient-skin/scripts/skin.py --responsive --out hero.html          # standalone page
```

Pure standard-library Python. PNG export needs Node + Playwright once:
`npm i -g playwright && npx playwright install chromium`. HTML, CSS, and SVG need nothing.

Palettes: `dawn` `sorbet` `glacier` `dusk` `meadow` `ember` `ink` (dark), or `--colors` with your own.
Add `--animate` and the blobs drift slowly, like light on water.
Layouts: `split` `corners` `wash` `halo`. See `gradient-skin/SKILL.md` for the full set of flags and the design
rules, `gradient-skin/references/recipe.md` for hand-writing it into React/Tailwind.

### Repo layout

```
gradient-skin/            the skill (SKILL.md, scripts/, references/, assets/fonts/)
gradient-skin.skill       packaged skill, importable into Claude
launch/          X posts, domain shortlist, launch images and the spec that made them
site/            landing page (index.html + og.png); `python3 site/build.py` regenerates it from the skill
```

## License

MIT for the code and docs. Bundled fonts (Instrument Serif, Inter, JetBrains Mono) are under the
SIL Open Font License, see `gradient-skin/assets/fonts/OFL.txt`.
