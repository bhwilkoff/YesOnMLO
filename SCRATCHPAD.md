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

- **Status**: v4 (robust sharing) LIVE at
  https://bhwilkoff.github.io/YesOnMLO/ — every send path is a real
  link + same-gesture copy + visible fallback (Decision 061); facts
  refreshed from the district's Sept 1 email + Dollars and Sense page
- **Active milestone**: M4 = certification updates + team tools
- **Last session**: 2026-09-02
- **Next actions**:
  1. **When Arapahoe certifies ballot content (~early Sept)**: add
     the measure letter (single find-and-replace), the certified mill
     figure (flip `estimatedMills.verified` in `js/data.js`), and the
     term — cite the certified language in CAMPAIGN-BRIEF.md
  2. **TABOR pro/con comment deadline** (~Sept 18 noon, unrecoverable)
     — campaign task, not site task; flagged to the team
  3. **Real-phone pass** of the studio (iPhone Safari + Android
     Chrome): `sms:` body, Messenger scheme, Web Share of the card into
     Instagram, Contact Picker, the `?d=` hand-off link arriving by
     text. Desktop Chrome is verified; phones are not.
  4. After Oct 1 the forum list auto-expires to a one-line note — no
     action needed, but check the home page reads right that week
  5. Candidate team tools (PARITY 🔮): local-FB-group directory (needs
     the team's group list), client-side QR of the `?d=` link for
     tabling, per-channel UTM links (decide analytics stance first)
- **Open questions**:
  - Final tagline (steering committee deciding; contenders in
    `private/STRATEGY.md`)
  - Mention the site to the registered agent (in-kind determination
    is the committee's call — compliance addendum §9)

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

**2026-08-26 (evening) — v2: the storytelling toolkit.** Found: v1 live with a
FALSE footer ("Paid for by Citizens for Littleton Public Schools" — the
committee didn't pay for the site), template-y AI design and copy, scope
overlapping citizensforlps.org, and share tools limited to copy/paste. User
directed: never claim untrue things; verify every claim; align look/feel with
the official site; narrow scope to storytelling; social-first tools; no
X/Twitter. Done: Decisions 058–060; full rebuild to 5 views (Start / Your
Story / Share Studio / The Cost / Playbook) in a warm-editorial design (Lora +
Source Sans Pro on warm paper, logo green as highlighter accent, star bullets,
staggered reveal); truthful footer; two research agents → verified share-intent
templates (docs/research/share-intents.md — Nextdoor ShareKit prefill!,
threads.com intent, LinkedIn shareActive, RFC-5724 sms:?body=, Web Share files
for Instagram, Contact Picker Android-only) and a full fact-check audit
(docs/research/fact-check-2026-08-26.md) that CORRECTED the site: GFOA is 31
years not 32 (cflps site's own 32 is unverifiable), $25/$100K is LPS's OWN
official estimate (May 29 letter), 7.05% 2026 school rate VERIFIED, Arapahoe
mails ballots Oct 2 (not "mid-Oct"), 2010–2020 results verified from county
PDFs, dead URLs replaced, "ongoing" not "four years." Data plane now: every
fact carries a sourceId → live-fetched URL; on-page source links everywhere;
sources index in Playbook. New tools: canvas share-card generator (3 sizes,
download + Web Share file path), per-network compose intents, person-to-person
SMS/WhatsApp + Contact Picker, calculator→draft handoff, draft persistence.
OG image (1200×630, PIL + real Lora) + og tags (the only "prefill"
FB/LinkedIn/Nextdoor allow). VERIFIED: node --check clean; DOM smoke 20/20;
headless-Chrome screenshots light+dark, true-375px probe (early clipping was
headless 500px window clamp, not a bug). Left: green; pushed to Pages.

**2026-08-27 — The share studio becomes a guided wizard, tested in real
Chrome.** Found: studio was "a long list of items that don't seem to be
leading anywhere" (user). Done: rebuilt as a four-step flow — 1 Who you are
(voice tiles → prompts that become your first line) · 2 Your words (draft +
optional fact/tips accordions) · 3 A picture (card line auto-seeded from the
draft's first sentence, live canvas preview) · 4 Send it (draft review with
edit link, platform tiles with plain-language roles, per-network guided
panels with numbered micro-steps, sent-state ✓ + encouragement tally).
Folded the separate Your Story view into step 1 (nav is now 4 items); home
CTAs deep-link to wizard steps (data-wstep); calculator's "put this number
in a post" seeds the draft and lands on Send It. Fixed a real UX bug found
by testing: the view-level staggered animation re-ran on step changes with
0.2s delay → blank flash; wizard steps now excluded from the stagger.
VERIFIED IN REAL CHROME (claude-in-chrome): full click-through of all four
steps; prompt → draft seeding; draft persistence across reload; card
auto-seed + live preview; **Nextdoor ShareKit confirmed end-to-end — the
opened tab's composer URL carried the complete story prefilled**; Facebook
copy-then-open flow + sharer.php; sent-state ✓ and tally ("You've taken
your story to 2 places"); calculator→step-4 handoff. Physical-click flakes
during testing were CDP click-delivery races (worked on retry/JS click),
not app bugs. Also verified: 375px wizard layout via iframe probe; DOM
smoke test rewritten for wizard IA, 20/20. Left: green; pushed.

**2026-09-02 — v4: every share goes through, and the district's Sept 1
email lands in the data plane.** Found: v3 wizard live; user asked to
"make sure that every share goes through on the correct platform with as
much persuasive power, storytelling, and direct connection possible" and
shared the district's Sept 1 community email (7 Dollars and Sense forums,
$600K-home example, budget-gap framing). Sources: littletonpublicschools.net
blocks curl (bot challenge) — read the Dollars and Sense page in real Chrome;
it carries the forum schedule verbatim, "$600,000 home → less than $13 per
month", the March 19, 2027 furlough date, the cut breakdown ($1.1M/$2.8M/
$5.4M/$500K), what-yes-buys ($2.5M for 2%, $800K furlough), and **GFOA 32
years** (resolves fact-check claim 8 with an LPS source). Done: data plane —
`forums`, `districtExample`, `placeNames`, four new/updated facts, calculator
opens on the district's $600K example; CAMPAIGN-BRIEF updated. Share engine
rebuilt around Decision 061: `<a href>` targets (no window.open), synchronous
in-gesture clipboard copy, "Didn't open?" fallback line + "Copy my words" on
every panel, per-network limits shown before the click with honest trim,
device-aware order + Messenger (mobile-only), Facebook "open my groups"
secondary, Instagram card-share primary on phones. New: live story
checklist (place · person · ask · under 120 words), "Pass it along" draft
link (`?d=` base64url; desktop→phone, lead→volunteer; earlier draft
recoverable), forum invites on Home + step 1 ("come with me" seeds a
personal invite naming the real time/place; list auto-expires).
`tools/toolkit_smoke.mjs` committed (87 checks: sources resolve, forums
ordered, tax model reproduces the district example, ids present, no X, no
window.open). VERIFIED IN REAL CHROME: forum invite → step 2 with checklist
scored; tile order desktop; Facebook/Nextdoor/SMS anchors + hrefs; Bluesky/
Threads over-limit lines; `?d=` link round-trip on a fresh load with the
"bring it back" notice; **two clipboard failure modes observed and fixed**
(await-then-open blocked by Safari; open-then-async-copy rejects "document
is not focused" in Chrome) — final shape verified with a physical click:
Facebook composer opened with the OG card and ⌘V pasted the exact draft
(user logged in for the test; nothing posted). 375px iframe probe: no
horizontal scroll, checklist + tiles stack cleanly. NOT verified: real
phones (sms:, Messenger scheme, Web Share files, Contact Picker). Left:
green; pushed.

**2026-09-02 (second pass) — photos, personal cards, and an honest
Instagram path.** User: "allow for you to upload a picture instead of just
doing the text shot… adjust the textshot… more personalization (I don't want
all of these to look the same)… check all of the sharing API's. The instagram
one only seems to work via the copy and paste method." Verified live in
Chrome: Threads intent prefills text + link card; wa.me shows text + link;
Facebook composer + paste (earlier today); LinkedIn preserves compose params
through its login redirect (not verified past login); Instagram has no web
intent (re-searched) — the phone share sheet with the PNG is the ceiling. Done:
step 3 rebuilt — source toggle (words on a card / your own photo via
`<input type=file accept=image/*>`, `createImageBitmap` with EXIF orientation,
cover-fit, never uploaded), 5 looks (paper/slate/green/cream/chalkboard), 3
typefaces (Lora/Source Sans/Caveat — Caveat added to the font link for the
card only), placement high/middle/low, 3 sizes with auto-shrink to fit, 4
shapes incl. 4:5 portrait and story safe zones, signature line, photo overlay
shade/panel + crop anchor, "Mix it up" (a new starting point, every control
stays live), choices persist in `ymlo_card`. Instagram panel: phones lead with
"Send the card to Instagram" (share sheet with file + text, caption copied);
desktop gets save-card + copy + instagram.com Create, or hand-off. Web Share
of the card now includes the words (apps that accept text keep them). VERIFIED
IN CHROME: chalkboard + handwritten + signature card at 1080×1350; simulated
JPG upload through the real file input → photo card with shade, white text,
signature, footer; panel overlay; Instagram panel renders with Save-the-card
secondary; smoke test 93/93. NOT verified: real-phone Web Share into
Instagram, HEIC decode on iOS Safari (createImageBitmap handles it there).
Left: green; pushed.

**2026-09-02 (third pass) — claim audit: "get a yard sign."** User: "Where
does it say on the website that you can get a yard sign? Remember, every
single claim and set of written text must be factually accurate for something
that is possible to do or share." Checked citizensforlps.org in Chrome: no
"get a yard sign" anywhere; the Volunteer form has an "I will take a yard
sign" checkbox and the events page lists "Begin Distribute Yard Signs — Sat
Sept 12, 10:00 AM." Hero rewritten to say exactly that with direct links to
/volunteer and /upcoming_events. Same pass: Nextdoor copy softened from
"removes repeat campaigning" to the guideline's own words (local ballot
measures allowed; over-posting not); Arapahoe's own calendar confirms "Oct 2:
ballots begin mailing" (the brief's stale ⚠️ mid-October row corrected, VSPCs
Oct 19 added). CAMPAIGN-BRIEF now lists what the official site lets a person
do, so future copy can only promise those. Left: green; pushed.

**2026-09-02 (fourth pass) — a second set of story stems.** User: "Can you
come up with another set of 'story stems/starters' for each of the 'who you
are' options?" Added 3–4 new stems per voice (parents 7, staff 6, alumni 6,
grown/no kids 6, business 5), same register: one concrete moment, a hint,
no lecture. Facts inside stems are anchored: furlough day is Friday, March
19, 2027 (D&S page); 2% average raise = $2.5M (D&S); 2010/2013/2018/2020 all
passed (Arapahoe results); yard signs = volunteer-form checkbox, out Sept 12
(cflps site). Smoke test now checks every voice has 4+ stems with hints
(128/128). Left: green; pushed.
