from PIL import Image, ImageOps, ImageFilter, ImageDraw, ImageFont

# crop boxes in 900x1200 (or 1200x900) preview coords: (x0, y0, size)
CROPS = [
    ('1', (165, 192, 400)),
    ('2', (60, 120, 700)),
    ('3', (370, 220, 480)),
    ('4', (160, 560, 520)),
    ('5', (200, 430, 560)),
    ('6', (350, 0, 440)),
    ('7', (665, 405, 345)),
    ('extra', (90, 100, 720)),
]
# regions to blur, in preview coords: (x0, y0, x1, y1)
BLUR = {
    '1': [(250, 125, 335, 190)],
    '3': [(800, 120, 880, 165)],
    '5': [(75, 195, 140, 235), (270, 230, 320, 320), (860, 55, 900, 95)],
    '7': [(55, 600, 195, 670)],
}
T = 720
GREEN = (76, 155, 47); INK = (57, 68, 74)
font = lambda s: ImageFont.truetype('/System/Library/Fonts/Supplemental/DIN Condensed Bold.ttf', s)

def tile(name, box):
    im = ImageOps.exif_transpose(Image.open(f'src/{name}.jpg')).convert('RGB')
    pw = 900 if im.width < im.height else 1200
    k = im.width / pw
    for (a, b, c, d) in BLUR.get(name, []):
        r = tuple(int(v * k) for v in (a, b, c, d))
        reg = im.crop(r).filter(ImageFilter.GaussianBlur(max(8, int(25 * k))))
        im.paste(reg, r[:2])
    x, y, s = box
    im = im.crop(tuple(int(v * k) for v in (x, y, x + s, y + s))).resize((T, T), Image.LANCZOS)
    return im

def badge(im, n):
    d = ImageDraw.Draw(im)
    r = 52; cx, cy = 28 + r, 28 + r
    d.ellipse((cx - r - 5, cy - r - 5, cx + r + 5, cy + r + 5), fill='white')
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=GREEN)
    d.text((cx, cy + 6), str(n), font=font(84), fill='white', anchor='mm')

G = 12
canvas = Image.new('RGB', (3 * T + 4 * G, 3 * T + 4 * G), 'white')
for i, (name, box) in enumerate(CROPS):
    t = tile(name, box); badge(t, i + 1)
    canvas.paste(t, (G + (i % 3) * (T + G), G + (i // 3) * (T + G)))

last = Image.new('RGB', (T, T), GREEN)
d = ImageDraw.Draw(last)
d.text((T // 2, 300), str(len(CROPS)), font=font(400), fill='white', anchor='mm')
d.text((T // 2, 520), 'SIGNS', font=font(96), fill=INK, anchor='mm')
d.text((T // 2, 610), 'ONE WALK', font=font(96), fill=INK, anchor='mm')
canvas.paste(last, (G + 2 * (T + G), G + 2 * (T + G)))
canvas.save('sign-count.jpg', quality=92)
canvas.resize((1080, 1080), Image.LANCZOS).save('preview.jpg', quality=88)
for name, _ in CROPS:
    pass
