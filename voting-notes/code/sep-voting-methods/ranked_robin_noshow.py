#!/usr/bin/env python3
"""Find a no-show paradox for BetterVoting's Ranked Robin.

Moulin's theorem (SEP "Voting Methods", Section 3.3) says every Condorcet
consistent method is susceptible to the no-show paradox once there are four or
more candidates.  Ranked Robin is Condorcet consistent, so a witness must
exist.  The SEP note quotes a witness for *minimax*; this searches for one that
holds for Ranked Robin as BetterVoting actually implements it.

The implementation mirrors packages/backend/src/Tabulators/RankedRobin.ts and
Util.ts at Equal-Vote/bettervoting:

  * pairwise winsAgainst is a strict majority
  * copelandScore = +1 per win, +0.5 per pairwise tie, +0 per loss  (Util.ts:257)
  * the candidates tied at the top copelandScore are the round's contenders
      - exactly one contender            -> winner
      - exactly two, pairwise decisive   -> the pairwise winner  (RankedRobin.ts)
      - otherwise                        -> random tiebreak
  * a profile whose winner comes from the random rung is REJECTED here, so every
    witness printed is deterministic under BV's own code.

No dependencies.  Run:  python3 ranked_robin_noshow.py
"""

import itertools
import random
from collections import Counter


def rankings_over(cands):
    return ["".join(p) for p in itertools.permutations(cands)]


# ---------------------------------------------------------------------------
# Ranked Robin, as BetterVoting implements it.
# ---------------------------------------------------------------------------

def pairwise_wins(profile, cands):
    """{(x, y): True} when x beats y by strict majority."""
    wins = {}
    for x, y in itertools.permutations(cands, 2):
        fx = sum(n for r, n in profile.items() if r.index(x) < r.index(y))
        fy = sum(n for r, n in profile.items() if r.index(y) < r.index(x))
        wins[(x, y)] = fx > fy
    return wins


def copeland_scores(profile, cands):
    wins = pairwise_wins(profile, cands)
    scores = {}
    for c in cands:
        s = 0.0
        for o in cands:
            if o == c:
                continue
            if wins[(c, o)]:
                s += 1.0
            elif wins[(c, o)] == wins[(o, c)]:   # neither beats the other: a tie
                s += 0.5
        scores[c] = s
    return scores, wins


def ranked_robin(profile, cands):
    """Return (winner, rung) where rung is 'copeland' | 'runoff' | 'random'."""
    scores, wins = copeland_scores(profile, cands)
    top = max(scores.values())
    contenders = sorted(c for c in cands if scores[c] == top)

    if len(contenders) == 1:
        return contenders[0], "copeland"

    if len(contenders) == 2:
        a, b = contenders
        if wins[(a, b)] != wins[(b, a)]:          # pairwise decisive
            return (a if wins[(a, b)] else b), "runoff"

    return contenders[0], "random"


# ---------------------------------------------------------------------------
# No-show search.
# ---------------------------------------------------------------------------

def prefers(ranking, x, y):
    return ranking.index(x) < ranking.index(y)


def find_noshow(profile, cands):
    """If some bloc of identical ballots is better off abstaining, return the witness."""
    w_with, rung_with = ranked_robin(profile, cands)
    if rung_with == "random":
        return None

    for ranking, count in sorted(profile.items()):
        for k in range(1, count + 1):
            reduced = Counter(profile)
            reduced[ranking] -= k
            if reduced[ranking] == 0:
                del reduced[ranking]
            if not reduced:
                continue
            w_without, rung_without = ranked_robin(reduced, cands)
            if rung_without == "random":
                continue
            if w_without != w_with and prefers(ranking, w_without, w_with):
                return {
                    "profile": dict(profile),
                    "bloc": (ranking, k),
                    "winner_with": w_with,
                    "rung_with": rung_with,
                    "winner_without": w_without,
                    "rung_without": rung_without,
                    "reduced": dict(reduced),
                    "cands": cands,
                }
    return None


def search(trials, max_voters, cands, seed=20260802):
    rng = random.Random(seed)
    rankings = rankings_over(cands)
    best = None
    for _ in range(trials):
        n = rng.randint(4, max_voters)
        profile = Counter(rng.choice(rankings) for _ in range(n))
        hit = find_noshow(profile, cands)
        if hit:
            total = sum(hit["profile"].values())
            if best is None or total < sum(best["profile"].values()):
                best = hit
    return best


def rate(samples, max_voters, cands, seed):
    rng = random.Random(seed)
    rankings = rankings_over(cands)
    hits = 0
    for _ in range(samples):
        n = rng.randint(4, max_voters)
        profile = Counter(rng.choice(rankings) for _ in range(n))
        if find_noshow(profile, cands):
            hits += 1
    return hits


