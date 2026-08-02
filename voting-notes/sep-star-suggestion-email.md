# Suggestion email — STAR and the score-plus-runoff gap in the SEP "Voting Methods" entry

Companion to [sep-voting-methods.md](sep-voting-methods.md).

**Status: drafted, not sent.** One ask, four supporting facts, and a paragraph conceding the weakest
part of the case before the recipient can find it. See *What stays out* for the three arguments that
were available and were cut.

## Where it goes

- **To: `epacuit@umd.edu`** — Eric Pacuit, Department of Philosophy, University of Maryland; author of
  the entry. SEP's editorial policy puts maintenance on authors — *"It remains the responsibility of
  authors to maintain their entries and to keep them current"* — and explicitly invites this kind of
  mail: *"Readers of the Encyclopedia are encouraged to contact authors directly with comments,
  corrections, and other suggestions."*
- **No cc to `editors@plato.stanford.edu`.** That address exists for editorial concerns about whether
  an entry meets the Encyclopedia's standards, and the Principal Editor's role is to adjudicate
  *criticisms* and negotiate revision schedules. This is a coverage suggestion about one paragraph.
  Copying the editors on it would read as escalation over a request, and would earn the reply it
  deserved.

Routing is simpler than the Lippman case: there is no downstream copy of an SEP entry to keep in sync.
The author revises the live text or nobody does.

## Sequencing: send the errata email first, and alone

There is already a second email to the same person —
[sep-voting-methods-errata-email](sep-voting-methods-errata-email.md), nine items, Gmail draft created,
not sent. **These must not go out together, and this one must not go first.** Three reasons, and the
third is the one that matters:

1. The errata email is **method-neutral and carries no disclosure**, by its own explicit reasoning: no
   item there makes any voting method look better or worse. That property is worth something, and it
   is destroyed by arriving alongside an email about STAR from someone who contributes to STAR
   software.
2. Bundled into one message, a clean errata report becomes the preamble to an advocacy request. That
   is the exact trade the [Lippman errata email](math-in-society-errata-email.md) refused when it cut
   its score-voting item.
3. **Retroactive discredit is the real risk.** The Lippman note put it plainly about its own
   disclosure: *discovered later, it discredits the other items retroactively.* Here the same logic
   runs forward in time. Nine corrections accepted on their merits, followed weeks later by a coverage
   request with a disclosure attached, reads as a careful reader who also has a view. The reverse
   order reads as an advocate who softened you up first.

So: errata first, wait for a reply or a decent interval, and send this one only if that exchange went
somewhere. If the errata email gets no response at all, this one is probably not worth sending either
— and that is information, not a setback.

## This is a request, not a correction — and that was cut once already

[math-in-society-errata-email](math-in-society-errata-email.md) had a fourth item asking Lippman to
consider covering score voting, and it was cut, on the grounds that it converted a correction into a
request. That reasoning was right there and is worth re-testing here, because this email is *only* the
request. Three things distinguish the cases:

1. **A survey's job is coverage.** A gen-ed textbook chapter that omits a method has made a scope
   decision. An encyclopedia entry titled "Voting Methods", organised as a taxonomy of the field, that
   omits a family of methods has a gap in the map. The complaint is about the map, not the territory.
2. **The remix escape doesn't exist here.** Lippman's book is CC BY-SA on a platform built for
   remixing, so the honest answer was "fork it". SEP entries are single-author, refereed and not
   remixable. Contacting the author is the only route, and the policy says so.
3. **The facts are new since the last revision.** The entry's substantive revision is 24 June 2019.
   The peer-reviewed paper is 2023. The author's own software implementation is later still. In 2019
   there was nothing to ask for.

## What the email rests on — four checkable facts

1. **A hole in the entry's own taxonomy.** §2.1 covers multi-stage methods (Plurality with Runoff,
   Hare, Coombs); §2.2 covers grading methods (Approval, k-Approval, Score, Cumulative, Negative,
   Majority Judgement). Nothing in the entry occupies the cell where a grading ballot feeds a second,
   pairwise stage. This holds whatever anyone thinks of STAR, and it is the actual ask.
2. **Peer-reviewed literature that postdates the revision.** Wolk, Quinn & Ogren, "STAR Voting,
   equality of voice, and voter satisfaction: considerations for voting method reform,"
   *Constitutional Political Economy* **34**(3): 310–334 (2023), doi:10.1007/s10602-022-09389-3 — the
   same volume of the same journal as Holliday & Pacuit, "Stable Voting," *CPE* **34**: 421–433
   (2023), doi:10.1007/s10602-022-09383-9. The email states the coincidence once, flatly, and does not
   lean on it. There is also a published correction to the STAR paper
   (doi:10.1007/s10602-023-09426-9); the email flags its existence rather than letting him find it.
