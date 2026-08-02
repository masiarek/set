# Agreeable Societies

Source: Deborah E. Berg, Serguei Norine, Francis Edward Su, Robin Thomas & Paul Wollan,
["Voting in agreeable societies"](http://arxiv.org/abs/0811.3245), *American Mathematical Monthly*
**117** (2010) 27–39 (arXiv:0811.3245v1, 20 Nov 2008; MSC 52A35, 91B12) — read 2026-08-01.

Second source: Craig Burkhart, *Approval Voting Theory with Multiple Levels of Approval*, Harvey Mudd
College senior thesis, May 2012 (advisor Francis Su, reader Ann Trenk),
[HMC Senior Theses 26](https://scholarship.claremont.edu/hmc_theses/26).

Every claim below is checked by [`code/agreeable-societies/verify.py`](code/agreeable-societies/verify.py)
(no dependencies, `python3 verify.py`, ~10 s).

## What it's about

Every other note here asks **who wins**. This one never asks it. There is no tabulation rule in the paper,
no ballot, no strategy, and no criterion — only voters, a political spectrum, and the sets of positions each
voter would accept. The question is:

> if small groups of voters agree *locally*, how much agreement is forced *globally*?

That is a Helly-type question from convex geometry, and the answer is a family of guarantees of the form
"some platform is acceptable to at least this fraction of the electorate." Su's group came at approval
voting from discrete geometry rather than social choice, which is why none of the names in
[approval-voting](approval-voting.md) — Brams, Fishburn, Myerson, Laslier, Saari — appear in it, and why
none of its theorems can settle anything those names argue about.

Read it as a note about **electorates**, not about methods. It is the only note here whose results survive
unchanged no matter which voting method you then run.

> "My idea of an agreeable person is a person who agrees with me." — Disraeli, the paper's epigraph

## The model

- A **society** is a triple (X, V, 𝒜): a **spectrum** X, a finite set of **voters** V, and each voter's
  **approval set** A_v ⊆ X. Each element of X is a **platform**.
- A **linear society** is one where X is a closed subset of ℝ and each approval set is X ∩ I for a closed
  bounded interval I (possibly empty). The intuition is Coombs' *J*-scale: a voter has an ideal point and
  accepts anything near enough.
- **Agreement number** a(p) = how many voters approve platform p; a(S) = max over p. **Agreement
  proportion** = a(S)/n.
- **(k, m)-agreeable**: the society has ≥ m voters, and among *every* m voters some k of them share a
  platform. So **(2,2)-agreeable = super-agreeable** (every pair agrees somewhere) and **(2,3)-agreeable =
  agreeable** (of any three voters, two agree).

Two modelling points that matter more than they look:

- **X can be all of ℝ (every conceivable platform) or just the finitely many positions actual candidates
  adopted.** These give different answers — see the caveat below.
- **None of the linear results use the metric**, only the ordinal structure of ℝ. There is no distance, no
  utility, and no notion of "how far" a voter is from a platform. That makes this model *weaker* than the
  spatial models in [ranked-robin-vse-run](ranked-robin-vse-run.md), and the results correspondingly more
  robust.

## The results

| # | Statement | Hypothesis |
|---|---|---|
| Thm 3 | **Helly**: n > d convex sets in ℝᵈ, every d+1 with a common point ⟹ all have a common point | — |
| Cor 4 | A (d+1, d+1)-agreeable ℝᵈ-convex society has a platform approved by **everyone** | spectrum must be all of ℝᵈ |
| **Thm 5** | **Super-Agreeable Linear Society Theorem**: pairwise agreement ⟹ a platform approved by **everyone** | linear |
| Thm 1 | An **agreeable** linear society has a platform approved by **at least half** | linear |
| **Thm 2** | **Agreeable Linear Society Theorem**: a (k,m)-agreeable linear society of n voters has a platform approved by **≥ n(k−1)/(m−1)** | linear |
| Fact 1 | clique number of the agreement graph **=** agreement number | linear (also d-box) |
| Fact 2 | the agreement graph of a linear society **is an interval graph** | linear |
| Thm 6 | interval graphs are **perfect** (χ = ω on every induced subgraph) | — |
| Lem 7 | m−1 = (k−1)q + ρ, 0 ≤ ρ ≤ k−2; every m vertices contain a k-clique ⟹ χ ≥ (n−ρ)/q | any graph |
| **Thm 8** | ω(G) ≥ **⌈(n−ρ)/q⌉**, and this is best possible; hence agreement proportion ≥ (k−1)/(m−1) | linear |
| Thm 9 | **Fractional Helly** (Kalai): α of the (d+1)-subsets intersect ⟹ some point in βn sets, β = 1−(1−α)^{1/(d+1)} | — |
| Thm 10 | (k,m)-agreeable ℝᵈ-convex ⟹ agreement proportion ≥ 1 − (1 − C(k,d+1)/C(m,d+1))^{1/(d+1)} | m > d |
| Thm 11 | every m vertices contain a k-clique ⟹ ω(G) ≥ **n−m+k**, best possible | **k ≤ m ≤ 2k−2** |
| Thm 13 | a (k,m)-agreeable **d-box** society has agreement number ≥ n−m+k, best possible | k ≤ m ≤ 2k−2 |

**The engine is Theorem 8, and it is a four-step chain**: (k,m)-agreeability caps how many voters can share
a colour (Lemma 7) ⟹ the graph needs many colours ⟹ interval graphs are perfect, so χ collapses to ω
(Facts 2 + Theorem 6) ⟹ Fact 1 turns ω back into an agreement number. Theorem 2 — the one Burkhart cites
and the one that reads like the headline — is a *corollary* of Theorem 8, and a lossy one: **Theorem 8's
⌈(n−ρ)/q⌉ is strictly stronger than n(k−1)/(m−1) in 80% of the 8,779 (society, k, m) cases tested.**

### Checked here

- **Fact 1** on 4,000 random linear societies, with the clique number computed independently by
  Bron–Kerbosch rather than read off the intervals.
- **Theorem 5** on 3,000 pairwise-agreeing societies; **Theorem 1** on 3,000 agreeable ones, where **350 hit
  the n/2 bound exactly** — "half" is not slack.
- **Theorem 8 is best possible**, by building the construction from its proof: q disjoint intervals cycled,
  then ρ isolated ones. Brute-forced over all C(9,6) = 84 subsets for (k,m) = (3,6), and their **Figure 7
  reproduced** — a (4,15)-agreeable society on n = 21 with q = 4, ρ = 2 and clique number exactly 5.
- **Theorem 11 exhaustively**: all 2¹⁵ graphs on 6 vertices. Exactly **172** satisfy "every 4 vertices
  contain a triangle", and every one has ω ≥ n−m+k = 5.
- **Its hypothesis m ≤ 2k−2 is load-bearing**: two disjoint triangles satisfy the (3,5) condition with
  clique number 3 < n−m+k = 4.
- **The restaurant example**: 14 restaurants on a boulevard, everyone eats at the 5 nearest. Both halves of
  their argument check out — the pigeonhole one (3 × 5 > 14) and the interval one — and over 20,000 random
  resident groups the lowest share ever sharing a restaurant was exactly 0.50.
- **Their Figure 8 reconstructed**: five explicit axis-parallel boxes whose agreement graph is exactly C₅,
  with clique number 2 and chromatic number 3. Box agreement graphs are not perfect, though Fact 1 survives.

## Four caveats, and the fourth is the interesting one

**1. No candidates, no winner, no method.** "A platform approved by ≥ n(k−1)/(m−1) voters exists" is not
"that candidate wins" — nothing is being counted or compared. Every question in
[approval-voting](approval-voting.md) (cutoffs, bullet voting, IIA, Condorcet) is un-askable in this model.

**2. Platforms are not candidates, and the gap is real.** Their Figures 2 → 3 make the point: restrict the
spectrum from all of ℝ to the positions actual candidates took, and agreeability can collapse. Reproduced
locally with an instance of my own: the society

    [(13,19), (8,11), (8,14), (3,9), (17,21), (5,11)]

is **(2,3)-agreeable on ℝ, but with candidates only at {2, 7, 10} the best it manages is (2,5)** — the
guarantee drops from "half the voters" to a quarter. An agreeable electorate does not imply an agreeable
*ballot*. The paper flags this for d > 1 and calls transferring platform results to candidate sets
"tricky"; at d = 1 it is not a theorem-breaker but it is a real weakening.

**3. Dimension one is doing all the work.** In ℝ²: **Fact 1 fails** (three segments forming a triangle
agree pairwise with no common point — verified), agreement graphs **stop being perfect** (the C₅ boxes), and
Theorem 10's general bound is far worse than the linear one — at d = 1 it never beats Theorem 8, worst case
(k,m) = (9,12) giving **0.326 against 0.727**. Everything strong here is one-dimensional.

**4. (k, m) is an assumption about the electorate that nobody can observe.** The paper says so itself, in
the Discussion: these parameters can be measured "only by surveying large numbers of people", and a society
debating outlawing murder is more agreeable than the same society debating tax reform. That is exactly the
shape of the move flagged in [approval-voting](approval-voting.md) for **dichotomous preferences** — a
strong, correct theorem on a restricted domain, where the whole empirical question is whether real
electorates are in the domain. The difference is that Berg et al. name the problem and put it in their open
questions; the advocacy pages audited in that note do not.

## Burkhart's two-level extension (2012)

The thesis adds a middle level. A voter is four points L < l < r < R: **approval region** [l, r] worth 1, a
**maybe region** [L,l) ∪ (r,R] worth ½, and the union is the **interest region**. The platform value is
V(p) = Σ_v V_v(p) — which makes it, read as a ballot, a **three-level score total**, the rung between
[approval](approval-voting.md) and [score](score-voting.md). Two voters *agree* iff some platform has
V_u(p) + V_v(p) > 1, so **two overlapping maybe regions are not agreement**. That one definitional choice
carries the whole thesis.

| # | Statement | Checked |
|---|---|---|
| Thm 3.1 | pairwise agreement ⟹ a platform in **every** interest region and **at least one** approval region | holds on 3,000 random societies |
| §3.2 | interest region = interval, maybe region = tolerance ⟹ the agreement graph **is a tolerance graph**, hence perfect | requires symmetric maybe regions; otherwise bitolerance |
| Thm 4.1 | β ≥ (1 − √(1−α))/2 | holds, but loose |
| Thm 4.2 | C(N,2)·α ≥ C(Nβ,2), i.e. α ⪆ β² for large N | holds |
| Thm 5.1 | equal approval regions, maybe regions µ× as long ⟹ a platform in ⌈N/(1+⌈µ⌉)⌉ approval regions | **exact** on the column construction |

- **Theorem 3.1's "at least one" cannot be raised to two.** Six voters with disjoint approval regions sitting
  inside each other's maybe regions agree pairwise, yet no platform is approved outright by two of them.
- **Theorem 4.1 is Abbott–Katchalski halved.** Its proof relaxes the two-level society to the interval graph
  of interest regions, applies Abbott–Katchalski, then pays a factor of 2 for β′ ≤ 2β. Nothing about the
  two-level structure is used, and it shows: across 3,000 random two-level societies β exceeds the bound by
  **0.35 on average**. Theorem 4.2 is the one that earns its keep — Lemma 4.1 (two voters sharing a *left*
  maybe region must agree) is what makes the edge count work.
- **Theorem 5.1 is exact**, verified on the column construction for µ ∈ {1,2,3,4} and N ∈ {5,7,9,12,13}.
- His §4.2 worked example checks out: N = 5, α = 7/10, β = 1/2, against bounds 0.226 and 7 ≥ 15/8.

**What it does not do**: the thesis names cutoff indeterminacy as approval's drawback on its page 2 (citing
Taylor & Pacelli) and never returns to it. The maybe region is *handed* to the voter, not chosen, so the
model sidesteps the one problem [approval-voting](approval-voting.md) is organised around. There is no
strategy, no winner and no criterion in 42 pages. It is also a senior thesis — unrefereed, and Theorem 5.2's
statement carries typos ("If p V = 1") — whereas the two results it builds on are not.

### A side finding on Abbott–Katchalski

Burkhart's Theorem 2.4 (Abbott & Katchalski 1979: β ≥ 1 − √(1−α) for interval graphs) held on all 4,000
random linear societies tested — **but it never once beat Berg's Theorem 8 on the same societies** (stronger
0 times, weaker 3,918, equal 82). That is not a defect: Theorem 8 is handed the whole agreeability profile
while Abbott–Katchalski gets only the edge density. It does mean the AMM paper's machinery supersedes the
thesis's, and the two papers never cite each other.

