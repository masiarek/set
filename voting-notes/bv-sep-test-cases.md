# Sending SEP examples to BetterVoting — what actually fits

Companion to [sep-voting-methods.md](sep-voting-methods.md). **Status: proposal, nothing filed.**

## Verdict first: BV has no educational surface, so "send the examples" means tests, not docs

The obvious idea — contribute the entry's worked examples as teaching material — does not survive
contact with the codebase. BetterVoting is a *tool*, and it deliberately outsources its explaining:

| surface | what is actually there |
|---|---|
| `en.yaml` → `methods:` | name, short name, and an external `learn_link` per method — starvoting.org, equal.vote, YouTube. No content of its own. |
| `en.yaml` → `about:` | title, description, team, contributors, contribute, donate. |
| `Sandbox.tsx` | no presets, no sample profiles, no scenarios. |
| `docs/` | developer documentation. |

So there is no page a worked Condorcet-paradox example would go on, and proposing one is proposing a
product direction rather than a contribution. **Where the entry's profiles do fit is the test suite**,
which is also the form Adam's BV work already takes.

## The gap that is real, and checkable in one command

`IRV.test.ts` has five tests: first-round majority, multiwinner, two-round, exhausted ballots, and
overvotes. Grepping it for `condorcet|monoton|no-show|paradox|cycle` returns **0**. The suite covers
ballot *plumbing* — transfers, exhaustion, malformed input — and nothing about the method's known
pathologies. Every profile below is a pathology with a published provenance and an arithmetic answer,
which is exactly what a regression fixture wants.

## One thing BV already gets right — do not file it

The entry's printed Hare and Coombs definitions elect *nobody* on a three-way first-place tie, because
they remove every poorly-performing candidate each round (finding 1 in
[sep-voting-methods](sep-voting-methods.md)). **BV does not inherit this.** `IRV.ts` pops exactly one
candidate per round (`remainingCandidates.pop()`) and sets `tieBreakType: 'random'` when the last two
are level. The degenerate profile is therefore safe, and filing it as a bug would be wrong. It is
still worth adding as a fixture, because it exercises the random-tiebreak path that nothing else tests.

## Shortlist, best first

### 1. The monotonicity failure — 17 ballots, and it is a failure of BV's own RCV

SEP §3.2. Two profiles identical but for two voters who move A from second to first:

```
Profile 1                    Profile 2
6: A>B>C                     6: A>B>C
5: C>A>B                     5: C>A>B
4: B>C>A                     4: B>C>A
2: B>A>C                     2: A>B>C     <- the only change
```

| | first preferences | eliminated | runoff | winner |
|---|---|---|---|---|
| Profile 1 | A 6, B 6, C 5 | C | A 11 – B 6 | **A** |
| Profile 2 | A 8, B 4, C 5 | B | C 9 – A 8 | **C** |

Raising A costs A the election. Recomputed by hand here as well as by the verifier, and note this is
an **IRV** failure, not merely a Plurality-with-Runoff one: at three candidates the two methods
eliminate the same candidate in both profiles, so BV's `rcv` reproduces it exactly.

Why it is the best candidate: it is small, it is deterministic (no tiebreak involved), it targets the
most-deployed method BV runs, and the pairing is the test — asserting `winner == A` then `winner == C`
across a two-ballot change is a monotonicity regression test in eight lines.

Worth knowing before writing the assertion: **neither profile has a Condorcet winner** — both carry
the cycle A>B>C>A — so nothing adjudicates between A and C on pairwise grounds. That makes it a clean
monotonicity fixture and a bad "IRV got it wrong" argument, which is a distinction worth keeping.

### 2. Three methods, three winners, 19 ballots

SEP §2.1. `7:A>B>C>D, 5:B>C>D>A, 4:D>B>C>A, 3:C>D>A>B`:

| method | winner |
|---|---|
| Plurality with Runoff | A |
| Hare / IRV | D |
| Coombs | B |
| Borda | B |
| Condorcet | none — Copeland ties B and C at +1 |

BV runs RCV and Ranked Robin on the same ballots, so this is a natural cross-method fixture: one
ballot set, and the assertion is that the methods *disagree* in a specific documented way.

### 3. The no-show paradox, for Ranked Robin

This is the one that touches Adam's existing BV work most directly. Moulin's theorem: with four or
more candidates, **every** Condorcet-consistent method has a no-show paradox. Ranked Robin is
Condorcet-consistent, so the theorem applies to it — abstaining voters can be better off than voting.

The search has now been run, against Ranked Robin as BV implements it — Copeland with ½ for a pairwise
tie (`Util.ts:257`), then the two-way pairwise runoff rung, then random — rejecting any profile whose
winner comes off the random rung. Witness, from
[`code/sep-voting-methods/ranked_robin_noshow.py`](code/sep-voting-methods/ranked_robin_noshow.py):

```
2: C>B>A>D
2: D>A>C>B     <- one of these two stays home
1: B>A>D>C
```

| | A | B | C | D | contenders | winner |
|---|---|---|---|---|---|---|
| all five vote | 2 | **2** | 1 | 1 | {A, B}, B beats A | **B** |
| one `D>A>C>B` abstains | 1.5 | **2** | **2** | 0.5 | {B, C}, C beats B | **C** |

The abstaining voter ranks C above B, so voting cost her the better outcome. **Five ballots, four
candidates, and no tiebreak on either side** — both winners come off the pairwise-runoff rung, so the
assertion is deterministic and safe to commit as a test.

Five voters is the **minimum**: exhaustive over all 26,561 anonymized four-candidate profiles with one
to five voters. And at **three** candidates Ranked Robin does not fail at all — clean across all 12,375
anonymized profiles up to eleven voters — so a three-candidate test would assert the wrong thing.

