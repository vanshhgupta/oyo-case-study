# Problem: booked, but no room

## 1. The problem in one sentence, in a guest's words

> "A confirmed booking means nothing if guests are denied check-in upon arrival." (guest review, row 127, after waiting two to three hours at 3 AM to be told there was no room)

In a product manager's words: **an OYO guest with a confirmed, often prepaid booking reaches the property and is refused the room, and in most cases OYO neither rehouses them nor makes them whole quickly.**

## 2. Who it happens to

The reviews do not record who the guest is, so these segments come from what the reviews describe. Counts are reviews among the 600 denials where the situation is stated; most reviews state none, so the counts are floors, not shares.

| Segment | What the reviews describe | Why the denial hurts them most |
|---|---|---|
| **Late arrivals in an unfamiliar city** | Arriving at night or after midnight (56 reviews), often off a train or bus | Fewest alternatives, least safety, phone battery and cash running out |
| **Families and travellers with dependants** | Children, parents or elderly relatives mentioned | Cannot "just walk to the next hotel" |
| **Purpose-bound travellers** | Exams, interviews, hospital visits, weddings | The trip cannot move, so the guest pays whatever the desk asks |
| **Prepaid guests** | 242 reviews say they paid online or in advance | Their money is with OYO, so they have no leverage at the desk and a refund fight afterwards |
| **Couples and local-ID holders** | 15 reviews (3% of stated reasons) | Refused under a rule OYO says the guest was shown; no refund is owed |

**Serve first: prepaid guests arriving on the day of booking or the evening of travel.** They are the largest group the reviews can identify, OYO already holds their money (so it can act without asking them to pay again), and they are where OYO's own promise ("shall ensure... alternate accommodation") is clearest. Couples and local-ID holders are deliberately not first: their refusals follow a disclosed rule, and the fix there is disclosure (idea 7 in `solutions.md`), not rescue.

## 3. Why the owner turns the guest away

This is the core of the problem, because the fix depends on which cause dominates. Shares are of the 479 denial reviews where the guest reports the hotel's reason (`research/review_analysis.md`, section 4).

| Cause | Share of stated reasons | What the owner is thinking | Evidence from the owner side |
|---|---:|---|---|
| **Property gone**: closed, no longer with OYO, not at the pin | 25.7% | Nothing; the owner has left. OYO's listing is stale. | "Wants to leave OYO" and contract-exit complaints (5.5% of owner business reviews); guests quote desks saying "no tie-up with OYO" |
| **No record / won't take OYO bookings** | 24.4% | "This booking isn't real to me", or "I've stopped taking OYO guests" | Owners describe "fake" bookings and bookings checked in by OYO staff (17% of owner business reviews, 29% since 2023) |
| **Price dispute**: "can't give it at this price" | 23.0% | "OYO sold my room below what I'd accept, and I'll pay commission on top" | OYO sets the price under the partner terms; 22% of owner business reviews say the price is cut below what they want |
| **No room**: full, sold to someone else, overbooked | 22.1% | "A walk-in pays more and pays now", or a genuine double booking | Guests report rooms "sold to someone else"; owners describe slow inventory tools |
| ID, couple or house rule | 3.1% | Local rules, police pressure, the owner's own policy | OYO's guest policy allows these refusals and owes no refund |
| Owner says OYO owes it money | 1.7% | "I won't honour OYO bookings until I'm paid" | Payouts are the top owner complaint (31% of owner business reviews) |

**What the causes have in common.** The first three, 73% of stated reasons, are cases where the owner's "no" already existed before the guest set out: the property had left, the hotel had stopped honouring OYO bookings, or the hotel would not take the price OYO had sold at. The partner terms explain why this "no" stays hidden until the desk: OYO "shall have exclusive rights to determine the pricing" and manages "100% of the Contracted Rooms inventory"; owners can move the price only "within a specified range" set by OYO's Tariff Manager (`research/sources.md`, A9); and the owner's app offers no step to accept or decline a booking (`research/feature_audit.md`, section 2). This is not new: in 2019, OYO itself told Reuters that it tags properties serving their notice period "that may deny check-ins to customers as 'sold out'" (sources, C1). The owner never says yes to a specific booking at a specific price, so the first moment the owner can say no is when the guest is standing at the counter.

**The insight: check-in denial at OYO is a consent problem, not an arrival problem.** OYO makes the promise on the owner's behalf; the owner disagrees with it at the only point it controls. That is why the existing rules, which forbid denial and fine the owner afterwards, do not prevent it.

