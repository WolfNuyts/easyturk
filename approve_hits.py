from easyturk import interface
from easyturk import EasyTurk
from collections import Counter

sandbox = False
enable = True

if sandbox:
    log_file = 'log_sandbox.txt'
else:
    log_file = 'log.txt'

with open(log_file, 'r') as f:
    lines = f.readlines()
hit_ids = list(set([l.split(' - ')[-1][:-1] for l in lines]))

with open('rejected_log.txt', 'r') as f:
    lines = f.readlines()
rejected_hit_ids = list(set([l[:-1] for l in lines]))

with open('approved_log.txt', 'r') as f:
    lines = f.readlines()
accepted_hit_ids = list(set([l[:-1] for l in lines]))

hit_ids = [i for i in hit_ids if i not in (accepted_hit_ids + rejected_hit_ids)]

results = interface.fetch_completed_hits(hit_ids, approve=False, sandbox=sandbox)

worker_count = {}
result_count = {}
empty_ids = []
auto_filled_ids = []
reject_assignments = []
accepted_assignments = []
rejected_hitids = []
accepted_hitids = []
for i in results:
    dict = results[i][0]
    worker_count[dict['worker_id']] = worker_count.setdefault(dict['worker_id'], 0) + 1
    out = dict['output'][1:]

    c = 0
    obj_nrs1 = []
    obj_nrs2 = []
    for r in out:
        a = r['results']['sentence']
        if a != 'None':
            c += 1
            obj_nrs1.append(r['results']['Objectnr1'])
            obj_nrs2.append(r['results']['Objectnr2'])

    result_count.setdefault(dict['worker_id'], [0, 0])
    result_count[dict['worker_id']][0] += c
    result_count[dict['worker_id']][1] += len(out)

    if c == 0:
        empty_ids.append(i)
        rejected_hitids.append(i)
        reject_assignments.append(dict['assignment_id'])
    elif max(Counter(obj_nrs1).values() or [0]) >= 8 or max(Counter(obj_nrs2).values() or [0]) >= 8:
        auto_filled_ids.append(i)
        rejected_hitids.append(i)
        reject_assignments.append(dict['assignment_id'])
    else:
        accepted_hitids.append(i)
        accepted_assignments.append(dict['assignment_id'])


et = EasyTurk(sandbox=sandbox)
if enable:
    if not sandbox:
        log_file = open('approved_log.txt', 'a')
        for i in accepted_hitids:
            log_file.write('{}\n'.format(i))
        log_file = open('rejected_log.txt', 'a')
        for i in rejected_hitids:
            log_file.write('{}\n'.format(i))

    for ass_id in reject_assignments:
        et.reject_assignment(ass_id)
    for ass_id in accepted_assignments:
        et.approve_assignment(ass_id)