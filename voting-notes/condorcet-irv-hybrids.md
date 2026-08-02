# Condorcet–IRV hybrids

The first note born from the [roadmap](roadmap.md), and the one the center-squeeze material has been
waiting for. The question: keep the ranked ballot, keep Hare's elimination machinery, and bolt on a
pairwise gate — do you get Condorcet compliance without importing the burial problem that plagues pure
Condorcet completions? Five methods answer it five slightly different ways, and the answer, checked
exhaustively below, is **yes for four of them** — with a precise characterization of the residue: the
four eliminate-by-first-preferences hybrids can only ever be buried into an outcome that *sincere plain
IRV would have produced anyway*. The fifth, BTR-IRV, is the instructive exception.

Everything here is recomputed: the five methods run over the library's existing profiles
([verify.py](code/condorcet-irv-hybrids/verify.py), 42 checks, exit 0), and a complete burial search
over every three-candidate nine-voter election there is ([burial.py](code/condorcet-irv-hybrids/burial.py)).

---

## Five ways to bolt a gate onto Hare

All five take ordinary ranked ballots and reduce to "elect the Condorcet winner" whenever one exists.
They differ only in *where* the pairwise check sits relative to the eliminations (definitions per
electowiki, cited in [methods.py](code/condorcet-irv-hybrids/methods.py)):

- **Smith//IRV** — compute the [Smith set](glossary.md) once, delete everyone outside it, run IRV on
  what remains. The `Smith//X` pattern the glossary already defines for Smith//Score.
- **Benham** — run IRV, but before each elimination check whether some remaining candidate pairwise-beats
  all other remaining candidates; the moment one does, elect them. The gate travels with the count.
- **Woodall** — run plain IRV eliminations untouched, but elect the first moment only one member of the
  *original* Smith set is still standing. The gate watches; the count never changes.
- **BTR-IRV** (bottom-two runoff) — each round, the two candidates with the fewest first preferences
  face off pairwise and the pairwise loser is eliminated. The only one of the five with no Smith
  computation at all — and the only one whose *eliminations* read the pairwise matrix, which turns out
  to be its undoing under burial. Originally proposed, per electowiki, by Rob LeGrand (2002) — the same
  LeGrand whose [calculator](legrand-ranked-ballot-methods.md) supplies half the profiles below.
- **Tideman's Alternative** (a.k.a. Alternative Smith) — repeat: restrict to the current Smith set; if
  one candidate remains, elect them; otherwise eliminate the fewest-first-preferences candidate and
  recompute. The gate is re-armed every round.

A naming triangle to defuse before going further. In this library **"Tideman" means ranked pairs** —
LeGrand's label, kept in the [glossary](glossary.md) and the [method survey](legrand-ranked-ballot-methods.md).
Tideman's Alternative is a *different* method carrying the same Nicolaus Tideman's name — he defines it
as "alternative Smith" in his 2006 book, though electowiki holds it is not his invention — and he also
appears in the [STV note](single-transferable-vote.md) as the formalizer of PSC. Three senses of one
surname. Same
hazard with **Woodall**: until now he appears here as the criteria author (mono-raise-delete in
[star-voting](star-voting.md), later-no-harm in [cardinal-voting-systems](cardinal-voting-systems.md));
the method above is the same Douglas Woodall wearing a different hat. And the Lumen profile below has a
candidate literally named Smith — the candidate, not the set.

## On the library's center squeezes

The three profiles where these notes have watched Hare eliminate the Condorcet winner, plus the two
cycle profiles, one table:

| profile | Condorcet winner | plain IRV | Smith//IRV | Benham | Woodall | BTR-IRV | Tideman's Alt |
|---|---|---|---|---|---|---|---|
| [99-voter Hare squeeze](hare-center-squeeze-examples.md) | Emil | Dana | **Emil** | **Emil** | **Emil** | **Emil** | **Emil** |
| [5-candidate spectrum](hare-center-squeeze-examples.md) | Center | FarLeft | **Center** | **Center** | **Center** | **Center** | **Center** |
| [Lumen 75-ballot](lumen-75-ballot-four-winners.md) | Garcia | Nguyen | **Garcia** | **Garcia** | **Garcia** | **Garcia** | **Garcia** |
| [LeGrand 921-voter](legrand-ranked-ballot-methods.md) | none (cycle) | Dave | Dave | Dave | Dave | **Brad** | Dave |
| [5-cycle, 69 voters](ranked-robin-origins.md) | none (cycle) | Ben | Ben | Ben | Ben | **Edith** | Ben |

Every hybrid elects the Condorcet winner on every profile that has one — 15 of 15, which is compliance
by construction, not news. The news is *how little work it takes*. When a Condorcet winner exists the
Smith set is exactly {CW}, so Benham, Woodall and Tideman's Alternative all elect **before a single
elimination happens**, and Smith//IRV's "IRV" runs on a one-candidate field. Only BTR-IRV actually
counts anything, and its counting is the nicest demonstration in the note:

