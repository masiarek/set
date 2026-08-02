#!/usr/bin/env python3
"""Verify every numeric claim in ../../single-transferable-vote.md.

STV: multi-winner, one transferable ranked vote per voter.  Set a quota; elect
anyone who reaches it; transfer their surplus; when nobody reaches it, eliminate
the lowest and transfer their pile.  Repeat until the seats are full.

Exact arithmetic throughout (fractions.Fraction), because surplus transfers
divide and the whole point of several checks below is that small differences in
the transfer rule change who wins.

The engine is validated in check 1 against the round-by-round count published in
the Wikipedia article before it is used for anything else.

Run:  python3 verify.py
No dependencies beyond the standard library.
"""

from fractions import Fraction
import random

CONTINUING, ELECTED, ELIMINATED = 0, 1, 2


def droop(votes, seats):
    return votes // (seats + 1) + 1


def hare(votes, seats):
    return Fraction(votes, seats)


class Bundle:
    """A group of identical ballots moving together, carrying a current value."""

    __slots__ = ("value", "prefs", "pos")

    def __init__(self, value, prefs, pos=0):
        self.value, self.prefs, self.pos = value, prefs, pos

    def next_continuing(self, status):
        p = self.pos
        while p < len(self.prefs) and status.get(self.prefs[p]) != CONTINUING:
            p += 1
        return (self.prefs[p], p) if p < len(self.prefs) else (None, p)


def stv(ballots, cands, seats, quota="droop", surplus="wigm", trace=None):
    """ballots: [(count, [ranked names])].  -> list of winners, in election order.

    surplus: 'wigm'    weighted inclusive Gregory -- all papers held, Scotland
             'gregory' basic Gregory -- only the last parcel received, Ireland
                       (Senate) and Northern Ireland
    """
    total = sum(n for n, _ in ballots)
    q = droop(total, seats) if quota == "droop" else hare(total, seats)

    status = {c: CONTINUING for c in cands}
    parcels = {c: [] for c in cands}          # each parcel is a list of Bundles

    def count(c):
        return sum(b.value for pc in parcels[c] for b in pc)

    def place(bundles):
        """Route bundles to their next continuing choice, as one new parcel each."""
        drop = {}
        for b in bundles:
            c, p = b.next_continuing(status)
            if c is None:
                continue                      # exhausted
            b.pos = p
            drop.setdefault(c, []).append(b)
        for c, bs in drop.items():
            parcels[c].append(bs)

    start = []
    for n, prefs in ballots:
        start.append(Bundle(Fraction(n), tuple(prefs)))
    place(start)

    first_prefs = {c: count(c) for c in cands}
    winners = []

    while len(winners) < seats:
        cont = [c for c in cands if status[c] == CONTINUING]
        if trace is not None:
            trace.append({c: count(c) for c in cont})

        if len(cont) + len(winners) <= seats:          # everyone left gets in
            for c in sorted(cont, key=lambda c: (-count(c), c)):
                status[c] = ELECTED
                winners.append(c)
            break

        reached = [c for c in cont if count(c) >= q]
        if reached:
            c = max(reached, key=lambda c: (count(c), c))
            surplus_value = count(c) - q
            status[c] = ELECTED
            winners.append(c)
            if len(winners) == seats:
                break
            held = parcels[c]
            parcels[c] = []
            if surplus_value > 0:
                relevant = held if surplus == "wigm" else [held[-1]]
                keep = held[:-1] if surplus == "gregory" else []
                pool = [b for pc in relevant for b in pc]
                base = sum(b.value for b in pool)
                movable = [b for b in pool
                           if b.next_continuing(status)[0] is not None]
                if base > 0 and movable:
                    factor = min(Fraction(1), surplus_value / base)
                    moved = [Bundle(b.value * factor, b.prefs, b.pos) for b in movable]
                    place(moved)
                parcels[c] = keep                      # retained, never moves again
            else:
                parcels[c] = held
        else:
            low = min(count(x) for x in cont)
            tied = [x for x in cont if count(x) == low]
            # backward tiebreak: fewest first preferences, then by name
            c = min(tied, key=lambda x: (first_prefs[x], x))
            status[c] = ELIMINATED
            held = parcels[c]
            parcels[c] = []
            place([b for pc in held for b in pc])

    return winners


