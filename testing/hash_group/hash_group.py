import json


with open('testing/table.json','r') as file:
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
    for mt in course['meetingTimes']:
        mt_days = '0b' + ''.join(['1' if mt[d] else '0' for d in days])
        mt_time = f'{mt["startTime"]}{mt["endTime"]}'
        mt_date = f'{mt["startDate"].replace("/","")}{mt["endDate"].replace("/","")}'
        mt_hash = mt_date + mt_time + mt_days
        mt['hash'] = mt_hash
    course_hashes = [mt['hash'] for mt in course['meetingTimes']]
    course_hashes.sort()
    course['hash'] = ''.join([mt_hash for mt_hash in course_hashes])

d = {}
for course in data:
    if course['name'] not in d:
        d[course['name']] = {}
    if course['hash'] not in d[course['name']]:
        d[course['name']][course['hash']] = []
    
    d[course['name']][course['hash']].append(course['crn'])

print('done')