#!/usr/bin/env python3
"""Oct 17 GOTV Reel: the scariest things around here this October, ranked.
Live Photos + two videos from Ben's library (raw/, exported from Photos).
Silent on purpose: add a trending sound inside Instagram / Facebook.

    python3 private/instagram-launch/source-files/polls-reel/make_polls_reel.py
"""
import pathlib, subprocess
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = pathlib.Path(__file__).resolve().parent
RAW = HERE / "raw"
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)
W, H, FPS = 1080, 1920, 30
TOP = 270  # Reels/TikTok header band ends at 250; bottom 480 px belongs to the platform
FONT = "/System/Library/Fonts/Helvetica.ttc"


def font(size):
    return ImageFont.truetype(FONT, size, index=1)


def classic(d, lines, top, size=60, gap=10, pad_x=18, pad_y=8):
    """Instagram Classic text: black on its own white rounded highlight per line."""
    f = font(size)
    asc, desc = f.getmetrics()
    h = asc + desc
    y = top
    for line in lines:
        if not line:
            y += h // 2
            continue
        w = d.textlength(line, font=f)
        x = (W - w) / 2
        d.rounded_rectangle((x - pad_x, y - pad_y, x + w + pad_x, y + h + pad_y), radius=14, fill="white")
        d.text((x, y), line, font=f, fill="black")
        y += h + 2 * pad_y + gap - 8
    assert y <= H - 480, f"text runs into the platform's bottom band: {lines}"
    return y


def frames(name, start, secs, vf):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(start), "-i", str(RAW / name), "-t", str(secs),
                          "-vf", f"fps={FPS},{vf}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         capture_output=True, check=True).stdout
    size = W * H * 3
    out = [Image.frombytes("RGB", (W, H), raw[i:i + size]) for i in range(0, len(raw) - size + 1, size)]
    n = int(secs * FPS)
    while len(out) < n:  # a Live Photo is ~2-3 s: hold it with a ping-pong
        out += out[::-1]
    return out[:n]


def fill(name, secs, start=0, xshift=0.0, hide=None):
    """Full-bleed 9:16 crop. hide = (x, y, w, h) on the output frame to blur (a house number)."""
    x = f"(iw-{W})/2*(1+{xshift})"
    vf = f"scale=-2:{H},crop={W}:{H}:{x}:0"
    if hide:
        hx, hy, hw, hh = hide
        vf = (f"{vf},split[a][b];[b]crop={hw}:{hh}:{hx}:{hy},boxblur=30:5[m];"
              f"[a][m]overlay={hx}:{hy}")
    return frames(name, start, secs, vf)


def fit(name, secs, start=0, y=420):
    """Whole frame, full width, over a blurred copy of itself; text gets the band above."""
    fh = round(W * 4 / 3)
    vf = (f"split[a][b];[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
          f"boxblur=40:2,eq=brightness=-0.12[bg];[b]scale={W}:{fh}[fg];[bg][fg]overlay=0:{y}")
    return frames(name, start, secs, vf)


def card(base, lines, top=TOP, size=60):
    out = []
    for fr in base:
        fr = fr.copy()
        if lines:
            classic(ImageDraw.Draw(fr), lines, top, size)
        out.append(fr)
    return out


