# Cardinal voting systems — the class, and one bad inference about Arrow

Source: [*Cardinal voting systems*](https://electowiki.org/wiki/Cardinal_voting_systems) (electowiki),
read 2026-08-01 via `action=raw` — the rendered page returns HTTP 403 to non-browser clients.

Verifier: [code/cardinal-arrow/verify.py](code/cardinal-arrow/verify.py) ·
output: [run-output.txt](code/cardinal-arrow/run-output.txt) — 5 checks, all pass.

> **Scope note on the source.** Same caveat as everywhere else electowiki is cited here
> ([approval-voting](approval-voting.md), [ranked-robin-origins](ranked-robin-origins.md)):
> [Electowiki:Policy](https://electowiki.org/wiki/Electowiki:Policy) declares a point of view and tells
> readers to go to Wikipedia for neutral information. This page leans on that permission harder than the
> Approval one does — see [§6](#6-three-more-claims-worth-not-repeating). It is used here as a **taxonomy**,
> which is what it is genuinely good at, and its load-bearing theoretical claim is checked rather than
> repeated.

## Why this note exists

Every other cardinal note in this folder is about *one method* —
[approval](approval-voting.md), [score](score-voting.md), [STAR](star-voting.md),
[majority judgment](majority-judgment.md). None of them defines the **class**, and the class turns out to
have vocabulary the individual notes never needed: what makes a method cardinal, what the scale is doing,
what happens to that scale under transformation, and — the entire half that was missing here — how cardinal
ballots are made **proportional** across many seats.

---

## 1. What makes a method cardinal

**Cardinal** (aka **evaluative**, **rated**, **graded**, **range**) methods let a voter evaluate each
candidate *independently on a common scale*. Two consequences the ranked family cannot offer: equal ratings
are allowed, and **skipped ratings can affect the result** — the blank-vs-zero problem
[score-voting](score-voting.md) works out from the sum-vs-average side.

The name is not about "numbers". It is about **cardinality of the grade set**:

> For a cardinal ballot to carry more information than an ordinal one, **the number of gradations must exceed
> the number of candidates** — that is the only way a strict ordering is recoverable from the ratings.

That single line reorganises the whole family, and it is the thing none of the other notes said. It also cuts
both ways, which the page does not say: at 6 grades and 7 candidates a 0–5 STAR ballot is *strictly less*
expressive than a ranking, and Equal Vote's own scale is 0–5.

### Pure vs. semi-cardinal

The page's most useful distinction, and one worth importing wholesale:

| | Methods | Why it matters |
|---|---|---|
| **Pure cardinal** | Approval, Score | The winner is a function of the score columns alone. Monotonicity is immediate ("raising a score cannot hurt"), and rated-IIA follows — a voter's score for C cannot touch the A-vs-B contest. No incentive for favorite betrayal, no wasted-vote logic. |
| **Semi-cardinal** | STAR, MJ tiebreaks, everything else | A second stage reads *across* columns. Every property in the left column is then up for grabs. |

This is exactly why [star-voting](star-voting.md) records STAR failing majority, Condorcet, clone
independence, later-no-harm **and** favorite betrayal while [score-voting](score-voting.md) records score
passing IIA: the runoff is the whole difference, and "cardinal" alone predicts nothing about a method that
has one. The page states this and then spends its Criticism section arguing as if all cardinal methods were
pure.

## 2. Scale vs. gradation — and scale invariance

Two different things that both sound like "the range":

- **The range doesn't matter.** Voting on [0,1], [0,100] or [−42,7] gives identical results under sum,
  average or median, because an order-preserving affine remap of *everyone's* scale preserves all three.
  Named: **scale invariance**.
- **The gradation does matter.** How many steps sit inside the range determines how much of the preference
  survives the ballot, per the cardinality line above.

**Scale invariance is not free once ballots are reweighted.** The page's own example: RRV fails it; SPAV
composed with the KP transform recovers it. That is the first thing in this material that is a genuine
design constraint rather than a talking point.

### The KP (Kotze–Pereira) transform

Converts a rated ballot into fractional **approval** ballots: a candidate scored *k* out of *m* is approved
on exactly *k* of *m* unit sub-ballots. So score voting on an *m*-level scale **is** approval voting run over
*m* sub-electorates.

Verified exactly — 20,000 random 7-voter, 4-candidate profiles on a 0–5 scale, **zero mismatches** between
the direct score total and the KP-reconstructed approval total (`verify.py`, check 5).

Why this earns its place here: it is the bridge that makes
[brandl-peters-approval-characterizations](brandl-peters-approval-characterizations.md) speak to score voting
at all. Anything the transform preserves, an approval theorem transfers to score at every scale.

### Approval rating

A candidate's total as a percentage of the maximum attainable — the total they'd have if every voter
max-scored them. Every voter giving a 5 on 0–10 is a **50% approval rating**. Trivial, and the only clean
way to compare totals across methods that use different scales.

## 3. The multi-winner half — the part that was entirely missing here

[glossary.md](glossary.md) had one bullet for this ("block approval / reweighted range / sequential
proportional approval"). The actual family is organised on an axis worth knowing, because **the reweighting
rule is a theory of what proportionality means**, not an implementation detail.

### Bloc methods (not proportional)

Top *k* totals win. **Bloc Approval**, **Bloc Score**, **Bloc STAR** (repeated top-two runoffs, two seats at
a time). These are the cardinal analogue of block plurality and they let a coherent majority take every
seat — the reason the sequential family exists.

### Sequential proportional methods

Elect one at a time: run the single-winner selection, then **reweight** ballots that already helped elect
someone, then repeat. The reweighting is the surplus transfer's cardinal analogue.

| System | Gradation | Reweighting philosophy | Party-list degenerate case |
|---|---|---|---|
| Reweighted Range Voting (RRV) | > 2 | Thiele | Highest averages |
| Single Distributed Vote | > 2 | Thiele | Highest averages |
| Sequential Proportional Approval (SPAV) | binary | Thiele | Highest averages |
| Sequentially Spent Score (SSS) | > 2 | Vote Unitarity | Hamilton |
| Allocated Score | > 2 | Monroe | Hamilton |
| Sequential Monroe | > 2 | Monroe | Hamilton |
| Sequential Phragmén | binary | Phragmén | — |
| Sequential Ebert | binary | Phragmén | — |

**The four philosophies, in one line each:**

- **Thiele** — a voter's influence decays harmonically in how many winners they already got. Diminishing
  returns on satisfaction.
- **Monroe** — each winner is *assigned* a quota of voters who are then spent. Representation as partition.
- **Phragmén** — winners impose a load spread across their supporters; minimise the maximum load. Fairness
  as evenness of burden, not of satisfaction.
- **Vote Unitarity** — each voter has exactly one vote's worth of influence to spend, and spends it down.

The **party-list column is the useful diagnostic**: run each on a pure party-list profile and Thiele methods
collapse to a **highest-averages** divisor method (D'Hondt/Webster family) while Monroe and Vote Unitarity
collapse to **Hamilton** (largest remainders). That is the same Hamilton/divisor split
[math-in-society-lippman](math-in-society-lippman.md) covers under apportionment, arriving from the other
direction — and it drags the whole **Balinski–Young** quota-vs-monotonicity trade into cardinal PR, which is
presumably why the page raises Balinski–Young at all.

The reweighting target is the **Hare Quota Criterion**: a solid coalition of a Hare quota's worth of voters
must get a seat.

### Optimal proportional methods

Pick the whole winner *set* at once by maximising a quality function — Harmonic Voting, **Proportional
Approval Voting (PAV)**, **Monroe's method**, **Ebert's method**, **max-Phragmén**, **PAMSAC**. Usually
implemented by trying every winner set, hence combinatorial in the number of seats.

Note **Ebert's method fails monotonicity** — the page uses this correctly, as an example of a cardinal method
failing an Arrow-adjacent property *for reasons unrelated to Arrow*. (Monotonicity is not one of Arrow's
conditions, which the page's phrasing slightly blurs.)

### One local connection

**SSS in that table is the method whose `verbosity=0` engine path I found broken in the STAR Voting
library.** It has no note here, and the reweighting philosophy above — Vote Unitarity, spend-down — is what
the buggy code path was implementing.

## 4. The Arrow claim, checked

This is the finding. The page's *Impossibility theorems* section says:

> "Since Arrow's theorem only applies to ordinal voting and not cardinal voting systems, several cardinal
> systems meet all these criteria. The typical examples are score voting and majority judgment."

**First clause: correct.** Arrow's conditions quantify over profiles of preference *orderings*; cardinal
ballots are not in the domain. This folder already asserts that from the opposite direction — it is precisely
the error [math-in-society-lippman](math-in-society-lippman.md) catches Lippman making, stating Arrow for "a
voting method" one page before introducing approval voting.

**Second clause: does not follow.** Two independent reasons, both checkable.

### 4a. "Satisfies IIA" is doing double duty

Arrow's IIA is about **preference orderings**. What score and MJ satisfy is **rated-IIA** — the social
ranking of A and B depends only on the *ratings* given to A and B. That is a weaker, different condition, and
it holds only while voters rate **absolutely**. Let them normalise to the field — which the same page argues
at length that voters will do — and it fails.

`verify.py` check 1 builds the minimal witness, with the extra property that **the candidate whose presence
flips the result is a loser**, i.e. an irrelevant alternative in the strict sense:

| Voters | u(A) | u(B) | u(C) |
|---|---|---|---|
| 5 | 0.5 | 0.6 | 0.0 |
| 4 | 1.0 | 0.0 | 0.9 |

Normalising each voter's best remaining candidate to 5 and worst to 0:

- **With C:** A = 40.83, B = 25.00, C = 18.00 → **A > B > C**. C finishes last.
- **Without C:** A = 20.00, B = 25.00 → **B > A**.

No voter's opinion of A or B changed. A last-place candidate reversed them. Under **absolute** scoring on the
same utilities the A-vs-B order is untouched (A = 32.5, B = 15 either way).

Over 200,000 random 9-voter profiles (check 2):

| Method | IIA violations | Rate | of which C finished last |
|---|---|---|---|
| Score, absolute | 0 | 0.00% | — |
| Score, normalised | 26,714 | **13.36%** | 11,956 |
| Majority judgment, absolute | 0 | 0.00% | — |
| Majority judgment, normalised | 29,726 | **14.86%** | 12,397 |

So the two methods the page names as exemplars are, under the behaviour the page itself predicts, the two
methods that break the property in roughly one profile in seven. [score-voting](score-voting.md) §4 already
had this conditional for score with a hand-worked example; **MJ was not known here to break the same way, and
it breaks slightly more often.**

### 4b. The deeper problem: it is a category error, not a pass

Arrow's conditions are predicates on functions whose *input is a preference profile*. A cardinal method isn't
one. The same ordering admits many honest ballots, and they elect different people (check 3):

| | 5 voters `A>B>C` | 4 voters `C>B>A` | Score winner |
|---|---|---|---|
| B warmly held | A 1.0, B 0.9, C 0.0 | C 1.0, B 0.9, A 0.0 | **B** (40.5) |
| B merely tolerated | A 1.0, B 0.1, C 0.0 | C 1.0, B 0.1, A 0.0 | **A** (25.0) |

Identical orderings, different winners. MJ separates on a three-bloc analogue (C wins one, B the other). A
rule that is not a function on Arrow's domain cannot satisfy conditions quantified over that domain — it is
outside the theorem, which is not the same as beating it.

### 4c. What the escape actually costs — Sen's theorem

There is a precise result here and the page does not cite it. Sen extended Arrow's framework to richer
informational bases and found:

> Cardinal **measurability** is not by itself enough to avoid the impossibility. The utilities must also be
> **interpersonally comparable**. (Sen 1970, Thm 8\*2; strengthened by d'Aspremont & Gevers 1977.)

Under **cardinal non-comparability** — the social ranking must be invariant when each voter's utility is
independently replaced by *aᵢu + bᵢ*, *aᵢ* > 0 — the Arrow impossibility survives intact.

Score voting is flatly not invariant under that. Check 4: over 100,000 random 5-voter profiles with an
independent positive affine rescaling per voter, **the winner changed 20,891 times (20.9%)**.

That is the whole answer. Score voting escapes Arrow by *assuming your 5 and my 5 are the same quantity* —
an assumption Arrow's framework deliberately withholds. It doesn't satisfy the conditions; it declines the
premise, and pays for it in a comparability assumption the ballot cannot enforce.

### 4d. The page contains its own refutation

Two sections earlier, in *Criticism*, the article records — attributed to majority-rule proponents rather
than asserted in its own voice — that voters "may normalize to different scales if a candidate enters or
exits," so "the presence of irrelevant candidates may thus change the outcome of the election, **even for
methods nominally passing IIA**."

And it reports that Balinski and Laraki "argued that a **common language** is required to avoid the
implications of Arrow's impossibility theorem, and designed Majority judgment to use scales based on such
common language."

A common language *is* interpersonal comparability. So the article states Sen's condition, attributes MJ's
escape to satisfying it, and then two sections later presents MJ as an example of *meeting Arrow's criteria*
— the one description its own sources don't support. The pieces are all on the page; nothing joins them.

**Verdict:** not a fabrication and not a small slip. The premise is right, the conclusion is wrong, and the
material needed to see why is already in the article.

## 5. The symmetry worth keeping

Two sources in these notes now get Arrow wrong **in opposite directions off the same fact**:

| Source | Error | Effect on a reader |
|---|---|---|
| Lippman, *Math in Society* §2.12 | States Arrow **without** "ranked", one page before teaching approval voting | Thinks the theorem condemns a method it never reached |
| electowiki, *Cardinal voting systems* | States the ordinal restriction correctly, then infers cardinal methods **satisfy** Arrow's conditions | Thinks the theorem has been beaten |

The shared fact — Arrow's hypothesis is ordinal — is genuinely load-bearing, genuinely often dropped, and
apparently just as easy to over-apply as to under-apply. Both entries belong in [whoops](whoops.md).

## 6. Three more claims worth not repeating

- **"Score voting has the lowest Bayesian Regret among all common single-winner election methods which have
  been tested."** No citation on the page. **Bayesian regret** — Warren Smith's measure of expected avoidable
  human unhappiness, the quantity **VSE inverts** — appears nowhere else in these notes, and the underlying
  simulations are the author's own. Take the term; leave the superlative.
- **"STAR Voting was found to have the highest Voter Satisfaction Efficiency rating overall."** Sourced to a
  bare link to Quinn's `vse-sim`. [ranked-robin-vse-run](ranked-robin-vse-run.md) is what running that
  codebase locally actually produces; the sentence is an advocacy claim about a research tool, cited to the
  tool.
- **"Satisfying the majority criterion reduces incentive for compromise and lowers Bayesian Regret."**
  Two causal claims and a conflation — the paragraph also asserts that IRV's majority compliance is "stronger"
  than the rated variant while arguing majority compliance is bad. Whatever the merits, it is argument
  presented as exposition.

The **majority criterion for rated ballots** is a real and useful term though, and new here: *if a candidate
is preferred and max-scored by an absolute majority, that candidate must win.* Strictly weaker than the
ordinary majority criterion, and MJ satisfies it while failing the ordinary one — which is a cleaner way to
state MJ's position than [majority-judgment](majority-judgment.md) currently does.

## 7. New ideas and terms

Everything below was absent from all 22 notes in this folder before today.

- **Cardinal / evaluative / rated / graded / range** — four synonyms for the class.
- **Pure vs. semi-cardinal** — winner is a function of the score columns alone, or isn't. The distinction
  that decides whether "cardinal" predicts anything about a method's compliance.
- **Gradation** — the count of steps in the scale, as opposed to its endpoints. Must exceed the candidate
  count for the ballot to out-inform a ranking.
- **Scale invariance** — multiplying all scores by a constant doesn't change the result. RRV fails it;
  SPAV + KP recovers it.
- **KP (Kotze–Pereira) transform** — rated ballots → fractional approval ballots. Verified exact.
- **Approval rating** — total as a fraction of the maximum attainable total.
- **Utilitarian winner** — the sum-maximising candidate. The thing score voting is *for*.
- **Bayesian regret** — expected avoidable human unhappiness; VSE is its inverse.
- **Majority criterion for rated ballots** — max-scored by a majority ⇒ must win.
- **Rated pairwise preference ballot** — a ballot format addressing the one thing cardinal ballots cannot
  express: a maximal preference between *every* pair when there are more than two candidates.
- **Normalization** — rescaling so your best gets the max and your worst the min. Named here; the *behaviour*
  was already worked out in [score-voting](score-voting.md) §4.
- **Thiele / Monroe / Phragmén / Vote Unitarity** — the four reweighting philosophies, and their
  highest-averages vs. Hamilton party-list signatures.
- **Hare Quota Criterion** — a Hare quota of like-minded voters must win a seat.
- **Bloc Approval / Bloc Score / Bloc STAR** — the non-proportional multi-winner cardinal methods.
- **SSS, Allocated Score, Sequential Monroe, Sequential Phragmén, Sequential Ebert, PAV, PAMSAC, Harmonic
  Voting, max-Phragmén, Single Distributed Vote** — the proportional cardinal family.
- **Reciprocal Score Voting, Chiastic Score Voting, Majority Choice Approval, Majority Approval Voting** —
  minor single-winner cardinal methods; MCA and MAV are median rules on binary ballots.
- **Free riding** — the multi-winner strategy single-member systems are immune to.
- **Sen's Theorem 8\*2 / cardinal non-comparability** — the result that prices the Arrow escape.
- **Random ballot** — under weak unanimity and finite precision, the *only* strategy-proof cardinal method
  (Dutta, Peters & Sen 2007). The cardinal counterpart to Gibbard–Satterthwaite.

## Links referenced

- [*Cardinal voting systems*](https://electowiki.org/wiki/Cardinal_voting_systems) · [Electowiki:Policy](https://electowiki.org/wiki/Electowiki:Policy)
- [Arrow's Theorem (Stanford Encyclopedia of Philosophy)](https://plato.stanford.edu/entries/arrows-theorem/)
  — Sen's Thm 8\*2 and the measurability-vs-comparability distinction
- Sen, *Collective Choice and Social Welfare* (1970); d'Aspremont & Gevers, "Equity and the Informational
  Basis of Collective Choice", *RES* 44 (1977)
- [Balinski & Laraki, "A theory of measuring, electing and ranking", *PNAS* 104 (2007)](https://www.pnas.org/content/pnas/104/21/8720.full.pdf)
  — the "common language" argument, cited by the page
- Dutta, Peters & Sen, ["Strategy-proof Cardinal Decision Schemes"](https://doi.org/10.1007/s00355-006-0152-9),
  *Soc Choice Welf* 28 (2007) — random ballot as the only strategy-proof cardinal rule
- Gibbard, "Manipulation of voting schemes: A general result", *Econometrica* 41 (1973)
- Woodall, ["Properties of Preferential Election Rules"](http://www.votingmatters.org.uk/ISSUE3/P5.HTM),
  *Voting matters* 3 (1994) — the later-no-harm criticism the page cites
- [Harmonic Voting (rangevoting.org)](https://rangevoting.org/QualityMulti.html)

## Related local material

- [score-voting](score-voting.md) — §4 is the same normalisation/IIA conditional, worked by hand; this note
  supplies the theorem behind it and extends the result to MJ
- [majority-judgment](majority-judgment.md) — records MJ passing IIA over 185,027 profiles. That result is
  correct and is about *absolute* grading; check 2 here is the other half of the conditional
- [approval-voting](approval-voting.md) — the binary extreme of the gradation axis; same IIA caveat from the
  cutoff side
- [star-voting](star-voting.md) — the semi-cardinal exemplar, and why the class label predicts nothing there
- [brandl-peters-approval-characterizations](brandl-peters-approval-characterizations.md) — the KP transform
  is what carries those theorems from approval to score
- [math-in-society-lippman](math-in-society-lippman.md) — the mirror-image Arrow error
- [single-transferable-vote](single-transferable-vote.md) — the ranked answer to the same multi-winner
  question; quota and surplus transfer against quota and reweighting
- [whoops](whoops.md) — the Arrow inference is indexed there
- [glossary.md](glossary.md) — all terms in §7 above are now defined there
