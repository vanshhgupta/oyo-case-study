"""Joins AI-coded tags to the Co-OYO (partner app) reviews and computes the numbers used in review_analysis.md.
Run from the project root:  .venv/bin/python research/analyse_owner.py
"""
import csv, json, collections
NAMES = {"pay": "Payouts late, held or missing", "ded": "Deductions, penalties and commission", "price": "OYO sets or cuts the room price",
         "book": "Bookings: fake, unexpected, auto check-in or not shown", "inv": "Inventory and room control", "guest": "Guest disputes",
         "supp": "Partner support unreachable or unhelpful", "exit": "Leaving OYO / contract termination", "app": "App works badly",
         "good": "Praise", "x": "Not specific"}
rows = {r["row"]: r for r in csv.DictReader(open("research/owner_reviews_filtered.csv"))}
tags = {}
for l in open("research/coding/owner_tags.txt"):
    k, t, s = l.strip().split("|"); tags[k] = (t.split(","), s)
assert set(tags) == set(rows)
with open("research/owner_reviews.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["row", "review_id", "date", "rating", "tags", "stance", "text"])
    for k in sorted(rows, key=int):
        r = rows[k]; w.writerow([k, r["review_id"], r["date"], r["rating"], ";".join(tags[k][0]), tags[k][1], r["text"]])
raw = list(csv.DictReader(open("research/owner_reviews_raw.csv")))
pct = lambda a, b: round(100 * a / b, 1)
def summarise(keys):
    spec = [k for k in keys if tags[k][0] not in (["x"], ["good"]) ]
    c = collections.Counter(t for k in spec for t in tags[k][0] if t not in ("x", "good"))
    nonapp = [k for k in spec if set(tags[k][0]) - {"app", "x", "good"}]
    c2 = collections.Counter(t for k in nonapp for t in tags[k][0] if t not in ("x", "good", "app"))
    money = sum(bool({"pay", "ded", "price"} & set(tags[k][0])) for k in nonapp)
    return {"reviews": len(keys), "specific_issue_reviews": len(spec), "tag_counts": {NAMES[t]: n for t, n in c.most_common()},
            "business_issue_reviews": len(nonapp),
            "business_tag_share": {NAMES[t]: {"n": n, "pct": pct(n, len(nonapp))} for t, n in c2.most_common()},
            "money_related": {"n": money, "pct_of_business": pct(money, len(nonapp))},
            "stance": dict(collections.Counter(tags[k][1] for k in keys))}
allk = list(tags)
recent = [k for k in tags if rows[k]["date"] >= "2023-01-01"]
S = {"raw_reviews": len(raw), "raw_window": [min(r["date"] for r in raw), max(r["date"] for r in raw)],
     "raw_ratings": dict(collections.Counter(r["rating"] for r in raw)), "by_year": dict(sorted(collections.Counter(r["date"][:4] for r in raw).items())),
     "coded_5plus_words": summarise(allk), "since_2023": summarise(recent)}
json.dump(S, open("research/owner_stats.json", "w"), indent=1, ensure_ascii=False)
print(json.dumps(S, indent=1, ensure_ascii=False))
