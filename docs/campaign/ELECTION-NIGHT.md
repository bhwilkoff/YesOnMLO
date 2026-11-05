# Reading election night in Colorado

Colorado votes by mail, and that makes results easy to misread. We got several
things wrong while watching our own count, and each one taught us something.
This is what we'd want to know going in.

## How the count really moves

1. Counties can start processing ballots about two weeks early. So the first
   results, right after 7 p.m., are a big block of early ballots. In Arapahoe
   County in 2026 that first drop was 187,231 ballots, about 69% of the eventual
   total received.
2. Then it slows way down. Late ballots still need signatures checked, and they
   come in by the truckload. Statewide, **40% of all ballots arrived in the final
   two days** of 2026 (1,599,988 by Nov 1, then 2,671,424 by Election Day).
3. Big counties take days. Small ones finish overnight. That's normal.
4. Voters can fix signature and ID problems for about eight days afterward, and
   military and overseas ballots can arrive through then, so a small number of
   votes can still move late.

## Three numbers that fool you

**"77 of 77 precincts reporting."** It doesn't mean finished. In a mail-ballot
state, a precinct can report with most of its ballots still in a tray.

**The results feed's "final upload" setting.** We saw it flip on and thought it
might mean done. But it was on for Denver, Boulder and Jefferson too, with
tens of thousands of ballots still to count. Ignore it.

**The county's uncounted ballots.** This is the one we got wrong the longest.
The state publishes ballots received by county, not by school district. Most of
Arapahoe County can't vote on an LPS measure, so the county's 64,000-ballot gap
was never our gap. Our Social Media lead caught this.

## The better way

Compare what's counted with what was received, then scale that to your district.

1. **Ballots received:** the Secretary of State's daily "Ballots Returned" news
   release links a spreadsheet with a row for each county.
2. **Ballots counted:** your county's results page, or the `ballotscast` value in
   its feed. Many counties don't publish that. For those, use the total votes for
   Governor, since nearly everyone votes that race. Counties that are nearly done
   sit around 96 to 97% of received.
3. **Your district's share:** find a past measure in your district from a similar
   election, and divide its votes by that year's county ballots. Midterm to
   midterm is best. Ours: 53,643 votes on the 2018 bond, out of 274,761 county
   ballots, is 19.5%. County canvass reports have these numbers and are public.
4. **Votes left:** your share, times ballots received, less about 1% for
   rejections, minus votes counted so far.
5. **What the other side needs:** (votes left + the lead) / 2, as a share of
   votes left.

`tools/campaign/election_watch.py` does all of that:

```sh
python3 tools/campaign/election_watch.py --county Arapahoe --election 127409 \
  --contest 79 --received 269853 --benchmark 53643 274761
```

It also lists each upload and how that batch broke. The contest number is the
end of the results page URL. The Secretary of State's results feed lists every
county's election ID, which is how you can scan every school measure in the state.

## Be careful with your comparisons

Comparing vote totals across years only works if the race is similar. House
districts looked like a good benchmark for us until we checked: two were
uncontested in 2026, and one had no Republican, so their totals were much lower
for reasons that had nothing to do with counting. Look at who was on the ballot
before you trust a number.

And slow growth in your area doesn't prove it's finished. It may just be waiting
behind somewhere else. The day after the election, only about 10% of new ballots
were ours, which looked like we were nearly done. In the next upload it was 24%.

## When to say you won

Wait for the district or your co-chairs. We held our "it passed" posts until the
superintendent's email said "the passage of Ballot Issue 4A," though the numbers
looked good well before that.

Until then, make posts that are true either way. We used "22,338 neighbors said
yes, and counting." Once it's called, use a number that can't go stale, like
"more than 23,000," since the count keeps moving after you post.

Results are unofficial until the county canvass board certifies them, and
remember that margins can shift a little until then.
