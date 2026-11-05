#!/usr/bin/env python3
"""Littleton High School '90s montage reel, built like the Arapahoe 1993 and Heritage reels: fast cuts under
building on-screen text, then the "Now it's our turn" card. SILENT on purpose:
the sound is picked in the Instagram / Facebook Reels editor.
Footage: LHS 96-97 video yearbook, uploaded to YouTube by Brandon Duncan (the upload has no sound).

    python3 tools/make_montage.py [reel-name ...]
"""
import pathlib, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

HERE = pathlib.Path(__file__).resolve().parent
RAW = HERE.parent / "raw"
OUT = HERE.parent / "out"
ROOT = HERE.parents[4]
OUT.mkdir(exist_ok=True)
IDS = {"lhs": "gjwtgyEF8Gw"}

W, H, FPS = 1080, 1920, 30
TOP = 290                   # Reels/TikTok header band ends at 250
FILM_W, FILM_H = 960, 720
FILM_X, FILM_Y = (W - FILM_W) // 2, 660   # film bottom 1380, above the 480 px bottom band
FONT = "/System/Library/Fonts/Helvetica.ttc"
INK, GREEN, SURFACE = (57, 68, 74), (47, 107, 29), (244, 246, 244)

# reel -> [(lines on screen, [(yearbook, source start s, seconds), ...]), ...]
REELS = {
    "lhs-90s": [
        (["If you went to school", "in the '90s,"], [("lhs", 41.0, 1.7), ("lhs", 71.9, 0.95), ("lhs", 83.9, 0.95)]),
        (["If you went to school", "in the '90s,", "this will look familiar."],
         [("lhs", 186.2, 1.4), ("lhs", 245.6, 1.4), ("lhs", 213.0, 1.4)]),
        (["Somebody bought", "those computers."], [("lhs", 1231.2, 1.4), ("lhs", 77.9, 0.95), ("lhs", 65.9, 0.95)]),
        (["Somebody taught them", "every harmony."], [("lhs", 666.7, 1.4), ("lhs", 720.7, 1.3), ("lhs", 756.8, 1.3)]),
        (["Somebody paid for", "the band uniforms."], [("lhs", 606.6, 1.4), ("lhs", 510.5, 1.4), ("lhs", 612.6, 1.3)]),
        (["Somebody got them", "all the way here."], [("lhs", 1952.0, 1.4), ("lhs", 1958.0, 1.4), ("lhs", 2100.5, 1.3)]),
        (["That somebody was", "the whole town."], [("lhs", 2156.2, 1.5), ("lhs", 2162.2, 1.6), ("lhs", 2198.2, 1.8)]),
    ],
}


def font(size):
    return ImageFont.truetype(FONT, size, index=1)


def classic(d, lines, top, size=60, gap=10, pad_x=18, pad_y=8):
    """Instagram Classic text: black on its own white rounded highlight per line."""
    f = font(size)
    asc, desc = f.getmetrics()
    h = asc + desc
    y = top
    for line in lines:
        w = d.textlength(line, font=f)
        assert w + 2 * pad_x <= W - 80, f"line too wide: {line}"
        x = (W - w) / 2
        d.rounded_rectangle((x - pad_x, y - pad_y, x + w + pad_x, y + h + pad_y), radius=14, fill="white")
        d.text((x, y), line, font=f, fill="black")
        y += h + 2 * pad_y + gap - 8
    assert y <= FILM_Y - 12, f"text runs into the film: {lines}"


def film(tag, t0, secs):
    n = round(secs * FPS)
    # trim the VHS capture's ragged edges before scaling to the film box
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t0:.3f}", "-i", str(RAW / f"{IDS[tag]}.mp4"),
                          "-frames:v", str(n), "-vf", f"fps={FPS},crop=632:474:11:3,scale={FILM_W}:{FILM_H}",
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
    size = FILM_W * FILM_H * 3
    frames = [Image.frombytes("RGB", (FILM_W, FILM_H), raw[i:i + size]) for i in range(0, len(raw) - size + 1, size)]
    assert len(frames) == n, f"{tag}@{t0}: got {len(frames)} of {n} frames"
    return frames


def end_card(secs=4.5):
    im = Image.new("RGB", (W, H), SURFACE)
    d = ImageDraw.Draw(im)

    def centered(txt, size, y, fill_):
        f = font(size)
        d.text(((W - d.textlength(txt, font=f)) / 2, y), txt, font=f, fill=fill_)

    centered("Now it's our turn.", 88, 330, INK)
    logo = Image.open(ROOT / "branding/yes-on-4a/stacked-light.png").convert("RGBA")
    logo = logo.resize((440, round(logo.height * 440 / logo.width)), Image.LANCZOS)
    im.paste(logo, ((W - logo.width) // 2, 500), logo)
    centered("4A, the LPS mill levy override", 52, 900, INK)
    centered("Ballots due by 7 p.m.", 48, 1060, GREEN)
    centered("Tuesday, Nov. 3", 48, 1125, GREEN)
    return [im] * int(secs * FPS)


def build(name):
    out = OUT / f"{name}.mp4"
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
                            "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264",
                            "-pix_fmt", "yuv420p", "-crf", "18", "-movflags", "+faststart", str(out)],
                           stdin=subprocess.PIPE)
    total, cuts_sheet, picks = 0, [], []
    for lines, cuts in REELS[name]:
        for tag, t0, secs in cuts:
            frs = film(tag, t0, secs)
            row = []
            for k, fr in enumerate(frs):
                im = Image.new("RGB", (W, H), "black")
                im.paste(fr, (FILM_X, FILM_Y))
                classic(ImageDraw.Draw(im), lines, TOP)
                enc.stdin.write(im.tobytes())
                if k in (0, len(frs) // 2, len(frs) - 1):
                    row.append(fr.resize((240, 180)))
                if k == len(frs) // 2 and cuts.index((tag, t0, secs)) == 0:
                    picks.append(im.resize((270, 480)))
            cuts_sheet.append((f"{tag}@{t0}", row))
            total += len(frs)
    card = end_card()
    for im in card:
        enc.stdin.write(im.tobytes())
    total += len(card)
    picks.append(card[0].resize((270, 480)))
    enc.stdin.close()
    assert enc.wait() == 0
    sheet = Image.new("RGB", (270 * len(picks), 480), "white")
    for i, p in enumerate(picks):
        sheet.paste(p, (i * 270, 0))
    sheet.save(OUT / f"{name}-check.jpg")
    # every cut: first / middle / last frame, so a hidden scene change or dissolve shows up
    f = ImageFont.truetype(FONT, 18)
    cs = Image.new("RGB", (3 * 240 + 110, 184 * len(cuts_sheet)), "white")
    d = ImageDraw.Draw(cs)
    for i, (label, row) in enumerate(cuts_sheet):
        d.text((4, i * 184 + 80), label, font=f, fill="black")
        for j, th in enumerate(row):
            cs.paste(th, (110 + j * 240, i * 184))
    cs.save(OUT / f"{name}-cuts.jpg", quality=85)
    print(f"{out} {total / FPS:.1f}s")


if __name__ == "__main__":
    for n in sys.argv[1:] or REELS:
        build(n)