def sntv(ballots, cands, seats):
    """Single non-transferable vote: first preferences only, top `seats` win."""
    t = {c: 0 for c in cands}
    for n, prefs in ballots:
        t[prefs[0]] += n
    return sorted(cands, key=lambda c: (-t[c], c))[:seats]


def irv(ballots, cands):
    """Plain IRV, using the SAME backward tiebreak as stv() above.

    That caveat is the whole point: with alphabetical tiebreaks instead, IRV and
    one-seat STV disagree on 15 of 4000 random profiles -- never because the
    algorithms differ, only because the tie rule does.
    """
    first = {c: 0 for c in cands}
    for n, prefs in ballots:
        first[prefs[0]] += n
    alive = list(cands)
    while len(alive) > 1:
        t = {c: 0 for c in alive}
        for n, prefs in ballots:
            for x in prefs:
                if x in alive:
                    t[x] += n
                    break
        lead = max(t, key=lambda c: (t[c], c))
        if t[lead] * 2 > sum(t.values()):
            return lead
        low = min(t.values())
        tied = [c for c in alive if t[c] == low]
        alive.remove(min(tied, key=lambda c: (first[c], c)))
    return alive[0]


# ---------------------------------------------------- the article's own count

PARTY_FOOD = [
    (3, ["Orange", "Pear"]),
    (8, ["Pear", "Strawberry", "Cake"]),
    (1, ["Strawberry", "Orange", "Pear"]),
    (3, ["Cake", "Chocolate"]),
    (1, ["Chocolate", "Cake", "Hamburger"]),
    (4, ["Hamburger", "Chicken"]),
    (3, ["Chicken", "Chocolate", "Hamburger"]),
]
FOODS = ["Orange", "Pear", "Strawberry", "Cake", "Chocolate", "Hamburger", "Chicken"]

# ---------------------------------------------------- the Lumen 75-ballot set
# Same profile as ../lumen-75-ballot/verify.py, reused as a cross-check.

LUMEN = [
    (20, ["Garcia", "Lee", "Nguyen", "Smith"]),
    (3,  ["Garcia", "Nguyen", "Lee", "Smith"]),
    (8,  ["Lee", "Nguyen", "Garcia", "Smith"]),
    (16, ["Nguyen", "Garcia", "Lee", "Smith"]),
    (28, ["Smith", "Lee", "Garcia", "Nguyen"]),
]
LUMEN_C = ["Garcia", "Lee", "Nguyen", "Smith"]


def rand_ballots(rng, cands, blocs=6, maxn=40):
    out = []
    for _ in range(blocs):
        prefs = cands[:]
        rng.shuffle(prefs)
        keep = rng.randint(2, len(cands))
        out.append((rng.randint(1, maxn), prefs[:keep]))
    return out


