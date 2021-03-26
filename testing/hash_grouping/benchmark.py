import json, time, argparse
from algo_group import create_schedules

parser = argparse.ArgumentParser()
parser.add_argument('--courses', dest='course_list', help='List of courses to create schedules from',nargs='+')
parser.add_argument('--term', dest='term', help='Term code')
parser.add_argument('--log',dest='log',help='Log results to file',default=False,action='store_true')
args = parser.parse_args()

with open(f'testing/hash_grouping/table-{args.term}.json','r') as file:
    data = json.load(file)

courses = [course for course in data if course['name'] in args.course_list]

start = time.time()
results = create_schedules(courses)
end = time.time()
duration = round(end - start, 2)

print(f'duration: {duration} seconds')
print(f'count: {len(results)}')

if args.log:
    results = [[group['crns'] for group in result] for result in results]
    results.insert(0, {'algorithm': 'hash/group', 'duration': duration + ' seconds', 'count': len(results)})
    with open(f'testing/hash_grouping/results-{args.term}.json','w') as file:
        json.dump(results, file)