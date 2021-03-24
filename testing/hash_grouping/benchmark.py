import json, time, sys, argparse
from algo_group import create_schedules

parser = argparse.ArgumentParser()
parser.add_argument('--courses', dest='course_list', help='List of courses to create schedules from',nargs='+')
parser.add_argument('--term', dest='term', help='Term code')
args = parser.parse_args()

with open(f'testing/hash_grouping/table-{args.term}.json','r') as file:
    data = json.load(file)

data = [item for item in data if item['name'] in args.course_list]

d = {}
for course in data:
    if course['name'] not in d:
        d[course['name']] = {}
    if course['hash'] not in d[course['name']]:
        d[course['name']][course['hash']] = {'hash': course['hash'], 'classtimes': course['classtimes'], 'crns': []}
    d[course['name']][course['hash']]['crns'].append(course['crn'])

courses = [[d[key][i] for i in d[key]] for key in d]

start = time.time()
results = create_schedules(courses)
end = time.time()
duration = round(end - start, 2)
results = [[group['crns'] for group in result] for result in results]
results.insert(0, {'algorithm': 'hash/group', 'duration': str(duration) + ' seconds', 'count': len(results)})
with open(f'testing/hash_grouping/results-{args.term}.json','w') as file:
    json.dump(results, file)