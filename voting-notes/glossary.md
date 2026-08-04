# Voting methods — glossary

One place for every term used across the notes in this folder. Entries marked **[LeGrand]** come from
[LeGrand's ranked-ballot site](legrand-ranked-ballot-methods.md), which names them but never defines them;
those definitions are filled in here from the standard social-choice literature. Entries marked
**[→ note]** are covered in more depth in the linked note.

---

## 1. Ballots and inputs

- **Ranked (ordinal) ballot** — an ordering of candidates: `A>B>C`. Notation `4:A>B>C` means four identical
  ballots; `A>B=C` means no preference between B and C. Ties in a ranking count as **half a vote each way**
  in pairwise comparisons.
- **Scored (cardinal) ballot** — a rating per candidate (`Palin 5, Begich 4, Peltola 0`). Carries *strength*
  of preference, which rankings cannot. [→ [rcv-and-core-support](rcv-and-core-support.md)]
- **Grading ballot** — the same object under the name the SEP entry gives it, which treats the grades as a
  shared *language* — a common scale meaning the same thing to every voter — rather than as arbitrary
  numbers. The distinction earns its keep because a grade is then interpersonally comparable by
  construction, which is what Sen's theorem says a cardinal method needs and what per-voter normalisation
  destroys. **A grading ballot is not a ranking with decoration**: collapse it to the ranking it induces and
  the mean and the median — the two quantities score voting and majority judgement actually differ over —
  are both gone. [→ [sep-voting-methods](sep-voting-methods.md),
  [cardinal-voting-systems](cardinal-voting-systems.md)]
- **Truncated / bullet ballot** — a ballot ranking only some candidates. Unranked candidates are conventionally
  placed below every ranked one and tied with each other.
- **Ordinal preferences** — rankings only; silent about gaps between candidates.
- **Cardinal preferences** — strength of preference; what any utility- or intensity-based argument requires.
- **Approval ballot** — a 0/1 score per candidate: approve any number, no limit, so **overvoting is
  impossible**. [→ [approval-voting](approval-voting.md)]
- **Disapproval ballot** — the same ballot inverted: everyone is approved unless you strike the name off.
  Logically identical to approval, psychologically not, and the form actually used in the Soviet
  multi-candidate elections of June 1987. [→ [approval-voting](approval-voting.md)]
- **Voting power (pair-discrimination sense)** — not a criterion but an advocacy metric, from CRV: the number
  of candidate pairs a ballot separates, *k*(*N*−*k*) for a ballot approving *k* of *N*. Plurality is the
  *k* = 1 case, so both methods are the same function under different constraints, and approval's advantage is
  a *maximum over ballots* — ⌊N/2⌋⌈N/2⌉, which is **no gain at all at three candidates** and goes unclaimed by
  the bullet voters who are ~80% of every measured approval electorate.
  [→ [approval-voting](approval-voting.md)]
- **Approval / score / STAR** — cardinal methods, outside LeGrand's ranked-only scope. STAR = Score Then
  Automatic Runoff (score everyone 0–5, top two by total score go to an automatic pairwise runoff).
  Score voting is approval with more levels; **combined approval** uses three (−1, 0, +1).
- **Approval cutoff (acceptance threshold)** — the line a voter draws through their own preference order to
  turn it into an approval ballot. Approval's entire strategic content lives here, because it is the one
  method with *many* sincere ballots per voter. A **fixed (dichotomous) cutoff** — "anyone I'd genuinely
  accept" — is IIA-safe; a **floating** one (above-average utility, top-k) is not.
  [→ [approval-voting](approval-voting.md)]
- **Rule (1) vs. Rule (2)** *(Horn)* — approval's instructions written two ways. **Rule (1)**: "vote for all
  and only those candidates you minimally approve of." **Rule (2)**: "vote by making a mark next to as many
  candidate names as you like." Both describe the same tabulation; only the first constrains what a mark
  *means*. Bullet voting your favorite violates (1) and complies perfectly with (2); (2) is violable only by
  defacing the ballot. Worth having a name for, because approval's advocacy assumes (1), its criticism
  attacks (2), and almost every argument about the method turns on which one is in play. Note what (1) buys:
  it makes the approval set an *attitude* fixed before the field is known, which is IIA by construction —
  so the properties proved under it are properties of the assumption, not of the count.
  [→ [horn-three-virtues-approval](horn-three-virtues-approval.md), [approval-voting](approval-voting.md)]
- **Dichotomous preferences** — candidates fall into exactly two indifference classes, acceptable and not,
  with no ranking inside either. Under this model approval is strategyproof *and* Condorcet-consistent;
  Brams and Fishburn concede it is unrealistic beyond a handful of voters. But the domain does more than
  flatter approval — on it approval is the *only* rule left standing. Brandl and Peters (2022) give eight
  characterizations, every one built on **consistency with variable electorates** (merge two electorates and
  the commonly chosen alternatives are what the merged electorate chooses) plus a headline axiom —
  strategyproofness, Condorcet, clone independence, and five others — plus housekeeping axioms that vary by
  theorem (anonymity, neutrality, faithfulness, continuity, non-triviality), none of them droppable. Read
  the assumption as a *domain restriction with a uniqueness theorem attached*, not as a thumb on the scale.
  Note too that on this domain the majority relation is **transitive** (Inada 1969) and orders candidates by
  approval score, so Condorcet cycles cannot occur at all. [→ [approval-voting](approval-voting.md)]
- **Summability** — a precinct can report one integer per candidate and the totals just add. Plurality and
  approval are summable; IRV and STV are not, because eliminations and transfers need the whole ballot set in
  one place. Administrative, not a fairness property — but it drives adoption, and it is why STV counts are
  centralised and slow. [→ [single-transferable-vote](single-transferable-vote.md)]

## 2. Pairwise machinery

- **Pairwise matrix** — one pass over the ballots yields, for every ordered pair (X, Y), how many voters
  ranked X over Y. Every Condorcet method reads only this matrix. In an *n*-candidate race each candidate has
  *n* − 1 matchups.
- **Head-to-head matchup** — one cell-pair of that matrix, treated as a two-candidate election.
- **Condorcet winner** — beats every other candidate head-to-head. May not exist.
- **Condorcet loser** — loses every head-to-head. May be beaten by a hair in each (LeGrand's Cora loses all
  four of hers 460–461).
- **Condorcet cycle** — A beats B beats C beats A. The reason pairwise methods need a completion rule at all.
- **Margin** — winner's votes minus loser's votes in a matchup. **Winning votes** — just the winner's total.
  Methods differ on which they use; the choice changes results when ballots are truncated.
- **Negative vote-counting** — building the pairwise matrix from approval ballots: X scores against Y the
  ballots approving X and not Y. Ballots approving both or neither cancel, so every margin collapses to
  approvals(X) − approvals(Y). Approval is therefore a Condorcet method on ballots ranking everyone 1st or
  last — one whose matrix is transitive by construction and carries no information the approval totals didn't,
  which is why approval ballots cannot identify the Condorcet winner.
  [→ [approval-voting](approval-voting.md)]
- **Beatpath** — a chain of pairwise victories `A>B>C>D`. Its **strength** is that of its *weakest* link.
- **Copeland score** — pairwise victories, a tie counting ½. Ceiling is *n* − 1, regardless of how many people
  voted — the source of the "12 ballots, 1 win" confusion.
  [→ [ranked-robin-results-explained](ranked-robin-results-explained.md)]
- **Tiebreaking ranking** — no unbiased method is always decisive (LeGrand's 25/25/25/25 example proves it);
  a fallback ordering is required, often from a randomly drawn ballot or a pre-drawn candidate order.

## 3. Candidate sets

These are *sets*, not winners — usually used as a filter before some other method (`Smith//X` = run X inside
the Smith set).

- **Smith set** **[LeGrand]** — the smallest non-empty set whose every member beats every candidate outside it.
  Contains the Condorcet winner when one exists; otherwise the top cycle. Also called the top cycle or GETCHA.
- **Schwartz set** **[LeGrand]** — the union of all minimal non-empty sets that no outside candidate beats.
  A subset of the Smith set; they differ only when pairwise ties are present. Also called GOCHA.
- **Landau set** **[LeGrand]** — the uncovered set: candidates X such that for every Y, either X beats Y, or X
  beats some Z that beats Y. Contains the Smith set's winner but is generally larger and less decisive.
- **Smith//Score** — restrict to the Smith set, then elect the highest total score. A common cardinal
  completion for Condorcet cycles. [→ [rcv-and-core-support](rcv-and-core-support.md)]

## 4. Methods

### Point count

- **Borda** **[LeGrand]** — score = (times ranked above another) − (times ranked below another); equivalently
  positional points 0…*n*−1. Strong under sincere voting, easiest to manipulate, and *not* clone-independent —
  a party can win by running extra candidates.
- **Antiplurality** (anti-plurality, veto rule) — the positional rule (1, 1, …, 1, 0): a point for every
  ballot that does *not* rank you last, so **fewest last-place votes wins**. Plurality's mirror image —
  (1, 0, …, 0) reads only the top of the ballot, this reads only the bottom — with **Borda** the midpoint of
  the family between them. **Coombs** (below) is this rule applied recursively instead of once.
  It fails the **majority criterion** flatly: `60:A>B>C, 40:B>C>A` elects B though A is the strict favourite
  of 60%. It fails **Condorcet**, as every positional rule must. And it can elect the **Condorcet loser** —
  `2:B>A>C, 2:C>A>B, 1:C>B>A` elects A, who loses 3–2 to both B and C, precisely because A is second on four
  ballots of five and last on one. Borda is the only positional rule that never does this
  (Fishburn–Gehrlein), which is the sharpest argument available for the middle of the family over either end.
  Its structural weakness is arithmetic: *n* voters distribute only *n* last-place votes among *m*
  candidates, so once the field is bigger than about three, most candidates sit on **zero** and the rule
  ties. The IMD card's own example is a case — 42 `A>B>C>D`, 26 `B>C>D>A`, 15 `C>D>B>A`, 17 `D>C>B>A` leaves
  both B and C on zero, so antiplurality is undecided at the first step and has to be re-run head-to-head
  (giving B, the Condorcet winner, where plurality gives A). Everything the ballot said about the top is
  discarded, so the rule reads "least objectionable" and nothing else — the **bland-winner objection** of §6
  in its purest form — and the only strategy it admits is burying your favourite's strongest rival in last
  place. It also cannot be run at all without a truncation convention: a ballot ranking two of five
  candidates has to be told who counts as last. [→ [mdi-trivia-cards](mdi-trivia-cards.md)]

- ***k*-Approval** — the scoring rule (1, …, 1, 0, …, 0) with *k* ones: a point to everyone ranked *k*th or
  higher. Plurality is *k* = 1 and antiplurality is *k* = *m* − 1, so the whole family above interpolates
  between them by moving one boundary. Worth keeping as a family because the boundary decides the election:
  on `2 ADBC, 2 BDAC, 1 CABD`, 1-approval elects {A, B}, 2-approval elects D and 3-approval elects {A, B}
  again — and the Condorcet winner is A. The cutoff-dependence of approval, stated as a difference between
  *rules* rather than between voters. [→ [sep-voting-methods](sep-voting-methods.md)]
- **Quota rule (single-winner)** — fix *q* between 0 and 1 and elect everyone with at least *q* × (number of
  voters) votes. Majority rule is *q* = 0.5, unanimity rule is *q* = 1. Its defect is the obvious one and it
  is worth stating plainly: **quota rules frequently elect nobody**, which is why every real use of one is
  paired with a runoff or a fallback. (Not the multi-winner quota of the STV entries below, nor the
  apportionment quota rule of §8 — three unrelated uses of the word.)
  [→ [sep-voting-methods](sep-voting-methods.md)]

### Borda-based recursive elimination

- **Nanson** **[LeGrand]** — repeatedly eliminate *all* candidates with a negative Borda score. Condorcet, Smith.
- **Baldwin** **[LeGrand]** — repeatedly eliminate the single worst Borda score. Condorcet, but non-monotonic.
- **Rouse** **[LeGrand]** — repeatedly drop the *best* Borda score until one candidate remains, then eliminate
  that one from the original field; repeat.

### First-preference elimination

- **Hare** **[LeGrand]** — the original name of **Instant Runoff Voting (IRV / RCV)**: eliminate the fewest
  first-place votes, repeat. Clone-independent and mutual-majority, but fails Condorcet, Smith and monotonicity.
- **Carey** **[LeGrand]** — eliminate *all* candidates below the average first-place total each round
  (generalizing Craig Carey's three-candidate IFPP).
- **Coombs** **[LeGrand]** — Hare in reverse: eliminate the *most last-place* votes each round.

### Cumulative

- **Bucklin** **[LeGrand]** — add second, then third, … preferences to the first-place counts until someone
  passes 50%. If several cross in the same round, the largest wins — which can be a pairwise loser.
  Progressive-Era US, and reportedly **the first highest-median rule** — the same rule majority judgment
  reaches from the cardinal side. [→ [majority-judgment](majority-judgment.md)]

### Pairwise

- **Black** **[LeGrand]** — Condorcet winner if one exists, else Borda. The most decisive method in the set.
- **Copeland** **[LeGrand]** — most pairwise victories (ties ½). Ignores margins entirely, so it ties often —
  the least decisive method in the set.
- **Small** **[LeGrand]** — Copeland, then if several tie for best, drop everyone else and recompute; repeat.
- **Dodgson** **[LeGrand]** — *as LeGrand defines it*: the smallest sum of defeat margins. ⚠️ The **classical
  Dodgson method** (Lewis Carroll) instead elects whoever needs the fewest adjacent swaps on ballots to become
  a Condorcet winner, and is NP-hard; LeGrand's rule is a cheap approximation of it.
- **Simpson** **[LeGrand]** — a.k.a. **minimax** / Simpson–Kramer: the smallest *maximum* pairwise defeat.
- **Raynaud** **[LeGrand]** — elimination form of Simpson: repeatedly remove whoever suffers the largest
  remaining single defeat.
- **Schulze** **[LeGrand]** — beatpath method: elect whoever has a stronger beatpath to each rival than that
  rival has back. The only method on LeGrand's chart satisfying the Schwartz criterion. In real use by
  several European cities, parties and open-source projects.
- **Tideman** **[LeGrand]** — **ranked pairs**: lock in pairwise victories strongest→weakest, skipping any
  that would contradict an already-locked stronger one. Produces a full ordering, not just a winner.
- **Condorcet–IRV hybrids** — the family that bolts a pairwise gate onto Hare elimination: Condorcet
  winner when one exists, IRV machinery otherwise. Burial against the eliminate-by-first-preferences
  members can only ever reproduce sincere IRV's outcome, never steal beyond it — measured at 3–4× more
  burial-resistant than minimax or Ranked Robin. [→ [condorcet-irv-hybrids](condorcet-irv-hybrids.md)]
  - **Smith//IRV** — compute the Smith set once, delete everyone outside it, run IRV on the rest.
  - **Benham** — run IRV, but before each elimination elect anyone who pairwise-beats all remaining.
  - **Woodall (method)** — plain IRV eliminations untouched; elect the moment only one member of the
    *original* Smith set survives. ⚠️ Same Douglas Woodall as the criteria author (mono-raise-delete,
    later-no-harm) — different hat.
  - **BTR-IRV** — bottom-two runoff: each round the two lowest first-preference candidates fight
    pairwise, the matchup loser is eliminated. No Smith computation anywhere — and the one hybrid whose
    *eliminations* read the (falsifiable) pairwise matrix, which makes it the family's weak member under
    burial.
  - **Tideman's Alternative** — a.k.a. Alternative Smith: restrict to the current Smith set, eliminate
    the fewest-first-preferences candidate, recompute; repeat until one remains. ⚠️ Not "Tideman" =
    ranked pairs above — a different method named for the same Nicolaus Tideman (whose third appearance
    here is the PSC paper in [single-transferable-vote](single-transferable-vote.md)).
- **Ranked Robin** — Equal Vote's Condorcet method; scores by matchup wins (Copeland), then breaks ties by
  greatest sum of pairwise margins among the tied (their "total advantage"). Debuted Oct 2021 as **Ranked
  Advantage Voting**, renamed Nov 2021. Honest-ballot VSE: top of the Condorcet cluster, tie-ladder
  VSE-neutral but the most decisive method in the votesim field.
  [→ [ranked-robin-results-explained](ranked-robin-results-explained.md),
  [ranked-robin-origins](ranked-robin-origins.md), [ranked-robin-vse-run](ranked-robin-vse-run.md)]
- **Top Two IRV** — only the two first-choice leaders reach the runoff.
  [→ [rcv-and-core-support](rcv-and-core-support.md)]

### Cardinal

Also **evaluative**, **rated**, **graded**, **range**: evaluate each candidate independently on a common
scale. Equal ratings are allowed and blanks are meaningful, neither of which a ranking permits.
[→ [cardinal-voting-systems](cardinal-voting-systems.md)]

- **Pure vs. semi-cardinal** — pure (approval, score) means the winner is a function of the score columns
  alone, which is what makes monotonicity and rated-IIA immediate. Semi-cardinal (STAR, MJ's tiebreak,
  everything else) adds a stage reading *across* columns, and all of those properties are back in play.
  **"Cardinal" on its own predicts nothing about a method with a second stage** — which is the whole
  distance between the [score](score-voting.md) and [STAR](star-voting.md) compliance rows.
  [→ [cardinal-voting-systems](cardinal-voting-systems.md)]
- **Score-then-runoff family** — methods taking a **grading ballot** and finishing with a *pairwise* stage:
  **STAR** (top two by total score, then whichever more voters graded above the other), **Smith//Score**,
  **3-2-1 voting** (Quinn: three semifinalists on "good" ratings, two finalists after dropping the one with
  most "bad", then pairwise), and **Reverse STAR** (pairwise stage first). They exist to answer a problem
  score voting has and the graders don't fix: once the finalists are set, exaggerating a grade cannot move
  the result, so the min-max incentive that turns [score voting](score-voting.md) into plurality loses its
  payoff. The family is the empty cell in the SEP entry's taxonomy — §2.1 Ranking Methods, §2.2 Voting by
  Grading, and nothing where the two meet. [→ [sep-voting-methods](sep-voting-methods.md),
  [star-voting](star-voting.md)]
- **Gradation** — the number of steps *inside* the scale, as against its endpoints. Where the family gets its
  name: a cardinal ballot out-informs a ranking only when the gradations **exceed the candidate count**, so a
  0–5 ballot in a 7-way race is strictly *less* expressive than a ranking.
  [→ [cardinal-voting-systems](cardinal-voting-systems.md)]
- **Scale invariance** — multiplying every score by a constant must not change the result. The *range*
  ([0,1] vs [0,100] vs [−42,7]) is irrelevant under sum, average and median; reweighting is where it stops
  being free — RRV fails it, SPAV + KP transform recovers it.
  [→ [cardinal-voting-systems](cardinal-voting-systems.md)]
- **KP (Kotze–Pereira) transform** — split a rated ballot into fractional approval ballots: scored *k* of *m*
  ⇒ approved on *k* of the *m* unit sub-ballots. So score voting **is** approval voting over *m*
  sub-electorates. Verified exact over 20,000 profiles, and the bridge that carries the
  approval-characterization results to score.
  [→ [cardinal-voting-systems](cardinal-voting-systems.md),
  [brandl-peters-approval-characterizations](brandl-peters-approval-characterizations.md)]
- **Approval rating** — a candidate's total as a percentage of the maximum attainable total. The clean way to
  compare totals across methods using different scales.
  [→ [cardinal-voting-systems](cardinal-voting-systems.md)]
- **Utilitarian winner** — the sum-maximising candidate. What score voting is *for*, and what the
  majoritarian criteria are traded against. [→ [cardinal-voting-systems](cardinal-voting-systems.md)]
- **Rated pairwise preference ballot** — a format addressing the one thing rating cannot express: a maximal
  preference between *every* pair once there are more than two candidates.
  [→ [cardinal-voting-systems](cardinal-voting-systems.md)]
- **Approval** — approve any number of candidates, most approvals wins. Weber named it in 1971,
  Brams and Fishburn formalised it in 1978. Its compliance depends on *how voters set their cutoff*, not on
  the tabulation: Condorcet-consistent under the leader rule or dichotomous preferences, capable of electing
  the Condorcet loser under a naive above-average cutoff. Used in Fargo ND 2018–2025 (banned statewide April
  2025) and in St. Louis since 2020. [→ [approval-voting](approval-voting.md)]
- **DYN (Delegable Yes/No) / SODA** — approval plus delegation: approve whom you like, or hand your ballot to
  a candidate to place on your behalf. Forest Simmons and Jameson Quinn respectively. The selling point is
  immunity to manipulated poll data, which matters because approval's leader rule makes the winner a function
  of published expectations. [→ [approval-voting](approval-voting.md)]
- **Score voting (range voting)** — score everyone on a fixed scale, highest total wins. Approval with more
  levels. The only method here that satisfies **IIA** (a candidate's total depends only on scores given to
  them) — but only if voters score absolutely rather than renormalising to the field. Honest score is
  excellent and strategic score is plurality: on Tennessee, sincere scores elect the Condorcet winner and
  min-maxed scores elect the Condorcet loser. That gap is what STAR's runoff exists to close.
  [→ [score-voting](score-voting.md), [star-voting](star-voting.md)]
- **Sum vs. average vs. average-with-quorum** — three rules sharing the name "score voting". Identical while
  every voter rates every candidate, different the moment a ballot has a blank, and they can elect different
  winners. Pirate Party Bavaria uses average-with-quorum. Majority judgment's answer is a fourth: the
  **median**. [→ [score-voting](score-voting.md), [majority-judgment](majority-judgment.md)]
- **Mean vs. median** — the mean moves with every ballot in proportion to how extreme it is, so
  exaggeration pays; the median only moves when a ballot crosses it, so it doesn't. The whole cardinal
  family sorts on this choice, and by the point-summing theorem it is also the participation/strategy
  trade. **Trimmed mean** (Olympic figure skating) is the practical hybrid.
  [→ [majority-judgment](majority-judgment.md)]
- **Grades as language** — Balinski and Laraki's premise that "Excellent" carries an absolute shared meaning
  a private 0–5 scale does not, so ballots can be *compared* rather than merely added. *Judge, don't vote.*
  [→ [majority-judgment](majority-judgment.md)]
- **Blank vs. zero** — an unrated candidate versus one rated 0: the same mark on paper, different states in
  a tabulator, and the thing sum-vs-average turns on. [→ [score-voting](score-voting.md)]
- **Absolute vs. normalised scoring** — score against a fixed internal standard, or rescale so your favourite
  gets the max and your worst the min? Score voting's IIA survives the first and dies on the second — the
  same conditional as approval's fixed-vs-floating cutoff. [→ [score-voting](score-voting.md)]
- **Reweighted range voting (Thiele's method)** — proportional multi-winner score. Used by the Academy for
  the Best Visual Effects nominees and by Pirate Party Germany. [→ [score-voting](score-voting.md)]
- **STAR (Score Then Automatic Runoff)** — score 0–5; the two highest totals become finalists; elect
  whichever finalist more ballots score higher. Proposed Oct 2014 by Mark Frohnmayer as **Score Runoff
  Voting**, Equal Vote's flagship. Monotonic in the mono-raise sense, but fails majority, Condorcet, clone
  independence, later-no-harm and favorite betrayal. No public government election has ever adopted it:
  both Oregon ballot measures lost (Lane County 2018 at 47.5%, Oakridge 2024 at 46%).
  [→ [star-voting](star-voting.md)]
- **Majority judgment (MJ)** — grade everyone on a verbal scale (Excellent … Reject); highest **median**
  grade wins, ties broken by stripping median grades until they separate. Balinski & Laraki, 2007/2010.
  Passes monotonicity, later-no-help and **IIA**; fails Condorcet, majority, consistency and
  **participation** — the last of these provably, by their own theorem. The median is what buys its
  strategy resistance: a bloc that min-maxes swings score totals by 80 points and moves no median at all.
  [→ [majority-judgment](majority-judgment.md)]
- **Highest median rule** — the family: elect the best median grade. Majority judgment, graduated majority
  judgment, usual judgment, and (reportedly) Bucklin. They differ only in how they break median ties, and
  the tiebreak decides real elections. [→ [majority-judgment](majority-judgment.md)]
- **Unified primary** — nonpartisan primary run by approval, top two advance to the general. St. Louis'
  Proposition D variant. [→ [approval-voting](approval-voting.md)]
- **Minor cardinal rules** — the rest of electowiki's single-winner table, listed so the names resolve:
  **Reciprocal Score Voting** (sum, >2 grades), **Chiastic Score Voting** (elect on the highest score *s*
  such that at least an *s*-sized share of voters rate the candidate ≥ *s* — an intersection rule, not a
  sum), **Majority Choice Approval** and **Majority Approval Voting** (median rules on binary ballots).
  [→ [cardinal-voting-systems](cardinal-voting-systems.md)]

### Pricing and delegation

Two methods that adjust *how much say* a voter has rather than how the ballots are counted. Both are aimed
at referenda more than at electing people. All from [sep-voting-methods](sep-voting-methods.md).

- **Negative voting** — vote *for* one candidate (+1) or *against* one candidate (−1). Equivalent to
  approving either a single candidate or everyone but one, so it is approval voting restricted to the two
  extreme ballot shapes.
- **Quadratic voting (Weyl)** — buy *v* votes for *v*² dollars, with the proceeds redistributed pro rata.
  An answer to tyranny of the majority that lets an intense minority outbid a lukewarm majority without
  handing anyone a veto, which is what raising the quota would do. The standard objections are both about
  wealth: whether the outcome beats majority rule in utilitarian terms once incomes differ, and whether any
  vote-buying mechanism can meet a legitimacy requirement (Laurence and Sher 2017).
- **Liquid democracy** — proxy voting where proxies may **re-delegate**, so votes flow transitively to whoever
  is left holding them. Direct democracy without the demand that everyone study every issue. The open
  problems are structural: delegation cycles, and vote mass concentrating on a handful of super-proxies.

### Multi-winner

Everything above elects one person. These fill several seats, and the question changes from "who should win"
to "who should be represented".

- **STV (single transferable vote)** — one transferable ranked vote per voter in a multi-seat district. Set
  a quota; elect whoever reaches it; transfer their **surplus**; when nobody reaches it, eliminate the lowest
  and transfer their pile. **With one seat it is exactly IRV.** Ireland since 1922, Malta, the Australian
  Senate, Tasmania, Scottish and NI local government, Cambridge MA, and the Academy Award nominees.
  [→ [single-transferable-vote](single-transferable-vote.md)]
- **Quota** — the votes that guarantee a seat. **Droop** = ⌊V/(S+1)⌋+1 is the smallest *safe* quota: S+1
  candidates can't all reach it, and one lower isn't safe. **Hare** = V/S is larger, so a *harder* bar.
  The choice changes the winning set in ~15% of random 3-seat profiles.
  [→ [single-transferable-vote](single-transferable-vote.md)]
- **Surplus transfer** — moving an elected candidate's above-quota votes onward. The rule varies by
  jurisdiction — whole-vote/random (Cambridge), **basic Gregory** on the last parcel only (Ireland Senate,
  NI), **WIGM** over all papers (Scotland), **Meek** recomputing the quota as ballots exhaust. WIGM and basic
  Gregory disagree ~12% of the time, which is why "STV" names a family.
  [→ [single-transferable-vote](single-transferable-vote.md)]
- **SNTV (single non-transferable vote)** — STV's ballot without the ranking or the transfers: first
  preferences, top *S* win. Semi-proportional, and the baseline STV must beat — it elects the same set
  ~62% of the time. [→ [single-transferable-vote](single-transferable-vote.md)]
- **Cumulative voting** — SNTV with the single vote made divisible: each voter gets a budget of voting weight
  and may **pile it onto one candidate** or spread it, top *S* win. Two forms in circulation — one vote per
  seat, each cast whole ("plumping" all of them on one candidate is the point), or one vote split into
  fractions that must sum to 1. Semi-proportional by self-organisation rather than by construction: a
  cohesive minority that concentrates while the majority spreads can seat a candidate on well under a
  majority, which is why it keeps being adopted as a **Voting Rights Act settlement remedy** in US county
  and school-board districts, and why Illinois used it for its legislature from 1870 to 1980. Most corporate
  boards still elect this way, weight being shares. The costs are real: the arithmetic is on the voter, so
  spoilage rises and turnout falls; and it is strategically brutal in the way SNTV is — weight given to your
  second choice is weight taken from your first, so concentrating too hard wastes votes and spreading too
  thin elects nobody, and the optimal play needs a poll. Note the §4 heading **Cumulative** above covers
  something unrelated: Bucklin's cumulative *tallying* of preference levels, not a divisible vote. The
  approval-ballot literature also uses "cumulative" for a third thing — the (1, ½, ⅓, …) equal-split
  scoring rule in §5.
- **Discrete cumulative voting** — cumulative voting with **indivisible tokens** instead of a fractional
  budget: *k* whole votes, distributed however you like. The variant nearly every real implementation uses,
  because fractions are what generate invalid ballots — a voter whose shares fail to sum to 1 has spoiled
  theirs, while tokens can only be miscounted, not mis-normalised. The tradeoff is granularity: *k* tokens
  over *m* candidates is a coarse cardinal ballot, and with small *k* it collapses toward SNTV.
  [→ [mdi-trivia-cards](mdi-trivia-cards.md)]
- **District magnitude** — seats per district. The real determinant of how proportional a result is; three
  seats means a 25% threshold. Shrinking districts is how a government tunes STV toward large parties
  without appearing to change the rules. [→ [single-transferable-vote](single-transferable-vote.md)]
- **Bloc methods (bloc approval / bloc score / bloc STAR)** — top *k* totals win, no reweighting. The
  cardinal analogue of block plurality, and **not proportional**: a coherent majority takes every seat. The
  reason the sequential family below exists. [→ [cardinal-voting-systems](cardinal-voting-systems.md)]
- **Sequential proportional cardinal methods** — elect one at a time, **reweighting** ballots that already
  helped elect someone, which is the surplus transfer's cardinal analogue. RRV (picks the Academy's Visual
  Effects nominees), SPAV, Sequentially Spent Score, Allocated Score, Sequential Monroe, Sequential
  Phragmén, Sequential Ebert. [→ [cardinal-voting-systems](cardinal-voting-systems.md),
  [score-voting](score-voting.md), [approval-voting](approval-voting.md)]
- **Thiele / Monroe / Phragmén / Vote Unitarity** — the four reweighting philosophies, i.e. four theories of
  what proportionality *is*. Thiele: influence decays harmonically in how many winners you already got
  (diminishing returns on satisfaction). Monroe: each winner is assigned a quota of voters who are then
  spent (representation as partition). Phragmén: winners impose a load spread over their supporters,
  minimise the maximum load (fairness as evenness of burden). Vote Unitarity: one vote's worth of influence,
  spent down. **The diagnostic is the party-list degenerate case** — Thiele methods collapse to a
  **highest-averages** divisor rule, Monroe and Vote Unitarity to **Hamilton**, which drags the whole
  Balinski–Young quota-vs-monotonicity trade into cardinal PR.
  [→ [cardinal-voting-systems](cardinal-voting-systems.md),
  [math-in-society-lippman](math-in-society-lippman.md)]
- **Hare Quota Criterion** — a solid coalition worth a Hare quota must win a seat. What the reweighting phase
  is aiming at, and the cardinal counterpart of PSC.
  [→ [cardinal-voting-systems](cardinal-voting-systems.md)]
- **Sequentially Spent Score (SSS)** — the Vote Unitarity method. Score ballots; each round elect the
  highest weighted total, then every voter **spends** exactly the stars they gave that winner, with
  "change" returned if the winner drew more than a Hare quota of score. Keith Edmonds; also Sequentially
  Subtracted Score or Unitary Cardinal Voting. **Strip the spending step and it is exactly Bloc Score** —
  which is what a `verbosity`-gated engine bug did in production, costing a 38% minority bloc its
  proportional seat. Its party-list case is **Hamilton**, verified at 100% agreement over 2,000 profiles.
  [→ [sequentially-spent-score](sequentially-spent-score.md)]
- **Vote unitarity** — vote weight as a *conserved budget*: (VU1) **proportionate spending**, the cost of
  electing a candidate never exceeds the score you gave them; (VU2) **unitary transformation**, residual
  budget is always the initial unit minus what has been spent. Written to sit between the two ways
  reweighting goes wrong — STV and Allocated Score **over**-remove influence (a 1-of-5 supporter can be
  allocated entirely), RRV **under**-removes it (a max-score supporter keeps half a ballot they already
  used). [→ [sequentially-spent-score](sequentially-spent-score.md)]
- **Scaling vs. capping** — the two ways to apply a reduced ballot weight to the candidates still standing.
  Scaling multiplies every remaining score by the weight; capping truncates each score *at* the weight.
  Capping is the more intuitive reading and **fails Justified Representation**, which is why SSS abandoned
  it. [→ [sequentially-spent-score](sequentially-spent-score.md)]
- **Justified Representation (JR)** — a cohesive group worth a quota must get *someone* they support. The
  standard fairness floor for multi-winner approval/score rules, and the axiom that killed SSS's capping
  variant. Weaker than proportionality, and much easier to check.
  [→ [sequentially-spent-score](sequentially-spent-score.md)]
- **Priceability** — a winner set is priceable if voters' budgets can be assigned to winners consistently at
  a common price per seat. Plain SSS is not; its Sequentially Shrinking Quota variant is.
  [→ [sequentially-spent-score](sequentially-spent-score.md)]
- **Vickrey quota** — the smaller of a Hare quota and the runner-up's total score. Charging a winner only
  what it took to beat the field, by analogy with Vickrey auctions.
  [→ [sequentially-spent-score](sequentially-spent-score.md)]
- **Optimal proportional methods** — choose the whole winner *set* at once by maximising a quality function,
  usually by trying every set: Proportional Approval Voting (PAV), Monroe's method, Ebert's method,
  max-Phragmén, Harmonic Voting, PAMSAC. Combinatorial in the seat count. **Ebert's method fails
  monotonicity.** [→ [cardinal-voting-systems](cardinal-voting-systems.md)]

## 5. Criteria and properties

Every one of these appears as a row in LeGrand's compliance table with no definition given.

- **Pareto-optimality (unanimity)** **[LeGrand]** — if every voter ranks A over B, B must not win.
- **Majority criterion** **[LeGrand]** — a candidate ranked first by an absolute majority must win.
- **Majority criterion for rated ballots** — the cardinal weakening: if a candidate is preferred *and*
  max-scored by an absolute majority, that candidate must win. Strictly weaker than the line above, and the
  cleanest statement of majority judgment's position — **MJ satisfies this while failing the ordinary
  majority criterion.** [→ [cardinal-voting-systems](cardinal-voting-systems.md),
  [majority-judgment](majority-judgment.md)]
- **Mutual majority criterion** **[LeGrand]** — if a majority ranks every member of a set S above every
  non-member, the winner must come from S. The multi-candidate generalization of the majority criterion.
- **Condorcet criterion** **[LeGrand]** — a Condorcet winner, when one exists, must win.
- **Smith criterion** **[LeGrand]** — the winner must come from the Smith set. Strictly stronger than Condorcet.
- **Schwartz criterion** **[LeGrand]** — the winner must come from the Schwartz set.
- **Clone independence** **[LeGrand]** — adding or removing a *clone* (a candidate ranked adjacently to
  another on every ballot) must not change which non-clone wins. Failing it creates the
  **candidate-saturation incentive**: parties gain by running extra similar candidates.
- **Monotonicity** **[LeGrand]** — ranking the winner *higher*, changing nothing else, must never make them
  lose (and ranking a loser lower must never make them win). IRV and every Borda-elimination method fail this.
- **Reverse symmetry** **[LeGrand]** — reverse every ballot and the unique winner must not still win. Nine of
  LeGrand's 13 scored methods fail it; verified counterexamples for all nine are in the
  [note](reverse-symmetry-examples.md).
- **Reinforcement (consistency)** **[LeGrand]** — if the same candidate wins two separate electorates, they
  must win the combined electorate. **Borda is the only method on LeGrand's chart that satisfies it** — a
  verified Coombs counterexample is in the [note](legrand-ranked-ballot-methods.md). On approval ballots the
  same axiom (stated as `f(P) ∩ f(P′) = f(P + P′)` whenever the intersection is non-empty) is the engine of
  every known characterization of approval voting.
  [→ [brandl-peters-approval-characterizations](brandl-peters-approval-characterizations.md)]
- **Nonmanipulability (strategy-proofness)** **[LeGrand]** — no voter ever gains by ranking insincerely.
  **Every** ranked method fails this; see Gibbard–Satterthwaite.
- **Independence of irrelevant alternatives (IIA)** — adding or removing a losing candidate must not change
  who wins. No ranked method satisfies it (Arrow). **Score voting does**, since a candidate's total depends
  only on the scores given to them — but only under absolute scoring; voters who renormalise to the field
  break it, exactly as a floating approval cutoff does. STAR loses it again to the runoff.
  [→ [score-voting](score-voting.md), [approval-voting](approval-voting.md), [star-voting](star-voting.md)]
- **IIA2 / IIA2\* / IIA2†** *(Horn's labels)* — the three things called IIA, kept apart. **Arrow's Condition
  3** is about *reordering* candidates other than X and Y in the voters' rankings. **IIA2** is the popular
  reading — *adding or removing* an alternative mustn't reverse a judgement between two others; this is what
  the Morgenbesser apple/blueberry/cherry joke is about, and it is not Arrow's condition. **IIA2\*** is its
  approval analogue, stated over approval statuses rather than rankings. **IIA2†** is the conditional,
  property-α form: your approval of X is unchanged when the option set grows or shrinks. Approval fails
  IIA2† — Horn concedes this and argues the failure isn't irrational, but Nagel's objection, quoted in the
  paper's own footnote 14 and never answered, is that failing it reopens agenda control by *adding or
  subtracting alternatives*. Which is the point of the compliance table's four rows: the cutoff is what moves.
  [→ [horn-three-virtues-approval](horn-three-virtues-approval.md), [approval-voting](approval-voting.md)]
- **Sen's property α (1970)** — if X is chosen from a set, X is chosen from every subset containing it.
  Choice-theoretic rather than electoral, and the ancestor of IIA2†; the sharper of the two contraction
  conditions people mean when they say "irrelevant alternatives."
- **Anonymity** — the result depends only on how many voters cast each ballot, never on *which* voter cast
  it. Swap two voters' ballots and nothing changes. A dictatorship is the textbook failure: swap the
  dictator's ballot with anyone who voted differently and the winner moves.
- **Neutrality** — the result depends only on the ballots, never on *which candidate is which*. Relabel the
  candidates and the winner is relabelled with them. Failed by any default winner, and — quietly — by the
  **tiebreaking ranking** of §2: a fixed candidate order used to settle ties is exactly a rule that treats
  one candidate better than another for reasons no voter supplied.
- **Near-decisiveness** — the method returns a single winner in every profile except an exact tie. Weaker
  than demanding a winner always, and the form May's Theorem needs.

### Axioms from the approval-ballot literature

Stated for **ballot aggregation functions** — rules mapping approval profiles to a non-empty set of winners,
ties included as outputs rather than something to break. All of these appear in the eight characterizations
of approval voting. [→ [brandl-peters-approval-characterizations](brandl-peters-approval-characterizations.md)]

- **Faithfulness** — a one-voter electorate elects exactly that voter's approved set. `f(A) = A`. Its only
  real job in the theorems is to exclude two jokes: **−AV** (elect the *least* approved) and **TRIV**.
- **Disjoint equality** — two voters with non-overlapping ballots tie everything either approved.
  `f(A + B) = A ∪ B` when `A ∩ B = ∅`.
- **Continuity (overwhelming majority)** — if `f(P) = {a}`, then adding enough copies of `P` to any other
  profile also elects `a`. Young's axiom; the same one Balinski–Laraki use against majority judgment
  [→ [majority-judgment](majority-judgment.md)].
- **Cancellation** — all approval scores equal ⇒ everything ties.
- **Kelly's extension / Kelly-manipulability** — the weakest set-preference extension: you prefer set *Y* to
  *Z* only if all of *Y* is approved or none of *Z* is. A manipulation under it is unambiguous. Approval is
  immune to unilateral ones — but **not to coordinated ones**: in `{a} + {b} + 2{c}` approval elects *c*,
  and the *a*- and *b*-voters both switching to `{a,b}` gives all three a share.
- **Fishburn's extension** — a refinement of Kelly's under which approval is *still* strategyproof.
- **Independence of clones / losers / Pareto dominated / never-approved alternatives** — four strengths of
  "a candidate who can't win can't matter", the paper's formalization of the spoiler effect. Each one
  characterizes approval when paired with consistency.
- **Scoring rule on approval ballots** — a vector (s₁, …, s_m) scoring by ballot *size*. Approval is
  (1, 1, …, 1); **plurality is (1, 0, …, 0)** — the rule that ignores every non-singleton ballot, and the
  formal shadow of universal bullet voting; cumulative voting is (1, ½, ⅓, …).
- **Later-no-harm** — expressing support for a later choice must not hurt your earlier ones. Approval
  necessarily fails it — that failure is the same fact as its monotonicity, seen from the other side.
  STAR fails it too: a mid-range score can lift a rival into the runoff *past* your favorite.
  IRV passes it, which is exactly why it can ignore backup preferences and center-squeeze.
  [→ [approval-voting](approval-voting.md), [star-voting](star-voting.md)]
- **mono-raise vs. mono-raise-delete** **[Woodall]** — two monotonicity variants that come apart under STAR.
  *mono-raise*: raising a candidate must not hurt them (STAR passes). *mono-raise-delete*: raising them
  **and zeroing everyone now below them** must not hurt them (STAR fails — deleting a candidate can swap the
  runoff for one your favorite loses). [→ [star-voting](star-voting.md)]
- **Sincere favorite (favorite-betrayal) criterion** — supporting your true favorite must never be
  counterproductive. Approval passes under every voter model; Hare fails it. STAR fails it too, but only
  narrowly: equal-rating your favorite with a compromise usually suffices, and a genuine violation needs a
  profile where it doesn't. [→ [approval-voting](approval-voting.md), [star-voting](star-voting.md)]
- **Participation criterion** — casting a sincere ballot must never make the result worse for you than
  staying home. Approval and score pass; **STAR and majority judgment fail**. Under STAR a bloc's middle
  score can lift a rival into the runoff past their own favorite. Under MJ the failure is *forced*: by
  Balinski and Laraki's own theorem the only methods satisfying participation plus continuity are
  **point-summing** methods, so any non-summing rule has no-show paradoxes by construction.
  [→ [score-voting](score-voting.md), [star-voting](star-voting.md),
  [majority-judgment](majority-judgment.md)]
- **Point-summing method** — Σ *f*(score) for a monotonic *f*: score voting and the positional rules.
  Balinski and Laraki proved these are the *only* consistent methods, and the only ones satisfying
  participation plus continuity — which is why the mean-vs-median choice is really a
  participation-vs-strategy-resistance choice. [→ [majority-judgment](majority-judgment.md)]
- **Median voter criterion** — the winner should be the candidate nearest the median voter. Majority
  judgment, the highest-*median-grade* rule, **fails** it: on Laslier's 650-voter left–right example it
  elects Left while the Condorcet winner and the score winner are both Center, because its tiebreak rewards
  the larger homogeneous wing. [→ [majority-judgment](majority-judgment.md)]
- **No-show paradox** — a bloc turns out and gets a worse result than by staying home; the concrete form of
  a participation failure. [→ [majority-judgment](majority-judgment.md),
  [sep-voting-methods](sep-voting-methods.md)]

The four axioms every characterization result starts from, and the two it usually cannot have. All from
[sep-voting-methods](sep-voting-methods.md).

- **Anonymity** — swapping two voters' ballots changes nothing; the outcome depends only on *how many* cast
  each ballot. Usually not an axiom at all in practice but a **choice of domain**: work with anonymized
  profiles (a function from ballots to counts) and anonymity is the type signature rather than a condition.
- **Neutrality** — swapping two candidates on every ballot swaps them in the result. The candidate-side
  mirror of anonymity, and stronger than it looks: it alone rules out resoluteness, since a profile that is
  its own image under a rotation of the candidates must have a winner *set* that is too, and no singleton is.
- **Universal domain** — the method is a total function; no profile may be refused.
- **Unanimity (Pareto)** — if every voter ranks A above B, B does not win.
- **Positive responsiveness** — a candidate who is winning or tied and then gains ground on some ballot
  becomes the **unique** winner. Strictly stronger than monotonicity, and the axiom that does the work in
  May's Theorem.
- **Resoluteness** — always exactly one winner, no ties. **Incompatible** with universal domain + anonymity
  + neutrality + unanimity once there are three or more candidates, so every method here is really a
  set-valued rule plus a tiebreak that lives outside the theory.
- **Reinforcement (consistency across districts)** — if two disjoint electorates share a winner, the
  combined electorate's winners are exactly the shared ones. Scoring rules satisfy it because scores add;
  **every Condorcet consistent method fails it**, which is the multiple-districts paradox.
- **Proportionality for solid coalitions (PSC)** — if a group ranks some set of candidates above all others
  on every ballot and is worth *k* quotas, that set gets at least *k* seats. STV's actual formal guarantee,
  and weaker than "proportional" in the everyday sense: it says nothing about voters who don't form solid
  blocs. [→ [single-transferable-vote](single-transferable-vote.md)]
- **Backward tiebreak** — resolve a tie on current counts by looking at an earlier round's counts (usually
  first preferences). Decides round 4 of the STV article's worked example; swapping it for an alphabetical
  rule makes one-seat STV and IRV disagree on 15 of 4,000 profiles.
  [→ [single-transferable-vote](single-transferable-vote.md)]
- **Exhausted ballot** — no usable preference left, so it stops transferring and sits out the rest of the
  count. Enough exhaustion lets STV candidates win on partial quotas.
  [→ [single-transferable-vote](single-transferable-vote.md)]
- **Equal Support** — STAR's name for a ballot that scores both finalists the same and so casts no vote in
  the automatic runoff. The scored-ballot analogue of an exhausted ballot: counted, but unable to help
  either finalist. Note that "preference" in BetterVoting's runoff legend means a *strict* preference
  between the two finalists, not "ranked or scored anyone at all".
  [→ [results-chart-denominators](results-chart-denominators.md)]
- **Decisiveness** — how often a method needs a tiebreaker at all. Black is the most decisive of LeGrand's
  set, Copeland the least.
- **Strategic straightforwardness** — how easy it is to vote honestly without regret; a softer, practical
  cousin of nonmanipulability. [→ [rcv-and-core-support](rcv-and-core-support.md)]

## 6. Failure modes and strategy

- **Spoiler effect** — a losing candidate's presence changes which of the others wins.
- **Center squeeze** — a broadly acceptable middle candidate is eliminated early because first-choice votes
  split to the flanks (Begich, Alaska 2022). [→ [rcv-and-core-support](rcv-and-core-support.md)]
- **Favorite betrayal** — ranking your true favorite lower helps them, or helps you. LeGrand's Katy/Luke/Mary
  election is a minimal example under Hare.
- **Lesser-evil coordination pressure** — voters for similar candidates must agree in advance whom to back;
  the plurality pathology that Carey reproduces.
- **Candidate saturation** — flooding a race with similar candidates to exploit a clone-dependent method.
- **Duverger's Law** — single-member plurality districts tend toward a **two-party system**; the companion
  *Duverger's hypothesis* is that proportional and multi-member systems tend toward more. Duverger, 1951.
  This is the two entries above it at the scale of a party system rather than an election: lesser-evil
  coordination pressure is the voter-side mechanism, candidate saturation the candidate-side one, and the
  party system is what they compound into over repeated elections. Called a law, but it is an empirical
  regularity with standing exceptions — Canada, India and the pre-2015 UK all run single-member plurality
  and sustain more than two parties, usually where third parties are regionally concentrated enough to win
  seats rather than merely votes. The mechanism is the durable part; the prediction is not.
  [→ [mdi-trivia-cards](mdi-trivia-cards.md)]
- **Bullet voting** — approving (or ranking) only your favorite. Approval's characteristic degeneracy: if
  everyone bullet votes, approval *is* plurality. 79% of voters did it in the 1987 MAA election, 80%+ in
  Dartmouth's student elections, and ~80% at the IEEE — which is the reason IEEE gave for repealing approval
  in 2002. Three measured electorates, all near four in five. [→ [approval-voting](approval-voting.md)]
- **Chicken dilemma / Burr dilemma** — two allied frontrunners' camps each bullet-vote to avoid helping the
  other, and a third candidate wins. Named for the Jefferson–Burr tie of 1800 — and **probably misnamed**,
  as CRV points out: 1800 was a 73–73 tie with Adams back on 65, a coordination failure rather than a third
  candidate slipping through. Nagel 2007. The standing rebuttal is that it assumes *asymmetric* strategic
  sophistication — canny A and B camps, naive C camp. [→ [approval-voting](approval-voting.md)]
- **Compromising** — approving a candidate you find unacceptable to block a worse one. Unlike favorite
  betrayal it never requires demoting your favorite. [→ [approval-voting](approval-voting.md)]
- **Runoff monopolisation** — STAR's clone failure: two near-identical candidates take *both* finalist
  slots, so the runoff is decided among allies and everyone else is locked out. The mirror image of Borda's
  clone problem — Borda rewards flooding the field, STAR rewards flooding its top.
  [→ [star-voting](star-voting.md)]
- **Runoff abstention** — under STAR, scoring both finalists equally removes your ballot from the runoff.
  The hidden cost of equal-rating, and why an all-5s ballot is nearly worthless.
  [→ [star-voting](star-voting.md)]
- **Tactical maximisation (min-maxing)** — scoring only 5s and 0s under score voting, since every point
  given to a rival counts against your favorite. The specific problem STAR's runoff was added to blunt.
  [→ [star-voting](star-voting.md)]
- **Agenda-setting manipulation** — controlling the *order* in which options are voted on pairwise, so that a
  sincere majority position is knocked out before the final round. The standard example is the 1956 Powell
  Amendment: opponents of school aid vote *for* the anti-discrimination amendment to make the bill
  unpassable, killing it against the status quo. Riker built a case against democracy on it; Mackie (2003)
  and Gilmour (2001) argue no such manipulation has ever been conclusively demonstrated in Congress. Two
  things worth keeping straight. The defence against it is **voting on all the options at once** — on the
  standard profile plurality, Borda, IRV and pairwise majority all elect the compromise, so this is a
  property of the agenda, not of the ballot. And it is distinct from **agenda control by adding or removing
  alternatives**, which simultaneity does *not* cure; see IIA2† in §5.
  [→ [horn-three-virtues-approval](horn-three-virtues-approval.md)]
- **Indeterminacy (Saari–Van Newenhizen)** — with voter preferences fixed, approval can *sincerely* elect
  any candidate, Condorcet winner or Condorcet loser, depending only on where voters put their cutoffs.
  Read as a defect by Saari, as responsiveness to intensity by Brams. The cheapest concrete instance is
  Horn's own worked example: on one 426-voter profile, enumerating all 32 sincere cutoff combinations elects
  the Condorcet winner in 24, the Condorcet **loser** in 5, and the status quo — the option a 77% majority
  opposes — in 3. Approval's answer there is a function of the cutoffs, not of the preferences.
  [→ [approval-voting](approval-voting.md), [horn-three-virtues-approval](horn-three-virtues-approval.md)]
- **Bland-winner objection** — the claim that Condorcet methods elect inoffensive nobodies.
  [→ [rcv-and-core-support](rcv-and-core-support.md)]
- **Free riding** — in a multi-winner method, withholding support from a candidate who is going to win
  anyway so your ballot keeps its weight for the next seat. The strategy that only *proportional* methods
  are exposed to: single-member systems are immune to it by construction, which is why the reweighting rule
  is where multi-winner strategy lives. [→ [cardinal-voting-systems](cardinal-voting-systems.md)]

Paradoxes of aggregating *issues* rather than candidates, plus two pieces of vocabulary for talking about how
often any of this happens. All from [sep-voting-methods](sep-voting-methods.md).

- **Condorcet's other paradox (Fishburn 1974)** — a profile where electing the Condorcet winner requires a
  scoring rule that gives **more points for second place than for first**. Condorcet's 81-voter example is
  the original: Score(A) − Score(B) = −8(s₁ − s₂), so A can only win if s₂ > s₁.
- **Multiple elections paradox (Brams, Kilgour & Zwicker 1998)** — vote on propositions separately and the
  winning *package* can be one that **no voter cast**. Thirteen voters, three propositions, N wins 7–6 on
  each, and the outcome NNN has zero supporters. Aggregating issue by issue and aggregating packages are
  different questions with different answers.
- **Anscombe's paradox (1976)** — a majority of voters can be on the losing side of a majority of issues.
  Five voters, three issues, and voters 1, 2 and 3 each lose two of the three.
- **Ostrogorski's paradox (1902)** — the same profile with candidates instead of referenda: the candidate
  holding the **minority** position on every issue wins 3–2, because voters back whoever agrees with them on
  most issues. The party-platform version of the multiple elections paradox.
- **Condorcet component** — a perfectly symmetric majority cycle: *n* voters for each of `ABC`, `BCA`, `CAB`.
  Contributes an equal score to every candidate under any positional rule, and a 2:1 margin around the cycle
  in the majority relation — so it is invisible to Borda and decisive for Condorcet. In the 81-voter example
  the Condorcet winner's margin is **+1**, assembled from +10 contributed by a 30-voter component and −1 by a
  3-voter reverse component against a real −8 among the voters in no cycle.
- **Impartial culture** — the standard null model: every ranking equally likely, independently per voter. It
  gives the quoted paradox frequencies (five candidates and seven voters: 21.5% chance of no Condorcet
  winner, rising to 25.1% as the electorate grows), and it is a **worst case** — Tsetlin et al. 2003 show any
  deviation lowers the cycle probability, and Regenwetter's empirical datasets find the usual methods
  agreeing outright. Quote a paradox probability without naming a distribution and this is the one being
  assumed.

## 7. Concepts from the values argument

All from [rcv-and-core-support](rcv-and-core-support.md).

- **Core support** — enthusiasm-based backing. Coherent only as a *cardinal* notion, not as "first-place
  rankings," since that count depends on who else is running.
- **Broad support** — acceptability to a wide swath of voters.
- **Fungibility of support** — under Condorcet, extra broad support can offset less core support; under IRV,
  too few first choices is an absolute veto.
- **Equal incentives argument** — methods where opposing ballots cancel symmetrically give candidates a
  reason to court *every* voter.
- **Core × broad method**, **threshold method** — proof-of-concept cardinal rules rewarding both.

## 8. Weighted voting and apportionment

All from [math-in-society-lippman](math-in-society-lippman.md). A separate literature from the rest of
these notes: not "who wins," but "how much say does each player already have," and "how do you split a
fixed number of seats."

- **Weighted voting system** — written `[q: w₁, w₂, …]`, where *q* is the **quota** (the weight needed to
  pass a motion) and *wᵢ* are the players' weights. The quota must be *more than* half the total weight,
  or a proposal and its negation can both reach it.
- **Coalition / winning coalition** — any group voting the same way; winning if its combined weight meets
  quota.
- **Critical player** — one whose departure turns a winning coalition into a losing one.
- **Dictator / veto power / dummy** — a player who meets quota alone; a player critical in *every* winning
  coalition; a player critical in *none*. A dummy has weight but no power.
- **Banzhaf power index** — a player's share of all critical-player occurrences across every winning
  coalition. Penrose 1946, reintroduced by Banzhaf 1965. In Nassau County's `[58: 31,31,28,21,2,2]` the
  three largest districts hold ⅓ of the power each and the other three hold **none** — North Hempstead
  has 18.3% of the weight and 0% of the power, which is the disparity Banzhaf litigated.
- **Shapley–Shubik power index** — a player's share of the *n*! **sequential coalitions** in which they
  are **pivotal** (the one whose joining reaches quota). Shapley & Shubik 1954. Usually close to Banzhaf,
  not identical: order of joining matters here and does not there.
- **Apportionment** — dividing a fixed whole number of seats among groups in proportion to population.
- **Quota (apportionment)** — a group's exact proportional share, population ÷ **standard divisor**;
  **lower quota** is its floor.
- **Quota rule** — every group's final seat count is its lower or upper quota. Satisfied by Hamilton and
  Lowndes; violable by every divisor method.
- **Divisor methods** — adjust the divisor until the rounded quotas total correctly. **Jefferson** rounds
  down (favors large states), **Adams** up (favors small), **Webster** to nearest, **Huntington–Hill** by
  the geometric mean of the bracketing integers — the last is US law since 1941.
- **Alabama paradox** — a group *loses* a seat when the total number of seats *increases*. Avoiding it is
  **house monotonicity**.
- **Population paradox** — a group whose population grows faster than another's transfers a seat *to* it.
  Avoiding it is **population monotonicity**.
- **New States paradox** — adding a new group with its own fair share changes the allocation among the
  existing ones.

## 9. Theorems

- **May's Theorem (1952)** — the floor under everything else in this section, and the only unqualified
  *positive* result here. With exactly **two** candidates, **anonymity + neutrality + monotonicity**
  characterize the **quota methods**: fix a threshold and elect whoever reaches it. Add
  **near-decisiveness** and the threshold is forced to exactly half the electorate — **simple majority,
  uniquely**. The squeeze is short: below half, both candidates can reach the quota; above half, neither
  need to; only at half is exactly one guaranteed to, barring an exact tie.
  Two cautions. May's own 1952 statement uses **positive responsiveness** (a strictly stronger monotonicity:
  a candidate who gains a supporter and loses none must go from tie to win), which delivers simple majority
  directly; the weaker plain-monotonicity version is what yields the quota-method family, and popular
  presentations slide between the two. And **"quota method" here is not the quota of §4** (the multi-winner
  Droop/Hare threshold) **nor the quota rule of §8** (apportionment) — three unrelated uses of the word.
  What the theorem really says is that the entire subject is a consequence of having three or more
  candidates: with two, the answer is settled and provably unique.
  A third axiom list is in circulation: the SEP entry states it as **neutrality + anonymity + unanimity +
  positive responsiveness**, and the unanimity is redundant — brute force over every neutral rule on
  anonymized two-candidate profiles (n = 3…6) leaves exactly one rule standing without it, and that rule is
  simple majority. Three sources, three lists, one theorem.
  [→ [mdi-trivia-cards](mdi-trivia-cards.md), [sep-voting-methods](sep-voting-methods.md)]
- **Gibbard–Satterthwaite theorem** — no deterministic ranked method with three or more candidates can be both
  non-dictatorial and strategy-proof. This is why LeGrand's "nonmanipulable?" row is uniformly NO: the design
  target is making manipulation *hard*, not impossible.
- **Fishburn's theorem (1974)** — for every *m* ≥ 3 there is a profile with a Condorcet winner such that
  **every** scoring rule ranks at least *m* − 2 candidates above them. The general form of what the worked
  examples keep showing one profile at a time: no positional rule is Condorcet consistent, and not merely by
  a whisker. For *m* = 3 the smallest witness takes **11 voters** — `2 ACB, 3 BAC, 2 BCA, 4 CBA`, where the
  Condorcet winner C is beaten by exactly one point under every scoring vector, because B has one more first
  place and the same number of seconds. Condorcet's own 81-voter example is *not* a witness: at s₁ = s₂ it
  ties. [→ [sep-voting-methods](sep-voting-methods.md)]
- **Moulin's theorem (1988)** — with **four or more** candidates, every Condorcet consistent method is
  susceptible to the **no-show paradox**. The ordinal twin of Balinski and Laraki's participation result for
  point-summing methods. The bound is on candidates, not a safety guarantee below it: minimax survived all
  12,369 three-candidate profiles up to 11 voters, while Black's Procedure — equally Condorcet consistent —
  fails on three candidates and eight voters. [→ [sep-voting-methods](sep-voting-methods.md)]
- **Young's characterization of scoring rules (1975)** — anonymity + neutrality + **reinforcement** +
  continuity, if and only if the method is a scoring rule. Since reinforcement is exactly the
  multiple-districts property, this says the **scoring rules are precisely the district-safe methods** — and
  with Zwicker's converse (every Condorcet consistent method fails reinforcement) it splits the ranked
  methods cleanly in two. [→ [sep-voting-methods](sep-voting-methods.md)]
- **Fishburn (1978b) / Alós-Ferrer (2006)** — on approval ballots, **faithfulness + cancellation +
  reinforcement** characterize approval voting, and neutrality comes free (Alós-Ferrer). The variable-domain
  ancestor of the eight Brandl–Peters characterizations.
  [→ [brandl-peters-approval-characterizations](brandl-peters-approval-characterizations.md),
  [sep-voting-methods](sep-voting-methods.md)]
- **Myerson's abstract scoring rules (1995)** — treat a ballot as a function from candidates to numbers and
  score by summing. Plurality, approval, Borda, range, cumulative voting and "formal utilitarian" are then
  one family distinguished only by which functions count as legal ballots, characterized by reinforcement,
  universal domain, neutrality and continuity. The frame in which the ordinal/cardinal split stops being a
  split. [→ [sep-voting-methods](sep-voting-methods.md)]
- **Balinski–Laraki cancellation result (2010)** — **no Condorcet consistent method cancels properly**, where
  *cancelling properly* means that adding a **Condorcet component** (a perfectly symmetric majority cycle,
  each ranking held by equally many voters) never changes the winner. Saari's argument that such a component
  is noise, turned into an impossibility. Borda cancels properly by construction — a component gives every
  candidate the same score — which is the sharpest available statement of the Borda-vs-Condorcet
  disagreement. [→ [sep-voting-methods](sep-voting-methods.md)]
- **Condorcet Jury Theorem** — the one result here from the **epistemic** side of the subject rather than the
  procedural one. If each voter independently has probability > ½ of picking the objectively better of two
  options, the probability that the majority picks it rises to certainty with the electorate. Condorcet 1785,
  first proved by Laplace. So majority rule is singled out twice over on two candidates — by May's Theorem on
  fairness grounds and by this on accuracy grounds. Young extended the idea past two options and showed
  **Borda count is the maximum-likelihood estimator** of the best candidate under a natural noise model,
  which is a wholly different argument for Borda than any compliance table gives. Its two premises —
  independence and uniform competence — are the standard targets (Dietrich 2008).
  [→ [sep-voting-methods](sep-voting-methods.md)]
- **Myerson–Weber voting equilibrium** — rational-voter model for approval: approve every candidate with a
  positive **prospective rating** (utility weighted by the probability your vote is pivotal in each pairwise
  tie). Approving your favorite and rejecting your least favorite are dominant strategies.
  [→ [approval-voting](approval-voting.md)]
- **Leader rule (Laslier)** — the practical special case: approve everyone you prefer to the expected
  leader, plus the leader if you prefer them to the expected runner-up. If everyone plays it, the
  equilibrium elects the Condorcet winner when one exists — where **"equilibrium" is load-bearing**. It is a
  fixed point requiring the expected top two to *be* the top two; believe the wrong pair and a third candidate
  can win on every ballot while the Condorcet winner loses. CRV's AppCW page states this as a theorem about
  elections, which it is not. [→ [approval-voting](approval-voting.md)]
- **Arrow's impossibility theorem** — no ranked method can simultaneously satisfy unrestricted domain,
  Pareto, independence of irrelevant alternatives, and non-dictatorship. Applies to *methods*; arguments about
  an idealized preference-aggregation *standard* are not bound by it.
  Two over-readings worth naming, because both are in print. **Dropping "ranked"** turns it into a claim
  about every voting method, which is how a textbook comes to condemn approval on the page before
  introducing it. And **"Arrow proves cycles are unavoidable"** confuses the theorem with the Condorcet
  paradox: the intransitivity belongs to the **pairwise majority relation**, which is one input a ranked
  method may or may not consult. Borda returns a three-way tie on the standard cycle; ranked pairs and
  Schulze emit a transitive order on every profile. Approval, score, STAR and majority judgment are all
  outside the theorem's scope, since it quantifies over ordinal rules and none of them is one — but **outside
  the theorem is not the same as satisfying its conditions**, which is the third over-reading and the one
  cardinal advocacy makes. The escape is also not free: Sen extended the framework to cardinal utilities and
  found that measurability alone doesn't buy anything — **without interpersonal comparability the
  impossibility survives intact**. A cardinal method escapes by assuming your 5 and my 5 are the same
  quantity, which Arrow's framework deliberately withholds and the ballot cannot enforce. That, plus a winner
  depending on information the preference profile doesn't contain (see **Indeterminacy** in §6), is what the
  escape actually costs.
  [→ [rcv-and-core-support](rcv-and-core-support.md), [math-in-society-lippman](math-in-society-lippman.md),
  [horn-three-virtues-approval](horn-three-virtues-approval.md)]
- **Inada's condition (1969)** — under **dichotomous preferences** the majority relation is **transitive**,
  and it orders candidates exactly by approval score. So on that domain a Condorcet cycle cannot occur at
  all, the approval winners are precisely the majority-maximal candidates, and every Smith/Schwartz/beatpath
  construction in §3 above is idle. This is the fact the whole approval-characterization literature rests on.
  [→ [brandl-peters-approval-characterizations](brandl-peters-approval-characterizations.md)]
- **Young–Levenglick (1978)** — with **ranked** ballots, no rule that elects weak Condorcet winners when they
  exist can satisfy consistency. Worth pairing with the line above: the *same* two axioms are incompatible on
  the ranked domain and **jointly characterize approval** on the dichotomous one. The clearest available
  statement of what the ballot format itself changes.
  [→ [brandl-peters-approval-characterizations](brandl-peters-approval-characterizations.md)]
- **Brandl–Peters characterizations (2022)** — eight of them, each pairing consistency with one headline
  axiom (strategyproofness, Condorcet, avoiding Condorcet losers, unanimous majorities, or one of four
  spoiler-independence conditions) plus housekeeping axioms that vary by theorem. All reduce to one base
  theorem: **consistency + faithfulness + disjoint equality force approval voting**.
  [→ [brandl-peters-approval-characterizations](brandl-peters-approval-characterizations.md)]
  **The word "ranked" is load-bearing** and textbooks drop it: cardinal methods take non-ordinal ballots,
  so the theorem's hypothesis does not reach them. Lippman's *Math in Society* states it for "a voting
  method" one page before introducing approval voting.
  [→ [math-in-society-lippman](math-in-society-lippman.md)]
- **Helly's theorem (1913/1921)** — n > d convex sets in ℝᵈ, every d+1 of which share a point, all share a
  point. At d = 1 it is just "pairwise intersecting intervals have a common point", and that is the whole
  engine behind the agreement results below. [→ [agreeable-societies](agreeable-societies.md)]
- **Super-Agreeable Linear Society Theorem (Berg–Norine–Su–Thomas–Wollan 2010)** — if every *pair* of voters
  approves some common platform, then some platform is approved by *everyone*. Helly at d = 1, read as
  voting. Fails on a **circular** spectrum, where pairwise agreement buys only a strict majority.
  [→ [agreeable-societies](agreeable-societies.md)]
- **Agreeable Linear Society Theorem (same authors)** — in a **(k,m)-agreeable** linear society of n voters,
  some platform has the approval of at least n(k−1)/(m−1) voters. So "of every three voters, two agree
  somewhere" forces a platform acceptable to half the electorate. A corollary of their sharper clique bound
  ⌈(n−ρ)/q⌉, which is strictly stronger about 80% of the time.
  [→ [agreeable-societies](agreeable-societies.md)]
- **Balinski–Young impossibility theorem** — no apportionment method satisfies the **quota rule** and
  **population monotonicity** together. Often misquoted as ruling out quota plus *any* paradox: quota with
  **house** monotonicity (no Alabama paradox) is achievable, and Balinski & Young built such a method
  themselves (the Quota method, 1975; Still 1979 characterises the whole class). Same Balinski as
  Balinski–Laraki [majority judgment](majority-judgment.md).
  [→ [math-in-society-lippman](math-in-society-lippman.md)]

- **Sen's Theorem 8\*2 (1970)** — the result that prices the cardinal escape from Arrow. Cardinal
  **measurability alone is not enough**: under *cardinal non-comparability* (the social ranking must survive
  replacing each voter's utility *u* by *aᵢu + bᵢ*, *aᵢ* > 0, independently per voter) the Arrow
  impossibility survives untouched. Utilities must also be **interpersonally comparable**. So score voting
  and majority judgment do not *satisfy* Arrow's conditions — they decline the premise, by assuming your 5
  and my 5 are the same quantity. Verified concretely: independent affine rescaling changes score voting's
  winner in **20.9%** of random 5-voter profiles. Strengthened by d'Aspremont & Gevers (1977). This is the
  theorem electowiki's *Cardinal voting systems* page needs and does not cite.
  [→ [cardinal-voting-systems](cardinal-voting-systems.md)]
- **Dutta–Peters–Sen (2007)** — the cardinal counterpart of Gibbard–Satterthwaite. Assuming weak unanimity
  and that voters do not report utilities with infinite precision, the **only** strategy-proof cardinal
  decision scheme is **random ballot**. Nondeterminism buys almost nothing.
  [→ [cardinal-voting-systems](cardinal-voting-systems.md)]
---

## 10. Agreement models

Vocabulary from the geometric side of approval theory, which asks how much agreement an *electorate*
contains rather than which candidate a *method* elects. Nothing here names a winner.
[→ [agreeable-societies](agreeable-societies.md)]

- **Society (X, V, 𝒜)** — a **spectrum** X of possible positions, a finite voter set V, and each voter's
  **approval set** A_v ⊆ X. Each element of X is a **platform**. A **linear** society has X ⊆ ℝ closed and
  interval approval sets; an **ℝᵈ-convex** society has convex approval sets in ℝᵈ; a **d-box** society has
  products of d intervals. The linear results use only the *order* on ℝ, never a distance.
- **Agreement number / agreement proportion** — how many voters approve the most-approved platform, and that
  count divided by n.
- **(k, m)-agreeable** — among *every* m voters, some k share a platform. **(2,2) = super-agreeable**,
  **(2,3) = agreeable**. A hypothesis about the electorate, not something readable off ballots.
- **Agreement graph** — voters as vertices, an edge when two approval sets intersect. For a linear society
  it is an **interval graph**, and its clique number equals the agreement number.
- **Perfect graph** — χ(H) = ω(H) on every induced subgraph. Interval graphs are perfect, which is what lets
  a colouring bound become an agreement bound; box agreement graphs are not (C₅ is realisable with five
  rectangles).
- **Tolerance graph** — an interval graph in which an edge requires overlap of at least the smaller
  *tolerance*. Burkhart's two-level ("approve / maybe / disapprove") societies are tolerance graphs when the
  maybe regions are symmetric, **bitolerance** graphs otherwise.
- **Piercing number** — the fewest platforms needed so that every voter approves at least one.
- **Boxicity** — the least d making a graph the agreement graph of a d-box society. Recognising boxicity ≤ 1
  is interval-graph recognition (easy); deciding boxicity ≤ d is NP-hard for every d ≥ 2.

---

## 11. Reading the literature

Not voting terms — vocabulary for the papers themselves, kept here so the front matter resolves.

- **JEL Classification** — the *Journal of Economic Literature* subject codes, maintained by the American
  Economic Association and used to index working papers and articles in EconLit. A letter for the broad
  field, digits to narrow it. Authors choose their own codes, so the list is best read as a claim about what
  a paper takes itself to be doing, not as a neutral catalogue entry. The five that keep recurring on
  social-choice papers:
  - **C72** — Noncooperative Games (under C7, Game Theory and Bargaining Theory). Strategic voting modelled
    as a game between voters.
  - **D01** — Microeconomic Behavior: Underlying Principles (under D0, General). Where an axiomatic
    treatment of preference itself goes.
  - **D02** — Institutions: Design, Formation, Operations, and Impact. A voting rule as an institution to be
    designed rather than a formula to be evaluated.
  - **D72** — Political Processes: Rent-Seeking, Lobbying, Elections, Legislatures, and Voting Behavior
    (under D7, Analysis of Collective Decision-Making). The application: elections.
  - **D82** — Asymmetric and Private Information; Mechanism Design (under D8, Information, Knowledge, and
    Uncertainty). The machinery: what a rule can extract from voters who may misreport.

  Read the combination rather than the codes one at a time. **D72 + D82 is the Gibbard–Satterthwaite corner
  of the scheme** — collective choice under misreporting — so the full set C72, D01, D02, D72, D82 announces
  a paper about *strategic manipulation of a voting rule, treated axiomatically*, which is most of §5 and
  §9. Absences say as much: nothing in D6 (welfare economics) means the paper is not arguing about which
  outcome is *better*, and nothing in C9 (design of experiments) means no ballots were collected.

---

## Sources

- [*Cardinal voting systems* (electowiki)](https://electowiki.org/wiki/Cardinal_voting_systems) — the class
  taxonomy and the proportional-cardinal family; declared point of view, and one bad Arrow inference checked
  in [cardinal-voting-systems](cardinal-voting-systems.md)
- [LeGrand, *Ranked-ballot voting methods*](https://www.cs.angelo.edu/~rlegrand/rbvote/) — methods, examples,
  criterion table, calculator
- [Ogren, *RCV and core support*](https://voting-in-the-abstract.medium.com/rcv-and-core-support-e0d1780a9184)
- [*Approval voting* (Wikipedia)](https://en.wikipedia.org/wiki/Approval_voting) — history, use, strategy,
  the model-dependent compliance table [→ [approval-voting](approval-voting.md)]
- [Brandl & Peters, *Approval Voting under Dichotomous Preferences*](https://www.dominik-peters.de/publications/av.pdf),
  *JET* 205 (2022) — the axioms, the eight characterizations, and Inada's transitivity
  [→ [brandl-peters-approval-characterizations](brandl-peters-approval-characterizations.md)]
- [Horn, *Three Unique Virtues of Approval Voting*](https://www.qeios.com/read/ZETKEQ.2), Qeios (2024) —
  the Rule (1) / Rule (2) distinction and the three readings of IIA; its three claimed virtues are shared
  with score voting and its worked example doesn't hold
  [→ [horn-three-virtues-approval](horn-three-virtues-approval.md)]
- [*STAR voting* (Wikipedia)](https://en.wikipedia.org/wiki/STAR_voting) — thin and advocacy-sourced; the
  criteria failures are worked out locally instead [→ [star-voting](star-voting.md)]
- [*Score voting* (Wikipedia)](https://en.wikipedia.org/wiki/Score_voting) — the baseline the other two are
  defined against; uncited properties section and an unsettled sum-vs-average definition
  [→ [score-voting](score-voting.md)]
- [*Majority judgment* (Wikipedia)](https://en.wikipedia.org/wiki/Majority_judgment) — the median answer,
  Balinski and Laraki's point-summing theorem, and Laslier's median-voter critique
  [→ [majority-judgment](majority-judgment.md)]
- [*Single transferable vote* (Wikipedia)](https://en.wikipedia.org/wiki/Single_transferable_vote) — the
  first multi-winner method here; quotas, surplus transfers, and a century of real use
  [→ [single-transferable-vote](single-transferable-vote.md)]
- [Berg, Norine, Su, Thomas & Wollan, *Voting in agreeable societies*](http://arxiv.org/abs/0811.3245),
  *Amer. Math. Monthly* 117 (2010) — Helly's theorem read as voting; agreement numbers, (k,m)-agreeability,
  and the interval/perfect-graph machinery. With Burkhart's 2012 HMC thesis on a third approval level
  [→ [agreeable-societies](agreeable-societies.md)]
- [Pacuit, *Voting Methods*](https://plato.stanford.edu/entries/voting-methods/), *Stanford Encyclopedia of
  Philosophy* (rev. 2019) — the characterization theorems (May, Young, Fishburn, Moulin, Myerson), the
  epistemic reading of voting and the Condorcet Jury Theorem, the issue-aggregation paradoxes, and impartial
  culture [→ [sep-voting-methods](sep-voting-methods.md)]
- [Equal Vote Coalition](https://www.equal.vote/) / [STAR Voting](https://www.starvoting.org/) — origin of
  both STAR and Ranked Robin
- [Equal Vote / BetterVoting](https://bettervoting.com) — Ranked Robin in production
