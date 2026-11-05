#!/usr/bin/env python3
"""4:5 (1080x1350) crops of the volunteer photos for the IG carousel / FB post.
Blurs the handwritten mailing addresses on the postcards."""
import pathlib
from PIL import Image, ImageFilter, ImageOps

LIB = pathlib.Path.home() / "Pictures/Photos Library.photoslibrary/resources/derivatives"
HERE = pathlib.Path(__file__).resolve().parent

# name, source, crop box (x0, y0) with 4:5 width/height derived, blur boxes (source coords)
PHOTOS = [
    ("1-car-painting", "A/A2D32E53-3E75-4AA4-A624-FD1B69097CA8_1_102_o.jpeg", (0, 0, 1229, 1536), []),
    ("2-postcards", "D/DC6E8387-8915-46A9-A5B7-40FA341C9E48_1_102_o.jpeg", (500, 0, 1729, 1536),
        [(1060, 1150, 1175, 1320), (1640, 1390, 1775, 1500)]),
    ("3-table-close", "2/29105383-5456-4900-AE26-2EC4534CB6D4_1_102_o.jpeg", (0, 128, 1536, 2048), []),
    ("4-table-wide", "8/884F3055-93C9-4555-88C4-4A19DB19BF6D_1_102_o.jpeg", (0, 128, 1536, 2048), []),
]

for name, src, box, blurs in PHOTOS:
    im = ImageOps.exif_transpose(Image.open(LIB / src)).convert("RGB")
    for b in blurs:
        im.paste(im.crop(b).filter(ImageFilter.GaussianBlur(14)), b[:2])
    im.crop(box).resize((1080, 1350), Image.LANCZOS).save(HERE / f"{name}.jpg", quality=92)
    print(name)
