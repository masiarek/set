#!/usr/bin/env python3
"""
Verifier for ../../brandl-peters-approval-characterizations.md

Checks what is checkable in Brandl & Peters, "Approval Voting under Dichotomous
Preferences: A Catalogue of Characterizations", Journal of Economic Theory 205
(2022), 105532.

WHAT BRUTE FORCE CAN AND CANNOT DO HERE
---------------------------------------
An axiom is a statement quantified over *all* profiles. So:

  * A FAILURE is a finite witness. When this script reports that a rule fails an
    axiom it prints the profile, and that result is exact.
  * A SATISFACTION is not. "No counterexample among profiles with <= N voters on
    <= 4 alternatives" is what we actually establish, and that is what gets
    printed. It is a spot-check of the paper, not a proof of it.
  * CONTINUITY is doubly bounded: it is an existential over k ("for some k"), so
    a *failure* means "no k <= KMAX worked". Both directions are windowed.

The characterization theorems themselves (uniqueness over the space of all
ballot aggregation functions) are not brute-forceable at all and are not
attempted. What IS mechanically checkable is the paper's Table 1: for each
theorem and each axiom in it, Appendix B names an example rule that satisfies
the theorem's *other* axioms and fails this one. That is a finite claim about
17 concrete rules, and it is the bulk of what runs below.

Run: python3 verify.py
"""

from fractions import Fraction
from itertools import combinations, permutations
import sys

# --------------------------------------------------------------------------
# Model (Section 2 of the paper)
#
# Alternatives are single characters. A ballot is a non-empty frozenset of
# alternatives -- identical to a dichotomous preference, per the paper's
# one-to-one correspondence. A profile is a dict {ballot: count} with a
# positive total; note this makes every rule anonymous by construction, which
# is why Example 1 ("AV but count voter 1 double") cannot be represented here.
# A ballot aggregation function maps (profile, agenda) to a non-empty subset of
# the agenda.
# --------------------------------------------------------------------------

ALTS = "abcd"          # global alternative set; agendas are subsets of this
MAX_VOTERS_3 = 4       # exhaustive window on 3-alternative agendas
MAX_VOTERS_4 = 3       # exhaustive window on 4-alternative agendas
KMAX = 30              # bound for the existential k in continuity
CONT_Q_VOTERS = 2      # continuity quantifies over all Q; we sweep small Q only


def ballots(agenda):
    """All non-empty subsets of the agenda, as frozensets."""
    out = []
    for k in range(1, len(agenda) + 1):
        for c in combinations(sorted(agenda), k):
            out.append(frozenset(c))
    return out


def profiles(agenda, max_voters):
    """Every profile on `agenda` with 1..max_voters voters."""
    bs = ballots(agenda)
    seen = []

    def rec(start, remaining, acc):
        if acc:
            seen.append(dict(acc))
        if remaining == 0:
            return
        for i in range(start, len(bs)):
            b = bs[i]
            acc[b] = acc.get(b, 0) + 1
            rec(i, remaining - 1, acc)
            acc[b] -= 1
            if acc[b] == 0:
                del acc[b]

    rec(0, max_voters, {})
    return seen


def nvoters(P):
    return sum(P.values())


def score(P, x):
    """Approval score: number of voters whose ballot contains x."""
    return sum(n for A, n in P.items() if x in A)


def padd(P, Q):
    R = dict(P)
    for A, n in Q.items():
        R[A] = R.get(A, 0) + n
    return R


def pmul(P, k):
    return {A: n * k for A, n in P.items()}


def single(A):
    return {frozenset(A): 1}


def permute(P, perm):
    """Apply a permutation (dict) of alternatives to a profile."""
    return {frozenset(perm[x] for x in A): n for A, n in P.items()}


def restrict(P, Z):
    """
    P restricted to agenda Z: P_Z(B) = sum of P(A) over A with A & Z == B.
    Returns None when some voter's ballot would become empty, which puts the
    profile outside the model (ballots must be non-empty).
    """
    out = {}
    for A, n in P.items():
        B = frozenset(A & set(Z))
        if not B:
            return None
        out[B] = out.get(B, 0) + n
    return out


def complement_profile(P, agenda):
    """P^c, per the paper: each ballot A becomes Y \\ A, except Y^c = Y."""
    Y = frozenset(agenda)
    out = {}
    for A, n in P.items():
        c = Y if A == Y else frozenset(Y - A)
        out[c] = out.get(c, 0) + n
    return out


def majority_prefers(P, x, y):
    """#voters preferring x to y, under dichotomous preferences."""
    return sum(n for A, n in P.items() if x in A and y not in A)


def condorcet_winner(P, agenda):
    for x in agenda:
        if all(majority_prefers(P, x, y) > majority_prefers(P, y, x)
               for y in agenda if y != x):
            return x
    return None


