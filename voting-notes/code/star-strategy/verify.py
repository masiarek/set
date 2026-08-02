"""Verifies the two STAR Voting examples in ../../star-strategy-pages-vs-wikipedia.md.

1. A participation (no-show) failure: a voter is worse off casting an honest
   ballot than staying home.
2. A score-cut displacement: a voter changes the outcome from their last choice
   to their favorite by RAISING a candidate they don't like, pushing the honest
   winner out of the top two.

Both were found by random search over small profiles and are reproduced here as
fixed profiles, so nothing depends on a seed. Every profile is tie-free at the
score cut and in the runoff, so no tiebreaker is involved.

    python3 verify.py

STAR: sum the scores, the top two advance, the runoff goes to whichever
finalist is scored higher on more ballots.
"""

CANDS = "ABCD"


def totals(ballots):
    return {c: sum(b[c] for b in ballots) for c in CANDS}


def star(ballots):
    """(winner, finalists, totals). Raises if any step needs a tiebreaker."""
    t = totals(ballots)
    ranked = sorted(CANDS, key=lambda c: -t[c])
    if t[ranked[1]] == t[ranked[2]]:
        raise ValueError(f"tie at the score cut: {t}")
    x, y = ranked[0], ranked[1]
    px = sum(1 for b in ballots if b[x] > b[y])
    py = sum(1 for b in ballots if b[y] > b[x])
    if px == py:
        raise ValueError(f"tied runoff {x} v {y}: {px}-{py}")
    return (x if px > py else y), (x, y), t


def table(ballots, mark=None, note=""):
    print("  voter |  A  B  C  D")
    for n, b in enumerate(ballots):
        tag = f"   <-- {note}" if n == mark else ""
        print(f"  {n:>5} | " + " ".join(f"{b[c]:>2}" for c in CANDS) + tag)


def bal(a, b, c, d):
    return dict(zip(CANDS, (a, b, c, d)))


# --- 1. participation failure -------------------------------------------------
# The extra voter's favorite (B) is in the runoff either way. Their 2 stars for D
# lift D over C, swapping the opponent -- and the new opponent beats B.

PARTICIPATION = [
    bal(4, 5, 0, 2),   # voter 0, the one deciding whether to vote
    bal(0, 5, 5, 0),
    bal(5, 0, 5, 1),
    bal(0, 4, 0, 5),
    bal(1, 2, 0, 3),
]


def check_participation():
    print("1. PARTICIPATION FAILURE (5 voters)\n")
    table(PARTICIPATION, mark=0, note="decides whether to show up")
    v = PARTICIPATION[0]

    stay_home = star(PARTICIPATION[1:])
    turn_out = star(PARTICIPATION)

    print(f"\n  stays home: totals {stay_home[2]}")
    print(f"              finalists {stay_home[1]} -> winner {stay_home[0]}")
    print(f"  votes:      totals {turn_out[2]}")
    print(f"              finalists {turn_out[1]} -> winner {turn_out[0]}")
    print(f"\n  Voter 0 scored {stay_home[0]}={v[stay_home[0]]} and "
          f"{turn_out[0]}={v[turn_out[0]]}.")

    assert stay_home[0] == "B" and turn_out[0] == "D"
    assert v["B"] == 5 and v["D"] == 2
    # the honest ballot raises the voter's favorite the most, yet loses them the election
    assert v["B"] == max(v.values())
    print("  An honest ballot cost them a 5-star winner and got them a 2-star one.")
    print("  => STAR does not satisfy the participation criterion. VERIFIED\n")


# --- 2. score-cut displacement (turkey-raising / burial from below) -----------
# Voter 5 already has C at 0, so they cannot bury C any further. Instead they
# raise A -- a candidate they scored 2 -- over C at the score cut. C never
# reaches the runoff, and A then loses it to voter 5's favorite, B.

DISPLACEMENT = [
    bal(0, 0, 1, 3),
    bal(1, 2, 5, 3),
    bal(5, 2, 3, 4),
    bal(3, 4, 2, 4),
    bal(4, 3, 4, 1),
    bal(2, 5, 0, 2),   # voter 5, the strategist (honest ballot)
    bal(4, 5, 5, 1),
]
STRATEGIST = 5
TURKEY, RAISED_TO = "A", 4


def check_displacement():
    print("2. SCORE-CUT DISPLACEMENT (7 voters)\n")
    table(DISPLACEMENT, mark=STRATEGIST, note="strategist (honest ballot shown)")
    v = DISPLACEMENT[STRATEGIST]

    honest = star(DISPLACEMENT)

    strategic_ballots = [dict(b) for b in DISPLACEMENT]
    strategic_ballots[STRATEGIST][TURKEY] = RAISED_TO
    strategic = star(strategic_ballots)

    print(f"\n  honest:    totals {honest[2]}")
    print(f"             finalists {honest[1]} -> winner {honest[0]}")
    print(f"  strategic: voter {STRATEGIST} raises {TURKEY} from "
          f"{v[TURKEY]} to {RAISED_TO}")
    print(f"             totals {strategic[2]}")
    print(f"             finalists {strategic[1]} -> winner {strategic[0]}")
    print(f"\n  Strategist scored {honest[0]}={v[honest[0]]} (honest winner) and "
          f"{strategic[0]}={v[strategic[0]]} (strategic winner).")

    assert honest[0] == "C" and v["C"] == 0, "honest winner is their last choice"
    assert strategic[0] == "B" and v["B"] == 5, "strategic winner is their favorite"
    assert "C" in honest[1] and "C" not in strategic[1], "C displaced from the runoff"
    assert TURKEY in strategic[1] and strategic[0] != TURKEY, "the turkey ran and lost"
    assert v[TURKEY] < v["B"], "the turkey is not their favorite"

    print("  They could not bury C (already at 0), so they lifted A over C instead.")
    print("  A made the runoff and lost it. Their favorite won. VERIFIED\n")

    print("  Why the usual rebuttal misses this: our page argues that promoting a")
    print("  less-preferred candidate risks squeezing your own favorite out of the")
    print(f"  runoff. Here B leads on score ({honest[2]['B']}) and is never at risk,")
    print("  so that check does not bind. The rebuttal holds when your favorite is")
    print("  marginal for the runoff, not when they are comfortably first.\n")


if __name__ == "__main__":
    check_participation()
    check_displacement()
    print("Both examples verified; no step required a tiebreaker.")
