# What 2,031 guest reviews and 398 hotel-owner reviews say about arriving at an OYO

<!-- METHOD-NOTE:START -->
<p><strong>How the reviews were coded.</strong> The reviews were coded by an AI model (Claude, made by Anthropic) against a written codebook, not by hand. Human validation of a random sample of 100 coded reviews is pending. Until it is done, treat every count from the reviews as AI-coded and not yet checked by a person.</p>
<!-- METHOD-NOTE:END -->

## 1. The data

| | Guest app | Partner (hotel-owner) app |
|---|---|---|
| App | "OYO : Hotel Booking App", `com.oyo.consumer` | "Co-OYO", `com.oyo.partnerapp` |
| Publisher on Google Play | PRISM: Hotels, Homes & Experiences in 35 Countries | same |
| How the app ID was confirmed | Play Store search for "OYO hotel booking" and "OYO partner"; both apps list the same publisher | same |
| Reviews collected | 12,000 most recent (Play Store, India store, English setting, newest first) | all 913 the store returned |
| Window | 19 May 2025 to 20 November 2026 | October 2018 to October 2026 (most from 2019 to 2022) |
| Filter | 5+ words and an arrival-stage keyword (check-in, denied, no room, extra money, refund, closed, couple, ID and similar) | 5+ words |
| Reviews coded | 2,031 candidates, of which 1,632 described a specific problem | 398, of which 181 described a business problem (not just app bugs) |

Scripts: `scrape_reviews.py` (collection), `filter_reviews.py` (keyword filter), `analyse_guest.py` and `analyse_owner.py` (counts). The coding rules are in `codebook.md`; the codes are in `coding/`; the joined data are `guest_reviews.csv` and `owner_reviews.csv`; every number below is in `review_stats.json` or `owner_stats.json`.

## 2. What these reviews can and cannot tell us

- **Reviewers skew angry.** 30% of the 12,000 guest reviews are 1-star, and 93% of the denial reviews are. People whose check-in went smoothly rarely write about it.
- **Reviews show which problems exist and how they feel. They do not show how often a problem happens per booking.** "37% of complaints" is not "37% of bookings". Nothing here gives a denial rate per booking; only OYO has that.
- **The keyword filter misses some complaints** (a review that says only "worst app" is not in the set) and catches some praise, which was coded `X` and excluded.
- **The guest side is a reviewer's account.** When a review says "the hotel said it was full", that is what the guest was told, not proof of why.
- **The owner data are thin and older.** Only 90 of the 398 coded owner reviews are from 2023 or later, and 178 are about the app being slow or broken. Owner numbers here are directional.
- **One coder, and it was an AI model.** See the method note above. A 100-review validation sample is in `validation/`.
- **Some reviews are from outside India** (mostly Indonesia, also Malaysia and the US). They were kept because the same app serves them. A keyword check finds 44 of the 600 denial reviews (7%) are clearly non-Indian, many of them about properties that had left OYO. Dropping them changes little: denials are 35.5% of problems instead of 36.8%, the four main reasons still split roughly evenly, and the "decided before arrival" share is 72% instead of 73% (`review_stats.json`, "robustness").

## 3. Guest side: what went wrong

| Issue (one per review) | Reviews | Share of 1,632 |
|---|---:|---:|
| **Denied at the property** | **600** | **36.8%** |
| Extra charge at the desk, guest stayed or outcome not stated | 298 | 18.3% |
| Room quality | 238 | 14.6% |
| Listing mismatch (photos, amenities, location) | 159 | 9.7% |
| Refund after the guest cancelled | 155 | 9.5% |
| Other booking problem | 126 | 7.7% |
| Cancelled or moved by the hotel or OYO before arrival | 56 | 3.4% |

**The working title holds.** Being refused a confirmed room is the single largest arrival-stage complaint, about twice the next one, and its share is steady across the window (33% to 40% in each half-year: see `review_stats.json`). The neighbouring problems considered as alternatives (listing mismatch, refund after cancellation, extra charges) are each smaller. Extra charges matter, but they are mostly the same dispute as one kind of denial (section 5), so they are folded into this study rather than treated as a rival topic.

