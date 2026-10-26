# Contributing

This is a **web-only** volunteer campaign toolkit (Decision 053) — vanilla
HTML/CSS/JavaScript, no framework, no build step, mobile-first.

The `apple/`, `android/`, `windows/`, and `tv/` directories are template
scaffolding and receive no campaign work.

## Volunteers first

The most valuable contributions are **true stories**, real questions
you've heard from neighbors, and corrections. Open an issue or email
citizens4lps@gmail.com.

## For developers

### Running locally

```sh
python3 -m http.server 8080      # http://localhost:8080
```

That's it — no installs, no dependencies.

### How facts enter the site

Every number on the site traces through a single pipeline:

1. **Source** — a document a reader can check
2. **`docs/campaign/CAMPAIGN-BRIEF.md`** — the narrative record with
   the source linked
3. **`js/data.js`** — the code-level data plane; every fact carries a
   `sourceId` pointing back to the brief
4. **`index.html`** — renders from `js/data.js`, never hardcoded

Unverified figures render with a visible `⚠️ Estimate` label
(Decision 054). Facts without sources get cut, not shipped
(Decision 058).

### Project structure

```
/
├── index.html            ← the full site (single page, 5 views)
├── g.html                ← generator tools (profile frame, share cards)
├── css/styles.css        ← main stylesheet
├── js/
│   ├── data.js           ← all campaign facts (the data plane)
│   ├── app.js            ← view system + navigation
│   └── api.js            ← API abstraction
├── assets/               ← static assets (images, social cards)
├── branding/yes-on-4a/   ← logo masters + generation pipeline
├── tools/                ← build-time scripts (card rendering, screenshots)
├── docs/
│   ├── campaign/         ← CAMPAIGN-BRIEF.md, SOCIAL-MEDIA-PLAYBOOK.md
│   └── research/         ← share intents, compliance, strategy research
├── CLAUDE.md             ← AI collaboration context
├── DECISIONS.md          ← architecture decisions (append-only)
├── PARITY.md             ← feature matrix
└── SCRATCHPAD.md         ← active session log
```

### Conventions

- **No inline styles** — CSS custom properties in `:root` in `styles.css`
- **Mobile-first** — all media queries use `min-width`
- **WCAG AA** — accessible colors, focus rings, semantic HTML
- **No emojis in code or commits** unless explicitly requested
- **Commit messages quote the user's request verbatim** when applicable
- **DECISIONS.md leads with WHY, not WHAT** — see
  `architectural-decision-log` skill
- Read `CLAUDE.md` for the full project context and AI collaboration
  methodology

### Before opening a PR

- [ ] Site loads and works at `http://localhost:8080`
- [ ] All 5 views render (Start, Share Studio, Profile Frame, The Cost,
      Playbook)
- [ ] Mobile layout looks right at 375px
- [ ] Any new fact traces through `CAMPAIGN-BRIEF.md` → `js/data.js`
- [ ] `PARITY.md` updated if a user-facing feature changed

## Reporting issues

Name the area in the title: `[share]`, `[calculator]`, `[frame]`,
`[playbook]`, `[home]`, or `[all]`.
