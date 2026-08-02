# Score Voting (Range Voting)

Source: [Score voting (Wikipedia)](https://en.wikipedia.org/wiki/Score_voting) — read 2026-08-01

Every number below is checked by [`code/score-voting/verify.py`](code/score-voting/verify.py) (no
dependencies, `python3 verify.py`).

## What it's about

Score every candidate on a fixed scale — 0–5, 0–9, 0–10, whatever — and the highest total wins. It is the
general case of which [approval](approval-voting.md) is the two-level special case and [STAR](star-voting.md)
is a two-round elaboration. Both of those notes lean on score voting as their baseline without ever working
it out; this fills that in.

The headline, and the reason the other two methods exist:

> **Honest score voting is one of the best methods there is. Strategic score voting is plurality.**

On the article's own Tennessee example, honest scores elect Nashville — the Condorcet winner, 603 to 457.
Take the *same voters with the same preferences* and have each of them min-max (10 for everyone above their
own average, 0 for the rest, the standard zero-information approval strategy) and the electorate elects
**Memphis, 42 to 41 — the Condorcet loser**, the same candidate first-past-the-post gives you. Nothing
changed but the strategy. Both results verified.

That single fact is the whole argument. Approval says: since strategic score collapses to approval anyway,
skip the pretence and use two levels. STAR says: keep the levels and add a runoff so exaggeration stops
paying. Everything else is detail.

## A caveat about the source

Thinner than the approval article and flagged **"lead too short" (August 2024)**. The Properties section —
the substantive claims about IIA, participation and monotonicity — carries **no citations at all**. Several
paragraphs in the Usage section are about *approval* (Brams on 19th-century England, Fargo's 2018 adoption),
padding a score article with its sibling's record.

And there is a real definitional problem in the first sentence, worked out in section 3 below.

## Key takeaways

### Mechanics and the sum/average ambiguity

- **Ballot**: a number per candidate on a fixed scale. Wikipedia's illustration uses 0–9; the Green Party of
  Utah uses 0–9; Pirate Party Bavaria uses 0–10; STAR uses 0–5; approval is 0–1.
- **The lead says the highest *average* score wins. The worked example computes *totals*.** These are the
  same rule only when every voter rates every candidate — which is exactly what the example does, so the
  article's own example cannot expose its own ambiguity. See below; this is not pedantry, it changes winners.
- **Empirically, scale design matters**: Baujard et al. found voters grade differently depending on the
  scale's length and whether negative grades are allowed. The scale is not a neutral container.

### Where it has been used

| Where | When | Notes |
|---|---|---|
| Sparta | ancient | Shout volume, measured by ear. The clapometer is the direct descendant |
| Republic of Venice (Doge) | 13th–18th c. | Multi-stage, multiple rounds of scoring |
| Greek legislative elections | 1864–1923 | Replaced by party-list PR |
| Swedish elections | early 20th c. | Proportional score; replaced by party-list PR |
| UN Secretary-General | current | Three-point: Encourage / Discourage / No Opinion, P5 veto |
| Latvian Saeima | current | Inside open-list PR |
| Green Party of Utah | current | Officers, 0–9 |
| Pirate Party Germany | current | Score, **reweighted range**, score-with-quorum, majority-grade |
| Wikipedia ArbCom | current | Three-point: Support / Neutral / Oppose |
| **Academy Award for Best Visual Effects** | current | Five nominees by **reweighted range voting** on 0–10 |

- **Non-political score voting is everywhere** and nobody calls it voting: Likert satisfaction surveys, IMDb
  and Amazon star ratings, app-store ratings, judged sports. The article's quiet point is that the ballot
  design is already familiar to everyone — which is a genuine adoption argument approval and STAR also
  borrow.
- **Albert Heckscher, 1892** — earliest known proponent, in a Danish dissertation. His "immanent method"
  scored alternatives from −1 to +1, modelling a voter's internal deliberation. That is 79 years before
  Weber named approval voting and 122 before STAR.

  **A cross-article inconsistency worth knowing**: Venice, Greece 1864–1923, Sweden, the UN, and Latvia are
  claimed by *both* the score article and the [approval](approval-voting.md) article, as examples of their
  respective methods, sometimes citing the same page of the same source (Mavrogordatos 351–352 for Greece).
  They can't both be right about what those elections were. Treat any "X used our method" claim on either
  page as a claim about a *family* of rated methods, not a specific one.

### Criteria

**Passes**: monotonicity, participation, and — the interesting one — **independence of irrelevant
alternatives**, with the caveat in section 4.

**Fails**: majority, Condorcet.

Score is the only method in these notes that passes IIA, and the reason is structural: a candidate's total
depends only on the scores given *to that candidate*. Nothing another candidate does can change it. That is
also why score has no spoiler effect in the usual sense, and why it is summable.

The catch is that it holds only if voters score on an **absolute** scale — some fixed internal standard of
what a 7 means — rather than normalising to the field in front of them. Real voters normalise. Section 4
shows exactly what that costs.

## 1. Tennessee, and every cell checked

Memphis 42%, Nashville 26%, Chattanooga 15%, Knoxville 17%. Scores 0–10, "proportional to relative
distance" from the mileage table the article hides in an HTML comment:

| Candidate | Memphis (42) | Nashville (26) | Chattanooga (15) | Knoxville (17) | Total |
|---|---|---|---|---|---|
| Memphis | 10 | 0 | 0 | 0 | **420** |
| Nashville | 4 | 10 | 6 | 5 | **603** |
| Chattanooga | 2 | 4 | 10 | 7 | **457** |
| Knoxville | 0 | 2 | 6 | 10 | **312** |

**All sixteen cells reproduce exactly** from the stated rule with round-half-up. Nashville wins, and
Nashville is also the Condorcet winner. (For contrast: FPTP elects Memphis, IRV elects Knoxville.)

## 2. This resolves the STAR table discrepancy — it was double rounding

Last time I checked the [STAR article's](star-voting.md) 0–5 version of this table, one cell didn't follow
the stated rule: Knoxville voters' Nashville score is printed as **2**, while deriving it from the distances
gives 2.689 → **3**. Having the 0–10 table explains it.

**The STAR table is this table halved, with round-half-to-even** — Python's `round()`. All sixteen cells
match under that rule, including the two that would otherwise look arbitrary:

| | 0–10 | halved | rounded | STAR prints |
|---|---|---|---|---|
| Knoxville → Nashville | 5 | 2.5 | **2** (half to even) | 2 |
| Knoxville → Chattanooga | 7 | 3.5 | **4** (half to even) | 4 |

So the chain is `5.378 → 5 → 2.5 → 2`, where going straight from the distances to a 0–5 scale gives
`2.689 → 3`. **Not a typo — a double-rounding artifact**, and the only cell where the two routes straddle a
boundary differently. That is a more accurate account than "the article has an error," and a more useful
one: the lesson is *don't rescale a rounded table, rescale the source*. Anyone generating fixture data for a
tabulator will hit this exact bug.

The STAR note has been corrected to say this.

## 3. The rule the article never settles: sum, average, or average with a quorum

The lead says highest **average** wins. The example computes **totals**. The Center for Election Science
source, cited for that very sentence, spells out that implementations differ: some score a skipped candidate
0, others don't count that ballot for them at all — and the latter kind need **quotas**, a minimum share of
voters who must rate you before you're eligible at all.

Three rules, and they are not equivalent as soon as any ballot has a blank. 100 voters, two real candidates:

| Voters | A | B |
|---|---|---|
| 60 | 10 | *blank* |
| 40 | 0 | 9 |

- **Total, blank = 0**: A 600, B 360 → **A wins**.
- **Average over those who rated you**: A 6.0, B 9.0 → **B wins**.
- **Average with a 50% quorum**: B was rated by 40 voters, fails the quorum, disqualified → **A wins**.

Same ballots, two different winners, and the difference is entirely in what a blank means. This is not
hypothetical: **Pirate Party Bavaria's rule for its 2025 Bundestag list is average-with-quorum** — ranking
by mean, minimum mean of 5 to make the list at all. And it is precisely the kind of thing that has to be
decided in a tabulator, where "unrated" and "rated zero" are different states in the data and identical on
paper.

Under averaging, note the incentive that appears from nowhere: **a candidate benefits from being rated by
fewer, more enthusiastic voters** — which is an argument for obscurity, and exactly what a quorum is
patching.

## 4. IIA: real, and conditional on voters not normalising

Score's IIA is genuine. 100 voters:

| Voters | A | B | C |
|---|---|---|---|
| 55 | 10 | 7 | 0 |
| 45 | 0 | 10 | 8 |

Totals A 550, B 835, C 360 → **B wins**. Delete C, a loser: A 550, B 835 — untouched, **B still wins**. No
ranked method can promise that (Arrow), and it is score's strongest formal claim.

Now let the voters **normalise** — favourite to 10, least favourite to 0, which is what people actually do
with a rating scale. With C present nothing changes. Remove C and the first bloc rescales: A was 10 and B
was 7, but B is now their *worst* remaining option, so B goes to 0.

Totals become A 550, B 450 → **A wins**. Removing a losing candidate flipped the result.

So score's IIA is a property of *absolute* scoring, exactly as approval's IIA is a property of a *fixed*
cutoff ([approval-voting](approval-voting.md), section 2). Same conditional, same failure mode, and the same
underlying question Ogren raises about core support in
[rcv-and-core-support](rcv-and-core-support.md): a standard that recalibrates to the field isn't a standard.

**Majority and Condorcet fail** outright, minimally:

| Voters | A | B |
|---|---|---|
| 51 | 10 | 9 |
| 49 | 0 | 10 |

B wins 949–510 although A is the strict favourite of 51 of 100 and beats B head-to-head 51–49. A's own
supporters defeated A by honestly recording that B was nearly as good — score's later-no-harm failure in two
rows.

## 5. What STAR's runoff costs: participation

Score satisfies participation and monotonicity — no violation of either in 56,979 clean random profiles.
STAR **loses** participation, and the runoff is why:

| Voters | A | B | C |
|---|---|---|---|
| 44 | 2 | 3 | 2 |
| 20 | 4 | 1 | 5 |
| **11** | **1** | **3** | **5** |

Without the last 11 voters: totals A 168, B 152, C 188 → finalists C and A → **C wins**.
With them: A 179, B 185, C 243 → finalists C and **B** → **B wins 44–31**.

Those 11 score C at 5 and B at 3. **By turning out, they replaced their favourite with their second
choice.** Staying home would have served them better. Their C=5 was not the problem — their B=3 was, lifting
B past A into the runoff, where B beat C.

This is worth being explicit about, because the usual framing is that STAR strictly improves on score. It
doesn't. The runoff buys resistance to exaggeration and pays for it in participation, later-no-harm,
Condorcet and clone independence — all of which plain score either satisfies or fails less badly. It is a
trade, not an upgrade.

## 6. Equal Vote's two methods disagree — how often, and which way

Equal Vote promotes both STAR (2014, cardinal) and Ranked Robin (2021, Condorcet). Run both on the same
ballots and they are not interchangeable.

On the clone profile from the [STAR note](star-voting.md) — 48 voters scoring `A1 5, A2 5, B 0`, 52 scoring
`A1 2, A2 1, B 3` — **STAR elects A1 and Ranked Robin elects B**, and B is the Condorcet winner and the
strict favourite of an absolute majority.

Across 58,952 random three-candidate profiles they **disagree 3.1% of the time**, and STAR fails to elect an
existing Condorcet winner in **1.6%** of profiles where one exists.

Two honest readings, and both belong here:

- **For STAR**: 3.1% is small. They agree 97% of the time, the disagreements need intensity gaps wide enough
  to override a pairwise majority, and STAR's defenders say that override is the *point* — Brams' argument
  for approval in exactly the same words. If you think a mild majority preference should lose to an intense
  minority one, this is a feature and the number is reassuringly small.
- **Against**: the disagreement is not random noise, it is **systematically** the Condorcet winner losing,
  and Equal Vote's own other method is built to guarantee that never happens. An organisation shipping both
  is shipping two different answers to "should a pairwise majority be able to lose?" — and the choice
  between them is a values choice their materials present as a menu of implementation options.

One caveat on those percentages: this is a crude model — three random blocs, uniform random scores — not a
spatial one. It shows the disagreement is common enough to hit in practice, not how often it would happen in
a real electorate. The spatial VSE work in [ranked-robin-vse-run](ranked-robin-vse-run.md) is the right tool
for that, and running STAR through the same votesim harness is the obvious next job.

## New ideas and terms

- **Score / range voting** — score everyone on a fixed scale, highest total wins. Approval is the two-level
  case; STAR adds a runoff.
- **Sum vs. average vs. average-with-quorum** — three different methods sharing one name. They diverge the
  moment a ballot has a blank, and the choice is invisible on paper but explicit in a tabulator.
- **Quorum / quota (score)** — a minimum share of voters who must rate a candidate before they can win.
  Exists to patch averaging's reward for being rated by few enthusiasts.
- **Blank vs. zero** — an unrated candidate and a candidate rated 0 are the same mark under summing and
  different states under averaging. The single most implementation-relevant distinction here.
- **Absolute vs. normalised scoring** — do you score against a fixed internal standard, or rescale so your
  favourite gets the max and your worst the min? IIA survives the first and dies on the second.
- **Reweighted range voting (Thiele's method)** — the proportional multi-winner variant; used by the
  Academy for Best Visual Effects nominees and by Pirate Party Germany.
- **Immanent method (Heckscher, 1892)** — scores on [−1, +1] as a model of individual deliberation. The
  earliest known score-voting proposal.
- **Moral bias in large elections** (Feddersen, Gailmard & Sandroni 2009) — experimentally, as the
  probability of being pivotal falls, voters behave *less* strategically. If it holds, the strategic
  collapse to approval is weakest exactly where elections are largest — a real empirical counterweight to
  the theory, and the best news score voting gets in this article.
- **Clapometer lineage** — Sparta measured shouting; talent shows still do. Score voting's ballot is the one
  form of voting people already use daily without noticing.

## Links referenced in the article

- [The Center for Range Voting](https://rangevoting.org/) · [The Center for Election Science](https://electionscience.org/)
  · [Equal Vote Coalition](https://www.equal.vote/)
- [Nunez & Laslier, "Preference intensity representation: strategic overstating in large elections" (2014)](https://hal.archives-ouvertes.fr/hal-00917099/file/overstateREVIEW20120928.pdf)
  — the "strategic score = approval" result, and where it doesn't hold
- [Laslier, "Strategic approval voting in a large electorate" (2006)](http://halshs.archives-ouvertes.fr/docs/00/12/17/51/PDF/stratapproval4.pdf)
  — strategic play elects the Condorcet winner
- [Feddersen, Gailmard & Sandroni, "Moral Bias in Large Elections" (2009)](https://www.jstor.org/stable/27798496)
- [Baujard et al., "How voters use grade scales in evaluative voting"](https://halshs.archives-ouvertes.fr/halshs-01618039/file/1729.pdf)
- [Baujard et al., "Who's favored by evaluative voting?" (2012 French election)](https://halshs.archives-ouvertes.fr/halshs-01090234/file/1430.pdf)
- [Lagerspetz, "Albert Heckscher on collective decision-making" (2014)](https://doi.org/10.1007/s11127-014-0169-z)
- [Mowbray & Gollmann, "Electing the Doge of Venice" (2007)](http://www.hpl.hp.com/techreports/2007/HPL-2007-28R1.pdf)
- [89th Academy Awards rules (PDF)](https://www.oscars.org/sites/oscars/files/89aa_rules.pdf#page=32) — Rule
  22, reweighted range voting for the Visual Effects nominees
- [Majority judgment](https://en.wikipedia.org/wiki/Majority_judgment) — the median-based alternative to
  averaging, written up in [majority-judgment](majority-judgment.md)

## Related local material

- [`code/score-voting/verify.py`](code/score-voting/verify.py) — every claim above, checked
- [approval-voting](approval-voting.md) — the two-level case; same IIA caveat, arrived at from the cutoff side
- [star-voting](star-voting.md) — score plus a runoff, and what that trade costs
- [majority-judgment](majority-judgment.md) — the median instead of the mean: the other answer to
  section 3's question, and the theorem saying you can't have both it and participation
- [ranked-robin-vse-run](ranked-robin-vse-run.md) — the spatial-model harness that could put a real number on
  section 6
- [rcv-and-core-support](rcv-and-core-support.md) — Ogren's cardinal argument, and the standards-that-
  recalibrate problem in its original form
- `Voting 2021 mbair/` — the local STAR tabulator, where blank-vs-zero is a code path
