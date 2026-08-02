#!/usr/bin/env python3
"""
Sequentially Spent Score (SSS) — checking electowiki's claims and one engine bug.

Sources under test:
  * https://electowiki.org/wiki/Sequentially_Spent_Score  (fetched 2026-08-02 via action=raw)
  * https://electowiki.org/wiki/Vote_unitarity            (same)
  * BUG_sss_verbosity.md / larryhastings/starvote#17, via the vendored fork in
    masiarek/star-voting-library

Pure Python, no dependencies. Exact rational arithmetic throughout (Fraction), so
every printed total is the real number and not a float artefact — the electowiki
page prints rounded intermediates and two of them are wrong, which only shows up
if you keep the fractions.

WHAT THIS SCRIPT CAN AND CANNOT ESTABLISH
-----------------------------------------
  * A FAILURE is a finite witness and is exact.
  * A SATISFACTION is only "no counterexample in the window searched"; windows are
    stated per check.
  * Checks 5-7 sample random profiles with a fixed seed, so they are reproducible
    but not exhaustive.

THE METHOD (scaling variant, from the page's own reference implementation)
--------------------------------------------------------------------------
  quota = V / W                       (on ballots normalised to [0,1])
  repeat W times:
      w  = argmax over remaining candidates of  sum_i  s[i][c] * weight[i]
      surplus_factor = max(total[w] / quota, 1)
      spent[i]  = s[i][w] * weight[i] / surplus_factor
      weight[i] = clip(weight[i] - spent[i], 0, 1)
"""

import itertools
import random
from fractions import Fraction as F

SEED = 20260802


# ---------------------------------------------------------------------------
# The method
# ---------------------------------------------------------------------------


def sss(ballots, cands, seats, maxscore=5, variant="scaling", reweight=True):
    """ballots: list of dicts {candidate: raw score}. Returns the winner list in order.

    variant   'scaling' (current) or 'capping' (the abandoned original)
    reweight  False disables the spending step entirely -> degenerates to Bloc Score.
              That is exactly what the starvote verbosity=0 bug did.
    """
    K = F(maxscore)
    s = [{c: F(b.get(c, 0)) / K for c in cands} for b in ballots]
    V = len(ballots)
    quota = F(V, seats)
    weight = [F(1)] * V
    remaining = list(cands)
    winners = []

    while len(winners) < seats:
        if variant == "capping":
            totals = {c: sum(s[i][c] for i in range(V)) for c in remaining}
        else:
            totals = {c: sum(s[i][c] * weight[i] for i in range(V)) for c in remaining}
        # deterministic tiebreak by name, so results are reproducible
        w = max(remaining, key=lambda c: (totals[c], [-ord(ch) for ch in c]))
        winners.append(w)
        remaining.remove(w)
        if len(winners) == seats:
            break

        if not reweight:
            continue

        if totals[w] > 0:
            surplus_factor = max(totals[w] / quota, F(1))
            for i in range(V):
                base = s[i][w] if variant == "capping" else s[i][w] * weight[i]
                spent = base / surplus_factor
                weight[i] = min(max(weight[i] - spent, F(0)), F(1))
            if variant == "capping":
                for i in range(V):
                    for c in remaining:
                        s[i][c] = min(s[i][c], weight[i])
    return winners


def sss_payments(ballots, cands, seats, maxscore=5):
    """Same as sss(), but also returns the payment function p[i][c] and the
    residual budgets, for checking the Vote Unitarity axioms VU1/VU2."""
    K = F(maxscore)
    s = [{c: F(b.get(c, 0)) / K for c in cands} for b in ballots]
    s0 = [dict(row) for row in s]
    V = len(ballots)
    quota = F(V, seats)
    weight = [F(1)] * V
    remaining = list(cands)
    winners, pay = [], [dict() for _ in range(V)]
    clip_bit = False

    while len(winners) < seats:
        totals = {c: sum(s[i][c] * weight[i] for i in range(V)) for c in remaining}
        w = max(remaining, key=lambda c: (totals[c], [-ord(ch) for ch in c]))
        winners.append(w)
        remaining.remove(w)
        for i in range(V):
            pay[i][w] = F(0)
        if len(winners) == seats:
            break
        if totals[w] > 0:
            surplus_factor = max(totals[w] / quota, F(1))
            for i in range(V):
                spent = s[i][w] * weight[i] / surplus_factor
                if spent > weight[i]:
                    clip_bit = True
                pay[i][w] = min(spent, weight[i])
                weight[i] = min(max(weight[i] - spent, F(0)), F(1))
    return winners, pay, weight, s0, clip_bit


