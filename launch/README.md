# Launch kit

| file | use |
|---|---|
| `x-posts.md` | main post options, thread, alt hooks, reply answers, timing |
| `domains.md` | domain shortlist + recommendation |
| `hero.json` | the spec that generated every image below (edit + re-run to change copy) |
| `images/hero-x.png` | 1600×900 — main post image, X/Twitter card |
| `images/og.png` | 1200×630 — `og:image` for the landing page |
| `images/square.png` | 1080×1080 — Instagram / LinkedIn |
| `images/palettes.png` | 1600×900 — thread post 2 |
| `images/one-prompt.png` | 1600×900 — the "demo" post |
| `images/wallpaper.png` | 2560×1440 — giveaway |

Regenerate after editing `hero.json`:

```bash
python3 gradient-skin/scripts/skin.py --spec launch/hero.json --size 1600x900 --out launch/images/hero-x.png
python3 gradient-skin/scripts/skin.py --spec launch/hero.json --size 1200x630 --out launch/images/og.png
```

## Article covers (`images/covers/`)

Each variant comes as a 16:9 `-card.png` (timeline card, quote posts) and a 1920×368 `-banner.png`
(the banner X shows inside the article). `article-thumb.png` is the default: the 70/30 wipe.

| variant | angle |
|---|---|
| `wipe70` | the hero mid-wipe, ours winning 70/30. Default. |
| `crossed` | template swatch crossed out, ours ticked, big headline. Clearest at thumbnail size. |
| `111k` | the hook from the article opening. Use for the carry post if you lead with the viral tweet. |
| `tweet` | a riff on the "worst code ever generated" format, from the brand's own account. |
| `taste` | "Taste you can install" with the install line and three palettes. For day-2 posts. |
| `dark` | ink palette version of `crossed`, for contrast in a light feed. |
