#!/usr/bin/env python3
"""Old movies about voting, cut into a five-day series of Reels that end on 4A.
Clips come from the archive.org originals named in ~/Downloads/Vote.archiveproj, fetched with
padding (fetch_sources.py -> raw/archive, fetch_all.py -> raw/all), because the app cuts tight to
subtitle cues and clips words. Every in/out point below sits in a pause, measured on the source's
loudness, never on whisper's word times (they run up to a second early). The dialogue IS the joke,
so source audio stays on. Every burned caption is re-heard by whisper before it ships; one that
can't be confirmed refuses the render.

    python3 make_vote_reel.py [reel-name ...]
"""
import pathlib, re, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFont

HERE = pathlib.Path(__file__).resolve().parent
RAW = HERE / "raw"
FADE_IN, FADE_OUT = 0.06, 0.10
ROOT = HERE.parents[3]
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)
MODEL = pathlib.Path.home() / ".cache/whisper-models/ggml-small.en.bin"

W, H, FPS = 1080, 1920, 30
SAFE_TOP, SAFE_BOTTOM = 250, H - 480
BOX_W, BOX_H = 1000, 750
BOX_X, BOX_Y = (W - BOX_W) // 2, 470
CAP_Y = BOX_Y + BOX_H + 24
FONT = "/System/Library/Fonts/Helvetica.ttc"
INK, GREEN, SURFACE = (57, 68, 74), (47, 107, 29), (244, 246, 244)
MEASURE = "4A, the LPS mill levy override"

# A beat: (source under raw/, in, out seconds within that file, title lines, caption, options).
# Options: fade_out (seconds), crop (ffmpeg crop expression; default is detected letterbox),
# line_over (source, in, out, seconds into the beat): a line laid over a shot where no one speaks.
# An end card: headline, then (text, size, colour) rows under the logo.
DUE_TUE = [("Ballots due by 7 p.m.", 52, GREEN), ("Tuesday, Nov. 3", 52, GREEN)]
DROP_BOX = ("Skip the mail. Use a drop box.", 44, INK)

T = {
    "ask": ["Old movies won't stop asking."],
    "ballot": ["On your ballot: 4A,", "the LPS mill levy override."],
    "favor": ["So, those in favor . . ."],
    "one": ["Think one ballot won't matter?"],
    "4a": ["On 4A, the LPS", "mill levy override . . ."],
    "kids": ["Kids can't vote on 4A."],
    "money": ["So there's no student vote", "on this money."],
    "adults": ["That leaves the grown-ups."],
    "counter": ["Ballot still on the counter?"],
    "tomorrow": ["Due tomorrow, 7 p.m."],
    "today": ["It's Election Day."],
    "tonight": ["Ballots due by 7 p.m. tonight."],
}

REELS = {
    # Fri Oct 30: the movies nag you.
    "1-old-movies-keep-asking": dict(beats=[
        ("archive/therecklessmoment1949", 3.00, 4.50, T["ask"], "How do you vote?", {}),
        ("archive/Kraft_Television--Keep_Our_Honor_Bright", 3.20, 4.85, T["ask"], "I didn't hear your vote, Matt.", {}),
        ("archive/gods-little-acre-1958", 3.25, 4.70, T["ask"], "Can it vote?", {}),
        ("archive/bodyandsoul1947", 2.30, 6.15, T["ask"],
         "Before we get lost in fun, don't forget to vote for the people's choice.", {}),
        ("archive/The_Green_Promise", 3.60, 6.00, T["ballot"], "Now we'll put it to a vote.", {}),
        ("archive/1934-midnight-chester-erskine-vo", 3.75, 5.75, T["ballot"], "All right, let's vote on the first question.", {}),
        ("archive/1939-persons-in-hiding-louis-king-vo", 3.65, 5.70, T["ballot"], "You've already got my vote.", {}),
        # The game-show host leaves only a 60ms gap before his next line.
        ("archive/Face_Game_Show_Stars", 4.25, 5.91, T["ballot"], "Bob will vote for ya, I'll tell ya.", {"fade_out": 0.05}),
        ("archive/ManOfTheMoment", 4.70, 7.20, T["favor"], "Those in favor, raise their hands.", {}),
        # The room voting yes has no dialogue; Salt of the Earth's chairman calls it.
        ("archive/ManOfTheMoment-long", 14.30, 17.00, T["favor"], "The ayes have it.",
         {"line_over": ("archive/SaltOfTheEarth_735", 2.85, 3.75, 0.9)}),
    ], end=("Your turn.", [*DUE_TUE, DROP_BOX])),

    # Sat Oct 31: one vote decides things.
    "2-one-vote": dict(beats=[
        ("all/002", 2.55, 8.70, T["one"], "How much of a plurality? One vote! Some landslide! I don't care, I won.", {}),
        ("all/043", 3.90, 8.50, T["4a"], "There's only one vote I care about. Will it be yes or no?", {}),
        ("all/000", 3.60, 5.00, T["4a"], "Yes, we vote for you.", {}),
    ], end=("One vote. Yours.", [*DUE_TUE, DROP_BOX])),

    # Sun Nov 1: kids can't vote, so it's on the adults.
    "3-kids-cant-vote": dict(beats=[
        # The audience laugh after the line is let ring and faded, not chopped.
        ("all/099", 3.55, 8.00, T["kids"], "Good heavens. I wouldn't see Chris until she was old enough to vote.",
         {"fade_out": 0.45}),
        ("all/021", 4.15, 8.85, T["money"],
         "...conducted a vote of the students to determine to what use this money should be put.", {}),
        ("archive/SaltOfTheEarth_735", 3.85, 6.22, T["adults"], "Now every adult is entitled to a vote.", {}),
    ], end=("They can't vote. You can.", [*DUE_TUE, ("Vote yes for them.", 44, INK)])),

    # Mon Nov 2: don't wait.
    "4-this-is-now": dict(beats=[
        # This print has Spanish subtitles burned into the bottom fifth; crop them off.
        ("all/095", 7.18, 10.95, T["counter"], "I'll vote for it at the next election. That's next November. This is now.",
         {"crop": "iw:ih*0.78:0:0"}),
        ("all/017", 0.10, 4.05, T["tomorrow"],
         "That gives us an overwhelming lead. Yes, but nothing's in the bag till the polls close.", {}),
    ], end=("This is now.", [("Ballots due by 7 p.m. tomorrow,", 48, GREEN), ("Tuesday, Nov. 3", 52, GREEN),
                              ("Drop yours off today.", 44, INK)])),

    # Tue Nov 3: Election Day.
    "5-election-day": dict(beats=[
        ("all/078-early", 6.06, 7.55, T["today"], "Time is up, and it's time now to vote.", {}),
        ("all/004", 0.75, 5.30, T["today"],
         "All right, got your hands all warmed up. You're the people who are going to do it now. We go for the vote.", {}),
        ("all/061", 5.45, 10.40, T["tonight"], "I have no more to say, because... well, I am confident how each of you will vote.", {}),
    ], end=("Vote yes.", [("Ballots due by 7 p.m. tonight.", 52, GREEN), ("Drop box or vote in person.", 44, INK)])),
}

