#!/usr/bin/env python3
"""Election-night reader for Colorado counties on Clarity results.

    python3 tools/campaign/election_watch.py --county Arapahoe --election 127409 \
        --contest 79 --received 269853 --benchmark 53643 274761

Prints the current count, what each upload added, and how much of your measure
is probably left. Colorado's public numbers need three cautions, all learned the
hard way on election night 2026:

1. "77 of 77 precincts" does not mean done in a mail-ballot state.
2. The feed's final-upload setting does not mean done either. It was on for
   counties that still had tens of thousands of ballots to count.
3. Ballots received are published by COUNTY, not by district. If your measure
   covers part of a county, the county gap is not your gap. Use --benchmark:
   a past measure's votes in your district, then that year's county ballots.

--received comes from your county's row in the Secretary of State's daily
"Ballots Returned" spreadsheet. --contest is the number at the end of the
results page URL (.../#/detail/79).
"""
import argparse, gzip, json, urllib.request

UA = {"User-Agent": "Mozilla/5.0"}
BASE = "https://results.enr.clarityelections.com/CO"
REJECTED = 0.0109  # Arapahoe's mail-ballot rejection rate in 2022


def get(url):
    raw = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40).read()
    return gzip.decompress(raw) if raw[:2] == b"\x1f\x8b" else raw


def snapshot(root, version, contest):
    rows = json.loads(get(f"{root}/{version}/json/en/summary.json"))
    settings = json.loads(get(f"{root}/{version}/json/en/electionsettings.json"))
    row = next(r for r in rows if r["K"] == str(contest))
    return {"when": settings["websiteupdatedat"], "yes": row["V"][0], "no": row["V"][1],
            "name": row["C"], "cast": int(settings["settings"]["electiondetails"].get("ballotscast") or 0)}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--county", required=True)
    p.add_argument("--election", required=True)
    p.add_argument("--contest", required=True)
    p.add_argument("--received", type=int)
    p.add_argument("--benchmark", type=int, nargs=2, metavar=("PAST_VOTES", "PAST_COUNTY_BALLOTS"))
    a = p.parse_args()
    root = f"{BASE}/{a.county}/{a.election}"
    current = get(f"{root}/current_ver.txt").decode().strip()
    versions = json.loads(get(f"{root}/{current}/json/en/electionsettings.json"))["versions"]

    print("Uploads:")
    prev = None
    for v in versions:
        try:
            s = snapshot(root, v, a.contest)
        except Exception:
            continue
        total = s["yes"] + s["no"]
        if not total:
            continue
        line = f"  {s['when']:<28} yes {s['yes']:>7,}  no {s['no']:>7,}  {100 * s['yes'] / total:5.2f}%  county {s['cast']:>8,}"
        if prev:
            added = total - prev["yes"] - prev["no"]
            if added:
                line += f"  batch +{added:,} at {100 * (s['yes'] - prev['yes']) / added:.1f}% yes"
        print(line)
        prev = s

    yes, no, lead = prev["yes"], prev["no"], prev["yes"] - prev["no"]
    print(f"\n{prev['name']}\nLead: {lead:,}")
    if a.received and prev["cast"]:
        print(f"County ballots counted: {prev['cast']:,} of {a.received:,} received ({100 * prev['cast'] / a.received:.1f}%)")
    if a.received and a.benchmark:
        expected = a.benchmark[0] / a.benchmark[1] * a.received * (1 - REJECTED)
        left = max(expected - yes - no, 0)
        print(f"Estimated final votes on this measure: {expected:,.0f}. About {left:,.0f} left. This is an estimate.")
        if left > abs(lead):
            print(f"The trailing side needs {100 * (left + abs(lead)) / 2 / left:.1f}% of what remains.")
        else:
            print("Fewer votes remain than the lead, if this estimate holds.")


if __name__ == "__main__":
    main()
