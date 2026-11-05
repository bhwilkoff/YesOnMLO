#!/usr/bin/env python3
"""Builds POST-THIS.md and the by-day/ folders from ONE list, so the doc
and the files can't disagree. Edit DAYS below, then rerun:

    python3 private/instagram-launch/source-files/one-stop-shop/build_days.py
"""
import pathlib, shutil

KIT = pathlib.Path(__file__).resolve().parent.parent  # source-files/
TOP = KIT.parent
REPO = TOP.parent.parent
OUT = TOP / "by-day"

OSS = "one-stop-shop/"
PHO = "oss-photos/"
CARD = REPO / "assets/social/one-stop-shop-portrait.png"

TUE = """Ballots mail Friday. This week is the big push, and we've made it one stop.

Outside the district's forums, and at Arapahoe High on Saturday and Sunday mornings, you can get your car painted, take a yard sign home, write postcards, and pick up a lit-drop turf. (No door-knocking. You just leave it at the door.)

Tonight: Littleton High School, 5:00. The district's forum is inside. Bring a neighbor who has questions.

No RSVP. Yes on 4A, the LPS mill levy override. #YesOn4A #YesOnLPS"""

WED_IG = """$2 a month for every $100,000 your home is worth. That is Dr. Lambert's number on the district's podcast. On a $600,000 home, about $13 a month.

So, what does it buy? A 2% average raise for LPS staff. And March 19 goes back to being a school day.

Yes on 4A, the LPS mill levy override. Ballots mail Friday.

Tonight we're outside Arapahoe High, 5:30, with car paint, yard signs, and postcards. #YesOn4A #YesOnLPS"""

WED_FB = """Last night outside Littleton High. [ADD one real detail: whose car, how many signs went out]

Tonight is Arapahoe High School, 5:30. The district's forum is inside. We're outside with everything: car painting, yard signs, postcards to write, and lit-drop turfs.

Tomorrow is Euclid, 6:00. Then Arapahoe again Saturday and Sunday at 9:30 a.m. #YesOn4A"""

THU = """This is what a one-stop shop looks like. Paint going on a back window. Signs and buttons on a folding table outside Arapahoe High. Postcards getting written at a kitchen table.

Tonight is the last forum: Euclid Middle School, 6:00. The district's forum is inside. We're outside with car paint, yard signs, postcards to write, and lit-drop turfs. (No door-knocking. You just leave it at the door.)

Can't make it tonight? Arapahoe High, Saturday and Sunday at 9:30 a.m.

Yes on 4A, the LPS mill levy override. Ballots mail tomorrow. #YesOn4A #YesOnLPS"""

PHOTOS = [PHO + n for n in ("1-car-painting.jpg", "2-postcards.jpg", "3-table-close.jpg", "4-table-wide.jpg")]

FRI_IG = """I got such a lovely text message this morning from my local elections office. It means they have been thinking about me... voting!

We hope you are as excited as we are to vote yes on 4A, the LPS mill levy override.

Ballot drop boxes are everywhere. Find the one closest to you at the link in our Story today.

#YesOn4A #YesOnLPS"""

FRI_FB = """I got such a lovely text message this morning from my local elections office. It means they have been thinking about me... voting!

We hope you are as excited as we are to vote yes on 4A, the LPS mill levy override.

Ballot drop locations are abundant and can be found here: https://www.arapahoeco.gov/your_county/arapahoevotes/voting_locations/ballot_drop_locations.php

#YesOn4A"""

BALLOT = "ballot-text/ballot-text-post.jpg"

SAT_FB = """Your ballot is on its way. If you want to do one more thing before you fill it out, we're at Arapahoe High School this morning and tomorrow, both at 9:30.

Get a yard sign, pick up postcards to write, take a lit-drop turf for your street (no knocking), or get your car painted. #YesOn4A"""

SAT_IG = """15 seconds. Every dollar of 4A, the LPS mill levy override, stays in LPS.

Collected here. Spent in our schools. Decided by a board we elect.

Ballots are in the mail. #YesOn4A #YesOnLPS"""

SUN_IG = """A question we hear a lot: my property taxes went up, so doesn't LPS already get that money?

No. It works the other way. Under the School Finance Act, when local property taxes bring in more, the state pays less, and the total stays the same. Jonathan from the district's finance office explains it better than we can (57 seconds, from the district's podcast).

A mill levy override is different. It is local money. We vote on it, and it stays here.

#YesOn4A #YesOnLPS"""

