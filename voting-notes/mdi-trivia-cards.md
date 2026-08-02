# Institute for Mathematics and Democracy — "Math and Politics Trivia"

<https://mathematics-democracy-institute.org/math-and-politics-trivia/> (IMD, Wellesley College)

A set of **53 infographic cards** in six categories, each a 1600×900 PNG: a definition, a worked
example, and a "find the answer at …" pointer. It is gen-ed outreach material, pitched a long way
below these notes — but three of the six categories are subjects these notes barely touch, and the
card set is the tidiest one-screen index of them I've found.

All 53 saved locally (the pages are image-only; the text is inside the PNGs and not scrapeable):

| Category | Cards | Local |
|---|---|---|
| Voting and Elections | 19 | `img/mdi-trivia/` |
| Apportionment | 12 | `img/mdi-apportionment/` |
| Quantification of Power | 7 | `img/mdi-power/` |
| Gerrymandering | 6 | `img/mdi-gerrymandering/` |
| Social Choice Theory | 6 | `img/mdi-social-choice/` |
| Electoral College | 3 | `img/mdi-electoral-college/` |

## Is any of it new? Almost none of it.

Dated by WordPress upload path (`/wp-content/uploads/YYYY/MM/`), which is when each card was
published:

| Uploaded | What appeared |
|---|---|
| 2021-11 | the six category hub cards |
| 2021-12 | the bulk — 13 voting cards, 10 apportionment, 5 power, 5 gerrymandering, 4 social choice |
| 2022-01 | STV, Center Squeeze, Banzhaf (revised) |
| 2022-02 | one gerrymandering card |
| 2022-03 | Duverger's Law |
| 2022-05 | Ties in the Electoral College, Banzhaf vs. Shapley–Shubik |
| 2022-06 | Prisoner's Dilemma |
| 2022-07 | Pareto vs. Unanimity, Tragedy of the Commons |
| 2022-08 | Tiebreakers in American Elections, **Antiplurality** — last new card in the voting set |
| 2023 | nothing |
| 2024-12 | **Population Paradox, corrected** — the only asset added to the whole trivia section since Aug 2022 |
| 2025–2026 | nothing |

So: the series ran hard for ten months, stopped in August 2022, and has been touched exactly once
since — a correction, not a new topic. Checked by grepping every asset reference on all six pages
for a 2023-or-later upload path; the Dec 2024 pair are the only hits.

### The one 2024 change, verified

`Population-Paradox-Corrected-1.png` replaces the original card. Its example: 24 seats; states
A 5,300, B 9,900, C 22,400. Standard divisor s = 37,600/24 = 1,566.67, quotients 3.383 / 6.319 /
14.298, lower quotas 3+6+14 = 23, and the single surplus seat goes to A on the largest remainder →
**(4, 6, 14)**. Then A grows 26%, B 25%, C 16%:

```
new populations   6,678 / 12,375 / 25,984      s = 45,037/24 = 1,876.54
quotients         3.5587 / 6.5946 / 13.8467    lower quotas 3+6+13 = 22
two surplus seats → C (.847) and B (.594)  →   (3, 7, 14)
```

**A loses a seat while growing fastest of the three.** The card is right and the example is a clean
one. Minor slip survives into the corrected version: the answer table prints the post-growth
quotients as 3.57 / 6.61 / 13.81, where the stated percentages give 3.5587 / 6.5946 / 13.8467. The
seat outcome is unaffected — the two largest remainders are C then B either way.

Worth knowing what was wrong *before* December 2024, and I can't tell from the outside: the
pre-correction card isn't in the media library any more, only its replacement.

### A topic announced and never shipped

The apportionment sidebar lists **"What is the Cube Root Law?"** — the proposal that a legislature
should have roughly the cube root of its population (≈693 seats for the US today, against the 435
frozen in 1929). There is no card, no section, and no other occurrence of the string on the page.
It is the only listed topic with nothing behind it, which is probably where the series stopped.

## What's actually new relative to `glossary.md`

Checked term by term against the glossary and the rest of the notes. Absent everywhere — the first
four have since been written up, the rest are still gaps:

- **May's Theorem** — anonymity + neutrality + monotonicity ⇒ a *quota method* for two candidates;
  add "nearly decisive" and the quota is forced to exactly half, i.e. simple majority. It's the
  natural floor under everything else — the one case where "which method?" has a proved answer, and
  the reason the rest of the subject is really a consequence of having three or more candidates.
  **Now in `glossary.md` §9**, along with anonymity, neutrality and near-decisiveness in §5, which
  the glossary had been using without defining. Two things the card glosses over and the glossary
  entry doesn't: May's 1952 statement uses *positive responsiveness*, strictly stronger than plain
  monotonicity, and the quota-method family is what the weaker version buys; and "quota method"
  collides with two unrelated senses of "quota" already in §4 and §8.
- **Duverger's Law** — plurality tends to two parties; the companion *hypothesis* is that PR tends
  to more. Nothing here named it, though `lesser-evil coordination pressure` and `candidate
  saturation` in §6 are its mechanism at the scale of a single election. **Now in `glossary.md`
  §6**, with the standing exceptions (Canada, India, the pre-2015 UK) noted — the mechanism is
  durable, the prediction isn't.