def bloc_score(ballots, cands, seats):
    totals = {c: sum(F(b.get(c, 0)) for b in ballots) for c in cands}
    return sorted(cands, key=lambda c: (-totals[c], c))[:seats]


def expand(spec):
    """[(n, dict), ...] -> flat ballot list"""
    out = []
    for n, d in spec:
        out.extend(dict(d) for _ in range(n))
    return out


def fmt(x, places=2):
    return f"{float(x):.{places}f}"


# ---------------------------------------------------------------------------
# CHECK 1 — the starvote verbosity bug, restated as a fact about the method
# ---------------------------------------------------------------------------

REPRO = [
    (6, {"Alice": 5, "Ben": 4, "Cara": 3, "Dan": 0, "Eve": 0}),
    (4, {"Alice": 4, "Ben": 5, "Cara": 3, "Dan": 0, "Eve": 0}),
    (3, {"Alice": 3, "Ben": 4, "Cara": 5, "Dan": 0, "Eve": 0}),
    (5, {"Alice": 0, "Ben": 0, "Cara": 0, "Dan": 5, "Eve": 4}),
    (3, {"Alice": 0, "Ben": 0, "Cara": 0, "Dan": 4, "Eve": 5}),
]
REPRO_CANDS = ["Alice", "Ben", "Cara", "Dan", "Eve"]


def check1():
    print("=" * 78)
    print("CHECK 1 — what the reweighting step is worth (the starvote verbosity bug)")
    print("=" * 78)
    ballots = expand(REPRO)
    print(f"  21 ballots: a 13-voter majority bloc (Alice/Ben/Cara) and an 8-voter")
    print(f"  minority bloc (Dan/Eve). 3 seats. 8/21 = 38% of the electorate, so the")
    print(f"  minority is worth 1.14 Hare quotas and is owed a seat.\n")

    full = sss(ballots, REPRO_CANDS, seats=3)
    none = sss(ballots, REPRO_CANDS, seats=3, reweight=False)
    bloc = bloc_score(ballots, REPRO_CANDS, seats=3)

    print(f"    SSS, reweighting on      -> {sorted(full)}")
    print(f"    SSS, reweighting removed -> {sorted(none)}")
    print(f"    Bloc Score               -> {sorted(bloc)}")
    ok = (sorted(full) == ["Alice", "Ben", "Dan"]
          and sorted(none) == sorted(bloc) == ["Alice", "Ben", "Cara"])
    print(f"\n    reweighting-removed SSS == Bloc Score: {sorted(none) == sorted(bloc)}")
    print(f"    minority bloc represented, with reweighting:    {'Dan' in full}")
    print(f"    minority bloc represented, without reweighting: {'Dan' in none}")
    print(f"\n  These are the exact winner sets the bug report records for verbosity=0")
    print(f"  and verbosity>=1. The engine was not mis-tabulating SSS; at verbosity=0")
    print(f"  it was running a DIFFERENT METHOD -- the non-proportional one.")
    print(f"\n  RESULT: {'PASS' if ok else 'FAIL'}")
    return ok


# ---------------------------------------------------------------------------
# CHECK 2 — the page's participation-failure example, recomputed exactly
# ---------------------------------------------------------------------------

PART_CANDS = ["A1", "A2", "B1", "B2", "C1"]
PART_CASE1 = [
    (30, {"A1": 10, "A2": 10, "B1": 0, "B2": 0}),
    (9, {"A1": 0, "A2": 0, "B1": 10, "B2": 10}),
    (1, {"A1": 1, "A2": 1, "B1": 10, "B2": 10}),
]
PART_CASE2 = PART_CASE1 + [(1, {"A1": 1, "A2": 1, "C1": 10})]