## Open questions the paper leaves

- **The smallest unknown case is d = 2, k = 2, m = 3.** Rajneesh Hegde (private communication) found a
  (2,3)-agreeable 2-box society with agreement proportion **3/8**; no construction is printed. Such an
  example needs 8 voters whose agreement graph has no independent set of 3 and no clique of 4 — a
  **Ramsey(3,4) graph on 8 vertices**. The Wagner graph's complement is one (clique number 3, independence
  number 2, both verified here). Whether *boxes* can realise it is the open part: 120,000 random 2-box
  societies never got below 1/2 here, so 3/8 stands as published and unreproduced.
- **Circular spectra behave differently.** Via Niedermaier–Rizzolo–Su, a super-agreeable society on a
  *circular* spectrum is only guaranteed a platform approved by a **strict majority**, not by everyone — in
  direct contrast with Theorem 5. Chris Hardin generalised this to (k,m)-agreeable circular societies. If
  the political spectrum wraps around, pairwise agreement buys you half as much.
- Piercing numbers (fewest platforms such that everyone approves one), **disconnected approval sets** (what
  if a voter approves two separate ranges?), weighted agreement graphs for partial agreement across axes,
  and how one might estimate k and m from limited survey data.

## How it sits against the rest of these notes

- It changes **no winner in any other note**, and it is not evidence for or against any method. Its use here
  is as the outside view: how much agreement an electorate contains, before any rule is applied.
