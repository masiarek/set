# Three Unique Virtues of Approval Voting — Horn (2024)

Source: Walter Horn, "Three Unique Virtues of Approval Voting", [Qeios](https://www.qeios.com/read/ZETKEQ) —
read 2026-08-01. Two versions, both CC BY:

| Version | Date | DOI | Status |
|---|---|---|---|
| Preprint v1 | 7 Feb 2024 | [10.32388/ZETKEQ](https://doi.org/10.32388/ZETKEQ) | superseded |
| v1 (published) | 12 Mar 2024 | [10.32388/ZETKEQ.2](https://doi.org/10.32388/ZETKEQ.2) | **peer-approved**, 3.40 from 5 reviewers |

Also on [PhilArchive](https://philarchive.org/rec/HORTUV). 3,248 views and 1,005 downloads across both
versions as of the read date. The two versions are copy-edited apart — commas, "best known" → "best-known",
citation style — and **every arithmetic claim below is word-for-word identical in both**, so all of this
applies to the peer-approved version, not just to the preprint.

Verifier: [code/horn-three-virtues/verify.py](code/horn-three-virtues/verify.py) ·
output: [run-output.txt](code/horn-three-virtues/run-output.txt) — 48 checks, no dependencies, `python3 verify.py`.

## What it's about

A philosophy paper, not a social-choice paper, arguing that approval voting has three virtues its rivals
lack: it doesn't violate IIA, it can't be beaten by agenda-setting, and it escapes Condorcet cycles and
therefore Arrow. It is the first note here on a paper making a *case for* a method rather than describing
one, and it is worth reading for one genuinely good distinction and one very instructive collapse.

The good distinction is the paper's opening move, and it is the same point
[approval-voting](approval-voting.md) reaches from the empirical side. Horn writes out approval's rule twice:

> **Rule (1)** — vote for all and only those candidates you minimally approve of.
> **Rule (2)** — vote by making a mark next to as many candidate names as you like.

Both describe approval. Only Rule (1) constrains what the marks *mean*. Bullet voting your favourite
violates (1) and is perfectly consistent with (2). Horn then says explicitly that the whole paper assumes
Rule (1) compliance — an "arguably fantastic 'ideal world'" — and that whether real voters comply is an
empirical question he isn't addressing.

That is exactly right, and it is the cleanest statement of the thing this folder keeps running into: approval's
criterion compliance is a property of the voter model, not of the tabulation. It is also, unfortunately, the
whole argument. Under Rule (1) each voter's approval set is an *attitude* fixed before the field is known, so
it cannot respond to the field — and "cannot respond to the field" is what IIA asks for. Virtue 1 is the
assumption restated.

## The one-paragraph version

Virtue 1 is true by stipulation and not unique. Virtue 3 is true, well known, and not unique — every cardinal
method escapes Arrow for the same reason, because Arrow's theorem quantifies over ordinal rules. Virtue 2 is
argued from a worked example whose arithmetic doesn't hold: a bloc of 132 is spent 165 times, one of its
approval profiles contradicts the paper's own preference-to-approval rule, and the "generalizable" result
stated afterwards says that the option with the most approvals loses. And on the paper's own numbers, the
anti-democratic outcome it says approval makes impossible is reachable under approval with entirely sincere,
Rule-(1)-compliant ballots — no strategy, no agenda.

## Virtue 1 — IIA

Horn distinguishes three things that get called IIA, which is more care than most treatments take:

- **Arrow's Condition 3**, over ordinal social welfare functions. Approval isn't one, so the condition doesn't
  apply. Horn says a "reasonably constructed approval analogue" is satisfied under Rule (1) — correct, and
  trivially so, since Rule (1) makes each candidate's approval independent of the rest by definition.
- **IIA2** — the popular version, about adding or removing an alternative. Horn builds an approval analogue
  (IIA2\*) in three clauses and argues the counterexamples to it aren't really counterexamples, because a
  violation would have to be simultaneous to be irrational, and simultaneous means self-contradictory.
- **IIA2†** — a Sen-property-α-flavoured conditional: your approval of X shouldn't change when the option set
  grows or shrinks. Horn concedes approval violates this, and argues that violating it isn't irrational,
  using a Sophie's-choice thought experiment.

The concession is the interesting part, because footnote 14 then quotes Jack Nagel — whom the paper thanks in
its first footnote, and who wrote the standard critical paper on approval, "The Burr Dilemma in Approval
Voting" (2007) — objecting that failing IIA2† "sets up the possibility of manipulation through agenda
control—i.e., by adding or subtracting alternatives."

That objection is not answered anywhere in the paper. It is also fatal to the *next* virtue: section III
argues approval defeats agenda control, and section II has just conceded the one form of IIA whose failure
reopens it. Sequential-agenda control is blocked; alternative-set control is conceded in a footnote. The
paper's virtues 1 and 2 are load-bearing against each other.

Not unique, either. Score voting satisfies IIA under exactly the same condition — absolute scoring, ratings
fixed independently of the field — and fails it the moment voters renormalise, which is the finding already
recorded in [score-voting](score-voting.md). Approval is score restricted to {0, 1}; there is no additional
protection in the restriction.

## Virtue 2 — agenda-setting

This is the section with the numbers, so this is the section the verifier is for.

Horn takes Riker's presentation of the 1956 Powell Amendment, disclaims all its history, and reuses the
numbers as a stipulated tax vote: `x` = triple taxes, `y` = a 15% rise, `z` = no change.

| Bloc | n | Ranking |
|---|---|---|
| Big taxers | 132 | x > y > z |
| Pragmatists | 67 | y > x > z |
| Small taxers | 130 | y > z > x |
| Anti-taxers A | 49 | z > x > y |
| Anti-taxers B | 48 | z > y > x |

426 members. (The printed percentages are rounded to sum to 100; that is not one of the errors here. The
restatement paragraph does label the 130 bloc `yxz` when the list it restates says `yzx`, and collapses the
two anti-tax blocs into `zyx`, but nothing downstream depends on either.)

**The manipulation story checks out.** Vote the amendment first, then the survivor against the status quo.
Sincerely: `y` beats `x` 245–181, then `y` beats `z` 329–97. With the 97 anti-taxers voting for the amendment
they least want: `x` beats `y` 229–197, then `z` beats `x` 227–199. The status quo survives although 329 of
426 — 77%, which the paper calls "a plurality" — prefer some increase to none. Horn's setup is sound.

### The approval count spends the same bloc twice

> "of the 132 big taxers, 99 approve of both x and y; and 66 approve of x and z"

99 + 66 = 165. The bloc has 132 members. And the published totals are not a typo on top of a correct count —
they reproduce exactly from 165:

```
x = 99 + 66 + 67          = 232   ✓ as printed
y = 99 + 67 + 130         = 296   ✓ as printed
z =      66 + 130 + 97    = 293   ✓ as printed
```

The election is run on a 459-member House. Repair the bloc to its stated 132 and the winner doesn't change,
which is the good news for the paper:

| Big-taxer split | x | y | z | Result |
|---|---|---|---|---|
| As printed (165) | 232 | 296 | 293 | y by **3** |
| 99 {x,y} + 33 {x,z} | 199 | 296 | 260 | y by 36 |
| 99 {x,y} + 33 {x} | 199 | 296 | 227 | y by 69 |

What does change is the sentence built on it. Horn calls this "a very narrow victory" and warns that "a very
small change in the breakdown … would flip it". The narrowness is entirely manufactured by the 33 phantom
voters; the real margin is an order of magnitude larger. The paper's own hedge is an artefact.

### One approval profile contradicts the paper's own rule

Section II.B states the entailment the paper uses to move between preferences and approvals:

> if J approves X and does not approve Y, then J judges X > Y.

The 66 big taxers are stipulated as `x > y > z` and approve `{x, z}`. Approving `z` and not `y` entails
`z > y`; their ranking says `y > z`. The verifier audits all six stipulated (ranking, approval set) pairs and
this is the only one that breaks — and it is the one holding up `z`'s total. Without those 66 approvals `z`
falls to 227 and there is no narrow race to describe.

### The generalization is not a generalization

> "Ax (the number of approvals of x) is greater than either Ay or Az; and (Ay + Az) is greater than Ax, then
> y will prevail in a rule compliant AV election."

Approval elects the largest total. If `Ax > Ay` and `Ax > Az`, then `x` wins — by the definition of the
method. Exhaustive search over all triples up to 40 finds zero cases where the antecedent holds and `y` wins,
because there cannot be any. Reading "either … or" as inclusive disjunction doesn't save it: `(Ax, Ay, Az) =
(2, 1, 2)` satisfies the antecedent and elects `z`.

And the example it generalizes doesn't satisfy it under either reading — `Ax` = 232 is the *smallest* of the
three totals, not the largest. The only repair that makes the statement true is to require `Ay` to be the
largest, at which point it says approval elects the candidate with the most approvals.

### What actually defeats the manipulation is simultaneity

The comparison the section needs is sequential-agenda voting against one-shot approval. But the one-shot half
of that contrast has nothing to do with approval. On the same profile, voting on all three at once:

| Method | x | y | z | Winner |
|---|---|---|---|---|
| Plurality | 132 | 197 | 97 | y |
| Borda (2/1/0) | 380 | 574 | 324 | y |
| IRV | — | — | — | y |
| Pairwise majority | — | — | — | y (Condorcet winner) |

Every one of them elects the compromise. Even plurality — the method approval exists to replace — defeats
this manipulation, because the manipulation is a property of the *agenda*, not of the ballot. "Such
distortions of democracy cannot occur under AV" is true and would remain true with "AV" replaced by almost
anything, provided you stop holding sequential votes.

### The headline: the manipulators' outcome, on sincere ballots

Rule (1) fixes each voter's approval set as an attitude, but it says nothing about *where the cutoff falls* —
approving your favourite only and approving your top two are both Rule-(1)-compliant, both sincere, both
upper sets of the ranking. Enumerate every combination of sincere cutoffs across the five blocs — 32
profiles — and the answers are:

| Winner | Profiles | Example |
|---|---|---|
| y — the Condorcet winner | 24 of 32 | x 132, y 197, z 97 |
| **x — the Condorcet loser** | 5 of 32 | x 199, y 197, z 97 |
| **z — the status quo** | 3 of 32 | x 132, y 197, z **227** |

`z` wins when the small taxers approve their top two and everyone else bullets. Nobody has misrepresented an
attitude, nobody has set an agenda, no vote is out of order — and approval delivers precisely the outcome
that the anti-taxers had to conspire to obtain under the sequential agenda, against a 77% majority for some
increase and against the Condorcet winner. Five more profiles elect `x`, which loses to both other options
head-to-head.

Horn sees the edge of this and writes it down — "a very small change in the breakdown … would flip it,
allowing for the status quo to again prevail" — and then, two paragraphs later, concludes that "such
distortions of democracy cannot occur under AV." The counterexample is in the paper, one sentence before the
impossibility claim.

The underlying point is the one this folder keeps arriving at from different directions: **approval's answer
is not a function of the preference profile.** The same 426 rankings elect any of the three options depending
on cutoffs. Section IV treats that as a virtue; section III needs it to be false.

## Virtue 3 — cycles and Arrow

The claim is that approval avoids Condorcet cycles and so is not subject to Arrow's theorem. Both halves are
true. Neither is unique, and one supporting sentence is wrong:

> "This sort of cycle, as Arrow has shown, is unavoidable under every type of minimally democratic
> preferentist voting mechanism whenever there are more than two candidates."

Arrow shows no ordinal social welfare function satisfies his four conditions together. He does not show that
every ranked method produces intransitive output. Borda on the standard 3-voter cycle returns 3–3–3: complete,
transitive, and tied. Ranked pairs and Schulze return transitive orders on every profile by construction. The
intransitivity belongs to the pairwise majority relation, which is one input a ranked method may or may not
consult — [math-in-society-lippman](math-in-society-lippman.md) records the same over-reading in a textbook,
where Arrow gets stated without the ordinal restriction on the page before approval is introduced.

Approval escapes Arrow because Arrow quantifies over ordinal rules and approval isn't one. So do score, STAR
and majority judgment, identically. What approval buys with the escape is visible in section IV's own table:
the three cyclic voters can produce many different approval profiles, so the same cycle yields many different
winners. Horn presents the multiplicity as showing approval "can also produce a legitimate winner." It equally
shows the winner is chosen by the cutoffs rather than by the preferences.

### The section IV table forbids what section II.B requires

Each row of the table lists the approval profiles said to be *consistent* with a voter's ranking. The rule
being applied is "any set containing your favourite" — so each row includes the set {favourite, worst},
skipping the middle candidate. For `P` with `x > y > z` that is `{x, z}`: approving `z` and not `y`, which by
II.B entails `z > y`. All three rows contain exactly one such cell:

| Voter | Ranking | Offending cell | Entails |
|---|---|---|---|
| P | x > y > z | {x, z} | z > y |
| Q | y > z > x | {x, y} | x > z |
| R | z > x > y | {y, z} | y > x |

Same defect as the 66 big taxers, three more times.

**Footnote 20 is the paper's one non-trivial computation, and it is correct.** Drop the approve-all and
approve-none columns and count the scenarios where `x` gets exactly two votes: 12 ways, `x` winning outright
in 2, tying in 8, losing to each of the other two once. All four numbers verify. But drop the three
II.B-violating cells as well and the 12 becomes **4** — 1 outright win, 3 ties, 0 losses. The footnote's
combinatorics rest on ballots the paper's own inference rule forbids.

## Is "unique" the right word?

The title says unique; the abstract says "generally not shared by its best-known competitors."

| Virtue | Shared with |
|---|---|
| 1 — IIA | score voting, under the same fixed-scale assumption; any rule taking exogenous per-candidate evaluations |
| 2 — no agenda-setting | every method, once all options are voted on simultaneously — plurality included |
| 3 — no cycles, escapes Arrow | score, STAR, majority judgment; and Borda, Schulze, ranked pairs never emit intransitive orders either |

Nothing here separates approval from score voting, which the paper never mentions. Given that the case is
built on Rule (1) — an assumption approval satisfies only by fiat and score satisfies just as well — the
paper is, in effect, an argument for cardinal ballots that has been labelled as an argument for approval.

## Errata, indexed

| # | Location | Claim | Status |
|---|---|---|---|
| 1 | §III | "of the 132 big taxers, 99 … and 66 …" | **165 ≠ 132**; the printed totals reproduce only from 165 |
| 2 | §III | the 66 rank x > y > z and approve {x, z} | contradicts the paper's own rule II.B |
| 3 | §III | "Ax greater than either Ay or Az … then y will prevail" | false under both readings; the example doesn't satisfy it |
| 4 | §III | "a very narrow victory" (3 votes) | artefact of erratum 1; corrected margin is 36 or 69 |
| 5 | §III | "a plurality of deciders prefers a tax increase" | 329/426 = 77%, a supermajority |
| 6 | §III restatement | the 130 bloc labelled `yxz` | the list it restates says `yzx` |
| 7 | §IV table | one cell per row skips the middle candidate | contradicts rule II.B; drops footnote 20's count from 12 to 4 |
| 8 | §IV | cycles "unavoidable under every type of … preferentist voting mechanism" | Borda, Schulze, ranked pairs always emit transitive orders |
| 9 | §I | Gibbard 1973 described as being about "multi-winner"/"multi-seat" schemes | Gibbard–Satterthwaite is single-winner, ≥3 alternatives |
| — | §IV, fn. 20 | 12 scenarios; 2 wins, 8 ties, 2 losses | **correct as printed** |

Five reviewers, an average of 3.40, and a peer-approval statement praising the paper's treatment of all three
virtues. None of the above appears to have been raised. That is the reason this note exists in the form it
does: the arithmetic in a peer-approved paper on a preprint server with open review is worth ten minutes of
`python3`.

## What survives

Stripped of the overclaims, there is a real argument left, and it is not nothing:

- **The Rule (1) / Rule (2) distinction is the right frame** and deserves to be quoted. Most approval
  advocacy slides between the two without noticing; most approval criticism attacks (2) while advocates
  defend (1). Naming them separates the disagreement.
- **Single-shot voting beats sequential agendas**, which is a genuine argument against amendment procedure in
  legislatures, just not an argument for approval specifically.
- **Approval is outside Arrow's scope**, correctly stated, in a literature where that is routinely muddled.

The paper's real thesis, once you follow it through, is that *if voters had fixed dichotomous attitudes,
approval would behave beautifully*. That is true, and it has a precise form —
[brandl-peters-approval-characterizations](brandl-peters-approval-characterizations.md) proves that on the
dichotomous domain approval is not merely good but forced, eight different ways. What Horn adds is the
observation that the domain restriction can be imposed by the *rule* rather than assumed of the *voters*. What
neither addresses is [approval-voting](approval-voting.md)'s record: 79% bullet voting in the 1987 MAA
election, run by the mathematicians who chose the method. Rule (1) is not a rule anyone has found a way to
enforce.

## New ideas and terms

- **Rule (1) vs. Rule (2)** — the instruction-level distinction between "approve all and only those you
  approve of" and "mark as many as you like". The first is violable by a sincere-looking ballot; the second
  is violable only by tearing the paper.
- **IIA2** — the popular non-Arrovian reading of IIA: adding or removing an alternative shouldn't reverse a
  judgement between two others. Horn's IIA2\* is its approval analogue; IIA2† is the Sen-property-α form.
- **Sen's property α** — if X is chosen from a set, X is chosen from every subset containing it.
- **Agenda-setting manipulation** — controlling the *order* of pairwise votes to defeat a majority position;
  the Powell Amendment is the standard example, and Riker's reading of it is itself disputed (Mackie 2003).
- **The Burr dilemma** — Nagel's approval-specific coordination failure, named for the 1800 Jefferson/Burr
  tie; cited here but not engaged.

## Links referenced

- [Qeios preprint v1](https://www.qeios.com/read/ZETKEQ) · [peer-approved v2](https://www.qeios.com/read/ZETKEQ.2)
  · [PhilArchive record](https://philarchive.org/rec/HORTUV)
- Arrow (1951), *Social Choice and Individual Values*
- Gibbard (1973), "Manipulation of Voting Schemes: A General Result", *Econometrica* 41(4)
- Nagel (2007), ["The Burr Dilemma in Approval Voting"](https://www.journals.uchicago.edu/doi/abs/10.1111/j.1468-2508.2007.00493.x), *Journal of Politics* 69(1)
- Niemi (1984), "The Problem of Strategic Behavior Under Approval Voting", *APSR* 78(4)
- Ohtsubo & Watanabe (2003), "Contrast Effects and Approval Voting", *Political Psychology* 24(3) — the
  empirical IIA violation the paper is answering
- Blydenburgh (1971), *Journal of Politics* 33(1); Riker (1986), *The Art of Political Manipulation*;
  Mackie (2003), *Democracy Defended* — the Powell Amendment dispute
- Sen (1970), *Collective Choice and Social Welfare*
- Horn (2020), *Democratic Theory Naturalized*, chs. 7–8 — where the author says the basic case for approval lives

## Related local material

- [approval-voting](approval-voting.md) — the empirical half; the compliance-table row that only dichotomous
  preferences pass, the dichotomous-cutoff IIA example, and the bullet-voting record that Rule (1) has to
  survive
- [brandl-peters-approval-characterizations](brandl-peters-approval-characterizations.md) — the rigorous
  version of this paper's thesis: on the dichotomous domain approval is the only rule left
- [score-voting](score-voting.md) — where IIA-under-absolute-scoring was already established, which is why
  virtue 1 isn't unique
- [math-in-society-lippman](math-in-society-lippman.md) — Arrow stated without the ordinal restriction, one
  page before approval is introduced; the same over-reading as erratum 8
- [glossary.md](glossary.md) — IIA, Condorcet winner/loser, agenda-setting, Gibbard–Satterthwaite
- [whoops](whoops.md) — errata 1–4 and 7 belong there