On the 99-voter profile — first preferences Dana 34, Fay 33, **Emil 32** — plain IRV eliminates the
Condorcet winner immediately, by one vote, and Dana wins the final 50–49. BTR-IRV puts the same Emil in
the bottom two both rounds, *and that is precisely what saves him*: bottom-two means pairwise fight, and
Emil is the Condorcet winner, so he wins every fight he is put in — 66–33 over Fay, then 65–34 over
Dana. The mechanism that kills the center under Hare (weak first-preference support) is the mechanism
that rescues it under BTR, because BTR converts "last place on tallies" into "a matchup you can't lose."

On the Lumen 75 ballots, BTR-IRV's first act is to eliminate **Nguyen — plain IRV's winner** — because
the round-1 bottom two are Lee and Nguyen and nearly-everyone's-second-choice Lee beats him 56–19.
Garcia then survives to a 39–36 final over Lee. Same ballots, same elimination machinery, opposite
story — and the one-vote Garcia-vs-Nguyen elimination (23 v 24) that decides the whole election under
plain IRV never happens at all.

## Inside a cycle, they are (almost all) just IRV

On both no-Condorcet-winner profiles, five of the six methods — plain IRV included — agree, and
**BTR-IRV is the lone dissenter both times**. That pattern is worth stating as the note's second
headline: with no Condorcet winner to gate on, Smith//IRV, Benham, Woodall and Tideman's Alternative
all collapsed to plain IRV on every profile tested, so the entire observable difference among the five
hybrids here is BTR's bottom-two runoff.

And BTR's dissents are not noise — both times it lands on the winner of a *named Condorcet completion*
from the existing notes:

- **921-voter profile** (cycle Brad→Erin 623, Erin→Dave 610, Dave→Brad 609; Cora loses every matchup
  460–461): the others elect Dave, the plain-IRV winner. BTR elects **Brad — the ranked pairs winner**
  from the [survey](legrand-ranked-ballot-methods.md). The pivot is the famous one-vote matchup: BTR's
  decisive bottom-two pairs Abby (98 first preferences) against Cora (200), and Abby survives 461–460 —
  the round where plain IRV kills Abby on tallies. Protected, Abby then eliminates Dave 485–436, and
  Brad beats Abby 463–458 in the final. Cora — the Condorcet loser who is one vote from beating
  everybody — acts as a shield and then a casualty, rerouting the whole elimination order.
- **5-cycle, 69 voters**: the others elect Ben; BTR elects **Edith — Ranked Robin's winner** from the
  [origin thread](ranked-robin-origins.md), the one with the best corrected margin sum (+20). Ben's own
  cycle credentials are middling — third of the five, margin sum −1 against Edith's +20; he wins under
  the other methods purely by elimination luck — plain IRV removes Frank on tallies, while BTR's round-3
  bottom two is Frank v Ben, Frank wins the matchup 37–32, and Ben is gone.

One convention caveat, in the spirit of the [thread-claims note](ranked-robin-thread-claims-checked.md):
the 5-cycle reconstruction contains equal ranks, which plain IRV does not define. The verifier splits a
ballot's top continuing rank-group evenly (exact fractions — hence tallies like Frank 21/2); pairwise
counting follows BetterVoting's Util.ts (strict preference only). BetterVoting's own IRV would simply
reject these ballots, so "IRV elects Ben" on this profile is convention-dependent. The Smith
computations are not — they are integer pairwise throughout.

## Burial, exhaustively

The reason to want these methods is Green-Armytage's claim (2011): hybrids of Condorcet and Hare
resist **burial** — insincerely demoting the strongest rival — far better than pure Condorcet
completions, because burial can only manufacture a *cycle*, and the hybrids hand cycles to an IRV stage
whose first-preference tallies the burial never touched. The claim is usually supported by simulation.
Three candidates is small enough to not simulate at all.

The universe: 3 candidates, all 6 strict rankings, **every** multiset of 9 ballots — C(14,5) = 2,002
elections, of which 1,890 have a sincere Condorcet winner. Burial means: a bloc sharing one sincere
ranking demotes the Condorcet winner to last while keeping its favorite on top; with three candidates
that pins the sincere ranking to f>cw>z and the insincere one to f>z>cw, so every (bloc, size) pair is
enumerable — 4,116 scenarios, 672 of which actually destroy the Condorcet winner. Success = the bloc's
favorite wins. Comparison baselines: minimax(margins) and Ranked Robin (Copeland + margin-sum
tie-break, exactly as in the [thread-claims verifier](ranked-robin-thread-claims-checked.md)).

