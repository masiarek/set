#!/usr/bin/env python3
"""Verify every numeric claim in ../../majority-judgment.md.

Majority judgment (Balinski & Laraki): voters GRADE every candidate on a verbal
scale; the candidate with the highest MEDIAN grade wins.  Ties on the median are
broken by stripping median grades one at a time until the medians separate --
equivalently, by the (median, sign, magnitude) key implemented below.

Run:  python3 verify.py
No dependencies. Every assertion below is checked, not printed on trust.
"""

import random

# ---------------------------------------------------------------- the method


def grades_of(prof, c):
    out = []
    for n, b in prof:
        out += [b[c]] * n
    return sorted(out)


def mj_key(prof, c):
    """Balinski-Laraki comparison key. Higher sorts better.

    median alpha; p = share strictly above, q = share strictly below.
    p > q  -> 'alpha+', better the larger p.   Otherwise 'alpha-', better the
    smaller q.  This is provably equivalent to removing median grades one by one.
    """
    g = grades_of(prof, c)
    a = g[(len(g) - 1) // 2]                 # lower median, the MJ convention
    p = sum(1 for x in g if x > a)
    q = sum(1 for x in g if x < a)
    return (a, 1, p) if p > q else (a, 0, -q)


def mj(prof, cands):
    best = max(cands, key=lambda c: mj_key(prof, c))
    tied = [c for c in cands if mj_key(prof, c) == mj_key(prof, best)]
    return best, len(tied) == 1


def mean_winner(prof, cands):
    t = {c: sum(n * b[c] for n, b in prof) for c in cands}
    best = max(t, key=t.get)
    return best, sum(1 for c in cands if t[c] == t[best]) == 1


def prefer(prof, x, y):
    return (sum(n for n, b in prof if b[x] > b[y]),
            sum(n for n, b in prof if b[y] > b[x]))


def condorcet(prof, cands):
    for c in cands:
        if all(prefer(prof, c, d)[0] > prefer(prof, c, d)[1] for d in cands if d != c):
            return c
    return None


# ------------------------------------------------- Laslier's left-right example

GROUPS = [("Far-left", 101), ("Left", 101), ("Cen-left", 101), ("Center", 50),
          ("Cen-right", 99), ("Right", 99), ("Far-right", 99)]
AXIS = [g for g, _ in GROUPS]
G7 = ["awful", "very bad", "bad", "mediocre", "good", "very good", "excellent"]
# candidate i graded by group j at 6 - |i-j|: your own camp is excellent, and
# each step away costs one grade.
LASLIER = [(size, {AXIS[i]: 6 - abs(i - j) for i in range(7)})
           for j, (_, size) in enumerate(GROUPS)]

# ---------------------------------------------------------------- Tennessee

TENN = ["Memphis", "Nashville", "Chattanooga", "Knoxville"]
DIST = {("Memphis", "Knoxville"): 345.1, ("Memphis", "Nashville"): 194.2,
        ("Memphis", "Chattanooga"): 268.1, ("Knoxville", "Nashville"): 159.5,
        ("Knoxville", "Chattanooga"): 96.2, ("Nashville", "Chattanooga"): 115.2}
SHARE = {"Memphis": 42, "Nashville": 26, "Chattanooga": 15, "Knoxville": 17}
G4 = ["poor", "fair", "good", "excellent"]


def dist(a, b):
    return 0.0 if a == b else (DIST.get((a, b)) or DIST[(b, a)])


def grade(home, c, farthest_clause=True):
    """The article's rule: own city excellent; THE FARTHEST CITY POOR; the rest
    good / fair / poor for under 100 / under 200 / over 200 miles."""
    d = dist(home, c)
    if d == 0:
        return 3
    if farthest_clause and d == max(dist(home, x) for x in TENN):
        return 0
    return 2 if d < 100 else (1 if d < 200 else 0)


def tenn_prof(farthest_clause=True):
    return [(SHARE[h], {c: grade(h, c, farthest_clause) for c in TENN}) for h in TENN]


# ---------------------------------------------------------------- the claims


def main():
    ok = []
    C3 = ["A", "B", "C"]

    # ---- 1. Tennessee ------------------------------------------------------
    TP = tenn_prof()
    assert {c: grade("Nashville", c) for c in TENN} == {
        "Memphis": 0, "Nashville": 3, "Chattanooga": 1, "Knoxville": 1}
    keys = {c: mj_key(TP, c) for c in TENN}
    assert keys["Memphis"][0] == 0                      # median poor
    assert all(keys[c][0] == 1 for c in ("Nashville", "Chattanooga", "Knoxville"))
    assert keys["Nashville"][1] == 1 and keys["Nashville"][2] == 26        # fair+
    assert keys["Chattanooga"] == (1, 0, -42) and keys["Knoxville"] == (1, 0, -42)
    assert mj(TP, TENN) == ("Nashville", True)
    assert condorcet(TP, TENN) == "Nashville"
    ok.append("Tennessee: Memphis poor, the rest fair; Nashville alone is fair+ (26 above, 0 below)")
    ok.append("  -> Nashville, who is also the Condorcet winner")

    # ---- 2. ...and that result hangs on one clause of the grading rule -----
    # Drop only the "farthest city gets Poor" clause and keep the mileage bands:
    # Nashville voters would grade Memphis 'fair' (194.2 < 200) instead of 'poor'.
    LOOSE = tenn_prof(farthest_clause=False)
    assert grade("Nashville", "Memphis", False) == 1
    assert mj_key(LOOSE, "Memphis") == (1, 1, 42)       # fair+, and 42 > 26
    assert mj(LOOSE, TENN)[0] == "Memphis"
    ok.append("one clause is load-bearing: without 'farthest city = poor', MJ elects MEMPHIS")
    ok.append("  the Condorcet loser, because 42 fair+ outranks Nashville's 26 fair+")

    # ---- 3. Laslier: the highest-median rule misses the median voter -------
    assert sum(s for _, s in GROUPS) == 650
    lk = {c: mj_key(LASLIER, c) for c in AXIS}
    assert lk["Far-left"][0] == 3 and lk["Far-right"][0] == 3          # mediocre
    assert all(lk[c][0] == 4 for c in AXIS[1:6])                       # good
    assert lk["Left"] == (4, 1, 303)
    assert lk["Cen-left"] == (4, 1, 252) and lk["Center"] == (4, 1, 250)
    assert lk["Cen-right"] == (4, 1, 248) and lk["Right"] == (4, 0, -303)
    assert mj(LASLIER, AXIS) == ("Left", True)
    assert condorcet(LASLIER, AXIS) == "Center"
    assert mean_winner(LASLIER, AXIS) == ("Center", True)
    ok.append("Laslier 650-voter left-right: five candidates tie at median 'good'")
    ok.append("  MJ -> Left; the Condorcet winner AND the score winner are both Center")
    ok.append("  so the highest-MEDIAN rule fails the MEDIAN VOTER criterion")

    # The mechanism: the tiebreak reads only the distance to the median, so the
    # bigger, more homogeneous wing beats the better-centred candidate.
    assert lk["Left"][2] > lk["Center"][2]
    assert sum(s for _, s in GROUPS[:3]) == 303 and sum(s for _, s in GROUPS[4:]) == 297
    ok.append("  left wing 303 vs right wing 297: MJ hands it to the larger wing, not the middle")

    # ---- 4. Majority criterion fails --------------------------------------
    # 51 of 100 grade A strictly highest, and A loses.
    MAJ = [(26, {"A": 5, "B": 4, "C": 0}),
           (25, {"A": 1, "B": 0, "C": 0}),
           (49, {"A": 0, "B": 4, "C": 5})]
    top = sum(n for n, b in MAJ if b["A"] > max(b[c] for c in C3 if c != "A"))
    assert top == 51 and top * 2 > 100
    assert mj(MAJ, C3)[0] == "B" and mj_key(MAJ, "A")[0] < mj_key(MAJ, "B")[0]
    ok.append("majority fails: A is the strict top grade of 51 of 100 voters and MJ elects B")

    # ---- 5. Participation fails (the no-show paradox) ---------------------
    rng = random.Random(20260801)
    found = None
    for _ in range(400000):
        prof = [(rng.randint(1, 40), {c: rng.randint(0, 5) for c in C3}) for _ in range(4)]
        w0, c0 = mj(prof[:-1], C3)
        w1, c1 = mj(prof, C3)
        if not (c0 and c1) or w0 == w1:
            continue
        joiner = prof[-1][1]
        if joiner[w0] > joiner[w1]:
            found = (prof, w0, w1)
            break
    assert found, "expected a no-show paradox"
    prof, w0, w1 = found
    assert prof[-1][1][w0] > prof[-1][1][w1]
    ok.append("participation fails: a bloc turns out and replaces its preferred winner")
    ok.append(f"  {[(n, dict(b)) for n, b in prof]}: without them {w0}, with them {w1}")

    # ---- 6. IIA holds ------------------------------------------------------
    rng = random.Random(7)
    checked = 0
    for _ in range(200000):
        prof = [(rng.randint(1, 40), {c: rng.randint(0, 5) for c in C3}) for _ in range(3)]
        w, clean = mj(prof, C3)
        if not clean:
            continue
        checked += 1
        for loser in [c for c in C3 if c != w]:
            sub = [c for c in C3 if c != loser]
            w2, clean2 = mj(prof, sub)
            assert not clean2 or w2 == w, (prof, w, loser, w2)
    assert checked > 100000
    ok.append(f"IIA holds: dropping a loser never moved the winner in {checked} clean profiles")

    # ---- 7. The median is what buys strategy resistance -------------------
    # One bloc maxes/mins its ballot. Watch the mean move and the median not.
    BASE = [(20, {"A": 3, "B": 4}), (20, {"A": 4, "B": 3}), (21, {"A": 3, "B": 3})]
    tot = {c: sum(n * b[c] for n, b in BASE) for c in ["A", "B"]}
    assert tot == {"A": 203, "B": 203}                               # dead heat on sum
    assert mj_key(BASE, "A")[0] == 3 and mj_key(BASE, "B")[0] == 3
    EXAG = [(20, {"A": 0, "B": 5}), (20, {"A": 4, "B": 3}), (21, {"A": 3, "B": 3})]
    tot2 = {c: sum(n * b[c] for n, b in EXAG) for c in ["A", "B"]}
    assert tot2 == {"A": 143, "B": 223}          # mean: exaggeration moved 80 points
    assert mj_key(EXAG, "A")[0] == 3 and mj_key(EXAG, "B")[0] == 3   # median: unmoved
    ok.append("strategy: one bloc min-maxing swings the score totals 203-203 -> 143-223,")
    ok.append("  and leaves both medians exactly where they were")

    # ---- 8. MJ vs plain score, how often do they differ? ------------------
    rng = random.Random(99)
    same = diff = 0
    for _ in range(120000):
        prof = [(rng.randint(1, 40), {c: rng.randint(0, 5) for c in C3}) for _ in range(3)]
        wm, c1 = mj(prof, C3)
        ws, c2 = mean_winner(prof, C3)
        if not (c1 and c2):
            continue
        same += wm == ws
        diff += wm != ws
    rate = 100 * diff / (same + diff)
    assert 10 < rate < 30, rate
    ok.append(f"MJ and score disagree on {rate:.1f}% of {same + diff} random 3-candidate profiles")

    rng = random.Random(4321)
    have = miss = 0
    for _ in range(120000):
        prof = [(rng.randint(1, 40), {c: rng.randint(0, 5) for c in C3}) for _ in range(3)]
        cw = condorcet(prof, C3)
        if cw is None:
            continue
        w, clean = mj(prof, C3)
        if not clean:
            continue
        have += 1
        miss += w != cw
    mrate = 100 * miss / have
    assert 5 < mrate < 25, mrate
    ok.append(f"and MJ misses an existing Condorcet winner in {mrate:.1f}% of {have} profiles")

    print("all checks passed\n")
    for line in ok:
        print(("  + " + line) if not line.startswith("  ") else ("   " + line.strip()))


if __name__ == "__main__":
    main()