This is the fixture worth filing, because it is a property of Ranked Robin that BV's suite has no test
for and that Moulin's theorem guarantees is there.

A smaller relative that *is* proved: Black's Procedure fails at **three** candidates and 8 voters —
`1:A>C>B, 3:B>A>C, 4:C>B>A` elects B, and removing the `A>C>B` voter elects C, which that voter
prefers. Useful as documentation that Moulin's four-candidate bound is about what is *possible*, not
about what every method does.

## Ballot format

BV's CSV importer is rank-column, per `frontend/.../cvrParsers.tsx` (ported from FairVote's
`rcv_cruncher`): a header of `rank1, rank2, …` plus an id column, one row per ballot, with the literal
markers `skipped` and `overvote`. Profile 1 above:

```csv
Index,rank1,rank2,rank3
1,A,B,C
...(6 rows)
7,C,A,B
...(5 rows)
12,B,C,A
...(4 rows)
16,B,A,C
17,B,A,C
```

Unit fixtures in `IRV.test.ts` do not use CSV — they build ballot objects directly, so a test
contribution should follow the existing shape in that file rather than the importer's.

## Status: item 3 posted to #1468; items 1–2 not filed

The Ranked Robin material went to
[Equal-Vote/bettervoting#1468](https://github.com/Equal-Vote/bettervoting/issues/1468#issuecomment-5160176044)
on 2026-08-02, as a comment rather than a new issue. It fits there precisely: #1468 is about the
**pairwise-runoff rung** in `singleWinnerRankedRobin`, and both winners in the five-ballot profile come
off that same rung — so it is a smaller vehicle (5 ballots, 4 candidates) than the issue's own repro
(21 ballots, 5 candidates) for asserting that the starred chart row equals `results.elected`.

The comment is explicit that the tabulation was computed and hand-checked but the **display behaviour
was not tested**, and that the no-show paradox is a guaranteed property rather than a bug.

The two IRV fixtures below were deliberately **kept out** of that thread — they are unrelated to the
Ranked Robin display bug, and dumping them into someone's specific bug report is how a useful comment
becomes noise. They remain unfiled, and the draft below is still the text for them if they ever go
anywhere.

## Draft issue for items 1–2 — NOT FILED

> **Title:** Add regression tests for known RCV pathologies (monotonicity, method disagreement)
>
> **Body:**
>
> `IRV.test.ts` currently covers ballot handling — majority, multiwinner, two-round, exhausted
> ballots, overvotes — but has no test for the method's documented pathologies. Grepping the suite for
> `condorcet|monoton|no-show|paradox|cycle` returns nothing.
>
> Proposing three fixtures. The first two are taken from Eric Pacuit's *Voting Methods* entry in the
> Stanford Encyclopedia of Philosophy (§3.2 and §2.1), so their expected values have a citable source
> rather than being whatever the implementation happened to return when the test was written. The
> third is derived from a theorem the same entry states (§3.3) and computed against this repo's own
> tabulator.
>
> **1. Monotonicity (17 ballots, no tiebreak).** Two profiles differing only in two voters who move A
> from 2nd to 1st. Profile 1: `6:A>B>C, 5:C>A>B, 4:B>C>A, 2:B>A>C` → eliminate C, **A wins 11–6**.
> Profile 2: `6:A>B>C, 5:C>A>B, 4:B>C>A, 2:A>B>C` → eliminate B, **C wins 9–8**. Raising A loses A the
> election. Neither profile has a Condorcet winner (cycle A>B>C>A), so this is purely a monotonicity
> fixture.
>
> **2. Method disagreement (19 ballots).** `7:A>B>C>D, 5:B>C>D>A, 4:D>B>C>A, 3:C>D>A>B` gives
> Plurality-with-Runoff → A, IRV → D, Coombs → B, Borda → B, and no Condorcet winner (Copeland ties B
> and C). A cross-method fixture for RCV vs Ranked Robin on one ballot set.
>
> **3. No-show paradox in Ranked Robin (5 ballots, deterministic).** `2:C>B>A>D, 2:D>A>C>B, 1:B>A>D>C`
> → Copeland A2 B2 C1 D1, contenders {A,B}, B beats A, **B wins**. Remove one `D>A>C>B` ballot →
> Copeland A1.5 B2 C2 D0.5, contenders {B,C}, C beats B, **C wins** — and that voter ranks C above B,
> so voting cost her the better outcome. Both winners come off the pairwise-runoff rung, so there is
> no random tiebreak to make the test flaky. Moulin's theorem guarantees this exists for any
> Condorcet-consistent method at four or more candidates; five voters is the minimum by exhaustive
> search, and at three candidates Ranked Robin is clean across all 12,375 profiles up to 11 voters.
> Not a bug — a documented property worth pinning so a future tiebreak change doesn't move it silently.
>
> Happy to write these as PRs in the existing `IRV.test.ts` / `RankedRobin.test.ts` style. Also happy
> to be told the suite is deliberately scoped to plumbing.

## Related local material

- [sep-voting-methods](sep-voting-methods.md) — the source note, findings 1, 8 and 9
- [`code/sep-voting-methods/verify.py`](code/sep-voting-methods/verify.py) — where every number above
  is recomputed
- [`code/sep-voting-methods/ranked_robin_noshow.py`](code/sep-voting-methods/ranked_robin_noshow.py) —
  Ranked Robin as BV implements it, and the no-show search behind item 3
- [ranked-robin-results-explained](ranked-robin-results-explained.md) — BV's tie-break ladder, and
  issue #1468, the closest existing work to item 3
- [sep-star-suggestion-email](sep-star-suggestion-email.md) — the other outbound draft from this note
