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
  director's stated reason was that "few of our members were using it." Dartmouth's alumni association
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
- **Brams and Herschbach (*Science*, 2001)**: approval should raise turnout, defuse spoilers, and reduce
  negative campaigning — you're courting your opponents' approvals, not just your own base.
- **1987 MAA presidential election, 5 candidates, 3,924 voters** (Brams' analysis): 79% approved exactly one,
  16% two, 5% three, 1% four. Winner had **1,267 approvals = 32%**. Even among mathematicians who chose the
  method, four out of five bullet voted.

## How the advocacy organizations present it

Six pages read on 2026-08-01 — three CES, one FairVote, two RCVRC. **None of the six discusses a downside of the
method its organization exists to support.** The two campaigning orgs fail in mirror-image ways: each states a
property that holds only under a favorable assumption as though it held unconditionally. CES: "no candidate can
ever be a spoiler" (true only under dichotomous preferences). FairVote: "RCV is a majority system" (true only of
continuing ballots). Everything needed to adjudicate them is already above, so this is mostly a lookup table.

The useful surprise is that no org is uniformly worse, and that **accuracy does not track balance**. CES's
flagship explainer is the weakest document here and its head-to-head page carries the worst single factual error,
yet CES's neutral explainer is the most accurate page either campaigner produced. FairVote's page is better
sourced than all three CES pages combined and is right about approval's real weakness — while being wrong about
its own method's central claim. And the most accurate pages of all belong to RCVRC, an organization that is
*less* balanced than FairVote by construction, because it is scoped to one method and says so.

Ranked by accuracy rather than balance: **RCVRC > CES "Differences" > FairVote > CES head-to-head > CES
explainer.**

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

### Net

Scored across all six pages, the three organizations are wrong in different registers.

| | CES | FairVote | RCVRC |
|---|---|---|---|
| Role | Approval advocacy | RCV advocacy | RCV implementation support |
| Audience | Voters | Voters, legislators | Election administrators |
| Sourcing | None on any of three pages | Extensive, though RCV evidence is largely self-citation — and `rankedchoicevoting.org` is the same org under another domain, so it can read as corroboration it isn't | Thin, and routes impact research to FairVote |
| Best page | The neutral explainer | The comparison page — one-sided but falsifiable | The FAQ and the UOCAVA material |
| Worst failure | Alaska misdiagnosed as vote-splitting; "no spoiler ever" | "RCV is a majority system"; omits exhaustion entirely | "Why adopt RCV?" with no counterpart; center squeeze never named |
| Concedes anything? | Yes — "RCV does not inherently favor any group" | No | Yes — exhaustion, "strong plurality", election-night uncertainty |
| Right about the opponent? | Yes on summability, count opacity, round-1-is-plurality | Yes on bullet voting, later-no-harm, cutoff subjectivity | Declines to discuss other methods at all |
| Currency | Fargo still shelved as a success story post-ban (Apr 2025) | Data stops Aug 2022 | Current (2025 UOCAVA figures) |

**The two campaigners each name the other's real problem accurately and deny their own.** FairVote correctly
identifies that approval's cutoff is subjective and that bullet voting collapses it toward plurality — the two
things this note documents best — while claiming a majority guarantee its own method does not deliver. CES
correctly identifies that IRV is unsummable, opaque to audit, and plurality-like in round 1 — all true — while
claiming a spoiler-freedom its own compliance table denies.

**RCVRC is the lesson about what "balanced" buys you.** It is the narrowest of the three — one method, by
charter, with a "why adopt" page and no "why not" — and it is also the most accurate, because its questions are
operational and operational questions have uncontested answers. Balance and accuracy came apart here: the page
most willing to say "your ballot becomes exhausted and will not count" is the one least interested in comparing
methods at all.

Practical use: for approval's genuine weaknesses read FairVote; for IRV's genuine weaknesses read the CES
head-to-head, then correct its Alaska paragraph before quoting it; for anything about how RCV is actually run —
ballot design, tabulation, audits, UOCAVA — read RCVRC and ignore its "why adopt" page. None is usable as a
summary of the comparison, and the disagreement between the campaigners is narrower than either admits: both are
arguing against plurality, and both are right about that.

**The gap none of them fills.** Across six pages and three organizations, not one discusses a downside of the
method it exists to support. Nothing here surveys the field neutrally, and nothing here reports a failure of its
own method — which is why this section is a lookup table rather than a reading list. For that, the academic
sources above and the Bipartisan Policy Center's
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
  the first place.
