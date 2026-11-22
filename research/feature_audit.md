# Feature audit: what happens today when a guest is denied check-in

The first interview question is "OYO already handles this, so what is new?". This document answers it from OYO's own public pages, then compares Booking.com, Airbnb, MakeMyTrip and Goibibo. Every excerpt below was read on the live page during the data collection window; the items marked ✔ were re-fetched and checked word for word a second time. Source links are in `sources.md`.

## 1. What OYO promises the guest

| Question | What OYO's pages say | Where |
|---|---|---|
| Is the guest promised a room or a replacement? | **Yes, firmly, in the Terms of Use:** "If any check-in is denied for a confirmed booking, OYO shall ensure that User is provided with an alternate accommodation of comparable standards." If it cannot, "OYO shall arrange for the refund of any pre booking amount". ✔ | Terms of Use, clause 4 (page shows "Last updated: 25/05/2026") |
| | **More softly, in the Guest Policy:** OYO first verifies with the hotel, then "will try" the same hotel, then "will try" another OYO property, and otherwise "you may be offered full refund". ✔ | Guest Policy |
| How does the guest report it? | Contact OYO "immediately" by the 24x7 helpline or the support page. The web help page asks only for a booking ID. There is no denial-specific hotline. | Guest Policy; Terms of Use 4.6 |
| Compensation beyond the room? | No: "OYO will not be liable for compensation beyond your booking payment." ✔ | Guest Policy |
| Who pays for a pricier replacement or the cab to it? | **Not stated** anywhere public. | — |
| How fast? | **No time limit** for relocation. Refunds in general: "within 7-14 working days". A separate "Service On-Time" promise (resolution within 1 hour, otherwise a refund) covers "selected hotels" in six cities and "any issue related to your stay"; it does not say whether denial is covered. | Guest Policy |
| Refund to source or to OYO Money? | Not stated for denials. | — |
| How long does the guest have to complain? | The two pages disagree. Terms of Use clause 17: a refund request can be raised "within 7 days from your checkout date". Guest Policy: "No complaint would be entertained post check out." | Terms of Use; Guest Policy |
| When does the guest get nothing? | If the hotel refuses unmarried couples or local IDs (the policy says this is shown before booking), if the guest lacks a valid original ID, or "if the Hotel is suspicious of the Guests check-in": "OYO shall be under no obligation to refund any amount to the Guest." ✔ | Guest Policy, Cancellation Policy points 3 and 4 |
| Pay-at-hotel bookings | May be "put on hold or cancelled" if the guest does not answer OYO's confirmation calls. A guest can arrive believing a pay-at-hotel booking is confirmed when it is not. | Guest Policy, Contact Policies |

## 2. What OYO's partner terms say to the hotel owner

These are the most important findings in the audit.

| Rule | Excerpt | Where |
|---|---|---|
| **Denial is already forbidden.** | The owner "shall not deny check-in to any OYO customer under any circumstances at the Property" ✔ | Partner Terms of Service (India), 2.G "Assured Check-in" |
| **The owner already pays for relocation.** | "the cost of shifting or relocating such OYO customers, cost of compensating the OYO customers for inconvenience ... shall be solely borne by the OYO Patron" ✔ | same |
| **Penalties are deducted from payouts.** | "OYO has the right to offset/adjust such amounts against monies due or payable to the OYO Patron and reserves the right to levy penalties" | same |
| Denial can get the listing suspended. | "denial of check in to guests who have valid bookings/ reservations" is a listed reason for suspension ✔ | Partner ToS 2.I, item 14 |
| **OYO, not the owner, sets the price.** | "OYO shall have exclusive rights to determine the pricing of Contracted Rooms" ✔. The prospectus adds that owners get "a limited degree of flexibility... to set prices within a specified range" ✔ | Partner ToS 2.F; UDRHP-I |
| **OYO controls the inventory.** | OYO "will manage and be responsible for complete revenue, pricing, inventory, and booking management for 100% of the Contracted Rooms inventory" ✔ | Partner ToS, OTA clause |
| Owner must honour the voucher. | "shall honour all the commitments made in the booking voucher at all times" ✔ | Partner ToS 2.J |
| A stated penalty, for one campaign only | Denying check-in on "Free Room Night" bookings costs the operator "10x of ARR" (ten times the average room rate) ✔ | Terms of Use page, operator policy table |
| Consumer-court costs | OYO can recover from the operator all costs of a consumer-forum claim caused by a denial attributable to the operator | Terms of Use page, clause 36 |
| The penalty schedule itself | The partner ToS refers to "OYO Policies" for penalty amounts. The linked domain did not resolve, and no schedule was found anywhere public. | — |

