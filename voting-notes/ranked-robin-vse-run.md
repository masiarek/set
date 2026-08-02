# Running the missing VSE: Ranked Robin in votesim (2026-08-01)

The [origins note](ranked-robin-origins.md) established that the only VSE data for Ranked Robin
in existence is a 2021 Slack-DM screenshot, and that John Huang's
[votesim](https://github.com/johnh865/election_sim) ships an unused `copeland()` that no benchmark
ever ran. So this note closes that gap: I implemented Ranked Robin in votesim, verified it, and
ran it against the field. Patch and scripts:
[code/ranked-robin-votesim/](code/ranked-robin-votesim/).

## Setup

- **Codebase:** johnh865/election_sim (2021; needs `scipy==1.11.4`/`numpy 1.26` on Python 3.12 —
  newer scipy removed a private interpolate API it imports).
- **Implementation:** `ranked_robin` added to `votesim/votemethods/condorcet.py`, built on the
  same machinery as the unused `copeland()`: Copeland tally as sign-of-margins row sum, then the
  [electowiki ladder](https://electowiki.org/wiki/Ranked_Robin) — 1st Degree (sum of margins among
  the tied finalists), 2nd Degree (sum of margins over all candidates) — with any remaining tie
  returned to the harness, which breaks it randomly (standing in for the lots/new-election
  recommendation). Registered in `ranked_methods`, so votesim hands it ranked ballots
  automatically. One convention note: votesim's `pairwise_rank_matrix` counts unranked candidates
  below every ranked one (its docstring says otherwise; the code is right), matching Ranked
  Robin's official ballot rules.
- **Verification** ([verify_ranked_robin.py](code/ranked-robin-votesim/verify_ranked_robin.py)):
  an independently written from-scratch reference implementation (pure loops, no votesim helpers)
  agreed with the patched method on **20,000 fuzzed elections with zero mismatches** (strict and
  truncated ballots, 3–6 candidates); hand-built cycle cases resolve exactly per the rule; and the
  zero-sum invariant on finalist margins — the same check that
  [caught the arithmetic errata](ranked-robin-origins.md#errata-both-example-images-have-arithmetic-slips)
  in the 2021 thread's images — was asserted on every tied election.
- **Model:** votesim's spatial model, **honest ballots only**. 100 voters, ndim ∈ {1, 2, 3} ×
  cnum ∈ {3, 5, 7} × 2,000 seeds = **18,000 electorates**, each method run on the *same cached
  ballots* per electorate, so method comparisons are paired. VSE =
  `regret_efficiency_candidate` (winner regret normalized between best and average candidate).
- **Caveats:** no strategy runs (votesim's tactical machinery is a much bigger lift); honest
  spatial ballots are complete strict rankings, so Ranked Robin's equal-rank and truncation
  handling is verified but not exercised in the VSE numbers; absolute VSE levels depend on model
  parameters (tol=1, linear utility base) — the paired *comparisons* are the point, not the
  absolute values (the DM screenshot's ~0.98s came from a different simulator and parameters).

## Results — mean honest-ballot VSE, n = 18,000

| method | mean VSE | paired Δ (RR − method) | significant? |
|---|---|---|---|
| **ranked_robin** | **0.8372** | — | — |
| copeland (random tiebreak) | 0.8371 | +0.0001 ± 0.0014 | no |
| smith_minimax | 0.8367 | +0.0005 ± 0.0018 | no |
| ranked_pairs | 0.8363 | +0.0009 ± 0.0017 | no |
| black | 0.8346 | +0.0026 ± 0.0019 | yes |
| borda | 0.8236 | +0.0136 ± 0.0029 | yes |
| star5 | 0.8207 | +0.0165 ± 0.0041 | yes |
| irv | 0.8013 | +0.0358 ± 0.0035 | yes |
| score5 | 0.7917 | +0.0455 ± 0.0040 | yes |
| top_two | 0.7781 | +0.0591 ± 0.0046 | yes |
| plurality | 0.6530 | +0.1842 ± 0.0080 | yes |

(± values are 95% CIs on the paired per-election deltas.)

**Ranked Robin lands exactly where the 2021 screenshot predicted:** at the top of a Condorcet
cluster whose members are statistically indistinguishable from each other, a solid step above
Black and Borda, ~3.6 VSE points above honest IRV, and far above plurality. The completion rule
is VSE-neutral; the Condorcet gate does all the utility work — the same conclusion the DM's
run-1/run-2 flip between "Sass" and Minimax already hinted at.

## The anatomy of ties (and what the margins ladder actually buys)

Per-election structure recorded during the run:

- **88.7%** of electorates have a Condorcet winner. Copeland ties occur in **8.6%** (1,546).
- Of those ties, **94.7% are pairwise dead heats** — finalist sets (nearly always pairs) whose
  every mutual margin is exactly 0, overwhelmingly near-clone candidates the electorate splits
  50–50. Only **82 of 18,000 elections (0.46%)** have actual cycle structure among the finalists.
- Consequently the celebrated **1st-Degree tiebreaker fired in just 78 elections** (5% of ties —
  essentially: all the real cycles). The workhorse is the **2nd Degree** (margins over *all*
  candidates), which resolved 754 of the dead heats — a rung the 2021 thread never even
  described, deferring to electowiki. The remaining 710 stayed tied to the random rung.
- On the tied elections themselves, resolving deterministically instead of randomly is worth
  nothing measurable in utility: RR − random-tiebreak Copeland = +0.0009 ± 0.0164 (n.s.) —
  near-clones have near-equal utilities, so a coin flip is almost free *in VSE terms*.

What the ladder buys instead is **decisiveness**. Unresolved-tie rate (method returned a tie and
the harness flipped a coin), all 11 methods, same 18,000 electorates:

| method | tie rate |
|---|---|
| **ranked_robin** | **3.9%** |
| irv | 4.4% |
| black | 4.8% |
| borda | 6.1% |
| score5 | 6.2% |
| copeland | 8.6% |
| top_two | 8.7% |
| ranked_pairs | 9.4% |
| smith_minimax | 9.8% |
| plurality | 9.9% |
| star5 | 9.9% |

Ranked Robin is the most decisive method in the whole field — less than half plain Copeland's tie
rate, and the most decisive Condorcet method by a wide margin (as implemented in this codebase;
smith_minimax and ranked_pairs return whole tied sets in the dead-heat elections that RR's 2nd
Degree resolves).

This is the cleanest quantitative version yet of the pattern running through these notes: the
margins ladder is **VSE-neutral but legitimacy-positive**. A 50–50 clone dead heat is precisely
the election where a coin flip costs nothing in voter satisfaction *and* looks worst in a results
UI ("the software picked"). That's multi_system_fan's 2021 tiebreaker-legitimacy worry, the
BV1550 unstable-winner incident, and the case for a deterministic rung in
[bettervoting#1063](https://github.com/Equal-Vote/bettervoting/issues/1063), all in one number:
deterministic rungs cut coin flips by 54% here while changing measured satisfaction by
statistically nothing.

## Reproducing

```bash
git clone https://github.com/johnh865/election_sim && cd election_sim
git apply ranked_robin_patch.diff
pip install scipy==1.11.4 numpy pandas matplotlib seaborn && pip install -e .
python verify_ranked_robin.py   # 20k-election fuzz vs independent reference
python run_rr_vse.py 2000 rr_vse_full.csv   # ~90 s
```

Open follow-ups: strategy runs (burying/compromising inside the finalist set — the thread's
biggest unanswered question) would need votesim's tactical harness or vse-sim; and this patch
could be offered upstream to johnh865/election_sim, which would make votesim the first simulator
to ship Ranked Robin.
