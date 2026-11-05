#!/usr/bin/env python3
"""Oct 10 + 11 one-stop-shop creative: a car-wall grid, a Chance two-panel,
and two Reels (an itinerary and a fast car flip). Silent video: add a
trending sound inside Instagram.

    python3 private/instagram-launch/source-files/weekend/make_weekend.py
"""
import pathlib, subprocess
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

HERE = pathlib.Path(__file__).resolve().parent
KIT = HERE.parent
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)
FONT = "/System/Library/Fonts/Helvetica.ttc"
INK = (57, 68, 74)
GREEN = (76, 155, 47)


def font(size):
    return ImageFont.truetype(FONT, size, index=1)


def classic(d, lines, top, size, width, gap=10, pad_x=18, pad_y=8, x0=0):
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
        x = x0 + (width - w) / 2
        d.rounded_rectangle((x - pad_x, y - pad_y, x + w + pad_x, y + h + pad_y), radius=14, fill="white")
        d.text((x, y), line, font=f, fill="black")
        y += h + 2 * pad_y + gap - 8
    return y


def fill(path, w, h, focus=(0.5, 0.5)):
    im = ImageOps.exif_transpose(Image.open(KIT / path)).convert("RGB")
    if path.endswith("09-car02.jpg"):  # landscape shot letterboxed in white
        im = im.crop((0, 270, 1080, 1080))
    return ImageOps.fit(im, (w, h), Image.LANCZOS, centering=focus)


CARS = [f"cars/cars-carousel-{n}.jpg" for n in
        ("01-car03", "02-car06", "03-car10", "04-car01", "05-car09", "06-car07",
         "07-car08", "08-car05", "09-car02", "10-tesla", "11-black-suv")]
WHERE = "Arapahoe High, southwest lot"


def car_wall():
    W, H, G, C, R = 1080, 1350, 8, 3, 4
    tw, th = (W - G * (C + 1)) // C, (H - G * (R + 1)) // R
    im = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(im)
    for i in range(C * R):
        x, y = G + (i % C) * (tw + G), G + (i // C) * (th + G)
        if i < len(CARS):
            im.paste(fill(CARS[i], tw, th), (x, y))
            continue
        d.rectangle((x, y, x + tw, y + th), fill=(244, 246, 244))
        for k in range(0, tw, 28):  # dashed outline: an empty window
            d.line((x + k, y + 3, x + min(k + 16, tw), y + 3), fill=GREEN, width=5)
            d.line((x + k, y + th - 3, x + min(k + 16, tw), y + th - 3), fill=GREEN, width=5)
        for k in range(0, th, 28):
            d.line((x + 3, y + k, x + 3, y + min(k + 16, th)), fill=GREEN, width=5)
            d.line((x + tw - 3, y + k, x + tw - 3, y + min(k + 16, th)), fill=GREEN, width=5)
        for txt, f, yy in (("Yours?", font(56), 70), ("Sat + Sun", font(34), 170), ("9:00 to 10:30", font(34), 214)):
            d.text((x + (tw - d.textlength(txt, font=f)) / 2, y + yy), txt, font=f, fill=INK)
    im.save(OUT / "car-wall.jpg", quality=92)


def chance(out, size, extra):
    W, H = size
    half = (H - 8) // 2 if not extra else 760
    im = Image.new("RGB", (W, H), "white")
    im.paste(fill("launch-kit/feed1-carousel-06-dog-stretch.jpg", W, half, (0.5, 0.45)), (0, 0))
    im.paste(fill("cars/cars-carousel-11-black-suv.jpg", W, half), (0, half + 8))
    d = ImageDraw.Draw(im)
    classic(d, ["Chance can't drive."], 40, 58, W)
    classic(d, ["You can."], half + 48, 58, W)
    if extra:
        classic(d, extra, 2 * half + 70, 50, W)
    im.save(OUT / out, quality=92)


def video(name, shots, fps=30):
    """shots: (photo, seconds, lines, text_top, zoom_from, zoom_to). Slow push-in per shot."""
    W, H = 1080, 1920
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
                          "-s", f"{W}x{H}", "-r", str(fps), "-i", "-", "-c:v", "libx264",
                          "-pix_fmt", "yuv420p", "-crf", "18", "-movflags", "+faststart",
                          str(OUT / name)], stdin=subprocess.PIPE)
    for photo, secs, lines, top, z0, z1 in shots:
        base = fill(photo, int(W * 1.12), int(H * 1.12)) if photo else Image.new("RGB", (int(W * 1.12), int(H * 1.12)), "white")
        n = int(secs * fps)
        for k in range(n):
            z = z0 + (z1 - z0) * k / max(n - 1, 1)
            cw, ch = int(base.width / z), int(base.height / z)
            l, t = (base.width - cw) // 2, (base.height - ch) // 2
            fr = base.crop((l, t, l + cw, t + ch)).resize((W, H), Image.BILINEAR)
            if lines:
                classic(ImageDraw.Draw(fr), lines, top, 60, W)
            p.stdin.write(fr.tobytes())
    p.stdin.close()
    p.wait()


