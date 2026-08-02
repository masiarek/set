#!/usr/bin/env python3
"""Verify every numeric claim in ../../star-voting.md.

STAR = Score Then Automatic Runoff: sum 0-5 scores, take the top two, then
elect whichever of those two is scored higher on more ballots.

Tie rules follow the Equal Vote Coalition's published ones
(https://www.starvoting.org/ties): a scoring-round tie is broken between the
tied candidates by head-to-head preference; a runoff tie is broken by total
score; anything left is a true tie decided by lot.  Getting this wrong matters
-- breaking a scoring tie against the leader instead of between the tied
candidates manufactures a monotonicity violation that does not exist.

Run:  python3 verify.py
No dependencies. Every assertion below is checked, not printed on trust.
"""

import itertools
import random

# ---------------------------------------------------------------- the method


def scores(prof, cands):
    return {c: sum(n * b[c] for n, b in prof) for c in cands}


def prefer(prof, x, y):
    """(voters scoring x above y, voters scoring y above x). Equal = neither."""
    return (sum(n for n, b in prof if b[x] > b[y]),
            sum(n for n, b in prof if b[y] > b[x]))


def star(prof, cands):
    """-> (winner, (finalist1, finalist2), scores, clean).

    clean is False when a coin flip was needed, i.e. the result is not
    determined by the ballots alone.
    """
    sc = scores(prof, cands)
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
            # Equal Vote rule: break it among the tied, head-to-head
            wins = {c: sum(1 for d in tied
                           if d != c and prefer(prof, c, d)[0] > prefer(prof, c, d)[1])
                    for c in tied}
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
    else:                                   # runoff tie -> higher total score
        if sc[f1] == sc[f2]:
            clean = False
        w = f1 if sc[f1] > sc[f2] else f2
    return w, (f1, f2), sc, clean


# ------------------------------------------------- other methods, for contrast


def ranks(b, cands):
    """Score ballot -> candidates best-first (ties broken by name, only used
    where the profile has no relevant ties)."""
    return sorted(cands, key=lambda c: (-b[c], c))


def plurality(prof, cands, alive=None):
    alive = alive or cands
    t = {c: 0 for c in alive}
    for n, b in prof:
        t[ranks(b, alive)[0]] += n
    return t


def irv(prof, cands):
    alive = list(cands)
    while len(alive) > 1:
        t = plurality(prof, cands, alive)
        lead = max(t, key=t.get)
        if t[lead] * 2 > sum(t.values()):
            return lead
        alive.remove(min(t, key=t.get))
    return alive[0]


def two_round(prof, cands):
    t = plurality(prof, cands)
    a, b = sorted(cands, key=lambda c: -t[c])[:2]
    x, y = prefer(prof, a, b)
    return a if x > y else b


def approval_top_k(prof, cands, k):
    t = {c: 0 for c in cands}
    for n, b in prof:
        for c in ranks(b, cands)[:k]:
            t[c] += n
    return t


def condorcet(prof, cands):
    for c in cands:
        if all(prefer(prof, c, d)[0] > prefer(prof, c, d)[1] for d in cands if d != c):
            return c
    return None


# ---------------------------------------------------------------- Tennessee

TENN = ["Memphis", "Nashville", "Chattanooga", "Knoxville"]

# Wikipedia's score table, read off the article as printed.
TENN_PROF = [
    (42, {"Memphis": 5, "Nashville": 2, "Chattanooga": 1, "Knoxville": 0}),
    (26, {"Memphis": 0, "Nashville": 5, "Chattanooga": 2, "Knoxville": 1}),
    (15, {"Memphis": 0, "Nashville": 3, "Chattanooga": 5, "Knoxville": 3}),
    (17, {"Memphis": 0, "Nashville": 2, "Chattanooga": 4, "Knoxville": 5}),
]

# Road distances in miles, from the HTML comment in the article's source.
DIST = {
    ("Memphis", "Knoxville"): 345.1, ("Memphis", "Nashville"): 194.2,
    ("Memphis", "Chattanooga"): 268.1, ("Knoxville", "Nashville"): 159.5,
    ("Knoxville", "Chattanooga"): 96.2, ("Nashville", "Chattanooga"): 115.2,
}


def dist(a, b):
    if a == b:
        return 0.0
    return DIST.get((a, b)) or DIST[(b, a)]


def derived_ballot(home):
    """The article's stated rule: 5 for your own city, 0 for the farthest, the
    rest 'proportional to their relative distance'."""
    far = max(dist(home, c) for c in TENN)
    out = {}
    for c in TENN:
        exact = 5.0 * (1.0 - dist(home, c) / far)
        out[c] = int(exact + 0.5)          # round half up
    return out


# ------------------------------------------- hand-built failure profiles

ABC = ["A", "B", "C"]

