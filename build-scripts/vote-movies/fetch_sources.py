#!/usr/bin/env python3
"""Pull each beat's source window from archive.org (per Vote.archiveproj), padded 3s each side,
so cuts can land in natural pauses instead of the app's subtitle-tight edges."""
import json, pathlib, subprocess, sys
HERE = pathlib.Path(__file__).resolve().parent
PROJ = pathlib.Path.home() / "Downloads/Vote.archiveproj/timeline.json"
OUT = HERE / "raw/archive"
OUT.mkdir(parents=True, exist_ok=True)
PAD = 3.0
WANT = ["therecklessmoment1949", "Kraft_Television--Keep_Our_Honor_Bright", "gods-little-acre-1958",
        "bodyandsoul1947", "1934-midnight-chester-erskine-vo", "1939-persons-in-hiding-louis-king-vo",
        "Face_Game_Show_Stars", "ManOfTheMoment", "SaltOfTheEarth_735",
        "stagecoach-colorized", "1934-midnight-chester-erskine-ve", "The_Green_Promise"]
clips = {c["catalogItemID"]: c for c in json.loads(PROJ.read_text())["timeline"]["clips"]}
meta = {}
for cid in WANT:
    c = clips[cid]
    s = c["sourceRange"]["start"]; d = c["sourceRange"]["duration"]
    t0 = s["value"] / s["timescale"]; dur = d["value"] / d["timescale"]
    w0 = max(0.0, t0 - PAD)
    out = OUT / f"{cid}.mov"
    if not out.exists():
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{w0:.3f}", "-i", c["sourceURL"], "-t", f"{dur + 2 * PAD:.3f}",
                        "-c:v", "libx264", "-crf", "14", "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2", str(out)], check=True)
    meta[cid] = {"window_start": w0, "app_in": t0 - w0, "app_out": t0 - w0 + dur, "label": c["label"], "url": c["sourceURL"]}
    print(cid, meta[cid]["app_in"], meta[cid]["app_out"], file=sys.stderr)
(OUT / "windows.json").write_text(json.dumps(meta, indent=1))
