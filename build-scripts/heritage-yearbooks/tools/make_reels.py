#!/usr/bin/env python3
"""Heritage High video-yearbook reels: this community invested in these kids; now it's our turn.
Cuts from Matt Adams's uploads of the Heritage (Littleton) video yearbooks, 1993-98.
Source audio is kept (it IS the point); every burned speech caption is re-heard by
whisper before it ships, and a caption that can't be confirmed refuses the render.

    python3 tools/make_reels.py [reel-name ...]
"""
import json, pathlib, re, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFont

HERE = pathlib.Path(__file__).resolve().parent
BASE = HERE.parent
RAW = BASE / "raw"
ROOT = BASE.parents[3]
OUT = BASE / "out"
OUT.mkdir(exist_ok=True)
MODEL = pathlib.Path.home() / ".cache/whisper-models/ggml-small.en.bin"

W, H, FPS = 1080, 1920, 30
SAFE_TOP, SAFE_BOTTOM = 250, H - 480
FILM_W, FILM_H = 960, 720
FILM_X, FILM_Y = (W - FILM_W) // 2, 470
CAP_Y = FILM_Y + FILM_H + 24
FONT = "/System/Library/Fonts/Helvetica.ttc"
INK, GREEN, SURFACE = (57, 68, 74), (47, 107, 29), (244, 246, 244)

Y93, Y95, Y96, Y97, Y98 = "hzTaJZUXj8w", "OCsY4SphM0c", "UwIcCvWb6ms", "MrdVwTJglyM", "xem-xcOB2Ow"

# Each beat: (source id, t0, t1, title lines above the film, spoken caption or None).
# A caption is what the person on tape says; it must be heard in [t0, t1] or the render refuses.
REELS = json.loads((HERE / "reels.json").read_text())

STOP = set("""a an the and or but to of in on at for with is are was were be been it its this that
i you he she we they me my our your his her their them us so do did does not no yes oh uh um
just like well what will would can could i'm it's that's we're you're there here have has had""".split())


def font(size, bold=True):
    return ImageFont.truetype(FONT, size, index=1 if bold else 0)


def wrap(d, text, f, maxw):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=f) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    return lines + [cur] if cur else lines


def classic(d, lines, top, size, limit):
    """Instagram Classic text: black on its own white rounded highlight per line."""
    f = font(size)
    asc, desc = f.getmetrics()
    h, pad_x, pad_y = asc + desc, 18, 8
    y = top
    for line in lines:
        w = d.textlength(line, font=f)
        assert w + 2 * pad_x <= W - 60, f"line too wide: {line}"
        x = (W - w) / 2
        d.rounded_rectangle((x - pad_x, y - pad_y, x + w + pad_x, y + h + pad_y), radius=14, fill="white")
        d.text((x, y), line, font=f, fill="black")
        y += h + 2 * pad_y + 2
    assert y <= limit, f"text overruns its band: {lines}"


def overlay(title, caption):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if title:
        classic(d, title, SAFE_TOP + 40, 58, FILM_Y - 14)
    if caption:
        f = font(46, bold=False)
        lines = wrap(d, caption, f, W - 140)
        assert len(lines) <= 3, f"caption too long: {caption}"
        y = CAP_Y
        for line in lines:
            w = d.textlength(line, font=f)
            d.text(((W - w) / 2, y), line, font=f, fill="white", stroke_width=3, stroke_fill="black")
            y += 58
        assert y <= SAFE_BOTTOM, f"caption runs into the platform band: {caption}"
    return im