# Clone independence + majority + Condorcet, all in one profile.
CLONE = [
    (48, {"A1": 5, "A2": 5, "B": 0}),
    (52, {"A1": 2, "A2": 1, "B": 3}),
]
CLONE_CANDS = ["A1", "A2", "B"]

# Later-no-harm: bloc X prefers A > B > C.  Scoring B at all costs them A.
LNH_SINCERE = [
    (45, {"A": 5, "B": 4, "C": 0}),
    (45, {"A": 1, "B": 3, "C": 5}),
    (10, {"A": 3, "B": 5, "C": 0}),
]
LNH_WITHHELD = [
    (45, {"A": 5, "B": 0, "C": 0}),
    (45, {"A": 1, "B": 3, "C": 5}),
    (10, {"A": 3, "B": 5, "C": 0}),
]

# Favorite betrayal: bloc X (48) must sink its own favourite A to get C, its
# second choice, instead of B, its last.
FB_SINCERE = [
    (48, {"A": 5, "B": 2, "C": 4}),
    (52, {"A": 1, "B": 5, "C": 0}),
    (8,  {"A": 0, "B": 2, "C": 3}),
]
FB_BETRAYED = [
    (48, {"A": 0, "B": 0, "C": 5}),
    (52, {"A": 1, "B": 5, "C": 0}),
    (8,  {"A": 0, "B": 2, "C": 3}),
]

ALL_BALLOTS = [dict(zip(ABC, t)) for t in itertools.product(range(6), repeat=3)]


# ---------------------------------------------------------------- the claims


