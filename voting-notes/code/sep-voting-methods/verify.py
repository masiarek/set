#!/usr/bin/env python3
"""Checks every computation in Eric Pacuit, "Voting Methods" (Stanford
Encyclopedia of Philosophy, substantive revision Mon Jun 24, 2019).

https://plato.stanford.edu/entries/voting-methods/

Every profile printed in the entry is transcribed below and every winner,
score, tally and theorem instance the entry asserts about it is recomputed.
Where the entry states a theorem rather than an example, the theorem is
tested by exhaustive search (May, the resoluteness impossibility, Moulin's
threshold, Fishburn's m=3 case) or by simulation (impartial culture).

No dependencies.  Run:  python3 verify.py
"""

import itertools
import random
from fractions import Fraction

CHECKS = []


def check(label, got, want):
    ok = got == want
    CHECKS.append((ok, label, got, want))
    print(f"{'PASS' if ok else 'FAIL'}  {label}\n        got  {got}\n        want {want}")
    return ok


def note(label, value):
    CHECKS.append((True, label, value, value))
    print(f"NOTE  {label}\n        {value}")


def rule(title):
    print(f"\n{'=' * 78}\n{title}\n{'=' * 78}")


# ---------------------------------------------------------------------------
# Generic machinery.  A profile is a list of (count, ranking) pairs, where a
# ranking is a string of candidate letters, best first.
# ---------------------------------------------------------------------------

def voters(profile):
    return sum(n for n, _ in profile)


def cands(profile):
    return sorted(set(profile[0][1]))


def pairwise(profile, a, b):
    """(voters ranking a above b, voters ranking b above a)."""
    va = sum(n for n, r in profile if r.index(a) < r.index(b))
    return va, voters(profile) - va


def majority_relation(profile):
    """{(a, b)} for every strict majority win of a over b."""
    out = set()
    for a, b in itertools.permutations(cands(profile), 2):
        va, vb = pairwise(profile, a, b)
        if va > vb:
            out.add((a, b))
    return out


def condorcet_winner(profile):
    m = majority_relation(profile)
    cs = cands(profile)
    for c in cs:
        if all((c, d) in m for d in cs if d != c):
            return c
    return None


def condorcet_loser(profile):
    m = majority_relation(profile)
    cs = cands(profile)
    for c in cs:
        if all((d, c) in m for d in cs if d != c):
            return c
    return None


def plurality(profile, remaining=None):
    cs = remaining if remaining is not None else set(cands(profile))
    score = {c: 0 for c in cs}
    for n, r in profile:
        for c in r:
            if c in cs:
                score[c] += n
                break
    return score


def lastplace(profile, remaining):
    score = {c: 0 for c in remaining}
    for n, r in profile:
        for c in reversed(r):
            if c in remaining:
                score[c] += n
                break
    return score


def borda(profile):
    cs = cands(profile)
    k = len(cs)
    return {c: sum(n * (k - 1 - r.index(c)) for n, r in profile) for c in cs}


def positional(profile, weights):
    """Score under an arbitrary scoring vector (s1 >= s2 >= ... >= sk)."""
    cs = cands(profile)
    return {c: sum(n * weights[r.index(c)] for n, r in profile) for c in cs}


def winners(score):
    top = max(score.values())
    return frozenset(c for c, v in score.items() if v == top)


def copeland(profile):
    m = majority_relation(profile)
    cs = cands(profile)
    return {c: sum(1 for d in cs if (c, d) in m) - sum(1 for d in cs if (d, c) in m)
            for c in cs}


def minimax(profile):
    """Simpson-Kramer: minimise the largest margin against you."""
    cs = cands(profile)
    worst = {}
    for c in cs:
        worst[c] = max(pairwise(profile, d, c)[0] - pairwise(profile, c, d)[0]
                       for d in cs if d != c)
    best = min(worst.values())
    return frozenset(c for c in cs if worst[c] == best)


# The entry's own definitions of the multi-stage methods (Section 2.1), stated
# with its explicit convention: "I assume that all of the poorly performing
# candidates will be removed in each round."

def hare(profile):
    n = voters(profile)
    remaining = set(cands(profile))
    while remaining:
        score = plurality(profile, remaining)
        for c, v in score.items():
            if 2 * v > n:
                return frozenset({c})
        low = min(score.values())
        remaining -= {c for c in remaining if score[c] == low}
    return frozenset()          # every remaining candidate was deleted at once


def coombs(profile):
    n = voters(profile)
    remaining = set(cands(profile))
    while remaining:
        score = plurality(profile, remaining)
        for c, v in score.items():
            if 2 * v > n:
                return frozenset({c})
        last = lastplace(profile, remaining)
        high = max(last.values())
        remaining -= {c for c in remaining if last[c] == high}
    return frozenset()


def plurality_runoff(profile):
    n = voters(profile)
    score = plurality(profile)
    for c, v in score.items():
        if 2 * v > n:
            return frozenset({c})
    ranked = sorted(score.values(), reverse=True)
    cutoff = ranked[1]                       # "top two (or more if there are ties)"
    finalists = {c for c, v in score.items() if v >= cutoff}
    return winners(plurality(profile, finalists))


# ---------------------------------------------------------------------------
rule("1. The 21-voter example (Section 1): Borda vs Condorcet")
# ---------------------------------------------------------------------------

SEC1 = [(3, "ABCD"), (5, "ACBD"), (7, "BDCA"), (6, "CBDA")]

