import json, argparse

# Converts the Banner data to the format used by the scheduler
parser = argparse.ArgumentParser()
parser.add_argument('--input',dest='input',help='Input file to convert')
parser.add_argument('--output',dest='output',help='Output file')
args = parser.parse_args()

days = [
    'saturday',
    'sunday',
    'monday',
    'tuesday',
    'wednesday',
    'thursday',
    'friday'
]
empty_hash = '000000000000000000000000000'

with open(args.input,'r') as file:
    data = json.load(file)

def format(item):
    entry = {
        'name': f'{item["subject"]} {item["courseNumber"]}', 
        'crn': int(item["courseReferenceNumber"]),
    }
    if item['meetingsFaculty']:
        entry['classtimes'] = []
        course_hashes = []
        for mf in item['meetingsFaculty']:
            mt = mf['meetingTime']
            mt_days = int(''.join(['1' if mt[d] else '0' for d in days]),2)
            # Format the dates as YYYYmmdd
            s_date_split = mt['startDate'].split('/')
            startDate = s_date_split[2] + s_date_split[0] + s_date_split[1]
            e_date_split = mt['endDate'].split('/')
            endDate = e_date_split[2] + e_date_split[0] + e_date_split[1]

            mt_hash = f'{startDate}{endDate}{mt["beginTime"]}{mt["endTime"]}{str(mt_days).zfill(3)}'
            course_hashes.append(mt_hash)

            entry['classtimes'].append({
              'hash': mt_hash,
              'start_date': int(startDate),
              'end_date': int(endDate),
              'start_time': int(mt['beginTime']),
              'end_time': int(mt['endTime']),
              'days': mt_days  
            })
        course_hashes.sort()
        entry['hash'] = ''.join(course_hashes)
        entry['hashes'] = course_hashes
    else:
        entry['classtimes'] = None
        entry['hash'] = empty_hash
        entry['hashes'] = []
    return entry

data = [format(item) for item in data]

with open(args.output,'w') as file:
    json.dump(data,file)