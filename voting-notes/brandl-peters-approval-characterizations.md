# Approval voting, axiomatically — Brandl & Peters (2022)

Source: [Brandl & Peters, "Approval Voting under Dichotomous Preferences: A Catalogue of Characterizations"](https://www.dominik-peters.de/publications/av.pdf),
*Journal of Economic Theory* 205 (2022), 105532, [doi:10.1016/j.jet.2022.105532](https://doi.org/10.1016/j.jet.2022.105532)
— read 2026-08-01. ([ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0022053122001223)
is paywalled; the authors' PDF is free and is the same published version.)

Verifier: [code/approval-characterizations/verify.py](code/approval-characterizations/verify.py) ·
output: [run-output.txt](code/approval-characterizations/run-output.txt)

## What it's about

Every other note in this folder asks what a method *does* — run the ballots, see who wins, see what breaks.
This one asks the opposite question: given a list of properties you want, which method are you forced into?
The answer here is approval voting, eight times over, and the interesting part is not that approval wins but
**how narrow the domain has to be for the question to have an answer at all**.

The domain is dichotomous preferences: every voter sorts candidates into approved and disapproved, indifferent
within each class. [approval-voting](approval-voting.md) already had this as the row of the compliance table
where approval passes everything, with Brams–Fishburn's caveat that real voters aren't like that. This paper
is the other half of that story — on that domain approval isn't merely *good*, it is **the only rule left**.

## The one-paragraph version

Nine numbered theorems. Theorem 1 is a base theorem (consistency + faithfulness + disjoint equality force
approval), proved from scratch in about a page of elementary algebra with no separating-hyperplane machinery.
Theorems 2–9 are the eight characterizations of the title, and seven of them are proved by showing their
axioms imply faithfulness and disjoint equality, then invoking Theorem 1. Appendix B then constructs 17
example rules proving that not one axiom anywhere can be dropped. The whole paper is a lattice with one
load-bearing beam.

## What the dichotomous domain actually buys

This is the fact that makes everything else work, and none of the other notes had it:

> **Under dichotomous preferences the majority relation is transitive** (Inada, 1969) **and orders candidates
> exactly by approval score.**

Consequences, all of them immediate once you see it:

- **Condorcet cycles cannot occur.** Not "rarely" — *cannot*. The entire apparatus of
  [Smith sets, Schwartz sets, beatpaths and cycle-resolution](glossary.md) is empty machinery here.
- **The approval winners are exactly the maximal elements of the majority relation**, so approval is a
  Condorcet method on this domain by construction, not by good fortune.
- The ✓ in the Condorcet column of the dichotomous row of
  [approval-voting.md's compliance table](approval-voting.md) is therefore *structural*. Wikipedia presents it
  as one checkmark among eight. It is the reason the other seven are reachable.

Verified exhaustively over all 1,144 profiles on 3 and 4 alternatives in the window: zero intransitivities,
the sign of every majority margin matches the sign of the approval-score gap, and the majority-maximal set
equals the approval winner set in every profile.

**And this is exactly what stops the result from travelling.** Cycles are the thing that makes ranked
social choice hard. Dichotomous preferences don't solve that problem; they define it out of existence.

## The centerpiece: the same axioms, two domains, different answers

The paper keeps noting, almost in passing, what its axiom bundles characterize when ballots are linear orders
instead. Collected in one place, this is the most useful thing in it:

| Axiom bundle | On linear orders | On dichotomous preferences |
|---|---|---|
| consistency + choosing (weak) Condorcet winners | **Impossible** — no such rule exists (Young & Levenglick 1978, Thm 2) | **Approval** (Thm 3, adding continuity) |
| consistency + neutrality + continuity + avoids Condorcet losers | **Borda** (Smith 1973 + Young 1975) | **Approval** (Thm 4) |
| consistency + neutrality + continuity + respects unanimous majorities | **Plurality** (Lepelley 1992; Sanver 2002) | **Approval** (Thm 5) |
| consistency + neutrality + independence of Pareto dominated alternatives | **Plurality** (Richelson 1978; Ching 1996; Öztürk 2020) | **Approval** (Thm 8) |
| consistency + reversal symmetry + independence of never-approved alternatives | **Borda** (Morkelyunas 1982; Saari & Barney 2003) | **Approval** (Thm 9) |

Read the first row twice. **Consistency and Condorcet are incompatible on the ranked domain and jointly
characterizing on the dichotomous one.** That single line does more to explain what the ballot format is
doing than any amount of arguing about expressiveness, and it is the sharpest available answer to the
cardinal-vs-ordinal question in [rcv-and-core-support](rcv-and-core-support.md): the ballot format is not a
convenience, it changes which axioms can coexist.

The Borda rows connect directly to
[ranked-robin-thread-claims-checked](ranked-robin-thread-claims-checked.md), where "sum all the margins"
turned out to be exactly Borda. Same axioms that pin Borda down there pin approval down here.

## The catalogue

Table 1 of the paper, transcribed. Every theorem is "AV is the only ballot aggregation function satisfying…";
the superscripts are the Appendix B example showing that axiom cannot be dropped.

| | Axioms | Undroppable because of |
|---|---|---|
| **Thm 1** (base) | consistency, faithfulness, disjoint equality | Ex 2, 16, 12 |
| **Thm 2** | anonymity, neutrality, consistency, non-triviality, **not Kelly-manipulable** | Ex 1, 3/4/15, 2, 10, 9/5 |
| **Thm 3** | consistency, continuity, **chooses Condorcet winners** (+ non-trivial) | Ex 6, 7, 5 |
| **Thm 4** | neutrality, consistency, continuity, **avoids Condorcet losers** | Ex 14, 6, 7, 5 |
| **Thm 5** | neutrality, consistency, continuity, **respects unanimous majorities** (+ non-trivial) | Ex 16, 8, 7, 5 |
| **Thm 6** | anonymity, consistency, faithfulness, **independence of clones** (needs \|X\| ≥ 4) | Ex 1, 2, 9/10, 5 |
| **Thm 7** | anonymity, neutrality, consistency, faithfulness, **independence of losers** | Ex 1, 3, 2, 9/10, 5 |
| **Thm 8** | anonymity, neutrality, consistency, **independence of Pareto dominated alternatives** | Ex 1, 3, 2, 5 |
| **Thm 9** | anonymity, consistency, reversal symmetry, **independence of never-approved alternatives** | Ex 1, 8, 5, 11 |

The bolded axiom is the headline; everything else is scaffolding. **The scaffolding is not optional** — this
is the thing the abstract's four-word summary hides, and the thing I got wrong on the first pass through this
material. "Consistency plus strategyproofness forces approval" is not a theorem in this paper. Theorem 2 also
needs anonymity, neutrality and non-triviality, and Appendix B has a counterexample ready for each.

### The axioms, in words

- **Consistency** (a.k.a. reinforcement) — split the electorate in two; if both halves choose some
  alternatives in common, the whole electorate chooses exactly those. Present in all nine theorems and in
  every prior characterization of approval. Formally `f(P) ∩ f(P′) = f(P + P′)` whenever the intersection is
  non-empty.
- **Faithfulness** — a one-voter electorate elects that voter's approved set. `f(A) = A`.
- **Disjoint equality** — two voters with non-overlapping ballots produce a tie between everything either
  approved. `f(A + B) = A ∪ B` when `A ∩ B = ∅`.
- **Continuity** (Myerson's "overwhelming majority") — if `f(P) = {a}`, then enough copies of `P` added to any
  other profile also elect `a`.
- **Cancellation** — if every alternative has the same approval score, everything ties.
- **Neutrality / anonymity** — candidate names and voter names don't matter.
- **Kelly-manipulability** — the weakest sensible strategyproofness. A voter can manipulate only if the
  insincere ballot makes the winner set *unambiguously* better: all winners approved where some weren't, or
  some winner approved where none were. Approval is immune (Prop. 1 proves the stronger **Fishburn**
  version too).
- **Independence of clones** — `a` and `b` are clones if every voter approves both or neither. Removing `b`
  must not disturb the others, and `b` wins iff `a` would have.
- **Independence of losers / of Pareto dominated / of never-approved alternatives** — three strengths of "a
  candidate who can't win can't matter." These are the paper's formalization of the spoiler effect.
- **Reversal symmetry** — if every voter approves the complement of their ballot instead, no previous winner
  may still win (unless everything was tied).

## The 17 tightness examples, and the one that matters empirically

Appendix B's examples are the best part of the paper for these notes, because they are concrete rules, not
proofs. The full axiom profile of all of them — recomputed independently rather than read off the paper — is
in [run-output.txt](code/approval-characterizations/run-output.txt) under "Check 3a". Highlights:

- **−AV**, which elects the *least* approved candidate, satisfies anonymity, neutrality, consistency,
  continuity, cancellation, non-triviality, reversal symmetry, independence of clones **and** independence of
  losers. Inside Theorems 6 and 7 it violates exactly one axiom — faithfulness. That is a good demonstration
  that a bundle of respectable-sounding axioms can be satisfied by an absurd rule, and it is why the one
  axiom that looks too obvious to state is the one holding the theorem up.
- Dropping faithfulness from Theorem 6 or 7 leaves **exactly AV, −AV and TRIV** — the paper says so, and both
  survivors check out. So faithfulness is doing one job: excluding two known jokes.
- **Example 5 is the bullet-voting collapse, written as an axiom failure.** The rule is plurality, defined
  here as "ignore every non-singleton ballot" — Fishburn's scoring rule (1, 0, …, 0), where approval is
  (1, 1, …, 1) and cumulative voting is (1, ½, ⅓, …).

  This is not literally what happens when voters bullet-vote — voters casting singletons is not the same as a
  rule discarding non-singletons — but on the sub-domain where everyone bullet-votes the two rules agree, and
  Appendix B is then a price list for the collapse. Of the 17 axioms tracked here, plurality keeps **5**
  (neutrality, consistency, continuity, non-triviality, independence of never-approved alternatives) and
  loses **12**, including every Condorcet property, every independence property but one, both
  strategyproofness notions, reversal symmetry, and respect for unanimous majorities.

  So when [approval-voting.md](approval-voting.md) records that over 80% of Dartmouth voters approved exactly
  one candidate in 2014 and 2016, and that IPO's 2016 presidential vote produced no nominee, this is what was
  being given up — not "some" of approval's advantages but nearly all of the ones this paper proves.

## Checking it

`verify.py` brute-forces every profile on 3 alternatives with ≤ 4 voters and on 4 alternatives with ≤ 3
voters — 1,144 profiles — against 17 axioms and 17 rules. **110 checks pass, 4 fail.** What the method can
and cannot establish is stated at the top of the script and matters for reading what follows: a *failure* is
a finite witness and is exact; a *satisfaction* is only "no counterexample in the window."

Confirmed exactly, including every witness the paper prints in its own prose: AV satisfies all 17 axioms;
PO and CNL fail consistency on the profiles given; Ex 7 fails continuity; Ex 11 fails independence of
never-approved alternatives; Ex 12 fails disjoint equality; Ex 13 fails cancellation on three voters; Inada's
transitivity; and Remark 2's group manipulation of approval (in `{a} + {b} + 2{c}` approval elects *c*, and
the *a*- and *b*-voters both switching to `{a,b}` produces a three-way tie — better for both under Kelly's
extension, which is why Theorem 2's immunity is to *unilateral* deviation only).

### Four Table 1 cells that don't stand up

A cell is valid only if the cited example **fails** its axiom *and* **satisfies every other axiom of that
theorem**. Four don't:

| Cell | Problem | Repairable? |
|---|---|---|
| Thm 5 / consistency ← Ex 8 | Ex 8 also fails **continuity** | Yes — Ex 6 (CNL) works |
| Thm 6 / ind. clones ← Ex 5 | Ex 5 also fails **faithfulness** | Yes — Ex 7, 11, 12, 13, 14, 15 all work |
| Thm 7 / ind. losers ← Ex 5 | Ex 5 also fails **faithfulness** | Yes — Ex 7, 11, 12, 13 all work |
| Thm 7 / neutrality ← Ex 3 | Ex 3 also fails **faithfulness** | Yes — Ex 15 works |

**No theorem is threatened.** Every cell has a replacement from inside Appendix B, found by exhaustive search
over the other 16 examples. These are citation defects at most, not gaps in the results.

Three of the four carry a caveat I can't remove: Table 1 was transcribed from the PDF's text layer, and PDF
extraction binds superscripts to tokens unreliably. The bottom three rows may be my transcription rather than
the paper. Two things do survive that caveat, though: Appendix B's prose for Examples 3 and 5 never claims
faithfulness for them, which is consistent with what the verifier found; and any theorem containing
faithfulness simply cannot be witnessed by a rule that fails it.

**The first row does not depend on the transcription at all**, and is the one real erratum:

> Appendix B argues that Example 8 (approval restricted to the most-frequently-cast ballots) satisfies
> continuity, "since the most-frequent ballots in *P* become the most-frequent ballots in *P′* + *kP* for
> large enough *k*." It doesn't.
>
> Take **P = 2{a} + 2{a,b}**. Both ballots occur twice, so both are most frequent, and approval over them
> gives *a* = 4, *b* = 2 → **f(P) = {a}**. Now take **Q = {a,b}**. In Q + kP the counts are {a}: 2k and
> {a,b}: 1 + 2k, so `{a,b}` is now the *unique* most-frequent ballot, and approval over it alone ties → **f(Q
> + kP) = {a,b} for every k.** Continuity demands some k give {a}. None does.
>
> The argument's gap: Q can *break a tie* among P's most-frequent ballots, so the most-frequent set shrinks
> to a proper subset rather than persisting — and a proper subset can elect someone else.

The implementation is checked against the paper's own printed values for Example 8 before this is claimed —
f({a,b}+{a,c}) = {a}, f({a,b}) = {a,b}, f(2{a,b}+{a,c}) = {a,b}, all reproduced — so the disagreement is
about the paper, not about the code.

Consequence: Example 8 does not show consistency is undroppable in **Theorem 5**, whose axioms include
continuity. It still works for **Theorem 9**, which has no continuity axiom.

### One smaller observation

Theorems 3 and 5 are *stated* for non-trivial rules, but the non-triviality axiom does not appear in their
Table 1 rows. It is load-bearing: TRIV (everything always ties) satisfies consistency, continuity, chooses
Condorcet winners, is neutral, and respects unanimous majorities — vacuously, in the continuity case, since
it never returns a singleton. Without non-triviality both theorems are false as stated. Same transcription
caveat applies.

## What this settles and what it doesn't

**Settles**: whether the dichotomous row of the compliance table is an assumption chosen to flatter approval.
It isn't. It is a domain on which approval is forced by axioms nobody would give up, eight different ways,
and on which the Condorcet machinery is provably idle.

**Doesn't settle**: anything about real electorates. The paper is candid about this — its own motivating
examples are meeting scheduling, hiring committees, and choosing an IT vendor, all cases where "meets the
requirement / doesn't" is genuinely the whole preference. It also offers a behavioural reading: a voter who
finds precise evaluation costly may *fall back* on a rough acceptable/unacceptable split. That is the honest
bridge to real elections, and it is a hypothesis, not a result.

So the argument relocates rather than resolving. It stops being "is approval good on this domain" — settled,
in approval's favour — and becomes **"how far from dichotomous are actual voters,"** which is the empirical
question the rest of [approval-voting.md](approval-voting.md) is about: cutoff indeterminacy, the Tennessee
zero-information scenario electing the Condorcet loser, the 2002 French and 2008/2009 German field
experiments, and the bullet-voting collapses at Dartmouth and IPO. Nothing in this paper touches those,
because the moment a voter has a third opinion about a candidate, none of it applies.

## New ideas and terms

- **Ballot aggregation function** — a rule mapping approval profiles to non-empty winner sets. Irresolute by
  design: ties are outputs, not something to break.
- **Consistency / reinforcement** — merge two electorates that agree on something and the agreement is the
  answer. The engine of every characterization here.
- **Faithfulness**, **disjoint equality**, **cancellation**, **continuity (overwhelming majority)** — the
  housekeeping axioms. See the list above.
- **Kelly's extension / Kelly-manipulability** — the weakest set-preference extension: prefer *Y* to *Z* only
  if all of *Y* is approved or none of *Z* is. Manipulation under it is unambiguous manipulation.
- **Fishburn's extension** — the refinement under which approval is *still* strategyproof (Prop. 1).
- **Independence of clones / of losers / of Pareto dominated / of never-approved alternatives** — four
  strengths of spoiler-resistance, each characterizing approval when paired with consistency.
- **Scoring rule on approval ballots** — a vector (s₁, …, s_m) scoring by ballot *size*: approval is
  (1, 1, …, 1), plurality is (1, 0, …, 0), cumulative voting is (1, ½, ⅓, …). Fishburn (1979): neutrality +
  continuity + consistency characterize this whole class.
- **Inada's condition** — dichotomous preferences make the majority relation transitive.

## Links referenced

- [Brandl & Peters (2022), author PDF](https://www.dominik-peters.de/publications/av.pdf) ·
  [doi:10.1016/j.jet.2022.105532](https://doi.org/10.1016/j.jet.2022.105532)
- Prior characterizations the paper builds on and strengthens: Fishburn (1978, 1979), Alós-Ferrer (2006),
  Sertel (1988)
- Cross-domain results in the table above: Young (1975); Smith (1973); Young & Levenglick (1978);
  Richelson (1978); Morkelyunas (1982); Lepelley (1992); Ching (1996); Saari & Barney (2003); Öztürk (2020)
- Field experiments cited for the domain's plausibility: Laslier & Van der Straeten (2004, 2008), France 2002;
  Alós-Ferrer & Granić (2012), Germany 2008/2009
- Inada (1969), for transitivity of the majority relation under dichotomous preferences

## Related local material

- [approval-voting](approval-voting.md) — the empirical half; the compliance table this note footnotes, and
  the bullet-voting record that Example 5 prices
- [glossary.md](glossary.md) — all terms above are indexed there
- [majority-judgment](majority-judgment.md) — the other note in this folder that turns on a theorem rather
  than an example; Balinski–Laraki's participation-plus-continuity result uses the same Young-style
  continuity axiom
- [ranked-robin-thread-claims-checked](ranked-robin-thread-claims-checked.md) — where "sum all margins" was
  shown to be Borda, which is what two of these axiom bundles characterize on the ranked domain
- [rcv-and-core-support](rcv-and-core-support.md) — the cardinal-vs-ordinal argument that the impossibility
  row of the cross-domain table speaks to directly
- [whoops](whoops.md) — Example 8's continuity argument is indexed there
