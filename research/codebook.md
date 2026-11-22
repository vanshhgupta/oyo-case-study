# Codebook for OYO guest and partner app reviews

This codebook was written after reading the first 70 guest-review candidates and then applied to every candidate. One denial reason (`dues`) and three hard-case rules were added while coding; after coding finished, all rows were searched by keyword for the new reason so that earlier rows were treated the same way. **The first-pass coding was done by an AI model (Claude, made by Anthropic) following this codebook, not by a person.** A random sample of 100 coded guest reviews is set aside in `validation/` so that a person can code it blind and measure agreement. Until that check has been run, treat every count below as AI-coded and unvalidated.

Each guest review gets four fields: one **issue**, a **denial reason** (only for issue `D`), zero or more **handling** tags, and two **flags**.

## 1. Issue (one per review)

Pick the issue that broke the stay. If a review mentions several, use this order of precedence: D, C, E, L, Q, R, O.

| Code | Name | Use when | Do not use when |
|---|---|---|---|
| `D` | Denied at the property | The guest had a booking, reached (or was about to reach) the property, and did not get a room on the booked terms: turned away, told there is no booking, told to pay more or leave, refused under an ID or couple rule, or the property was closed, missing or no longer with OYO. | The guest stayed and only complains about paying extra (use `E`). |
| `C` | Cancelled or changed before arrival | The hotel or OYO cancelled, moved or changed a confirmed booking before the guest arrived. | The guest learned it only at the desk (use `D`). |
| `E` | Extra charge at the desk, guest stayed or no outcome given | Asked at the property to pay more than the app price, and the review does not say the guest was turned away. | |
| `L` | Listing mismatch | The property or room is not what the listing showed: photos, amenities, name, location far from the pin, AC missing. | Hygiene or broken items only (use `Q`). |
| `Q` | Room quality | Dirty, broken, unsafe or noisy room, poor service during the stay. | |
| `R` | Refund after the guest cancelled | The guest cancelled, or the review is only about a refund, and the refund was late, refused or credited to the OYO wallet. | The refund follows a denial or listing problem (code that issue, put the refund under handling). |
| `O` | Other booking problem | Payment, booking changes, app pricing, staff conduct, early checkout, support-only complaints with a specific booking problem. | |
| `X` | Not relevant or not specific | Praise, app usability, generic "fraud app" with no described event, non-OYO topics. | |

## 2. Denial reason (issue `D` only, one per review)

Code the reason **the hotel gave**, as the guest reports it. If the hotel gave two, code the first one stated.

| Code | Reason | Examples of what the guest reports |
|---|---|---|
| `full` | No room | "rooms are full", "hotel is booked", "no room available", room given to someone else |
| `norec` | No record of the booking | "booking not received", "we don't accept OYO / online bookings", "this booking is not ours" |
| `price` | Price dispute | "can't give at this price", "pay ₹X more or leave", "promotional price not valid" |
| `rule` | ID, couple or house rule | local ID refused, unmarried couple, marriage certificate demanded, original ID demanded |
| `gone` | Property gone | closed, locked, not at the address, does not exist, no longer partnered with OYO |
| `dues` | Dispute with OYO | the hotel says OYO has not paid it, or its contract terms with OYO are in dispute (added after row 199, the first case) |
| `unst` | Not stated | the review says only that the room was denied |

## 3. Handling (what happened after the guest asked for help; zero or more)

| Code | Meaning |
|---|---|
| `rb` | OYO or the hotel arranged another room or property |
| `ok` | Eventually let in at the same property after calls or waiting |
| `rf` | Refund received |
| `rd` | Refund pending or delayed |
| `rr` | Refund refused, or the guest says the money is lost |
| `wl` | Refund given only as OYO wallet money or a voucher |
| `px` | Guest paid the extra amount to get the room |
| `su` | Support unreachable: calls on hold or cut, no reply, chatbot only |
| `sh` | Support reached but did not solve it: rude, blamed the hotel, asked for proof, "can't do anything" |

A review is a **handling complaint** if it has any of `rd`, `rr`, `wl`, `su` or `sh`.

## 4. Flags

| Code | Set when the review says |
|---|---|
| `p` | the booking was prepaid or paid online |
| `n` | it happened at night, at midnight or late in the evening |

## Record format

One line per candidate in `coding/guest_tags.txt`: `row|issue|reason|handling|flags`, where `row` is the row number in `guest_reviews_filtered.csv`, and lists are comma-separated or `-` when empty. Example: `48|D|full|sh|p,n`.

## Rules for hard cases

- Reviews in Hindi, Hinglish or Indonesian are coded when the meaning is clear; otherwise `X`.
- A general statement that hotels refuse OYO bookings ("hotels don't allow check-in without extra money") counts as `D` only if it says the guest was refused; a general statement about extra money is `E`.
- "Money wasted" or "lost my money" counts as `rr`.
- When OYO "initiated a refund" that has not arrived, code `rd`.
- If the hotel says the booking or payment was "not received" and makes the guest pay again, code `D` with reason `norec` and handling `px`, even though the guest stayed. If the hotel only asks for more than the app price and the guest pays and stays, code `E`.
- A review that only praises a named support agent for a refund, with no problem described, is `R` with `rf`.
- Reviews by the property side posted on the guest app are `X`.

## Partner (owner) app codebook

Each Co-OYO review gets one or more **owner issue** tags and one **stance** (`neg`, `pos`, `mixed`).

| Code | Owner issue | Use when the owner says |
|---|---|---|
| `pay` | Payouts | payments late, held, missing, settlement unclear |
| `ded` | Deductions and penalties | penalties, fines, deductions, "chargeback", commission higher than agreed |
| `price` | Pricing control | OYO sets or cuts room prices, discounts the owner did not agree to |
| `book` | Booking problems | fake or unexpected bookings, bookings not shown, cancellations, booking sync with the front desk |
| `inv` | Inventory and room control | cannot close rooms, block dates, mark rooms sold, update availability |
| `guest` | Guest disputes | guest complaints judged against the owner, couple or ID disputes, guest misconduct |
| `supp` | Partner support | relationship manager or support unreachable or unhelpful |
| `exit` | Leaving OYO | wants to leave, contract termination, still listed after leaving |
| `app` | App works badly | crashes, login, slow, OTP |
| `good` | Praise | useful app, good earnings |
| `x` | Not relevant | no clear meaning |

Record format in `coding/owner_tags.txt`: `row|tags|stance`.