## 4. Guest side: why the hotel said no

The reason the hotel gave, as the guest reports it, for the 600 denials:

| Reason the hotel gave | Reviews | Share of 600 | Share of the 479 with a stated reason |
|---|---:|---:|---:|
| Property closed, missing, or no longer with OYO | 123 | 20.5% | 25.7% |
| No record of the booking, or "we don't accept OYO bookings" | 117 | 19.5% | 24.4% |
| Price dispute: "can't give it at this price", pay more or leave | 110 | 18.3% | 23.0% |
| No room: full, sold to someone else, overbooked | 106 | 17.7% | 22.1% |
| ID, couple or other house rule | 15 | 2.5% | 3.1% |
| Hotel says it has a payment or contract dispute with OYO | 8 | 1.3% | 1.7% |
| No reason stated | 121 | 20.2% | — |

**No single cause dominates.** Four causes each account for roughly a quarter of stated reasons. This matters for the solution: a fix aimed at only one cause (say, overbooking) would leave three quarters of the problem untouched.

**But three of the four share something.** In a closed or delisted property, a hotel that refuses OYO bookings, and a hotel that will not honour the app price, the hotel's "no" already existed before the guest set out. Together these are **350 of 479 stated reasons (73%)**. Only "no room" (22%) is plausibly a same-day surprise, and some of those were not surprises either:

> "Before 1week called them to confirm the details and the manager/ receptionist whoever....saying that all rooms are full" (guest review, row 713)

> "I called & enquired previous day about the booking, I was assured that rooms were available. When I went for check in Manager denied it." (row 599)

The second quote is the opposite case: a hotel that said yes the day before and no at the desk. A pre-arrival check would not catch it, which is why the solution also needs a rescue.

ID and couple rules, often assumed to be the main cause of denials at OYO, are only 3% of stated reasons in this window.

**Other details from the denial reviews**

- 40% (242 of 600) mention that the booking was prepaid or paid online. The guest's money is already with OYO.
- 9% (56) mention arriving at night or after midnight.
- 6% (38) say they paid the extra amount the hotel demanded to get a room.

## 5. The bridge to extra charges

The 110 "price dispute" denials and the 298 "extra charge" reviews are the same conversation with a different ending: the hotel rejects the app price, and the guest either leaves (a denial) or pays (an extra charge). Together they are **408 reviews, 25% of all problems**. This is where the guest side meets the owner side (section 7).

