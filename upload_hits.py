import os
import pickle

from easyturk import EasyTurk, interface


def launch_coreference_bbox(data, reward=1.00, tasks_per_hit=10, sandbox=False):
    """Launches HITs to ask workers to coreference bboxes.

    Args:
        data: List containing image urls for the task.
        reward: A postive valued dollar amount per task.
        tasks_per_hit: Number of images per hit.
        sandbox: Whether to interact on sandbox or production.

    Returns:
        A list of hit ids that have been launched.
    """
    et = EasyTurk(sandbox=sandbox)
    template = 'coreference_bbox.html'
    hit_ids = []
    i = 0
    while i < len(data):
        hit = et.launch_hit(
            template,
            data[i:i+tasks_per_hit],
            reward=reward,
            title='Annotate bounding boxes',
            description=('Annotate bounding boxes with their corresponding sentence parts.'),
            keywords='image, caption, text, bounding box',
            country=country,
            frame_height=3400,
            max_assignments=1,
            hits_approved=50,
            percent_approved=95)
        hit_id = hit['HIT']['HITId']
        hit_ids.append(hit_id)
        i += tasks_per_hit
    return hit_ids


tasks_per_hit = 10
sandbox = False
reward = 1.05
country = 'US'
max_instances = 500

et = EasyTurk(sandbox=sandbox)
print(et.get_account_balance())

if sandbox:
    log_file_name = 'log_sandbox.txt'
else:
    log_file_name = 'log.txt'

if os.path.isfile(log_file_name):
    with open(log_file_name, 'r') as f:
        lines = f.readlines()
    used_ids = list(set([int(l.split(' - ')[0]) for l in lines]))
else:
    used_ids = []

with open('coref/instances.pkl', 'rb') as f:
    instances = pickle.load(f)

data = []
for img_id in instances:
    if img_id in used_ids:
        continue
    data.append({'img_id': img_id,
                 'url': 'https://mturk-coco-coref.s3.eu-west-3.amazonaws.com/images/{}.jpg'.format(img_id),
                 'sentences': [i.encode('ascii','ignore') for i in instances[img_id]['sentences']]})

    if len(data) >= max_instances:
        break

hit_ids = launch_coreference_bbox(data, reward=reward, tasks_per_hit=tasks_per_hit, sandbox=sandbox)
print(hit_ids)

log_file = open(log_file_name, 'a')
for i, d in enumerate(data):
    log_file.write('{} - {}\n'.format(d['img_id'], hit_ids[i//tasks_per_hit]))
