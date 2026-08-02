# Reverse symmetry: what the calculator's checkbox is for, and four violations

Source: [rob-legrand.github.io/ranked-ballot-voting-calculator](https://rob-legrand.github.io/ranked-ballot-voting-calculator/)
— the maintained rewrite of LeGrand's calculator ([notes](legrand-ranked-ballot-methods.md)). Every result below was
run there on 2026-08-01 with an explicit tiebreaking ranking, so all of it is reproducible.

LeGrand's criterion table scores 13 methods on **reverse symmetry** and nine of them get a ❌ — the largest block of
failures in the table apart from nonmanipulability (which is a theorem) and reinforcement (which only Borda passes).
The calculator has a checkbox built specifically to test the criterion; this note supplies four worked violations to
point it at, between them convicting **all nine** failing methods.

## The criterion

> **Reverse symmetry** — reverse every ballot and the unique winner must not still win.

The intuition: a ranked ballot has no privileged direction. If a method reads `Abby>Brad>Cora` as evidence for Abby,
it should read the same ballot upside-down as evidence *against* Abby. A method that elects the same candidate from an
election and its mirror image is keying on something other than the preferences — usually on where candidates sit in
an elimination order, which is an artifact of the counting rule rather than of what voters said.

Who passes, per LeGrand's table:

| | reverse-symmetric |
|---|---|
| ✅ (4) | Borda, Copeland, Schulze, Tideman |
| ❌ (9) | Baldwin, Bucklin, Carey, Coombs, Dodgson, Hare, Nanson, Raynaud, Simpson |
| unscored | Black, Small (described on the site but never scored) |

## Running the test

Two runs of the same ballots:

1. Enter the ballots **and an explicit tiebreaking ranking**. Note the winner X.
2. Tick **Reverse all rankings**, calculate again with the same tiebreaker.
3. If X wins both times, that method fails reverse symmetry on this example.

Three things that will bite you:

- **The tiebreaker is mandatory in practice.** Leave it blank and the calculator draws a random ballot, so the same
  input can give different winners on different clicks. Tie-broken winners are flagged with `*` in the results table.
- **An asterisked winner proves nothing.** The criterion is about the *unique* winner; if the method actually tied and
  the tiebreaker picked, you have no violation either way. In Example 1 below, twelve methods elect Abby in the
  forward run — but six of those twelve did it only on the tiebreaker, so only the other six can be tested at all.
- **The checkbox flips the tiebreaker too.** In Example 1 the forward run reports `Abby>Brad>Cora` as the tiebreaker
  and the reversed run reports `Cora>Brad>Abby`. That is deliberate: reversing the ballots but not the tiebreaker
  would leave one asymmetry in the input and could manufacture a "violation" out of the tiebreak alone.

## Example 1: six methods at once (9 voters, 3 candidates)

```
3:Abby>Brad>Cora
1:Brad>Abby>Cora
3:Brad>Cora>Abby
2:Cora>Abby>Brad
```

Tiebreaking ranking: `Abby>Brad>Cora`. The pairwise matrix is a clean 3-cycle — Abby beats Brad 5–4, Brad beats
Cora 7–2, Cora beats Abby 5–4 — so there is no Condorcet winner and the Smith set is everybody.

| | forward | reversed |
|---|---|---|
| **Abby** | Baldwin, Carey, Coombs, Hare, Nanson, Raynaud, Copeland\*, Dodgson\*, Schulze\*, Simpson\*, Small\*, Tideman\* | Baldwin, Carey, Coombs, Hare, Nanson, Raynaud |
| **Brad** | Black, Borda, Bucklin | — |
| **Cora** | — | Black, Borda, Bucklin, Copeland\*, Dodgson\*, Schulze\*, Simpson\*, Small\*, Tideman\* |

**Six clean violations in one run**: Baldwin, Carey, Coombs, Hare, Nanson and Raynaud all elect Abby forward and
Abby reversed, with no tiebreaker involved either time. Borda, Black and Bucklin switch Brad → Cora, which is what
passing looks like.

Why Hare does it. Forward, first preferences are Abby 3, Brad 4, Cora 2; Cora is eliminated and her two
`Cora>Abby>Brad` ballots transfer to Abby, who wins 5–4. Reversed, the ballots become `3:Cora>Brad>Abby`,
`1:Cora>Abby>Brad`, `3:Abby>Cora>Brad`, `2:Brad>Abby>Cora`; first preferences are now Cora 4, Abby 3, Brad 2, so
**Brad** is eliminated and his two ballots transfer to Abby, who wins 5–4 again. Abby is nobody's largest bloc in
either direction, and in both directions she is the one standing when the smallest bloc's second choices land.

Coombs gets there by the mirror route: forward, Cora has the most last places (4) and is dropped, leaving Abby 5,
Brad 4; reversed, Brad has the most last places (4) and is dropped, leaving Abby 5, Cora 4.

## Example 2: a Condorcet winner does not save you (9 voters, 4 candidates)

```
3:Mark>Owen>Nell>Pete
2:Nell>Owen>Pete>Mark
1:Owen>Mark>Nell>Pete
3:Pete>Owen>Mark>Nell
```

Tiebreaking ranking: `Mark>Nell>Owen>Pete`. Here **Owen is the Condorcet winner** — he beats Mark 6–3, Nell 7–2 and
Pete 6–3.

| | forward | reversed |
|---|---|---|
| **Owen** | Baldwin, Black, Borda, Bucklin, Coombs, Copeland, Dodgson, Nanson, Schulze, Simpson, Small, Raynaud\*, Tideman\* | — |
| **Pete** | Carey, Hare | Baldwin, Carey, Dodgson, Hare, Nanson, Schulze, Simpson, Coombs\*, Copeland\*, Raynaud\*, Small\*, Tideman\* |
| **Nell** | — | Black, Borda, Bucklin |

Reversed, Owen goes from Condorcet winner to **Condorcet loser** — he now loses every pairwise contest 3–6, 2–7, 3–6
— and drops out of the Smith set entirely, which is left as {Mark, Nell, Pete}. Every Condorcet method dutifully
abandons him. **Hare and Carey elect Pete both ways**, cleanly.

Hare's rounds, forward: first preferences Mark 3, Nell 2, **Owen 1**, Pete 3, so the Condorcet winner is eliminated
first; then Nell (2) goes; Pete beats Mark 5–4. Reversed: Owen now has *zero* first preferences and goes first
again, then Mark, and Pete wins 6–3. Owen is eliminated first for being everyone's compromise and eliminated first
for being everyone's last resort, and Hare returns the same winner either way.

This is the strongest of the four examples because the failure has nothing to do with a cycle: the forward election
has a perfectly well-defined Condorcet winner and Hare still can't tell the election from its mirror image.

## Example 3: the smallest one — Bucklin on 5 ballots

```
1:Jana>Lisa>Kurt
2:Lisa>Kurt>Jana
1:Kurt>Jana>Lisa
1:Jana>Kurt>Lisa
```

Tiebreaking ranking: `Jana>Kurt>Lisa`. **Bucklin elects Kurt forward and Kurt reversed**, unasterisked both times.
Everything here is a 3–2 cycle, so most other methods need the tiebreaker and prove nothing.

The count, forward: round 1 gives Jana 2, Lisa 2, Kurt 1 — no majority of 5. Round 2 adds second preferences: Jana 3,
Kurt 4, Lisa 3; all three cross the threshold at once and Kurt has the most. Reversed, the ballots become
`1:Kurt>Lisa>Jana`, `2:Jana>Kurt>Lisa`, `1:Lisa>Jana>Kurt`, `1:Lisa>Kurt>Jana`, and round 2 produces the *identical*
totals: Jana 3, Kurt 4, Lisa 3. Kurt is everybody's second choice, and reversing a ballot leaves the middle
candidate in the middle.

## Example 4: Dodgson and Simpson (12 voters, 4 candidates)

```
3:Seth>Umar>Rosa>Tara
1:Umar>Rosa>Tara>Seth
5:Rosa>Tara>Umar>Seth
3:Seth>Tara>Umar>Rosa
```

Tiebreaking ranking: `Rosa>Seth>Tara>Umar`. **Dodgson and Simpson elect Seth forward and Seth reversed**, both
unasterisked. (Bucklin switches cleanly here, Tara → Umar; Carey and Hare both switch but with an asterisk on one
side. Example 3 catches Bucklin and Example 2 catches Carey and Hare.)

Simpson's mechanism is visible in the pairwise matrix, and it is the cleanest illustration in this note of what
reverse symmetry is really testing. Seth **ties every one of his three pairwise contests 6–6**. Simpson elects
whoever's worst pairwise defeat is smallest:

| | worst opposition, forward | worst opposition, reversed |
|---|---|---|
| Rosa | 7 (Umar) | 9 (Tara) |
| **Seth** | **6** | **6** |
| Tara | 9 (Rosa) | 8 (Umar) |
| Umar | 8 (Tara) | 7 (Rosa) |

Reversing the ballots transposes the pairwise matrix, so every other candidate's worst defeat changes — but a 6–6 tie
transposes to a 6–6 tie. Seth's score is *invariant under reversal by construction*, and he wins both times.

Dodgson falls out of the same fact. LeGrand's Dodgson is the smallest **sum of defeat margins** (not Carroll's
adjacent-swap version — see [glossary.md](glossary.md)), and Seth, tying everything, is the only candidate with *no*
defeats at all: his score is 0 forward and 0 reversed, while Rosa, Tara and Umar each lose at least one contest in
each direction. Any method whose score is built only from a candidate's defeats will do this to a universally tied
candidate.

