# Center squeeze in the calculator: one famous example, and a better one

Source: [rob-legrand.github.io/ranked-ballot-voting-calculator](https://rob-legrand.github.io/ranked-ballot-voting-calculator/)
— the maintained rewrite of LeGrand's calculator ([notes](legrand-ranked-ballot-methods.md)). All results below
were run there on 2026-08-01 with an explicit tiebreaking ranking, so they are reproducible.

The calculator ships ~25 example ballot files. Two of them make the same point — that Hare (IRV) can eliminate a
candidate who beats every rival head-to-head. One is famous and rhetorically loaded; the other is unlabelled,
milder-looking, and actually the stronger demonstration. This note works both.

> **A note on names.** The first example is captioned on the site as a "silly Hare example" and ships with two
> 20th-century mass murderers as the flank candidates and a founding father as the centrist. Those names aren't
> doing arithmetic, they're doing rhetoric — they make the conclusion unarguable before you've read the ballots,
> which is exactly what you don't want in a worked example. I've relabelled the candidates **Dana / Emil / Fay**
> (LeGrand's own house style is consecutive-letter name triples: Abby/Brad/Cora, Jana/Kurt/Lisa, Mark/Nell/Owen).
> Emil is the middle letter and the middle candidate. Ballot counts are untouched, so every number below matches
> the site's own example byte for byte.

## Example 1: 99 voters, 3 candidates

```
34:Dana>Emil>Fay
33:Fay>Emil>Dana
16:Emil>Dana>Fay
16:Emil>Fay>Dana
```

Two hostile flanks (Dana 34, Fay 33) whose voters both rank Emil second, and a middle bloc of 32 split evenly on
which flank it fears less.

Pairwise matrix (row = "for", column = "against"; **bold** = winning side; every pair sums to 99):

| for \ against | Dana | Emil | Fay |
|---|---|---|---|
| **Dana** | — | 34 | **50** |
| **Emil** | **65** | — | **66** |
| **Fay** | 49 | 33 | — |

**Emil is the Condorcet winner, and not narrowly** — he takes roughly two-thirds against each flank. Borda scores
(row sum − column sum): Dana −30, **Emil +64**, Fay −34.

Every method the calculator implements elects Emil, except two:

| Winner | Methods |
|---|---|
| **Emil** (13) | Baldwin, Black, Borda, Bucklin, Coombs, Copeland, Dodgson, Nanson, Raynaud, Schulze, Simpson, Small, Tideman |
| **Dana** (2) | **Hare**, Carey |

Hare's trace, verbatim from the calculator:

| Round | Dana | Emil | Fay | Eliminated |
|---|---|---|---|---|
| 1 | 34 | **32** | 33 | Emil — fewest first ranks |
| 2 | **50** | — | 49 | Fay → Dana wins 50–49 |

That's the whole mechanism. Emil loses on the one statistic Hare looks at in round 1 (first ranks: 32, last by
one vote) and is gone before the 65–34 and 66–33 preferences that dominate every other method are ever read.
Carey agrees with Hare for the same reason: average first-rank total is 33, and Emil's 32 is the only
below-average score, so Carey drops him too.

Two follow-ups I ran, which the site doesn't:

- **Fay is a spoiler.** Put `Fay` in "candidates to ignore" and Hare elects Emil 65–34. Fay's presence, not
  Fay's votes, flips the Hare winner — and Fay is Dana's *opposite*, not a clone. This isn't clone-spoiling,
  it's center-squeeze spoiling, and it's the exact failure the ["core support"](rcv-and-core-support.md) argument
  is about.
- **It hangs on 2 ballots.** Move two voters from `Fay>Emil>Dana` to `Emil>Fay>Dana` (Emil 34, Dana 34, Fay 31)
  and Hare joins the other fourteen methods on Emil. The whole disagreement is 2 of 99 ballots wide.

## Is it a useful example?

**Partly. The structure is real; the presentation is loaded and the magnitude is invented.**

What's genuinely right about it:

- **The failure mode is not hypothetical.** A Condorcet winner finishing last on first preferences and being
  eliminated in round 1 is what happened in Burlington VT 2009 and in Alaska's 2022 U.S. House special, where
  Begich beat both Peltola and Palin head-to-head and was eliminated first
  ([details](rcv-and-core-support.md)). If you want a 4-line election that reproduces Alaska's shape, this is it.
- **It isolates one variable.** Fifteen methods, one disagreement, three candidates. Nothing else is going on,
  which is rare and useful.
- **It makes the mechanism visible.** "Hare looks at the smallest amount of ballot information at any one time"
  is LeGrand's own framing, and this is the cleanest instance of it in the whole example set.

What's unfair about it:

- **The names carry the argument.** With those candidates, no reader can say "actually the IRV winner was fine" —
  the example forecloses the counterargument instead of answering it. Relabelled, the same ballots invite the
  real question: is a candidate 34% of voters rank first and 33% rank *last* better or worse than one nobody
  ranks first at 33% but everybody tolerates? That's a genuine values dispute; the original names pretend it
  isn't one.
- **The margins are engineered, and simultaneously.** Emil trails on first preferences by 1 and 2 votes while
  winning pairwise 2:1. Real center squeezes are nothing like that lopsided — Begich's head-to-head wins were a
  few points, not thirty. The example needs both knobs set to extremes at once and is 2 ballots from collapsing.
- **The second preferences are perfectly bipolar.** 100% of Dana's voters and 100% of Fay's voters rank Emil
  second. Real electorates never split that cleanly, and this is what manufactures the 2:1 pairwise margins.
- **It proves possibility, not frequency.** "Hare *can* do this" was never in dispute — it's a theorem
  (Hare fails the Condorcet criterion; see the compliance table in
  [legrand-ranked-ballot-methods.md](legrand-ranked-ballot-methods.md)). A constructed example can't tell you how
  often it happens, which is the only question that matters for choosing a method.
- **The weapon points both ways.** The same calculator's headline 921-voter example has Dodgson and Simpson
  electing the **Condorcet loser** while Copeland, Schulze and Tideman rank her last. Anyone can build the
  4-line election that makes their least favourite method look monstrous. Cherry-picked worst cases are cheap
  for every method here.

**Verdict:** keep it as a *mechanism* demo — it's the shortest thing that shows exactly where Hare throws
information away. Don't cite it as evidence about IRV, and don't use it with the original names. For persuasion,
use Alaska 2022: real ballots, real margins, and no rhetorical scaffolding.

## Example 2: the better one, already on the page

The site also ships this, captioned "Hare jumps to extremes on a left-right spectrum" — neutrally named, and
nobody seems to quote it:

```
18:FarLeft>Left>Center>Right>FarRight
16:Left>FarLeft>Center>Right>FarRight
17:Center>Left>Right>FarLeft>FarRight
 9:Center>Right>FarRight>Left>FarLeft
19:Right>FarRight>Center>Left>FarLeft
21:FarRight>Right>Center>Left>FarLeft
```

Center is again the Condorcet winner, beating all four rivals 60–66 out of 100. But this time **Center also
leads on first preferences** — 26, ahead of FarRight's 21 and FarLeft's 18 — and *still* loses under Hare:

| Round | Center | FarLeft | Left | Right | FarRight | Eliminated |
|---|---|---|---|---|---|---|
| 1 | **26** | 18 | 16 | 19 | 21 | Left (16) |
| 2 | 26 | 34 | — | 19 | 21 | Right (19) |
| 3 | **26** | 34 | — | — | 40 | **Center** |
| 4 | — | **51** | — | — | 49 | FarRight → **FarLeft** wins |

Center leads round 1, is never overtaken by a candidate that survives it, and is eliminated third because both
flanks consolidate faster than the middle can. Hare elects **FarLeft** — who started with 18 first preferences,
the second *fewest* — and Bucklin elects **Left**, a third answer. Thirteen methods elect Center.

Why this one is better than Example 1 for every purpose except brevity:

- **It kills the "core support" defence outright.** You cannot say the Hare winner had more first-choice
  enthusiasm; Center had the most first preferences and lost anyway. Example 1's centrist is last on first
  preferences, which leaves the IRV advocate an argument. This one doesn't.
- **Five candidates, three winners** — it shows the method disagreement *and* the mechanism, not just the
  mechanism.
- **Neutral names**, and they encode the structure (a spectrum) instead of a verdict.
- **It's not knife-edge.** The eliminations at rounds 1–3 have margins of 3, 2 and 8; it doesn't unravel if you
  move two ballots.

## A calculator quirk found along the way

Supply a tiebreaking ranking and the results footnote both **mislabels and truncates** it. On the 5-candidate
example above, a supplied tiebreak of `FarRight>Right>Center>Left>FarLeft` is echoed as:

> \* The ranking FarRight>Right>Center>Left> was used as a random-ballot tiebreaker.

The last candidate is dropped (leaving a dangling `>`), and a *user-supplied* ranking is described as a
"random-ballot tiebreaker" — the phrase the page reserves for the case where you supply nothing and it draws a
ballot at random. Display only: I ran the example with two opposite tiebreak orders and Tideman elected Center
both times. But it makes the asterisk unreadable as an audit trail, which is the one job it has. Consistent with
the other quirks in [legrand-ranked-ballot-methods.md](legrand-ranked-ballot-methods.md); not filed upstream.

## Related local material

- [legrand-ranked-ballot-methods.md](legrand-ranked-ballot-methods.md) — the 16 methods, the compliance table,
  and the calculator's other quirks
- [rcv-and-core-support.md](rcv-and-core-support.md) — Alaska 2022, and why "core support = first rankings" is
  the belief this example attacks
- [glossary.md](glossary.md) — center squeeze, Condorcet winner, Hare, Carey, Bucklin, spoiler