- The cutoff problem that dominates [approval-voting](approval-voting.md) is *assumed away* — the interval
  endpoints are given. Where that note asks "which sincere ballot does a voter cast?", this one starts after
  the answer.
- The (k,m)-agreeable condition is a **domain restriction of the same species as dichotomous preferences**:
  strong theorems, unobservable hypothesis. That parallel is the most useful thing in the paper for these
  notes.
- Burkhart's V(p) is a three-level score total, so his "maximum value platform" is the
  [score-voting](score-voting.md) winner over a continuum — but with no candidates, and with agreement
  defined by a rule (V_u + V_v > 1) that is not score.
- Unlike the spatial VSE work in [ranked-robin-vse-run](ranked-robin-vse-run.md), there are **no utilities
  and no metric** here — only order.

## New ideas and terms

- **Society / spectrum / platform / approval set** — the model above. A *linear* society has an interval
  approval set on a subset of ℝ; an *ℝᵈ-convex* society has convex approval sets in ℝᵈ; a *d-box* society
  has products of d intervals.
- **Agreement number, agreement proportion** — the most-approved platform's count, and that over n.
- **(k, m)-agreeable** — among every m voters, some k share a platform. (2,2) = super-agreeable, (2,3) =
  agreeable.
- **Agreement graph** — voters as vertices, edges when approval sets intersect. For linear societies it is
  an *interval graph* and its clique number is the agreement number.