- **Antiplurality** — fewest last-place votes wins; previously only a passing mention in the
  Wikipedia talk draft. Coombs' scoring rule without the elimination, and the card's own example is
  a good one: 42 `A>B>C>D`, 26 `B>C>D>A`, 15 `C>D>B>A`, 17 `D>C>B>A` → A is last on 58 ballots, B
  and C on none, so the rule ties immediately and the card re-runs it head-to-head (C is below B on
  68) → **B wins, where plurality elects A on 42 first preferences**. **Now in `glossary.md` §4**
  under Point count, next to Borda, since it's the positional rule (1, …, 1, 0) — plurality's mirror
  image with Borda at the midpoint. Two things worth more than the card gives them: that immediate
  tie is structural, not bad luck (*n* voters supply only *n* last-place votes, so most of a field
  larger than three sits on zero), and antiplurality **can elect the Condorcet loser** —
  `2:B>A>C, 2:C>A>B, 1:C>B>A` elects A, who loses 3–2 to both rivals, because A is second on four of
  five ballots. Borda is the only positional rule that never does that, which turns the mirror-image
  framing into an actual argument for the middle of the family.
- **Discrete cumulative voting** — cumulative voting with indivisible tokens rather than a
  fractional budget. My first pass said §4 already had cumulative voting and only lacked the
  discrete variant; that was wrong. The **Cumulative** heading in §4 covers Bucklin's cumulative
  *tallying* of preference levels, an unrelated sense, and cumulative voting had no entry at all
  beyond a passing (1, ½, ⅓, …) in §5. **Both are now in `glossary.md` §4** under Multi-winner,
  next to SNTV — which is what cumulative voting generalizes — with the three-way collision on the
  word "cumulative" flagged, the VRA-remedy and Illinois 1870–1980 history, and the reason the
  discrete form is the one actually deployed: fractional budgets that fail to sum to 1 are how these
  elections generate invalid ballots.
- **Electoral College mechanics** — the "+2 effect" (two senatorial electors regardless of size)
  and the 12th-Amendment contingent election on a tie. `whoops.md` has plenty of misfiring
  elections but nothing on this.
- **Gerrymandering metrics** — packing and cracking, the **efficiency gap**, the **Polsby–Popper
  compactness score**, and the National Popular Vote Interstate Compact. Districting is the one
  major area of the subject these notes have no entry for at all.
- **Paradox of Positive Association** — Saari's name for what §5 calls monotonicity failure. A
  synonym worth having in the glossary, since it's how the older literature indexes it.
- **Prisoner's Dilemma / Tragedy of the Commons** — game theory rather than social choice, and the
  only two cards with no bearing on anything here.
- **Named divisor methods** — Jefferson, Adams, Webster, Dean, Huntington–Hill each get a card with
  worked arithmetic. §8 has "divisor methods" generically plus Balinski–Young; the individual
  rounding rules (floor / ceiling / arithmetic mean / harmonic mean / geometric mean) aren't spelled
  out, and the Lippman note used them without naming the pattern.
- **Cube Root Law** — name only, see above.

Already covered here and covered better: Arrow, IIA, Pareto, Gibbard–Satterthwaite, Banzhaf,
Shapley–Shubik, weighted voting, the Alabama / population / New States paradoxes, Balinski–Young,
and every method on the voting page.

## Flags on the voting cards

The prose sections under the cards are advocacy-shaped, and several claims are ones these notes
already have counterexamples for:

- **"Fargo, MN"** — Fargo is in North Dakota. Doubly stale: per `approval-voting.md`, North Dakota
  banned approval voting in April 2025, so Fargo no longer uses it at all.
- **"In 2020, RCV is on the ballot in Massachusetts and Alaska"** — present tense, six years old.
  (MA Question 2 failed, AK Measure 2 passed.)
- **"Unless there is a tie, the winner will receive the majority of votes"** — true only of
  *continuing* ballots. Exhausted ballots are in the glossary for this reason.
- **"Ranked choice voting avoids the spoiler effect"** — Alaska 2022, in `whoops.md`, is the
  counterexample; the site's own Center Squeeze card describes the mechanism that refutes it.
- **"[Approval] is not susceptible to strategic voting"** — flatly wrong, and the thesis of
  `approval-voting.md` is the opposite: approval's criterion compliance is a property of where
  voters set their cutoff, which is the strategic choice. Cf. 79% bullet voting in the 1987 MAA
  election.
- **"Range voting discourages dishonest voting"** — backwards. `score-voting.md`: honest score is
  one of the best methods there is, strategic score is plurality.
- **Range voting's tabulation** — the card describes dividing by the number of voters who scored the
  candidate, plus a fixed number of "fake" votes at a set score to damp small enthusiastic blocs.
  That is average-with-quorum, the Pirate Party Bavaria rule in `score-voting.md`, and it's the one
  place the site is more precise than most textbook treatments.
- **"The likelihood of a tie is very high"** (Condorcet) — overclaim. `ranked-robin-vse-run.md` puts
  Copeland's unresolved rate flat at ~17%, and 95% of those are clone dead heats rather than cycles.
- **1998 Minnesota** — "almost everyone who voted for Humphrey had Coleman as a second choice …
  62% of people actually preferred Coleman" is asserted with no source and doesn't follow from
  anything on the card.
- Typos in the shipped filenames and headings: `Single-Transfrable-Vote`, `Unanimty`,
  `Comopactness`, and a sidebar reading "Polsby-**Pepper** Compactness Score".

The best card in the set is **What is the Best Ranked Voting Method?** — W. H. Wallis's 110-ballot,
5-candidate profile where plurality, runoff, instant runoff, Borda and Condorcet elect **A, B, C, D
and E respectively**, one method per candidate. Cleaner than LeGrand's 921-voter four-winner example
in `legrand-ranked-ballot-methods.md`, and the two together are the whole argument that the method
is the decision.
