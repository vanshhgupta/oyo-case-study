"""Builds strategy/impact_model.xlsx with live formulas, then evaluates it with pycel to confirm the numbers.
Run from the project root:  .venv/bin/python strategy/build_model.py
Every input sits in its own labelled cell with its source, or the word "assumption".
"""
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.comments import Comment

OUT = "strategy/impact_model.xlsx"
wb = Workbook()
ws = wb.active
ws.title = "Model"
BLUE = Font(color="1F3FBF", bold=True)
BOLD = Font(bold=True)
HEAD = PatternFill("solid", fgColor="E6E3F0")
INFILL = PatternFill("solid", fgColor="F3F6FF")
RES = PatternFill("solid", fgColor="FFF4E0")
thin = Border(bottom=Side(style="thin", color="CCCCCC"))

ws["A1"] = "RoomReady impact model: pre-arrival confirmation + desk rescue (India, one year)"
ws["A1"].font = Font(bold=True, size=14)
ws["A2"] = ("Independent student case study, not affiliated with OYO. Projected impact under stated assumptions; nothing here has been "
            "built or measured. Blue cells are inputs: change one and everything below recalculates.")
ws["A2"].alignment = Alignment(wrap_text=True)
ws.merge_cells("A2:F2"); ws.row_dimensions[2].height = 32

hdr = ["Input", "Pessimistic", "Base", "Optimistic", "Unit", "Source or 'assumption'"]
for i, h in enumerate(hdr, 1):
    c = ws.cell(row=4, column=i, value=h); c.font = BOLD; c.fill = HEAD

# (row, label, pess, base, opt, unit, source)
INPUTS = [
    (5, "India gross booking value (GBV), FY25", 3511.53, 3511.53, 3511.53, "₹ crore", "Sourced: UDRHP-I (29 Jun 2026), 'GBV – India' Fiscal 2025 = ₹35,115.31 million (hotels in India and Nepal, plus Weddingz and Workspaces)"),
    (6, "Average value of one booking", 1300, 1000, 800, "₹", "Assumption. Anchor: median rupee amount quoted in denial and extra-charge reviews is ₹750 (n=89, middle half ₹500 to ₹1,158). Higher value = fewer bookings = pessimistic"),
    (7, "Check-in denials per booking", 0.002, 0.004, 0.006, "share", "Assumption. No public per-booking figure exists; see sanity check against complaint tickets below"),
    (8, "Share of denials caught early by the handshake", 0.30, 0.45, 0.60, "share", "Assumption. Ceiling: in 73% of denials with a stated reason, the hotel's 'no' existed before arrival (review_analysis.md, section 4)"),
    (9, "Denied guests who get a bed today (rebooked or let in)", 0.097, 0.097, 0.097, "share", "Review data: 58 of 600 denial reviews (review_stats.json)"),
    (10, "Denied guests who get a bed with Desk Rescue", 0.40, 0.60, 0.75, "share", "Assumption. Booking.com requires same-day relocation within 30 minutes (feature_audit.md)"),
    (11, "Guests who accept an early move (the rest take a refund)", 0.50, 0.70, 0.85, "share", "Assumption"),
    (12, "Gross profit as a share of GBV", 0.1919, 0.1919, 0.1919, "share", "Sourced: UDRHP-I, Gross Profit (% of GBV) Fiscal 2025 = 19.19% (company-wide, not India-only)"),
    (13, "Future bookings lost when a guest stops using the app", 2, 3, 4, "bookings", "Assumption. Context: repeat customers generated 60.33% of direct room nights in FY25 (UDRHP-I)"),
    (14, "Chance a guest stops using the app after an unresolved denial", 0.30, 0.40, 0.50, "share", "Assumption. Lower = smaller benefit = pessimistic"),
    (15, "Chance a guest stops using the app after a desk rescue", 0.15, 0.10, 0.05, "share", "Assumption"),
    (16, "Chance a guest stops using the app after an early move", 0.10, 0.05, 0.03, "share", "Assumption"),
    (17, "Support cost of one desk denial today", 100, 150, 200, "₹", "Assumption. Reviews describe 20-minute to two-hour calls and repeat contacts"),
    (18, "Support cost of one early move", 40, 40, 40, "₹", "Assumption. Mostly automated"),
    (19, "OYO top-up per accepted early move", 200, 120, 80, "₹", "Assumption. Design caps it at ₹400; many moves need no top-up"),
    (20, "Cost of one desk rescue (room difference + cab)", 550, 400, 300, "₹", "Assumption. Design caps the cab at ₹250"),
    (21, "Share of desk-rescue cost recovered from the owner", 0.30, 0.50, 0.70, "share", "Assumption. Partner ToS 2.G already makes the owner bear relocation; recovery only when the owner had confirmed"),
    (22, "Extra bookings owners decline because saying no early is now easy", 0.003, 0.0015, 0.0005, "share of all bookings", "Assumption. The biggest risk in the model; the pilot measures it first"),
    (23, "Running cost (engineering, operations)", 3.0, 1.5, 1.0, "₹ crore a year", "Assumption"),
    (24, "Customer complaints received, FY25 (all markets)", 691727, 691727, 691727, "tickets", "Sourced: UDRHP-I, 'Number of Customer complaints received' Fiscal 2025. Used only for the sanity check"),
]
for r, label, p, b, o, unit, src in INPUTS:
    ws.cell(row=r, column=1, value=label)
    for col, v in zip((2, 3, 4), (p, b, o)):
        c = ws.cell(row=r, column=col, value=v); c.font = BLUE; c.fill = INFILL
        if unit.startswith("share"):
            c.number_format = "0.00%" if v < 0.01 else "0.0%"
        elif unit.startswith("₹"):
            c.number_format = "#,##0.00" if r == 5 else "#,##0"
        else:
            c.number_format = "#,##0"
    ws.cell(row=r, column=5, value=unit)
    s = ws.cell(row=r, column=6, value=src); s.alignment = Alignment(wrap_text=True, vertical="top")
    for col in range(1, 7):
        ws.cell(row=r, column=col).border = thin

