import json, time, argparse
from algo_matrix import create_schedules
import numpy as np

matrix_shape = (12*31*24*60)
packed_64_shape = (8370)
packed_32_shape = (16740)

parser = argparse.ArgumentParser()
parser.add_argument('--courses', dest='course_list', help='List of courses to create schedules from',nargs='+')
parser.add_argument('--term', dest='term', help='Term code')
parser.add_argument('--log',dest='log',help='Log results to file',default=False,action='store_true')
args = parser.parse_args()

file = f'table-{args.term}.json'
with open(file,'r') as file:
    data = json.load(file)

courses = [course for course in data if course['name'] in args.course_list]

start_total = time.time()
for course in courses:
    for group in course['groups']:
        if len(group['matrix']) != 0:
            group['matrix'] = np.array(group['matrix'],dtype=np.uint32).view(np.uint64)

start = time.time()
results = create_schedules(courses)
end = time.time()
duration = round(end - start, 2)
total_duration = round(end - start_total,2)

print(f'algorithm duration: {duration} seconds')
print(f'total duration: {total_duration} seconds')
print(f'count: {len(results)}')

if args.log:
    results = [[group['crns'] for group in result] for result in results]
    results.insert(0, {'algorithm': 'matrix', 'duration': str(duration) + ' seconds', 'count': len(results)})
    with open(f'results-{args.term}.json','w') as file:
        json.dump(results, file, indent=2)