STOP = set("""a an the and or but to of in on at for with is are was were be been it its this that
i you he she we they me my our your his her their them us so do did does not no yes oh uh um
just like well what will would can could i'm it's that's we're you're there here have has had
all ya""".split())
HOMOPHONES = {"eyes": "ayes", "'em": "them"}


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
    classic(d, title, SAFE_TOP + 40, 58, BOX_Y - 14)
    f = font(50, bold=False)
    lines = wrap(d, caption, f, W - 140)
    assert len(lines) <= 3, f"caption too long: {caption}"
    y = CAP_Y
    for line in lines:
        w = d.textlength(line, font=f)
        d.text(((W - w) / 2, y), line, font=f, fill="white", stroke_width=3, stroke_fill="black")
        y += 64
    assert y <= SAFE_BOTTOM, f"caption runs into the platform band: {caption}"
    return im


def words(text):
    return {HOMOPHONES.get(w, w) for w in re.findall(r"[a-z']+", text.lower())}


def src_of(name):
    return RAW / f"{name}.mov"


def crop_of(src, t0, t1):
    """The picture inside any letterbox/pillarbox over [t0, t1], by the most common cropdetect answer."""
    r = subprocess.run(["ffmpeg", "-ss", f"{t0:.3f}", "-t", f"{t1 - t0:.3f}", "-i", str(src),
                        "-vf", "cropdetect=24:2:0", "-an", "-f", "null", "-"], capture_output=True, text=True).stderr
    found = re.findall(r"crop=(\d+:\d+:\d+:\d+)", r)
    return max(set(found), key=found.count)


def heard(name, t0, t1, caption, opts):
    """Fraction of the caption's content words whisper hears in [t0, t1]; None = couldn't check."""
    want = words(caption) - STOP
    if not want or not MODEL.exists():
        return None
    if "line_over" in opts:
        name, t0, t1, _ = opts["line_over"]
    with tempfile.TemporaryDirectory() as td:
        wav = pathlib.Path(td) / "c.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t0:.2f}", "-t", f"{t1 - t0:.2f}",
                        "-i", str(src_of(name)), "-ar", "16000", "-ac", "1", str(wav)], check=True)
        r = subprocess.run(["whisper-cli", "-m", str(MODEL), "-f", str(wav), "-nt", "-np"],
                           capture_output=True, text=True)
    return len(want & words(r.stdout)) / len(want) if r.returncode == 0 else None