**How this differs from the Zomato study.** There, the bottleneck was evidence: nobody could prove whether an item was missing. Here, the facts are rarely in dispute (the guest is visibly at the desk and the hotel openly says no). The bottleneck is timing and incentive: when the owner's refusal surfaces, and what it costs the owner to refuse early versus late.

## 4. The journey: where each failure could have been caught, and by whom

| Step | What happens today | Failure that could be caught here | Who could catch it |
|---|---|---|---|
| 1. Listing | OYO lists the property at an OYO-set price | **Property gone**: stale listing still sells | OYO (listing health: no check-ins, failed calls, guest "closed" reports) |
| 2. Search and booking | Guest books; OYO confirms instantly | House rule not seen; price below owner's floor | OYO (show rules up front); OYO pricing |
| 3. Booking reaches the hotel | Appears in Co-OYO; no accept step | **No record / won't take OYO**: the hotel ignores or rejects it silently | The owner, *if asked* |
| 4. Hours before arrival | Nothing systematic; some guests call and are told "full" | **Price dispute, no room, won't take OYO**: the owner's decision exists but is unspoken | The owner, *if asked*; OYO acts on the answer |
| 5. At the desk | Guest refused; calls OYO; holds | Every cause surfaces here, at the worst time | OYO support, with a clock and a budget |
| 6. Afterwards | Refund in 7–14 days, wallet credit or nothing; owner penalty offset against payouts if applied | Guest churns; owner resents an opaque deduction | OYO (refund to source, visible penalty with evidence) |

Steps 3 and 4 are the gap. Nobody asks the owner, so nobody hears the "no".

## 5. Prevention or rescue: which matters more?

- **Prevention** means the guest never travels to a room that is not there. It can catch the 73% of stated causes whose "no" exists in advance, if the owner is asked and answering honestly is safe for the owner. It costs little per booking: a tap in the owner app, plus a rebooking made in daylight, before travel, with more inventory available.
- **Rescue** means that when a denial still happens, the guest has a bed within minutes. It is needed for the 22% "no room" cases that arise on the day, for owners who confirm and then refuse anyway, and for unreachable properties. It is expensive per case (night-time rebooking, cab, support time), but it is what the guest remembers.

**Prevention matters more for volume and cost; rescue matters more for trust.** Because OYO already promises rescue on paper and the reviews show it rarely happens (5% rebooked), the MVP needs both: prevention to shrink the problem to a size where rescue is affordable, and a rescue with a clock so that the promise becomes real for what is left.

## 6. What it costs OYO

Order-of-magnitude reasoning; the numbers are in `impact_model.xlsx`.

- **Refunds and relocation.** Under its own terms OYO owes a comparable room or a refund; in practice many denied guests describe no refund at all (25% "refund refused or money lost"), which is a liability rather than a saving.
- **Support load.** Denial reviews often describe long support interactions (holds of 20 minutes to two hours, repeated calls), and 56% of them complain about handling.
- **Lost repeat bookings.** A guest denied a prepaid room after a long journey is a likely lost customer. This is the largest cost in the model and the least certain.
- **Regulatory and legal exposure.** Consumer commissions have held OYO liable in at least twelve denied-check-in cases and rejected its "only a platform" defence; one ₹414 booking became a refund plus ₹5,000 compensation and ₹3,000 costs (sources, D4). The Central Consumer Protection Authority has said it plans to hold hotel aggregators responsible for unanswered complaints (D2). OYO's own terms already let it recover consumer-forum costs from operators, which shows it knows the exposure exists.
- **Supply.** Every unresolved denial is also a broken relationship with an owner. Fines without consent push owners towards leaving, which shows up next year as more "property gone" denials.

## 7. Out of scope

- **Room quality and listing mismatch** after check-in (15% and 10% of problems): a different journey stage with different fixes (audits, photo verification).
- **Refunds after a guest's own cancellation** (9.5%): a policy question about cancellation terms and OYO Money.
- **Changing OYO's pricing model.** The price dispute is a symptom of OYO setting prices. A price floor for owners is listed as a later idea, not part of the MVP, because it changes the core business model and needs data this study does not have.
- **Couple and local-ID policy itself**: a legal and social question; the study only covers showing the rule before booking.
- **Markets outside India**, although some reviews come from them.
