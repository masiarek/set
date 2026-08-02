# Math in Society (Lippman) — chapters 2–4

Source: David Lippman, *Math in Society* ([LibreTexts](https://math.libretexts.org/Bookshelves/Applied_Mathematics/Math_in_Society_(Lippman)),
CC BY-SA 3.0), chapters 2 (Voting Theory), 3 (Weighted Voting), 4 (Apportionment).
Compiled PDF read 2026-08-01; tables taken from the live HTML, because the PDF renders them as images.

Every number below is checked by [`code/math-in-society/verify.py`](code/math-in-society/verify.py)
(no dependencies, `python3 verify.py`). 39 checks, all passing.

## What it's about

The standard American gen-ed maths textbook treatment of voting — the one a non-major actually
meets. Chapter 2 walks plurality → IRV → Borda → Copeland, introducing one fairness criterion per
failure, and closes on Arrow. Chapters 3 and 4 are territory these notes had not touched at all:
**power indices** (Banzhaf, Shapley–Shubik) and **apportionment** (Hamilton, Jefferson, Webster,
Huntington–Hill, Lowndes).

Chapter 2 is mostly a retread of [legrand](legrand-ranked-ballot-methods.md) and
[lumen](lumen-75-ballot-four-winners.md) with better prose and fewer methods. The value is in three
places: one misstated theorem that matters, one worked example that is a gift, and — in chapters 3
and 4 — a second impossibility theorem, also misstated, in a literature adjacent to everything else
here.

## The headline: two impossibility theorems, both overclaimed

### Arrow, stated without the ordinal restriction (§2.12)

> "Arrow's Impossibility Theorem states, roughly, that it is not possible for a voting method to
> satisfy every fairness criteria that we've discussed."

Attributed to Kenneth Arrow, "in 1949." Three problems, in increasing order of importance:

- **The date.** The standard citations are the 1950 *JPE* paper and the 1951 book. 1949 is when the
  RAND work was written up; no one cites it that way.
- **The criteria.** The ones "we've discussed" are Condorcet, monotonicity, majority and IIA. Arrow's
  theorem uses unrestricted domain, Pareto, IIA and non-dictatorship. Only IIA is shared.
  [glossary.md](glossary.md) already states it correctly.
- **The scope — this is the one that matters.** Arrow's theorem is about **ranked** methods. The book
  says "a voting method," full stop, and then §2.13 introduces **approval voting** on the very next
  page. A student reading straight through concludes Arrow has just ruled out the cardinal method
  they are about to be taught. It has not: approval and score take non-ordinal input, which is
  exactly the hypothesis Arrow's theorem needs. The result that does constrain cardinal methods is
  Gibbard–Satterthwaite / Gibbard 1977, and it is about strategyproofness, not fairness criteria.

This is a **live** error, not an artefact of an old PDF — the LibreTexts page reads the same today
(fetched 2026-08-01).

The sequencing makes it worse than a loose sentence. §2.12 is titled *"So Where's the Fair Method?"*
and answers "there isn't one, and here is the theorem." §2.13 then presents approval as one more
method that also fails. The chapter never tells the student that the impossibility it just invoked
does not reach past §2.12.

### Balinski–Young, refuted by Balinski and Young (§4.4)

> "The Balinski-Young Impossibility Theorem shows that any apportionment method which always follows
> the quota rule will be subject to the possibility of paradoxes like the Alabama, New States, or
> Population paradoxes."

The genuine theorem is **quota + population monotonicity is impossible**. Quota + *house*
monotonicity — that is, satisfying quota while never suffering the **Alabama paradox** — is perfectly
achievable, and Balinski and Young built such a method themselves: the **Quota method**, *Amer. Math.
Monthly* 82 (1975). Still, *Math. of OR* 4 (1979), characterises the entire class of house-monotone
methods satisfying quota. So the textbook's version is contradicted by the same two authors it names.

The verifier demonstrates this constructively on **the book's own exercise 9** (populations 6000,
6000, 2000):

| house size | Hamilton | C's seats |
|---|---|---|
| 10 | (4, 4, 2) | 2 |
| 11 | (5, 5, 1) | **1** |

Hamilton satisfies quota at both sizes and still loses C a seat as the house grows — the Alabama
paradox, which is what exercise 9c is asking for. But the book's blanket claim says *any*
quota-following method must be exposed to this, and on this instance that is false:

    (4,4,2) at h=10   →   (5,4,2) at h=11

Both satisfy quota; nobody loses a seat. Exhaustive search confirms a quota-satisfying,
house-monotone chain exists for every house size 1–11 here, and for all 300 random instances tested.
Hamilton has the Alabama paradox; **satisfying quota is not what causes it**.

### The connection worth keeping