3. **His own package already implements STAR.** `pref_voting` (Holliday & Pacuit, *JOSS* 2025) —
   `pref_voting/grade_methods.py`, `@vm(name="STAR")`, docstring pointing at `starvoting.us`, with
   parallel-universe tiebreaking for the runoff seeding. Verified by reading the file, not the docs.
   This is the strongest fact in the email because it removes the "unfamiliar method" reply entirely.
4. **The entry already raises the problem the family answers.** §2.2 notes score voting's exposure to
   strategic exaggeration. The runoff stage is the designed response. Offering the arithmetic is a
   gift rather than an argument.

## What stays out, and why

- **Adoption momentum. There is none, and claiming it would end the conversation.** Lane County 2018
  failed 47.6–52.4; Eugene's council deadlocked 4–4 in 2020 with the mayor breaking it against
  referral; Eugene Measure 20-349 was defeated in May 2024; Oakridge Measure 20-364 was defeated in
  November 2024 at ~46%; the 2024 statewide Oregon initiative never qualified for the ballot. Actual
  use is confined to party-internal elections — Multnomah County Democrats 2019, Independent Party of
  Oregon 2020, Democratic Party of Oregon delegate elections 2020, Libertarian Party of Oregon from
  2023. **The email states this itself, in its own voice, before he can look it up.** A recipient who
  finds the record after reading an email that implied otherwise discards the other three facts too.
- **VSE and Bayesian-regret superlatives.** [cardinal-voting-systems](cardinal-voting-systems.md)
  already convicts an advocacy page of an uncited Bayesian-regret superlative and a STAR VSE figure
  cited to the simulation tool that produced it. Sending a specialist a number with that provenance,
  in his own field, would be worse than sending nothing.
- **Any claim that STAR is better than what the entry covers.** Not the ask, and not an argument worth
  having by email with someone who writes axiomatic characterisations for a living.
- **The ordinal-framing observation** that is section 1 of the note. It is the honest *diagnosis* of
  why the taxonomy has this hole, but stated to the author it becomes a lecture on his own framing
  from a stranger. It survives as a single subordinate clause and nothing more.
- **The 185-check verifier as a credential.** It opens the email as a fact about how the entry was
  read, and is offered at the end as something he might want. It is not used to buy standing.

## The COI disclosure goes in paragraph two, not at an item

The Lippman email put its disclosure at item 3 and left the header clean, because items 1, 2 and 4 were
method-neutral and a top-level disclosure would have coloured them for nothing. That reasoning
inverts here: **this email is about one method, promoted by an organisation whose software Adam
contributes to, and there is no neutral remainder to protect.** Late disclosure in a single-topic
advocacy-shaped email reads as concealment. Early, it costs one sentence and buys the rest.

---

## The email

Subject: **A gap in the taxonomy of "Voting Methods": grading ballots with a second stage**

---

Dear Professor Pacuit,

I have spent the past week working through your SEP entry on voting methods, checking it
computationally as I went — the 21-voter opening example, Borda's 1784 case, the Hare/Coombs/Runoff
comparison on 19 voters, Condorcet's 81 voters and Saari's decomposition of them, the monotonicity and
no-show and multiple-districts profiles, May's theorem, Moulin's threshold, and the impartial-culture
cycle rates. 185 checks, no discrepancies with the entry. I have not read a survey in this area that
held up as well, and I am grateful for it.

A disclosure before the substance, because everything below concerns one method: I am a volunteer
contributor to BetterVoting, election software maintained by the Equal Vote Coalition, which advocates
for STAR voting. Please weigh what follows accordingly. I have tried to restrict myself to things you
can check in a few minutes.

**The suggestion concerns the entry's taxonomy rather than any method's merits.** §2.1 covers
multi-stage methods — Plurality with Runoff, Hare, Coombs — where a first stage narrows the field and a
later stage decides. §2.2 covers grading methods — Approval, k-Approval, Score, Cumulative, Negative
Voting, Majority Judgement — where the ballot carries grades rather than a ranking. The entry has no
cell where the two meet: no method that takes a grading ballot, uses the grades to narrow the field,
and then decides by pairwise majority.

That cell now has occupants. STAR (Score Then Automatic Runoff) sums 0–5 grades, advances the top two,
and elects whichever of them more voters graded above the other; Smith//Score and 3-2-1 voting are
variations on the same score-then-pairwise idea. One of them is implemented in your own `pref_voting`
package — `grade_methods.py`, `@vm(name="STAR")`, with parallel-universe tiebreaking for the runoff
seeding. Since the entry's last substantive revision is June 2019 and the package is later, I assume
that is the entire explanation, and I mention it only because it means I am not proposing an
unfamiliar method.