SUN_FB = """Five tables, five days. [ADD a real count if anyone kept one: signs, postcards, turfs]

Thank you to everyone who came by. If you picked up a turf, this is the week to drop it. #YesOn4A"""

MON = """It comes down to teachers. Dr. Lambert said it plainly on the district's podcast: "We don't wanna lose them."

So, $2.5 million of 4A, the LPS mill levy override, goes to a 2% average raise. Your ballot is in the mail. #YesOn4A"""

TUE2_FB = """Your ballot is here, and maybe you still have questions. Good. Bring them.

Citizens for LPS is hosting two information meetings about 4A, the LPS mill levy override:
Thursday, Oct 8, 10:00 a.m., Koelbel Library
Friday, Oct 9, 9:30 a.m., Bemis Library

No RSVP. #YesOn4A"""

WED2 = """March 19, 2027. Every school, every office, every bus in LPS, closed for a day. That is how the district saves $800,000 this year. (One day of salaries costs more than that.)

If 4A, the LPS mill levy override, passes, March 19 is a school day again. #YesOn4A"""

THU2_FB = """This morning at 10:00 we're at Koelbel Library, talking about 4A, the LPS mill levy override. Bring your questions, and bring your ballot if you haven't filled it out yet.

Hosted by Citizens for LPS. Tomorrow: Bemis Library, 9:30. #YesOn4A"""

FRI2_FB = """Last one: Bemis Library, 9:30 this morning. Questions about 4A, the LPS mill levy override, are welcome, and so are the hard ones.

Hosted by Citizens for LPS. #YesOn4A"""

BD = "ballot-drop/out/"
NEAREST = "https://www.arapahoevotes.gov/Find-My-Nearest"

SAT3 = """I voted Wednesday. Signed the envelope, followed the blue signs to the drop box at Goodson Recreation Center, and that was it.

Yes on 4A, the LPS mill levy override.

(Leave the button at home when you drop. The box says no electioneering within 100 feet, and it means it.)

Your ballot is probably on your kitchen counter, waiting for you. #YesOn4A #YesOnLPS"""

SAT3_FB = SAT3.replace("#YesOn4A #YesOnLPS", "Find the drop box closest to you: " + NEAREST + " #YesOn4A")

MON3 = """My favorite drop box is at Goodson Recreation Center, 6315 S. University Blvd.

You don't actually need the address. Follow the blue signs with the red arrows. Past the trees. Past the rust-colored sculpture with the purple balls. And there it is.

Arapahoe County has 24-hour drop boxes all over. Find the one closest to you at the link in our Story.

Yes on 4A, the LPS mill levy override. Where's your favorite? #YesOn4A #YesOnLPS"""

MON3_FB = MON3.replace("at the link in our Story", "here: " + NEAREST).replace(" #YesOnLPS", "")

WED3 = """Folks ask us about drop boxes. The box answers most of it, right on the side.

Is it watched? By video, at all times.
Is it open at night? Yes. 24 hours a day, through Nov 3.
When does it close? 7 p.m. on election night.
Can I drop off my family's ballots too? Yes, up to 10 per person.

And one more, from the county's drop-box list that came with your ballot: "All valid ballots are counted in the same manner, regardless of the closeness or outcome of any race."

Yes on 4A, the LPS mill levy override. #YesOn4A"""

FRI3 = """Colorado doesn't count postmarks. Your ballot has to reach the county by 7 p.m. on Nov 3. (It's printed right on the envelope.)

So, why wait? Early leaves room for the things that go wrong: a ballot lost in the mail pile, a signature that needs fixing, a kid with a juice box.

Mine went in Wednesday. Yes on 4A, the LPS mill levy override. #YesOn4A #YesOnLPS"""

FRI3_FB = FRI3.replace(" #YesOnLPS", "")

MON4_FB = """Starting today, Voter Service and Polling Centers are open across Arapahoe County, Monday to Friday, 8 a.m. to 5 p.m.

Lost your ballot? Never got one? Moved? Go in. They can register you, give you a new ballot, or let you vote right there.

In Littleton: Arapahoe Community College, 5900 S. Santa Fe Dr. Check wait times before you go: """ + NEAREST + """

Yes on 4A, the LPS mill levy override. #YesOn4A"""

WK = "weekend/out/"
TURF = "lit-drop turf (no door-knocking, done by Monday)"

