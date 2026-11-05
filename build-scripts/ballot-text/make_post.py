#!/usr/bin/env python3
"""The county's ballot-mailed text, set on a 1080x1350 Instagram card."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BG = (30, 30, 30)
W, H = 1080, 1350
shot = Image.open("screenshot.png").convert("RGB")
w = 980
shot = shot.resize((w, round(shot.height * w / shot.width)), Image.LANCZOS).filter(
    ImageFilter.UnsharpMask(radius=1.2, percent=60, threshold=2))

card = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(card)
big = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 64, index=1)
small = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 46, index=1)

y = (H - shot.height) // 2 + 40
head = "Your ballot is on its way."
d.text((W // 2, y - 90), head, font=big, fill="white", anchor="ms")
card.paste(shot, ((W - w) // 2, y))
d.text((W // 2, y + shot.height + 110), "Vote yes on 4A.", font=small, fill=(76, 155, 47), anchor="ms")
card.save("ballot-text-post.jpg", quality=94)