| method | profiles where burial succeeds (of 1,890) | scenarios rewarded | scenarios backfiring |
|---|---|---|---|
| minimax(margins) | 174 (9.2%) | 251 | 842 |
| Ranked Robin | **233 (12.3%)** | 299 | 845 |
| plain IRV | **0** | 0 | 508 |
| Smith//IRV, Benham, Woodall, Tideman's Alt | 58 (3.1%) | 164 | 836 |
| BTR-IRV | 145 (7.7%) | 272 | 800 |

(The four gate-style hybrids have *identical* success sets at every electorate size tested — with three
candidates and complete ballots they all reduce to "Condorcet winner, else IRV winner of the cycle."
Sweeps at n = 5, 7, 11 show the same ordering: 15/20/6/15, 60/80/24/54, 415/567/126/330 for
minimax / Ranked Robin / gate hybrids / BTR.)

Four findings, in descending order of how much they matter:

**1. Green-Armytage holds, 3-to-1.** Minimax is buriable on 3.0× as many profiles as the gate hybrids,
Ranked Robin on 4.0×. Of the 672 cycle-manufacturing burials, minimax rewards 37.4%, the hybrids 24.4%.
And 96 profiles fall to *both* pure completions while falling to *no* hybrid.

**2. The residue is characterized — the gate hybrids never lose ground to burial, they only fail to
gain it.** In every one of the gate hybrids' successful-burial records — all 3,196 of them across
n = 2..11 — **sincere plain IRV already elects the buriers' favorite.** Burial against these methods
cannot steal an election; it can only dissolve the Condorcet gate that was protecting the sincere winner
from IRV, dropping the result back to what IRV would have done with honest ballots. For three candidates
this is a theorem, not an observation: burial edits only the cw-vs-z tally — first preferences and the
f-vs-z matchup are untouched — so f can never be *made* a Condorcet winner, only handed a cycle, and the
cycle goes to IRV. A method that adopts a gate hybrid is, burial-wise, never worse off than IRV and
never better off than honest-Condorcet. That is the precise content of "hybrid."

**3. Ranked Robin is *more* burial-prone than minimax** — 233 vs 174 at n = 9, 567 vs 415 at n = 11.
Not a surprise once said out loud: its margin-sum tie-break is Borda-flavored, and burial pumps margins
directly. The [thread-claims note](ranked-robin-thread-claims-checked.md) proved the Copeland gate is
the only thing between Ranked Robin and Borda; this is what that costs under the one strategy Borda is
famous for.

**4. BTR-IRV is the weak hybrid, and the reason generalizes.** 145 profiles — closer to minimax than to
Benham. Its eliminations *consult the falsified matrix*, so burial steers who gets eliminated, not just
whether the gate holds: in 806 of BTR's 1,290 successful scenarios (n = 2..11) the buriers' favorite is
**not** the sincere IRV winner — theft beyond anything sincere IRV would have done, a channel the gate
hybrids provably lack. "Condorcet–Hare
resistance" is specifically a property of *eliminating by first preferences*, which burial cannot touch —
not of hybridization as such.

The smallest clean success against the pure completions but not the hybrids (no tie-break fires
anywhere), 9 voters:

```
Sincere (Condorcet winner C):        Buried (4 B>C>A voters demote C):
  2  A>C>B                             2  A>C>B
  4  B>C>A                             4  B>A>C
  3  C>B>A                             3  C>B>A
  A v B 2-7   A v C 2-7   B v C 4-5    A v B 2-7   A v C 6-3   B v C 4-5
                                       -> cycle A > C > B > A
minimax:      C -> B   burial SUCCEEDS   (worst defeats: A +5, B +1, C +3)
Ranked Robin: C -> B   burial SUCCEEDS   (Copeland all tied; margin sums A -2, B +4, C -2)
Benham:       C -> C   burial FAILS      (no champion; tallies [A 2, B 4, C 3] eliminate A;
Smith//IRV:   C -> C   burial FAILS       C beats B 5-4 and wins)
```

The burial changed exactly one number — the A-vs-C tally — and that is the whole story: first
preferences still read A 2, B 4, C 3, C still beats B head-to-head, so the falsified cycle hands the
election to an IRV stage that sees nothing wrong and quietly re-elects C.

And the hybrids' own weak spot, 5 voters — sincere profile `1 A>C>B, 2 B>A>C, 2 C>A>B` (Condorcet
winner A): one C>A>B voter flips to C>B>A, manufactures the cycle, and the four gate hybrids eliminate
A on tallies [A 1, B 2, C 2] and elect C — their minimal tie-free case. (BTR-IRV lands on the same
winner here through a bottom-two matchup that needs the fixed-order tie-break; its first fully tie-free
success takes 7 voters.) The tell, per finding 2: sincere plain IRV on this profile *already elects C*.
The gate was the only thing protecting A, and burial dissolved it.

