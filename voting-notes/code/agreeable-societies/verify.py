#!/usr/bin/env python3
"""Verify every claim in ../../agreeable-societies.md.

Two sources, one model.  Berg, Norine, Su, Thomas & Wollan, "Voting in
agreeable societies" (Amer. Math. Monthly 117 (2010) 27-39, arXiv:0811.3245)
model each voter's APPROVAL SET as a closed interval on a political spectrum
and ask how much GLOBAL agreement is forced by a LOCAL condition.  Burkhart's
2012 Harvey Mudd senior thesis adds a second, half-weight "maybe" level to the
same picture.

Nothing here is about who wins an election: the objects are approval sets and
platforms, and every quantity below is an agreement count.

Run:  python3 verify.py
No dependencies. Every assertion below is checked, not printed on trust.
"""

import itertools
import math
import random
from fractions import Fraction as F

# ====================================================================
# Part 1 -- linear societies (Berg et al.)
# A society is a list of closed intervals (a, b) on a spectrum.
# ====================================================================


def agreement_number(ivals):
    """a(S) = max over platforms p of the number of approval sets containing p.

    For closed intervals the maximum is attained at some left endpoint, so
    scanning left endpoints is exact, not a sample.
    """
    if not ivals:
        return 0
    return max(sum(1 for (a, b) in ivals if a <= p <= b) for (p, _) in ivals)


def is_km_agreeable(ivals, k, m):
    """Every m voters contain k with a common platform (brute force)."""
    if len(ivals) < m:
        return False
    return all(agreement_number(list(s)) >= k
               for s in itertools.combinations(ivals, m))


def best_k_for(ivals, m):
    """Largest k such that the society is (k, m)-agreeable."""
    if len(ivals) < m:
        return 0
    return min(agreement_number(list(s))
               for s in itertools.combinations(ivals, m))


def agreement_graph(ivals):
    """Vertices = voters, edges = pairs whose approval sets intersect."""
    n = len(ivals)
    adj = [set() for _ in range(n)]
    for i, j in itertools.combinations(range(n), 2):
        (a, b), (c, d) = ivals[i], ivals[j]
        if a <= d and c <= b:
            adj[i].add(j)
            adj[j].add(i)
    return adj


def max_clique(adj):
    """Bron-Kerbosch with pivoting. Independent of any interval structure."""
    best = 0

    def bk(r, p, x):
        nonlocal best
        if not p and not x:
            best = max(best, len(r))
            return
        if len(r) + len(p) <= best:
            return
        pivot = max(p | x, key=lambda u: len(adj[u] & p))
        for v in list(p - adj[pivot]):
            bk(r | {v}, p & adj[v], x & adj[v])
            p = p - {v}
            x = x | {v}

    bk(set(), set(range(len(adj))), set())
    return best


def chromatic_number(adj):
    """Exact, by backtracking. Small graphs only."""
    n = len(adj)
    if n == 0:
        return 0

    def colorable(c):
        color = [-1] * n

        def go(v):
            if v == n:
                return True
            for col in range(c):
                if all(color[u] != col for u in adj[v] if u < v):
                    color[v] = col
                    if go(v + 1):
                        return True
                    color[v] = -1
            return False

        return go(0)

    for c in range(1, n + 1):
        if colorable(c):
            return c
    return n


def random_society(rng, n, span=30, width=10):
    return [(lambda a: (a, a + rng.randint(0, width)))(rng.randint(0, span))
            for _ in range(n)]


# ====================================================================
# Part 2 -- two-level societies (Burkhart)
# A voter is (L, l, r, R) with L < l < r < R.
#   approval region A = [l, r]      value 1
#   maybe region    M = [L,l) u (r,R]   value 1/2
#   interest region I = [L, R]
# ====================================================================


def value(voter, p):
    L, l, r, R = voter
    if l <= p <= r:
        return F(1)
    if L <= p < l or r < p <= R:
        return F(1, 2)
    return F(0)


