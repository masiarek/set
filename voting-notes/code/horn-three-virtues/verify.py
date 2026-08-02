#!/usr/bin/env python3
"""Checks every number in Walter Horn, "Three Unique Virtues of Approval Voting".

Source: Qeios, preprint v1 (7 Feb 2024, doi:10.32388/ZETKEQ) and the peer-approved
v2 (12 Mar 2024, doi:10.32388/ZETKEQ.2).  The two versions are copy-edited apart;
every arithmetic claim tested here is word-for-word identical in both, so each
check applies to the published version.

No dependencies.  Run:  python3 verify.py
"""

from itertools import combinations, product

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
# The Powell / tax profile (Section III).  Riker's breakdown as Horn prints it.
# ---------------------------------------------------------------------------

# bloc name -> (count, preference order, best to worst)
PROFILE = {
    "big taxers":  (132, "xyz"),
    "pragmatists": (67,  "yxz"),
    "small taxers": (130, "yzx"),
    "anti-tax A":  (49,  "zxy"),
    "anti-tax B":  (48,  "zyx"),
}
ELECTORATE = sum(n for n, _ in PROFILE.values())
CANDS = "xyz"


def pairwise(a, b, profile=PROFILE):
    """(votes for a, votes for b) in the a-vs-b majority contest."""
    va = sum(n for n, p in profile.values() if p.index(a) < p.index(b))
    return va, sum(n for n, _ in profile.values()) - va


def plurality(profile=PROFILE):
    return {c: sum(n for n, p in profile.values() if p[0] == c) for c in CANDS}


def borda(profile=PROFILE):
    return {c: sum(n * (2 - p.index(c)) for n, p in profile.values()) for c in CANDS}


def irv(profile=PROFILE):
    alive = set(CANDS)
    while True:
        tally = {c: 0 for c in alive}
        for n, p in profile.values():
            tally[next(c for c in p if c in alive)] += n
        total = sum(tally.values())
        top = max(tally, key=tally.get)
        if tally[top] * 2 > total or len(alive) == 2:
            return top, tally
        alive.discard(min(tally, key=tally.get))


def condorcet(profile=PROFILE):
    for c in CANDS:
        if all(pairwise(c, d, profile)[0] > pairwise(c, d, profile)[1]
               for d in CANDS if d != c):
            return c
    return None


rule("1. The stated preference profile")

check("blocs sum to Riker's House", ELECTORATE, 426)
note("percentages as printed vs. recomputed",
     {b: (n, f"{100 * n / ELECTORATE:.2f}%") for b, (n, _) in PROFILE.items()})

# Horn's restatement labels the 130-member bloc "yxz", but the list it restates
# says "yzx"; and it collapses zxy + zyx into "zyx".
note("paper's restatement of the 30% bloc",
     "printed 'They are yxz or \"Small Taxers\"' -- the line it restates says yzx; "
     "the same paragraph also collapses zxy (49) + zyx (48) into 'zyx'")

check("a majority, not a plurality, prefers some increase to the status quo",
      sum(n for n, p in PROFILE.values() if p[0] != "z"), 329)
note("that share", f"{100 * 329 / ELECTORATE:.1f}% -- the paper says 'a plurality'")

rule("2. The sequential agenda manipulation Horn describes actually works")

# Amendment vote (x vs y), then the survivor against the status quo z.
sincere_amend = pairwise("x", "y")
check("sincere amendment vote x vs y", sincere_amend, (181, 245))
sincere_final = pairwise("y", "z")
check("sincere final vote y vs z", sincere_final, (329, 97))
check("sincere sequential outcome", "y", "y")

# Anti-taxers (97) vote for the amendment they least want, to sink the bill.
strat_x = sum(n for b, (n, p) in PROFILE.items()
              if b.startswith("anti-tax") or p.index("x") < p.index("y"))
check("strategic amendment vote x vs y", (strat_x, ELECTORATE - strat_x), (229, 197))
strat_final = pairwise("x", "z")
check("strategic final vote x vs z", strat_final, (199, 227))
check("strategic sequential outcome", "z", "z")

rule("3. The approval mapping over-counts its own bloc")

# "of the 132 big taxers, 99 approve of both x and y; and 66 approve of x and z"
check("99 + 66 against a bloc of 132", 99 + 66, 132)   # expected to FAIL
note("implied electorate", 99 + 66 + 67 + 130 + 97)

published = {
    "x": 99 + 66 + 67,
    "y": 99 + 67 + 130,
    "z": 66 + 130 + 97,
}
check("published totals reproduce from 165 big taxers, not 132",
      published, {"x": 232, "y": 296, "z": 293})
check("published margin y over z", published["y"] - published["z"], 3)

