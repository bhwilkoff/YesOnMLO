# Run it again: using this toolkit for your own election

This repo helped a volunteer campaign pass Ballot Issue 4A, a $10 million
mill levy override for Littleton Public Schools, in November 2026. It cost
almost nothing to run, and every piece of it is here for you to take.

You don't need to be a developer to use most of it. You do need one person who
can edit text files and push to GitHub, or a friend who will. If that person
has an AI coding assistant, `CLAUDE.md` tells it how this project works.

## 1. Get your own copy

**The easy way:** on GitHub, click **Use this template**, then **Create a new
repository**. Leave "Include all branches" unchecked. That gets you the
lightweight toolkit without the media archive.

**From the command line:**

```sh
git clone --single-branch --branch main https://github.com/bhwilkoff/YesOnMLO.git my-campaign
cd my-campaign
python3 -m http.server 8080     # then open http://localhost:8080
```

Use `--single-branch`. Without it, you download about a gigabyte of our photos
and video, which you don't need to get started. See
[the media archive](#10-look-at-what-we-made) if you want them.

## 2. Check that a site like this is OK for you to run

Do this before you write a word. Campaign finance and school-district rules
differ by state, and the rules are the part you cannot fix afterward.

1. Read `docs/research/colorado-compliance.md`. If you aren't in Colorado, use it
   as a list of questions, not answers.
2. Find out who your registered agent is. On legal questions, that person has
   the last word, not this document.
3. Draw a hard line between the district and the campaign. District staff time,
   email, buildings and logos stay out of it. If you hold a role on both sides,
   as our Social Media lead did, write down how you will keep them apart.
4. Decide what "Paid for by" line you need and where, and ask your registered
   agent. We kept it on the site, print and paid ads, and left it off free posts
   from our own accounts because they weren't ads. That was our call, not legal
   advice for you.

## 3. Make it yours

Work through this in order. Each row is a real place this campaign is
hardcoded, so nothing is left to find on your own.

| Step | File | What to change |
|---|---|---|
| 1 | `docs/campaign/CAMPAIGN-BRIEF.md` | Replace every fact, with a source for each one. **This goes first.** Everything else comes from here |
| 2 | `js/data.js` | `SOURCES`, then `CAMPAIGN`: `officialSite`, `toolkitUrl`, `measure`, `ballotSummary`, `facts`, `storyPrompts`, `taxCalc`, `forums`, `carPainting`, `campaignMeetings`, `placeNames`, `playbook`. Set `outcome` to `null` |
| 3 | `index.html` | Title and meta tags, hero text, logo alt text, footer links, "Paid for by" text |
| 4 | `js/app.js` | Search for `citizensforlps`, `4A`, `LPS` and `Yes on`. Key spots: `SITE_URL`, the card footer, share titles, default card text, the profile-frame ring text, and the tax-share sentences. Card colors are near the top of the card section |
| 5 | `css/styles.css` | Colors in `:root` and the dark-mode block. Use your own campaign colors, not the district's |
| 6 | `branding/yes-on-4a/` | Replace the logo masters, then run `python3 tools/render_brand_assets.py` to regenerate every logo, favicon and app icon. Never crop a logo by hand |
| 7 | `branding/social/*.html` | Your social cards. Run `python3 tools/render_social_cards.py` to make all four sizes |
| 8 | `manifest.json` | App name and theme color |
| 9 | `CNAME` | Your domain, or delete the file to use `yourname.github.io/repo` |
| 10 | `LICENSE`, `README.md`, `CONTRIBUTING.md`, `docs/campaign/SOCIAL-MEDIA-PLAYBOOK.md` | Your names, your dates, your contact address |

Then run the test. It checks that every fact has a source, the dates are in
order, the tax math reproduces the district's own example, and the page has
what the code expects:

```sh
node tools/toolkit_smoke.mjs
```

**Three rules to keep while you do this:**

- **A fact without a source doesn't ship.** If a figure isn't official yet, set
  `verified: false` and the site labels it as an estimate.
- **Every action claim has to be doable.** Before writing "get a yard sign,"
  go find the actual form or button, and link to it. Our truth was a checkbox.
- **Name the measure in full on first use.** A neighbor has no idea what "4A"
  means. We always wrote "4A, the LPS mill levy override," and the site builds
  that from `CAMPAIGN.measure`, so you change it once.

## 4. Put it online for free

1. Push to your repo. It must be public for free GitHub Pages.
2. On GitHub: **Settings, Pages**. Source: `main` branch, `/` root.
3. If you have a domain, point it at GitHub Pages. An apex domain needs the four
   GitHub `A` records. Then keep the `CNAME` file: if it's deleted, GitHub drops
   your domain.
4. Check it on a phone. Most of your volunteers will use one.

**Decide early which link you share.** We had two sites and they had different
jobs. The official campaign site was for voters: every card, text and post sent
people there. This toolkit was for the folks spreading the word. The moment
someone is persuaded is the wrong moment to land them on a tool for volunteers.

## 5. What you can drop

`android/`, `apple/`, `windows/`, `tv/`, `cast/`, `tv.js`, `tv.css`, and the
store and TV docs came from the project template and were never used. A campaign
travels by links, not app installs. Delete them if you like. Nothing on the site
depends on them.

## 6. Run the campaign

- **The plan:** `docs/campaign/SOCIAL-MEDIA-PLAYBOOK.md`, week by week. Move the
  dates to match your ballot-mailing date, which everything hangs on.
- **What we'd do again and what we wouldn't:** `docs/campaign/RETROSPECTIVE.md`.
  Read this one first.
- **How the images and videos got made:** `docs/campaign/MEDIA-PLAYBOOK.md`.
- **The research:** `docs/research/campaign-strategy.md` for why these measures
  pass or fail, and `docs/research/share-intents.md` for what each social network
  actually allows.

Set these up in the first two weeks. We learned each of them late:

1. Get several people in as admins on Facebook and Instagram, and walk each one
   through it. This is essential and harder than it sounds.
2. Ask everyone to send photos and video from every event, to one person. Pictures
   and video are currency, and you can't go back and take them later.
3. Get permission for photos of anyone who isn't an adult, in writing, before you
   post. Or leave their faces out.
4. Recruit a small crew whose only job is to like, comment and share your posts.

## 7. Keep your team's private work private

Two folders are in `.gitignore`, so nothing in them can be pushed by accident:

- `private/` for strategy, targeting and working files
- `git ignore/` for source documents from your steering committee

Your repo is public. Assume the other side reads it. Keep audience targeting and
committee deliberations in those folders until the election is over, then decide
what to publish. Decision 063 explains how we did that.

## 8. Election night

Use `docs/campaign/ELECTION-NIGHT.md` and `tools/campaign/election_watch.py`.
The short version: "all precincts reporting" doesn't mean what it sounds like in
a vote-by-mail state, and there's a better way to read the numbers.

## 9. When it's over

1. Set `CAMPAIGN.outcome` in `js/data.js`. The home page shows it right away.
2. Post your thanks. Wait for your campaign or district to call the race first.
3. Write down your lessons while you remember them, and send them to the next
   group.
4. If you share your archive, run the privacy process in
   `docs/campaign/MEDIA-PLAYBOOK.md` first. It has to happen before you publish,
   because you can't reliably take something back off the internet.

## 10. Look at what we made

All our photos, videos and finished posts are on the `campaign-archive` branch of
this repo, with a guide to what's there. You can browse it on GitHub. To download
it:

```sh
git clone --single-branch --branch campaign-archive https://github.com/bhwilkoff/YesOnMLO.git yes-on-4a-archive
```

The code is MIT licensed. The photos and video are not, and belong to the folks
who took them. They're there so you can learn from them, not to reuse in your own
campaign. See `LICENSE-MEDIA.md` on that branch.

If you use this, we'd love to hear how it went. And if you make it better, send
it back so the next group gets that too.
