#!/usr/bin/env python3
"""Sat Oct 10 one-stop shop: three photos from this morning as a 4:5
carousel pushing Sunday. Blurs the handwritten names and addresses.

    python3 private/instagram-launch/source-files/weekend/make_today.py
"""
import pathlib
from PIL import Image, ImageFilter, ImageOps

HERE = pathlib.Path(__file__).resolve().parent
RAW, OUT = HERE / "raw", HERE / "out"


def load(name):
    return ImageOps.exif_transpose(Image.open(RAW / name)).convert("RGB")


def blur(im, boxes):
    """boxes as fractions (x0, y0, x1, y1) of the whole image; soft-edged so it reads as focus, not a sticker."""
    from PIL import ImageDraw
    soft = im.filter(ImageFilter.GaussianBlur(45))
    mask = Image.new("L", im.size, 0)
    d = ImageDraw.Draw(mask)
    for x0, y0, x1, y1 in boxes:
        d.rounded_rectangle((x0 * im.width, y0 * im.height, x1 * im.width, y1 * im.height), radius=120, fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(60))
    return Image.composite(soft, im, mask)


def crop45(im, cx, cy):
    """Largest 4:5 window, centred as near (cx, cy) as the frame allows."""
    w = min(im.width, round(im.height * 4 / 5))
    h = round(w * 5 / 4)
    l = min(max(round(im.width * cx - w / 2), 0), im.width - w)
    t = min(max(round(im.height * cy - h / 2), 0), im.height - h)
    return im.crop((l, t, l + w, t + h)).resize((1080, 1350), Image.LANCZOS)


crop45(load("IMG_4641.jpg"), 0.38, 0.5).save(OUT / "sat-1-painting.jpg", quality=92)
crop45(load("IMG_4643.jpg"), 0.55, 0.6).save(OUT / "sat-2-table.jpg", quality=92)

# Envelope area is the bottom 45% of the frame; boxes below are in its coordinates.
def env(x0, y0, x1, y1):
    return (x0, 0.55 + 0.45 * y0, x1, 0.55 + 0.45 * y1)

notes = blur(load("IMG_4642.jpg"), [env(-0.03, 0.1, 0.3, 0.66), env(0.47, 0.36, 0.93, 1.05)])
crop45(notes, 0.5, 0.5).save(OUT / "sat-3-notes.jpg", quality=92)
print("ok")


def square(im, x0, y0):
    """Largest square, its top-left at (x0, y0) as fractions, clamped to the frame."""
    side = min(im.size)
    l = min(round(im.width * x0), im.width - side)
    t = min(round(im.height * y0), im.height - side)
    return im.crop((l, t, l + side, t + side)).resize((1080, 1080), Image.LANCZOS)


# Mon Oct 12 weekend recap: Sunday's crowd first, then Saturday's three. Square,
# because Sunday's wide shot can't go 4:5 without cutting people off.
def smiley(im, faces):
    """Cover each (cx, cy, size) face with a smiling-face emoji. Used for kids we have no release for."""
    from PIL import ImageDraw, ImageFont
    f = ImageFont.truetype("/System/Library/Fonts/Apple Color Emoji.ttc", 160)
    glyph = Image.new("RGBA", (180, 180), (0, 0, 0, 0))
    ImageDraw.Draw(glyph).text((10, 10), "\U0001F60A", font=f, embedded_color=True)
    glyph = glyph.crop(glyph.getbbox())
    for cx, cy, size in faces:
        g = glyph.resize((size, size), Image.LANCZOS)
        im.paste(g, (cx - size // 2, cy - size // 2), g)
    return im


sunday = square(load("IMG_8080.jpeg"), 0.185, 0)
smiley(sunday, [(479, 487, 104), (1066, 539, 76)]).save(OUT / "mon-1-sunday.jpg", quality=92)
square(load("IMG_4641.jpg"), 0.12, 0).save(OUT / "mon-2-painting.jpg", quality=92)
square(load("IMG_4643.jpg"), 0, 0.2).save(OUT / "mon-3-table.jpg", quality=92)
square(notes, 0, 0.06).save(OUT / "mon-4-notes.jpg", quality=92)