def condorcet_loser(P, agenda):
    for x in agenda:
        if all(majority_prefers(P, y, x) > majority_prefers(P, x, y)
               for y in agenda if y != x):
            return x
    return None


def pareto_dominated(P, agenda, y):
    """y is dominated if some x is approved by every y-approver, and by more."""
    for x in agenda:
        if x == y:
            continue
        if all(x in A for A in P if y in A) and any(x in A and y not in A for A in P):
            return True
    return False


# --------------------------------------------------------------------------
# Rules. Every rule is f(profile, agenda) -> frozenset of winners.
# AV plus the 17 examples of Appendix B (Example 1 is non-anonymous and so
# cannot exist in this model; it is the anonymity witness and is skipped).
# --------------------------------------------------------------------------

def _argmax(agenda, key):
    vals = {x: key(x) for x in agenda}
    best = max(vals.values())
    return frozenset(x for x in agenda if vals[x] == best)


def _argmin(agenda, key):
    vals = {x: key(x) for x in agenda}
    worst = min(vals.values())
    return frozenset(x for x in agenda if vals[x] == worst)


def AV(P, Y):
    return _argmax(Y, lambda x: score(P, x))


def minus_AV(P, Y):                                     # Example 9
    return _argmin(Y, lambda x: score(P, x))


def TRIV(P, Y):                                         # Example 10
    return frozenset(Y)


def PO(P, Y):                                           # Example 2
    return frozenset(x for x in Y if not pareto_dominated(P, Y, x))


def AV_lex(P, Y):                                       # Example 3
    return frozenset([min(AV(P, Y))])


def constant(P, Y):                                     # Example 4
    return frozenset([min(Y)])


def plurality(P, Y):                                    # Example 5
    """Scoring rule (1, 0, ..., 0): ignores every non-singleton ballot."""
    def s(x):
        return sum(n for A, n in P.items() if len(A) == 1 and x in A)
    if all(len(A) > 1 for A in P):        # all voters ignored -> full tie
        return frozenset(Y)
    return _argmax(Y, s)


def CNL(P, Y):                                          # Example 6
    loser = condorcet_loser(P, Y)
    return frozenset(x for x in Y if x != loser)


def AV_then_plurality(P, Y):                            # Example 7
    W = AV(P, Y)
    def pl(x):
        return sum(n for A, n in P.items() if len(A) == 1 and x in A)
    return _argmax(W, pl)


def AV_most_frequent(P, Y):                             # Example 8
    top = max(P.values())
    Q = {A: n for A, n in P.items() if n == top}
    return AV(Q, Y)


def AV_pl_veto_double(P, Y):                            # Example 11
    def w(A):
        return 2 if (len(A) == 1 or len(A) == len(Y) - 1) else 1
    return _argmax(Y, lambda x: sum(n * w(A) for A, n in P.items() if x in A))


def AV_veto_double(P, Y):                               # Example 12
    def w(A):
        return 2 if len(A) == len(Y) - 1 else 1
    return _argmax(Y, lambda x: sum(n * w(A) for A, n in P.items() if x in A))


def scoring_card(P, Y):                                 # Example 13
    """Ballot A gives |A|*(|Y|-|A|) points to each alternative it approves."""
    m = len(Y)
    return _argmax(Y, lambda x: sum(n * len(A) * (m - len(A))
                                    for A, n in P.items() if x in A))


def ex14(P, Y):                                         # Example 14
    """Like AV, but the ballot {a} gives 1 to a and 0.5 to each of b and c."""
    a, b, c = ALTS[0], ALTS[1], ALTS[2]
    half = Fraction(1, 2)

    def s(x):
        t = Fraction(0)
        for A, n in P.items():
            if A == frozenset([a]):
                if x == a:
                    t += n
                elif x in (b, c) and x in Y:
                    t += n * half
            elif x in A:
                t += n
        return t
    return _argmax(Y, s)


def ex15(P, Y):                                         # Example 15
    """1+eps to approved, 1 to `a` if unapproved. Equivalent description:
    return the intersection of all ballots if non-empty, else {a}."""
    inter = frozenset(Y)
    for A, n in P.items():
        inter &= A
    if inter:
        return inter
    return frozenset([min(Y)])


def ex16(P, Y):                                         # Example 16
    """A ballot approving a: 2 points to a, 1 to each other approved.
    A ballot disapproving a: -1 to a, 1 to each approved."""
    a = ALTS[0]

    def s(x):
        t = 0
        for A, n in P.items():
            if a in A:
                t += n * (2 if x == a else (1 if x in A else 0))
            else:
                t += n * (-1 if x == a else (1 if x in A else 0))
        return t
    return _argmax(Y, s)


