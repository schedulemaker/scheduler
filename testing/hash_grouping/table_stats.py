import json,csv,argparse

# Gets course stats from the raw JSON file from Banner

parser = argparse.ArgumentParser()
parser.add_argument('--file',dest='file',help='File to get stats for')
args = parser.parse_args()

empty_hash = '000000000000000000000000000'
with open(args.file,'r') as file:
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
        course['hash'] = empty_hash

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

with open(f'{args.file[:-5]}-stats.csv', 'w') as file:
    file.writelines(['Course,Sections,Groups,Grouped size(%)\n'])
    lines = [[key, sum([len(d[key][subkey]) for subkey in d[key]]), len(d[key])] for key in d]
    file.writelines([f'{i[0]},{i[1]},{i[2]},{round(i[2]/i[1],2)}\n' for i in lines])