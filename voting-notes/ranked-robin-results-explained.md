# Ranked Robin results pages, explained (why 12 ballots can show "1 win")

Source: BetterVoting's Ranked Robin results screen — the screenshots from
[bettervoting#885](https://github.com/Equal-Vote/bettervoting/issues/885) (election
[tcvc7r](https://bettervoting.com/tcvc7r/results)) and
[bettervoting#886](https://github.com/Equal-Vote/bettervoting/issues/886) (election
[p6vr9k](https://bettervoting.com/p6vr9k/results), test case BV1550, 3 candidates, 12 ballots).

## The short answer

Yes — **1 win, 1 win, 0 wins is correct**, and so is "12 voters." The page mixes two different
units, and that's the whole confusion:

| Number on screen | What it counts | Unit |
|---|---|---|
| "12 voters" | Ballots cast | **people** |
| "# Wins" (the 1 / 1 / 0 bars) | Head-to-head **matchups won** | **matchups** |
| Matchup bars (42% / 17% / 42%) | How the 12 voters split inside one matchup | **people** |
| "Win Rate" (50%) | Wins ÷ possible matchups (n − 1) | **matchups** |

Think of a **round-robin sports tournament** with 3 teams. Each pair plays one game, so each team
plays 2 games. The 12 voters are the judges who decide every game. The standings show **games won
(0–2)**, never the number of judges. Expecting "6 wins" is expecting the standings to show points
scored instead of games won.

With *n* candidates each candidate has *n − 1* matchups, so the most wins anyone can show here is
**2**, no matter whether 12 or 12,000 people voted. This score is the **Copeland score** — the
field in the tabulator is literally named `copelandScore`.

## Worked example: BV1550 (Ann, Bob, Cal — 12 ballots)

The actual ballots from the CSV attached to #886 (rank 1 = favorite; blank = unranked, which
counts below every ranked candidate; two blanks on the same ballot = no preference between them):

| # | Ann | Bob | Cal |
|---|-----|-----|-----|
| 1 | 1 | 2 | – |
| 2 | 1 | 2 | – |
| 3 | – | 2 | 1 |
| 4 | – | 1 | 1 |
| 5 | 1 | 2 | – |
| 6 | 1 | 2 | – |
| 7 | 1 | 2 | – |
| 8 | – | 2 | 1 |
| 9 | 2 | 1 | – |
| 10 | 1 | 1 | 1 |
| 11 | – | 1 | – |
| 12 | – | – | 1 |

Score every pairing across all 12 ballots ("game 1", "game 2", "game 3"):

| Matchup | For left | Equal | For right | Result |
|---|---|---|---|---|
| **Ann vs Bob** | 5 (ballots 1,2,5,6,7) | 2 (ballots 10,12) | 5 (ballots 3,4,8,9,11) | **5–5 draw** |
| **Ann vs Cal** | 6 (1,2,5,6,7,9) | 2 (10,11) | 4 (3,4,8,12) | **Ann wins** |
| **Bob vs Cal** | 7 (1,2,5,6,7,9,11) | 2 (4,10) | 3 (3,8,12) | **Bob wins** |

These are exactly the bars in the screenshots: Ann–Bob 42% / 17% / 42% is 5/12, 2/12, 5/12; Ann–Cal
50% / 17% / 33% is 6/12, 2/12, 4/12. Every matchup row sums to 12 voters — the "12" and the "1"
coexist because they measure different things.

Final standings (the "# Wins" chart):

| Candidate | Matchups won | Win Rate (of n − 1 = 2) |
|---|---|---|
| Ann (A) | 1 (beat Cal; drew Bob) | 50% |
| Bob (B) | 1 (beat Cal; drew Ann) | 50% |
| Cal (C) | 0 | 0% |

A drawn matchup gives **neither** candidate a win — that's why 1 + 1 + 0 = 2 wins total instead of
3. (Some Copeland variants award ½ for a draw; BetterVoting's does not.)

## So who won — and why it looked "unstable"

Ann and Bob tie at 1 win each. The tabulator
([RankedRobin.ts](https://github.com/Equal-Vote/bettervoting/blob/main/packages/backend/src/Tabulators/RankedRobin.ts))
breaks ties in this order:

1. **Most matchup wins** (Copeland score) — Ann and Bob tied, so continue.
2. **If exactly two are tied: their own head-to-head** ("preferred over X in runoff") — but
   Ann–Bob was itself a 5–5 draw, so continue.
3. **Random pick.** The code logs: *"picked in random tie-breaker, more robust tiebreaker not yet
   implemented"* and sets `tieBreakType: 'random'`.

That third rung is why identical ballots produced different winners on different runs (the
"unstable tie breaking" I reported in #885), and why the header cheerfully says "A wins!" without
disclosing that a coin flip decided it. Both problems are tracked upstream:

- [#886](https://github.com/Equal-Vote/bettervoting/issues/886) — who won, Bob or Ann? Was the tie disclosed?
- [#1063](https://github.com/Equal-Vote/bettervoting/issues/1063) — deterministic tie-breaking using candidate lot numbers
- [#1432](https://github.com/Equal-Vote/bettervoting/issues/1432) — surface tie-break explanations in results UI + exports
- [#1168](https://github.com/Equal-Vote/bettervoting/issues/1168) — document that Ranked Robin uses Copeland tie-breaking
- [#885](https://github.com/Equal-Vote/bettervoting/issues/885) — closed as not-planned (the numbers were correct; this page is the explanation I wished the UI had)

## Common misreadings (the traps I fell into)

- **"I expected 6 wins and 6 wins."** 6 is the number of *ballots* preferring Ann in her winning
  matchup (Ann > Cal on 6 of 12). "# Wins" counts *matchups*, so the ceiling is n − 1 = 2, not 12.
- **"Is it 12 voters or 2 voters?"** The wins chart sums to 2 (1 + 1 + 0), which looks like a tiny
  electorate. That 2 is *decided matchups*, not people; the 12 voters sit inside each matchup bar.
- **A 50% bar doesn't mean half the voters.** It means half the *possible matchups* (1 of 2).
