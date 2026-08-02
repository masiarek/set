#!/usr/bin/env python3
"""Check the four testable claims made in votingtheory.org topic 136.

Thread: "New Simple Condorcet Method - Basically Copeland+Margins" (Sass, 2021),
the debut of Ranked Robin. Nobody in the thread ran the numbers on any of these.

  C1  Sass, post 28: "If you add a weak candidate into the mix, then all of the
      top candidates who would make it into the finalist set each gain exactly 1
      more win, which doesn't change anything meaningful."
  C2  post 40 (deleted account), on Jack Waugh's total-margin variant:
      "That would be identical to Borda."
  C3  Sass, post 18: the one-sentence tally "among the candidates who tie for
      winning the most head-to-head matchups, elect the candidate with the best
      average rank" is mathematically equivalent -- but Sass calls it misleading.
  C4  Jack Waugh, post 13: Ranked Robin "throws away less information in case of
      a cycle" than Copeland, "in such a way that ties are less likely as the
      electorate grows larger."

Notes: ../../ranked-robin-thread-claims-checked.md
Run:   python3 verify.py        (stdlib only, ~40s)
"""

import random
from itertools import combinations

# --------------------------------------------------------------------------
# Ballots and tabulation
#
# A ballot is a list of tiers, best first: [["A"], ["B", "C"]] means A ranked
# 1st, B and C ranked equal 2nd. Candidates in no tier are unranked and count
# as tied for last (the rule Marylander proposed in post 14 and Sass adopted).
# Skipped ranks are ignored -- that is what makes the tier list the whole
# ballot: gaps carry no information.
#
# A profile is a list of (weight, ballot) pairs.
# --------------------------------------------------------------------------


def positions(ballot, cands):
    """Tier index per candidate; unranked share the one worst index.

    Empty tiers are skipped ranks and are dropped before numbering -- "skipped
    ranks are simply ignored and will neither hurt nor help your vote".
    """
    pos = {}
    i = 0
    for tier in ballot:
        if not tier:
            continue
        for c in tier:
            pos[c] = i
        i += 1
    return {c: pos.get(c, i) for c in cands}


def matrix(profile, cands):
    """mat[(x, y)] = ballots preferring x to y."""
    mat = {(x, y): 0 for x in cands for y in cands if x != y}
    for w, ballot in profile:
        pos = positions(ballot, cands)
        for x, y in combinations(cands, 2):
            if pos[x] < pos[y]:
                mat[(x, y)] += w
            elif pos[y] < pos[x]:
                mat[(y, x)] += w
    return mat


def copeland(mat, cands):
    """Matchup wins, a pairwise tie scoring half (BetterVoting's 2026 rule)."""
    s = {}
    for x in cands:
        v = 0.0
        for y in cands:
            if x == y:
                continue
            if mat[(x, y)] > mat[(y, x)]:
                v += 1.0
            elif mat[(x, y)] == mat[(y, x)]:
                v += 0.5
        s[x] = v
    return s


def margin_sum(mat, x, over):
    return sum(mat[(x, y)] - mat[(y, x)] for y in over if y != x)


def ranked_robin(profile, cands, degrees=2):
    """Returns (winners, finalists). len(winners) > 1 means unresolved.

    Degree 1: greatest sum of margins over the other finalists (the thread's
    step 4). Degree 2: greatest sum of margins over all candidates (electowiki).
    """
    mat = matrix(profile, cands)
    scores = copeland(mat, cands)
    best = max(scores.values())
    finalists = sorted(c for c in cands if scores[c] == best)
    live = finalists
    if len(live) > 1 and degrees >= 1:
        tot = {c: margin_sum(mat, c, finalists) for c in live}
        hi = max(tot.values())
        live = sorted(c for c in live if tot[c] == hi)
    if len(live) > 1 and degrees >= 2:
        tot = {c: margin_sum(mat, c, cands) for c in live}
        hi = max(tot.values())
        live = sorted(c for c in live if tot[c] == hi)
    return live, finalists