- **Perfect graph** — χ(H) = ω(H) for every induced subgraph H. Interval graphs are perfect; box agreement
  graphs are not (C₅).
- **Tolerance graph** — interval graph where an edge needs overlap of at least the smaller *tolerance*.
  Burkhart's two-level societies are tolerance graphs when the maybe regions are symmetric, bitolerance
  graphs otherwise.
- **Piercing number** — fewest platforms needed so that every voter approves at least one.
- **Boxicity** — least d such that a graph is the agreement graph of a d-box society. Deciding boxicity ≤ d
  is NP-hard for every d ≥ 2; boxicity ≤ 1 is interval-graph recognition, which is easy.

## Links referenced in the article

- [Voting in agreeable societies, arXiv:0811.3245](http://arxiv.org/abs/0811.3245) ·
  [ar5iv full text](https://ar5iv.labs.arxiv.org/html/0811.3245)
- Kalai, "Intersection patterns of convex sets", *Israel J. Math.* **48** (1984) 161–174 — fractional Helly
- Radon, *Math. Ann.* **83** (1921) 113–115 — the first publication of Helly's theorem
- Chudnovsky, Robertson, Seymour & Thomas, "The strong perfect graph theorem", *Ann. Math.* **164** (2006)
  51–229
- Golumbic & Trenk, *Tolerance Graphs*, Cambridge, 2004 — Burkhart's other source
- Abbott & Katchalski, "A Turán type problem for interval graphs", *Discrete Math.* **25** (1979) 85–88 —
  cited by Burkhart, not by Berg et al.

## Related local material

- [approval-voting](approval-voting.md) — the method this is nominally about, and the note whose central
  problem (the cutoff) this model assumes away
- [score-voting](score-voting.md) — where Burkhart's half-weight level would land if it were a ballot
- [glossary](glossary.md) — the terms above are indexed there
- [ranked-robin-vse-run](ranked-robin-vse-run.md) — spatial models with utilities and an actual tabulation
  rule, for contrast
