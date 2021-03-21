import json, time

hash_length = 27
empty_hash = '000000000000000000000000000'

term = '202036'
with open(f'testing/hash_grouping/table-{term}.json','r') as file:
    data = json.load(file)

course_list = ['ENG 0802', 'IH 0851', 'IH 0852']
data = [item for item in data if item['name'] in course_list]

d = {}
for course in data:
    if course['name'] not in d:
        d[course['name']] = {}
    if course['hash'] not in d[course['name']]:
        d[course['name']][course['hash']] = []
    d[course['name']][course['hash']].append(course['crn'])

hashes = [d[key] for key in d.keys()]
courses = [list(i) for i in hashes]

# def check_times(to_check, schedule):
#     for section in [s for s in schedule if s['classtimes'] != None]:
#         for classtime_a in section['classtimes']:
#             for classtime_b in to_check['classtimes']:
#                 # Check if date ranges overlap
#                 if not (classtime_a['start_date'] > classtime_b['end_date'] or classtime_b['start_date'] > classtime_a['end_date']):
#                     # Check if days overlap
#                     if classtime_a['days'] & classtime_b['days']:
#                         # Check if times overlap
#                         if not (classtime_a['start_time'] > classtime_b['end_time'] or classtime_b['start_time'] > classtime_a['end_time']):
#                             return False
#     return True       

def parse_hash(hash_str):
    hash_strs = [hash_str[i:i+hash_length] for i in range(0, len(hash_str), hash_length)]
    return [{
        'start_date': h[:8],
        'end_date': h[8:16],
        'start_time': int(h[16:20]),
        'end_time': int(h[20:24]),
        'days': int(h[24:])
    } for h in hash_strs]


def check_times(to_check, schedule):
    for hash_str in [h[0] for h in schedule if h[0] != empty_hash]:
        for classtime_a in parse_hash(hash_str):
            for classtime_b in parse_hash(to_check):
                # Check if date ranges overlap
                if not (classtime_a['start_date'] > classtime_b['end_date'] or classtime_b['start_date'] > classtime_a['end_date']):
                    # Check if days overlap
                    if classtime_a['days'] & classtime_b['days']:
                        # Check if times overlap
                        if not (classtime_a['start_time'] > classtime_b['end_time'] or classtime_b['start_time'] > classtime_a['end_time']):
                            return False
    return True   

def create(courses):
    courses.sort(key=len)
    hashes.sort(key=len)
    course_idxs, group_idxs, temp, results = [],[],[],[]
    course_idxs.append(0)
    hash_str = courses[0][0]
    temp.append([hash_str,hashes[0][hash_str]])
    group_idxs.append(1)

    course_idx = 1

    # While there are still courses left to try
    while len(course_idxs) > 0:
        # Resume trying remaining sections
        if len(course_idxs) != len(temp):
            group_idx = group_idxs.pop()
        # Otherwise move on to the next course
        else: 
            course_idxs.append(course_idx)
            group_idx = 0
        
        current_course = courses[course_idxs[-1]]
        # Go through each section of the course and check if it works
        while group_idx < len(current_course): 
            hash_str = current_course[group_idx]
            # Add the section if it does not conflict OR if it has no meeting times (online class)
            if hash_str == empty_hash or check_times(hash_str, temp):
                temp.append([hash_str, hashes[course_idx][hash_str]])
                # Save our place so we can resume where we left off (with the next section)
                group_idxs.append(group_idx + 1)
                break
            # Otherwise, try the next section
            group_idx += 1
        
        # Once we have a section for each course, add the schedule to the list of results and remove the last section so we can try any remaining sections
        if len(temp) == len(courses):
            results.append(list(temp))
            temp.pop()
        # Otherwise, if we have tried all of the sections for this course, go back to the previous course and try any remaining sections
        elif group_idx >= len(current_course):
            course_idxs.pop()
            if len(course_idxs) > 0:
                temp.pop()
            course_idx -= 1
        # Otherwise,
        else: 
            course_idx += 1

    return results

start = time.time()
results = create(courses)
end = time.time()
duration = round(end - start, 2)
results = [[pair[1] for pair in result] for result in results]
results.insert(0, {'algorithm': 'hash/group', 'duration': str(duration) + ' seconds', 'count': len(results)})
with open(f'testing/hash_grouping/results-{term}.json','w') as file:
    json.dump(results, file)