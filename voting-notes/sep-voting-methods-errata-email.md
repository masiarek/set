# Errata email — Pacuit, *Voting Methods* (SEP)

Companion to [sep-voting-methods.md](sep-voting-methods.md).

**Status: drafted, not sent. No Gmail draft exists** — an earlier revision of this file claimed one
had been created; checked against the mailbox on 2026-08-02 and it had not. The only draft to this
recipient is an unrelated one from 2023. Nine items: five substantive, one bundle of wording, one
definitional inconsistency, and the bibliography list.

## Where it goes

- **To: `epacuit@umd.edu`** — Eric Pacuit, University of Maryland. The address is the one printed in
  the entry's own copyright line.
- **No cc.** The SEP's [information page](https://plato.stanford.edu/info.html) states the policy
  plainly: *"Readers of the Encyclopedia are encouraged to contact authors directly with comments,
  corrections, and other suggestions for improvements."* `editors@plato.stanford.edu` is the
  institutional fallback if the author route goes nowhere — not a first stop, and cc'ing it on a first
  contact reads as going over someone's head.

## No conflict-of-interest disclosure, and why

The [Lippman errata email](math-in-society-errata-email.md) carries one, because item 3 there softens
a criticism of a rated method and I contribute to software used by an organisation that advocates for
one. Nothing here has that shape. Every item is method-neutral: two are arithmetic-adjacent slips, one
is a definitional gap that breaks Hare and Coombs equally, one is a redundant axiom in a theorem about
two-candidate majority rule, and the rest are citations. There is no item whose acceptance would make
any voting method look better or worse.

**That property is worth protecting, and there is now something that could cost it.**
[sep-star-suggestion-email](sep-star-suggestion-email.md) is a second draft to the same recipient,
asking him to consider covering the score-plus-runoff family in a future revision — a request, about
one method, carrying a disclosure. **Send this email first, on its own, and that one only if this
exchange goes somewhere.** Sent together, or in the other order, the disclosure attached to that email
colours these nine method-neutral items retroactively, which is precisely the failure the Lippman
email's disclosure was placed to avoid.

## What stayed cut

Three observations from the note that are **critiques rather than corrections**, and so do not belong
in an errata email:

1. **The resoluteness impossibility in §4.2 is proved with more than it needs.** On anonymized
   profiles — the entry's own §1.1 convention — the Condorcet component is fixed by the candidate
   rotation, so Neutrality alone kills Resoluteness and the three tables are unnecessary. The proof is
   correct as printed. Sending someone a shorter proof of their own lemma is a different email.
2. **The monotonicity example in §3.2 rests on a majority cycle**, which the text does not mention.
   That is an addition, not an error.
