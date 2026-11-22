"""Joins the AI-coded tags to the filtered reviews and computes every number used in review_analysis.md.
Writes research/guest_reviews.csv (one row per candidate, with its codes) and research/review_stats.json.
Run from the project root:  .venv/bin/python research/analyse_guest.py
"""
import csv, json, collections

ISSUE = {"D": "Denied at the property", "C": "Cancelled or moved before arrival", "E": "Extra charge at the desk (stayed or no outcome)",
         "L": "Listing mismatch", "Q": "Room quality", "R": "Refund after guest cancelled", "O": "Other booking problem", "X": "Not relevant or not specific"}
REASON = {"full": "No room (full, sold, given to someone else)", "norec": "No record of the booking / won't accept OYO bookings",
          "price": "Price dispute (pay more or leave)", "rule": "ID, couple or house rule", "gone": "Property closed, missing or left OYO",
          "dues": "Hotel cites a payment or contract dispute with OYO", "unst": "No reason stated"}
HANDLING = {"rb": "rebooked elsewhere", "ok": "eventually let in", "rf": "refund received", "rd": "refund pending or late",
            "rr": "refund refused or money lost", "wl": "refund only as OYO wallet/voucher", "px": "paid the extra to get a room",
            "su": "support unreachable", "sh": "support reached but did not solve it"}
COMPLAINT = {"rd", "rr", "wl", "su", "sh"}

rows = {r["row"]: r for r in csv.DictReader(open("research/guest_reviews_filtered.csv"))}
tags = {}
for line in open("research/coding/guest_tags.txt"):
    row, issue, reason, handling, flags = line.strip().split("|")
    tags[row] = dict(issue=issue, reason=reason, handling=[] if handling == "-" else handling.split(","), flags=[] if flags == "-" else flags.split(","))
assert set(tags) == set(rows), "every candidate must be coded exactly once"

