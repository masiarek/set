#!/usr/bin/env python3
"""Verify every numeric claim in ../../math-in-society-lippman.md.

Source: David Lippman, *Math in Society* (LibreTexts), chapters 2-4.
Compiled PDF read 2026-08-01; every table below was taken from the live
LibreTexts HTML, not reconstructed, because the PDF renders them as images.

Run:  python3 verify.py
No dependencies. Every assertion is checked, not printed on trust.
"""

from fractions import Fraction
from itertools import combinations

FAIL = []


def check(label, got, want):
    ok = got == want
    if not ok:
        FAIL.append(label)
    print("  %-58s %s" % (label, "ok" if ok else "FAIL got=%r want=%r" % (got, want)))


def head(t):
    print("\n" + t + "\n" + "-" * len(t))


# ===================================================================== ranked
# A profile is a list of (count, ranking) with ranking best-to-worst.

def first_place(prof, cands):
    return {c: sum(n for n, b in prof if b[0] == c) for c in cands}


def prefer(prof, x, y):
    """(voters preferring x to y, voters preferring y to x)."""
    a = b = 0
    for n, ballot in prof:
        if ballot.index(x) < ballot.index(y):
            a += n
        else:
            b += n
    return a, b


def condorcet(prof, cands):
    for c in cands:
        if all(prefer(prof, c, d)[0] > prefer(prof, c, d)[1]
               for d in cands if d != c):
            return c
    return None


def condorcet_loser(prof, cands):
    for c in cands:
        if all(prefer(prof, c, d)[0] < prefer(prof, c, d)[1]
               for d in cands if d != c):
            return c
    return None


def plurality(prof, cands):
    fp = first_place(prof, cands)
    return max(fp, key=fp.get)


def irv(prof, cands):
    live = list(cands)
    while True:
        fp = first_place([(n, [c for c in b if c in live]) for n, b in prof], live)
        total = sum(fp.values())
        for c in live:
            if fp[c] * 2 > total:
                return c
        if len(live) <= 1:
            return live[0]
        live.remove(min(live, key=lambda c: fp[c]))


# ------------------------------------------------- 2.4 Example 4: city council
# https://math.libretexts.org/@go/page/34179
CITY = [(342, ["Elle", "Don", "Key"]),
        (214, ["Don", "Key", "Elle"]),
        (298, ["Key", "Don", "Elle"])]
CITY_C = ["Don", "Key", "Elle"]

head("2.4 Example 4 -- city council (the Condorcet winner with the FEWEST first places)")

check("total voters = 854", sum(n for n, _ in CITY), 854)

# The three pairwise counts the book prints.
check("Elle vs Don   342 / 512", prefer(CITY, "Elle", "Don"), (342, 512))
check("Elle vs Key   342 / 512", prefer(CITY, "Elle", "Key"), (342, 512))
check("Don  vs Key   556 / 298", prefer(CITY, "Don", "Key"), (556, 298))

check("plurality winner = Elle", plurality(CITY, CITY_C), "Elle")
check("IRV winner = Key", irv(CITY, CITY_C), "Key")
check("Condorcet winner = Don", condorcet(CITY, CITY_C), "Don")

fp = first_place(CITY, CITY_C)
check("first places  Don 214 / Key 298 / Elle 342",
      (fp["Don"], fp["Key"], fp["Elle"]), (214, 298, 342))

# The point: the Condorcet winner has the SMALLEST first-place count in the field.
check("Don has strictly fewest first places",
      fp["Don"] == min(fp.values()) and list(fp.values()).count(min(fp.values())) == 1,
      True)
check("Don's first-place share = 214/854", Fraction(fp["Don"], 854), Fraction(214, 854))
print("      -> %.2f%% first preferences, and beats both rivals head to head"
      % (100 * fp["Don"] / 854))
check("Elle wins plurality on a minority", Fraction(fp["Elle"], 854) < Fraction(1, 2), True)
print("      -> Elle wins with %.2f%%" % (100 * fp["Elle"] / 854))


# --------------------------------------- 2.14 Example 13: approval and majority
# https://math.libretexts.org/@go/page/36257
APPR = [(80, ["A", "B", "C"]),
        (15, ["B", "C", "A"]),
        (5,  ["C", "B", "A"])]
APPR_C = ["A", "B", "C"]

head("2.14 Example 13 -- approval 'fails majority' ONLY under the book's cutoff model")