def main():
    ok = []

    # ---- 1. Reproduce the published count exactly -------------------------
    assert sum(n for n, _ in PARTY_FOOD) == 23
    assert droop(23, 3) == 6
    tr = []
    w = stv(PARTY_FOOD, FOODS, 3, trace=tr)
    assert tr[0] == {"Orange": 3, "Pear": 8, "Strawberry": 1, "Cake": 3,
                     "Chocolate": 1, "Hamburger": 4, "Chicken": 3}
    assert tr[1]["Strawberry"] == 3                 # Pear's surplus of 2 lands here
    assert tr[2]["Cake"] == 4                       # Chocolate eliminated, Cake +1
    assert tr[3]["Orange"] == 4 and tr[3]["Cake"] == 6   # Strawberry out, Cake elected
    assert w == ["Pear", "Cake", "Hamburger"]
    ok.append("engine reproduces the article's 23-vote count: quota 6, winners Pear/Cake/Hamburger")
    ok.append("  and every round-by-round tally in the published table")

    # ---- 2. STV with one seat IS instant-runoff voting ---------------------
    assert droop(75, 1) == 38 and 38 * 2 > 75       # Droop for 1 seat = a majority
    assert stv(LUMEN, LUMEN_C, 1) == ["Nguyen"] == [irv(LUMEN, LUMEN_C)]
    rng = random.Random(20260801)
    agree = 0
    for _ in range(4000):
        b = rand_ballots(rng, ["A", "B", "C", "D"])
        if stv(b, ["A", "B", "C", "D"], 1) == [irv(b, ["A", "B", "C", "D"])]:
            agree += 1
    assert agree == 4000
    ok.append("STV with 1 seat == IRV: same winner on the Lumen 75 ballots (Nguyen)")
    ok.append("  and on 4000 random 4-candidate profiles -- given the SAME tiebreak rule")
    # Swap in an alphabetical elimination tiebreak and they come apart, purely on ties.
    def irv_alpha(ballots, cands):
        alive = list(cands)
        while len(alive) > 1:
            t = {c: 0 for c in alive}
            for n, prefs in ballots:
                for x in prefs:
                    if x in alive:
                        t[x] += n
                        break
            lead = max(t, key=lambda c: (t[c], c))
            if t[lead] * 2 > sum(t.values()):
                return lead
            alive.remove(min(t, key=lambda c: (t[c], c)))
        return alive[0]
    rng = random.Random(20260801)
    split = 0
    for _ in range(4000):
        b = rand_ballots(rng, ["A", "B", "C", "D"])
        if stv(b, ["A", "B", "C", "D"], 1) != [irv_alpha(b, ["A", "B", "C", "D"])]:
            split += 1
    assert split == 15, split
    ok.append(f"  swap in an alphabetical tiebreak and they split on {split}/4000 -- ties, not logic")

    # ---- 3. Why Droop is the smallest safe quota --------------------------
    # (S+1) candidates each holding a Droop quota would need more votes than exist.
    for V in range(2, 400):
        for S in range(1, 8):
            q = droop(V, S)
            assert (S + 1) * q > V                  # safe: at most S can reach it
            assert (S + 1) * (q - 1) <= V           # minimal: one lower is not safe
    ok.append("Droop is exactly the smallest safe quota, both halves checked for every")
    ok.append("  V < 400 and S < 8: (S+1)*q > V, and (S+1)*(q-1) <= V")
    assert droop(23, 3) == 6 and hare(23, 3) == Fraction(23, 3)
    assert float(hare(23, 3)) > 7.6
    ok.append("  on the party profile Droop is 6 and Hare is 7.67 -- Hare is the harder bar")

    # ---- 4. The quota choice changes who wins ------------------------------
    rng = random.Random(11)
    diff = 0
    trials = 0
    example = None
    for _ in range(4000):
        b = rand_ballots(rng, ["A", "B", "C", "D", "E"])
        d = stv(b, ["A", "B", "C", "D", "E"], 3, quota="droop")
        h = stv(b, ["A", "B", "C", "D", "E"], 3, quota="hare")
        trials += 1
        if set(d) != set(h):
            diff += 1
            if example is None:
                example = (b, d, h)
    assert example, "expected Droop and Hare to part ways"
    rate = 100 * diff / trials
    ok.append(f"Droop vs Hare elect different sets in {rate:.1f}% of {trials} random 3-seat profiles")

    # ---- 5. So does the surplus-transfer rule ------------------------------
    rng = random.Random(5)
    gdiff = 0
    gtrials = 0
    gex = None
    for _ in range(6000):
        b = rand_ballots(rng, ["A", "B", "C", "D", "E"])
        a = stv(b, ["A", "B", "C", "D", "E"], 3, surplus="wigm")
        g = stv(b, ["A", "B", "C", "D", "E"], 3, surplus="gregory")
        gtrials += 1
        if set(a) != set(g):
            gdiff += 1
            if gex is None:
                gex = (b, a, g)
    assert gex, "expected WIGM and basic Gregory to part ways"
    grate = 100 * gdiff / gtrials
    ok.append(f"WIGM (Scotland) vs basic Gregory (Ireland Senate, NI) differ in {grate:.1f}%")
    ok.append(f"  of {gtrials} profiles -- 'STV' names a family, not a method")

    # ---- 6. How much do the transfers actually change? --------------------
    rng = random.Random(77)
    same = 0
    n = 0
    for _ in range(6000):
        cands = ["A", "B", "C", "D", "E", "F"]
        b = rand_ballots(rng, cands, blocs=8)
        n += 1
        if set(stv(b, cands, 3)) == set(sntv(b, cands, 3)):
            same += 1
    srate = 100 * same / n
    assert 40 < srate < 95, srate
    ok.append(f"STV and plain first-preferences (SNTV) elect the same 3 of 6 in {srate:.1f}% of")
    ok.append(f"  {n} profiles -- the article's point that transfers often change nothing")

    # ---- 7. Non-monotonicity, inherited from IRV --------------------------
    rng = random.Random(3)
    hit = None
    for _ in range(40000):
        cands = ["A", "B", "C", "D", "E"]
        b = rand_ballots(rng, cands, blocs=5)
        base = set(stv(b, cands, 2))
        for i, (cnt, prefs) in enumerate(b):
            for wc in base:
                if wc not in prefs or prefs.index(wc) == 0:
                    continue
                lifted = list(prefs)
                j = lifted.index(wc)
                lifted[j - 1], lifted[j] = lifted[j], lifted[j - 1]
                b2 = b[:i] + [(cnt, lifted)] + b[i + 1:]
                if wc not in set(stv(b2, cands, 2)):
                    hit = (b, i, wc, base, set(stv(b2, cands, 2)))
                    break
            if hit:
                break
        if hit:
            break
    assert hit, "expected a monotonicity failure"
    ok.append("non-monotonic, as IRV is: promoting a winner one place on one bloc's")
    ok.append(f"  ballots unseats them -- {hit[2]} drops out of {sorted(hit[3])}")

    # ---- 8. Proportionality for solid coalitions --------------------------
    # 100 voters, 4 seats, Droop = 21.  A bloc of 45 ranks its two candidates
    # first on every ballot -- two full quotas -- and must take two seats.
    PSC = [(25, ["L1", "L2", "R1", "R2", "R3"]),
           (20, ["L2", "L1", "R1", "R2", "R3"]),
           (30, ["R1", "R2", "R3", "L1", "L2"]),
           (25, ["R2", "R3", "R1", "L1", "L2"])]
    CS = ["L1", "L2", "R1", "R2", "R3"]
    assert sum(n for n, _ in PSC) == 100 and droop(100, 4) == 21
    won = stv(PSC, CS, 4)
    assert sum(1 for c in won if c.startswith("L")) == 2
    assert sum(1 for c in won if c.startswith("R")) == 2
    ok.append("proportionality for solid coalitions: a 45-voter bloc solid for 2 candidates")
    ok.append("  takes exactly 2 of 4 seats (quota 21); the 55-voter side takes 2")

    # ---- 9. Seats change the answer, not just the count -------------------
    one = stv(LUMEN, LUMEN_C, 1)
    three = stv(LUMEN, LUMEN_C, 3)
    assert one == ["Nguyen"] and droop(75, 3) == 19
    assert three == ["Smith", "Garcia", "Lee"], three
    # Smith and Garcia clear quota on first preferences (28 and 23); Smith's
    # surplus of 9 plus part of Garcia's 4 carries Lee past 19.
    assert set(three).isdisjoint({"Nguyen"})
    ok.append("same 75 ballots, quota 19: 3 seats elect Smith, Garcia and Lee --")
    ok.append("  and NOT Nguyen, the candidate one-seat STV/IRV elects outright")

    print("all checks passed\n")
    for line in ok:
        print(("  + " + line) if not line.startswith("  ") else ("   " + line.strip()))


if __name__ == "__main__":
    main()
