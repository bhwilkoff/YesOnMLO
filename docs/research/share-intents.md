# Share Mechanisms for a Static Campaign Site (verified August 2026)

Research for the no-backend (GitHub Pages, vanilla JS) share studio.
Verified against official platform docs where they exist. The pattern:
**URL-based prefilled text is dead on Facebook/Instagram by policy but
alive on Nextdoor, Threads, Bluesky, WhatsApp, LinkedIn (undocumented),
SMS, and email** — so the reliable architecture is copy-the-caption +
open-the-network where prefill is banned, real intents everywhere else,
with the Web Share API as the mobile fast path.

## The templates in production (js/app.js SHARE_TARGETS)

| Network | Template | Prefill? | Notes |
|---|---|---|---|
| **Nextdoor** | `https://nextdoor.com/sharekit/?source={name}&body={text}` | ✅ up to 3,500 chars | Official ShareKit; preview card generated from the LAST url in body; user picks neighborhood in composer. [Docs](https://developer.nextdoor.com/reference/share-plugin) |
| **SMS/iMessage** | `sms:?body={text}` (recipient-less) | ✅ | RFC 5724 `?body=` form works on modern iOS AND Android (the `&body` variant is iOS-7-era). Link at END of text for previews. Multi-recipient doesn't work on iOS. [Ref](https://sethmlarson.dev/sms-urls) |
| **WhatsApp** | `https://wa.me/?text={text}` | ✅ | No number → contact chooser. Numbers digits-only intl format. [Docs](https://faq.whatsapp.com/5913398998672934) |
| **Facebook** | `sharer.php?u={url}` after clipboard copy | ❌ URL only | `quote` param ignored; Meta policy prohibits prefilled messages. OG tags carry the preview. No URL can target a group composer — link volunteers to `facebook.com/groups/{slug}` + paste. [Docs](https://developers.facebook.com/docs/sharing/reference/share-dialog) |
| **Instagram** | copy caption + open app / Web Share API with PNG file | ❌ none exists | No web compose intent at all. Mobile: `navigator.share({files})` puts the card in the share sheet → Instagram. Stories: manual Link sticker. |
| **LinkedIn** | `linkedin.com/feed/?shareActive=true&text={text}` | ✅ (undocumented) | Works in 2026 but unsupported — could break; fallback `sharing/share-offsite/?url=`. [Official docs](https://learn.microsoft.com/en-us/linkedin/consumer/integrations/self-serve/share-on-linkedin) |
| **Threads** | `https://www.threads.com/intent/post?text={text}&url={url}` | ✅ | Official Meta docs; domain is threads.com now. Optional `tag`. [Docs](https://developers.facebook.com/docs/threads/threads-web-intents) |
| **Bluesky** | `https://bsky.app/intent/compose?text={text}` | ✅ | Official; 300-grapheme cap — truncate drafts. [Docs](https://docs.bsky.app/docs/advanced-guides/intent-links) |
| **Email** | `mailto:?subject={s}&body={b}` | ✅ | Keep whole encoded URI under ~2,000 chars; `%0D%0A` newlines; pair with copy button (no-mail-app desktops silently no-op). |
| **Messenger** | mobile `fb-messenger://share/?link={url}`; desktop needs an app_id | ❌ URL only | Web Share API sheet is the better mobile answer; no no-app-id desktop path. |

## Web Share API

- `navigator.share({title, text, url})` — iOS Safari, Android Chrome,
  macOS Safari, desktop Chrome/Edge (not Linux, not Firefox). HTTPS +
  user gesture required.
- **Files**: `navigator.canShare({files:[pngFile]})` → share a
  generated PNG into the native sheet (Instagram/Messages/WhatsApp
  appear with the image attached). Facebook/Instagram targets DROP
  accompanying text — always clipboard-copy the caption first.
- Desktop share sheets are sparse: prefer per-network buttons there.

## Contact Picker API

`navigator.contacts.select(['name','tel'], {multiple:true})` —
**Chrome/Edge on Android only** (no iOS, no desktop). OS-mediated,
per-invocation, nothing uploaded. Progressive enhancement only; the
universal fallback (recipient-less `sms:?body=`) is nearly as good.
[MDN](https://developer.mozilla.org/en-US/docs/Web/API/Contact_Picker_API)

## Canvas share cards

- Same-origin images only (else `toBlob` throws SecurityError); wait
  for `document.fonts.ready` before drawing text; manual wrapping.
- iOS canvas memory cap ~16M pixels — 1080×1920 at 1× is fine.
- 2026 dimensions: FB link preview / og:image **1200×630**; feed
  portrait **1080×1350** (IG is transitioning grids to 3:4 — design
  center-safe); stories **1080×1920** with ~250px top/bottom safe
  zones. [Buffer guide](https://buffer.com/resources/social-media-image-sizes/)

## Clipboard API

- `writeText` universal (the backbone of copy-caption flows).
- `write` with `image/png` works Chrome/Edge/Safari/Firefox 127+, but
  multi-representation (image+text) paste targets take only one —
  prefer separate "copy caption" / "copy image" actions; Safari needs
  the promise-based ClipboardItem dance inside the gesture.

## Also relevant

- **OG tags are the only "prefill" Facebook/LinkedIn/Nextdoor-preview/
  iMessage allow** — every shareable page needs real static OG tags
  (crawlers don't run JS) and a 1200×630 og:image.
- **Client-side QR** (vendored lib, no CDN) for tabling/yard-sign →
  share-page flows.
- **UTM discipline**: mint per-channel `?utm_source=` links so free
  analytics show which channels move.
- Web Share *Target* (PWA receiving shares): niche; skip for now.

## Addendum 2026-09-02 — the clipboard + popup trap (observed in Chrome)

Two orderings both fail; only one shape works:

1. `await navigator.clipboard.writeText(text); window.open(url)` —
   Safari blocks the `window.open` as a popup (no longer inside the
   gesture after the await).
2. `<a href target=_blank>` + `navigator.clipboard.writeText` in the
   click handler (no await) — the new tab takes focus before Chrome's
   async permission check, and the promise rejects with **"Document
   is not focused"**. The composer opens; the clipboard is empty.

Working shape: a real `<a href>` for the navigation, plus a
**synchronous** copy in the same gesture — hidden textarea, `select()`,
`document.execCommand('copy')` (deprecated but universal and
synchronous) — with the async API only as a fallback when execCommand
returns false. Verified with a real mouse click: Facebook's composer
opened in a new tab and ⌘V pasted the exact draft.

Also verified: `sharer.php?u=https://citizensforlps.org` renders the
committee's OG card (Facebook resolves it to the NationBuilder domain
in the preview). Programmatic `.click()` carries no user activation
and cannot exercise the clipboard path — test with a physical click.

**Per-network limits now enforced before the click** (js/app.js
`SHARE_TARGETS.limit` / `.soft`): Threads 500 · Bluesky 300 graphemes
including the appended link · LinkedIn 3,000 · Nextdoor 3,500 ·
`mailto:` body ~1,500 (keeps the URI under ~2,000) · soft notes for SMS
(400) and Instagram captions (2,200).

**Draft hand-off in the URL**: `?view=studio&step=4&d=<base64url
utf-8>`; imported on load, then stripped with `replaceState` so a
refresh doesn't re-import over edits. Links stay well under 2,000
characters for drafts up to ~1,400 characters.

## Live verification 2026-09-02 (real Chrome, logged-in where noted)

| Network | Result |
|---|---|
| **Facebook** `sharer.php?u=` | ✅ Composer opened with the Citizens for LPS OG card; ⌘V pasted the exact copied draft (logged in; nothing posted) |
| **Threads** `threads.com/intent/post?text=&url=` | ✅ "New thread" composer prefilled with the text AND the link card (logged in; nothing posted) |
| **WhatsApp** `wa.me/?text=` | ✅ api.whatsapp.com "Share on WhatsApp" page shows the full text + link; Open app / Continue to WhatsApp Web (no login needed) |
| **LinkedIn** `feed/?shareActive=true&text=` | ⚠️ Redirects to sign-in but preserves the compose params in `session_redirect`; not verified past login (no credentials entered). Documented `share-offsite` fallback stays on the panel |
| **Nextdoor** ShareKit | ✅ verified end-to-end 2026-08-27 (composer carried the complete story) |
| **Bluesky** intent | Official docs; requires login to see the composer — not re-verified |
| **Instagram** | ❌ No web intent exists in 2026 (re-searched). Ceiling: `navigator.share({files:[png], text})` on a phone → Instagram appears in the sheet (Feed/Story). Instagram DROPS the text, so the caption is copied first and pasted; the card itself carries the line and a signature so the story travels even if nobody pastes. Desktop: instagram.com → Create → upload the saved PNG, or hand the draft to the phone via `?d=` |

Design consequence for Instagram: make the **picture** carry the
message (own photo or styled card + signature) and make the phone
the primary path. Copy-and-paste is the caption fallback, not the
flow.
