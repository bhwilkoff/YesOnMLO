# Tell the Story of Our Schools

**A storytelling toolkit for volunteers supporting the Littleton
Public Schools mill levy override — November 3, 2026.**

Live at **https://bhwilkoff.github.io/YesOnMLO/**

The campaign's official home is
[citizensforlps.org](https://citizensforlps.org) — join, volunteer,
donate, and events all live there. This toolkit does one narrower
thing: it helps supporters tell their own story about these schools
and get it in front of the neighbors who can vote.

> Made by volunteers. Nobody paid for this site and it costs nothing
> to run. It is not published by any campaign committee and was not
> produced with school district resources.

---

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

Volunteers first, developers welcome:

- **Not a developer?** The best contributions are true stories, real
  questions you've heard from neighbors, and corrections. Open an
  issue or email citizens4lps@gmail.com.
- **Developer?** Vanilla HTML/CSS/JS, no build step, mobile-first,
  WCAG AA. Read `CLAUDE.md`. Facts only enter through
  `docs/campaign/CAMPAIGN-BRIEF.md` → `js/data.js`, with sources.
- Run locally: `python3 -m http.server 8080`.

## For other communities

Fork it. Everything except the LPS facts is reusable: the sourced
data plane, the share studio and its verified intent templates, the
card generator, the research. If your district is fighting for
funding too, replace `js/data.js` and `docs/campaign/` and go.

---

*Scaffolded from a multi-platform app template; the `apple/`,
`android/`, `windows/`, `tv/` directories and DECISIONS 001–052 are
template reference and receive no campaign work.*
