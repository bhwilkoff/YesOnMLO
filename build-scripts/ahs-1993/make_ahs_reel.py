#!/usr/bin/env python3
"""Arapahoe High, 1993: this community invested in these kids; now it's our turn.
Recut of a volunteer-shared 1993 Arapahoe High montage (1080x1920, 4:3 film in a
black frame at y 596-1323, burned title above it). Our words replace that title.
Silent on purpose: add a sound inside Instagram / Facebook.

    python3 private/instagram-launch/source-files/ahs-1993/make_ahs_reel.py [source.MP4]
"""
import pathlib, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SRC = sys.argv[1] if len(sys.argv) > 1 else str(pathlib.Path.home() / "Downloads/Arapahoe1993.MP4")
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)
W, H, FPS = 1080, 1920, 30
TOP = 290           # Reels/TikTok header band ends at 250
FILM_SRC_Y, FILM_H = 596, 728
FILM_Y = 660        # film bottom lands at 1388, above the 480 px bottom band
FONT = "/System/Library/Fonts/Helvetica.ttc"
INK, GREEN, SURFACE = (57, 68, 74), (47, 107, 29), (244, 246, 244)


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
    return y


def film(t0, t1):
    """Source seconds [t0, t1), film band only."""
    n = round((t1 - t0) * FPS)
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t0:.3f}", "-i", SRC, "-frames:v", str(n),
                          "-vf", f"crop={W}:{FILM_H}:0:{FILM_SRC_Y}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         capture_output=True, check=True).stdout
    size = W * FILM_H * 3
    return [Image.frombytes("RGB", (W, FILM_H), raw[i:i + size]) for i in range(0, len(raw) - size + 1, size)]


# (lines on screen, [source cuts]) -- cuts start 2 frames after each detected scene change
# so no shot opens on the tail of the source's own dissolve.
BEATS = [
    (["Arapahoe High School, 1993."], [(0.10, 1.75), (2.53, 3.00), (3.50, 4.55), (4.67, 6.60)]),
    (["Arapahoe High School, 1993.", "These were LPS kids."], [(8.10, 9.90)]),
    (["This community helped pay for", "their teachers,"], [(12.57, 14.00), (14.13, 15.40), (17.47, 18.95)]),
    (["This community helped pay for", "their teachers,", "their classrooms,"], [(29.07, 30.65), (37.07, 38.50)]),
    (["This community helped pay for", "their teachers,", "their classrooms,", "and their Friday nights."],
     [(24.50, 27.30), (27.40, 28.95), (43.10, 44.80)]),
    (["Those kids grew up."], [(48.97, 49.90), (50.00, 50.87), (50.97, 51.77)]),
    (["Today they're the parents", "and neighbors of LPS kids."],
     [(51.87, 53.50), (54.50, 55.27), (55.97, 56.57), (57.63, 58.55)]),
    (["Someone invested in them."], [(59.13, 60.20), (11.17, 12.45)]),
]


def beat_frames(lines, cuts):
    frames = []
    for t0, t1 in cuts:
        for fr in film(t0, t1):
            im = Image.new("RGB", (W, H), "black")
            im.paste(fr, (0, FILM_Y))
            classic(ImageDraw.Draw(im), lines, TOP)
            frames.append(im)
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
    assert 1125 + 60 <= H - 480
    return [im] * int(secs * FPS)


def main():
    out = OUT / "reel-arapahoe-1993.mp4"
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
                            "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264",
                            "-pix_fmt", "yuv420p", "-crf", "18", "-movflags", "+faststart", str(out)],
                           stdin=subprocess.PIPE)
    total, picks = 0, []
    shots = [beat_frames(lines, cuts) for lines, cuts in BEATS] + [end_card()]
    for shot in shots:
        for fr in shot:
            enc.stdin.write(fr.tobytes())
        total += len(shot)
        picks.append(shot[len(shot) // 2].resize((270, 480)))
    enc.stdin.close()
    enc.wait()
    sheet = Image.new("RGB", (270 * len(picks), 480), "white")
    for i, p in enumerate(picks):
        sheet.paste(p, (i * 270, 0))
    sheet.save(OUT / "check-sheet.jpg")
    print(f"{out} {total / FPS:.1f}s")


if __name__ == "__main__":
    main()
