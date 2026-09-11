#!/usr/bin/env python3
"""Generate every derived brand raster in assets/ from branding/yes-on-4a/.

The campaign supplied four logo lockups (horizontal/stacked x light/dark
ground) as transparent PNGs plus Illustrator masters. Everything the site
serves is DERIVED here — never hand-cropped — so a new logo drop is one
file swap plus one command:

    python3 tools/render_brand_assets.py

Produces:
  assets/yes-on-4a-logo.png        header lockup, light ground (trimmed)
  assets/yes-on-4a-logo-dark.png   header lockup, dark ground (trimmed)
  assets/favicon-32.png            tab icon, solid paper ground
  assets/favicon-32-dark.png       tab icon, solid ink ground
  assets/apple-touch-icon.png      180x180, solid paper (iOS rounds it)
  assets/icon-192.png              PWA, solid paper
  assets/icon-512.png              PWA, solid paper
  assets/icon-512-maskable.png     PWA maskable; mark inset to the safe zone

The icon mark is the graduation cap + figure + star cropped off the top of
the STACKED lockup at the blank row band between the cap and the wordmark
(found by scanning, not hardcoded, so a re-drawn logo still works). The
full wordmark is unreadable below ~96px, which is why the icons use the
mark alone.
"""

import pathlib
import sys

try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow required:  python3 -m pip install Pillow")

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "branding" / "yes-on-4a"
OUT = ROOT / "assets"

# Grounds from css/styles.css :root — keep in lockstep.
PAPER = (251, 250, 247, 255)   # --paper  #FBFAF7
INK = (25, 29, 32, 255)        # dark-mode --paper  #191D20


def trim(im):
    """Crop to the alpha bounding box."""
    box = im.getchannel("A").getbbox()
    return im.crop(box) if box else im


def icon_mark(path):
    """The cap+figure+star: everything above the blank band that separates
    the mark from the wordmark in the stacked lockup."""
    im = Image.open(path).convert("RGBA")
    alpha = im.getchannel("A")
    w, h = im.size
    rows = [
        any(alpha.getpixel((x, y)) > 8 for x in range(0, w, 2))
        for y in range(h)
    ]
    filled = [y for y, on in enumerate(rows) if on]
    if not filled:
        sys.exit(f"{path.name}: no content")
    top, bottom = filled[0], filled[-1]

    gap_start = None
    best = None
    for y in range(top, bottom + 1):
        if not rows[y]:
            gap_start = y if gap_start is None else gap_start
        elif gap_start is not None:
            run = y - gap_start
            if run >= 5 and best is None:      # first real gap = under the cap
                best = gap_start
            gap_start = None
    if best is None:
        sys.exit(f"{path.name}: no gap between mark and wordmark")
    return trim(im.crop((0, 0, w, best)))


CHARCOAL = (49, 62, 73)
GREEN = (144, 202, 101)
WHITE = (255, 255, 255)


def reverse_ink(im):
    """The designer's own dark-ground treatment, applied to a lockup that
    was only supplied light: charcoal -> green, green -> white.

    That mapping is not invented. Comparing the supplied light and dark
    tagline lockups shows the ink swaps exactly, with matching pixel
    counts (29212/4394 light vs 28694/4809 dark). `verify_reverse()`
    re-derives the supplied dark file from the light one and fails the
    build if the mapping ever stops matching."""
    import numpy as np
    a = np.array(im.convert("RGBA")).astype(np.int16)
    rgb, alpha = a[..., :3], a[..., 3]
    d_char = np.abs(rgb - np.array(CHARCOAL)).sum(axis=-1)
    d_green = np.abs(rgb - np.array(GREEN)).sum(axis=-1)
    out = a.copy()
    ink = alpha > 0
    out[..., :3] = np.where(
        ((d_char <= d_green) & ink)[..., None], np.array(GREEN), np.array(WHITE)
    )
    out[..., 3] = alpha
    return Image.fromarray(out.astype("uint8"), "RGBA")


