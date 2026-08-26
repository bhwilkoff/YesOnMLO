# YesOnMLO — The Citizens for LPS Campaign Toolkit

**Volunteer-built tools supporting the $10 million Littleton Public
Schools mill levy override on the November 3, 2026 ballot.**

Littleton Public Schools faces a $10.6M structural budget gap. Before
asking voters for anything, the district cut $6.5M, froze every
employee's wages, and scheduled an unpaid furlough day. The MLO
restores what one-time cuts can't: competitive teacher pay, full
instructional days, intact class sizes, and safe schools. LPS voters
have passed every recent funding measure with 56%+ of the vote — this
toolkit exists to help this community do it again.

> **Paid for by Citizens for LPS.** Built by volunteers on personal
> time. Not produced or distributed with school district resources.

---

## What's here

### The web app (`index.html`, `css/`, `js/`)

A mobile-first, no-framework site with shareable URLs for every view:

| View | URL | What it does |
|---|---|---|
| Home | `?` | The case in 30 seconds: the gap, the three pillars, the ballot history, countdowns |
| The Facts | `?view=facts` | The sourced story: deficit drivers, cuts already made, what the MLO funds |
| Your Cost | `?view=calculator` | A transparent tax calculator that **shows every step of the math** — and labels every unverified number as an estimate |
| FAQ | `?view=faq` | Answers that teach how Colorado school funding actually works |
| Key Dates | `?view=dates` | The all-mail-ballot calendar, registration links, return deadlines |
| Get Involved | `?view=involved` | The involvement ladder, from two minutes to ongoing |
| Share Kit | `?view=share` | Story prompts + copyable facts for volunteers — your story beats any slogan |

**Run locally**: `python3 -m http.server 8080` → http://localhost:8080.
**Deploy**: push to `main`; GitHub Pages serves it.

### The campaign docs (`docs/campaign/`)

- **`CAMPAIGN-BRIEF.md`** — the single source of truth for verified
  campaign facts. Every number the tools display traces here, with its
  source. Unofficial figures carry ⚠️ VERIFY flags.
- **`SOCIAL-MEDIA-PLAYBOOK.md`** — the full platform strategy: where
  to spend effort (Facebook groups > everything), Nextdoor's rules,
  the Amplifier Corps volunteer model, rapid-response protocol, paid
  ads (including Meta's final-week blackout), and a week-by-week
  content arc from September 1 to Election Day.

### The research (`docs/research/`)

- **`campaign-strategy.md`** — why school tax measures pass or fail
  (the political-science literature + Colorado's 2023–2025 record),
  messaging that works and messaging that backfires with suburban
  swing voters, coalition tactics, and case studies from Douglas
  County, Cherry Creek, Thompson, Brighton 27J, and Jeffco.
- **`colorado-compliance.md`** — the legal reference: issue-committee
  registration and TRACER reporting, "Paid for by" disclaimer rules,
  the district/campaign firewall (CRS 1-45-117), the TABOR-notice
  comment deadline (**~September 18 — hard and unrecoverable**), MLO
  law, the 2026 tax math, and a full deadlines table.

## Ground rules (Decisions 053–057 in DECISIONS.md)

1. **Web only.** Voters are reached by shared links, not app installs.
2. **Every fact has provenance.** Numbers live in `js/data.js` and
   trace to `CAMPAIGN-BRIEF.md`; unverified figures are visibly
   labeled as estimates. A campaign that publishes one wrong number
   loses the trust argument permanently.
3. **Compliance is baked in.** Attribution renders on every page from
   one shared footer; nothing here uses district resources; district
   materials are linked, never reproduced as advocacy.
4. **Strategy is private; tools are public.** `git ignore/` and
   `private/` never leave this machine.
5. **Tools teach.** The calculator shows its arithmetic; the FAQ
   explains the funding system; the share kit prompts your own story.
   A supporter who understands the measure can persuade a neighbor —
   that's the theory of change.

## Contributing

This repo is built to welcome campaign volunteers, not just
developers:

- **Not a developer?** The highest-value contributions are facts and
  stories: corrections to `docs/campaign/CAMPAIGN-BRIEF.md`, new FAQ
  questions you've heard from real neighbors, and story prompts for
  the share kit. Open an issue or email the committee.
- **Developer?** Read `CLAUDE.md` for conventions. The short version:
  vanilla HTML/CSS/JS, no build step, mobile-first, WCAG AA, every
  fact from `js/data.js`, every view inside the shared shell.
- **Before anything ships**: does it make a supporter more capable —
  or just louder? We build the first kind.

The official campaign lives at
[citizensforlps.org](https://citizensforlps.org) — this toolkit
complements it and routes voters there.

## For other communities

Everything here except the LPS-specific facts is reusable: the
research syntheses, the compliance reference structure, the
provenance-flagged data plane, the calculator, and the share-kit
pattern. If your district is facing the same fight, fork it, replace
`js/data.js` and `docs/campaign/`, and run. Public education is worth
it everywhere.

---

*This repository was scaffolded from a multi-platform app template;
`CLAUDE.md`, `DECISIONS.md` (entries 001–052), and the `apple/`,
`android/`, `windows/`, `tv/` directories carry the template's
reference material and receive no campaign work.*
