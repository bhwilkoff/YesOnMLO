#!/usr/bin/env python3
"""Final celebration set: montage carousel, Reel, wash-your-car, THANK YOU, Stories,
Facebook cover. The district called 4A on Nov 4. The yes count is floored to the nearest
thousand ("more than 23,000") so it stays true as the last ballots are counted.

    python3 private/instagram-launch/source-files/victory/make_victory.py [reel|stills]
"""
import json, pathlib, subprocess, sys, urllib.request
from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = pathlib.Path(__file__).resolve().parent
RAW, OUT = HERE / "raw", HERE / "out"
OUT.mkdir(exist_ok=True)
REPO = HERE.parents[3]
LOGO = REPO / "branding/yes-on-4a/stacked-light.png"
HELV = "/System/Library/Fonts/Helvetica.ttc"
NEUE = "/System/Library/Fonts/HelveticaNeue.ttc"
INK, GREEN, DEEP, CREAM = (57, 68, 74), (76, 155, 47), (47, 107, 29), (244, 241, 232)
FPS, W, H, TOP = 30, 1080, 1920, 270
FEED = "https://results.enr.clarityelections.com/CO/Arapahoe/127409"


def font(size, bold=True):
    return ImageFont.truetype(HELV, size, index=1 if bold else 0)


def classic(d, lines, top, size, width, gap=10, pad_x=18, pad_y=8):
    """Instagram Classic text: black on its own white rounded highlight per line."""
    f = font(size)
    asc, desc = f.getmetrics()
    h, y = asc + desc, top
    for line in lines:
        w = d.textlength(line, font=f)
        x = (width - w) / 2
        d.rounded_rectangle((x - pad_x, y - pad_y, x + w + pad_x, y + h + pad_y), radius=14, fill="white")
        d.text((x, y), line, font=f, fill="black")
        y += h + 2 * pad_y + gap - 8
    return y


def photo(name, size, focus=(0.5, 0.5)):
    im = ImageOps.exif_transpose(Image.open(RAW / name)).convert("RGB")
    return ImageOps.fit(im, size, Image.LANCZOS, centering=focus)


def centered(d, y, text, f, fill, width):
    d.text(((width - d.textlength(text, font=f)) / 2, y), text, font=f, fill=fill)


