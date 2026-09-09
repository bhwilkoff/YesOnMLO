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
    for src, dest in [
        ("horizontal-tagline-light.png", "yes-on-4a-logo.png"),
        ("horizontal-tagline-dark.png", "yes-on-4a-logo-dark.png"),
    ]:
        im = trim(Image.open(SRC / src).convert("RGBA"))
        im.save(OUT / dest, optimize=True)
        wrote.append(f"{dest}  {im.width}x{im.height}")

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
