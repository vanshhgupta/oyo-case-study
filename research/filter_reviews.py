"""Keyword filter: keep guest reviews (5+ words) that may describe something going wrong between booking and the stay.
The filter is deliberately broad; the coding step (codebook.md) removes reviews that turn out not to be relevant.
Run from the project root:  .venv/bin/python research/filter_reviews.py
"""
import csv, re
KW = re.compile(r"""check.?in|checkin|denied|deny|denie|refus|not\ allow|n'?t\ allow|didnt\ allow|no\ room|room\ not|rooms?\ (were|was|is)\ (not\ )?(full|available)|
not\ available|unavailable|sold\ out|overbook|over\ book|booking\ (is\ |was\ )?(not|n'?t)|not\ (found|received|confirmed|showing|show)|
reach(ed)?\ (the\ )?(hotel|property)|arriv|reception|front\ desk|receptionist|manager|hotel\ (staff|owner|people|guy)|
couple|unmarried|married|local\ id|id\ proof|aadha?ar|\bid\b|extra\ (money|charge|amount|payment|rs|rupees)|pay\ (more|extra|again|in\ cash|cash)|
\bcash\b|double\ (charge|payment)|prepaid|paid\ online|online\ pay|refund|cancel|closed|shut|not\ (an\ )?oyo|no\ longer|
different\ (hotel|room|property|location)|photos?|pictures?|fake|mismatch|not\ as\ (shown|per|described)|another\ hotel|other\ hotel|
shift(ed)?\ (us|me|to)|relocat|alternat|night|midnight|stranded|road|street""", re.I | re.X)

rows = list(csv.DictReader(open("research/guest_reviews_raw.csv")))
keep = [r for r in rows if len(r["text"].split()) >= 5 and KW.search(r["text"])]
with open("research/guest_reviews_filtered.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["row"] + list(rows[0].keys()))
    w.writeheader()
    for i, r in enumerate(keep, 1):
        w.writerow({"row": i, **r})
print(len(rows), "raw ->", len(keep), "candidates")
