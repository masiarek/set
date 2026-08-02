"""VSE benchmark: Ranked Robin vs. the field, on votesim's spatial model.

Honest ballots. For each electorate (seed x ndim x cnum), all methods run
on the same voters and candidates, so per-election comparisons are paired.
"""
import sys
import csv
import time
import numpy as np
from votesim.models import spatial

METHODS = ['plurality', 'irv', 'top_two', 'borda', 'black',
           'copeland', 'ranked_robin', 'smith_minimax', 'ranked_pairs',
           'score5', 'star5']

NDIMS = [1, 2, 3]
CNUMS = [3, 5, 7]
NUMVOTERS = 100
NSEEDS = int(sys.argv[1]) if len(sys.argv) > 1 else 2
OUT = sys.argv[2] if len(sys.argv) > 2 else 'rr_vse_pilot.csv'

t0 = time.time()
rows = []
key_vse_c = 'output.winner.regret_efficiency_candidate'
key_vse_v = 'output.winner.regret_efficiency_voter'
printed_keys = False

for ndim in NDIMS:
    for cnum in CNUMS:
        for seed in range(NSEEDS):
            e = spatial.Election(None, None, seed=seed, name='rr-vse')
            v = spatial.Voters(seed=seed, tol=1, base='linear')
            v.add_random(NUMVOTERS, ndim=ndim)
            c = spatial.Candidates(v, seed=seed)
            c.add_random(cnum, sdev=1.5)
            e.set_models(voters=v, candidates=c)
            for method in METHODS:
                r = e.run(etype=method)
                out = e._result_calc.output
                if not printed_keys:
                    ks = [k for k in out if 'regret' in k or 'ties' in k]
                    print('METRIC KEYS:', ks, flush=True)
                    printed_keys = True
                runner = e._result_calc.runner
                mtied = int(len(runner.winners_no_ties) == 0)
                mout = runner.output if isinstance(runner.output, dict) else {}
                tdeg = mout.get('tie_degree', -1)
                fin_size = 0
                deadheat = -1
                has_cw = -1
                if method == 'ranked_robin':
                    tally = mout['tally']
                    has_cw = int(np.max(tally) == cnum - 1)
                    if tdeg >= 1:
                        fin = mout['finalists']
                        fin_size = len(fin)
                        sub = mout['margin_matrix'][np.ix_(fin, fin)]
                        deadheat = int(np.all(sub == 0))
                rows.append({
                    'ndim': ndim, 'cnum': cnum, 'seed': seed,
                    'method': method,
                    'vse_c': out.get(key_vse_c), 'vse_v': out.get(key_vse_v),
                    'method_tied': mtied, 'tie_degree': tdeg,
                    'fin_size': fin_size, 'deadheat': deadheat, 'has_cw': has_cw,
                    'winner': int(runner.winners[0]),
                })

with open(OUT, 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)

n_elections = len(NDIMS) * len(CNUMS) * NSEEDS
print(f'{len(rows)} rows ({n_elections} electorates x {len(METHODS)} methods) '
      f'in {time.time()-t0:.1f}s -> {OUT}', flush=True)
