# URL scheme — the shareable-link contract

Every surface on the site has a URL that can be shared, bookmarked, or
sent as a link. This doc is the contract.

## View navigation

The site uses `?view=` query parameters for top-level navigation.
Each view corresponds to a nav button in the header.

| View | URL | What it shows |
|---|---|---|
| Start (default) | `https://yeson4a.org` or `?view=home` | Hero, 3-step CTA, forum list, ballot summary |
| Share Studio | `?view=studio` | 4-step guided wizard for crafting + sharing your story |
| Profile Frame | `?view=frame` | Photo upload, 4 frame designs, drag/zoom/save |
| The Cost | `?view=cost` | Interactive tax calculator with county assessor math |
| Playbook | `?view=playbook` | Per-network guides, pushback advice, sources index |

## Deep parameters

Several views accept additional parameters for deep linking into a
specific state.

| Parameter | Used by | Example | Purpose |
|---|---|---|---|
| `step=N` | Share Studio | `?view=studio&step=2` | Jump to a specific wizard step (1–4) |
| `d=…` | Share Studio | `?view=studio&d=encodedDraft` | Pre-seed the draft — enables desktop → phone hand-off and team lead → volunteer starting drafts |
| `wstep=N` | Home → Studio | Internal `data-wstep` attribute | Home page CTAs link into specific studio steps |
| `anchor=ID` | Playbook | `?view=playbook&anchor=playbook-sources` | Scroll to a named section within a view |

## The draft hand-off link (`?d=`)

The `?d=` parameter carries a volunteer's draft in the URL itself.
No server, nothing stored. Use cases:

- **Desktop → phone**: write on a laptop, text yourself the link,
  open on phone to post from the native app
- **Team lead → volunteer**: share a starting draft that the
  volunteer can personalize before posting

An earlier draft is recoverable on import — the studio doesn't
silently overwrite work.

## Sharing rules

Every URL the site produces is an `https://yeson4a.org/…` link —
always meaningful to any recipient, regardless of device. There are
no app installs, no custom schemes, no native deep links (Decision
053: web only).

The site's share mechanics are documented in
`docs/research/share-intents.md` and verified against current
platform behavior. Key constraint: Meta (Facebook, Instagram,
Messenger) forbids URL prefill — those flows use copy-then-open
with a visible fallback link (Decision 061).