def ex17(P, Y):                                         # Example 17
    """+1 approved / -1 disapproved, except a-vs-b ballots score +/-2."""
    a, b = ALTS[0], ALTS[1]

    def s(x):
        t = 0
        for A, n in P.items():
            ab = (a in A and b not in A)
            ba = (b in A and a not in A)
            if ab and x == a:
                t += 2 * n
            elif ab and x == b:
                t -= 2 * n
            elif ba and x == b:
                t += 2 * n
            elif ba and x == a:
                t -= 2 * n
            else:
                t += n if x in A else -n
        return t
    return _argmax(Y, s)


# num -> (label, rule, minimum agenda size the paper states for it)
EXAMPLES = {
    2: ("PO (Pareto optimal alternatives)", PO, 2),
    3: ("AV_lex (lexicographically first AV winner)", AV_lex, 2),
    4: ("constant rule", constant, 2),
    5: ("plurality (ignores non-singleton ballots)", plurality, 2),
    6: ("CNL (all non-Condorcet-losers)", CNL, 2),
    7: ("AV then highest plurality score", AV_then_plurality, 2),
    8: ("AV over most-frequent ballots only", AV_most_frequent, 2),
    9: ("-AV (lowest approval score)", minus_AV, 2),
    10: ("TRIV (everything ties)", TRIV, 2),
    11: ("AV, plurality and veto ballots doubled", AV_pl_veto_double, 2),
    12: ("AV, veto ballots doubled", AV_veto_double, 2),
    13: ("scoring rule |A|(|X|-|A|)", scoring_card, 4),   # paper: |X| >= 4
    14: ("AV except {a} spills 0.5 onto b and c", ex14, 4),  # paper: |X| >= 4
    15: ("consensus intersection, else {a}", ex15, 2),
    16: ("AV except a scores 2 / -1", ex16, 2),
    17: ("+1/-1 with a-vs-b ballots doubled", ex17, 2),
}


def agendas_for(exnum, agendas):
    """Only the agendas the paper's stated scope for this example covers."""
    lo = EXAMPLES[exnum][2]
    return [(Y, Ps) for Y, Ps in agendas if len(Y) >= lo]


def holds(rule, ax, agendas):
    """(ok, witness) for `rule` against axiom `ax` over the given agendas."""
    for Y, Ps in agendas:
        ok, w = AXIOMS[ax](rule, Y, Ps)
        if not ok:
            return False, f"|Y|={len(Y)}: {w}"
    return True, None


# --------------------------------------------------------------------------
# Axioms. Each returns (ok, witness_string_or_None).
# --------------------------------------------------------------------------

def ax_neutrality(f, Y, Ps):
    for P in Ps:
        fP = f(P, Y)
        for order in permutations(sorted(Y)):
            perm = dict(zip(sorted(Y), order))
            lhs = f(permute(P, perm), Y)
            rhs = frozenset(perm[x] for x in fP)
            if lhs != rhs:
                return False, f"P={show(P)} perm={perm} f(pi P)={sh(lhs)} != pi f(P)={sh(rhs)}"
    return True, None


def ax_consistency(f, Y, Ps):
    fs = [(P, f(P, Y)) for P in Ps]
    for P, fP in fs:
        for Q, fQ in fs:
            inter = fP & fQ
            if inter:
                fPQ = f(padd(P, Q), Y)
                if fPQ != inter:
                    return False, (f"P={show(P)} f={sh(fP)}; Q={show(Q)} f={sh(fQ)}; "
                                   f"f(P+Q)={sh(fPQ)} != {sh(inter)}")
    return True, None


def ax_faithfulness(f, Y, Ps):
    for A in ballots(Y):
        if f(single(A), Y) != A:
            return False, f"f({sh(A)})={sh(f(single(A), Y))}"
    return True, None


def ax_continuity(f, Y, Ps):
    """f(P'+kP) = {a} for some k, whenever f(P) = {a}.

    Doubly windowed: the outer quantifier over P' is swept only over profiles
    with <= CONT_Q_VOTERS voters, and the existential k only up to KMAX. A
    reported failure is therefore "no k <= KMAX worked", not a proof -- so
    every failure this raises is re-derived by hand in the note before it is
    reported as a real one.
    """
    singles = [(P, next(iter(fP))) for P in Ps
               for fP in [f(P, Y)] if len(fP) == 1]
    Qs = profiles(Y, CONT_Q_VOTERS)
    for P, a in singles:
        for Q in Qs:
            if not any(f(padd(Q, pmul(P, k)), Y) == frozenset([a])
                       for k in range(1, KMAX + 1)):
                return False, (f"f(P)={{{a}}} for P={show(P)}, but no k<={KMAX} "
                               f"gives f(Q+kP)={{{a}}} for Q={show(Q)}")
    return True, None


