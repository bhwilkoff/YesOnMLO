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
  // Re-read in a browser 2026-09-02: carries the forum schedule, the
  // $600,000-home example, the March 19, 2027 furlough date, the cut
  // breakdown, and "32 consecutive years" for GFOA.
  lpsDollarsAndSense: {
    label: 'LPS "Dollars and Sense" budget page (read Sept 2, 2026)',
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
  // LPS's own budget page now says 32 (read 2026-09-02) — the district
  // is the source for its own award count, so 32 is the figure we use.
  lpsGfoa32: {
    label: 'LPS "Dollars and Sense": GFOA award, 32 consecutive years',
    url: 'https://www.littletonpublicschools.net/page/dollars-and-sense/',
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
      text: 'On August 13, 2026, the LPS Board of Education voted to place a $10 million mill levy override on the November ballot. The vote was 5–0. The district faces a $10.6 million budget gap and balanced this year with one-time measures: central-office staffing cuts, operating-budget reductions and restructuring, a wage freeze, and an unpaid furlough day on March 19, 2027.',
      sourceId: 'lpsDollarsAndSense',
    },
    {
      text: 'If voters say yes, the district has said the ongoing funding goes to keeping teacher pay competitive (a 2% average raise), cancelling the furlough day, targeted math and reading staffing, career-readiness programs, and student safety and mental-health staff. The district says 100% of the money stays local. It estimates the cost at about $25 a year per $100,000 of home value. Its example is a $600,000 home at less than $13 a month.',
      sourceId: 'lpsDollarsAndSense',
    },
    {
      text: 'A mill levy override is additional local property-tax funding a Colorado community can approve for its own school district. It is collected here and controlled by the school board we elect.',
      sourceId: 'crsMlo',
    },
  ],

  /*
   * Facts a volunteer can drop into a post. Each has display text,
   * a ready-to-paste share version, and a source.
   */
  facts: [
    {
      text: 'Before asking voters for anything, LPS closed a $10.6 million gap: $1.1 million cut from central-office staffing, $2.8 million from operating budgets and restructuring, $5.4 million shifted in the general fund, a wage freeze, and an unpaid furlough day on March 19, 2027.',
      share: 'Before asking voters for anything, LPS closed a $10.6 million gap. $1.1 million cut from the central office. $2.8 million from operating budgets. A wage freeze for every employee. An unpaid furlough day. The mill levy override comes after the district did its part.',
      sourceId: 'lpsDollarsAndSense',
    },
    {
      text: 'The district’s own estimate of the cost: about $25 a year for every $100,000 of home value. Its example: a $600,000 home pays less than $13 a month.',
      share: 'The district’s own estimate for the LPS mill levy override is about $25 a year per $100,000 of home value. Their example is a $600,000 home at less than $13 a month.',
      sourceId: 'lpsDollarsAndSense',
    },
    {
      text: 'The district has said what a yes vote buys: $2.5 million for a 2% average raise so LPS can keep teachers from leaving for neighboring districts, and $800,000 to cancel the March 19, 2027 furlough day and give students that school day back.',
      share: 'What a yes vote on the LPS mill levy override buys, according to the district: a 2% average raise so our teachers stop leaving for districts that pay more, and the furlough day cancelled. Kids get March 19 back as a school day.',
      sourceId: 'lpsDollarsAndSense',
    },
    {
      text: 'If it fails, the district says the wage freeze stays, more furlough days are possible, and career-readiness programs could be capped. If it passes, 100% of the money stays in LPS schools.',
      share: 'The district has been plain about it. If the mill levy override fails, the wage freeze stays and more furlough days are possible. If it passes, every dollar stays in LPS schools.',
      sourceId: 'lpsDollarsAndSense',
    },
    {
      text: 'The Board of Education’s vote to put this on the ballot was unanimous, 5–0.',
      share: 'The LPS Board of Education voted 5–0 to put the mill levy override in front of voters this November.',
      sourceId: 'cflpsHome',
    },
    {
      text: 'Less than 2% of the LPS operating budget goes to central administration. About 85% of general-fund spending is salaries and benefits for the people who work with students.',
      share: 'Less than 2% of the LPS budget goes to central administration. About 85% is pay and benefits for the people who work with our kids.',
      sourceId: 'cflpsAdmin',
    },
    {
      text: 'LPS has earned the Government Finance Officers Association’s excellence-in-financial-reporting award for 32 consecutive years.',
      share: 'LPS has earned the national award for excellence in financial reporting 32 years in a row. This is a district that takes care of the money we give it.',
      sourceId: 'lpsGfoa32',
    },
    {
      text: 'LPS voters have approved every recent funding measure: the 2010 override (57.5% yes), 2013 bond (60.3%), 2018 bond (56.8%), and 2020 override (57.7%), per Arapahoe County official results.',
      share: 'LPS voters have said yes to every recent school funding measure. 2010, 2013, 2018, 2020. Every one passed with at least 56% (Arapahoe County official results).',
      sourceId: 'arapahoeResults',
    },
    {
      text: 'A mill levy override is additional local funding under Colorado law. It is collected here and controlled by the school board we elect.',
      share: 'The LPS mill levy override is local money under Colorado law. Collected here, spent on our schools, controlled by the school board we elect.',
      sourceId: 'crsMlo',
    },
    {
      text: 'Arapahoe County mails ballots to every active registered voter starting October 2, 2026. Ballots must be received, not postmarked, by 7:00 p.m. on November 3.',
      share: 'Ballots start arriving in Arapahoe County mailboxes October 2. No polling place needed. Find the LPS mill levy override on yours and get it back by 7 p.m. November 3. Received, not postmarked.',
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
        { text: 'A furlough day sounds small until it’s your family’s Friday. Here’s what March 19 looks like for us…',
          hint: 'The district’s furlough day is Friday, March 19, 2027. The logistics are the story. Childcare, missed work, a kid home for no good reason.' },
        { text: 'I asked my kid their favorite class this week. Here’s what they said, and who teaches it.',
          hint: 'Ask permission before naming your kid or the teacher.' },
        { text: 'Here’s something my kid’s teacher did this week that isn’t in any job description…',
          hint: 'The note home, the lunch-duty pep talk, the 9 p.m. email. One extra thing.' },
        { text: 'I used to think “class size” was a statistic. Then I watched what ___ does with ___ kids in one room…',
          hint: 'Name the teacher (with permission) and the number. The reader does the math.' },
        { text: 'The bus driver, the crossing guard, the counselor, the coach. Here are the people who got my kid through last year…',
          hint: 'Every one of them is on the wage freeze this year. Name the ones you can.' },
        { text: 'The thing I’d tell a family that just moved into the district…',
          hint: 'What you wish someone had told you. End with why you’re voting yes.' },
      ],
    },
    {
      voice: 'If you teach or work in the schools',
      prompts: [
        { text: 'I’ve taught here ___ years. Here’s what kept me, and what a wage freeze says to people like me…',
          hint: 'Post on your own time, from your own account, as yourself. Never from work.' },
        { text: 'Here’s one thing in my classroom that families never see…',
          hint: 'The small, concrete detail beats the big claim.' },
        { text: 'The supply I bought with my own money this fall was…',
          hint: 'One item, one price. Not a complaint. Just the fact.' },
        { text: 'Here’s what a 2% raise actually means in my house…',
          hint: 'The district says $2.5 million of the override goes to a 2% average raise. Put one real thing next to it: a car repair, a month of groceries.' },
        { text: 'The student I’m still thinking about from last year is…',
          hint: 'No names, ever. The kind of kid, the turn they took, and what a steady staff made possible.' },
        { text: 'People ask why I haven’t left for a district that pays more. Here’s my honest answer…',
          hint: 'Be honest about the pull. End on what keeps you, and what would make staying possible.' },
      ],
    },
    {
      voice: 'If you graduated from these schools',
      prompts: [
        { text: 'I graduated from ___ in ___. Here’s the teacher I still think about…',
          hint: 'Alumni voices reach people no campaign can.' },
        { text: 'My kids go to the same school I did. Here’s what’s the same, and what’s at stake…',
          hint: 'Two generations in one building is the whole district in one story.' },
        { text: 'The thing I learned at ___ that I still use every week is…',
          hint: 'A skill, a habit, a sentence a teacher said once.' },
        { text: 'I was the kid who needed ___. Here’s who noticed…',
          hint: 'The counselor, the coach, the librarian, the para. The person, not the program.' },
        { text: 'I went back to ___ recently. Here’s what’s changed, and what hasn’t…',
          hint: 'The building, the trophy case, the teacher who’s somehow still there.' },
        { text: 'Class of ___. If you were there with me, you remember Ms. ___, and you probably still live nearby…',
          hint: 'Tag your classmates. Alumni reach alumni, and a lot of them vote here.' },
      ],
    },
    {
      voice: 'If your kids are grown, or you never had kids here',
      prompts: [
        { text: 'Our kids finished at LPS years ago. I’m still voting yes, because…',
          hint: 'Longtime neighbors persuade longtime neighbors.' },
        { text: 'We moved here because of the schools. ___ years later, here’s what that choice has been worth…',
          hint: 'Strong schools and strong neighborhoods are the same story.' },
        { text: 'I don’t have kids in these schools. Here’s why I’m voting yes anyway…',
          hint: 'The neighbor kid who shovels your walk. The teenager who bags your groceries. Who you’re voting for.' },
        { text: 'My grandkid’s teacher at ___…',
          hint: 'Grandparents are on Facebook. Write it for the friends who are too.' },
        { text: 'Every house for sale on our block lists the schools first. Here’s what that tells me…',
          hint: 'The realtors already know. Say it plainly.' },
        { text: 'I’ve lived here ___ years and voted yes on every school measure: 2010, 2013, 2018, 2020. Here’s why this one is no different…',
          hint: 'LPS voters approved all four (Arapahoe County official results). If you were here for them, say what they built.' },
      ],
    },
    {
      voice: 'If you run a local business',
      prompts: [
        { text: 'I hire in this community. Here’s what LPS graduates bring through my door…',
          hint: 'The workforce story, told from the counter, not a podium.' },
        { text: 'The LPS student who works for me after school…',
          hint: 'Ask them first. What they bring, what they’re learning, why it matters that their school is steady.' },
        { text: 'When a family decides whether to move here, the first thing they ask about is the schools. Here’s what that means for a business like mine…',
          hint: 'Customers, hires, the block. Schools are why people choose a town.' },
        { text: 'March 19 is a furlough day. Here’s what one closed school day does to a small business with parents on staff…',
          hint: 'The district’s furlough day is Friday, March 19, 2027. Coverage, call-outs, the parent who has to choose.' },
        { text: 'I signed up to take a yard sign for the shop. Here’s why…',
          hint: 'Yard signs go out starting September 12. The sign-up is the volunteer form at citizensforlps.org.' },
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
    // The district's own worked example ("a $600,000 home would equal
    // less than $13 per month") — the calculator opens on it so a
    // reader can check the district's arithmetic before their own.
    districtExample: { homeValue: 600000, monthlyText: 'less than $13 a month', verified: true,
      sourceId: 'lpsDollarsAndSense' },
    defaultHomeValue: 600000,
  },

  /*
   * The district's Dollars and Sense community forums — Superintendent
   * Todd Lambert presenting the budget and the measure, then Q&A. These
   * are district-track informational meetings (not campaign events):
   * our tool's job is to help a supporter bring a neighbor. No
   * registration; Spanish interpretation at every session.
   * Dates are ISO local; times as the district prints them.
   */
  forums: {
    sourceId: 'lpsDollarsAndSense',
    host: 'Superintendent Todd Lambert',
    sessions: [
      { date: '2026-09-14', time: '5:00–6:00 p.m.', place: 'Newton Middle School' },
      { date: '2026-09-15', time: '6:00–7:00 p.m.', place: 'Goddard Middle School' },
      { date: '2026-09-23', time: '6:00–7:00 p.m.', place: 'Powell Middle School' },
      { date: '2026-09-28', time: '5:30–6:30 p.m.', place: 'Heritage High School' },
      { date: '2026-09-29', time: '5:00–6:00 p.m.', place: 'Littleton High School' },
      { date: '2026-09-30', time: '5:30–6:30 p.m.', place: 'Arapahoe High School' },
      { date: '2026-10-01', time: '6:00–7:00 p.m.', place: 'Euclid Middle School' },
    ],
  },

  /*
   * Names the story checklist recognizes as "a real place" — every LPS
   * school plus the two cities the district serves. Teaching aid only:
   * it nudges a writer toward the specific, it never blocks a post.
   */
  placeNames: [
    'Arapahoe', 'Heritage', 'Littleton High', 'Options', 'Newton', 'Goddard',
    'Powell', 'Euclid', 'Field', 'Hopkins', 'Wilder', 'Runyon', 'Sandburg',
    'Lenski', 'Franklin', 'Highland', 'Moody', 'East Elementary', 'Peabody',
    'Twain', 'Centennial Academy', 'Littleton Academy', 'Littleton Prep',
    'Village at North', 'Village at Highland', 'Littleton', 'Centennial',
    'Elementary', 'Middle School', 'High School',
  ],

  /*
   * The playbook digest — how the team shows up on each network.
   * Deliberately no X/Twitter. Full strategy:
   * docs/campaign/SOCIAL-MEDIA-PLAYBOOK.md
   */
  playbook: [
    {
      name: 'Facebook',
      role: 'where the votes are',
      how: 'Local groups matter more than pages. Post your story in the neighborhood and school groups you already belong to, as yourself. Comment early and kindly on other supporters’ posts. The first hour decides how far a post goes. Events and live video reach grandparents.',
    },
    {
      name: 'Instagram',
      role: 'parents & younger voters',
      how: 'Stories with the link sticker. Reels under a minute, captions on. Use your own photo or the card from the studio. Start an “Add Yours” sticker: the LPS teacher I still think about.',
    },
    {
      name: 'Nextdoor',
      role: 'neighbors and seniors. Careful here',
      how: 'Nextdoor allows civil discussion of a local ballot measure in the main feed and does not allow over-posting about it. So one post per phase, as a resident. Why you are voting yes. Answer questions kindly. Link to citizensforlps.org. Step back. Nobody argues in a Nextdoor thread. Repeats break the guidelines and cost goodwill.',
    },
    {
      name: 'LinkedIn',
      role: 'colleagues & local professionals',
      how: 'A different register. Schools are the reason families and employers pick a town. One post about what LPS meant for your family or your hiring reaches neighbors who never see campaign content anywhere else.',
    },
    {
      name: 'Texts & DMs',
      role: 'the channel that matters most',
      how: 'A message from someone who knows you beats everything else we can do, and it is not close. Five people who live in the district. One note each, in your words. The studio drafts it with you. You send it.',
    },
    {
      name: 'Threads & Bluesky',
      role: 'if you’re already there',
      how: 'Small local reach and almost no effort. The studio posts your story there in one tap. Don’t build a presence for this.',
    },
  ],
};
