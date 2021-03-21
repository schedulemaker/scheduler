import json

filename = 'temple-202036'
with open(f'testing/{filename}-clean.json','r') as file:
    data = json.load(file)

days = [
    'saturday',
    'sunday',
    'monday',
    'tuesday',
    'wednesday',
    'thursday',
    'friday'
]

for course in data:
    course['name'] = f'{course["subject"]} {course["courseNumber"]}'
    course_hashes = []
    if course['meetingsFaculty']:
        for mf in course['meetingsFaculty']:
            mt = mf['meetingTime']
            mt_days = int(''.join(['1' if mt[d] else '0' for d in days]),2)
            mt_time = f'{mt["beginTime"]}{mt["endTime"]}'
            mt_date = f'{mt["startDate"].replace("/","")}{mt["endDate"].replace("/","")}'
            mt_hash = f'{mt_date}{mt_time}{mt_days}'
            course_hashes.append(mt_hash)
        course_hashes.sort()
        course['hash'] = ''.join(course_hashes)
    else:
        course['hash'] = '0000000000000000000000000'

d = {}
d_times = {}
for course in data:
    if course['name'] not in d:
        d[course['name']] = {}
    if course['hash'] not in d[course['name']]:
        d[course['name']][course['hash']] = []
    if course['hash'] not in d_times:
        d_times[course['hash']] = []

    d[course['name']][course['hash']].append(course['courseReferenceNumber'])
    d_times[course['hash']].append(course['courseReferenceNumber'])

print('done')