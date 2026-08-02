# Majority Judgment

Source: [Majority judgment (Wikipedia)](https://en.wikipedia.org/wiki/Majority_judgment) — read 2026-08-01

Every number below is checked by [`code/majority-judgment/verify.py`](code/majority-judgment/verify.py)
(no dependencies, `python3 verify.py`).

## What it's about

Grade every candidate on a verbal scale — Balinski and Laraki propose **Excellent, Very Good, Good,
Acceptable, Poor, Reject** — and elect whoever has the highest **median** grade. Ties on the median are
broken by stripping median grades one at a time until the medians separate.

It is the direct answer to the question left open in [score-voting](score-voting.md): sum, average, or
something else? Majority judgment says **none of the above — use the median**, and the entire case for the
method follows from that one substitution:

- The **mean** is moved by every ballot in proportion to how extreme it is, so exaggeration pays and score
  voting collapses toward approval under strategy.
- The **median** is moved only by ballots that cross it. A voter who hates a candidate can drag the mean
  down forever, but can only push the median down by one position no matter how hard they push.

That is a real and demonstrable property, and it is why this method exists.

There is a second, less mathematical claim underneath: the grades are supposed to be **words, not numbers**.
Balinski and Laraki argue "Excellent" carries an absolute, shared meaning that a 5 on someone's private 0–5
scale does not, which is what lets ballots be *compared* rather than merely added. Their slogan is *Judge,
don't vote.*

## Key takeaways

### Mechanics

- **Ballot**: a grade per candidate, from a verbal scale. Ties allowed, and you may grade as many or as few
  as you wish.
- **Winner**: highest median grade.
- **Tiebreak**: remove one median grade from each tied candidate, repeat until the medians differ.
  Equivalently, and how the verifier computes it: let *α* be the median, *p* the share strictly above, *q*
  the share strictly below. If *p > q* the candidate is **α+**, better the larger *p*; otherwise **α−**,
  better the smaller *q*. α+ beats α−.
- For an even electorate MJ takes the **lower** median, so a 50/50 split resolves downward.

### Lineage

- **Francis Galton, 1907** — a letter to *Nature* proposing the median for allocating budgets. The idea is
  older than every method in these notes except plurality.
- **Bucklin voting** — Progressive-Era US, and per this article **the first highest-median rule**. That is a
  direct link to [LeGrand's](legrand-ranked-ballot-methods.md) Bucklin, sitting in the glossary as a
  cumulative ranked method; the same rule read two different ways.
- **Trimmed means in judged sports** — Olympic figure skating drops extreme scores for exactly the reason MJ
  takes a median: to blunt biased or strategic judges. A hybrid, not a pure median.
- **Balinski & Laraki**: proposed 2007 (*PNAS*), book 2010 (MIT Press).
- **Variants**: **graduated majority judgment** and **usual judgment** keep the median but change the
  tiebreak (Fabre 2020); **MJU** (Varloot & Laraki 2022) lets voters express uncertainty.

### Where it has been used

- **2007 French presidential exit poll**, run by Balinski and Laraki themselves. Not nationally
  representative, but it agreed with other experiments: **François Bayrou** would have won under MJ and most
  other alternative rules, rather than Sarkozy, Royal or Le Pen. Their striking observation is that anyone
  who knew French politics could identify the four candidates from the grade distributions alone — "the
  grades contain meaningful information."
- Wine competitions, and further political research polling in France and the US.

No public government election. This is a research method with an experimental record, not an adopted one.

### Criteria

**Passes**: monotonicity, later-no-help, and **independence of irrelevant alternatives** — verified here
over 185,027 clean random profiles, no violation. IIA is structural: a candidate's median depends only on
the grades given to that candidate, and the tiebreak only ever compares candidates already tied.

**Fails**: Condorcet, Condorcet loser, later-no-harm, consistency, **participation**, **majority**, and
mutual majority.

The article footnotes three genuine softenings, and they are worth keeping straight because each is
narrower than it first sounds:

- **Majority**: MJ satisfies a weakened version — if exactly one candidate gets *perfect* grades from a
  majority, they win. The full criterion fails.
- **Later-no-harm**: MJ offers a weaker guarantee — grading another candidate *at or below your preferred
  winner's median* cannot hurt them. Note the bar is the winner's median, not your own grade for them.
- **Condorcet**: MJ passes it in strong Nash equilibrium, as score voting does. Under sincere grading it
  fails.

### The deepest thing in the article: MJ's participation failure is forced

Balinski and Laraki proved that **the only join-consistent methods are point-summing methods** — a mild
generalisation of score voting that includes positional rules. Precisely, the only methods satisfying
consistency have the form

    Σ f(score)   for some monotonic f

and any method satisfying participation *plus* either stepwise continuity or the Archimedean property
("respect for large electorates") is a point-summing method.

Read that backwards and it says: **if you want participation, you must essentially be score voting.** MJ's
no-show paradox is not a bug awaiting a patch in version 2 — it is the price of not being a summing method,
and it was proved by the method's own inventors. Their reply is empirical rather than formal: they claim
such failures would be rare in practice.

This is the sharpest framing available of the whole cardinal family. Mean and median are not two
implementations of one idea; they sit on opposite sides of a proved impossibility, and you are choosing
between **participation** and **strategy resistance**.

## 1. Tennessee — and a clause doing more work than it looks

Four grades: your own city Excellent, **the farthest city Poor**, and the rest Good / Fair / Poor for under
100 / under 200 / over 200 miles.

| Candidate | Memphis (42) | Nashville (26) | Chattanooga (15) | Knoxville (17) | Median |
|---|---|---|---|---|---|
| Memphis | excellent | poor | poor | poor | **poor** |
| Nashville | fair | excellent | fair | fair | **fair+** |
| Chattanooga | poor | fair | excellent | good | **fair−** |
| Knoxville | poor | fair | good | excellent | **fair−** |

Three candidates tie on a median of Fair. Nashville has 26 grades above it and **none below** → *fair+*.
Chattanooga and Knoxville each have 32 above and 42 below → *fair−*. Nashville wins, and Nashville is the
Condorcet winner. So far, so good.

**Now notice how fragile that is.** The rule has two clauses, and the second — "the farthest city gets
Poor" — reads like a throwaway. Drop it, keep only the mileage bands, and one cell changes: Nashville voters
would grade Memphis *fair* rather than *poor*, because Memphis is 194.2 miles away and the band boundary is
200.

That single cell gives Memphis a median of Fair with **42 above and 0 below — fair+ with p = 42**, which
beats Nashville's *fair+ with p = 26*. **MJ elects Memphis, the Condorcet loser**, on a five-mile technicality.

This is not an error in the article; both clauses are stated. It is a property of coarse grading: with only
four grades, one band boundary decides the election, and the tiebreak then reads only *how many* voters sit
above the median, not how far above. It also connects directly to Baujard et al.'s empirical finding in
[score-voting](score-voting.md) that voters grade differently depending on the scale offered. **Under MJ,
scale design is not presentation — it is part of the method.**

## 2. The highest-median rule misses the median voter

This is Laslier's critique, and it is the strongest thing in the article. 650 voters spread across a
left–right axis, each group running a candidate, seven grades, and each voter's grade drops one step per
unit of political distance:

| Group | Far-left | Left | Cen-left | Center | Cen-right | Right | Far-right |
|---|---|---|---|---|---|---|---|
| Voters | 101 | 101 | 101 | **50** | 99 | 99 | 99 |

Medians: Far-left and Far-right land on *mediocre*; **five candidates tie on *good*.** The tiebreak:

| Candidate | median | above (p) | verdict |
|---|---|---|---|
| **Left** | good | **303** | good+ |
| Cen-left | good | 252 | good+ |
| Center | good | 250 | good+ |
| Cen-right | good | 248 | good+ |
| Right | good | — (303 below) | good− |

**Majority judgment elects Left.** Meanwhile the **Condorcet winner is Center**, and so is the **score/mean
winner** — both verified. The left wing totals 303 voters and the right 297, and MJ hands the election to
the larger, more homogeneous wing rather than to the middle.

So the highest-**median**-grade rule fails the **median voter** criterion. That is not a pun for its own
sake — it is the actual finding, and the mechanism is the tiebreak: it counts *how many* voters are above
the median and ignores everything about how the rest are distributed. A candidate with a big solid bloc on
one side beats a candidate who is genuinely everyone's second choice.

The article notes that graduated majority judgment breaks this tie differently and would elect Center. I
did not verify that claim — my own continuous interpolation lands on Center-left, close to Center but not
identical, and Fabre's exact formulation is not given in the article. Treat the GMJ claim as the article's,
not as checked here. What *is* checked is that MJ elects Left and that the tiebreak is what does it.

## 3. What the median actually buys

The strategy-resistance claim is real, and one profile shows it cleanly. 61 voters, two candidates, a dead
heat on totals:

| Voters | A | B |
|---|---|---|
| 20 | 3 | 4 |
| 20 | 4 | 3 |
| 21 | 3 | 3 |

Totals: **A 203, B 203.** Medians: both 3.

Now let the first bloc min-max — A down to 0, B up to 5, the standard score-voting exaggeration:

- **Score totals swing to A 143, B 223** — an 80-point move from 20 voters out of 61.
- **Both medians stay exactly at 3.**

That is the whole argument for the median in one table. The exaggerating bloc bought itself an
eighty-point swing under score voting and *nothing at all* under majority judgment. Balinski and Laraki go
further and prove highest-median rules minimise the share of the electorate with an incentive to be
dishonest — though note that proof is by the method's inventors, the same caveat that applies to
[Equal Vote's material on STAR](star-voting.md).

The cost of that immunity is everything in the "fails" list above, and by the B&L theorem, the participation
failure specifically is not optional.

## 4. How different is it, really?

Over random three-candidate profiles (crude model — three blocs, uniform random grades — so read these as
"common enough to meet in practice", not as real-electorate rates):

| Comparison | Rate |
|---|---|
| MJ disagrees with plain score | **16.2%** of 110,083 profiles |
| MJ misses an existing Condorcet winner | **7.9%** of 107,266 profiles |

For calibration, the same harness in [score-voting](score-voting.md) put STAR and Ranked Robin at 3.1%
disagreement and STAR at 1.6% Condorcet misses. So **swapping the mean for the median is a much bigger
change than adding a runoff** — roughly five times the divergence, and MJ departs from the Condorcet winner
about five times as often as STAR does.

That cuts both ways, and the honest statement of it is:

- **For MJ**: departures from Condorcet are the *intended* behaviour, not a defect. The method's premise is
  that a shared absolute standard ("is this person Good?") is a better basis for a collective decision than
  aggregated pairwise preference. If you accept that premise, a 7.9% divergence is the method working.
- **Against**: the divergence is large, systematic, and — per Laslier — biased toward the largest
  homogeneous faction rather than toward consensus. That is close to the opposite of what a "consensus
  method" is usually sold as doing, and it is the specific charge the method has never really answered.

## How it sits against the rest of these notes

- **vs. [score voting](score-voting.md)** — same ballots, different statistic, and the trade is proved
  rather than empirical: score keeps participation and consistency, MJ keeps strategy resistance, and
  Balinski and Laraki's own theorem says you cannot have both.
- **vs. [STAR](star-voting.md)** — two different patches to the same problem. STAR keeps the mean and adds
  an ordinal runoff so exaggeration stops paying at the decisive step; MJ replaces the mean outright.
  Both lose participation to do it. STAR stays much closer to Condorcet (1.6% vs 7.9%).
- **vs. [approval](approval-voting.md)** — approval's answer to the same strategy problem is to remove the
  levels entirely. MJ's is to keep six levels and make them robust. Both claim to be the honest ballot.
- **vs. Condorcet methods ([Ranked Robin](ranked-robin-results-explained.md))** — MJ is the furthest from
  them of anything in these notes, and deliberately so: it denies that pairwise majority preference is the
  right primitive at all.
- **vs. Bucklin ([LeGrand](legrand-ranked-ballot-methods.md))** — reportedly the first highest-median rule.
  LeGrand's cumulative description and this article's median description are the same family.

## New ideas and terms

- **Highest median rule** — elect the candidate with the best median grade. MJ, graduated MJ, usual
  judgment and Bucklin are all instances.
- **Median grade (α), and α+ / α−** — MJ's comparison key: the median, then whether more voters sit above
  it (α+) or below (α−), then by how many. The whole tiebreak.
- **Grades as language** — the claim that "Excellent" has an absolute shared meaning a private numeric scale
  lacks, so ballots can be compared rather than merely summed. *Judge, don't vote.*
- **Point-summing method** — Σ f(score) for monotonic f; score voting and positional rules. By Balinski and
  Laraki's theorem, the *only* methods that can satisfy consistency, and the only ones satisfying
  participation plus continuity.
- **Join-consistency** — if a candidate wins two separate electorates they must win the merged one. The
  property whose only solutions are point-summing methods.
- **Rating consistency** — the criterion B&L define instead and MJ satisfies: two electorates that grade X
  *Excellent* and X *Acceptable* do not actually agree, so ordinary consistency asks the wrong question.
- **No-show paradox** — losing because you turned out. MJ's participation failure, and by the theorem above,
  unavoidable for any non-summing method.
- **Median voter criterion** — the winner should be the candidate closest to the median voter. MJ, the
  highest-*median*-grade rule, fails it.
- **Trimmed mean** — drop the extremes, average the rest. Olympic figure skating's hybrid; the practical
  compromise between mean and median.

## Links referenced in the article

- [Balinski & Laraki, "A theory of measuring, electing and ranking", *PNAS* 104(21) (2007)](https://www.pnas.org/content/pnas/104/21/8720.full.pdf)
- Balinski & Laraki, *Majority Judgment: Measuring, Ranking, and Electing*, MIT Press (2010) — the
  point-summing theorem is chapter 1, pp. 295–301
- [Balinski & Laraki, "Judge, don't Vote" (2010)](https://sites.google.com/site/ridalaraki/xfiles) — the
  rating-consistency argument
- [Laslier, "On choosing the alternative with the best median evaluation" (2010)](https://halshs.archives-ouvertes.fr/hal-00397403/document)
  and ["The strange 'Majority Judgment'" (2018)](https://halshs.archives-ouvertes.fr/hal-01965227) — the
  median-voter critique worked above
- [Felsenthal & Machover, "The Majority Judgement voting procedure: a critical evaluation" (2008)](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.324.1143&rep=rep1&type=pdf)
  — the no-show paradox
- [Fabre, "Tie-breaking the Highest Median: Alternatives to the Majority Judgment", *Social Choice and Welfare* 56 (2020)](https://github.com/bixiou/highest_median/raw/master/Tie-breaking%20Highest%20Median%20-%20Fabre%202019.pdf)
- [Varloot & Laraki, "Level-strategyproof Belief Aggregation Mechanisms" (2022)](https://doi.org/10.1145/3490486.3538309)
  — majority judgment with uncertainty
- [de Swart, "How to Choose a President, Mayor, Chair: Balinski and Laraki Unpacked" (2021)](https://doi.org/10.1007/s00283-021-10124-3)
- Galton, "One vote, one value", *Nature* 75, 28 Feb 1907, p. 414
- [Highest median voting rules](https://en.wikipedia.org/wiki/Highest_median_voting_rules) ·
  [Usual judgment](https://en.wikipedia.org/wiki/Usual_judgment) ·
  [Graduated majority judgment](https://en.wikipedia.org/wiki/Graduated_majority_judgment)

## Related local material

- [`code/majority-judgment/verify.py`](code/majority-judgment/verify.py) — every claim above, checked
- [score-voting](score-voting.md) — the mean, and the sum/average question MJ answers with the median
- [star-voting](star-voting.md) — the other patch to score voting's strategy problem
- [approval-voting](approval-voting.md) — the no-levels-at-all answer
- [legrand-ranked-ballot-methods](legrand-ranked-ballot-methods.md) — Bucklin, the ancestor
- [whoops.md](whoops.md) — where the load-bearing-clause and median-voter findings are indexed
