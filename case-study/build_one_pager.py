"""Builds case-study/one_pager.pdf with ReportLab (not by printing HTML).
Uses Georgia, which has the rupee sign. Reads the method note from research/validation/results.json if validation has been done.
Run from the project root:  .venv/bin/python case-study/build_one_pager.py
"""
import json, pathlib
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepInFrame)
from reportlab.lib.styles import ParagraphStyle

ROOT = pathlib.Path(__file__).resolve().parents[1]
CFG = json.load(open(ROOT / "project_config.json"))
F = "/System/Library/Fonts/Supplemental/"
pdfmetrics.registerFont(TTFont("G", F + "Georgia.ttf"))
pdfmetrics.registerFont(TTFont("GB", F + "Georgia Bold.ttf"))
pdfmetrics.registerFont(TTFont("GI", F + "Georgia Italic.ttf"))
pdfmetrics.registerFontFamily("G", normal="G", bold="GB", italic="GI", boldItalic="GB")

INK, MUTED, ACCENT, WARM = colors.HexColor("#1d1b26"), colors.HexColor("#5d5a6b"), colors.HexColor("#4338ca"), colors.HexColor("#b45309")
S = lambda name, **k: ParagraphStyle(name, fontName=k.pop("f", "G"), textColor=k.pop("c", INK), **k)
kick = S("k", f="GB", fontSize=7.5, leading=10, c=WARM)
h1 = S("h1", f="GB", fontSize=24, leading=27)
lead = S("lead", fontSize=10.5, leading=14.2)
h2 = S("h2", f="GB", fontSize=10.5, leading=13, c=ACCENT, spaceBefore=6, spaceAfter=2)
body = S("b", fontSize=8.6, leading=11.6)
small = S("s", fontSize=7.2, leading=9.4, c=MUTED)
statn = S("sn", f="GB", fontSize=19, leading=21, c=WARM)
stat = S("st", fontSize=7.6, leading=9.8, c=MUTED)

res = ROOT / "research/validation/results.json"
if res.exists():
    r = json.load(open(res)); f = r["fields"]
    method = (f"Reviews were coded by an AI model (Claude, made by Anthropic) against a written codebook, not by hand. {CFG['author']} coded a "
              f"random sample of {r['n']} blind: agreement on the main issue {f['issue']['agreement_pct']}% (Cohen's kappa {f['issue']['kappa']}).")
else:
    method = ("Reviews were coded by an AI model (Claude, made by Anthropic) against a written codebook, not by hand. Human validation of a "
              "random sample of 100 coded reviews is pending; until then, treat review counts as AI-coded and unchecked.")

story = []
story.append(Paragraph("PRODUCT CASE STUDY · OYO, INDIA · INDEPENDENT, NOT AFFILIATED WITH OYO", kick))
story.append(Spacer(1, 3))
story.append(Paragraph("Booked, but no room", h1))
story.append(Spacer(1, 4))
story.append(Paragraph("A guest arrives with a confirmed, often prepaid OYO booking and the front desk turns them away. "
                       "The hotel's \"no\" usually existed before the guest left home; nobody asked for it until the guest was at the counter.", lead))
story.append(Spacer(1, 7))

stats = [("37%", "of 1,632 arrival-stage problems in recent guest app reviews are a denied check-in, the largest single issue"),
         ("73%", "of denials with a stated reason were decided before arrival: hotel gone, not taking OYO bookings, or refusing the app price"),
         ("10%", "of denied guests say they ended up in a bed through OYO or the hotel; 56% also complain about the follow-up"),
         ("68%", "of hotel owners' business complaints in the owner app's reviews are about money: payouts, deductions, price")]
st = Table([[Paragraph(n, statn) for n, _ in stats], [Paragraph(t, stat) for _, t in stats]], colWidths=[44 * mm] * 4)
st.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f3f1ec")),
                        ("LINEAFTER", (0, 0), (-2, -1), 3, colors.white), ("TOPPADDING", (0, 0), (-1, -1), 6),
                        ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
story.append(st)

left = []
left.append(Paragraph("The insight", h2))
left.append(Paragraph("Check-in denial is a <b>consent problem, not an arrival problem</b>. OYO's partner terms already forbid denial \"under any "
                      "circumstances\" and make the owner pay for relocation, but OYO sets the price within a range and manages the inventory, and "
                      "the owner app has no step to accept a booking. The owner never agrees to a specific booking at a specific price, so it says no "
                      "at the only point it controls: the front desk.", body))
