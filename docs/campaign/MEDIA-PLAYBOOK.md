# How we made the images and videos

Everything we posted was made from real photos by a small volunteer team. This is
the process, the rules we learned, and how to do it again. The actual scripts, source
photos and finished posts are on the `campaign-archive` branch.

## The workflow

1. **Collect.** Photos and video come to one person.
2. **Pick.** Look at everything at full size, not as thumbnails.
3. **Clear.** Check each picture for kids, addresses, plates and permission.
4. **Build.** A small Python script for each batch makes the images and video.
5. **Check by eye.** Every image at full size. For video, sampled frames at least,
   then watch it on a phone.
6. **Hand off.** One document says what to post, when, with the exact caption.

Scripts matter here for a simple reason: the numbers and the wording change. When
a new vote count landed on election night, one command rebuilt every image and video.

## Rules for any post

**Name the measure.** First mention is always in full: "4A, the LPS mill levy
override." Never a bare "4A" to a cold reader.

**Link to the official site.** Voters go to the campaign's site, not the toolkit.
Instagram doesn't make caption links tappable, so use a link sticker in Stories.

**Use the right names.** Locals say "Heritage" and "Arapahoe," not "Heritage High."

**Sound like the page.** Ours is short, warm and grateful. Facebook used ". . ." and
"&" and exclamation points. Instagram ran a bit plainer.

**Don't describe the picture.** A line should be a question or an idea. Keep any
label to a small "School, year."

**Let the real pictures be.** No filters. Text in Instagram's own Classic style:
black on a white rounded box. People asked that nothing look AI-made.

**Post natively** to each platform. Don't share from one to the other.

**"Paid for by":** we kept it on the site, print and paid ads, and left it off free
posts. Add it back if you boost a post. Ask your registered agent.

## Reels

- **One premise, and every shot pays it off.** A halloween Reel of ours got rejected
  because it mixed dogs, skeletons and a countdown. The rebuilt version was one
  ranked list: "Scariest things around here," ending on a ballot still on the
  counter at 7:01 p.m.
- **Don't reuse a subject.** The same followers saw last week's.
- **Keep text in the safe area.** On a 1080x1920 frame, the top 250 pixels and bottom
  480 belong to the app. Our scripts stop with an error if text goes there.
- **Silent montages, sound added later.** Render with no audio, then pick a sound in
  the Reels editor. For movie clips, the dialogue is the joke, so keep it and add
  captions.
- **Live Photos are free video.** Each one holds about two seconds of motion.

Our Photos workflow: copy `Photos.sqlite`, find assets by date, make contact sheets
from the thumbnails, then export originals with AppleScript. The originals and Live
clips are often only in iCloud, so `tools/campaign/photos_export.applescript` asks
the Photos app to fetch them.

## Throwback and nostalgia posts

These were our best performers. They also went wrong the most.

- **The vote has to show on the image**, not just in the caption. Say the link to the
  vote in one sentence before you build. If you can't, skip it.
- **Pick eras today's parents remember.** For us that was the '80s through the 2000s.
  Our first try, cafeteria pages from the 1950s to '70s, went nowhere.
- **Montage beats a single scene.** Many short shots under building text.
- **Never tell alumni their age**, and don't aim at one graduating class.
- **Ask first.** Yearbooks, school videos and museum scans belong to someone. The
  finished Reels are in the public archive, and the sources are linked in
  `VIDEO-SOURCES.md`.

## Old-movie supercuts

Public-domain films telling people to vote made a fun GOTV series. Clip apps often
cut tight to subtitles, which clips words at the joins and looks like a mistake. Pull
the source with a few seconds of padding, cut in the pauses by measuring the sound,
fade the audio slightly, and join before encoding once. Check any archive item's name
for signs it's a rip of a copyrighted film.

## Celebration posts

- Make images that stay true while ballots are counted, then switch to final wording
  when it's called. See `ELECTION-NIGHT.md`.
- Multi-photo montages, one theme per slide, read as far more finished than single
  photos. Our carousel: Paint Pens, Yard Signs, Folding Tables, Kitchen Tables,
  Buttons, All of Us.
- Every picture has to match its headline. We pulled a parking-lot shot out of
  "Kitchen Tables."
- Have someone at your party whose job is to take photos.

## The posting document

Our lead asked for exactly this, after we wrote too much the first time: one
document, each post in order, with the file and the exact caption. Nothing about
days already past. No strategy mixed in. Files in numbered folders, in posting order.
Every day gets a feed post on both Instagram and Facebook; a Story alone doesn't count.

We generated the document and folders from a single list, so they couldn't disagree.
That script is `build_days.py` on the archive branch.

## Protecting people

This is the part that can't be undone, so it comes before anything is published.

**Decide your rule first.** Ours: adults are fine, no faces of anyone who is a child
today, and no personal information about anyone. Go by how old someone is now. A student
in a 1993 yearbook is an adult, and may be a grandparent.

**What to look for:**

- **Kids.** Including in the background and in reflections.
- **Handwriting.** Signed yearbook pages can hold names and phone numbers that text
  scanning misses.
- **Home addresses:** envelopes, postcards, house numbers, a yard sign in front of a
  recognizable house.
- **Names:** on letters, name tags, envelopes.
- **License plates.**
- **Marked ballots.** Your own is your choice. Don't publish someone else's.
- **Hidden data.** Phone photos and Live Photos store the GPS location and device.
  A photo of a yard sign can give away a home's exact location without showing a
  house number.

**How we checked our archive:**

1. Listed every file, and set aside groups we couldn't publish, like third-party news
   clips.
2. Ran `tools/campaign/media_scan.swift`, which uses Apple's Vision framework to find
   faces and read any text in each image and in frames sampled from each video.
3. Looked at every remaining file on contact sheets. A person made the final call.
   Face detection misses faces, and it can't tell a child from an adult.
4. Used the blurred version of a picture wherever one existed. The raw original of
   a blurred picture isn't safe just because the post was.
5. Built the archive from an allowlist, so a file only got in if we named it.
6. Rebuilt every file without metadata, then confirmed it by reading the file
   structure. A plain text search for "GPS" gives false alarms in compressed files.
7. Scanned the finished archive again, and searched every text file for emails,
   phone numbers and addresses.

Check your scanner, too. Our first run reported no faces in any still photo. That
was a bug in our script, and we only noticed because the party photos were obviously
full of faces. A clean result from a broken tool looks exactly like a clean result.

**A lesson from the end of our campaign:** a raw postcard photo showed a voter's
name and address in a draft Reel. Older posts had used a blurred version, but the
new build picked up the original. We caught it by looking at a single frame. Always
look.

## Rights

Every outside source we used is listed in `VIDEO-SOURCES.md`.

Being allowed to post something isn't the same as being allowed to republish it.
CBS Colorado gave us permission to use its segment in the campaign, and the district
let us edit its podcast. Neither is the same as permission to put the files in a public
archive, so we didn't.
