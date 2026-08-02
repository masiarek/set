# Approval Voting

Source: [Approval voting (Wikipedia)](https://en.wikipedia.org/wiki/Approval_voting) — read 2026-08-01

## What it's about

Approve as many candidates as you like; most approvals wins. It is the simplest cardinal method — a score
ballot restricted to {0, 1} — and the only one on that list whose ballot is still a plurality ballot with the
"vote for one" instruction removed. That is its whole pitch: kill vote-splitting without changing the ballot
paper, the tabulator, or the summability of the count (one integer per candidate, addable precinct by
precinct). Because the number of approvals is unlimited, an overvote is impossible by construction.

This is the method LeGrand says he prefers to all sixteen ranked methods on his own site
([legrand-ranked-ballot-methods](legrand-ranked-ballot-methods.md)), so it is worth knowing what it actually
does.

## Key takeaways

### Mechanics and lineage

- **Robert J. Weber coined the name in 1971**; Steven Brams (political scientist) and Peter Fishburn
  (mathematician) published the full treatment in *American Political Science Review* in 1978. The 1983
  Brams–Fishburn book *Approval Voting* is the standard reference and the source of most strategy results
  below.
- **Multiwinner is trivial but crude**: for ten seats, take the ten highest approval totals. That is
  block approval, not proportional — [Sequential Proportional Approval Voting](https://en.wikipedia.org/wiki/Sequential_proportional_approval_voting)
  (Sweden, early 20th c.) is the proportional variant.
- **Score voting is approval with more levels** (0–5 instead of 0–1); combined approval voting uses three
  (−1, 0, +1); the D21 – Janeček method caps you at two approvals plus one negative vote.

### Where it has actually been used

| Where | When | Notes |
|---|---|---|
| Papal conclaves | 1294–1621 | ~40 cardinals, repeated rounds until someone appears on ⅔ of ballots |
| Republic of Venice (Doge) | 13th–18th c. | Multi-stage, mixed with sortition |
| Greek legislative elections | 1864–1923 | Secret marble-drop boxes, one per candidate; replaced by party-list PR |
| Swedish elections | early 20th c. | Sequential *proportional* approval; replaced by party-list PR |
| UN Secretary-General straw polls | current | Approve / disapprove / no opinion; P5 disapproval acts as a veto |
| Latvian Saeima | current | Inside open-list PR: positive, negative, or no vote on any number of candidates |
| Fargo, ND | 2018–2025 | First US jurisdiction; see below |
| St. Louis, MO | 2020– | Proposition D passed with 70%; approval used as a "unified primary" (top two advance) |

Sourced from Wikipedia. A longer and looser list of claimed precedents — Sparta, the pre-12th-Amendment US,
the USSR, China's National People's Congress — is CRV's, and is adjudicated in the CRV section below; the
headline one does not survive.

- **Fargo** adopted approval by ballot initiative in 2018, after a 2015 commissioner race split six ways and
  was won on a **22% plurality**. First election 9 June 2020: two commissioners from seven candidates, both
  winners over 50% approval, **2.3 approvals per ballot**, 62% of polled voters happy with the change. June
  2022: mayor re-elected from seven candidates at ~65% approval with **1.6 approvals per ballot**; the
  commission race (two seats, fifteen candidates) drew **3.1 approvals per ballot**.
- **Fargo is over.** A 2023 ban was vetoed by Governor Doug Burgum on home-rule grounds and the override
  failed; in **April 2025 Governor Kelly Armstrong signed a bill banning both RCV and approval statewide**,
  ending it in Fargo.
- **St. Louis 2021 mayoral primary**: Tishaura Jones 57% and Cara Spencer 46% advanced; Lewis Reed 39% and
  Andrew Jones 14% were eliminated. Four candidates, **1.6 approvals per ballot** — note the totals sum to
  156%, which is what an approval result looks like.
- **Organizations**: MAA (1986), IEEE and INFORMS' predecessor and ASA (all 1987), Society for Social Choice
  and Welfare (1992), American Mathematical Society. Parties: American Solidarity, Greens of TX and OH,
  Libertarian National Committee and LP-TX/CO/AZ/NY, Alliance 90/The Greens (Munich), Czech and German
  Pirates.
- **Two documented retreats, which are the interesting part.** IEEE dropped it in 2002 — the executive
  director's stated reason was that "few of our members were using it," and CRV puts a number on the same
  reason: **"the large percentage (80%) of IEEE members who voted plurality-style"**
  ([rangeVapp](https://rangevoting.org/rangeVapp.html), filed there under "A failure of approval voting in the
  real world"). Dartmouth's alumni association
  replaced it with runoffs by an 82–18 vote in 2009; Dartmouth students used it for student-body president
  from 2011 and abandoned it before 2017, after winners kept landing under 40% (41% in 2011, 32% in 2012) and
  *The Dartmouth* reported **over 80% of voters approving exactly one candidate** in 2014 and 2016. The
  Independent Party of Oregon used it for nominations 2011–2016, then switched to STAR in 2020 after its 2016
  presidential preference vote produced no nominee — nobody cleared 32%.

  Universal bullet voting collapses approval into plurality. That is the practical failure mode, and it has
  happened repeatedly in low-stakes, low-information elections.

### Strategy: the defining problem

- **There is no unique sincere vote.** Wikipedia's (Brams–Fishburn) definition: a vote is sincere if,
  whenever it approves someone, it also approves everyone strictly preferred to them. With strict preferences
  A > B > C > D that leaves five sincere votes — {}, {A}, {A,B}, {A,B,C}, {A,B,C,D} — and if B and C are tied
  in the voter's esteem, {A,C} is sincere too. Every other method has one honest ballot; approval makes you
  choose an **approval cutoff**, and that choice is inescapably strategic even when your preferences are
  honest.
- **Consequence**: with fixed voter preferences, approval can sincerely elect *any* candidate, including both
  the Condorcet winner and the Condorcet loser. Saari and Van Newenhizen call this indeterminacy and treat it
  as a defect that is "robust, not isolated"; they also wrote the rebuttal arguing it is really
  responsiveness to cardinal utility rather than a bug. Brams' position is blunter: voters' pragmatic
  judgments about who is *acceptable* should outrank the Condorcet criterion.
  A compact worked instance on a real ranked profile is in
  [lumen-75-ballot-four-winners](lumen-75-ballot-four-winners.md): 75 ballots, and top-1 / top-2 / top-3 cutoffs
  elect the plurality winner, the Borda winner, and (tied) the Condorcet winner — three answers, all sincere.
- **Bullet voting / the chicken (Burr) dilemma** — approve only your favorite so you don't help your
  second choice beat them. If both frontrunners' camps do it, a weaker third candidate wins. The Fargo 2020
  poll run *by opponents* of approval found **30% of bullet voters did so strategically, 57% sincerely** —
  which cuts both ways as evidence.
  - **The best rebuttal is CRV's, and it is a real argument**
    ([BurrSummary](https://www.rangevoting.org/BurrSummary.html)): the dilemma assumes *asymmetric* strategic
    sophistication. If A and B voters are canny enough to withhold approval from each other, C's voters are
    canny enough not to bullet-vote a candidate who can't win — they would approve C plus their preferred of
    {A, B}, and the split stops mattering. "It is unsymmetrical/illogical to presume only the {A,B}-supporters
    would strategically exaggerate but not the C-supporters… If the problem is genuine it is because of
    unsymmetrical/illogical human psychology, not logical strategy." Nagel's answer is that the asymmetry is
    supplied by the two allies' infighting — a "retaliatory spiral" between A and B that C's camp has no
    equivalent of.
  - **The rebuttal's second leg is weaker than the first**, and is worth naming because it recurs: "the problem
    is lessened with better pre-election polling — if the voters knew C was likely to win, then A and B would
    not be the two frontrunners." That is the AppCW hypothesis again (see the CRV section), i.e. *assume the
    poll is right*, which is the one thing approval ballots cannot supply.
  - **One candidate real-world instance, and it is a counterfactual.** CRV's own answer to "where has this
    happened" is "the only fairly-clear example known to me": **Portugal 1986**. First round — Freitas do
    Amaral (right) 46.3%, then Soares 25.4%, Zenha 20.9%, Pintasilgo 7.4%, the left split three ways; runoff —
    **Soares beat Freitas do Amaral 51.18% to 48.82%** (verified 2026-08-01; CRV rounds it 51.3–48.7). A left
    majority, a right plurality leader, and two near-tied allies: under approval with both left camps bullet
    voting, Freitas do Amaral wins. Approval was not used, so this is a reconstruction, not a case.
- **Compromising** — approving someone you find unacceptable to stop someone worse. Approval's honest-favorite
  version of lesser-evil voting; it never requires you to *demote* your favorite.
- **What approval is immune to**: burying and push-over. You cannot reverse two candidates' order on an
  approval ballot — only move the cutoff — so the ranked-method reversal strategies have no expression.
- **Myerson–Weber rational voter model**: approve every candidate with a positive *prospective rating*
  (utility weighted by pivot probabilities). Approving your favorite and rejecting your least favorite are
  **dominant strategies**. Useful special cases:
  - all pairwise ties equally likely ("zero info") → approve everyone with **above-average utility**;
  - a clear expected winner and runner-up (**Laslier's leader rule**) → approve everyone you prefer to the
    expected leader, plus the leader if you prefer them to the runner-up. *If everyone plays this, the
    equilibrium elects the Condorcet winner when one exists.* Same result under trembling-hand ballots.
  - With four or more candidates an optimal vote can require skipping a more-preferred candidate while
    approving a less-preferred one — but only in inherently unstable configurations.
- **Dichotomous preferences are the magic case.** If a voter genuinely sorts candidates into acceptable /
  unacceptable with no ranking inside either group, approval is **strategyproof** — one uniquely best ballot
  regardless of everyone else — and if all voters are like that, approval **always elects the Condorcet
  winner**. Brams–Fishburn's own caveat: with more than a handful of voters and three-plus candidates, this
  is not a realistic assumption.
- **…and on that domain approval is the only rule, not merely a good one.** The Wikipedia article stops at
  the compliance claim, which makes the dichotomous row read like an assumption chosen to flatter approval.
  [Brandl & Peters (2022)](https://www.dominik-peters.de/publications/av.pdf) is the stronger result:
  restricted to dichotomous preferences, approval voting is **uniquely characterized** — eight separate
  characterizations (their Theorems 2–9), every one built on **consistency with variable electorates** (if
  two disjoint electorates both choose some alternatives in common, the merged electorate chooses exactly
  the ones they agree on) plus one headline axiom: strategyproofness, choosing Condorcet winners, avoiding
  Condorcet losers, respecting unanimous majorities, independence of clones, independence of losers,
  independence of dominated alternatives, or independence of never-approved alternatives. All eight reduce
  to one base theorem (Theorem 1: consistency + faithfulness + disjoint equality).
  - **The headline axiom is never sufficient by itself.** Each theorem also carries housekeeping axioms —
    anonymity, neutrality, faithfulness, continuity, non-triviality — and *which* ones differs per theorem.
    Their Table 1 is the map, with a numbered counterexample against each axiom proving it can't be dropped.
    "Consistency plus strategyproofness forces approval" is not what the paper says; Theorem 2 also needs
    anonymity, neutrality and non-triviality.
  - What this does *not* do is rescue the row for real electorates. It relocates the argument: the question
    stops being "is approval good on this domain" (settled, and settled in approval's favor) and becomes
    "how far from dichotomous are actual voters," which is the empirical question the rest of this note is
    about — cutoffs, the Tennessee example, and the 2002/2012 French field experiments.

### Criterion compliance depends on the voter model, not the method

This is the unusual bit — the compliance table has one row per *model of how voters set their cutoff*, not a
single verdict.

The sharpest statement of why is Horn's, and it is worth having before the table. Approval's instructions can
be written two ways: **Rule (1)** — "vote for all and only those candidates you minimally approve of" — or
**Rule (2)** — "vote by making a mark next to as many candidate names as you like." Same tabulation; only the
first constrains what a mark *means*. Bullet voting your favorite violates (1) and complies perfectly with
(2). So the rows below are not four theories about voter psychology so much as four answers to *which rule is
actually in force*, and the last row is what Rule (1) gets you: an approval set that is an attitude, fixed
before the field is known. **Assuming Rule (1) compliance is the dichotomous row, imposed procedurally rather
than assumed of the voters.** That reframing is genuinely useful — and the note that makes it also shows what
it costs, since every criterion it then proves is a property of the assumption rather than of the count.
[→ [horn-three-virtues-approval](horn-three-virtues-approval.md)]

| Voter model | Majority | Monotone + Participation | Condorcet + Smith | IIA | Clone indep. | Reversal sym. | Sincere favorite | Strategyproof |
|---|---|---|---|---|---|---|---|---|
| Zero information | ✗ | ✓ | ✗ | ✗ | ✗ | ✓ | ✓ | ✗ |
| Leader rule | ✓ | ✓ | ✓ | ✗ | — | — | ✓ | ✗ |
| Trembling ballots | ✓ | ✓ | ✓ | ✗ | — | — | ✓ | ✗ |
| Binary (dichotomous) preferences † | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

(Wikipedia flags this table as incomplete; the blanks are blank there. ✗ on IIA for the three realistic rows
is the honest headline.)

† The all-✓ row understates the case, and one ✓ here is not the coincidence it looks like. Under dichotomous
preferences the majority relation is **transitive** (Inada 1969) and orders candidates exactly by approval
score — so Condorcet cycles cannot arise at all, and the Condorcet ✓ is structural rather than lucky.
Beyond passing, [Brandl & Peters (2022)](https://www.dominik-peters.de/publications/av.pdf) show approval is
the **only** rule passing several of these: strategyproofness, Condorcet, clone independence and reversal
symmetry each appear as the headline axiom of a characterization theorem (each also needing housekeeping
axioms — see the bullet above; consistency alone plus one criterion does not do it). So parts of this row are
uniqueness results, not compliance results. The row's weakness is its premise, not its checkmarks.

- **Sincere favorite is satisfied in every row** — approval never punishes you for approving your favorite.
  That is its strongest formal claim and the direct answer to
  [favorite betrayal](glossary.md) under Hare/IRV.
- **Monotonicity holds unconditionally** (more approvals never hurt), and approval **fails later-no-harm**
  (approving a second candidate can beat your first). Brams' framing: those two facts are the same fact seen
  from opposite sides, and the tension between them is exactly what the cutoff decision resolves.

## Worked example 1 — Tennessee capital, five strategy scenarios

Same electorate as the standard Condorcet example. Nashville is the Condorcet winner, Memphis the Condorcet
loser. Wikipedia's von Neumann–Morgenstern utilities (0–100), with the average I need for the zero-info rule:

| Faction (share) | Memphis | Nashville | Chattanooga | Knoxville | Average |
|---|---|---|---|---|---|
| Memphis (42%) | 100 | 15 | 10 | 0 | 31.25 |
| Nashville (26%) | 0 | 100 | 20 | 15 | 33.75 |
| Chattanooga (15%) | 0 | 15 | 100 | 35 | 37.5 |
| Knoxville (17%) | 0 | 15 | 40 | 100 | 38.75 |

**Zero-info** (approve above your own average) — worked through myself:

- Memphis voters: only 100 > 31.25 → {Memphis}
- Nashville voters: only 100 > 33.75 → {Nashville}
- Chattanooga voters: 100 > 37.5, but Knoxville's 35 falls just short → {Chattanooga}
- Knoxville voters: 100 and Chattanooga's 40 both clear 38.75 → {Chattanooga, Knoxville}

Totals: **Memphis 42, Nashville 26, Chattanooga 32, Knoxville 17.** Memphis — the Condorcet *loser* — wins,
on minority approval, with more voters disapproving than approving. Only one faction approved more than one
candidate.

All five scenarios from the article:

| Expectations | Memphis | Nashville | Chattanooga | Knoxville | Winner |
|---|---|---|---|---|---|
| Zero-info | 42 | 26 | 32 | 17 | Memphis (Condorcet loser) |
| Memphis leading Chattanooga | 42 | 58 | 58 | 58 | three-way tie |
| Chattanooga leading Knoxville | 42 | 68 | 83 | 17 | Chattanooga |
| Chattanooga leading Nashville | 42 | 68 | 32 | 17 | Nashville |
| Nashville leading Memphis | 42 | 58 | 32 | 32 | Nashville |

Only the last row is an equilibrium — the expected winner and runner-up match the actual ones — and there the
Condorcet winner takes it. The second row collapses into a three-way tie precisely because the expected
leader was the Condorcet loser and everyone who didn't rank Memphis first ranked it last.

**The lesson**: with preferences held fixed, approval's outcome is a function of what voters *believe about
the polls*. Polling error isn't noise around an approval result; it moves the result.

## Worked example 2 — dichotomous cutoff and IIA

The article's second example separates two cutoff rules that look similar and behave differently. Four
candidates, approval percentages per bloc, voters approving anything above **50%** (a fixed, dichotomous
cutoff) versus anything above **their own average** (a floating cutoff):

| Bloc | A | B | C | D | Their average |
|---|---|---|---|---|---|
| 25% | 90 | 60 | 40 | 10 | 50 |
| 35% | 10 | 90 | 60 | 40 | 50 |
| 30% | 40 | 10 | 90 | 60 | 50 |
| 10% | 60 | 40 | 10 | 90 | 50 |

Both rules coincide here: **C wins with 65%**, over B 60%, D 40%, A 35%.

Now drop a loser and recompute:

- **A drops out, floating (above-average) cutoff** → the averages all shift and **B wins with 60%**, C 55%.
  The winner changed because an irrelevant alternative left. IIA violated.
- **A drops out, fixed 50% cutoff** → nobody's ballot changes; **C still wins**.
- **D drops out, "approve your top 2"** → **B wins with 70%**, C and A on 65%. IIA violated again.
- **D drops out, fixed 50% cutoff** → **C still wins**.

So approval's IIA failure isn't in the tabulation — it's entirely in the cutoff rule. A voter with a genuinely
fixed standard of acceptability gives approval IIA for free; a voter who recalibrates against the field does
not. That is the same "your values shouldn't depend on who else is running" point Ogren makes about core
support in [rcv-and-core-support](rcv-and-core-support.md), arriving from the opposite direction.

This is also the whole of the published case that approval satisfies IIA. Horn's first "unique virtue" is the
fixed-cutoff column above, asserted as a rule (approve exactly those you approve of, whoever else is running)
rather than observed in voters — which makes it true by stipulation, and no more approval's property than
score voting's, since score satisfies IIA under absolute scoring for the identical reason. What that paper
adds is the concession: it distinguishes Arrow's actual Condition 3 from the popular add-or-remove reading
(**IIA2**) and from the contraction form (**IIA2†**, Sen's property α), and grants that approval fails IIA2†.
Its own footnote 14 then quotes Nagel pointing out that failing IIA2† reopens manipulation by *adding or
subtracting candidates* — the third and fourth rows of the table above, in one sentence, unanswered.

The stronger version of the demonstration below is in that note too. Take one 426-voter ranked profile,
enumerate all 32 combinations of **sincere** cutoffs — each bloc approving its top one or top two, every
ballot an upper set of its own ranking — and approval elects the Condorcet winner in 24, the Condorcet
**loser** in 5, and the option a 77% majority opposes in 3. No floating cutoff, no recalibration, no
strategy: just the fact that "sincere" doesn't pick out one ballot.
[→ [horn-three-virtues-approval](horn-three-virtues-approval.md)]

A corollary worth stating, because textbooks trip on it: **a ranked profile cannot determine an approval result.**
Ranked ballots carry no utilities, so the fixed cutoff — the well-behaved one — isn't computable from them; top-*k*
is the only cutoff a ranking can express, and top-*k* is floating. Any exercise that "runs approval voting" on a
preference schedule is therefore reporting its own stipulation, not the method's answer. Worked out against a
gen-ed textbook that does exactly this, and then advertises the result as a majority-criterion failure, in
[lumen-75-ballot-four-winners](lumen-75-ballot-four-winners.md).

## Empirical comparisons

- **2002 French presidential, first round.** Actual: Chirac 19.9%, Le Pen 16.9%, Jospin 16.2% — Jospin
  eliminated, and Le Pen then lost the runoff 82.2–17.8, which is about as clear a sign as exists that the
  wrong two advanced. Laslier and Van der Straeten's in-precinct approval experiment: **Chirac 36.7%, Jospin
  32.9%, Le Pen 25.1%** — Jospin advances, Le Pen doesn't. A textbook center-squeeze correction.
- **2012 French presidential** (Baujard et al., approval and score): unifying candidates gained, polarizing
  ones lost, relative to plurality.
- **Brams and Herschbach, ["The Science of Elections"](https://www.science.org/doi/10.1126/science.292.5521.1449),
  *Science* **292** (5521), p. 1449, 25 May **2001*** (verified 2026-08-01; electowiki dates it 2000 and is
  wrong — the DOI encodes vol. 292 / iss. 5521 / p. 1449, and vol. 292 runs Apr–Jun 2001): approval should raise
  turnout, defuse spoilers, and reduce
  negative campaigning — you're courting your opponents' approvals, not just your own base. **All three are
  predictions, and two are marked unevidenced by a friendly source.** Brams restates them as numbered points in
  his MIT alumni column, which CRV hosts with bracketed editor's notes: turnout is "probably true but…not
  supported by direct evidence," and reduced negative campaigning is "not supported by any evidence I know of.
  And indeed there is some evidence against it" — Nagel's Burr dilemma being the counter-mechanism. See the CRV
  section below.
- **1987 MAA presidential election, 5 candidates, 3,924 voters** (Brams' analysis): 79% approved exactly one,
  16% two, 5% three, 1% four. Winner had **1,267 approvals = 32%**. Even among mathematicians who chose the
  method, four out of five bullet voted.

## How the advocacy organizations present it

Eight pages read on 2026-08-01 — three CES, one FairVote, two RCVRC, one CRV, one electowiki. **Six of the eight
discuss no downside of the method their source exists to promote**, and the two exceptions each have a reason:
CRV promotes *range* voting, so approval is its second choice and conceding approval's limits is how it sells the
upgrade; electowiki is a wiki whose declared policy tells readers to go to Wikipedia for neutral information. The
two campaigning orgs fail in mirror-image ways: each states a property that holds only
under a favorable assumption as though it held unconditionally. CES: "no candidate can ever be a spoiler" (true
only under dichotomous preferences). FairVote: "RCV is a majority system" (true only of continuing ballots).
Everything needed to adjudicate them is already above, so this is mostly a lookup table.

The useful surprise is that no org is uniformly worse, and that **accuracy does not track balance**. CES's
flagship explainer is the weakest document here and its head-to-head page carries the worst single factual error,
yet CES's neutral explainer is the most accurate page either campaigner produced. FairVote's page is better
sourced than all three CES pages combined and is right about approval's real weakness — while being wrong about
its own method's central claim. And the most accurate pages of all belong to RCVRC, an organization that is
*less* balanced than FairVote by construction, because it is scoped to one method and says so.

Ranked by accuracy rather than balance: **RCVRC > CES "Differences" > FairVote > CRV > electowiki > CES
head-to-head > CES explainer.** CRV lands mid-table for a reason no other page manages: it repeats CES's false
spoiler claim *and* names approval's cutoff problem in the same document, and it is the only page here that makes
a checkable quantitative claim — so its errors are provable rather than arguable. electowiki is the hardest to
place and the ranking undersells it: it has the survey's best single section (indeterminacy, worked and
double-cited) sitting beside its worst sourcing (an unsourced claim that China's NPC uses approval voting, and a
whole section resting on a `[citation needed]`). **Depth and reliability came apart on one page.**

### CES — ["What is Approval Voting?"](https://electionscience.org/education/approval-voting) (Chris Raleigh, Jun 2024)

~300 words, seven bullets, no citations, no numbers, no acknowledged trade-off. (CES's `/library/…` URLs all
redirect to `/education/…`; canonical paths used throughout.)

| Claim | Verdict | Adjudicated by |
|---|---|---|
| "It eliminates vote-splitting … no candidate can ever be a *spoiler*" | **False as stated** | IIA is ✗ in three of the four rows of the compliance table, ✓ only under dichotomous preferences. Worked example 2 above *is* a spoiler: drop A under a floating cutoff and the winner moves C → B |
| "The candidate with the broadest support across the electorate wins" | **Conditional** | Zero-information Tennessee elects Memphis, the Condorcet *loser*, on 42 approvals with more voters disapproving than approving. Holds under the leader rule and trembling ballots, not in general |
| "Candidates dividing the electorate is not a viable strategy" | **False** | The Burr/chicken dilemma is exactly that strategy; Fargo candidates campaigned on "just vote once" |
| "It makes every voter more powerful" | **Unqualified** | Kimball's St. Louis finding — majority-White wards cast multiple approvals at higher rates — is unequal power, contingent on who understands the cutoff |
| "Voters can support candidates who may not be their first choice" | **True** | Sincere favorite passes in *every* row of the table. Approval's strongest formal claim |
| "It can run on our current machines" | **True** | Summability |

Bullet voting — the documented practical failure mode, and the best-evidenced thing on this page's subject
(Dartmouth 41% and 32% winners with >80% approving exactly one; MAA 79%) — goes unmentioned, as do the Burr
dilemma and cutoff indeterminacy. The library still shelves "Success Stories: Fargo Before and After Approval
Voting" although the April 2025 statewide ban ended approval voting in Fargo; the flagship success story is now a
repeal.

### CES — ["Why CES Advocates for Approval Voting Instead of RCV"](https://electionscience.org/education/approval-voting-vs-rcv) (Chris Raleigh, Jun 2024)

CES's actual answer to FairVote: seven self-chosen criteria, approval and RCV assessed under each. No citations
again, and the criteria are picked by the advocate — but three of the seven are **substantively correct and are
FairVote's genuine weak points**, which makes this the more serious document of the two CES pages.

**Where it lands:**

- **Summability and count transparency.** "Votes cannot be counted until all are received, leading to long
  delays… difficult to follow where a voter's vote actually landed." This is true and it is structural, not
  rhetorical: approval reports one integer per candidate per precinct, IRV requires full cast vote records
  centrally. Recount behaviour follows from the same fact. FairVote's page never engages it.
- **Machines and cost.** Broadly right, and the reason approval keeps clearing procurement hurdles RCV doesn't.
- **"First place selections are essentially the same as plurality votes, as they are mutually exclusive."**
  Sharp, and correct. It is the cleanest one-line statement of why IRV's round 1 inherits plurality's pathologies
  — the exact mechanism behind [center squeeze](hare-center-squeeze-examples.md).
- **"RCV does not inherently favor any group, despite what may be claimed."** An unforced concession against
  interest. Worth noticing; FairVote's page contains no equivalent.

**Where it repeats the overclaim:** "Vote splitting is eliminated in approval voting elections. The 'spoiler
effect' is negated." Same false flat statement as the explainer, same refutation — IIA ✗ in three of four rows.
And "voters have multiple, clear strategies to stop hyperpartisans by approving multiple candidates" is precisely
the situation the Burr dilemma describes, in which those strategies conflict.

**The Alaska claim is the substantive error.** CES writes: "In the 2022 Alaska congressional election, two
Republicans and a Democrat ran. Despite 60% of voters preferring a Republican, their votes split between the two
candidates. This fragmentation allowed the Democrat, initially with only 40% support, to win." Three problems:

1. **Wrong mechanism.** This was a center squeeze, not vote-splitting. Begich was the *Condorcet winner* — he beat
   both Peltola and Palin head-to-head — and IRV eliminated him first
   ([rcv-and-core-support](rcv-and-core-support.md)). Naming it "fragmentation" describes the plurality failure
   IRV is designed to address, and misses the failure IRV actually committed.
2. **Backwards causation.** Peltola led round 1 outright, so **plurality would have elected her too.** IRV did not
   *enable* the outcome; it failed to *prevent* it. As written the sentence implies the reverse.
3. **"60% preferring a Republican" conflates first preferences with preference.** 60% ranked a Republican first;
   enough Begich voters preferred Peltola to Palin that Peltola won the runoff — which is the whole mechanism, and
   is the thing "core support" arguments get wrong in the other direction.

The honest version of this example cuts at CES too: approval elects Begich under the leader rule, but under the
bullet-voting behaviour actually observed in Fargo, Dartmouth and the MAA it degenerates toward plurality, and
plurality elected Peltola. CES cites the right election for the wrong reason.

### CES — ["How Approval Voting and RCV Are Different"](https://electionscience.org/education/differences) (Jul 2024)

A short neutral explainer, and **the most accurate page any advocacy organization has on this list.** It describes
both mechanics without disparaging either, correctly names exhausted ballots ("their ballots are removed from the
entire process, or 'exhausted'"), and states the stopping rule as "until someone gets 50% of **the remaining
votes**." It closes: "Every person is entitled to like approval voting, ranked choice voting (RCV) or both."

That formulation is the punchline of this whole section. **Approval voting's campaign arm describes IRV's majority
threshold more accurately than FairVote does** — FairVote's page claims RCV runs until "a majority winner (a
candidate won with more than half of the vote)" and never mentions exhaustion at all. When the opposing advocate
states your method's guarantee more precisely than you do, that is a fact about your page, not about the method.

### FairVote — ["Ranked Choice Voting vs. Approval Voting"](https://fairvote.org/resources/electoral-systems/ranked_choice_voting_vs_approval_voting/)

Longer, sourced, and genuinely checkable — but its only argument section is titled "Advantages of RCV compared to
approval voting," with no counterpart, and its RCV evidence is overwhelmingly FairVote's own data pages while the
approval critiques cite outsiders. Data stops at August 2022.

> **Watch the domain.** `rankedchoicevoting.org` is **FairVote**, not a second source. It serves FairVote's
> homepage byte-identically — same SHA-1 as `fairvote.org`, `<title>Homepage - FairVote</title>`,
> `<link rel="canonical" href="https://fairvote.org/">` — and browsers normalise the address bar to `fairvote.org`
> on load. Checked 2026-08-01.
>
> This matters because that domain used to belong to someone else. The **Ranked Choice Voting Resource Center**
> is a separate 501(c)(3) serving election *administrators* — implementation guidance, "RCV in a Box", state
> assessments, officials' webinars — and search descriptions still identify `www.rankedchoicevoting.org` as its
> website. RCVRC is now at [rcvresources.org](https://www.rcvresources.org/) (403s to `curl` from bot-blocking;
> live in a browser). I could not establish when or how the domain moved, and make no claim of merger or
> acquisition — only that the neutral-sounding domain now resolves to the advocacy org.
>
> Practical consequence: a citation to "rankedchoicevoting.org" and one to "fairvote.org" are **the same source**,
> and counting them as two independent ones overstates corroboration. For non-advocacy material — ballot design,
> tabulation logistics, audits, exhaustion as an operational fact rather than a talking point — use RCVRC or the
> Bipartisan Policy Center's [*Reform Meets Reality*](https://bipartisanpolicy.org/report/reform-meets-reality-how-ranked-choice-voting-impacts-election-administration/).

**Where it is right, and these are not small:**

- Bullet voting is approval's core weakness, and Nagel's *Burr Dilemma* is cited legitimately.
- Approval cannot express strength of preference between two approved candidates — the later-no-harm trade above,
  stated accurately.
- "Ranking another candidate second will not hurt your first choice" is **true**: IRV satisfies later-no-harm and
  approval does not. Honestly stated, and the one criterion where approval is strictly worse.
- St. Louis Ward 17: the approval leader at 69% lost the head-to-head runoff. A real observed data point.
- The Fargo candidate quotes are real, and damning.

**Where it mirrors CES:**

| Claim | Problem |
|---|---|
| "RCV is a majority system"; the count "continues until there's a majority winner" | A majority of *continuing* ballots in the final round, not of ballots cast — exhausted ballots routinely put the winner below half (Maine CD-2, 2018). The page is internally inconsistent: it dings approval for "no guarantee that the winner will have the support of at least half of the voters," then claims RCV supplies exactly that guarantee |
| "Approval voting has no majority criterion" | The criterion is defined over ranked ballots; and compliance here is model-dependent — ✗ under zero-information, ✓ under the other three rows |
| 60% bullet voting in Fargo proves approval "reverts to plurality-like dynamics" | Its own headline stat is that 71% of RCV voters rank multiple candidates — i.e. ~29% bullet vote there too, which is what produces exhausted ballots. Same behaviour, opposite framing |
| "No sustained evidence finds that approval voting increases representation" | Absence of evidence from two cities over ~2 years, presented as a contrast in findings — while the same page correctly says approval lacks data |

Selective disclosure is the real tell: approval's manipulability gets a full section, while IRV's
non-monotonicity, favorite betrayal and center squeeze are never named — though the page's own
"doesn't elect broadly-supported candidates" argument applies to IRV at least as forcefully
([hare-center-squeeze-examples](hare-center-squeeze-examples.md),
[lumen-75-ballot-four-winners](lumen-75-ballot-four-winners.md), and Burlington 2009 / Alaska 2022 in
[rcv-and-core-support](rcv-and-core-support.md)).

### RCVRC — [rcvresources.org](https://www.rcvresources.org/), ["Why adopt RCV?"](https://www.rcvresources.org/why-adopt-rcv) and the [FAQ](https://www.rcvresources.org/frequently-asked-questions)

The **Ranked Choice Voting Resource Center**, a division of the Election Administration Resource Center
(nonpartisan 501(c)(3)) — the org whose old domain FairVote now serves (see the callout above). Aimed at election
administrators rather than voters, and that changes the failure mode: it is *less* balanced than FairVote by
construction and *more* accurate in practice, because operational questions have answers that aren't contested.

**Not balanced, and candid about why.** There is a "Why adopt RCV?" page and no counterpart. Asked in the FAQ
whether it covers approval, STAR, score or Borda, the answer is: "No, we do not… we are focused on the
implementation of ranked choice voting (RCV) and no other voting methods. If you are interested in any of these
methods, we encourage you to start your own resource center." Snippy, but it is a clearer scope declaration than
either campaigner makes.

**Where it is more honest than FairVote, on exactly the points FairVote gets wrong:**

- **Exhausted ballots, stated plainly and unprompted, twice.** "If you do not rank any other candidates and your
  first-choice candidate gets eliminated, your ballot becomes exhausted and will not count in any later rounds."
  FairVote's comparison page never uses the word. This is the largest honesty gap in the survey.
- **No flat majority claim.** RCV yields "a majority or, **at least**, strong plurality winners" — precisely the
  hedge FairVote drops. Its Portland 2024 example locates the number correctly: Wilson on 34% of first choices,
  "59% of the vote in the final round of tabulation."
- **Election-night timing answered without defensiveness.** "Some RCV winners will be known on election night,
  while others may not be known until all ballots are counted," with the real bottleneck identified as ballot
  scanning — common to every election. A better answer to CES's delay attack than a campaigner could write.
- **Audits, concretely**: Minneapolis and San Francisco, plus risk-limiting audit pilots in 2019–2020. No other
  page in this survey has any audit content.
- **UOCAVA is the best material on any of the six pages.** Runoffs disenfranchise deployed and overseas voters
  when the second round comes faster than international mail; ranked ballots fix it in one mailing. Six states do
  this as of 2025 — AL, AR, GA, LA, MS, SC — plus Springfield, IL. Genuine administrative substance with no
  ideological load, and it is an argument for *ranked ballots as infrastructure* rather than for IRV as a rule.

**Where it is still campaigning:**

- **It cites FairVote as its evidence base** — "reports on the impact of RCV on civility in elections are
  available from FairVote." With the domain finding above, the circle tightens rather than widens: the
  administration-facing resource routes its impact research to the advocacy org. Not independent corroboration.
- **"Won't RCV confuse voters? No."** Flat denial, immediately followed by the honest concession that
  "tabulation of RCV results can be more involved." The "No" does the advocacy; the next sentence does the work.
- **Same selective disclosure, milder.** "Does ranking more than one candidate weaken my first-choice vote? No"
  is *true* — later-no-harm. But nothing on the site says that ranking your true favorite **first** can hurt you.
  Alaska 2022 appears as evidence for campaign civility; its center squeeze goes unmentioned
  ([rcv-and-core-support](rcv-and-core-support.md)).
- Self-description as "the premier source… nationally recognized for our expertise."

### CRV — ["The Joys of Approval Voting"](https://rangevoting.org/approval.html) (Warren D. Smith, Center for Range Voting)

The odd one out, and the most informative page in the survey for structural reasons. CRV advocates **range
voting**, so approval is its *second* choice, and the variants list says so outright: "We could add intermediate
options between full approval and full disapproval. When you do that, you get range voting." Everything below
follows from that. It is the only page here that concedes a weakness of the method it is promoting, the only one
that fact-checks its own guest author, and the only one that makes a quantitative argument at all — which means
it is the only one I can check instead of adjudicate.

It also declares its sources honestly, in a way no other page attempts: it names five people whose sentences it
uses (Brams, Kimport, Ossipoff, Jennings, Lomax), warns that "Brams may not entirely agree with the present page,"
and adds "We in turn do not entirely agree with that essay."

**The voting-power table, checked — and it does not survive.** The page defines voting power as the number of
candidate pairs your ballot can discriminate between, gives plurality *N*−1 and approval *N*²/4, and tabulates the
ratio **N²/(4N−4)**: 1.125 at 3 candidates, 2.778 at 10, 25.25 at 100. Three problems, in increasing order of
seriousness.

1. **One row is simply wrong.** At *N* = 20 the page prints **5.363**; its own formula gives 400/76 = **5.263**.
   Every other row matches to the digit, so this is a transposition, not a different model.
2. **Every odd row overstates.** A ballot approving *k* of *N* discriminates *k*(*N*−*k*) pairs — plurality is
   just the *k* = 1 case — so approval's maximum is ⌊N/2⌋⌈N/2⌉, not *N*²/4. For odd *N* that is (*N*²−1)/4, and
   the correction is not cosmetic at the small end:

   | *N* | Page | Integer-correct | |
   |---|---|---|---|
   | 3 | 1.125 | **1.000** | no gain at all |
   | 5 | 1.563 | 1.500 | |
   | 7 | 2.042 | 2.000 | |
   | 9 | 2.531 | 2.500 | |
   | 20 | 5.363 | 5.263 | even *N*, so this one is just the arithmetic slip above |

   **In the canonical three-candidate spoiler scenario — the case the page's own opening argument is about — the
   gain by this metric is exactly zero.** Approving 2 of 3 discriminates the same two pairs as approving 1 of 3.
3. **It is an upper bound over ballots that voters demonstrably don't cast.** The maximum is reached only by
   approving half the field; a bullet vote scores *N*−1, i.e. **plurality's power exactly**. Every measured approval
   electorate in this note bullet-votes at roughly that rate — MAA 79%, Dartmouth over 80%, and IEEE ~80%
   "plurality-style" *by CRV's own account* (see below). So the advertised power ratio is the value of a ballot
   four voters in five decline to cast.

   And the metric's premise is the zero-information model: it counts all pairs as equally likely to be the
   pivotal one. That is precisely the assumption under which worked example 1 above
   elects Memphis, the Condorcet *loser*. Under an informative poll only one pair is live — leader versus
   runner-up — which plurality can also discriminate, by voting for the better frontrunner. What approval actually
   buys there is that you needn't abandon your favorite to do it. That is the **sincere favorite criterion**,
   which the note establishes above without a formula and which holds in every row of the compliance table. The
   power table is a weaker, breakable version of a claim CRV already has in stronger form.

**The overclaim is CES's, word for word in substance:** "With approval voting, spoilers do not happen." False as
stated, refuted the same way — IIA ✗ in three of four rows, and worked example 2 is a constructed instance. The
same sentence continues "approving your true favorite is never strategically unwise," which is **true**; the
compound sentence welds an unconditional falsehood to a genuine theorem.

> **The refutation is on CRV's own site, disabled.** Its sub-page
> [EarlyUS.html](https://rangevoting.org/EarlyUS.html) contains, inside an HTML comment and therefore invisible in
> a browser, a paragraph in Smith's voice ending: "'vote splitting' effects *can* still occur in approval voting —
> contrary to some advertising." A second comment on the same page hides the remainder of Nagel's abstract, the
> part urging researchers toward instant-runoff options. These are the only two substantive comments on the page,
> and both cut against approval; the main approval page has none. I record this as a fact about the source —
> commented-out text is often just a draft the author disabled — and make no claim about why.

**The history list is the page's weakest section and its most-copied one.** Its summary sentence — Venice,
Sparta, papal conclaves, "1000s of elections in the USSR," "the first 4 USA presidencies," UN Secretary-General —
carries a single hedge: "(Approximately. The rules were slightly different in most of these cases…)" naming only
the vice-presidential twist. Verdicts on the claims not already in the table above:

| Claim | Verdict |
|---|---|
| Sparta was **range**, Venice **approval** | Correctly assigned, and more careful than most retellings — the Spartan shout is a loudness rating, not a set |
| "Used to elect the first 4 USA presidencies" | **Not approval.** Article II gave each elector **exactly two** votes, for two different persons, one of whom had to be from another state — mandatory *k* = 2 with a residency constraint, where approval's defining property is that *k* is unlimited. Nagel's own phrasing, which the page quotes, is "a variant of approval voting" |
| — and the hedge names the wrong twist | The VP consolation prize is the *second* problem. CRV's own sub-page concedes the first: "the early USA was not precisely using approval voting because there was a 2-vote limit," and that 1796, with 13 candidates, is "more dubious" |
| USSR, "1000s of elections" | Real, and better sourced than anything on the page — the sub-page cites five NYT pieces and an FEC report for the 21 June 1987 vote across ~5% of the USSR's 50,000 localities. But it was **disapproval** voting (cross names off), and the page says so itself |
| China's NPC since 1979 | Offered without comment as a credential |
| Econometric Society fellows (1980), NAS final ballot (1981), PA Democratic straw poll (1983), ND Senate bill (1987), Oregon five-option advisory referendum (1990) | Brams–Fishburn material, consistent with the published record; not independently checked here |
| Societies "beginning in 1987" | The table above dates MAA to 1986. One-year discrepancy, unadjudicated |

**The fourth of those four US elections is the Jefferson–Burr tie of 1800** — the event that gives the **Burr
dilemma** its name in the glossary above, and the reason the 12th Amendment exists. CRV's flagship American
precedent for approval is the system whose collapse supplies approval's signature strategic pathology. The
sub-page argues the tie was not really a pathology (both men won) while conceding the mechanism.

**The membership arithmetic is stale in the same way CES's Fargo page is.** The adopters list totals ~466,000
members, of which **IEEE's 377,000 is 81%** — and IEEE dropped approval in 2002. The page presents it in the
present tense and closes "at least several hundred thousand individuals have had direct experience with AV," a
figure that is mostly one defector. CRV is not unaware: a separate page,
[FeerstTheory](https://rangevoting.org/FeerstTheory.html), documents the abandonment, carries Unger's account
that IEEE adopted approval to stop one insurgent candidate and dropped it when he died, has Brams confirming the
2002 decision, and elsewhere gives the ~80% plurality-style voting figure. **That is an approval-friendly source
independently corroborating this note's bullet-voting thesis** — and it is the third measured electorate, after
MAA and Dartmouth, to land near 80%. It is also where you learn that **Jack Nagel — author of the Burr-dilemma
critique — was one of the two people who got IEEE to adopt approval in the first place.**

**Where it is honest — and whose honesty it is.** Three genuine concessions:

- **The cutoff problem, named.** "Although AV encourages sincere voting, it does not altogether eliminate
  strategic calculations… the voter is still faced with the decision of where to draw the line between acceptable
  and nonacceptable candidates," and "the voter's calculus and its effects on outcomes is not yet entirely
  understood." Only FairVote otherwise names this.
- **A recommendation against its own method**: "in elections with more than one winner AV is not recommended if
  the goal is to mirror a diversity of views, especially of minorities."
- Both are Brams's sentences, lightly edited, from his MIT alumni column
  ([BramsWM](https://rangevoting.org/BramsWM.html), c. 2002 — datable from "Arrow… 51 years ago" and the 2000
  election). Brams wrote "not yet **well** understood for either AV or other voting procedures"; CRV prints "not
  yet **entirely** understood either for AV or **especially for more complicated** voting procedures," turning a
  confession into a comparative. **Every hedge on the page is borrowed; the unhedged prose is CRV's own.**

**And then it fact-checks its guest.** The Brams column is hosted with four bracketed editor's notes, all
correcting *against* approval — the only instance of this in the survey:

| Brams claims | CRV's editor's note |
|---|---|
| Condorcet candidates "almost always win under AV" | "'almost always' was too strong: three of the five 2001–2005 Debian leader elections featured different Approval and Condorcet winners" |
| AV "will reduce negative campaigning" | "not supported by any evidence I know of. And indeed there is some evidence against it" — citing Nagel's Burr dilemma |
| AV "will increase voter turnout" | "probably is true but is not supported by direct evidence" |
| AV gives minority candidates "their proper due" | Still "distorts the vote totals heavily against them… range voting experimentally gives such candidates far higher vote counts" |

Two of those are the Brams–Herschbach predictions listed under empirical comparisons
above, marked unevidenced by a sympathetic source. And the fourth note shows the mechanism plainly: the
correction terminates in range voting. **CRV concedes accurately, and every concession is an advertisement.**

#### The AppCW theorem — sound proof, oversold conclusion

CRV's sharpest technical page is ["Approval yields Condorcet winners in
practice"](https://www.rangevoting.org/AppCW.html), and it is the formal backing for the "for practical
purposes, Approval is a Condorcet method" line. It deserves working through, because the proof is correct and
the headline is not what the proof establishes. Verified with
[code/appcw-threshold/verify.py](code/appcw-threshold/verify.py); output in
[run-output.txt](code/appcw-threshold/run-output.txt).

**The claim.** Voters rank the candidates, pick a threshold, approve everything above it, and — if the approval
winner *A* and the Condorcet winner *C* would differ — place that threshold between *A* and *C*. Then, the page
says, no election exists in which *A* ≠ *C*.

**The proof, in full**: suppose *A* ≠ *C*. Voters threshold between them. A majority prefers *C* to *A*, so *C*
is approved more often than *A*. So *A* was not the approval winner. Contradiction.

**The step is exactly right, and its reason is the identity from the electowiki section below.** Ballots
approving both or neither of the two frontrunners cancel, so the approval margin between them *is* their
pairwise margin. Checked over all 3-candidate profiles up to 12 voters against every frontrunner belief —
**111,378 cases, zero violations.** This is not an approximation; it is the same algebra.

**The leap is not.** "*A* is not the winner" is not "*C* is the winner," and the proof never closes that gap. A
third candidate sitting above both camps' thresholds can outpoll both. A 100-voter witness, three candidates:

| Ballots | | Pairwise |
|---|---|---|
| 51 | `C > D > A` | C beats A 51–49 |
| 49 | `D > A > C` | C beats D 51–49 |

***C* is the Condorcet winner.** Now let the poll say the race is *A* versus *C*, with *A* ahead — a wrong poll,
since the true top two are *C* and *D*. Every voter plays the leader rule against that belief:

| Belief | A | C | D | Winner |
|---|---|---|---|---|
| *A* leads *C* | 49 | 51 | **100** | **D** — approved on every ballot, and not the Condorcet winner |
| *C* leads *A* | 49 | 51 | 49 | C |
| *C* leads *D* (true pair) | 49 | 51 | 49 | C |
| *D* leads *C* (true pair) | 0 | 51 | 49 | C |

Nobody voted insincerely, nobody's preferences changed, and the theorem's own strategy was followed to the
letter. Name the wrong pair and the Condorcet winner loses to a candidate every single ballot approved. Across
all profiles with a Condorcet winner up to 12 voters, **27.3% of (profile, belief) combinations fail to elect it
outright** — inflated by counting ties as failures, so read the witness rather than the percentage, but the
direction is not in doubt.

**So the theorem is a fixed point, not a result about elections.** Its hypothesis is not an assumption about how
voters behave — it is the assumption that voters' beliefs about the top two are *correct*, which is the thing
the election is held to determine. Stated honestly it reads: *approval has an equilibrium at the Condorcet
winner.* That is Laslier's leader-rule result, already in the strategy section above, and CRV's own authorship
note concedes the priority chain — Smith Aug 2006, Laslier independently Dec 2006, and "it already had been
stated in Laurent Mann's PhD thesis at Ecole Polytechnique in Palaiseau 1995" (that thesis I could not locate;
recorded as CRV's claim).

**And the hypothesis is the exact negation of the chicken dilemma.** "Place your threshold between the top two"
presumes there are two plausible winners. The Burr situation is the three-viable-candidate case, where no such
pair exists — so the theorem is silent precisely where approval's best-documented pathology lives. CRV knows
this: its own [range-vs-approval page](https://rangevoting.org/rangeVapp.html) lists Burr's dilemma as item 13,
one item after "A failure of approval voting in the real world."

#### …and the Burr page answers Nagel with the same assumption

[BurrSummary](https://www.rangevoting.org/BurrSummary.html) gives CRV's reply to the chicken dilemma, and it has
two legs. The first is a genuine argument — the asymmetry objection, worked into the strategy section above, and
the strongest thing anyone in this survey says in approval's defence. The second is: "**Problem also lessened
with better pre-election polling**: if the voters knew C was thus-likely to win, then A and B would not be the
two 'frontrunners'… and the problem would disappear or diminish."

That is AppCW's hypothesis, restated for a different objection. So **CRV's answers to approval's two best-known
problems — that it need not elect the Condorcet winner, and that it has a chicken dilemma — are the same
assumption used twice: the poll is right.** The witness above is what that assumption costs when it isn't: a
wrong pair, honest voters, the theorem's own strategy, and a third candidate winning on every ballot. This note's
Tennessee example makes the same point from the other end — expectations don't perturb an approval result, they
determine it.

Two things on that page worth keeping regardless:

- **The name is probably wrong, and CRV says so first.** "It is probably misnamed since this problem actually
  did not happen in the Burr 1800 election — Burr & Jefferson still placed top." Correct: 1800 produced a
  **73–73 tie** with Adams back on 65, which is a coordination failure, not a third candidate slipping through.
  It answers the disaster mode rather than the mechanism — Nagel's claim is about the chicken *tension*, and the
  tie is what that tension produced. CRV pushes further, and this part is sharp: the campaign to savage Burr was
  organised by **Hamilton**, their opponent, so the 1800 strategising was done by the *C* camp — "exactly the
  opposite of Nagel's thinking."
- **A methodological concession about CRV's flagship number.** "Because our Bayesian regret computer simulations
  employed thus-logical strategic voters… the BR measurements were unable to see this whole problem (or only saw
  a small effect from it)." Bayesian regret is the quantitative backbone of the entire site, and here its author
  states that it is blind to the one pathology named in the literature — because the simulated voters are too
  rational to fall into it. Then concludes anyway that the dilemma "seems not to cause a great deal of Bayesian
  regret."

> **A second disabled passage, same pattern as EarlyUS.** An HTML comment on AppCW records Mike Ossipoff
> pointing out that the result may already appear in Niemi & Riker, "The Choice of Voting Systems", *Scientific
> American* **234** (6), June 1976, 21–27 — a real article, citation verified 2026-08-01. Invisible in a
> browser. That makes two rangevoting.org pages whose only substantive commented-out text is a concession
> against the page's own framing.

### electowiki — ["Approval voting"](https://electowiki.org/wiki/Approval_voting)

Not an organization — a community wiki, running since 2005, and **the only source in this survey that declares
its own bias and tells you where to go instead.** From
[Electowiki:Policy](https://electowiki.org/wiki/Electowiki:Policy), under the "EPOV" (electowiki point-of-view)
heading:

> "We have a point of view. electowiki tries to be a general resource for experts to get complete information,
> but makes no promises about neutrality. **Other sources, such as Wikipedia, should be used to obtain neutral
> information.**"

[Electowiki:About](https://electowiki.org/wiki/Electowiki:About) repeats it — "we don't pretend to have a
dispassionate 'neutral point of view'" — and `Electowiki:Neutral_point_of_view` 404s. EPOV does commit to "err on
the side of neutrality" and to "not rewrite history," and reserves "latitude to editorialize on other positions."
So the balance question is answered by the site's own policy; what is left is whether the article is *good*, and
the answer splits cleanly.

**Technically the most honest treatment in the survey:**

- **"Indeterminacy of outcome" is the best section on any page here.** A concrete 15-voter, 3-candidate profile
  where *any* candidate wins with every voter honest, the advocates' rebuttal quoted fairly ("AV responds
  positively to distinctions voters make among candidates that ordinal preference rankings do not mirror"), and
  then Niemi's criticism cited — the method "almost begs voters to behave strategically." Thesis, antithesis,
  footnotes. This is the Saari–Van Newenhizen material above, worked concretely.
- **Names the chicken dilemma** and gives a favorite-betrayal example (10 `A>B`, 41 `B>A`, 49 `C>A`) that it
  explicitly labels an averted center squeeze.
- **Concedes against its own side on summability** — the one advantage CES leans on hardest. Proportional
  approval is *not* precinct-summable, because the winner needs to know which candidates each ballot approved,
  not just per-candidate totals. No other page qualifies this.
- **The Equilibrium section is genuinely sophisticated**, including that "it is not possible to figure out who
  the CW is from Approval ballots."
- **"Connection to Condorcet methods" is the page's largest section and its best technical content** — worked
  out below, because it contains a provable identity, a fair statement of the strongest pro-approval argument,
  and an arithmetic slip.

**And the worst factual hygiene in the survey:**

- **It contradicts itself on IIA within two paragraphs.** "Criterion compliance" asserts flatly that approval
  satisfies "Independence of irrelevant alternatives"; the next section says "in Approval voting the implication
  does not necessarily hold… the rule may lead the election outcome to depend on what non-winning candidates were
  present." The compliance table above is the resolution it lacks: ✓ only under fixed/dichotomous cutoffs, ✗ under
  all three realistic models.
- **Its Tennessee example picks the flattering cutoff** — "supposing that voters voted for their two favorite
  candidates" → Nashville 68, the Condorcet winner. Worked example 1 above runs the zero-information rule on the
  same electorate and elects Memphis, the Condorcet *loser*, on 42.

  Worth keeping as a pair: **Lumen picks top-2 to make approval fail the majority criterion
  ([lumen-75-ballot-four-winners](lumen-75-ballot-four-winners.md)); electowiki picks top-2 to make approval elect
  the Condorcet winner.** Identical floating cutoff, opposite morals — which is the indeterminacy thesis
  demonstrating itself across two sources that never cite each other.
- **Unsourced and strange usage claims.** "China's National People's Congress… has been elected via, essentially,
  Approval Voting since 1979" — "essentially" load-bearing for a body whose elections are indirect and
  uncontested, no citation. "Approval voting was widely used with introducing democracy in the Soviet Union
  started by M.S. Gorbachev" — unsourced and garbled. An entire section, "Relation to effectiveness of choices,"
  rests on "Operations research has shown… sigmoidally related to the level of approval **[citation needed]**"
  and stands anyway.
- Invokes a "unanimous consensus criterion" and "greatest possible consensus criterion" that are not standard
  social-choice criteria; "Effect on elections" gives the criticism one clause and the rebuttal four sentences;
  Fargo is still listed as current usage with no mention of the April 2025 ban.

**Two discrepancies against this note. One resolved, one still open:**

- **Brams–Herschbach date — resolved against electowiki.** It dates the *Science* paper to 2000; the paper is
  ["The Science of Elections"](https://www.science.org/doi/10.1126/science.292.5521.1449), *Science* **292**
  (5521), p. 1449, **25 May 2001**. The DOI encodes the volume, issue and page, and vol. 292 runs April–June
  2001. This note's 2001 stands. Checked 2026-08-01.
- **Greek parliament dates — open.** electowiki says 1864–**1926**, this note (from Wikipedia) says 1864–**1923**.
  Neither side is sourced, so the 1923/1926 endpoint is unverified in both directions — don't cite the end year
  from either without a primary source.

#### Worth taking from it: approval *is* a Condorcet method, on ballots that rank everyone 1st or last

The page's framing, and it is exactly right: treat an approval ballot as a ranked ballot with every approved
candidate tied 1st and every other tied last, count pairwise, and you have run a Condorcet method. What makes
this more than a curiosity is that the resulting matrix is **not** informative in the way a real pairwise matrix
is — and there is a one-line identity behind that.

Count each pair the "negative vote-counting" way: X's score against Y is the number of ballots approving X and
not Y. Ballots approving *both* or *neither* contribute to neither side, so

> margin(X, Y) = (X, not Y) − (Y, not X) = **approvals(X) − approvals(Y)**

Every margin is just the difference of two approval totals. Three consequences, none of which the page states in
one place:

- The pairwise ranking **is** the approval ranking, necessarily. Same order, no new information.
- **Cycles are impossible** — the margins are differences of a single number per candidate, so the relation is
  transitive by construction. This is the same structural fact as the dichotomous-preference row of the
  compliance table above (Inada 1969), arrived at from the ballot side rather than the preference side.
- Which is precisely why "it is not possible to figure out who the CW is from Approval ballots." The matrix
  looks like pairwise data and carries none: it is one number per candidate, wearing a matrix as a costume.

**The worked example has two bad cells.** 30 `AB`, 20 `BC`, 10 `ADE`, 20 `BCE` — approvals B 70, A 40, C 40,
E 30, D 10, and the page's ranking (B; A = C; E; D) is right. But of the 20 off-diagonal cells, **18 are correct
and two are not**: B-vs-A is given as 20 where it is **40**, and B-vs-D as 50 where it is **70**. Both are short
by exactly 20 — the `20 BCE` ballots dropped out of row B twice — and both are detectable from the identity
above, since they are the only two cells whose margin isn't the difference of the approval totals. Verified
2026-08-01 against all 20 cells. The conclusion survives, because the ranking comes from the totals column
rather than the matrix.

**And it states the strongest argument for approval that this note has encountered**, fairly and in one
sentence: when voters are honest you get a utilitarian outcome, and when they are strategic you at least get the
Condorcet winner — so you are covered at both ends. The page adds, against interest, that this is "not as much
the case with Score voting or STAR voting."

The gap is the middle, and the page documents it elsewhere without connecting the two. Strategic approval
voters can always **deny** the pairwise loser of any matchup, but "can not always make the pairwise winner…
win," and this is "most easily seen in chicken dilemma-type situations." A real electorate is neither uniformly
honest nor uniformly strategic; it is a mix, which is the regime the Burr dilemma occupies, and the disjunction
covers the two endpoints while the failure mode lives between them.

### Net

Scored across all eight pages, the four organizations and one wiki are wrong in different registers.

| | CES | FairVote | RCVRC | CRV | electowiki |
|---|---|---|---|---|---|
| Role | Approval advocacy | RCV advocacy | RCV implementation support | **Range** advocacy; approval is its second choice | Community wiki with a *declared* point of view |
| Audience | Voters | Voters, legislators | Election administrators | Reform-curious generalists, online voting-theory readers | Experts and activists already inside the field |
| Sourcing | None on any of three pages | Extensive, though RCV evidence is largely self-citation — and `rankedchoicevoting.org` is the same org under another domain, so it can read as corroboration it isn't | Thin, and routes impact research to FairVote | None inline, but sub-pages carry real citations (five NYT pieces for the USSR claim) and the arithmetic is shown, so it is checkable | Bimodal: real footnotes on the strategy sections, nothing at all on usage history, one section on an unresolved `[citation needed]` |
| Best page | The neutral explainer | The comparison page — one-sided but falsifiable | The FAQ and the UOCAVA material | The hosted Brams column, for the editor's notes correcting it | "Indeterminacy of outcome" — best section in the survey |
| Worst failure | Alaska misdiagnosed as vote-splitting; "no spoiler ever" | "RCV is a majority system"; omits exhaustion entirely | "Why adopt RCV?" with no counterpart; center squeeze never named | "Spoilers do not happen"; a voting-power table wrong in every odd row and one even one | Asserts IIA compliance, then refutes it two paragraphs later; China's NPC cited as an approval-voting user |
| Concedes anything? | Yes — "RCV does not inherently favor any group" | No | Yes — exhaustion, "strong plurality", election-night uncertainty | Yes — the cutoff problem and multiwinner unsuitability, in Brams's borrowed words | Yes — indeterminacy, the chicken dilemma, and that proportional approval is *not* summable |
| Right about the opponent? | Yes on summability, count opacity, round-1-is-plurality | Yes on bullet voting, later-no-harm, cutoff subjectivity | Declines to discuss other methods at all | Right about *approval* — bullet voting, the cutoff, IEEE's reversal are all documented on the site, just not on this page | Cites its critics by name (Niemi) rather than paraphrasing them away |
| Currency | Fargo still shelved as a success story post-ban (Apr 2025) | Data stops Aug 2022 | Current (2025 UOCAVA figures) | IEEE listed as a user 24 years after it quit; **Fargo and St. Louis appear nowhere on the page** | Fargo listed as current usage, no mention of the April 2025 ban |
| Admits its bias? | No | No | Implicitly — states its scope, not its slant | Implicitly — the range preference is the whole page | **Yes, in writing, and names Wikipedia as the fix** |

**The two campaigners each name the other's real problem accurately and deny their own.** FairVote correctly
identifies that approval's cutoff is subjective and that bullet voting collapses it toward plurality — the two
things this note documents best — while claiming a majority guarantee its own method does not deliver. CES
correctly identifies that IRV is unsummable, opaque to audit, and plurality-like in round 1 — all true — while
claiming a spoiler-freedom its own compliance table denies.

**RCVRC is the lesson about what "balanced" buys you.** It is the narrowest of the four — one method, by
charter, with a "why adopt" page and no "why not" — and it is also the most accurate, because its questions are
operational and operational questions have uncontested answers. Balance and accuracy came apart here: the page
most willing to say "your ballot becomes exhausted and will not count" is the one least interested in comparing
methods at all.

**CRV is the lesson about where candor comes from.** It is the only page in the survey that names a weakness of
the method it is promoting, and the reason is not virtue but position: approval is its *second* choice, so every
concession is a step toward range voting. It concedes the cutoff problem in Brams's borrowed sentences, corrects
Brams four times in its own, and each correction ends by pointing at the upgrade. Advocacy pages concede exactly
when the concession sells something — which is also why the two pure campaigners concede nothing.

And **the two approval advocates fail on Fargo in opposite directions**: CES still shelves it as a success story
after the April 2025 ban, while CRV — which has been arguing for approval since the 2000s — never mentions that
the only two US jurisdictions ever to adopt it exist.

Practical use: for approval's genuine weaknesses read FairVote, then CRV's sub-pages (not its approval page) for
the ones FairVote can't be bothered to document; for IRV's genuine weaknesses read the CES head-to-head, then
correct its Alaska paragraph before quoting it; for anything about how RCV is actually run — ballot design,
tabulation, audits, UOCAVA — read RCVRC and ignore its "why adopt" page. None is usable as a summary of the
comparison, and the disagreement between the campaigners is narrower than any admits: all four are arguing
against plurality, and all four are right about that.

**The gap none of them fills.** Across seven pages and four organizations, only CRV discusses a downside of the
method it is promoting, and only because it is promoting something else. Nothing here surveys the field
neutrally, and nothing here reports a failure of its *first* choice — which is why this section is a lookup table
rather than a reading list. For that, the academic sources above and the Bipartisan Policy Center's
[*Reform Meets Reality*](https://bipartisanpolicy.org/report/reform-meets-reality-how-ranked-choice-voting-impacts-election-administration/)
are the substitutes.

## How it sits against the rest of these notes

- **vs. IRV/Hare**: approval cannot center-squeeze the way Hare does
  ([hare-center-squeeze-examples](hare-center-squeeze-examples.md)) — nothing is eliminated, so no backup
  support is ever discarded — and it passes sincere favorite outright. It pays for that with cutoff
  indeterminacy, which IRV doesn't have. The trade is visible on a single electorate in
  [lumen-75-ballot-four-winners](lumen-75-ballot-four-winners.md): IRV returns one answer but the wrong one —
  eliminating the Condorcet winner by a single vote, non-monotonically, while rewarding favorite betrayal —
  and approval's answer is right only if you pick the right cutoff, which the ballots don't give you.
- **vs. Condorcet (Ranked Robin, Schulze, …)**: approval only reaches the Condorcet winner *conditionally* —
  under the leader rule, trembling ballots, or dichotomous preferences. Ranked Robin
  ([ranked-robin-results-explained](ranked-robin-results-explained.md)) gets there unconditionally from the
  pairwise matrix. Approval's counterargument is that the ranked ballot never had the intensity information in
  the first place. The best version of it is electowiki's, above: **honest voters give a utilitarian winner,
  strategic voters give the Condorcet winner, so you are covered at both ends** — with two gaps. Real
  electorates are a mix, and the mix is where the chicken dilemma lives; and the strategic branch is an
  *equilibrium*, not a guarantee — CRV's AppCW theorem delivers the Condorcet winner only when voters' expected
  top two are the actual top two, and a wrong poll can elect a third candidate outright. Note also that approval *is* a
  Condorcet method on {1st, last} ballots; it just can't tell you who the Condorcet winner is, because its
  pairwise margins are only differences of approval totals.
- **vs. [STAR](star-voting.md)**: the "more expressive" branch — 0–5 scores plus an automatic runoff. The
  Independent Party of Oregon walked exactly that path in 2020 after approval failed to produce a nominee.
  Whether the extra levels help or just invite more strategy is the live disagreement; the criticism section
  here is precisely that binary is under-expressive, and the reply is that grading invites strategy. The
  criteria trade is sharp: approval passes sincere favorite outright and fails later-no-harm absolutely,
  while STAR fails both only partially and argues that is the better bargain.
- **vs. LeGrand's ranked-only world**: he prefers approval and never covers it, which is why his site can't
  speak to the cardinal-vs-ordinal argument at all.
- **vs. the academic case for approval**: two papers, pulling opposite ways on the same premise. Brandl and
  Peters take the dichotomous domain as a hypothesis and prove approval is the *only* rule on it, eight
  times ([brandl-peters-approval-characterizations](brandl-peters-approval-characterizations.md)). Horn tries
  to obtain the same domain by fiat — write the ballot instruction as Rule (1) and the restriction is
  imposed rather than assumed — and claims three virtues follow
  ([horn-three-virtues-approval](horn-three-virtues-approval.md)). The move is worth understanding and it
  doesn't work: all three virtues are shared with score voting, and the paper's own worked example elects the
  Condorcet loser and the status quo under sincere Rule (1) ballots. Between them they locate the real
  question exactly — not *is the dichotomous domain nice* (it is, provably) but *can anything make an
  electorate live on it*. The 79% MAA figure above is the answer so far.

## New ideas and terms

- **Approval cutoff / acceptance threshold** — the line a voter draws through their own preference order.
  The whole strategic content of an approval ballot. *Floating* (above-average, top-k) cutoffs break IIA;
  *fixed* (dichotomous) cutoffs don't.
- **Dichotomous preferences** — candidates sort into two indifference classes, acceptable and not. Under this
  model approval is strategyproof and Condorcet-consistent, and by Brandl–Peters (2022) it is the *only*
  rule that is. Unrealistic at scale.
- **Consistency with variable electorates (reinforcement)** — split the voters in two; if both halves choose
  some alternatives in common, the whole electorate must choose exactly those. The axiom every one of the
  eight Brandl–Peters characterizations of approval is built on.
- **Sincere vote (approval sense)** — any ballot that, if it approves X, also approves everything strictly
  above X. Deliberately admits many ballots per voter.
- **Bullet voting** — approving only your favorite. The mechanism by which approval degenerates into
  plurality.
- **Chicken dilemma / Burr dilemma** — two allied frontrunners' camps each bullet-vote to protect their own
  candidate and hand the win to a third. Named for the Jefferson–Burr tie of 1800, and **probably misnamed**:
  1800 produced a 73–73 tie, not a third-candidate win. Nagel 2007; the standing rebuttal is CRV's asymmetry
  argument, and the one candidate real-world instance is a Portugal 1986 counterfactual.
- **Compromising** — approving an unacceptable candidate to block a worse one. The honest-favorite cousin of
  lesser-evil voting.
- **Prospective rating (Myerson–Weber)** — utility weighted by the probability your vote is pivotal in each
  pairwise tie. Approve everything positive.
- **Leader rule (Laslier)** — approve everyone you prefer to the expected leader, plus the leader if you
  prefer them to the runner-up. Its equilibrium is the Condorcet winner — where **"equilibrium" is
  load-bearing**: the result is a fixed point requiring the expected top two to *be* the top two. Believe the
  wrong pair and a third candidate can win outright, on every ballot (the AppCW witness above).
- **Later-no-harm** — approving an additional candidate must not hurt your earlier ones. Approval **fails**
  this, necessarily, and its monotonicity is the flip side of the same coin.
- **Sincere favorite criterion** — approving your true favorite is never counterproductive. Approval passes
  under every voter model.
- **Summability** — a method is summable if a precinct can report one number per candidate. Approval is;
  IRV isn't. An administrative property, not a fairness one, but it drives adoption.
- **Unified primary** — a nonpartisan primary using approval, top two advance. St. Louis' Proposition D
  variant.
- **Overvote immunity** — no ballot can be spoiled by marking too many candidates, because there is no limit.
- **Voting power, pair-discrimination sense (CRV)** — the number of candidate pairs a ballot separates:
  *k*(*N*−*k*) for a ballot approving *k* of *N*. Plurality is the *k* = 1 case, so the two methods are the same
  function under different constraints. An upper bound over available ballots, not a property the method
  delivers — a bullet vote scores exactly plurality — and at *N* = 3 the maximum gain is nil.
- **Negative vote-counting (approval as a Condorcet method)** — score each pair by ballots approving X and not
  Y. Ballots approving both or neither cancel, so every margin collapses to approvals(X) − approvals(Y): the
  pairwise order *is* the approval order, cycles cannot occur, and the matrix holds nothing the totals didn't.
  The reason approval ballots cannot identify the Condorcet winner.
- **Disapproval voting** — the Soviet 1987 form: every candidate is approved unless you cross the name off.
  Logically identical to approval, psychologically the reverse, and CRV says so itself.
- **DYN (Simmons) / SODA (Quinn)** — approval plus delegation: approve candidates, or hand them your ballot to
  place. Sold on immunity to manipulated poll data, which matters exactly because the leader rule makes
  approval's winner a function of published expectations.

## Links referenced in the article

- [Brams & Fishburn, *Approval Voting* (1983)](https://archive.org/details/approvalvoting00bram) — the
  standard reference; nearly every strategy claim above traces here
- Brams & Fishburn, "Going from Theory to Practice: The Mixed Success of Approval Voting" — published in
  *Social Choice and Welfare* **25 (2–3), 2005, 457–474**,
  [doi:10.1007/s00355-005-0013-y](https://doi.org/10.1007/s00355-005-0013-y). The freely readable
  [NYU PDF](https://web.archive.org/web/20181218010629/http://www.nyu.edu/gsas/dept/politics/faculty/brams/theory_to_practice.pdf)
  is the preprint, often cited as 2003; not collated against the published text here. Source of most of the
  society-adoption dates that CRV repeats — and its title is the hedge CRV drops.
- [Laslier & Van der Straeten, "Approval Voting: An Experiment during the French 2002 Presidential Election"](https://web.archive.org/web/20050507223548/http://www.lse.ac.uk/collections/VPP/VPPpdf_Wshop2/jflkvdscaen.pdf)
- [Baujard et al., "Who's favored by evaluative voting?" (2012 French election)](https://hal.archives-ouvertes.fr/hal-00803024/file/cahier_2013-05.pdf)
- [Myerson & Weber, "A Theory of Voting Equilibria"](https://ghostarchive.org/archive/20221009/http://www.kellogg.northwestern.edu/research/math/papers/782.pdf)
- [Laslier, "Strategic approval voting in a large electorate"](https://halshs.archives-ouvertes.fr/docs/00/12/17/51/PDF/stratapproval4.pdf)
- [Nagel, "The Burr Dilemma in Approval Voting" (2007)](https://www.journals.uchicago.edu/doi/10.1111/j.1468-2508.2007.00493.x)
- [Hamlin & Hua, "The case for approval voting" (2023)](https://doi.org/10.1007/s10602-022-09381-x)
- [Center for Election Science — Fargo's first approval election](https://www.electionscience.org/commentary-analysis/fargos-first-approval-voting-election-results-and-voter-experience/)
- [Center for Election Science — Fargo's second approval election](https://electionscience.org/commentary-analysis/fargos-second-approval-voting-election-runs-smoothly/)
- [AP: North Dakota governor signs bill ending Fargo's voting system (April 2025)](https://apnews.com/article/fargo-north-dakota-legislature-voting-elections-8f85df3e17bf77fd7af41693569831ac)
- **CRV / rangevoting.org**, read 2026-08-01 —
  ["The Joys of Approval Voting"](https://rangevoting.org/approval.html) (the page proper) ·
  [Approval executive summary](https://rangevoting.org/AppExec.html) ·
  [Range vs. approval, items 12–13](https://rangevoting.org/rangeVapp.html) (approval's real-world failure and
  Burr's dilemma, in CRV's own words) ·
  [the first four US presidential elections](https://rangevoting.org/EarlyUS.html) (with the two-vote limit
  conceded, and two passages disabled in HTML comments) ·
  [Soviet use](https://rangevoting.org/SovietApp.html) (the best-sourced claim on the site) ·
  [why IEEE abandoned it](https://rangevoting.org/FeerstTheory.html) (Unger, with a note from Brams)
- [Brams, "Approval Voting: A Better Way to Select a Winner"](https://rangevoting.org/BramsWM.html) — the MIT
  alumni "What Matters" column, c. 2002, which supplies CRV's page with its hedges; hosted with four editor's
  notes correcting it against approval
- Brams & Nagel, "Approval Voting in Practice", *Public Choice* **71 (1–2), 1991, 1–17**,
  [doi:10.1007/BF00138446](https://doi.org/10.1007/BF00138446) — the IEEE adoption written up by the two people
  who arranged it, one of whom later wrote [the Burr dilemma paper](https://www.journals.uchicago.edu/doi/10.1111/j.1468-2508.2007.00493.x)
- [Score voting](https://en.wikipedia.org/wiki/Score_voting) ·
  [Multiwinner approval](https://en.wikipedia.org/wiki/Multiwinner_approval_voting) ·
  [Sequential proportional approval](https://en.wikipedia.org/wiki/Sequential_proportional_approval_voting) ·
  [Unified primary](https://en.wikipedia.org/wiki/Unified_primary)

## Further reading — not cited by the article

- [Brandl & Peters, "Approval voting under dichotomous preferences: A catalogue of characterizations" (2022)](https://www.dominik-peters.de/publications/av.pdf)
  — *Journal of Economic Theory* 205, 105532, [doi:10.1016/j.jet.2022.105532](https://doi.org/10.1016/j.jet.2022.105532)
  ([ScienceDirect, paywalled](https://www.sciencedirect.com/science/article/abs/pii/S0022053122001223); the
  authors' PDF above is free). Eight characterizations of approval on the dichotomous domain, all resting on
  consistency with variable electorates. The modern companion to Brams–Fishburn 1978 and the reason the
  dichotomous row of the compliance table above is a uniqueness theorem rather than a favorable assumption.
  **Worked out in full, with a verifier, in
  [brandl-peters-approval-characterizations](brandl-peters-approval-characterizations.md)** — including why
  the Condorcet ✓ in that row is structural (Inada 1969: the majority relation is transitive here, so cycles
  cannot occur at all), and a price list for the bullet-voting collapse recorded above: the paper's
  Example 5 *is* plurality, the scoring rule (1, 0, …, 0), and it keeps 5 of the 17 axioms tracked there
  while losing 12.
- [Horn, "Three Unique Virtues of Approval Voting" (2024)](https://www.qeios.com/read/ZETKEQ.2) — Qeios,
  peer-approved, [doi:10.32388/ZETKEQ.2](https://doi.org/10.32388/ZETKEQ.2), CC BY. The case that approval
  satisfies IIA, defeats agenda-setting, and escapes Arrow. Take the Rule (1) / Rule (2) distinction, which
  is the best framing of the compliance table above that I have seen anywhere; leave the three virtues, all
  of which score voting shares. **Checked line by line, with a verifier, in
  [horn-three-virtues-approval](horn-three-virtues-approval.md)** — including nine errata in the worked
  example, and the enumeration showing that the paper's own ballots elect the outcome it says approval makes
  impossible.

## Related local material

- [brandl-peters-approval-characterizations](brandl-peters-approval-characterizations.md) — the axiomatic
  half of this note: what approval is *forced* to be, and on what domain
- [horn-three-virtues-approval](horn-three-virtues-approval.md) — the advocacy half, in a refereed paper
  rather than on a campaign page: Rule (1) vs. Rule (2), the three readings of IIA, and what happens when the
  cutoff indeterminacy documented here is run against an argument that denies it
- [agreeable-societies](agreeable-societies.md) — the geometric half: approval sets as intervals on a
  political spectrum, asking how much agreement an *electorate* contains rather than which candidate wins.
  Its **(k,m)-agreeable** hypothesis is the same species of domain restriction as dichotomous preferences
  above — strong theorems, unobservable premise — and unlike the advocacy pages surveyed here, its authors
  say so themselves
- [glossary.md](glossary.md) — all terms above are indexed there
- [rcv-and-core-support](rcv-and-core-support.md) — the cardinal-vs-ordinal argument approval sits inside
- [legrand-ranked-ballot-methods](legrand-ranked-ballot-methods.md) — the ranked-only site whose author
  prefers approval to everything on it
- [hare-center-squeeze-examples](hare-center-squeeze-examples.md) — the failure mode approval is immune to
- [lumen-75-ballot-four-winners](lumen-75-ballot-four-winners.md) — cutoff indeterminacy worked on a ranked
  profile, and a textbook that mistakes one stipulated cutoff for the method
- [star-voting](star-voting.md) — the six-level end of the same family, with worked criterion failures