with open("research/guest_reviews.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["row", "review_id", "date", "rating", "issue", "denial_reason", "handling", "prepaid", "night", "handling_complaint", "text"])
    for k in sorted(rows, key=int):
        r, t = rows[k], tags[k]
        w.writerow([k, r["review_id"], r["date"], r["rating"], t["issue"], t["reason"] if t["issue"] == "D" else "",
                    ";".join(t["handling"]), int("p" in t["flags"]), int("n" in t["flags"]),
                    int(bool(COMPLAINT & set(t["handling"]))), r["text"]])

raw = list(csv.DictReader(open("research/guest_reviews_raw.csv")))
rel = {k: t for k, t in tags.items() if t["issue"] != "X"}
N = len(rel)
pct = lambda a, b: round(100 * a / b, 1) if b else 0.0
S = {"raw_reviews": len(raw), "window": [min(r["date"] for r in raw), max(r["date"] for r in raw)],
     "raw_ratings": dict(collections.Counter(r["rating"] for r in raw)),
     "candidates": len(tags), "relevant": N, "not_relevant": len(tags) - N}

ic = collections.Counter(t["issue"] for t in rel.values())
S["issues"] = {ISSUE[i]: {"code": i, "n": n, "pct_of_relevant": pct(n, N)} for i, n in ic.most_common()}

D = {k: t for k, t in rel.items() if t["issue"] == "D"}
nd = len(D)
rc = collections.Counter(t["reason"] for t in D.values())
stated = nd - rc["unst"]
S["denials"] = {"n": nd, "reasons": {REASON[r]: {"code": r, "n": n, "pct_of_denials": pct(n, nd),
                "pct_of_stated": pct(n, stated) if r != "unst" else None} for r, n in rc.most_common()},
                "stated_reason_n": stated}
S["denials"]["prepaid_mentioned"] = {"n": sum("p" in t["flags"] for t in D.values()), "pct": pct(sum("p" in t["flags"] for t in D.values()), nd)}
S["denials"]["night_mentioned"] = {"n": sum("n" in t["flags"] for t in D.values()), "pct": pct(sum("n" in t["flags"] for t in D.values()), nd)}
hc = collections.Counter(h for t in D.values() for h in t["handling"])
S["denials"]["handling"] = {HANDLING[h]: {"code": h, "n": n, "pct_of_denials": pct(n, nd)} for h, n in hc.most_common()}
S["denials"]["any_outcome_described"] = {"n": sum(bool(t["handling"]) for t in D.values()), "pct": pct(sum(bool(t["handling"]) for t in D.values()), nd)}
got_bed = sum(bool({"rb", "ok"} & set(t["handling"])) for t in D.values())
S["denials"]["got_a_bed_via_platform_or_desk"] = {"n": got_bed, "pct": pct(got_bed, nd)}

# Handling-complaint rate by issue type: the within-sample comparison
S["handling_complaint_rate_by_issue"] = {}
for i in ic:
    grp = [t for t in rel.values() if t["issue"] == i]
    c = sum(bool(COMPLAINT & set(t["handling"])) for t in grp)
    S["handling_complaint_rate_by_issue"][ISSUE[i]] = {"code": i, "n": len(grp), "complaints": c, "rate": pct(c, len(grp))}
# Same comparison inside denials, by reason
S["handling_complaint_rate_by_denial_reason"] = {}
for r in rc:
    grp = [t for t in D.values() if t["reason"] == r]
    c = sum(bool(COMPLAINT & set(t["handling"])) for t in grp)
    rb = sum("rb" in t["handling"] for t in grp)
    S["handling_complaint_rate_by_denial_reason"][REASON[r]] = {"code": r, "n": len(grp), "complaints": c, "rate": pct(c, len(grp)), "rebooked": rb}

# Money at the desk: price-dispute denials plus extra-charge reviews
money = sum(1 for t in rel.values() if t["issue"] == "E" or (t["issue"] == "D" and t["reason"] == "price"))
S["money_at_the_desk"] = {"n": money, "pct_of_relevant": pct(money, N), "note": "issue E plus denials with reason 'price'"}
# 'Booked, but no room' family: D + C
S["booked_but_no_room_family"] = {"n": ic["D"] + ic["C"], "pct_of_relevant": pct(ic["D"] + ic["C"], N)}
# Ratings within denials
S["denials"]["ratings"] = dict(collections.Counter(rows[k]["rating"] for k in D))
# By half-year, to show it is not one bad month
half = collections.Counter((rows[k]["date"][:4] + ("-H1" if rows[k]["date"][5:7] <= "06" else "-H2")) for k in D)
allrel = collections.Counter((rows[k]["date"][:4] + ("-H1" if rows[k]["date"][5:7] <= "06" else "-H2")) for k in rel)
S["denial_share_by_half_year"] = {h: {"denials": half[h], "relevant": allrel[h], "pct": pct(half[h], allrel[h])} for h in sorted(allrel)}
# Robustness: drop reviews that are clearly from outside India (keyword rule), recompute the headline numbers
import re
NONIN = re.compile(r"\b(saya|tidak|sudah|udah|bayar|penginapan|hotelnya|kerjasama|gak|nak|takde|aplikasi|dana|Indonesia|Malaysia|Philippines|UAE|Jeddah|Texas|Tx|Oregon|Arkansas|Oklahoma|Indianapolis|Odessa|Waco|Texarkana|Luling|Kuala|Yogyakarta)\b|\$\d", re.I)
relI = {k: t for k, t in rel.items() if not NONIN.search(rows[k]["text"])}
DI = {k: t for k, t in relI.items() if t["issue"] == "D"}
cI = collections.Counter(t["reason"] for t in DI.values()); stI = len(DI) - cI["unst"]
S["robustness_excluding_clearly_non_indian"] = {"denials": len(DI), "relevant": len(relI), "denial_share_pct": pct(len(DI), len(relI)),
    "non_indian_denials": nd - len(DI), "stated_reasons": {REASON[r]: {"n": n, "pct_of_stated": pct(n, stI)} for r, n in cI.items() if r != "unst"},
    "pre_decided_pct_of_stated": pct(cI["gone"] + cI["norec"] + cI["price"], stI)}
S["denials"]["pre_decided_gone_norec_price"] = {"n": rc["gone"] + rc["norec"] + rc["price"], "pct_of_stated": pct(rc["gone"] + rc["norec"] + rc["price"], stated)}
json.dump(S, open("research/review_stats.json", "w"), indent=1, ensure_ascii=False)
print(json.dumps(S, indent=1, ensure_ascii=False))
