# Tell the Story of Our Schools

**A free storytelling toolkit for volunteer school-funding campaigns.**

Volunteers built this for Ballot Issue 4A, the $10 million Littleton Public Schools
mill levy override. **4A passed in November 2026.** Now it's yours to reuse.

- **Want to run it for your own election?** Start with
  [`docs/RUN-IT-AGAIN.md`](docs/RUN-IT-AGAIN.md).
- **Want to know what worked?** Read
  [`docs/campaign/RETROSPECTIVE.md`](docs/campaign/RETROSPECTIVE.md).
- **See it live:** https://yeson4a.org

> Made by volunteers. Nobody paid for this site and it costs nothing to run. It is
> not published by any campaign committee and was not produced with school district
> resources.

---

## Get started

```sh
git clone --single-branch --branch main https://github.com/bhwilkoff/YesOnMLO.git my-campaign
cd my-campaign
python3 -m http.server 8080     # then open http://localhost:8080
node tools/toolkit_smoke.mjs    # checks every fact has a source
```

No framework, no build step, no backend and no hosting bill. It's plain HTML, CSS and
JavaScript on free GitHub Pages. Every campaign fact lives in `docs/campaign/CAMPAIGN-BRIEF.md`
and `js/data.js`, so that's most of what you change.

## What's in here

| You want | Go to |
|---|---|
| The step-by-step guide for a new election | `docs/RUN-IT-AGAIN.md` |
| What we learned, including our strategy | `docs/campaign/RETROSPECTIVE.md` |
| The week-by-week social media plan | `docs/campaign/SOCIAL-MEDIA-PLAYBOOK.md` |
| How the images and videos got made, and how to protect people in them | `docs/campaign/MEDIA-PLAYBOOK.md` |
| How to read election night in a vote-by-mail state | `docs/campaign/ELECTION-NIGHT.md` |
| Every outside video and archival source, with links | `docs/campaign/VIDEO-SOURCES.md` |
| How other Colorado school measures did in 2026 | `docs/research/2026-colorado-school-measures.md` |
| Why the count took so long | `docs/research/2026-why-the-count-took-so-long.md` |
| Our original strategy notes and Facebook research | `docs/research/` |
| Election-night and media-review tools | `tools/campaign/` |
| Every photo, video and finished post we can share | the [`campaign-archive`](https://github.com/bhwilkoff/YesOnMLO/tree/campaign-archive) branch |

## What the toolkit does

- **Your Story** — prompts organized by who you are (parent, teacher
  on personal time, alum, longtime neighbor, business owner), with
  plain guidance: one true moment, one fact, one ask.
- **Share Studio** — draft once, then hand your words to each
  network with the least friction the platform allows: Nextdoor's
  official composer prefill, SMS and WhatsApp with the message
  staged, LinkedIn/Threads/Bluesky compose intents, honest
  copy-then-open flows for Facebook and Instagram (Meta forbids
  prefill), and the phone's native share sheet. Plus a share-card
  generator (canvas → PNG in feed, story, and link-preview sizes)
  and person-to-person tools for texting people you actually know in
  the district.
- **Profile Frame** — wear 4A without posting about it. Upload
  your photo, pick a design (Badge, Clean, Icon, Around the edge),
  drag/zoom/rotate the badge, and save a framed profile picture.
  Nothing is uploaded — everything stays on your device.
- **The Cost** — a calculator that shows the county assessor's
  actual three-step math, with every assumption adjustable and every
  source linked on the page. Estimates are labeled as estimates
  until the district publishes official figures.
- **Team Playbook** — how we show up on each network (Facebook
  groups, Instagram, Nextdoor's rules, LinkedIn, texts and DMs,
  Threads/Bluesky — no X), how to handle pushback kindly, and the
  sources for every number on the site.

## Ground rules (DECISIONS.md 053–060)

1. **Nothing untrue, ever** (058). The footer states the site's real
   provenance. Every fact carries a source a reader can check —
   facts without sources get cut, not shipped.
2. **Narrow scope** (059). We complement citizensforlps.org, never
   duplicate it. Every feature must help someone tell or spread a
   story.
3. **Social-first** (060). Every tool ends in a post, a message, or
   a conversation. Share mechanics are verified against current
   platform docs (`docs/research/share-intents.md`), and we never
   fake organic reach.
4. **Facts are a data plane** (054). Every number lives in
   `js/data.js` with a `sourceId`, traced through
   `docs/campaign/CAMPAIGN-BRIEF.md`. Unverified figures render with
   visible estimate labels.
5. **Web only** (053), **strategy private** (056), **tools teach**
   (057).

## The research behind it

- `docs/research/campaign-strategy.md` — why school-funding measures
  pass or fail; Colorado's 2023–2025 record; messaging that works
  and backfires.
- `docs/campaign/SOCIAL-MEDIA-PLAYBOOK.md` — the team's full
  platform strategy and week-by-week arc.
- `docs/research/colorado-compliance.md` — issue-committee law, the
  district/campaign firewall, hard deadlines.
- `docs/research/share-intents.md` — the verified 2026 share-intent
  templates the studio is built on.

## Contributing

If you use this, we'd love to hear about it:

- **Not a developer?** Tell us how your campaign went, what confused you, and
  what we got wrong. Open an issue.
- **Developer?** Vanilla HTML/CSS/JS, no build step, mobile-first,
  WCAG AA. Read `CLAUDE.md`. Facts only enter through
  `docs/campaign/CAMPAIGN-BRIEF.md` → `js/data.js`, with sources.
- Run locally: `python3 -m http.server 8080`.

## License

The code is MIT licensed, so fork it and change anything. The photos and videos on the
`campaign-archive` branch are not, and the logo and committee name belong to the
campaign. Replace them with your own.

---

*Scaffolded from a multi-platform app template; the `apple/`,
`android/`, `windows/`, `tv/` directories and DECISIONS 001–052 are
template reference and receive no campaign work.*