def platforms(voters):
    """Every point where the step function V can change, plus midpoints.

    Coordinates are integers throughout, so sampling the integers and the
    half-integers in range is exact for these piecewise-constant functions.
    """
    pts = sorted({c for v in voters for c in v})
    out = []
    for i, p in enumerate(pts):
        out.append(F(p))
        if i + 1 < len(pts):
            out.append(F(2 * p + 1, 2))
    return out


def total_value(voters, p):
    return sum(value(v, p) for v in voters)


def two_level_intersect(u, v):
    """Definition 3.1: I_u meets A_v, or I_v meets A_u."""
    def meets(x, y):
        return x[0] <= y[1] and y[0] <= x[1]
    Iu, Au = (u[0], u[3]), (u[1], u[2])
    Iv, Av = (v[0], v[3]), (v[1], v[2])
    return meets(Iu, Av) or meets(Iv, Au)


def alpha_beta(voters):
    n = len(voters)
    e = sum(1 for u, v in itertools.combinations(voters, 2)
            if two_level_intersect(u, v))
    alpha = F(e, math.comb(n, 2))
    beta = max(total_value(voters, p) for p in platforms(voters)) / n
    return alpha, beta


def random_two_level(rng, n, span=40):
    out = []
    for _ in range(n):
        pts = sorted(rng.sample(range(span), 4))
        out.append(tuple(pts))
    return out


# ====================================================================


