#!/usr/bin/env python3
"""Condorcet-IRV hybrid election methods, house-style: plain Python 3, no
dependencies beyond the standard library, exact arithmetic throughout
(fractions.Fraction, needed because equal-ranked first preferences are split
evenly), deterministic and documented tie-breaks.

Ballot model
------------
A profile is a list of (count, groups) where groups is a tuple of tuples of
candidate names: each inner tuple is one rank position, candidates inside it
are ranked EQUAL (no preference between them).  Unranked candidates are simply
absent and count below every ranked candidate.  parse_ranking() turns the
notes' string convention ("Dre=Cici" = equal rank) into this form.

Pairwise counting: a is preferred to b on a ballot iff a is ranked and either
b is unranked or a's rank index is smaller.  Equal ranks and joint omission
contribute to neither side.  (This mirrors BetterVoting's Util.ts convention,
already used in code/thread136-claims/five_cycle_repro.py.)

First preferences: a ballot's top rank group is intersected with the
continuing candidates; the first non-empty group from the top splits the
ballot's count EVENLY (exact Fractions) among its continuing members.  A
ballot with no continuing candidate ranked is exhausted and contributes to
neither tallies nor the majority denominator.

Tie-breaks: every method takes a fixed candidate order (default: the order the
candidate list was given in).  Whenever a rule must choose among tied
candidates, it chooses the one EARLIEST in that fixed order as the victim
(elimination / runoff loser), records the event in the result's "ties" list,
and the callers print it.  No randomness anywhere.

Method definitions (electowiki citations)
-----------------------------------------
- Smith set:   https://electowiki.org/wiki/Smith_set
  (smallest non-empty set whose every member pairwise-beats every non-member;
  computed by Copeland-ordered prefix scan, then verified against a brute-force
  search over all subsets whenever there are <= 8 candidates)
- IRV:         https://electowiki.org/wiki/Instant-runoff_voting
  (eliminate fewest-first-preferences, transfer, stop on a strict majority of
  continuing ballots)
- Smith//IRV:  https://electowiki.org/wiki/Smith//IRV
  (restrict to the Smith set ONCE, up front, then run plain IRV inside it)
- Benham:      https://electowiki.org/wiki/Benham%27s_method
  (before each IRV elimination, elect any remaining candidate who pairwise-
  beats all other remaining candidates)
- Woodall:     https://electowiki.org/wiki/Woodall%27s_method
  (run plain IRV eliminations; elect at the first moment only one member of
  the ORIGINAL Smith set remains among continuing candidates)
- BTR-IRV:     https://electowiki.org/wiki/BTR-IRV
  (each round the two candidates with fewest first preferences face off
  pairwise; the pairwise loser is eliminated; repeat until one remains)
- Tideman's Alternative (Alternative Smith):
               https://electowiki.org/wiki/Tideman%27s_Alternative_methods
  (repeat: restrict to the current Smith set; if one candidate remains elect
  them; otherwise eliminate the fewest-first-preferences candidate; recompute)
"""

from fractions import Fraction
from itertools import combinations


# ---------------------------------------------------------------- ballots

def parse_ranking(entries):
    """['A', 'B=C', 'D'] -> (('A',), ('B', 'C'), ('D',)).  '=' joins equal ranks."""
    return tuple(tuple(e.split("=")) for e in entries)


def parse_profile(rows):
    """[(count, [rank strings]), ...] -> internal profile."""
    return [(n, parse_ranking(r)) for n, r in rows]


def fmt(x):
    """Exact tally as a short string (Fractions shown as p/q)."""
    x = Fraction(x)
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


# ---------------------------------------------------------------- pairwise

def pairwise(profile, cands):
    """m[(a, b)] = number of ballots ranking a strictly above b."""
    m = {(a, b): 0 for a in cands for b in cands if a != b}
    for n, groups in profile:
        rank = {}
        for i, g in enumerate(groups):
            for c in g:
                rank[c] = i
        for a in cands:
            ra = rank.get(a)
            if ra is None:
                continue
            for b in cands:
                if b == a:
                    continue
                rb = rank.get(b)
                if rb is None or ra < rb:
                    m[(a, b)] += n
    return m


def beats(m, a, b):
    return m[(a, b)] > m[(b, a)]


def condorcet_winner(profile, cands):
    """The candidate who pairwise-beats every other, or None."""
    m = pairwise(profile, cands)
    for c in cands:
        if all(beats(m, c, d) for d in cands if d != c):
            return c
    return None


