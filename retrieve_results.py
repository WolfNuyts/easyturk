import os

from easyturk import interface
import pickle
from easyturk import EasyTurk
from collections import Counter

prev_results = {}
if os.path.exists('results.pkl'):
    with open('results.pkl', 'rb') as f:
        prev_results = pickle.load(f)

with open('approved_log.txt', 'r') as f:
    lines = f.readlines()
accepted_hit_ids = list(set([l[:-1] for l in lines]))

results = interface.fetch_completed_hits(accepted_hit_ids, approve=False, sandbox=False)
results.update(prev_results)

with open('results.pkl', 'wb') as f:
    pickle.dump(results, f)