def ax_disjoint_equality(f, Y, Ps):
    bs = ballots(Y)
    for A in bs:
        for B in bs:
            if not (A & B):
                P = padd(single(A), single(B))
                if f(P, Y) != (A | B):
                    return False, f"f({sh(A)}+{sh(B)})={sh(f(P, Y))} != {sh(A | B)}"
    return True, None


def ax_cancellation(f, Y, Ps):
    for P in Ps:
        sc = {x: score(P, x) for x in Y}
        if len(set(sc.values())) == 1 and f(P, Y) != frozenset(Y):
            return False, f"all scores equal in P={show(P)} but f(P)={sh(f(P, Y))}"
    return True, None


def ax_non_trivial(f, Y, Ps):
    for P in Ps:
        if f(P, Y) != frozenset(Y):
            return True, None
    return False, "f(P)=X on every profile in the window"


def ax_chooses_cw(f, Y, Ps):
    for P in Ps:
        cw = condorcet_winner(P, Y)
        if cw is not None and cw not in f(P, Y):
            return False, f"CW={cw} not chosen in P={show(P)}, f(P)={sh(f(P, Y))}"
    return True, None


def ax_avoids_cl(f, Y, Ps):
    for P in Ps:
        cl = condorcet_loser(P, Y)
        if cl is not None and cl in f(P, Y):
            return False, f"CL={cl} chosen in P={show(P)}, f(P)={sh(f(P, Y))}"
    return True, None


def ax_unanimous_majorities(f, Y, Ps):
    for P in Ps:
        n = nvoters(P)
        for A, k in P.items():
            if 2 * k > n and not (f(P, Y) & A):
                return False, f"ballot {sh(A)} held by {k}/{n} but f(P)={sh(f(P, Y))}"
    return True, None


def ax_reversal_symmetry(f, Y, Ps):
    for P in Ps:
        fP = f(P, Y)
        if fP != frozenset(Y):
            fc = f(complement_profile(P, Y), Y)
            if fP & fc:
                return False, f"P={show(P)}: f(P)={sh(fP)} meets f(P^c)={sh(fc)}"
    return True, None


def _kelly_weak(W, Z, R):
    """W >=_R Z under Kelly's extension: W subset of R, or Z misses R."""
    return W <= R or not (Z & R)


def _fishburn_weak(W, Z, R):
    return W <= R or not (Z & R) or (W - Z <= R and not ((Z - W) & R))


def _sp(f, Y, Ps, weak):
    """Not manipulable for the given set-preference extension."""
    for P in Ps:
        for R in ballots(Y):
            sincere = f(padd(P, single(R)), Y)
            for A in ballots(Y):
                if A == R:
                    continue
                manip = f(padd(P, single(A)), Y)
                if weak(manip, sincere, R) and not weak(sincere, manip, R):
                    return False, (f"R={sh(R)} reports {sh(A)} at P={show(P)}: "
                                   f"{sh(sincere)} -> {sh(manip)}")
    return True, None


def ax_kelly_sp(f, Y, Ps):
    return _sp(f, Y, Ps, _kelly_weak)


def ax_fishburn_sp(f, Y, Ps):
    return _sp(f, Y, Ps, _fishburn_weak)


def _independence(f, Y, Ps, pick_subagendas):
    for P in Ps:
        fY = f(P, Y)
        for Z in pick_subagendas(P, Y, fY):
            PZ = restrict(P, Z)
            if PZ is None:
                continue                      # outside the model
            if f(PZ, Z) != fY & frozenset(Z):
                return False, (f"P={show(P)}, Y={''.join(sorted(Y))} -> "
                               f"Z={''.join(sorted(Z))}: f_Z={sh(f(PZ, Z))} != "
                               f"{sh(fY & frozenset(Z))}")
    return True, None


def ax_ind_losers(f, Y, Ps):
    def subs(P, Y, fY):
        out = []
        for k in range(len(fY), len(Y)):
            for Z in combinations(sorted(Y), k):
                if fY <= frozenset(Z):
                    out.append(Z)
        return out
    return _independence(f, Y, Ps, subs)


def ax_ind_dominated(f, Y, Ps):
    def subs(P, Y, fY):
        dom = [x for x in Y if pareto_dominated(P, Y, x)]
        out = []
        for k in range(1, len(dom) + 1):
            for drop in combinations(dom, k):
                Z = tuple(sorted(set(Y) - set(drop)))
                if Z:
                    out.append(Z)
        return out
    return _independence(f, Y, Ps, subs)


