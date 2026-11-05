#!/usr/bin/env python3
"""Timestamped contact sheets: one thumb every STEP s (labels are the frame's true pts), 10x10 per sheet."""
import pathlib, re, subprocess, sys
from PIL import Image, ImageDraw, ImageFont
src, tag, step, out = sys.argv[1], sys.argv[2], float(sys.argv[3]), pathlib.Path(sys.argv[4])
TW, TH = 192, 141
r = subprocess.run(["ffmpeg", "-i", src, "-vf",
                    f"select='isnan(prev_selected_t)+gte(t-prev_selected_t\\,{step})',showinfo,scale={TW}:{TH}",
                    "-vsync", "0", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True)
pts = [float(m) for m in re.findall(rb"pts_time:([\d.]+)", r.stderr)]
sz = TW * TH * 3
thumbs = [Image.frombytes("RGB", (TW, TH), r.stdout[i:i + sz]) for i in range(0, len(r.stdout) - sz + 1, sz)]
f = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 16)
for s in range(0, len(thumbs), 100):
    sheet = Image.new("RGB", (TW * 10, (TH + 18) * 10), "white")
    d = ImageDraw.Draw(sheet)
    for k, t in enumerate(thumbs[s:s + 100]):
        x, y = (k % 10) * TW, (k // 10) * (TH + 18)
        sheet.paste(t, (x, y + 18))
        d.text((x + 2, y), f"{pts[s + k]:.1f}", font=f, fill="black")
    sheet.save(out / f"{tag}_{s // 100:02d}.jpg", quality=80)
print(len(thumbs), "thumbs")
