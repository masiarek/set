#!/usr/bin/env python3
"""Exhaustive burial search: Condorcet-IRV hybrids vs pure Condorcet completions.

Claim under test (Green-Armytage 2011, "Four Condorcet-Hare hybrid methods for
single-winner elections", Voting Matters 29): hybrids that finish with an IRV
stage are far more burial-resistant than pure Condorcet completions, because a
successful burial has to manufacture a cycle, and the IRV stage then tends to
eliminate the buriers' own candidate rather than reward it.

Universe enumerated, and why it is exhaustive for the claim
-----------------------------------------------------------
* Candidates: exactly three, A B C; fixed deterministic tie-break order A,B,C.
* Ballots: the 6 strict complete rankings (no truncation, no equal ranks).
* Profiles: EVERY multiset of n = 9 such ballots -- all compositions of 9
  into 6 ordered non-negative parts, C(14,5) = 2002 profiles.  Voters are
  anonymous, so a multiset IS an election: nothing at (3 candidates, 9
  voters, strict ballots) lies outside this set.  Candidate labels are NOT
  deduplicated, so the counts are closed under relabelling.  A sweep over
  n = 2..11 is printed as well, so the headline n = 9 numbers can be seen to
  be typical rather than a parity accident; n = 9 is the headline because an
  odd voter count rules out pairwise ties, matching the strict-win Condorcet
  definitions in methods.py.
* Burial move: a bloc is any k >= 1 of the voters sharing one sincere
  ranking, and the move demotes the sincere Condorcet winner (cw) to last
  while keeping the bloc's favorite on top.  With three candidates that
  forces the sincere ranking to be  f > cw > z  and the insincere one to be
  f > z > cw: rankings with cw already last have no move to make, and
  rankings with cw on top belong to cw's own supporters (their favorite
  already wins under every method that elects the CW).  So enumerating
  (eligible ranking, bloc size k) -- at most 2 rankings, k = 1..count -- is
  the COMPLETE burial universe for this profile family.
* Success: the method's sincere winner is not f, and after the burial the
  method elects f.  (Every Condorcet method's sincere winner is cw by
  definition; plain IRV's need not be.)
* Backfire (also counted): the sincere winner was cw and the burial hands
  the election to z, the bloc's sincere LAST choice.

Two easy theorems the code re-verifies on every run:
  - Burial only edits the cw-vs-z pairwise tally.  f's tallies against both
    others are untouched, and cw beat f sincerely, so f can never be MADE a
    Condorcet winner: every successful burial must manufacture a cycle
    (asserted for each success found).
  - With 3 candidates, plain IRV is completely burial-proof under this
    definition: first preferences are untouched, so round 1 is unchanged,
    and the buried ballots still sit with f until f is eliminated -- at
    which point f cannot win.  Asserted: zero IRV successes.

Baselines implemented here (pure Condorcet completions):
  - Minimax(margins): elect the candidate whose worst pairwise defeat margin
    is smallest.  https://electowiki.org/wiki/Minimax
  - Ranked Robin: most pairwise wins (ties count half), then greatest margin
    sum over the tied finalists, then over all candidates -- the exact rule
    in code/thread136-claims/verify.py (degrees=2), finished with the fixed
    candidate order if still tied.

Hybrids come from methods.py: Smith//IRV, Benham, Woodall, BTR-IRV,
Tideman's Alternative.  Plain IRV rides along as a third comparison point.

Everything is enumerated in a fixed order with deterministic tie-breaks
(earliest candidate in A,B,C order; every invoked tie-break is recorded and
excluded from the "tie-free" counts), so the output is identical on every
run.  No randomness anywhere.

Run:  python3 burial.py        (stdlib only, deterministic)
"""

import os
import sys
from fractions import Fraction
from itertools import permutations

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from methods import (pairwise, condorcet_winner, first_prefs, fmt,
                     irv, smith_irv, benham, woodall, btr_irv, tideman_alt)

CANDS = ("A", "B", "C")
ORDER = list(CANDS)
RANKINGS = tuple(sorted(permutations(CANDS)))  # 6 strict rankings, lex order


# ---------------------------------------------------------------- profiles

def compositions(n, k):
    """All k-tuples of non-negative integers summing to n, lexicographic."""
    if k == 1:
        yield (n,)
        return
    for head in range(n + 1):
        for tail in compositions(n - head, k - 1):
            yield (head,) + tail


