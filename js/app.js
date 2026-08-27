/**
 * Tell the Story of Our Schools — Main Application Logic
 *
 * Vanilla JS, single IIFE. Views toggled by showView(); URL state via
 * ?view= (shareable). All facts come from js/data.js and every fact
 * renders WITH its source (Decisions 054, 058). The share studio's
 * platform intents live in SHARE_TARGETS below — verify against
 * current platform docs before changing (Decision 060).
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
  const VIEW_NAMES = ['home', 'story', 'studio', 'cost', 'playbook'];
  const VIEW_TITLES = {
    home: 'Tell the Story of Our Schools',
    story: 'Your Story — Tell the Story of Our Schools',
    studio: 'Share Studio — Tell the Story of Our Schools',
    cost: 'What It Costs — Tell the Story of Our Schools',
    playbook: 'Team Playbook — Tell the Story of Our Schools',
  };

  function showView(name, fromHistory = false, anchor = null) {
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
    const main = $('main-content');
    if (anchor && $(anchor)) {
      $(anchor).scrollIntoView({ block: 'start' });
    } else {
      main.scrollTop = 0;
    }
  }

  document.addEventListener('click', (e) => {
    const target = e.target.closest('[data-view]');
    if (target) showView(target.dataset.view, false, target.dataset.anchor || null);
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
     YOUR STORY — prompts seed the studio draft
  ================================================================ */
  function renderPrompts() {
    $('prompt-groups').innerHTML = CAMPAIGN.storyPrompts.map((group, gi) => `
      <div class="prompt-group">
        <p class="prompt-voice">${escHtml(group.voice)}</p>
        ${group.prompts.map((p, pi) => `
          <div class="prompt-card" data-prompt="${gi}:${pi}" role="button" tabindex="0"
               aria-label="Use this prompt in the share studio">
            &ldquo;${escHtml(p.text)}&rdquo;
            <span class="prompt-hint">${escHtml(p.hint)} Tap to start writing.</span>
          </div>`).join('')}
      </div>`).join('');

    const usePrompt = (key) => {
      const [gi, pi] = key.split(':').map(Number);
      const prompt = CAMPAIGN.storyPrompts[gi]?.prompts[pi];
      if (!prompt) return;
      setDraft(prompt.text + ' ');
      showView('studio');
      $('studio-draft').focus();
    };
    $('prompt-groups').addEventListener('click', (e) => {
      const card = e.target.closest('[data-prompt]');
      if (card) usePrompt(card.dataset.prompt);
    });
    $('prompt-groups').addEventListener('keydown', (e) => {
      const card = e.target.closest('[data-prompt]');
      if (card && (e.key === 'Enter' || e.key === ' ')) {
        e.preventDefault();
        usePrompt(card.dataset.prompt);
      }
    });
  }

  /* ================================================================
     STUDIO — draft, facts, card maker, share targets, relational
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

  /* ---- Card maker (canvas → PNG) ---- */
  const CARD_SIZES = {
    square: { w: 1080, h: 1080 },
    story: { w: 1080, h: 1920 },
    wide: { w: 1200, h: 630 },
  };

  function drawCard(canvas, size) {
    const { w, h } = CARD_SIZES[size];
    canvas.width = w;
    canvas.height = h;
    const ctx = canvas.getContext('2d');
    const text = $('card-text').value.trim() || 'I’m voting yes on the LPS mill levy override.';

    // Warm paper ground + slate ink + green accents (brand palette)
    ctx.fillStyle = '#FBFAF7';
    ctx.fillRect(0, 0, w, h);
    ctx.fillStyle = '#90CA65';
    ctx.fillRect(0, 0, w, Math.round(h * 0.012));

    const pad = Math.round(w * 0.09);
    const maxWidth = w - pad * 2;

    // Star (the logo's motif, not the logo itself — this card is the
    // sharer's own voice, not a committee production; Decision 058)
    ctx.fillStyle = '#90CA65';
    const starSize = Math.round(w * 0.045);
    drawStar(ctx, pad + starSize / 2, Math.round(h * 0.16), 5, starSize / 2, starSize / 4.4);

    // Main text, wrapped, in Lora
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

    // Footer rule + pointer to the campaign's official home
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

  function initCardMaker() {
    const canvas = $('card-canvas');
    const redraw = () => {
      // Wait for the webfonts so the preview matches the download
      document.fonts.ready.then(() => drawCard(canvas, $('card-size').value));
    };
    $('card-text').addEventListener('input', redraw);
    $('card-size').addEventListener('change', redraw);
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

    // Mobile: hand the PNG straight to the share sheet (this is the
    // real route into Instagram — image attached, caption pasted).
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
    redraw();
  }

  /* ---- Share targets ----
   * Each target: how a static site can hand the volunteer's words to
   * that platform with the least friction. mode:
   *   'url'  — open an intent URL with the text/link prefilled
   *   'copy' — copy the draft, then open the platform (no prefill API)
   * Templates verified against current platform documentation — see
   * docs/research/share-intents.md. Never fake organic reach.
   */
  const SITE_URL = 'https://citizensforlps.org';

  /*
   * Ordered by friction (lowest first), per the verified research in
   * docs/research/share-intents.md. Nextdoor leads: it has an
   * official prefill URL AND it's this campaign's local-persuasion
   * channel. Facebook/Instagram forbid prefill by policy — those use
   * the copy-then-open flow, honestly labeled.
   */
  const SHARE_TARGETS = [
    {
      id: 'nextdoor', name: 'Nextdoor',
      tip: 'Your actual neighbors. Opens Nextdoor’s composer with your words already in place — you pick the neighborhood and post. One genuine post per phase; never on repeat.',
      mode: 'url',
      url: (text) => `https://nextdoor.com/sharekit/?source=lps-storyteller&body=${encodeURIComponent(text + '\n' + SITE_URL)}`,
      button: 'Open with your words',
    },
    {
      id: 'sms', name: 'Text message',
      tip: 'The channel that moves votes most. Opens your messages app with your words staged — you choose who gets it.',
      mode: 'url',
      url: (text) => `sms:?body=${encodeURIComponent(text + ' ' + SITE_URL)}`,
      button: 'Open with your words',
    },
    {
      id: 'whatsapp', name: 'WhatsApp',
      tip: 'Opens WhatsApp with your words ready to send — pick the person or the group chat.',
      mode: 'url',
      url: (text) => `https://wa.me/?text=${encodeURIComponent(text + '\n' + SITE_URL)}`,
      button: 'Open with your words',
    },
    {
      id: 'facebook', name: 'Facebook',
      tip: 'Facebook doesn’t let websites prefill your post, so this copies your words first, then opens the share box — paste and post. Even better: paste it straight into a local group you belong to.',
      mode: 'copy-open',
      url: () => `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(SITE_URL)}`,
      button: 'Copy words + open',
    },
    {
      id: 'instagram', name: 'Instagram',
      tip: 'Instagram can’t be prefilled from the web at all. Download your share card above, then this copies your caption and opens Instagram — attach the card, paste, post. In a story, add the link sticker.',
      mode: 'copy-open',
      url: () => 'https://www.instagram.com/',
      button: 'Copy caption + open',
    },
    {
      id: 'linkedin', name: 'LinkedIn',
      tip: 'Opens the LinkedIn composer with your words in place. The professional angle lands here: schools are part of why families and employers choose a town.',
      mode: 'url',
      url: (text) => `https://www.linkedin.com/feed/?shareActive=true&text=${encodeURIComponent(text + '\n' + SITE_URL)}`,
      button: 'Open with your words',
    },
    {
      id: 'email', name: 'Email',
      tip: 'For the neighbor, the book club, the HOA thread. Opens a draft with your words.',
      mode: 'url',
      url: (text) => `mailto:?subject=${encodeURIComponent('Why I’m voting yes for LPS')}&body=${encodeURIComponent(text + '\n\n' + SITE_URL)}`,
      button: 'Open a draft',
    },
    {
      id: 'threads', name: 'Threads',
      tip: 'Opens the Threads composer with your words in place.',
      mode: 'url',
      url: (text) => `https://www.threads.com/intent/post?text=${encodeURIComponent(text)}&url=${encodeURIComponent(SITE_URL)}`,
      button: 'Open with your words',
    },
    {
      id: 'bluesky', name: 'Bluesky',
      tip: 'Opens the Bluesky composer with your words in place. Bluesky posts cap at 300 characters — keep it short here.',
      mode: 'url',
      url: (text) => `https://bsky.app/intent/compose?text=${encodeURIComponent((text.length > 260 ? text.slice(0, 257) + '…' : text) + '\n' + SITE_URL)}`,
      button: 'Open with your words',
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

  function renderShareTargets() {
    // Mobile fast path: the native share sheet reaches Messages,
    // WhatsApp, Messenger, Instagram, and more in one tap.
    let nativeRow = '';
    if (navigator.share) {
      nativeRow = `
      <div class="share-target">
        <div class="share-target-info">
          <p class="share-target-name">Your phone's share sheet</p>
          <p class="share-target-tip">One tap to everything installed on your phone — Messages, WhatsApp, Messenger, Instagram, and the rest.</p>
        </div>
        <button class="share-target-btn" id="native-share">Share&hellip;</button>
      </div>`;
    }
    $('share-targets').innerHTML = nativeRow + SHARE_TARGETS.map((t, i) => `
      <div class="share-target">
        <div class="share-target-info">
          <p class="share-target-name">${escHtml(t.name)}</p>
          <p class="share-target-tip">${escHtml(t.tip)}</p>
        </div>
        <button class="share-target-btn" data-target="${i}">${escHtml(t.button)}</button>
      </div>`).join('');

    const nativeBtn = $('native-share');
    if (nativeBtn) {
      nativeBtn.addEventListener('click', async () => {
        const text = getDraft().trim();
        if (!text) {
          $('studio-draft').focus();
          return;
        }
        try {
          await navigator.share({ text, url: SITE_URL });
        } catch { /* user cancelled */ }
      });
    }

    $('share-targets').addEventListener('click', async (e) => {
      const btn = e.target.closest('[data-target]');
      if (!btn) return;
      const target = SHARE_TARGETS[Number(btn.dataset.target)];
      const text = getDraft().trim();
      if (!text) {
        showView('studio');
        $('studio-draft').focus();
        $('studio-draft').placeholder = 'Write a few words first — even one sentence.';
        return;
      }
      if (target.mode === 'copy-open') {
        const copied = await copyDraft();
        btn.textContent = copied ? 'Copied — opening…' : 'Opening…';
        setTimeout(() => { btn.textContent = target.button; }, 2500);
        window.open(target.url(text), '_blank', 'noopener');
      } else {
        window.open(target.url(text), '_blank', 'noopener');
      }
    });
  }

  /* ---- Person to person ---- */
  function renderRelationalTools() {
    const el = $('relational-tools');
    const personalNote = () =>
      getDraft().trim() ||
      'Hey — you live in the LPS area, right? The schools have a mill levy override on the November ballot and it matters a lot to our family. Can I tell you about it?';

    let html = `
      <div class="share-target">
        <div class="share-target-info">
          <p class="share-target-name">Text someone you know</p>
          <p class="share-target-tip">Opens your messages with a note ready — your draft if you’ve written one, a friendly opener if you haven’t. Edit it to sound like you before sending.</p>
        </div>
        <button class="share-target-btn" id="rel-sms">Open messages</button>
      </div>
      <div class="share-target">
        <div class="share-target-info">
          <p class="share-target-name">WhatsApp someone you know</p>
          <p class="share-target-tip">Same idea, for the group chat or the friend abroad in your neighborhood WhatsApp.</p>
        </div>
        <button class="share-target-btn" id="rel-wa">Open WhatsApp</button>
      </div>`;

    // Contact Picker API — progressive: only where supported
    if ('contacts' in navigator && 'select' in navigator.contacts) {
      html += `
      <div class="share-target">
        <div class="share-target-info">
          <p class="share-target-name">Pick from your contacts</p>
          <p class="share-target-tip">Choose a person from your own contacts and we’ll open a text to them. Nothing is uploaded anywhere — the picking happens on your phone.</p>
        </div>
        <button class="share-target-btn" id="rel-contacts">Choose a person</button>
      </div>`;
    }
    el.innerHTML = html;

    $('rel-sms').addEventListener('click', () => {
      window.open(`sms:?body=${encodeURIComponent(personalNote())}`, '_self');
    });
    $('rel-wa').addEventListener('click', () => {
      window.open(`https://wa.me/?text=${encodeURIComponent(personalNote())}`, '_blank', 'noopener');
    });
    const contactsBtn = $('rel-contacts');
    if (contactsBtn) {
      contactsBtn.addEventListener('click', async () => {
        try {
          const picked = await navigator.contacts.select(['tel', 'name'], { multiple: false });
          const tel = picked?.[0]?.tel?.[0];
          if (tel) {
            window.open(`sms:${encodeURIComponent(tel)}?body=${encodeURIComponent(personalNote())}`, '_self');
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
      showView('studio');
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
    renderPrompts();
    initDraft();
    renderFactList();
    initCardMaker();
    renderShareTargets();
    renderRelationalTools();
    initCalculator();
    renderPlaybook();
    renderSources();
    showView(initialViewFromURL(), true);
  }

  init();
})();
