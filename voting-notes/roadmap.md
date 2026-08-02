# Roadmap — what to add next

A gap analysis of these notes, run 2026-08-02: the existing files were mapped topic-by-topic
(958 coverage entries across 21 notes and the glossary), then compared against the field from five
angles — classic social choice theory, the single-winner method landscape, multi-winner/PR, strategy
and empirics, and adjacent/frontier topics. What follows is the merged, prioritized result. Entries
link to the existing note each new one should connect to.

The test applied throughout: does the topic serve the STAR / approval / RCV / Condorcet focus, and
does it suit the house method — claims checked against sources, worked small profiles, verifiers?

---

## Top tier

1. ✅ **Condorcet–IRV hybrids: Smith//IRV, Benham, BTR-IRV, Woodall, Tideman's Alternative.**
   **Done 2026-08-02** — [condorcet-irv-hybrids](condorcet-irv-hybrids.md), with an exhaustive
   3-candidate burial search that also delivers a down payment on item 2.
   The direct fix for the center-squeeze pathologies documented in
   [hare-center-squeeze-examples](hare-center-squeeze-examples.md), on the same ranked ballots.
   Smith//IRV exists here only as a VSE-table row; the others not at all. Green-Armytage's
   Condorcet–Hare strategy-resistance results are the key literature — the same author audited in
   [wikipedia-talk-strategic-voting-draft](wikipedia-talk-strategic-voting-draft.md). Trace each
   hybrid over the existing 75- and 99-voter profiles; cover the burial-vulnerability trade-off
   against plain IRV.

2. **Burial vulnerability of Condorcet methods.**
   Waugh's burying/compromising question is flagged *still open* in
   [ranked-robin-origins](ranked-robin-origins.md), and burial is the strategic objection to
   Copeland+Borda methods like Ranked Robin — the largest hole in the deepest strand of these notes.
   Sources: Green-Armytage 2011, Ogren 2024, Robinette 2023. The verifier infrastructure already
   exists (5-cycle and BV1550 profiles).

3. **Strategic-voter VSE simulations.**
   [ranked-robin-vse-run](ranked-robin-vse-run.md) is honest-ballots-only and names this as the
   follow-up. Equal Vote's incentive ratios (STAR 1:1, IRV 3:1, plurality 18:1) rest on strategy-mix
   runs not yet reproduced here; votesim is installed and verified. Merrill 1984 supplies the
   academic lineage.

4. **Burlington 2009, full workup.**
   Name-dropped in three files, never worked — the only US election with published ballots showing
   IRV non-monotonicity in the wild, the real-world twin of
   [lumen-75-ballot-four-winners](lumen-75-ballot-four-winners.md). Ballot data is public, so the
   recompute-everything method applies directly. The 2010 repeal / 2021 partial readoption arc
   belongs in [whoops](whoops.md).

5. **Real STAR ballot data: bullet-voting and min-maxing rates.**
   Bullet-voting is measured here for approval (~80% at MAA, Dartmouth, IEEE) and framed as
   approval's practical failure mode; the parallel question for STAR — do real voters use the middle
   scores the runoff depends on? — is unanswered. Testable against Multnomah Dems / IPO / star.vote
   data. Connects to [star-strategy-pages-vs-wikipedia](star-strategy-pages-vs-wikipedia.md).

6. **Allocated Score / STAR-PR.**
   Mention-only in [cardinal-voting-systems](cardinal-voting-systems.md) and the glossary, yet it is
   Equal Vote's own proportional method. Quota allocation on 5-star ballots, fractional surplus
   handling, comparison against SSS and Sequential Monroe on shared profiles, known monotonicity
   quirks — a worked spec that doubles as a test oracle.

7. **Justified representation (JR / PJR / EJR) + Method of Equal Shares.**
   The modern proportionality axioms for approval/cardinal committees — the framework that
   adjudicates the SPAV/PAV/Phragmén/SSS comparison already in
   [cardinal-voting-systems](cardinal-voting-systems.md) (PAV satisfies EJR; SPAV fails even PJR).
   Equal Shares is the flagship EJR method with real deployments (participatory budgeting in
   Wieliczka, Aarau) and the direct competitor to SSS. Small profiles, exhaustive committee checks —
   ideal verifier material. Completes the column PSC starts in
   [single-transferable-vote](single-transferable-vote.md).

