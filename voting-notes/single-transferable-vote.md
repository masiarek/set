# Single Transferable Vote (STV)

Source: [Single transferable vote (Wikipedia)](https://en.wikipedia.org/wiki/Single_transferable_vote) —
read 2026-08-01

Every number below is checked by [`code/stv/verify.py`](code/stv/verify.py) (standard library only,
`python3 verify.py`). The engine is exact-arithmetic (`fractions.Fraction`) and is **validated against the
article's own published round-by-round count before it is used for anything else** — surplus transfers
divide, and several findings below turn on small differences in how.

## What it's about

The first multi-winner method in these notes, and the one that makes every previous note a special case of
something bigger.

Each voter casts **one** transferable ranked vote in a district electing several members. Set a **quota** —
the number of votes that guarantees a seat. Elect anyone who reaches it. Their **surplus** above the quota
transfers to next preferences, because those votes weren't needed. When nobody reaches the quota, eliminate
the lowest and transfer their pile. Repeat until the seats are full.

The single idea underneath: **a vote should be neither wasted on a loser nor wasted on a landslide.** Every
other mechanism is bookkeeping in service of that.

Two things follow immediately, and both matter for the rest of these notes:

- **With one seat, STV is exactly instant-runoff voting.** The Droop quota for one seat is a majority. Same
  algorithm, same winner — verified on the [Lumen 75-ballot profile](lumen-75-ballot-four-winners.md) and on
  4,000 random profiles. So every IRV pathology in these notes is an STV pathology.
- **With more than one seat it stops behaving like IRV at all**, because the surplus transfer has no
  single-winner analogue. Same 75 ballots, three seats: STV elects Smith, Garcia and Lee — and **not
  Nguyen**, the candidate one-seat STV elects outright.

## Key takeaways

### The quota

**Droop** (near-universal): `floor(valid votes / (seats + 1)) + 1`. **Hare** (Thomas Hare's original):
`valid votes / seats`.

Droop is not a convention, it is the unique answer to a question. It is the **smallest quota that S+1
candidates cannot all reach** — so it can never elect too many — and one vote lower is not safe. Both halves
checked exhaustively for every electorate under 400 and every seat count under 8:

    (S+1) × q  >  V        safe: at most S can reach it
    (S+1) × (q−1)  ≤  V    minimal: a quota one lower is not safe

It generalises the majority: 50%+1 for one seat, 25%+1 for three, 10%+1 for nine. Hare is larger and
therefore a **harder** bar — on the article's 23-vote example Droop is 6 and Hare is 7.67. Counter-intuitively
this makes Hare *worse* for small parties hoping to win one seat, though it can protect a second-place party
in some configurations.

**The quota choice is not cosmetic**: Droop and Hare elect different sets in **15.4%** of 4,000 random
three-seat profiles.

### Transfers, and why "STV" is a family not a method

Two kinds. **Eliminations** are simple: the pile moves to each ballot's next usable preference. **Surpluses**
are where every real system differs, because you must decide *which* papers represent the surplus:

- **Whole-vote / random** (Cambridge MA, historically Cincinnati; Ireland's Dáil uses a deterministic
  "exact method" cousin) — move whole ballots, chosen so the transferred bundle mirrors the pile.
- **Basic Gregory** (Ireland's Senate, Northern Ireland) — fractional, but examines only the **last parcel**
  of papers the candidate received.
- **Weighted inclusive Gregory, WIGM** (Scottish local elections) — fractional over **all** papers held.
- **Meek's method** (1969, computer-only; John Muir Trust since 1998) — recomputes the quota as ballots
  exhaust. Conceptually the cleanest and the least used.

These are not equivalent. **WIGM and basic Gregory elect different sets in 11.7%** of 6,000 random
three-seat profiles — same ballots, same quota, different published rule. The article's own line is that STV
"can be considered a family of voting systems rather than a single system," and that number is what it costs.

### What STV guarantees

**Proportionality for solid coalitions (PSC).** If a group of voters ranks some set of candidates above all
others on every ballot ("solid" for them), and the group is worth *k* quotas, that set gets at least *k*
seats. Verified: 100 voters, 4 seats, quota 21, a 45-voter bloc solid for two candidates takes exactly 2
seats and the 55-voter remainder takes 2.

This is the formal core, and it is weaker than "proportional" in the everyday sense — it says nothing about
voters whose preferences don't form solid blocs.

### What it doesn't

- **Non-monotonic**, inherited whole from IRV: promoting a winner one place on one bloc's ballots can unseat
  them. Found by search.
- **Not summable** — a precinct cannot report one number per candidate. Eliminations and transfers need the
  whole ballot set in one place, which is why STV counts are centralised and slow.
- **Proportionality depends on district magnitude, not on STV.** Three-seat districts have a 25% threshold.
  Ireland's median district magnitude was five in 1923; successive governments cut it, which
  "directly benefits larger parties at the expense of smaller ones." An Irish parliamentary committee
  recommended a four-seat minimum in 2010. **Gerrymandering under STV is done by resizing districts, not
  redrawing them.**
- **By-elections are genuinely unsolved.** A multi-member seat falling vacant has no natural replacement
  rule, and the article lists six live approaches — countback from the original ballots (ACT, Tasmania,
  Malta, Cambridge MA), appointing the last-eliminated candidate, co-option, a single-winner IRV by-election
  (Ireland national, Scotland local — and non-proportional if a minority's seat is being refilled), party
  nomination (Ireland local), or a pre-filed successor list (European Parliament).

### How much do the transfers actually change?

The article makes a claim that is easy to miss and unusually self-critical: **outcomes under STV often do not
differ from what plain first-preference counting would have produced.** It cites Scottish local elections
2007–2022 and a 1930 Edmonton election where the STV winners were exactly the SNTV winners.

Checked: STV and **SNTV** (single non-transferable vote — first preferences only, top *S* win) elect the same
three of six candidates in **61.5%** of 6,000 random profiles. So the whole transfer apparatus changes the
result about two times in five. That is neither nothing nor the transformation the advocacy material
implies, and it is the honest frame for the ballot-complexity objection.

## 1. The article's own count, reproduced

23 guests choose 3 foods. Droop quota = ⌊23/4⌋ + 1 = **6**.

| Ballots | Ranking |
|---|---|
| 3 | Orange > Pear |
| 8 | Pear > Strawberry > Cake |
| 1 | Strawberry > Orange > Pear |
| 3 | Cake > Chocolate |
| 1 | Chocolate > Cake > Hamburger |
| 4 | Hamburger > Chicken |
| 3 | Chicken > Chocolate > Hamburger |

| Round | Orange | Pear | Straw | Cake | Choc | Burger | Chicken |
|---|---|---|---|---|---|---|---|
| 1 | 3 | **8 → elected** | 1 | 3 | 1 | 4 | 3 |
| 2 (Pear's surplus of 2 → Strawberry) | 3 | — | 3 | 3 | 1 | 4 | 3 |
| 3 (Chocolate eliminated → Cake) | 3 | — | 3 | 4 | out | 4 | 3 |
| 4 (Strawberry eliminated) | 4 | — | out | **6 → elected** | out | 4 | 3 |
| 5 (Chicken eliminated → Burger) | 4 | — | out | — | out | **7 → elected** | out |

Winners: **Pear, Cake, Hamburger.** Every cell above is asserted in the verifier.

Two details worth extracting:

- **Round 4 is decided by a tiebreak.** Orange, Strawberry and Chicken are all on 3. The article eliminates
  Strawberry because it had the fewest *first preferences* (1 vs 3 and 3) — a **backward tiebreak**, looking
  at an earlier round. Had Orange gone instead, Cake never reaches quota that round.
- **Strawberry's pile splits.** Its 3 votes are one original ballot (→ Orange, skipping the already-elected
  Pear) and two inherited from Pear (→ Cake). A transferred vote carries its own remaining preferences.

## 2. One seat is IRV — and ties are where implementations diverge

The Droop quota for one seat is ⌊V/2⌋+1, a bare majority, and the algorithm collapses to instant-runoff
voting. On the Lumen 75 ballots both elect **Nguyen**; across 4,000 random four-candidate profiles they never
disagree.

**Given the same tiebreak rule.** Swap in an alphabetical elimination tiebreak instead of the backward one
and they split on **15 of 4,000** — never because the algorithms differ, only because the tie rule does. On
one of those profiles two candidates sit on 38 votes each; backward tiebreak eliminates the one with fewer
first preferences and A wins, alphabetical eliminates A and C wins.

That is the third time in these notes that a tie convention has changed a result — after
[Ranked Robin's tie ladder](ranked-robin-results-explained.md) and the STAR tie-break bug I introduced and
then caught in [star-voting](star-voting.md). **Tie rules are not boilerplate**, and in real STV counts
(small districts, exhausted ballots, fractional values) exact ties are commoner than they look.

## 3. What proportionality buys, on ballots we already know

The [Lumen 75-ballot profile](lumen-75-ballot-four-winners.md) is already worked out elsewhere in these
notes: Smith wins plurality on 28 first preferences while being ranked **last on 47 of 75 ballots**; Garcia is
the Condorcet winner; IRV elects Nguyen.

Run it as a **three-seat STV** election. Quota = ⌊75/4⌋+1 = **19**.

| | |
|---|---|
| First preferences | Garcia 23, Smith 28, Nguyen 16, Lee 8 |
| Smith | 28 ≥ 19 → **elected**, surplus 9 → Lee |
| Garcia | 23 ≥ 19 → **elected**, surplus 4 split 20:3 → Lee, Nguyen |
| Lee | 8 + 9 + 3.48 = 20.48 ≥ 19 → **elected** |

Winners: **Smith, Garcia, Lee** — and **not Nguyen**, whom one-seat STV elects outright.

This is the clearest statement of what multi-winner does that single-winner can't, and it cuts both ways:

- Smith, the candidate a majority ranks *last*, gets a seat. Under STV that is correct behaviour — 28 of 75
  voters back Smith first, that clears a quota, and denying them representation is what proportionality
  exists to prevent. Under every single-winner note here, electing Smith would be a scandal.
- Nguyen, who wins the single-seat contest, gets nothing. Nguyen's support is broad-but-shallow: 16 first
  preferences, below quota, and the transfers that made Nguyen an IRV winner never happen because Lee and
  Garcia are never eliminated.

**"Who should win?" and "who should be represented?" are different questions**, and they have different
answers on the same ballots. That's the whole case for reading multi-winner methods separately.

## 4. Where it is actually used

Unlike every cardinal method in these notes, STV has a real and long governmental record.

| Where | Since | Notes |
|---|---|---|
| **Ireland** (Dáil) | 1922 | 39 constituencies, 3–5 seats, the reference implementation |
| **Malta** | — | Parliament and local councils |
| **Australia** (Senate) | 1948 | State-by-state; group voting tickets 1984–2016, abolished for distorting results |
| **Tasmania** (Hare-Clark) | 1896/1909 | First parliament in the world to use it |
| **Northern Ireland** | — | Assembly, basic Gregory |
| **Scotland** (local) | 2007 | WIGM |
| **New South Wales** (upper house) | 1991 | 21 seats in one statewide district |
| **Western Australia** | 2025 | 37 seats — the largest district magnitude in use |
| **ACT** | 1992 referendum | Countback for vacancies |
| **Cambridge, Massachusetts** | — | Cincinnati random-transfer method |
| **New York City** | 1937–1947 | Uniform quota, so council size *varied with turnout*: 26, 21, 26, 17, 23 seats |
| **Academy Awards** | — | Choosing nominees in each category |

- **Origin**: Thomas Wright Hill proposed transferable voting in **1819**; **Carl Andræ** put it in practice
  in Denmark in **1856**; **Thomas Hare** developed it independently in **1857** and gets the credit. **John
  Stuart Mill** championed it in *Considerations on Representative Government*; **Walter Bagehot** attacked
  it. **Catherine Helen Spence** added multi-member districts to Hare's at-large scheme, which is the form
  everyone now uses.
- **The 1979 General Medical Council switch** is the sharpest adoption anecdote in the article: under FPTP
  only white male GPs were elected; after switching to STV, women, immigrant GPs and specialists were.
- **Manipulating STV is NP-complete**, and requires knowing all the ballots — which is effectively only
  possible after counting. The Academy cites exactly this as its reason for using it.
- **Estonia dropped it after one election** (1990 → party-list in 1992) because the ballots didn't show
  candidates' party affiliation.

## 5. Real numbers from real elections

Worth recording because they are the strongest empirical case in the article:

- **Ireland 2020**, Dublin Bay South: **78% of votes cast were used to elect someone**, and 80% of first
  preferences went to the four parties that won seats. Two members were elected under quota, the lower by
  about 10%.
- **Quota varies by turnout, not by design**: Dublin Bay South's quota was 7,919 and Wexford's 12,513, on
  near-identical electorates per seat (19,250 vs 22,600) — turnout was 52% vs 67%.
- **Cambridge MA 2021**: 90% of voters helped elect someone; 65% saw their first choice elected; 95% saw at
  least one of their top three.

The counterweight, from the same article: in **Cavan–Monaghan 2020** the five seats went to candidates who
were already leading on first preferences, and the four least popular parties' candidates were eliminated
early — i.e. the transfers confirmed the first count rather than changing it. That is the 61.5% figure above,
in the wild.

## How it sits against the rest of these notes

- **vs. [IRV/Hare](hare-center-squeeze-examples.md)** — literally the same method with one seat. Every center
  squeeze, non-monotonicity and favorite-betrayal result in these notes applies. What multi-seat STV adds is
  that the *consequences* shrink: eliminating a middle candidate costs one seat of several, not the whole
  district.
- **vs. [approval](approval-voting.md) and [score](score-voting.md)** — their multi-winner forms (block
  approval, sequential proportional approval, reweighted range) reweight or exhaust ballots for the same
  reason STV transfers surpluses: to stop a majority sweeping every seat. STV does it with rankings and a
  quota; [reweighted range](score-voting.md) does it with scores and a divisor. The Academy uses **both** —
  STV for nominees, reweighted range for Visual Effects.
- **vs. Condorcet methods ([Ranked Robin](ranked-robin-results-explained.md))** — not comparable, and that's
  the point. Condorcet asks who should beat everyone; STV asks which *group* of winners represents the
  district. Section 3 is the same ballots giving different answers to those two questions.
- **vs. everything else here** — STV is the only method in these notes with a century of continuous national
  use. Whatever its formal failures, it is the one that has actually survived contact with voters.

## New ideas and terms

- **Quota** — the number of votes that guarantees a seat. **Droop** = ⌊V/(S+1)⌋+1, the smallest safe one;
  **Hare** = V/S, larger and harder; **Imperiali**, smaller and unsafe.
- **Surplus** — votes an elected candidate holds above the quota. Transferring them is the idea that
  distinguishes STV from every single-winner method.
- **Parcel** — a batch of ballots a candidate received in one transfer. Basic Gregory looks only at the
  **last** parcel; inclusive/weighted Gregory looks at all of them, and they disagree 11.7% of the time.
- **Transfer value** — the fraction a ballot is worth after contributing to an election. Why exact
  arithmetic matters.
- **Exhausted ballot** — no remaining usable preference; it stops transferring. Under optional preferential
  voting, enough exhaustion lets candidates win on partial quotas.
- **Proportionality for solid coalitions (PSC)** — *k* quotas' worth of voters solid for a set of candidates
  get *k* of them. STV's actual formal guarantee.
- **District magnitude** — seats per district. The real determinant of proportionality, and the lever
  governments use to tune STV without appearing to change it.
- **SNTV** — single non-transferable vote: STV's ballot without the ranking or the transfers. The baseline
  STV must beat, and doesn't 61.5% of the time.
- **Countback** — filling a vacancy by re-examining the original ballots rather than holding a by-election.
- **Vote leakage** — transfers crossing party lines, which STV permits and list PR does not; credited with
  reducing partisanship.
- **Backward tiebreak** — break a tie on current counts by looking at an earlier round's counts. Decides
  round 4 of the worked example.
- **Meek's method** — recompute the quota as ballots exhaust. The 1969 insight that computers make the
  conceptually simple version feasible.

## Links referenced in the article

- [Tideman, "The Single Transferable Vote", *Journal of Economic Perspectives* 9(1) (1995)](https://doi.org/10.1257/jep.9.1.27)
  — the PSC formalisation
- [Bartholdi & Orlin, "Single Transferable Vote Resists Strategic Voting"](https://courses.cs.duke.edu/fall06/cps296.2/stv_hard.pdf)
  — the NP-completeness result
- [Bardal, Brill, McCune & Peters, "Proportionality in Practice" (arXiv 2505.00520, 2025)](http://arxiv.org/abs/2505.00520)
  — the Scotland 2007–2022 STV-vs-SNTV finding
- [Gilmour, "Review of some aspects of STV for local elections in Wales" (2021)](https://www.researchgate.net/publication/350495590)
  — Gregory variants
- [O'Neill, "Comments on the STV Rules Proposed by British Columbia", *Voting matters* 22](https://www.votingmatters.org.uk/ISSUE22/I22P4.pdf)
  — which papers count as "relevant"
- [Cambridge STV rules (OpaVote)](https://www.opavote.com/methods/cambridge-stv-rules)
- [33rd Dáil election results (2020)](https://data.oireachtas.ie/ie/oireachtas/electoralProcess/electionResults/dail/2020/2020-05-01_33rd-dail-general-election-results_en.pdf)
- [Gosnell, "An Irish Free State Senate Election", *APSR* 20(1) (1926)](https://www.jstor.org/stable/pdf/1945103.pdf)
  — 19 seats, 76 candidates, counted by hand
- [FairVote: Proportional Representation in New York City, 1936–1947](https://fairvote.org/report/proportion_representation_in_new_york_city_1936_1947/)
- [Counting single transferable votes](https://en.wikipedia.org/wiki/Counting_single_transferable_votes) ·
  [Comparison of the Hare and Droop quotas](https://en.wikipedia.org/wiki/Comparison_of_the_Hare_and_Droop_quotas)
  · [Schulze STV](https://en.wikipedia.org/wiki/Schulze_STV) · [CPO-STV](https://en.wikipedia.org/wiki/CPO-STV)
  · [Method of equal shares](https://en.wikipedia.org/wiki/Method_of_equal_shares)

## Related local material

- [`code/stv/verify.py`](code/stv/verify.py) — the engine, validated against the published count, plus every
  claim above
- [lumen-75-ballot-four-winners](lumen-75-ballot-four-winners.md) — the 75 ballots reused in sections 2 and 3
- [hare-center-squeeze-examples](hare-center-squeeze-examples.md) — STV's single-seat behaviour, in detail
- [score-voting](score-voting.md) — reweighted range, the cardinal cousin of the surplus transfer
- [approval-voting](approval-voting.md) — sequential proportional approval, the same trick with approvals
- [whoops.md](whoops.md) — where the tiebreak finding is indexed
