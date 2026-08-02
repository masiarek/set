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
- **Approval / score / STAR** — cardinal methods, outside LeGrand's ranked-only scope. STAR = Score Then
  Automatic Runoff (score everyone 0–5, top two by total score go to an automatic pairwise runoff).

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
  verified Coombs counterexample is in the [note](legrand-ranked-ballot-methods.md).
- **Nonmanipulability (strategy-proofness)** **[LeGrand]** — no voter ever gains by ranking insincerely.
  **Every** ranked method fails this; see Gibbard–Satterthwaite.
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

## 8. Theorems

- **Gibbard–Satterthwaite theorem** — no deterministic ranked method with three or more candidates can be both
  non-dictatorial and strategy-proof. This is why LeGrand's "nonmanipulable?" row is uniformly NO: the design
  target is making manipulation *hard*, not impossible.
- **Arrow's impossibility theorem** — no ranked method can simultaneously satisfy unrestricted domain,
  Pareto, independence of irrelevant alternatives, and non-dictatorship. Applies to *methods*; arguments about
  an idealized preference-aggregation *standard* are not bound by it.
  [→ [rcv-and-core-support](rcv-and-core-support.md)]

---

## Sources

- [LeGrand, *Ranked-ballot voting methods*](https://www.cs.angelo.edu/~rlegrand/rbvote/) — methods, examples,
  criterion table, calculator
- [Ogren, *RCV and core support*](https://voting-in-the-abstract.medium.com/rcv-and-core-support-e0d1780a9184)
- [Equal Vote / BetterVoting](https://bettervoting.com) — Ranked Robin in production
