# Sequentially Spent Score — a budget, and what happens when you don't spend it

Sources: [*Sequentially Spent Score*](https://electowiki.org/wiki/Sequentially_Spent_Score) and
[*Vote unitarity*](https://electowiki.org/wiki/Vote_unitarity) (electowiki), read 2026-08-02 via
`action=raw` — the rendered pages 403 non-browser clients. Plus
[BUG_sss_verbosity.md](https://github.com/masiarek/star-voting-library) in the vendored `starvote` fork and
[larryhastings/starvote#17](https://github.com/larryhastings/starvote/issues/17).

Verifier: [code/sss/verify.py](code/sss/verify.py) · output: [run-output.txt](code/sss/run-output.txt) —
7 checks, all pass. Pure Python, exact `Fraction` arithmetic throughout, which is what makes §3 possible.

> **Scope note.** Same declared point of view as the rest of electowiki
> ([approval-voting](approval-voting.md), [cardinal-voting-systems](cardinal-voting-systems.md)). This page
> is unusual among them: it publishes a reference implementation, states its own method's failures, and
> keeps the counterexample that killed an earlier variant. That makes it far more checkable than most, and
> checking it turns up two defects and one confirmed-in-full example.

## Why this note exists

[cardinal-voting-systems](cardinal-voting-systems.md) put SSS in a table — Vote Unitarity reweighting,
Hamilton party-list case — and noted it was the one method there with a local connection and no note. It is
also the method whose engine bug I found in [star-voting-library](https://github.com/masiarek/star-voting-library),
and that bug turns out to be the best available demonstration of what the method's central step actually does.

## 1. The method

Invented by Keith Edmonds, also called Sequentially Subtracted Score or Unitary Cardinal Voting. Score
ballots, usually 0–5, multi-winner.

**The metaphor is a budget.** Each voter starts with 5 stars. When a candidate you scored is elected, you
*spend* the stars you gave them — no more, because you can't be charged for support you didn't express, and
no less, because you got what you paid for. Your remaining influence is what's left in the budget.

```
quota = V / W                                       (ballots normalised to [0,1])
repeat W times:
    w = argmax over remaining candidates of  Σᵢ s[i][c] · weight[i]
    surplus_factor = max(total[w] / quota, 1)        ← "change" if w was over-funded
    spent[i]  = s[i][w] · weight[i] / surplus_factor
    weight[i] = weight[i] − spent[i]
```

Two things follow immediately, and they are the whole design:

- **You cannot be over-charged.** A voter who scored the winner 1 star spends 1 star. This is what
  [Allocated Score](cardinal-voting-systems.md) gets wrong by construction — there a voter who gave the
  winner 1 of 5 can be allocated entirely and lose *all* future influence.
- **You cannot be under-charged either.** RRV halves a full-score supporter's ballot and no more, so they
  keep influence they have already used. SSS takes it to zero.

The page is explicit that these are the two failure directions it was designed between, and it is right that
they are opposite: STV/Allocated Score over-remove, RRV under-removes.

### Vote Unitarity, formally

The axiom the method was reverse-engineered from. A rule satisfies it if there is a payment function
`p[i][c] ≥ 0` such that:

- **(VU1) Proportionate spending** — `p[i][c] ≤ s[i][c]`. Never charged more than you offered.
- **(VU2) Unitary transformation** — residual budget `b[i] = 1 − Σ p[i][c] ≥ 0` at every stage. Weight is
  neither created nor destroyed.

**Verified exact** over 3,000 random profiles (check 7): zero VU1 violations, zero VU2 violations, and the
`clip(…, 0, 1)` in the reference implementation **never binds** — spending is `s·w/surplus ≤ w` because
`s ≤ 1` and `surplus ≥ 1`, so the clip is defensive, not load-bearing.

Worth untangling one line on the wiki: VU2's remark that "no rule using multiplicative or other non-additive
reweighting can satisfy this condition" reads, at first, as ruling SSS out — SSS scales the whole ballot by
`weight`. It doesn't. The *budget* is tracked additively (`weight −= spent`); the ballot scaling is how the
budget is applied. Those are different objects and only the first is what VU2 quantifies over.

## 2. The finding: what the reweighting step is worth

The starvote bug — [issue #17](https://github.com/larryhastings/starvote/issues/17), fixed in the fork
2026-08-01, still open upstream at 2.1.6 — was that the entire ballot-allocation block in
`sequentially_spent_score()` sat inside `if options.verbosity:`. At `verbosity=0` **no stars were ever
spent**. A logging flag decided the winner.

The interesting part is not the defect. It's that the broken path is a coherent method, and naming it
explains SSS better than the wiki's four-step procedure does:

| | 21 ballots, 3 seats, 13-voter majority bloc + 8-voter minority bloc |
|---|---|
| SSS, reweighting on | **Alice, Ben, Dan** |
| SSS, reweighting removed | **Alice, Ben, Cara** |
| Bloc Score | **Alice, Ben, Cara** |

The minority bloc is 8/21 = 38% of the electorate, worth 1.14 Hare quotas, and owed a seat. With the
spending step, they get Dan. Without it, **SSS is exactly Bloc Score** — verified identical, check 1 — and
they get nothing.

Those are the precise winner sets the bug report records for `verbosity=0` and `verbosity>=1`. So the engine
was never mis-tabulating SSS; at `verbosity=0` it was running the *non-proportional* method from the same
family. Line up the taxonomy in [cardinal-voting-systems](cardinal-voting-systems.md) and the bug moved SSS
one row up the table, from the sequential-proportional block to the bloc block.

**The reweighting is not an implementation detail of SSS. It is the entire difference between SSS and the
method it is built to replace.** That is why a bug hiding it is invisible in single-winner tests and in any
election where the majority is entitled to every seat — you need a minority holding a quota before the two
methods disagree at all.

## 3. Two defects in the page

Both found by recomputing, both harmless to the conclusions they sit under, both the sort of thing that gets
copied forward.

### 3a. The participation example's printed totals are wrong

The page proves SSS fails participation with a 2-seat, max-10 example — clone candidates, one voter added.
**The failure is real and reproduces exactly** (check 2): 40 voters elect {A, A}; add one voter who scores
A above B, and the winner set becomes {A, B}. That voter's turnout cost their preferred candidate a seat.

The round-2 totals it prints to show the margin do not:

| | page prints | actually | B (page / actual) |
|---|---|---|---|
| Case 1 | A = 100.66 | **A = 101.60** | 99.33 / 99.34 |
| Case 2 | A = 98.36 | **A = 98.22** | 99.32 / 99.32 |

Both A figures drop the surviving contribution of the one-star voters to the second A clone. The
comparison — and therefore the finding — is unaffected in both cases: 101.60 > 99.34 still gives {A,A}, and
98.22 < 99.32 still gives {A,B}. But the printed intermediates are not what the stated procedure produces,
and they're the numbers a reader would reuse.

### 3b. The centrist-bias example is inherited from a variant the page says was abandoned

Under *Sorted Surplus Handling Variant*, the page motivates the variant with a toy election:

> 41% `A:5 B:2 C:0` · 20% `A:0 B:5 C:0` · 41% `A:0 B:2 C:5`, five winners — "where only Bs are elected."

Run it (check 4):

| Variant | Result | "only Bs"? |
|---|---|---|
| **Scaling** (the current method) | B, B, B, **A**, **C** | no — B takes 3 of 5 |
| **Capping** (abandoned, per the same page) | B, B, B, B, B | **yes** |

Entitlements are A 2.01, B 0.98, C 2.01. So the claim is a *capping-variant* result, kept in a section about
the standard surplus handling, on a page that elsewhere says capping "was abandoned when examples such as
the following were found."

The bias being illustrated is real either way — a 20% bloc taking 3 seats on a 0.98 entitlement is still
about **3× over-representation**, and the strategic incentive drawn from it (both wings truncate B to 0)
survives. It is 3× and not 5×, and the argument for Sorted Surplus is correspondingly weaker than the page
makes it look.

## 4. What checks out

**The capping variant's Justified Representation failure** — the page's reason for abandoning it —
reproduces exactly (check 3). 58 voters, 17 candidates, 6 seats:

- capping elects **{B1, B2, B3, B4, C1, C2}**, precisely as claimed
- the first 10 voters (17.2% of the electorate, more than one sixth) get nobody they scored
- scaling elects **A**, so the current method passes the case that killed the old one

This is a well-built counterexample and the page deserves credit for keeping it.

**The criteria table** spot-checks consistent over 4,000 random profiles (check 5): monotone ✓ (0
violations), IIA ✓ (0), participation ✗ (16 violations found, as claimed). Two caveats the table doesn't
carry:

- **IIA here is the multi-winner "remove a loser" form**, and it is a property of **absolute** scoring only —
  the same conditional that [cardinal-voting-systems](cardinal-voting-systems.md) §4a establishes for score
  and MJ. A page listing IIA as an unqualified Yes for a *cardinal* method is repeating the equivocation
  checked there.
- The participation failure is **structural, not incidental**: the page is right that all quota-based
  proportional systems fail it, STV and Allocated Score included.

**"The natural extension of the Hamilton method"** — confirmed, and this is the sharpest result here
(check 6). Over 2,000 random 3-party list profiles at 5 seats:

| SSS seat vector matches | agreement |
|---|---|
| **Hamilton** (largest remainders) | **2,000 / 2,000 — 100.0%** |
| Webster / Sainte-Laguë | 1,898 / 2,000 — 94.9% |
| D'Hondt | 1,409 / 2,000 — 70.5% |

That closes the party-list column of [cardinal-voting-systems](cardinal-voting-systems.md) §3 with a number
rather than a citation, and it means the Hamilton-side of the **Balinski–Young** trade — quota satisfied,
population monotonicity given up — is inherited by SSS wholesale. The apportionment material in
[math-in-society-lippman](math-in-society-lippman.md) is about the same objects, reached from the other end.

## 5. The variant zoo

The page lists seven. Worth knowing which are live:

- **Scaling vs. capping** — how a reduced-weight ballot supports remaining candidates. Scaling multiplies
  all scores by the remaining weight; capping instead truncates each score *at* the weight. Capping is more
  intuitive ("a voter at 50% weight who scored you 80% should give you 50%") and **fails Justified
  Representation**, which is why it was abandoned. Scaling is current.
- **Sorted Surplus Handling** — take the quota of score from the most enthusiastic supporters first, rather
  than pro rata, to blunt the centrist bias in §3b. Costs manual countability.
- **Sequentially Shrinking Quota** — dynamic quota that refunds prior winners when a later one is elected
  below quota. Limits **free riding** and makes SSS **priceable**. Computationally hard.
- **Vickrey Quota** — charge the smaller of the runner-up's total and a Hare quota, so a candidate is not
  over-charged for beating a weak field. Named for Vickrey auctions; non-retroactive, so cheaper than the
  dynamic quota.
- **Quota of Ballot Selection** — swap the utilitarian argmax for Sequential Monroe's selection rule.
- **Sequentially Spent STAR** — a runoff on the final seat.
- **Mixed Compensatory** — regional STAR winners spend score, then at-large SSS compensates. The cardinal
  analogue of MMP.

## 6. New ideas and terms

- **Vote unitarity** — vote weight as a conserved budget, spent proportionately, never created or destroyed.
  VU1 + VU2 above. Edmonds.
- **Proportionate spending** — the cost of electing a candidate never exceeds the support you gave them.
- **Scaling vs. capping** — the two ways to apply a reduced ballot weight to remaining candidates.
- **Justified Representation (JR)** — a cohesive group worth a quota must get *someone* they support. The
  axiom that killed the capping variant, and the standard multi-winner fairness floor from the
  computational-social-choice literature.
- **Priceability** — a winner set is priceable if voters' budgets can be assigned to winners consistently at
  a common price. Sequentially Shrinking Quota gets it; plain SSS doesn't.
- **Vickrey quota** — the smaller of a Hare quota and the runner-up's total score.
- **Surplus factor / "change"** — `max(total/quota, 1)`; the divisor returning over-payment to voters.
- **Hare score quota** — `voters × maxscore / seats`. The starvote engine's name for the same thing.
- **Sequentially Subtracted Score / Unitary Cardinal Voting** — SSS's other names.

## Links referenced

- [*Sequentially Spent Score*](https://electowiki.org/wiki/Sequentially_Spent_Score) ·
  [*Vote unitarity*](https://electowiki.org/wiki/Vote_unitarity) ·
  [*Allocated Score*](https://electowiki.org/wiki/Allocated_Score)
- [larryhastings/starvote#17](https://github.com/larryhastings/starvote/issues/17) — the verbosity bug,
  open upstream at 2.1.6; fixed in the [star-voting-library](https://github.com/masiarek/star-voting-library)
  fork with `tests/test_verbosity_invariance.py` as the regression guard
- [Market-based voting (rangevoting.org)](https://rangevoting.org/MarketBasedVoting.html) — the
  score-as-money analogy the page draws on

## Related local material

- [cardinal-voting-systems](cardinal-voting-systems.md) — the taxonomy this fills in; §3's party-list column
  is settled here at 100% Hamilton agreement, and §4a's IIA caveat applies to this page's criteria table
- [score-voting](score-voting.md) — the single-winner selection rule SSS runs each round
- [single-transferable-vote](single-transferable-vote.md) — the ranked answer to the same problem. Quota and
  surplus transfer against quota and spending; STV over-removes influence, which is the failure Vote
  Unitarity was written against
- [star-voting](star-voting.md) — Sequentially Spent STAR bolts STAR's runoff onto the last seat
- [math-in-society-lippman](math-in-society-lippman.md) — Hamilton, quota and Balinski–Young from the
  apportionment side; SSS inherits that whole trade
- [whoops](whoops.md) — both defects in §3 are indexed there
- [glossary.md](glossary.md) — §6's terms are defined there