def approval_top_k(prof, cands, k):
    return {c: sum(n for n, b in prof if c in b[:k]) for c in cands}


def approval_winner(tally):
    return max(tally, key=tally.get)


check("total voters = 100", sum(n for n, _ in APPR), 100)

fpa = first_place(APPR, APPR_C)
check("A holds a strict majority of first places (80/100)",
      fpa["A"] * 2 > 100, True)
check("A is also the Condorcet winner", condorcet(APPR, APPR_C), "A")
check("C is the Condorcet loser", condorcet_loser(APPR, APPR_C), "C")

top2 = approval_top_k(APPR, APPR_C, 2)
check("top-two approval tally A80 B100 C20",
      (top2["A"], top2["B"], top2["C"]), (80, 100, 20))
check("top-two approval elects B (the book's majority failure)",
      approval_winner(top2), "B")

top1 = approval_top_k(APPR, APPR_C, 1)
check("bullet-vote approval tally A80 B15 C5",
      (top1["A"], top1["B"], top1["C"]), (80, 15, 5))
check("bullet-vote approval elects A -- majority criterion SATISFIED",
      approval_winner(top1), "A")

top3 = approval_top_k(APPR, APPR_C, 3)
check("approve-all is a 100-100-100 tie, no winner",
      len(set(top3.values())), 1)

# So on ONE fixed profile of preferences the same tabulation rule passes or fails
# the majority criterion depending only on where voters put the cutoff.
check("same preferences, different cutoff -> different winner",
      approval_winner(top1) != approval_winner(top2), True)


# =================================================================== weighted
def banzhaf(q, w):
    n = len(w)
    crit = [0] * n
    for r in range(1, n + 1):
        for C in combinations(range(n), r):
            if sum(w[i] for i in C) >= q:
                for i in C:
                    if sum(w[j] for j in C if j != i) < q:
                        crit[i] += 1
    tot = sum(crit)
    return crit, [Fraction(c, tot) for c in crit]


# ------------------------------------------------------- 3.4 Example 7: Nassau
# https://math.libretexts.org/@go/page/34186
head("3.4 Example 7 -- Nassau County: weight without power")

NASSAU_W = [31, 31, 28, 21, 2, 2]
NASSAU_N = ["Hempstead#1", "Hempstead#2", "OysterBay",
            "NorthHempstead", "LongBeach", "GlenCove"]
crit, idx = banzhaf(58, NASSAU_W)

check("total weight 115, quota 58 is a simple majority",
      (sum(NASSAU_W), 58 * 2 > sum(NASSAU_W)), (115, True))
check("three large districts critical 16 times each", crit[:3], [16, 16, 16])
check("three small districts critical 0 times each", crit[3:], [0, 0, 0])
check("each large district holds exactly 1/3 of the power",
      idx[:3], [Fraction(1, 3)] * 3)
check("North Hempstead is a dummy despite 21/115 of the weight",
      idx[3], Fraction(0))
print("      -> North Hempstead: %.1f%% of the weight, %.1f%% of the power"
      % (100 * 21 / 115, 0.0))


# --------------------------------------- 3.4 Example 6: the Scottish Parliament
head("3.4 Example 6 -- the Scottish Parliament example drops a sitting MSP")

# The book's system. 2007 election: SNP 47, Lab 46, Con 17, LD 16, Grn 2 ... and
# one independent (Margo MacDonald). The book totals 128; the parliament has 129.
BOOK_W = [47, 46, 17, 16, 2]
REAL_W = [47, 46, 17, 16, 2, 1]

check("book's weights total 128", sum(BOOK_W), 128)
check("actual 2007 parliament totals 129", sum(REAL_W), 129)

_, bi = banzhaf(65, BOOK_W)
_, ri = banzhaf(65, REAL_W)

# The book's punchline: LibDems (16) and Greens (2) have EQUAL power.
check("book: LibDem index == Green index", bi[3] == bi[4], True)
check("book: both are 1/9", (bi[3], bi[4]), (Fraction(1, 9), Fraction(1, 9)))
check("book: SNP 1/3", bi[0], Fraction(1, 3))

# It survives restoring the missing member -- so the omission does not break the
# lesson. But the omitted member is not powerless.
check("with the independent restored, LD == Green still", ri[3] == ri[4], True)
check("with the independent restored, both are 3/28",
      (ri[3], ri[4]), (Fraction(3, 28), Fraction(3, 28)))