FRI4 = """One stop. Pick what you need.

Tomorrow and Sunday, 9:00 to 10:30 a.m., southwest parking lot at Arapahoe High School. Get your car painted, take a yard sign for your yard, or pick up a """ + TURF + """.

Yes on 4A, the LPS mill levy override. #YesOn4A #YesOnLPS"""

FRI4_FB = FRI4.replace(" #YesOnLPS", "")

DOGS = """This yard sign has a security detail. (They take the job very seriously. Mostly.)

Want one for your yard? Come see us Sunday morning, 9:00 to 10:30, in the southwest parking lot at Arapahoe High School. Yard signs, car paint, and lit-drop turfs.

Yes on 4A, the LPS mill levy override. #YesOn4A #YesOnLPS"""

DOGS_FB = DOGS.replace(" #YesOnLPS", "")

WALK = """Yard sign after yard sign, all down the block.

Want one? Sunday morning, 9:00 to 10:30, southwest parking lot at Arapahoe High School. Lit-drop turfs go out today too: no knocking, done by Monday.

Yes on 4A, the LPS mill levy override. #YesOn4A #YesOnLPS"""

TODAY = """This morning in the southwest lot at Arapahoe High. Paint going on a window, handwritten notes headed to neighbors, and a table with everything on it.

We're back tomorrow, Sunday, 9:00 to 10:30 a.m. Get your car painted, take a yard sign for your yard, or pick up a lit-drop turf (no door-knocking, done by Monday).

Yes on 4A, the LPS mill levy override. #YesOn4A #YesOnLPS"""

TODAY_FB = """What a morning at Arapahoe High! Paint going on a window, handwritten notes headed to neighbors, and a table with everything on it . . . thank you to everyone who came by.

We're back tomorrow, Sunday, 9:00 to 10:30 a.m., in the southwest parking lot. Car paint, yard signs, and lit-drop turfs (no door-knocking, done by Monday).

Yes on 4A, the LPS mill levy override. #YesOn4A"""

SATPICS = [WK + "sat-1-painting.jpg", WK + "sat-2-table.jpg", WK + "sat-3-notes.jpg"]

RECAP = """Two mornings in the southwest lot at Arapahoe High. Paint going on a window, handwritten notes headed to neighbors, and on Sunday, a crowd.

Thank you to everyone who came by.

Now the part that counts: your ballot. Fill it out, sign the envelope, and drop it at any 24-hour drop box. Yes on 4A, the LPS mill levy override. #YesOn4A #YesOnLPS"""

RECAP_FB = """Two mornings at Arapahoe High . . . thank you to everyone who came by! Paint going on a window, handwritten notes headed to neighbors, and on Sunday, a crowd.

(If you picked up a lit-drop turf, today's the day to finish it.)

Now the part that counts: your ballot. Fill it out, sign the envelope, and drop it at any 24-hour drop box. Find the closest one: """ + NEAREST + """

Yes on 4A, the LPS mill levy override. #YesOn4A"""

MONPICS = [WK + "mon-1-sunday.jpg", WK + "mon-2-painting.jpg", WK + "mon-3-table.jpg", WK + "mon-4-notes.jpg"]

SAT4 = """Room for one more window. (Or twenty.)

This morning, 9:00 to 10:30, southwest parking lot at Arapahoe High School. Car paint, yard signs, and lit-drop turfs. Swing by, even for five minutes!

Yes on 4A, the LPS mill levy override. #YesOn4A #YesOnLPS"""

SAT4_FB = SAT4.replace(" #YesOnLPS", "")

SUN4 = """Sunday morning, 9:00 to 10:30, southwest parking lot at Arapahoe High School. Bring the car. We'll bring the paint.

Lit-drop turfs go out today too: no knocking, done by Monday.

Yes on 4A, the LPS mill levy override. #YesOn4A #YesOnLPS"""

SUN4_FB = """Chance can't drive. So Chance can't get his car painted.

You can . . . this morning, 9:00 to 10:30, southwest parking lot at Arapahoe High School. Yard signs and lit-drop turfs too!

Yes on 4A, the LPS mill levy override. #YesOn4A"""

COUNTER = """Right now, on a lot of kitchen counters across LPS, there's an envelope that says Official Ballot Enclosed. And a booklet sitting right next to it.

Ballots started mailing October 2. If yours is still in the pile, this is your nudge.

Open the booklet and read the comments for 4A, the LPS mill levy override. Then fill out your ballot, sign the envelope, and drop it at any 24-hour drop box.

Yes on 4A. #YesOn4A #YesOnLPS"""