The Balinski of chapter 4 is **Michel Balinski** — the same Balinski as Balinski & Laraki in
[majority-judgment.md](majority-judgment.md). Chapter 4's impossibility and MJ's point-summing
theorem are one person's two results, in two literatures these notes had been treating as unrelated.

## Chapter 2: the two examples worth taking

### Example 4 — the Condorcet winner with the *fewest* first preferences (§2.4)

|  | 342 | 214 | 298 |
|---|---|---|---|
| 1st | Elle | Don | Key |
| 2nd | Don | Key | Don |
| 3rd | Key | Elle | Elle |

854 voters. Verified:

- **Plurality elects Elle** on 342/854 = **40.05%**, a minority.
- **IRV elects Key** — Don is eliminated first and transfers to Key.
- **Don is the Condorcet winner**, 512–342 over Elle and 556–298 over Key.
- Don's first-place count is **214 = 25.06%**, strictly the **smallest in the field**.

This is FairVote's "core support" argument sitting in a gen-ed textbook with the arithmetic already
done: a candidate with a quarter of the first preferences, last on that measure, who beats everyone
head to head. [rcv-and-core-support.md](rcv-and-core-support.md) argues that first-preference counts
cannot define core support coherently; this is the cleanest single profile for making that concrete,
and it comes from a source with no stake in the fight.

The book's own framing is notable: it presents this as a *plurality* failure and a *vote-splitting*
story (two Democrats, one Republican), then in §2.7 observes that IRV fails the Condorcet criterion
here too — but treats that as the price of removing the incentive for insincere voting, not as a
problem. It never remarks that its Condorcet winner is last on first preferences.

### Example 13 — the approval "majority failure" is a cutoff artefact (§2.14)

The book's stated lesson is "Approval voting can very easily violate the Majority Criterion."

|  | 80 | 15 | 5 |
|---|---|---|---|
| 1st | A | B | C |
| 2nd | B | C | B |
| 3rd | C | A | A |

A holds a **strict majority** of first preferences (80/100) and is also the Condorcet winner. Then:

> "suppose that this election was held using Approval Voting, and **every voter marked approval of
> their top two candidates**."

