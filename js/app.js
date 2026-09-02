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
 * docs/research/share-intents.md (Decision 060) — and every send path
 * is a real link with a visible fallback (Decision 061): the words are
 * always on the clipboard before the network opens, so nothing a
 * volunteer wrote can be lost to a blocked popup or a missing app.
 */
(function () {
  'use strict';

  const $ = (id) => document.getElementById(id);

  function escHtml(str) {
    const d = document.createElement('div');
    d.textContent = str;
    return d.innerHTML;
  }
  const escAttr = (str) => escHtml(str).replace(/"/g, '&quot;');

  const fmtUSD = (n, digits = 0) =>
    n.toLocaleString('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: digits, minimumFractionDigits: digits });
  const fmtNum = (n) => n.toLocaleString('en-US');

  const srcLink = (sourceId) => {
    const s = SOURCES[sourceId];
    if (!s) return '';
    return `<span class="src-link">Source: <a href="${s.url}" target="_blank" rel="noopener">${escHtml(s.label)}</a></span>`;
  };

  /*
   * Where the person is. Phones get the share sheet, Messages, and
   * Messenger first; desktops get the composers that actually exist
   * there and a hand-off to the phone for the rest. iPadOS reports
   * itself as a Mac, hence the touch-points check.
   */
  const IS_MOBILE = /Android|iPhone|iPad|iPod/i.test(navigator.userAgent) ||
    (navigator.maxTouchPoints > 1 && /Mac/.test(navigator.platform));

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
    const forumBtn = e.target.closest('[data-forum]');
    if (forumBtn) {
      inviteToForum(Number(forumBtn.dataset.forum));
      return;
    }
    const stepBtn = e.target.closest('[data-wstep]');
    if (stepBtn) {
      if ($('view-studio').hidden) showView('studio');
      gotoStep(Number(stepBtn.dataset.wstep));
      return;
    }
    const target = e.target.closest('[data-view]');
    if (target) {
      showView(target.dataset.view);
      if (target.dataset.anchor) {
        const el = $(target.dataset.anchor);
        if (el) el.scrollIntoView({ block: 'start' });
      }
    }
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
     HOME — the sourced ballot summary + the forums
  ================================================================ */
  function renderBallotSummary() {
    $('ballot-summary').innerHTML = CAMPAIGN.ballotSummary.map((item) => `
      <div class="ballot-item">
        <p>${escHtml(item.text)}</p>
        ${srcLink(item.sourceId)}
      </div>`).join('');
  }

  function localDate(iso) {
    const [y, m, d] = iso.split('-').map(Number);
    return new Date(y, m - 1, d);
  }
  function todayStart() {
    const t = new Date();
    return new Date(t.getFullYear(), t.getMonth(), t.getDate());
  }
  const fmtDay = (date) => date.toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric' });
  const fmtDayShort = (date) => date.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' });

  function upcomingForums() {
    const today = todayStart();
    return CAMPAIGN.forums.sessions
      .map((s, i) => ({ ...s, i, when: localDate(s.date) }))
      .filter((s) => s.when >= today);
  }

  function renderForums() {
    const list = $('forum-list');
    if (!list) return;
    const upcoming = upcomingForums();
    const src = srcLink(CAMPAIGN.forums.sourceId);
    if (!upcoming.length) {
      list.innerHTML = `<p class="body">The district's fall forums have wrapped up. The budget and ballot details they covered stay on the district's Dollars and Sense page.</p>${src}`;
      return;
    }
    list.innerHTML = `
      <ul class="forum-list">${upcoming.map((s) => `
        <li class="forum-row">
          <div class="forum-when">
            <span class="forum-day">${escHtml(fmtDay(s.when))}</span>
            <span class="forum-time">${escHtml(s.time)}</span>
          </div>
          <div class="forum-place">${escHtml(s.place)}</div>
          <button class="link-btn forum-invite" data-forum="${s.i}">Invite someone &rarr;</button>
        </li>`).join('')}
      </ul>
      <p class="fine">No sign-up needed. Spanish interpretation at every session. ${src}</p>`;
  }

  /*
   * "Come with me" is a story anyone can tell, even before they have
   * one of their own. The draft names a real time and place, in the
   * writer's own voice, and lands on step 2 so they finish it.
   */
  function forumInviteText(s) {
    return `The superintendent is taking questions about the LPS budget and the mill levy override at ${s.place} on ${fmtDay(s.when)}, ${s.time.replace(/\.$/, '')}. No sign-up, and there's Spanish interpretation. Want to go with me? I'd like the company — and I'm voting yes.`;
  }

  function inviteToForum(i) {
    const s = CAMPAIGN.forums.sessions[i];
    if (!s) return;
    setDraft(forumInviteText({ ...s, when: localDate(s.date) }));
    cardTextTouched = false;
    if ($('view-studio').hidden) showView('studio');
    gotoStep(2);
    $('studio-draft').focus();
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
    if (n === 4) { renderDraftReview(); refreshTargetDetail(); }
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

    const next = upcomingForums()[0];
    const quick = $('voice-forum');
    if (quick && next) {
      quick.hidden = false;
      quick.innerHTML = `Don't have a story yet? Invite someone to the district's next budget forum —
        <button class="link-btn-inline" data-forum="${next.i}">${escHtml(fmtDayShort(next.when))} at ${escHtml(next.place)}</button>.
        "Come with me" is a story too.`;
    }
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
    renderChecklist();
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

  /*
   * The story checklist — three things the research says make a
   * post land, checked live as you type. It teaches the shape of a
   * persuasive post; it never blocks one. (Learning-orientation:
   * the writer keeps every decision.)
   */
  const PLACE_RE = new RegExp('\\b(' + CAMPAIGN.placeNames.map((p) => p.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('|') + ')\\b', 'i');
  const ASK_RE = /\b(vot(e|ing)\s+yes|yes\s+on\s+the|yes\s+for\s+lps|i(’|')?m\s+a\s+yes|vote\s+for\s+it)\b/i;
  const PERSON_RE = /\b(teacher|teachers|kid|kids|daughter|son|student|students|neighbor|neighbors|principal|coach|counselor|paraprofessional|bus driver|librarian|nurse|my class|our class|graduated|grew up)\b/i;

  function wordCount(text) {
    return text.trim() ? text.trim().split(/\s+/).length : 0;
  }

  function storyChecks(text) {
    const words = wordCount(text);
    return [
      { ok: PLACE_RE.test(text), label: 'Names a real place', hint: 'a school, a neighborhood, "Littleton" or "Centennial"' },
      { ok: PERSON_RE.test(text), label: 'Has a person in it', hint: 'a teacher, a kid, a neighbor — someone the reader can picture' },
      { ok: ASK_RE.test(text), label: 'Makes the ask', hint: '"I’m voting yes" — say it plainly, once' },
      { ok: words > 0 && words <= 120, label: 'Readable at a red light', hint: `${words} words — under 120 travels; longer is fine for email or Nextdoor` },
    ];
  }

  function renderChecklist() {
    const box = $('story-checks');
    if (!box) return;
    const text = getDraft();
    if (!text.trim()) { box.hidden = true; return; }
    box.hidden = false;
    const checks = storyChecks(text);
    const done = checks.filter((c) => c.ok).length;
    box.innerHTML = `
      <p class="checks-title">${done === checks.length ? 'That’s a post.' : 'What makes a post land'}</p>
      <ul class="checks">${checks.map((c) => `
        <li class="check ${c.ok ? 'ok' : ''}">
          <span class="check-mark" aria-hidden="true">${c.ok ? '✓' : '○'}</span>
          <span><span class="check-label">${escHtml(c.label)}</span> <span class="check-hint">${escHtml(c.hint)}</span></span>
        </li>`).join('')}
      </ul>`;
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

  const canShareFiles = (() => {
    try {
      const probe = new File([new Blob(['x'], { type: 'image/png' })], 'x.png', { type: 'image/png' });
      return !!(navigator.canShare && navigator.canShare({ files: [probe] }));
    } catch { return false; }
  })();

  function shareCardFile() {
    const canvas = $('card-canvas');
    drawCard(canvas, $('card-size').value);
    canvas.toBlob(async (blob) => {
      if (!blob) return;
      const file = new File([blob], 'lps-share-card.png', { type: 'image/png' });
      try {
        await navigator.share({ files: [file] });
      } catch { /* user cancelled */ }
    }, 'image/png');
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
    if (canShareFiles) {
      shareBtn.hidden = false;
      shareBtn.addEventListener('click', () => {
        copyDraft();
        shareCardFile();
      });
    }
    redrawCard();
  }

  /* ================================================================
     STEP 4 — send it
     Templates verified against current platform documentation —
     docs/research/share-intents.md. Never fake organic reach.

     Every target is a real <a href> (never window.open after an
     await — Safari blocks that as a popup), the words are copied to
     the clipboard in the same gesture, and a fallback line appears
     after the click so a blocked tab or a missing app never eats a
     volunteer's story (Decision 061).
  ================================================================ */
  const SITE_URL = 'https://citizensforlps.org';

  const graphemes = (() => {
    if (typeof Intl !== 'undefined' && Intl.Segmenter) {
      const seg = new Intl.Segmenter('en', { granularity: 'grapheme' });
      return (s) => [...seg.segment(s)].length;
    }
    return (s) => [...s].length;
  })();

  function trimTo(text, max) {
    if (graphemes(text) <= max) return { text, trimmed: false };
    const chars = [...text];
    return { text: chars.slice(0, Math.max(0, max - 1)).join('').replace(/\s+\S*$/, '') + '…', trimmed: true };
  }

  const SHARE_TARGETS = [
    {
      id: 'sms', name: 'Text a friend', role: 'means the most',
      steps: [
        'Think of one person who lives around here.',
        'The button opens your Messages app with your words staged.',
        'Address it, make it sound like you, send.',
      ],
      desktopNote: 'On a computer this opens Messages only if it’s set up here. If nothing happens, your words are copied — text them from your phone, or use “Pass it along” below to send this draft to your phone.',
      mode: 'url', scheme: true,
      url: (text) => `sms:?body=${encodeURIComponent(text + ' ' + SITE_URL)}`,
      button: 'Open Messages',
      contactPicker: true,
      soft: 400, softNote: 'Texts over about 400 characters read as a wall; the first line has to earn the rest.',
    },
    {
      id: 'nextdoor', name: 'Nextdoor', role: 'your actual neighbors',
      steps: [
        'The button opens Nextdoor’s composer with your words already in it.',
        'Pick your neighborhood, look it over, post.',
        'One genuine post is plenty — Nextdoor removes repeat campaigning, and neighbors tune it out anyway.',
      ],
      mode: 'url', limit: 3500,
      url: (text) => `https://nextdoor.com/sharekit/?source=lps-storyteller&body=${encodeURIComponent(text + '\n' + SITE_URL)}`,
      button: 'Open Nextdoor',
      fallback: { label: 'nextdoor.com', url: 'https://nextdoor.com/' },
    },
    {
      id: 'facebook', name: 'Facebook', role: 'groups beat feeds',
      steps: [
        'Facebook doesn’t let sites pre-fill posts, so the button copies your words first.',
        'The share box opens with the campaign link — paste your words above it, look it over, post.',
        'Even better: open a neighborhood or school group you belong to and paste it there instead.',
      ],
      mode: 'copy-open',
      url: () => `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(SITE_URL)}`,
      button: 'Copy + open Facebook',
      secondary: { label: 'Copy + open my groups instead', url: 'https://www.facebook.com/groups/' },
      fallback: { label: 'facebook.com', url: 'https://www.facebook.com/' },
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
      fallback: { label: 'web.whatsapp.com', url: 'https://web.whatsapp.com/' },
    },
    {
      id: 'messenger', name: 'Messenger', role: 'the family thread', mobileOnly: true,
      steps: [
        'Messenger takes the link but not your words, so the button copies them first.',
        'Pick the person or the thread, paste your words, send.',
      ],
      mode: 'copy-open', scheme: true,
      url: () => `fb-messenger://share/?link=${encodeURIComponent(SITE_URL)}`,
      button: 'Copy + open Messenger',
      fallback: { label: 'messenger.com', url: 'https://www.messenger.com/' },
    },
    {
      id: 'instagram', name: 'Instagram', role: 'card + caption',
      steps: [
        'Instagram has no way for a site to start a post, so this is two moves: the card, then your words.',
        IS_MOBILE
          ? 'The button copies your words and sends the card to your share sheet — pick Instagram.'
          : 'Save the card in step 3 (or do this part from your phone). The button copies your words and opens Instagram.',
        'New post → add the card → paste your caption. In a story, add the link sticker.',
      ],
      mode: 'copy-open', shareCard: true,
      url: () => 'https://www.instagram.com/',
      button: canShareFiles ? 'Copy words + share the card' : 'Copy + open Instagram',
      fallback: { label: 'instagram.com', url: 'https://www.instagram.com/' },
      soft: 2200, softNote: 'Instagram captions cap at 2,200 characters.',
    },
    {
      id: 'linkedin', name: 'LinkedIn', role: 'the professional case',
      steps: [
        'The button opens LinkedIn’s composer with your words in place.',
        'The angle that lands here: schools are why families and employers choose a town.',
        'Look it over, post.',
      ],
      mode: 'url', limit: 3000,
      url: (text) => `https://www.linkedin.com/feed/?shareActive=true&text=${encodeURIComponent(text + '\n' + SITE_URL)}`,
      button: 'Open LinkedIn',
      fallback: { label: 'the plain LinkedIn share box', url: `https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(SITE_URL)}` },
    },
    {
      id: 'email', name: 'Email', role: 'the neighbor thread',
      steps: [
        'For the book club, the HOA thread, the family list.',
        'The button opens a draft with your words in the body.',
        'Address it and send.',
      ],
      desktopNote: 'If no mail app opens, your words are copied — paste them into Gmail or whatever you use.',
      mode: 'url', scheme: true, limit: 1500,
      url: (text) => `mailto:?subject=${encodeURIComponent('Why I’m voting yes for LPS')}&body=${encodeURIComponent(text + '\n\n' + SITE_URL)}`,
      button: 'Open a draft',
    },
    {
      id: 'threads', name: 'Threads', role: 'if you’re there',
      steps: [
        'The button opens the Threads composer with your words in place.',
        'Look it over, post.',
      ],
      mode: 'url', limit: 500,
      url: (text) => `https://www.threads.com/intent/post?text=${encodeURIComponent(text)}&url=${encodeURIComponent(SITE_URL)}`,
      button: 'Open Threads',
      fallback: { label: 'threads.com', url: 'https://www.threads.com/' },
    },
    {
      id: 'bluesky', name: 'Bluesky', role: 'if you’re there',
      steps: [
        'Bluesky posts cap at 300 characters including the link.',
        'The button opens the composer with your words in place.',
        'Look it over, post.',
      ],
      mode: 'url', limit: 300 - (SITE_URL.length + 1),
      limitLabel: `300 including the campaign link, which leaves ${300 - (SITE_URL.length + 1)} for your words`,
      url: (text) => `https://bsky.app/intent/compose?text=${encodeURIComponent(text + '\n' + SITE_URL)}`,
      button: 'Open Bluesky',
      fallback: { label: 'bsky.app', url: 'https://bsky.app/' },
    },
  ];

  /* Phones lead with the personal channels; desktops with the
     composers that exist there. Same targets, honest order. */
  const MOBILE_ORDER = ['sms', 'whatsapp', 'messenger', 'nextdoor', 'facebook', 'instagram', 'email', 'linkedin', 'threads', 'bluesky'];
  const DESKTOP_ORDER = ['facebook', 'nextdoor', 'email', 'linkedin', 'whatsapp', 'sms', 'instagram', 'threads', 'bluesky'];

  function orderedTargets() {
    const order = IS_MOBILE ? MOBILE_ORDER : DESKTOP_ORDER;
    return SHARE_TARGETS
      .filter((t) => !t.mobileOnly || IS_MOBILE)
      .sort((a, b) => order.indexOf(a.id) - order.indexOf(b.id));
  }

  /*
   * Copy synchronously inside the gesture. The async Clipboard API
   * rejects with "document is not focused" when the send link opens a
   * new tab in the same click; the selection-based copy completes
   * before the navigation and works in every browser. Async is the
   * fallback for the rare engine that refuses execCommand.
   */
  function copySync(text) {
    const ta = document.createElement('textarea');
    ta.value = text;
    ta.setAttribute('readonly', '');
    ta.className = 'sr-only';
    document.body.appendChild(ta);
    ta.select();
    ta.setSelectionRange(0, text.length);
    let ok = false;
    try { ok = document.execCommand('copy'); } catch { ok = false; }
    ta.remove();
    return ok;
  }
  function copyText(text) {
    if (copySync(text)) return Promise.resolve(true);
    try {
      return navigator.clipboard.writeText(text).then(() => true, () => false);
    } catch {
      return Promise.resolve(false);
    }
  }
  function copyDraft() {
    const text = getDraft().trim();
    return text ? copyText(text) : Promise.resolve(false);
  }

  function renderDraftReview() {
    const draft = getDraft().trim();
    $('draft-review-text').textContent = draft
      ? (draft.length > 220 ? draft.slice(0, 217) + '…' : draft)
      : 'Nothing yet — tap edit and give it one honest sentence. That’s enough.';
  }

  let selectedTarget = null;

  function renderTargetGrid() {
    // The system share sheet leads on a phone (it IS the phone's
    // network list) and trails on a desktop, where it's sparse and the
    // per-network composers do the real work.
    const nativeTile = navigator.share ? `
      <button class="target-tile" data-target="native">
        <span class="target-tile-name">${IS_MOBILE ? 'Your phone' : 'This computer’s share menu'}</span>
        <span class="target-tile-role">${IS_MOBILE ? 'one tap to everything' : 'if it has one'}</span>
      </button>` : '';
    let tiles = IS_MOBILE ? nativeTile : '';
    tiles += orderedTargets().map((t) => `
      <button class="target-tile" data-target="${t.id}">
        <span class="target-tile-name">${escHtml(t.name)}</span>
        <span class="target-tile-role">${escHtml(t.role)}</span>
      </button>`).join('');
    if (!IS_MOBILE) tiles += nativeTile;
    tiles += `
      <button class="target-tile target-tile-handoff" data-target="handoff">
        <span class="target-tile-name">Pass it along</span>
        <span class="target-tile-role">${IS_MOBILE ? 'to a friend who’ll post too' : 'to your phone, or a teammate'}</span>
      </button>`;
    $('target-grid').innerHTML = tiles;

    $('target-grid').addEventListener('click', (e) => {
      const tile = e.target.closest('[data-target]');
      if (!tile) return;
      selectedTarget = tile.dataset.target;
      refreshTargetDetail();
    });
  }

  function refreshTargetDetail() {
    document.querySelectorAll('.target-tile').forEach((t) =>
      t.classList.toggle('selected', t.dataset.target === selectedTarget));
    if (!selectedTarget) return;
    if (selectedTarget === 'native') renderNativeDetail();
    else if (selectedTarget === 'handoff') renderHandoffDetail();
    else renderTargetDetail(SHARE_TARGETS.find((t) => t.id === selectedTarget));
  }

  function markSent(id) {
    sentTo.add(id);
    const tile = document.querySelector(`[data-target="${id}"]`);
    if (tile) tile.classList.add('sent');
    const n = sentTo.size;
    const tally = $('sent-tally');
    tally.hidden = false;
    tally.textContent = n === 1
      ? 'One down. Each place you share reaches people the others don’t — pick another?'
      : `You’ve taken your story to ${n} places. That’s real reach — thank you.`;
  }

  function emptyDraftDetail(detail, name) {
    detail.innerHTML = `
      <p class="target-detail-name">${escHtml(name)}</p>
      <p class="body">There’s nothing to send yet. One honest sentence is enough.</p>
      <button class="btn" data-wstep="2">Write your words &rarr;</button>`;
  }

  function renderNativeDetail() {
    const detail = $('target-detail');
    detail.hidden = false;
    const text = getDraft().trim();
    if (!text) return emptyDraftDetail(detail, IS_MOBILE ? 'Your phone’s share sheet' : 'This computer’s share menu');
    detail.innerHTML = `
      <p class="target-detail-name">${IS_MOBILE ? 'Your phone’s share sheet' : 'This computer’s share menu'}</p>
      <ol class="micro-steps">
        <li>${IS_MOBILE ? 'The button opens your phone’s own share menu — Messages, WhatsApp, Messenger, Instagram, everything installed.' : 'The button opens the system share menu — on a Mac that’s Messages, Mail, AirDrop and whatever else is installed; on Windows, the apps you’ve set up.'}</li>
        <li>Pick the app, pick the person or audience.</li>
        <li>Your words and the campaign link ride along (Facebook and Instagram drop the words — they’re on your clipboard, paste them).</li>
      </ol>
      <button class="btn" id="target-action">Share&hellip;</button>
      <p class="fallback-line" id="target-fallback" hidden></p>`;
    $('target-action').addEventListener('click', async () => {
      copyText(text);
      try {
        await navigator.share({ title: 'Why I’m voting yes for LPS', text, url: SITE_URL });
        markSent('native');
      } catch {
        showFallback('The share menu didn’t open. Your words are copied — pick a network below and paste them.');
      }
    });
  }

  function showFallback(html) {
    const line = $('target-fallback');
    if (!line) return;
    line.hidden = false;
    line.innerHTML = html;
  }

  function fitLine(t, text) {
    const n = graphemes(text);
    if (t.limit && n > t.limit) {
      return `<p class="fit-line fit-over">Your words run ${fmtNum(n)} characters; ${escHtml(t.name)} allows ${escHtml(t.limitLabel || fmtNum(t.limit))}. We’ll trim the end with an ellipsis — or <button class="link-btn-inline" data-wstep="2">tighten it yourself</button>.</p>`;
    }
    if (t.soft && n > t.soft) {
      return `<p class="fit-line">${fmtNum(n)} characters. ${escHtml(t.softNote)}</p>`;
    }
    if (t.limit) {
      return `<p class="fit-line fit-ok">Fits — ${fmtNum(n)} of ${fmtNum(t.limit)} characters.</p>`;
    }
    return '';
  }

  function renderTargetDetail(t) {
    const detail = $('target-detail');
    detail.hidden = false;
    const raw = getDraft().trim();
    if (!raw) return emptyDraftDetail(detail, t.name);

    const { text } = t.limit ? trimTo(raw, t.limit) : { text: raw };
    const href = t.url(text);
    const urlTooLong = t.scheme && href.length > 1900 && t.id === 'email';

    let extra = '';
    if (t.contactPicker && 'contacts' in navigator && 'select' in navigator.contacts) {
      extra += `<div class="target-detail-extra">
        <button class="btn btn-quiet" id="target-contacts">Or pick straight from your contacts</button>
        <p class="fine">The picking happens on your phone — nothing is uploaded anywhere.</p>
      </div>`;
    }
    if (t.secondary) {
      extra += `<div class="target-detail-extra">
        <a class="btn btn-quiet target-secondary" href="${escAttr(t.secondary.url)}" target="_blank" rel="noopener">${escHtml(t.secondary.label)}</a>
      </div>`;
    }

    const primary = t.shareCard && canShareFiles
      ? `<button class="btn" id="target-action">${escHtml(t.button)}</button>`
      : `<a class="btn" id="target-action" href="${escAttr(href)}" ${t.scheme ? '' : 'target="_blank" rel="noopener"'}>${escHtml(t.button)}</a>`;

    detail.innerHTML = `
      <p class="target-detail-name">${escHtml(t.name)}</p>
      <ol class="micro-steps">${t.steps.map((s) => `<li>${escHtml(s)}</li>`).join('')}</ol>
      ${fitLine(t, raw)}
      ${!IS_MOBILE && t.desktopNote ? `<p class="fine">${escHtml(t.desktopNote)}</p>` : ''}
      <div class="target-actions">
        ${primary}
        <button class="btn btn-quiet" id="target-copy">Copy my words</button>
      </div>
      ${extra}
      <p class="fallback-line" id="target-fallback" hidden></p>`;

    const fallbackHtml = () => {
      const open = t.fallback
        ? ` Open <a href="${escAttr(t.fallback.url)}" target="_blank" rel="noopener">${escHtml(t.fallback.label)}</a> and paste them.`
        : '';
      return `Didn’t open? Your words are on your clipboard.${open}`;
    };

    $('target-action').addEventListener('click', (e) => {
      // Copy in the same gesture — no await before the navigation, or
      // Safari treats the new tab as a popup and blocks it.
      copyText(text).then((ok) => {
        if (!ok) showFallback('Your browser wouldn’t copy automatically — use “Copy my words” and paste.');
      });
      if (t.shareCard && canShareFiles) {
        e.preventDefault();
        shareCardFile();
      }
      markSent(t.id);
      setTimeout(() => {
        if ($('target-fallback')?.hidden) showFallback(fallbackHtml());
      }, urlTooLong ? 0 : 2500);
    });

    $('target-copy').addEventListener('click', () => {
      copyText(text).then((ok) => {
        $('target-copy').textContent = ok ? 'Copied' : 'Select the text in step 2 and copy it';
        setTimeout(() => { $('target-copy').textContent = 'Copy my words'; }, 2000);
      });
    });

    document.querySelector('.target-secondary')?.addEventListener('click', () => {
      copyText(text);
      markSent(t.id);
      setTimeout(() => showFallback(fallbackHtml()), 2500);
    });

    const contactsBtn = $('target-contacts');
    if (contactsBtn) {
      contactsBtn.addEventListener('click', async () => {
        try {
          const picked = await navigator.contacts.select(['tel', 'name'], { multiple: false });
          const tel = picked?.[0]?.tel?.[0];
          if (tel) {
            window.location.href = `sms:${encodeURIComponent(tel)}?body=${encodeURIComponent(text + ' ' + SITE_URL)}`;
            markSent('sms');
          }
        } catch { /* user cancelled */ }
      });
    }
  }

  /* ================================================================
     PASS IT ALONG — the draft travels in the URL
     Drafts otherwise live only in this browser. A link that carries
     the words lets a volunteer finish on their phone, and lets the
     team hand a starting draft to someone who'll make it their own.
  ================================================================ */
  const b64url = {
    encode: (s) => btoa(String.fromCharCode(...new TextEncoder().encode(s))).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, ''),
    decode: (s) => {
      const b = s.replace(/-/g, '+').replace(/_/g, '/');
      const bin = atob(b + '='.repeat((4 - b.length % 4) % 4));
      return new TextDecoder().decode(Uint8Array.from(bin, (c) => c.charCodeAt(0)));
    },
  };

  function draftLink() {
    const base = `${location.origin}${location.pathname}`;
    return `${base}?view=studio&step=4&d=${b64url.encode(getDraft().trim())}`;
  }

  function renderHandoffDetail() {
    const detail = $('target-detail');
    detail.hidden = false;
    const text = getDraft().trim();
    if (!text) return emptyDraftDetail(detail, 'Pass it along');
    const link = draftLink();
    const tooLong = link.length > 2000;
    detail.innerHTML = `
      <p class="target-detail-name">Pass it along</p>
      <ol class="micro-steps">
        <li>This link opens the studio with your words already loaded — nothing is stored anywhere but in the link itself.</li>
        <li>${IS_MOBILE
          ? 'Send it to a friend who’d post something like it; they’ll rewrite it in their own voice.'
          : 'Text or email it to yourself to finish on your phone (Instagram and Messages live there), or send it to a teammate as a starting draft.'}</li>
      </ol>
      ${tooLong ? '<p class="fit-line">This draft is long for a link; some apps cut long links off. Shorten it a little if the link doesn’t open cleanly.</p>' : ''}
      <input class="field-input handoff-link" id="handoff-link" type="text" readonly value="${escAttr(link)}" aria-label="Link to this draft">
      <div class="target-actions">
        <button class="btn" id="handoff-copy">Copy the link</button>
        <a class="btn btn-quiet" id="handoff-email" href="mailto:?subject=${encodeURIComponent('My LPS story draft')}&body=${encodeURIComponent('Finish this on your phone: ' + link)}">Email it to me</a>
        ${navigator.share ? '<button class="btn btn-quiet" id="handoff-share">Share the link&hellip;</button>' : ''}
      </div>`;
    $('handoff-copy').addEventListener('click', () => {
      copyText(link).then((ok) => {
        $('handoff-copy').textContent = ok ? 'Link copied' : 'Select the link above and copy it';
        setTimeout(() => { $('handoff-copy').textContent = 'Copy the link'; }, 2000);
      });
    });
    $('handoff-link').addEventListener('focus', (e) => e.target.select());
    $('handoff-share')?.addEventListener('click', async () => {
      try { await navigator.share({ title: 'My LPS story draft', url: link }); } catch { /* cancelled */ }
    });
  }

  function importDraftFromURL() {
    const params = new URLSearchParams(location.search);
    const d = params.get('d');
    if (!d) return null;
    let incoming = '';
    try { incoming = b64url.decode(d).trim(); } catch { return null; }
    params.delete('d');
    params.delete('step');
    const clean = `${location.pathname}?${params.toString()}`.replace(/\?$/, '?');
    history.replaceState({ view: 'studio' }, '', clean);
    if (!incoming) return null;
    const existing = getDraft().trim();
    setDraft(incoming);
    cardTextTouched = false;
    if (existing && existing !== incoming) {
      const notice = $('draft-notice');
      notice.hidden = false;
      notice.innerHTML = `We loaded the draft from the link you opened. Your earlier draft is still here —
        <button class="link-btn-inline" id="draft-restore">bring it back</button>.`;
      $('draft-restore').addEventListener('click', () => {
        setDraft(existing);
        notice.hidden = true;
      });
    }
    return Number(new URLSearchParams(location.search).get('step')) || 4;
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
    $('calc-home-value').value = fmtNum(tc.defaultHomeValue);
    $('calc-mills').value = tc.estimatedMills.value;
    $('calc-rate').value = (tc.residentialAssessmentRate.value * 100).toFixed(2);

    const unverified = !tc.estimatedMills.verified || !tc.residentialAssessmentRate.verified;
    $('calc-est-note').textContent = unverified
      ? 'The assessment rate and the $25-per-$100,000 estimate are the state’s and the district’s own published figures. The mill number is derived from them and stays an estimate until the county certifies the ballot language this fall — this page will be updated the day the certified figure exists.'
      : 'Figures reflect the certified ballot language and published official rates.';

    const ex = tc.districtExample;
    $('calc-sources').innerHTML = `
      The calculator opens on the district's own example — a ${fmtUSD(ex.homeValue)} home at "${escHtml(ex.monthlyText)}" — so you can check their arithmetic before you check yours (<a href="${SOURCES[ex.sourceId].url}" target="_blank" rel="noopener">${escHtml(SOURCES[ex.sourceId].label)}</a>).
      Assessment rate (7.05% for 2026): <a href="${SOURCES[tc.residentialAssessmentRate.sourceId].url}" target="_blank" rel="noopener">${escHtml(SOURCES[tc.residentialAssessmentRate.sourceId].label)}</a>.
      The district's estimate — "approximately $25 annually for every $100,000 of home value":
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
        `For that, teachers get a raise instead of a freeze, the furlough day comes off the calendar, and every dollar stays in LPS schools. I’m voting yes.`
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
    const seen = new Set();
    $('sources-list').innerHTML = `<ul class="sources-list">` +
      Object.values(SOURCES).filter((s) => !seen.has(s.url) && seen.add(s.url)).map((s) =>
        `<li><a href="${s.url}" target="_blank" rel="noopener">${escHtml(s.label)}</a></li>`).join('') +
      `</ul>`;
  }

  /* ================================================================
     BOOT
  ================================================================ */
  function init() {
    renderBallotSummary();
    renderForums();
    renderVoices();
    initPromptClicks();
    initDraft();
    renderFactList();
    initCardMaker();
    renderTargetGrid();
    initCalculator();
    renderPlaybook();
    renderSources();
    const importedStep = importDraftFromURL();
    const requestedStep = Number(new URLSearchParams(location.search).get('step')) || null;
    showView(importedStep ? 'studio' : initialViewFromURL(), true);
    gotoStep(importedStep || requestedStep || 1);
  }

  init();
})();