left.append(Paragraph("The design: RoomReady", h2))
for t in ["<b>Ask early.</b> The owner confirms each prepaid booking by 6 hours before check-in. A \"no\" or no answer moves the guest to a confirmed "
          "room within 3 km (OYO pays up to ₹400 difference) or refunds to source, before travel.",
          "<b>Rescue fast.</b> A location-checked \"refused at the desk\" report starts a 15-minute clock: call the hotel, then rebook nearby with a cab "
          "up to ₹250, or start the refund at once and offer honest next options.",
          "<b>Charge fairly.</b> Declining early is free up to 1 in 20 bookings a month; refusing at the desk after confirming costs the owner the actual "
          "relocation, shown with evidence and open to a 48-hour appeal."]:
    left.append(Paragraph("• " + t, body))
left.append(Paragraph("Costed first", h2))
left.append(Paragraph("The first, generous version (free unlimited declines, uncapped top-ups, ₹300 credit per moved guest) lost <b>₹6.9 crore a year</b> "
                      "in the base case, mostly because a free \"no\" gets used. The capped design is roughly break-even.", body))
imp = Table([["₹ crore a year, projected", "Pessimistic", "Base", "Optimistic"],
             ["Benefit", "0.8", "4.0", "11.4"], ["Cost", "6.2", "3.9", "3.0"], ["Net", "−5.4", "+0.1", "+8.4"]],
            colWidths=[38 * mm, 20 * mm, 16 * mm, 20 * mm])
imp.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "G", 7.8), ("FONT", (0, 0), (-1, 0), "GB", 7.8), ("FONT", (0, 3), (-1, 3), "GB", 7.8),
                         ("TEXTCOLOR", (1, 3), (1, 3), colors.HexColor("#b42318")), ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
                         ("LINEBELOW", (0, 0), (-1, -1), 0.4, colors.HexColor("#dddddd")), ("TOPPADDING", (0, 0), (-1, -1), 2),
                         ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]))
left.append(Spacer(1, 3)); left.append(imp)
left.append(Paragraph("Main assumptions: 0.4% of bookings end in a denial (no public figure exists), and owners decline at most 0.15% more bookings once "
                      "saying no early is easy. Base case: about 83,000 more guests a year with a bed.", small))
left.append(Paragraph("How we'd know", h2))
left.append(Paragraph("North star: share of prepaid bookings where the guest sleeps in a confirmed room at the price paid. Guardrails: extra owner declines "
                      "(kill above 0.3%), net cost, owner churn, appeals upheld, abuse. Pilot randomised by property: ~570 per arm for 8 weeks.", body))

right = [Image(str(ROOT / "case-study/img/g3.png"), width=46 * mm, height=46 * mm * 770 / 400),
         Paragraph("Prototype: the hotel declined, so the guest is moved before travelling. Invented names and prices.", small)]
cols = Table([[left, right]], colWidths=[122 * mm, 54 * mm])
cols.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (0, 0), 8)]))
story.append(cols)

story.append(Spacer(1, 5))
story.append(Paragraph("Method and limits", h2))
story.append(Paragraph(method + " Data: 12,000 OYO guest app reviews (19 May 2025 to 20 November 2026; 2,031 coded) and 913 owner app reviews; "
                       "OYO's draft IPO prospectus, guest and partner terms; consumer-court orders. Reviews show which problems exist, not how often "
                       "they happen per booking. No interviews were done.", small))
story.append(Spacer(1, 4))
story.append(Paragraph(f"<b>{CFG['author']}</b> · An independent student case study, not affiliated with or endorsed by OYO or its parent company. "
                       "Projected impact under stated assumptions; nothing here has been built or measured.", small))

doc = SimpleDocTemplate(str(ROOT / "case-study/one_pager.pdf"), pagesize=A4, leftMargin=16 * mm, rightMargin=16 * mm,
                        topMargin=13 * mm, bottomMargin=11 * mm, title="Booked, but no room", author=CFG["author"],
                        subject="Product case study: check-in denial at OYO")
doc.build(story)
print("wrote case-study/one_pager.pdf")
