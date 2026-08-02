# Where Ranked Robin came from: the "Ranked Advantage Voting" thread (2021)

Source: [votingtheory.org topic 136 — "New Simple Condorcet Method - Basically
Copeland+Margins"](https://www.votingtheory.org/forum/topic/136/new-simple-condorcet-method-basically-copeland-margins)
(Sass, 2021-10-26 → 2022-03-02; 6 participants, 40 posts, ~13.7k views), cross-checked against the
[electowiki article](https://electowiki.org/wiki/Ranked_Robin) it grew into.

This thread is the public debut of **Ranked Robin** — the method BetterVoting runs today
([results explainer](ranked-robin-results-explained.md)). It was proposed under the working name
**"Ranked Advantage Voting"**, and the electowiki article never mentions that name — the thread is
the only place the RAV phase is documented, which is most of why this note exists. In post 25
(2021-11-15) Sass drops in "Ranked Robin (the official name of this method)" — the renaming as it
reached the forum. Per electowiki's history section, the pieces slightly predate and interleave
with the thread: Sass had proposed the tie-breaking protocol on 2021-09-30 as Equal Vote's default
recommendation for ranked ballots, Sara Wolk coined the name "Ranked Robin" on 2021-11-07 (tagged
*citation needed*), and Sass created the electowiki page on 2021-11-08 — a week before announcing
the name in the thread.

The thread's four *testable* claims — Sass's IIA defense, the "identical to Borda" coda, the
one-sentence tally, and Waugh's tie-rate intuition — are checked against computation in a companion
note: [ranked-robin-thread-claims-checked.md](ranked-robin-thread-claims-checked.md).

A scraping note: the thread's five key exhibits are **PNG uploads, invisible to text extraction**
(the ballot language, both worked examples, the Condorcet-winner display, and the first VSE
numbers). Everything below is transcribed from the images, and the arithmetic re-checked — which
turned up real errata ([see below](#errata-both-example-images-have-arithmetic-slips)).

## The design, as first proposed

Ballot: rank as many as you like, equal ranks allowed, skipped ranks ignored (version 2.0 added,
after Marylander's prodding: unranked counts below every ranked candidate). Tally:

1. Compare every pair of candidates head-to-head.
2. If one candidate beats all others (the usual case), elect them.
3. Otherwise the candidates tied for **most matchup wins** become *finalists*; everyone else is
   eliminated.
4. Each finalist's **relative advantage** over another finalist = difference in voters preferring
   one over the other, expressed as % points of all ballots. Sum them: the **total advantage**.
5. Highest total advantage wins.

So: Copeland, completed by summed pairwise margins *within the tied set*. Sass was upfront that
the Copeland framing was forum clickbait — the pitch identity was "Condorcet, older than RCV, now
explainable," aimed squarely at converting Instant-Runoff supporters (Andrew Yang is named in the
opening post) with a name deliberately adjacent to "Ranked Choice Voting."

Post 2 adds the presentation idea that survived into the official article: **five disclosure
levels** — (1) winner only, (2) finalists' total advantages, (3) matchup-win counts, (4) finalists'
pairwise advantages, (5) full preference matrix. The "what is normally shown to the public" band in
the example images is levels 1–3.

## Timeline

| Date (UTC) | Where | Event |
|---|---|---|
| 2021-09-30 | Equal Vote (per electowiki) | Sass proposes the tie-breaking protocol as the default recommendation for ranked ballots |
| 2021-10-25 | Slack DM (screenshot in post 5) | Sass tells John Huang and Marcus Ogren to call it "Ranked Advantage Voting" |
| 2021-10-26 | [post 1](https://www.votingtheory.org/forum/topic/136/new-simple-condorcet-method-basically-copeland-margins/1) | Proposal posted: ballot language 1.0, worked 3-cycle and 5-cycle examples; Huang to run VSE "this week" |
| 2021-10-26 | post 2 | The five presentation levels |
| 2021-10-27 | [post 5](https://www.votingtheory.org/forum/topic/136/new-simple-condorcet-method-basically-copeland-margins/5) | First VSE numbers arrive from Marcus Ogren (screenshot; transcribed below) |
| 2021-10-28 | posts 9–10 | Marketing rationale ("an upgrade from RCV"); ballot language 2.0 |
| 2021-10-31 | post 14 | Marylander's rewrite: shorter, no predictions in ballot text, "margin" because voters know it from sports, elimination reframed as a tiebreaker |
| 2021-11-01 | post 18 | The one-sentence tally: among the candidates tied for most head-to-head wins, elect the one with the best average rank — flagged as equivalent but potentially misleading |
| 2021-11-01 | r/EndFPTP (per electowiki) | Reddit discussion thread starts |
| 2021-11-01→21 | posts 20–22, 28 | Borda-strategy debate (below) |
| 2021-11-07 | Equal Vote (per electowiki, *cn*) | Sara Wolk coins the name "Ranked Robin" |
| 2021-11-08 | electowiki | Sass creates the wiki page ("Intro to new voting method") |
| 2021-11-15 | [post 25](https://www.votingtheory.org/forum/topic/136/new-simple-condorcet-method-basically-copeland-margins/25) | **Renamed Ranked Robin in the thread**; IIA failure conceded in the same post; distinguished from Ranked STAR (which is described as a score method in ranked clothing — a different niche) |
| 2021-11-21 | post 29 | multi_system_fan: tiebreak rules look arbitrary → let voters *vote on the tiebreaker* on the same ballot; rob objects that similar tiebreak options would split the vote |
| 2022-03-02 | posts 39–40 | Coda: Jack Waugh asks whether dropping the Copeland gate (just sum margins over *all* candidates) loses much; answer: that is *identical to Borda* |

## The first VSE numbers (transcribed from the post-5 screenshot)

A phone screenshot of a Slack DM from Marcus Ogren (they/them), 2021-10-27: "VSE sims from two
different runs with 2000 iterations in each" — with "Sass" as the placeholder name for the method:

| method | strategy | run 1 | run 2 |
|---|---|---|---|
| IRV | honBallot | 0.9046497 | 0.8978764 |
| IRV | vaBallot | 0.9077720 | 0.9577976 |
| Minimax | honBallot | 0.9810738 | 0.9763306 |
| Ranked Pairs | honBallot | 0.9810664 | 0.9760153 |
| Schulze | honBallot | 0.9763326 | 0.9676992 |
| Raynaud | honBallot | 0.9786494 | 0.9729025 |
| Smith//IRV | honBallot | 0.9775352 | 0.9725057 |
| **Sass (= Ranked Robin)** | honBallot | **0.9813435** | 0.9753971 |

Read with care: unpublished, 2000 iterations, unknown parameters (Sass immediately asked for more
detail and more strategy runs). Still, the shape is the standard one: the Condorcet completions
cluster within ~0.015 of each other while honest-ballot IRV sits 7–8 points back. Ranked Robin
edges out every other Condorcet method in run 1 and lands mid-pack (behind Minimax and Ranked
Pairs) in run 2 — i.e., the choice of completion rule barely moves VSE; the Condorcet gate does
the work. Sass also mentioned Ogren had run Borda-strategy attacks against it, which it reportedly
held up well against — those numbers were never posted, and the promised John Huang VSE run never
appeared in the thread either.

**As far as I can tell, this screenshot is the only VSE data for Ranked Robin in existence.** A
2026-08-01 sweep found nothing published: Jameson Quinn's
[vse-sim](https://github.com/electionscience/vse-sim) has never contained a Copeland or Ranked
Robin method (full git history and all branches checked — its only Condorcet entries are Schulze
and Ranked Pairs); Huang's [votesim](https://github.com/johnh865/election_sim) *implements*
`copeland()` but no benchmark ever ran it, and his Feb 2021 summary report has no Copeland row;
Ogren's *Candidate Incentive Distributions* paper skips it (and uses CID, not VSE); and the
Wolk/Quinn/Ogren 2023 STAR paper's lone Condorcet method is Smith//Minimax. Equal Vote's accuracy
claims for Ranked Robin lean on Quinn's numbers for *other* Condorcet methods. Closest published
proxies: Quinn's Ranked Pairs/Schulze at ~98% honest-ballot VSE (Ranked Pairs ~86% under
strategy), and Huang's ranked_pairs at 0.849 averaged across strategy profiles.

## The worked examples, transcribed

Both examples use six candidates (Dre, Edith, Frank, Ben, Abby, Cici). Pair totals vary from pair
to pair (equal ranks and truncation ⇒ some ballots express no preference), and the advantage
percentages divide by *all* ballots: N = 68 in the 3-cycle, 69 in the 5-cycle.

### 3-cycle (post 1)

"# of voters who prefer *row* over *column*":

| over → | Dre | Edith | Frank | Ben | Abby | Cici |
|---|---|---|---|---|---|---|
| **Dre** | — | 39 | 15 | 35 | 40 | 36 |
| **Edith** | 24 | — | 32 | 36 | 43 | 35 |
| **Frank** | 48 | 24 | — | 36 | 33 | 36 |
| **Ben** | 32 | 23 | 32 | — | 30 | 32 |
| **Abby** | 28 | 19 | 28 | 24 | — | 28 |
| **Cici** | 32 | 33 | 32 | 30 | 23 | — |

Matchup wins: Dre 4, Edith 4, Frank 4, Ben 2, Abby 1, Cici 0 → finalists {Dre, Edith, Frank}, a
perfect rock-paper-scissors (Dre > Edith > Frank > Dre). Margins among finalists decide it:
**Frank is elected** (he took the largest pairwise win inside the cycle).

### 5-cycle (post 1)

| over → | Dre | Edith | Frank | Ben | Abby | Cici |
|---|---|---|---|---|---|---|
| **Dre** | — | 33 | 20 | 35 | 34 | 44 |
| **Edith** | 25 | — | 37 | 29 | 43 | 43 |
| **Frank** | 49 | 24 | — | 37 | 28 | 45 |
| **Ben** | 32 | 31 | 32 | — | 30 | 32 |
| **Abby** | 35 | 26 | 34 | 25 | — | 45 |
| **Cici** | 16 | 26 | 16 | 31 | 24 | — |

Five candidates tie at 3 wins each (only Cici loses everything) → five finalists, and the totals
rank Edith +29.0, Frank +21.7, Ben −1.4, Abby −21.7, Dre −27.5: **Edith is elected**. A nice
stress-test of step 4 — the tiebreaker handles a five-way tie as easily as a three-way one.

### Errata: both example images have arithmetic slips

Re-deriving every number from the matrices (script-checked 2026-08-01):

| Image | Slip | Image says | Matrix says |
|---|---|---|---|
| 3-cycle | Frank ↔ Dre margin (33 votes / 68) | ±45.6 | **±48.5** |
| 3-cycle | Edith-over-Frank *cell* contradicts its own sentence (which correctly says 11.8) | +18.8 | **+11.8** |
| 3-cycle | Totals | Dre −23.5, Edith −3.3, Frank +33.8 | **−26.5, −10.3, +36.8** |
| 5-cycle | Dre ↔ Abby margin in Dre's block (1 vote / 69) — Abby's own block correctly says ±1.4, so the image contradicts itself | −8.7 | **−1.4** |
| 5-cycle | Dre's total | −34.8 | **−27.5** |

Every other number in both images is exact. Neither slip changes the winner (still Frank, still
Edith). The stray +18.8 in the 3-cycle happens to equal the Edith-over-Frank margin *from the
5-cycle* — my guess is a copy-paste between the two spreadsheets.

**The takeaway sanity check:** within any finalist set, relative advantages are antisymmetric, so
the finalists' total advantages **must sum to zero**. The published 3-cycle totals sum to +7.0 and
the 5-cycle's to −7.3 — either sum, on its own, proves an arithmetic error without recounting a
single cell. (The corrected totals sum to 0.0 exactly.) Cheap invariant, worth running against any
Ranked Robin results display.

## What the official spec became (electowiki, checked 2026-08-01)

The thread's step 4 is only the first rung of what the
[electowiki article](https://electowiki.org/wiki/Ranked_Robin) formalized as **degrees of
tiebreakers** (post 28 already points readers to the wiki for the 2nd Degree):

| Degree | Rule |
|---|---|
| 1st | Among the finalists (tied on matchup wins), greatest sum of win margins *over the other finalists* — the thread's step 4 |
| 2nd | Still tied → greatest sum of win margins over *all* candidates |
| 3rd | Still tied → fewest total votes for-and-against (least polarizing); the article recommends **not** using this or deeper rungs in public elections — lots or a new election shake voter trust less |
| 4th | Shortest-beatpath strengths among the tied |

Other things the article settled that the thread left open: unranked candidates count as tied for
last (Marylander's point, adopted); ties after the 1st Degree are about as rare as FPTP ties, and
after the 2nd rarer still; a full criteria table (passes Condorcet, Smith, ISDA, majority,
Condorcet loser, monotonicity, reversal symmetry, resolvability; fails IIA, participation,
consistency, clone independence — clone failures only possible when there's no Condorcet winner,
and cloning can never make the cloned candidate lose); and the lineage claim that the method goes
back to Ramon Llull (1299) via Condorcet and Copeland, with the 1st-Degree completion
independently described by Dasgupta & Maskin ("The Fairest Vote of All", *Scientific American*
2004). One 2025 postscript: Sara Wolk clarified on the talk page that "Ranked Robin" was always
meant as an approachable umbrella name for Condorcet voting generally, not only this exact
procedure — the brand loosening back toward the thread's original pitch ("Condorcet, made
explainable").

The loosening is now official policy: the current
[equal.vote/ranked_robin](https://equal.vote/ranked_robin) page (checked 2026-08-01) no longer
fixes the margins rule at all. It describes the head-to-head core, then offers jurisdictions a
**menu of cycle tiebreakers** — Copeland (tied candidate with the most matchup wins), Favorite
(top-ranked on the most ballots; sourced to Vermont's 2024 bill H.424), and Smith-Minimax
(smallest worst-loss margin) — with advice to pick one transparent rule in advance and stick with
it. "Total advantage" and the five presentation levels appear nowhere on it. So the thread's
specific design survives in electowiki's 1st Degree and in BetterVoting's tabulator, while the
equal.vote brand has become the Condorcet umbrella Wolk described.

## What the thread teaches

- **The Copeland gate is the whole firewall against Borda pathologies.** The finalist stage is
  mathematically tournament-Borda (Sass concedes the equivalence, and the "best average rank"
  one-liner leans on it). The identity is classical — Duncan Black (1958) already noted a Borda
  score can be read off the pairwise matrix as a row sum, and the margins row-sum is an
  order-preserving affine transform of it (sources collected in the notes of
  [electowiki's Borda article](https://electowiki.org/wiki/Borda_count): Levin & Nalebuff; Wright
  & Barry). Two fine points: the identity stays exact under equal ranks and truncation only with
  the half-point "tournament" convention on both sides, and summing margins *within the finalist
  set* computes the Borda count of the reduced election among finalists — a different quantity
  from full-election Borda, which is precisely what the gate changes. Drop the gate and sum
  margins over *all* candidates — Jack Waugh's 2022 simplification — and you have literally
  reinvented Borda (post 40), with its teaming and burying problems. Marylander's framing (post 22): it's easier to attack Copeland directly than the Borda
  count *inside the tied set*. Sass's list of differences from classic Borda: finalists only,
  equal ranks allowed, skipped ranks ignored, no completion requirement, tournament-style
  counting. Compare the [BV1550 post-mortem](ranked-robin-results-explained.md): Copeland is
  margin-blind and ties; Borda sees margins and decides — each is the other's blind spot, and
  Ranked Robin is precisely the "Copeland, then Borda-among-tied" splice. (Note the official 2nd
  Degree — margins over *all* candidates — is exactly the rule post 40 calls Borda; by then the
  field is restricted to Copeland winners, which is what keeps it defensible.)
- **Criteria honesty, and criteria-as-spectrum.** Ranked Robin fails IIA, conceded the moment it
  was named. Sass's defense (post 28) is that pass/fail is reductive — adding a weak candidate
  gives every serious contender exactly one more win, so *in practice* only deep-tiebreaker
  elections are IIA-fragile. Marylander adds the political-science version (post 27): the public
  doesn't check criteria, it reacts to pathological elections after the fact — IRV advocates can
  see how 1991's Lizard-vs-Wizard runoff shames top-two without noticing it shames IRV too.
- **Hand-countability was designed in, not bolted on.** Post 15 gives three worked procedures for
  building a preference matrix at a precinct (per-ballot matrix ticks; per-pair passes; per-pair
  three-pile sorting for recounts) — the substance behind "precinct-summable," and the direct
  ancestor of the "preference matrix for precincts and nerds" band in the example images. The
  electowiki article expanded this into the local-recount and risk-limiting-audit argument
  against IRV.
- **The tiebreaker-legitimacy worry aged well.** multi_system_fan (post 29) argued tiebreak rules
  look arbitrary and are a PR liability, proposing voters choose the tiebreaker on the ballot
  itself (rob: those options would vote-split). Five years later BetterVoting's random third rung
  produced exactly the predicted legitimacy incident — the unstable-winner reports of
  [#885](https://github.com/Equal-Vote/bettervoting/issues/885) /
  [#886](https://github.com/Equal-Vote/bettervoting/issues/886) and the deterministic-tiebreak ask
  of [#1063](https://github.com/Equal-Vote/bettervoting/issues/1063). The electowiki article's own
  advice (prefer lots or a fresh election over 3rd-Degree cleverness) is the same instinct.
- **Ballot-language lessons that generalize.** Marylander's rewrite principles: fewer words; define
  nothing the public already knows ("margin" from sports); never put predictions ("in most
  elections…") in ballot text; make eliminations implicit by framing the second stage as a
  tiebreaker. Sass's counter-worry: "margin" and "average rank" both invite voters to think rank
  *distances* matter (they don't — only order does), so on ballots redundancy beats concision.
  Both wanted real field testing; none is reported in the thread.
- **A cardinal sibling was proposed the same week.** rob's
  [Reverse STAR (topic 130)](https://www.votingtheory.org/forum/topic/130/star-like-method-reverse-star)
  is the same skeleton on score ballots: pairwise wins first, and among those tied for most wins,
  highest total score — STAR's two stages in reverse order. rob's own one-sentence framing of the
  two methods differed by a single word: best average *rank* vs. best average *score*.

## Open questions (as of the thread; status 2026-08-01)

- **Burying/compromising inside the finalist set** — Jack Waugh's Gibbard-flavored challenge.
  Ogren's Borda-strategy runs were mentioned secondhand but never posted, and no published
  strategy-resistance numbers for Ranked Robin exist (the electowiki article offers criteria
  arguments, not simulation results). Still open after
  [my honest-ballot VSE run](ranked-robin-vse-run.md) — strategy runs need votesim's tactical
  harness or vse-sim.
- ~~VSE, published~~ — **resolved, negatively (2026-08-01):** nothing citable was ever published
  anywhere; the thread's DM screenshot is the only known VSE data for the method (details in the
  VSE section above). **Follow-up, same day:** I implemented Ranked Robin in Huang's votesim
  (starting from its unused `copeland()`) and ran 18,000 spatial elections — it tops a
  statistically indistinguishable Condorcet cluster, ~3.6 VSE points above honest IRV, and its
  margins ladder turns out to be VSE-neutral but halves the unresolved-tie rate:
  [ranked-robin-vse-run.md](ranked-robin-vse-run.md).
- **3+-way Copeland ties in production:** the thread's showcase examples are a 3-way and a 5-way
  tie decided by total margins (the official 1st Degree), but BetterVoting's `RankedRobin.ts`
  ladder (per the [BV1550 note](ranked-robin-results-explained.md)) applies head-to-head only when
  *exactly two* tie, then falls to random — for a 3-way tie like the thread's own example, does
  the deployed tabulator actually run the margins stage, or skip straight to the random rung?
  Needs a source dive; if it skips, that's a spec-vs-implementation gap worth filing upstream.
- **Field testing of ballot language** — proposed repeatedly, never reported.

## Links

- The thread: [topic 136](https://www.votingtheory.org/forum/topic/136/new-simple-condorcet-method-basically-copeland-margins) — key posts: [1 (proposal)](https://www.votingtheory.org/forum/topic/136/new-simple-condorcet-method-basically-copeland-margins/1), [5 (VSE)](https://www.votingtheory.org/forum/topic/136/new-simple-condorcet-method-basically-copeland-margins/5), [25 (naming)](https://www.votingtheory.org/forum/topic/136/new-simple-condorcet-method-basically-copeland-margins/25), [40 (Borda coda)](https://www.votingtheory.org/forum/topic/136/new-simple-condorcet-method-basically-copeland-margins/40)
- Image uploads transcribed above: [ballot language](https://www.votingtheory.org/forum/assets/uploads/files/1635211207586-ballot-language-1.0-resized.png) · [Condorcet-winner display](https://www.votingtheory.org/forum/assets/uploads/files/1635211235473-condorcet-winner.png) · [3-cycle](https://www.votingtheory.org/forum/assets/uploads/files/1635211254794-3-cycle.png) · [5-cycle](https://www.votingtheory.org/forum/assets/uploads/files/1635211268576-5-cycle.png) · [VSE screenshot](https://www.votingtheory.org/forum/assets/uploads/files/1635347455186-img_4086.png)
- Where it landed: [Ranked Robin on electowiki](https://electowiki.org/wiki/Ranked_Robin) (incl. a worked example needing all four tiebreak degrees, with a [live BetterVoting election](https://bettervoting.com/3r3yf7/results)) · [equal.vote/ranked_robin](https://equal.vote/ranked_robin) · [BetterVoting results explainer](ranked-robin-results-explained.md)
- Kin: [Reverse STAR (topic 130)](https://www.votingtheory.org/forum/topic/130/star-like-method-reverse-star) · Dasgupta & Maskin, "The Fairest Vote of All", *Scientific American* 290(3), 2004
- [Glossary](glossary.md) — Copeland score, margin, Borda, Ranked Robin
