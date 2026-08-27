/**
 * Campaign facts data plane (Decisions 054, 058).
 *
 * RULES:
 *  - Every fact carries a sourceId resolving to a real, checkable URL
 *    in SOURCES. A fact without a source doesn't ship.
 *  - verified:false means the figure awaits official confirmation and
 *    the UI must label it as an estimate.
 *  - To change a fact: update docs/campaign/CAMPAIGN-BRIEF.md with the
 *    source first, then this file, in the same commit.
 */

/*
 * Every URL below was fetched and confirmed live on 2026-08-26 —
 * see docs/research/fact-check-2026-08-26.md for the full audit with
 * quotes. Do not add a source you haven't loaded in a browser.
 */
const SOURCES = {
  lpsPressRelease: {
    label: 'LPS: "Board Approves $10M Mill Levy Override Measure" (Aug 14, 2026)',
    url: 'https://www.littletonpublicschools.net/article/3075947',
  },
  lpsDeficitLetter: {
    label: 'LPS Superintendent\'s budget letter (May 29, 2026)',
    url: 'https://www.littletonpublicschools.net/article/2950007',
  },
  lpsDollarsAndSense: {
    label: 'LPS "Dollars and Sense" budget pages',
    url: 'https://www.littletonpublicschools.net/page/dollars-and-sense/',
  },
  cflpsHome: {
    label: 'Citizens for LPS (Aug 19, 2026 news)',
    url: 'https://citizensforlps.org/',
  },
  cflpsAdmin: {
    label: 'Citizens for LPS: central office budget share',
    url: 'https://citizensforlps.nationbuilder.com/how_much_of_the_budget_goes_to_the_central_office',
  },
  lpsGfoa: {
    label: 'LPS: GFOA excellence award, 31st consecutive year (June 2025)',
    url: 'http://web.archive.org/web/20250615045746/https://littletonpublicschools.net/district/nr/lps-finance-wins-excellence-award-31st-consecutive-year',
  },
  littletonIndependent: {
    label: 'Littleton Independent, Aug 3, 2026',
    url: 'https://www.littletonindependent.net/news/article_a094d1b7-6ef1-4cf3-81d9-66f09420745d.html',
  },
  arapahoeResults: {
    label: 'Arapahoe County official election results archive',
    url: 'https://www.arapahoeco.gov/your_county/arapahoevotes/records_data/past_elections_file_library.php',
  },
  arapahoeVotes: {
    label: 'Arapahoe County Elections',
    url: 'https://www.arapahoeco.gov/your_county/arapahoevotes/index.php',
  },
  crsMlo: {
    label: 'Colorado mill levy override law, CRS 22-54-108',
    url: 'https://law.justia.com/codes/colorado/title-22/article-54/section-22-54-108/',
  },
  dptRate: {
    label: 'Colorado Division of Property Taxation: 2026 residential school assessment rate',
    url: 'https://dpt.colorado.gov/residential-school-assessment-rate',
  },
  coSosCalendar: {
    label: 'Colorado Secretary of State 2026 election calendar',
    url: 'https://www.coloradosos.gov/pubs/elections/calendars/2026ElectionCalendar.pdf',
  },
  goVoteColorado: {
    label: 'GoVoteColorado (Colorado SOS voter portal)',
    url: 'https://www.govotecolorado.gov',
  },
};