def profile_of(counts):
    """counts (aligned with RANKINGS) -> methods.py profile."""
    return [(c, tuple((x,) for x in r)) for c, r in zip(counts, RANKINGS) if c]


# ------------------------------------------- pure Condorcet completions

def minimax(profile, cands, order=None):
    """Minimax(margins): smallest worst pairwise defeat margin wins."""
    order = list(order or cands)
    m = pairwise(profile, cands)
    score = {c: max(m[(d, c)] - m[(c, d)] for d in cands if d != c) for c in cands}
    best = min(score.values())
    tied = [c for c in cands if score[c] == best]
    w = min(tied, key=order.index)
    ties = ([] if len(tied) == 1 else
            [f"TIEBREAK (minimax): {sorted(tied, key=order.index)} tied at {best:+d}; "
             f"{w} chosen (earliest in fixed order {order})"])
    rounds = ["worst defeat margin: " + "  ".join(f"{c} {score[c]:+d}" for c in cands),
              f"-> {w} elected (smallest worst defeat)"]
    return {"winner": w, "rounds": rounds, "ties": ties}


def ranked_robin(profile, cands, order=None):
    """Ranked Robin, the thread136 rule: Copeland (pairwise ties half), then
    margin sum over the tied finalists, then over all candidates, then the
    fixed candidate order (recorded as a tie-break)."""
    order = list(order or cands)
    m = pairwise(profile, cands)
    cop = {x: sum((Fraction(1) if m[(x, y)] > m[(y, x)] else
                   Fraction(1, 2) if m[(x, y)] == m[(y, x)] else Fraction(0))
                  for y in cands if y != x)
           for x in cands}
    top = max(cop.values())
    finalists = [c for c in cands if cop[c] == top]
    rounds = ["pairwise wins (ties half): "
              + "  ".join(f"{c} {fmt(cop[c])}" for c in cands)
              + f"; finalists {{{', '.join(finalists)}}}"]
    live = list(finalists)
    if len(live) > 1:
        d1 = {c: sum(m[(c, y)] - m[(y, c)] for y in finalists if y != c)
              for c in finalists}
        hi = max(d1[c] for c in live)
        live = [c for c in live if d1[c] == hi]
        rounds.append("margin sums among finalists: "
                      + "  ".join(f"{c} {d1[c]:+d}" for c in finalists)
                      + f" -> {{{', '.join(live)}}}")
    if len(live) > 1:
        d2 = {c: sum(m[(c, y)] - m[(y, c)] for y in cands if y != c) for c in live}
        hi = max(d2.values())
        live = [c for c in live if d2[c] == hi]
        rounds.append("margin sums over all candidates: "
                      + "  ".join(f"{c} {d2[c]:+d}" for c in d2)
                      + f" -> {{{', '.join(live)}}}")
    w = min(live, key=order.index)
    ties = ([] if len(live) == 1 else
            [f"TIEBREAK (Ranked Robin): {sorted(live, key=order.index)} still tied; "
             f"{w} chosen (earliest in fixed order {order})"])
    rounds.append(f"-> {w} elected")
    return {"winner": w, "rounds": rounds, "ties": ties}


ALL_METHODS = [
    ("Minimax", minimax),
    ("RankedRobin", ranked_robin),
    ("IRV", irv),
    ("Smith//IRV", smith_irv),
    ("Benham", benham),
    ("Woodall", woodall),
    ("BTR-IRV", btr_irv),
    ("TidemanAlt", tideman_alt),
]
FN = dict(ALL_METHODS)
NAMES = [name for name, _ in ALL_METHODS]
PURE = ["Minimax", "RankedRobin"]
HYBRID = ["Smith//IRV", "Benham", "Woodall", "BTR-IRV", "TidemanAlt"]


# ---------------------------------------------------------------- the search

def burial_moves(counts, cw):
    """Every legal burial: (favorite f, bloc's last choice z, buried counts,
    sincere ranking, bloc size k).  Exhaustive per the module docstring."""
    for i, r in enumerate(RANKINGS):
        if counts[i] == 0 or r[1] != cw:
            continue
        f, z = r[0], r[2]
        j = RANKINGS.index((f, z, cw))
        for k in range(1, counts[i] + 1):
            nc = list(counts)
            nc[i] -= k
            nc[j] += k
            yield f, z, tuple(nc), r, k