Two things have changed since 2019 that might make the family worth a paragraph.

**A peer-reviewed treatment now exists.** Sara Wolk, Jameson Quinn and Marcus Ogren, "STAR Voting,
equality of voice, and voter satisfaction: considerations for voting method reform," *Constitutional
Political Economy* 34(3):310–334 (2023) — as it happens the same volume as your and Wes Holliday's
"Stable Voting," at 421–433. I do not think it is the last word on the method, and in fairness it
carries a published correction (doi:10.1007/s10602-023-09426-9); its central metrics, Voter
Satisfaction Efficiency and Pivotal Voter Strategic Incentive, are simulation-based and inherit the
usual questions about the electorate model. But it is the kind of citation the entry's bibliography is
made of, and it did not exist when you last revised.

**And the entry already raises the problem the family is designed to answer.** §2.2 notes score
voting's exposure to strategic exaggeration. That exposure is not marginal. On the standard
five-city example — not one of yours — sincere 0–10 grades elect the Condorcet winner 603 to 457,
while the same voters with the same underlying preferences, each min-maxing (top score to everyone
above their own mean, zero to the rest), elect the Condorcet *loser* 42 to 41. Nothing changes but the
strategy, and the result is the plurality winner. The second stage exists to remove the payoff from
that exaggeration: once the top two are fixed, only the relative order of those two matters, and
inflating a grade cannot help. Whether it succeeds is an empirical question I am not qualified to
settle. But it is a response to a problem the entry itself states, which is more than can be said for
most proposals.

**What I am not claiming, since you would find it out anyway.** STAR has no governmental adoption
anywhere in the world. Lane County, Oregon rejected it in 2018 at 47.6%; Eugene's council deadlocked
in 2020 and the mayor broke the tie against referral; Eugene voters defeated Measure 20-349 in May
2024; Oakridge voters defeated Measure 20-364 that November at about 46%; the 2024 statewide Oregon
initiative failed to qualify. Its actual use is confined to internal party elections in Oregon. If
the entry's threshold for inclusion is real-world use, this family does not meet it, and I would not
argue that it does. I raise the family because the taxonomy has a hole in it, and I think a reader is
currently left with the impression that grading methods and multi-stage methods are disjoint kinds —
which is, I suspect, an artefact of how naturally the field's framework fits preference orderings.

So the ask is a small one: a sentence or two in §2.2 observing that a grading ballot can feed a second
pairwise stage, naming STAR as the instance with a literature behind it, and citing Wolk et al. If it
warrants more than that, you are far better placed than I am to judge how much.

Two offers, either or both. The verification script is a single dependency-free Python file that
transcribes every profile in the entry and recomputes every winner, tally and theorem instance it
asserts — including exhaustive checks of the anonymity/neutrality/resoluteness impossibility and of
Moulin's threshold, where minimax survived all 12,369 three-candidate profiles up to 11 voters while
Black's procedure fails at 3 candidates and 8. You are welcome to it, for whatever it is worth as an
independent check, or to ignore it. And if a paragraph on score-plus-runoff methods would be useful
but not worth your time to draft, I am happy to write a draft you can discard or rewrite entirely.

Thank you again for the entry — and for `pref_voting`, which I have been using. I am equally happy to
be told I have misread the entry's intended scope.

Best regards,

Adam Masiarek

---

## If he says no

Two replies are likely and both are fine.

- *"Out of scope — the entry covers methods with an established literature and practice."* That is a
  defensible line, and the adoption paragraph has already conceded the ground it stands on. No reply
  needed beyond thanks.
- *"The framework is about preference aggregation from orderings."* This is the interesting answer,
  and the right response is not to argue but to ask whether §2.2's grading methods sit comfortably
  inside that framework either — which is the question [sep-voting-methods](sep-voting-methods.md)
  section 1 is about, and worth more as a question than as an assertion.

## Related local material

- [sep-voting-methods](sep-voting-methods.md) — the note on the entry, and the verifier offered here
- [`code/sep-voting-methods/verify.py`](code/sep-voting-methods/verify.py) — the 185 checks
- [math-in-society-errata-email](math-in-society-errata-email.md) — the precedent, including the
  score-voting ask that was cut from it and the reasoning that was re-tested here
- [score-voting](score-voting.md) — the sincere-vs-min-max arithmetic quoted in the email, verified
- [cardinal-voting-systems](cardinal-voting-systems.md) — why the VSE and Bayesian-regret figures
  stayed out
- [star-voting](star-voting.md) — the method itself
