#!/usr/bin/env python3
"""Verify the Condorcet-IRV hybrid methods against the library's profiles.

Runs plain IRV plus five hybrids (Smith//IRV, Benham, Woodall, BTR-IRV,
Tideman's Alternative) on every ballot-complete profile in the library and
checks:

  (a) every hybrid elects the Condorcet winner whenever one exists;
  (b) plain IRV fails to elect the CW on the known center-squeeze profiles
      (cross-checked against each note's recorded winners);
  (c) on the cycle profiles the hybrids' DISAGREEMENTS with each other and
      with IRV are reported — that divergence is the interesting content;
  (d) profiles where all five hybrids agree with each other but not with IRV
      are noted.

Two library profiles are ballot-free and therefore skipped, as their notes
say a verifier must: thread136-3cycle (published only as a pairwise-matrix
PNG; no reconstruction exists) and alaska-2022 (qualitative description only;
real ballots live in the linked arXiv analysis).

Run:  python3 verify.py
No dependencies beyond the standard library.  Every claim is printed as a
PASS/FAIL check; any FAIL makes the script exit non-zero.
"""

import sys
from fractions import Fraction

from methods import (METHODS, HYBRIDS, parse_profile, pairwise, beats,
                     condorcet_winner, copeland, smith_set, fmt)

# ---------------------------------------------------------------- profiles
# Extracted verbatim from the library notes/code named in each entry.

