#!/usr/bin/env node
/**
 * Data-plane integrity test for the campaign toolkit (Decision 054).
 * Runs in plain Node — no browser, no deps:
 *
 *   node tools/toolkit_smoke.mjs
 *
 * Checks that every fact carries a sourceId that resolves, that the
 * forums are well-formed and in date order, that the tax model
 * reproduces the district's own worked example, and that index.html
 * has every element id app.js reaches for. Real-browser behavior
 * (share intents, clipboard, Web Share) is verified separately in
 * Chrome — see SCRATCHPAD.md session log.
 */
import { readFileSync } from 'node:fs';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const read = (p) => readFileSync(path.join(root, p), 'utf8');

const ctx = {};
vm.createContext(ctx);
vm.runInContext(read('js/data.js') + '\nthis.SOURCES = SOURCES; this.CAMPAIGN = CAMPAIGN;', ctx);
const { SOURCES, CAMPAIGN } = ctx;

const APP = read('js/app.js');
const HTML = read('index.html');
const CSS = read('css/styles.css');

let pass = 0, fail = 0;
const check = (cond, msg) => { if (cond) pass++; else { fail++; console.error('FAIL:', msg); } };

// Every source is a real https/http URL with a label.
for (const [id, s] of Object.entries(SOURCES)) {
  check(/^https?:\/\//.test(s.url) && s.label, `source ${id} has url+label`);
}

// Every fact-bearing item resolves its sourceId.
const withSource = [
  ...CAMPAIGN.ballotSummary, ...CAMPAIGN.facts,
  CAMPAIGN.taxCalc.residentialAssessmentRate, CAMPAIGN.taxCalc.estimatedMills,
  CAMPAIGN.taxCalc.perHundredK, CAMPAIGN.taxCalc.districtExample, CAMPAIGN.forums,
];
for (const item of withSource) {
  check(SOURCES[item.sourceId], `sourceId "${item.sourceId}" resolves (${(item.text || item.note || 'model').slice(0, 40)})`);
}
for (const f of CAMPAIGN.facts) check(f.text && f.share, 'fact has text + share');

// Story prompts: every voice has at least four stems, each with a hint.
for (const g of CAMPAIGN.storyPrompts) {
  check(g.prompts.length >= 4, `voice "${g.voice}" has 4+ stems (${g.prompts.length})`);
  for (const p of g.prompts) check(p.text && p.hint, `stem has text + hint: ${p.text.slice(0, 30)}`);
}

// Forums: ISO dates, strictly ascending, all in the 2026 election fall.
const dates = CAMPAIGN.forums.sessions.map((s) => s.date);
check(dates.every((d) => /^2026-(09|10)-\d{2}$/.test(d)), 'forum dates are ISO 2026 fall');
check(dates.every((d, i) => i === 0 || d > dates[i - 1]), 'forum dates ascend');
check(CAMPAIGN.forums.sessions.length === 7, 'seven forums (district email 2026-09-01)');
check(CAMPAIGN.forums.sessions.every((s) => s.time && s.place), 'each forum has time + place');

// The committee's own meetings are a SEPARATE list (confirmed with the
// organizer 2026-09-09): same offer, different host. Never merged.
const cm = CAMPAIGN.campaignMeetings;
check(cm && cm.sessions.length === 2, 'two committee-hosted meetings');
check(cm.host === 'Citizens for LPS', 'committee meetings name their host');
check(cm.sessions.every((s) => /^2026-10-(08|09)$/.test(s.date) && s.time && s.place), 'committee meetings dated Oct 8-9 with time + place');
check(!CAMPAIGN.forums.sessions.some((s) => cm.sessions.some((c) => c.date === s.date)), 'the two lists share no dates');
// Render-time contract: app.js reads all three of these. A missing key
// is a blank line on the page, not an exception, so assert them here.
check(['short', 'long', 'atDistrictForums'].every((k) => typeof CAMPAIGN.carPainting?.[k] === 'string'), 'carPainting carries the strings app.js renders');

// Profile-photo frame. The canvas work can only be proven in a real
// browser (headless virtual time starves the badge image loads), so
// these guard the wiring the DOM depends on.
check(/VIEW_NAMES\s*=\s*\[[^\]]*'frame'/.test(APP), 'frame is a registered view');
check(APP.includes('initFrameMaker()'), 'initFrameMaker runs at boot');
['frame-canvas', 'frame-file', 'frame-studio', 'frame-zoom', 'frame-download']
  .forEach((id) => check(HTML.includes(`id="${id}"`), `frame markup has #${id}`));
// display:grid would beat the hidden attribute, as it did on first build.
check(/\.frame-studio\[hidden\][^{]*\{[^}]*display:\s*none/.test(CSS), 'frame-studio[hidden] is forced to display:none');
check(!/drawCard[\s\S]{0,400}yes-on-4a-logo/.test(APP), 'share cards still avoid the lockup (Decision 058)');
// The badge uses the tagline-FREE wordmark: at avatar size the tagline
// is unreadable clutter.
check(APP.includes("assets/yes-on-4a-wordmark.png"), 'frame badge uses the tagline-free wordmark');
check(!/frameBadges[\s\S]{0,400}yes-on-4a-logo\.png/.test(APP), 'frame badge does not use the tagline lockup');
check(APP.includes('trackNavOverflow()'), 'nav scroll affordance is wired');
['frame-design', 'frame-cutout', 'frame-rotate', 'frame-recenter', 'frame-url', 'frame-soften']
  .forEach((id) => check(HTML.includes(`id="${id}"`), `frame markup has #${id}`));
check(APP.includes('FRAME_DESIGNS'), 'frame designs are presets, not separate toggles');
// Ring must SAY something; it used to just delete the badge, which on a
// set where every design has a ring looked like doing nothing.
check(/ring:\s*\{[^}]*ringText/.test(APP), 'the ring design carries text, not just an empty ring');
check(!/banner:\s*\{/.test(APP), 'the chord banner design is gone');
check(/pointers\.size >= 2/.test(APP), 'pinch-to-zoom is handled');
check(APP.includes("addEventListener('wheel'"), 'wheel zoom is handled');
// The link on the ring points at the campaign, never this toolkit
// (Decision 059 amendment).
check(APP.includes("'citizensforlps.org'"), 'ring link is the campaign site');
check(!/drawArcText\([^)]*yeson4a/.test(APP), 'ring link is not the toolkit domain');
check(APP.includes("globalCompositeOperation = 'destination-in'"), 'transparent-corner cutout is implemented');

// Tax model reproduces the district's own example: $600K → "< $13/mo".
const tc = CAMPAIGN.taxCalc;
const monthly = tc.districtExample.homeValue * tc.residentialAssessmentRate.value * (tc.estimatedMills.value / 1000) / 12;
check(monthly < 13 && monthly > 11, `district example: $600K → $${monthly.toFixed(2)}/mo (< $13)`);
check(Math.abs(100000 * tc.residentialAssessmentRate.value * tc.estimatedMills.value / 1000 - tc.perHundredK.value) < 1, '$25 per $100K reproduces');
check(tc.defaultHomeValue === tc.districtExample.homeValue, 'calculator opens on the district example');

// Unverified figures stay flagged until certification.
check(tc.estimatedMills.verified === false, 'mills remain unverified until ballot certification');

// The page carries every id the app reaches for.
const html = read('index.html');
const app = read('js/app.js');
const ids = new Set([...app.matchAll(/\$\('([a-z0-9-]+)'\)/g)].map((m) => m[1]));
for (const id of ids) {
  if (/^(wstep|stepper|view|nav)-/.test(id)) continue;   // templated ids checked below
  const dynamic = ['target-action', 'target-copy', 'target-contacts', 'target-fallback', 'target-card-share', 'target-card-copy', 'target-card-save', 'handoff-copy', 'handoff-link', 'handoff-share', 'draft-restore'];
  if (dynamic.includes(id)) continue;                      // rendered by app.js itself
  check(html.includes(`id="${id}"`), `index.html has #${id}`);
}
for (let i = 1; i <= 4; i++) check(html.includes(`id="wstep-${i}"`) && html.includes(`id="stepper-${i}"`), `wizard step ${i} markup`);

// No share target may point at X/Twitter (Decision 060).
check(!/twitter\.com|x\.com\/intent/.test(app), 'no X/Twitter intents');
// Every send path is a link or a same-gesture share — never window.open after an await (Decision 061).
check(!/await[^\n]*\n[^\n]*window\.open/.test(app) && !app.includes('window.open('), 'no window.open share paths');

console.log(`${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
