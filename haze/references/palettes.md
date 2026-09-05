# Haze palettes

Each palette is four *cool* colours, four *warm* colours, a base paper colour, a light-leak colour and an
ink colour. With `--layout split` the cool four sit on the left, the warm four on the right. Values are
in `scripts/haze.py` (`PALETTES`); this file says what they feel like and when to reach for them.

| name | cool → warm | feel | reach for it when |
|---|---|---|---|
| `dawn` | mint · sky · lavender · pink → cream · gold · peach · blush | the reference look; sunrise over paper | default; fintech, crypto, "serious but friendly" |
| `sorbet` | rose · raspberry · pink → apricot · lemon · peach | dessert, playful | consumer apps, creator tools, anything "fun" |
| `glacier` | mint · ice · lilac → near-white | cold, clean, quiet | dev tools, infra, security, minimal brands |
| `dusk` | lavender · violet · periwinkle → apricot · coral · rose | evening, romantic | wellness, lifestyle, AI assistants |
| `meadow` | sage · mint · sky → lemon · lime | fresh, outdoors | health, climate, food |
| `ember` | apricot · coral → honey · amber (all warm) | golden hour | hospitality, luxury, "gold leaf" |
| `ink` | deep teal · indigo → umber · plum on charcoal | dark mode aurora | dark UIs, gaming, crypto dashboards |

## From a brand colour

Given one brand hex (say `#5B4BFF`, an electric violet):

1. Convert to HSL. Keep the hue (≈ 246°).
2. Make the **anchor blob**: same hue, saturation 60–80%, lightness 84–88% → `#d6d0ff`.
3. Make three **cool neighbours** by rotating hue −40°, −80°, +25° at the same lightness →
   sky `#cfe1ff`, mint `#c8f4ec`, pink `#f0cdf5`.
4. Make four **warm** colours from the complementary side (hue +150…+200°), lightness 86–92% →
   cream `#f9efc6`, gold `#f2db95`, peach `#f8d6c0`, blush `#f8e2dc`. (Warm sides can be shared across
   brands — the cool side carries the identity.)
5. Base: the brand hue at 2–3% saturation, 96% lightness → `#f4f3f8`.
6. Ink: the brand hue at 20% saturation, 7% lightness → `#0f0e1a`.

```bash
python3 scripts/haze.py --colors "#d6d0ff,#cfe1ff,#c8f4ec,#f0cdf5,#f9efc6,#f2db95,#f8d6c0,#f8e2dc" --base "#f4f3f8"
```

Sanity checks: every colour ≥ 82% lightness; at least one hue jump ≥ 90° between the two sides; no two
adjacent blobs within 15° of each other unless the point is a monochrome wash.

## Quick HSL helper (Python, stdlib)

```python
import colorsys
def pastel(hex_color, dh=0, l=0.86, s=0.7):
    r,g,b = (int(hex_color.lstrip('#')[i:i+2],16)/255 for i in (0,2,4))
    h,_,_ = colorsys.rgb_to_hls(r,g,b)
    r,g,b = colorsys.hls_to_rgb((h + dh/360) % 1, l, s)
    return '#%02x%02x%02x' % tuple(int(round(v*255)) for v in (r,g,b))
brand = '#5B4BFF'
cool = [pastel(brand,0), pastel(brand,-40), pastel(brand,-80), pastel(brand,25)]
warm = [pastel(brand,160,.90,.8), pastel(brand,175,.78,.75), pastel(brand,195,.86), pastel(brand,185,.92,.6)]
print(','.join(cool+warm))
```
