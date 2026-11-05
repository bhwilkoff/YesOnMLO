#!/usr/bin/env python3
"""LPS Memories, Oct 22-25: '80s yearbook photos (Classmates.com scans on the
Internet Archive, pages pulled into ../pages by pdftoppm at native 100 dpi).
Nostalgia is the hook; every post ends on why we keep funding LPS.

    python3 private/instagram-launch/source-files/yearbook-scans/tools/make_memories.py
"""
import pathlib
from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = pathlib.Path(__file__).resolve().parent.parent
ROOT = HERE.parents[3]
PAGES, OUT = HERE / "pages", HERE / "out"
OUT.mkdir(exist_ok=True)
for old in OUT.glob("*.jpg"):
    old.unlink()
FONT = "/System/Library/Fonts/Helvetica.ttc"
INK, GREEN, PAPER, EDGE = (57, 68, 74), (47, 107, 29), (244, 241, 233), (200, 196, 186)
YEARS = ["1988", "1997", "2002", "2004", "2010", "2013", "2018", "2020"]
DUE = "Ballots due by 7 p.m. Tuesday, Nov. 3"


def font(size, bold=True):
    return ImageFont.truetype(FONT, size, index=1 if bold else 0)


def crop(name, box):
    return Image.open(PAGES / f"{name}.jpg").convert("RGB").crop(box)


def fit(im, w, h):
    s = min(w / im.width, h / im.height)
    return ImageOps.expand(im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS), border=2, fill=EDGE)


def lines_at(d, lines, y, size, fill, bold=True, gap=12, W=1080):
    f = font(size, bold)
    asc, desc = f.getmetrics()
    for line in lines:
        w = d.textlength(line, font=f)
        assert w <= W - 100, f"too wide: {line}"
        d.text(((W - w) / 2, y), line, font=f, fill=fill)
        y += asc + desc + gap
    return y


def logo(width):
    lg = Image.open(ROOT / "branding/yes-on-4a/stacked-light.png").convert("RGBA")
    return lg.resize((width, round(lg.height * width / lg.width)), Image.LANCZOS)


MARK = logo(120)