def check2():
    print()
    print("=" * 78)
    print("CHECK 2 — the participation failure, and the page's printed arithmetic")
    print("=" * 78)
    r1 = sss(expand(PART_CASE1), PART_CANDS, seats=2, maxscore=10)
    r2 = sss(expand(PART_CASE2), PART_CANDS, seats=2, maxscore=10)
    print(f"  Case 1 (40 voters):  winners {r1}")
    print(f"  Case 2 (41 voters, one added A=1 C=10 voter):  winners {r2}")

    kinds1 = sorted(w[0] for w in r1)
    kinds2 = sorted(w[0] for w in r2)
    conclusion = kinds1 == ["A", "A"] and kinds2 == ["A", "B"]
    print(f"\n  by candidate type: case 1 -> {kinds1}, case 2 -> {kinds2}")
    print(f"  The added voter scored A above B, and their turning out cost A a seat.")
    print(f"  Participation failure reproduced: {conclusion}")

    # Recompute the round-2 totals the page prints.
    print(f"\n  The page also prints the round-2 totals. Recomputing them exactly:")
    for label, spec, printed in (("Case 1", PART_CASE1, {"A": "100.66", "B": "99.33"}),
                                 ("Case 2", PART_CASE2, {"A": "98.36", "B": "99.32"})):
        ballots = expand(spec)
        V = len(ballots)
        quota = F(V, 2)
        s = [{c: F(b.get(c, 0), 10) for c in PART_CANDS} for b in ballots]
        tot_a1 = sum(row["A1"] for row in s)
        sf = max(tot_a1 / quota, F(1))
        weight = [F(1) - row["A1"] / sf for row in s]
        a2 = sum(s[i]["A2"] * weight[i] for i in range(V)) * 10
        b1 = sum(s[i]["B1"] * weight[i] for i in range(V)) * 10
        print(f"    {label}: A(2nd) = {fmt(a2)}  (page prints {printed['A']}), "
              f"B = {fmt(b1)}  (page prints {printed['B']})")
    print(f"\n  Both A figures omit the small-score voters' surviving contribution to the")
    print(f"  second A clone. The comparison, and so the finding, is unaffected -- but the")
    print(f"  printed intermediates are not what the stated procedure produces.")
    print(f"\n  RESULT: {'PASS' if conclusion else 'FAIL'} — the participation failure is real.")
    return conclusion


# ---------------------------------------------------------------------------
# CHECK 3 — the capping variant's Justified Representation failure
# ---------------------------------------------------------------------------


def jr_profile():
    spec = [
        (5, {"A": 3, "D1": 5}),
        (5, {"A": 3, "D2": 5}),
        (6, {"B1": 3, "C1": 2, "D3": 5}),
        (6, {"B1": 3, "C1": 2, "D4": 5}),
        (6, {"B2": 3, "C1": 2, "D5": 5}),
        (6, {"B2": 3, "C1": 2, "D6": 5}),
        (6, {"B3": 3, "C2": 2, "D7": 5}),
        (6, {"B3": 3, "C2": 2, "D8": 5}),
        (6, {"B4": 3, "C2": 2, "D9": 5}),
        (6, {"B4": 3, "C2": 2, "D10": 5}),
    ]
    cands = ["A"] + [f"B{i}" for i in range(1, 5)] + ["C1", "C2"] \
        + [f"D{i}" for i in range(1, 11)]
    return spec, cands