def ax_ind_never_approved(f, Y, Ps):
    def subs(P, Y, fY):
        never = [x for x in Y if score(P, x) == 0]
        out = []
        for k in range(1, len(never) + 1):
            for drop in combinations(never, k):
                Z = tuple(sorted(set(Y) - set(drop)))
                if Z:
                    out.append(Z)
        return out
    return _independence(f, Y, Ps, subs)


def ax_ind_clones(f, Y, Ps):
    """a,b clones in P if every ballot contains both or neither. Then removing
    b must not disturb the others, and b wins iff a wins without b."""
    for P in Ps:
        fY = f(P, Y)
        for a, b in permutations(sorted(Y), 2):
            if not all((a in A) == (b in A) for A in P):
                continue
            Z = tuple(sorted(set(Y) - {b}))
            PZ = restrict(P, Z)
            if PZ is None:
                continue
            fZ = f(PZ, Z)
            if fZ != fY & frozenset(Z):
                return False, (f"clones {a},{b} in P={show(P)}: f_Z={sh(fZ)} != "
                               f"{sh(fY & frozenset(Z))}")
            if (b in fY) != (a in fZ):
                return False, (f"clones {a},{b} in P={show(P)}: b in f_Y={b in fY} "
                               f"but a in f_Z={a in fZ}")
    return True, None


AXIOMS = {
    "neutrality": ax_neutrality,
    "consistency": ax_consistency,
    "faithfulness": ax_faithfulness,
    "continuity": ax_continuity,
    "disjoint equality": ax_disjoint_equality,
    "cancellation": ax_cancellation,
    "non-triviality": ax_non_trivial,
    "chooses Condorcet winners": ax_chooses_cw,
    "avoids Condorcet losers": ax_avoids_cl,
    "respects unanimous majorities": ax_unanimous_majorities,
    "reversal symmetry": ax_reversal_symmetry,
    "Kelly-strategyproofness": ax_kelly_sp,
    "Fishburn-strategyproofness": ax_fishburn_sp,
    "independence of clones": ax_ind_clones,
    "independence of losers": ax_ind_losers,
    "independence of dominated alt.": ax_ind_dominated,
    "independence of never-approved alt.": ax_ind_never_approved,
}


# --------------------------------------------------------------------------
# Table 1 of the paper. For each theorem: its axioms, and for each axiom the
# Appendix B example(s) cited as showing the axiom cannot be dropped.
# "anon." rows are omitted: this model is anonymous by construction, so
# Example 1 (AV counting voter 1 double) has no representation here.
# --------------------------------------------------------------------------

TABLE_1 = {
    "Theorem 1": {"consistency": [2], "faithfulness": [16], "disjoint equality": [12]},
    "Theorem 2": {"neutrality": [3, 4, 15], "consistency": [2],
                  "non-triviality": [10], "Kelly-strategyproofness": [9, 5]},
    "Theorem 3": {"consistency": [6], "continuity": [7],
                  "chooses Condorcet winners": [5]},
    "Theorem 4": {"neutrality": [14], "consistency": [6], "continuity": [7],
                  "avoids Condorcet losers": [5]},
    "Theorem 5": {"neutrality": [16], "consistency": [8], "continuity": [7],
                  "respects unanimous majorities": [5]},
    "Theorem 6": {"consistency": [2], "faithfulness": [9, 10],
                  "independence of clones": [5]},
    "Theorem 7": {"neutrality": [3], "consistency": [2], "faithfulness": [9, 10],
                  "independence of losers": [5]},
    "Theorem 8": {"neutrality": [3], "consistency": [2],
                  "independence of dominated alt.": [5]},
    "Theorem 9": {"consistency": [8], "reversal symmetry": [5],
                  "independence of never-approved alt.": [11]},
}

# Theorems 3 and 5 are stated for non-trivial rules; Table 1 lists non-triviality
# only for Theorem 2. Checked explicitly in check_triv_gap().
IMPLICIT_NONTRIVIAL = ["Theorem 3", "Theorem 5"]


# --------------------------------------------------------------------------
# Output helpers
# --------------------------------------------------------------------------

def sh(S):
    return "{" + ",".join(sorted(S)) + "}" if S else "{}"


def show(P):
    return " + ".join(f"{n}*{sh(A)}" if n > 1 else sh(A)
                      for A, n in sorted(P.items(), key=lambda kv: sorted(kv[0])))


PASS, FAIL = "  ok  ", " FAIL "
results = {"pass": 0, "fail": 0}


def report(ok, label, detail=""):
    results["pass" if ok else "fail"] += 1
    print(f"[{PASS if ok else FAIL}] {label}" + (f"\n              {detail}" if detail else ""))
    return ok


# --------------------------------------------------------------------------
# Check 1 -- Inada (1969): on the dichotomous domain the majority relation is
# transitive and orders alternatives by approval score, so no Condorcet cycle
# can exist and the approval winners are exactly the maximal elements.
# --------------------------------------------------------------------------

