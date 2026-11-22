# PRD: RoomReady, pre-arrival confirmation and desk rescue

*Independent student case study, not affiliated with OYO. A working PRD written as if for OYO's India guest and partner product teams.*

| | |
|---|---|
| Owner | Product manager, guest trust (case study author) |
| Teams | Guest app, partner app (Co-PRISM, formerly Co-OYO), supply operations, customer support, payments |
| Status | Draft for a pilot in three to four cities |
| Related | `strategy/problem.md`, `strategy/solutions.md`, `strategy/metrics.md`, `strategy/impact_model.xlsx` |

## 1. Background

Being refused a confirmed room is the largest arrival-stage complaint in recent OYO guest app reviews: 600 of 1,632 coded problems (37%). Only about 10% of those guests describe ending up in a bed through OYO or the hotel, and 56% also complain about how the problem was handled.

OYO's own terms already promise the guest "alternate accommodation of comparable standards" and already forbid the owner to deny check-in "under any circumstances". Neither works at the moment that matters, because the owner never agrees to a specific booking at a specific price: OYO sets the price within a range and manages the inventory, and the owner app has no step to accept a booking. In 73% of denials where the guest reports a reason, the owner's "no" (property gone, not taking OYO bookings, price refused) existed before the guest set out. It surfaces at the desk because nobody asked earlier.

## 2. Goals and non-goals

**Goals**
1. Move the owner's "no" from the desk to hours before arrival, so that the guest is moved before travelling.
2. When a guest is refused at the desk anyway, give them a confirmed bed, or a clear next step with their money already on its way back, within 15 minutes.
3. Make an honest early "no" the owner's best option, and keep penalties for owners who confirmed and then refused, with evidence and an appeal.
4. Do it at roughly break-even cost (see `impact_model.xlsx`).

**Non-goals**
- Changing how OYO prices rooms or its revenue share (a later bet, see "Open questions").
- Room quality or listing accuracy after check-in.
- Couple and local-ID policy itself.
- Bookings made on other travel sites (pilot phase).
- Pay-at-hotel bookings (pilot phase; next after prepaid).

## 3. Users

| User | Situation | What they need |
|---|---|---|
| **Prepaid guest arriving the same evening** (primary) | Booked and paid in the app; often travelling for an exam, a hospital visit or work; may arrive late | To know before leaving that the room is really there, and if not, a confirmed alternative or their money back |
| **Guest refused at the desk** | Standing at the counter, sometimes at night, with luggage or family | A bed within minutes, no argument with the desk, no extra payment |
| **Hotel owner or manager** (partner) | Runs a small hotel; sells walk-ins; disputes some OYO prices; uses a phone, not a desktop | A simple way to say yes or no in time, no surprise deductions, and a fair hearing |
| **Support agent** | Handles the escalation | A clock, a budget, a list of nearby confirmed rooms, and authority to act |

## 4. User stories

1. As a prepaid guest, I want to see that the hotel has confirmed my room at my price before I leave, so that I don't travel to a room that isn't there.
2. As a prepaid guest whose hotel can't honour my booking, I want a confirmed room nearby or a full refund to my original payment method, offered before I travel.
3. As a guest refused at the desk, I want to tap one button and have OYO deal with the hotel, so that I don't have to argue or pay more.
4. As a guest refused at the desk with no room free nearby, I want to know straight away that my money is safe and what my options are.
5. As an owner, I want to confirm or decline tonight's bookings in one screen, so that I can say no honestly without being fined.
6. As an owner charged for a desk refusal, I want to see exactly why and what it cost, and to appeal if the guest was at fault.
7. As a support agent, I want a pre-approved budget and a list of nearby confirmed rooms, so that I can rebook without asking a manager.

## 5. MVP features and acceptance criteria