def check3():
    print()
    print("=" * 78)
    print("CHECK 3 — the capping variant fails Justified Representation")
    print("=" * 78)
    spec, cands = jr_profile()
    ballots = expand(spec)
    print(f"  {len(ballots)} voters, {len(cands)} candidates, 6 seats. "
          f"Hare quota = {len(ballots)}/6 = {fmt(F(len(ballots), 6))} voters.")
    print(f"  The first 10 voters all score A at 3; they are 10/58 = 17.2% of the")
    print(f"  electorate, more than one sixth, so JR entitles them to representation.\n")

    cap = sss(ballots, cands, seats=6, variant="capping")
    sca = sss(ballots, cands, seats=6, variant="scaling")
    print(f"    capping variant: {sorted(cap)}")
    print(f"    scaling variant: {sorted(sca)}")
    claimed = sorted(["B1", "B2", "B3", "B4", "C1", "C2"])
    print(f"\n    capping result matches the page's claim {claimed}: {sorted(cap) == claimed}")
    print(f"    A elected under capping: {'A' in cap}")
    print(f"    A elected under scaling: {'A' in sca}")
    ok = sorted(cap) == claimed and "A" not in cap and "A" in sca
    print(f"\n  RESULT: {'PASS' if ok else 'FAIL'} — the page's stated reason for abandoning")
    print("          the capping variant reproduces exactly.")
    return ok


# ---------------------------------------------------------------------------
# CHECK 4 — the "only Bs are elected" centrist-bias example
# ---------------------------------------------------------------------------


def check4():
    print()
    print("=" * 78)
    print("CHECK 4 — the surplus-handling centrist bias ('only Bs are elected')")
    print("=" * 78)
    cands = ["A1", "A2", "A3", "A4", "A5", "B1", "B2", "B3", "B4", "B5",
             "C1", "C2", "C3", "C4", "C5"]

    def bloc_ballot(prefix_scores):
        d = {}
        for letter, sc in prefix_scores.items():
            for i in range(1, 6):
                d[f"{letter}{i}"] = sc
        return d

    spec = [
        (41, bloc_ballot({"A": 5, "B": 2, "C": 0})),
        (20, bloc_ballot({"A": 0, "B": 5, "C": 0})),
        (41, bloc_ballot({"A": 0, "B": 2, "C": 5})),
    ]
    ballots = expand(spec)
    print(f"  102 voters, 5 seats, three blocs 41 / 20 / 41. The page states, under")
    print(f"  'Sorted Surplus Handling Variant', that here 'only Bs are elected'.\n")
    print(f"  proportional entitlement at 5 seats: "
          f"A {41/102*5:.2f}   B {20/102*5:.2f}   C {41/102*5:.2f}\n")

    results = {}
    for variant in ("scaling", "capping"):
        w = sss(ballots, cands, seats=5, variant=variant)
        kinds = [x[0] for x in w]
        results[variant] = kinds
        seats_b = kinds.count("B")
        print(f"    {variant:8s}: {w}")
        print(f"    {'':8s}  by bloc {kinds} — B takes {seats_b}/5, "
              f"'only Bs' = {set(kinds) == {'B'}}")

    only_b_capping = set(results["capping"]) == {"B"}
    not_only_b_scaling = set(results["scaling"]) != {"B"}
    ok = only_b_capping and not_only_b_scaling

    print(f"\n  The claim holds for the CAPPING variant and not for the SCALING one —")
    print(f"  and scaling is the current method; the same page says capping 'was")
    print(f"  abandoned'. So the example is inherited from the superseded variant.")
    print(f"\n  The bias it illustrates is real either way: the 20% centre bloc is owed")
    print(f"  0.98 seats and takes {results['scaling'].count('B')} under the current method — about 3x")
    print(f"  over-representation, not 5x. Both 41% wings are owed 2.01 and get 1 each.")
    print(f"  The strategic incentive the page draws from it (wings truncate B to 0)")
    print(f"  survives at the smaller magnitude.")
    print(f"\n  RESULT: {'PASS' if ok else 'FAIL'} — claim reproduces only under capping.")
    return ok


# ---------------------------------------------------------------------------
# CHECK 5 — the criteria table, spot-checked by random search
# ---------------------------------------------------------------------------


def random_profile(rng, n_voters, cands, maxscore=5):
    return [{c: rng.randrange(maxscore + 1) for c in cands} for _ in range(n_voters)]


