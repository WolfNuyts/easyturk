from easyturk import EasyTurk

sandbox = False

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

et = EasyTurk(sandbox=sandbox)
progress = et.show_hit_progress(hit_ids)
print(progress)
counter = {'completed': 0, 'max_assignments': 0}
for hit_id in hit_ids:
    for k in counter:
        counter[k] += progress[hit_id][k]

print('')
print('------- TOTAL ----------------------------------------------------')
print(counter)
print('rejected assignments: {}'.format(len(rejected_hit_ids)))
print('accepted assignments: {}'.format(len(accepted_hit_ids)))