3. **No centre squeeze, and no domain restrictions.** The entry defines Hare, names it as
   Ranked-Choice Voting, lists it among the non-monotonic methods and never shows the failure mode
   that decided Alaska 2022; single-peakedness and Black's median-voter theorem appear nowhere in the
   body. Both are editorial scope decisions in a survey that is explicitly selective ("I focus on
   voting methods that either are familiar or help illustrate important ideas"). Not errata.

Item 1 is the one I most wanted to include and am least sure about cutting. It stays cut because the
email is asking for text changes, and "your proof is longer than necessary" is not a text change.

---

## The email

Subject: **Errata in "Voting Methods" (SEP), and one definitional gap**

---

Dear Professor Pacuit,

I keep a set of notes on voting methods in which every claim I record gets recomputed, and I recently
worked through your SEP entry that way — transcribing each printed profile and re-deriving every
winner, score and tally from it. Everything reproduces: the 21-voter opener, Condorcet's 81 voters,
the grading example and both of its manipulations, the Coombs districts, Zwicker's argument, the
multiple-elections and Ostrogorski profiles, and the impartial-culture figures (I get 21.4% and 25.1%
by simulation). I did not find an incorrect number anywhere in the entry.

I did find nine things that look like errors, and one that I think is a genuine definitional gap. The
script that checks all of this is at

  https://github.com/masiarek/set/blob/master/voting-notes/code/sep-voting-methods/verify.py

and it has no dependencies, if you would rather run it than take my word.

**1. §2.1 — the Hare and Coombs definitions elect nobody on the profile in §3.1.**

Both are stated with the convention "I assume that all of the poorly performing candidates will be
removed in each round," and both end "if there is no such candidate, then the remaining candidate(s)
are declared the winners."

On the Condorcet paradox profile of §3.1 —

    1 voter:  A B C
    1 voter:  B C A
    1 voter:  C A B

— every candidate has one first-place vote and one last-place vote. Round one deletes all three under
either rule, and the fallback clause has nothing left to name, so both methods return the empty set on
the entry's own flagship example.

This also touches the sentence just above: "If there are only three candidates, then the above two
voting methods are the same." Exhaustively over all 5,004 anonymized three-candidate profiles with one
to nine voters, Hare and Plurality with Runoff disagree on 501 of them, and in every single case the
disagreement is Hare returning nothing while the runoff returns the tied set. The smallest is two
voters, `1 B>C>A` and `1 C>B>A`: Hare deletes A, then deletes B and C together for want of a strict
majority. So the identification is exactly right wherever Hare is decisive, and the exceptions are
precisely the profiles the deletion rule empties.

The paragraph after the definitions already anticipates this — "An alternative approach would use a
tie-breaking rule to select one of the poorly performing candidates to be removed at each round" — so
perhaps the smallest fix is to add to that paragraph that under the convention adopted here a method
may eliminate every remaining candidate and return no winner, which is one reason the alternative is
usually preferred.

**2. §2.1 — the runoff transfers in the 19-voter example are stated the wrong way round.**

The text reads: "the groups voting for candidates C and D transfer their support to candidates B and
A, respectively, with A winning 10 – 9."

The runoff is A against B. The C-first group ranks `C D A B`, so it supports A; the D-first group
ranks `D B C A`, so it supports B. It should be "to candidates A and B, respectively." The total is
unaffected — 7 + 3 = 10 against 5 + 4 = 9 — since both halves of the pairing are transposed together.

**3. §4.1 — "two election scenarios with 7 voters and 3 candidates."**

The table below that sentence has five voters ranking four candidates, and all eight Borda scores
printed (9 / 5 / 10 / 6 and 9 / 6 / 8 / 7) are correct for five voters and four candidates. Only the
sentence needs changing.

**4. §4.2 — May's Theorem is stated with one axiom more than it needs.**

The entry gives it as Neutrality, Anonymity, Unanimity and Positive Responsiveness. May's 1952
statement uses three conditions, and Unanimity is not among them; it is implied by the others rather
than assumed. Enumerating every neutral rule on anonymized two-candidate profiles (ballots: A,
abstain, B; outcomes: A, B, tie) for electorates of three, four, five and six voters, exactly one rule
in each case satisfies Neutrality and Positive Responsiveness, and it is simple majority — adding
Unanimity eliminates nothing.

The biconditional as printed is of course still true. I mention it only because the point of a
characterisation theorem is which axioms are load-bearing, and a reader comparing this statement
against May's paper will find an axiom in one and not the other.

**5. §3.1.1 — Condorcet's 81-voter example does not instantiate the m = 3 case of Fishburn's theorem.**

The entry works the example, shows that a scoring rule can elect A only if s₂ > s₁, and then
introduces the theorem with "Peter Fishburn generalized this example as follows." The theorem asks for
at least m − 2 candidates with a **greater** score than the Condorcet winner, which at m = 3 means one
candidate strictly ahead under every scoring rule. On this profile, at s₁ = s₂ (2-approval), A and B
tie at 70, so no candidate is strictly ahead.

What the example establishes is the slightly weaker statement that A cannot be the unique winner under
any scoring rule with s₁ ≥ s₂ — which is exactly what the surrounding text argues, so the fix may be
just "generalized this phenomenon" or a word about strictness.

If it is useful, searching by electorate size, the smallest three-candidate profile that does
instantiate the theorem takes 11 voters:

    2 voters:  A C B
    3 voters:  B A C          C is the Condorcet winner: 6–5 over A, 6–5 over B
    2 voters:  B C A
    4 voters:  C B A

Here B has one more first place than C (5 to 4) and exactly as many seconds (4 each), so
Score(B) − Score(C) = 1 for every scoring vector, and no profile with ten or fewer voters does it.

**6. §4.2 — "voters" for "candidates", twice.**

In Faithfulness: "the winners are the set of voters chosen by that voter." And in the definition just
above the approval characterisation: "A variable domain voting method assigns a non-empty set of
voters to each anonymous profile — i.e., it is a function V : Π → ℘(X) − ∅", where X is the set of
candidates.

**7. §2.2 vs §4.2 — two conventions for the approval ballot set.**

§2.2 defines approval voting with "where the empty set means the voter abstains"; §4.2 sets up the
Fishburn/Alós-Ferrer characterisation with "the set of ballots B is the set of non-empty subsets of
the set of candidates … (selecting the ballot X consisting of all candidates means that the voter
abstains)." Both are standard and they agree on every winner, but the switch is silent, and
Faithfulness is stated in the vocabulary of the second while the method was defined in the first.

**8. §2.2 — "the voter in the middle column."**

Used twice for a voter who is the middle *row* of that table; the columns are the candidates.

**9. Bibliography.**

These are the citations I could not resolve against the reference list:

- "Chebotarev and Smais 1998" (§4.2) — the bibliography entry is Chebotarev and **Shamis**.
- "Balinksi" for Balinski, in §2.2 and §5.2.
- Young, "Condorcet's theory of voting," is listed as **1998**; *American Political Science Review*
  volume 82 is 1988, and the body cites "Young (1975, 1988, 1995)".
- **Young 1974** is cited in §4.2 with no entry in the bibliography.
- **Nurmi 1999** (§3) and **Nurmi 1998** (§5.2) are cited; the bibliography lists only Nurmi 1987.
- **Posner and Weyl 2018** (§2.3, cited twice, presumably *Radical Markets*) — the bibliography has
  Posner and Weyl 2015 and 2017 only.
- **Lalley and Weyl 2018b** (§2.3) — the bibliography has 2018a only.
- **Bloembergen, Grossi and Lackner 2018** (§2.3) — no entry; Lackner does not appear in the
  bibliography at all.
- **Ostrogorski 1902** (§3.4) — no entry. The only occurrence of the name in the bibliography is
  inside the title of Rae and Daudt 1976.
- **Brams and Sanver 2009** (§2.2) — the bibliography entry for "Voting systems that combine approval
  and preference" carries no year.
- "Fabienne 2017" (§2.3) is listed as "Fabienne, P., 2013" — the author of the SEP *Political
  Legitimacy* entry is Fabienne **Peter**, and the text year, the bibliography year and the archive
  URL (sum2017) give three different dates.

Thank you for the entry — it is the piece I send people who want the axiomatic side of this without a
textbook, and §4.3 in particular has no substitute I know of.

Best regards,
Adam Masiarek