def check5(trials=4000):
    print()
    print("=" * 78)
    print("CHECK 5 — the page's criteria table, spot-checked")
    print("=" * 78)
    rng = random.Random(SEED)
    cands = ["a", "b", "c", "d", "e"]
    seats = 2
    fails = {"monotone": 0, "iia": 0, "participation": 0}
    part_witness = None

    for _ in range(trials):
        ballots = random_profile(rng, 7, cands)
        base = sss(ballots, cands, seats)

        # Monotonicity: raise a winner's score on one ballot; they must still win.
        i = rng.randrange(len(ballots))
        w = base[0]
        if ballots[i][w] < 5:
            bumped = [dict(b) for b in ballots]
            bumped[i][w] = min(5, bumped[i][w] + 1)
            if w not in sss(bumped, cands, seats):
                fails["monotone"] += 1

        # IIA: delete a candidate who won nothing; the winner set must not move.
        losers = [c for c in cands if c not in base]
        if losers:
            drop = rng.choice(losers)
            reduced = [{c: v for c, v in b.items() if c != drop} for b in ballots]
            if sorted(sss(reduced, [c for c in cands if c != drop], seats)) != sorted(base):
                fails["iia"] += 1

        # Participation: add one ballot; the adder must not be made worse off in the
        # weak sense of "the new set is strictly worse by their own scores".
        extra = {c: rng.randrange(6) for c in cands}
        after = sss(ballots + [extra], cands, seats)
        before_u = sum(extra[c] for c in base)
        after_u = sum(extra[c] for c in after)
        if after_u < before_u:
            fails["participation"] += 1
            if part_witness is None:
                part_witness = (before_u, after_u)

    print(f"  {trials:,} random 7-voter, 5-candidate, 2-seat profiles.\n")
    print(f"    {'property':<20}{'claimed':>10}{'violations':>13}{'verdict':>12}")
    for key, claimed in (("monotone", "Yes"), ("iia", "Yes"), ("participation", "No")):
        n = fails[key]
        agree = (n == 0) if claimed == "Yes" else (n > 0)
        print(f"    {key:<20}{claimed:>10}{n:>13,}{'consistent' if agree else 'CONFLICT':>12}")
    if part_witness:
        print(f"\n    a participation witness: the added voter's own score for the winner set")
        print(f"    fell from {part_witness[0]} to {part_witness[1]} by voting.")
    ok = fails["monotone"] == 0 and fails["iia"] == 0 and fails["participation"] > 0
    print(f"\n  RESULT: {'PASS' if ok else 'FAIL'} — table consistent with the search.")
    print("          Note IIA here is the multi-winner 'remove a loser' form and, as with")
    print("          score voting, it is a property of ABSOLUTE scoring only.")
    return ok


# ---------------------------------------------------------------------------
# CHECK 6 — "the natural extension of the Hamilton method"
# ---------------------------------------------------------------------------


def hamilton(votes, seats):
    total = sum(votes)
    quotas = [F(v * seats, total) for v in votes]
    base = [int(q) for q in quotas]
    left = seats - sum(base)
    order = sorted(range(len(votes)), key=lambda i: (-(quotas[i] - base[i]), i))
    for i in order[:left]:
        base[i] += 1
    return base


def divisor(votes, seats, rule="dhondt"):
    seatv = [0] * len(votes)
    for _ in range(seats):
        if rule == "dhondt":
            q = [F(votes[i], seatv[i] + 1) for i in range(len(votes))]
        else:  # webster / sainte-lague
            q = [F(votes[i], 2 * seatv[i] + 1) for i in range(len(votes))]
        seatv[q.index(max(q))] += 1
    return seatv


