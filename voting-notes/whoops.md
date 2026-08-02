# Election whoops

An index of the things that went wrong, collected from across these notes. Two kinds: **elections that
misfired** in public, and **errors in the sources** found while checking them. Nothing here is new — every
entry links to the note that works it out and, where there is one, the verifier that proves it.

The reason to keep this list is not schadenfreude alone. Almost every worthwhile example in voting theory is
a whoops: the methods only visibly differ when something goes wrong, so the failures *are* the curriculum.

---

## Part 1 — elections that misfired

| What happened | Where | Note |
|---|---|---|
| **Condorcet winner eliminated first.** Nick Begich beat both rivals head-to-head; IRV dropped him in round 1 and Peltola won. The textbook centre squeeze, in a real federal election. | Alaska special, Aug 2022 | [rcv-and-core-support](rcv-and-core-support.md) |
| **The wrong two advanced.** Le Pen reached the runoff on 16.9% and lost it 82.2–17.8. An in-precinct approval experiment run the same day would have advanced Chirac and Jospin instead. | France, presidential, 2002 | [approval-voting](approval-voting.md) |
| **A six-way split elected a 22% winner** — the race that convinced Fargo to adopt approval voting in the first place. | Fargo ND commission, 2015 | [approval-voting](approval-voting.md) |
| **The primary produced no nominee.** Approval voting, and nobody cleared 32%. The party abandoned approval for STAR four years later. | Independent Party of Oregon presidential preference, 2016 | [approval-voting](approval-voting.md), [star-voting](star-voting.md) |
| **Approval degenerated into plurality.** Winners kept landing under 40% (41% in 2011, 32% in 2012) and over 80% of voters approved exactly one candidate in 2014 and 2016. Students dropped it before 2017. | Dartmouth student body president, 2011–2016 | [approval-voting](approval-voting.md) |
| **Adopted, then abandoned.** IEEE rescinded approval in 2002 — the stated reason was that few members used it. Dartmouth's alumni reverted to runoffs 82–18 in 2009. | IEEE 2002, Dartmouth 2009 | [approval-voting](approval-voting.md) |
| **Reform banned by the state.** Fargo ran two approval elections, then North Dakota outlawed both approval and RCV statewide in April 2025. A 2023 attempt had been vetoed and survived an override. | North Dakota, 2023 & 2025 | [approval-voting](approval-voting.md) |
| **Both public STAR measures lost**, ten years apart — Lane County 2018 at 47.5%, Oakridge 2024 at 46% — and a 2020 Eugene referral died on the mayor's tiebreaking vote. No public election has ever used STAR. | Oregon, 2018–2024 | [star-voting](star-voting.md) |
| **A gen-ed textbook's own homework exercise** eliminates the Condorcet winner by one vote under IRV, is non-monotonic, rewards favorite betrayal by the winner's own supporters, and contains two spoilers. The module notices none of it. | Lumen Learning, *Voting Theory* | [lumen-75-ballot-four-winners](lumen-75-ballot-four-winners.md) |

## Part 2 — errors in the sources

Found by recomputing rather than by reading. Where a note has a verifier, the error is asserted in code.

