#!/usr/bin/env python3
"""Verify every numeric claim in ../../score-voting.md.

Score voting: each voter scores every candidate on a fixed scale; highest total
(or average -- see section 3, they are not the same rule) wins.

Run:  python3 verify.py
No dependencies. Every assertion below is checked, not printed on trust.
"""

import random

# ---------------------------------------------------------------- machinery


def totals(prof, cands):
    return {c: sum(n * b[c] for n, b in prof if c in b) for c in cands}


def averages(prof, cands):
    """Average over voters who actually rated the candidate (blank = abstain)."""
    out = {}
    for c in cands:
        rated = sum(n for n, b in prof if c in b)
        out[c] = (sum(n * b[c] for n, b in prof if c in b) / rated) if rated else 0.0
    return out


def prefer(prof, x, y):
    """(voters scoring x above y, voters scoring y above x). Blank counts as 0."""
    return (sum(n for n, b in prof if b.get(x, 0) > b.get(y, 0)),
            sum(n for n, b in prof if b.get(y, 0) > b.get(x, 0)))


def condorcet(prof, cands):
    for c in cands:
        if all(prefer(prof, c, d)[0] > prefer(prof, c, d)[1] for d in cands if d != c):
            return c
    return None


def star(prof, cands):
    """Score Then Automatic Runoff, Equal Vote tie rules. -> (winner, clean)."""
    sc = totals(prof, cands)
    clean = True
    top = max(sc.values())
    lead = [c for c in cands if sc[c] == top]
    if len(lead) > 1:
        if len(lead) > 2:
            clean = False
        f1, f2 = sorted(lead)[:2]
    else:
        f1 = lead[0]
        rest = [c for c in cands if c != f1]
        second = max(sc[c] for c in rest)
        tied = [c for c in rest if sc[c] == second]
        if len(tied) == 1:
            f2 = tied[0]
        else:
            wins = {c: sum(1 for d in tied if d != c
                           and prefer(prof, c, d)[0] > prefer(prof, c, d)[1]) for c in tied}
            best = max(wins.values())
            short = [c for c in tied if wins[c] == best]
            if len(short) > 1:
                clean = False
            f2 = short[0]
    a, d = prefer(prof, f1, f2)
    if a > d:
        w = f1
    elif d > a:
        w = f2
    else:
        if sc[f1] == sc[f2]:
            clean = False
        w = f1 if sc[f1] > sc[f2] else f2
    return w, clean


def ranked_robin(prof, cands):
    """Copeland matchup wins (ties 1/2), then greatest sum of pairwise margins."""
    cop, marg = {}, {}
    for c in cands:
        w = t = m = 0
        for d in cands:
            if d == c:
                continue
            a, b = prefer(prof, c, d)
            m += a - b
            if a > b:
                w += 1
            elif a == b:
                t += 1
        cop[c], marg[c] = w + t / 2, m
    best = max(cop.values())
    top = [c for c in cands if cop[c] == best]
    if len(top) == 1:
        return top[0], True
    bm = max(marg[c] for c in top)
    short = [c for c in top if marg[c] == bm]
    return short[0], len(short) == 1


# ---------------------------------------------------------------- Tennessee

TENN = ["Memphis", "Nashville", "Chattanooga", "Knoxville"]

DIST = {
    ("Memphis", "Knoxville"): 345.1, ("Memphis", "Nashville"): 194.2,
    ("Memphis", "Chattanooga"): 268.1, ("Knoxville", "Nashville"): 159.5,
    ("Knoxville", "Chattanooga"): 96.2, ("Nashville", "Chattanooga"): 115.2,
}
SHARE = {"Memphis": 42, "Nashville": 26, "Chattanooga": 15, "Knoxville": 17}