def reel(name, segs, fps=30):
    """segs: ("still", path, secs, lines, top, z0, z1) or ("clip", path, secs, lines, top, xshift).
    Clips are Live Photo .mov files (3:4 portrait), cropped to 9:16; xshift nudges the crop (-1..1)."""
    W, H = 1080, 1920
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
                            "-s", f"{W}x{H}", "-r", str(fps), "-i", "-", "-c:v", "libx264",
                            "-pix_fmt", "yuv420p", "-crf", "18", "-movflags", "+faststart",
                            str(OUT / name)], stdin=subprocess.PIPE)
    for seg in segs:
        kind, path, secs, lines, top = seg[:5]
        n = int(secs * fps)
        if kind == "clip":
            x = f"(iw-{W})/2*(1+{seg[5]})"
            raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(KIT / path), "-t", str(secs),
                                  "-vf", f"fps={fps},scale=-2:{H},crop={W}:{H}:{x}:0",
                                  "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
            frames = [raw[i:i + W * H * 3] for i in range(0, len(raw), W * H * 3)]
            frames = (frames + frames[::-1] * 3)[:n] if len(frames) < n else frames[:n]
            for fb in frames:
                fr = Image.frombytes("RGB", (W, H), fb)
                if lines:
                    classic(ImageDraw.Draw(fr), lines, top, 60, W)
                enc.stdin.write(fr.tobytes())
        elif len(seg) > 7 and "pan" in seg[7]:
            # Wide shot: full height, slide the 9:16 window across so nobody is cut in half.
            x0, x1 = seg[7]["pan"]
            src = ImageOps.exif_transpose(Image.open(KIT / path)).convert("RGB")
            src = src.resize((round(src.width * H / src.height), H), Image.LANCZOS)
            span = src.width - W
            for k in range(n):
                t = k / max(n - 1, 1)
                t = t * t * (3 - 2 * t)
                l = round(span * (x0 + (x1 - x0) * t))
                fr = src.crop((l, 0, l + W, H))
                if lines:
                    classic(ImageDraw.Draw(fr), lines, top, 60, W)
                enc.stdin.write(fr.tobytes())
        elif len(seg) > 7 and seg[7].get("fit"):
            # Group shot: the whole photo, over a blurred, dimmed copy of itself.
            src = ImageOps.exif_transpose(Image.open(KIT / path)).convert("RGB")
            bg = ImageOps.fit(src, (W, H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(40))
            bg = Image.blend(bg, Image.new("RGB", (W, H), "black"), 0.35)
            fg = src.resize((W, round(src.height * W / src.width)), Image.LANCZOS)
            z0, z1 = seg[5], seg[6]
            for k in range(n):
                z = z0 + (z1 - z0) * k / max(n - 1, 1)
                f2 = fg.resize((round(fg.width * z), round(fg.height * z)), Image.BILINEAR)
                fr = bg.copy()
                fr.paste(f2, ((W - f2.width) // 2, (H - f2.height) // 2 + 120))
                if lines:
                    classic(ImageDraw.Draw(fr), lines, top, 60, W)
                enc.stdin.write(fr.tobytes())
        else:
            z0, z1 = seg[5], seg[6]
            focus = seg[7]["focus"] if len(seg) > 7 else (0.5, 0.5)
            base = fill(path, int(W * 1.12), int(H * 1.12), focus)
            for k in range(n):
                z = z0 + (z1 - z0) * k / max(n - 1, 1)
                cw, ch = int(base.width / z), int(base.height / z)
                l, t = (base.width - cw) // 2, (base.height - ch) // 2
                fr = base.crop((l, t, l + cw, t + ch)).resize((W, H), Image.BILINEAR)
                if lines:
                    classic(ImageDraw.Draw(fr), lines, top, 60, W)
                enc.stdin.write(fr.tobytes())
    enc.stdin.close()
    enc.wait()


car_wall()
chance("chance-feed.jpg", (1080, 1350), None)
chance("chance-story.jpg", (1080, 1920), ["Sunday, 9:00 to 10:30 a.m.", "Arapahoe High School,", "southwest parking lot."])


FLIP = [(c, 0.45, None, 0, 1.04, 1.0) for c in CARS]
FLIP[0] = (CARS[0], 1.2, ["A few of the cars", "we've painted."], 260, 1.04, 1.0)
FLIP.append(("weekend/out/car-wall.jpg", 3.2, ["Yours is next.", "", "Saturday + Sunday", "9:00 to 10:30 a.m.", "Arapahoe High School,", "southwest parking lot."], 600, 1.0, 1.05))
video("reel-car-flip.mp4", FLIP)

R = "weekend/raw/"
SUN = ["Sunday morning,", "9:00 to 10:30 a.m.", "Arapahoe High School,", "southwest parking lot."]
WHEN = ["Saturday + Sunday", "9:00 to 10:30 a.m.", "Arapahoe High School,", "southwest parking lot."]

# The real Oct 3 one-stop shop: pick what you need.
reel("reel-five-steps.mp4", [
    ("still", R + "IMG_4625.jpeg", 3.0, ["One stop.", "Pick what you need."], 220, 1, 1, {"pan": (0.15, 0.7)}),
    ("still", R + "IMG_4619.jpeg", 2.6, ["Get your car painted."], 220, 1.0, 1.05, {"focus": (0.2, 0.6)}),
    ("clip", R + "IMG_6759.mov", 2.4, ["Drive home like this."], 220, -0.7),
    ("still", R + "IMG_4623.jpeg", 2.8, ["Grab a yard sign", "for your yard."], 300, 1.0, 1.04, {"fit": True}),
    ("still", "launch-kit/feed1-carousel-01-buttons-table.jpg", 2.4, ["Take a lit-drop turf.", "No knocking."], 220, 1.0, 1.08),
    ("still", R + "IMG_4620.jpeg", 4.0, WHEN, 220, 1, 1, {"pan": (0.0, 1.0)}),
])

# Live Photos: the dogs at the front window, the sign out in the yard.
DOGS = ["IMG_6822", "IMG_6824", "IMG_6825", "IMG_6826", "IMG_6828"]
reel("reel-security-detail.mp4",
     [("clip", R + d + ".mov", 2.6, ["This yard sign has", "a security detail."] if i < 2 else None, 1450, -0.8) for i, d in enumerate(DOGS)]
     + [("clip", R + "IMG_6823.mov", 3.4, ["Want one for your yard?", ""] + SUN, 1380, -0.8)])

# Live Photos from a walk around the neighborhood, Oct 5 and 6.
WALK = ["IMG_6803", "IMG_6810", "IMG_6812", "IMG_6813", "IMG_6814", "IMG_6815", "IMG_6816", "IMG_6817", "IMG_6818"]
reel("reel-sign-walk.mp4",
     [("clip", R + w + ".mov", 1.25, ["Yard signs are going up."], 220, 0) for w in WALK]
     + [("clip", R + "IMG_6804.mov", 3.6, ["Want one?", ""] + SUN, 1380, 0)])


def square(path, box, out):
    """box = (left, top, size) as fractions of width, height, and short side."""
    im = ImageOps.exif_transpose(Image.open(KIT / path)).convert("RGB")
    side = round(min(im.size) * box[2])
    l, t = round(im.width * box[0]), round(im.height * box[1])
    im.crop((l, t, l + side, t + side)).resize((1080, 1080), Image.LANCZOS).save(OUT / out, quality=92)


# Sunday push: the real Oct 3 shop as a square carousel, nobody cropped out.
square(R + "IMG_4620.jpeg", (0.0, 0.0, 1.0), "sun-1-painters.jpg")
square(R + "IMG_4623.jpeg", (0.08, 0.0, 1.0), "sun-2-volunteers.jpg")
square(R + "IMG_4619.jpeg", (0.0, 0.17, 1.0), "sun-3-painting.jpg")
square(R + "IMG_4625.jpeg", (0.06, 0.0, 1.0), "sun-4-table.jpg")

im = fill(R + "IMG_4619.jpeg", 1080, 1920, (0.2, 0.6))
d = ImageDraw.Draw(im)
classic(d, ["Tomorrow morning,", "9:00 to 10:30."] + WHEN[2:], 200, 58, 1080)
classic(d, ["Car paint, yard signs,", "and lit-drop turfs.", "", "Pick what you need."], 1380, 50, 1080)
im.save(OUT / "story-tomorrow-10-11.jpg", quality=92)

print("\n".join(sorted(x.name for x in OUT.iterdir())))