COUNTER_FB = """Is this on your kitchen counter right now? It's on a lot of them . . . the envelope that says Official Ballot Enclosed, and the booklet that came with it.

Ballots started mailing October 2. If yours is still sitting in the pile, this is your nudge.

Open the booklet and read the comments for 4A, the LPS mill levy override. Then fill out your ballot, sign the envelope, and drop it at any 24-hour drop box. Find the closest one: """ + NEAREST + """

Want to know more first? https://citizensforlps.org

Yes on 4A. #YesOn4A"""

REEL = "polls-reel/out/reel-scariest-things.mp4"

SCARY = """Scariest things around here this October, ranked. (Number one is the only one you can fix.)

If your ballot is still on the counter: fill it in, sign the envelope, and drop it in any 24-hour drop box. It has to be there by 7 p.m. on Tuesday, Nov 3.

Yes on 4A, the LPS mill levy override. #YesOn4A #YesOnLPS"""

SCARY_FB = """Scariest things around here this October, ranked . . . and number one is the only one you can fix!

If your ballot is still on the counter: fill it in, sign the envelope, and drop it in any 24-hour drop box by 7 p.m. Tuesday, Nov 3. Find the closest one: """ + NEAREST + """

Yes on 4A, the LPS mill levy override. #YesOn4A"""

SOUND = "The video is silent on purpose. Add a trending sound in the Reels editor before you post."

YB = "yearbook-scans/out/"
TEACH = [YB + f"teachers-{i}.jpg" for i in range(1, 6)]
HOME = [YB + f"homecoming-{i}.jpg" for i in range(1, 7)]
DUE = "Ballots due by 7 p.m. Tuesday, Nov. 3."
FB_DUE = DUE + " Find your nearest drop box: " + NEAREST + " #YesOn4A"
YES_YEARS = "1988, 1997, 2002, 2004, 2010, 2013, 2018 and 2020"

TEACH_IG = """Mrs. Gaspar graded papers with her pet owl. That's Littleton High School, 1984.

Everybody has one. The teacher who made you want to show up.

This community paid those teachers. It still does. And right now, LPS teachers are working under a wage freeze. 4A, the LPS mill levy override, lifts it with a 2% average raise.

So, who was yours? Tell us their name.

""" + DUE + " #YesOn4A #YesOnLPS"

TEACH_FB = """Who was your favorite LPS teacher? Mrs. Gaspar graded papers with her pet owl . . . Littleton High School, 1984.

This community paid those teachers. It still does. And right now, LPS teachers are working under a wage freeze. 4A, the LPS mill levy override, lifts it with a 2% average raise.

Tell us your teacher's name in the comments!

""" + FB_DUE

HARDY_IG = """In 1984, somebody asked Mr. Hardy what computers would be like in the year 2000. His answer is right there in the Littleton High School yearbook: \u201cHouses will probably be run by computers.\u201d

He wasn't wrong. LHS already offered three computer classes that year, AP included. Teachers were getting kids ready for a world nobody could see yet.

They still are. 4A, the LPS mill levy override, funds career-readiness programs, so today's students are ready for whatever comes next.

""" + DUE + " #YesOn4A #YesOnLPS"

HARDY_FB = """1984: Mr. Hardy at Littleton High School predicts that by the year 2000, \u201chouses will probably be run by computers.\u201d

He wasn't wrong! LHS already offered three computer classes that year, AP included . . . teachers getting kids ready for a world nobody could see yet.

They still are. 4A, the LPS mill levy override, funds career-readiness programs, so today's students are ready for whatever comes next.

""" + FB_DUE

HOME_IG = """Remember homecoming? The king and queen at Littleton High School in 1984. The drama club's float. The band. Heritage, between quarters, 1981. The Arapahoe crowd in 1973.

Somebody paid for all of it: the teachers, the coaches, the band directors. Today's LPS kids deserve the same.

Now it's our turn. Tag someone who was there.

Yes on 4A, the LPS mill levy override. """ + DUE + " #YesOn4A #YesOnLPS"

HOME_FB = """Remember homecoming? Littleton High School's king and queen in 1984 . . . the drama club's float . . . Heritage between quarters in 1981 . . . and the Arapahoe crowd in 1973.

Somebody paid for all of it: the teachers, the coaches, the band directors. Today's LPS kids deserve the same.

Now it's our turn. Tag someone who was there!

Yes on 4A, the LPS mill levy override. """ + FB_DUE

