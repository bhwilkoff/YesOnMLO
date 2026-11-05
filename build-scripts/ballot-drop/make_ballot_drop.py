#!/usr/bin/env python3
"""Ben's Oct 7 ballot drop at Goodson Rec Center: unfiltered 4:5 feed crops
and Classic-style Stories (black on a white highlight), same look as the
one-stop-shop Stories.

    python3 private/instagram-launch/source-files/ballot-drop/make_ballot_drop.py

Facts on these images come from the photos themselves (the box's own
labels, the envelope) and the drop-location insert mailed with the ballot.
"""
import pathlib
from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = pathlib.Path(__file__).resolve().parent
FULL = HERE / "full"
OUT = HERE / "out"
FONT = "/System/Library/Fonts/Helvetica.ttc"


def font(size):
    return ImageFont.truetype(FONT, size, index=1)


def load(name):
    return ImageOps.exif_transpose(Image.open(FULL / f"IMG_{name}.jpeg")).convert("RGB")


def crop(im, w, h, fx=0.5, fy=0.5):
    """Scale to cover w x h, then crop around the focal point (fx, fy)."""
    s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = min(max(round(im.width * fx - w / 2), 0), im.width - w)
    y = min(max(round(im.height * fy - h / 2), 0), im.height - h)
    return im.crop((x, y, x + w, y + h))


def block(draw, lines, top, size, pad_x=18, pad_y=8):
    f = font(size)
    asc, desc = f.getmetrics()
    h = asc + desc
    y = top
    for line in lines:
        if not line:
            y += h // 2
            continue
        w = draw.textlength(line, font=f)
        x = (1080 - w) / 2
        draw.rounded_rectangle((x - pad_x, y - pad_y, x + w + pad_x, y + h + pad_y), radius=14, fill="white")
        draw.text((x, y), line, font=f, fill="black")
        y += h + 2 * pad_y + 2


def feed(name, out, fx=0.5, fy=0.5):
    crop(load(name), 1080, 1350, fx, fy).save(OUT / out, quality=92)
    print(out)


def story(name, out, blocks, fx=0.5, fy=0.5):
    im = crop(load(name), 1080, 1920, fx, fy)
    d = ImageDraw.Draw(im)
    for lines, top, size in blocks:
        block(d, lines, top, size)
    im.save(OUT / out, quality=92)
    print(out)


OUT.mkdir(exist_ok=True)

# Feed photos, unfiltered.
feed("6843", "feed-buttons.jpg", fy=0.45)
feed("6846", "feed-envelope-in-slot.jpg", fx=0.55, fy=0.4)
feed("6855", "feed-goodson-sign.jpg", fy=0.6)
feed("6858", "feed-sign-path.jpg", fx=0.55, fy=0.55)
feed("6853", "feed-sign-sculpture.jpg", fx=0.45, fy=0.55)
feed("6857", "feed-goodson-wide.jpg", fy=0.55)
feed("6845", "feed-box-closes-7pm.jpg", fx=0.45, fy=0.45)
feed("6844", "feed-box-front.jpg", fy=0.5)
feed("6850", "feed-hand-at-box.jpg", fx=0.45, fy=0.5)

# Stories.
story("6843", "story-i-voted.jpg", [
    (["I voted Wednesday."], 200, 64),
    (["Yes on 4A, the LPS", "mill levy override.", "", "Your ballot is probably on", "your kitchen counter,", "waiting for you."], 1420, 48),
], fx=0.5, fy=0.45)

story("6858", "story-follow-the-signs.jpg", [
    (["Follow the signs."], 200, 64),
    (["Find the drop box", "closest to you."], 1690, 52),
], fx=0.6)

story("6845", "story-the-box.jpg", [
    (["Open 24 hours.", "Watched by video.", "Closes 7 p.m. on Nov 3.", "Ballots only."], 1420, 52),
], fx=0.4)

story("6850", "story-mine-is-in.jpg", [
    (["Mine's in.", "Is yours?"], 200, 64),
], fx=0.45)

# A sign with no location in frame: Goodson is a drop box, not a service center.
story("6854", "story-vspc-open.jpg", [
    (["Voter Service Centers", "open today."], 180, 60),
    (["Lost your ballot? Never got one?", "Go in. They'll fix it.", "", "Mon to Fri, 8 a.m. to 5 p.m."], 1300, 46),
], fx=0.5)