def check_inada(agendas):
    print("\n== Check 1: Inada (1969) -- majority relation on the dichotomous domain ==")
    cycles = 0
    order_mismatch = 0
    maximal_mismatch = 0
    total = 0
    for Y, Ps in agendas:
        for P in Ps:
            total += 1
            # transitivity of strict majority preference
            for x, y, z in permutations(sorted(Y), 3):
                if (majority_prefers(P, x, y) > majority_prefers(P, y, x) and
                        majority_prefers(P, y, z) > majority_prefers(P, z, y)):
                    if not majority_prefers(P, x, z) > majority_prefers(P, z, x):
                        cycles += 1
            # majority order == approval-score order
            for x, y in permutations(sorted(Y), 2):
                maj = majority_prefers(P, x, y) - majority_prefers(P, y, x)
                app = score(P, x) - score(P, y)
                if (maj > 0) != (app > 0) or (maj == 0) != (app == 0):
                    order_mismatch += 1
            # maximal elements of the majority relation == approval winners
            maximal = frozenset(x for x in Y if not any(
                majority_prefers(P, y, x) > majority_prefers(P, x, y) for y in Y))
            if maximal != AV(P, Y):
                maximal_mismatch += 1
    report(cycles == 0, f"no intransitivity in {total} profiles (would be a Condorcet cycle)",
           "" if cycles == 0 else f"{cycles} violations")
    report(order_mismatch == 0, "majority margin and approval-score gap agree in sign everywhere",
           "" if order_mismatch == 0 else f"{order_mismatch} mismatches")
    report(maximal_mismatch == 0, "majority-maximal set == approval winners everywhere",
           "" if maximal_mismatch == 0 else f"{maximal_mismatch} mismatches")


# --------------------------------------------------------------------------
# Check 2 -- AV satisfies every axiom used in the paper.
# --------------------------------------------------------------------------

def check_av(agendas):
    print("\n== Check 2: AV satisfies every axiom in the catalogue ==")
    for name in AXIOMS:
        ok, w = holds(AV, name, agendas)
        report(ok, f"AV: {name}", w or "")


# --------------------------------------------------------------------------
# Check 3 -- Table 1 tightness. For theorem T and axiom a witnessed by example
# k: example k must FAIL a, SATISFY the other axioms of T, and differ from AV.
# --------------------------------------------------------------------------

def check_table1(agendas):
    """
    A cited example is a valid tightness witness for (theorem T, axiom a) iff it
    FAILS a and SATISFIES every other axiom of T. Both halves are checked.

    Caveat that matters for reading the output: TABLE_1 was transcribed from the
    published PDF's text layer, and PDF extraction binds superscripts to tokens
    unreliably. A cell that fails here may be a mis-transcribed citation rather
    than a defect in the paper -- so check_repair() then asks whether some other
    example in Appendix B would have served, which distinguishes the two.
    """
    print("\n== Check 3: Table 1 tightness -- is each cited example a valid witness? ==")
    gaps = []
    for thm, axmap in TABLE_1.items():
        axset = set(axmap)
        for ax, exnums in sorted(axmap.items()):
            for k in exnums:
                label, rule, _ = EXAMPLES[k]
                ags = agendas_for(k, agendas)
                fails_it, witness = holds(rule, ax, ags)
                report(not fails_it,
                       f"{thm} / drop '{ax}' -> Ex {k} ({label}) fails it",
                       witness if not fails_it else
                       "NO counterexample in window -- witness unconfirmed")
                bad = ""
                for other in sorted(axset - {ax}):
                    ok, w = holds(rule, other, ags)
                    if not ok:
                        bad = f"but Ex {k} also fails '{other}' -- {w}"
                        break
                report(not bad, f"{thm} / Ex {k} satisfies the other axioms of {thm}", bad)
                if bad:
                    gaps.append((thm, ax, k, axset))
    return gaps


def check_repair(gaps, agendas):
    """For each broken cell, is there any other Appendix B example that works?"""
    if not gaps:
        return
    print("\n== Check 3b: can a different Appendix B example witness those cells? ==")
    for thm, ax, orig, axset in gaps:
        found = []
        for k, (label, rule, _) in sorted(EXAMPLES.items()):
            if k == orig:
                continue
            ags = agendas_for(k, agendas)
            ok_ax, _ = holds(rule, ax, ags)
            if ok_ax:
                continue                       # must fail the dropped axiom
            if all(holds(rule, o, ags)[0] for o in axset - {ax}):
                found.append(f"Ex {k} ({label})")
        report(bool(found),
               f"{thm} / '{ax}': replacement for Ex {orig}",
               ", ".join(found) if found else
               "none of the other 15 examples satisfies the rest and fails this "
               "-- the cell needs a witness from outside Appendix B")