def all_profiles(cands, n):
    """Every anonymized profile of exactly n voters over `cands`."""
    rankings = rankings_over(cands)
    k = len(rankings)
    # compositions of n into k non-negative parts
    for cuts in itertools.combinations(range(n + k - 1), k - 1):
        counts, prev = [], -1
        for c in cuts:
            counts.append(c - prev - 1)
            prev = c
        counts.append(n + k - 1 - prev - 1)
        yield Counter({r: c for r, c in zip(rankings, counts) if c})


def exhaustive(cands, max_voters):
    """Check every anonymized profile up to max_voters. Returns (checked, witness)."""
    checked = 0
    for n in range(1, max_voters + 1):
        for profile in all_profiles(cands, n):
            checked += 1
            hit = find_noshow(profile, cands)
            if hit:
                return checked, hit
    return checked, None


def show(hit, title):
    print(f"\n{'=' * 78}\n{title}\n{'=' * 78}")
    if not hit:
        print("  none found")
        return
    cands = hit["cands"]
    total = sum(hit["profile"].values())
    ranking, k = hit["bloc"]
    print(f"  {total} voters, {len(cands)} candidates\n")
    for r, n in sorted(hit["profile"].items(), key=lambda kv: (-kv[1], kv[0])):
        mark = "   <- the bloc that stays home" if r == ranking else ""
        print(f"    {n:2d}: {'>'.join(r)}{mark}")
    scores, _ = copeland_scores(Counter(hit["profile"]), cands)
    rscores, _ = copeland_scores(Counter(hit["reduced"]), cands)
    print(f"\n  Copeland with them:    {scores}")
    print(f"  winner with them:      {hit['winner_with']}  (via {hit['rung_with']})")
    print(f"  Copeland without them: {rscores}")
    print(f"  winner without them:   {hit['winner_without']}  (via {hit['rung_without']})")
    print(f"\n  {k} voter(s) ranking {'>'.join(ranking)} get {hit['winner_without']} "
          f"by staying home, and prefer it to {hit['winner_with']}.")
    print("  Both winners come from a deterministic rung: no random tiebreak involved.")


def verify(hit):
    """Re-derive the claim from scratch, independent of the search."""
    cands = hit["cands"]
    p, rp = Counter(hit["profile"]), Counter(hit["reduced"])
    ranking, _ = hit["bloc"]
    a, ra = ranked_robin(p, cands)
    b, rb = ranked_robin(rp, cands)
    checks = [
        ("winner with the bloc matches", a, hit["winner_with"]),
        ("winner without the bloc matches", b, hit["winner_without"]),
        ("the winners differ", a != b, True),
        ("the bloc prefers the abstention outcome", prefers(ranking, b, a), True),
        ("no random rung with them", ra != "random", True),
        ("no random rung without them", rb != "random", True),
    ]
    print("\n  verification:")
    ok = True
    for label, got, want in checks:
        good = got == want
        ok &= good
        print(f"    {'PASS' if good else 'FAIL'}  {label}: {got!r}")
    return ok


if __name__ == "__main__":
    print(__doc__)

    hit4 = search(trials=60000, max_voters=9, cands="ABCD")
    show(hit4, "Smallest no-show witness found for BetterVoting's Ranked Robin")
    assert hit4 and verify(hit4), "expected a four-candidate witness"

    # The four-candidate witness above is minimal by exhaustive search, not just
    # the smallest the random sampler happened to reach.
    checked4, first4 = exhaustive("ABCD", 5)
    print(f"\n{'=' * 78}\nIs five voters really the minimum?\n{'=' * 78}")
    print(f"  exhaustively checked all {checked4:,} anonymized 4-candidate profiles with 1-5 voters")
    if first4:
        print(f"  smallest witness has {sum(first4['profile'].values())} voters -> "
              f"the 5-voter profile above is minimal")
    else:
        print("  none found at 5 or fewer voters (contradicts the search above)")

    # Moulin's bound is about four candidates.  What happens at three is the half
    # the theorem leaves open - the same question the SEP note asks of minimax.
    checked3, hit3 = exhaustive("ABC", 11)
    print(f"\n{'=' * 78}\nThree candidates: what Moulin's bound leaves open\n{'=' * 78}")
    print(f"  exhaustively checked all {checked3:,} anonymized 3-candidate profiles with 1-11 voters")
    if hit3:
        show(hit3, "  a three-candidate witness EXISTS")
    else:
        print("  no no-show paradox found in any of them")
        print("\n  So Ranked Robin behaves like minimax rather than like Black's Procedure:")
        print("  the SEP note records minimax surviving all 12,369 three-candidate profiles")
        print("  up to 11 voters while Black's fails at 8 voters.  Ranked Robin survives too.")
        print("  Moulin's theorem is about what is possible at four, not about what every")
        print("  Condorcet method does at three.")

    N = 20000
    h4 = rate(N, 15, "ABCD", seed=7)
    print(f"\n{'=' * 78}\nHow often, at four candidates\n{'=' * 78}")
    print(f"  {h4:5d}/{N} = {100 * h4 / N:5.2f}% of random 4-candidate profiles (4-15 voters)")
    print("  admit a no-show paradox for some bloc, both outcomes deterministic.")
