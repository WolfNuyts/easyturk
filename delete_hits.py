from easyturk import EasyTurk

sandbox = False
enabled = True

et = EasyTurk(sandbox=sandbox)
lst = et.list_hits()
hit_ids = [i['HITId'] for i in lst]


progress = et.show_hit_progress(hit_ids)
print(progress)
counter = {'completed': 0, 'max_assignments': 0}
for hit_id in hit_ids:
    for k in counter:
        counter[k] += progress[hit_id][k]

print('')
print('------- TOTAL ----------------------------------------------------')
print(counter)

if enabled:
    for i in hit_ids:
        et.delete_hit(i)
