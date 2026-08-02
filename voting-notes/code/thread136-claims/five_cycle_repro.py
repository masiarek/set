#!/usr/bin/env python3
"""The thread's 5-cycle showcase example, reconstructed as actual ballots.

votingtheory.org topic 136 post 1 published two worked examples as PNGs of a
*preference matrix* -- it never published ballots. BetterVoting's sandbox needs
ballots. This file carries a 69-ballot profile that reproduces all 30 cells of
the published 5-cycle matrix exactly, found by simulated annealing over weighted
weak orders (--search re-runs the hunt; the result below is seeded and fixed).

Ballot encoding is BetterVoting's: one integer per candidate, 1 = best, 0 =
unranked, equal numbers = no preference expressed. Pairwise counting here mirrors
packages/backend/src/Tabulators/Util.ts (`remapZero`, strict `<`), so the numbers
below are what the deployed tabulator sees.

Filed as evidence on Equal-Vote/bettervoting#1469.
Run:  python3 five_cycle_repro.py          verify + print the sandbox paste block
      python3 five_cycle_repro.py --search  re-run the reconstruction search
"""

import random
import sys

C = ["Dre", "Edith", "Frank", "Ben", "Abby", "Cici"]
N = 69

# Transcribed from the post-1 PNG: TARGET[(row, col)] = voters preferring row over col.
TARGET = {
    ("Dre", "Edith"): 33, ("Dre", "Frank"): 20, ("Dre", "Ben"): 35, ("Dre", "Abby"): 34, ("Dre", "Cici"): 44,
    ("Edith", "Dre"): 25, ("Edith", "Frank"): 37, ("Edith", "Ben"): 29, ("Edith", "Abby"): 43, ("Edith", "Cici"): 43,
    ("Frank", "Dre"): 49, ("Frank", "Edith"): 24, ("Frank", "Ben"): 37, ("Frank", "Abby"): 28, ("Frank", "Cici"): 45,
    ("Ben", "Dre"): 32, ("Ben", "Edith"): 31, ("Ben", "Frank"): 32, ("Ben", "Abby"): 30, ("Ben", "Cici"): 32,
    ("Abby", "Dre"): 35, ("Abby", "Edith"): 26, ("Abby", "Frank"): 34, ("Abby", "Ben"): 25, ("Abby", "Cici"): 45,
    ("Cici", "Dre"): 16, ("Cici", "Edith"): 26, ("Cici", "Frank"): 16, ("Cici", "Ben"): 31, ("Cici", "Abby"): 24,
}

# (count, [rank per candidate in C order]);  1 = best, 0 = unranked.
BALLOTS = [
    (9, [4, 0, 3, 5, 2, 4]),
    (8, [2, 3, 3, 5, 1, 4]),
    (8, [1, 1, 3, 2, 2, 3]),
    (7, [4, 2, 3, 1, 5, 0]),
    (6, [3, 4, 1, 2, 0, 5]),
    (6, [4, 1, 2, 3, 3, 0]),
    (6, [0, 2, 4, 1, 3, 1]),
    (5, [3, 5, 1, 5, 1, 4]),
    (4, [5, 1, 4, 3, 0, 2]),
    (2, [3, 1, 2, 1, 5, 0]),
    (2, [1, 1, 0, 3, 0, 4]),
    (2, [2, 3, 0, 2, 4, 1]),
    (2, [3, 0, 1, 0, 4, 2]),
    (1, [3, 5, 2, 0, 4, 1]),
    (1, [0, 0, 5, 2, 4, 3]),
]

PAIRS = [(a, b) for a in C for b in C if a != b]


def counts(ballots):
    """Pairwise tallies exactly as Util.ts computes votesPreferredOver."""
    m = {p: 0 for p in PAIRS}
    for w, ranks in ballots:
        key = {c: (float("inf") if r == 0 else r) for c, r in zip(C, ranks)}
        for a, b in PAIRS:
            if key[a] < key[b]:
                m[(a, b)] += w
    return m


