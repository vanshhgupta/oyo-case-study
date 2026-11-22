"""Draws the 100-review validation sample. Run once; the output is already in this folder.
Creates:
  validation_sample.xlsx  - the sheet you fill in (the AI's codes are NOT in it)
  answer_key.csv          - the AI's codes for the same 100 reviews (kept out of git; do not open it before you finish)
Run from the project root:  .venv/bin/python research/validation/make_sample.py
"""
import csv, random
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation

rows = list(csv.DictReader(open("research/guest_reviews.csv")))
random.seed(42)                      # fixed seed, so the same sample is drawn every time
sample = random.sample(rows, 100)

with open("research/validation/answer_key.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["sample_id", "row", "issue", "denial_reason", "support_or_refund_complaint"])
    for i, r in enumerate(sample, 1):
        w.writerow([f"S{i:03d}", r["row"], r["issue"], r["denial_reason"], "yes" if r["handling_complaint"] == "1" else "no"])

wb = Workbook(); ws = wb.active; ws.title = "Code these"
head = ["sample_id", "rating", "review_text", "issue", "denial_reason", "support_or_refund_complaint", "your_notes"]
ws.append(head)
for c in ws[1]:
    c.font = Font(bold=True); c.fill = PatternFill("solid", fgColor="DDE7F0")
for i, r in enumerate(sample, 1):
    ws.append([f"S{i:03d}", int(r["rating"]), r["text"], None, None, None, None])
for col, width in zip("ABCDEFG", [10, 7, 90, 9, 14, 16, 30]):
    ws.column_dimensions[col].width = width
for row in ws.iter_rows(min_row=2, max_col=3):
    row[2].alignment = Alignment(wrap_text=True, vertical="top")
dv_issue = DataValidation(type="list", formula1='"D,C,E,L,Q,R,O,X"', allow_blank=True)
dv_reason = DataValidation(type="list", formula1='"full,norec,price,rule,gone,dues,unst"', allow_blank=True)
dv_yn = DataValidation(type="list", formula1='"yes,no"', allow_blank=True)
for dv, col in [(dv_issue, "D"), (dv_reason, "E"), (dv_yn, "F")]:
    ws.add_data_validation(dv); dv.add(f"{col}2:{col}101")
ws.freeze_panes = "D2"

guide = wb.create_sheet("How to code")
lines = [
    "Code each review yourself before you look at anything else. Do not open answer_key.csv or research/guest_reviews.csv until you have finished.",
    "Use research/codebook.md. It takes about 60 to 90 minutes for 100 reviews.",
    "",
    "issue (one per review): D denied at the property | C cancelled or moved before arrival | E extra charge at the desk, guest stayed or no outcome",
    "  L listing mismatch | Q room quality | R refund after the guest cancelled | O other booking problem | X not relevant or not specific",
    "  If several apply, use this order: D, C, E, L, Q, R, O.",
    "denial_reason (only when issue is D): full | norec | price | rule | gone | dues | unst  (the reason the HOTEL gave; the first one if two)",
    "support_or_refund_complaint: yes if the review complains that the refund was late, refused or only given as OYO wallet money,",
    "  or that support was unreachable or did not solve it. Otherwise no.",
    "",
    "When you finish, save the file and run:  .venv/bin/python research/validation/compare.py research/validation/validation_sample.xlsx",
    "Then:  .venv/bin/python research/validation/write_method_note.py",
]
for l in lines:
    guide.append([l])
guide.column_dimensions["A"].width = 140
wb.save("research/validation/validation_sample.xlsx")
print("sample drawn:", len(sample), "| issue mix in sample:", {k: sum(r["issue"] == k for r in sample) for k in "DCELQROX"})