# The article's printed 0-10 table, and the STAR article's printed 0-5 table.
SCORE10 = {
    "Memphis":     {"Memphis": 10, "Nashville": 4, "Chattanooga": 2, "Knoxville": 0},
    "Nashville":   {"Memphis": 0, "Nashville": 10, "Chattanooga": 4, "Knoxville": 2},
    "Chattanooga": {"Memphis": 0, "Nashville": 6, "Chattanooga": 10, "Knoxville": 6},
    "Knoxville":   {"Memphis": 0, "Nashville": 5, "Chattanooga": 7, "Knoxville": 10},
}
STAR5 = {
    "Memphis":     {"Memphis": 5, "Nashville": 2, "Chattanooga": 1, "Knoxville": 0},
    "Nashville":   {"Memphis": 0, "Nashville": 5, "Chattanooga": 2, "Knoxville": 1},
    "Chattanooga": {"Memphis": 0, "Nashville": 3, "Chattanooga": 5, "Knoxville": 3},
    "Knoxville":   {"Memphis": 0, "Nashville": 2, "Chattanooga": 4, "Knoxville": 5},
}


def dist(a, b):
    return 0.0 if a == b else (DIST.get((a, b)) or DIST[(b, a)])


def derived(home, top):
    """The stated rule: `top` for home, 0 for the farthest, linear in between."""
    far = max(dist(home, c) for c in TENN)
    return {c: int(top * (1 - dist(home, c) / far) + 0.5) for c in TENN}


def prof_from(table):
    return [(SHARE[h], table[h]) for h in TENN]


# ---------------------------------------------------------------- the claims