ws["A26"] = "Calculation"; ws["A26"].font = BOLD; ws["A26"].fill = HEAD
for col in range(2, 7):
    ws.cell(row=26, column=col).fill = HEAD
# (row, label, formula with {c} for the column letter, number format, explanation)
CALC = [
    (27, "Bookings a year", "={c}5*10^7/{c}6", "#,##0", "GBV ÷ average booking value"),
    (28, "Denials a year", "={c}27*{c}7", "#,##0", ""),
    (29, "Denials caught early (guest moved before travelling)", "={c}28*{c}8", "#,##0", ""),
    (30, "Denials that still reach the desk", "={c}28-{c}29", "#,##0", ""),
    (31, "Gross profit per booking", "={c}6*{c}12", "#,##0", "₹"),
    (32, "Future gross profit lost when a guest leaves", "={c}13*{c}31", "#,##0", "₹"),
    (33, "Chance a denied guest leaves, today", "={c}9*{c}15+(1-{c}9)*{c}14", "0.0%", "weighted by today's rescue rate"),
    (34, "Benefit: denials caught early", "={c}29*(({c}33-{c}16)*{c}32+({c}11-{c}9)*{c}31+({c}17-{c}18))", "#,##0", "₹: guests kept + bookings kept + support saved"),
    (35, "Benefit: more desk rescues", "={c}30*({c}10-{c}9)*(({c}14-{c}15)*{c}32+{c}31)", "#,##0", "₹: guests kept + bookings kept"),
    (36, "Cost: top-ups for early moves", "={c}29*{c}11*{c}19", "#,##0", "₹"),
    (37, "Cost: extra desk rescues, after recovery from owners", "={c}30*({c}10-{c}9)*{c}20*(1-{c}21)", "#,##0", "₹"),
    (38, "Cost: extra owner declines", "={c}27*{c}22*({c}19*{c}11+{c}16*{c}32+(1-{c}11)*{c}31+{c}18)", "#,##0", "₹: top-up, some churn, refunded bookings, support"),
    (39, "Cost: running", "={c}23*10^7", "#,##0", "₹"),
]
for r, label, f, fmt, note in CALC:
    ws.cell(row=r, column=1, value=label)
    for col in "BCD":
        c = ws[f"{col}{r}"]; c.value = f.format(c=col); c.number_format = fmt
    ws.cell(row=r, column=6, value=note)
    for col in range(1, 7):
        ws.cell(row=r, column=col).border = thin

