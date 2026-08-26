# Project Scratchpad — YesOnMLO (Citizens for LPS Campaign Toolkit)

> Active working notes. When this file exceeds ~150 lines, move
> completed milestone detail to ARCHIVE.md and keep this lean.
>
> See `PARITY.md` for the cross-platform feature matrix (single
> source of truth — don't duplicate rows here).
>
> The Current State block below is injected at every session start.
> If it drifts behind the code, fix it FIRST, then work — a stale
> scratchpad is worse than none.

## Current state

- **Status**: LIVE at https://bhwilkoff.github.io/YesOnMLO/ —
  public repo by owner decision ("transparent as possible"); brand
  aligned with citizensforlps.org
- **Active milestone**: M2 — verification pass + first shareable tools
- **Last session**: 2026-08-26
- **Next actions**:
  1. **Verify the ⚠️ facts** in CAMPAIGN-BRIEF.md: TABOR comment
     deadline (call LPS DEO — likely **Sept 18 noon**, unrecoverable),
     Arapahoe ballot-mail date, 7.05% vs 6.95% school assessment
     rate, certified ballot measure letter, MLO term (4-year sunset
     per LRPC minutes vs "ongoing" per press release)
  2. Flip `verified: true` in `js/data.js` as official figures land
     (same commit cites the source in CAMPAIGN-BRIEF.md)
  3. Real-browser check of the live site at 375px + dark mode
  4. Candidate next tools (PARITY §1 🔮 rows): myth-vs-fact card
     generator, interactive content-calendar tracker, drop-box map
  5. Keep `events` in `js/data.js` in sync with
     citizensforlps.org/upcoming_events
- **Open questions**:
  - Final tagline (steering committee deciding; contenders in
    `private/STRATEGY.md`) — update `js/data.js` `tagline` when set
  - Does this site stay a team toolkit, or get adopted/linked by
    citizensforlps.org? (Affects domain + OG image work)

---

## Milestones

### M0 — Campaign foundation ✅ (2026-08-26)

- [x] Platform set decided: **web only** (Decision 053)
- [x] CLAUDE.md project identity + campaign palette
- [x] PARITY.md: platform set + toolkit feature rows
- [x] Campaign facts data plane (`js/data.js` ← CAMPAIGN-BRIEF.md,
      Decision 054) with ⚠️ VERIFY provenance flags
- [x] Research corpus: campaign strategy, social media playbook,
      Colorado compliance (docs/campaign/ + docs/research/)
- [x] Private/public split (`git ignore/` + `private/` gitignored,
      Decision 056)
- [ ] GitHub Pages enabled (blocked on repo-visibility decision)

### M1 — Web toolkit v1 ✅ (2026-08-26)

A voter can understand the measure, see their own cost with the math
shown, and find how to vote; a volunteer can pull story prompts and
facts to share.

Learning-orientation check (Decision 057): calculator shows all
arithmetic and invites adjusting assumptions ✅; FAQ teaches the
funding system ✅; share kit prompts personal stories over
copy-paste ✅; vanilla no-framework implementation ✅.

**Acceptance** (web): 7 views render from data plane ✅ (DOM-shim
smoke test 10/10); unverified figures visibly labeled ✅; "Paid for
by" on every surface ✅; real-browser + phone-width check ⏳.

### M2 — Verification pass + shareable tools (next)

- [ ] All ⚠️ VERIFY facts confirmed or corrected (see Current State)
- [ ] Real-browser render check at 375px + dark mode
- [ ] Registered agent name in footer disclaimer
- [ ] Myth-vs-fact shareable card generator (learning-orientation
      check before building)
- [ ] Interactive week-by-week content calendar for the social team

---

## When to add a binding design doc

When a platform crosses ~5 views OR you find yourself making
inconsistent UI choices, create that platform's binding doc —
`tvOS-DESIGN.md`, `iOS-DESIGN.md`, `macOS-DESIGN.md`, `WEB-DESIGN.md`,
`ANDROID-DESIGN.md` — seeded from the matching per-platform template
in `docs/templates/` (start from `PLATFORM-DESIGN-template.md`, the
index). Invoke
`binding-design-doc-discipline` for the workflow. Treat as binding
from the moment it exists.

The sibling docs share a shape: the **principles** are identical;
the **idioms** they reference diverge per platform. Deliberate
rule inversions between platforms (tvOS auto-focuses Play; iOS
never steals focus) are stated explicitly so they don't get
"harmonized" away.

---

## Open questions

<!-- Add questions as they arise; remove when resolved. Don't
     accumulate — every question should have a path to resolution. -->

---

## Out of scope (intentionally)

Document explicitly-rejected ideas so future sessions don't
re-litigate them. "We thought about this and chose not to design it
now" is far more useful than silently re-arriving at the same answer.

When a request gets declined, write a row. Format:
`**Idea** — Why declined. Revisit when …` (revisit condition lets
the entry retire when circumstances change).

| Idea | Why declined | Revisit when |
|---|---|---|
| <!-- e.g. Web push notifications | Too-inconsistent UX across browsers; APNs/FCM cover the need on mobile | iOS + Android push ship and a real cross-platform request appears --> | | |

---

## Session log

<!-- Append-only. Format: state found → work done → state left.
     Keep entries short — one paragraph per session. -->

**2026-08-24 — Windows scaffold + Tidbits lessons ported.** Found: sixth-gen
template with docs/windows/ present but no `windows/` source scaffold, a
WINDOWS-STORE-SUBMISSION.md that was an unadapted Tidbits copy (real Store
IDs), a playbook describing a pre-ship layout, and no vendored Windows skill.
Done: committed the `windows/` scaffold (AppName.Core / .App / .HeadlessTests /
.Windows — the as-shipped Tidbits architecture with every version gotcha
pre-solved; builds clean, 11 headless tests pass, shell PNGs verified light +
dark at 1180×760 and the 900×680 floor, versions stamped from
AppVersion.xcconfig); generalized WINDOWS-STORE-SUBMISSION.md (placeholders +
§0 checklist, all 12 gotchas + IAP §7 kept); rewrote WINDOWS-PLAYBOOK.md to the
as-built flat layout (.NET 10, TFM-isolation, DPAPI, narrow-width shell
renders, network-race flag); added the `windows-production-gotchas` skill;
added a `## Windows app` CLAUDE.md section + Windows columns in both design
tables; appended DECISIONS 035–039 (anonymous-account deletion, query-not-load,
generator merge guards, randomness-outside-selection, per-store billing
shapes); README tree/step-12 + CONTRIBUTING now name the scaffold. Left: green;
Store assets (7 PNGs) intentionally not generated (per-app branding);
first-Windows-run baselines armed via `-f update_baselines=true` as documented.

**2026-08-24 (second pass) — parity + store-approval robustness.** Found: the
scaffold wave left three lesson families unported — multi-store IAP release
choreography, Play pre-launch/publish traps, and the parity-audit method
lessons. Done: new `docs/store/IAP-RELEASE-CHOREOGRAPHY.md` (financial
paperwork as owner-only critical path, one-review-submission-per-IAP-product /
ship serially, the Ready-to-Submit trap, per-platform License Agreement,
empty-success vs thrown-error, per-store query shapes, real-provisioning-only
purchase verification, the launch-order checklist); store-submission-playbook
gained the IAP section + the internal-track-has-no-pre-launch-report /
Test-Lab-yourself / refused-to-auto-submit / all-or-nothing-submit bullets;
play-cli-submission gained Rules 7–8 (Console stalls, testlab-android.sh);
cross-platform-parity-discipline gained the degenerate-outcome audit pass
(tie/zero/empty/cold-quit), the both-directions stale-⏳ check (false docs vs
false cells), and the failure-class organization for whole-platform-port
audits; tvos-platform-patterns gained the SignInWithAppleButton-in-Form
swallowed-click gotcha; CLAUDE.md table + README tree point at the new doc.
Left: green.

**2026-08-26 — Campaign bootstrap: template → Citizens for LPS toolkit.**
Found: pristine multi-platform template, first commit only; four source
PDFs in `git ignore/` (LPS $10M MLO press release, LRPC minutes + deck
with 2010–2020 ballot history, steering-committee tagline email). Done:
gitignored `git ignore/` + new `private/`; read all sources; ran three
parallel research agents (campaign strategy, social media playbook,
Colorado compliance) → `docs/research/campaign-strategy.md`,
`docs/research/colorado-compliance.md`,
`docs/campaign/SOCIAL-MEDIA-PLAYBOOK.md`; wrote
`docs/campaign/CAMPAIGN-BRIEF.md` (facts + provenance + ⚠️ VERIFY
flags) and `private/STRATEGY.md` (steering-derived targeting, never
committed); appended Decisions 053–057 (web-only, facts-as-data-plane,
compliance-as-architecture, private/public split, tools-teach);
rewrote CLAUDE.md identity, README, PARITY (web-only + feature rows),
manifest. Built web toolkit v1: `js/data.js` facts data plane,
`index.html` 7 views (home/facts/calculator/faq/dates/involved/share),
`css/styles.css` campaign palette (logo-derived green/slate, dark mode,
type ramp), `js/app.js` view system + transparent 3-step tax
calculator (7.05% school rate × 3.5 est. mills, estimate-labeled) +
share kit (story prompts, copyable facts, Web Share API). VERIFIED:
`node --check` clean; DOM-shim smoke test 10/10 assertions (history
table, FAQ, pillars, calculator math $650K→~$160/yr matching research
worked example, estimate labels, countdown, view toggling). NOT yet
verified: real-browser render (no screenshot this session — check
before sharing widely). Key research findings logged: TABOR pro/con
comment deadline ~Sept 18 noon is the highest-leverage unrecoverable
date; Meta ad authorization must start NOW (3–4 week lead); Meta
final-week new-ad blackout ~Oct 27; citizensforlps.org already exists
(co-chairs Amy Clark + Briana McCrumb) — this repo complements it.
Left: green; next actions in Current State.

**2026-08-26 (second pass) — brand alignment with citizensforlps.org + ship
to Pages.** Found: v1 toolkit with placeholder branding and generic footer.
Done: crawled citizensforlps.nationbuilder.com (home, news_and_data, three
budget articles, volunteer, upcoming_events) — captured committee legal name
(Citizens for Littleton Public Schools), registered agent (Lucie Stanish, →
footer disclaimer now complete), co-chairs, PO Box, 5–0 board vote, budget
breakdown (58.5% salaries; central admin <2%; GFOA ×32 years; FTE trend),
real volunteer roles, and the event calendar (postcards/yard signs Sept 12,
lit drops Oct 3–11). Sampled the official logo pixels (#90CA65 green /
#323F49 slate) + theme fonts (Lora/Source Sans Pro) and re-tokenized
styles.css (logo green fails AA for white text → slate CTAs, deep-green
links); header now uses the real logo (light + dark variants copied to
assets/). Added budget-bars section (Facts), events list (Get Involved),
admin-cost FAQ, board-vote + GFOA share facts. VERIFIED: node --check clean;
DOM-shim smoke test 14/14. Pushed to GitHub Pages per user: "the whole point
of having a public repository is the ability to use github pages… as
transparent as possible." Left: green; real-browser check still pending.