def slide(scan, above, below=(), big=False, W=1080, H=1350, top=70, bottom_pad=140):
    """Yearbook photo on paper. `above` = headline lines, `below` = label/our line.
    The small Yes on 4A mark sits bottom-right so a single slide still says what it's for."""
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)
    y = lines_at(d, above, top, 64 if big else 46, INK, gap=12) + 20
    below_h = sum(56 for _ in below)
    shot = fit(scan, W - 80, H - y - below_h - bottom_pad - 40)
    im.paste(shot, ((W - shot.width) // 2, y))
    y = y + shot.height + 26
    for i, line in enumerate(below):
        y = lines_at(d, [line], y, 38 if (i == 0 and "School" in line) else 46, INK if (i == 0 and "School" in line) or "\u201c" in line or "\u201d" in line else GREEN, bold=not (i == 0 and "School" in line))
    assert y <= H - bottom_pad + 10, f"{above}: runs into the mark ({y})"
    im.paste(MARK, (W - MARK.width - 36, H - MARK.height - 30), MARK)
    return im


def end_card(lead, middle, years=False, W=1080, H=1350):
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)
    y = lines_at(d, lead, 120, 58, INK, gap=14)
    if years:
        f = font(50)
        y += 36
        for row in (YEARS[:4], YEARS[4:]):
            txt = "   ".join(row)
            d.text(((W - d.textlength(txt, font=f)) / 2, y), txt, font=f, fill=GREEN)
            y += 72
    y = lines_at(d, middle, y + 40, 50, GREEN, gap=12)
    lg = logo(330)
    im.paste(lg, ((W - lg.width) // 2, y + 50), lg)
    y = lines_at(d, ["Now it's our turn."], y + 50 + lg.height + 40, 62, INK)
    y = lines_at(d, ["4A, the LPS mill levy override", DUE], y + 6, 38, INK, bold=False, gap=8)
    assert y <= H - 40, f"end card overflows ({y})"
    return im


def save(slides, stem):
    for i, im in enumerate(slides, 1):
        im.save(OUT / f"{stem}-{i}.jpg", quality=92)
    thumbs = [im.resize((270, 338)) for im in slides]
    sheet = Image.new("RGB", (270 * len(thumbs), 338), "white")
    for i, t in enumerate(thumbs):
        sheet.paste(t, (i * 270, 0))
    sheet.save(OUT / f"check-{stem}.jpg")


GASPAR = crop("1984-90", (495, 175, 1089, 902))
QUALLS = crop("1984-85", (0, 0, 668, 1030))
HARDY = crop("1984-93", (11, 0, 660, 1023))
LAB = crop("1981-29", (33, 660, 715, 1111))
LIBRARY = crop("1981-15", (30, 70, 1096, 910))

teachers = [
    slide(GASPAR, ["Who was your favorite", "LPS teacher?"], ["Littleton High School, 1984",
          "The best ones made you want to show up."], big=True),
    slide(QUALLS, ["Littleton High School, 1984"], [
          "Who believed in you before you did?"]),
    slide(LAB, ["Heritage High School, 1981"], ["Somebody taught them to look closer."]),
    slide(LIBRARY, ["Heritage High School, 1981"], ["What did you learn here", "that you still use today?"]),
    end_card(["This community paid", "those teachers.", "It still does."],
             ["Today, LPS teachers are working", "under a wage freeze.", "4A lifts it: a 2% average raise."]),
]
save(teachers, "teachers")

slide(HARDY, ["In 1984, Mr. Hardy was asked what", "computers would be like in 2000."],
      ["\u201cHouses will probably be", "run by computers.\u201d",
       "Great teachers get kids ready for", "a future nobody can see yet.", "4A keeps that going."]).save(OUT / "hardy-feed.jpg", quality=92)

KING = crop("1984-17", (0, 95, 545, 980))
PARADE = crop("1982-22", (400, 750, 1100, 1270))
FLOAT = crop("1984-20", (75, 540, 460, 965))
BAND = crop("1984-16", (0, 505, 735, 905))
EAGLES = crop("1981-14", (580, 766, 1076, 1130))
CROWD = crop("1973-6", (0, 0, 1100, 1156))

homecoming = [
    slide(KING, ["Remember homecoming?"], ["Littleton High School, 1984", "Who were you with that night?"], big=True),
    slide(FLOAT, ["Littleton High School, 1984"], ["What did you build with your friends?"]),
    slide(BAND, ["Littleton High School, 1984"], ["Somebody taught every one of those notes."]),
    slide(EAGLES, ["Heritage High School, 1981"], ["Who would you tag from this crowd?"]),
    slide(CROWD, ["Arapahoe High School, 1973"], ["Today's kids deserve this feeling too."]),
    end_card(["Somebody paid for all of it:", "the teachers, the coaches,", "the band directors."],
             ["Today's LPS kids deserve", "the same."]),
]
save(homecoming, "homecoming")


def every_time(W, H, out):
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)
    top = 290 if H > 1400 else 60
    y = lines_at(d, ["Littleton Boulevard, 1982"], top, 46, INK, W=W)
    shot = fit(PARADE, W - 80, 470)
    im.paste(shot, ((W - shot.width) // 2, y + 20))
    y = lines_at(d, ["A whole town, showing up.", "That's what a yes vote is too."], y + 20 + shot.height + 22, 44, GREEN, gap=8, W=W)
    y = lines_at(d, ["Since 1988, every time LPS", "has asked, voters said yes."], y + 30, 52, INK, gap=10, W=W)
    f = font(48)
    y += 20
    for row in (YEARS[:4], YEARS[4:]):
        txt = "   ".join(row)
        d.text(((W - d.textlength(txt, font=f)) / 2, y), txt, font=f, fill=GREEN)
        y += 66
    y = lines_at(d, ["Now it's our turn."], y + 20, 60, INK, W=W)
    y = lines_at(d, ["4A, the LPS mill levy override"], y + 4, 38, INK, bold=False, W=W)
    assert y <= (H - 480 if H > 1400 else H - 40), f"{out} overflows ({y})"
    im.save(OUT / out, quality=92)


every_time(1080, 1350, "every-time-feed.jpg")


def story(scan, lines, sticker_note_room, out, label):
    W, H = 1080, 1920
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)
    y = lines_at(d, [label], 290, 42, INK, W=W) + 20
    shot = fit(scan, W - 80, 560)
    im.paste(shot, ((W - shot.width) // 2, y))
    y = lines_at(d, lines, y + shot.height + 50, 60, INK, gap=14, W=W)
    assert y + sticker_note_room <= H - 480, f"{out}: no room for the sticker"
    im.paste(MARK, (W - MARK.width - 40, H - 480 - MARK.height), MARK)
    im.save(OUT / out, quality=92)


story(GASPAR, ["Who was your favorite", "LPS teacher?"], 240, "story-teacher-question.jpg", "Littleton High School, 1984")
story(LIBRARY, ["Yes on 4A, the LPS", "mill levy override.", "Your ballot is due by", "7 p.m. Tuesday, Nov. 3."], 140, "story-ballot-due.jpg", "Heritage High School, 1981")
print("ok")