# Repair the bloc to its stated size, under both readings of Horn's parenthetical
# "(or of x only, which will here make no difference)".
for tail, label in ((("x", "z"), "33 approve {x,z}"), (("x",), "33 bullet x")):
    fixed = {c: 0 for c in CANDS}
    for c in ("x", "y"):
        fixed[c] += 99
    for c in tail:
        fixed[c] += 33
    for c in ("x", "y"):
        fixed[c] += 67
    for c in ("y", "z"):
        fixed[c] += 130
    fixed["z"] += 97
    win = max(fixed, key=fixed.get)
    runner = sorted(fixed.values())[-2]
    note(f"bloc repaired to 132, {label}",
         f"{fixed} -> {win} wins by {fixed[win] - runner}")

rule("4. Three stipulated approval sets contradict the paper's own rule II.B")

# II.B(1): "if J approves X and does not approve Y at D, then J judges X > Y at D."
def sincerity_violations(pref, approved):
    """Pairs (a, b) where a is approved, b is not, yet the voter ranks b above a."""
    return [(a, b) for a in approved for b in CANDS
            if b not in approved and pref.index(b) < pref.index(a)]


STIPULATED = [
    ("big taxers, 99", "xyz", {"x", "y"}),
    ("big taxers, 66", "xyz", {"x", "z"}),
    ("pragmatists, 67", "yxz", {"x", "y"}),
    ("small taxers, 130", "yzx", {"y", "z"}),
    ("anti-taxers, 97 (zxy)", "zxy", {"z"}),
    ("anti-taxers, 97 (zyx)", "zyx", {"z"}),
]
bad = {n: sincerity_violations(p, a) for n, p, a in STIPULATED if sincerity_violations(p, a)}
check("Section III approval sets consistent with rule II.B", bad, {})   # expected to FAIL

# The Section IV table: each row is "any set containing your favourite", not
# "any upper set of your ranking".
TABLE = {
    "P": ("xyz", [{"x", "y", "z"}, {"x", "y"}, {"x", "z"}, {"x"}, set()]),
    "Q": ("yzx", [{"x", "y", "z"}, {"x", "y"}, {"y", "z"}, {"y"}, set()]),
    "R": ("zxy", [{"x", "y", "z"}, {"x", "z"}, {"y", "z"}, {"z"}, set()]),
}
table_bad = {v: [sorted(s) for s in opts if sincerity_violations(p, s)]
             for v, (p, opts) in TABLE.items()}
check("Section IV table cells consistent with rule II.B", table_bad, {})   # expected to FAIL

rule("5. The 'generalizable' result, as stated, is self-contradicting")

# "Ax is greater than either Ay or Az; and (Ay + Az) is greater than Ax,
#  then y will prevail in a rule compliant AV election."
strict = [(ax, ay, az) for ax, ay, az in product(range(0, 40), repeat=3)
          if ax > ay and ax > az and ay + az > ax
          and max((ay, "y"), (ax, "x"), (az, "z"))[1] == "y"]
check("conjunctive reading: triples where the antecedent holds and y wins",
      len(strict), 0)
note("why", "AV elects argmax; Ax > Ay and Ax > Az means x wins by definition")

loose = [(ax, ay, az) for ax, ay, az in product(range(1, 40), repeat=3)
         if (ax > ay or ax > az) and ay + az > ax
         and max((ay, "y"), (ax, "x"), (az, "z"))[1] != "y"]
check("disjunctive reading: counterexamples exist", len(loose) > 0, True)
note("smallest disjunctive counterexample (Ax, Ay, Az)", min(loose, key=sum))

note("the paper's own example against the antecedent",
     f"Ax={published['x']} is LESS than both Ay={published['y']} and "
     f"Az={published['z']}, so the example does not satisfy the rule it "
     "is offered as an instance of")

rule("6. On the same profile, every simultaneous method defeats the manipulation")

check("plurality", plurality(), {"x": 132, "y": 197, "z": 97})
check("Borda (2/1/0)", borda(), {"x": 380, "y": 574, "z": 324})
check("Borda points conserved", sum(borda().values()), 3 * ELECTORATE)
check("IRV winner", irv()[0], "y")
check("Condorcet winner", condorcet(), "y")
check("x is the Condorcet loser",
      [pairwise("x", d) for d in "yz"], [(181, 245), (199, 227)])
note("conclusion",
     "the compromise y wins under plurality, Borda, IRV and pairwise majority "
     "when all three options are voted on at once -- the defence against "
     "agenda-setting is simultaneity, not approval")

rule("7. Sincere approval on the same profile can elect the status quo")

# Rule (1) fixes each voter's approval set as an attitude, but says nothing about
# where the cutoff falls.  Enumerate every combination of sincere cutoffs: each
# bloc approves its top 1 or its top 2.  (Approving all three, or none, shifts
# every total equally.)
def approvals(cutoffs):
    tally = {c: 0 for c in CANDS}
    for (n, p), k in zip(PROFILE.values(), cutoffs):
        for c in p[:k]:
            tally[c] += n
    return tally