ws["A41"] = "Result (₹ crore a year)"; ws["A41"].font = BOLD; ws["A41"].fill = HEAD
for col in range(2, 7):
    ws.cell(row=41, column=col).fill = HEAD
RESULTS = [
    (42, "Total benefit", "=({c}34+{c}35)/10^7", "#,##0.0"),
    (43, "Total cost", "=({c}36+{c}37+{c}38+{c}39)/10^7", "#,##0.0"),
    (44, "Net impact", "={c}42-{c}43", "#,##0.0;[Red]-#,##0.0"),
    (45, "Guests with a bed instead of a refund fight (extra, a year)", "={c}29*{c}11+{c}30*({c}10-{c}9)", "#,##0"),
]
for r, label, f, fmt in RESULTS:
    ws.cell(row=r, column=1, value=label).font = BOLD
    for col in "BCD":
        c = ws[f"{col}{r}"]; c.value = f.format(c=col); c.number_format = fmt; c.fill = RES; c.font = BOLD

ws["A47"] = "Sanity checks"; ws["A47"].font = BOLD; ws["A47"].fill = HEAD
for col in range(2, 7):
    ws.cell(row=47, column=col).fill = HEAD
CHECKS = [
    (48, "Denials as a share of FY25 complaint tickets (all markets)", "={c}28/{c}24", "0.0%", "Should be well under 100%; complaints also cover payments, changes, quality"),
    (49, "Value of denied bookings (₹ crore)", "={c}28*{c}6/10^7", "#,##0.0", "Equals the denial rate × GBV"),
    (50, "Benefit per denial caught early (₹)", "=IF({c}29=0,0,{c}34/{c}29)", "#,##0", "Hand check, base case: (0.371 − 0.05) × ₹576 + (0.70 − 0.097) × ₹192 + (₹150 − ₹40) ≈ ₹185 + ₹116 + ₹110 ≈ ₹411"),
]
for r, label, f, fmt, note in CHECKS:
    ws.cell(row=r, column=1, value=label)
    for col in "BCD":
        c = ws[f"{col}{r}"]; c.value = f.format(c=col); c.number_format = fmt
    ws.cell(row=r, column=6, value=note)

ws["A52"] = "Whiteboard version (one line)"; ws["A52"].font = BOLD
ws["A53"] = ("~3.5 crore bookings × 0.4% denied = 1.4 lakh denials. Catch 45% before travel and rescue 60% of the rest at the desk; "
             "each guest kept is worth ~₹600 of future gross profit. That is ~₹4 crore a year of benefit, roughly cancelled by "
             "~₹4 crore of top-ups, rescue costs, extra owner declines and running cost.")
ws["A53"].alignment = Alignment(wrap_text=True); ws.merge_cells("A53:F53"); ws.row_dimensions[53].height = 48

for col, w in zip("ABCDEF", [56, 14, 14, 14, 18, 90]):
    ws.column_dimensions[col].width = w
ws.freeze_panes = "B5"

# ---------------- Design v1 vs v2 (base case) ----------------
v = wb.create_sheet("Design v1 vs v2")
v["A1"] = "Why the design changed: the first, generous version costed in the base case"; v["A1"].font = Font(bold=True, size=13)
v["A2"] = ("v1 = early decline is free with no limit, OYO pays the full price difference with no cap, a ₹300 goodwill credit to every moved "
           "or rescued guest, and OYO absorbs rescue costs to keep owners happy. v2 = the design in the PRD. Other inputs come from the Base column of 'Model'.")
v["A2"].alignment = Alignment(wrap_text=True); v.merge_cells("A2:D2"); v.row_dimensions[2].height = 46
for i, h in enumerate(["Input that differs", "v1 (generous)", "v2 (PRD)", "Why v2 differs"], 1):
    c = v.cell(row=4, column=i, value=h); c.font = BOLD; c.fill = HEAD
