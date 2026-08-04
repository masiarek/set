# BetterVoting issues ↔ these notes

The join between this folder and [Equal-Vote/bettervoting](https://github.com/Equal-Vote/bettervoting)'s
tracker. **Not an index of everything filed** — there are 257 issues authored there, 160 of them open,
and listing them here would duplicate the tracker badly and go stale within a week. What this page
covers is the intersection worth curating: **the issues these notes back with recomputation**, and the
findings in these notes that could become issues but haven't.

The reason to keep it: an issue's credibility rests on whether the number in it was checked or
eyeballed, and that fact lives here rather than in the tracker. If a maintainer pushes back on any row
below, the verifier named in it is the answer.

Checked against the tracker on **2026-08-02**; states drift, so re-check before leaning on the status
column.

---

## Filed, and backed by a verifier here

| # | state | what it claims | backed by |
|---|---|---|---|
| [885](https://github.com/Equal-Vote/bettervoting/issues/885) | closed *(not planned)* | Unstable tie-breaking in Ranked Robin. **Closed on my own re-reading** — the original report misread a Copeland win. | [ranked-robin-results-explained](ranked-robin-results-explained.md) |
| [886](https://github.com/Equal-Vote/bettervoting/issues/886) | closed *(completed)* | "Who won — Bob or Ann?" on test case BV1550, 3 candidates, 12 ballots. Fixed by the `JacksonLoper/tiebreaker` merge of 2026-05-12; results pages now show "Tied!" / "won after tiebreaker". | [ranked-robin-results-explained](ranked-robin-results-explained.md) |
| [1468](https://github.com/Equal-Vote/bettervoting/issues/1468) | **open** | Chart stars the wrong candidate when a Copeland tie is broken by the head-to-head runoff: header uses `results.elected`, chart renders row 0 of the `(copelandScore desc, tieBreakOrder asc)` pre-sort because `RankedRobin.ts` passes no `evaluate` to `runBlocTabulator`. | [ranked-robin-results-explained](ranked-robin-results-explained.md); five-ballot runoff-rung fixture in [bv-sep-test-cases](bv-sep-test-cases.md) + [`ranked_robin_noshow.py`](code/sep-voting-methods/ranked_robin_noshow.py) |
| [1469](https://github.com/Equal-Vote/bettervoting/issues/1469) | **open** | 3+-way Copeland ties skip the official 1st-Degree margins tiebreaker and fall straight to random — the margins rule is not implemented at any tie size. | [ranked-robin-thread-claims-checked](ranked-robin-thread-claims-checked.md) + [`code/thread136-claims/verify.py`](code/thread136-claims/verify.py) |
| [1471](https://github.com/Equal-Vote/bettervoting/issues/1471) | **open** | `ResultsBarChart` puts percentage labels (denominator = all bars, line 52) and the "majority threshold" marker (denominator excludes the last bar, lines 83–88) on one axis. A 33% winner is drawn past a line labelled "majority". Presentation only — tabulation and legend wording are both correct. | [results-chart-denominators](results-chart-denominators.md); live repros [2dm864](https://bettervoting.com/2dm864/results) (STAR) and [hx848r](https://bettervoting.com/hx848r/results) (IRV) |

The proof that makes #1469 bite is in the thread-claims note: with three candidates and no drawn
matchups **every cycle is a 3-way tie**, so the implemented two-way branch can never fire on a cycle
at all — it only catches draw-induced ties like the BV1550 Ann/Bob case.

## Filed by others, relevant here

| # | state | why it matters to these notes |
|---|---|---|
| [1063](https://github.com/Equal-Vote/bettervoting/issues/1063) | **open** | Deterministic tie-breaking via candidate lot numbers. The standing fix for every random-rung finding below; [ranked-robin-vse-run](ranked-robin-vse-run.md) puts a number on how often the rung fires. |
| [1168](https://github.com/Equal-Vote/bettervoting/issues/1168) | **open** | @jacksonloper: document that Ranked Robin uses Copeland tie-breaking. [ranked-robin-origins](ranked-robin-origins.md) is the history that documentation would need. |
| [1432](https://github.com/Equal-Vote/bettervoting/issues/1432) | **open** | Surface tie-break explanations in the results UI and JSON/CSV export. |
| [1379](https://github.com/Equal-Vote/bettervoting/issues/1379) | **open** | BV555, STAR scoring-round 3-way tie — the STAR-side twin of the Ranked Robin tie work. |

## Posted as comments, not issues

- **[#1468 comment, 2026-08-02](https://github.com/Equal-Vote/bettervoting/issues/1468#issuecomment-5160176044)**
  — a five-ballot, four-candidate profile that exercises the same pairwise-runoff rung as the issue
  (smaller than its own 21-ballot repro), plus the same profile minus one ballot as a second
  runoff-rung case. The pair is also a **no-show paradox**, flagged explicitly as *not a bug*: Moulin's
  theorem guarantees it for any Condorcet-consistent method at four or more candidates. Text as sent:
  [bv-1468-comment-posted](bv-1468-comment-posted.md).

  Stated in the comment and worth repeating: the **tabulation** was computed and hand-checked, the
  **display** behaviour was not tested against this profile.

- **[#1471 comment, 2026-08-03](https://github.com/Equal-Vote/bettervoting/issues/1471#issuecomment-5173488984)**
  — the screenshots the original report was missing, taken from two live elections rather than the
  sandbox: [2dm864](https://bettervoting.com/2dm864/results) (STAR) and
  [hx848r](https://bettervoting.com/hx848r/results) (IRV). Adds three things not in the issue: STAR's
  legend names its denominator less clearly than IRV's; a "majority of all voters" line would fall
  **off the right edge** of the STAR plot; and the marker is set on only the first two rows
  (`i < 2 ? m : null`), so the dashed line stops before the row that most visibly crosses it. Figures
  and reasoning: [results-chart-denominators](results-chart-denominators.md).

- **[#1471 comment, 2026-08-04](https://github.com/Equal-Vote/bettervoting/issues/1471#issuecomment-5178781174)**
  — the **Bloc STAR** half, on the live QA election [fk38pk](https://bettervoting.com/fk38pk/results)
  (BV1815 — 3 candidates, 2 seats, 3 ballots), which carries the best and worst case of the issue one
  click apart: seat 1 has no Equal Support, so both denominators agree and the chart is honest; seat 2
  draws all three bars at 33% with the marker at **1 vote**, level with *both* candidate bars, in a
  runoff nobody won (the seat went to the score rung). Two points new to the issue: the widget renders
  once per `roundIndex`, so a Bloc race repeats the defect per seat and later seats should show it
  worst; and `m = sum/2` is **half, not a majority**, so a denominator-only fix still ends both bars on
  the line. Carries the LH reports for the seat pair and for a single-winner control. Text as sent:
  [bv-1471-bloc-comment-posted](bv-1471-bloc-comment-posted.md); figures added to
  [results-chart-denominators](results-chart-denominators.md).

  Verification split, as stated in the comment: tabulation checked two ways (LH engine + BV's own
  export for `fk38pk` — same winners, same runoff counts, same `tieBreakType`); the chart readings come
  from screenshots taken 2026-08-04 and match `ResultsBarChart.tsx` on `main`; no proposed fix tested.

- **[#904 comment, 2026-08-04](https://github.com/Equal-Vote/bettervoting/issues/904#issuecomment-5178824529)**
  — **retracting my own Should-Be.** #904 (open since April 2025) asks for one string: the display name
  for STAR under Basic Multi-Winner. It proposes **"STAR Bloc Voting"**. Five sources say **"Bloc
  STAR"**, adjective first — the BPML naming doc the issue itself links, technical specifications
  1.c/1.e, starvoting.org/multi_winner, electowiki, and `starvote`'s own `Bloc_STAR_Voting`. So does
  the house pattern: `en.yaml:161` already ships the sibling as **Proportional STAR Voting**, and the
  two render one above the other in the same list. And the help page in #1474 uses "Bloc STAR"
  throughout, so shipping "STAR Bloc" would put two names for one method on one site. Sources and the
  local propagation (`star-voting-library` publishes under `02_STAR_Bloc/`):
  [bloc-star-bpml-fixtures](bloc-star-bpml-fixtures.md).

  Nothing in the [sizing note](https://github.com/masiarek/bettervoting-qa/blob/master/issues/904-star-bloc-naming.md)
  changes — same chokepoint, same three render sites, same E2E selector, still display-only, still
  about half a day. Only the string does. **Blocked on an upstream answer** rather than on code: worth
  hearing whether Equal Vote has a house preference before opening the PR, since renaming a user-facing
  label twice is worse than asking once.

## Sent as a pull request

- **[#1474, 2026-08-04](https://github.com/Equal-Vote/bettervoting/pull/1474)** — a Bloc STAR help page
  for docs.bettervoting.com (`docs/help/bloc_star.md`), plus one line giving `tips.bloc_multi_winner`
  the `learn_link` it was the only method tip to lack. The gap it fills: BetterVoting *runs* Bloc STAR
  (STAR + **Basic Multi-Winner**) but documents it nowhere — the ballot text sits inside
  `paper_ballots.md`, `faq.md` never says "multi-winner", and the at-large / Section 2 Voting Rights
  Act warning from [starvoting.org/multi_winner](https://www.starvoting.org/multi_winner) appears on no
  BV page at all. Related to [#1086](https://github.com/Equal-Vote/bettervoting/issues/1086) (results
  page links "How STAR voting works" for a Bloc race, issue suggests electowiki) — the PR gives that
  link a first-party target but does not touch the results page, so #1086 stays open.

  The worked example is the 3-ballot `Over_50_percent_bloc` profile, re-run here through the vendored
  `starvote` engine: A wins seat 1 outright, then the seat-2 runoff **ties 1–1 with one no-preference
  ballot** and the score rung elects C. Worth keeping in mind whenever "elects majority preferred
  winners" is quoted: C's seat rests on one voter in three — the same denominator question as
  [#1471](https://github.com/Equal-Vote/bettervoting/issues/1471)
  ([results-chart-denominators](results-chart-denominators.md)).

  One wording deviation flagged in the PR: starvoting.org says at-large bloc voting "was banned in the
  Voting Rights Act". The page says instead that such systems have repeatedly been struck down **under
  Section 2** where they diluted minority voting strength, which is what the record supports. The
  recommendation is unchanged.

  **Corrected 2026-08-04 (`fe6c1773`), after the PR was opened.** The page had said a runoff
  percentage is "a share of the voters who expressed a preference between *those two finalists*, not a
  share of everyone who voted" — which is the **opposite** of #1471. The bar labels divide by every
  ballot cast; it is the dashed majority threshold that divides by the preference-expressing subset
  (`ResultsBarChart.tsx:85` drops the last row from the marker's denominator only). Documenting the
  reverse of an issue filed from the same desk would have been the worst version of this mistake. The
  replacement also names the on-screen category, **Equal Support** (`en.yaml:304`), so a reader can
  find it on the chart. This paragraph carried the same error and has been fixed above.

## Checked and deliberately *not* filed

Recording these matters as much as the filings — it stops the same non-bug being re-reported later.

- **BV's IRV does not inherit the SEP entry's "eliminate everyone" defect.** Pacuit's printed Hare and
  Coombs definitions return ∅ on a perfect three-way first-place tie. `IRV.ts` pops exactly one
  candidate per round and sets `tieBreakType: 'random'` when the last two are level, so the degenerate
  profile is safe. Filing it would have been wrong. [sep-voting-methods](sep-voting-methods.md),
  finding 1.
- **The Ranked Robin no-show paradox is not a defect.** Guaranteed by Moulin's theorem for any
  Condorcet-consistent method at m ≥ 4; no tie-breaking change can remove it. Worth a regression
  fixture, not a bug report.
- **Ranked Robin is clean at three candidates.** No no-show paradox in any of the 12,375 anonymized
  3-candidate profiles up to 11 voters, so a three-candidate test would assert the wrong thing.

## Not filed yet — candidates

- **Two IRV regression fixtures**: a 17-ballot monotonicity failure (raising A loses A the election;
  no tiebreak involved) and a 19-ballot profile giving three different winners across
  Plurality-runoff / IRV / Coombs / Borda. Kept out of #1468 because they are unrelated to that
  display bug. Draft text in [bv-sep-test-cases](bv-sep-test-cases.md).
- **`IRV.test.ts` has no pathology coverage at all** — five tests, all ballot plumbing, and the suite
  greps clean for `condorcet|monoton|no-show|paradox|cycle`. The gap itself may be worth raising
  separately from any particular fixture.

## Live test elections

- **mj26yj** — [results](https://bettervoting.com/mj26yj/results), "BV1550-R1 — Ranked Robin — 3 cand —
  12 ballots — RRBN retest", created 2026-08-01 via the public API as a guest, still open. Owner is
  the guest `temp_id` `61abacb9-15a6-49f2-b8bd-16c8764783f4`; administering or closing it needs that
  set as the `temp_id` cookie on bettervoting.com, or the election claimed from a signed-in account.

- **xw23m9** — [results](https://bettervoting.com/xw23m9/results), "BV2263 — Over 50%: every point on
  every ballot", minted 2026-08-04 with `create_bv_test_election.py` (owner = the real BV account, not
  a guest). Three voters, three candidates, A scored 5 by every voter: score share, ballot share and
  decided-voter share all read 100%, which makes it the **control** for the denominator work — the one
  configuration where the runoff chart's labels and its majority marker cannot disagree. It renders
  correctly today, and the #1471 comment above links it as the regression fixture for whichever fix
  lands. BV agrees with LH line for line (A wins; 15 / 1 / 0; runoff 3–0, no Equal Support;
  `tieBreakType: "none"`). Two-seat twin: BV1815 `fk38pk`. Case files in star-voting-library at
  `01_STAR/02_Examples/cases/bv2263_xw23m9_over_50_percent.yaml` (renamed from
  `over_50_percent_star_c3_b3` once it stopped being LH-only; the old page URL — the one baked into
  xw23m9's permanent description — is kept alive by a `redirect_maps` entry in `mkdocs.yml`).

## Related local material

- [ranked-robin-results-explained](ranked-robin-results-explained.md) — the results-page note where
  most of this work started, and BetterVoting's tie-break ladder in full
- [ranked-robin-thread-claims-checked](ranked-robin-thread-claims-checked.md) — the cycle/tie theorem
  behind #1469
- [bv-sep-test-cases](bv-sep-test-cases.md) — the SEP-derived fixtures and what fits where
- [sep-voting-methods](sep-voting-methods.md) — Moulin's theorem, and the no-show witness
- [glossary](glossary.md) — Copeland, the tie-break ladder, no-show paradox