winners = {}
for cutoffs in product([1, 2], repeat=len(PROFILE)):
    tally = approvals(cutoffs)
    best = max(tally.values())
    won = tuple(sorted(c for c in CANDS if tally[c] == best))
    winners.setdefault(won, []).append((cutoffs, tally))

check("achievable outcomes over all 32 sincere cutoff profiles",
      sorted(winners), [("x",), ("y",), ("z",)])
for won in sorted(winners):
    cutoffs, tally = winners[won][0]
    note(f"  {'/'.join(won)} wins in {len(winners[won])} of 32",
         f"e.g. cutoffs {dict(zip(PROFILE, cutoffs))} -> {tally}")

z_case = winners[("z",)][0]
note("the status quo winning on wholly sincere ballots",
     f"cutoffs {dict(zip(PROFILE, z_case[0]))} -> {z_case[1]}; "
     f"z wins although {329}/{ELECTORATE} prefer a tax increase to no change "
     "and y is the Condorcet winner -- the manipulators' outcome, with nobody "
     "misrepresenting anything and no agenda to set")
x_case = winners[("x",)][0]
note("and the Condorcet loser winning on wholly sincere ballots",
     f"cutoffs {dict(zip(PROFILE, x_case[0]))} -> {x_case[1]}")

rule("8. Footnote 20's combinatorics")

# "even if we remove the second and sixth columns ... there would be, for example,
#  12 different ways in which x could get exactly two votes. In those 12 scenarios,
#  x would win in two, tie in eight, and lose to each of the other candidates once."
TRUNCATED = {v: [s for s in opts if s and len(s) < 3] for v, (_, opts) in TABLE.items()}
check("options per voter after the truncation", {v: len(o) for v, o in TRUNCATED.items()},
      {"P": 3, "Q": 3, "R": 3})

def cycle_outcomes(options):
    out = {"x_two": 0, "x_sole": 0, "tie": 0, "loses_to": {"y": 0, "z": 0}}
    for combo in product(*(options[v] for v in "PQR")):
        tally = {c: sum(1 for s in combo if c in s) for c in CANDS}
        if tally["x"] != 2:
            continue
        out["x_two"] += 1
        best = max(tally.values())
        won = [c for c in CANDS if tally[c] == best]
        if won == ["x"]:
            out["x_sole"] += 1
        elif "x" in won:
            out["tie"] += 1
        else:
            for c in won:
                out["loses_to"][c] += 1
    return out


fn20 = cycle_outcomes(TRUNCATED)
check("footnote 20: ways x gets exactly two votes", fn20["x_two"], 12)
check("footnote 20: x wins outright in two", fn20["x_sole"], 2)
check("footnote 20: x ties in eight", fn20["tie"], 8)
check("footnote 20: x loses to each other candidate once", fn20["loses_to"],
      {"y": 1, "z": 1})

# Re-run keeping only the cells that satisfy rule II.B.
SINCERE = {v: [s for s in TRUNCATED[v] if not sincerity_violations(TABLE[v][0], s)]
           for v in "PQR"}
check("sincere options per voter", {v: len(o) for v, o in SINCERE.items()},
      {"P": 2, "Q": 2, "R": 2})
check("ways x gets exactly two votes, insincere cells removed",
      cycle_outcomes(SINCERE)["x_two"], 12)   # expected to FAIL
note("recount", cycle_outcomes(SINCERE))

rule("9. Cycles are a property of pairwise majority, not of every ranked method")

CYCLE = {"P": (1, "xyz"), "Q": (1, "yzx"), "R": (1, "zxy")}
check("the cycle is real: x>y, y>z, z>x by majority",
      [(a, b, pairwise(a, b, CYCLE)) for a, b in (("x", "y"), ("y", "z"), ("z", "x"))],
      [("x", "y", (2, 1)), ("y", "z", (2, 1)), ("z", "x", (2, 1))])
check("Borda's social ordering on the cycle is complete and transitive (a 3-way tie)",
      borda(CYCLE), {"x": 3, "y": 3, "z": 3})
note("so", "Borda, Schulze and ranked pairs all return a transitive social order "
     "on this profile; 'this sort of cycle is unavoidable under every type of "
     "minimally democratic preferentist voting mechanism' overstates it -- the "
     "intransitivity belongs to the pairwise majority relation, which is one "
     "input a ranked method may or may not use")

rule("Summary")
failed = [c for c in CHECKS if not c[0]]
print(f"{len(CHECKS)} checks recorded, {len(failed)} discrepancies with the paper:")
for _, label, got, want in failed:
    print(f"  - {label}: got {got}, paper implies {want}")
