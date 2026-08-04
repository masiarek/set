A Bloc STAR instance of this, on an election that is already live — and the smallest form I can get it into: **two bars touching the line at once.**

[`fk38pk`](https://bettervoting.com/fk38pk/results) is an old QA election of mine — 3 candidates, 2 seats, 3 ballots. Its results page paginates one card per seat, and the two cards happen to be a before/after of this issue inside a single election.

### Seat 1 — the two denominators coincide, and the chart is right

<img src="https://raw.githubusercontent.com/masiarek/set/master/voting-notes/img/bv1471-bloc-seat1-fk38pk.png" width="560" alt="Seat 1: scoring round A 12, C 2, B 1; runoff A 100% with the majority threshold line at mid-bar">

No ballot rates the two finalists equally, so the label denominator (all bars, `3 + 0 + 0`) and the marker's (`(3 + 0)/2`) are measured against the same 3 voters. A's bar reads 100%, the line sits at 50% of that axis. Nothing to report.

### Seat 2 — Equal Support is a third of the ballots

<img src="https://raw.githubusercontent.com/masiarek/set/master/voting-notes/img/bv1471-bloc-seat2-fk38pk.png" width="560" alt="Seat 2: runoff C 33%, B 33%, Equal Support 33%, with both candidate bars reaching the majority threshold line">

With A elected and removed, C and B each hold one preference and one voter rates them equally — bars `1 / 1 / 1`:

| | value | label shown | marker |
|---|:--:|:--:|---|
| C | 1 | **33%** | |
| B | 1 | **33%** | |
| Equal Support | 1 | 33% | |
| *majority threshold* | | | drawn at `(1+1)/2 = ` **1 vote** |

So the marker lands at exactly the height of **both** candidate bars, while their labels read 33%. Two bars touch a line labelled "majority threshold" in a runoff that **nobody won** — the seat went to the score rung, and the page says so at the top ("Tied! A and C won after tiebreaker", `tieBreakType: "score"`). The tabulation is right; I'd just expect a reader to conclude both candidates cleared a majority, when what happened is the opposite.

### Two things this adds to the report above

**1. Bloc STAR runs it once per seat.** `STARResultSummaryWidget` renders per `roundIndex`, so every seat draws its own runoff chart with its own marker. And later rounds are where I'd expect the Equal Support bar to be *largest* — the strongest candidates have already been elected and removed, so the pairs left over are the ones voters were most indifferent between. That's precisely where the two denominators diverge most, so the gap should be more visible in multi-seat races than in the single-winner examples in the issue, not less.

**2. `m = sum / 2` is half, not a majority.** At an even number of decided voters, a bar that *reaches* the line has exactly ½ — tied, not winning. Seat 2 is the degenerate case: both bars on the line, no majority anywhere on the chart. So if fix option 1 lands (label against the marker's denominator), the marker is worth making a strict majority in the same pass — `Math.floor(sum/2) + 1` for whole votes, or drawing the line just past ½ — otherwise the corrected chart shows 50% / 50% with both bars ending exactly on "majority threshold".

### The counts, for reference

Independently tabulated with Larry Hastings' [`starvote`](https://github.com/larryhastings/starvote) (my teaching fork, which adds the runoff-percentage line). Same winners as BetterVoting, same rung:

```text
--- Bloc STAR Voting Method (2 winners) ---
 Tabulating 3 ballots to fill 2 seats.
A,B,C
4,1,0
3,0,2
5,0,0

[Score Distribution] (how many ballots gave each star rating)
                Score
Candidate  5  4  3  2  1  0  | Total   Avg
A          1  1  1  0  0  0  |    12   4.0
B          0  0  0  0  1  2  |     1   0.3
C          0  0  0  1  0  2  |     2   0.7

Round 1: Scoring Round
 The two highest-scoring candidates advance to the next round.
   A             -- 12 -- First place
   C             --  2 -- Second place
   B             --  1
 A and C advance.

Round 1: Automatic Runoff Round
 The candidate preferred in the most head-to-head matchups wins.
   A             -- 3 -- First place
   C             -- 0
   Equal Support -- 0
 A wins.
   Voters with a preference: 3 of 3 (no Equal Support).
   A 3 (100%) vs C 0 (0%); majority = 2.

──────────────────────────────────────────────────
Round 2: Scoring Round
 The two highest-scoring candidates advance to the next round.
   C             -- 2 -- First place
   B             -- 1 -- Second place
 C and B advance.

Round 2: Automatic Runoff Round
 The candidate preferred in the most head-to-head matchups wins.
   B             -- 1 -- Tied for first place
   C             -- 1 -- Tied for first place
   Equal Support -- 1
 There's a two-way tie for first.

Round 2: Automatic Runoff Round: First tiebreaker
 The highest-scoring candidate wins.
   C             -- 2 -- First place
   B             -- 1
 C wins.

Winners — Bloc STAR Voting Method (2 winners)
 A
 C
```

<details>
<summary>And the single-winner control — one candidate holding every point on every ballot (no BV election for this one)</summary>

Worth having as a regression fixture for whichever fix lands: it is the case where all three denominators agree, so a correct chart must still show 100% with the marker at ½ and no Equal Support bar.

```text
--- STAR Voting Method (single winner) ---
 Tabulating 3 ballots.
A,B,C
5,0,0
5,1,0
5,0,0

[Score Distribution] (how many ballots gave each star rating)
                Score
Candidate  5  4  3  2  1  0  | Total   Avg
A          3  0  0  0  0  0  |    15   5.0
B          0  0  0  0  1  2  |     1   0.3
C          0  0  0  0  0  3  |     0   0.0

Scoring Round
 The two highest-scoring candidates advance to the next round.
   A             -- 15 -- First place
   B             --  1 -- Second place
   C             --  0
 A and B advance.

Automatic Runoff Round
 The candidate preferred in the most head-to-head matchups wins.
   A             -- 3 -- First place
   B             -- 0
   Equal Support -- 0
 A wins.
   Voters with a preference: 3 of 3 (no Equal Support).
   A 3 (100%) vs B 0 (0%); majority = 2.

Winner — STAR Voting Method (single winner)
 A
```

</details>

Both elections, the three denominators side by side, and the ballots as runnable YAML: [Over 50% — what a landslide actually buys](https://masiarek.github.io/star-voting-library/02_STAR_Bloc/01_Learn/over_50_percent.html) · [the BV1815 case page](https://masiarek.github.io/star-voting-library/02_STAR_Bloc/02_Examples/bv1815_bloc_3c2s_basic.html).

**What's checked and what isn't:** the tabulation is verified two ways (the LH engine above and BetterVoting's own export for `fk38pk`, which agree on winners, runoff counts and `tieBreakType`). The chart readings are from the screenshots above, taken from the live page today; the label/marker arithmetic matches `ResultsBarChart.tsx` as it stands on `main`. I have not tested any proposed fix.