VROWS = [
    (5, "OYO top-up per accepted early move (₹)", 250, "=Model!C19", "Cap at ₹400 and offer same-price rooms first"),
    (6, "Goodwill credit per moved or rescued guest (₹)", 300, 0, "A guest moved before travelling has lost little; credit only by agent judgement"),
    (7, "Share of rescue cost recovered from the owner", 0, "=Model!C21", "Recover only when the owner had confirmed, with evidence shown"),
    (8, "Extra bookings owners decline", 0.004, "=Model!C22", "Decline above 1 in 20 bookings a month lowers ranking"),
]
for r, label, a, b, why in VROWS:
    v.cell(row=r, column=1, value=label)
    ca = v.cell(row=r, column=2, value=a); ca.font = BLUE; ca.fill = INFILL
    cb = v.cell(row=r, column=3, value=b)
    for c in (ca, cb):
        c.number_format = "0.00%" if r == 8 else ("0%" if r == 7 else "#,##0")
    v.cell(row=r, column=4, value=why)
v["A10"] = "Result, base case (₹ crore a year)"; v["A10"].font = BOLD; v["A10"].fill = HEAD
# Same formulas as Model, base column, with the four overrides and a goodwill credit.
B = "Model!C"
def vf(col):
    top, gw, rec, ext = f"{col}5", f"{col}6", f"{col}7", f"{col}8"
    benefit = f"(({B}34+{B}35)/10^7)"
    c_top = f"{B}29*{B}11*({top}+{gw})"
    c_res = f"{B}30*({B}10-{B}9)*({B}20*(1-{rec})+{gw})"
    c_dec = f"{B}27*{ext}*({top}*{B}11+{B}16*{B}32+(1-{B}11)*{B}31+{B}18)"
    cost = f"(({c_top}+{c_res}+{c_dec}+{B}39)/10^7)"
    return benefit, cost
for col in "BC":
    ben, cost = vf(col)
    v[f"{col}11"] = "=" + ben; v[f"{col}12"] = "=" + cost; v[f"{col}13"] = f"={col}11-{col}12"
    for r in (11, 12, 13):
        v[f"{col}{r}"].number_format = "#,##0.0;[Red]-#,##0.0"; v[f"{col}{r}"].fill = RES
v["A11"] = "Total benefit"; v["A12"] = "Total cost"; v["A13"] = "Net impact"; v["A13"].font = BOLD
v["A15"] = "Reading: the benefit is the same in both. v1 spends it, and more, mostly on owners declining bookings they would otherwise have honoured."
for col, w in zip("ABCD", [48, 16, 16, 80]):
    v.column_dimensions[col].width = w

wb.save(OUT)
print("saved", OUT)

# ---------------- Evaluate with pycel ----------------
from pycel import ExcelCompiler
xl = ExcelCompiler(filename=OUT)
def g(ref): return xl.evaluate(ref)
print("\nResults (₹ crore a year)       pess     base      opt")
for r, name in [(42, "benefit"), (43, "cost"), (44, "NET")]:
    print(f"  {name:28s}", *[f"{g(f'Model!{c}{r}'):8.2f}" for c in "BCD"])
print("  extra guests with a bed       ", *[f"{g(f'Model!{c}45'):8,.0f}" for c in "BCD"])
print("  denials a year                ", *[f"{g(f'Model!{c}28'):8,.0f}" for c in "BCD"])
print("  denials / complaint tickets   ", *[f"{g(f'Model!{c}48'):8.1%}" for c in "BCD"])
print("  benefit per early catch (₹)   ", *[f"{g(f'Model!{c}50'):8,.0f}" for c in "BCD"])
print(f"  v1 net {g('Design v1 vs v2!B13'):.2f}   v2 net {g('Design v1 vs v2!C13'):.2f}")
before = g("Model!C44")
xl.set_value("Model!C7", 0.008)
after = g("Model!C44")
print(f"\nRecalculation test: base denial rate 0.4% -> 0.8% moves base net from {before:.2f} to {after:.2f} crore")
assert abs(after - before) > 0.1
