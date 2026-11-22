# Solutions: from nine ideas to one MVP

The problem (`problem.md`): the owner's "no" usually exists before the guest travels, but nobody asks for it, so it surfaces at the desk; and when it does, OYO rarely rehouses the guest (5% in the reviews). The ideas below are organised by where in the journey they act.

## 1. The ideas

| # | Idea | Journey step | Cause it targets |
|---|---|---|---|
| 1 | **Pre-arrival confirmation ("RoomReady handshake").** Hours before check-in, the owner confirms each booking at its price with one tap in the owner app. If the owner declines or does not answer, OYO moves the guest to a confirmed room nearby, or refunds to source, before the guest travels. | 3–4 | Gone, won't take OYO, price dispute, full (whenever known in advance) |
| 2 | **Desk Rescue with a clock.** A "Refused at the desk" button that checks the guest's location, calls the hotel, and within 15 minutes either confirms the room or books a nearby one, with the cab paid and the refund to source started. | 5 | Every cause that still reaches the desk |
| 3 | **Fair-penalty ledger.** Declining early is free (up to a limit). Refusing at the desk after confirming makes the owner pay the guest's relocation, shown line by line with the evidence (confirmation time, guest location, call log) and a 48-hour appeal. | 4–6 | The owner's reason to say no late instead of early |
| 4 | **Stale-listing sweep.** Pause listings automatically when signals show the property has gone: missed confirmations, no check-ins, guest "closed" reports, failed calls. | 1 | Gone (26% of stated reasons) |
| 5 | **Owner price floor.** Owners set a minimum nightly price; any OYO discount below it is funded by OYO, not the owner. | 2 | Price dispute (23%) |
| 6 | **"Sold at the desk" inventory button.** Owners mark a room sold to a walk-in in real time, so OYO stops selling it. | 3 | No room (22%) |
| 7 | **House rules before payment.** Couple and local-ID rules shown on the payment screen, with a tick to acknowledge. | 2 | ID, couple, house rule (3%) |
| 8 | **Generous compensation.** Every denied guest gets double their money back or a large credit. | 6 | None directly; pays for the failure |
| 9 | **Zero tolerance.** Delist any property after one confirmed denial. | 6 | All, through deterrence |

## 2. Scoring

RICE = Reach × Impact × Confidence ÷ Effort. **Reach** is the share of denials the idea can affect (from the reason split in `research/review_analysis.md`). **Impact**: 3 = prevents the denial, 2 = gives the guest a bed or changes owner behaviour, 1 = softens the outcome. **Confidence** is how sure I am the idea works as described. **Effort** is rough person-months for a first version.

| # | Idea | Reach | Impact | Confidence | Effort | RICE | Reasoning behind the scores |
|---|---|---:|---:|---:|---:|---:|---|
| 9 | Zero tolerance | 100% | 1 | 30% | 0.5 | 60 | Cheap to switch on and touches every denial, but the partner terms already forbid denial and allow suspension, and reviews show it does not stop it; deterrence mostly pushes the "no" further out of sight. |
| 8 | Generous compensation | 100% | 1 | 50% | 1 | 50 | Easy to ship; does not put anyone in a bed at 11 PM; invites false claims. |
| 2 | Desk Rescue | 100% | 2 | 70% | 3 | 47 | Every desk denial can use it; Booking.com shows a same-day clock is workable at scale; needs supply search, a call bridge, a cab credit. |
| 4 | Stale-listing sweep | 26% | 3 | 80% | 1.5 | 42 | Narrow but certain: a closed hotel should not be bookable. Mostly rules on signals OYO already has. |
| 3 | Fair-penalty ledger | 60% | 2 | 50% | 2 | 30 | Can only apply where the owner had a chance to say no, so reach equals the handshake's; confidence is moderate because owners distrust deductions. |
| 1 | RoomReady handshake | 60% | 3 | 60% | 4 | 27 | Reach capped below the 73% of pre-decided causes because some owners will confirm and still refuse; needs owner-app, notification and rebooking work. |
| 7 | Rules before payment | 3% | 1 | 80% | 0.5 | 5 | Cheap but tiny reach in this data. |
| 5 | Owner price floor | 23% | 3 | 40% | 6 | 5 | Attacks a root cause, but changes how OYO prices and funds discounts; low confidence without pricing data. |
| 6 | "Sold at desk" button | 22% | 1.5 | 40% | 4 | 3 | Owners would have to choose to use it at the moment they are selling to a walk-in; partly covered by idea 1. |

## 3. Where I overrode the scores, and why

RICE does not see cost, dependencies or guardrails. Four overrides:

