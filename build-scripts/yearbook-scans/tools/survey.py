#!/usr/bin/env python3
"""Contact sheets of every yearbook page (numbered) for picking.

    python3 private/instagram-launch/source-files/yearbook-scans/tools/survey.py
"""
import pathlib, subprocess, tempfile
from PIL import Image, ImageDraw, ImageFont

HERE = pathlib.Path(__file__).resolve().parent.parent
RAW, OUT = HERE / "raw", HERE / "survey"
COLS, TW, TH, PER = 8, 240, 310, 48
font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 22)

for pdf in sorted(RAW.glob("*.pdf")):
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(["pdftoppm", "-r", "18", "-jpeg", str(pdf), f"{tmp}/p"], check=True)
        pages = sorted(pathlib.Path(tmp).glob("p-*.jpg"), key=lambda p: int(p.stem.split("-")[1]))
        for s in range(0, len(pages), PER):
            chunk = pages[s:s + PER]
            rows = -(-len(chunk) // COLS)
            sheet = Image.new("RGB", (COLS * TW, rows * (TH + 26)), "white")
            d = ImageDraw.Draw(sheet)
            for i, p in enumerate(chunk):
                im = Image.open(p); im.thumbnail((TW - 6, TH - 6))
                x, y = (i % COLS) * TW, (i // COLS) * (TH + 26)
                sheet.paste(im, (x + 3, y + 26))
                d.text((x + 4, y + 1), p.stem.split("-")[1], fill="red", font=font)
            sheet.save(OUT / f"{pdf.stem}_{s // PER:02d}.jpg", quality=80)
    print(pdf.stem, len(pages))