**F1. Owner confirmation (handshake)**
- Every prepaid booking appears in the partner app's "Confirm arrivals" list with booking value, room type, guest count and expected arrival.
- The deadline is 6 hours before check-in time; for bookings made less than 8 hours ahead, 30 minutes after booking.
- Reminder notification 2 hours before the deadline; automated phone call (keypad 1 = confirm, 2 = can't honour) 30 minutes before.
- "Can't honour" asks for one reason: sold out, room out of service, price too low, not taking OYO bookings, property closed.
- *Accepted when:* 95% of pilot bookings get an answer or reach the deadline with the status recorded; an answer is stored with a timestamp and shown to the guest within 1 minute.

**F2. Guest confirmation status and early move**
- The trip screen shows "Waiting", "Room confirmed by the hotel at [time]" or "The hotel can't hold your room".
- On "can't honour" or no answer by the deadline, the guest is offered within 10 minutes: up to four rooms within 3 km, already confirmed by those hotels, at the same or a better rating; OYO pays any price difference up to ₹400; or a full refund to the original payment method, started immediately.
- *Accepted when:* 90% of early moves are offered within 10 minutes of the trigger; a refund chosen here is initiated within 1 minute and never credited to the OYO wallet unless the guest chooses that.

**F3. Desk Rescue**
- "I'm at the hotel and was refused" button on the trip screen from 2 hours before check-in until noon the next day.
- Location check: the guest's phone within 200 m of the property; if location is off, the guest can still report and an agent verifies by call.
- Starts a visible 15-minute clock; OYO calls the hotel immediately (a call bridge, not the guest).
- If the hotel agrees: the guest sees a confirmation and a desk code, and "nothing more to pay".
- If not: book a confirmed room within 3 km (price difference paid by OYO), with a cab credit up to ₹250.
- If nothing comparable is free: refund to source starts at once, and the guest is offered a farther room with cab both ways, reimbursement of up to ₹600 above the original price against a bill, or continued search with an update every 10 minutes, plus a "call me" option.
- *Accepted when:* median time from report to a confirmed bed or a started refund ≤ 15 minutes, p90 ≤ 30 minutes in the pilot.

**F4. Fair-penalty ledger (thin version)**
- Declining by the deadline is free while the property's declines stay at or below 1 in 20 prepaid bookings in a rolling 30 days; above that, the listing's ranking is lowered and an account manager is notified.
- A desk refusal after confirming is charged at the actual cost of relocation (room difference + cab), as its own line on the payout statement, with the evidence: confirmation time, the guest's location at report time, call log, rebooking.
- Appeal within 48 hours with a reason and optional photo; the charge is paused until a person reviews it (within 3 working days).
- *Accepted when:* 100% of charges show their evidence; appeals are decided within 3 working days.

**F5. Listing pause**
- A listing is paused when it misses three confirmations in a row, or when a desk report says "closed" and the call bridge cannot reach the property.
- The owner can reactivate by confirming the property is operating; supply operations verifies before reactivation after a "closed" report.

## 6. Main flow

1. Guest books and pays. Booking appears in the owner's "Confirm arrivals".
2. Owner confirms → guest sees "Room confirmed" → normal stay.
3. Owner declines or misses the deadline → guest is offered a confirmed nearby room or a refund, before travelling → owner is not charged (within the decline limit).
4. Guest refused at the desk → Desk Rescue: call the hotel → if resolved, stay; if not, rebook nearby or refund plus options → if the owner had confirmed, the relocation is charged to the owner with evidence and an appeal.

The clickable version is `prototype/index.html`.

## 7. Edge cases

| Case | Behaviour |
|---|---|
| Owner confirms, then the room genuinely breaks (flood, power) | Owner can mark "room out of service" up to arrival; treated as a late decline (free once a month), not a desk refusal |
| Guest arrives after the hold time on the booking | Desk Rescue still available; if the hotel shows the guest arrived late with no message, the owner is not charged |
| Guest has no valid ID or breaks a house rule shown before booking | Owner appeals with the reason; if upheld, no charge to the owner and the refund follows the existing guest policy |
| Location services off or the phone is dead | Report by phone from the desk; agent verifies with the hotel |
| Multi-room group booking | Treated per room; the early move keeps the group together or offers a refund for the whole group |
| Guest reports a refusal but has already checked in | Hotel's check-in record and the call shut the case; repeated false reports flag the account |
| Hotel cannot be reached at all during the rescue | Treated as "closed": rebook or refund immediately; listing paused pending verification |
| Desk demands extra money but gives the room | Guest taps "the desk asks me to pay"; same call bridge; if the guest already paid, OYO refunds the extra and charges the owner |

## 8. Metrics

North star: share of prepaid bookings where the guest sleeps in a confirmed room at the price paid with nothing extra at the desk. Leading indicator: confirmation rate by deadline. Guardrails: extra declines, net cost per 1,000 bookings, owner churn, appeal-upheld rate, abuse rate, early-move rate. Full definitions and thresholds: `strategy/metrics.md`.

## 9. Rollout

| Phase | Scope | Exit criterion |
|---|---|---|
| 0. Dry run (2 weeks) | Handshake visible to owners in one city, no guest-facing changes, no penalties | 80% of bookings answered by the deadline; owner feedback from 20 calls |
| 1. Pilot (8 weeks + follow-up) | Randomised by property, ~570 properties per arm, prepaid only | Ship rules in `metrics.md` |
| 2. Prepaid, all cities | All prepaid bookings on OYO's own channels | Guardrails hold for 4 weeks |
| 3. Pay-at-hotel and OTA bookings | Handshake for pay-at-hotel; Desk Rescue for OTA bookings | Separate test |

## 10. Open questions

1. How does today's in-app help flow handle a denied check-in, and what is the internal target for resolving it? (Not visible publicly.)
2. What is OYO's current penalty schedule for denials, and how often is it applied? (The partner terms refer to "OYO Policies", which are not public.)
3. What share of India bookings are prepaid, and what is the real denial rate per booking? (Not disclosed; the two most important inputs to the model.)
4. Will small owners answer a phone-based handshake at 2 PM on a busy day? (Test in the dry run.)
5. Should a later version let owners set a minimum price, with OYO funding discounts below it, to remove the price dispute at its source?
6. Do OTA partners send bookings through the same confirmation path, or does the handshake need their cooperation?
