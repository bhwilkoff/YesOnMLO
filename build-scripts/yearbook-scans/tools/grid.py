#!/usr/bin/env python3
"""Render chosen pages side by side for a closer look: grid.py out.jpg book:page ..."""
import sys, subprocess, tempfile, pathlib
from PIL import Image, ImageDraw, ImageFont
HERE = pathlib.Path(__file__).resolve().parent.parent
font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 26)
ims = []
with tempfile.TemporaryDirectory() as tmp:
    for spec in sys.argv[2:]:
        book, p = spec.split(":")
        pdf = next((HERE / "raw").glob(f"*{book}*.pdf"))
        subprocess.run(["pdftoppm", "-r", "55", "-jpeg", "-f", p, "-l", p, str(pdf), f"{tmp}/x"], check=True)
        f = sorted(pathlib.Path(tmp).glob("x-*.jpg"))[0]
        im = Image.open(f).convert("RGB"); f.unlink()
        d = ImageDraw.Draw(im); d.text((6, 4), spec, fill="red", font=font)
        ims.append(im)
w = sum(i.width for i in ims); h = max(i.height for i in ims)
sheet = Image.new("RGB", (w, h), "white"); x = 0
for i in ims: sheet.paste(i, (x, 0)); x += i.width
sheet.save(sys.argv[1], quality=85)