def copeland(profile, cands):
    """Wins + ties/2 (used only to order the Smith prefix scan)."""
    m = pairwise(profile, cands)
    out = {}
    for c in cands:
        w = sum(1 for d in cands if d != c and m[(c, d)] > m[(d, c)])
        t = sum(1 for d in cands if d != c and m[(c, d)] == m[(d, c)])
        out[c] = Fraction(w) + Fraction(t, 2)
    return out


def smith_set(profile, cands):
    """Smallest set S with every member of S pairwise-beating every candidate
    outside S (the beats-all-outside definition).  Smith members provably have
    strictly higher Copeland scores than non-members, so the set is a prefix of
    the Copeland ordering; we scan prefixes and, for <= 8 candidates, verify
    against a brute-force search over ALL subsets, smallest first."""
    cands = list(cands)
    m = pairwise(profile, cands)

    def dominant(S):
        return all(beats(m, a, b) for a in S for b in cands if b not in S)

    cop = copeland(profile, cands)
    order = sorted(cands, key=lambda c: (-cop[c], cands.index(c)))
    result = None
    for k in range(1, len(cands) + 1):
        if dominant(order[:k]):
            result = frozenset(order[:k])
            break
    assert result is not None  # the full set is always dominant (vacuously)

    if len(cands) <= 8:  # brute-force verification over all subsets
        brute = None
        for k in range(1, len(cands) + 1):
            for S in combinations(cands, k):
                if dominant(S):
                    brute = frozenset(S)
                    break
            if brute is not None:
                break
        assert brute == result, (brute, result)
    return result


# ---------------------------------------------------------------- IRV core

def first_prefs(profile, alive):
    """(tallies, active) — top continuing rank group splits the ballot evenly;
    exhausted ballots (no continuing candidate ranked) count for nothing."""
    t = {c: Fraction(0) for c in alive}
    active = Fraction(0)
    for n, groups in profile:
        for g in groups:
            cont = [c for c in g if c in alive]
            if cont:
                share = Fraction(n, len(cont))
                for c in cont:
                    t[c] += share
                active += n
                break
    return t, active


def _tally_line(t, alive):
    return "  ".join(f"{c} {fmt(t[c])}" for c in alive)


def _pick_victim(tied, order, ties, context):
    """Deterministic tie-break: the tied candidate EARLIEST in the fixed order
    is the victim.  Records the event whenever there was a real tie."""
    victim = min(tied, key=order.index)
    if len(tied) > 1:
        ties.append(f"TIEBREAK ({context}): {sorted(tied, key=order.index)} tied; "
                    f"{victim} chosen (earliest in fixed order {order})")
    return victim


def _result(winner, rounds, ties):
    return {"winner": winner, "rounds": rounds, "ties": ties}


def irv(profile, cands, order=None):
    """Plain IRV with the strict-majority-of-continuing-ballots stop."""
    order = list(order or cands)
    alive = list(cands)
    rounds, ties = [], []
    while True:
        t, active = first_prefs(profile, alive)
        if len(alive) == 1:
            rounds.append(f"[{_tally_line(t, alive)}] -> {alive[0]} elected (last remaining)")
            return _result(alive[0], rounds, ties)
        lead = max(alive, key=lambda c: t[c])
        if t[lead] * 2 > active:
            rounds.append(f"[{_tally_line(t, alive)}] -> {lead} elected "
                          f"(majority of {fmt(active)} continuing ballots)")
            return _result(lead, rounds, ties)
        lo = min(t[c] for c in alive)
        tied = [c for c in alive if t[c] == lo]
        out = _pick_victim(tied, order, ties, "IRV elimination")
        rounds.append(f"[{_tally_line(t, alive)}] -> eliminate {out}")
        alive.remove(out)


def smith_irv(profile, cands, order=None):
    """Smith//IRV: restrict to the Smith set once, then plain IRV inside it."""
    order = list(order or cands)
    S = smith_set(profile, cands)
    inside = [c for c in cands if c in S]
    sub = irv(profile, inside, order=order)
    rounds = [f"Smith set = {{{', '.join(inside)}}}; run IRV inside it"] + sub["rounds"]
    return _result(sub["winner"], rounds, sub["ties"])


def benham(profile, cands, order=None):
    """Benham: before each IRV elimination, elect any remaining candidate who
    pairwise-beats all other remaining candidates."""
    order = list(order or cands)
    alive = list(cands)
    rounds, ties = [], []
    while True:
        m = pairwise(profile, alive)
        for c in alive:
            if all(beats(m, c, d) for d in alive if d != c):
                rounds.append(f"{c} pairwise-beats all of {{{', '.join(x for x in alive if x != c)}}}"
                              if len(alive) > 1 else f"{c} is the last remaining candidate")
                rounds.append(f"-> {c} elected")
                return _result(c, rounds, ties)
        t, _ = first_prefs(profile, alive)
        lo = min(t[c] for c in alive)
        tied = [c for c in alive if t[c] == lo]
        out = _pick_victim(tied, order, ties, "Benham elimination")
        rounds.append(f"no pairwise champion; [{_tally_line(t, alive)}] -> eliminate {out}")
        alive.remove(out)


