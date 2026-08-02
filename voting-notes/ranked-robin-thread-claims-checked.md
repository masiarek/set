# The Ranked Robin thread's four claims, checked

Companion to [ranked-robin-origins.md](ranked-robin-origins.md), which tells the story of
[votingtheory.org topic 136](https://www.votingtheory.org/forum/topic/136/new-simple-condorcet-method-basically-copeland-margins)
(Sass, 2021 — the debut of Ranked Robin under the working name "Ranked Advantage Voting"). This
note does the other half: the thread contains four claims that can be *settled* by computation, and
in five years nobody in it ran a single number against any of them. Verifier:
[code/thread136-claims/verify.py](code/thread136-claims/verify.py) (stdlib only, ~40 s, every
example asserted, [saved output](code/thread136-claims/run-output.txt)).

| # | Claim | Who | Verdict |
|---|---|---|---|
| C1 | Adding a weak candidate gives every contender "exactly 1 more win, which doesn't change anything meaningful" | Sass, [post 28](https://www.votingtheory.org/forum/topic/136/new-simple-condorcet-method-basically-copeland-margins/28) | **True of the case described, and the case described is the one that can't hurt.** Exact theorem for a candidate who loses *every* matchup; false the moment the newcomer wins one |
| C2 | Summing margins over all candidates "would be identical to Borda" | [post 40](https://www.votingtheory.org/forum/topic/136/new-simple-condorcet-method-basically-copeland-margins/40) | **Correct, and more strongly than stated** — an exact algebraic identity that survives equal ranks and truncation |
| C3 | "Best average rank" is mathematically equivalent but misleading to voters | Sass, [post 18](https://www.votingtheory.org/forum/topic/136/new-simple-condorcet-method-basically-copeland-margins/18) | **Both halves right.** Equivalent only under two conventions the sentence never states; each one, dropped, elects the other candidate |
| C4 | Ties get rarer as the electorate grows, because the method throws away less than Copeland | Jack Waugh, [post 13](https://www.votingtheory.org/forum/topic/136/new-simple-condorcet-method-basically-copeland-margins/13) | **Confirmed, with a caveat he didn't anticipate**: Copeland's own tie rate does *not* fall with electorate size — it's flat at ~17% — only the margins rung melts away |

Throughout, "Ranked Robin" means the deployed ladder: Copeland matchup wins (a pairwise tie scoring
half), then 1st degree = margins summed *among the finalists*, then 2nd degree = margins summed
*over all candidates*. Ballots allow equal ranks, ignore skipped ranks, and treat unranked as tied
last.

## C1 — the IIA defense proves less than it sounds like

Jack Waugh pushed on Arrow ([post 24](https://www.votingtheory.org/forum/topic/136/new-simple-condorcet-method-basically-copeland-margins/24));
Sass conceded IIA failure immediately, then argued in post 28 that the failure is theoretical:

> The finalist set (typically just 1 candidate) is based on how many other candidates are beaten. If
> you add a weak candidate into the mix, then all of the top candidates who would make it into the
> finalist set each gain exactly 1 more win, which doesn't change anything meaningful.

### The half that is a theorem

If the newcomer X loses **every** matchup, the argument is not just plausible, it's airtight — and
stronger than Sass claimed. Every other candidate's Copeland score rises by exactly 1, so the
ranking by wins is untouched and the finalist set is *identical*; X, with zero wins, is never a
finalist, so the 1st-degree margins — summed among finalists only — never see it. The 1st-degree
result is bit-for-bit unchanged. (Checked anyway on 6,631 random profiles with equal ranks and
truncation switched on: no exceptions, as there cannot be.)

### The half Sass flagged, confirmed

Post 28 hedges that "only when we start getting into a 2nd Degree tiebreaker" could an irrelevant
alternative swing things. It can, and here is a six-ballot election where it does:

```
A
C > B > D
C > A > B > X=D
C > B > D > A
A > X > C > D > B
D=A > X > B > C
```

Copeland: A 3.5, B 2.0, C 3.5, D 1.0, **X 0.0** — X loses all four matchups and is never a
finalist. A and C are pairwise tied 3–3, so the 1st degree cannot separate them and the 2nd degree
runs:

| | A | C | elects |
|---|---|---|---|
| margins over all candidates, **without X** | +3 | +6 | **C** |
| margins over all candidates, **with X** | +8 | +7 | **A** |

The entire difference is the margin against X: A beats X by 5, C by only 1. A candidate who wins
nothing decides the election. In random profiles this fires in 0.80% of cases where an all-losing
candidate is added (176 / 21,980) — it first requires a 1st-degree tie, which is itself rare
([C4](#c4--do-ties-thin-out-as-the-electorate-grows)).

### The half that is simply wrong

"Weak candidate" and "candidate who loses every matchup" are not the same thing, and the whole
argument rests on their being the same. One matchup win is enough:

**100 ballots — 49 `A>B>C`, 2 `C>A>B`, 49 `B>C>A`.**

| | vs A | vs B | vs C |
|---|---|---|---|
| A | — | 51–49 | 49–51 |
| B | 49–51 | — | 98–2 |
| C | 51–49 | 2–98 | — |

Without C, A beats B 51–49 and wins. Add C — 2 first preferences, beaten by B 98–2 — and the field
becomes a 3-cycle, all three tie on one win, and the margins elect **B** (A 0, B +94, C −94). C
takes 2% of first preferences, loses to the eventual winner by 96 votes, and changes the outcome.
Because C beats A, it does *not* hand every contender the same +1, and that is the only thing Sass's
argument ever needed.

**How to cite this fairly.** This is generic Condorcet IIA failure, not a Ranked Robin defect —
every Condorcet method breaks on this profile, and the [electowiki article](https://electowiki.org/wiki/Ranked_Robin)'s
criteria table says so openly. What doesn't survive is the *reassurance*: the "+1 to everyone"
reasoning covers only pairwise-dominated newcomers, and the spoilers that matter are precisely the
ones that win something. Sass's practical point may still hold — a candidate strong enough to beat a
front-runner is arguably not "irrelevant" — but that is a different argument, and it needs making.

## C2 — the Borda coda is exactly right

The thread's last exchange (March 2022). Waugh proposes dropping the Copeland gate: rank as many as
you like, equal ranking allowed, unranked assumed worst, and elect whoever has the largest sum of
margins over *all* candidates. A since-deleted account replies, in full: "That would be identical to
Borda." Nobody checks. It is an exact identity:

> **Σ<sub>y≠x</sub> [ n(x≻y) − n(y≻x) ]  =  2·Borda(x) − (m−1)·V**

with Borda scored tournament-style (one point per ballot beaten, half a point per pairwise tie) over
m candidates and V ballots. The subtracted term is identical for every candidate, so this is an
order-preserving transform: the two methods produce the same ranking, not merely a correlated one.
Verified on 20,000 random profiles with equal ranks and truncation both active — the conditions
under which you'd most expect an equivalence like this to leak.

The convention matters and is worth stating out loud, because it's where a reader could reasonably
object: the identity needs pairwise ties scored at half and unranked candidates tied last. Under a
*positional* Borda that honours the rank numbers a voter wrote, it fails — see [C3](#c3--best-average-rank-is-equivalent-and-misleading-both-halves-check-out).

So the Copeland gate is not a refinement of Waugh's method; it is the only thing standing between
Ranked Robin and Borda, with Borda's teaming and burying incentives intact. That gives the origins
note's "the Copeland gate is the whole firewall" a precise statement: **outside the finalist set,
margins are Borda; inside it, they are the Borda count of the reduced election among finalists**,
which is a different quantity. Marylander's version ([post 22](https://www.votingtheory.org/forum/topic/136/new-simple-condorcet-method-basically-copeland-margins/22)) —
easier to attack Copeland directly than the Borda count inside the tied set — is the strategic
reading of the same fact.

## C3 — "best average rank" is equivalent *and* misleading; both halves check out

Sass's one-sentence pitch, post 18: *"Among the candidates who tie for winning the most head-to-head
matchups, elect the candidate with the best average rank."* He then talks himself out of it — the
word "among" is doing too much work, and "average rank" is "misleading to voters despite the line
saying that skipped ranks are ignored." He was right on both counts, and each objection has a
counterexample that flips the winner.

**(i) Rank gaps.** 100 ballots, two candidates: 51 voters mark A 1st and B 2nd; 49 mark B 1st and A
**9th**, leaving ranks 2–8 blank.

| reading | A | B | elects |
|---|---|---|---|
| the method (skipped ranks ignored) | beats B 51–49 | | **A** |
| average rank, gaps collapsed | 1.49 | 1.51 | **A** ✓ |
| average rank as the voter wrote it | 4.92 | 1.51 | **B** ✗ |

A voter who reads "average rank" the way the phrase actually reads gets the opposite winner. Note
how thin the honest margin is — 1.49 vs 1.51 — while the literal reading isn't close. Sass's same
objection applies to Marylander's "margin of victory" wording ([post 14](https://www.votingtheory.org/forum/topic/136/new-simple-condorcet-method-basically-copeland-margins/14)),
which he raised in reply: sports margins are magnitudes, and voters may assume rank *distance*
counts.

**(ii) Which election is the average over?** Nine ballots, four candidates:

```
C>A>B>D   C>A>B>D   D>B>A>C   C>B>A>D   B>D>C>A
D>A>C>B   D>B>C>A   A>B>D>C   A>B>C>D
```

A and B tie for most matchup wins (2 each) and become the finalists. Average rank over the **full
ballot**: A 2.44, B 2.33 → B. Margins **among the finalists only**, which is the actual rule: A
beats B 5–4 → **A**. Same sentence, two readings, two winners. The equivalence holds only when the
average is taken inside the finalist set, and "among" is the only word carrying that.

The takeaway for anyone reusing the one-liner: it is a correct summary for someone who already knows
the algorithm, and an ambiguous instruction for anyone who doesn't. The thread never resolved this —
both Sass and Marylander called for field testing of ballot language, and none was ever reported.

## C4 — do ties thin out as the electorate grows?

Waugh, post 13: Ranked Robin "throws away less information in case of a cycle, in such a way that
ties are less likely as the electorate grows larger." Four candidates, impartial culture, strict
complete rankings:

| voters | trials | no Condorcet winner | Copeland tie | unresolved after 1st degree | after 2nd degree |
|---:|---:|---:|---:|---:|---:|
| 5 | 20,000 | 13.70% | 13.70% | 4.81% | 2.51% |
| 15 | 20,000 | 16.50% | 16.50% | 2.12% | 0.66% |
| 51 | 12,000 | 17.05% | 17.05% | 1.20% | 0.27% |
| 201 | 5,000 | 17.22% | 17.22% | 0.76% | 0.00% |
| 1,001 | 1,500 | 16.73% | 16.73% | 0.20% | 0.00% |

Confirmed — but the shape is more interesting than the claim. **Copeland's tie rate does not fall
with the electorate at all**; it rises and settles near 17%, because Copeland ties are structural
(cycles), not coincidental. What melts away is everything below: the margins rungs need an exact
integer coincidence, and integers get harder to tie as they get bigger. 4.81% → 0.20% at the 1st
degree; the 2nd degree finds nothing at all past a few hundred voters. Waugh's mechanism — the extra
information Ranked Robin keeps — is exactly what converts a persistent tie rate into a vanishing
one.

*Sanity check on the simulation:* the no-Condorcet-winner column tracks the standard
impartial-culture figures (≈17.6% for four candidates asymptotically; my five- and six-candidate
runs at 101 voters give 24.0% and 32.0% against textbook ≈25% and ≈32%).

### A small theorem the table exposes

The first two columns are *equal in every row*, and that is forced. With no pairwise ties, Copeland
scores sum to m(m−1)/2. If there is no Condorcet winner, the top score is at most m−2, and a unique
top scorer would cap the total at m²−3m+1 — which is short of m(m−1)/2 unless m ≥ 4.56. So:

> **With four or fewer candidates, "no Condorcet winner" and "Copeland tie" are the same event.**
> Every cycle reaches the margins rung.

From five candidates up they come apart: at m=5, 14.5% of cycle profiles still have a unique
Copeland winner (m=6: 25.8%), and the tiebreaker never runs. The practical consequence points the
other way from how the tiebreaker is usually discussed — in the three- and four-candidate races that
make up most real elections, the 1st-degree margins rule is not an exotic corner case, it is the
*entire* cycle path.

### Which is what makes BetterVoting's gap matter

That settles the open question the origins note left about the deployed tabulator. `RankedRobin.ts`
handles one winner, or *exactly two* tied with a decisive head-to-head, and sends everything else to
a random pick — the 1st-degree margins rule is not implemented at any tie size. Filed upstream as
[Equal-Vote/bettervoting#1469](https://github.com/Equal-Vote/bettervoting/issues/1469). The theorem
above says how much that costs: with three candidates and no drawn matchups, **every** cycle is a
3-way tie, so the implemented two-way branch can never fire on a cycle at all — it only catches
draw-induced ties like the [BV1550 Ann/Bob case](ranked-robin-results-explained.md). Given a cycle:

| candidates | no Condorcet winner | → 2-way (handled) | → 3+-way (**random**) | → unique Copeland winner |
|---:|---:|---:|---:|---:|
| 3 | 8.7% | 0.0% | **100.0%** | 0.0% |
| 4 | 17.3% | 50.1% | **49.9%** | 0.0% |
| 5 | 24.7% | 58.9% | **26.8%** | 14.3% |
| 6 | 31.0% | 54.1% | **19.4%** | 26.5% |

With equal ranks and truncation switched on — BetterVoting's actual ballot rules — three candidates
split 37.9% two-way / **32.0% three-way** / 30.1% resolved outright.

**Caveat on the generator.** Impartial culture is the worst case for cycles — real electorates are
structured, and my [spatial-model VSE run](ranked-robin-vse-run.md) found ties there are ~95% clone
dead heats rather than cycles, a completely different taxonomy. Both generators agree on the point
at issue: tie rates below the Copeland stage fall with V.

## What this changes

- **Cite Sass's IIA defense with its scope attached.** "Adding a weak candidate changes nothing" is
  a theorem about candidates who lose *every* matchup and a false statement about weak candidates in
  general — one matchup win breaks it, at 2% of first preferences.
- **"The Copeland gate is the whole firewall" is now an identity, not an analogy** (C2), which is
  the sharper way to state it when the origins note's claim gets challenged.
- **Don't reuse the one-sentence tally as ballot text.** Two unstated conventions, two live
  counterexamples. As a summary for people who know the method it's fine.
- **In small fields the 1st-degree tiebreaker is the whole cycle path**, not a corner case — worth
  knowing before treating the margins rung as a formality, and directly relevant to the deployed
  tabulator's two-way-only shortcut.

## Links

- The thread: [topic 136](https://www.votingtheory.org/forum/topic/136/new-simple-condorcet-method-basically-copeland-margins) · story and transcriptions: [ranked-robin-origins.md](ranked-robin-origins.md)
- Verifier: [code/thread136-claims/verify.py](code/thread136-claims/verify.py) · [output](code/thread136-claims/run-output.txt)
- Related: [Ranked Robin results explained](ranked-robin-results-explained.md) · [the missing VSE run](ranked-robin-vse-run.md) · [Glossary](glossary.md) — Copeland score, margin, Borda, IIA
