# Metrics, experiment and risks

## 1. North-star metric

**Kept promises: the share of prepaid bookings where the guest sleeps in a confirmed room at the price they paid, without paying anything extra at the desk.** The room can be at the booked hotel or one OYO arranged before the stay.

**Why this one.** It is the promise the product exists to keep, in the guest's terms. It rises when a denial is prevented, when a denied guest is rescued, and when an extra-charge demand is stopped, so it rewards all three parts of RoomReady. It cannot be gamed by refunding people: a refunded guest has no room and counts as a broken promise.

**Its weakness.** It is close to 100% and moves in hundredths of a percent, so it is a poor day-to-day steering metric. It can be inflated by moving guests to other hotels too freely (a move counts as kept), which is why the early-move rate is a guardrail. And "paid nothing extra" needs a post-stay question or a desk report to measure, so it is partly self-reported.

## 2. Fast leading indicator

**Confirmation rate by deadline**: the share of prepaid bookings the owner confirms by the handshake deadline (6 hours before check-in). It moves within a day of launch, it is fully measured in the owner app, and it predicts the north star: a booking confirmed early is the cheapest kept promise.

## 3. Supporting metrics

| Metric | Why it matters |
|---|---|
| Desk denials per 1,000 prepaid bookings | The thing being prevented |
| Median and 90th-percentile minutes from desk report to a confirmed bed | The rescue clock (target: median ≤ 15, p90 ≤ 30) |
| Share of desk reports resolved within 15 minutes | Whether the promise on the screen is true |
| Guests moved before travel, and share who accept the move | Prevention working, and whether the offered rooms are good enough |
| Refund-to-source time for denied guests | The money half of the promise |
| 90-day repeat booking rate of guests who had a denial or an early move | The long-run value in the impact model |
| Support contacts per denial | Cost and guest effort |

## 4. Guardrails

| Guardrail | Limit for the pilot | Why |
|---|---|---|
| **Extra declines**: decline rate in treatment minus the denial rate in control | ≤ 0.15% of bookings (base case); kill above 0.3% | The biggest risk in the impact model: a free "no" gets used |
| **Net cost per 1,000 prepaid bookings** (top-ups + rescues − recoveries) | Within the base case in `impact_model.xlsx` | Keeps it a break-even project, not a subsidy |
| **Owner churn**: properties leaving per month | Not more than 0.5 percentage points above control | A fix that drives supply away is a failure |
| **Owner disputes**: appeals per 1,000 bookings, and share of appeals upheld | Appeals upheld ≤ 20% | High upheld appeals mean the evidence is wrong and penalties are unfair |
| **Abuse**: desk reports per 1,000 prepaid bookings, and share where the location check fails or the hotel shows the guest was checked in | Reports ≤ 2× control's denial contacts; failed checks ≤ 10% | Stops the rescue becoming a free upgrade |
| **Early-move rate** | ≤ 1.5% of bookings | Moves are cheap but not free, and too many make the north star meaningless |

## 5. Experiment

**Unit of randomisation: the property.** The handshake and the penalty rules change what the owner does, so one hotel cannot run two rule sets for different guests without confusion and spillover. Randomising by guest or booking would contaminate both arms. Properties are stratified by city and by their past denial-related complaints so that the arms are balanced.

**Control:** today's flow (no handshake; existing support; existing penalties). **Treatment:** RoomReady for prepaid bookings (handshake, Desk Rescue, fair-penalty ledger, listing pause).

**Duration:** 8 weeks of bookings, with a further 12 weeks of follow-up for the 90-day repeat rate. Eight weeks covers weekdays, weekends and at least one holiday peak, when the "full" cause is most likely.

**Sample size (back of the envelope)**

| Input | Value | Source |
|---|---|---|
| Desk denial rate in control | 0.4% of prepaid bookings | Assumption (impact model base case) |
| Smallest effect worth detecting | 30% fewer desk denials (0.4% → 0.28%) | Judgement: below this, the base case loses money |
| Significance and power | 5% two-sided, 80% | Convention |
| Bookings per arm if bookings were independent | (1.96 + 0.84)² × (0.004 × 0.996 + 0.0028 × 0.9972) ÷ 0.0012² ≈ **36,900** | Two-proportion formula |
| Prepaid bookings per property in 8 weeks | ≈ 180 | 35.1 million bookings a year ÷ 14,937 India hotels × 8/52 × 50% assumed prepaid |
| Intra-property correlation | 0.01 | Assumption |
| Design effect | 1 + (180 − 1) × 0.01 ≈ 2.8 | Cluster adjustment |
| **Bookings per arm** | ≈ **103,000** | 36,900 × 2.8 |
| **Properties per arm** | ≈ **570** | 103,000 ÷ 180 |

About 1,150 properties in total, roughly 8% of OYO's India hotels: three or four large cities would be enough.

**Decision rules**

| Result | Decision |
|---|---|
| Desk denials fall by at least 25% (significant), median minutes to a bed ≤ 15, extra declines ≤ 0.15% of bookings, net cost within the base case, owner churn within the guardrail | **Ship** to all prepaid bookings, then test pay-at-hotel |
| Denials fall, but extra declines are 0.15–0.3% or cost is above the base case | **Iterate**: tighten the free-decline limit, move the deadline closer to arrival, or limit top-ups, and rerun for 4 weeks |
| Extra declines above 0.3% of bookings, owner churn up by more than 0.5 points a month, or desk denials fall by less than 10% | **Kill** the handshake; keep Desk Rescue only if its clock is met |

## 6. Main risks

| Risk | Mitigation |
|---|---|
| Owners confirm everything without looking ("rubber-stamping"), then refuse at the desk anyway | The ledger charges a confirmed-then-refused booking; the leading indicator is watched alongside desk denials, not alone |
| Owners use the free "no" to keep rooms for walk-ins | Free declines capped at 1 in 20 bookings; above that, ranking falls; measured as the extra-decline guardrail |
| Guests abuse the desk button for an upgrade | Location check, a call to the hotel, and the hotel's check-in record; repeat reporters reviewed by an agent |
| No comparable room nearby at night (the hard case) | Refund to source starts at once; farther room with cab both ways; reimbursement up to a cap; honest screen instead of a spinner |
| Small owners do not use the app daily | An automated phone call with keypad answer as the fallback channel; the deadline reminder 2 hours ahead |
| Penalties feel like one more opaque deduction | Each charge is its own line with the evidence, and a 48-hour appeal reviewed by a person |
| Bookings from other travel sites (OTAs) are outside the flow | Pilot covers OYO's own channels first; OTA bookings follow if the pilot ships |
| The base-case economics are thin | The pilot measures the two inputs that decide them (extra declines and early-move acceptance) before any wider launch |