def verify_reverse():
    """Check the CLAIM behind reverse_ink, not a pixel diff.

    The claim is that the designer's dark treatment swaps the two inks:
    charcoal -> green, green -> white. So the light lockup's
    charcoal:green ink ratio must equal the dark lockup's green:white
    ratio. Comparing ratios instead of pixels is deliberate — the two
    supplied files differ by a pixel in height, so any aligned diff
    reports ~5% edge noise that says nothing about the mapping.
    """
    import numpy as np

    def inks(path):
        a = np.array(trim(Image.open(path).convert("RGBA"))).astype(np.int16)
        solid = a[..., 3] > 250
        rgb = a[..., :3][solid]
        near = lambda c: int((np.abs(rgb - np.array(c)).sum(-1) < 30).sum())
        return near(CHARCOAL), near(GREEN), near(WHITE)

    l_char, l_green, _ = inks(SRC / "horizontal-tagline-light.png")
    _, d_green, d_white = inks(SRC / "horizontal-tagline-dark.png")
    if min(l_char, l_green, d_green, d_white) == 0:
        sys.exit("verify_reverse: expected inks missing from a supplied lockup")
    light_ratio = l_char / l_green
    dark_ratio = d_green / d_white
    drift = abs(light_ratio - dark_ratio) / light_ratio
    if drift > 0.15:
        sys.exit(
            f"reverse_ink no longer matches the designer's dark treatment "
            f"(light charcoal:green {light_ratio:.2f} vs dark green:white "
            f"{dark_ratio:.2f}, {drift:.0%} drift). Ask for a tagline-free "
            f"dark file instead of deriving one."
        )
    return f"ink ratios agree within {drift:.1%}"


def on_ground(mark, size, ground, inset=1.0):
    """Square canvas of `ground` with `mark` centered, scaled to `inset`."""
    canvas = Image.new("RGBA", (size, size), ground)
    target = max(1, int(size * inset))
    scale = min(target / mark.width, target / mark.height)
    m = mark.resize(
        (max(1, round(mark.width * scale)), max(1, round(mark.height * scale))),
        Image.LANCZOS,
    )
    canvas.alpha_composite(m, ((size - m.width) // 2, (size - m.height) // 2))
    return canvas.convert("RGB")


def main():
    if not SRC.is_dir():
        sys.exit(f"missing {SRC.relative_to(ROOT)}")
    OUT.mkdir(exist_ok=True)
    wrote = []

    # Header lockups — trimmed so CSS `height` controls real ink, not padding.
    # `yes-on-4a-wordmark.png` is the tagline-free lockup: at profile-picture
    # size the tagline is unreadable and reads as clutter, so the badge uses
    # this one. Everything else keeps the tagline.
    for src, dest in [
        ("horizontal-tagline-light.png", "yes-on-4a-logo.png"),
        ("horizontal-tagline-dark.png", "yes-on-4a-logo-dark.png"),
        ("facebook-header.png", "yes-on-4a-wordmark.png"),
    ]:
        im = trim(Image.open(SRC / src).convert("RGBA"))
        im.save(OUT / dest, optimize=True)
        wrote.append(f"{dest}  {im.width}x{im.height}")

    # Reversed wordmark for the green-band frame design.
    rev = reverse_ink(trim(Image.open(SRC / "facebook-header.png").convert("RGBA")))
    rev.save(OUT / "yes-on-4a-wordmark-reversed.png", optimize=True)
    wrote.append(f"yes-on-4a-wordmark-reversed.png  {rev.width}x{rev.height}  [{verify_reverse()}]")

    light = icon_mark(SRC / "stacked-light.png")
    dark = icon_mark(SRC / "stacked-dark.png")

    # Solid grounds: a transparent favicon disappears into a themed tab strip.
    for name, mark, ground, size, inset in [
        ("favicon-32.png", light, PAPER, 32, 1.0),
        ("favicon-32-dark.png", dark, INK, 32, 1.0),
        ("apple-touch-icon.png", light, PAPER, 180, 0.82),
        ("icon-192.png", light, PAPER, 192, 0.86),
        ("icon-512.png", light, PAPER, 512, 0.86),
        # Maskable: launchers crop to a circle; keep the mark inside the
        # inner 80% safe zone or the star loses its points.
        ("icon-512-maskable.png", light, PAPER, 512, 0.60),
    ]:
        on_ground(mark, size, ground, inset).save(OUT / name, optimize=True)
        wrote.append(f"{name}  {size}x{size}")

    for line in wrote:
        print("  wrote assets/" + line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
