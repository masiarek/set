#!/usr/bin/env python3
"""
Verifier for the AppCW claim on rangevoting.org.

Source: https://www.rangevoting.org/AppCW.html
  "Strategic Range (Approval) voting yields (under reasonable assumptions) a
   Condorcet winner whenever one exists"

THE CLAIM AND ITS PROOF, AS PUBLISHED
-------------------------------------
Assumption: voters rank the candidates, pick a threshold T, approve everything
above T, and place T "to cause their vote to have the most impact" -- in
particular, if the approval winner A and the Condorcet winner C would differ,
every voter places T somewhere between A and C.

Proof (verbatim in substance): suppose A != C. Voters threshold between C and A.
That makes C approved more often than A, since a majority prefers C to A.
So A was not the approval winner. Contradiction. QED.

WHAT THIS SCRIPT CHECKS
-----------------------
Two separate things, because the proof and the headline are not the same claim.

  STEP (sound).  If every voter thresholds between X and Y, then
                 approvals(Y) > approvals(X) exactly when Y beats X pairwise.
                 Ballots approving both or neither cancel, so the approval
                 margin between the two IS the pairwise margin. Checked
                 exhaustively below; no counterexample exists.

  LEAP (unsound as stated).  "A is not the winner" does not give "C is the
                 winner". A third candidate D, ranked above the threshold by
                 both camps, can outpoll both. The proof never rules this out;
                 it is ruled out only by re-running the argument on the *true*
                 top two, which is what makes the result a fixed point rather
                 than a theorem about elections.

So the claim is true of an equilibrium and false of an election whose voters
believe a wrong poll. The witness below is a three-candidate, 100-voter profile
with a Condorcet winner, where a poll naming the wrong frontrunner pair elects
a candidate who is neither the Condorcet winner nor the putative approval
winner -- with every ballot approving them.

Exhaustive part: all 3-candidate profiles with up to MAXV voters (compositions
of n into the 6 strict orders), all ordered frontrunner beliefs.
"""

from itertools import combinations, permutations

CANDS = "ACD"
ORDERS = ["".join(p) for p in permutations(CANDS)]
MAXV = 12


def beats(profile, x, y):
    """Voters ranking x above y."""
    return sum(n for n, o in profile if o.index(x) < o.index(y))


def condorcet_winner(profile, cands=CANDS):
    for c in cands:
        if all(beats(profile, c, d) > beats(profile, d, c) for d in cands if d != c):
            return c
    return None


def leader_rule(profile, leader, runner, cands=CANDS):
    """Laslier's leader rule: approve everyone you prefer to the expected
    leader, plus the leader if you prefer them to the expected runner-up.
    This is the page's "place T between the two" made precise."""
    totals = {c: 0 for c in cands}
    for n, o in profile:
        approved = {c for c in cands if o.index(c) < o.index(leader)}
        if o.index(leader) < o.index(runner):
            approved.add(leader)
        for c in approved:
            totals[c] += n
    return totals


def compositions(n, k):
    if k == 1:
        yield (n,)
        return
    for i in range(n + 1):
        for rest in compositions(n - i, k - 1):
            yield (i,) + rest


def profiles(max_voters):
    for n in range(1, max_voters + 1):
        for counts in compositions(n, len(ORDERS)):
            yield [(c, o) for c, o in zip(counts, ORDERS) if c]


def main():
    # ---- 1. the published witness -------------------------------------------
    witness = [(51, "CDA"), (49, "DAC")]
    print("WITNESS  51 C>D>A , 49 D>A>C")
    for x, y in combinations(CANDS, 2):
        print(f"  {x} vs {y}: {beats(witness, x, y)}-{beats(witness, y, x)}")
    cw = condorcet_winner(witness)
    print(f"  Condorcet winner: {cw}")
    for leader, runner in [("A", "C"), ("C", "A"), ("C", "D"), ("D", "C")]:
        t = leader_rule(witness, leader, runner)
        w = max(t, key=t.get)
        flag = "" if w == cw else "   <-- Condorcet winner LOSES"
        print(f"  poll: {leader} leads {runner} -> {t} winner {w}{flag}")

    # ---- 2. the proof's step, exhaustively ----------------------------------
    checked = violations = 0
    for p in profiles(MAXV):
        for leader, runner in permutations(CANDS, 2):
            t = leader_rule(p, leader, runner)
            pairwise = beats(p, runner, leader) - beats(p, leader, runner)
            approval = t[runner] - t[leader]
            checked += 1
            if pairwise != approval:
                violations += 1
    print(f"\nSTEP  approval margin == pairwise margin, for the two believed "
          f"frontrunners:\n  {checked} (profile, belief) pairs checked, "
          f"{violations} violations")

    # ---- 3. how often the leap fails ----------------------------------------
    total = failed = 0
    for p in profiles(MAXV):
        cw = condorcet_winner(p)
        if cw is None:
            continue
        for leader, runner in permutations(CANDS, 2):
            t = leader_rule(p, leader, runner)
            best = max(t.values())
            winners = [c for c in CANDS if t[c] == best]
            total += 1
            if winners != [cw]:
                failed += 1
    print(f"\nLEAP  profiles with a Condorcet winner, over all frontrunner "
          f"beliefs:\n  {total} cases, {failed} in which the believed pair does "
          f"not elect the Condorcet winner outright "
          f"({100.0 * failed / total:.1f}%)")
    print("\n  (Ties count as failures here; the point is only that the belief, "
          "not the\n   profile, decides. Beliefs that name the true top two do "
          "elect the CW.)")


if __name__ == "__main__":
    main()