def borda_tournament(mat, cands, voters):
    """Borda scored off the pairwise matrix: 1 per ballot beaten, half a tie."""
    s = {}
    for x in cands:
        acc = 0.0
        for y in cands:
            if x == y:
                continue
            ties = voters - mat[(x, y)] - mat[(y, x)]
            acc += mat[(x, y)] + 0.5 * ties
        s[x] = acc
    return s


def borda_positional(profile, cands, honor_gaps):
    """Borda as a voter might read 'average rank': lower is better.

    honor_gaps=True reads the rank *numbers the voter wrote* (a ballot marking
    A=1 and B=5 gives B a 5). honor_gaps=False collapses gaps, which is what
    the method actually does. Unranked candidates take the worst rank + 1.
    """
    tot = {c: 0.0 for c in cands}
    n = 0
    for w, ballot in profile:
        n += w
        if honor_gaps:
            marks = {c: i + 1 for i, tier in enumerate(ballot) for c in tier}
            worst = max(marks.values(), default=0) + 1
            for c in cands:
                tot[c] += w * marks.get(c, worst)
        else:
            pos = positions(ballot, cands)
            for c in cands:
                tot[c] += w * (pos[c] + 1)
    return {c: tot[c] / n for c in cands}


# --------------------------------------------------------------------------
# Random profiles
# --------------------------------------------------------------------------

def random_profile(rng, cands, voters, allow_equal=False, allow_trunc=False):
    prof = []
    for _ in range(voters):
        order = list(cands)
        rng.shuffle(order)
        if allow_trunc and rng.random() < 0.4:
            order = order[: rng.randint(1, len(cands) - 1)]
        if allow_equal and len(order) > 1 and rng.random() < 0.4:
            i = rng.randrange(len(order) - 1)
            ballot = [[c] for c in order]
            ballot[i] = [order[i], order[i + 1]]
            del ballot[i + 1]
        else:
            ballot = [[c] for c in order]
        prof.append((1, ballot))
    return prof


def report(title):
    print("\n" + "=" * 74)
    print(title)
    print("=" * 74)


# --------------------------------------------------------------------------
# C1a. Adding a candidate who loses EVERY matchup cannot change the winner
#      at the 1st degree. Sass's argument, stated exactly.
# --------------------------------------------------------------------------

def c1a():
    report("C1a  A candidate who loses every matchup never changes the 1st-degree\n"
           "     result -- Sass's '+1 win to everyone' argument, tested")
    rng = random.Random(20211121)
    base = ["A", "B", "C", "D"]
    full = base + ["X"]
    tested = 0
    for _ in range(60000):
        prof = random_profile(rng, full, rng.choice([5, 7, 9, 11]),
                              allow_equal=True, allow_trunc=True)
        mat = matrix(prof, full)
        if any(mat[("X", y)] >= mat[(y, "X")] for y in base):
            continue  # X must lose every matchup outright
        tested += 1
        stripped = [(w, [[c for c in t if c != "X"] for t in b]) for w, b in prof]
        stripped = [(w, [t for t in b if t]) for w, b in stripped]
        with_x, _ = ranked_robin(prof, full, degrees=1)
        without, _ = ranked_robin(stripped, base, degrees=1)
        assert with_x == without, (prof, with_x, without)
    print(f"  {tested:,} profiles where X loses all four matchups: the 1st-degree")
    print("  outcome is identical with and without X, every time.")
    print("  Reason it is a theorem, not luck: X's presence adds exactly +1 to every")
    print("  other candidate's Copeland score, so the ranking by wins -- and hence the")
    print("  finalist set -- is untouched; X is never a finalist, so the margins summed")
    print("  among finalists never see it.")


# --------------------------------------------------------------------------
# C1b. ...but a candidate who loses every matchup CAN decide the 2nd degree.
# --------------------------------------------------------------------------

