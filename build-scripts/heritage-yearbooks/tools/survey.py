#!/usr/bin/env python3
"""Timestamped contact sheets: one thumb every STEP s, 10x10 per sheet."""
import pathlib, subprocess, sys
from PIL import Image, ImageDraw, ImageFont
src, tag, step = sys.argv[1], sys.argv[2], float(sys.argv[3])
out = pathlib.Path(sys.argv[4])
dur = float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",src],capture_output=True,text=True).stdout)
TW, TH = 192, 144
raw = subprocess.run(["ffmpeg","-v","error","-i",src,"-vf",f"fps=1/{step},scale={TW}:{TH}","-f","rawvideo","-pix_fmt","rgb24","-"],capture_output=True,check=True).stdout
sz = TW*TH*3
thumbs = [Image.frombytes("RGB",(TW,TH),raw[i:i+sz]) for i in range(0,len(raw)-sz+1,sz)]
f = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 16)
per = 100
for s in range(0, len(thumbs), per):
    sheet = Image.new("RGB", (TW*10, (TH+18)*10), "white")
    d = ImageDraw.Draw(sheet)
    for k, t in enumerate(thumbs[s:s+per]):
        i = s + k
        x, y = (k % 10)*TW, (k//10)*(TH+18)
        sheet.paste(t, (x, y+18))
        sec = i*step + step/2
        d.text((x+2, y), f"{int(sec//60)}:{sec%60:04.1f}", font=f, fill="black")
    sheet.save(out / f"{tag}_{s//per:02d}.jpg", quality=80)