def logo(canvas, width, y):
    lg = Image.open(LOGO).convert("RGBA")
    lg = lg.resize((width, round(lg.height * width / lg.width)), Image.LANCZOS)
    canvas.paste(lg, ((canvas.width - width) // 2, y), lg)
    return y + lg.height


def save(im, name):
    im.save(OUT / name, quality=92)
    print(name)


# --- Reel ---------------------------------------------------------------

SHOTS = [  # file, seconds, focus x, label lines
    ("IMG_4641.jpg", 1.7, .62, ["It took paint pens."]),
    ("painter-pink.jpg", 1.3, .45, ["It took paint pens."]),
    ("IMG_6647.mov", 1.4, .5, ["It took paint pens."]),
    ("IMG_7103.mov", 1.7, .5, ["It took yard signs."]),
    ("IMG_6697.mov", 1.3, .5, ["It took yard signs."]),
    ("IMG_4613.jpg", 1.9, .5, ["It took a folding table", "in a parking lot."]),
    ("IMG_4643.jpg", 1.4, .5, ["It took a folding table", "in a parking lot."]),
    ("kitchen-postcards.jpg", 1.8, .42, ["It took a kitchen table."]),
    ("sat-3-notes.jpg", 1.4, .5, ["It took a lot of postcards."]),
    ("IMG_7824.mov", 1.6, .5, ["It took buttons."]),
    ("IMG_8401.mov", 1.9, .36, ["Then, election night."]),
    ("IMG_8407.mov", 2.3, .36, ["It took all of us."]),
    ("IMG_8406.mov", 1.7, .4, ["It took all of us."]),
    ("IMG_8404.jpeg", 2.0, .46, ["It took all of us."]),
    ("IMG_8409.mov", 2.2, .3, ["It took all of us."]),
]


def still_frames(name, secs, fx):
    im = ImageOps.exif_transpose(Image.open(RAW / name)).convert("RGB")
    s = max(W / im.width, H / im.height) * 1.08
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    n = int(secs * FPS)
    for i in range(n):  # slow push in
        z = 1 - .06 * i / n
        cw, ch = W / 1.0 * z * 1.0, H * z
        x = (im.width - cw) * fx
        y = (im.height - ch) / 2
        yield im.resize((W, H), Image.BILINEAR, box=(x, y, x + cw, y + ch))


def live_frames(name, secs, fx):
    vf = f"fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}:(iw-{W})*{fx}:(ih-{H})/2"
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(RAW / name), "-vf", vf, "-f", "rawvideo",
                          "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
    size = W * H * 3
    out = [Image.frombytes("RGB", (W, H), raw[i:i + size]) for i in range(0, len(raw) - size + 1, size)]
    n = int(secs * FPS)
    while len(out) < n:  # a Live Photo runs 1.5-3 s: ping-pong if it's short
        out += out[::-1]
    return out[:n]


def count():
    ua = {"User-Agent": "Mozilla/5.0"}
    ver = urllib.request.urlopen(urllib.request.Request(FEED + "/current_ver.txt", headers=ua)).read().decode().strip()
    rows = json.load(urllib.request.urlopen(urllib.request.Request(f"{FEED}/{ver}/json/en/summary.json", headers=ua)))
    yes, no = next(x for x in rows if x["K"] == "79")["V"][:2]
    print("feed", ver, yes, no)
    return yes, no


def floor_k(yes):
    return f"{yes // 1000 * 1000:,}"


def end_card():
    c = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(c)
    yes, _ = count()
    centered(d, 330, "IT PASSED.", cond(170), INK, W)
    centered(d, 550, "4A, the LPS mill levy override", font(50), DEEP, W)
    centered(d, 625, f"More than {floor_k(yes)} neighbors said yes.", font(44, False), INK, W)
    centered(d, 690, "Thank you.", font(44, False), INK, W)
    bottom = logo(c, 300, 790)
    assert bottom <= H - 480 + 90
    return c


def reel():
    name = "reel-it-took-all-of-us.mp4"
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p",
                          "-movflags", "+faststart", str(OUT / name)], stdin=subprocess.PIPE)
    sheet = []
    for file, secs, fx, label in SHOTS:
        fr = live_frames(file, secs, fx) if file.endswith(".mov") else still_frames(file, secs, fx)
        for i, im in enumerate(fr):
            im = im.copy()
            bottom = classic(ImageDraw.Draw(im), label, TOP, 60, W)
            assert bottom <= H - 480
            if i == 12:
                sheet.append(im.resize((216, 384)))
            p.stdin.write(im.tobytes())
    card = end_card()
    sheet.append(card.resize((216, 384)))
    for _ in range(int(3.5 * FPS)):
        p.stdin.write(card.tobytes())
    p.stdin.close()
    p.wait()
    S = Image.new("RGB", (216 * 8, 384 * 2), "black")
    for i, t in enumerate(sheet):
        S.paste(t, ((i % 8) * 216, (i // 8) * 384))
    S.save(OUT / "check-reel.jpg", quality=85)
    print(name)


# --- Stills -------------------------------------------------------------

def cond(size):
    return ImageFont.truetype(NEUE, size, index=9)


GUT, PAD = 8, 24


def montage(size, head, cells, kicker=None, cols=12, rows=12, top=None):
    """Cream sheet, a condensed headline, then photos on a grid. cells = (file, x, y, w, h, focus)."""
    w, h = size
    c = Image.new("RGB", size, CREAM)
    d = ImageDraw.Draw(c)
    top = top if top is not None else 0
    y = top + 38
    if kicker:
        centered(d, y, kicker, font(38), DEEP, w)
        y += 50
    size = 112
    while cond(size).getlength(head) > w - 130:
        size -= 2
    centered(d, y + (112 - size) // 2, head, cond(size), INK, w)
    y += 136
    gw, gh = (w - 2 * PAD) / cols, (h - y - PAD - (top if top else 0)) / rows
    for f, x, yy, cw, ch, *foc in cells:
        x0, y0 = round(PAD + x * gw), round(y + yy * gh)
        x1, y1 = round(PAD + (x + cw) * gw) - GUT, round(y + (yy + ch) * gh) - GUT
        if x + cw == cols:
            x1 = w - PAD
        if yy + ch == rows:
            y1 = round(y + rows * gh)
        c.paste(photo(f, (x1 - x0, y1 - y0), foc[0] if foc else (.5, .5)), (x0, y0))
    return c


F = (1080, 1350)
CARS = [f"cars-carousel-{n}.jpg" for n in ("01-car03", "02-car06", "03-car10", "04-car01", "05-car09", "06-car07",
                                           "07-car08", "08-car05", "10-tesla", "11-black-suv", "12-markers")]
SLIDES = [
    ("IT PASSED.", "4A, the LPS mill levy override", [
        ("IMG_8409.jpeg", 0, 0, 7, 6, (.28, .6)), ("sun-1-painters.jpg", 7, 0, 5, 3), ("sun-2-volunteers.jpg", 7, 3, 5, 3),
        ("IMG_8407.jpeg", 0, 6, 7, 6, (.33, .5)), ("cars-carousel-08-car05.jpg", 7, 6, 5, 3, (.5, .35)),
        ("IMG_7104.jpg", 7, 9, 5, 3, (.5, .85))]),
    ("PAINT PENS.", "It took", [
        ("sun-1-painters.jpg", 0, 0, 12, 5, (.5, .5))] + [
        (CARS[i], (k % 4) * 3, 5 + (k // 4) * 3.5, 3, 3.5, (.5, .4)) for k, i in enumerate((0, 1, 2, 3, 4, 5, 7, 9))]),
    ("YARD SIGNS.", "It took", [
        ("IMG_7104.jpg", 0, 0, 6, 8, (.5, .85)), ("sign-extra.jpg", 6, 0, 6, 4, (.5, .35)), ("sign-2.jpg", 6, 4, 6, 4, (.5, .45)),
        ("sign-3.jpg", 0, 8, 4, 4, (.75, .55)), ("IMG_6697.jpg", 4, 8, 4, 4, (.5, .42)), ("sign-6.jpg", 8, 8, 4, 4, (.75, .15))]),
    ("FOLDING TABLES.", "It took", [
        ("sun-2-volunteers.jpg", 0, 0, 7, 7), ("IMG_4613.jpg", 7, 0, 5, 7, (.5, .55)),
        ("IMG_4625.jpeg", 0, 7, 7, 5, (.62, .6)), ("IMG_4643.jpg", 7, 7, 5, 5, (.5, .62))]),
    ("KITCHEN TABLES.", "It took", [
        ("kitchen-postcards.jpg", 0, 0, 7, 12, (.42, .5)), ("letters-blurred.jpg", 7, 0, 5, 12, (.3, .5))]),
    ("BUTTONS.", "It took", [
        ("IMG_6843.jpg", 0, 0, 7, 12, (.5, .4)), ("IMG_7824.jpg", 7, 0, 5, 5, (.5, .3)), ("btn-plaid.jpg", 7, 5, 5, 4, (.5, .32)), ("btn-table.jpg", 7, 9, 5, 3)]),
    ("ALL OF US.", "It took", [
        ("IMG_8407.jpeg", 0, 0, 12, 6, (.5, .55)), ("IMG_8404.jpeg", 0, 6, 6, 6, (.46, .5)),
        ("IMG_8409.jpeg", 6, 6, 6, 3, (.3, .55)), ("IMG_8402.jpeg", 6, 9, 3, 3, (.35, .25)), ("IMG_8401.jpeg", 9, 9, 3, 3, (.45, .45))]),
]


def closer(name, size, top):
    w, h = size
    c = Image.new("RGB", size, CREAM)
    d = ImageDraw.Draw(c)
    yes, no = count()
    strip = ["IMG_8404.jpeg", "cars-carousel-02-car06.jpg", "sun-2-volunteers.jpg", "IMG_7104.jpg"]
    tw = (w - 2 * PAD - 3 * GUT) // 4
    foc = [(.46, .3), (.5, .4), (.5, .5), (.5, .85)]
    for i, f in enumerate(strip):
        c.paste(photo(f, (tw, 300), foc[i]), (PAD + i * (tw + GUT), top))
    y = top + 340
    centered(d, y, f"{floor_k(yes)}+", cond(230), GREEN, w)
    centered(d, y + 262, "neighbors said yes.", font(54), INK, w)
    centered(d, y + 340, "4A, the LPS mill levy override, passed.", font(38), DEEP, w)
    centered(d, y + 402, "The wage freeze lifts: a 2% average raise for LPS staff.", font(30, False), INK, w)
    centered(d, y + 444, "And March 19 goes back to being a school day.", font(30, False), INK, w)
    logo(c, 230, y + 510)
    save(c, name)


def carousel():
    for i, (head, kicker, cells) in enumerate(SLIDES, 1):
        save(montage(F, head, cells, kicker), f"carousel-{i}.jpg")
    closer("carousel-8.jpg", F, 60)


MOSAIC = ["IMG_8404.jpeg", "IMG_4623.jpeg", "IMG_6647.jpg", "IMG_8407.jpeg", "IMG_4641.jpg", "IMG_7104.jpg",
          "painter-pink.jpg", "IMG_8409.jpeg", "kitchen-postcards.jpg", "btn-table.jpg", "IMG_8401.jpeg", "IMG_4613.jpg",
          "IMG_6697.jpg", "IMG_8406.jpeg", "sat-3-notes.jpg", "IMG_4625.jpeg", "IMG_8402.jpeg", "IMG_6843.jpg",
          "IMG_7103.jpg", "IMG_4643.jpg", "kitchen-postcards.jpg", "btn-plaid.jpg", "IMG_7824.jpg", "IMG_9684.jpeg"]


def tiles(w, h, tile):
    cols, rows = -(-w // tile), -(-h // tile)
    t = Image.new("RGB", (cols * tile, rows * tile))
    for i in range(cols * rows):
        f = MOSAIC[(i * 7 + i // cols * 5) % len(MOSAIC)]
        t.paste(photo(f, (tile, tile)), ((i % cols) * tile, (i // cols) * tile))
    return t.crop((0, 0, w, h))


def fit_font(text, width):
    size = 100
    while True:
        f = ImageFont.truetype(NEUE, size + 4, index=9)
        if f.getlength(text) > width:
            return ImageFont.truetype(NEUE, size, index=9)
        size += 4


def thank_you(name, w, h, lines, tile, top, span=.92):
    mask = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(mask)
    y = top
    for t in lines:
        f = fit_font(t, w * span)
        box = d.textbbox((0, 0), t, font=f)
        d.text(((w - (box[2] - box[0])) / 2 - box[0], y - box[1]), t, font=f, fill=255)
        y += (box[3] - box[1]) + 34
    c = Image.new("RGB", (w, h), CREAM)
    c.paste(tiles(w, h, tile), (0, 0), mask)
    dd = ImageDraw.Draw(c)
    if span == .92:
        centered(dd, y + 26, "Neighbors did this.", font(int(w * .046)), INK, w)
        logo(c, int(w * .26), y + 110)
    else:  # Facebook crops the cover's sides on phones: keep everything in the middle 1080 px
        centered(dd, y + 2, "Your Neighbors Said Yes.", font(54), INK, w)
        assert logo(c, 250, y + 76) <= h - 20
    save(c, name)


def wash():
    cells = [(CARS[i], (i % 3) * 4, (i // 3) * 3, 4, 3, (.5, .4)) for i in (0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 8, 8)][:12]
    cells[11] = ("cars-carousel-09-car02.jpg", 8, 9, 4, 3, (.5, .5))
    save(montage(F, "WASH YOUR CAR NOW.", cells, "You can"), "wash-your-car.jpg")


def stories():
    S, T = (1080, 1920), 250
    save(montage(S, "ALL OF US.", SLIDES[6][2], "It took", top=T), "story-last-night.jpg")
    closer("story-count.jpg", S, 330)
    cells = [(CARS[i], (i % 3) * 4, (i // 3) * 3, 4, 3, (.5, .4)) for i in (0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 8, 2)]
    cells[11] = ("cars-carousel-09-car02.jpg", 8, 9, 4, 3, (.5, .5))
    head = montage(S, "WASH YOUR CAR.", cells, "You can", top=T)
    save(head, "story-wash.jpg")


def stills():
    carousel()
    wash()
    stories()
    thank_you("thank-you-feed.jpg", 1080, 1350, ["THANK", "YOU"], 135, 110)
    thank_you("story-thank-you.jpg", 1080, 1920, ["THANK", "YOU"], 135, 330)
    thank_you("facebook-cover.jpg", 1640, 624, ["THANK YOU"], 80, 48, span=.64)


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    if what in ("stills", "all"):
        stills()
    if what in ("reel", "all"):
        reel()