EVERY_IG = """Littleton Boulevard, 1982. The homecoming parade, marching right past the House of Pancakes.

This community has been showing up for its schools for a long time. Since 1988, every time LPS has asked, voters said yes: """ + YES_YEARS + """.

Somebody did it for us. Now it's our turn.

Yes on 4A, the LPS mill levy override. """ + DUE + " #YesOn4A #YesOnLPS"

EVERY_FB = """Littleton Boulevard, 1982 . . . the homecoming parade, marching right past the House of Pancakes!

Since 1988, every time LPS has asked, voters said yes: """ + YES_YEARS + """.

Somebody did it for us. Now it's our turn.

Yes on 4A, the LPS mill levy override. """ + FB_DUE

SHARE = "Share the post to your Story (paper-airplane button, Add to story)."

VM = "vote-movies/out/"
SOUND_ON = "Leave the original movie sound on. The lines are the joke, and they're captioned for anyone watching muted."
STORY_LINK = SHARE + " Add a link sticker: " + NEAREST + " (sticker text: Drop boxes)."

MOV1_IG = """Old movies have been nagging folks to vote for decades. (Bob will vote for ya, I'll tell ya.)

So, those in favor: 4A, the LPS mill levy override, is on your ballot. Fill in yes and turn it in.

""" + DUE + " Skip the mail. Use a drop box. #YesOn4A #YesOnLPS"

MOV1_FB = """Old movies have one thing to say . . . vote. (Bob will vote for ya, I'll tell ya.)

4A, the LPS mill levy override, is on your ballot. Those in favor, fill in yes and turn it in!

""" + FB_DUE

MOV2_IG = """“How much of a plurality?” “One vote!” “Some landslide!”

One ballot doesn't feel like much. But every election gets counted the same way: one at a time.

On 4A, the LPS mill levy override, yours counts. Vote yes.

""" + DUE + " Skip the mail. Use a drop box. #YesOn4A #YesOnLPS"

MOV2_FB = """“How much of a plurality?” “One vote!” “Some landslide!” . . .

One ballot doesn't feel like much. But every election gets counted the same way: one at a time.

On 4A, the LPS mill levy override, yours counts. Vote yes!

""" + FB_DUE

MOV3_IG = """LPS students don't get a vote on 4A, the LPS mill levy override. Not even the ones it's for.

So it's on us. The district says a yes keeps teacher pay competitive with a 2% average raise, and gives students March 19 back as a school day.

They can't vote. You can. """ + DUE + " #YesOn4A #YesOnLPS"

MOV3_FB = """LPS students don't get a vote on 4A, the LPS mill levy override . . . not even the ones it's for.

So it's on us. The district says a yes keeps teacher pay competitive with a 2% average raise, and gives students March 19 back as a school day.

They can't vote. You can! """ + FB_DUE

MOV4_IG = """“I'll vote for it at the next election.” “That's next November. This is now.”

If your ballot is still on the counter, tomorrow is the last day. It has to reach the county by 7 p.m. Tuesday, and it's too late to mail it.

So, drop it off today. Yes on 4A, the LPS mill levy override. The closest drop box is at the link in our Story. #YesOn4A #YesOnLPS"""

MOV4_FB = """“I'll vote for it at the next election.” “That's next November. This is now.”

If your ballot is still on the counter, tomorrow is the last day. It has to reach the county by 7 p.m. Tuesday, and it's too late to mail it . . . so drop it off today!

Yes on 4A, the LPS mill levy override. Find your nearest drop box: """ + NEAREST + " #YesOn4A"

MOV5_IG = """It's Election Day. Time is up, and it's time now to vote.

Ballots have to be in by 7 p.m. tonight. Drop yours in any drop box, or vote in person at a Voter Service and Polling Center.

Already voted? Thank you. Now text one friend who hasn't.

Yes on 4A, the LPS mill levy override. The closest drop box is at the link in our Story. #YesOn4A #YesOnLPS"""

MOV5_FB = """It's Election Day! Time is up, and it's time now to vote.

Ballots have to be in by 7 p.m. tonight. Drop yours in any drop box, or vote in person at a Voter Service and Polling Center. Find the closest: """ + NEAREST + """

Already voted? Thank you . . . now text one friend who hasn't.

Yes on 4A, the LPS mill levy override. #YesOn4A"""