| The error | Source | Consequence | Note |
|---|---|---|---|
| **Double-rounded score table.** The 0–5 Tennessee table is the score article's 0–10 table halved with round-half-to-even, so `5.378 → 5 → 2.5 → 2` where deriving 0–5 from the distances gives `2.689 → 3`. One cell off. | STAR voting (Wikipedia) | Winner unchanged (Nashville, 68–32), but the printed total 293 should be 310 — and totals are what a tabulator test asserts on | [star-voting](star-voting.md) |
| **The lead and the worked example use different rules.** "Highest *average* score" in sentence one; the example computes *totals*. They diverge as soon as any ballot has a blank, and can elect different winners. | Score voting (Wikipedia) | The article's own example can't expose it — all 100 voters rate all 4 cities | [score-voting](score-voting.md) |
| **The same historical elections claimed by two method articles.** Venice, Greece 1864–1923, Sweden, the UN and Latvia appear as *approval* on one page and *score* on the other, sometimes citing the same page of the same source. | Approval vs. Score (Wikipedia) | Read "X used our method" as a claim about rated methods generally | [score-voting](score-voting.md) |
| **Percentage doesn't match the count.** Lane County Measure 20-290 is 74,408 to 82,157 = 47.53%, printed as 47.6%. | STAR voting (Wikipedia) | Cosmetic | [star-voting](star-voting.md) |
| **A load-bearing clause that reads like a throwaway.** The Tennessee grading rule has two parts — mileage bands, *and* "the farthest city gets Poor". Apply only the bands and Nashville voters grade Memphis *fair* instead of *poor* (194.2 miles, boundary at 200). | Majority judgment (Wikipedia) | MJ then elects **Memphis, the Condorcet loser**, 42 fair+ beating Nashville's 26 fair+ | [majority-judgment](majority-judgment.md) |
| **Criteria asserted with no examples, and partly uncited** — mutual majority and reversal symmetry tagged citation-needed; the whole Properties section of the score article has no citations; both articles lean on the advocacy organisations that invented the methods. | STAR & Score (Wikipedia) | The failures had to be constructed locally to check them | [star-voting](star-voting.md), [score-voting](score-voting.md) |
| **Showcase images fail a zero-sum sanity check** — both the 3-cycle and 5-cycle diagrams in the origin thread. | Ranked Robin origin thread | Winners survive correction | [ranked-robin-origins](ranked-robin-origins.md) |
| **Four claims nobody had ever run numbers against**, including "adding a weak candidate changes nothing" (true only for candidates who lose *every* matchup) and a "best average rank" one-liner that elects the other candidate under either convention it fails to state. | Ranked Robin origin thread | A 2%-of-first-preferences candidate flips the winner | [ranked-robin-thread-claims-checked](ranked-robin-thread-claims-checked.md) |
| **Not the method it's named after.** LeGrand's "Dodgson" is the smallest sum of defeat margins; classical Dodgson is fewest adjacent ballot swaps, and is NP-hard. The site's rule is a cheap approximation. | LeGrand, *Ranked-ballot voting methods* | Different winners in general | [legrand-ranked-ballot-methods](legrand-ranked-ballot-methods.md) |
| **A results page that reads as nonsense.** 12 ballots reported as "1 win" — Copeland matchup wins presented where readers expect ballot counts, with a 50% bar meaning half the *matchups*. | BetterVoting results UI | Since fixed | [ranked-robin-results-explained](ranked-robin-results-explained.md) |
| **A logging flag decided the winner.** The whole ballot-allocation block in `sequentially_spent_score()` sat inside `if options.verbosity:`, so at `verbosity=0` no stars were ever spent. | `starvote` 2.1.6 (Larry Hastings) | **SSS silently degenerated into Bloc Score** — verified identical — and a 38% minority bloc lost the seat it was owed: `['Alice','Ben','Cara']` instead of `['Alice','Ben','Dan']`. Fixed in the fork with a verbosity-invariance regression test; [open upstream](https://github.com/larryhastings/starvote/issues/17) | [sequentially-spent-score](sequentially-spent-score.md) |
| **A counterexample inherited from a variant the same page says was abandoned.** "Only Bs are elected" on the 41/20/41 centrist-bias profile is a **capping**-variant result; under the current **scaling** variant the centre bloc takes 3 of 5 seats, not 5. | electowiki, *Sequentially Spent Score* | The bias is real either way — a 0.98-seat entitlement taking 3 seats is still ~3x over-representation — but it is 3x, not 5x, so the case for the Sorted Surplus variant is weaker than the page makes it look | [sequentially-spent-score](sequentially-spent-score.md) |
| **Round-2 totals that the stated procedure doesn't produce.** The participation example prints A = 100.66 and A = 98.36; recomputing exactly gives **101.60** and **98.22**. Both drop the one-star voters' surviving contribution to the second A clone. | electowiki, *Sequentially Spent Score* | **No effect on the finding** — the inequality goes the same way in both cases and SSS does fail participation. But they are the numbers a reader would reuse | [sequentially-spent-score](sequentially-spent-score.md) |
| **Arrow's theorem stated without the word "ranked."** "It is not possible for a voting method to satisfy every fairness criteria that we've discussed" — and the criteria named aren't Arrow's conditions either. | *Math in Society* §2.12 (Lippman/LibreTexts) | **Approval voting is introduced on the next page.** The chapter appears to condemn a method the theorem's hypothesis never reached. Still live on the page | [math-in-society-lippman](math-in-society-lippman.md) |
| **The same fact over-applied the other way.** The ordinal restriction stated *correctly*, then used to infer that "several cardinal systems meet all these criteria," naming score voting and majority judgment. Neither is a function on Arrow's domain — the same orderings admit honest ballots with different winners — and the IIA they do satisfy holds only under absolute rating: let voters normalise and score breaks it on **13.4%** of random profiles, MJ on **14.9%**. | electowiki, *Cardinal voting systems* | **The mirror image of the row above.** The page's own Criticism section states the refutation (voters "may normalize to different scales"; Balinski–Laraki's "common language") and never joins it up. Sen's Thm 8\*2 is the missing citation: cardinal measurability without interpersonal comparability leaves the impossibility intact | [cardinal-voting-systems](cardinal-voting-systems.md) |
| **Balinski–Young overclaimed, and refuted by Balinski and Young.** Stated as ruling out "the Alabama, New States, or Population paradoxes" for any quota-following method; the theorem is quota + *population* monotonicity. Quota + house monotonicity is achievable — B&Y's own Quota method (1975) does it. | *Math in Society* §4.4 (Lippman/LibreTexts) | Refuted by the book's **own exercise 9**: (4,4,2)→(5,4,2) satisfies quota at ten and eleven seats and takes nothing from anyone | [math-in-society-lippman](math-in-society-lippman.md) |
| **A tightness witness that isn't continuous.** Appendix B argues Example 8 satisfies continuity because "the most-frequent ballots in *P* become the most-frequent ballots in *P′* + *kP* for large enough *k*." They can instead shrink to a *proper subset*: with P = 2{a}+2{a,b} and Q = {a,b}, f(P) = {a} but f(Q+kP) = {a,b} for every k. | Brandl & Peters, *JET* 205 (2022) | **No theorem affected.** It costs Example 8 one of its two cited roles — it can't witness Thm 5, which has a continuity axiom — and Ex 6 witnesses that cell instead | [brandl-peters-approval-characterizations](brandl-peters-approval-characterizations.md) |
| **A criterion failure manufactured by an assumption.** Approval "very easily violates the Majority Criterion" — demonstrated by *supposing* every voter approves their top two. Bullet-vote the same profile and approval elects the majority winner; approve-all and there's no winner at all. | *Math in Society* §2.14 (Lippman/LibreTexts) | The cutoff, not the tabulation, is doing all the work — the [approval](approval-voting.md) indeterminacy finding, in a textbook that doesn't notice | [math-in-society-lippman](math-in-society-lippman.md) |
| **A weighted-voting example that drops a sitting member.** The 2007 Scottish Parliament given as `[65: 47,46,17,16,2]`, total 128; the parliament has 129 — one independent is missing. | *Math in Society* §3.4 (Lippman/LibreTexts) | The lesson survives (LibDems and Greens still tie), but the dropped member is **not a dummy** — 1/28 ≈ 3.6% of the Banzhaf power, in a chapter about who has none | [math-in-society-lippman](math-in-society-lippman.md) |
| **A bloc of 132 spent 165 times.** "Of the 132 big taxers, 99 approve of both *x* and *y*; and 66 approve of *x* and *z*." The printed totals 232/296/293 reproduce only from 165, so the worked election runs on a 459-member House. | Horn, *Three Unique Virtues of Approval Voting* §III (Qeios, peer-approved) | Winner unchanged, but the "very narrow victory" of **3 votes** that the section's own hedge is built on is really **36 or 69** | [horn-three-virtues-approval](horn-three-virtues-approval.md) |
| **Four ballots the paper's own inference rule forbids.** §II.B says approving X and not Y entails X > Y. The 66 big taxers rank *x > y > z* and approve {*x*, *z*}; and one cell in every row of the §IV table is {favourite, worst}, skipping the middle. | Horn, *Three Unique Virtues* §§III–IV | Those 66 approvals are the whole of *z*'s near-win; and footnote 20's **12 scenarios become 4** once the forbidden cells go — 1 win, 3 ties, 0 losses | [horn-three-virtues-approval](horn-three-virtues-approval.md) |
| **A "generalizable" result in which the largest total loses.** "*Ax* … is greater than either *Ay* or *Az*; and (*Ay* + *Az*) is greater than *Ax*, then *y* will prevail." Approval elects the argmax. Exhaustive search to 40 finds zero satisfying triples; (2, 1, 2) kills the disjunctive reading too. | Horn, *Three Unique Virtues* §III | The example offered as an instance doesn't satisfy the antecedent either — *Ax* = 232 is the **smallest** of the three totals | [horn-three-virtues-approval](horn-three-virtues-approval.md) |
| **An impossibility claim refuted two paragraphs above it.** "Such distortions of democracy cannot occur under AV" — against the author's own "a very small change in the breakdown … would flip it, allowing for the status quo to again prevail." | Horn, *Three Unique Virtues* §III | Enumerating all 32 sincere Rule-(1) cutoff profiles on the paper's own ballots elects the **status quo in 3 and the Condorcet loser in 5**, against a 77% majority for change — no strategy, no agenda. The [approval](approval-voting.md) cutoff indeterminacy again, in the paper that denies it | [horn-three-virtues-approval](horn-three-virtues-approval.md) |
| **Arrow's theorem restated as "cycles are unavoidable"** under "every type of minimally democratic preferentist voting mechanism." | Horn, *Three Unique Virtues* §IV | Borda returns 3–3–3 on the standard cycle; ranked pairs and Schulze are transitive by construction. The intransitivity belongs to the **pairwise majority relation**, not to every ranked method — a **third** way to misread the same load-bearing fact, alongside the Lippman and electowiki rows above: not dropping the ordinal restriction, and not over-applying it, but confusing the theorem with the Condorcet paradox | [horn-three-virtues-approval](horn-three-virtues-approval.md) |
| **Two elimination rules that elect nobody.** Hare and Coombs are defined with "all of the poorly performing candidates will be removed in each round," and the fallback is "the remaining candidate(s) are declared the winners." On a perfect first-place tie there are none. | Pacuit, *Voting Methods* §2.1 (SEP, rev. 2019) | The definitions return **∅ on the entry's own Condorcet paradox profile** (`1 ABC, 1 BCA, 1 CAB`). Exhaustively over 5,004 three-candidate profiles with ≤9 voters, this is the *only* way Hare and Plurality-with-Runoff disagree — 501 profiles, all of them Hare electing nobody | [sep-voting-methods](sep-voting-methods.md) |
| **Runoff transfers stated backwards.** "The groups voting for candidates C and D transfer their support to candidates B and A, respectively." C's group ranks `C D A B` and D's ranks `D B C A`, so it is A and B respectively. | Pacuit, *Voting Methods* §2.1 | None — the printed 10–9 is right, because the same error is made twice. The example is the best in the entry: the same 19 ballots give three different winners across its three multi-stage methods | [sep-voting-methods](sep-voting-methods.md) |
| **A theorem stated with a redundant axiom.** May's Theorem given as neutrality + anonymity + **unanimity** + positive responsiveness; May 1952 uses three of those four. | Pacuit, *Voting Methods* §4.2 | Biconditional still true. Brute force over every neutral rule on anonymized two-candidate profiles, n = 3…6: exactly **one** rule survives without unanimity, and it is simple majority. Third source in these notes, third axiom list for the same theorem | [sep-voting-methods](sep-voting-methods.md) |
| **A theorem introduced as the generalisation of an example that doesn't instantiate it.** Fishburn's theorem needs some candidate *strictly* ahead of the Condorcet winner under every scoring rule; on Condorcet's 81 voters, 2-approval **ties** A and B at 70. | Pacuit, *Voting Methods* §3.1.1 | The theorem is true and the example is correct — they just don't meet. The smallest three-candidate witness takes **11 voters** (`2 ACB, 3 BAC, 2 BCA, 4 CBA`), verified by exhaustive search over every smaller electorate | [sep-voting-methods](sep-voting-methods.md) |
| **Ten dangling or wrong citations** in a survey whose main use is its bibliography — Chebotarev and "Smais" for Shamis, Young 1998 for the 1988 *APSR* paper, Nurmi 1998 and 1999 against a bibliography holding only 1987, and no entry at all for Ostrogorski 1902, Posner and Weyl 2018, Lalley and Weyl 2018b, or Bloembergen, Grossi and Lackner 2018. | Pacuit, *Voting Methods* (SEP) | Nothing mathematical. But the entry's job is to route readers to the literature, and Fabienne Peter is indexed under her given name with three different years across text, bibliography and URL | [sep-voting-methods](sep-voting-methods.md) |

## Part 3 — my own

Kept here because the notes are supposed to be checkable, and two of these were caught only by writing the
verifier.

- **A monotonicity violation that wasn't.** My first STAR implementation broke scoring-round ties against the
  score *leader* instead of between the tied candidates. Under Equal Vote's actual published rule the
  violation disappears. The verifiers now implement the published rule and flag any result that needed a
  coin flip. [star-voting](star-voting.md)
- **A favorite-betrayal example that didn't require betrayal.** The first search hit was really a
  bury-plus-equal-rate strategy with a demotion attached; equal-rating achieved the same result. The search
  now requires that *no* loyal ballot does as well. [star-voting](star-voting.md)
- **"The article has an error"** was too strong for the STAR score table. It's a double-rounding artifact
  inherited from rescaling the 0–10 table, which is a more useful diagnosis — and only visible once the
  score article was read. Corrected in place. [score-voting](score-voting.md)
- **Summarised a paper from its abstract.** I wrote that Brandl–Peters proves "consistency plus any one of
  strategyproofness, majority agreement, clone independence, or invariance under removing inferior
  alternatives forces approval." It doesn't: every one of the eight characterizations also needs housekeeping
  axioms — anonymity, neutrality, faithfulness, continuity, non-triviality — that vary by theorem, and the
  paper's Table 1 attaches a counterexample to each proving it undroppable. The abstract's four-item list is
  a summary of the *headline* axioms, and I read it as the full hypothesis. Caught only by reading the actual
  PDF. [brandl-peters-approval-characterizations](brandl-peters-approval-characterizations.md)
- **Two wrong guesses in the STV verifier**, both caught by the assertions rather than by me. I asserted that
  *S* candidates can always reach the Droop quota — false for small electorates (3 votes, 2 seats: quota 2,
  and 2×2 > 3); the theorem is only the upper bound plus minimality. And I predicted the 3-seat winners on
  the Lumen ballots would be Garcia/Nguyen/Smith; the real answer is Smith/Garcia/Lee, which turned out to be
  the better finding. [single-transferable-vote](single-transferable-vote.md)
- **Two bugs in the Horn verifier, caught by the paper being right.** I counted "prefers some increase to the
  status quo" as the blocs ranking *z* last, which misses the 130 who rank it second, and I built the
  strategic amendment tally by adding all 97 anti-taxers to everyone already preferring *x*, double-counting
  the 49. Both surfaced as failed assertions against Horn's own printed numbers — 229–197 and 227–199 are
  correct in the paper. The checks that matter cut both ways or they aren't checks.
  [horn-three-virtues-approval](horn-three-virtues-approval.md)

## What the pattern says

Five things recur often enough to be worth naming:

1. **Nearly every failure is a middle candidate problem.** Center squeeze, the clone taking a runoff slot,
   the majority favourite who never reaches round 2, majority judgment handing a left–right election to the
   larger wing instead of the centre — all are a broadly acceptable candidate losing to the structure of the
   count rather than to the voters. The methods disagree about almost nothing else.
2. **Adoption reverses more often than it sticks.** IEEE, Dartmouth twice, the Independent Party of Oregon,
   Fargo by state pre-emption. The interesting question is rarely "does the method work" but "does it
   survive its first few elections."
3. **The errors cluster where a source generalizes.** Not in the prose explaining what a method does, but in
   the worked example meant to demonstrate it and in the sentence afterwards saying what the example proves —
   a table, a diagram, a percentage, or a "thus, in general." Horn's paper has both halves in one section: a
   miscounted bloc, and then a stated generalization the example doesn't satisfy. Those are the parts readers
   skim and reuse. That's the argument for the verifiers.
4. **Tie rules decide real elections, and nobody writes them down.** Three separate times now: Ranked
   Robin's tie ladder, the STAR scoring-round tie I got wrong and then caught, and STV — where swapping a
   backward tiebreak for an alphabetical one makes one-seat STV and IRV disagree on 15 of 4,000 profiles.
   The tiebreak is usually a footnote in the spec and the deciding rule in the count.
5. **Refereeing reads arguments; it doesn't rerun examples.** The two peer-reviewed papers here carry the
   most checkable claims of anything in this folder, and both have errata found by recomputation: a *Journal
   of Economic Theory* tightness witness that fails the continuity it is argued to have, and a paper
   peer-approved by five reviewers at 3.40 whose worked election spends a 132-member bloc 165 times. Neither
   needed anything past arithmetic. Open review didn't obviously help either: Qeios publishes its reviews,
   and the platform's peer-approval statement for that paper praises all three virtues by name.

5. **Prose errors travel by inference, not by arithmetic.** The two Arrow entries above are the only
   findings here that no recomputation could have caught, and they are the same sentence over-applied in
   opposite directions — one textbook stretching the theorem past its hypothesis, one wiki treating the
   hypothesis as a licence. Both are load-bearing for a reader deciding whether cardinal ballots "solve"
   anything, and neither is in a table.

## Related

- [glossary.md](glossary.md) — every failure mode named here, defined
- All verifiers: [`code/`](code/)