def main():
    ok = []

    # ---- 1. The article's own example, checked cell by cell ---------------
    for home in TENN:
        assert derived(home, 10) == SCORE10[home], home
    ok.append("Tennessee 0-10: all 16 printed cells follow the stated distance rule")

    T = prof_from(SCORE10)
    tot = totals(T, TENN)
    assert tot == {"Memphis": 420, "Nashville": 603, "Chattanooga": 457, "Knoxville": 312}
    assert max(tot, key=tot.get) == "Nashville"
    assert condorcet(T, TENN) == "Nashville"
    ok.append("totals 420/603/457/312 -> Nashville, who is also the Condorcet winner")

    # ---- 2. Where the STAR article's 0-5 table came from ------------------
    # It is this table halved, with round-half-to-EVEN (Python's round()).
    for home in TENN:
        for c in TENN:
            assert round(SCORE10[home][c] / 2) == STAR5[home][c], (home, c)
    ok.append("the STAR article's 0-5 table is exactly this table halved, round-half-to-even")

    # Deriving 0-5 straight from the distances instead disagrees in one cell:
    direct = {h: derived(h, 5) for h in TENN}
    gaps = [(h, c) for h in TENN for c in TENN if direct[h][c] != STAR5[h][c]]
    assert gaps == [("Knoxville", "Nashville")]
    assert STAR5["Knoxville"]["Nashville"] == 2 and direct["Knoxville"]["Nashville"] == 3
    # 5.378 -> 5 -> 2.5 -> 2 (half to even), but 2.689 -> 3 going direct.
    assert abs(10 * (1 - 159.5 / 345.1) - 5.378) < 1e-3
    assert abs(5 * (1 - 159.5 / 345.1) - 2.689) < 1e-3
    ok.append("so the one 0-5 cell that looked wrong is a DOUBLE-ROUNDING artifact:")
    ok.append("  5.378 -> 5 -> 2.5 -> 2, where deriving 0-5 directly gives 2.689 -> 3")

    # ---- 3. Sum vs average vs quorum: one ballot set, two winners ---------
    # 'B' is simply absent from the first bloc's ballot -- a blank, not a zero.
    BLANK = [(60, {"A": 10, "C": 0}), (40, {"B": 9, "A": 0, "C": 1})]
    AB = ["A", "B", "C"]
    t = totals(BLANK, AB)
    assert t == {"A": 600, "B": 360, "C": 40} and max(t, key=t.get) == "A"
    av = averages(BLANK, AB)
    assert av["A"] == 6.0 and av["B"] == 9.0 and abs(av["C"] - 0.4) < 1e-9
    assert max(av, key=av.get) == "B"
    # quorum: a candidate must be rated by at least half the voters to be eligible
    rated = {c: sum(n for n, b in BLANK if c in b) for c in AB}
    assert rated == {"A": 100, "B": 40, "C": 100}
    eligible = [c for c in AB if rated[c] >= 50]
    assert eligible == ["A", "C"] and max(eligible, key=lambda c: av[c]) == "A"
    ok.append("blank != zero: same ballots give A by total, B by average, A by average+quorum")

    # The article's own example cannot expose this -- everyone rates everyone,
    # so total and average are the same ranking.
    assert sorted(TENN, key=lambda c: -tot[c]) == sorted(TENN, key=lambda c: -averages(T, TENN)[c])
    ok.append("...and the article's example can't show it: all 100 voters rate all 4 cities")

    # ---- 4. IIA holds for absolute scores, breaks under normalisation -----
    ABS = [(55, {"A": 10, "B": 7, "C": 0}), (45, {"A": 0, "B": 10, "C": 8})]
    t3 = totals(ABS, AB)
    assert t3 == {"A": 550, "B": 835, "C": 360} and max(t3, key=t3.get) == "B"
    drop = [(n, {k: v for k, v in b.items() if k != "C"}) for n, b in ABS]
    t2 = totals(drop, ["A", "B"])
    assert t2 == {"A": 550, "B": 835} and max(t2, key=t2.get) == "B"
    ok.append("IIA with absolute scores: dropping loser C leaves B winning, totals untouched")

    def normalise(b):
        lo, hi = min(b.values()), max(b.values())
        return {c: (10 if hi == lo else round(10 * (v - lo) / (hi - lo))) for c, v in b.items()}

    norm3 = [(n, normalise(b)) for n, b in ABS]
    assert totals(norm3, AB) == t3                    # already normalised
    norm2 = [(n, normalise({k: v for k, v in b.items() if k != "C"})) for n, b in ABS]
    assert norm2[0][1] == {"A": 10, "B": 0} and norm2[1][1] == {"A": 0, "B": 10}
    t2n = totals(norm2, ["A", "B"])
    assert t2n == {"A": 550, "B": 450} and max(t2n, key=t2n.get) == "A"
    ok.append("...but if voters renormalise to the field, dropping C flips B -> A. IIA fails")

    # ---- 5. Majority and Condorcet both fail ------------------------------
    MAJ = [(51, {"A": 10, "B": 9}), (49, {"A": 0, "B": 10})]
    tm = totals(MAJ, ["A", "B"])
    assert tm == {"A": 510, "B": 949} and max(tm, key=tm.get) == "B"
    assert condorcet(MAJ, ["A", "B"]) == "A" and prefer(MAJ, "A", "B") == (51, 49)
    ok.append("majority/Condorcet fail: A is the choice of 51 of 100, B wins 949-510")

    # ---- 6. Honest score is excellent; strategic score is plurality -------
    # Zero-information approval strategy: max out everyone above your own mean.
    strat = []
    for home in TENN:
        b = SCORE10[home]
        mean = sum(b.values()) / len(b)
        strat.append((SHARE[home], {c: (1 if b[c] > mean else 0) for c in TENN}))
    assert strat[0][1] == {"Memphis": 1, "Nashville": 0, "Chattanooga": 0, "Knoxville": 0}
    assert strat[2][1] == {"Memphis": 0, "Nashville": 1, "Chattanooga": 1, "Knoxville": 1}
    ts = totals(strat, TENN)
    assert ts == {"Memphis": 42, "Nashville": 41, "Chattanooga": 32, "Knoxville": 32}
    assert max(ts, key=ts.get) == "Memphis"
    ok.append("min-maxed, the SAME electorate elects Memphis 42-41 -- the Condorcet LOSER")
    ok.append("  (honest score elects Nashville, the Condorcet winner, 603-457)")

    # ---- 7. Score keeps participation and monotonicity; STAR loses them ---
    C3 = ["A", "B", "C"]
    rng = random.Random(20260801)
    checked = 0
    for _ in range(60000):
        prof = [(rng.randint(1, 60), {c: rng.randint(0, 5) for c in C3}) for _ in range(3)]
        base, joiner = prof[:-1], prof[-1][1]
        tb, tf = totals(base, C3), totals(prof, C3)
        wb, wf = max(tb, key=tb.get), max(tf, key=tf.get)
        if len({c for c in C3 if tb[c] == tb[wb]}) > 1 or len({c for c in C3 if tf[c] == tf[wf]}) > 1:
            continue
        checked += 1
        assert not (joiner[wb] > joiner[wf]), (prof, wb, wf)   # participation
        for i, (n, b) in enumerate(prof):                      # monotonicity
            for new in range(b[wf] + 1, 6):
                ab = dict(b); ab[wf] = new
                tr = totals(prof[:i] + [(n, ab)] + prof[i + 1:], C3)
                assert max(tr, key=tr.get) == wf
    assert checked > 30000
    ok.append(f"score: no participation or monotonicity failure in {checked} clean profiles")

    # STAR's runoff costs participation. Found by search, hard-coded here:
    JOIN = [(44, {"A": 2, "B": 3, "C": 2}), (20, {"A": 4, "B": 1, "C": 5}),
            (11, {"A": 1, "B": 3, "C": 5})]
    wo, c1 = star(JOIN[:2], C3)
    wi, c2 = star(JOIN, C3)
    assert c1 and c2 and wo == "C" and wi == "B"
    assert JOIN[2][1]["C"] > JOIN[2][1]["B"]        # the joiners preferred C
    assert totals(JOIN[:2], C3) == {"A": 168, "B": 152, "C": 188}
    assert totals(JOIN, C3) == {"A": 179, "B": 185, "C": 243}
    ok.append("STAR participation fails: 11 voters preferring C 5 to B 3 turn out, and C loses to B")
    ok.append("  their B=3 lifted B past A into the runoff, where B beat their own favourite")

    # ---- 8. STAR vs Ranked Robin, Equal Vote's own two methods ------------
    CLONE = [(48, {"A1": 5, "A2": 5, "B": 0}), (52, {"A1": 2, "A2": 1, "B": 3})]
    CC = ["A1", "A2", "B"]
    assert star(CLONE, CC) == ("A1", True)
    assert ranked_robin(CLONE, CC) == ("B", True)
    assert condorcet(CLONE, CC) == "B"
    ok.append("Equal Vote's own two methods split on the clone profile: STAR->A1, Ranked Robin->B")

    rng = random.Random(99)
    same = diff = 0
    for _ in range(60000):
        prof = [(rng.randint(1, 60), {c: rng.randint(0, 5) for c in C3}) for _ in range(3)]
        ws, o1 = star(prof, C3)
        wr, o2 = ranked_robin(prof, C3)
        if not (o1 and o2):
            continue
        same += ws == wr
        diff += ws != wr
    rate = 100 * diff / (same + diff)
    assert 2.0 < rate < 4.5, rate
    ok.append(f"over {same + diff} random 3-candidate profiles they disagree {rate:.1f}% of the time")

    rng = random.Random(1234)
    have = miss = 0
    for _ in range(60000):
        prof = [(rng.randint(1, 60), {c: rng.randint(0, 5) for c in C3}) for _ in range(3)]
        cw = condorcet(prof, C3)
        if cw is None:
            continue
        w, o = star(prof, C3)
        if not o:
            continue
        have += 1
        miss += w != cw
    mrate = 100 * miss / have
    assert 1.0 < mrate < 2.5, mrate
    ok.append(f"and STAR misses an existing Condorcet winner in {mrate:.1f}% of {have} profiles")

    print("all checks passed\n")
    for line in ok:
        print(("  + " + line) if not line.startswith("  ") else ("   " + line.strip()))


if __name__ == "__main__":
    main()