**What the owner's app offers** (Co-OYO, Google Play listing): booking and reservation management; "Manage room availability, sellable status, and room occupancy"; a "real-time view of live escalations from customers who are at your property"; guest call-picked rate; a "3C score"; daily payouts; price selection from a range with a suggested price. ✔ **The listing describes no step where the owner accepts or confirms an individual booking.** That fits the partner terms, under which OYO controls pricing and inventory.

## 3. So what is new?

On paper, OYO already has the three things a student would propose first: a guest promise ("shall ensure... alternate accommodation"), an owner ban ("shall not deny... under any circumstances"), and an owner penalty (relocation costs, penalties offset against payouts, suspension).

The reviews show that these do not work at the moment of truth: only 5% of denied guests describe being rebooked (`review_analysis.md`, section 6). Three gaps explain why the paper rules fail, and they are what this case study works on:

1. **The owner is never asked.** OYO sets the price (owners can move it only within a range OYO sets) and sells the room on the owner's behalf, and no step asks the owner to confirm a booking before the guest travels. The first time the owner can say no is at the desk.
2. **The guest's promise has no clock.** "Shall ensure" has no time limit, no stated owner of the price difference, and no in-app path built for someone standing at a counter at night.
3. **The penalty arrives as one more deduction.** Penalties are offset against payouts under a schedule that is not public. Owners already describe deductions as opaque and unfair (28% of owner business complaints, 49% since 2023). A bigger hidden penalty is unlikely to change behaviour, and likely to deepen the distrust that drives some refusals.

## 4. What I could not see

- The in-app "Need help" flow after a booking ID is entered (it needs a real booking), whether a "check-in denied" issue type exists, and its internal time targets.
- Whether OYO pays for the replacement room or transport in practice, and how often it relocates rather than refunds.
- The penalty schedule ("OYO Policies"), the 3C or quality score rules, and whether a denial affects ranking.
- What Co-OYO shows the owner during a "live escalation", and whether any owners are asked to accept bookings.
- Internal denial rates.

These are the first questions to ask anyone who works at OYO, and they are listed as open questions in the PRD.

## 5. How others handle a host or hotel that refuses a confirmed booking

| | Who must rebook the guest | Who pays | Time limit | Penalty on the host or hotel |
|---|---|---|---|---|
| **Booking.com** | The property: "it's your responsibility to find your guest accommodation elsewhere, of the same or a better standard – and cover the costs." ✔ Booking.com customer service also contacts both sides. | Property pays the replacement and transport ("organise transport... or you might have to reimburse it later") ✔ | For relocations on the day or within 24 hours of check-in, **30 minutes** ✔ (2 hours if 1 to 7 days out, 24 hours if more) | Commission is still charged on overbookings unless the property has had no more than four in 12 months ✔ |
| **Airbnb** | Airbnb offers rebooking or a refund when a "Host fails to provide their guest access"; guests must report within 72 hours ✔ | Airbnb "may, but [is] not obligated to" contribute to the new booking; the host's payout is reduced by the refund | — | Host cancellation fee: 50% of the reservation if 48 hours or less before check-in ✔ (minimum $50), the calendar is blocked for those dates, and the host can lose Superhost status or the listing |
| **MakeMyTrip** | "similar alternate accommodation at the discretion of MMT (subject to availability at that time), or refunding the booking amount" | Not stated | None | Not public. "Hotels reserves the sole right of admission" |
| **Goibibo** | Same wording as MakeMyTrip | Not stated | None | Not public. Its "goStays" assurance covers amenities (AC, TV, WiFi, clean rooms), not check-in |

**What carries over:** Booking.com shows that a firm clock (30 minutes on the day) and costs charged to the property can coexist with a large hotel supply. Airbnb shows the value of a penalty that rises as check-in approaches, which rewards a host for saying no early. Neither asks the hotel to re-confirm each booking before arrival; Booking.com and Airbnb hotels and hosts set their own prices and availability, so the "owner never agreed" gap is much smaller there. That gap is specific to OYO's model.