def c1b():
    report("C1b  The same all-losing candidate can flip the 2nd-degree tiebreak")
    base = ["A", "B", "C", "D"]
    full = base + ["X"]
    prof = [
        (1, [["A"]]),
        (1, [["C"], ["B"], ["D"]]),
        (1, [["C"], ["A"], ["B"], ["X", "D"]]),
        (1, [["C"], ["B"], ["D"], ["A"]]),
        (1, [["A"], ["X"], ["C"], ["D"], ["B"]]),
        (1, [["D", "A"], ["X"], ["B"], ["C"]]),
    ]
    stripped = [(w, [[c for c in t if c != "X"] for t in b]) for w, b in prof]
    stripped = [(w, [t for t in b if t]) for w, b in stripped]
    mat = matrix(prof, full)
    print("  Six ballots (truncation and equal ranks both in play):")
    for w, b in prof:
        print("    " + " > ".join("=".join(t) for t in b))
    assert all(mat[("X", y)] < mat[(y, "X")] for y in base)
    print(f"  Copeland: " + ", ".join(f"{c} {copeland(mat, full)[c]}" for c in full)
          + "   -> X loses all four matchups, is never a finalist")
    with_x, fin = ranked_robin(prof, full, degrees=2)
    without, fin0 = ranked_robin(stripped, base, degrees=2)
    mat0 = matrix(stripped, base)
    print(f"  Finalists {fin}, and they are pairwise tied "
          f"({mat[('A','C')]}-{mat[('C','A')]}), so the 1st degree cannot separate them.")
    print("  2nd degree, margins summed over all candidates:")
    print(f"    without X:  A {margin_sum(mat0,'A',base):+d}, "
          f"C {margin_sum(mat0,'C',base):+d}   -> {without[0]}")
    print(f"    with X:     A {margin_sum(mat,'A',full):+d}, "
          f"C {margin_sum(mat,'C',full):+d}   -> {with_x[0]}")
    print(f"    the whole difference is the margin against X: A beats X by "
          f"{mat[('A','X')] - mat[('X','A')]}, C by only "
          f"{mat[('C','X')] - mat[('X','C')]}.")
    assert fin == ["A", "C"] and without == ["C"] and with_x == ["A"]
    print("  A candidate who wins nothing decides the election. This is the case Sass")
    print("  himself flagged in post 28 -- confirmed.")

    rng = random.Random(7)
    flips = seen = 0
    for _ in range(200000):
        p = random_profile(rng, full, rng.choice([6, 8, 10]),
                           allow_equal=True, allow_trunc=True)
        m = matrix(p, full)
        if any(m[("X", y)] >= m[(y, "X")] for y in base):
            continue
        s = [(w, [[c for c in t if c != "X"] for t in b]) for w, b in p]
        s = [(w, [t for t in b if t]) for w, b in s]
        seen += 1
        a, _ = ranked_robin(p, full, degrees=2)
        b_, _ = ranked_robin(s, base, degrees=2)
        if a != b_ and len(a) == 1 and len(b_) == 1:
            flips += 1
    print(f"  Rate: {flips} flips in {seen:,} random profiles where X loses every")
    print(f"  matchup ({flips/seen:.2%}) -- rare, and it needs the 1st degree to have")
    print("  tied first, which is itself the rare case (see C4).")


# --------------------------------------------------------------------------
# C1c. A candidate who wins ONE matchup breaks the argument at the 1st degree.
# --------------------------------------------------------------------------

def c1c():
    report("C1c  A candidate with 2% of first preferences flips the winner")
    cands = ["A", "B", "C"]
    prof = [
        (49, [["A"], ["B"], ["C"]]),
        (2,  [["C"], ["A"], ["B"]]),
        (49, [["B"], ["C"], ["A"]]),
    ]
    mat = matrix(prof, cands)
    print("  100 ballots:  49 A>B>C   2 C>A>B   49 B>C>A")
    print(f"    A vs B: {mat[('A','B')]}-{mat[('B','A')]}   "
          f"A vs C: {mat[('A','C')]}-{mat[('C','A')]}   "
          f"B vs C: {mat[('B','C')]}-{mat[('C','B')]}")
    assert mat[("A", "B")] == 51 and mat[("C", "A")] == 51 and mat[("B", "C")] == 98
    two = [(w, [t for t in b if t != ["C"]]) for w, b in prof]
    w2, _ = ranked_robin(two, ["A", "B"])
    w3, fin3 = ranked_robin(prof, cands)
    print(f"  Without C: A beats B 51-49  ->  winner {w2[0]}")
    print(f"  With C:    3-cycle, all three tie on 1 win {fin3}, margins "
          f"A 0, B +94, C -94  ->  winner {w3[0]}")
    assert w2 == ["A"] and w3 == ["B"]
    print("  C takes 2 first preferences and loses to B by 96 votes. It is 'weak' by")
    print("  any ordinary meaning -- but it beats A, so it does NOT hand every")
    print("  contender the same +1, and the winner changes. Sass's argument covers")
    print("  only candidates who lose to everyone; the spoilers that matter are")
    print("  exactly the ones that don't. (Every Condorcet method fails here -- this")
    print("  is IIA failure, not a Ranked Robin defect.)")


