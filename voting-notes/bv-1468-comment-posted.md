Two compact profiles that exercise the **same runoff rung** this issue is about, offered as regression fixtures for whatever fix lands — the current repro is 21 ballots and 5 candidates, and these are 5 ballots and 4.

## A minimal runoff-rung profile

Candidates `A,B,C,D`. Sandbox input (rank per candidate, in candidate order):

```
2:3,2,1,4
2:2,4,3,1
2,1,4,3
```

which is

```
2  C>B>A>D
2  D>A>C>B
1  B>A>D>C
```

Copeland (with ½ per pairwise tie, per `Util.ts`): **A 2, B 2, C 1, D 1**. A and B tie at the top, B beats A head-to-head, so B wins on the `preferred over ... in runoff` rung — the deterministic rung named in this issue. Every pairwise comparison here is decisive, so there is no random tiebreak anywhere in the profile.

That makes it a smaller vehicle for the assertion this issue implies: after the fix, the starred row of the head-to-head chart should equal `results.elected`. I have **not** run the frontend against it — I computed the tabulation side only (a reimplementation of `singleWinnerRankedRobin` plus the `copelandScore` rule at `Util.ts`, cross-checked by hand on all twelve pairwise comparisons). So treat the display behaviour as unverified and the tabulation as checked.

## The same profile, minus one ballot — a second runoff-rung case, and a no-show paradox

Drop **one** of the two `D>A>C>B` ballots:

```
2:3,2,1,4
2,4,3,1
2,1,4,3
```

Copeland becomes **A 1.5, B 2, C 2, D 0.5**. Now B and C tie at the top, C beats B head-to-head, so **C** wins — again on the runoff rung, again with no random tiebreak.

So the pair gives two runoff-rung outcomes off almost the same ballots, which is convenient for a table-driven test.

It is also worth pinning for its own sake. The voter who was removed ranks `D>A>C>B` — she prefers **C** to **B**, and her ballot is what made **B** win. Voting cost her the better outcome: a **no-show paradox**.

This is **not a bug.** Moulin's theorem says every Condorcet-consistent method is susceptible to the no-show paradox once there are four or more candidates, and Ranked Robin is Condorcet consistent, so this is guaranteed to exist and no tie-breaking change can remove it. The reason to have it as a test is that it is a documented property sitting right next to the code this issue touches, and a fixture stops a future tiebreak refactor from moving it silently.

Two results from the search, in case they are useful for choosing test sizes:

- **Five ballots is the minimum.** Exhaustive over all 26,561 anonymized 4-candidate profiles with 1–5 voters; nothing smaller works.
- **At three candidates Ranked Robin does not fail at all** — no no-show paradox in any of the 12,375 anonymized 3-candidate profiles up to 11 voters. So a three-candidate test would assert the wrong thing. Ranked Robin lands on the same side of Moulin's bound as minimax, and not with methods like Black's Procedure, which fails at three candidates and eight voters.

## Offer

Happy to send these as a PR adding cases to `RankedRobin.test.ts`, either alongside the fix or independently of it. Equally happy to be told the suite is deliberately scoped to ballot handling and that pathology fixtures are not wanted — the tabulation numbers above stand either way.

Separately, I have two IRV fixtures in the same vein (a 17-ballot monotonicity failure, and a 19-ballot profile where Plurality-runoff, IRV, Coombs and Borda give three different winners). Those are unrelated to this issue, so I have kept them out of it — say the word and I will open something separate.
