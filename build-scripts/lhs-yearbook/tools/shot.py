#!/usr/bin/env python3
"""Print the shot around each SRC@T: shot bounds by frame-difference spikes within +-8 s.
    python3 shot.py 93@252 97@36 ...
"""
import subprocess, sys, statistics, pathlib
RAW = pathlib.Path(__file__).resolve().parent.parent / "raw"
IDS = {"lhs": "gjwtgyEF8Gw"}
FPS, W, H = 30, 64, 48
def shot(tag, t):
    t0 = max(0, t - 8)
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t0}", "-t", "16", "-i", str(RAW / f"{IDS[tag]}.mp4"),
                          "-vf", f"fps={FPS},scale={W}:{H},format=gray", "-f", "rawvideo", "-"],
                         capture_output=True, check=True).stdout
    n = W * H
    fr = [raw[i:i + n] for i in range(0, len(raw) - n + 1, n)]
    d = [sum(abs(a - b) for a, b in zip(fr[i], fr[i - 1])) / n for i in range(1, len(fr))]
    med = statistics.median(d)
    cut = [i + 1 for i, v in enumerate(d) if v > max(10, 5 * med)]
    k = round((t - t0) * FPS)
    a = max([c for c in cut if c <= k], default=0)
    b = min([c for c in cut if c > k], default=len(fr))
    return t0 + a / FPS, t0 + b / FPS, med
for arg in sys.argv[1:]:
    tag, t = arg.split("@")
    a, b, med = shot(tag, float(t))
    print(f"{arg:10s} shot {a:8.2f} - {b:8.2f}  ({b - a:4.1f}s, med diff {med:.1f})")
