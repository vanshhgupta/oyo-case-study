"""Checks that every quote on the case study page and in review_analysis.md appears verbatim in the review data.
Quotes on the page are <blockquote class="q" data-src="guest|owner">; in the analysis they are Markdown '> "..."' lines.
Run from the project root:  .venv/bin/python check_quotes.py   (exits with an error if any quote is not found)
"""
import csv, html, re, sys
def norm(s):
    s = html.unescape(s)
    for a, b in [("“", '"'), ("”", '"'), ("‘", "'"), ("’", "'"), ("…", "...")]:
        s = s.replace(a, b)
    return re.sub(r"\s+", " ", s).strip().lower()
texts = {"guest": [norm(r["text"]) for r in csv.DictReader(open("research/guest_reviews.csv"))],
         "owner": [norm(r["text"]) for r in csv.DictReader(open("research/owner_reviews.csv"))]}
quotes = []
page = open("case-study/index.html").read()
for src, body in re.findall(r'<blockquote class="q" data-src="(\w+)"><p>(.*?)</p>', page, re.S):
    quotes.append(("page", src, re.sub("<[^>]+>", "", body)))
for line in open("research/review_analysis.md"):
    m = re.match(r'> "(.*)" \((Co-OYO review|guest review|row|the hotel)', line)
    if m:
        quotes.append(("review_analysis.md", "owner" if m.group(2).startswith("Co-OYO") else "guest", m.group(1)))
bad = 0
for where, src, q in quotes:
    parts = [p.strip(' "') for p in re.split(r"\.\.\.(?!\.)|…", norm(q).strip('"')) if p.strip(' ".')]
    ok = any(all(p in t for p in parts) for t in texts[src])
    print(("OK      " if ok else "MISSING "), where, "|", q[:80])
    bad += not ok
print(f"\n{len(quotes) - bad} of {len(quotes)} quotes found verbatim in the review data.")
sys.exit(1 if bad else 0)
