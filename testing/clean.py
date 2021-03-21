import json, html

# Cleans the data from Banner, including:
#   - Consistent values for courses with no meeting times
#   - Removing HTML entities from text
#   - Removing duplicate meeting time entries

days = [
    'saturday',
    'sunday',
    'monday',
    'tuesday',
    'wednesday',
    'thursday',
    'friday'
]

filename = 'temple-202103'
with open(f'testing/{filename}.json', 'r') as file:
    data = json.load(file)

for item in data:
    # Clean course titles and instructor names
    item['courseTitle'] = html.unescape(item['courseTitle'].replace('&nbsp;',''))
    for faculty in item['faculty']:
        faculty['displayName'] = html.unescape(faculty['displayName'].replace('&nbsp;',''))
    # Remove any empty meeting times
    item['meetingsFaculty'] = [mf for mf in item['meetingsFaculty'] if all([mf['meetingTime']['beginTime'], mf['meetingTime']['endTime']])]   
    if len(item['meetingsFaculty']) == 0:
        item['meetingsFaculty'] = None
    # Remove any duplicate meeting times
    if item['meetingsFaculty']:
        unique = {}
        for mf in item['meetingsFaculty']:
            mt = mf['meetingTime']
            mt_days = ''.join(['1' if mt[d] else '0' for d in days])
            mt_time = f'{mt["beginTime"]}{mt["endTime"]}'
            mt_date = f'{mt["startDate"].replace("/","")}{mt["endDate"].replace("/","")}'
            mt_hash = mt_date + mt_time + mt_days
            unique[mt_hash] = mf
        item['meetingsFaculty'] = list(unique.values())

with open(f'testing/{filename}-clean.json','w') as file:
    json.dump(data,file)