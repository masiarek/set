#!/usr/bin/env python3
"""Verify every claim in ../../lumen-75-ballot-four-winners.md.

The profile is the senior-class-president example from Lumen Learning's
"Putting It Together: Voting Theory" (Math for Liberal Arts, Module 7):
https://courses.lumenlearning.com/wmopen-mathforliberalarts/chapter/putting-it-together-voting-theory/

Run:  python3 verify.py
No dependencies. Every assertion below is checked, not printed on trust.
"""

from itertools import permutations

CANDS = ["Garcia", "Lee", "Nguyen", "Smith"]

BASE = [
    (20, ["Garcia", "Lee", "Nguyen", "Smith"]),
    (3,  ["Garcia", "Nguyen", "Lee", "Smith"]),
    (8,  ["Lee", "Nguyen", "Garcia", "Smith"]),
    (16, ["Nguyen", "Garcia", "Lee", "Smith"]),
    (28, ["Smith", "Lee", "Garcia", "Nguyen"]),
]
N = sum(n for n, _ in BASE)


# ---------------------------------------------------------------- machinery

def plurality(prof, alive):
    t = {c: 0 for c in alive}
    for n, b in prof:
        for x in b:
            if x in alive:
                t[x] += n
                break
    return t


def borda(prof, cands):
    k = len(cands)
    t = {c: 0 for c in cands}
    for n, b in prof:
        for i, x in enumerate([x for x in b if x in cands]):
            t[x] += n * (k - i)
    return t


def pairwise(prof, cands):
    return {(a, b): sum(n for n, bal in prof if bal.index(a) < bal.index(b))
            for a, b in permutations(cands, 2)}


def condorcet(prof, cands):
    m = pairwise(prof, cands)
    for c in cands:
        if all(m[(c, d)] > m[(d, c)] for d in cands if d != c):
            return c
    return None


def copeland(prof, cands):
    """Matchup wins, ties count 1/2 — Ranked Robin's first step."""
    m = pairwise(prof, cands)
    out = {}
    for c in cands:
        w = sum(1 for d in cands if d != c and m[(c, d)] > m[(d, c)])
        t = sum(1 for d in cands if d != c and m[(c, d)] == m[(d, c)])
        out[c] = w + t / 2
    return out


def margin_sum(prof, cands):
    """Ranked Robin's tiebreak step: sum of pairwise margins."""
    m = pairwise(prof, cands)
    return {c: sum(m[(c, d)] - m[(d, c)] for d in cands if d != c) for c in cands}


def ranked_robin(prof, cands):
    """Copeland wins, then sum-of-margins. Returns (winner, decided_at_step)."""
    cop = copeland(prof, cands)
    best = max(cop.values())
    top = [c for c in cands if cop[c] == best]
    if len(top) == 1:
        return top[0], "wins"
    ms = margin_sum(prof, cands)
    return max(top, key=lambda c: ms[c]), "margins"


def irv(prof, cands, trace=False):
    alive, log = list(cands), []
    while len(alive) > 1:
        t = plurality(prof, alive)
        lead = max(t, key=t.get)
        if t[lead] * 2 > sum(t.values()):
            log.append((dict(t), "majority of continuing ballots"))
            return (lead, log) if trace else lead
        lo = min(t.values())
        out = [c for c in alive if t[c] == lo]
        log.append((dict(t), "eliminate " + ", ".join(out)))
        for c in out:
            alive.remove(c)
    return (alive[0], log) if trace else alive[0]


def coombs(prof, cands):
    alive = list(cands)
    while len(alive) > 1:
        t = plurality(prof, alive)
        lead = max(t, key=t.get)
        if t[lead] * 2 > sum(t.values()):
            return lead
        last = {c: 0 for c in alive}
        for n, b in prof:
            last[[x for x in b if x in alive][-1]] += n
        alive.remove(max(last, key=last.get))
    return alive[0]


def bucklin(prof, cands):
    tally = {c: 0 for c in cands}
    for depth in range(len(cands)):
        for n, b in prof:
            tally[[x for x in b if x in cands][depth]] += n
        lead = max(tally, key=tally.get)
        if tally[lead] * 2 > N:
            return lead, depth + 1, dict(tally)
    return max(tally, key=tally.get), len(cands), dict(tally)


