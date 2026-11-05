#!/usr/bin/env python3
"""Forum-week + weekend one-stop-shop Stories, in Instagram's Classic text
style (black on a white highlight) over the launch kit's CLEAN photos.

    python3 private/instagram-launch/source-files/one-stop-shop/make_stories.py
"""
import pathlib
from PIL import Image, ImageDraw, ImageFont

HERE = pathlib.Path(__file__).resolve().parent
KIT = HERE.parent  # source-files/
FONT = "/System/Library/Fonts/Helvetica.ttc"


def font(size):
    return ImageFont.truetype(FONT, size, index=1)  # Helvetica Bold


def block(draw, lines, top, size, gap=10, pad_x=18, pad_y=8, spacer=None):
    """Draw centred lines, each on its own white rounded highlight.
    An empty string is a blank spacer line."""
    f = font(size)
    asc, desc = f.getmetrics()
    h = asc + desc
    y = top
    for line in lines:
        if not line:
            y += spacer or h // 2
            continue
        w = draw.textlength(line, font=f)
        x = (1080 - w) / 2
        draw.rounded_rectangle(
            (x - pad_x, y - pad_y, x + w + pad_x, y + h + pad_y), radius=14, fill="white"
        )
        draw.text((x, y), line, font=f, fill="black")
        y += h + 2 * pad_y + gap - 8
    return y


def story(bg, out, blocks):
    im = Image.open(KIT / bg if "/" in bg else KIT / "launch-kit" / bg).convert("RGB").resize((1080, 1920))
    d = ImageDraw.Draw(im)
    for lines, top, size in blocks:
        block(d, lines, top, size)
    im.save(HERE / out, quality=92)
    print(out)


OFFER = ["Paint your car.", "Grab a yard sign.", "Write postcards.", "Pick up a lit-drop turf.", "(No door-knocking.)"]

# The week, then the weekend, on the table-of-supplies photo.
story("story6-paint-my-car-CLEAN.jpg", "story-oss-week.jpg", [
    (["One stop.", "Everything you need", "for Yes on 4A."], 220, 64),
    (OFFER, 700, 50),
    (["Tue 9/29  Littleton HS  5:00", "Wed 9/30  Arapahoe HS  5:30",
      "Thu 10/1  Euclid MS  6:00", "Sat 10/3  Arapahoe HS  9:30am",
      "Sun 10/4  Arapahoe HS  9:30am"], 1290, 46),
])

# "Tonight" stories, one per forum. The district's forum is inside;
# the table outside is ours. Both halves stay in the same breath.
tonight = [
    ("story4-forums-CLEAN.jpg", "story-oss-TONIGHT-littleton-9-29.jpg",
     ["Tonight. The district's forum is", "inside Littleton High School, 5:00."]),
    ("cars/story-cars-yours-CLEAN.jpg", "story-oss-TONIGHT-arapahoe-9-30.jpg",
     ["Tonight. The district's forum is", "inside Arapahoe High School, 5:30."]),
    ("cars/story-cars-poll-CLEAN.jpg", "story-oss-TONIGHT-euclid-10-1.jpg",
     ["Tonight. The district's forum is", "inside Euclid Middle School, 6:00.", "Last one before ballots mail."]),
]
for bg, out, head in tonight:
    # The Euclid photo is two cars stacked; its lower window sits where
    # the other photos have empty body panel, so the text goes in the sky.
    story(bg, out, [
        (head, 200, 52),
        (["We're outside with everything:", "car paint, yard signs, postcards,", "and lit-drop turfs.", "", "Bring a neighbor with questions."], 990 if "euclid" in out else 1340, 48),
    ])

# Weekend pickups. Ballots are in mailboxes by now.
for day, date, out in [("Saturday", "10/3", "story-oss-SATURDAY-arapahoe-10-3.jpg"),
                       ("Sunday", "10/4", "story-oss-SUNDAY-arapahoe-10-4.jpg")]:
    story("story4-forums-CLEAN.jpg" if day == "Saturday" else "cars/story-cars-yours-CLEAN.jpg", out, [
        ([f"{day} morning, 9:30.", "Arapahoe High School."], 200, 60),
        (["Ballots are in mailboxes.", "Come get your yard sign,", "postcards, a lit-drop turf,", "or your car painted."], 1340, 50),
    ])

# The committee's own information meetings. Ours, not the district's:
# the Stories say "hosted by Citizens for LPS" every time.
story("story1-hello-CLEAN.jpg", "story-meetings-both.jpg", [
    (["Got questions about 4A,", "the LPS mill levy override?", "Bring them."], 200, 56),
    (["Thu 10/8  Koelbel Library  10:00am", "Fri 10/9  Bemis Library  9:30am", "", "Hosted by Citizens for LPS."], 1600, 44),
])
story("story5-add-yours-CLEAN.jpg", "story-meeting-koelbel-10-8.jpg", [
    (["This morning, 10:00.", "Koelbel Library."], 200, 60),
    (["Questions about 4A, the LPS", "mill levy override? Bring them.", "", "Hosted by Citizens for LPS."], 1440, 48),
])
story("story2-cbs-CLEAN.jpg", "story-meeting-bemis-10-9.jpg", [
    (["This morning, 9:30.", "Bemis Library."], 200, 60),
    (["Questions about 4A, the LPS", "mill levy override? Bring them.", "", "Hosted by Citizens for LPS."], 1440, 48),
])

# Oct 10 + 11 one-stop shops (Amy's 10/9 email): 9:00-10:30 a.m., the
# southwest parking lot at Arapahoe High. Lit drops are due 10/12.
WHERE = ["Arapahoe High School,", "southwest parking lot."]
story("story6-paint-my-car-CLEAN.jpg", "story-oss-weekend-10-10-11.jpg", [
    (["Saturday + Sunday", "9:00 to 10:30 a.m."] + WHERE, 200, 56),
    (["Lit-drop turfs.", "No knocking. Done by Monday.", "", "Yard signs and car paint too."], 1340, 48),
])
story("story4-forums-CLEAN.jpg", "story-oss-TODAY-arapahoe-10-10.jpg", [
    (["This morning,", "9:00 to 10:30."] + WHERE, 200, 58),
    (["Take a lit-drop turf.", "Take a yard sign.", "Get your car painted."], 1340, 50),
])
story("cars/story-cars-yours-CLEAN.jpg", "story-oss-LAST-arapahoe-10-11.jpg", [
    (["Sunday morning,", "9:00 to 10:30."] + WHERE, 200, 58),
    (["Lit-drop turfs go out today.", "Drop them by Monday.", "", "Car not painted yet? Come by."], 1340, 48),
])
