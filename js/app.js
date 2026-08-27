/**
 * Tell the Story of Our Schools — Main Application Logic
 *
 * Vanilla JS, single IIFE. Views toggled by showView(); URL state via
 * ?view= (shareable). All facts come from js/data.js and every fact
 * renders WITH its source (Decisions 054, 058).
 *
 * The share studio is a four-step wizard (who you are → your words →
 * a picture → send it) so people who don't normally post have one
 * clear next move at every moment. Platform intents in SHARE_TARGETS
 * are verified against current platform docs — see
 * docs/research/share-intents.md (Decision 060).
 */
(function () {
  'use strict';

  const $ = (id) => document.getElementById(id);

  function escHtml(str) {
    const d = document.createElement('div');
    d.textContent = str;
    return d.innerHTML;
  }

  const fmtUSD = (n, digits = 0) =>
    n.toLocaleString('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: digits, minimumFractionDigits: digits });
  const fmtNum = (n) => n.toLocaleString('en-US');

  const srcLink = (sourceId) => {
    const s = SOURCES[sourceId];
    if (!s) return '';
    return `<span class="src-link">Source: <a href="${s.url}" target="_blank" rel="noopener">${escHtml(s.label)}</a></span>`;
  };

  /* ================================================================
     VIEW SYSTEM
  ================================================================ */
  const VIEW_NAMES = ['home', 'studio', 'cost', 'playbook'];
  const VIEW_TITLES = {
    home: 'Tell the Story of Our Schools',
    studio: 'Share Studio — Tell the Story of Our Schools',
    cost: 'What It Costs — Tell the Story of Our Schools',
    playbook: 'Team Playbook — Tell the Story of Our Schools',
  };

  function showView(name, fromHistory = false) {
    if (!VIEW_NAMES.includes(name)) name = 'home';
    VIEW_NAMES.forEach((n) => {
      const view = $(`view-${n}`);
      if (view) view.hidden = n !== name;
      const btn = $(`nav-${n}`);
      if (btn) {
        btn.classList.toggle('active', n === name);
        btn.setAttribute('aria-current', n === name ? 'page' : 'false');
      }
    });
    if (!fromHistory) {
      const url = name === 'home' ? '?' : `?view=${name}`;
      history.pushState({ view: name }, '', url);
    }
    document.title = VIEW_TITLES[name];
    $('main-content').scrollTop = 0;
  }

  document.addEventListener('click', (e) => {
    const stepBtn = e.target.closest('[data-wstep]');
    if (stepBtn) {
      if ($('view-studio').hidden) showView('studio');
      gotoStep(Number(stepBtn.dataset.wstep));
      return;
    }
    const target = e.target.closest('[data-view]');
    if (target) showView(target.dataset.view);
  });
  $('wordmark-home').addEventListener('click', (e) => {
    e.preventDefault();
    showView('home');
  });
  window.addEventListener('popstate', (e) => {
    showView(e.state?.view || initialViewFromURL(), true);
  });
  function initialViewFromURL() {
    return new URLSearchParams(window.location.search).get('view') || 'home';
  }

  /* ================================================================
     HOME — the sourced ballot summary
  ================================================================ */
  function renderBallotSummary() {
    $('ballot-summary').innerHTML = CAMPAIGN.ballotSummary.map((item) => `
      <div class="ballot-item">
        <p>${escHtml(item.text)}</p>
        ${srcLink(item.sourceId)}
      </div>`).join('');
  }

  /* ================================================================
     THE WIZARD — shared state
  ================================================================ */
  let currentStep = 1;
  let maxStepReached = 1;
  const sentTo = new Set();

  function gotoStep(n) {
    currentStep = n;
    maxStepReached = Math.max(maxStepReached, n);
    for (let i = 1; i <= 4; i++) {
      $(`wstep-${i}`).hidden = i !== n;
      const item = $(`stepper-${i}`);
      item.classList.toggle('current', i === n);
      item.classList.toggle('done', i < n && stepIsDone(i));
      item.setAttribute('aria-current', i === n ? 'step' : 'false');
    }
    if (n === 3) seedCardText();
    if (n === 4) renderDraftReview();
    $('main-content').scrollTop = 0;
  }

  function stepIsDone(i) {
    if (i === 1) return true;                 // visiting counts — a voice is optional
    if (i === 2) return getDraft().trim().length > 0;
    if (i === 3) return true;                 // the picture is optional
    return sentTo.size > 0;
  }

  /* ================================================================
     STEP 1 — who's telling this story
  ================================================================ */
  function renderVoices() {
    $('voice-grid').innerHTML = CAMPAIGN.storyPrompts.map((g, gi) => `
      <button class="voice-tile" data-voice="${gi}">${escHtml(g.voice)}</button>`).join('');

    $('voice-grid').addEventListener('click', (e) => {
      const tile = e.target.closest('[data-voice]');
      if (!tile) return;
      document.querySelectorAll('.voice-tile').forEach((t) =>
        t.classList.toggle('selected', t === tile));
      renderVoicePrompts(Number(tile.dataset.voice));
    });
  }

  function renderVoicePrompts(gi) {
    const group = CAMPAIGN.storyPrompts[gi];
    $('voice-prompts').innerHTML = `
      <p class="body">Tap the one that stirs something — it becomes your first line, and you finish it.</p>` +
      group.prompts.map((p, pi) => `
        <div class="prompt-card" data-prompt="${gi}:${pi}" role="button" tabindex="0">
          &ldquo;${escHtml(p.text)}&rdquo;
          <span class="prompt-hint">${escHtml(p.hint)}</span>
        </div>`).join('');
  }

  function initPromptClicks() {
    const usePrompt = (key) => {
      const [gi, pi] = key.split(':').map(Number);
      const prompt = CAMPAIGN.storyPrompts[gi]?.prompts[pi];
      if (!prompt) return;
      setDraft(prompt.text + ' ');
      gotoStep(2);
      $('studio-draft').focus();
      // put the cursor at the end, ready to continue the sentence
      const box = $('studio-draft');
      box.setSelectionRange(box.value.length, box.value.length);
    };
    $('voice-prompts').addEventListener('click', (e) => {
      const card = e.target.closest('[data-prompt]');
      if (card) usePrompt(card.dataset.prompt);
    });
    $('voice-prompts').addEventListener('keydown', (e) => {
      const card = e.target.closest('[data-prompt]');
      if (card && (e.key === 'Enter' || e.key === ' ')) {
        e.preventDefault();
        usePrompt(card.dataset.prompt);
      }
    });
  }

  /* ================================================================
     STEP 2 — your words
  ================================================================ */
  const DRAFT_KEY = 'ymlo_draft';

  function getDraft() { return $('studio-draft').value; }
  function setDraft(text) {
    $('studio-draft').value = text;
    draftChanged();
  }
  function draftChanged() {
    $('draft-count').textContent = fmtNum(getDraft().length);
    try { localStorage.setItem(DRAFT_KEY, getDraft()); } catch { /* private mode */ }
  }

  function initDraft() {
    try {
      const saved = localStorage.getItem(DRAFT_KEY);
      if (saved) $('studio-draft').value = saved;
    } catch { /* private mode */ }
    $('studio-draft').addEventListener('input', draftChanged);
    $('draft-clear').addEventListener('click', () => setDraft(''));
    draftChanged();
  }

  function renderFactList() {
    $('fact-list').innerHTML = CAMPAIGN.facts.map((f, i) => `
      <div class="fact-row">
        <div class="fact-text">
          ${escHtml(f.text)}
          ${srcLink(f.sourceId)}
        </div>
        <button class="fact-add" data-fact="${i}">add</button>
      </div>`).join('');

    $('fact-list').addEventListener('click', (e) => {
      const btn = e.target.closest('[data-fact]');
      if (!btn) return;
      const fact = CAMPAIGN.facts[Number(btn.dataset.fact)];
      const draft = getDraft();
      setDraft(draft + (draft && !draft.endsWith('\n') ? '\n\n' : '') + fact.share);
      btn.textContent = 'added';
      setTimeout(() => { btn.textContent = 'add'; }, 1500);
    });
  }

  /* ================================================================
     STEP 3 — a picture (canvas → PNG)
  ================================================================ */
  const CARD_SIZES = {
    square: { w: 1080, h: 1080 },
    story: { w: 1080, h: 1920 },
    wide: { w: 1200, h: 630 },
  };

  let cardTextTouched = false;

  function seedCardText() {
    if (cardTextTouched) return;
    const draft = getDraft().trim();
    if (!draft) return;
    // First sentence, trimmed to card length — the author can rewrite it.
    const firstSentence = draft.split(/(?<=[.!?])\s/)[0] || draft;
    $('card-text').value = firstSentence.length > 160
      ? firstSentence.slice(0, 157) + '…'
      : firstSentence;
    redrawCard();
  }

  function drawCard(canvas, size) {
    const { w, h } = CARD_SIZES[size];
    canvas.width = w;
    canvas.height = h;
    const ctx = canvas.getContext('2d');
    const text = $('card-text').value.trim() || 'I’m voting yes on the LPS mill levy override.';

    ctx.fillStyle = '#FBFAF7';
    ctx.fillRect(0, 0, w, h);
    ctx.fillStyle = '#90CA65';
    ctx.fillRect(0, 0, w, Math.round(h * 0.012));

    const pad = Math.round(w * 0.09);
    const maxWidth = w - pad * 2;

    // The logo's star motif — not the committee's logo: this card is
    // the sharer's own voice, not a committee production (Decision 058)
    ctx.fillStyle = '#90CA65';
    const starSize = Math.round(w * 0.045);
    drawStar(ctx, pad + starSize / 2, Math.round(h * 0.16), 5, starSize / 2, starSize / 4.4);

    const fontSize = size === 'wide' ? Math.round(w * 0.052) : Math.round(w * 0.062);
    ctx.fillStyle = '#323F49';
    ctx.font = `700 ${fontSize}px Lora, Georgia, serif`;
    ctx.textBaseline = 'top';
    const lines = wrapText(ctx, text, maxWidth);
    const lineHeight = Math.round(fontSize * 1.28);
    let y = Math.round(h * 0.16) + starSize + Math.round(h * 0.045);
    lines.forEach((line) => {
      ctx.fillText(line, pad, y);
      y += lineHeight;
    });

    const footY = h - Math.round(h * (size === 'wide' ? 0.16 : 0.1));
    ctx.strokeStyle = '#E3E2DC';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(pad, footY);
    ctx.lineTo(w - pad, footY);
    ctx.stroke();
    ctx.fillStyle = '#5A6772';
    ctx.font = `600 ${Math.round(w * 0.026)}px "Source Sans Pro", sans-serif`;
    ctx.fillText('Learn more: citizensforlps.org', pad, footY + Math.round(h * 0.02));
  }

  function drawStar(ctx, cx, cy, points, outer, inner) {
    ctx.beginPath();
    for (let i = 0; i < points * 2; i++) {
      const r = i % 2 === 0 ? outer : inner;
      const a = (Math.PI / points) * i - Math.PI / 2;
      const x = cx + Math.cos(a) * r;
      const y = cy + Math.sin(a) * r;
      i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
    }
    ctx.closePath();
    ctx.fill();
  }

  function wrapText(ctx, text, maxWidth) {
    const words = text.split(/\s+/);
    const lines = [];
    let line = '';
    words.forEach((word) => {
      const test = line ? `${line} ${word}` : word;
      if (ctx.measureText(test).width > maxWidth && line) {
        lines.push(line);
        line = word;
      } else {
        line = test;
      }
    });
    if (line) lines.push(line);
    return lines;
  }

  function redrawCard() {
    document.fonts.ready.then(() => drawCard($('card-canvas'), $('card-size').value));
  }

  function initCardMaker() {
    const canvas = $('card-canvas');
    $('card-text').addEventListener('input', () => {
      cardTextTouched = true;
      redrawCard();
    });
    $('card-size').addEventListener('change', redrawCard);
    $('card-download').addEventListener('click', () => {
      drawCard(canvas, $('card-size').value);
      canvas.toBlob((blob) => {
        if (!blob) return;
        const a = document.createElement('a');
        a.href = URL.createObjectURL(blob);
        a.download = `lps-share-card-${$('card-size').value}.png`;
        a.click();
        URL.revokeObjectURL(a.href);
      }, 'image/png');
    });

    // Mobile: hand the PNG straight to the share sheet (the real
    // route into Instagram — image attached, caption pasted).
    const shareBtn = $('card-share');
    const probe = new File([new Blob(['x'], { type: 'image/png' })], 'x.png', { type: 'image/png' });
    if (navigator.canShare && navigator.canShare({ files: [probe] })) {
      shareBtn.hidden = false;
      shareBtn.addEventListener('click', async () => {
        await copyDraft();
        drawCard(canvas, $('card-size').value);
        canvas.toBlob(async (blob) => {
          if (!blob) return;
          const file = new File([blob], 'lps-share-card.png', { type: 'image/png' });
          try {
            await navigator.share({ files: [file] });
          } catch { /* user cancelled */ }
        }, 'image/png');
      });
    }
    redrawCard();
  }

  /* ================================================================
     STEP 4 — send it
     Templates verified against current platform documentation —
     docs/research/share-intents.md. Never fake organic reach.
  ================================================================ */
  const SITE_URL = 'https://citizensforlps.org';

  const SHARE_TARGETS = [
    {
      id: 'sms', name: 'Text a friend', role: 'means the most',
      steps: [
        'Think of one person who lives around here.',
        'The button opens your Messages app with your words staged.',
        'Address it, make it sound like you, send.',
      ],
      mode: 'url',
      url: (text) => `sms:?body=${encodeURIComponent(text + ' ' + SITE_URL)}`,
      button: 'Open Messages',
      contactPicker: true,
    },
    {
      id: 'nextdoor', name: 'Nextdoor', role: 'your actual neighbors',
      steps: [
        'The button opens Nextdoor’s composer with your words already in it.',
        'Pick your neighborhood, look it over, post.',
        'One genuine post is plenty — Nextdoor removes repeat campaigning, and neighbors tune it out anyway.',
      ],
      mode: 'url',
      url: (text) => `https://nextdoor.com/sharekit/?source=lps-storyteller&body=${encodeURIComponent(text + '\n' + SITE_URL)}`,
      button: 'Open Nextdoor',
    },
    {
      id: 'facebook', name: 'Facebook', role: 'groups beat feeds',
      steps: [
        'We just copied your words (Facebook doesn’t let sites pre-fill posts).',
        'The share box opens — paste, look it over, post.',
        'Even better: open a local group you belong to and paste it there instead.',
      ],
      mode: 'copy-open',
      url: () => `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(SITE_URL)}`,
      button: 'Copy + open Facebook',
    },
    {
      id: 'whatsapp', name: 'WhatsApp', role: 'the group chat',
      steps: [
        'The button opens WhatsApp with your words ready.',
        'Pick the person or the group chat.',
        'Send it — the link preview comes along automatically.',
      ],
      mode: 'url',
      url: (text) => `https://wa.me/?text=${encodeURIComponent(text + '\n' + SITE_URL)}`,
      button: 'Open WhatsApp',
    },
    {
      id: 'instagram', name: 'Instagram', role: 'card + caption',
      steps: [
        'Go back one step and save the share card — that’s your picture.',
        'This button copies your words and opens Instagram.',
        'New post → add the card → paste your caption. In a story, add the link sticker.',
      ],
      mode: 'copy-open',
      url: () => 'https://www.instagram.com/',
      button: 'Copy + open Instagram',
    },
    {
      id: 'linkedin', name: 'LinkedIn', role: 'the professional case',
      steps: [
        'The button opens LinkedIn’s composer with your words in place.',
        'The angle that lands here: schools are why families and employers choose a town.',
        'Look it over, post.',
      ],
      mode: 'url',
      url: (text) => `https://www.linkedin.com/feed/?shareActive=true&text=${encodeURIComponent(text + '\n' + SITE_URL)}`,
      button: 'Open LinkedIn',
    },
    {
      id: 'email', name: 'Email', role: 'the neighbor thread',
      steps: [
        'For the book club, the HOA thread, the family list.',
        'The button opens a draft with your words in the body.',
        'Address it and send.',
      ],
      mode: 'url',
      url: (text) => `mailto:?subject=${encodeURIComponent('Why I’m voting yes for LPS')}&body=${encodeURIComponent(text + '\n\n' + SITE_URL)}`,
      button: 'Open a draft',
    },
    {
      id: 'threads', name: 'Threads', role: 'if you’re there',
      steps: [
        'The button opens the Threads composer with your words in place.',
        'Look it over, post.',
      ],
      mode: 'url',
      url: (text) => `https://www.threads.com/intent/post?text=${encodeURIComponent(text)}&url=${encodeURIComponent(SITE_URL)}`,
      button: 'Open Threads',
    },
    {
      id: 'bluesky', name: 'Bluesky', role: 'if you’re there',
      steps: [
        'Bluesky posts cap at 300 characters, so we’ll trim if needed.',
        'The button opens the composer with your words in place.',
        'Look it over, post.',
      ],
      mode: 'url',
      url: (text) => `https://bsky.app/intent/compose?text=${encodeURIComponent((text.length > 260 ? text.slice(0, 257) + '…' : text) + '\n' + SITE_URL)}`,
      button: 'Open Bluesky',
    },
  ];

  async function copyDraft() {
    const text = getDraft().trim();
    if (!text) return false;
    try {
      await navigator.clipboard.writeText(text);
      return true;
    } catch {
      return false;
    }
  }

  function renderDraftReview() {
    const draft = getDraft().trim();
    $('draft-review-text').textContent = draft
      ? (draft.length > 220 ? draft.slice(0, 217) + '…' : draft)
      : 'Nothing yet — tap edit and give it one honest sentence. That’s enough.';
  }

  function renderTargetGrid() {
    let tiles = '';
    if (navigator.share) {
      tiles += `
      <button class="target-tile" data-target="native">
        <span class="target-tile-name">Your phone</span>
        <span class="target-tile-role">one tap to everything</span>
      </button>`;
    }
    tiles += SHARE_TARGETS.map((t, i) => `
      <button class="target-tile" data-target="${i}">
        <span class="target-tile-name">${escHtml(t.name)}</span>
        <span class="target-tile-role">${escHtml(t.role)}</span>
      </button>`).join('');
    $('target-grid').innerHTML = tiles;

    $('target-grid').addEventListener('click', (e) => {
      const tile = e.target.closest('[data-target]');
      if (!tile) return;
      document.querySelectorAll('.target-tile').forEach((t) =>
        t.classList.toggle('selected', t === tile));
      if (tile.dataset.target === 'native') {
        renderNativeDetail();
      } else {
        renderTargetDetail(Number(tile.dataset.target));
      }
    });
  }

  function markSent(id, tileSelector) {
    sentTo.add(id);
    const tile = document.querySelector(tileSelector);
    if (tile) tile.classList.add('sent');
    const n = sentTo.size;
    const tally = $('sent-tally');
    tally.hidden = false;
    tally.textContent = n === 1
      ? 'One down. Each place you share reaches people the others don’t — pick another?'
      : `You’ve taken your story to ${n} places. That’s real reach — thank you.`;
  }

  function renderNativeDetail() {
    const detail = $('target-detail');
    detail.hidden = false;
    detail.innerHTML = `
      <p class="target-detail-name">Your phone's share sheet</p>
      <ol class="micro-steps">
        <li>The button opens your phone's own share menu — Messages, WhatsApp, Messenger, Instagram, everything installed.</li>
        <li>Pick the app, pick the person or audience.</li>
        <li>Your words and the campaign link ride along.</li>
      </ol>
      <button class="btn" id="target-action">Share&hellip;</button>`;
    $('target-action').addEventListener('click', async () => {
      const text = getDraft().trim();
      if (!text) { gotoStep(2); $('studio-draft').focus(); return; }
      try {
        await navigator.share({ text, url: SITE_URL });
        markSent('native', '[data-target="native"]');
      } catch { /* user cancelled */ }
    });
  }

  function renderTargetDetail(i) {
    const t = SHARE_TARGETS[i];
    const detail = $('target-detail');
    detail.hidden = false;

    let extra = '';
    if (t.contactPicker && 'contacts' in navigator && 'select' in navigator.contacts) {
      extra = `<div class="target-detail-extra">
        <button class="btn btn-quiet" id="target-contacts">Or pick straight from your contacts</button>
        <p class="fine">The picking happens on your phone — nothing is uploaded anywhere.</p>
      </div>`;
    }

    detail.innerHTML = `
      <p class="target-detail-name">${escHtml(t.name)}</p>
      <ol class="micro-steps">${t.steps.map((s) => `<li>${escHtml(s)}</li>`).join('')}</ol>
      <button class="btn" id="target-action">${escHtml(t.button)}</button>
      ${extra}`;

    $('target-action').addEventListener('click', async () => {
      const text = getDraft().trim();
      if (!text) { gotoStep(2); $('studio-draft').focus(); return; }
      if (t.mode === 'copy-open') {
        const copied = await copyDraft();
        const btn = $('target-action');
        btn.textContent = copied ? 'Copied — opening…' : 'Opening…';
        setTimeout(() => { btn.textContent = t.button; }, 2500);
      }
      window.open(t.url(text), t.id === 'sms' ? '_self' : '_blank', 'noopener');
      markSent(t.id, `[data-target="${i}"]`);
    });

    const contactsBtn = $('target-contacts');
    if (contactsBtn) {
      contactsBtn.addEventListener('click', async () => {
        try {
          const picked = await navigator.contacts.select(['tel', 'name'], { multiple: false });
          const tel = picked?.[0]?.tel?.[0];
          const text = getDraft().trim() ||
            'Hey — you live in the LPS area, right? The schools have a mill levy override on the November ballot and it matters a lot to our family. Can I tell you about it?';
          if (tel) {
            window.open(`sms:${encodeURIComponent(tel)}?body=${encodeURIComponent(text)}`, '_self');
            markSent('sms', `[data-target="${i}"]`);
          }
        } catch { /* user cancelled */ }
      });
    }
  }

  /* ================================================================
     THE COST — transparent calculator, sourced
  ================================================================ */
  function parseHomeValue() {
    const raw = $('calc-home-value').value.replace(/[^0-9.]/g, '');
    return parseFloat(raw) || 0;
  }

  function calcNumbers() {
    const homeValue = parseHomeValue();
    const rate = parseFloat($('calc-rate').value) / 100 || 0;
    const mills = parseFloat($('calc-mills').value) || 0;
    const assessed = homeValue * rate;
    const annual = assessed * (mills / 1000);
    return { homeValue, rate, mills, assessed, annual, monthly: annual / 12 };
  }

  function renderCalculator() {
    const { homeValue, rate, mills, assessed, annual, monthly } = calcNumbers();
    $('calc-steps').innerHTML = `
      <div class="calc-step">
        <div>
          <div class="calc-step-label">1. The county assesses your home</div>
          <div class="calc-step-math">${fmtUSD(homeValue)} &times; ${(rate * 100).toFixed(2)}% assessment rate</div>
        </div>
        <div class="calc-step-value">${fmtUSD(assessed)}</div>
      </div>
      <div class="calc-step">
        <div>
          <div class="calc-step-label">2. The override applies its mills</div>
          <div class="calc-step-math">${fmtUSD(assessed)} &times; ${mills} mills &divide; 1,000</div>
        </div>
        <div class="calc-step-value">${fmtUSD(annual, 0)} / year</div>
      </div>
      <div class="calc-step calc-result">
        <div class="calc-step-label">For your household, that's about</div>
        <div class="calc-step-value">${fmtUSD(monthly, 2)} a month</div>
      </div>`;
  }

  function initCalculator() {
    const tc = CAMPAIGN.taxCalc;
    $('calc-mills').value = tc.estimatedMills.value;
    $('calc-rate').value = (tc.residentialAssessmentRate.value * 100).toFixed(2);

    const unverified = !tc.estimatedMills.verified || !tc.residentialAssessmentRate.verified;
    $('calc-est-note').textContent = unverified
      ? 'The assessment rate and the $25-per-$100,000 estimate are the state’s and the district’s own published figures. The mill number is derived from them and stays an estimate until the county certifies the ballot language this fall — this page will be updated the day the certified figure exists.'
      : 'Figures reflect the certified ballot language and published official rates.';

    $('calc-sources').innerHTML = `
      Assessment rate (7.05% for 2026): <a href="${SOURCES[tc.residentialAssessmentRate.sourceId].url}" target="_blank" rel="noopener">${escHtml(SOURCES[tc.residentialAssessmentRate.sourceId].label)}</a>.
      The district's own estimate — "approximately $25 annually for every $100,000 of home value":
      <a href="${SOURCES[tc.perHundredK.sourceId].url}" target="_blank" rel="noopener">${escHtml(SOURCES[tc.perHundredK.sourceId].label)}</a>.
      The mill figure here (${tc.estimatedMills.value}) is derived from those two numbers; the certified ballot language will set the final figure.
      The formula is the county assessor's: home value &times; assessment rate &times; mills &divide; 1,000.`;

    ['calc-home-value', 'calc-mills', 'calc-rate'].forEach((id) => {
      $(id).addEventListener('input', renderCalculator);
    });
    $('calc-home-value').addEventListener('blur', () => {
      const v = parseHomeValue();
      if (v) $('calc-home-value').value = fmtNum(v);
    });
    $('calc-share').addEventListener('click', () => {
      const { monthly } = calcNumbers();
      setDraft(
        `I did the math for our house: the LPS mill levy override works out to about ${fmtUSD(monthly, 2)} a month for us. ` +
        `For that, teachers keep competitive pay, class sizes hold, and kids get their furlough day back as a school day. I’m voting yes.`
      );
      cardTextTouched = false;
      showView('studio');
      gotoStep(4);
    });
    renderCalculator();
  }

  /* ================================================================
     PLAYBOOK + SOURCES
  ================================================================ */
  function renderPlaybook() {
    $('playbook-list').innerHTML = CAMPAIGN.playbook.map((p) => `
      <div class="play-item">
        <p class="play-name">${escHtml(p.name)}<span class="play-role">${escHtml(p.role)}</span></p>
        <p class="play-how">${escHtml(p.how)}</p>
      </div>`).join('');
  }

  function renderSources() {
    $('sources-list').innerHTML = `<ul class="sources-list">` +
      Object.values(SOURCES).map((s) =>
        `<li><a href="${s.url}" target="_blank" rel="noopener">${escHtml(s.label)}</a></li>`).join('') +
      `</ul>`;
  }

  /* ================================================================
     BOOT
  ================================================================ */
  function init() {
    renderBallotSummary();
    renderVoices();
    initPromptClicks();
    initDraft();
    renderFactList();
    initCardMaker();
    renderTargetGrid();
    initCalculator();
    renderPlaybook();
    renderSources();
    showView(initialViewFromURL(), true);
    gotoStep(1);
  }

  init();
})();