def main():
    ok = []

    # ---------------------------------------------------------------
    # 1. Fact 2 + Fact 1: the agreement graph of a linear society is an
    #    interval graph, and its clique number IS the agreement number.
    # ---------------------------------------------------------------
    rng = random.Random(20081120)
    checked = 0
    for _ in range(4000):
        s = random_society(rng, rng.randint(2, 9))
        if max_clique(agreement_graph(s)) != agreement_number(s):
            raise AssertionError(f"Fact 1 failed on {s}")
        checked += 1
    ok.append(f"Fact 1 (clique number = agreement number) holds on all "
              f"{checked} random linear societies, max-clique computed "
              f"independently by Bron-Kerbosch")

    # ---------------------------------------------------------------
    # 2. Theorem 5: a super-agreeable ((2,2)-agreeable) linear society has a
    #    platform approved by EVERY voter.
    # ---------------------------------------------------------------
    found = 0
    for _ in range(200000):
        s = random_society(rng, rng.randint(2, 7), span=12, width=8)
        if not is_km_agreeable(s, 2, 2):
            continue
        found += 1
        assert agreement_number(s) == len(s), s
        if found >= 3000:
            break
    ok.append(f"Theorem 5 (Super-Agreeable Linear Society): all {found} "
              f"pairwise-agreeing societies found have a platform approved "
              f"by every voter")

    # ---------------------------------------------------------------
    # 3. Theorem 1: an agreeable ((2,3)-agreeable) society has a platform
    #    approved by at least half the voters.  And the "half" is not
    #    slack -- societies that hit it exactly exist.
    # ---------------------------------------------------------------
    found = tight = 0
    for _ in range(200000):
        s = random_society(rng, rng.randint(3, 8), span=14, width=6)
        if not is_km_agreeable(s, 2, 3):
            continue
        found += 1
        n = len(s)
        assert agreement_number(s) >= n / 2, s
        if agreement_number(s) == math.ceil(n / 2) and n % 2 == 0:
            tight += 1
        if found >= 3000:
            break
    ok.append(f"Theorem 1: all {found} agreeable societies have a platform "
              f"approved by >= half the voters; {tight} of them meet the "
              f"bound exactly, so 'half' cannot be improved")

    # ---------------------------------------------------------------
    # 4. Theorem 2 and Theorem 8 on the same random societies, and the
    #    claim in the proof that Theorem 8 is the stronger of the two.
    # ---------------------------------------------------------------
    tested = t8_strict = 0
    for _ in range(3000):
        s = random_society(rng, rng.randint(4, 8), span=16, width=7)
        n = len(s)
        a = agreement_number(s)
        for m in range(3, n + 1):
            k = best_k_for(s, m)
            if k < 2:
                continue
            q, rho = divmod(m - 1, k - 1)
            assert 0 <= rho <= k - 2 or k == 2, (k, m, q, rho)
            t2 = F(n * (k - 1), m - 1)
            t8 = math.ceil((n - rho) / q)
            assert a >= t2, (s, k, m, a, t2)          # Theorem 2
            assert a >= t8, (s, k, m, a, t8)          # Theorem 8
            assert t8 >= t2, (k, m, n, t8, t2)        # Thm 8 dominates Thm 2
            tested += 1
            t8_strict += t8 > t2
    ok.append(f"Theorems 2 and 8 hold on all {tested} (society, k, m) cases; "
              f"Theorem 8's ceil((n-rho)/q) is strictly stronger than "
              f"n(k-1)/(m-1) in {100 * t8_strict / tested:.0f}% of them")

    # ---------------------------------------------------------------
    # 5. Theorem 8 is best possible: the construction from its proof.
    #    Their Figure 7 is (k,m) = (4,15), n = 21, q = 4, rho = 2.
    # ---------------------------------------------------------------
    def construction(k, m, n):
        """q disjoint intervals cycled n-rho times, then rho isolated ones."""
        q, rho = divmod(m - 1, k - 1)
        ivals, classes = [], []
        for i in range(n - rho):
            j = i % q
            ivals.append((10 * j, 10 * j + 1))
            classes.append(j)
        for t in range(rho):
            ivals.append((10 * q + 10 * t, 10 * q + 10 * t + 1))
            classes.append(q + t)
        return ivals, q, rho

    # 5a. honest brute force on a small instance, chosen so that rho > 0
    ivals, q, rho = construction(3, 6, 9)
    assert (q, rho) == (2, 1), (q, rho)
    assert is_km_agreeable(ivals, 3, 6), ivals
    assert max_clique(agreement_graph(ivals)) == math.ceil((9 - rho) / q) == 4
    ok.append(f"Theorem 8 tightness, brute forced over all C(9,6)=84 subsets: "
              f"the (3,6) construction on n=9 is (3,6)-agreeable with clique "
              f"number exactly ceil((9-{rho})/{q}) = 4")

    # 5b. Figure 7 itself: C(21,15) = 54264 subsets is slow, but intervals in
    #     one class are interchangeable, so enumerating class-count vectors is
    #     exhaustive rather than a sample.  Cross-checked against 5a's brute
    #     force below.
    def km_agreeable_by_classes(sizes, k, m):
        worst = None
        ranges = [range(0, s + 1) for s in sizes]
        for counts in itertools.product(*ranges):
            if sum(counts) != m:
                continue
            worst = max(counts) if worst is None else min(worst, max(counts))
        return worst is not None and worst >= k

    def class_sizes(k, m, n):
        _, q, rho = construction(k, m, n)
        sizes = [0] * (q + rho)
        for i in range(n - rho):
            sizes[i % q] += 1
        for t in range(rho):
            sizes[q + t] = 1
        return sizes, q, rho

    sizes, q, rho = class_sizes(3, 6, 9)
    assert km_agreeable_by_classes(sizes, 3, 6)          # agrees with 5a
    sizes, q, rho = class_sizes(4, 15, 21)
    assert (q, rho) == (4, 2), (q, rho)
    assert km_agreeable_by_classes(sizes, 4, 15), sizes
    fig7 = math.ceil((21 - rho) / q)
    ivals, _, _ = construction(4, 15, 21)
    assert max_clique(agreement_graph(ivals)) == fig7 == 5
    ok.append(f"their Figure 7 reproduced: a (4,15)-agreeable society on n=21 "
              f"with q=4, rho=2 and clique number exactly {fig7}")

    # ---------------------------------------------------------------
    # 6. The restaurant example: 14 restaurants on a boulevard, everyone eats
    #    at the 5 nearest.  Both halves of their argument.
    # ---------------------------------------------------------------
    windows = [(i, i + 4) for i in range(10)]            # 5 consecutive of 14
    assert all(b < 14 for _, b in windows)
    # (a) pigeonhole: 3 residents x 5 restaurants > 14 restaurants
    assert 3 * 5 > 14
    # (b) directly: every 3 windows contain an intersecting pair
    assert is_km_agreeable(windows, 2, 3)
    worst = min(agreement_number([windows[i] for i in c])
                for c in itertools.combinations_with_replacement(range(10), 7))
    assert worst >= math.ceil(7 / 2), worst
    lo = 2.0
    for _ in range(20000):
        n = rng.randint(3, 12)
        s = [windows[rng.randrange(10)] for _ in range(n)]
        assert is_km_agreeable(s, 2, 3), s
        lo = min(lo, agreement_number(s) / n)
    ok.append(f"restaurant example: the 10 five-restaurant windows are "
              f"(2,3)-agreeable, and over 20000 random resident groups the "
              f"lowest share ever sharing one restaurant was {lo:.2f}")

    # ---------------------------------------------------------------
    # 7. Their Figure 2 -> Figure 3 point: restricting the spectrum from all
    #    of R to the actual CANDIDATES can destroy agreeability.
    # ---------------------------------------------------------------
    def restricted_best_k(s, cands, m):
        sets = [frozenset(c for c in cands if a <= c <= b) for (a, b) in s]
        worst = m
        for sub in itertools.combinations(sets, m):
            best = max((sum(1 for t in sub if c in t) for c in cands),
                       default=0)
            worst = min(worst, best)
        return worst

    example = None
    for _ in range(200000):
        s = random_society(rng, 6, span=20, width=7)
        if not is_km_agreeable(s, 2, 3):
            continue
        cands = sorted(rng.sample(range(21), 3))
        if restricted_best_k(s, cands, 3) < 2:
            m = 4
            while m <= 6 and restricted_best_k(s, cands, m) < 2:
                m += 1
            example = (s, cands, m)
            break
    assert example is not None
    s, cands, m = example
    ok.append(f"restricting the spectrum breaks agreeability, as in their "
              f"Figures 2-3: the society {s} is (2,3)-agreeable on R, but "
              f"with candidates only at {cands} it is not -- the best it "
              f"manages is (2,{m})")

    # ---------------------------------------------------------------
    # 8. Fact 1 fails in R^2: three convex sets, pairwise agreement, no
    #    common platform.  Three segments forming a triangle.
    # ---------------------------------------------------------------
    tri = [((0, 0), (4, 0)), ((4, 0), (2, 4)), ((2, 4), (0, 0))]
    meets = [(4, 0), (2, 4), (0, 0)]        # s0&s1, s1&s2, s0&s2
    for (i, j), p in zip([(0, 1), (1, 2), (0, 2)], meets):
        for si in (tri[i], tri[j]):
            (x1, y1), (x2, y2) = si
            cross = (x2 - x1) * (p[1] - y1) - (y2 - y1) * (p[0] - x1)
            assert cross == 0 and min(x1, x2) <= p[0] <= max(x1, x2)
    assert len(set(meets)) == 3             # three distinct points => no common one
    ok.append("Fact 1 fails for R^2-convex societies: three segments meeting "
              "pairwise at three distinct points, so the agreement graph is a "
              "triangle while the agreement number is 2")

    # ---------------------------------------------------------------
    # 9. Their Figure 8: a 2-box society whose agreement graph is a 5-cycle,
    #    so agreement graphs of box societies are not perfect.
    # ---------------------------------------------------------------
    boxes = [((0, 1), (0, 3)),      # v1
             ((1, 2), (3, 5)),      # v2
             ((2, 3), (4, 6)),      # v3
             ((3, 4), (1, 6)),      # v4
             ((0, 4), (0, 1))]      # v5

    def box_adj(bs):
        n = len(bs)
        adj = [set() for _ in range(n)]
        for i, j in itertools.combinations(range(n), 2):
            (xi, yi), (xj, yj) = bs[i], bs[j]
            if xi[0] <= xj[1] and xj[0] <= xi[1] and \
               yi[0] <= yj[1] and yj[0] <= yi[1]:
                adj[i].add(j)
                adj[j].add(i)
        return adj

    adj = box_adj(boxes)
    c5 = {0: {1, 4}, 1: {0, 2}, 2: {1, 3}, 3: {2, 4}, 4: {3, 0}}
    assert all(adj[i] == c5[i] for i in range(5)), adj
    assert max_clique(adj) == 2 and chromatic_number(adj) == 3
    # Fact 1 still holds for boxes (projection onto each axis + Theorem 5)
    corners = [(bx[0], by[0]) for (bx, by) in boxes]
    agree = max(sum(1 for (bx, by) in boxes
                    if bx[0] <= p <= bx[1] and by[0] <= qq <= by[1])
                for (p, qq) in corners)
    assert agree == 2 == max_clique(adj)
    ok.append("Figure 8 reconstructed: 5 axis-parallel boxes whose agreement "
              "graph is exactly C5 -- clique number 2 but chromatic number 3, "
              "so box agreement graphs are not perfect (while Fact 1 survives)")

    # ---------------------------------------------------------------
    # 10. Theorem 11, exhaustively, on every graph on 6 vertices; and the
    #     necessity of the hypothesis m <= 2k-2.
    # ---------------------------------------------------------------
    def every_m_has_k_clique(adj, k, m):
        n = len(adj)
        for sub in itertools.combinations(range(n), m):
            sadj = [adj[v] & set(sub) for v in range(n)]
            best = 0
            for c in itertools.combinations(sub, k):
                if all(y in sadj[x] for x, y in itertools.combinations(c, 2)):
                    best = k
                    break
            if best < k:
                return False
        return True

    n, k, m = 6, 3, 4                       # k <= m <= 2k-2 = 4
    pairs = list(itertools.combinations(range(n), 2))
    hits = 0
    for mask in range(1 << len(pairs)):
        adj = [set() for _ in range(n)]
        for b, (i, j) in enumerate(pairs):
            if mask >> b & 1:
                adj[i].add(j)
                adj[j].add(i)
        if every_m_has_k_clique(adj, k, m):
            hits += 1
            assert max_clique(adj) >= n - m + k, mask
    assert hits > 0
    ok.append(f"Theorem 11 verified exhaustively: all {hits} graphs on 6 "
              f"vertices in which every 4 vertices contain a triangle have "
              f"clique number >= n-m+k = {n - m + k} (all 2^15 graphs tested)")

    # tightness, and why m <= 2k-2 is needed
    n, k, m = 6, 3, 4
    adj = [set() for _ in range(n)]
    for i, j in itertools.combinations(range(n - m + k), 2):
        adj[i].add(j)
        adj[j].add(i)                        # clique of n-m+k, rest isolated
    assert every_m_has_k_clique(adj, k, m) and max_clique(adj) == n - m + k
    n, k, m = 6, 3, 5                        # m = 2k-1, outside the range
    adj = [set() for _ in range(n)]
    for grp in ([0, 1, 2], [3, 4, 5]):
        for i, j in itertools.combinations(grp, 2):
            adj[i].add(j)
            adj[j].add(i)
    assert every_m_has_k_clique(adj, k, m) and max_clique(adj) == 3 < n - m + k
    ok.append("and the hypothesis m <= 2k-2 is not decoration: two disjoint "
              "triangles satisfy the (3,5) hypothesis with clique number 3 < "
              "n-m+k = 4")

    # ---------------------------------------------------------------
    # 11. Theorem 10 (R^d-convex) is weaker than Theorem 8 at d = 1, as the
    #     paper says.
    # ---------------------------------------------------------------
    worst = None
    for k in range(2, 13):
        for m in range(k, 13):
            t10 = 1 - (1 - math.comb(k, 2) / math.comb(m, 2)) ** 0.5
            t8 = (k - 1) / (m - 1)
            assert t10 <= t8 + 1e-12, (k, m, t10, t8)
            gap = t8 - t10
            if worst is None or gap > worst[0]:
                worst = (gap, k, m, t10, t8)
    ok.append(f"Theorem 10 at d=1 never beats Theorem 8 over 2<=k<=m<=12; "
              f"worst case (k,m)=({worst[1]},{worst[2]}) gives "
              f"{worst[3]:.3f} against {worst[4]:.3f}")

    # ---------------------------------------------------------------
    # 12. How low can a (2,3)-agreeable 2-box society go?  The paper reports
    #     3/8 (Hegde, private communication) with no construction.  Random
    #     search, reported honestly.
    # ---------------------------------------------------------------
    def independence_number(adj):
        n = len(adj)
        comp = [set(range(n)) - adj[v] - {v} for v in range(n)]
        return max_clique(comp)

    # What a 3/8 example must look like: 8 voters, (2,3)-agreeable means no
    # independent set of size 3, and agreement number 3 means no clique of
    # size 4.  That is exactly a Ramsey(3,4) graph on 8 vertices, and the
    # Wagner graph V8 (C8 plus its four main diagonals) is one.
    wag = [set() for _ in range(8)]
    for i in range(8):
        for j in ((i + 1) % 8, (i + 4) % 8):
            wag[i].add(j)
            wag[j].add(i)
    comp_wag = [set(range(8)) - wag[v] - {v} for v in range(8)]
    assert max_clique(wag) == 2 and independence_number(wag) == 3
    assert max_clique(comp_wag) == 3 and independence_number(comp_wag) == 2

    best = None
    for _ in range(120000):
        nb = 8
        bs = []
        for _ in range(nb):
            x = sorted(rng.sample(range(12), 2))
            y = sorted(rng.sample(range(12), 2))
            bs.append((tuple(x), tuple(y)))
        a2 = box_adj(bs)
        if independence_number(a2) >= 3:      # not (2,3)-agreeable
            continue
        prop = F(max_clique(a2), nb)          # = agreement proportion, Fact 1
        if best is None or prop < best:
            best = prop
    ok.append(f"a (2,3)-agreeable 8-voter society with agreement proportion "
              f"3/8 needs a Ramsey(3,4) agreement graph -- the Wagner graph's "
              f"complement is one (clique 3, independence 2, both checked). "
              f"Whether boxes can realise it is another matter: 120000 random "
              f"2-box societies never got below {best}, so their reported 3/8 "
              f"(Hegde, private communication) stands unreproduced here")

    # ---------------------------------------------------------------
    # 13. Abbott-Katchalski as Burkhart states it: beta >= 1 - sqrt(1-alpha)
    #     for interval graphs.  Tested against Berg's Theorem 8 on the same
    #     societies -- neither implies the other.
    # ---------------------------------------------------------------
    ak_wins = berg_wins = both = 0
    for _ in range(4000):
        s = random_society(rng, rng.randint(4, 8), span=16, width=7)
        n = len(s)
        e = sum(1 for u, v in itertools.combinations(range(n), 2)
                if u in agreement_graph(s)[v])
        alpha = e / math.comb(n, 2)
        beta = agreement_number(s) / n
        assert beta >= 1 - math.sqrt(1 - alpha) - 1e-12, (s, alpha, beta)
        ak = n * (1 - math.sqrt(1 - alpha))
        best_berg = 0
        for m in range(3, n + 1):
            k = best_k_for(s, m)
            if k < 2:
                continue
            q, rho = divmod(m - 1, k - 1)
            best_berg = max(best_berg, math.ceil((n - rho) / q))
        if ak > best_berg + 1e-9:
            ak_wins += 1
        elif best_berg > ak + 1e-9:
            berg_wins += 1
        else:
            both += 1
    ok.append(f"Abbott-Katchalski (beta >= 1-sqrt(1-alpha)) holds on all 4000 "
              f"random linear societies -- but never usefully: against Berg's "
              f"Theorem 8 on the same societies it is stronger {ak_wins} "
              f"times, weaker {berg_wins}, equal {both}. Theorem 8 is given "
              f"more input (the whole agreeability profile, not just edge "
              f"density), so this is a comparison of what each bound is "
              f"handed, not a defect in Abbott-Katchalski")

    # ---------------------------------------------------------------
    # 14. Burkhart Theorem 3.1: pairwise agreement puts a platform in every
    #     INTEREST region and at least one APPROVAL region -- and one is all
    #     you get.
    # ---------------------------------------------------------------
    rng2 = random.Random(2012)
    found = 0
    for _ in range(400000):
        vs = random_two_level(rng2, rng2.randint(2, 5), span=14)
        if not all(two_level_intersect(u, v)
                   for u, v in itertools.combinations(vs, 2)):
            continue
        found += 1
        good = [p for p in platforms(vs)
                if all(value(v, p) >= F(1, 2) for v in vs)
                and any(value(v, p) == 1 for v in vs)]
        assert good, vs
        if found >= 3000:
            break
    ok.append(f"Burkhart Theorem 3.1 holds on all {found} pairwise-agreeing "
              f"two-level societies: a platform in every interest region and "
              f"at least one approval region")

    nested = [(0, 10 * i, 10 * i + 1, 1000) for i in range(1, 7)]
    assert all(two_level_intersect(u, v)
               for u, v in itertools.combinations(nested, 2))
    assert max(sum(1 for v in nested if value(v, p) == 1)
               for p in platforms(nested)) == 1
    ok.append("and 'at least one' cannot be raised to two: 6 voters with "
              "disjoint approval regions inside each other's maybe regions "
              "agree pairwise, yet no platform is approved outright by two")

    # ---------------------------------------------------------------
    # 15. Burkhart's own worked example (his section 4.2) and his two bounds
    #     on random two-level societies.
    # ---------------------------------------------------------------
    a_ex, b_ex = F(7, 10), F(1, 2)
    assert b_ex >= (1 - math.sqrt(1 - a_ex)) / 2
    assert math.comb(5, 2) * a_ex == 7
    assert F(5) * b_ex * (F(5) * b_ex - 1) / 2 == F(15, 8)
    assert 7 >= F(15, 8)
    ok.append("his section 4.2 example checks out: N=5, alpha=7/10, beta=1/2, "
              "lower bound 0.226 and upper bound 7 >= 15/8")

    slack = []
    for _ in range(3000):
        vs = random_two_level(rng2, rng2.randint(3, 7), span=30)
        n = len(vs)
        alpha, beta = alpha_beta(vs)
        lo = (1 - math.sqrt(1 - float(alpha))) / 2
        assert float(beta) >= lo - 1e-12, (vs, alpha, beta)
        nb = float(n) * float(beta)
        assert math.comb(n, 2) * float(alpha) >= nb * (nb - 1) / 2 - 1e-9
        slack.append(float(beta) - lo)
    ok.append(f"his Theorems 4.1 and 4.2 hold on 3000 random two-level "
              f"societies, but 4.1 is loose: beta exceeds the lower bound by "
              f"{sum(slack) / len(slack):.2f} on average (the bound throws "
              f"away a factor of 2)")

    # ---------------------------------------------------------------
    # 16. Burkhart Theorem 5.1: equal approval regions, maybe regions mu
    #     times as long, everyone agrees pairwise => a platform in
    #     ceil(N/(1+mu)) approval regions, and the column construction shows
    #     that is exact.
    # ---------------------------------------------------------------
    for mu in (1, 2, 3, 4):
        for N in (5, 7, 9, 12, 13):
            cols = 1 + mu
            step = F(mu + 1, mu)             # widest spacing still agreeing
            vs = []
            for i in range(N):
                left = step * (i % cols)
                vs.append((left - mu, left, left + 1, left + 1 + mu))
            assert all(two_level_intersect(u, v)
                       for u, v in itertools.combinations(vs, 2)), (mu, N)
            pts = sorted({c for v in vs for c in v})
            top = max(sum(1 for v in vs if v[1] <= p <= v[2]) for p in pts)
            assert top == math.ceil(N / (1 + mu)), (mu, N, top)
    ok.append("his Theorem 5.1 is exact on the column construction: for mu in "
              "1..4 and N in {5,7,9,12,13} the most-approved platform lands in "
              "exactly ceil(N/(1+mu)) approval regions")

    print("all checks passed\n")
    for line in ok:
        print("  + " + line)


if __name__ == "__main__":
    main()