def heard(src, t0, t1, caption):
    """Fraction of the caption's content words whisper hears in [t0, t1]; None = couldn't check."""
    want = {w for w in re.findall(r"[a-z']+", caption.lower()) if w not in STOP}
    if len(want) < 2 or not MODEL.exists():
        return None
    with tempfile.TemporaryDirectory() as td:
        wav = pathlib.Path(td) / "c.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t0:.2f}", "-t", f"{t1 - t0 + 0.4:.2f}",
                        "-i", str(RAW / f"{src}.mp4"), "-ar", "16000", "-ac", "1", str(wav)], check=True)
        r = subprocess.run(["whisper-cli", "-m", str(MODEL), "-f", str(wav), "-nt", "-np"],
                           capture_output=True, text=True)
    got = set(re.findall(r"[a-z']+", r.stdout.lower()))
    return len(want & got) / len(want) if r.returncode == 0 else None


def segment(i, beat, td):
    src, t0, t1, title, caption = beat
    png = td / f"o{i}.png"
    overlay(title, caption).save(png)
    out = td / f"s{i}.mp4"
    vf = (f"[0:v]scale={FILM_W}:{FILM_H},setsar=1,fps={FPS},"
          f"pad={W}:{H}:{FILM_X}:{FILM_Y}:black[f];[f][1:v]overlay=0:0,format=yuv420p[v]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t0:.3f}", "-t", f"{t1 - t0:.3f}",
                    "-i", str(RAW / f"{src}.mp4"), "-i", str(png), "-filter_complex", vf,
                    "-map", "[v]", "-map", "0:a", "-c:v", "libx264", "-crf", "18", "-r", str(FPS),
                    "-c:a", "aac", "-ar", "48000", "-ac", "2", str(out)], check=True)
    return out


def end_card(td, secs=4.5):
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
    png = td / "end.png"
    im.save(png)
    out = td / "end.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", str(png), "-f", "lavfi",
                    "-i", "anullsrc=r=48000:cl=stereo", "-t", str(secs), "-vf", "format=yuv420p",
                    "-c:v", "libx264", "-crf", "18", "-r", str(FPS), "-c:a", "aac", str(out)], check=True)
    return out


def has_audio(path):
    r = subprocess.run(["ffmpeg", "-i", str(path), "-af", "volumedetect", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    m = re.search(r"mean_volume: (-?[\d.]+) dB", r)
    return m and float(m[1]) > -60


def build(name):
    beats = REELS[name]
    for src, t0, t1, _, cap in beats:
        if cap:
            s = heard(src, t0, t1, cap)
            assert s is not None and s >= 0.6, f"{name}: caption not heard ({s}) at {src} {t0}: {cap}"
    with tempfile.TemporaryDirectory() as td:
        td = pathlib.Path(td)
        parts = [segment(i, b, td) for i, b in enumerate(beats)] + [end_card(td)]
        lst = td / "list.txt"
        lst.write_text("".join(f"file '{p}'\n" for p in parts))
        joined = td / "joined.mp4"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst),
                        "-c", "copy", str(joined)], check=True)
        dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
                                    "csv=p=0", str(joined)], capture_output=True, text=True).stdout)
        out = OUT / f"{name}.mp4"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(joined), "-c:v", "copy",
                        "-af", f"loudnorm=I=-16:TP=-1.5:LRA=11,afade=t=in:d=0.3,afade=t=out:st={dur - 5.0:.2f}:d=0.6",
                        "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(out)], check=True)
    assert has_audio(out), f"{name}: render lost its audio"
    frames = []
    t = 0.0
    for src, t0, t1, *_ in beats:
        frames.append(t + (t1 - t0) / 2)
        t += t1 - t0
    frames.append(t + 2)
    picks = []
    for ft in frames:
        raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{ft:.2f}", "-i", str(out), "-frames:v", "1",
                              "-vf", "scale=270:480", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                             capture_output=True, check=True).stdout
        picks.append(Image.frombytes("RGB", (270, 480), raw))
    sheet = Image.new("RGB", (270 * len(picks), 480), "white")
    for i, p in enumerate(picks):
        sheet.paste(p, (i * 270, 0))
    sheet.save(OUT / f"{name}-check.jpg")
    print(f"{out} {dur:.1f}s")


if __name__ == "__main__":
    for n in sys.argv[1:] or REELS:
        build(n)