1. **Ideas 9 and 8 score highest, and both are rejected.** They fail the guardrails, not the arithmetic. Zero tolerance fails the owner-side guardrail (see the second objection below). Generous compensation fails the cost guardrail: in the costing, a ₹300 goodwill credit to every moved or rescued guest is a large part of why the first design loses ₹6.9 crore a year (`impact_model.xlsx`, sheet "Design v1 vs v2").
2. **The handshake (1) goes in although it scores below Desk Rescue (2).** It is a dependency for idea 3, and the cost model shows that rescue alone is the expensive way to fix this: each desk rescue costs about ₹400 at night, while an early move costs about ₹120 in daylight. The handshake is what makes the rescue affordable.
3. **The fair-penalty ledger (3) goes in as a thin version.** Without it, the handshake gives owners a free "no" and nothing else, and the costing shows that extra owner declines are the single biggest risk to the economics. The ledger is what makes an early, honest "no" the best option for an owner who cannot honour a booking.
4. **The stale-listing sweep (4) goes in, folded into the handshake.** A missed confirmation is the strongest signal that a property has gone, so the sweep is mostly a rule on handshake data.

## 4. The MVP: RoomReady

**Ideas 1 + 2 + 3 (thin) + 4, for prepaid bookings first.**

- **Ask before the guest travels.** The owner confirms each prepaid booking by 6 hours before check-in (within 30 minutes for same-day bookings). A reminder goes out 2 hours before the deadline, then an automated call.
- **Act on the answer.** "Can't honour" or no answer means the guest is offered, before travelling, a confirmed room within 3 km at the same or a better rating, with OYO paying any difference up to ₹400, or a refund to source started immediately.
- **Rescue with a clock.** At the desk, a location-checked report starts a 15-minute clock: call the hotel; if it still refuses, book a nearby room (difference paid, cab up to ₹250); if nothing comparable is free, start the refund at once and offer the next-best options (a farther room with cab both ways, or reimbursement up to ₹600 above the original price).
- **Make honesty the owner's best option.** Declining early is free up to 1 in 20 bookings a month; above that, the listing ranks lower and an account manager calls. Refusing at the desk after confirming costs the owner the actual relocation (as the partner terms already say), shown with evidence and open to appeal.
- **Close dead listings.** Three missed confirmations in a row, or a "closed" desk report confirmed by a call, pause the listing.

Why prepaid first: OYO already holds the money (so a move or refund needs nothing from the guest), and OYO's own terms already promise these guests "alternate accommodation of comparable standards".

## 5. How costing changed the design

The first version (v1) was generous: no limit on free declines, OYO paying any price difference without a cap, a ₹300 goodwill credit to every moved or rescued guest, and OYO absorbing rescue costs so as not to upset owners. Costed in the base case, **v1 loses ₹6.9 crore a year**, with the benefit unchanged. Most of the extra cost comes from owners declining bookings they would otherwise have honoured (a free "no" is used), then the goodwill credits.

v2, the MVP above, changes four things: a cap on top-ups, credit only by agent judgement, owner recovery when the owner had confirmed, and a decline limit tied to ranking. **v2 is roughly break-even in the base case (+₹0.1 crore a year), loses ₹5.4 crore in the pessimistic case and gains ₹8.4 crore in the optimistic case.** It is a trust and promise-keeping project that roughly pays for itself, not a profit project, and the case where it loses money is driven mainly by extra owner declines. That is why the pilot measures the decline rate before anything else (`metrics.md`).

## 6. Rejected ideas, one line each

- **5. Owner price floor:** the strongest long-term fix for price disputes, but it changes OYO's pricing model and needs data this study does not have; it is the first item for "what next".
- **6. "Sold at desk" button:** relies on the owner volunteering information at the moment it is selling the room to someone else; the handshake asks at a better moment.
- **7. Rules before payment:** worth doing as a small fix outside this project, but 3% of stated causes cannot justify the project's focus.
- **8. Generous compensation:** pays for the failure instead of fixing it, costs more than the benefit, and invites false claims.
- **9. Zero tolerance:** already in the contract, does not work in practice, and pushes supply away.

## 7. Two objections, answered properly

**"Why not just compensate every guest generously?"**
Because money after the fact does not solve the moment that matters. A guest at the counter at 11 PM needs a bed, not a credit next week. Compensation is also the most expensive way to respond: in the base case, a ₹300 credit to every affected guest plus uncapped top-ups helps turn a break-even project into a ₹6.9 crore loss. And it invites gaming: any guest could claim a denial. RoomReady spends the money on the rescue itself (the room difference and the cab), verifies the claim by the guest's location and a call to the hotel, and keeps discretionary credit for agents to use when the rescue fails.

**"Why not simply penalise or delist every owner who denies a check-in?"**
Because OYO already does, on paper. The partner terms say the owner "shall not deny check-in to any OYO customer under any circumstances", make the owner bear relocation costs, allow penalties offset against payouts, and list denial as a reason to suspend the listing. The reviews show this has not prevented denials. Most denials come from owners who disagree with the booking (the price, the channel, or the relationship itself), and a penalty they cannot see coming, deducted from a payout they already find opaque, gives them a reason to leave rather than comply. Owners leaving shows up later as more "property gone" denials, the largest single cause. Penalties work only when the owner had a fair chance to say no; the handshake gives that chance, and the ledger keeps the penalty for owners who said yes and then broke their word.