PROFILES = [
    {
        # LeGrand's 99-voter center squeeze (hare-center-squeeze-examples.md):
        # CW Emil is last on first preferences by one vote; Hare elects Dana.
        "name": "legrand-99-hare-squeeze",
        "candidates": ["Dana", "Emil", "Fay"],
        "rows": [
            (34, ["Dana", "Emil", "Fay"]),
            (33, ["Fay", "Emil", "Dana"]),
            (16, ["Emil", "Dana", "Fay"]),
            (16, ["Emil", "Fay", "Dana"]),
        ],
        "n": 99,
        "known_cw": "Emil",
        "known_irv": "Dana",
        "center_squeeze": True,
    },
    {
        # The calculator's 100-voter left-right spectrum
        # (hare-center-squeeze-examples.md): CW Center LEADS first preferences
        # (26) and still loses under Hare; Hare elects FarLeft 51-49.
        "name": "legrand-spectrum-100",
        "candidates": ["FarLeft", "Left", "Center", "Right", "FarRight"],
        "rows": [
            (18, ["FarLeft", "Left", "Center", "Right", "FarRight"]),
            (16, ["Left", "FarLeft", "Center", "Right", "FarRight"]),
            (17, ["Center", "Left", "Right", "FarLeft", "FarRight"]),
            (9,  ["Center", "Right", "FarRight", "Left", "FarLeft"]),
            (19, ["Right", "FarRight", "Center", "Left", "FarLeft"]),
            (21, ["FarRight", "Right", "Center", "Left", "FarLeft"]),
        ],
        "n": 100,
        "known_cw": "Center",
        "known_irv": "FarLeft",
        "center_squeeze": True,
    },
    {
        # Lumen Learning senior-class-president exercise
        # (code/lumen-75-ballot/verify.py): CW Garcia, IRV elects Nguyen.
        "name": "lumen-75",
        "candidates": ["Garcia", "Lee", "Nguyen", "Smith"],
        "rows": [
            (20, ["Garcia", "Lee", "Nguyen", "Smith"]),
            (3,  ["Garcia", "Nguyen", "Lee", "Smith"]),
            (8,  ["Lee", "Nguyen", "Garcia", "Smith"]),
            (16, ["Nguyen", "Garcia", "Lee", "Smith"]),
            (28, ["Smith", "Lee", "Garcia", "Nguyen"]),
        ],
        "n": 75,
        "known_cw": "Garcia",
        "known_irv": "Nguyen",
        "center_squeeze": True,
    },
    {
        # LeGrand's 921-voter, 5-candidate no-CW example
        # (legrand-ranked-ballot-methods.md): cycle Brad > Erin > Dave > Brad;
        # Cora is the Condorcet loser, losing every matchup 460-461.
        "name": "legrand-921-four-winners",
        "candidates": ["Abby", "Brad", "Cora", "Dave", "Erin"],
        "rows": [
            (98,  ["Abby", "Cora", "Erin", "Dave", "Brad"]),
            (64,  ["Brad", "Abby", "Erin", "Cora", "Dave"]),
            (12,  ["Brad", "Abby", "Erin", "Dave", "Cora"]),
            (98,  ["Brad", "Erin", "Abby", "Cora", "Dave"]),
            (13,  ["Brad", "Erin", "Abby", "Dave", "Cora"]),
            (125, ["Brad", "Erin", "Dave", "Abby", "Cora"]),
            (124, ["Cora", "Abby", "Erin", "Dave", "Brad"]),
            (76,  ["Cora", "Erin", "Abby", "Dave", "Brad"]),
            (21,  ["Dave", "Abby", "Brad", "Erin", "Cora"]),
            (30,  ["Dave", "Brad", "Abby", "Erin", "Cora"]),
            (98,  ["Dave", "Brad", "Erin", "Cora", "Abby"]),
            (139, ["Dave", "Cora", "Abby", "Brad", "Erin"]),
            (23,  ["Dave", "Cora", "Brad", "Abby", "Erin"]),
        ],
        "n": 921,
        "known_cw": None,
        "cycle": True,
    },
    {
        # Ranked Robin thread's 5-cycle showcase, reconstructed as 69 real
        # ballots (code/thread136-claims/five_cycle_repro.py).  '=' joins equal
        # ranks; unranked candidates are omitted and count below all ranked.
        "name": "thread136-5cycle-69",
        "candidates": ["Dre", "Edith", "Frank", "Ben", "Abby", "Cici"],
        "rows": [
            (9, ["Abby", "Frank", "Dre=Cici", "Ben"]),
            (8, ["Abby", "Dre", "Edith=Frank", "Cici", "Ben"]),
            (8, ["Dre=Edith", "Ben=Abby", "Frank=Cici"]),
            (7, ["Ben", "Edith", "Frank", "Dre", "Abby"]),
            (6, ["Frank", "Ben", "Dre", "Edith", "Cici"]),
            (6, ["Edith", "Frank", "Ben=Abby", "Dre"]),
            (6, ["Ben=Cici", "Edith", "Abby", "Frank"]),
            (5, ["Frank=Abby", "Dre", "Cici", "Edith=Ben"]),
            (4, ["Edith", "Cici", "Ben", "Frank", "Dre"]),
            (2, ["Edith=Ben", "Frank", "Dre", "Abby"]),
            (2, ["Dre=Edith", "Ben", "Cici"]),
            (2, ["Cici", "Dre=Ben", "Edith", "Abby"]),
            (2, ["Frank", "Cici", "Dre", "Abby"]),
            (1, ["Cici", "Frank", "Dre", "Abby", "Edith"]),
            (1, ["Ben", "Cici", "Abby", "Frank"]),
        ],
        "n": 69,
        "known_cw": None,
        "cycle": True,
    },
]

SKIPPED = [
    ("thread136-3cycle", "pairwise matrix only (PNG); no ballot profile exists"),
    ("alaska-2022", "qualitative note only; no ballot counts to transcribe"),
]

# ---------------------------------------------------------------- checking

failures = []


def check(label, cond, detail=""):
    tag = "PASS" if cond else "FAIL"
    if not cond:
        failures.append(label)
    print(f"{tag}  {label}" + (f"  [{detail}]" if detail and not cond else ""))