def approval_top_k(prof, cands, k):
    t = {c: 0 for c in cands}
    for n, b in prof:
        for x in b[:k]:
            t[x] += n
    return t


def variant(**kw):
    """Rebuild the profile with substitutions; drop empty groups."""
    return [(n, b) for n, b in kw["rows"] if n > 0]


# ---------------------------------------------------------------- the claims

def main():
    ok = []

    assert N == 75
    ok.append("75 ballots")

    # 1. The page's four methods, four winners.
    p = plurality(BASE, CANDS)
    assert p == {"Garcia": 23, "Lee": 8, "Nguyen": 16, "Smith": 28}
    assert max(p, key=p.get) == "Smith"
    ok.append("plurality -> Smith (23/8/16/28)")

    b = borda(BASE, CANDS)
    assert b == {"Garcia": 212, "Lee": 214, "Nguyen": 165, "Smith": 159}
    assert sum(b.values()) == N * 10          # each ballot spends 4+3+2+1
    assert max(b, key=b.get) == "Lee"
    ok.append("Borda -> Lee (212/214/165/159, sum 750)")

    w, log = irv(BASE, CANDS, trace=True)
    assert w == "Nguyen"
    assert log[1][0] == {"Garcia": 23, "Nguyen": 24, "Smith": 28}
    ok.append("IRV -> Nguyen (Garcia eliminated 23 v 24 in round 2)")

    m = pairwise(BASE, CANDS)
    assert (m[("Garcia", "Lee")], m[("Garcia", "Nguyen")], m[("Garcia", "Smith")]) == (39, 51, 47)
    assert condorcet(BASE, CANDS) == "Garcia"
    ok.append("Condorcet -> Garcia (39-36, 51-24, 47-28)")

    # 2. Smith is last on a majority of ballots yet wins plurality.
    last_smith = sum(n for n, bal in BASE if bal[-1] == "Smith")
    assert last_smith == 47 and last_smith * 2 > N
    ok.append("Smith ranked last on 47 of 75 ballots")

    # 3. Ranked Robin elects Garcia -- and does so at the WINS step, not margins.
    cop = copeland(BASE, CANDS)
    assert cop == {"Garcia": 3, "Lee": 2, "Nguyen": 1, "Smith": 0}
    rr, step = ranked_robin(BASE, CANDS)
    assert (rr, step) == ("Garcia", "wins")
    ok.append("Ranked Robin -> Garcia, decided at the wins step (3/2/1/0)")

    # 4. ...which matters, because the margins step alone would say Lee.
    ms = margin_sum(BASE, CANDS)
    assert ms == {"Garcia": 49, "Lee": 53, "Nguyen": -45, "Smith": -57}
    assert max(ms, key=ms.get) == "Lee"
    # margin-sum is an affine image of Borda: it reproduces Borda's order
    assert sorted(ms, key=ms.get) == sorted(b, key=b.get)
    # Exact identity. With points k..1, Borda(c) = sum_d m[c,d] + N, and every
    # pair sums to N, so margin(c) = 2*Borda(c) - N*(k+1) = 2*Borda(c) - 375.
    for c in CANDS:
        assert ms[c] == 2 * b[c] - N * (len(CANDS) + 1)
    ok.append("margin-sum alone -> Lee; margin-sum == 2*Borda - 375 exactly")

    # 5. Other Condorcet-consistent methods agree on Garcia.
    minimax = {c: max(m[(d, c)] - m[(c, d)] for d in CANDS if d != c) for c in CANDS}
    assert min(minimax, key=minimax.get) == "Garcia" and minimax["Garcia"] == -3
    assert coombs(BASE, CANDS) == "Garcia"
    ok.append("Minimax -> Garcia; Coombs -> Garcia")

    # 6. Bucklin gives a fifth reading (same tallies as top-2 approval).
    bw, depth, btal = bucklin(BASE, CANDS)
    assert (bw, depth) == ("Lee", 2)
    assert btal == approval_top_k(BASE, CANDS, 2)
    ok.append("Bucklin -> Lee at depth 2, tallies identical to top-2 approval")

    # 7. Approval has no single answer here: the threshold picks the winner.
    a1, a2, a3 = (approval_top_k(BASE, CANDS, k) for k in (1, 2, 3))
    assert max(a1, key=a1.get) == "Smith"
    assert max(a2, key=a2.get) == "Lee"
    assert max(a3, key=a3.get) == "Garcia"
    assert a3["Garcia"] == 75 and a3["Lee"] == 75      # a genuine 75-75 tie at top-3
    ok.append("approval: top-1 -> Smith, top-2 -> Lee, top-3 -> Garcia/Lee tie at 75")

    # 8. IRV monotonicity failure: raising Nguyen makes Nguyen lose.
    window = []
    for k in range(0, 29):
        prof = variant(rows=[
            (20, ["Garcia", "Lee", "Nguyen", "Smith"]),
            (3,  ["Garcia", "Nguyen", "Lee", "Smith"]),
            (8,  ["Lee", "Nguyen", "Garcia", "Smith"]),
            (16, ["Nguyen", "Garcia", "Lee", "Smith"]),
            (28 - k, ["Smith", "Lee", "Garcia", "Nguyen"]),
            (k,  ["Nguyen", "Smith", "Lee", "Garcia"]),
        ])
        if irv(prof, CANDS) != "Nguyen":
            window.append(k)
            assert condorcet(prof, CANDS) == "Garcia"   # CW never moves
    assert window == list(range(6, 14))
    ok.append("IRV non-monotonic: promoting Nguyen on 6-13 of the 28 Smith ballots elects Garcia")

    # the k=6 trace: Smith, not Garcia, is now the round-2 casualty
    prof6 = variant(rows=[
        (20, ["Garcia", "Lee", "Nguyen", "Smith"]),
        (3,  ["Garcia", "Nguyen", "Lee", "Smith"]),
        (8,  ["Lee", "Nguyen", "Garcia", "Smith"]),
        (16, ["Nguyen", "Garcia", "Lee", "Smith"]),
        (22, ["Smith", "Lee", "Garcia", "Nguyen"]),
        (6,  ["Nguyen", "Smith", "Lee", "Garcia"]),
    ])
    w6, log6 = irv(prof6, CANDS, trace=True)
    assert w6 == "Garcia"
    assert log6[1][0] == {"Garcia": 23, "Nguyen": 30, "Smith": 22}
    ok.append("k=6 trace: Smith eliminated at 22, its ballots elect Garcia 45-30")

    # 9. IRV favorite betrayal: Garcia's own bloc does better abandoning Garcia.
    minimum = None
    for j in range(0, 21):
        prof = variant(rows=[
            (20 - j, ["Garcia", "Lee", "Nguyen", "Smith"]),
            (j,  ["Lee", "Garcia", "Nguyen", "Smith"]),
            (3,  ["Garcia", "Nguyen", "Lee", "Smith"]),
            (8,  ["Lee", "Nguyen", "Garcia", "Smith"]),
            (16, ["Nguyen", "Garcia", "Lee", "Smith"]),
            (28, ["Smith", "Lee", "Garcia", "Nguyen"]),
        ])
        if irv(prof, CANDS) == "Lee" and minimum is None:
            minimum = j
    assert minimum == 8      # Lee is their #2; sincerity gets them Nguyen, their #3
    ok.append("IRV favorite betrayal: 8 of 20 Garcia voters ranking Lee first elects Lee (their #2)")

    # 10. Both losers are IRV spoilers against the Condorcet winner.
    assert irv(BASE, ["Garcia", "Lee", "Smith"]) == "Garcia"      # drop Nguyen
    assert irv(BASE, ["Garcia", "Lee", "Nguyen"]) == "Garcia"     # drop Smith
    assert irv(BASE, ["Lee", "Nguyen", "Smith"]) == "Lee"         # drop Garcia
    ok.append("IRV spoilers: removing Nguyen OR Smith elects Garcia")

    print("all checks passed\n")
    for line in ok:
        print("  +", line)


if __name__ == "__main__":
    main()
