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
| `images/article-two-tweets.png` | 1600×900 — the "their post → ours" image inside the article |
| `compose.py` | rebuilds that image with the real post pasted in |

Regenerate after editing `hero.json`:

```bash
python3 gradient-skin/scripts/skin.py --spec launch/hero.json --size 1600x900 --out launch/images/hero-x.png
python3 gradient-skin/scripts/skin.py --spec launch/hero.json --size 1200x630 --out launch/images/og.png
```

## The two-post image

The post the article opens with is https://x.com/ryandavogel/status/1956365206147244167. X blocks
downloads from here, so screenshot it yourself and pass the file:

```bash
python3 launch/compose.py --shot ~/Downloads/ryan.png              # side by side
python3 launch/compose.py --shot ~/Downloads/ryan.png --layout stacked   # theirs on top, ours below
python3 launch/compose.py                                          # no screenshot: quoted card + permalink
```

In the article itself, paste that URL on its own line so X renders the real post as an embed, then put
the image under it.

## Article covers (`images/covers/`)

Each variant comes as a 16:9 `-card.png` (timeline card, quote posts) and a 1920×368 `-banner.png`
(the banner X shows inside the article). `article-thumb.png` and `article-banner.png` are the defaults: the crossed-out swatch vs ours. The same art is `og.png`, `hero-x.png` and `square.png`.

| variant | angle |
|---|---|
| `wipe70` | the hero mid-wipe, ours winning 70/30. |
| `crossed` | template swatch crossed out, ours ticked, big headline. Default everywhere. |
| `111k` | the hook from the article opening. Use for the carry post if you lead with the viral tweet. |
| `tweet` | a riff on the "worst code ever generated" format, from the brand's own account. |
| `taste` | "Taste you can install" with the install line and three palettes. For day-2 posts. |
| `dark` | ink palette version of `crossed`, for contrast in a light feed. |