def main():
    for p in PROFILES:
        p["profile"] = parse_profile(p["rows"])

    # ---- engine validation against each note's recorded numbers ----------
    print("== engine validation against the notes' recorded numbers ==")
    for p in PROFILES:
        total = sum(n for n, _ in p["profile"])
        check(f"{p['name']}: ballot total is {p['n']}", total == p["n"], f"got {total}")

    p99 = next(p for p in PROFILES if p["name"] == "legrand-99-hare-squeeze")
    m = pairwise(p99["profile"], p99["candidates"])
    check("legrand-99: Emil beats Dana 65-34 and Fay 66-33",
          (m[("Emil", "Dana")], m[("Dana", "Emil")]) == (65, 34)
          and (m[("Emil", "Fay")], m[("Fay", "Emil")]) == (66, 33), str(m))

    psp = next(p for p in PROFILES if p["name"] == "legrand-spectrum-100")
    m = pairwise(psp["profile"], psp["candidates"])
    check("spectrum-100: Center beats all four rivals with 60-66 support",
          all(beats(m, "Center", d) and 60 <= m[("Center", d)] <= 66
              for d in psp["candidates"] if d != "Center"), str(m))

    plu = next(p for p in PROFILES if p["name"] == "lumen-75")
    m = pairwise(plu["profile"], plu["candidates"])
    check("lumen-75: Garcia's matchups are 39-36, 51-24, 47-28",
          (m[("Garcia", "Lee")], m[("Garcia", "Nguyen")], m[("Garcia", "Smith")]) == (39, 51, 47)
          and (m[("Lee", "Garcia")], m[("Nguyen", "Garcia")], m[("Smith", "Garcia")]) == (36, 24, 28))

    p921 = next(p for p in PROFILES if p["name"] == "legrand-921-four-winners")
    m = pairwise(p921["profile"], p921["candidates"])
    check("legrand-921: cycle Brad>Erin 623, Erin>Dave 610, Dave>Brad 609",
          (m[("Brad", "Erin")], m[("Erin", "Dave")], m[("Dave", "Brad")]) == (623, 610, 609),
          f"got {m[('Brad', 'Erin')]}, {m[('Erin', 'Dave')]}, {m[('Dave', 'Brad')]}")
    check("legrand-921: Cora loses all four matchups exactly 460-461",
          all(m[("Cora", d)] == 460 and m[(d, "Cora")] == 461
              for d in p921["candidates"] if d != "Cora"))
    cop = copeland(p921["profile"], p921["candidates"])
    check("legrand-921: Copeland Abby 3, Brad 3, Dave 2, Erin 2, Cora 0",
          cop == {"Abby": 3, "Brad": 3, "Cora": 0, "Dave": 2, "Erin": 2}, str(cop))

    p5c = next(p for p in PROFILES if p["name"] == "thread136-5cycle-69")
    cop = copeland(p5c["profile"], p5c["candidates"])
    check("5cycle-69: Copeland five-way tie at 3 (Cici 0)",
          cop == {"Dre": 3, "Edith": 3, "Frank": 3, "Ben": 3, "Abby": 3, "Cici": 0}, str(cop))
    m = pairwise(p5c["profile"], p5c["candidates"])
    finalists = ["Dre", "Edith", "Frank", "Ben", "Abby"]
    msum = {c: sum(m[(c, d)] - m[(d, c)] for d in finalists if d != c) for c in finalists}
    check("5cycle-69: finalist margin sums Edith +20, Frank +15, Ben -1, Abby -15, Dre -19",
          msum == {"Edith": 20, "Frank": 15, "Ben": -1, "Abby": -15, "Dre": -19}, str(msum))

    # ---- Condorcet winners and Smith sets ---------------------------------
    print("\n== Condorcet winners and Smith sets ==")
    for p in PROFILES:
        cw = condorcet_winner(p["profile"], p["candidates"])
        p["cw"] = cw
        p["smith"] = smith_set(p["profile"], p["candidates"])
        smith_str = "{" + ", ".join(c for c in p["candidates"] if c in p["smith"]) + "}"
        print(f"  {p['name']}: CW = {cw}, Smith = {smith_str}")
        check(f"{p['name']}: CW matches the note ({p['known_cw']})", cw == p["known_cw"],
              f"got {cw}")
        if cw is not None:
            check(f"{p['name']}: Smith set is exactly {{{cw}}}", p["smith"] == {cw})

    check("legrand-921: Smith set is everyone but Condorcet-loser Cora",
          p921["smith"] == {"Abby", "Brad", "Dave", "Erin"})
    check("5cycle-69: Smith set is the five Copeland-tied finalists (not Cici)",
          p5c["smith"] == set(finalists))

    # ---- run every method on every profile --------------------------------
    for p in PROFILES:
        p["res"] = {name: fn(p["profile"], p["candidates"]) for name, fn in METHODS}

    print("\n== results table (winner by method x profile) ==")
    names = [name for name, _ in METHODS]
    wcol = max(len(p["name"]) for p in PROFILES) + 2
    print(" " * wcol + "  ".join(f"{n:<11}" for n in ["CW"] + names))
    for p in PROFILES:
        row = [str(p["cw"])] + [p["res"][n]["winner"] for n in names]
        print(f"{p['name']:<{wcol}}" + "  ".join(f"{w:<11}" for w in row))

    # ---- tie-breaks that fired --------------------------------------------
    print("\n== tie-breaks that fired ==")
    fired = False
    for p in PROFILES:
        for name in names:
            for t in p["res"][name]["ties"]:
                fired = True
                print(f"  {p['name']} / {name}: {t}")
    if not fired:
        print("  (none — every elimination and runoff was decided by the numbers)")

    # ---- claim (a): hybrids elect the CW whenever one exists --------------
    print("\n== claim (a): every hybrid elects the Condorcet winner when one exists ==")
    for p in PROFILES:
        if p["cw"] is None:
            continue
        for h in HYBRIDS:
            w = p["res"][h]["winner"]
            check(f"{p['name']}: {h} elects CW {p['cw']}", w == p["cw"], f"got {w}")

    # ---- claim (b): plain IRV fails the CW on the center-squeeze profiles --
    print("\n== claim (b): plain IRV misses the CW on the center-squeeze profiles ==")
    for p in PROFILES:
        if not p.get("center_squeeze"):
            continue
        w = p["res"]["IRV"]["winner"]
        check(f"{p['name']}: IRV elects {p['known_irv']} (note's recorded winner), not CW {p['cw']}",
              w == p["known_irv"] and w != p["cw"], f"got {w}")

    # ---- claim (c): divergence on the cycle profiles ----------------------
    print("\n== claim (c): where the methods disagree on the cycle profiles ==")
    for p in PROFILES:
        if not p.get("cycle"):
            continue
        groups = {}
        for name in names:
            groups.setdefault(p["res"][name]["winner"], []).append(name)
        print(f"  {p['name']}:")
        for w, ms in sorted(groups.items(), key=lambda kv: -len(kv[1])):
            print(f"    {w}: {', '.join(ms)}")
        if len(groups) > 1:
            print(f"    -> {len(groups)} distinct winners across the six methods")
        else:
            print("    -> unanimous despite the cycle")

    # ---- claim (d): hybrids unanimous but different from IRV --------------
    print("\n== claim (d): profiles where all five hybrids agree and IRV differs ==")
    any_d = False
    for p in PROFILES:
        hw = {p["res"][h]["winner"] for h in HYBRIDS}
        iw = p["res"]["IRV"]["winner"]
        if len(hw) == 1 and iw not in hw:
            any_d = True
            (w,) = hw
            note = f"CW {p['cw']}" if p["cw"] else "no CW"
            print(f"  {p['name']}: hybrids unanimous on {w}, IRV says {iw} ({note})")
    if not any_d:
        print("  (none)")
    check("claim (d) holds on every profile with a CW (hybrids unanimous on CW, IRV elsewhere)",
          all(len({p["res"][h]["winner"] for h in HYBRIDS}) == 1
              and p["res"]["IRV"]["winner"] != p["cw"]
              for p in PROFILES if p["cw"] is not None))

    # ---- round-by-round traces for the two headline profiles --------------
    for pname in ["lumen-75", "legrand-99-hare-squeeze"]:
        p = next(q for q in PROFILES if q["name"] == pname)
        print(f"\n== round-by-round: {pname} ==")
        for name in names:
            print(f"  {name} -> {p['res'][name]['winner']}")
            for line in p["res"][name]["rounds"]:
                print(f"      {line}")

    # ---- skipped profiles -------------------------------------------------
    print("\n== skipped profiles (no ballots exist, per their notes) ==")
    for name, why in SKIPPED:
        print(f"  {name}: {why}")

    print()
    if failures:
        print(f"{len(failures)} CHECK(S) FAILED")
        for f in failures:
            print("  -", f)
        sys.exit(1)
    print("all checks passed")


if __name__ == "__main__":
    main()
