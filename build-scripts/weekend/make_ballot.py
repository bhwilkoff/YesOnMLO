#!/usr/bin/env python3
"""Thu Oct 15: the ballot envelope and the county's information booklet,
as a 4:5 feed photo. Blurs the envelope's barcode and mail code.

    python3 private/instagram-launch/source-files/weekend/make_ballot.py
"""
from make_today import load, blur, crop45, OUT

im = load("ballot/IMG_6808.jpeg")
im = blur(im, [(0.095, 0.400, 0.265, 0.462)])
crop45(im, 0.5, 0.5).save(OUT / "thu-ballot-counter.jpg", quality=92)