def analyze(n):
    """Run every burial scenario at voter count n through all 8 methods."""
    stats = {name: {"profiles": set(), "tiefree": set(),
                    "scenarios": 0, "backfire": 0, "records": []}
             for name in NAMES}
    total = cw_profiles = scenarios = cycled = 0
    for counts in compositions(n, 6):
        total += 1
        prof = profile_of(counts)
        cw = condorcet_winner(prof, CANDS)
        if cw is None:
            continue
        cw_profiles += 1
        sincere = {name: fn(prof, CANDS, order=ORDER) for name, fn in ALL_METHODS}
        for f, z, nc, r, k in burial_moves(counts, cw):
            scenarios += 1
            bprof = profile_of(nc)
            bcw = condorcet_winner(bprof, CANDS)
            if bcw is None:
                cycled += 1
            for name, fn in ALL_METHODS:
                if sincere[name]["winner"] == f:
                    continue  # favorite already wins; nothing to gain
                res = fn(bprof, CANDS, order=ORDER)
                st = stats[name]
                if res["winner"] == f:
                    # a successful burial can never make f the CW (f's own
                    # pairwise tallies are untouched and cw beat f sincerely)
                    assert bcw is None, "successful burial must manufacture a cycle"
                    st["scenarios"] += 1
                    st["profiles"].add(counts)
                    tf = not sincere[name]["ties"] and not res["ties"]
                    if tf:
                        st["tiefree"].add(counts)
                    st["records"].append((counts, nc, r, k, cw, tf))
                elif res["winner"] == z and sincere[name]["winner"] == cw:
                    st["backfire"] += 1
    assert stats["IRV"]["scenarios"] == 0, \
        "3-candidate IRV must be burial-proof under this definition"
    return {"n": n, "total": total, "cw": cw_profiles,
            "scenarios": scenarios, "cycled": cycled, "stats": stats}


# ---------------------------------------------------------------- reporting

def report(title):
    print("\n" + "=" * 74)
    print(title)
    print("=" * 74)


def show_profile(counts, indent="    "):
    for c, r in zip(counts, RANKINGS):
        if c:
            print(f"{indent}{c}  {'>'.join(r)}")


def show_matrix(prof, indent="    "):
    m = pairwise(prof, CANDS)
    for a, b in (("A", "B"), ("A", "C"), ("B", "C")):
        if m[(a, b)] > m[(b, a)]:
            note = f"{a} beats {b}"
        elif m[(b, a)] > m[(a, b)]:
            note = f"{b} beats {a}"
        else:
            note = "tie"
        print(f"{indent}{a} v {b}: {m[(a, b)]}-{m[(b, a)]}   ({note})")
    return m


def cycle_line(m):
    """'X > Y > Z > X' for a strict 3-cycle, else None."""
    wins = {x: [y for y in CANDS if y != x and m[(x, y)] > m[(y, x)]]
            for x in CANDS}
    if not all(len(v) == 1 for v in wins.values()):
        return None
    x = "A"
    y = wins[x][0]
    z = wins[y][0]
    return f"{x} > {y} > {z} > {x}"


def show_scenario(counts, nc, r, k, cw, show):
    """Print one burial scenario in full and run the given methods on it."""
    prof, bprof = profile_of(counts), profile_of(nc)
    f, z = r[0], r[2]
    n = sum(counts)
    print(f"  {n} voters.  Sincere profile (Condorcet winner: {cw}):")
    show_profile(counts)
    print("    pairwise:")
    show_matrix(prof)
    bloc_total = counts[RANKINGS.index(r)]
    print(f"\n  Burial: {k} of the {bloc_total} voters ranking {'>'.join(r)} "
          f"demote {cw} to last, keeping {f} on top: {f}>{z}>{cw}")
    print("  Insincere profile:")
    show_profile(nc)
    print("    pairwise:")
    bm = show_matrix(bprof)
    cyc = cycle_line(bm)
    if cyc:
        print(f"    -> no Condorcet winner any more; manufactured cycle {cyc}")
    for name in show:
        s = FN[name](prof, CANDS, order=ORDER)
        b = FN[name](bprof, CANDS, order=ORDER)
        if s["winner"] != f and b["winner"] == f:
            verdict = f"burial SUCCEEDS ({f}, the bloc's favorite)"
        elif b["winner"] == cw:
            verdict = f"burial FAILS ({cw} still wins)"
        elif b["winner"] == z:
            verdict = f"burial BACKFIRES ({z}, the bloc's sincere last choice)"
        else:
            verdict = "burial fails"
        print(f"\n  {name}: sincere winner {s['winner']}, buried winner "
              f"{b['winner']}  -- {verdict}")
        for line in b["rounds"]:
            print(f"      {line}")
        for line in b["ties"]:
            print(f"      {line}")
    return prof, bprof