TITLE = "What to post: the 4A celebration"

VIC = "victory/out/"
SILENT = "Silent on purpose. Add a sound in the Reels editor before you post."

CAROUSEL = """Instagram:

It took paint pens. It took yard signs. It took folding tables in parking lots and kitchen tables at home. It took all of us.

4A, the LPS mill levy override, passed. The wage freeze lifts, LPS staff get a 2% average raise, and March 19 goes back to being a school day.

To everyone who said yes: thank you. To everyone who said no: LPS is still your district. Keep asking good questions. #YesOn4A #YesOnLPS


Facebook:

4A, the LPS mill levy override, passed!!!

It took paint pens, yard signs, folding tables, kitchen tables & a whole lot of neighbors . . . thank you!!

The wage freeze lifts, LPS staff get a 2% average raise & March 19 goes back to being a school day. #YesOn4A"""

REEL = """Instagram:

This is what it looks like when neighbors do the work.

4A, the LPS mill levy override, passed. Thank you. #YesOn4A #YesOnLPS


Facebook:

This is what it looks like when neighbors do the work . . .

4A, the LPS mill levy override, passed. Thank you, thank you, thank you! #YesOn4A"""

WASH = """Instagram:

You can wash your car now. (Or don't. We won't tell.)

Thank you for driving around with 4A, the LPS mill levy override, on your back window all fall. #YesOn4A #YesOnLPS


Facebook:

You can wash your car now . . . or don't. We won't tell!

Thank you for driving around with 4A, the LPS mill levy override, on your back window all fall. #YesOn4A"""

NEIGHBORS = """Instagram and Facebook:

Neighbors did this. Thank you for everything you gave to 4A, the LPS mill levy override. #YesOn4A #YesOnLPS"""

DAYS = [
    ("01 It passed - final set", "Everything in posting order, about an hour apart. The same files go to Instagram and Facebook, posted natively to each.", [
        ("First", "Carousel", [VIC + f"carousel-{i}.jpg" for i in range(1, 9)], CAROUSEL, None),
        ("Second", "Reel", VIC + "reel-it-took-all-of-us.mp4", REEL, SILENT),
        ("Third", "Photo post", VIC + "wash-your-car.jpg", WASH, None),
        ("Fourth", "Photo post", VIC + "thank-you-feed.jpg", NEIGHBORS, None),
        ("Through the day", "Instagram Stories", [VIC + n for n in ("story-count.jpg", "story-last-night.jpg", "story-wash.jpg", "story-thank-you.jpg")], None, "One after each feed post. Also share the Reel to your Story."),
        ("Any time", "Facebook cover", VIC + "facebook-cover.jpg", None, "Everything sits in the middle so it survives the phone crop."),
    ]),
]

def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    doc = ["# " + TITLE, "",
           "Everything is in `by-day/`. The files are numbered in the order you post them, "
           "and `captions.txt` has the text ready to copy.", "",
           "Post the same files natively to each platform. Don't share a post from one into the other.", ""]
    for label, intro, posts in DAYS:
        folder = OUT / label
        folder.mkdir()
        doc += ["---", "", f"## {label}", ""]
        if intro:
            doc += [intro, ""]
        txt = [label, "=" * len(label), ""]
        for n, (when, where, src, cap, note) in enumerate(posts, 1):
            names = []
            srcs = src if isinstance(src, list) else [src] if src else []
            for k, one in enumerate(srcs):
                one = pathlib.Path(one) if pathlib.Path(one).is_absolute() else KIT / one
                tag = f"{n}{'abcdefgh'[k]}" if len(srcs) > 1 else f"{n}"
                names.append(f"{tag} - {where} - {when}".replace("+", "and").replace(".", "").rstrip() + one.suffix)
                shutil.copy2(one, folder / names[-1])
            name = ", ".join(names)
            head = f"**{n}. {when}: {where}**" + ("  " + ", ".join(f"`{x}`" for x in names) if names else "  (no file)")
            doc += [head]
            txt += [f"{n}. {when}: {where}" + (f"   [{name}]" if name else "")]
            if note:
                doc += ["", note]
                txt += [note]
            if cap:
                doc += [""] + ["> " + l if l else ">" for l in cap.split("\n")]
                txt += ["", cap]
            doc += [""]
            txt += ["", ""]
        (folder / "captions.txt").write_text("\n".join(txt))
    (TOP / "POST-THIS.md").write_text("\n".join(doc))


main()