- **vs. [STAR](star-voting.md)**: the "more expressive" branch — 0–5 scores plus an automatic runoff. The
  Independent Party of Oregon walked exactly that path in 2020 after approval failed to produce a nominee.
  Whether the extra levels help or just invite more strategy is the live disagreement; the criticism section
  here is precisely that binary is under-expressive, and the reply is that grading invites strategy. The
  criteria trade is sharp: approval passes sincere favorite outright and fails later-no-harm absolutely,
  while STAR fails both only partially and argues that is the better bargain.
- **vs. LeGrand's ranked-only world**: he prefers approval and never covers it, which is why his site can't
  speak to the cardinal-vs-ordinal argument at all.

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
  candidate and hand the win to a third. Named for the Jefferson–Burr tie of 1800.
- **Compromising** — approving an unacceptable candidate to block a worse one. The honest-favorite cousin of
  lesser-evil voting.
- **Prospective rating (Myerson–Weber)** — utility weighted by the probability your vote is pivotal in each
  pairwise tie. Approve everything positive.
- **Leader rule (Laslier)** — approve everyone you prefer to the expected leader, plus the leader if you
  prefer them to the runner-up. Its equilibrium is the Condorcet winner.
- **Later-no-harm** — approving an additional candidate must not hurt your earlier ones. Approval **fails**
  this, necessarily, and its monotonicity is the flip side of the same coin.
- **Sincere favorite criterion** — approving your true favorite is never counterproductive. Approval passes
  under every voter model.
- **Summability** — a method is summable if a precinct can report one number per candidate. Approval is;
  IRV isn't. An administrative property, not a fairness one, but it drives adoption.
- **Unified primary** — a nonpartisan primary using approval, top two advance. St. Louis' Proposition D
  variant.
- **Overvote immunity** — no ballot can be spoiled by marking too many candidates, because there is no limit.

## Links referenced in the article

- [Brams & Fishburn, *Approval Voting* (1983)](https://archive.org/details/approvalvoting00bram) — the
  standard reference; nearly every strategy claim above traces here
- [Brams & Fishburn, "Going from Theory to Practice: The Mixed Success of Approval Voting" (2003)](https://web.archive.org/web/20181218010629/http://www.nyu.edu/gsas/dept/politics/faculty/brams/theory_to_practice.pdf)
- [Laslier & Van der Straeten, "Approval Voting: An Experiment during the French 2002 Presidential Election"](https://web.archive.org/web/20050507223548/http://www.lse.ac.uk/collections/VPP/VPPpdf_Wshop2/jflkvdscaen.pdf)
- [Baujard et al., "Who's favored by evaluative voting?" (2012 French election)](https://hal.archives-ouvertes.fr/hal-00803024/file/cahier_2013-05.pdf)
- [Myerson & Weber, "A Theory of Voting Equilibria"](https://ghostarchive.org/archive/20221009/http://www.kellogg.northwestern.edu/research/math/papers/782.pdf)
- [Laslier, "Strategic approval voting in a large electorate"](https://halshs.archives-ouvertes.fr/docs/00/12/17/51/PDF/stratapproval4.pdf)
- [Nagel, "The Burr Dilemma in Approval Voting" (2007)](https://www.journals.uchicago.edu/doi/10.1111/j.1468-2508.2007.00493.x)
- [Hamlin & Hua, "The case for approval voting" (2023)](https://doi.org/10.1007/s10602-022-09381-x)
- [Center for Election Science — Fargo's first approval election](https://www.electionscience.org/commentary-analysis/fargos-first-approval-voting-election-results-and-voter-experience/)
- [Center for Election Science — Fargo's second approval election](https://electionscience.org/commentary-analysis/fargos-second-approval-voting-election-runs-smoothly/)
- [AP: North Dakota governor signs bill ending Fargo's voting system (April 2025)](https://apnews.com/article/fargo-north-dakota-legislature-voting-elections-8f85df3e17bf77fd7af41693569831ac)
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

## Related local material

- [glossary.md](glossary.md) — all terms above are indexed there
- [rcv-and-core-support](rcv-and-core-support.md) — the cardinal-vs-ordinal argument approval sits inside
- [legrand-ranked-ballot-methods](legrand-ranked-ballot-methods.md) — the ranked-only site whose author
  prefers approval to everything on it
- [hare-center-squeeze-examples](hare-center-squeeze-examples.md) — the failure mode approval is immune to
- [lumen-75-ballot-four-winners](lumen-75-ballot-four-winners.md) — cutoff indeterminacy worked on a ranked
  profile, and a textbook that mistakes one stipulated cutoff for the method
- [star-voting](star-voting.md) — the six-level end of the same family, with worked criterion failures