def still(path, secs, y=420, z1=1.04):
    """A photo, full width, slow push-in, over a blurred copy of itself."""
    src = Image.open(path).convert("RGB")
    bg = src.resize((W, H)).filter(ImageFilter.GaussianBlur(40))
    bg = Image.eval(bg, lambda v: int(v * 0.88))
    fg = src.resize((W, round(src.height * W / src.width)), Image.LANCZOS)
    n = int(secs * FPS)
    out = []
    for k in range(n):
        z = 1 + (z1 - 1) * k / max(n - 1, 1)
        f2 = fg.resize((round(fg.width * z), round(fg.height * z)), Image.BILINEAR)
        fr = bg.copy()
        fr.paste(f2, ((W - f2.width) // 2, y - (f2.height - fg.height) // 2))
        out.append(fr)
    return out


def timed(base, beats):
    """beats: [(seconds_in, lines, top, size)]; every beat stays on once it appears."""
    out = []
    for i, fr in enumerate(base):
        fr = fr.copy()
        d = ImageDraw.Draw(fr)
        for t, lines, top, size in beats:
            if i >= t * FPS:
                classic(d, lines, top, size)
        out.append(fr)
    return out


TITLE = ["Scariest things around here", "this October, ranked:"]
TT = TOP + 175  # an item's line, under the title

COUNTER = HERE.parent / "weekend/out/thu-ballot-counter.jpg"  # name, address, barcodes already out

SHOTS = [
    # Ben's own yard: tombstones, a skeleton, and the sign. House number on the planter blurred.
    lambda: timed(fill("IMG_6819.mov", 3.6, xshift=0.4, hide=(0, 1280, 140, 180)),
                  [(0, TITLE, TOP, 48), (1.3, ["5. Our yard.", "(The sign is the least", "scary part.)"], TT, 62)]),
    lambda: timed(fill("IMG_6712.mov", 2.4, hide=(300, 340, 240, 140)),
                  [(0, TITLE, TOP, 48), (0, ["4. This guy."], TT, 62)]),
    lambda: timed(fill("IMG_2444.MOV", 3.0, start=1.5),
                  [(0, TITLE, TOP, 48), (0, ["3. Whatever this is,", "on our stairs."], TT, 62)]),
    lambda: timed(fill("IMG_6805.MOV", 3.0, start=8.0),
                  [(0, TITLE, TOP, 48), (0, ["2. This entire yard."], TT, 62)]),
    lambda: timed(still(COUNTER, 3.8, y=560),
                  [(0, ["And the scariest:"], TOP, 56),
                   (1.0, ["1. A ballot still on the counter", "at 7:01 p.m. on Nov 3."], TOP + 90, 50)]),
    lambda: timed(fill("IMG_6849.mov", 3.0, xshift=0.3), [(0, ["Not scary at all:"], TOP, 60)]),
    lambda: timed(fit("IMG_6842.mov", 4.2, y=760), [(0, ["Fill it in. Sign it.", "Drop it in any", "24-hour drop box.", "",
                                                         "Due by 7 p.m.", "Tuesday, Nov 3."], TOP, 52)]),
]


def end_card(secs=3.0):
    im = Image.new("RGB", (W, H), (244, 246, 244))
    d = ImageDraw.Draw(im)
    for txt, size, y, fill_ in (("Yes on 4A,", 84, 700, (57, 68, 74)),
                                ("the LPS mill levy override.", 56, 810, (57, 68, 74)),
                                ("Don't let it haunt you.", 50, 940, (47, 107, 29))):
        f = font(size)
        d.text(((W - d.textlength(txt, font=f)) / 2, y), txt, font=f, fill=fill_)
    return [im] * int(secs * FPS)


def main():
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
                            "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264",
                            "-pix_fmt", "yuv420p", "-crf", "18", "-movflags", "+faststart",
                            str(OUT / "reel-scariest-things.mp4")], stdin=subprocess.PIPE)
    total, picks = 0, []
    for make in SHOTS + [end_card]:
        shot = make()
        for fr in shot:
            enc.stdin.write(fr.tobytes())
        total += len(shot)
        picks.append(shot[len(shot) // 2].resize((270, 480)))
    enc.stdin.close()
    enc.wait()
    # Contact sheet of one frame per shot, for checking by eye.
    sheet = Image.new("RGB", (270 * 6, 480 * ((len(picks) + 5) // 6)), "white")
    for i, p in enumerate(picks):
        sheet.paste(p, ((i % 6) * 270, (i // 6) * 480))
    sheet.save(OUT / "check-sheet.jpg", quality=85)
    print(f"{total / FPS:.1f} s")


main()
