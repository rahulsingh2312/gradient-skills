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
python3 haze/scripts/haze.py --spec launch/hero.json --size 1600x900 --out launch/images/hero-x.png
python3 haze/scripts/haze.py --spec launch/hero.json --size 1200x630 --out launch/images/og.png
```
