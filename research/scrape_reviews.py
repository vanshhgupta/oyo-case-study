"""Collect recent Google Play reviews of OYO's guest app and its partner (hotel owner) app.

Guest app:   com.oyo.consumer   ("OYO : Hotel Booking App")
Partner app: com.oyo.partnerapp ("Co-OYO", the app OYO's hotel partners use)
Both are listed on Google Play under the developer name "PRISM: Hotels, Homes & Experiences in 35 Countries".
Run from the project root:  .venv/bin/python research/scrape_reviews.py
"""
import csv
from google_play_scraper import app, reviews, Sort

TARGETS = [("com.oyo.consumer", "research/guest_reviews_raw.csv", 12000),
           ("com.oyo.partnerapp", "research/owner_reviews_raw.csv", 6000)]

for app_id, path, cap in TARGETS:
    meta = app(app_id, lang="en", country="in")
    print(app_id, "|", meta["title"], "|", meta["developer"], "|", meta["installs"], "| rating", round(meta["score"] or 0, 2), "| reviews", meta.get("reviews"))
    out, token = [], None
    while len(out) < cap:
        batch, token = reviews(app_id, lang="en", country="in", sort=Sort.NEWEST, count=200, continuation_token=token)
        if not batch:
            break
        out.extend(batch)
        if token is None:
            break
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["review_id", "date", "rating", "thumbs_up", "app_version", "text"])
        for r in out:
            w.writerow([r["reviewId"], r["at"].date().isoformat(), r["score"], r["thumbsUpCount"],
                        r.get("reviewCreatedVersion") or "", (r["content"] or "").replace("\n", " ").strip()])
    print("  collected", len(out), "from", out[-1]["at"].date(), "to", out[0]["at"].date())