check("electorate", voters(SEC1), 21)
check("plurality scores", plurality(SEC1), {"A": 8, "B": 7, "C": 6, "D": 0})
check("voters ranking A last", sum(n for n, r in SEC1 if r[-1] == "A"), 13)
check("C vs A", pairwise(SEC1, "C", "A"), (13, 8))
check("C vs B", pairwise(SEC1, "C", "B"), (11, 10))
check("C vs D", pairwise(SEC1, "C", "D"), (14, 7))
check("B vs A", pairwise(SEC1, "B", "A"), (13, 8))
check("B vs C", pairwise(SEC1, "B", "C"), (10, 11))
check("B vs D", pairwise(SEC1, "B", "D"), (21, 0))
check("Condorcet winner", condorcet_winner(SEC1), "C")
check("Condorcet loser", condorcet_loser(SEC1), "A")
check("Borda scores", borda(SEC1), {"A": 24, "B": 44, "C": 38, "D": 20})

# The entry computes the Borda scores twice, once as a sum of pairwise support
# and once positionally.  That the two agree is the identity checked in
# thread136-claims: Borda score = sum over rivals of pairwise support.
pairsum = {c: sum(pairwise(SEC1, c, d)[0] for d in cands(SEC1) if d != c)
           for c in cands(SEC1)}
check("sum of pairwise support == positional Borda", pairsum, borda(SEC1))
check("Borda total is n*C(k,2)", sum(borda(SEC1).values()), 21 * 6)
check("no majority winner exists (quota rules are indecisive here)",
      max(plurality(SEC1).values()) * 2 > 21, False)

# ---------------------------------------------------------------------------
rule("2. Borda 1784: plurality elects the Condorcet loser (Section 2)")
# ---------------------------------------------------------------------------

BORDA1784 = [(1, "ABC"), (7, "ACB"), (7, "BCA"), (6, "CBA")]

check("plurality scores", plurality(BORDA1784), {"A": 8, "B": 7, "C": 6})
check("B vs A", pairwise(BORDA1784, "B", "A"), (13, 8))
check("C vs A", pairwise(BORDA1784, "C", "A"), (13, 8))
check("C vs B", pairwise(BORDA1784, "C", "B"), (13, 8))
check("Condorcet loser is the plurality winner", condorcet_loser(BORDA1784), "A")
check("plurality order exactly reverses the majority order",
      (sorted(plurality(BORDA1784), key=lambda c: -plurality(BORDA1784)[c]),
       ["C", "B", "A"]),
      (["A", "B", "C"], ["C", "B", "A"]))

# ---------------------------------------------------------------------------
rule("3. k-Approval and Approval (Sections 2.1, 2.2)")
# ---------------------------------------------------------------------------

KAPP = [(2, "ADBC"), (2, "BDAC"), (1, "CABD")]


def k_approval(profile, k):
    cs = cands(profile)
    score = {c: 0 for c in cs}
    for n, r in profile:
        for c in r[:k]:
            score[c] += n
    return score


check("1-approval winners", winners(k_approval(KAPP, 1)), frozenset("AB"))
check("2-approval winners", winners(k_approval(KAPP, 2)), frozenset("D"))
check("3-approval winners", winners(k_approval(KAPP, 3)), frozenset("AB"))
check("2-approval scores", k_approval(KAPP, 2), {"A": 3, "B": 2, "C": 1, "D": 4})
check("Condorcet winner", condorcet_winner(KAPP), "A")

# "The Approval ballot ({A},{B},{A,C}) does elect the Condorcet winner."
approval_ballots = [(2, {"A"}), (2, {"B"}), (1, {"A", "C"})]
apscore = {c: sum(n for n, s in approval_ballots if c in s) for c in "ABCD"}
check("approval scores for the entry's ballot profile",
      apscore, {"A": 3, "B": 2, "C": 1, "D": 0})
check("that approval profile elects the Condorcet winner", winners(apscore),
      frozenset("A"))

# ---------------------------------------------------------------------------
rule("4. Plurality-with-Runoff vs Hare vs Coombs, 19 voters (Section 2.1)")
# ---------------------------------------------------------------------------

RUNOFF19 = [(7, "ABCD"), (5, "BCDA"), (4, "DBCA"), (3, "CDAB")]

check("plurality scores", plurality(RUNOFF19), {"A": 7, "B": 5, "C": 3, "D": 4})
check("Plurality with Runoff winner", plurality_runoff(RUNOFF19), frozenset("A"))
check("Hare winner", hare(RUNOFF19), frozenset("D"))
check("Coombs winner", coombs(RUNOFF19), frozenset("B"))
check("Borda scores", borda(RUNOFF19), {"A": 24, "B": 37, "C": 30, "D": 23})
check("Borda winner", winners(borda(RUNOFF19)), frozenset("B"))
check("Condorcet winner", condorcet_winner(RUNOFF19), None)
check("Copeland win-loss records", copeland(RUNOFF19),
      {"A": -1, "B": 1, "C": 1, "D": -1})

# The runoff is A vs B.  Which way do the C-first and D-first groups transfer?
c_group = [r for n, r in RUNOFF19 if r[0] == "C"][0]
d_group = [r for n, r in RUNOFF19 if r[0] == "D"][0]
check("the C-first group (CDAB) transfers to",
      "A" if c_group.index("A") < c_group.index("B") else "B", "A")
check("the D-first group (DBCA) transfers to",
      "A" if d_group.index("A") < d_group.index("B") else "B", "B")