## Coverage

| Method | reverse-symmetric (LeGrand) | violation demonstrated |
|---|:-:|---|
| Baldwin | ❌ | Example 1 |
| Bucklin | ❌ | Example 3 |
| Carey | ❌ | Examples 1, 2 |
| Coombs | ❌ | Example 1 |
| Dodgson | ❌ | Example 4 |
| Hare | ❌ | Examples 1, 2 |
| Nanson | ❌ | Example 1 |
| Raynaud | ❌ | Example 1 |
| Simpson | ❌ | Example 4 |
| Borda, Copeland, Schulze, Tideman | ✅ | — (no violation exists) |

All nine ❌ methods are convicted, every one by a run in which neither the forward nor the reversed winner was
tie-broken.

The ✅ side is only ever *consistent* with these examples, never proved by them — Borda switches winner in all four,
and Schulze switches cleanly in Example 2 (Owen → Pete). Copeland and Tideman need the tiebreaker on at least one
side of all four examples, so nothing here even tests them. That asymmetry is the nature of the thing: one example
can refute a criterion but no number of examples can establish it.

## What a brute-force search says

Constructing these needed a search; the profiles above are the smallest found. Findings worth keeping (scripts were
throwaway, but the searches are easy to redo):

- **Hare needs a Condorcet cycle to fail on 3 candidates.** Over every 3-candidate profile with ≤8 ballots per
  ordering and ≤22 voters, every Hare reverse-symmetry failure had a cycle — not one occurred alongside a Condorcet
  winner. Move to 4 candidates and they are common, which is why Example 2 has four candidates.
- **Simpson needs 4 candidates.** No 3-candidate failure turned up in ~200k random profiles; 4-candidate ones are
  easy to find.
- **Bucklin is the cheapest to break** — 5 voters and 3 candidates, as in Example 3. It also fails much more
  readily than the others at every size.
- Hare and Coombs fail together on the same 9-voter profile surprisingly often; Example 1 is one of six minimal
  9-voter profiles that do it (the other five are relabellings of the same structure).

## Related

- Definition and the rest of the criteria: [glossary.md](glossary.md)
- The criteria table, the calculator's other two options, and the verified Coombs reinforcement failure:
  [legrand-ranked-ballot-methods.md](legrand-ranked-ballot-methods.md)
- The other worked-example note, on center squeeze: [hare-center-squeeze-examples.md](hare-center-squeeze-examples.md)