def check_profile_matrix(agendas):
    """The primary artifact: each rule's actual axiom profile in the window.
    Independent of how Table 1 was transcribed."""
    print("\n== Check 3a: axiom profile of every Appendix B rule (. = holds, X = fails) ==")
    axs = list(AXIOMS)
    short = {a: a.replace("independence of", "ind.").replace("strategyproofness", "SP")
             for a in axs}
    print(f"\n{'rule':<44}" + "".join(f"{i+1:>3}" for i in range(len(axs))))
    for i, a in enumerate(axs):
        print(f"{'':<44}{i+1:>3}  {short[a]}")
    print()
    for k, (label, rule, lo) in [(0, ("AV", AV, 2))] + sorted(EXAMPLES.items()):
        ags = agendas_for(k, agendas) if k else agendas
        name = f"AV" if k == 0 else f"Ex {k:>2}  {label}"
        row = "".join("  ." if holds(rule, a, ags)[0] else "  X" for a in axs)
        print(f"{name:<44}{row}")


# --------------------------------------------------------------------------
# Check 4 -- inline witnesses stated in the paper's own prose.
# --------------------------------------------------------------------------

def p(*items):
    """Build a profile from ballot strings, e.g. p('a','bc','bc')."""
    P = {}
    for s in items:
        A = frozenset(s)
        P[A] = P.get(A, 0) + 1
    return P


def check_stated_witnesses():
    print("\n== Check 4: the paper's own worked witnesses, reproduced exactly ==")
    Y3, Y4 = "abc", "abcd"

    report(PO(p('a', 'c'), Y3) == frozenset('ac') and
           PO(p('b', 'c'), Y3) == frozenset('bc') and
           PO(p('a', 'b', 'c', 'c'), Y3) == frozenset('abc'),
           "Ex 2: PO fails consistency via PO(a+c)={a,c}, PO(b+c)={b,c}, PO(a+b+2c)={a,b,c}")

    report(CNL(p('a', 'b'), Y3) == frozenset('ab') and
           CNL(p('a', 'c'), Y3) == frozenset('ac') and
           CNL(p('a', 'a', 'b', 'c'), Y3) == frozenset('abc'),
           "Ex 6: CNL fails consistency via f(a+b)={a,b}, f(a+c)={a,c}, f(2a+b+c)={a,b,c}")

    report(plurality(p('a', 'bc', 'bc'), Y3) == frozenset('a'),
           "Ex 5: plurality elects a Condorcet loser -- f({a}+2{b,c})={a}")
    report(plurality(p('a', 'b'), Y3) == frozenset('ab') and
           plurality(p('a', 'bc'), Y3) == frozenset('a'),
           "Ex 5: plurality fails independence of clones -- f(a+b)={a,b} but f(a+{b,c})={a}")
    report(plurality(p('a', 'ab', 'c'), Y3) == frozenset('ac') and
           plurality(p('a', 'a', 'c'), Y3) == frozenset('a'),
           "Ex 5: plurality fails independence of losers -- f(a+{a,b}+c)={a,c} vs f(2a+c)={a}")

    # Ex 7, exactly as the paper states it: P={b}, P'={a}+{a,b}+{b,c}.
    P, Pp = p('b'), p('a', 'ab', 'bc')
    report(AV_then_plurality(Pp, Y3) == frozenset('a') and
           all(AV_then_plurality(padd(P, pmul(Pp, k)), Y3) == frozenset('b')
               for k in range(1, KMAX + 1)),
           f"Ex 7: fails continuity -- f(P')={{a}} but f(P+kP')={{b}} for every k<={KMAX}, "
           f"P={{b}}, P'={{a}}+{{a,b}}+{{b,c}}")

    # Ex 8 sanity check FIRST: our implementation must reproduce the three
    # values the paper itself prints for Example 8. If it does, the continuity
    # counterexample below is about the paper, not about this file.
    report(AV_most_frequent(p('ab', 'ac'), Y3) == frozenset('a') and
           AV_most_frequent(p('ab'), Y3) == frozenset('ab') and
           AV_most_frequent(p('ab', 'ab', 'ac'), Y3) == frozenset('ab'),
           "Ex 8: implementation reproduces the paper's own printed values -- "
           "f({a,b}+{a,c})={a}, f({a,b})={a,b}, f(2{a,b}+{a,c})={a,b}")

    # Ex 8's claimed continuity, tested against the paper's own argument.
    P8, Q8 = p('a', 'a', 'ab', 'ab'), p('ab')
    report(AV_most_frequent(P8, Y3) == frozenset('a') and
           all(AV_most_frequent(padd(Q8, pmul(P8, k)), Y3) == frozenset('ab')
               for k in range(1, KMAX + 1)),
           f"Ex 8: CONTRADICTS its stated continuity -- f(P)={{a}} for P=2{{a}}+2{{a,b}}, "
           f"yet f(Q+kP)={{a,b}} for every k<={KMAX} with Q={{a,b}}. The tie between the "
           f"two most-frequent ballots of P is broken by Q, so P's most-frequent SET "
           f"shrinks rather than persists")

    report(AV_pl_veto_double(p('ab', 'c'), Y4) == frozenset('c') and
           AV_pl_veto_double(p('ab', 'c'), Y3) == frozenset('abc'),
           "Ex 11: fails independence of never-approved alt. -- "
           "f_abcd({a,b}+{c})={c} but f_abc({a,b}+{c})={a,b,c}")

    report(AV_veto_double(p('a', 'bc'), Y3) == frozenset('bc'),
           "Ex 12: fails disjoint equality -- f({a}+{b,c})={b,c}, not {a,b,c}")

    report(scoring_card(p('a', 'b', 'cd'), Y4) == frozenset('cd'),
           "Ex 13: fails cancellation on 3 voters -- f({a}+{b}+{c,d})={c,d} with |X|=4")

    report(AV(p('a', 'b', 'c', 'c'), Y3) == frozenset('c') and
           AV(p('ab', 'ab', 'c', 'c'), Y3) == frozenset('abc'),
           "Remark 2: AV is GROUP-manipulable -- {a}+{b}+2{c} elects c; "
           "the a- and b-voters both report {a,b} and reach a tie including their approved set")