| cutoff | A | B | C | winner |
|---|---|---|---|---|
| top two (the book's) | 80 | **100** | 20 | **B** — majority criterion fails |
| bullet vote | **80** | 15 | 5 | **A** — majority criterion holds |
| approve all | 100 | 100 | 100 | three-way tie, no winner |

Same preferences, same tabulation rule, three different answers. The violation is produced entirely
by the **assumed cutoff**, not by approval voting.

This is exactly the finding in [approval-voting.md](approval-voting.md) — that approval's criterion
compliance is a property of *how voters set their cutoff* rather than of the tabulation — and this is
the best specimen of it yet. Better than the [Lumen](lumen-75-ballot-four-winners.md) one, because
the book *states its assumption in the sentence* and still reports the outcome as a property of the
method. The assumption is doing all the work and is presented as scene-setting.

Worth being fair about: the book is not wrong that approval *can* fail majority. It is wrong to
demonstrate it this way without noting that the same profile passes under a different cutoff — which
is the actual interesting fact.

## Chapter 3: power indices (new territory)

Banzhaf — **Penrose 1946, reintroduced by Banzhaf 1965** (the book gets this lineage right, which is
better than most treatments). Shapley–Shubik 1954. Vocabulary: dictator, veto power, dummy, coalition,
critical player, pivotal player.

**Nassau County (§3.4, Example 7)** is the set piece, and it checks out exactly: `[58: 31, 31, 28, 21, 2, 2]`.
The three large districts are critical 16 times each — **1/3 of the power apiece** — and the three
small ones are critical **zero** times. North Hempstead holds **18.3% of the weight and 0% of the
power**. This is the cleanest demonstration in any of these notes that a proportionally-assigned
weight and actual influence are different quantities.

### The Scottish Parliament example drops a sitting MSP (§3.4, Example 6)

The book gives `[65: 47, 46, 17, 16, 2]` for the 2007 parliament — SNP, Labour, Conservative,
LibDem, Green. That totals **128**. The Scottish Parliament has **129** seats: the 2007 election also
returned one **independent, Margo MacDonald**.

Computed both ways:

| | SNP 47 | Lab 46 | Con 17 | LD 16 | Grn 2 | Ind 1 |
|---|---|---|---|---|---|---|
| book, total 128 | 1/3 | 7/27 | 5/27 | **1/9** | **1/9** | — |
| actual, total 129 | 9/28 | 1/4 | 5/28 | **3/28** | **3/28** | **1/28** |

The book's punchline **survives** — its point is that the LibDems (16 seats) and the Greens (2 seats)
have *identical* Banzhaf power, and they still do once the independent is restored. So this is an
erratum, not a broken lesson.

But the dropped member is **not a dummy**: critical in 2 winning coalitions, **1/28 ≈ 3.6%** of the
power — more than a third of what the 16-seat LibDems hold. In a chapter whose entire subject is that
small players can have zero power, silently deleting the smallest player is an unfortunate place to
be imprecise.

### Smaller: §3.2 contradicts itself on the quota bound

The definition box says the quota must be **more than** half the total weight. The explanation one
line later says "the quota must be **at least** half." The book's own example, `[3: 3, 2, 1]` with
total weight 6, is precisely the counterexample to "at least" — quota 3 is exactly half, and both a
yes-coalition and a no-coalition reach it, which is the situation the rule exists to prevent.

## Chapter 4: apportionment (new territory)

Hamilton, Jefferson, Webster, Huntington–Hill, Lowndes; the quota rule; the Alabama, New States and
Population paradoxes; gerrymandering. Beyond the Balinski–Young overclaim above:

**Two dates off by one, in the same direction.**

- "[Hamilton's] method was approved by Congress in 1791, but was vetoed by President Washington."
  The bill passed the House **21 Feb 1792** and the Senate **12 Mar 1792**; Washington vetoed it
  **5 April 1792** — the first presidential veto in US history.
- "Jefferson's method was adopted, and used in Congress from **1791** through 1842." The replacement
  act was signed **14 April 1792**.

**A claim worth flagging as unverified.** §4.4: "if Webster's method had been applied to every
apportionment of Congress in all of American history, it would have followed the quota rule every
single time." This is Balinski & Young's, and plausible, but the book gives no citation and I have
not checked it against the census series. Not recorded as fact here.

**Adams's method** appears only in exercise 17, unnamed in the body — worth knowing the book has the
divisor-method family nearly complete (Adams, Jefferson, Webster, Huntington–Hill) but only names
three.

## What the book does not contain

Grepped the full text: **no STAR, no score, no range, no majority judgment, no Condorcet method
beyond Copeland.** Approval is the only cardinal method in the book and occupies two short sections,
one of which is the flawed majority-criterion demonstration above. The Schulze method appears once,
as exercise 10 in §2.18, as a research prompt.

So the cardinal family is represented by its weakest member, argued against with its weakest
argument, immediately after an impossibility theorem that has been stated in a way that appears to
condemn it. That is not advocacy on the book's part — chapter 2 is even-handed and the IRV section is
franker about IRV's failures than most — but it is the net effect.

## Cross-references

- [glossary.md](glossary.md) — Arrow (stated correctly there), Condorcet winner, IIA, monotonicity;
  needs **Banzhaf index**, **Shapley–Shubik index**, **quota rule**, **Alabama paradox**,
  **Balinski–Young** added.
- [rcv-and-core-support.md](rcv-and-core-support.md) — Example 4 is the ideal worked profile.
- [approval-voting.md](approval-voting.md) — Example 13 is the cutoff-indeterminacy finding in the wild.
- [majority-judgment.md](majority-judgment.md) — same Balinski.
- [whoops.md](whoops.md) — the Arrow scope error and the Balinski–Young overclaim both belong there.
- [math-in-society-errata-email.md](math-in-society-errata-email.md) — draft correspondence.

## Sources

- [*Math in Society*, chapter 2: Voting Theory](https://math.libretexts.org/Bookshelves/Applied_Mathematics/Math_in_Society_(Lippman)/02:_Voting_Theory)
- [§2.12: So Where's the Fair Method?](https://math.libretexts.org/@go/page/36255) — the Arrow statement
- [§2.14: What's Wrong with Approval Voting?](https://math.libretexts.org/@go/page/36257) — Example 13
- [§3.4: Banzhaf Power Index](https://math.libretexts.org/@go/page/34186) — Nassau County, Scottish Parliament
- [§4.4: Webster's Method](https://math.libretexts.org/Bookshelves/Applied_Mathematics/Math_in_Society_(Lippman)/04:_Apportionment/4.04:_Websters_Method) — the Balinski–Young statement
- Balinski & Young, "The Quota Method of Apportionment", *Amer. Math. Monthly* 82 (1975), 701–730
- [Still, "Quotatone Apportionment Methods", *Math. of OR* 4 (1979), 31–39](https://pubsonline.informs.org/doi/10.1287/moor.4.1.31) — characterises all house-monotone methods satisfying quota
- [AMS Feature Column: Apportionment — Balinski and Young's contribution](https://www.ams.org/publicoutreach/feature-column/fcarc-apportionii3)
- [Apportionment Act of 1792](https://en.wikipedia.org/wiki/Apportionment_Act_of_1792) — the veto dates
- [2007 Scottish Parliament election](https://en.wikipedia.org/wiki/2007_Scottish_Parliament_election) — 129 seats, incl. one independent