# --------------------------------------------------------------------------
# C2. Waugh's total-margin method == Borda (post 40's one-line answer).
# --------------------------------------------------------------------------

def c2():
    report("C2  'Sum every candidate's margins over all others' IS Borda")
    rng = random.Random(2022302)
    cands = ["A", "B", "C", "D", "E"]
    m = len(cands)
    for _ in range(20000):
        v = rng.choice([5, 9, 40])
        prof = random_profile(rng, cands, v, allow_equal=True, allow_trunc=True)
        mat = matrix(prof, cands)
        bt = borda_tournament(mat, cands, v)
        for x in cands:
            assert margin_sum(mat, x, cands) == 2 * bt[x] - (m - 1) * v
    print(f"  Identity holds on 20,000 random profiles, with equal ranks and")
    print(f"  truncation switched on:")
    print("      sum of x's margins  ==  2 * Borda(x)  -  (m-1) * V")
    print("  The subtracted term is the same for every candidate, so the two rankings")
    print("  are identical, not merely correlated. Post 40's one-line reply is exactly")
    print("  right -- and stays right under equal ranking and truncation, provided")
    print("  Borda is scored tournament-style (half a point per pairwise tie, unranked")
    print("  tied last). Waugh's simplification deletes the Copeland gate, and the")
    print("  gate is the only thing separating Ranked Robin from Borda.")


# --------------------------------------------------------------------------
# C3. "best average rank" -- equivalent, and misleading. Both halves.
# --------------------------------------------------------------------------

def c3():
    report("C3  The one-sentence pitch is equivalent only under two conventions\n"
           "    the sentence does not state")
    cands = ["A", "B"]
    prof = [
        (51, [["A"], ["B"]]),                       # marks 1, 2
        (49, [["B"], [], [], [], [], [], [], [], ["A"]]),   # marks 1, then 9
    ]
    mat = matrix(prof, cands)
    win, _ = ranked_robin(prof, cands)
    gaps = borda_positional(prof, cands, honor_gaps=True)
    flat = borda_positional(prof, cands, honor_gaps=False)
    print("  (i) Rank gaps. 100 ballots, two candidates:")
    print("        51 voters mark A 1st, B 2nd")
    print("        49 voters mark B 1st and A 9th (ranks 2-8 skipped)")
    print(f"      Method (skipped ranks ignored): A beats B "
          f"{mat[('A','B')]}-{mat[('B','A')]}, elects {win[0]}")
    print(f"      Average rank as the voter WROTE it:  A {gaps['A']:.2f}, "
          f"B {gaps['B']:.2f}  -> B looks better")
    print(f"      Average rank with gaps collapsed:    A {flat['A']:.2f}, "
          f"B {flat['B']:.2f}  -> A, matching the method")
    assert win == ["A"] and gaps["B"] < gaps["A"] and flat["A"] < flat["B"]
    print("      A voter who takes 'best average rank' literally gets the opposite")
    print("      winner. Sass's objection in post 18 was correct.")

    rng = random.Random(1101)
    cands = ["A", "B", "C", "D"]
    for _ in range(300000):
        v = rng.choice([7, 9, 11])
        prof = random_profile(rng, cands, v)
        win, fin = ranked_robin(prof, cands, degrees=1)
        if len(fin) != 2 or len(win) != 1:
            continue
        avg = borda_positional(prof, cands, honor_gaps=False)
        by_avg = min(fin, key=lambda c: avg[c])
        if by_avg != win[0] and avg[fin[0]] != avg[fin[1]]:
            print("\n  (ii) Which election is the average taken over? Ballots:")
            for w, b in prof:
                print("       " + " > ".join("=".join(t) for t in b))
            print(f"      Finalists tied on wins: {fin}")
            print(f"      Average rank over the FULL ballot: "
                  + ", ".join(f"{c} {avg[c]:.2f}" for c in fin)
                  + f"  -> {by_avg}")
            print(f"      Margins among the finalists only (the actual rule) "
                  f"-> {win[0]}")
            print("      Same sentence, two readings, two winners. The equivalence")
            print("      holds only when the average is taken within the finalist set,")
            print("      which is what post 18's 'among' has to carry on its own.")
            return
    print("  no (ii) example found")