Last: burial *backfires* — elects the bloc's sincere last choice — about **5×** as often as it succeeds
under the gate hybrids (836 vs 164 scenarios), 3.4× under minimax, and under plain IRV it is all
downside: 508 backfires, 0 successes. Deterrence, not just resistance.

## What they cost

Honest accounting, with verification status marked:

- **Monotonicity** — the IRV stage gives it up. Schulze and ranked pairs are the [survey](legrand-ranked-ballot-methods.md)'s
  only methods passing Condorcet + clone independence + monotonicity + Smith together; the hybrids keep
  Smith and drop the monotonicity guarantee. *Literature claim, not yet locally verified — building a
  worked mono-raise failure for each hybrid is the natural follow-up, and the
  [Lumen note](lumen-75-ballot-four-winners.md)'s non-monotonic profile is the place to start.*
- **Later-no-harm** — gone, necessarily: no Condorcet method can satisfy it (Woodall 1997 — the same
  Douglas Woodall a third time, and the exact result Green-Armytage 2011 cites for the price). The
  criterion enters this library through his 1994 paper, cited in
  [cardinal-voting-systems](cardinal-voting-systems.md). *Literature claim.*
- **Summability** — the pairwise matrix is precinct-summable but the IRV stage is not, so the hybrids
  inherit IRV's centralized count. The ballot-vs-rule separability argument in
  [ranked-robin-results-explained](ranked-robin-results-explained.md) applies unchanged; what the
  hybrids lose relative to Ranked Robin is exactly the ability to hand-count matchups at the precinct.
- **Decisiveness** — a quiet win: across all five library profiles and the 9-voter example,
  **no tie-break ever fired** — and in the 5-voter example the four gate hybrids ran tie-free while
  minimax, Ranked Robin and BTR-IRV each needed the fixed-order tie-break. The IRV stage is as decisive
  inside a cycle as Hare is anywhere, where Copeland-family methods fall to tie ladders on the same
  profiles ([BV1550](ranked-robin-results-explained.md) defeated essentially every completion).

## What this note did not do

The [3-cycle from the origin thread](ranked-robin-origins.md) exists only as a corrected pairwise
matrix, and Alaska 2022 only as reported results — no ballots, so no runs; verify.py lists both as
skipped rather than pretending. The four gate hybrids were mutually indistinguishable on everything
here — separating Smith//IRV from Benham from Woodall from Tideman's Alternative needs ≥4-candidate
cycles with the right structure, or truncated ballots, and no profile in the library currently does it;
constructing one is an open item. Compromising (the strategy the hybrids inherit from Hare's side of
the family, per Green-Armytage 2014's list) was not searched — it belongs in the strategic-VSE note the
[roadmap](roadmap.md) ranks third. And the monotonicity failures asserted above remain to be built.

## Verifier

[code/condorcet-irv-hybrids/](code/condorcet-irv-hybrids/) — three files, no dependencies, exact
arithmetic (integers; exact fractions where equal ranks force splitting):

- `methods.py` — pairwise matrix, Condorcet winner, Smith set (Copeland-prefix computation
  cross-checked against brute-force smallest-dominant-set search on every profile), IRV, and the five
  hybrids, with electowiki citations.
- `verify.py` — the five library profiles, all round-by-round traces, 42 PASS/FAIL checks, exit 0.
  Engine validation includes the note-recorded numbers: Emil 65–34/66–33, Garcia's 39–36 final, the
  921 cycle's 623/610/609 and Cora's uniform 460–461, and the 5-cycle margin sums +20/+15/−1/−15/−19.
- `burial.py` — the exhaustive burial search, deterministic (re-run verified byte-identical), every
  invoked tie-break recorded and excluded from tie-free counts.

## Sources

- [Green-Armytage, "Four Condorcet-Hare hybrid methods for single-winner elections", *Voting matters* 29 (2011)](http://www.votingmatters.org.uk/ISSUE29/I29P1.pdf) —
  the four gate hybrids (under his names: Woodall, Benham, Smith-AV, Tideman) and the
  strategy-resistance argument this note tests by enumeration. BTR-IRV is not in the paper.
- [Green-Armytage, "Strategic voting and nomination", *Social Choice and Welfare* 42 (2014)](https://doi.org/10.1007/s00355-013-0725-3) —
  the compromising/burial vulnerability lists, already read closely in
  [wikipedia-talk-strategic-voting-draft](wikipedia-talk-strategic-voting-draft.md).
- [electowiki](https://electowiki.org/) — method definitions (Smith//IRV, Benham's method, Woodall's
  method, BTR-IRV, Tideman's Alternative), cited individually in methods.py.