note("entry says", "'the groups voting for candidates C and D transfer their "
     "support to candidates B and A, respectively' -- the pairing is reversed; "
     "C's group transfers to A and D's group to B.  The printed total (A wins "
     "10-9) is right: 7+3 = 10 and 5+4 = 9")
check("runoff tally A vs B", (7 + 3, 5 + 4), (10, 9))

# ---------------------------------------------------------------------------
rule("5. The tie convention: Hare and Coombs on the entry's own paradox profile")
# ---------------------------------------------------------------------------

CYCLE3 = [(1, "ABC"), (1, "BCA"), (1, "CAB")]

check("plurality scores are a perfect three-way tie", plurality(CYCLE3),
      {"A": 1, "B": 1, "C": 1})
check("Hare, as the entry defines it, returns", hare(CYCLE3), frozenset())
check("Coombs, as the entry defines it, returns", coombs(CYCLE3), frozenset())
check("Plurality with Runoff returns", plurality_runoff(CYCLE3), frozenset("ABC"))
note("so", "on the profile the entry uses to state Condorcet's paradox, its "
     "own Hare and Coombs definitions elect nobody: every candidate ties for "
     "fewest first places, all are deleted in round one, and the fallback "
     "clause ('the remaining candidate(s) are declared the winners') has "
     "nothing left to name")

# "If there are only three candidates, then the above two voting methods are
# the same."  Exhaustive test under the entry's stated conventions.
RANKINGS3 = ["".join(p) for p in itertools.permutations("ABC")]


def profiles_of_size(n, rankings):
    """All anonymized profiles of exactly n voters."""
    k = len(rankings)
    for cut in itertools.combinations(range(n + k - 1), k - 1):
        counts, prev = [], -1
        for c in cut:
            counts.append(c - prev - 1)
            prev = c
        counts.append(n + k - 1 - prev - 1)
        yield [(c, r) for c, r in zip(counts, rankings) if c]


disagree, total, empty_hare, other = 0, 0, 0, []
examples = []
for n in range(1, 10):
    for prof in profiles_of_size(n, RANKINGS3):
        total += 1
        h, p = hare(prof), plurality_runoff(prof)
        if not h:
            empty_hare += 1
        if h != p:
            disagree += 1
            if h:
                other.append((prof, sorted(h), sorted(p)))
            if len(examples) < 3:
                examples.append((prof, sorted(h), sorted(p)))
note("3-candidate profiles scanned (1..9 voters)", total)
note("profiles where Hare and Plurality-with-Runoff disagree", disagree)
note("profiles where Hare, as defined, elects nobody", empty_hare)
check("every disagreement is a Hare profile with no winner at all", other, [])
check("so the two methods agree whenever Hare returns anyone",
      disagree, empty_hare)
note("smallest examples (profile, Hare, Plurality-with-Runoff)", examples)
note("so", "the identification of the two methods on three candidates holds "
     "wherever Hare is decisive; the 10% of profiles where it is not are the "
     "ones its stated deletion rule wipes out")

# ---------------------------------------------------------------------------
rule("6. Score Voting vs Majority Judgement, 5 voters (Section 2.2)")
# ---------------------------------------------------------------------------

GRADES = [           # voter -> {candidate: grade}
    {"A": 4, "B": 3, "C": 1},
    {"A": 4, "B": 3, "C": 2},
    {"A": 2, "B": 0, "C": 3},
    {"A": 2, "B": 3, "C": 4},
    {"A": 1, "B": 0, "C": 2},
]


def means(g):
    return {c: Fraction(sum(v[c] for v in g), len(g)) for c in "ABC"}