# --------------------------------------------------------------------------
# C4. Do ties thin out as the electorate grows? (Waugh, post 13)
# --------------------------------------------------------------------------

def c4():
    report("C4  Tie rates against electorate size, 4 candidates, impartial culture")
    rng = random.Random(1031)
    cands = ["A", "B", "C", "D"]
    plan = [(5, 20000), (15, 20000), (51, 12000), (201, 5000), (1001, 1500)]
    print(f"  {'voters':>7} {'trials':>7} {'no Condorcet w':>15} {'Copeland tied':>14}"
          f" {'after 1st deg':>14} {'after 2nd deg':>14}")
    for v, trials in plan:
        nocw = cop = deg1 = deg2 = 0
        for _ in range(trials):
            prof = random_profile(rng, cands, v)
            mat = matrix(prof, cands)
            if max(copeland(mat, cands).values()) < len(cands) - 1:
                nocw += 1
            w0, fin = ranked_robin(prof, cands, degrees=0)
            if len(fin) > 1:
                cop += 1
            if len(ranked_robin(prof, cands, degrees=1)[0]) > 1:
                deg1 += 1
            if len(ranked_robin(prof, cands, degrees=2)[0]) > 1:
                deg2 += 1
        print(f"  {v:>7} {trials:>7} {nocw/trials:>14.2%} {cop/trials:>13.2%}"
              f" {deg1/trials:>13.2%} {deg2/trials:>13.2%}")
    print("  The first two columns are equal in every row, and that is forced, not luck:")
    print("  with m candidates and no pairwise ties, the scores sum to m(m-1)/2, so a")
    print("  unique top score of m-2 needs m^2-3m+1 >= m(m-1)/2, i.e. m >= 5. For four")
    print("  or fewer candidates, 'no Condorcet winner' and 'Copeland tie' are the same")
    print("  event -- every cycle reaches the margins rung. From five candidates up they")
    print("  come apart:")
    for m in (5, 6):
        cs = [chr(ord("A") + i) for i in range(m)]
        nocw = cop = 0
        trials = 8000
        for _ in range(trials):
            prof = random_profile(rng, cs, 101)
            mat = matrix(prof, cs)
            sc = copeland(mat, cs)
            if max(sc.values()) < m - 1:
                nocw += 1
                if sum(1 for c in cs if sc[c] == max(sc.values())) == 1:
                    cop += 1
        print(f"    m={m}, 101 voters: no Condorcet winner {nocw/trials:.1%}; of those,"
              f" {cop/nocw:.1%} still have a")
        print(f"      unique Copeland winner, so the tiebreaker never runs at all.")
    print("  Copeland ties stay common at every size -- they are structural (cycles and")
    print("  symmetric standoffs), not an artifact of small electorates. The margins")
    print("  rung is what melts away with V: it needs an exact integer coincidence,")
    print("  which gets rarer as the numbers get bigger. Waugh's post-13 intuition,")
    print("  confirmed: the extra information Ranked Robin keeps is exactly what")
    print("  converts a persistent tie rate into a vanishing one.")


if __name__ == "__main__":
    c1a()
    c1b()
    c1c()
    c2()
    c3()
    c4()
    print("\nAll assertions passed.")
