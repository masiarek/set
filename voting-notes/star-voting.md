# STAR Voting

Source: [STAR voting (Wikipedia)](https://en.wikipedia.org/wiki/STAR_voting) — read 2026-08-01

Every number below is checked by [`code/star-voting/verify.py`](code/star-voting/verify.py) (no
dependencies, `python3 verify.py`). Two of the article's own figures don't survive that check; see below.

## What it's about

**S**core **T**hen **A**utomatic **R**unoff. Score every candidate 0–5. Sum the scores, take the top two,
then elect whichever of those two is scored higher on more ballots. One ballot, two rounds, no eliminations.

The design is a **reaction to score voting's strategy problem**. Under plain score, the optimal play is
almost always to min-max — 5 for your side, 0 for everyone else — because every point you give a rival
counts directly against your favorite. The runoff is meant to defuse that: in round 2 only the *order* of
your two finalists matters, so a 5-vs-4 ballot and a 5-vs-0 ballot count exactly the same. Exaggeration buys
you nothing at the decisive step. But scores still decide *who reaches* that step, so honest intermediate
scores still do work in round 1.

That is the whole method, and its whole tension: round 1 is cardinal and round 2 is ordinal, and the two
rounds reward different things.

## A caveat about the source

Unusually for these notes, the article is weak and says so. It carries a **"third-party sources needed"
banner (April 2024)**; a large share of the citations are to the Equal Vote Coalition and starvoting.org —
the advocacy organisations that invented and promote the method — and two of the compliance claims (mutual
majority, reversal symmetry) are tagged citation-needed as of July 2026. The mechanics and the adoption
record are solid and checkable. The criteria section is a list of assertions with almost no worked examples,
which is why I built my own below rather than repeating it.

## Key takeaways

### Mechanics

- **Ballot**: 0–5 stars per candidate, six levels. Equal scores allowed and expected; skipped candidates
  count as 0.
- **Round 1 (score)**: sum all scores, take the two highest.
- **Round 2 (automatic runoff)**: each ballot counts as one vote for whichever finalist it scored *higher*.
  Ballots scoring them equally count for neither — they abstain from the runoff. This is why an all-5s or
  all-0s ballot is nearly worthless, and why max-min strategy has a real cost.
- **Ties** (Equal Vote's published rules) resolve by going back to the ballots first: a scoring-round tie
  goes to whoever wins the head-to-head *between the tied candidates*; a runoff tie goes to the higher total
  score; only what survives both is a true tie decided by lot.

  This detail is not cosmetic. My first implementation broke a scoring tie against the score *leader*
  instead of between the tied candidates, and it manufactured a monotonicity violation that doesn't exist
  under the real rule. The verify script now implements the published rule and flags any result that needed
  a coin flip, so nothing below is an artifact of tiebreaking.

### Origin and adoption

- Proposed **October 2014 by Mark Frohnmayer** as **Score Runoff Voting (SRV)**, renamed STAR. Promoted by
  the **Equal Vote Coalition** — the same organisation behind Ranked Robin (2021) and
  [bettervoting.com](https://bettervoting.com).
- **No public government election has ever adopted it.** Both public ballot measures failed:
  - **Lane County, Oregon, Measure 20-290 (Nov 2018)** — over 16,000 petition signatures got it on the
    ballot; it lost **74,408 yes to 82,157 no**. That is **47.53%** yes, not the 47.6% the article states
    (checked). Eugene, inside the county, voted 54% yes.
  - **Oakridge, Oregon (Nov 2024)** — city council voted 5–1 to refer it; the measure would have run three
    elections under STAR then held a permanent-adoption vote. **Failed at 46%.**
  - A 2020 Eugene measure died before reaching voters: the city council deadlocked 4–4 on referral and
    **Mayor Lucy Vinis cast the deciding vote against**.
- **Organisational use, all in Oregon**: Multnomah County Democrats (2019, internal elections), Independent
  Party of Oregon (2020 primary — having abandoned *approval* after its 2016 primary produced no nominee),
  Democratic Party of Oregon (2020 convention delegates), Libertarian Party of Oregon (authorised 2022, from
  2023).

  So the honest summary is: a decade old, real institutional use, geographically concentrated in one state,
  and zero public elections. That is a weaker record than approval's — which at least got Fargo and
  St. Louis, even if [North Dakota then banned it](approval-voting.md).

### What it satisfies and what it doesn't

**Passes**: monotonicity in the mono-raise sense (raising a candidate's score never hurts them), and
resolvability.

**Fails**: majority, mutual majority, Condorcet, clone independence, participation, consistency, reversal
symmetry, later-no-harm, and favorite betrayal.

That is a long failure list, and Equal Vote's response is not to dispute it but to reject the framing. Their
"Farewell to Pass/Fail" argument is that it is "better for a system to fail two opposing criteria" and
thereby soften both, than to pass one absolutely. Later-no-harm and favorite betrayal are the opposing pair:

- A method that fully passes **later-no-harm** (IRV) can safely ignore your backup preferences — which is
  precisely how center squeeze happens.
- A method that fully passes **favorite betrayal** (approval) makes your top score cheap and pushes you
  toward bullet voting.

STAR fails both partially. Whether "fails two criteria a little" beats "passes one and fails its opposite
badly" is a values question, not a theorem — but it is a coherent position, and it is the actual argument.

## Worked example 1 — Tennessee, and a slip in the article's own table

Standard electorate: Memphis 42%, Nashville 26%, Chattanooga 15%, Knoxville 17%. Scores as the article
prints them (row = candidate, column = voter bloc):

| Candidate | Memphis (42) | Nashville (26) | Chattanooga (15) | Knoxville (17) | Total |
|---|---|---|---|---|---|
| Memphis | 5 | 0 | 0 | 0 | **210** |
| Nashville | 2 | 5 | 3 | 2 | **293** |
| Chattanooga | 1 | 2 | 5 | 4 | **237** |
| Knoxville | 0 | 1 | 3 | 5 | **156** |

Finalists Nashville (293) and Chattanooga (237). Runoff: Memphis and Nashville voters both score Nashville
higher (2>1 and 5>2), Chattanooga and Knoxville voters both score Chattanooga higher — **Nashville 68,
Chattanooga 32**. Nashville wins, and Nashville is the real capital and the Condorcet winner.

**One cell doesn't follow the article's own rule.** It states the rule — 5 for your home city, 0 for the
farthest, the rest "proportional to their relative distance" — and hides the mileage table in an HTML
comment. Applying that rule with round-half-up reproduces fifteen of the sixteen cells exactly. The
sixteenth doesn't: Knoxville voters' score for Nashville is printed as **2**, but

    5 × (1 − 159.5 / 345.1) = 2.689 → 3

and every other borderline cell rounds that way (Nashville voters give Knoxville 0.89 → 1; Chattanooga
voters give Nashville 2.85 → 3).

**Why — it's double rounding, not a typo.** The [score voting article](score-voting.md) carries the same
example on a 0–10 scale, and *this table is that one halved with round-half-to-even*. All sixteen cells match
under that rule, including the two that otherwise look arbitrary:

| | 0–10 | halved | round-half-to-even | printed here |
|---|---|---|---|---|
| Knoxville → Nashville | 5 | 2.5 | **2** | 2 |
| Knoxville → Chattanooga | 7 | 3.5 | **4** | 4 |

So the chain is `5.378 → 5 → 2.5 → 2`, where deriving 0–5 straight from the distances gives `2.689 → 3`.
The one discrepant cell is the only one where the two routes straddle a boundary differently. The lesson is
the useful part: **don't rescale a rounded table, rescale the source.**

**It changes nothing here.** Derived directly, Nashville's total goes 293 → 310, the finalists are still
Nashville and Chattanooga, and the runoff is still 68–32. But the totals column is exactly what a tabulator
test would assert on, so it matters to anyone reusing this table as fixture data.

**Same ballots, six methods** (all verified):

| Method | Winner |
|---|---|
| First-past-the-post | Memphis (42%) — the Condorcet loser |
| IRV | Knoxville — centre candidates eliminated first |
| Score | Nashville |
| Approval (top two) | Nashville, 68 |
| Two-round runoff | Nashville |
| **STAR** | **Nashville** |

This is the example STAR advocates lead with, and it is a fair one — but note that on this profile STAR
agrees with score, approval and plain runoff. It doesn't distinguish itself here; it just avoids being
plurality or IRV.

## Worked example 2 — one profile, three failures

The article asserts the majority and clone failures with no example. Here is one I built and verified; it
demonstrates majority, Condorcet **and** clone independence failing simultaneously. 100 voters:

| Voters | A1 | A2 | B |
|---|---|---|---|
| 48 | 5 | 5 | 0 |
| 52 | 2 | 1 | 3 |

Totals: **A1 344, A2 292, B 156.** Finalists A1 and A2. Runoff: the 52 prefer A1 (2>1), the 48 are
indifferent (5=5) — **A1 wins**.

What just happened:

- **Majority criterion fails.** B is the strict top choice of 52 of 100 voters — an absolute majority — and
  never even reaches the runoff. B's supporters like B only mildly (3 of 5); A1's supporters adore A1. STAR
  reads intensity, and here intensity outvotes a majority.
- **Condorcet fails.** B beats A1 head-to-head 52–48 and beats A2 52–48. B is the Condorcet winner and
  finishes third.
- **Clone independence fails.** Delete A2 — a clone of A1, adjacent to it on every ballot — and the
  two-candidate race is A1 344 vs B 156, runoff **B wins 52–48**. Adding a clone of the front-runner flips
  the winner from B to A1.

The clone mechanism is the one the article names in passing and worth stating plainly: **clones don't split
the vote in STAR, they occupy the runoff.** Two near-identical candidates can take both finalist slots and
lock everyone else out, at which point the runoff is a formality among allies. That is the mirror image of
Borda's clone problem — under Borda running extra candidates wins by inflating your score, under STAR it
wins by monopolising the runoff.

## Worked example 3 — failing later-no-harm and favorite betrayal, verified

**Later-no-harm.** 100 voters; the 45-bloc prefers A > B > C:

| Voters | A | B | C |
|---|---|---|---|
| 45 | 5 | **4** | 0 |
| 45 | 1 | 3 | 5 |
| 10 | 3 | 5 | 0 |

Totals A 300, B 365, C 225 → finalists B and A → runoff **B wins 55–45**.

Now the 45-bloc gives B **0** instead of 4, changing nothing else. Totals A 300, B 185, C 225 → finalists A
and C → runoff **A wins 55–45**. They get their favorite.

So honestly recording "I like B more than C" cost that bloc the win. Their B score lifted B past C into the
runoff, and B then beat their own favorite. That is later-no-harm failing, and it is the price of the
runoff round reading scores from round 1.

**Favorite betrayal.** The harder claim, because in STAR you can usually protect yourself by *equal-rating*
— scoring your favorite and your compromise both 5 — which is not betrayal. A genuine violation needs a case
where equal-rating is not enough. Found by exhaustive search over all 216 possible ballots for the
manipulating bloc:

| Voters | A | B | C |
|---|---|---|---|
| 48 | 5 | 2 | 4 |
| 52 | 1 | 5 | 0 |
| 8 | 0 | 2 | 3 |

Sincerely: A 292, B 372, C 216 → finalists B and A → **B wins 60–48**. The 48-bloc gets B, worth 2 to them.

Their problem: their favorite A is strong enough to take the second slot but loses the runoff to B. As long
as A is in the runoff, B wins. They would rather have C (worth 4).

Every ballot that keeps A at or tied for the top — including A=5, C=5 — is worth exactly **2**. Sinking A
below C and bullet-voting C (A=0, B=0, C=5) gives A 52, B 276, C 264 → finalists B and C → runoff **C wins
56–52**, worth **4**. The bloc must abandon its own favorite to do better; nothing loyal works.

That is favorite betrayal proper, and the mechanism is specific to STAR: your favorite can be *too strong in
round 1* and cost you round 2 by crowding out a compromise who would have won.

## Monotonicity: passes the usual one, fails a neighbour

Raising a candidate's score never hurts them — no violation turned up in **196,699** random clean
three-candidate profiles.

But Woodall's **mono-raise-delete** fails, and the verify script finds a case:

| Voters | A | B | C |
|---|---|---|---|
| 5 | 5 | 1 | 1 |
| 53 | 3 | 2 | 1 |
| 46 | 0 | 3 | 4 |

Totals A 184, B 249, C 242 → finalists B and C → **B wins 53–46**.

Now the 46-bloc raises B to 5 and drops everyone now below B to 0 (`A=0, B=5, C=0`) — the natural "I'm going
all-in on B" ballot. Totals A 184, B 341, C 58 → finalists B and **A** → runoff **A wins 58–46**. B loses.

Raising B didn't hurt B; **zeroing C did**, by knocking C out of the runoff and replacing it with A, who
beats B. Exactly the mechanism Woodall's footnote describes. The practical lesson is the useful part: in
STAR, the strategically dangerous act is not scoring your favorite too low, it's **scoring everyone else
0** — you may delete the very opponent your favorite could have beaten.

## What the runoff costs: participation

The usual framing is that STAR strictly improves on plain score. It doesn't — the runoff is a trade, and
participation is part of the price. Plain score satisfies participation; STAR fails it:

| Voters | A | B | C |
|---|---|---|---|
| 44 | 2 | 3 | 2 |
| 20 | 4 | 1 | 5 |
| **11** | **1** | **3** | **5** |

Without the last 11: totals A 168, B 152, C 188 → finalists C and A → **C wins**.
With them: A 179, B 185, C 243 → finalists C and **B** → **B wins 44–31**.

Those 11 voters score C at 5 and B at 3. **By showing up they replaced their favourite with their second
choice** — staying home would have served them better. Same mechanism as the later-no-harm failure above:
their B=3 lifted B past A into the runoff, where B beat C.

Plain score also keeps monotonicity *and* IIA, both of which STAR loses. Set against what STAR buys —
resistance to min-maxing — the ledger is genuinely two-sided. Details in [score-voting](score-voting.md).

## Equal Vote ships two methods, and they disagree

Equal Vote promotes STAR (2014) and Ranked Robin (2021). On the same ballots these are not interchangeable.

The clone profile from example 2 is a case in point: **STAR elects A1, Ranked Robin elects B** — and B is
the Condorcet winner and the strict favourite of an absolute majority. Across 58,952 random three-candidate
profiles the two methods **disagree 3.1% of the time**, and STAR fails to elect an existing Condorcet winner
in **1.6%** of the profiles that have one.

Both readings are fair:

- **For STAR**: 3.1% is small — they agree 97% of the time. The disagreements need an intensity gap wide
  enough to override a pairwise majority, and STAR's advocates argue that override is the *point*, in the
  same terms Brams uses for approval. If you think an intense minority should sometimes beat a mild
  majority, this is the feature working, and rarely.
- **Against**: the disagreement isn't noise, it is **systematically the Condorcet winner losing** — and
  Equal Vote's other method exists to guarantee that never happens. Shipping both means shipping two answers
  to "can a pairwise majority lose?", a values question, presented as a choice of implementation.

Caveat on the percentages: three random blocs with uniform random scores is a crude model, good for showing
the disagreement is common enough to meet in practice, not for estimating its real-world rate. The spatial
votesim harness in [ranked-robin-vse-run](ranked-robin-vse-run.md) is the right tool, and putting STAR
through it is the obvious next job.

## How it sits against the rest of these notes

- **vs. [score voting](score-voting.md)** — STAR is score plus a runoff, and the runoff is why: honest score
  elects the Condorcet winner on Tennessee, min-maxed score elects the Condorcet *loser* on the same
  preferences. That failure mode is STAR's entire reason for existing. What it costs is participation, IIA,
  and monotonicity's neighbour, all of which plain score keeps.
- **vs. [approval](approval-voting.md)** — the same family, one bit vs. six levels. Approval passes sincere
  favorite outright and fails later-no-harm absolutely; STAR fails both partially and calls that an
  improvement. Approval's open question is *where do I put my cutoff*; STAR's is *how do I spend my middle
  scores*. The Independent Party of Oregon walked this exact path in 2020, approval → STAR, which is the
  single best piece of evidence either way and it points at STAR.
- **vs. [Ranked Robin](ranked-robin-results-explained.md)** — Equal Vote's other method, quantified in the
  section above: Ranked Robin elects the Condorcet winner unconditionally from the pairwise matrix, STAR can
  leave them out of the runoff entirely.
- **vs. [IRV/Hare](hare-center-squeeze-examples.md)** — STAR's headline claim. On Tennessee, IRV elects
  Knoxville and STAR elects Nashville. STAR has no eliminations, so no ballot's information is ever
  discarded mid-count, and centre candidates can't be squeezed out on first preferences. What STAR
  substitutes is a different squeeze: you must survive the *score* round, where clones and intensity decide.
- **vs. [Borda](legrand-ranked-ballot-methods.md)** — both are clone-vulnerable, for opposite reasons.
  Borda rewards flooding the field; STAR rewards flooding the *top* of the field.

## New ideas and terms

- **Score Then Automatic Runoff** — score round picks two finalists, runoff round picks between them on
  preference order alone. One ballot, one election.
- **Automatic runoff** — round 2. Each ballot is one vote for the higher-scored finalist; equal scores
  abstain. The step that makes exaggeration pointless at the decisive moment.
- **Score Runoff Voting (SRV)** — STAR's original 2014 name.
- **Tactical maximisation / min-maxing** — scoring only 5s and 0s under score voting. The specific problem
  the runoff was added to solve.
- **Runoff abstention** — scoring two finalists equally removes you from the runoff. The hidden cost of
  equal-rating, and why all-5s ballots are near-worthless.
- **Runoff monopolisation** — STAR's clone failure: near-identical candidates take both finalist slots and
  lock out everyone else. Distinct from vote-splitting.
- **mono-raise vs. mono-raise-delete** — STAR passes the first (raising a candidate can't hurt them) and
  fails the second (raising them *while zeroing everyone below* can). The danger is in the deletion.
- **"Farewell to Pass/Fail"** — Equal Vote's argument that failing two opposing criteria mildly beats
  passing one and failing its opposite badly. The method's actual defence against its long failure list.
- **Later-no-harm / favorite betrayal as an opposing pair** — the two criteria STAR deliberately splits the
  difference on; IRV passes the first, approval the second.

## Links referenced in the article

- [STAR Voting](https://www.starvoting.org/) · [Equal Vote Coalition](https://www.equal.vote/) ·
  [bettervoting.com](https://bettervoting.com/)
- [How are ties in STAR Voting broken?](https://www.starvoting.org/ties) — the tiebreak rules implemented in
  the verify script
- ["Farewell to Pass/Fail"](https://www.starvoting.org/pass_fail) — the criteria-failure defence
- [Woodall, "Monotonicity and Single-Seat Election Rules", *Voting matters* 6 (1996)](http://www.votingmatters.org.uk/ISSUE6/P4.HTM)
  — the mono-raise / mono-raise-delete distinction
- [LWV of Washington, "A Review of Various Election Methods" (2020)](https://lwvwa.org/resources/Documents/Review%20of%20Election%20Methods%202-12-20.pdf)
  — the article's one non-advocacy source for the majority-criterion failure
- ["Score Runoff Voting" (IVN, 2016)](https://ivn.us/2016/12/08/score-runoff-voting/) — Frohnmayer's
  original pitch
- [Lane County 2018 official results (PDF)](https://apps.lanecounty.org/currentelection/20181106_Results.pdf)
- [Oakridge 2024 measure results](https://www.ci.oakridge.or.us/city-council-candidates-2024/page/2024-city-council-ballot-measures-election-results)
- [Highest median voting rules](https://en.wikipedia.org/wiki/Highest_median_voting_rules) — the median-based
  cousin, written up in [majority-judgment](majority-judgment.md): the other way to stop exaggeration
  paying, and it costs participation too

## Related local material

- [`code/star-voting/verify.py`](code/star-voting/verify.py) — every claim above, checked
- [score-voting](score-voting.md) — what STAR is built on, what the runoff fixes, and what it costs
- [approval-voting](approval-voting.md) — the one-bit end of the same family
- [ranked-robin-results-explained](ranked-robin-results-explained.md),
  [ranked-robin-origins](ranked-robin-origins.md) — Equal Vote's other method, and its Condorcet guarantee
- [rcv-and-core-support](rcv-and-core-support.md) — Ogren's cardinal argument, built on 0–5 star ballots
- [hare-center-squeeze-examples](hare-center-squeeze-examples.md) — the failure STAR is sold against
- `Voting 2021 mbair/` — the local STAR tabulator project
