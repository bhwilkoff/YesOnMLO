/**
 * Campaign facts data plane (Decision 054).
 *
 * Every number rendered anywhere in the app lives HERE, and every
 * entry traces to a sourced row in docs/campaign/CAMPAIGN-BRIEF.md.
 * Facts not yet officially published carry `verified: false` and the
 * UI must label them as estimates. To change a fact: update
 * CAMPAIGN-BRIEF.md with the source first, then this file.
 */
const CAMPAIGN = {
  committee: 'Citizens for LPS',
  committeeLegalName: 'Citizens for Littleton Public Schools',
  registeredAgent: 'Lucie Stanish',
  coChairs: ['Amy Clark', 'Briana McCrumb'],
  mailingAddress: 'P.O. Box 2231, Littleton, CO 80161',
  committeeEmail: 'citizens4lps@gmail.com',
  // The committee's official public website — every share ultimately
  // routes voters there (one canonical home; see SOCIAL-MEDIA-PLAYBOOK).
  canonicalSite: 'https://citizensforlps.org',
  siteName: 'Yes for LPS',
  // Ballot measure letter is assigned at county certification.
  // Until then render the descriptive name, never a guessed letter.
  measureName: { value: 'the LPS Mill Levy Override', verified: false,
    note: 'Ballot letter pending county certification' },
  tagline: { value: 'Local Funding for LPS Kids', verified: false,
    note: 'Steering committee finalizing tagline' },

  measure: {
    amount: 10000000,
    kind: 'mill levy override',
    district: 'Littleton Public Schools',
    deficit: 10600000,
    boardApproved: '2026-08-13',
    boardVote: '5–0 unanimous',
    source: 'LPS press release, 2026-08-14; citizensforlps.org news, 2026-08-19',
  },

  pillars: [
    {
      title: 'Attract and keep outstanding teachers',
      detail: 'Lifts the temporary wage freeze and restores step advancements so LPS can recruit and keep top-tier educators.',
    },
    {
      title: 'Sustain academic excellence and career readiness',
      detail: 'Protects classroom funding, keeps student-to-teacher ratios intact, and preserves career-readiness programs.',
    },
    {
      title: 'Keep schools safe and fully open',
      detail: 'Supports safety, wellness, and operations — and prevents future furlough days, preserving instructional days for students.',
    },
  ],

  // Why the district is short: the 2026–27 budget was balanced with
  // one-time measures that are not sustainable.
  deficitDrivers: [
    'State-level revenue constraints',
    "Ongoing shifts in Colorado's school funding formula",
    'Declining enrollment',
    'Rising operational costs',
  ],
  oneTimeMeasures: [
    { label: 'Staffing reductions', amount: 1100000 },
    { label: 'General fund cuts', amount: 5400000 },
    { label: 'Employee wage freeze', amount: null },
    { label: 'Districtwide furlough day', amount: null },
  ],

  // 2026–27 general fund breakdown, from the campaign's budget
  // analysis (citizensforlps.org/how_does_lps_spend_money and
  // /how_much_of_the_budget_goes_to_the_central_office).
  budget: {
    expenditures: [
      { label: 'Salaries', pct: 58.5 },
      { label: 'Benefits', pct: 21.1 },
      { label: 'Purchased services', pct: 7.4 },
      { label: 'Charter schools', pct: 6.0 },
      { label: 'Transfers', pct: 3.5 },
      { label: 'Supplies', pct: 3.1 },
      { label: 'Capital / other', pct: 0.4 },
    ],
    revenue: [
      { label: 'State funding', pct: 39.4 },
      { label: 'Property taxes', pct: 39.0 },
      { label: 'Existing mill levy override', pct: 15.1 },
      { label: 'Specific ownership taxes', pct: 3.9 },
      { label: 'Other local / interest / transfers', pct: 2.4 },
      { label: 'Federal funding', pct: 0.2 },
    ],
    centralAdminPct: 'less than 2%',
    gfoaYears: 32,
    fteByYear: [
      { year: '2022–23', fte: 1493.1 },
      { year: '2023–24', fte: 1527.6 },
      { year: '2024–25', fte: 1579.1 },
      { year: '2025–26', fte: 1511.2 },
      { year: '2026–27', fte: 1422.6 },
    ],
  },

  // LPS voters have said yes to every recent funding measure.
  history: [
    { year: 2010, kind: 'Mill Levy Override', amount: '$12M', yesPct: 57.52, totalVotes: 43841 },
    { year: 2013, kind: 'Bond', amount: '$80M', yesPct: 60.34, totalVotes: 33213 },
    { year: 2018, kind: 'Bond', amount: '$298.9M', yesPct: 56.83, totalVotes: 53643 },
    { year: 2020, kind: 'Mill Levy Override', amount: '6→11 mills', yesPct: 57.66, totalVotes: 62581 },
  ],

  election: {
    day: { value: '2026-11-03', verified: true },
    ballotsMailed: { value: '2026-10-12', verified: false,
      note: 'Colorado mails ballots 18–22 days before Election Day; exact date pending county calendar' },
    ballotsDueTime: '7:00 p.m. on Election Day',
  },

  /*
   * Tax-impact model. The district has committed to publishing the
   * official estimated tax impact "in the coming weeks" (press
   * release, 2026-08-14). Until those figures arrive, every value
   * below is an ESTIMATE and the calculator labels it as such.
   *
   *   annual $ = home value × assessment rate × (mills / 1000)
   */
  taxCalc: {
    // 2026 residential assessment rate for SCHOOL levies under
    // SB24-233/HB24B-1001 is 7.05% (may adjust to 6.95%) — verify at
    // dpt.colorado.gov/residential-school-assessment-rate before
    // flipping verified:true. Never mix in the non-school 6.8% rate.
    residentialAssessmentRate: { value: 0.0705, verified: false,
      note: '2026 school-levy residential assessment rate per SB24-233; confirm 7.05% vs 6.95% with the Division of Property Taxation' },
    // ~$25/yr per $100K of home value is the district's published
    // estimate (Littleton Independent) → ≈3.5 mills at 7.05%. MLOs are
    // typically fixed-dollar with a floating mill rate — confirm
    // against certified ballot language.
    estimatedMills: { value: 3.5, verified: false,
      note: "Implied by the district's ~$25/yr per $100K estimate; confirm from certified ballot language" },
    perHundredK: { value: 25, verified: false,
      note: 'District estimate reported by the Littleton Independent' },
    defaultHomeValue: 650000,
  },

  faq: [
    {
      q: 'What is a mill levy override, in plain English?',
      a: 'Colorado sets a base level of funding for every school district. A mill levy override (MLO) is the one tool state law gives a local community to add its own property-tax dollars ON TOP of that base — and unlike state funding, every MLO dollar is collected locally, stays in this district, and cannot be taken back by the state. It is not a loan and carries no debt or interest: it is direct, ongoing operating money for classrooms.',
    },
    {
      q: 'How is this different from a bond?',
      a: 'Bonds borrow money for buildings — construction, roofs, security doors — and are paid back over decades. An MLO pays for people and programs: teacher salaries, class sizes, counselors, electives. Buildings cannot teach; the MLO is about who is in the classroom.',
    },
    {
      q: 'Why does LPS need this now?',
      a: 'The district faces a $10.6 million ongoing budget gap driven by state funding constraints, changes in the state funding formula, declining enrollment, and rising costs. The 2026–27 budget was balanced with one-time measures — $1.1M in staffing cuts, $5.4M in general-fund cuts, a wage freeze for every employee, and an unpaid furlough day. Those close the gap once; they do not close it next year.',
    },
    {
      q: "Hasn't LPS been cutting costs already?",
      a: 'Yes — before asking voters for anything, the district cut roughly $6.5 million through staffing reductions, restructuring, and general-fund cuts, froze wages, and scheduled a furlough day. The MLO is the step the community takes only after the district has done its part.',
    },
    {
      q: 'How much of the budget goes to administration?',
      a: 'Less than 2% of the LPS operating budget goes to central administration — and when cuts came, central office staffing and department budgets were reduced first to shield classrooms. About 85% of general-fund spending is salaries and benefits for the people who work with students. LPS has also earned the Government Finance Officers Association’s excellence-in-financial-reporting award for 32 consecutive years.',
    },
    {
      q: 'What happens if it passes?',
      a: "Educator compensation is restored retroactively to the start of the contract year, the spring furlough day comes off the calendar (students get that instructional day back), class-size ratios hold, and career-readiness programs continue. LPS stays competitive with neighboring districts for the best teachers.",
    },
    {
      q: 'What happens if it fails?',
      a: 'The one-time cuts become permanent and deepen. The wage freeze and furlough days continue, which in practice means losing teachers to neighboring districts that pay more — and deeper cuts to programs in the years that follow.',
    },
    {
      q: 'Where does the money go — can it be diverted?',
      a: 'MLO dollars are local by law. They are collected by the county, go directly to Littleton Public Schools, and cannot be redirected by the state legislature or spent outside the district. The ballot language itself defines what the funds support.',
    },
    {
      q: 'How much will it cost me?',
      a: 'The district will publish official tax-impact figures for homeowners. Until then, use our calculator to see how the math works — home value × assessment rate × mills — with clearly-labeled estimates you can adjust yourself.',
    },
    {
      q: "Doesn't declining enrollment mean the district needs LESS money?",
      a: "Costs don't fall one student at a time — a class of 24 costs the same to teach as a class of 27, and buildings, buses, and safety staff serve everyone. Meanwhile Colorado funds districts per student, so declining enrollment cuts revenue faster than it cuts costs. The district is pairing this measure with long-range right-sizing planning; the MLO keeps classrooms whole while that work happens.",
    },
    {
      q: "I'm a senior on a fixed income. What does this really mean for me?",
      a: "Two Colorado programs soften the impact. The senior homestead exemption (65+, in your home 10+ years) exempts 50% of the first $200,000 of your home's value — so your actual increase is smaller than the headline number. Colorado also offers a property-tax deferral program for seniors. And there's a return on the investment: the strongest research on school funding measures finds passage lifts nearby home values by about 6% over the following decade — strong schools are a big part of why Littleton-area homes hold their value.",
    },
    {
      q: "Prop NN is also on my ballot. Isn't the state already handling school funding?",
      a: "They're separate questions. Prop NN is a statewide measure about state money — and none of it is guaranteed to reach LPS. The mill levy override is the only measure on your ballot where every dollar is collected locally, stays in LPS schools by law, and is controlled by a school board you elect. However you vote on NN, it doesn't close the LPS gap.",
    },
    {
      q: 'Who can vote on this?',
      a: 'Every registered voter living within Littleton Public Schools boundaries — which include Littleton AND parts of Centennial and unincorporated Arapahoe County. You do not need to be a parent. Colorado mails every registered voter a ballot in mid-October.',
    },
  ],

  // Mirrors the real volunteer options at citizensforlps.org/volunteer.
  involvement: [
    { level: 'Two minutes', actions: [
      'Share the campaign with your friends, family, and community',
      'Tell one neighbor why you’re voting yes',
    ]},
    { level: 'An hour', actions: [
      'Take a yard sign',
      'Fill out postcards to voters',
      'Write a letter to the editor of a local paper',
      'Write a personal post about what LPS means to your family',
    ]},
    { level: 'Ongoing', actions: [
      'Join a literature-drop walk',
      'Paint your car windows for the campaign',
      'Attend events and share information with talking points',
      'Help with ballot-return reminders in the final two weeks',
    ]},
  ],

  // Campaign calendar from citizensforlps.org/upcoming_events
  // (RSVP links live there). Keep in sync when new events post.
  events: [
    { when: 'Sat Aug 29, 10:00 AM', what: 'Letters to the Editors' },
    { when: 'Sat Sep 12, 10:00 AM', what: 'Distribute postcards' },
    { when: 'Sat Sep 12, 10:00 AM', what: 'Yard sign distribution begins' },
    { when: 'Mon Sep 21, 6:00 PM', what: 'Car painting begins' },
    { when: 'Sat Sep 26, 10:00 AM', what: 'Start mailing postcards' },
    { when: 'Sat Oct 3, 9:00 AM', what: 'Lit Drop Walk' },
    { when: 'Sun Oct 4, 10:00 AM', what: 'Lit Drop Walk' },
    { when: 'Mon Oct 5, 4:00 PM', what: 'Deadline to mail postcards' },
    { when: 'Sat Oct 10, 9:00 AM', what: 'Lit Drop Walk' },
    { when: 'Sun Oct 11, 9:00 AM', what: 'Lit Drop Walk' },
  ],
};
