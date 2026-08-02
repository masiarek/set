"""Adversarial verification of the ranked_robin patch to votesim.

Reference implementation written independently (pure loops, no votesim
helpers), compared against the patched method over randomized ballots.
Conventions matched to votesim's honest sim ballots: strict rankings
1..b, possibly truncated with 0 = unranked = below every ranked candidate
(and tied with other unranked candidates -- contributing no vote either way).
"""
import numpy as np
from votesim.votemethods.condorcet import ranked_robin, copeland
from votesim.votemethods.condcalcs import pairwise_rank_matrix

rng = np.random.default_rng(20260801)


def ref_matrix(ranks):
    ranks = np.asarray(ranks)
    n = ranks.shape[1]
    M = np.zeros((n, n), dtype=int)
    for ballot in ranks:
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                ri, rj = ballot[i], ballot[j]
                if ri != 0 and (rj == 0 or ri < rj):
                    M[i, j] += 1
    return M


def ref_ranked_robin(ranks):
    """Returns (winner_set, tie_degree). winner_set is the set of candidates
    that survive all deterministic stages (len>1 => unresolved tie)."""
    M = ref_matrix(ranks)
    n = M.shape[0]
    margins = M - M.T
    cope = [sum(1 for j in range(n) if margins[i][j] > 0)
            - sum(1 for j in range(n) if margins[i][j] < 0) for i in range(n)]
    best = max(cope)
    finalists = [i for i in range(n) if cope[i] == best]
    if len(finalists) == 1:
        return set(finalists), 0
    # 1st degree: margins among finalists
    t1 = {i: sum(margins[i][j] for j in finalists if j != i) for i in finalists}
    m1 = max(t1.values())
    s1 = [i for i in finalists if t1[i] == m1]
    if len(s1) == 1:
        return set(s1), 1
    # 2nd degree: margins vs all
    t2 = {i: sum(margins[i][j] for j in range(n) if j != i) for i in s1}
    m2 = max(t2.values())
    s2 = [i for i in s1 if t2[i] == m2]
    return set(s2), (2 if len(s2) == 1 else 3)


def run_patched(ranks):
    w, t, out = ranked_robin(np.asarray(ranks))
    if len(w) == 1:
        return {int(w[0])}, out['tie_degree']
    return set(int(x) for x in t), out['tie_degree']


fails = 0

# --- 1. Hand-built: classic 3-cycle, margins must decide (1st degree) ---
# 35 A>B>C, 33 B>C>A, 32 C>A>B  -> cycle A>B (67-33), B>C (68-32), C>A (65-35)
ballots = ([[1, 2, 3]] * 35) + ([[3, 1, 2]] * 33) + ([[2, 3, 1]] * 32)
ws, deg = run_patched(ballots)
# margins: A: +34 (vs B) -30 (vs C) = +4 ; B: -34+36 = +2 ; C: +30-36 = -6
assert ws == {0} and deg == 1, (ws, deg)
rs, rdeg = ref_ranked_robin(ballots)
assert rs == ws and rdeg == deg

# --- 2. Hand-built: Condorcet winner present -> degree 0, agrees with copeland ---
ballots = ([[1, 2, 3]] * 40) + ([[2, 1, 3]] * 35) + ([[3, 2, 1]] * 25)
ws, deg = run_patched(ballots)
assert deg == 0 and ws == {0} or ws == {1}
wc, tc, _ = copeland(np.asarray(ballots))
assert set(wc) == ws

# --- 3. Hand-built: perfectly symmetric cycle -> unresolved (degree 3) ---
ballots = ([[1, 2, 3]] * 10) + ([[3, 1, 2]] * 10) + ([[2, 3, 1]] * 10)
ws, deg = run_patched(ballots)
assert deg == 3 and ws == {0, 1, 2}, (ws, deg)

# --- 4. Fuzz: strict + truncated ballots, small fields (ties common) ---
n_iter = 20000
degree_counts = {0: 0, 1: 0, 2: 0, 3: 0}
for it in range(n_iter):
    nv = int(rng.integers(3, 26))
    nc = int(rng.integers(3, 7))
    ranks = np.zeros((nv, nc), dtype=int)
    for v in range(nv):
        perm = rng.permutation(nc) + 1
        ranks[v] = perm
        if rng.random() < 0.4:  # truncate: keep top k
            k = int(rng.integers(1, nc))
            ranks[v][ranks[v] > k] = 0
    ws, deg = run_patched(ranks)
    rs, rdeg = ref_ranked_robin(ranks)
    degree_counts[deg] += 1
    if ws != rs or deg != rdeg:
        fails += 1
        if fails <= 5:
            print('MISMATCH at iter', it, 'patched:', ws, deg, 'ref:', rs, rdeg)
            print(ranks.tolist())

# --- 5. Fuzz invariants on the patched implementation ---
for it in range(2000):
    nv = int(rng.integers(3, 40))
    nc = int(rng.integers(3, 8))
    ranks = np.array([rng.permutation(nc) + 1 for _ in range(nv)])
    w, t, out = ranked_robin(ranks)
    # library matrix must match the independent one on strict ballots
    assert np.array_equal(pairwise_rank_matrix(ranks), ref_matrix(ranks))
    if out['tie_degree'] >= 1:
        # zero-sum invariant: finalist margins among finalists sum to 0
        assert out['finalist_tally'].sum() == 0, out
        # winner (if any) must be a finalist
        if len(w):
            assert w[0] in out['finalists']

print('fuzz iterations:', n_iter, ' mismatches:', fails)
print('tie degree distribution over fuzz runs:', degree_counts)
print('ALL OK' if fails == 0 else 'FAILURES PRESENT')
