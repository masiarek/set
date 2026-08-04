# Two Bloc STAR fixtures out of the BPML docs, re-run

The BetterVoting QA material for Bloc STAR lives in a small tree of Google Docs hanging off
[**Bloc STAR Voting / Basic Multi-Winner STAR Voting**](https://docs.google.com/document/d/1XsfRVA6zdHFRAkRCMyxBTK18WIDq03vSRKpJLnrHxC4/edit) —
the naming doc linked from [bettervoting#904](https://github.com/Equal-Vote/bettervoting/issues/904).
Two of the docs it links carry real ballot profiles with engine output pasted in. Both are recorded
here because they are otherwise only in Drive, and both were re-run before being written down.

Engine: `starvote` 2.0.6 (local checkout). Where the upstream repo is quoted, it is HEAD at 2.1.6.

*(Which BetterVoting issues these notes back with recomputation:
[bettervoting-issues.md](bettervoting-issues.md).)*

---

## The name is "Bloc STAR", not "STAR Bloc"

This is the finding worth acting on, because [#904](https://github.com/Equal-Vote/bettervoting/issues/904)
asks for exactly one string and proposes the wrong one.

| Source | Name |
|---|---|
| The BPML naming doc itself | "Bloc STAR Voting / Basic Multi-Winner STAR Voting" |
| [STAR Voting technical specifications](https://www.starvoting.org/technical_specifications) 1.c / 1.e | *"Bloc STAR Voting" or "Basic Multi-Winner STAR Voting"* |
| [starvoting.org/multi_winner](https://www.starvoting.org/multi_winner) | Bloc STAR |
| [electowiki](https://electowiki.org/wiki/Bloc_STAR_Voting) | Bloc STAR Voting |
| `starvote` | `starvote.Bloc_STAR_Voting` |

Adjective first, in all five. #904's **Should-Be** says "STAR Bloc Voting", and that string had been
carried forward into the sizing note and the planned i18n key.

The internal argument agrees. `en.yaml:161` already ships the sibling method as **Proportional STAR
Voting** — adjective first — and the two names render one above the other in the same method list.
The adjective keys that already exist pair the same way: `bloc_multi_winner_adj: Bloc` /
`proportional_multi_winner_adj: Proportional`. And the help page in
[#1474](https://github.com/Equal-Vote/bettervoting/pull/1474) uses "Bloc STAR" in every occurrence, so
landing "STAR Bloc" would put two names for one method on one site.

Raised on the issue 2026-08-04:
[comment](https://github.com/Equal-Vote/bettervoting/issues/904#issuecomment-5178824529). Note that
`star-voting-library` also uses `02_STAR_Bloc/` in its published paths, so a decision here has a second
place to propagate to.

---

## Fixture 1 — three ballots, two seats, a tie no rung can break

From [*Unbreakable Tie (bloc - two seats)*](https://docs.google.com/document/d/1oVByGI83PMYnVgFOYMu8Xh5vCE_oV0Vvsj5xPXelqKU/edit).
A Latin square: every candidate takes each of 3, 4 and 5 exactly once.

```text
[options]
seats = 2
method = bloc
tiebreaker = none

[ballots]
a = 3   b = 4   c = 5
a = 5   b = 3   c = 4
a = 4   b = 5   c = 3
```

Totals 12 / 12 / 12. Every rung ties in turn — head-to-head (each candidate beats one and loses to
one, a clean 3-cycle), then the five-star count (one apiece) — and the engine gives up:

```text
[Bloc STAR: Round 1: Scoring Round: Unbreakable Tie]
  Tie between a, b, and c.
```

Confirmed locally: `UnbreakableTieError` at round 1. The value of this one is that it is the smallest
profile where **BetterVoting and the reference engine legitimately disagree** — BV resolves it by
random draw and elects B then A, `starvote` with `tiebreaker = none` refuses. Both are correct
behaviour; they are answers to different questions. It is the natural companion to the tie material in
[bv-sep-test-cases](bv-sep-test-cases.md).

### The doc's own ballot table does not reproduce it

The doc states the ballots three times: a plain `A,B,C` listing, a rendered Andre/Blake/Carmen table,
and the `[ballots]` block above. **The table disagrees with the other two.**

| | row 1 | row 2 | row 3 | totals | result |
|---|---|---|---|---|---|
| listing + `[ballots]` | 3,4,5 | 5,3,4 | 4,5,3 | 12 / 12 / 12 | unbreakable tie ✓ |
| rendered table | 3,4,5 | 4,5,3 | **5,4,3** | 12 / **13** / **11** | no tie at all; winners B then A |

Row 3 should be `4,5,3`. Anyone rebuilding the case from the table gets a different election and never
sees the tie the doc is about. Verified both ways.

---

## Fixture 2 — nine ballots, six candidates, three seats

From [*Bloc Voting: seats = 3 and candidates = 6*](https://docs.google.com/document/d/1jwlC0klDwz_13Sg8fZGqKYVBVJ3zCjN7hnD-zgRMbc4/edit).
Three ballot groups:

| ×  | Johnny Cash | Elvis Presley | Santa Claus | The Lesser Evil | Someone I Like | Apocalypse Now |
|---|---|---|---|---|---|---|
| 3 | 0 | 2 | 4 | 3 | 5 | 0 |
| 4 | 2 | 1 | 3 | 4 | 3 | 2 |
| 2 | 1 | 1 | 5 | 2 | 5 | 0 |
| **score** | **10** | **12** | **34** | **29** | **37** | **8** |

Winners **Someone I Like → Santa Claus → The Lesser Evil**. Confirmed against the engine; the seat
totals and every runoff line match the output pasted in the doc.

### What makes it worth keeping: the seat-1 runoff is 3–0 with six abstentions

| seat | finalists | runoff | Equal Support | winner's label on the chart |
|---|---|---|---|---|
| 1 | Someone I Like vs Santa Claus | 3 – 0 | **6 of 9** | **33.3%** |
| 2 | Santa Claus vs The Lesser Evil | 5 – 4 | 0 | 55.6% |
| 3 | The Lesser Evil vs Elvis Presley | 9 – 0 | 0 | 100% |

Two thirds of the electorate scored the seat-1 finalists identically — both are broadly liked, so
almost nobody distinguishes them — and the seat is carried 3–0 by the third who did. This is
[#1471](https://github.com/Equal-Vote/bettervoting/issues/1471) in its starkest form so far: a winner
labelled **33.3%** on the same axis as a "majority threshold" drawn at 1.5 votes, which is 16.7% of
that axis. See [results-chart-denominators](results-chart-denominators.md).

**It also cuts against an expectation recorded in
[bv-1471-bloc-comment-posted](bv-1471-bloc-comment-posted.md).** That note reasons that Equal Support
should be *largest in later seats*, since the strongest candidates have been elected and removed and
what is left are pairs voters were most indifferent between. Here it runs the other way round —
Equal Support is 6, 0, 0 — because the indifference was concentrated at the top, between two
front-runners nearly everyone scored alike, while the later pairs were sharply distinguished. The
mechanism in that note is real, but it is a tendency and not a rule, and a maintainer testing the
claim could land on a profile like this one. Worth stating as "where the two denominators diverge
most is profile-dependent, and can be seat 1."

---

## A `starvote` bug the tie fixture walks into

Running fixture 1 raises:

```text
UnbreakableTieError: Round 1: Scoring Round: {int_to_words(len(tie), flowery=False)}-way tie in Scoring Round
```

Two `break_tie` calls in `_star_round()` are missing the `f` prefix, so the template leaks verbatim
instead of reading "three-way tie". Still present at upstream HEAD — `starvote/__init__.py:1690`
(Scoring Round) and `:1717` (Automatic Runoff Round), v2.1.6. The two sibling call sites at `:1979` and
`:2350` have the `f`, which is what makes it plainly a typo rather than a convention.

`_star_round()` backs both single-winner STAR and Bloc STAR, so this reaches any STAR tie that gets as
far as a custom tiebreaker or `tiebreaker=None`. Cosmetic — the exception type, the tie set and the
control flow are all correct — but it lands in the message a caller logs or shows a user. Not yet
filed; would be the second open report on that repo after
[#17](https://github.com/larryhastings/starvote/issues/17) ([sequentially-spent-score](sequentially-spent-score.md)).

---

## A third fixture, not from the docs — bloc STAR ≠ top *k* scorers

Constructed here while checking the [glossary](glossary.md) entry for bloc methods, which said bloc
approval, bloc score **and bloc STAR** are all "top *k* totals win". The first two are. Bloc STAR is
not, because it repeats the *runoff* as well as the scoring round, and a runoff can overturn a score
lead. Five ballots are enough to separate them:

```text
3 ballots:  A = 3   B = 5   C = 4
2 ballots:  A = 5   B = 0   C = 0
```

Scores **A 19, B 15, C 12**. Bloc score, two seats, takes the top two totals: **A and B**. Bloc STAR:

- seat 1 — A (19) and B (15) are finalists; three voters prefer B, two prefer A → **B**
- seat 2 — B removed; A (19) and C (12) are finalists; three voters prefer C, two prefer A → **C**

Winners **B then C**, and the candidate with the highest score by four points takes no seat at all.
Confirmed against the engine. Worth keeping as the one-line answer to "isn't bloc just top-*k*?", and
as a reminder that the score column on a Bloc STAR results page does not predict the winner set.

## The rest of the doc tree, briefly

- [*Multi-winner - Block STAR Voting - BPML - L3*](https://docs.google.com/document/d/1IGfMQtBGLDVSdY5TkY1A8IV_eOrV12Vay9mGoIMesdQ/edit) — a stub. Its only content is the open question "What to copy from this document".
- [*Bloc Voting - General*](https://docs.google.com/document/d/1bEe-afCD3XAndI2N4FuTuS4dAANWa1hM1IqWw6CRCas/edit) — a paraphrase of Wikipedia's *plurality block voting*. Nothing method-specific.
- [*BV1225 — Approve a slate of candidates*](https://docs.google.com/document/d/1y8Wct7g4bHSLp6MBUc59XX9eaiuHuXNzILYb5jj6QxE/edit) — about slates rather than Bloc STAR, but it carries the **Hugo Awards** episode: roughly 400 of ~1800 nominators voting an agreed slate could take an entire category shortlist, which is the majority-sweeps-every-seat failure of bloc methods happening in a real election with real consequences. Fixed in 2017 by moving to [E Pluribus Hugo](https://electowiki.org/wiki/E_Pluribus_Hugo), a proportional rule. A better citation than an abstract 55/45 board for the "not proportional" warning on the [#1474](https://github.com/Equal-Vote/bettervoting/pull/1474) help page, if that page ever wants one.

## What's checked and what isn't

- **Checked:** both fixtures re-run through `starvote` 2.0.6 — winners, totals and the unbreakable-tie
  error. Both variants of the fixture-1 ballot table run separately to establish which one is wrong.
  The runoff tallies and Equal Support counts for fixture 2 hand-computed as well as engine-run, and
  they match the output pasted in the doc. The `f`-prefix bug read from upstream source at HEAD.
- **Derived, not observed:** the "33.3% label, threshold at 1.5 votes" reading for fixture 2. The
  33.3% is the figure in the doc's own results table; the threshold position is computed from
  `ResultsBarChart.tsx` as it stands on `main` (`sum` drops the Equal Support row, `m = sum/2`).
  Fixture 2 has not been re-run as a live election on bettervoting.com — [`fk38pk`](https://bettervoting.com/fk38pk/results)
  in [bv-1471-bloc-comment-posted](bv-1471-bloc-comment-posted.md) is the one with screenshots.
- **Not checked:** the *screenshots and issue reports* inside those docs, which are from the
  `star-vote.herokuapp.com` era (2023) and describe a UI two rewrites ago — "only one winner is marked
  with a Star", "the report is cut off", missing zeros in the ballot CSV. Any of them may have been
  fixed years ago. They are not carried into this note as findings, only noted as unverified history.
- **Not established:** whether Equal Vote has a house preference on "Bloc STAR" vs "STAR Bloc". Five
  sources say Bloc STAR; nobody upstream has answered yet.
