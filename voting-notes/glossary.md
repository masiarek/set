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
- **Ranked Robin** — Equal Vote's Condorcet method; scores by matchup wins (Copeland), then breaks ties by
  greatest sum of pairwise margins among the tied (their "total advantage"). Debuted Oct 2021 as **Ranked
  Advantage Voting**, renamed Nov 2021. Honest-ballot VSE: top of the Condorcet cluster, tie-ladder
  VSE-neutral but the most decisive method in the votesim field.
  [→ [ranked-robin-results-explained](ranked-robin-results-explained.md),
  [ranked-robin-origins](ranked-robin-origins.md), [ranked-robin-vse-run](ranked-robin-vse-run.md)]
- **Top Two IRV** — only the two first-choice leaders reach the runoff.
  [→ [rcv-and-core-support](rcv-and-core-support.md)]

### Cardinal

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
- **District magnitude** — seats per district. The real determinant of how proportional a result is; three
  seats means a 25% threshold. Shrinking districts is how a government tunes STV toward large parties
  without appearing to change the rules. [→ [single-transferable-vote](single-transferable-vote.md)]
- **Block approval / reweighted range / sequential proportional approval** — the cardinal multi-winner
  family. Block approval (top *k* totals) is not proportional; the others reweight ballots that already
  elected someone, which is the surplus transfer's cardinal analogue. Reweighted range picks the Academy's
  Visual Effects nominees. [→ [score-voting](score-voting.md), [approval-voting](approval-voting.md)]

## 5. Criteria and properties

Every one of these appears as a row in LeGrand's compliance table with no definition given.

- **Pareto-optimality (unanimity)** **[LeGrand]** — if every voter ranks A over B, B must not win.
- **Majority criterion** **[LeGrand]** — a candidate ranked first by an absolute majority must win.
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
  a participation failure. [→ [majority-judgment](majority-judgment.md)]
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
- **Bullet voting** — approving (or ranking) only your favorite. Approval's characteristic degeneracy: if
  everyone bullet votes, approval *is* plurality. 79% of voters did it in the 1987 MAA election, 80%+ in
  Dartmouth's student elections, and ~80% at the IEEE — which is the reason IEEE gave for repealing approval
  in 2002. Three measured electorates, all near four in five. [→ [approval-voting](approval-voting.md)]
- **Chicken dilemma / Burr dilemma** — two allied frontrunners' camps each bullet-vote to avoid helping the
  other, and a third candidate wins. Named for the Jefferson–Burr tie of 1800.
  [→ [approval-voting](approval-voting.md)]
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
- **Indeterminacy (Saari–Van Newenhizen)** — with voter preferences fixed, approval can *sincerely* elect
  any candidate, Condorcet winner or Condorcet loser, depending only on where voters put their cutoffs.
  Read as a defect by Saari, as responsiveness to intensity by Brams. [→ [approval-voting](approval-voting.md)]
- **Bland-winner objection** — the claim that Condorcet methods elect inoffensive nobodies.
  [→ [rcv-and-core-support](rcv-and-core-support.md)]

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

- **Gibbard–Satterthwaite theorem** — no deterministic ranked method with three or more candidates can be both
  non-dictatorial and strategy-proof. This is why LeGrand's "nonmanipulable?" row is uniformly NO: the design
  target is making manipulation *hard*, not impossible.
- **Myerson–Weber voting equilibrium** — rational-voter model for approval: approve every candidate with a
  positive **prospective rating** (utility weighted by the probability your vote is pivotal in each pairwise
  tie). Approving your favorite and rejecting your least favorite are dominant strategies.
  [→ [approval-voting](approval-voting.md)]
- **Leader rule (Laslier)** — the practical special case: approve everyone you prefer to the expected
  leader, plus the leader if you prefer them to the expected runner-up. If everyone plays it, the
  equilibrium elects the Condorcet winner when one exists. [→ [approval-voting](approval-voting.md)]
- **Arrow's impossibility theorem** — no ranked method can simultaneously satisfy unrestricted domain,
  Pareto, independence of irrelevant alternatives, and non-dictatorship. Applies to *methods*; arguments about
  an idealized preference-aggregation *standard* are not bound by it.
  [→ [rcv-and-core-support](rcv-and-core-support.md)]
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

## Sources

- [LeGrand, *Ranked-ballot voting methods*](https://www.cs.angelo.edu/~rlegrand/rbvote/) — methods, examples,
  criterion table, calculator
- [Ogren, *RCV and core support*](https://voting-in-the-abstract.medium.com/rcv-and-core-support-e0d1780a9184)
- [*Approval voting* (Wikipedia)](https://en.wikipedia.org/wiki/Approval_voting) — history, use, strategy,
  the model-dependent compliance table [→ [approval-voting](approval-voting.md)]
- [Brandl & Peters, *Approval Voting under Dichotomous Preferences*](https://www.dominik-peters.de/publications/av.pdf),
  *JET* 205 (2022) — the axioms, the eight characterizations, and Inada's transitivity
  [→ [brandl-peters-approval-characterizations](brandl-peters-approval-characterizations.md)]
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
- [Equal Vote Coalition](https://www.equal.vote/) / [STAR Voting](https://www.starvoting.org/) — origin of
  both STAR and Ranked Robin
- [Equal Vote / BetterVoting](https://bettervoting.com) — Ranked Robin in production