check("the omitted independent is NOT a dummy", ri[5] != 0, True)
check("the omitted independent holds 1/28", ri[5], Fraction(1, 28))
print("      -> the dropped MSP carries %.1f%% of the Banzhaf power" % (100 / 28))


# =============================================================== apportionment
def quotas(pops, seats):
    tot = sum(pops)
    return [Fraction(p * seats, tot) for p in pops]


def hamilton(pops, seats):
    q = quotas(pops, seats)
    a = [int(x) for x in q]
    rem = seats - sum(a)
    order = sorted(range(len(pops)), key=lambda i: q[i] - a[i], reverse=True)
    for i in order[:rem]:
        a[i] += 1
    return a


def satisfies_quota(alloc, pops, seats):
    import math
    q = quotas(pops, seats)
    return all(math.floor(q[i]) <= alloc[i] <= math.ceil(q[i])
               for i in range(len(pops)))


head("4.4 Balinski-Young -- the book's version is refuted by Balinski and Young")

# The book's own exercise 9: A 6000, B 6000, C 2000, at 10 then 11 seats.
EX9 = [6000, 6000, 2000]

h10 = hamilton(EX9, 10)
h11 = hamilton(EX9, 11)
check("Hamilton at 10 seats = (4,4,2)", h10, [4, 4, 2])
check("Hamilton at 11 seats = (5,5,1)", h11, [5, 5, 1])
check("C LOSES a seat when the house grows -- Alabama paradox",
      h11[2] < h10[2], True)
check("Hamilton satisfied quota at both sizes",
      (satisfies_quota(h10, EX9, 10), satisfies_quota(h11, EX9, 11)), (True, True))

# Now the refutation. The book says a method that always follows the quota rule
# "will be subject to" paradoxes like Alabama. If that were so, then on THIS
# instance no house-monotone chain of quota-satisfying allocations could exist.
# Search exhaustively for one.


def quota_allocs(pops, seats):
    """Every allocation of `seats` that satisfies the quota rule."""
    import math
    q = quotas(pops, seats)
    lo = [math.floor(x) for x in q]
    hi = [math.ceil(x) for x in q]
    out = []

    def rec(i, acc, left):
        if i == len(pops):
            if left == 0:
                out.append(tuple(acc))
            return
        for v in range(lo[i], hi[i] + 1):
            if 0 <= left - v:
                rec(i + 1, acc + [v], left - v)
    rec(0, [], seats)
    return out


def monotone_chain_exists(pops, max_seats):
    """Is there a quota-satisfying allocation for every house size 1..max_seats
    that never takes a seat away as the house grows?"""
    reach = set(quota_allocs(pops, 1))
    for h in range(2, max_seats + 1):
        nxt = quota_allocs(pops, h)
        reach = {a for a in nxt
                 if any(all(a[i] >= p[i] for i in range(len(pops))) for p in reach)}
        if not reach:
            return False, h
    return True, None


ok, stuck = monotone_chain_exists(EX9, 11)
check("a quota-satisfying, house-monotone chain EXISTS for house sizes 1..11",
      (ok, stuck), (True, None))

# Concretely, the step the book's claim says cannot be arranged:
check("(4,4,2) at h=10 satisfies quota", satisfies_quota([4, 4, 2], EX9, 10), True)
check("(5,4,2) at h=11 satisfies quota", satisfies_quota([5, 4, 2], EX9, 11), True)
check("(4,4,2) -> (5,4,2) takes nothing away from anyone",
      all([5, 4, 2][i] >= [4, 4, 2][i] for i in range(3)), True)

# And it is not a quirk of this instance.
import random
random.seed(20260801)
bad = 0
for _ in range(300):
    k = random.randint(3, 5)
    pops = [random.randint(1, 400) for _ in range(k)]
    ok, _ = monotone_chain_exists(pops, 12)
    if not ok:
        bad += 1
check("over 300 random instances, a quota+house-monotone chain always exists",
      bad, 0)

print("""
      So: quota + house monotonicity (no Alabama paradox) is achievable.
      Balinski and Young built such a method themselves -- the Quota method,
      Amer. Math. Monthly 82 (1975) -- and Still, Math. of OR 4 (1979),
      characterises the whole class. The real impossibility is
      quota + POPULATION monotonicity, which is not what the book says.""")


# ---------------------------------------------------------------------- report
print("\n" + "=" * 70)
if FAIL:
    print("FAILURES: %d" % len(FAIL))
    for f in FAIL:
        print("  -", f)
    raise SystemExit(1)
print("all checks passed")