> "Sir, a room cannot be provided at such a low price. If you want the room, you will have to pay an extra ₹300." (row 1075, the hotel staff's words as the guest reports them)

## 6. Guest side: what happened after the guest asked for help

This is the comparison that is least affected by reviewer bias, because the same bias applies to every issue type in the same sample. For each issue, the share of reviews that also complain about how it was handled afterwards (refund late, refused or only as OYO wallet money; support unreachable or unhelpful):

| Issue | Reviews | Also complain about handling |
|---|---:|---:|
| **Denied at the property** | 600 | **56.0%** |
| Cancelled or moved before arrival | 56 | 39.3% |
| Listing mismatch | 159 | 37.1% |
| Extra charge at the desk | 298 | 30.5% |
| Room quality | 238 | 21.0% |

(Refund-after-cancellation and "other" are left out: a complaint about handling is part of how those two are defined, at 85.8% and 59.5%.)

**A guest who is denied a room is 2.7 times as likely to complain about the follow-up as a guest with a dirty room.** That is the rescue failing, on top of the original failure.

What the 600 denial reviews say happened next (a review can say several things; 66% describe some outcome):

| Outcome | Reviews | Share of 600 |
|---|---:|---:|
| Refund refused, or money described as lost | 150 | 25.0% |
| Support unreachable (hold, disconnected, chatbot only) | 101 | 16.8% |
| Support reached but did not solve it | 90 | 15.0% |
| Refund pending or late | 40 | 6.7% |
| Paid the extra to get a room | 38 | 6.3% |
| **Rebooked at another property** | **31** | **5.2%** |
| Eventually let in at the same property | 27 | 4.5% |
| Refund only as OYO wallet money or a voucher | 17 | 2.8% |
| Refund received | 8 | 1.3% |

**Only 58 of 600 (9.7%) say they ended up with a bed through OYO or the hotel** (rebooked or let in). Within denials, the worst-handled cause is the property that is gone: 75% of those reviews complain about handling, the highest of any reason, against 44% for price disputes. When there is no one at the desk, the guest's only counterparty is OYO.

The sample also contains a cluster of 5-star reviews that thank a named OYO support agent for solving a denial or a refund within "30 minutes", which suggests an existing escalation team. Some of these may be prompted by a review campaign; they are coded like any other review.

## 7. Owner side: what hotel owners say about OYO

Of the 398 coded Co-OYO reviews, 178 are about the app being slow or buggy; these cluster in late 2018 and late 2022, when reviewers say an older owner app was replaced. The 181 that describe a business problem:

| What the owner complains about | Reviews | Share of 181 |
|---|---:|---:|
| Payouts late, held or missing | 56 | 30.9% |
| Partner support unreachable or unhelpful | 53 | 29.3% |
| Deductions, penalties and commission higher than agreed | 50 | 27.6% |
| OYO sets or cuts the room price below what the owner wants | 40 | 22.1% |
| Bookings: "fake" bookings, bookings checked in by OYO staff, bookings not shown | 31 | 17.1% |
| Wants to leave OYO, or cannot get out of the contract | 10 | 5.5% |
| Cannot control inventory | 8 | 4.4% |

**68% (123 of 181) are about money: what OYO pays, what it deducts, and what price it sells the room at.** Since 2023 the mix shifts towards deductions (49% of 45 recent business reviews) and distrust of bookings (29%).

In the owners' own words:

> "i give room for 2400 at my property, I was given a price of 1400 on oyo ... all of a sudden my price was dropped to 876." (Co-OYO review, 2026)

> "Hotel set rate above 1500 but booking received 650 or 700." (Co-OYO review, 2020)

> "The rates settled with hotel at the time of signing the contract are all declined to there minimum low value without intimating the hotel owners." (Co-OYO review, 2019)

Owners also describe being charged for guests who never arrived and for bookings checked in by OYO staff, which explains why some front desks treat an OYO booking with suspicion rather than as a firm reservation.

## 8. What the two sides say together

Read separately, the guest reviews list four different reasons for a denial. Read next to the owner reviews, they look like one pattern: **the owner does not regard an OYO booking, at OYO's price, as something it agreed to.** The owner's grievances are about price and money; the hotel's most common stated reasons at the desk are a refused price, a refused channel ("we don't accept OYO"), and a relationship that has already ended. The front desk is the one point in the journey where the owner, not OYO, decides, so that is where the disagreement surfaces, with a guest standing at the counter.

This is an interpretation, not something the reviews prove. It is the reading that fits both data sets, and it is the one the strategy documents test.

## 9. Cross-check: consumer courts and a complaint forum

A second, independent public source points the same way (details and links in `sources.md`, section D).

- **Consumer commissions.** Twelve decisions on OYO check-in denials were verified from orders or full press reports. The hotel reasons the commissions recorded are the same causes as in the reviews: the contract had ended or the hotel had "no association with OYO", a payment dispute with OYO, extra money demanded, full, or no record of the booking. In every reported decision on the merits that was found, OYO's "only a booking platform" defence was rejected.
- **Complaint forum.** Of 40 check-in-denial complaints on consumercomplaints.in (read in full, mostly from 2022–2023), 17 involve a payment or contract dispute between OYO and the hotel, 15 guests were asked for more money at the desk, and OYO offered another hotel in only 4. In 6, the booking was later marked "checked in" or "no-show" and the refund refused on that basis.
- **What it adds:** the rescue rate (4 of 40, 10%) is close to the reviews' 10%, from a different population and period; and the dispute between OYO and the owner is visible in adjudicated cases, not only in angry reviews.
- **Limits:** courts and forums show the extreme tail, most incidents are older than the review window, and neither measures how often denials happen.

## 10. Quotes used on the case study page

Every quote on the page is checked against `guest_reviews.csv` or `owner_reviews.csv` by `check_quotes.py`, which fails if any quoted text is not found verbatim in the data.
