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

// Forums: ISO dates, strictly ascending, all in the 2026 election fall.
const dates = CAMPAIGN.forums.sessions.map((s) => s.date);
check(dates.every((d) => /^2026-(09|10)-\d{2}$/.test(d)), 'forum dates are ISO 2026 fall');
check(dates.every((d, i) => i === 0 || d > dates[i - 1]), 'forum dates ascend');
check(CAMPAIGN.forums.sessions.length === 7, 'seven forums (district email 2026-09-01)');
check(CAMPAIGN.forums.sessions.every((s) => s.time && s.place), 'each forum has time + place');

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
  const dynamic = ['target-action', 'target-copy', 'target-contacts', 'target-fallback', 'handoff-copy', 'handoff-link', 'handoff-share', 'draft-restore'];
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