# --------------------------------------------------------------------------
# Check 5 -- the role of faithfulness in Theorems 6 and 7. The paper says that
# dropping it leaves exactly AV, -AV and TRIV. So -AV and TRIV must satisfy the
# remaining axioms.
# --------------------------------------------------------------------------

def check_faithfulness_role(agendas):
    print("\n== Check 5: dropping faithfulness leaves -AV and TRIV standing ==")
    for k, axs in ((6, ["consistency", "independence of clones"]),
                   (7, ["neutrality", "consistency", "independence of losers"])):
        for exnum in (9, 10):
            label, rule, _ = EXAMPLES[exnum]
            ok, bad = True, ""
            for ax in axs:
                good, w = holds(rule, ax, agendas)
                if not good:
                    ok, bad = False, f"fails '{ax}' -- {w}"
                    break
            report(ok, f"Theorem {k} minus faithfulness: Ex {exnum} ({label}) "
                       f"satisfies {', '.join(axs)}", bad)


# --------------------------------------------------------------------------
# Check 6 -- is non-triviality really needed in Theorems 3 and 5? Table 1 does
# not list it there, but both theorem statements say "non-trivial".
# --------------------------------------------------------------------------

def check_triv_gap(agendas):
    print("\n== Check 6: does TRIV survive Theorems 3 and 5 without non-triviality? ==")
    for thm, axs in (("Theorem 3", ["consistency", "continuity", "chooses Condorcet winners"]),
                     ("Theorem 5", ["neutrality", "consistency", "continuity",
                                    "respects unanimous majorities"])):
        survives, bad = True, ""
        for ax in axs:
            ok, w = holds(TRIV, ax, agendas)
            if not ok:
                survives, bad = False, f"TRIV fails '{ax}' -- {w}"
                break
        report(survives,
               f"{thm}: TRIV satisfies {', '.join(axs)} -- so non-triviality "
               f"(in the theorem statement, absent from Table 1) is load-bearing", bad)


# --------------------------------------------------------------------------

def main():
    print(__doc__.strip().split("Run:")[0].strip())
    print("\n" + "=" * 78)
    print(f"window: agendas 'abc' (<= {MAX_VOTERS_3} voters) and 'abcd' "
          f"(<= {MAX_VOTERS_4} voters); continuity bound k <= {KMAX}")
    print("=" * 78)

    Y3 = "abc"
    Y4 = "abcd"
    agendas = [(Y3, profiles(Y3, MAX_VOTERS_3)), (Y4, profiles(Y4, MAX_VOTERS_4))]
    for Y, Ps in agendas:
        print(f"  |Y|={len(Y)}: {len(Ps)} profiles")

    check_inada(agendas)
    check_av(agendas)
    check_profile_matrix(agendas)
    gaps = check_table1(agendas)
    check_repair(gaps, agendas)
    check_stated_witnesses()
    check_faithfulness_role(agendas)
    check_triv_gap(agendas)

    print("\n" + "=" * 78)
    print(f"passed {results['pass']}, failed {results['fail']}")
    print("=" * 78)
    return 1 if results["fail"] else 0


if __name__ == "__main__":
    sys.exit(main())
