# The accidental example: 75 ballots, four methods, four winners

Source: Lumen Learning, *Mathematics for the Liberal Arts*, Module 7 —
["Putting It Together: Voting Theory"](https://courses.lumenlearning.com/wmopen-mathforliberalarts/chapter/putting-it-together-voting-theory/).
All numbers below re-derived from the ballots on 2026-08-01 with
[`code/lumen-75-ballot/verify.py`](code/lumen-75-ballot/verify.py) — 15 assertions, no dependencies, `python3 verify.py`.

Every worked center-squeeze example in these notes so far was **built by someone making a point**: LeGrand's "silly
Hare example" with its loaded names, the 5-candidate left-right spectrum, the origin thread's showcase cycles
([details](hare-center-squeeze-examples.md)). Their weakness is always the same — a constructed example proves
possibility, which was never in dispute.

This one is different. It's the closing recap exercise in a freshman general-education math course, written to
illustrate "different methods give different answers," by authors with no reform agenda and no apparent idea what
else is in their own ballots. **It is a clean IRV pathology found in the wild, in a textbook that doesn't notice.**

## The profile

Senior class president, 75 ballots, four candidates:

```
20:Garcia>Lee>Nguyen>Smith
 3:Garcia>Nguyen>Lee>Smith
 8:Lee>Nguyen>Garcia>Smith
16:Nguyen>Garcia>Lee>Smith
28:Smith>Lee>Garcia>Nguyen
```

Smith is a polarising 37% bloc: most first preferences (28) and **last on 47 of 75 ballots** — a majority. Garcia is
the broad compromise. Lee is nearly everyone's second choice and almost nobody's first (8).

Pairwise matrix (row = "for", column = "against"; **bold** = winning side; every pair sums to 75):

| for \ against | Garcia | Lee | Nguyen | Smith |
|---|---|---|---|---|
| **Garcia** | — | **39** | **51** | **47** |
| **Lee** | 36 | — | **56** | **47** |
| **Nguyen** | 24 | 19 | — | **47** |
| **Smith** | 28 | 28 | 28 | — |

> The page prints this transposed (its columns are the winners), which is the reverse of LeGrand's convention and
> of every other matrix in these notes. Same data, and its stated conclusion is right.

## What the page shows

| Method | Winner | How |
|---|---|---|
| Plurality | **Smith** | 28 vs 23 / 16 / 8 — while last on 47 ballots |
| Borda (4/3/2/1) | **Lee** | 214 vs Garcia 212 — a 2-point gap |
| IRV / Hare | **Nguyen** | see trace below |
| Condorcet | **Garcia** | beats all three: 39–36, 51–24, 47–28 |

Its arithmetic is correct throughout — Borda totals sum to 750 = 75 × 10, every pairwise pair sums to 75. The page
then asks "Which voting method do you think is the most fair?" and stops.

## What the page doesn't say

**Garcia beats every opponent head-to-head and loses under all three other methods.** The page reports the Condorcet
winner as the fourth of four answers, as if it were one more arbitrary convention, and never names the failure. It
also never uses the words *center squeeze*, *monotonicity*, or *Condorcet criterion* — the last of which it has just
demonstrated a violation of.

**Ranked Robin elects Garcia**, at the first step, without needing its tiebreak ladder:

| | Garcia | Lee | Nguyen | Smith |
|---|---|---|---|---|
| Matchup wins (Copeland) | **3** | 2 | 1 | 0 |
| Sum of margins | +49 | **+53** | −45 | −57 |

A total order, no cycle, no tie — so the [1st-Degree tiebreaker never fires](ranked-robin-vse-run.md), consistent
with the VSE finding that unresolved Ranked Robin ties are overwhelmingly clone dead heats rather than cycles.
Minimax and Coombs also elect Garcia.

### The wrinkle worth keeping: Ranked Robin's two steps disagree here

Garcia leads on **wins** (3 vs 2); Lee leads on **margins** (+53 vs +49). Had the ladder been ordered
margins-first, this profile would elect Lee — the Borda winner.

That isn't a coincidence. Sum-of-margins is an affine image of Borda: with points *k*…1,
`margin(c) = 2·Borda(c) − N(k+1)`, here `2·Borda − 375`, which `verify.py` checks exactly for all four candidates.
So "Copeland wins, then margins" is literally "Condorcet, then Borda as the runner-up rule," and this profile is a
compact demonstration that the two halves of that ladder can point at different people. Useful counterweight to the
VSE result that the margins step is outcome-neutral in aggregate — neutral on average is not neutral always.

### It hangs on one vote

IRV's trace:

| Round | Garcia | Lee | Nguyen | Smith | Action |
|---|---|---|---|---|---|
| 1 | 23 | **8** | 16 | 28 | Lee eliminated; all 8 → Nguyen |
| 2 | **23** | — | **24** | 28 | **Garcia eliminated, by one vote** |
| 3 | — | — | **47** | 28 | Nguyen wins |

The Condorcet winner is eliminated at 23 against Nguyen's 24. One ballot the other way and IRV joins everyone else
on Garcia. That's narrower than the 2-ballot margin in the calculator's famous 99-voter example — and unlike that
one, nobody tuned it.

## Three things I ran that the page doesn't

**1. It's non-monotonic, and dramatically so.** Take 6 of the 28 `Smith>Lee>Garcia>Nguyen` voters and have them
promote Nguyen — the eventual winner — from *last* to *first*:

| Round | Garcia | Lee | Nguyen | Smith | Action |
|---|---|---|---|---|---|
| 1 | 23 | **8** | 22 | 22 | Lee eliminated |
| 2 | 23 | — | 30 | **22** | Smith eliminated (not Garcia) |
| 3 | **45** | — | 30 | — | **Garcia wins** |

Nguyen loses *because* Nguyen was ranked higher. Promoting Nguyen drains Smith below Garcia, so Smith takes the
round-2 elimination instead, and Smith's ballots — which rank Garcia above Nguyen — elect Garcia. The six voters who
raised Nguyen to first thereby got their **last** choice. The paradox holds for any 6 to 13 of those 28 ballots, and
the Condorcet winner stays Garcia throughout. This is a live [monotonicity](glossary.md) failure sitting in a
gen-ed textbook.

**2. Garcia's own supporters are punished for sincerity.** The 20 `Garcia>Lee>Nguyen>Smith` voters get Nguyen —
their third choice. If 8 of them abandon Garcia and rank Lee first, Lee wins: their **second** choice. Sincere
first-preference support for the Condorcet winner is strictly worse for them than betraying him. Textbook
[favorite betrayal](glossary.md), and it directly contradicts FairVote's "ranking another candidate second will not
hurt your first choice" framing — true as stated, but it's the *first* ranking that's unsafe here.

**3. Both losers are spoilers.** Remove Nguyen and IRV elects Garcia. Remove Smith and IRV elects Garcia. Neither is
a clone of anyone; they are ordinary rivals whose mere presence flips the result away from the pairwise winner.

## The approval-voting hole

The module teaches approval voting one page earlier, then omits it from this comparison. That omission is the most
interesting thing on the page, because approval **has no determinate answer here** — the winner is whatever the
voters' thresholds say it is:

| Assumption | Garcia | Lee | Nguyen | Smith | Winner |
|---|---|---|---|---|---|
| Approve top 1 | 23 | 8 | 16 | **28** | Smith |
| Approve top 2 | 39 | **56** | 27 | 28 | Lee |
| Approve top 3 | **75** | **75** | 47 | 28 | Garcia / Lee tie |

Three assumptions, three answers, and the third is an exact 75–75 tie (neither Garcia nor Lee is last on any
ballot). The top-2 row is also numerically identical to Bucklin at depth 2, which is where Bucklin stops — so
Bucklin gives a fifth reading of the same electorate.

This is precisely the objection to the module's own
["What's Wrong with Approval Voting?"](https://courses.lumenlearning.com/wmopen-mathforliberalarts/chapter/introduction-approval-voting/)
section, which "proves" a majority-criterion violation by *stipulating* that "every voter marked approval of their
top two candidates." Pick a different stipulation and you get a different winner; the stipulation is doing all the
work. A ranked profile does not determine an approval outcome, and that — not the textbook's rigged example — is
the real difficulty with approval voting.

## Is it a useful example?

**Yes, and for a reason the other examples in these notes can't claim: nobody built it to win an argument.**

Against the two calculator examples ([notes](hare-center-squeeze-examples.md)):

- **It's provenance-clean.** The 99-voter example needs a disclaimer about its candidate names and a second one
  about its engineered 2:1 margins. This one needs neither. "The winner here is from a Lumen gen-ed textbook's own
  recap exercise" is an unusually hard opening to argue with.
- **Its margins are realistic.** Garcia beats Lee 39–36 — three votes. The 99-voter example's centrist wins
  pairwise by roughly 2:1, which no real electorate produces. Realistic margins are the whole reason this profile
  also happens to be non-monotonic; lopsided constructions rarely are.
- **It carries more failures per ballot.** Condorcet failure, non-monotonicity, favorite betrayal, two spoilers,
  and an approval-threshold indeterminacy — in 5 ballot types. Example 2 shows the mechanism more vividly but
  exhibits fewer distinct pathologies.
- **It's weaker on the "core support" defence.** Garcia has 23 first preferences, second-most — good enough to
  refuse the "no real support" dismissal, but not the outright lead that makes Example 2 unanswerable. Example 2
  is still the better single choice when the argument is specifically about first-choice enthusiasm.
- **It shares Example 1's knife-edge problem.** One vote. Anyone can say "so it's a coin flip, so what" — and the
  honest reply is that a method whose answer differs from the pairwise winner on a coin flip is the point, not a
  defect in the example.

**Verdict:** the best persuasion example in these notes, because of where it comes from rather than what it shows.
Lead with the provenance, show the 23-vs-24 round, then the monotonicity table — a textbook that set out to
demonstrate "methods disagree" accidentally demonstrated that IRV can eliminate the pairwise winner by one vote and
then punish the voters who tried to help the eventual winner. Keep Alaska 2022 for real-ballot evidence
([details](rcv-and-core-support.md)); keep Example 2 for the core-support argument; use this one to open.

## Related local material

- [hare-center-squeeze-examples.md](hare-center-squeeze-examples.md) — the two constructed examples this one is
  measured against
- [ranked-robin-vse-run.md](ranked-robin-vse-run.md) — the margins step's aggregate neutrality, which the
  wins/margins disagreement above qualifies
- [ranked-robin-results-explained.md](ranked-robin-results-explained.md) — Copeland matchup wins vs. ballot counts
- [rcv-and-core-support.md](rcv-and-core-support.md) — Alaska 2022 and the first-rankings argument
- [legrand-ranked-ballot-methods.md](legrand-ranked-ballot-methods.md) — Minimax, Coombs, Bucklin, and the
  compliance table
- [glossary.md](glossary.md) — center squeeze, Condorcet winner, Copeland, monotonicity, favorite betrayal, spoiler
