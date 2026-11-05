#!/usr/bin/env python3
"""Pull EVERY clip in Vote.archiveproj from archive.org with 4s padding, for planning the series.
Skips sources that can't be used at all (lectures, wrestling, 9/11, modern rips)."""
import json, pathlib, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
HERE = pathlib.Path(__file__).resolve().parent
PROJ = pathlib.Path.home() / "Downloads/Vote.archiveproj/timeline.json"
OUT = HERE / "raw/all"
OUT.mkdir(parents=True, exist_ok=True)
PAD = 4.0
SKIP = ("MIT", "HgE2qInDXQ8", "911-Chronology", "Zeitgeist", "roped.-2020", "kitten.-with", "Computer_6",
        "satte", "sadaa", "Tenderness", "LionOfTheDesert", "mithowtospeak")
clips = json.loads(PROJ.read_text())["timeline"]["clips"]
clips.sort(key=lambda c: c["timelineStart"]["value"] / c["timelineStart"]["timescale"])
meta = []
def get(i_c):
    i, c = i_c
    s = c["sourceRange"]["start"]; d = c["sourceRange"]["duration"]
    t0 = s["value"] / s["timescale"]; dur = d["value"] / d["timescale"]
    w0 = max(0.0, t0 - PAD)
    key = f"{i:03d}"
    out = OUT / f"{key}.mov"
    if not out.exists():
        r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{w0:.3f}", "-i", c["sourceURL"], "-t", f"{dur + 2 * PAD:.3f}",
                            "-c:v", "libx264", "-crf", "16", "-preset", "veryfast", "-c:a", "pcm_s16le", "-ar", "48000",
                            "-ac", "2", str(out)], capture_output=True, text=True)
        if r.returncode:
            print("FAIL", key, c["catalogItemID"], r.stderr[-200:], file=sys.stderr)
            return None
    return {"key": key, "id": c["catalogItemID"], "label": c["label"], "url": c["sourceURL"],
            "window_start": w0, "app_in": t0 - w0, "app_out": t0 - w0 + dur}
todo = [(i, c) for i, c in enumerate(clips) if not any(k in c["catalogItemID"] for k in SKIP)]
with ThreadPoolExecutor(6) as ex:
    meta = [m for m in ex.map(get, todo) if m]
(OUT / "index.json").write_text(json.dumps(meta, indent=1))
print(len(todo), "wanted,", len(meta), "fetched")