def find_joint_example(max_n=11):
    """Smallest-n scenario with NO tie-break anywhere in which burial succeeds
    under BOTH pure completions and fails under BOTH Benham and Smith//IRV.
    Also reports the smallest n at which any (tie-break-driven) hit exists."""
    need = ["Minimax", "RankedRobin", "Benham", "Smith//IRV"]
    first_any = None
    for n in range(2, max_n + 1):
        for counts in compositions(n, 6):
            prof = profile_of(counts)
            cw = condorcet_winner(prof, CANDS)
            if cw is None:
                continue
            sinc = {nm: FN[nm](prof, CANDS, order=ORDER) for nm in need}
            for f, z, nc, r, k in burial_moves(counts, cw):
                bprof = profile_of(nc)
                res = {nm: FN[nm](bprof, CANDS, order=ORDER) for nm in need}
                if (res["Minimax"]["winner"] == f
                        and res["RankedRobin"]["winner"] == f
                        and res["Benham"]["winner"] != f
                        and res["Smith//IRV"]["winner"] != f):
                    if first_any is None:
                        first_any = n
                    if not any(sinc[nm]["ties"] or res[nm]["ties"] for nm in need):
                        return n, (counts, nc, r, k, cw), first_any
    return None, None, first_any


def main():
    print("Exhaustive burial search over 3-candidate strict-ranking profiles.")
    print("Deterministic throughout; tie-break order A, B, C; see docstring.")

    sweep = {n: analyze(n) for n in range(2, 12)}

    # ---------------------------------------------------------------- 1
    report("1  Universe and burial-success PROFILE counts, n = 2..11\n"
           "   (a profile counts once if ANY single-ranking bloc succeeds)")
    hdr = f"  {'n':>2} {'profiles':>8} {'with CW':>7} {'blocs':>6} {'cycled':>6}"
    for name in NAMES:
        hdr += f" {name:>11}"
    print(hdr)
    for n, res in sweep.items():
        row = (f"  {n:>2} {res['total']:>8} {res['cw']:>7} "
               f"{res['scenarios']:>6} {res['cycled']:>6}")
        for name in NAMES:
            row += f" {len(res['stats'][name]['profiles']):>11}"
        print(row)
    print("  'blocs'  = burial scenarios enumerated (eligible ranking x bloc size k);")
    print("  'cycled' = scenarios where the burial destroys the Condorcet winner.")
    print("  IRV's column is 0 by theorem: burial edits no first preference, and the")
    print("  buried ballots sit with the favorite until the favorite is eliminated.")

    # ---------------------------------------------------------------- 2
    res9 = sweep[9]
    st9 = res9["stats"]
    report(f"2  Headline universe n = 9: {res9['total']} profiles, "
           f"{res9['cw']} with a Condorcet winner,\n"
           f"   {res9['scenarios']} burial scenarios ({res9['cycled']} of them "
           f"manufacture a cycle)")
    print(f"  {'method':>11} {'success profiles':>17} {'tie-free':>9} "
          f"{'scenarios':>10} {'backfires':>10}")
    for name in NAMES:
        s = st9[name]
        print(f"  {name:>11} {len(s['profiles']):>17} {len(s['tiefree']):>9} "
              f"{s['scenarios']:>10} {s['backfire']:>10}")
    print("  'tie-free' = success profiles witnessed by a scenario whose sincere AND")
    print("  buried tabulations both ran without any recorded tie-break.")
    print("  'backfires' = scenarios where the burial handed the win to z, the")
    print("  bloc's sincere LAST choice (sincere winner had been the CW).")
    smithlike = ["Smith//IRV", "Benham", "Woodall", "TidemanAlt"]
    if all(st9[s]["profiles"] == st9["Smith//IRV"]["profiles"] for s in smithlike):
        print("  Note: Smith//IRV, Benham, Woodall and Tideman's Alternative have")
        print("  IDENTICAL success sets here -- with 3 candidates and no exhausted")
        print("  ballots they all reduce to 'elect the CW, else the IRV winner of")
        print("  the cycle', so only BTR-IRV can differ (different elimination rule).")

    # ---------------------------------------------------------------- 3
    report("3  The Green-Armytage claim, against these exhaustive counts")
    pure_union = set()
    for name in PURE:
        pure_union |= st9[name]["profiles"]
    hyb_union = set()
    for name in HYBRID:
        hyb_union |= st9[name]["profiles"]
    cwn = res9["cw"]
    print(f"  Of {cwn} profiles with a sincere CW (n = 9):")
    for name in NAMES:
        share = len(st9[name]["profiles"]) / cwn
        print(f"    {name:>11}: {len(st9[name]['profiles']):>4} burial-vulnerable "
              f"({share:6.2%})")
    mm, hy = len(st9["Minimax"]["profiles"]), len(st9["Benham"]["profiles"])
    print(f"  Any pure completion vulnerable: {len(pure_union)}  |  "
          f"any hybrid vulnerable: {len(hyb_union)}")
    both = st9["Minimax"]["profiles"] & st9["RankedRobin"]["profiles"]
    saved = {p for p in both if not any(p in st9[h]["profiles"] for h in HYBRID)}
    print(f"  Profiles where BOTH pure completions fall but NO hybrid does: "
          f"{len(saved)}")
    if hy:
        print(f"  Vulnerability ratio, Minimax : Benham = {mm} : {hy} "
              f"= {mm / hy:.1f} : 1")
    print(f"  Scenario view: {res9['cycled']} burials manufacture a cycle; "
          f"Minimax rewards {st9['Minimax']['scenarios']} of them "
          f"({st9['Minimax']['scenarios'] / res9['cycled']:.1%}), Benham "
          f"{st9['Benham']['scenarios']} ({st9['Benham']['scenarios'] / res9['cycled']:.1%}).")
    print("  Mechanism check (asserted for every success): f never becomes the CW;")
    print("  every successful burial rides a manufactured cycle.  The hybrids resolve")
    print("  that cycle with IRV, whose first-preference tallies the burial cannot")
    print("  touch -- which is exactly Green-Armytage's argument.")

    # ---------------------------------------------------------------- 4
    n4, hit, n4_any = find_joint_example()
    report("4  Smallest worked example: burial beats Minimax AND Ranked Robin,\n"
           "   but Benham and Smith//IRV shrug it off")
    if hit is None:
        print("  No tie-free scenario exists for n <= 11 in this universe"
              + ("" if n4_any is None else
                 f" (tie-break-driven ones exist from n = {n4_any})") + ".")
    else:
        counts, nc, r, k, cw = hit
        if n4_any is not None and n4_any < n4:
            print(f"  Tie-break-driven hits exist from n = {n4_any} (perfect "
                  f"first-preference ties\n  broken by the fixed A,B,C order -- "
                  f"artifacts, not evidence).  The smallest\n  hit with NO "
                  f"tie-break anywhere is at n = {n4} voters:\n")
        else:
            print(f"  Found at n = {n4} voters, no tie-break involved anywhere.\n")
        prof, bprof = show_scenario(counts, nc, r, k, cw,
                                    ["Minimax", "RankedRobin", "Benham", "Smith//IRV"])
        f, z = r[0], r[2]
        ts, _ = first_prefs(prof, list(CANDS))
        tb, _ = first_prefs(bprof, list(CANDS))
        assert ts == tb
        ms, mb = pairwise(prof, CANDS), pairwise(bprof, CANDS)
        assert ms[(f, cw)] == mb[(f, cw)] and ms[(cw, f)] == mb[(cw, f)]
        print("\n  Why the IRV stage kills it: the burial changed ONLY the "
              f"{cw}-vs-{z} tally.")
        print(f"  First preferences are untouched ("
              + "  ".join(f"{c} {fmt(tb[c])}" for c in CANDS)
              + f"), and {cw} still beats {f}")
        print(f"  head-to-head {mb[(cw, f)]}-{mb[(f, cw)]}, so {f} cannot be made "
              f"the Condorcet winner -- only a")
        print(f"  cycle.  Minimax and Ranked Robin score that cycle from margins, "
              f"which the")
        print(f"  bloc just falsified in {f}'s favor.  Benham and Smith//IRV hand "
              f"the cycle to")
        print(f"  the IRV stage instead: it eliminates on sincere-looking first "
              f"preferences,")
        print(f"  where the buriers gave {f} nothing new, and the runoff restores "
              f"{cw}.")

    # ---------------------------------------------------------------- 5
    report("5  The hybrids' own weak spot: does burial EVER succeed against them?")
    any_hybrid = any(sweep[n]["stats"][h]["scenarios"] for n in sweep for h in HYBRID)
    if not any_hybrid:
        print("  Never, for any n in 2..11.")
    else:
        for h in HYBRID:
            ns = [n for n in sweep if sweep[n]["stats"][h]["records"]]
            if ns:
                n0 = min(ns)
                n0tf = min((n for n in sweep
                            if any(rec[-1] for rec in sweep[n]["stats"][h]["records"])),
                           default=None)
                print(f"  {h:>11}: first success at n = {n0} "
                      f"(first tie-free at n = {n0tf}); at n = 9 vulnerable on "
                      f"{len(st9[h]['profiles'])} of {res9['cw']} CW-profiles "
                      f"({st9[h]['scenarios']} scenarios).")
            else:
                print(f"  {h:>11}: no success anywhere in n = 2..11.")

        # Crisp characterization, checked over every Smith-like success found:
        # the sincere plain-IRV winner is ALREADY the bloc's favorite f.  (For 3
        # candidates this is a theorem: f can only win the buried cycle if the
        # CW is eliminated first, and burial changes no first preferences and
        # no f-vs-z tally, so the sincere IRV run is move-for-move the same.)
        smith_recs = 0
        for n in sweep:
            for h in ["Smith//IRV", "Benham", "Woodall", "TidemanAlt"]:
                for counts, nc, r, k, cw, tf in sweep[n]["stats"][h]["records"]:
                    assert irv(profile_of(counts), CANDS, order=ORDER)["winner"] == r[0]
                    smith_recs += 1
        btr_recs = btr_extra = 0
        for n in sweep:
            for counts, nc, r, k, cw, tf in sweep[n]["stats"]["BTR-IRV"]["records"]:
                btr_recs += 1
                if irv(profile_of(counts), CANDS, order=ORDER)["winner"] != r[0]:
                    btr_extra += 1
        print(f"\n  Characterization (verified over all {smith_recs} Smith-like "
              f"success scenarios,")
        print("  n = 2..11): in EVERY one, sincere plain IRV already elects the "
              "bloc's favorite.")
        print("  Burial never pushes Smith//IRV, Benham, Woodall or Tideman's "
              "Alternative")
        print("  anywhere IRV would not have gone sincerely -- it merely knocks "
              "the CW into a")
        print("  cycle so the Condorcet gate stops protecting the CW from the "
              "IRV stage.")
        print(f"  BTR-IRV has a second channel: its bottom-two runoff consults "
              f"the falsified")
        print(f"  pairwise matrix itself, so burial can steer eliminations too "
              f"-- in {btr_extra} of its")
        print(f"  {btr_recs} success scenarios the sincere IRV winner was NOT "
              f"the bloc's favorite.")
        print("  That is why BTR-IRV's counts sit far above the other four "
              "hybrids'.")

        # minimal tie-free hybrid-beating example, in deterministic search order
        pick = None
        for n in sorted(sweep):
            for h in HYBRID:
                for counts, nc, r, k, cw, tf in sweep[n]["stats"][h]["records"]:
                    if tf:
                        pick = (n, h, counts, nc, r, k, cw)
                        break
                if pick:
                    break
            if pick:
                break
        if pick is None:
            print("\n  No tie-free hybrid-beating scenario exists for n <= 11.")
        else:
            n_min, first_h, counts, nc, r, k, cw = pick
            print(f"\n  Minimal TIE-FREE hybrid-beating example (n = {n_min}, "
                  f"lexicographically first,\n  found under {first_h}; shown under "
                  f"every method):\n")
            show_scenario(counts, nc, r, k, cw,
                          ["Minimax", "RankedRobin", "Smith//IRV", "Benham",
                           "Woodall", "BTR-IRV", "TidemanAlt"])
            s_irv = irv(profile_of(counts), CANDS, order=ORDER)
            print(f"\n  The tell: sincere plain IRV on this profile already elects "
                  f"{s_irv['winner']} -- the")
            print(f"  buriers' favorite.  The hybrid's Condorcet gate was the only "
                  f"thing standing")
            print(f"  between {r[0]} and the win; the burial dissolves the gate "
                  f"into a cycle and")
            print(f"  the IRV stage does the rest.")

    print("\nAll assertions passed.  Re-run to reproduce byte-identical output.")


if __name__ == "__main__":
    main()
