#!/usr/bin/env python3
"""
Checking electowiki's claim that cardinal methods "meet all Arrow's criteria".

The claim under test, from https://electowiki.org/wiki/Cardinal_voting_systems
(section "Impossibility theorems", fetched 2026-08-01):

    "Since Arrow's theorem only applies to ordinal voting and not cardinal voting
     systems, several cardinal systems meet all these criteria. The typical
     examples are score voting and majority judgment."

The first clause is right and the second does not follow. This script separates
the two by testing four distinct propositions, because "satisfies IIA" is being
used for two different conditions and the equivocation is the whole error.

WHAT THIS SCRIPT CAN AND CANNOT ESTABLISH
-----------------------------------------
  * A FAILURE is a finite witness and is exact. When a check reports a violating
    profile, that profile is printed and can be recomputed by hand.
  * A SATISFACTION is only "no counterexample in the window searched". Windows
    are stated per check. Rated-IIA of score and of MJ are additionally true by a
    one-line structural argument (a candidate's total/median reads only its own
    column); the search is a regression test on the implementation, not a proof.

CONVENTIONS
-----------
  * Utilities are drawn from a continuous distribution, so exact ties among a
    single voter's utilities have probability zero and the min/max normalisation
    is well defined. The hand-built witness profiles have no ties either.
  * Scores are continuous on [0, MAXSCORE]. Discretising to 0..5 would only add
    rounding artefacts of the kind already documented in star-voting.md; the
    claim under test is about the methods, not about grid resolution.
  * Majority judgment uses the lower median. All MJ profiles here use an odd
    number of voters, so the choice does not bite.
"""

import itertools
import random
from fractions import Fraction

MAXSCORE = 5.0
SEED = 20260801

# ---------------------------------------------------------------------------
# Methods
# ---------------------------------------------------------------------------


def absolute_scores(utils, cands):
    """Voter reports utility on a fixed external scale. No reference to the field."""
    return {c: utils[c] * MAXSCORE for c in cands}


def normalised_scores(utils, cands):
    """Voter rescales so their best remaining candidate gets MAXSCORE, worst gets 0."""
    vals = [utils[c] for c in cands]
    lo, hi = min(vals), max(vals)
    if hi == lo:
        return {c: 0.0 for c in cands}
    return {c: (utils[c] - lo) / (hi - lo) * MAXSCORE for c in cands}


def score_totals(profile, cands, ballot_fn):
    """profile: list of (weight, utils dict). Returns {candidate: summed score}."""
    totals = {c: 0.0 for c in cands}
    for weight, utils in profile:
        b = ballot_fn(utils, cands)
        for c in cands:
            totals[c] += weight * b[c]
    return totals


def score_ranking(profile, cands, ballot_fn):
    t = score_totals(profile, cands, ballot_fn)
    return sorted(cands, key=lambda c: (-t[c], c)), t