def woodall(profile, cands, order=None):
    """Woodall: plain IRV eliminations (no majority stop); elect at the first
    moment only one member of the ORIGINAL Smith set is still continuing."""
    order = list(order or cands)
    S0 = smith_set(profile, cands)
    alive = list(cands)
    rounds = [f"original Smith set = {{{', '.join(c for c in cands if c in S0)}}}"]
    ties = []
    while True:
        smith_alive = [c for c in alive if c in S0]
        if len(smith_alive) == 1:
            rounds.append(f"only Smith member continuing -> {smith_alive[0]} elected")
            return _result(smith_alive[0], rounds, ties)
        t, _ = first_prefs(profile, alive)
        lo = min(t[c] for c in alive)
        tied = [c for c in alive if t[c] == lo]
        out = _pick_victim(tied, order, ties, "Woodall elimination")
        rounds.append(f"[{_tally_line(t, alive)}] -> eliminate {out}")
        alive.remove(out)


def btr_irv(profile, cands, order=None):
    """BTR-IRV: each round the two lowest first-preference candidates face off
    pairwise and the pairwise loser is eliminated; repeat until one remains.
    Ties: equal tallies at the bottom-two boundary put the candidate EARLIEST
    in the fixed order into the runoff; a tied runoff eliminates the earlier."""
    order = list(order or cands)
    alive = list(cands)
    rounds, ties = [], []
    while len(alive) > 1:
        t, _ = first_prefs(profile, alive)
        ranked = sorted(alive, key=lambda c: (t[c], order.index(c)))
        b1, b2 = ranked[0], ranked[1]
        if len(ranked) > 2 and t[ranked[1]] == t[ranked[2]]:
            ties.append(f"TIEBREAK (BTR bottom-two selection): {ranked[1]} and {ranked[2]} "
                        f"tied at {fmt(t[ranked[1]])}; {ranked[1]} enters the runoff "
                        f"(earlier in fixed order {order})")
        m = pairwise(profile, [b1, b2])
        if m[(b1, b2)] > m[(b2, b1)]:
            out = b2
        elif m[(b2, b1)] > m[(b1, b2)]:
            out = b1
        else:
            out = _pick_victim([b1, b2], order, ties, "BTR runoff (pairwise tie)")
        rounds.append(f"[{_tally_line(t, alive)}] bottom two {b1} v {b2}: pairwise "
                      f"{fmt(m[(b1, b2)])}-{fmt(m[(b2, b1)])} -> eliminate {out}")
        alive.remove(out)
    rounds.append(f"-> {alive[0]} elected (last remaining)")
    return _result(alive[0], rounds, ties)


def tideman_alt(profile, cands, order=None):
    """Tideman's Alternative (Alternative Smith): repeat — restrict to the
    current Smith set; if one candidate remains elect them; otherwise eliminate
    the fewest-first-preferences candidate among the remaining; recompute."""
    order = list(order or cands)
    alive = list(cands)
    rounds, ties = [], []
    while True:
        S = smith_set(profile, alive)
        if len(S) == 1:
            (w,) = S
            rounds.append(f"Smith set of {{{', '.join(alive)}}} = {{{w}}} -> {w} elected")
            return _result(w, rounds, ties)
        if set(alive) != S:
            dropped = [c for c in alive if c not in S]
            alive = [c for c in alive if c in S]
            rounds.append(f"restrict to Smith set {{{', '.join(alive)}}} "
                          f"(drops {', '.join(dropped)})")
        t, _ = first_prefs(profile, alive)
        lo = min(t[c] for c in alive)
        tied = [c for c in alive if t[c] == lo]
        out = _pick_victim(tied, order, ties, "Tideman-Alternative elimination")
        rounds.append(f"[{_tally_line(t, alive)}] -> eliminate {out}")
        alive.remove(out)


METHODS = [
    ("IRV", irv),
    ("Smith//IRV", smith_irv),
    ("Benham", benham),
    ("Woodall", woodall),
    ("BTR-IRV", btr_irv),
    ("TidemanAlt", tideman_alt),
]

HYBRIDS = [name for name, _ in METHODS if name != "IRV"]
