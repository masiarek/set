# LeGrand's ranked-ballot voting methods (Angelo State)

Source: Rob LeGrand, *Ranked-ballot voting methods* — <https://www.cs.angelo.edu/~rlegrand/rbvote/>

- [Descriptions of the methods](https://www.cs.angelo.edu/~rlegrand/rbvote/desc.html) — 16 methods with worked examples
- [Evaluation of the methods](https://www.cs.angelo.edu/~rlegrand/rbvote/eval.html) — 13 methods × 12 criteria compliance table
- [Ranked-ballot voting calculator](https://www.cs.angelo.edu/~rlegrand/rbvote/calc.html) — paste ballots, get every method's winner at once

The author calls it an unfinished work in progress (the Smith/Schwartz/Landau section literally trails off in
ellipses), and he prefers Approval Voting to all of it. But it is still one of the most compact
worked-example-per-method references on the web, and the calculator is the fastest way to see 16 methods disagree
on the same ballots.

## Why it's worth keeping

Most explainers give you one method and one example. LeGrand gives you **one election and sixteen answers** —
his 921-voter, 5-candidate example produces four different winners depending on the method, *and* the method
families split on who the *worst* candidate is. That single example is the best argument I've seen that
"which ranked method" is a real decision, not a technicality.

## Ballot notation

`A>B>C` = one voter preferring A to B to C. `4:A>B>C` = four such ballots. Ties allowed with `=`:
`3:A>B=C>D`. Tied ranks count as **half a vote each way** in the pairwise matrix. Every method here
picks the majority winner with only two candidates; they diverge from three up.

## The methods

### Point count

- **Borda** — score = (times ranked over another) − (times ranked under another). Equivalent to the usual
  0,1,2,…,*n*−1 positional count, but the over-minus-under form handles ties and truncation without
  special-casing. Widely held to be the best ranked method *if voters are sincere*, and probably the easiest
  to manipulate if they aren't.

  `14:Alan>Beth>Carl / 11:Beth>Carl>Alan / 7:Carl>Alan>Beth` → Alan 6, Beth 8, Carl −14 → **Beth**.

  Borda is not clone-independent, and LeGrand's example of that is the sharpest one in the piece:

  ```
  63:Eric>Fran>Gary
  37:Fran>Gary>Eric
  ```

  Eric has 63% of first places and would win in a two-way race, but Borda elects **Fran** — so the left-wing
  party wins by *running an extra candidate*. That's the candidate-saturation incentive: under a
  clone-dependent method, parties are rewarded for flooding the ballot.

### Recursive elimination using Borda

All three are Condorcet methods (they elect the Condorcet winner when one exists).

- **Nanson** — eliminate *every* candidate with a negative Borda score, recompute, repeat.
- **Baldwin** — eliminate only the single lowest Borda score, recompute, repeat.
- **Rouse** — Baldwin with an extra layer of recursion: repeatedly drop the *highest*-scoring candidate until
  one remains, then eliminate *that* one from the original field; repeat.

  On `14:Jana>Kurt>Lisa / 7:Kurt>Lisa>Jana / 11:Lisa>Jana>Kurt` (Borda: Jana 14, Kurt −8, Lisa −6) the three
  give **three different winners**: Nanson → Jana, Baldwin → Lisa, Rouse → Jana. Baldwin diverges because
  after dropping Kurt the recomputed scores flip to Jana −4, Lisa 4.

### First-preference elimination

- **Hare** — the original name of **Instant Runoff Voting**. Count first ranks, drop the smallest, repeat.
- **Carey** — generalization of Craig Carey's three-candidate IFPP: drop *all* candidates with
  below-average first-rank totals each round.
- **Coombs** — Hare in reverse: drop the candidate with the most *last*-place votes each round.

  On `9:Katy>Luke>Mary / 4:Luke>Mary>Katy / 6:Mary>Luke>Katy` (19 voters, avg first-rank 6.33) all three
  disagree: Hare → **Mary**, Carey → **Katy**, Coombs → **Luke**.

  Two strategy lessons from that one election:
  - Under Hare the Katy-first voters are *punished for sincerity* — voting `Luke>Katy>Mary` instead would
    have blocked their last choice. (Textbook favorite betrayal / [center squeeze](rcv-and-core-support.md).)
  - Under Carey the Luke- and Mary-first voters are punished for *not coordinating* — exactly the
    lesser-evil pressure of plurality.

  LeGrand's structural point: Hare, Carey and Coombs "consider the smallest amount of ballot information at
  any one time" of any method here.

### Cumulative

- **Bucklin** — count first ranks; if nobody has a majority, add second ranks, then third, until someone
  passes 50%.

  `7:Mark>Nell>Owen / 2:Nell>Mark>Owen / 3:Owen>Mark>Nell / 5:Owen>Nell>Mark` (17 voters) → round 2 gives
  Nell 14 and Mark 12. **Both** clear the majority bar in the same round, but Nell has more, so Nell wins —
  even though Mark beats Nell head-to-head 10–7. Bucklin can elect over a pairwise loser.

### Pairwise (Condorcet) methods

The pivot in LeGrand's argument: with only two candidates sincere voting is always optimal, so treat a
multi-candidate race as a **series of two-candidate elections**. One pass over the ballots builds the
**pairwise matrix**; every method below reads only that matrix.

- **Black** — Condorcet winner if one exists, else the Borda winner. The most decisive method in the set.
- **Copeland** — count pairwise victories, ties count ½. Ignores *margins* entirely, so it ties often — the
  least decisive method here. (This is the score BetterVoting's Ranked Robin reports as
  [`copelandScore`](ranked-robin-results-explained.md).)
- **Small** — Copeland, but if several tie for best, eliminate everyone else and recompute; repeat.
- **Dodgson** — sum each candidate's margins of defeat, take the smallest; "closest to being a Condorcet
  winner." ⚠️ See the caveat below — this is *not* the classical Dodgson rule.
- **Simpson** (minimax / Simpson–Kramer) — smallest *maximum* pairwise defeat. Equivalently: keep ignoring
  the smallest defeat until one candidate is unbeaten.
- **Raynaud** — elimination form of Simpson: repeatedly remove the candidate suffering the single largest
  remaining defeat.
- **Schulze** — resolves cycles with **beatpaths**. A beatpath is a chain of pairwise victories
  (`Abby>Erin>Dave>Brad`); its strength is its *weakest* link. Elect whoever has a stronger beatpath to every
  rival than that rival has back. Usually agrees with Simpson but dodges Simpson's pathologies.
- **Tideman** (ranked pairs) — sort victories strongest→weakest and lock them in, skipping any that would
  contradict already-locked stronger ones; the result is a full ordering.
- **Smith**, **Schwartz**, **Landau** — so indecisive they're treated as producing candidate *sets*, not
  winners. The page stubs these out and never finishes them.

## The canonical example: 921 voters, 5 candidates, no Condorcet winner

```
 98:Abby>Cora>Erin>Dave>Brad     124:Cora>Abby>Erin>Dave>Brad
 64:Brad>Abby>Erin>Cora>Dave      76:Cora>Erin>Abby>Dave>Brad
 12:Brad>Abby>Erin>Dave>Cora      21:Dave>Abby>Brad>Erin>Cora
 98:Brad>Erin>Abby>Cora>Dave      30:Dave>Brad>Abby>Erin>Cora
 13:Brad>Erin>Abby>Dave>Cora      98:Dave>Brad>Erin>Cora>Abby
125:Brad>Erin>Dave>Abby>Cora     139:Dave>Cora>Abby>Brad>Erin
                                  23:Dave>Cora>Brad>Abby>Erin
```

Pairwise matrix (row = "for", column = "against"; **bold** = the winning side; every pair sums to 921):

| for \ against | Abby | Brad | Cora | Dave | Erin |
|---|---|---|---|---|---|
| **Abby** | — | 458 | **461** | **485** | **511** |
| **Brad** | **463** | — | **461** | 312 | **623** |
| **Cora** | 460 | 460 | — | 460 | 460 |
| **Dave** | 436 | **609** | **461** | — | 311 |
| **Erin** | 410 | 298 | **461** | **610** | — |

Everything interesting about this election lives in two facts:

1. **Cora is the Condorcet loser** — she loses all four matchups — but she loses every one of them by
   exactly **one vote** (460–461).
2. There is a **cycle**: Brad > Erin > Dave > Brad (623, 610, 609 — three of the four largest margins).

Derived scores (checked by hand against the matrix):

| Candidate | Pairwise W–L | Copeland | Borda (row−col) | Largest defeat | Σ defeat margins |
|---|---|---|---|---|---|
| Abby | 3–1 | 3 | **+146** | 5 | 5 |
| Brad | 3–1 | 3 | +34 | 297 | 297 |
| Cora | 0–4 | 0 | −4 | **1** | **4** |
| Dave | 2–2 | 2 | −50 | 299 | 348 |
| Erin | 2–2 | 2 | −126 | 325 | 426 |

And the winners:

| Method | Winner | Why |
|---|---|---|
| Black | **Abby** | no Condorcet winner → Borda winner |
| Copeland | **Abby & Brad** (tie) | both 3 victories |
| Small | **Brad** | breaks the Copeland tie by the Abby–Brad matchup, 463–458 |
| Dodgson | **Cora** | smallest sum of defeat margins (4) |
| Simpson | **Cora** | smallest maximum defeat (1) |
| Raynaud | **Abby** | eliminates Erin (−325), Brad (−297), Dave (−49), Cora (−1) |
| Schulze | **Abby** | beats Brad/Dave/Erin 511–463 by beatpath, Cora 461–460 |
| Tideman | **Brad** | lock 623 Brad>Erin, 610 Erin>Dave, **skip** 609 Dave>Brad (contradiction), then the rest → `Brad>Abby>Erin>Dave>Cora` |

**The punchline.** Copeland, Schulze and Tideman rank Cora *last*. Dodgson and Simpson **elect** her. Both
readings are defensible from the same matrix: she never wins, but she is never really beaten either. Whether
"nobody strongly objects" beats "wins the most matchups" is a values question the arithmetic can't settle.
(LeGrand notes Dodgson and Simpson elect a Condorcet loser only very rarely; Copeland, Schulze and Tideman
never do.)

## Criterion compliance (from eval.html)

Definitions of these criteria are in [glossary.md](glossary.md) — the site names them but never defines them.

| Criterion | Baldwin | Borda | Bucklin | Carey | Coombs | Copeland | Dodgson | Hare | Nanson | Raynaud | Schulze | Simpson | Tideman |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| Pareto-optimal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| majority | ✅ | ❌ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Condorcet | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| mutual majority | ✅ | ❌ | ✅ | ❌ | ❌ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ |
| clone-independent | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ | ✅ | ❌ | ✅ |
| monotonic | ❌ | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ |
| Smith | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ✅ | ✅ | ✅ | ❌ | ✅ |
| reverse-symmetric | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ |
| reinforcing | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Schwartz | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| nonmanipulable | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

Things this table says out loud that are easy to miss:

- **The bottom row is all ❌**, and that's a theorem, not a shortcoming of the candidates on offer:
  Gibbard–Satterthwaite. The design goal is making manipulation *hard*, not impossible.
- **Only Borda is reinforcing.** Every other method here can elect X in precinct 1, X in precinct 2, and Y
  when you merge the ballots.
- **Schulze and Tideman are the only two with ✅ on all of Condorcet + clone-independence + monotonicity +
  Smith + reverse symmetry.** Schulze additionally gets Schwartz.
- **Hare (IRV) is the odd one out**: ✅ clone-independent and mutual-majority, ❌ Condorcet, Smith *and*
  monotonic. That's the RCV trade-off in one column.
- Only 13 of the 16 described methods are evaluated — **Rouse, Black and Small are described but never
  scored**.

### The reinforcement failure, verified

The site ships this as a bare ballot file with no explanation. Running it (2026-08-01):

```
# precinct 1                # precinct 2
8:B>C>A>D                   8:B>A>D>C
6:C>D>A>B                   2:B>C>D>A
4:D>B>C>A                   6:C>A>D>B
                            2:C>B>D>A
                            2:D>B>C>A
```

Coombs elects **B** in precinct 1 (eliminating D, A, C) and **B** in precinct 2 (eliminating C, D, A) — but
on the combined 38 ballots B has the most last-place votes (12) and is eliminated *first*, and **C** wins.
Two precincts that agree, overruled by their own sum.

## The calculator (explored 2026-08-01)

[calc.html](https://www.cs.angelo.edu/~rlegrand/rbvote/calc.html) is pure client-side JavaScript — no
server, no applet, so it still works and can be read as source. Input is one ballot per line, optionally
`count:A>B>C`, with `#` comments. Three options worth knowing:

- **Candidates to ignore** — treats them as having dropped out *after* the ballots were cast. The fastest
  way to demonstrate a spoiler or clone failure: run it, remove the spoiler, run it again.
- **Tiebreaking ranking** — supply one and results become deterministic and reproducible. Leave it blank
  and it draws a random ballot, so *the same input can give different winners on different clicks*.
  Winners decided this way are flagged with an asterisk in the output — always check for it.
- **Reverse all rankings** — flips every ballot, for testing reverse-symmetry violations.

Three things the page doesn't tell you, found by reading the source:

- **Four methods refuse equal-rank ballots.** Hare, Bucklin, Carey and Coombs all abort with *"…require
  fully-ranked ballots with no tied preferences."* `calcall()` silently *omits* them from the results
  table rather than warning you — so a run on ballots with any `=` quietly reports 11 methods instead of
  15, with nothing saying why. Every pairwise method handles ties fine (half a vote each way).
- **There is a 17th method, and it's dormant.** A `LeGrand` button exists in the HTML, but it's commented
  out — as is its call inside `calcall()`, *and* the function body itself. Its real name is
  `calclegrandschulze`, and reading it shows a Schulze variant that compares **strongest beatpaths of
  length at most k**, iterating k from 1 to n−1, rather than beatpaths of any length. Revived by hand on
  a test election it runs correctly, so this is finished work that was switched off, not a stub.
- **Rouse isn't there either** — described on desc.html, absent from both the calculator and eval.html.

A worked cross-check using it — 12 ballots where nine of eleven methods tie and only Borda decides — is in
[ranked-robin-results-explained.md](ranked-robin-results-explained.md).

## Caveats and corrections

- **"Dodgson" here is not Dodgson's method.** The classical Dodgson rule (Charles Dodgson / Lewis Carroll)
  elects the candidate needing the fewest *adjacent swaps on ballots* to become a Condorcet winner — a rule
  that is NP-hard to compute. LeGrand's version sums pairwise defeat *margins*, which is a cheap
  approximation (in the Tideman/"simplified Dodgson" family), not the real thing. Don't cite this page for
  Dodgson's method.
- **Name mapping to the usual literature:** Hare = IRV/RCV; Simpson = minimax (Simpson–Kramer), the
  winning-votes variant; Tideman = ranked pairs; Small = an iterated-Copeland rule that's rare elsewhere.
- **Criteria are named but never defined** anywhere on the site — that gap is what
  [glossary.md](glossary.md) fills.
- **Ranked ballots only.** No approval, score, or STAR — even though the author's own index page says he'd
  rather have Approval. So the site can't speak to the cardinal-vs-ordinal argument in
  [rcv-and-core-support.md](rcv-and-core-support.md); every method here is stuck in the ordinal world Ogren
  argues is the wrong level of description.
- **Compliance claims are the author's**, presented without proofs. They match the standard results where
  I've checked, but treat the table as a map, not a citation.

## Related local material

- [rcv-and-core-support.md](rcv-and-core-support.md) — the ordinal/cardinal argument these methods can't reach
- [ranked-robin-results-explained.md](ranked-robin-results-explained.md) — Copeland scoring in a live tabulator
- [glossary.md](glossary.md) — every term above, defined in one place