def mj_medians(profile, cands, ballot_fn):
    """Lower median of each candidate's grades, weights expanded."""
    out = {}
    for c in cands:
        grades = []
        for weight, utils in profile:
            grades.extend([ballot_fn(utils, cands)[c]] * weight)
        grades.sort()
        out[c] = grades[(len(grades) - 1) // 2]
    return out


def mj_ranking(profile, cands, ballot_fn):
    med = mj_medians(profile, cands, ballot_fn)
    return sorted(cands, key=lambda c: (-med[c], c)), med


def relative_order(ranking, a, b):
    return "<" if ranking.index(a) < ranking.index(b) else ">"


# ---------------------------------------------------------------------------
# Check 1 — the hand-built witness: normalised score fails IIA, and the
# candidate whose presence flips the result is a LOSER (a genuine spoiler).
# ---------------------------------------------------------------------------

WITNESS = [
    (5, {"A": 0.5, "B": 0.6, "C": 0.0}),
    (4, {"A": 1.0, "B": 0.0, "C": 0.9}),
]


def check1():
    print("=" * 78)
    print("CHECK 1 — normalised score voting fails IIA; the spoiler is a loser")
    print("=" * 78)
    print("Underlying utilities (unchanged throughout; nobody's opinion of A or B moves):")
    for w, u in WITNESS:
        print(f"    {w} voters:  A={u['A']:.1f}  B={u['B']:.1f}  C={u['C']:.1f}")

    ok = True
    for label, fn in (("normalised", normalised_scores), ("absolute", absolute_scores)):
        r3, t3 = score_ranking(WITNESS, ["A", "B", "C"], fn)
        r2, t2 = score_ranking(WITNESS, ["A", "B"], fn)
        ab3, ab2 = relative_order(r3, "A", "B"), relative_order(r2, "A", "B")
        print(f"\n  {label} scoring")
        print(f"    with C:    " + "  ".join(f"{c}={t3[c]:7.3f}" for c in "ABC")
              + f"   -> {' > '.join(r3)}")
        print(f"    without C: " + "  ".join(f"{c}={t2[c]:7.3f}" for c in "AB")
              + f"                 -> {' > '.join(r2)}")
        flipped = ab3 != ab2
        print(f"    A vs B reverses when C is removed: {flipped}")
        if label == "normalised":
            last = r3[-1]
            print(f"    C's place in the three-way race: {last == 'C'} "
                  f"(C is {'last' if last == 'C' else 'NOT last'}) "
                  f"-> C is an irrelevant alternative in the strict sense")
            ok &= flipped and last == "C"
        else:
            ok &= not flipped
    print(f"\n  RESULT: {'PASS' if ok else 'FAIL'} — normalisation breaks IIA, "
          f"absolute scoring does not.")
    return ok


# ---------------------------------------------------------------------------
# Check 2 — how often, over random profiles, and does MJ break the same way?
# ---------------------------------------------------------------------------


def random_profile(rng, n_voters, cands):
    return [(1, {c: rng.random() for c in cands}) for _ in range(n_voters)]


def check2(trials=200_000):
    print()
    print("=" * 78)
    print("CHECK 2 — frequency of IIA failure over random profiles")
    print("=" * 78)
    rng = random.Random(SEED)
    cands = ["A", "B", "C"]
    stats = {k: 0 for k in ("score_norm", "score_abs", "mj_norm", "mj_abs",
                            "score_norm_loser", "mj_norm_loser")}
    for _ in range(trials):
        prof = random_profile(rng, 9, cands)
        for tag, ranker, fn in (
            ("score_norm", score_ranking, normalised_scores),
            ("score_abs", score_ranking, absolute_scores),
            ("mj_norm", mj_ranking, normalised_scores),
            ("mj_abs", mj_ranking, absolute_scores),
        ):
            r3, _ = ranker(prof, cands, fn)
            r2, _ = ranker(prof, ["A", "B"], fn)
            if relative_order(r3, "A", "B") != relative_order(r2, "A", "B"):
                stats[tag] += 1
                if r3[-1] == "C" and tag.endswith("norm"):
                    stats[tag + "_loser"] += 1

    print(f"  {trials:,} random 9-voter, 3-candidate profiles; C removed each time.")
    print(f"  A-vs-B order reversed by removing C:\n")
    print(f"    {'method':<28}{'violations':>12}{'rate':>10}{'C was last':>13}")
    for tag, name in (("score_abs", "score, absolute"),
                      ("score_norm", "score, normalised"),
                      ("mj_abs", "majority judgment, absolute"),
                      ("mj_norm", "majority judgment, normalised")):
        loser = f"{stats.get(tag + '_loser', 0):>13,}" if tag.endswith("norm") else f"{'-':>13}"
        print(f"    {name:<28}{stats[tag]:>12,}{stats[tag]/trials:>9.2%}{loser}")
    ok = stats["score_abs"] == 0 and stats["mj_abs"] == 0 and stats["score_norm"] > 0
    print(f"\n  RESULT: {'PASS' if ok else 'FAIL'} — absolute rating never violates IIA "
          f"in this window;\n          normalisation does, for both methods.")
    return ok, stats


# ---------------------------------------------------------------------------
# Check 3 — the category error. A cardinal method is not a function on Arrow's
# domain: one preference ORDERING admits many honest ballots, with different
# winners. So it cannot "satisfy" or "fail" a condition quantified over orderings.
# ---------------------------------------------------------------------------

# Each pair holds the SAME preference orderings and differs only in how strongly
# the middle candidate is liked. One pair per method, because the two methods
# read intensity differently and no single pair separates both.

SCORE_PAIR = (
    # B is a warmly-held second choice for everyone -> B wins
    [(5, {"A": 1.00, "B": 0.90, "C": 0.00}),    # A > B > C
     (4, {"A": 0.00, "B": 0.90, "C": 1.00})],   # C > B > A
    # identical orderings, B merely tolerated -> A wins
    [(5, {"A": 1.00, "B": 0.10, "C": 0.00}),    # A > B > C
     (4, {"A": 0.00, "B": 0.10, "C": 1.00})],   # C > B > A
)

MJ_PAIR = (
    [(3, {"A": 1.00, "B": 0.80, "C": 0.00}),    # A > B > C
     (3, {"A": 0.00, "B": 1.00, "C": 0.90}),    # B > C > A
     (3, {"A": 0.00, "B": 0.85, "C": 1.00})],   # C > B > A   -> C wins
    [(3, {"A": 1.00, "B": 0.80, "C": 0.00}),    # A > B > C
     (3, {"A": 0.00, "B": 1.00, "C": 0.20}),    # B > C > A
     (3, {"A": 0.00, "B": 0.15, "C": 1.00})],   # C > B > A   -> B wins
)


def orderings(profile, cands):
    return [tuple(sorted(cands, key=lambda c: -u[c])) for _, u in profile]


def check3():
    print()
    print("=" * 78)
    print("CHECK 3 — same ordinal profile, two honest cardinal ballots, two winners")
    print("=" * 78)
    cands = ["A", "B", "C"]
    ok = True
    for name, ranker, (p1, p2), stat in (
        ("score", score_ranking, SCORE_PAIR, "total"),
        ("majority judgment", mj_ranking, MJ_PAIR, "median"),
    ):
        o1, o2 = orderings(p1, cands), orderings(p2, cands)
        same_orderings = o1 == o2
        r1, t1 = ranker(p1, cands, absolute_scores)
        r2, t2 = ranker(p2, cands, absolute_scores)
        print(f"\n  {name} (absolute scoring, so IIA is not in play):")
        print(f"    orderings, profile 1: {[''.join(o) for o in o1]}")
        print(f"    orderings, profile 2: {[''.join(o) for o in o2]}   identical: {same_orderings}")
        print(f"    profile 1 {stat}: " + "  ".join(f"{c}={t1[c]:6.2f}" for c in cands)
              + f"   -> winner {r1[0]}")
        print(f"    profile 2 {stat}: " + "  ".join(f"{c}={t2[c]:6.2f}" for c in cands)
              + f"   -> winner {r2[0]}")
        differ = r1[0] != r2[0]
        print(f"    same orderings, different winner: {same_orderings and differ}")
        ok &= same_orderings and differ
    print(f"\n  RESULT: {'PASS' if ok else 'FAIL'} — the method is not a function of the")
    print("          preference profile, which is the object Arrow's conditions quantify over.")
    return ok


# ---------------------------------------------------------------------------
# Check 4 — Sen's Theorem 8*2 made concrete. Cardinal NON-COMPARABILITY says the
# social ranking must be invariant under an independent positive affine
# transformation of each voter's utility. Score voting is not. That is the
# assumption doing the work — not a pass on Arrow's conditions.
# ---------------------------------------------------------------------------


def check4(trials=100_000):
    print()
    print("=" * 78)
    print("CHECK 4 — score voting is not invariant under individual affine rescaling")
    print("=" * 78)
    print("  Sen's cardinal-non-comparability axiom: replacing voter i's utility u_i by")
    print("  a_i*u_i + b_i (a_i > 0), independently per voter, must not change the social")
    print("  ranking. Under that axiom the Arrow impossibility survives (Sen 1970, Thm 8*2).")
    rng = random.Random(SEED + 1)
    cands = ["A", "B", "C"]
    flips = 0
    witness = None
    for _ in range(trials):
        prof = random_profile(rng, 5, cands)
        r0, _ = score_ranking(prof, cands, absolute_scores)
        resc = []
        coeffs = []
        for w, u in prof:
            a, b = rng.uniform(0.1, 3.0), rng.uniform(-1.0, 1.0)
            coeffs.append((a, b))
            resc.append((w, {c: a * u[c] + b for c in cands}))
        r1, _ = score_ranking(resc, cands, absolute_scores)
        if r0[0] != r1[0]:
            flips += 1
            if witness is None:
                witness = (prof, coeffs, r0, r1)
    print(f"\n  {trials:,} random 5-voter profiles, each voter's utilities independently")
    print(f"  rescaled by a positive affine map:")
    print(f"    winner changed: {flips:,} / {trials:,}  ({flips/trials:.1%})")
    if witness:
        prof, coeffs, r0, r1 = witness
        print(f"\n  first witness:")
        for (w, u), (a, b) in zip(prof, coeffs):
            print(f"    u = (" + ", ".join(f"{u[c]:.4f}" for c in cands)
                  + f")   ->  a={a:.4f} b={b:+.4f}")
        print(f"    winner before rescaling: {r0[0]}    after: {r1[0]}")
    ok = flips > 0
    print(f"\n  RESULT: {'PASS' if ok else 'FAIL'} — score voting reads the ballots as")
    print("          interpersonally comparable. Strip that assumption and it is back")
    print("          inside the impossibility, exactly as Sen's theorem says.")
    return ok


# ---------------------------------------------------------------------------
# Check 5 — KP transform: a scored ballot is equivalent to fractional approval
# ballots, so score voting = approval voting on the transformed profile.
# (Page section "Kotze-Pereira transformation".)
# ---------------------------------------------------------------------------


def kp_transform(utils, cands, levels):
    """Split a scored ballot into `levels` unit approval ballots.
    A candidate scored k/levels is approved on exactly k of them."""
    out = []
    for L in range(1, levels + 1):
        threshold = Fraction(L, levels)
        out.append({c for c in cands if Fraction(utils[c]).limit_denominator(levels) >= threshold})
    return out


def check5():
    print()
    print("=" * 78)
    print("CHECK 5 — KP transform: score over m levels == approval over m sub-electorates")
    print("=" * 78)
    rng = random.Random(SEED + 2)
    cands = ["A", "B", "C", "D"]
    levels = 5
    mismatches = 0
    trials = 20_000
    for _ in range(trials):
        prof = [(1, {c: Fraction(rng.randrange(levels + 1), levels) for c in cands})
                for _ in range(7)]
        direct = {c: sum(w * u[c] for w, u in prof) for c in cands}
        via_kp = {c: 0 for c in cands}
        for w, u in prof:
            for ballot in kp_transform(u, cands, levels):
                for c in ballot:
                    via_kp[c] += w
        if any(direct[c] * levels != via_kp[c] for c in cands):
            mismatches += 1
    ok = mismatches == 0
    print(f"  {trials:,} random 7-voter profiles, 4 candidates, 0..{levels} scale.")
    print(f"  score total x {levels} != approval total over the {levels} KP sub-ballots: "
          f"{mismatches:,}")
    print(f"\n  RESULT: {'PASS' if ok else 'FAIL'} — the transform is exact, so any claim")
    print("          proved for approval transfers to score at every scale. This is what")
    print("          'scale invariance' buys and why the two rows of the compliance table")
    print("          cannot come apart on anything the transform preserves.")
    return ok


# ---------------------------------------------------------------------------

def main():
    print(__doc__)
    results = []
    results.append(("normalised score fails IIA, spoiler is a loser", check1()))
    ok2, _ = check2()
    results.append(("IIA failure rates over random profiles", ok2))
    results.append(("one ordering, many honest ballots, many winners", check3()))
    results.append(("not invariant under individual affine rescaling", check4()))
    results.append(("KP transform is exact", check5()))

    print()
    print("=" * 78)
    print("SUMMARY")
    print("=" * 78)
    for name, ok in results:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    print()
    print("  Verdict on the electowiki sentence:")
    print("    'Arrow's theorem only applies to ordinal voting'      -> correct")
    print("    'therefore several cardinal systems meet all these")
    print("     criteria'                                            -> does not follow")
    print()
    print("  Checks 3 and 4 give the reason. Cardinal methods are not rules on Arrow's")
    print("  domain at all, and the extra thing they assume -- that one voter's 5 means")
    print("  what another's 5 means -- is precisely the assumption Arrow's framework")
    print("  withholds. Sen 1970 Thm 8*2: cardinal measurability WITHOUT interpersonal")
    print("  comparability leaves the impossibility exactly where it was.")
    return all(ok for _, ok in results)


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