def main():
    ok = []

    # ---- 1. Tennessee, exactly as the article prints it -------------------
    w, finalists, sc, clean = star(TENN_PROF, TENN)
    assert sc == {"Memphis": 210, "Nashville": 293, "Chattanooga": 237, "Knoxville": 156}
    assert set(finalists) == {"Nashville", "Chattanooga"} and clean
    assert prefer(TENN_PROF, "Nashville", "Chattanooga") == (68, 32)
    assert w == "Nashville"
    ok.append("Tennessee: 210/293/237/156, runoff Nashville 68 - Chattanooga 32")

    # ---- 2. ...but one printed score does not follow the article's own rule
    derived = {home: derived_ballot(home) for home in TENN}
    printed = {
        "Memphis": TENN_PROF[0][1], "Nashville": TENN_PROF[1][1],
        "Chattanooga": TENN_PROF[2][1], "Knoxville": TENN_PROF[3][1],
    }
    mismatches = [(h, c, printed[h][c], derived[h][c])
                  for h in TENN for c in TENN if printed[h][c] != derived[h][c]]
    assert mismatches == [("Knoxville", "Nashville", 2, 3)], mismatches
    # 5 * (1 - 159.5/345.1) = 2.689 -> 3, and every other cell rounds half up too
    assert abs(5 * (1 - 159.5 / 345.1) - 2.6894) < 1e-3
    ok.append("one printed cell is off: Knoxville voters' Nashville score is 2, rule gives 3")

    fixed = [(42, derived["Memphis"]), (26, derived["Nashville"]),
             (15, derived["Chattanooga"]), (17, derived["Knoxville"])]
    w2, f2, sc2, _ = star(fixed, TENN)
    assert sc2["Nashville"] == 310 and sc2["Memphis"] == 210
    assert set(f2) == {"Nashville", "Chattanooga"} and w2 == "Nashville"
    ok.append("...harmless: Nashville 293 -> 310, same finalists, same winner")

    # ---- 3. The comparison table on the same page -------------------------
    p = plurality(TENN_PROF, TENN)
    assert max(p, key=p.get) == "Memphis" and p["Memphis"] == 42
    assert irv(TENN_PROF, TENN) == "Knoxville"
    assert max(sc, key=sc.get) == "Nashville"                       # score voting
    a2 = approval_top_k(TENN_PROF, TENN, 2)
    assert a2 == {"Memphis": 42, "Nashville": 68, "Chattanooga": 58, "Knoxville": 32}
    assert two_round(TENN_PROF, TENN) == "Nashville"
    assert condorcet(TENN_PROF, TENN) == "Nashville"
    ok.append("same ballots: FPTP->Memphis, IRV->Knoxville, score/approval/runoff/STAR->Nashville")

    # ---- 4. One profile, three named failures -----------------------------
    w, finalists, sc, clean = star(CLONE, CLONE_CANDS)
    assert sc == {"A1": 344, "A2": 292, "B": 156} and clean
    assert set(finalists) == {"A1", "A2"} and w == "A1"

    # B is the strict favourite of 52 of 100 voters -- an absolute majority
    maj = sum(n for n, b in CLONE if b["B"] > max(b[c] for c in CLONE_CANDS if c != "B"))
    assert maj == 52 and maj * 2 > 100
    # B is the Condorcet winner
    assert condorcet(CLONE, CLONE_CANDS) == "B"
    assert prefer(CLONE, "B", "A1") == (52, 48) and prefer(CLONE, "B", "A2") == (52, 48)
    # remove the clone and B wins
    two = [(n, {k: v for k, v in b.items() if k != "A2"}) for n, b in CLONE]
    assert star(two, ["A1", "B"])[0] == "B"
    ok.append("clone profile: majority favourite + Condorcet winner B misses the runoff;")
    ok.append("  dropping A1's clone flips the winner A1 -> B (clone independence fails)")

    # ---- 5. Later-no-harm --------------------------------------------------
    ws, _, scs, c1 = star(LNH_SINCERE, ABC)
    ww, _, scw, c2 = star(LNH_WITHHELD, ABC)
    assert scs == {"A": 300, "B": 365, "C": 225} and ws == "B" and c1
    assert scw == {"A": 300, "B": 185, "C": 225} and ww == "A" and c2
    assert prefer(LNH_SINCERE, "A", "B") == (45, 55)
    assert prefer(LNH_WITHHELD, "A", "C") == (55, 45)
    ok.append("later-no-harm fails: 45 A>B>C voters scoring B 4 instead of 0 lose A, get B")

    # ---- 6. Favorite betrayal, and it is genuinely required ----------------
    w0 = star(FB_SINCERE, ABC)[0]
    w1 = star(FB_BETRAYED, ABC)[0]
    assert w0 == "B" and w1 == "C"
    sincere = FB_SINCERE[0][1]
    assert sincere["C"] > sincere["B"]          # the bloc really does prefer C to B
    n0 = FB_SINCERE[0][0]
    best_loyal, best_betray = sincere[w0], sincere[w0]
    for ab in ALL_BALLOTS:
        trial = [(n0, ab)] + FB_SINCERE[1:]
        wt, _, _, ct = star(trial, ABC)
        if not ct:
            continue
        val = sincere[wt]
        if any(ab[c] > ab["A"] for c in ABC if c != "A"):
            best_betray = max(best_betray, val)
        else:
            best_loyal = max(best_loyal, val)   # includes equal-rating A with others
    assert best_loyal == 2 and best_betray == 4
    ok.append("favorite betrayal fails: bloc gains only by scoring its favourite BELOW another;")
    ok.append("  every ballot keeping A top-equal is worth 2, sinking A is worth 4")

    # ---- 7. mono-raise holds up; mono-raise-delete does not ----------------
    rng = random.Random(20260801)
    tested = 0
    for _ in range(200000):
        prof = [(rng.randint(1, 60), {c: rng.randint(0, 5) for c in ABC})
                for _ in range(3)]
        wref, _, _, clean = star(prof, ABC)
        if not clean:
            continue
        tested += 1
        for i, (n, b) in enumerate(prof):
            for new in range(b[wref] + 1, 6):
                ab = dict(b); ab[wref] = new
                trial = list(prof); trial[i] = (n, ab)
                wt, _, _, ct = star(trial, ABC)
                assert not ct or wt == wref, (prof, i, new, wref, wt)
    assert tested > 100000
    ok.append(f"mono-raise: no violation in {tested} clean random profiles")

    hit = None
    rng = random.Random(11)
    for _ in range(200000):
        prof = [(rng.randint(1, 60), {c: rng.randint(0, 5) for c in ABC})
                for _ in range(3)]
        wref, _, _, clean = star(prof, ABC)
        if not clean:
            continue
        for i, (n, b) in enumerate(prof):
            for new in range(b[wref] + 1, 6):
                ab = {c: (new if c == wref else (0 if b[c] < new else b[c]))
                      for c in ABC}
                trial = list(prof); trial[i] = (n, ab)
                wt, _, _, ct = star(trial, ABC)
                if ct and wt != wref:
                    hit = (prof, i, wref, wt, ab)
                    break
            if hit:
                break
        if hit:
            break
    assert hit, "expected a mono-raise-delete violation (Woodall)"
    ok.append("mono-raise-delete: violation found, confirming Woodall's footnote")
    ok.append(f"  {[(n, dict(b)) for n, b in hit[0]]} raise {hit[2]} -> {hit[4]} elects {hit[3]}")

    # ---- 8. Lane County 2018 ----------------------------------------------
    yes, no = 74408, 82157
    assert yes + no == 156565
    assert abs(yes / (yes + no) * 100 - 47.53) < 0.01
    ok.append("Lane County 20-290: 74,408 - 82,157 = 47.53% yes (article rounds it 47.6%)")

    print("all checks passed\n")
    for line in ok:
        print("  +" if not line.startswith("  ") else "   ", line.strip()
              if not line.startswith("  ") else line)


if __name__ == "__main__":
    main()
