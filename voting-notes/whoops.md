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
| **Arrow's theorem stated without the word "ranked."** "It is not possible for a voting method to satisfy every fairness criteria that we've discussed" — and the criteria named aren't Arrow's conditions either. | *Math in Society* §2.12 (Lippman/LibreTexts) | **Approval voting is introduced on the next page.** The chapter appears to condemn a method the theorem's hypothesis never reached. Still live on the page | [math-in-society-lippman](math-in-society-lippman.md) |
| **Balinski–Young overclaimed, and refuted by Balinski and Young.** Stated as ruling out "the Alabama, New States, or Population paradoxes" for any quota-following method; the theorem is quota + *population* monotonicity. Quota + house monotonicity is achievable — B&Y's own Quota method (1975) does it. | *Math in Society* §4.4 (Lippman/LibreTexts) | Refuted by the book's **own exercise 9**: (4,4,2)→(5,4,2) satisfies quota at ten and eleven seats and takes nothing from anyone | [math-in-society-lippman](math-in-society-lippman.md) |
| **A criterion failure manufactured by an assumption.** Approval "very easily violates the Majority Criterion" — demonstrated by *supposing* every voter approves their top two. Bullet-vote the same profile and approval elects the majority winner; approve-all and there's no winner at all. | *Math in Society* §2.14 (Lippman/LibreTexts) | The cutoff, not the tabulation, is doing all the work — the [approval](approval-voting.md) indeterminacy finding, in a textbook that doesn't notice | [math-in-society-lippman](math-in-society-lippman.md) |
| **A weighted-voting example that drops a sitting member.** The 2007 Scottish Parliament given as `[65: 47,46,17,16,2]`, total 128; the parliament has 129 — one independent is missing. | *Math in Society* §3.4 (Lippman/LibreTexts) | The lesson survives (LibDems and Greens still tie), but the dropped member is **not a dummy** — 1/28 ≈ 3.6% of the Banzhaf power, in a chapter about who has none | [math-in-society-lippman](math-in-society-lippman.md) |

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
- **Two wrong guesses in the STV verifier**, both caught by the assertions rather than by me. I asserted that
  *S* candidates can always reach the Droop quota — false for small electorates (3 votes, 2 seats: quota 2,
  and 2×2 > 3); the theorem is only the upper bound plus minimality. And I predicted the 3-seat winners on
  the Lumen ballots would be Garcia/Nguyen/Smith; the real answer is Smith/Garcia/Lee, which turned out to be
  the better finding. [single-transferable-vote](single-transferable-vote.md)

## What the pattern says

Three things recur often enough to be worth naming:

1. **Nearly every failure is a middle candidate problem.** Center squeeze, the clone taking a runoff slot,
   the majority favourite who never reaches round 2, majority judgment handing a left–right election to the
   larger wing instead of the centre — all are a broadly acceptable candidate losing to the structure of the
   count rather than to the voters. The methods disagree about almost nothing else.
2. **Adoption reverses more often than it sticks.** IEEE, Dartmouth twice, the Independent Party of Oregon,
   Fargo by state pre-emption. The interesting question is rarely "does the method work" but "does it
   survive its first few elections."
3. **The errors cluster in worked examples, not prose.** Every source error above is in a table, a diagram,
   or a percentage — the parts readers skim and reuse. That's the argument for the verifiers.
4. **Tie rules decide real elections, and nobody writes them down.** Three separate times now: Ranked
   Robin's tie ladder, the STAR scoring-round tie I got wrong and then caught, and STV — where swapping a
   backward tiebreak for an alphabetical one makes one-seat STV and IRV disagree on 15 of 4,000 profiles.
   The tiebreak is usually a footnote in the spec and the deciding rule in the count.

## Related

- [glossary.md](glossary.md) — every failure mode named here, defined
- All verifiers: [`code/`](code/)