def medians(g):
    return {c: sorted(v[c] for v in g)[len(g) // 2] for c in "ABC"}


def grades_to_profile(g):
    """Rank candidates by grade; only used where no voter has a tie."""
    prof = []
    for v in g:
        assert len(set(v.values())) == 3, "tie in grades"
        prof.append((1, "".join(sorted("ABC", key=lambda c: -v[c]))))
    return prof


check("mean grades", {c: str(v) for c, v in means(GRADES).items()},
      {"A": "13/5", "B": "9/5", "C": "12/5"})
check("means as decimals", [float(means(GRADES)[c]) for c in "ABC"],
      [2.6, 1.8, 2.4])
check("median grades", medians(GRADES), {"A": 2, "B": 3, "C": 2})
check("Score Voting winner", winners(means(GRADES)), frozenset("A"))
check("Majority Judgement winner", winners(medians(GRADES)), frozenset("B"))
check("Condorcet winner of the induced rankings",
      condorcet_winner(grades_to_profile(GRADES)), "C")
check("C beats A and C beats B, 3-2",
      (pairwise(grades_to_profile(GRADES), "C", "A"),
       pairwise(grades_to_profile(GRADES), "C", "B")), ((3, 2), (3, 2)))

# The score manipulation: voter 3 raises C to 4 and drops A to 1.
G2 = [dict(v) for v in GRADES]
G2[2]["C"], G2[2]["A"] = 4, 1
check("after manipulation, mean of A", float(means(G2)["A"]), 2.4)
check("after manipulation, mean of C", float(means(G2)["C"]), 2.6)
check("Score Voting now elects C", winners(means(G2)), frozenset("C"))
check("the medians did not move", medians(G2), medians(GRADES))

# The Majority Judgement manipulation (Felsenthal and Machover, Example 3.3).
G3 = [dict(v) for v in GRADES]
G3[2]["A"] = 4
check("after MJ manipulation, medians", medians(G3), {"A": 4, "B": 3, "C": 2})
check("Majority Judgement now elects A", winners(medians(G3)), frozenset("A"))
check("and the manipulator really does prefer A to B",
      GRADES[2]["A"] > GRADES[2]["B"], True)
note("wording", "the entry calls this voter 'the voter in the middle column' "
     "twice; the voters are the rows of that table, the columns are candidates")

# ---------------------------------------------------------------------------
rule("7. Condorcet's 81-voter example (Section 3.1.1)")
# ---------------------------------------------------------------------------

C81 = [(30, "ABC"), (1, "ACB"), (29, "BAC"), (10, "BCA"), (10, "CAB"), (1, "CBA")]

check("electorate", voters(C81), 81)
check("A vs B", pairwise(C81, "A", "B"), (41, 40))
check("A vs C", pairwise(C81, "A", "C"), (60, 21))
check("B vs C", pairwise(C81, "B", "C"), (69, 12))
check("Condorcet winner", condorcet_winner(C81), "A")
check("Borda scores", borda(C81), {"A": 101, "B": 109, "C": 33})
check("Borda winner", winners(borda(C81)), frozenset("B"))

first = {c: sum(n for n, r in C81 if r[0] == c) for c in "ABC"}
second = {c: sum(n for n, r in C81 if r[1] == c) for c in "ABC"}
check("first-place counts (the entry's 31 / 39 / 11)", first,
      {"A": 31, "B": 39, "C": 11})
check("second-place counts (the entry's 39 / 31 / 11)", second,
      {"A": 39, "B": 31, "C": 11})


# "The only way to elect A using any scoring method is to assign more points to
# candidates ranked second than to candidates ranked first."
def a_beats_b(s1, s2):
    sc = positional(C81, (s1, s2, Fraction(0)))
    return sc["A"] > sc["B"]


check("A never outscores B unless s2 > s1",
      [a_beats_b(Fraction(1), t) for t in
       (Fraction(0), Fraction(1, 2), Fraction(1), Fraction(3, 2))],
      [False, False, False, True])
check("at s1 = s2 (2-approval) A and B TIE rather than B winning",
      positional(C81, (1, 1, 0)), {"A": 70, "B": 70, "C": 22})
note("so", "this profile is not itself a witness for the m=3 case of Fishburn's "
     "theorem: 2-approval leaves no candidate with a *greater* score than the "
     "Condorcet winner.  The entry does not claim it is, but it presents the "
     "theorem as a generalisation of this example")


# Is there a 3-candidate witness at all?  Search for a profile with a Condorcet
# winner that is strictly outscored by someone under *every* scoring rule.
def strictly_beaten_everywhere(prof, cw):
    """True if for every scoring vector (1, t, 0), t in [0,1], some candidate
    strictly outscores cw."""
    cs = cands(prof)
    others = [c for c in cs if c != cw]
    firsts = {c: sum(n for n, r in prof if r[0] == c) for c in cs}
    seconds = {c: sum(n for n, r in prof if r[1] == c) for c in cs}
    # score_c(t) = firsts[c] + t*seconds[c];  need max_c (score_c - score_cw) > 0
    lines = [(firsts[c] - firsts[cw], seconds[c] - seconds[cw]) for c in others]
    breaks = [Fraction(0), Fraction(1)]
    for (a1, b1), (a2, b2) in itertools.combinations(lines, 2):
        if b1 != b2:
            t = Fraction(a2 - a1, b1 - b2)
            if 0 < t < 1:
                breaks.append(t)
    return all(max(a + b * t for a, b in lines) > 0 for t in breaks)


witness, best_n = None, None
for n in range(3, 13):
    for prof in profiles_of_size(n, RANKINGS3):
        cw = condorcet_winner(prof)
        if cw and strictly_beaten_everywhere(prof, cw):
            witness, best_n = prof, n
            break
    if witness:
        break
note("smallest 3-candidate Fishburn witness found (search: n <= 12)",
     (best_n, witness))
if witness:
    cw = condorcet_winner(witness)
    note("its Condorcet winner / plurality / Borda / 2-approval winners",
         (cw, sorted(winners(plurality(witness))), sorted(winners(borda(witness))),
          sorted(winners(positional(witness, (1, 1, 0))))))

# ---------------------------------------------------------------------------
rule("8. Saari's decomposition of the 81 voters (Section 3.1.1)")
# ---------------------------------------------------------------------------

G1 = [(10, "ABC"), (10, "BCA"), (10, "CAB")]        # a Condorcet component
G2C = [(1, "ACB"), (1, "CBA"), (1, "BAC")]          # the reverse component
G3 = [(20, "ABC"), (28, "BAC")]


def merge(*profs):
    acc = {}
    for p in profs:
        for n, r in p:
            acc[r] = acc.get(r, 0) + n
    return [(n, r) for r, n in sorted(acc.items())]


check("the three groups reconstruct the profile",
      sorted(merge(G1, G2C, G3)), sorted(merge(C81)))
check("group sizes", (voters(G1), voters(G2C), voters(G3)), (30, 3, 48))
check("group 3 elects B", pairwise(G3, "B", "A"), (28, 20))
check("each component gives every candidate the same Borda score",
      (len(set(borda(G1).values())), len(set(borda(G2C).values()))), (1, 1))
check("Borda is therefore decided by group 3 alone",
      {c: borda(G1)[c] + borda(G2C)[c] + borda(G3)[c] for c in "ABC"}, borda(C81))

# But the components do NOT cancel in the majority relation: that is the point.
check("component margins on A vs B (group1, group2, group3)",
      tuple(pairwise(g, "A", "B")[0] - pairwise(g, "A", "B")[1]
            for g in (G1, G2C, G3)), (10, -1, -8))
check("they sum to A's one-vote win", 10 - 1 - 8, 1)
note("so", "A's Condorcet win over B is a margin of exactly 1, assembled from "
     "+10 contributed by the 30-voter cycle and -1 by the 3-voter reverse "
     "cycle against a genuine -8 in the 48 voters who are not in any cycle")

# ---------------------------------------------------------------------------
rule("9. Monotonicity failure of Plurality with Runoff (Section 3.2)")
# ---------------------------------------------------------------------------

MONO1 = [(6, "ABC"), (5, "CAB"), (4, "BCA"), (2, "BAC")]
MONO2 = [(6, "ABC"), (5, "CAB"), (4, "BCA"), (2, "ABC")]

check("scenario 1 plurality scores", plurality(MONO1), {"A": 6, "B": 6, "C": 5})
check("scenario 1 winner", plurality_runoff(MONO1), frozenset("A"))
check("scenario 1 runoff tally A vs B", pairwise(MONO1, "A", "B"), (11, 6))
check("scenario 2 plurality scores", plurality(MONO2), {"A": 8, "B": 4, "C": 5})
check("scenario 2 winner", plurality_runoff(MONO2), frozenset("C"))
check("scenario 2 runoff tally C vs A", pairwise(MONO2, "C", "A"), (9, 8))
check("the two voters who promoted A rank C last", "BAC"[-1], "C")

check("neither scenario has a Condorcet winner",
      (condorcet_winner(MONO1), condorcet_winner(MONO2)), (None, None))
check("both scenarios carry the same majority cycle A > B > C > A",
      (majority_relation(MONO1), majority_relation(MONO2)),
      ({("A", "B"), ("B", "C"), ("C", "A")},
       {("A", "B"), ("B", "C"), ("C", "A")}))
check("Borda elects A in both, so the promotion costs A nothing under Borda",
      (winners(borda(MONO1)), winners(borda(MONO2))),
      (frozenset("A"), frozenset("A")))
check("Borda scores in the two scenarios",
      (borda(MONO1), borda(MONO2)),
      ({"A": 19, "B": 18, "C": 14}, {"A": 21, "B": 16, "C": 14}))
note("so", "the entry's monotonicity example is built on a majority cycle: "
     "there is no Condorcet winner in either scenario, so nothing adjudicates "
     "between A and C on Condorcet grounds.  The scoring rule that Section 4.2 "
     "will show fails IIA is the one that behaves monotonically here")

# ---------------------------------------------------------------------------
rule("10. The no-show paradox (Section 3.3)")
# ---------------------------------------------------------------------------

SHOW = [(4, "ABC"), (3, "BCA"), (1, "CAB"), (3, "CBA")]
NOSHOW = [(2, "ABC"), (3, "BCA"), (1, "CAB"), (3, "CBA")]

check("11-voter plurality scores", plurality(SHOW), {"A": 4, "B": 3, "C": 4})
check("11-voter winner", plurality_runoff(SHOW), frozenset("C"))
check("runoff tally C vs A", pairwise(SHOW, "C", "A"), (7, 4))
check("9-voter plurality scores", plurality(NOSHOW), {"A": 2, "B": 3, "C": 4})
check("9-voter winner", plurality_runoff(NOSHOW), frozenset("B"))
check("runoff tally B vs C", pairwise(NOSHOW, "B", "C"), (5, 4))
check("the absentees rank B above C", "ABC".index("B") < "ABC".index("C"), True)

# ---------------------------------------------------------------------------
rule("11. The multiple districts paradox (Section 3.3)")
# ---------------------------------------------------------------------------

D1 = [(3, "ABC"), (3, "BCA"), (3, "CAB"), (1, "CBA")]
D2 = [(2, "ABC"), (3, "BAC")]

check("district 1 last-place counts", lastplace(D1, set("ABC")),
      {"A": 4, "B": 3, "C": 3})
check("district 1 Coombs winner", coombs(D1), frozenset("B"))
check("district 1 second round B vs C", pairwise(D1, "B", "C"), (6, 4))
check("district 2 Coombs winner", coombs(D2), frozenset("B"))
check("combined last-place counts", lastplace(merge(D1, D2), set("ABC")),
      {"A": 4, "B": 3, "C": 8})
check("combined Coombs winner", coombs(merge(D1, D2)), frozenset("A"))
check("combined second round A vs B", pairwise(merge(D1, D2), "A", "B"), (8, 7))

# Zwicker's proof that every Condorcet consistent method fails reinforcement.
Z1 = [(2, "ABC"), (2, "BCA"), (2, "CAB")]
Z2 = [(1, "ABC"), (2, "BAC")]
check("Zwicker district 1 has no Condorcet winner", condorcet_winner(Z1), None)
check("Zwicker district 2 Condorcet winner", condorcet_winner(Z2), "B")
check("Zwicker combined Condorcet winner", condorcet_winner(merge(Z1, Z2)), "A")
note("so", "a Condorcet consistent V must elect B in district 2 and A in the "
     "combination, so B cannot be among V's winners in district 1; permuting "
     "the labels in district 2 rules out A and C the same way, leaving V with "
     "no winner at all in district 1")

# The same pair also refutes "cancelling properly" (Balinski and Laraki).
check("district 1 is a Condorcet component",
      len(set(n for n, _ in Z1)) == 1 and len(Z1) == 3, True)

# And scoring rules never fail reinforcement: scores simply add.
random.seed(20260801)
bad = 0
for _ in range(2000):
    p1 = [(random.randint(0, 4), r) for r in RANKINGS3]
    p2 = [(random.randint(0, 4), r) for r in RANKINGS3]
    p1 = [(n, r) for n, r in p1 if n] or [(1, "ABC")]
    p2 = [(n, r) for n, r in p2 if n] or [(1, "ABC")]
    for w in ((2, 1, 0), (1, 0, 0), (1, 1, 0), (5, 2, 0)):
        w1, w2 = winners(positional(p1, w)), winners(positional(p2, w))
        both = w1 & w2
        if both and winners(positional(merge(p1, p2), w)) != both:
            bad += 1
check("scoring rules failing reinforcement in 2000 random district pairs", bad, 0)

# ---------------------------------------------------------------------------
rule("12. The multiple elections paradox, Anscombe, Ostrogorski (Section 3.4)")
# ---------------------------------------------------------------------------

MULTI = {"YYY": 1, "YYN": 1, "YNY": 1, "YNN": 3,
         "NYY": 1, "NYN": 3, "NNY": 3, "NNN": 0}

check("electorate", sum(MULTI.values()), 13)
tallies = [(sum(n for b, n in MULTI.items() if b[i] == "Y"),
            sum(n for b, n in MULTI.items() if b[i] == "N")) for i in range(3)]
check("per-proposition tallies", tallies, [(6, 7), (6, 7), (6, 7)])
check("the winning package", "".join("Y" if y > n else "N" for y, n in tallies),
      "NNN")
check("voters who cast that package", MULTI["NNN"], 0)

ANSCOMBE = [("Y", "Y", "N"), ("N", "N", "N"), ("N", "Y", "Y"),
            ("Y", "N", "Y"), ("Y", "N", "Y")]
maj = tuple("Y" if sum(1 for v in ANSCOMBE if v[i] == "Y") * 2 > 5 else "N"
            for i in range(3))
check("majority position on each issue", maj, ("Y", "N", "Y"))
losers = [i + 1 for i, v in enumerate(ANSCOMBE)
          if sum(1 for j in range(3) if v[j] != maj[j]) >= 2]
check("voters on the losing side of a majority of issues", losers, [1, 2, 3])

CAND_A, CAND_B = ("Y", "N", "Y"), ("N", "Y", "N")
votes = {"A": 0, "B": 0}
for v in ANSCOMBE:
    agree_a = sum(1 for j in range(3) if v[j] == CAND_A[j])
    votes["A" if agree_a >= 2 else "B"] += 1
check("Ostrogorski: the minority-position candidate wins", votes, {"A": 2, "B": 3})

# ---------------------------------------------------------------------------
rule("13. Agenda control and Borda manipulation (Section 4.1)")
# ---------------------------------------------------------------------------

AGENDA = [(1, "BDCA"), (1, "ABDC"), (1, "CABD")]
check("every voter prefers B to D", pairwise(AGENDA, "B", "D"), (3, 0))
check("round 1, A vs B", pairwise(AGENDA, "A", "B"), (2, 1))
check("round 2, A vs C", pairwise(AGENDA, "C", "A"), (2, 1))
check("round 3, C vs D", pairwise(AGENDA, "D", "C"), (2, 1))
note("so", "the agenda elects D, which every voter ranks below B")

MANIP1 = [(1, "CDBA"), (1, "BACD"), (1, "ACBD"), (1, "ACDB"), (1, "DCAB")]
MANIP2 = [(1, "CDBA"), (1, "BACD"), (1, "ABDC"), (1, "ACDB"), (1, "DCAB")]

check("scenario 1 Borda scores", borda(MANIP1),
      {"A": 9, "B": 5, "C": 10, "D": 6})
check("scenario 1 winner", winners(borda(MANIP1)), frozenset("C"))
check("scenario 2 Borda scores", borda(MANIP2),
      {"A": 9, "B": 6, "C": 8, "D": 7})
check("scenario 2 winner", winners(borda(MANIP2)), frozenset("A"))
check("the manipulator's sincere ranking prefers A to C",
      "ACBD".index("A") < "ACBD".index("C"), True)
check("voters in the example", voters(MANIP1), 5)
check("candidates in the example", len(cands(MANIP1)), 4)
note("entry says", "'Consider the following two election scenarios with 7 "
     "voters and 3 candidates' -- the table beneath it has 5 voters and 4 "
     "candidates, and every Borda score printed is for 5 voters and 4 candidates")
note("what the manipulation is", "the third voter moves C from second to last "
     "while leaving her favourite A on top: burial, the same move our "
     "star-strategy note verifies against the STAR pages")

# ---------------------------------------------------------------------------
rule("14. Borda and IIA (Section 4.2)")
# ---------------------------------------------------------------------------

IIA1 = [(3, "ABCX"), (2, "BCAX"), (2, "CABX")]
IIA2 = [(3, "ABCX"), (2, "BCXA"), (2, "CXAB")]

check("scenario 1 Borda scores", borda(IIA1), {"A": 15, "B": 14, "C": 13, "X": 0})
check("scenario 2 Borda scores", borda(IIA2), {"A": 11, "B": 12, "C": 13, "X": 6})


def restrict(profile, keep):
    return [(n, "".join(c for c in r if c in keep)) for n, r in profile]


check("the A/B/C sub-rankings are identical in both scenarios",
      sorted(restrict(IIA1, "ABC")), sorted(restrict(IIA2, "ABC")))
check("yet the Borda order reverses",
      (sorted("ABC", key=lambda c: -borda(IIA1)[c]),
       sorted("ABC", key=lambda c: -borda(IIA2)[c])),
      (["A", "B", "C"], ["C", "B", "A"]))
check("the A/B/C part is itself a majority cycle",
      majority_relation(restrict(IIA1, "ABC")), {("A", "B"), ("B", "C"), ("C", "A")})

# ---------------------------------------------------------------------------
rule("15. No resolute anonymous neutral method (Section 4.2)")
# ---------------------------------------------------------------------------


def permute(profile, mapping):
    return sorted(merge([(n, "".join(mapping[c] for c in r)) for n, r in profile]))


rotate = {"A": "B", "B": "C", "C": "A"}
check("the Condorcet component is fixed by the candidate 3-cycle",
      permute(CYCLE3, rotate), sorted(merge(CYCLE3)))
check("no singleton winner set is fixed by that 3-cycle",
      [set(rotate[c] for c in s) == set(s) for s in ("A", "B", "C")],
      [False, False, False])
note("so", "on anonymized profiles - the convention the entry adopts in 1.1 - "
     "Neutrality alone kills Resoluteness here: the profile is its own image "
     "under the rotation, so the winner set must be too, and no singleton is.  "
     "The entry's three-table argument re-derives the Anonymity it has "
     "already built into the domain")

# ---------------------------------------------------------------------------
rule("16. May's Theorem: is Unanimity doing any work? (Section 4.2)")
# ---------------------------------------------------------------------------

# Ballots on two candidates: vote A, abstain, vote B.  An anonymized profile is
# (a, z, b).  An outcome is 'A', 'B' or 'T' (tie).  Anonymity is built into the
# domain, exactly as the entry does.


def two_cand_profiles(n):
    return [(a, z, n - a - z) for a in range(n + 1) for z in range(n + 1 - a)]


def is_positively_responsive(rule_, profs):
    pset = set(profs)
    for (a, z, b) in profs:
        out = rule_[(a, z, b)]
        # a single improvement for A: one B-vote becomes an abstention, or one
        # abstention becomes an A-vote
        for better in [(a, z + 1, b - 1), (a + 1, z - 1, b)]:
            if better in pset and out in ("A", "T") and rule_[better] != "A":
                return False
        # the mirror image, for B
        for better in [(a - 1, z + 1, b), (a, z - 1, b + 1)]:
            if better in pset and out in ("B", "T") and rule_[better] != "B":
                return False
    return True


def is_unanimous(rule_, n):
    return rule_[(n, 0, 0)] == "A" and rule_[(0, 0, n)] == "B"


def majority_rule(a, z, b):
    return "A" if a > b else "B" if b > a else "T"


for n in (3, 4, 5, 6):
    profs = two_cand_profiles(n)
    pairs, selfpaired, seen = [], [], set()
    for p in profs:
        (a, z, b) = p
        q = (b, z, a)
        if p in seen:
            continue
        seen.add(p)
        seen.add(q)
        if p == q:
            selfpaired.append(p)
        else:
            pairs.append((p, q))
    survivors, pr_only, pr_and_un = [], 0, 0
    for combo in itertools.product("ABT", repeat=len(pairs)):
        rule_ = {p: "T" for p in selfpaired}      # neutrality forces these ties
        for (p, q), out in zip(pairs, combo):
            rule_[p] = out
            rule_[q] = {"A": "B", "B": "A", "T": "T"}[out]
        if not is_positively_responsive(rule_, profs):
            continue
        pr_only += 1
        if is_unanimous(rule_, n):
            pr_and_un += 1
            survivors.append(rule_)
    same_as_majority = all(
        all(r[(a, z, b)] == majority_rule(a, z, b) for (a, z, b) in profs)
        for r in survivors)
    check(f"n={n}: rules satisfying Neutrality + Positive Responsiveness", pr_only, 1)
    check(f"n={n}: ... how many of those also satisfy Unanimity", pr_and_un, pr_only)
    check(f"n={n}: the survivor is majority rule", same_as_majority, True)

note("so", "Unanimity is redundant in the entry's statement of May's Theorem: "
     "Anonymity (built into the anonymized domain), Neutrality and Positive "
     "Responsiveness already pin down majority rule, and May's own 1952 "
     "statement uses exactly those three")

# ---------------------------------------------------------------------------
rule("17. Moulin's threshold: Condorcet consistency and participation")
# ---------------------------------------------------------------------------

RANKINGS4 = ["".join(p) for p in itertools.permutations("ABCD")]


def black(profile):
    """Black's Procedure, as the entry defines it: the Condorcet winner if one
    exists, otherwise the Borda winner."""
    cw = condorcet_winner(profile)
    return frozenset(cw) if cw else winners(borda(profile))


def participation_violation(method, prof, maxleave=1):
    """Does a bloc of identical voters regret showing up?  Only unambiguous
    (singleton vs singleton) cases count, so no tie-breaking convention is
    smuggled in.  The entry's own no-show example withdraws 2 voters, so blocs
    up to `maxleave` are allowed."""
    w_all = method(prof)
    if len(w_all) != 1:
        return None
    win = next(iter(w_all))
    for i, (n, r) in enumerate(prof):
        for k in range(1, min(n, maxleave) + 1):
            smaller = [(m if j != i else m - k, s) for j, (m, s) in enumerate(prof)]
            smaller = [(m, s) for m, s in smaller if m]
            if not smaller:
                continue
            w_out = method(smaller)
            if len(w_out) != 1:
                continue
            out = next(iter(w_out))
            if out != win and r.index(out) < r.index(win):
                return (prof, f"{k} x {r}", win, out)
    return None


# Three candidates: minimax survives everything reachable by exhaustive search.
found3, scanned3 = None, 0
for n in range(2, 12):
    for prof in profiles_of_size(n, RANKINGS3):
        scanned3 += 1
        v = participation_violation(minimax, prof, maxleave=3)
        if v:
            found3 = v
            break
    if found3:
        break
note("3-candidate profiles scanned exhaustively (2..11 voters)", scanned3)
check("minimax no-show violations with 3 candidates", found3, None)

# But "some Condorcet method survives at m=3" is not "every one does".
BLACK3 = [(1, "ACB"), (3, "BAC"), (4, "CBA")]
check("Black's Procedure on 8 voters: no Condorcet winner, so Borda decides",
      (condorcet_winner(BLACK3), borda(BLACK3)), (None, {"A": 5, "B": 10, "C": 9}))
check("Black elects B", black(BLACK3), frozenset("B"))
BLACK3_OUT = [(3, "BAC"), (4, "CBA")]
check("with the ACB voter absent, C becomes the Condorcet winner",
      condorcet_winner(BLACK3_OUT), "C")
check("Black then elects C", black(BLACK3_OUT), frozenset("C"))
check("and the absentee ranks C above B", "ACB".index("C") < "ACB".index("B"), True)

# Four candidates: both methods fail, which is Moulin's theorem.
BLACK4 = [(1, "ACBD"), (1, "BADC"), (2, "CBAD"), (1, "CBDA"), (1, "DBAC")]
check("Black on 6 voters elects", black(BLACK4), frozenset("B"))
check("with the ACBD voter absent, Black elects",
      black([(1, "BADC"), (2, "CBAD"), (1, "CBDA"), (1, "DBAC")]), frozenset("C"))
check("and that absentee ranks C above B",
      "ACBD".index("C") < "ACBD".index("B"), True)

exhaustive_none = True
for n in (3, 4, 5):
    for prof in profiles_of_size(n, RANKINGS4):
        if participation_violation(black, prof, maxleave=1):
            exhaustive_none = False
            break
check("no Black no-show paradox on 4 candidates with 5 or fewer voters",
      exhaustive_none, True)

MINIMAX4 = [(2, "ADCB"), (2, "BCAD"), (2, "CADB"), (1, "CBAD"),
            (1, "DABC"), (1, "DBAC"), (2, "DBCA")]
v4 = participation_violation(minimax, MINIMAX4, maxleave=2)
check("minimax on 11 voters has a no-show paradox", v4 is not None, True)
note("witness (profile, bloc that stays home, winner with them, winner without)",
     v4)
note("so", "Moulin's theorem is about what is *possible*, not about what every "
     f"method does: minimax survived all {scanned3} three-candidate profiles "
     "up to 11 voters and fails on four, while Black's Procedure - also "
     "Condorcet consistent - already fails on three candidates and 8 voters")

# ---------------------------------------------------------------------------
rule("18. Impartial culture: how likely is a Condorcet cycle? (Section 5.1)")
# ---------------------------------------------------------------------------


def no_cw_probability(m, n, trials, seed):
    rng = random.Random(seed)
    alts = list(range(m))
    pairs = list(itertools.combinations(alts, 2))
    hits = 0
    for _ in range(trials):
        beats = [[0] * m for _ in range(m)]
        for _ in range(n):
            ballot = alts[:]
            rng.shuffle(ballot)
            pos = {c: i for i, c in enumerate(ballot)}
            for a, b in pairs:
                if pos[a] < pos[b]:
                    beats[a][b] += 1
                else:
                    beats[b][a] += 1
        cw = None
        for a in alts:
            if all(beats[a][b] > beats[b][a] for b in alts if b != a):
                cw = a
                break
        if cw is None:
            hits += 1
    return hits / trials


p57 = no_cw_probability(5, 7, 200000, 11)
note("P(no Condorcet winner), 5 candidates, 7 voters, 200k trials",
     f"{p57:.4f}  (entry: 21.5%)")
check("within 0.5 points of the entry's 21.5%", abs(p57 - 0.215) < 0.005, True)

p5inf = no_cw_probability(5, 151, 30000, 12)
note("P(no Condorcet winner), 5 candidates, 151 voters, 30k trials",
     f"{p5inf:.4f}  (entry's limiting value: 25.1%)")
check("within 1 point of the entry's 25.1%", abs(p5inf - 0.251) < 0.01, True)

trend = [(m, round(no_cw_probability(m, 7, 20000, 13 + m), 3))
         for m in (3, 5, 10, 20)]
note("with 7 voters fixed, P(no Condorcet winner) as candidates grow", trend)
check("it rises monotonically toward 1",
      all(a[1] < b[1] for a, b in zip(trend, trend[1:])), True)

odd = [(n, round(no_cw_probability(3, n, 40000, 30 + n), 4))
       for n in (3, 5, 9, 25, 101)]
note("with 3 candidates fixed, P over odd electorates (limit 8.77%)", odd)
check("it rises with the electorate but not to certainty", odd[-1][1] < 0.09, True)

# ---------------------------------------------------------------------------
rule("Summary")
# ---------------------------------------------------------------------------

failed = [c for c in CHECKS if not c[0]]
print(f"{len(CHECKS)} checks recorded, {len(failed)} discrepancies with the entry:")
for _, label, got, want in failed:
    print(f"  - {label}: got {got}, entry implies {want}")
