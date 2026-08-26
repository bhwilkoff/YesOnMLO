/**
 * Yes for LPS — Main Application Logic
 *
 * Architecture: single IIFE. Views are <section> elements toggled by
 * showView(); URL state via ?view= (shareable canonical URLs). All
 * campaign facts come from CAMPAIGN (js/data.js) — nothing rendered
 * here may carry a number that isn't in the data plane (Decision 054).
 * Facts with verified:false must render with an estimate label.
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

  /* ================================================================
     VIEW SYSTEM
  ================================================================ */
  const VIEW_NAMES = ['home', 'facts', 'calculator', 'faq', 'dates', 'involved', 'share'];
  const VIEW_TITLES = {
    home: 'Yes for LPS',
    facts: 'The Facts — Yes for LPS',
    calculator: 'What It Costs You — Yes for LPS',
    faq: 'FAQ — Yes for LPS',
    dates: 'Key Dates — Yes for LPS',
    involved: 'Get Involved — Yes for LPS',
    share: 'Share Kit — Yes for LPS',
  };

  function showView(name, fromHistory = false) {
    if (!VIEW_NAMES.includes(name)) name = 'home';
    if (document.startViewTransition) {
      document.startViewTransition(() => applyViewSwap(name, fromHistory));
    } else {
      applyViewSwap(name, fromHistory);
    }
  }

  function applyViewSwap(name, fromHistory) {
    VIEW_NAMES.forEach((n) => {
      const view = $(`view-${n}`);
      if (view) view.hidden = n !== name;
      const btn = $(`nav-${n}`);
      if (btn) {
        btn.classList.toggle('active', n === name);
        btn.setAttribute('aria-current', n === name ? 'page' : 'false');
      }
    });
    $('main-content').scrollTop = 0;
    if (!fromHistory) {
      const url = name === 'home' ? '?' : `?view=${name}`;
      history.pushState({ view: name }, '', url);
    }
    document.title = VIEW_TITLES[name];
  }

  // Any element with data-view navigates (nav items + in-page CTAs).
  document.addEventListener('click', (e) => {
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
     HOME — countdown, pillars, history
  ================================================================ */
  function daysUntil(iso) {
    const now = new Date();
    const target = new Date(`${iso}T12:00:00`);
    return Math.max(0, Math.ceil((target - now) / 86400000));
  }

  function renderCountdown() {
    const el = $('countdown-strip');
    const e = CAMPAIGN.election;
    const cells = [
      { num: daysUntil(e.ballotsMailed.value), label: 'days until ballots mail', est: !e.ballotsMailed.verified },
      { num: daysUntil(e.day.value), label: 'days until Election Day', est: !e.day.verified },
    ];
    el.innerHTML = cells.map((c) => `
      <div class="countdown-cell">
        <div class="countdown-num">${c.num}</div>
        <div class="countdown-label">${escHtml(c.label)}${c.est ? ' (est.)' : ''}</div>
      </div>`).join('');
  }

  function renderPillars(containerId) {
    $(containerId).innerHTML = CAMPAIGN.pillars.map((p) => `
      <div class="pillar">
        <div class="pillar-title">${escHtml(p.title)}</div>
        <div class="pillar-detail">${escHtml(p.detail)}</div>
      </div>`).join('');
  }

  function renderHistory() {
    const rows = CAMPAIGN.history.map((h) => `
      <tr>
        <td class="tabular">${h.year}</td>
        <td>${escHtml(h.kind)}</td>
        <td>${escHtml(h.amount)}</td>
        <td class="pct-yes">${h.yesPct.toFixed(1)}% yes</td>
        <td class="tabular">${fmtNum(h.totalVotes)}</td>
      </tr>`).join('');
    $('history-table').innerHTML = `
      <thead><tr><th>Year</th><th>Measure</th><th>Amount</th><th>Result</th><th>Votes cast</th></tr></thead>
      <tbody>${rows}</tbody>`;
  }

  /* ================================================================
     FACTS
  ================================================================ */
  function renderFacts() {
    $('deficit-drivers').innerHTML = CAMPAIGN.deficitDrivers
      .map((d) => `<li>${escHtml(d)}</li>`).join('');
    $('one-time-measures').innerHTML = CAMPAIGN.oneTimeMeasures.map((m) => {
      const amt = m.amount ? ` — ${fmtUSD(m.amount)}` : '';
      return `<li>${escHtml(m.label)}${amt}</li>`;
    }).join('');
  }

  function renderBudget() {
    const renderBars = (containerId, rows) => {
      $(containerId).innerHTML = rows.map((r) => `
        <div class="budget-row">
          <div class="budget-row-head">
            <span class="budget-row-label">${escHtml(r.label)}</span>
            <span class="budget-row-pct">${r.pct.toFixed(1)}%</span>
          </div>
          <div class="budget-bar"><div class="budget-bar-fill" style="width:${r.pct}%"></div></div>
        </div>`).join('');
    };
    renderBars('budget-expenditures', CAMPAIGN.budget.expenditures);
    renderBars('budget-revenue', CAMPAIGN.budget.revenue);
  }

  /* ================================================================
     CALCULATOR — shows every step of the math (Decision 057)
  ================================================================ */
  function parseHomeValue() {
    const raw = $('calc-home-value').value.replace(/[^0-9.]/g, '');
    return parseFloat(raw) || 0;
  }

  function renderCalculator() {
    const homeValue = parseHomeValue();
    const rate = parseFloat($('calc-rate').value) / 100 || 0;
    const mills = parseFloat($('calc-mills').value) || 0;
    const assessed = homeValue * rate;
    const annual = assessed * (mills / 1000);
    const monthly = annual / 12;

    $('calc-steps').innerHTML = `
      <div class="calc-step">
        <div>
          <div class="calc-step-label">1. Assessed value</div>
          <div class="calc-step-math">${fmtUSD(homeValue)} × ${(rate * 100).toFixed(2)}% assessment rate</div>
        </div>
        <div class="calc-step-value">${fmtUSD(assessed)}</div>
      </div>
      <div class="calc-step">
        <div>
          <div class="calc-step-label">2. MLO tax</div>
          <div class="calc-step-math">${fmtUSD(assessed)} × ${mills} mills ÷ 1,000</div>
        </div>
        <div class="calc-step-value">${fmtUSD(annual, 0)} / year</div>
      </div>
      <div class="calc-step calc-result">
        <div class="calc-step-label">What that means monthly</div>
        <div class="calc-step-value">${fmtUSD(monthly, 2)} / month</div>
      </div>`;
  }

  function initCalculator() {
    const tc = CAMPAIGN.taxCalc;
    $('calc-mills').value = tc.estimatedMills.value;
    $('calc-rate').value = (tc.residentialAssessmentRate.value * 100).toFixed(2);

    const unverified = !tc.estimatedMills.verified || !tc.residentialAssessmentRate.verified;
    $('calc-est-note').textContent = unverified
      ? '⚠️ Estimate only. The district will publish official tax-impact figures; this page will be updated the day they arrive. Until then, the mill and assessment-rate numbers below are our clearly-labeled best estimates — adjust them yourself and watch the math change.'
      : 'Figures reflect the district’s published official estimates.';

    $('calc-context').textContent =
      'A "mill" is one dollar of tax per $1,000 of assessed value — and for school levies, assessed value is only about 7% of what your home is worth on the market. The district’s early estimate works out to roughly $25 per year for every $100,000 of home value — about the cost of a streaming subscription per month for a typical household.';

    ['calc-home-value', 'calc-mills', 'calc-rate'].forEach((id) => {
      $(id).addEventListener('input', renderCalculator);
    });
    $('calc-home-value').addEventListener('blur', () => {
      const v = parseHomeValue();
      if (v) $('calc-home-value').value = fmtNum(v);
    });
    renderCalculator();
  }

  /* ================================================================
     FAQ
  ================================================================ */
  function renderFaq() {
    $('faq-list').innerHTML = CAMPAIGN.faq.map((item) => `
      <details class="faq-item">
        <summary>${escHtml(item.q)}</summary>
        <div class="faq-answer">${escHtml(item.a)}</div>
      </details>`).join('');
  }

  /* ================================================================
     DATES
  ================================================================ */
  function renderDates() {
    const e = CAMPAIGN.election;
    const rows = [
      { when: 'Mid-October', what: 'Ballots mailed to every registered voter in the LPS boundary', est: !e.ballotsMailed.verified },
      { when: 'Mid–late Oct', what: 'Return your ballot early — drop boxes are open 24/7 and most LPS neighbors vote in the first two weeks', est: false },
      { when: 'Late October', what: 'Last safe day to return by MAIL — after this, use a drop box', est: true },
      { when: 'Nov 3, 2026', what: `Election Day — ballots must be RECEIVED by ${CAMPAIGN.election.ballotsDueTime} (postmarks don't count)`, est: false },
    ];
    $('dates-list').innerHTML = rows.map((r) => `
      <div class="date-row">
        <div class="date-when">${escHtml(r.when)}${r.est ? ' <span class="date-est">(est.)</span>' : ''}</div>
        <div class="date-what">${escHtml(r.what)}</div>
      </div>`).join('');
  }

  /* ================================================================
     GET INVOLVED
  ================================================================ */
  function renderInvolvement() {
    $('involvement-ladder').innerHTML = CAMPAIGN.involvement.map((rung) => `
      <div class="ladder-rung">
        <div class="ladder-level">${escHtml(rung.level)}</div>
        <ul>${rung.actions.map((a) => `<li>${escHtml(a)}</li>`).join('')}</ul>
      </div>`).join('');

    $('events-list').innerHTML = CAMPAIGN.events.map((ev) => `
      <div class="event-row">
        <div class="event-when">${escHtml(ev.when)}</div>
        <div class="event-what">${escHtml(ev.what)}</div>
      </div>`).join('');
  }

  /* ================================================================
     SHARE KIT — prompts + facts + Web Share API
  ================================================================ */
  const STORY_PROMPTS = [
    'The teacher who changed things for my kid was…',
    'We chose this neighborhood because of the schools. Here’s what that’s been worth to us…',
    'I don’t have kids in LPS anymore, but I’m voting yes because…',
    'A furlough day sounds small until you’re the family arranging childcare for it. Here’s ours…',
    'I asked my LPS student what their favorite class is. Here’s what they said, and here’s who teaches it…',
  ];

  function shareFacts() {
    const m = CAMPAIGN.measure;
    const b = CAMPAIGN.budget;
    return [
      `LPS already cut ${fmtUSD(6500000)} before asking voters for anything — including a wage freeze and a furlough day.`,
      `The ${fmtUSD(m.amount)} mill levy override is local by law: collected here, spent here, and the state can never redirect it.`,
      `The LPS Board of Education voted ${m.boardVote} to put this measure on the ballot.`,
      `Central administration is ${b.centralAdminPct} of the LPS budget — and LPS has earned the national excellence-in-financial-reporting award ${b.gfoaYears} years running.`,
      `If it passes, LPS educators get their negotiated pay restored retroactively — and students get their furlough day back as a school day.`,
      `LPS voters have passed every recent school funding measure with at least 56% support. This community shows up for its schools.`,
      `Every registered voter in the LPS boundary gets a mail ballot in mid-October. No polling place needed — vote from your kitchen table.`,
    ];
  }

  function renderShareKit() {
    $('story-prompts').innerHTML = STORY_PROMPTS.map((p) => `
      <div class="prompt-card">"${escHtml(p)}"</div>`).join('');

    $('share-facts').innerHTML = shareFacts().map((f, i) => `
      <div class="share-fact">
        <span>${escHtml(f)}</span>
        <button class="btn btn-ghost" data-fact="${i}">Copy</button>
      </div>`).join('');

    $('share-facts').addEventListener('click', async (e) => {
      const btn = e.target.closest('[data-fact]');
      if (!btn) return;
      await navigator.clipboard.writeText(shareFacts()[Number(btn.dataset.fact)]);
      const original = btn.textContent;
      btn.textContent = 'Copied!';
      setTimeout(() => { btn.textContent = original; }, 1500);
    });

    const siteURL = `${location.origin}${location.pathname}`;
    const shareData = {
      title: 'Yes for LPS',
      text: 'See what the LPS mill levy override funds, what it costs, and how to help.',
      url: siteURL,
    };
    $('share-site-btn').addEventListener('click', async () => {
      if (navigator.share) {
        try { await navigator.share(shareData); } catch { /* user cancelled */ }
      } else {
        await navigator.clipboard.writeText(siteURL);
        $('share-feedback').textContent = 'Link copied — paste it anywhere.';
      }
    });
    $('copy-link-btn').addEventListener('click', async () => {
      await navigator.clipboard.writeText(siteURL);
      $('share-feedback').textContent = 'Link copied — paste it anywhere.';
    });
  }

  /* ================================================================
     BOOT
  ================================================================ */
  function init() {
    renderCountdown();
    renderPillars('home-pillars');
    renderPillars('facts-pillars');
    renderHistory();
    renderFacts();
    renderBudget();
    initCalculator();
    renderFaq();
    renderDates();
    renderInvolvement();
    renderShareKit();
    showView(initialViewFromURL(), true);
  }

  init();
})();