def verify(ballots):
    assert sum(w for w, _ in ballots) == N, "ballot count"
    m = counts(ballots)
    bad = {p: (m[p], TARGET[p]) for p in TARGET if m[p] != TARGET[p]}
    assert not bad, f"matrix mismatch: {bad}"
    print(f"{N} ballots in {len(ballots)} types reproduce all 30 published cells exactly.\n")

    cop = {a: sum(1 for b in C if b != a and m[(a, b)] > m[(b, a)])
              + 0.5 * sum(1 for b in C if b != a and m[(a, b)] == m[(b, a)])
           for a in C}
    print("Copeland: " + ", ".join(f"{c} {cop[c]:g}" for c in C))
    top = max(cop.values())
    fin = [c for c in C if cop[c] == top]
    assert len(fin) == 5 and "Cici" not in fin
    print(f"Finalists tied on {top:g} wins: {', '.join(fin)}  "
          "-> 3+ tied, so RankedRobin.ts takes the random rung\n")

    tot = {a: sum(m[(a, b)] - m[(b, a)] for b in fin if b != a) for a in fin}
    assert sum(tot.values()) == 0, "finalist margins must be zero-sum"
    print("1st Degree (sum of margins among the five finalists):")
    for c, v in sorted(tot.items(), key=lambda kv: -kv[1]):
        print(f"  {c:6} {v:+3d} votes  {v / N * 100:+5.1f}%")
    win = max(tot, key=lambda c: tot[c])
    assert win == "Edith" and tot["Edith"] == 20
    print(f"\nSpec winner: {win}, +{tot[win] / N * 100:.1f}% -- matching the thread's own")
    print("published totals (+29.0, +21.7, -1.4, -21.7, -27.5), which also confirms the")
    print("image erratum: Dre is -27.5%, not the -34.8% printed in the PNG.")


def paste_block():
    print("\n--- BetterVoting sandbox (https://bettervoting.com/sandbox) ---")
    print("Voting Method: Ranked Robin,  Number of winners: 1")
    print("Candidates: " + ",".join(C))
    print("Votes:")
    for w, r in BALLOTS:
        print(f"{w}:" + ",".join(map(str, r)))


def search(K, iters, seed):
    """Anneal over K weighted weak-order types; returns (L1 distance, state)."""
    rng = random.Random(seed)
    tvec = [TARGET[p] for p in PAIRS]

    def vec(ranks):
        key = {c: (float("inf") if ranks[c] == 0 else ranks[c]) for c in C}
        return [1 if key[a] < key[b] else 0 for a, b in PAIRS]

    types = [{c: rng.randint(0, 5) for c in C} for _ in range(K)]
    weights = [N // K] * K
    weights[0] += N - sum(weights)
    vecs = [vec(t) for t in types]
    cur = [sum(w * v[i] for w, v in zip(weights, vecs)) for i in range(len(PAIRS))]
    dist = sum(abs(cur[i] - tvec[i]) for i in range(len(PAIRS)))
    best, state = dist, (list(weights), [dict(t) for t in types])
    T0, T1 = 12.0, 0.02
    for it in range(iters):
        T = T0 * (T1 / T0) ** (it / iters)
        if rng.random() < 0.7:
            t, c = rng.randrange(K), rng.choice(C)
            old, new = types[t][c], rng.randint(0, 5)
            if new == old:
                continue
            types[t][c] = new
            nv, w, nd = vec(types[t]), weights[t], dist
            for i in range(len(PAIRS)):
                d = w * (nv[i] - vecs[t][i])
                if d:
                    nd += abs(cur[i] + d - tvec[i]) - abs(cur[i] - tvec[i])
            if nd <= dist or rng.random() < pow(2.718, -(nd - dist) / T):
                for i in range(len(PAIRS)):
                    cur[i] += w * (nv[i] - vecs[t][i])
                vecs[t], dist = nv, nd
            else:
                types[t][c] = old
        else:
            a, b = rng.randrange(K), rng.randrange(K)
            if a == b or weights[a] == 0:
                continue
            nd = dist
            for i in range(len(PAIRS)):
                d = vecs[b][i] - vecs[a][i]
                if d:
                    nd += abs(cur[i] + d - tvec[i]) - abs(cur[i] - tvec[i])
            if nd <= dist or rng.random() < pow(2.718, -(nd - dist) / T):
                for i in range(len(PAIRS)):
                    cur[i] += vecs[b][i] - vecs[a][i]
                weights[a] -= 1
                weights[b] += 1
                dist = nd
        if dist < best:
            best, state = dist, (list(weights), [dict(t) for t in types])
            if best == 0:
                break
    return best, state


if __name__ == "__main__":
    if "--search" in sys.argv:
        for K in (12, 14, 16, 20):
            for seed in range(6):
                d, (w, t) = search(K, 400000, 1000 * K + seed)
                if d == 0:
                    print(f"EXACT K={K} seed={seed}")
                    for wi, ti in sorted(((wi, ti) for wi, ti in zip(w, t) if wi), key=lambda x: -x[0]):
                        print(f"  ({wi}, {[ti[c] for c in C]}),")
                    sys.exit(0)
            print(f"K={K}: best distance {d}", flush=True)
        sys.exit("no exact reconstruction found")
    verify(BALLOTS)
    paste_block()
