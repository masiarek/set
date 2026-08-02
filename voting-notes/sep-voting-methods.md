# Voting Methods — the Stanford Encyclopedia entry (Pacuit)

Source: [Eric Pacuit, "Voting Methods"](https://plato.stanford.edu/entries/voting-methods/), *The Stanford
Encyclopedia of Philosophy* — first published 3 Aug 2011, **substantive revision 24 Jun 2019**, read
2026-08-02. The link that started this note was the
[Fall 2018 archive](https://plato.stanford.edu/archives/fall2018/entries/voting-methods/); the differences
are set out below and they are not small.

Verifier: [code/sep-voting-methods/verify.py](code/sep-voting-methods/verify.py) ·
output: [run-output.txt](code/sep-voting-methods/run-output.txt) — 185 checks, every profile in the entry
recomputed, plus exhaustive searches for the four theorems it states without witnesses.

## What it's about

The first source in this folder that is neither a textbook, an encyclopedia article written by advocates, nor
a paper with a thesis. It is a philosophy reference work: a survey whose job is to lay out the landscape and
point at the literature. That changes what there is to check. There is no thesis to test, no advocacy to
audit, and the arithmetic is careful — **every winner, score and tally it prints is correct**. What the
verifier found instead sits one layer down: two definitions that break on the entry's own examples, a theorem
stated with a redundant axiom, a proof that uses more than it needs, and an example presented as an instance
of a theorem it doesn't quite instantiate.

The reason to have it here is coverage. Sixteen notes in, this folder can work an election but has almost
nothing on **why** a method might be the right one, and nothing at all on the possibility that a vote has a
*correct* answer rather than merely a fair procedure. That is section 4.3 of this entry, and it has no
counterpart anywhere else in these notes.

## What the 2019 revision changed

The Fall 2018 edition is the one still cached in a lot of links. Comparing tables of contents:

| Fall 2018 | Current (Jun 2019) |
|---|---|
| 2. Examples of Voting Methods *(undivided)* | 2.1 Ranking Methods · 2.2 Voting by Grading · **2.3 Quadratic Voting and Liquid Democracy** · **2.4 Criteria for Comparing Voting Methods** |
| 3.3 Multiple Districts Paradox | 3.3 **Variable Population Paradoxes** — the multiple districts paradox, now preceded by the **no-show paradox** and **Moulin's theorem** |
| *(absent)* | **4.4 Computational Social Choice** |
| 5. Concluding Remarks: from Theory to Practice | 5.1 From Theory to Practice · **5.2 Further Reading** |

So the whole participation/no-show strand, quadratic voting, liquid democracy, the computational-complexity
material and the list of criteria for comparing methods are 2019 additions. Anscombe and Ostrogorski were
already there in 2018. If you have notes from the Fall 2018 text, the missing piece is exactly the part these
notes care most about — [participation](glossary.md) and the no-show paradox, which is where
[majority-judgment](majority-judgment.md) and [score-voting](score-voting.md) both ended up.

## What it has that these notes don't

Genuinely new relative to the glossary, in rough order of how much it matters here:

- **The epistemic conception of voting** (§4.3) — the idea that a vote can be *correct*, not merely fair.
  Coleman and Ferejohn's proceduralism, Cohen's three conditions, and the **Condorcet Jury Theorem**:
  independent voters each better than a coin flip make majority rule converge to certainty as the electorate
  grows. Then Young's result that **Borda count is the maximum-likelihood estimator** of the best candidate
  under a noise model — which is a completely different argument for Borda than any in
  [legrand-ranked-ballot-methods](legrand-ranked-ballot-methods.md), where it is just one row of a
  compliance table.
- **Fishburn's theorem** (§3.1.1) — for every *m* ≥ 3 there is a profile with a Condorcet winner where *every*
  scoring rule puts at least *m*−2 candidates above them. The general statement of the fact
  [score-voting](score-voting.md) and [lumen-75-ballot-four-winners](lumen-75-ballot-four-winners.md) keep
  bumping into one profile at a time.
- **Moulin's theorem** (§3.3) — with four or more candidates, *every* Condorcet consistent method has a
  no-show paradox. The participation failures in [majority-judgment](majority-judgment.md) were forced by
  Balinski and Laraki's own theorem; this is the ordinal twin of that result.
- **Young's characterization of scoring rules** (§4.2) — anonymity + neutrality + **reinforcement** +
  continuity, if and only if it is a scoring rule. Reinforcement is the multiple-districts property, so this
  says the scoring rules are exactly the district-safe methods. With Fishburn/Alós-Ferrer for approval and
  **Myerson's abstract scoring rules** covering plurality, approval, Borda, range and cumulative voting in one
  frame.
- **Condorcet components and "cancelling properly"** (§3.1.1) — Saari's argument that a perfectly symmetric
  cycle is noise that a method ought to ignore, plus Balinski and Laraki's proof that **no Condorcet
  consistent method can cancel properly**.
- **Three paradoxes of packaging** (§3.4) — the **multiple elections paradox** (an outcome with zero
  supporters), **Anscombe's paradox** (a majority of voters on the losing side of a majority of issues), and
  **Ostrogorski's paradox** (the candidate holding the minority position on every issue wins). Nothing in
  these notes touches referendum bundling at all.
- **Quadratic voting** and **liquid democracy** (§2.3) — the two methods here that price or delegate
  influence rather than aggregate it.
- **Impartial culture** (§5.1) — the standard distribution for asking how *likely* a paradox is, and the
  entry is careful to say it is a worst case (Tsetlin et al.), against which Regenwetter's empirical work
  finds real electorates where all the usual methods agree.
- Smaller: **negative voting**, **k-approval** as a family, **Condorcet's other paradox**, the
  NP-completeness of Dodgson's method, and the observation that **quota rules are indecisive** — Majority
  Rule as the *q* = 0.5 case of a family whose members often elect nobody.

Two absences worth recording, since both came up when this note was scoped:

- **No domain restrictions.** Single-peakedness and Black's median-voter theorem appear nowhere in the body
  (the phrase surfaces only inside a bibliography title). The entry's answer to "when does the paradox go
  away?" is entirely probabilistic — impartial culture and empirical frequency — never structural.
- **No centre squeeze.** Hare is defined, named as Ranked-Choice Voting and Instant Runoff, and listed among
  the non-monotonic methods — but the worked monotonicity failure is for Plurality with Runoff, and the
  failure mode that decided [Alaska 2022](rcv-and-core-support.md) is never described. The most widely
  adopted reform method in the English-speaking world gets a definition and a mention.

## Findings

### 1. Its own Hare and Coombs definitions elect nobody on its own Condorcet paradox

Section 2.1 defines the multi-stage methods and states the tie convention explicitly: *"I assume that all of
the poorly performing candidates will be removed in each round."* Then Section 3.1 states Condorcet's paradox
with the smallest possible profile:

```
1  A B C
1  B C A
1  C A B
```

Every candidate has one first place. Under the stated rule, round one deletes **all three**, and the fallback
clause — *"if there is no such candidate, then the remaining candidate(s) are declared the winners"* — has
nothing left to name. Hare and Coombs both return the empty set on the entry's flagship example. Plurality
with Runoff, whose tie clause is *"the top two candidates (or more if there are ties)"*, returns all three.

This also bears on the claim in §2.1 that *"if there are only three candidates, then the above two voting
methods are the same."* Exhaustively over all 5,004 anonymized three-candidate profiles with 1–9 voters:

| | count |
|---|---|
| profiles where Hare and Plurality with Runoff disagree | **501** |
| profiles where Hare, as defined, elects nobody | **501** |
| disagreements where Hare *did* return someone | **0** |

So the identification is exactly right wherever Hare is decisive, and the 10% of profiles where the two
methods part company are precisely the ones the deletion rule wipes out. The smallest is two voters:
`1 B C A, 1 C B A` — Hare deletes A, then deletes B and C together for want of a strict majority.

This is a definitional gap, not an error: the entry flags in the same paragraph that *"an alternative
approach would use a tie-breaking rule."* It is worth recording because the reader who implements the printed
definitions gets a method that crashes on the canonical three-voter example.

### 2. The runoff transfers are described backwards

Section 2.1's 19-voter example separating Plurality with Runoff from Hare:

```
7  A B C D        Plurality with Runoff → A
5  B C D A        Hare                  → D
4  D B C A        Coombs                → B
3  C D A B        Borda                 → B      (no Condorcet winner)
```

The entry's narration: *"the groups voting for candidates C and D transfer their support to candidates B and
A, respectively, with A winning 10 – 9."* The pairing is reversed. The C-first group ranks `C D A B`, so in an
A-vs-B runoff it supports **A**; the D-first group ranks `D B C A`, so it supports **B**. The total is right —
7 + 3 = 10 against 5 + 4 = 9 — because the two errors are the same error twice.

The example itself is the best one in the entry, and better than it says: the same 19 ballots give **three
different winners** across the three multi-stage methods it defines, Borda agrees with Coombs, and there is no
Condorcet winner to arbitrate — Copeland ties B and C at +1. It is [lumen-75](lumen-75-ballot-four-winners.md)
in miniature, four sections before the entry gets to paradoxes.

### 3. "7 voters and 3 candidates" for an example with 5 voters and 4 candidates

Section 4.1, introducing the Borda manipulation: *"Consider the following two election scenarios with 7 voters
and 3 candidates."* The table below it has five voters ranking four candidates, and every Borda score printed
(9 / 5 / 10 / 6 and 9 / 6 / 8 / 7) is computed for five voters and four candidates. All eight scores check
out; only the sentence is wrong.

Worth naming what the manipulation is, since the entry doesn't: the third voter moves C from second to last
while keeping her true favourite A on top. That is **burial**, the move
[star-strategy-pages-vs-wikipedia](star-strategy-pages-vs-wikipedia.md) had to construct by exhaustive search
to show it works under STAR. Here it is the entry's illustration of Gibbard–Satterthwaite.

### 4. Condorcet's 81 voters do not witness the m = 3 case of Fishburn's theorem

Section 3.1.1 works Condorcet's 81-voter profile, shows the Borda winner B beats the Condorcet winner A, and
then observes that a scoring rule can elect A *only* if s₂ > s₁. All correct: with s₃ normalised to 0,

> Score(A) − Score(B) = 31·s₁ + 39·s₂ − (39·s₁ + 31·s₂) = **−8(s₁ − s₂)**

Then: *"Peter Fishburn generalized this example as follows"*, and the theorem says that for m ≥ 3 some profile
has **at least m − 2 candidates with a greater score than the Condorcet winner** under every scoring rule. For
m = 3 that is one candidate, strictly ahead, for every rule. This profile isn't one: at s₁ = s₂ — 2-approval —
A and B **tie at 70**, so no candidate has a *greater* score. The entry doesn't claim the profile is a witness,
but it presents the theorem as the generalisation of it, and it isn't.

A witness does exist, and searching exhaustively by electorate size, **the smallest takes 11 voters**:

```
2  A C B
3  B A C          C is the Condorcet winner (6–5 over A, 6–5 over B)
2  B C A          B outscores C under every scoring rule
4  C B A
```

The reason is as simple as it can be: B has one more first place than C (5 to 4) and exactly as many seconds
(4 each), so Score(B) − Score(C) = 1 at every s₂/s₁ ratio in [0, 1]. No profile with ten or fewer voters does
it. Plurality, Borda and 2-approval all elect B here — the *whole* scoring family, unanimous against the
pairwise winner.

### 5. Saari's cancellation argument, with the arithmetic the entry leaves qualitative

The entry splits Condorcet's 81 voters into three groups — a 30-voter cycle, a 3-voter reverse cycle, and 48
voters who are in neither — and argues that *"within each of these groups, it is natural to assume that the
voters' opinions cancel each other out."* Verified, and then quantified:

| | contribution to Borda | margin contributed to A vs B |
|---|---|---|
| Group 1: 10 `ABC`, 10 `BCA`, 10 `CAB` | **+30 to every candidate** | **+10** |
| Group 2: 1 `ACB`, 1 `CBA`, 1 `BAC` | **+3 to every candidate** | **−1** |
| Group 3: 20 `ABC`, 28 `BAC` | 68 / 76 / 0 | **−8** |
| total | 101 / 109 / 33 ✓ | **+1** ✓ |

That is the whole argument in one table. The components are exactly neutral for Borda — each candidate takes
first, second and last place once per cycle — and they are exactly *not* neutral for the majority relation,
because a cycle contributes a 2:1 margin in one direction on every pair. **A's Condorcet win over B is a
margin of one vote, manufactured by the cycles against a real eight-vote deficit among the 48 voters who are
not in any cycle.** Whether that makes A a spurious winner or B a spurious winner is the argument the entry
says is unsettled; the accounting isn't.

### 6. May's Theorem is stated with a redundant axiom

Section 4.2:

> **Theorem (May 1952).** A voting method for choosing between two candidates satisfies Neutrality, Anonymity,
> Unanimity and Positive Responsiveness if and only if the method is majority rule.

May's 1952 theorem uses **three** conditions — anonymity, neutrality and positive responsiveness. Unanimity is
not one of them, and it is not needed. Brute force over every neutral rule on anonymized two-candidate
profiles (ballots: vote A, abstain, vote B; outcomes: A, B, tie — anonymity is built into the domain exactly
as the entry's §1.1 does):

| electorate | rules satisfying Neutrality + Positive Responsiveness | ...also satisfying Unanimity | is the survivor majority rule? |
|---|---|---|---|
| n = 3 | 1 | 1 | yes |
| n = 4 | 1 | 1 | yes |
| n = 5 | 1 | 1 | yes |
| n = 6 | 1 | 1 | yes |

Unanimity removes nothing because there is nothing left to remove. Harmless as a statement — the biconditional
is still true — but it obscures which axioms are load-bearing, which is the entire point of a characterization
result. Compare the [MDI trivia card](mdi-trivia-cards.md) version, which states it as anonymity + neutrality
+ monotonicity ⇒ a quota method, then adds near-decisiveness to force simple majority: three different axiom
lists for the same theorem across two sources, and only one of them is May's.

### 7. The resoluteness impossibility is proved with more than it needs

Section 4.2 shows there is no **resolute** method satisfying Universal Domain, Anonymity, Neutrality and
Unanimity, using three successive tables and a permutation-of-voters argument that appeals to Anonymity at the
end. But §1.1 has already declared that *"in the remainder of this article (unless otherwise specified), I
will restrict attention to anonymized profiles"* — on that domain anonymity is not an axiom, it is the type
signature. And then the proof is one line:

> The profile `1 ABC, 1 BCA, 1 CAB` is **fixed by the candidate rotation** A→B→C→A. Neutrality forces the
> winner set to be fixed by it too. No singleton is.

Same conclusion, one axiom, no tables. The entry's version re-derives the anonymity it already assumed.

### 8. The monotonicity example rests on a majority cycle

Section 3.2's Plurality-with-Runoff failure — two voters promote A from second to first, and A loses to C —
checks out exactly (11–6 in scenario 1, 9–8 the other way in scenario 2). What the entry doesn't say is that
**neither scenario has a Condorcet winner**: both carry the cycle A > B > C > A, so there is no pairwise
standard by which either outcome is the right one. The failure is bare, which is the strongest form of it.

And the method that behaves monotonically here is Borda, which elects A in both scenarios (19–18–14, then
21–16–14). Two sections later Borda is the entry's example of an IIA failure. That trade is the spine of the
whole subject and the entry never puts the two examples side by side.

### 9. What Moulin's theorem does and does not say

*"If there are four or more candidates, then every Condorcet consistent voting method is susceptible to the
no-show paradox."* The bound is on **m**, and the natural misreading is that three candidates are safe. Tested
on two Condorcet methods the entry itself defines, counting only unambiguous singleton-winner cases so no
tie-breaking convention is smuggled in:

| | 3 candidates | 4 candidates |
|---|---|---|
| **Minimax** (Simpson) | no violation in **all 12,369** profiles with 2–11 voters, blocs of up to 3 abstaining | fails — 11 voters, a bloc of 2 |
| **Black's Procedure** (Condorcet winner, else Borda) | **fails — 8 voters, one abstainer** | fails — 6 voters, one abstainer |

Black's three-candidate failure is small enough to print:

```
1  A C B      no Condorcet winner (A ties both), so Borda decides: B 10, C 9, A 5  → B wins
3  B A C
4  C B A      remove the ACB voter → C becomes the Condorcet winner → C wins
```

The `ACB` voter ranks C above B, so showing up cost her the better outcome. Moulin's theorem is about what is
*possible* below four candidates, not about what any particular method does: one Condorcet method survives
everything an exhaustive search can reach at m = 3, and another fails at eight voters.

### 10. The impartial-culture numbers check out

Section 5.1 quotes Riker's table: five candidates and seven voters gives a **21.5%** chance of a majority
cycle, rising to **25.1%** as the electorate grows and to certainty as candidates are added. Monte Carlo
(200k trials for the first, 30k for the second):

| | simulated | entry |
|---|---|---|
| 5 candidates, 7 voters | **21.43%** | 21.5% |
| 5 candidates, 151 voters | **25.07%** | 25.1% (limit) |
| 7 voters, m = 3 / 5 / 10 / 20 | 7.3% / 21.3% / 42.5% / 60.9% | "increases to certainty" |
| 3 candidates, n = 3 / 5 / 9 / 25 / 101 | 5.7% / 7.0% / 7.8% / 8.4% / 8.7% | "increases, though not necessarily to certainty" (limit 8.77%) |

Both hedges in that passage are exact: the candidate direction runs to certainty, the voter direction
converges to a number well under 10%. And the entry is straight about the assumption — impartial culture is a
worst case (Tsetlin et al. 2003), so these are ceilings, not forecasts. That is a more careful treatment of
paradox frequency than any other source in these notes, most of which quote a probability with no
distribution attached.

### 11. Approval's ballot set is defined two incompatible ways

§2.2: *"Each voter selects a subset of the candidates (**where the empty set means the voter abstains**)."*

§4.2: *"the set of ballots B is the set of **non-empty** subsets of the set of candidates … (**selecting the
ballot X consisting of all candidates** means that the voter abstains)."*

Both conventions are standard and they agree on every winner, since a ballot approving everybody and a ballot
approving nobody shift every candidate's score equally. But the Fishburn/Alós-Ferrer characterization is
stated for the second and the method for the first, and **Faithfulness** — *"if there is exactly one voter,
the winners are the set chosen by that voter"* — is exactly where the difference would bite if it bit
anywhere. Our [brandl-peters](brandl-peters-approval-characterizations.md) note has the same theorem with
approval ballots as functions to {0,1}, which sidesteps the question.

The neighbouring claim is the one these notes already know: *"if there is a unique Condorcet winner, then that
candidate **may** be elected under approval voting."* That "may" is Brams's theorem, and it is the
[indeterminacy](approval-voting.md) result under its polite name — approval can also elect the Condorcet
loser on the same preferences, as the entry says a sentence later.

### 12. Errata

Substantive first, then the bibliography.

| The error | Where | Consequence |
|---|---|---|
| **Runoff transfers stated backwards** — "the groups voting for C and D transfer their support to B and A, respectively" | §2.1, 19-voter example | None on the result; C's group goes to A and D's to B, and 10–9 is right either way |
| **"7 voters and 3 candidates"** for a table with 5 voters and 4 candidates | §4.1 | None; all eight Borda scores are correct for 5 and 4 |
| **Hare and Coombs elect nobody** on a perfect first-place tie | §2.1 definitions vs §3.1 example | The stated definitions return ∅ on the entry's own Condorcet paradox profile |
| **May's Theorem stated with four axioms**; May 1952 uses three | §4.2 | Biconditional still true; Unanimity is redundant given the other three |
| **"the set of voters chosen by that voter"** in Faithfulness, and "assigns a non-empty set of **voters** to each anonymous profile" for a function into ℘(X) | §4.2 | Should be *candidates* in both |
| **"the voter in the middle column"** for a voter who is a table *row* | §2.2, twice | Wording |
| **Approval ballots defined with, then without, the empty set** | §2.2 vs §4.2 | No winner changes |
| **"Balinksi"** for Balinski | §2.2 and §5.2 | Spelling; the bibliography has it right |
| **"Chebotarev and Smais 1998"** | §4.2 | The bibliography entry is **Chebotarev and Shamis** |
| **Young "1998"** for the 1988 *APSR* paper (the volume number 82 given is 1988's), and **Young 1974** cited in the text with no entry | bibliography / §4.2 | Two of the four Young citations don't resolve |
| **Nurmi 1999 and Nurmi 1998** cited; the bibliography lists only **Nurmi 1987** | §3, §5.2 | Both dangle |
| **Posner and Weyl 2018** (*Radical Markets*) cited twice; bibliography has only 2015 and 2017 | §2.3 | Dangles |
| **Lalley and Weyl 2018b** cited; bibliography has only 2018a | §2.3 | Dangles |
| **Bloembergen, Grossi and Lackner 2018** cited; no entry, and Lackner appears nowhere in the bibliography | §2.3 | Dangles |
| **Ostrogorski 1902** cited; no entry (the only "Ostrogorski" in the bibliography is inside Rae and Daudt's title) | §3.4 | Dangles |
| **Brams and Sanver 2009** cited; the bibliography entry carries **no year** | §2.2 | Unresolvable as printed |
| **"Fabienne 2017"**, listed as "Fabienne, P., 2013" — the author of the SEP *Political Legitimacy* entry is **Fabienne Peter**, indexed here under her given name, with the text year, the bibliography year and the archive URL (sum2017) all disagreeing | §2.3 / bibliography | Three different years for one citation |

Ten of the seventeen are citation hygiene, which is what a survey is *for*; the ratio is worth knowing before
using the bibliography as a reading list.

## What it gets right that the other sources didn't

Three things, all worth stealing:

**The k-approval sequence.** One five-voter profile, and 1-, 2- and 3-approval elect `{A,B}`, `{D}` and
`{A,B}`:

```
2  A D B C        1-approval (= plurality): A, B
2  B D A C        2-approval:               D
1  C A B D        3-approval:               A, B     Condorcet winner: A
```

D is nobody's first choice and everybody's compromise, so widening the approval window by one seat elects him
and widening it again drops him. This is the cleanest demonstration in any source here that "approval-style"
names a family, not a method — and that where you set the cutoff decides the election, which is the
[indeterminacy](approval-voting.md) finding stated as a *rule* difference rather than a *voter* difference.

**The grading example.** Five voters, three candidates, grades 0–4, and three methods give three answers:

| | A | B | C |
|---|---|---|---|
| mean | **2.6** | 1.8 | 2.4 |
| median | 2 | **3** | 2 |
| pairwise (from the same grades) | — | — | **beats both, 3–2** |

Score elects A, Majority Judgement elects B, the Condorcet winner is C. Six numbers per candidate and the
whole mean-vs-median-vs-pairwise argument is on the page. [majority-judgment](majority-judgment.md) needed a
650-voter spatial model to make the same point; this does it with fifteen grades. The entry then runs both
manipulations on it — the score manipulation that moves A from 2.6 to 2.4 and doesn't touch either median, and
Felsenthal and Machover's MJ manipulation that lifts A's median from 2 to 4 — so the strategy comparison uses
one profile too.

**The honesty about impartial culture.** §5.1 gives the probability, names the distribution, says the
distribution is a worst case, cites the people who proved it, and then reports that the empirical work finds
the methods agreeing anyway. Compare every advocacy page in these notes that quotes a failure rate with no
model behind it.

## Where it fits with the rest of the folder

- **Hare = RCV = IRV = one-seat STV.** The entry names the first three as synonyms;
  [single-transferable-vote](single-transferable-vote.md) supplies the fourth.
- **Score voting by average.** §2.2 defines Score Voting as the largest *average* grade, while §4.2's Myerson
  framework defines Range Voting by *summing*. Consistent only because every voter grades every candidate —
  the moment a ballot can leave a candidate blank they diverge, which is the discrepancy
  [score-voting](score-voting.md) found in the Wikipedia article's own lead.
- **Dodgson's method** is defined here correctly (fewest pairwise swaps, NP-complete) and is the standard
  against which [legrand-ranked-ballot-methods](legrand-ranked-ballot-methods.md) found LeGrand's "Dodgson" to
  be a cheap approximation.
- **Cumulative voting** gets a one-line definition and a Myerson-style formalisation (ballots summing to 1),
  which is the general form of the discrete version in [mdi-trivia-cards](mdi-trivia-cards.md).
- **Nanson, Coombs, Copeland, Schwartz, Black, Condorcet's Rule** are all defined, and all already in the
  [glossary](glossary.md) from LeGrand — this entry is the citation for the ones LeGrand names without
  attribution.
- **Arrow** is stated correctly and for social welfare functions, with the ordinal restriction intact — the
  thing [math-in-society-lippman](math-in-society-lippman.md) found dropped and
  [cardinal-voting-systems](cardinal-voting-systems.md) found over-applied. Third source, first clean
  statement.

## Bottom line

A survey that earns its place by covering what the worked-example sources structurally can't: characterization
theorems, the epistemic reading of voting, and the question of how *likely* the paradoxes are. Its arithmetic
is sound — 185 checks, no wrong number anywhere — and what breaks under recomputation is definitional: two
elimination rules that return nobody on the entry's own paradox profile, an axiom in May's theorem that isn't
doing anything, a proof that uses an axiom it has already assumed, and a theorem introduced as the
generalisation of an example that doesn't instantiate it. The smallest profile that does instantiate it takes
eleven voters, and it is in the verifier.