8. **Single-peakedness, Black's median voter theorem, Sen's value restriction.**
   The theory gap under everything: nearly every worked example in these notes quietly assumes
   single-peakedness, center squeeze is literally "the median voter's candidate gets eliminated,"
   and Black's theorem explains the 88.7% Condorcet-winner rate measured in
   [ranked-robin-vse-run](ranked-robin-vse-run.md) — yet the theorem is never stated. Sen 1966
   unifies it with the Inada entry already in
   [brandl-peters-approval-characterizations](brandl-peters-approval-characterizations.md).

## Second tier

- **Kemeny–Young.** The one major Condorcet completion missing from
  [legrand-ranked-ballot-methods](legrand-ranked-ballot-methods.md) — while Young–Levenglick 1978,
  the theorem that *characterizes* it, is already covered. Young 1988 (Kemeny as maximum-likelihood
  estimate under Condorcet's error model) brings the **Condorcet jury theorem** and the epistemic
  reading of Condorcet methods along for free. NP-hard with cheap look-alikes, pairing with the
  existing Dodgson correction.
- **Gibbard 1978 + Duggan–Schwartz.** [math-in-society-lippman](math-in-society-lippman.md) calls
  Gibbard 1978 "the result that actually constrains cardinal methods," then never treats it. Also
  fixes Horn erratum 9's loose end (the multi-winner mislabel; Duggan–Schwartz is the right theorem
  for irresolute rules).
- **Maine RCV record.** The missing half of the empirical story next to the deep Alaska coverage:
  2016 adoption, constitutional litigation, the 2018 CD-2 count, people's-veto fights, four cycles
  of exhaustion data.
- **Primary architecture.** Top-two, top-four/Final Five, fusion voting, and the Alaska 2024 repeal
  referendum. The notes analyze Alaska 2022's tabulation but never the primary that produced its
  candidate set. Connects to [rcv-and-core-support](rcv-and-core-support.md).
- **Two-round runoff vs IRV.** France 2002, contingent/supplementary vote, the UOCAVA problem —
  what "instant" actually deletes (inter-round campaigning and information). Half-covered already in
  [approval-voting](approval-voting.md) and [ranked-robin-results-explained](ranked-robin-results-explained.md).
- **STAR's design-space siblings: 3-2-1, Smith//Score, Reverse STAR.** Completes the 2×2 of stage
  orderings (score→pairwise = STAR; pairwise→score = Smith//Score/Reverse STAR) and grounds the
  threshold-then-Condorcet ideas in [rcv-and-core-support](rcv-and-core-support.md) in named
  literature. 3-2-1 is Quinn's sibling method, designed against the bullet-voting incentive measured
  in the approval notes.
- **Split Cycle and Stable Voting.** Holliday–Pacuit's margin-based methods are the refereed version
  of the spoiler-immunity theorem proved in
  [ranked-robin-thread-claims-checked](ranked-robin-thread-claims-checked.md), and they modernize a
  Condorcet-completion survey that currently stops at the classical set.
- **Party-list PR: D'Hondt / Sainte-Laguë = Jefferson / Webster.** Builds the bridge the "party-list
  degenerate case" diagnostic in [cardinal-voting-systems](cardinal-voting-systems.md) leans on;
  divisor methods are already half-covered in [math-in-society-lippman](math-in-society-lippman.md).
- **Ballot exhaustion data.** Burnett–Kogan 2015 (9.6–27% in four cities), FairVote's
  counter-analyses, Alaska/Maine numbers — turns the talking-point dispute already documented into
  numbers.
- **Risk-limiting audits and RAIRE.** The operational half of the summability arguments: whether
  IRV, STAR, and Ranked Robin admit efficient audits is a live deployment question.

## Self-flagged gaps

[mdi-trivia-cards](mdi-trivia-cards.md) names two of its own:

- **Gerrymandering metrics** — efficiency gap, mean-median, partisan symmetry, Polsby–Popper.
  Arithmetic on wasted votes, ideal for the verifier style; and the efficiency gap's own pathologies
  (it brands proportional outcomes gerrymanders at lopsided statewide shares) suit the
  audit-the-advocacy-metric tradition.
- **Electoral College mechanics and NPVIC** — winner-take-all as a state choice, the +2 effect,
  faithless electors post-*Chiafalo*, the compact's status and legal contingencies. The historical
  pieces (1800 tie, 12th Amendment) are already in [approval-voting](approval-voting.md).

## Skip or defer

Quadratic voting, liquid democracy, sortition and citizens' assemblies, futarchy, and LLM-mediated
deliberation all sound current but sit off this library's center of gravity — ballot and tabulation
design. Sen's liberal paradox and judgment aggregation (List–Pettit) are completeness items for the
impossibility shelf, not priorities. Revisit if the library's scope widens from elections to
collective decision-making generally.