def segment(i, beat, td):
    name, t0, t1, title, caption, opts = beat
    src = src_of(name)
    crop = opts.get("crop") or crop_of(src, t0, t1)
    png = td / f"o{i}.png"
    overlay(title, caption).save(png)
    out = td / f"s{i}.mov"
    vf = (f"[0:v]crop={crop},scale={BOX_W}:{BOX_H}:force_original_aspect_ratio=decrease,setsar=1,fps={FPS},"
          f"pad={W}:{H}:{BOX_X}+({BOX_W}-iw)/2:{BOX_Y}+({BOX_H}-ih)/2:black[f];"
          f"[f][1:v]overlay=0:0,tpad=stop_mode=clone:stop_duration=0.2,format=yuv420p[v]")
    # Whole frames, and audio padded/trimmed to exactly that length, or sync drifts at every join.
    d, fo = round((t1 - t0) * FPS) / FPS, opts.get("fade_out", FADE_OUT)
    af = f"afade=t=in:d={FADE_IN},afade=t=out:st={d - fo:.3f}:d={fo},apad,atrim=0:{d:.6f}"
    extra = []
    if "line_over" not in opts:
        vf += f";[0:a]{af}[mix]"
    else:
        lsrc, l0, l1, at = opts["line_over"]
        extra = ["-ss", f"{l0:.3f}", "-t", f"{l1 - l0:.3f}", "-i", str(src_of(lsrc))]
        vf += (f";[2:a]afade=t=in:d=0.05,afade=t=out:st={l1 - l0 - 0.08:.3f}:d=0.08,"
               f"adelay={int(at * 1000)}:all=1[l];[0:a][l]amix=inputs=2:normalize=0:duration=first,{af}[mix]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t0:.3f}", "-t", f"{d:.3f}", "-i", str(src),
                    "-i", str(png), *extra, "-filter_complex", vf, "-map", "[v]", "-map", "[mix]",
                    "-frames:v", str(round(d * FPS)), "-c:v", "libx264", "-crf", "18", "-r", str(FPS),
                    "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2", str(out)], check=True)
    return out


def end_card(td, headline, rows, secs=5.0):
    im = Image.new("RGB", (W, H), SURFACE)
    d = ImageDraw.Draw(im)

    def centered(txt, size, y, fill_):
        f = font(size)
        w = d.textlength(txt, font=f)
        assert w <= W - 80, f"end card line too wide: {txt}"
        d.text(((W - w) / 2, y), txt, font=f, fill=fill_)

    size = 96
    while d.textlength(headline, font=font(size)) > W - 80:
        size -= 4
    centered(headline, size, 330 + (96 - size) // 2, INK)
    logo = Image.open(ROOT / "branding/yes-on-4a/stacked-light.png").convert("RGBA")
    logo = logo.resize((440, round(logo.height * 440 / logo.width)), Image.LANCZOS)
    im.paste(logo, ((W - logo.width) // 2, 500), logo)
    centered(MEASURE, 52, 900, INK)
    y = 1040
    for text, size, colour in rows:
        if colour is INK:
            y += 50
        centered(text, size, y, colour)
        y += 70
    assert y <= SAFE_BOTTOM, "end card runs into the platform band"
    png = td / "end.png"
    im.save(png)
    out = td / "end.mov"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", str(png), "-f", "lavfi",
                    "-i", "anullsrc=r=48000:cl=stereo", "-t", str(secs), "-vf", "format=yuv420p",
                    "-c:v", "libx264", "-crf", "18", "-r", str(FPS), "-c:a", "pcm_s16le", str(out)], check=True)
    return out


def has_audio(path):
    r = subprocess.run(["ffmpeg", "-i", str(path), "-af", "volumedetect", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    m = re.search(r"mean_volume: (-?[\d.]+) dB", r)
    return m and float(m[1]) > -60


def build(name):
    reel = REELS[name]
    beats = reel["beats"]
    print(name)
    for b in beats:
        s = heard(b[0], b[1], b[2], b[4], b[5])
        print(f"  heard {s if s is None else round(s, 2)}: {b[4]}")
        assert s is not None and s >= 0.6, f"caption not heard ({s}) at {b[0]} {b[1]}: {b[4]}"
    with tempfile.TemporaryDirectory() as td:
        td = pathlib.Path(td)
        parts = [segment(i, b, td) for i, b in enumerate(beats)] + [end_card(td, *reel["end"])]
        lst = td / "list.txt"
        lst.write_text("".join(f"file '{p}'\n" for p in parts))
        joined = td / "joined.mov"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst),
                        "-c", "copy", str(joined)], check=True)
        dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
                                    "csv=p=0", str(joined)], capture_output=True, text=True).stdout)
        out = OUT / f"{name}.mp4"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(joined), "-t", f"{dur:.6f}", "-c:v", "copy",
                        "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
                        "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", str(out)], check=True)
    assert has_audio(out), "render lost its audio"
    frames, t = [], 0.0
    for b in beats:
        d = round((b[2] - b[1]) * FPS) / FPS
        frames.append(t + d / 2)
        t += d
    frames.append(t + 2)
    picks = []
    for ft in frames:
        raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{ft:.2f}", "-i", str(out), "-frames:v", "1",
                              "-vf", "scale=270:480", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                             capture_output=True, check=True).stdout
        picks.append(Image.frombytes("RGB", (270, 480), raw))
    sheet = Image.new("RGB", (270 * 6, 480 * ((len(picks) + 5) // 6)), "white")
    for i, p in enumerate(picks):
        sheet.paste(p, ((i % 6) * 270, (i // 6) * 480))
    sheet.save(OUT / f"{name}-check.jpg")
    print(f"{out} {dur:.1f}s")


if __name__ == "__main__":
    for n in sys.argv[1:] or REELS:
        build(n)