const CAMPAIGN = {
  officialSite: 'https://citizensforlps.org',
  toolkitUrl: 'https://bhwilkoff.github.io/YesOnMLO/',

  /*
   * What's on the ballot — the short, sourced version for the home
   * page. Plain sentences, each with the source it came from.
   */
  ballotSummary: [
    {
      text: 'On August 13, 2026, the LPS Board of Education voted to place a $10 million mill levy override on the November ballot — a 5–0 vote. The district faces a $10.6 million budget gap and balanced this year with one-time measures: staffing reductions, operating-budget cuts, a wage freeze, and an unpaid furlough day.',
      sourceId: 'lpsPressRelease',
    },
    {
      text: 'If voters say yes, the district has said the ongoing funding goes to keeping teacher pay competitive, holding class-size ratios, sustaining career-readiness programs, and safety and operations — and the furlough day comes off the calendar. The district estimates the cost at about $25 a year per $100,000 of home value.',
      sourceId: 'lpsDeficitLetter',
    },
    {
      text: 'A mill levy override is additional local property-tax funding a Colorado community can approve for its own school district — collected here and controlled by the school board our community elects.',
      sourceId: 'crsMlo',
    },
  ],

  /*
   * Facts a volunteer can drop into a post. Each has display text,
   * a ready-to-paste share version, and a source.
   */
  facts: [
    {
      text: 'Before asking voters for anything, LPS closed a $10.6 million gap with central-office staffing reductions, operating-budget cuts, general-fund savings, a wage freeze, and an unpaid furlough day.',
      share: 'Before asking voters for anything, LPS closed a $10.6 million gap the hard way — staffing reductions, budget cuts, a wage freeze for employees, and an unpaid furlough day. The mill levy override is what comes after the district did its part.',
      sourceId: 'lpsDeficitLetter',
    },
    {
      text: 'The district’s own estimate of the cost: about $25 a year for every $100,000 of home value.',
      share: 'The district’s own estimate for the LPS mill levy override: about $25 a year per $100,000 of home value. For most homes here, that’s the cost of one takeout dinner a year per $100K.',
      sourceId: 'lpsDeficitLetter',
    },
    {
      text: 'The Board of Education’s vote to put this on the ballot was unanimous, 5–0.',
      share: 'The LPS Board of Education voted 5–0 — unanimous — to bring the mill levy override to voters this November.',
      sourceId: 'cflpsHome',
    },
    {
      text: 'Less than 2% of the LPS operating budget goes to central administration. About 85% of general-fund spending is salaries and benefits for the people who work with students.',
      share: 'Worth knowing: less than 2% of the LPS budget goes to central administration. About 85% is pay and benefits for the people who work with our kids.',
      sourceId: 'cflpsAdmin',
    },
    {
      text: 'LPS has earned the Government Finance Officers Association’s excellence-in-financial-reporting award for 31 consecutive years, most recently for fiscal year 2024.',
      share: 'LPS has earned the national award for excellence in financial reporting 31 years in a row. This is a district that takes care of the money we give it.',
      sourceId: 'lpsGfoa',
    },
    {
      text: 'LPS voters have approved every recent funding measure: the 2010 override (57.5% yes), 2013 bond (60.3%), 2018 bond (56.8%), and 2020 override (57.7%) — per Arapahoe County official results.',
      share: 'This community has always shown up for its schools: LPS voters approved the 2010, 2013, 2018, and 2020 school funding measures, every one with at least 56% support (Arapahoe County official results).',
      sourceId: 'arapahoeResults',
    },
    {
      text: 'A mill levy override is additional local funding under Colorado law — collected here and controlled by the school board we elect.',
      share: 'The LPS mill levy override is local money under Colorado law — collected here, spent on our schools, controlled by the school board we elect.',
      sourceId: 'crsMlo',
    },
    {
      text: 'Arapahoe County mails ballots to every active registered voter starting October 2, 2026. Ballots must be received — not postmarked — by 7:00 p.m. on November 3.',
      share: 'Ballots land in Arapahoe County mailboxes starting October 2. No polling place needed — look for the LPS mill levy override on yours, and get it back by 7 p.m. November 3 (received, not postmarked).',
      sourceId: 'arapahoeVotes',
    },
  ],

  /*
   * Story prompts, grouped by voice. Tapping one seeds the studio
   * draft. The hint is a nudge, not a script.
   */
  storyPrompts: [
    {
      voice: 'If you’re a parent',
      prompts: [
        { text: 'The moment I knew my kid’s teacher really saw them was…',
          hint: 'Name the school. One moment, told the way you’d tell it at pickup.' },
        { text: 'A furlough day sounds small until it’s your family’s Tuesday. Here’s what it looks like for us…',
          hint: 'The logistics are the story — childcare, missed work, a kid home for no good reason.' },
        { text: 'I asked my kid their favorite class this week. Here’s what they said — and who teaches it.',
          hint: 'Ask permission before naming your kid or the teacher.' },
      ],
    },
    {
      voice: 'If you teach or work in the schools',
      prompts: [
        { text: 'I’ve taught here ___ years. Here’s what kept me — and what a wage freeze says to people like me…',
          hint: 'Post on your own time, from your own account, as yourself. Never from work.' },
        { text: 'Here’s one thing in my classroom that families never see…',
          hint: 'The small, concrete detail beats the big claim.' },
      ],
    },
    {
      voice: 'If you graduated from these schools',
      prompts: [
        { text: 'I graduated from ___ in ___. Here’s the teacher I still think about…',
          hint: 'Alumni voices reach people no campaign can.' },
        { text: 'My kids go to the same school I did. Here’s what’s the same — and what’s at stake…',
          hint: 'Multi-generation stories are the heart of this district.' },
      ],
    },
    {
      voice: 'If your kids are grown — or you never had kids here',
      prompts: [
        { text: 'Our kids finished at LPS years ago. I’m still voting yes, because…',
          hint: 'Longtime neighbors persuade longtime neighbors.' },
        { text: 'We moved here because of the schools. ___ years later, here’s what that choice has been worth…',
          hint: 'Strong schools and strong neighborhoods are the same story.' },
      ],
    },
    {
      voice: 'If you run a local business',
      prompts: [
        { text: 'I hire in this community. Here’s what LPS graduates bring through my door…',
          hint: 'The workforce story, told from the counter, not a podium.' },
      ],
    },
  ],

  /*
   * Tax-impact model. Every value labeled an estimate until the
   * district publishes official figures (it has said it will).
   *   annual $ = home value x assessment rate x (mills / 1000)
   */
  taxCalc: {
    // "2026 Residential School Assessment Rate - 7.05%" — Colorado
    // Division of Property Taxation, fetched 2026-08-26.
    residentialAssessmentRate: { value: 0.0705, verified: true,
      sourceId: 'dptRate',
      note: '2026 rate; the State Board of Equalization can adjust in future years' },
    // Derived from the district's own official estimate ("approximately
    // $25 annually for every $100,000 of home value" — Superintendent's
    // letter, May 29, 2026): 25 / 7.05 ≈ 3.5 mills. The certified mill
    // figure arrives with county ballot certification (~September).
    estimatedMills: { value: 3.5, verified: false,
      sourceId: 'lpsDeficitLetter',
      note: 'Derived from the district’s $25-per-$100K estimate; certified ballot language will set the final figure' },
    perHundredK: { value: 25, verified: true, sourceId: 'lpsDeficitLetter' },
    defaultHomeValue: 650000,
  },

  /*
   * The playbook digest — how the team shows up on each network.
   * Deliberately no X/Twitter. Full strategy:
   * docs/campaign/SOCIAL-MEDIA-PLAYBOOK.md
   */
  playbook: [
    {
      name: 'Facebook',
      role: 'where the votes are',
      how: 'Local groups matter more than pages — post your story in the neighborhood and school-community groups you actually belong to, as yourself. Comment kindly and early on other supporters’ posts; the first hour decides what the algorithm does with a post. Events and lives reach grandparents.',
    },
    {
      name: 'Instagram',
      role: 'parents & younger voters',
      how: 'Stories with the link sticker, Reels under a minute with captions on. Use the share card from the studio. “Add Yours” story stickers travel: start one — “the LPS teacher I still think about.”',
    },
    {
      name: 'Nextdoor',
      role: 'neighbors & seniors — handle with care',
      how: 'Local ballot measures are allowed; campaigning on repeat is not. One genuine post per phase, as a resident: introduce why you’re voting yes, answer questions civilly, link to citizensforlps.org, and step back. Never argue in a thread. Over-posting gets removed and costs goodwill.',
    },
    {
      name: 'LinkedIn',
      role: 'colleagues & local professionals',
      how: 'A different register: schools as the reason families and employers choose a community. One thoughtful post — what LPS meant for your family or your hiring — reaches neighbors who never see campaign content anywhere else.',
    },
    {
      name: 'Texts & DMs',
      role: 'the highest-value channel we have',
      how: 'A personal message to someone who knows you beats everything else in the research — by a lot. Five people who live in the district, one honest note each, in your words. The studio’s person-to-person tools draft it with you; you send it yourself.',
    },
    {
      name: 'Threads & Bluesky',
      role: 'if you’re already there',
      how: 'Small local reach, but low effort: the studio buttons post your same story there in one tap. Don’t build a presence from scratch for this.',
    },
  ],
};