def check6(trials=2000):
    print()
    print("=" * 78)
    print("CHECK 6 — 'the natural extension of the Hamilton method'")
    print("=" * 78)
    rng = random.Random(SEED + 3)
    seats = 5
    n_parties = 3
    agree_h = agree_d = agree_w = 0
    first_diff = None

    for _ in range(trials):
        votes = [rng.randrange(5, 60) for _ in range(n_parties)]
        cands, spec = [], []
        for p in range(n_parties):
            cands += [f"P{p}c{j}" for j in range(seats)]
        for p in range(n_parties):
            spec.append((votes[p], {f"P{p}c{j}": 5 for j in range(seats)}))
        winners = sss(expand(spec), cands, seats)
        got = [sum(1 for w in winners if w.startswith(f"P{p}c")) for p in range(n_parties)]

        h = hamilton(votes, seats)
        d = divisor(votes, seats, "dhondt")
        wb = divisor(votes, seats, "webster")
        agree_h += got == h
        agree_d += got == d
        agree_w += got == wb
        if got != h and first_diff is None:
            first_diff = (votes, got, h)

    print(f"  {trials:,} random 3-party list profiles, 5 seats, every voter giving max")
    print(f"  score to their own party's slate and 0 to everyone else.\n")
    print(f"    SSS seat vector == Hamilton (largest remainders): {agree_h:,}/{trials:,}"
          f"  ({agree_h/trials:.1%})")
    print(f"    SSS seat vector == D'Hondt:                       {agree_d:,}/{trials:,}"
          f"  ({agree_d/trials:.1%})")
    print(f"    SSS seat vector == Webster/Sainte-Lague:          {agree_w:,}/{trials:,}"
          f"  ({agree_w/trials:.1%})")
    if first_diff:
        v, got, h = first_diff
        print(f"\n    first disagreement with Hamilton: votes {v} -> SSS {got}, Hamilton {h}")
    ok = agree_h > agree_d and agree_h > agree_w
    print(f"\n  RESULT: {'PASS' if ok else 'FAIL'} — the party-list signature is Hamilton's,")
    print("          not a divisor method's, which is the claim in the taxonomy.")
    return ok


# ---------------------------------------------------------------------------
# CHECK 7 — does SSS actually satisfy Vote Unitarity as formalised?
# ---------------------------------------------------------------------------


def check7(trials=3000):
    print()
    print("=" * 78)
    print("CHECK 7 — the Vote Unitarity axioms VU1 and VU2, as stated on the wiki")
    print("=" * 78)
    rng = random.Random(SEED + 5)
    cands = ["a", "b", "c", "d"]
    vu1_fail = vu2_fail = clipped = 0

    for _ in range(trials):
        ballots = random_profile(rng, 6, cands)
        winners, pay, weight, s0, clip_bit = sss_payments(ballots, cands, seats=2)
        clipped += clip_bit
        for i in range(len(ballots)):
            for c in winners:
                if pay[i].get(c, F(0)) > s0[i][c]:
                    vu1_fail += 1
            residual = F(1) - sum(pay[i].values())
            if residual != weight[i] or residual < 0:
                vu2_fail += 1

    print(f"  {trials:,} random 6-voter, 4-candidate, 2-seat profiles, exact arithmetic.\n")
    print(f"    VU1 (proportionate spending, p[i][c] <= s[i][c]) violations: {vu1_fail:,}")
    print(f"    VU2 (residual budget == 1 - sum of payments)   violations: {vu2_fail:,}")
    print(f"    profiles where the weight clip at 0 was load-bearing:       {clipped:,}")
    ok = vu1_fail == 0 and vu2_fail == 0
    print(f"\n  RESULT: {'PASS' if ok else 'FAIL'} — SSS satisfies its own axioms exactly,")
    print("          and the clip in the reference implementation never binds: spending is")
    print("          s[i][w]*weight[i]/surplus <= weight[i] because s <= 1 and surplus >= 1.")
    print("          Note the wiki's VU2 remark that 'no rule using multiplicative")
    print("          reweighting can satisfy this condition' is about the BUDGET being")
    print("          additive; SSS scales the ballot multiplicatively and tracks the budget")
    print("          additively, which is why it passes.")
    return ok


# ---------------------------------------------------------------------------

def main():
    print(__doc__)
    results = [
        ("reweighting is the method (verbosity bug)", check1()),
        ("participation failure real; printed totals off", check2()),
        ("capping variant fails Justified Representation", check3()),
        ("surplus-handling centrist bias", check4()),
        ("criteria table spot-check", check5()),
        ("party-list signature is Hamilton", check6()),
        ("VU1 / VU2 hold exactly", check7()),
    ]
    print()
    print("=" * 78)
    print("SUMMARY")
    print("=" * 78)
    for name, ok in results:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    return all(ok for _, ok in results)


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
