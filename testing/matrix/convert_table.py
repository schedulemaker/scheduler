import json, argparse, numpy as np
from datetime import datetime
from dateutil.rrule import rrule, WEEKLY


# Converts the Banner data to the format used by the scheduler
parser = argparse.ArgumentParser()
parser.add_argument('--input',dest='input',help='Input file to convert')
parser.add_argument('--output',dest='output',help='Output file')
args = parser.parse_args()

days = [
    'monday',
    'tuesday',
    'wednesday',
    'thursday',
    'friday',
    'saturday',
    'sunday',
]

ct_keys = [
    'start_date',
    'end_date',
    'start_time',
    'end_time',
    'days'
]

empty_hash = '000000000000000000000000000'

matrix_shape = (12,31,24,60)

# args.input = 'testing/data/temple-202036-clean.json'

with open(args.input,'r') as file:
    data = json.load(file)

# Creates the matrix representation of the meeting time and extracts the hash
def get_hash_matrix(mf):
    mt = mf['meetingTime']

    mt_days = int(''.join(['1' if mt[d] else '0' for d in days]),2)
    # Format the dates as YYYYmmdd
    s_date_split = mt['startDate'].split('/')
    start_date = s_date_split[2] + s_date_split[0] + s_date_split[1]
    e_date_split = mt['endDate'].split('/')
    end_date = e_date_split[2] + e_date_split[0] + e_date_split[1]
    mt_hash = f'{start_date}{end_date}{mt["beginTime"]}{mt["endTime"]}{str(mt_days).zfill(3)}'

    # Create matrix representation of classtime
    matrix = np.zeros(matrix_shape, dtype=np.byte)
    start = datetime(int(s_date_split[2]),int(s_date_split[0]),int(s_date_split[1]))
    end = datetime(int(e_date_split[2]),int(e_date_split[0]),int(e_date_split[1]))
    rule = rrule(freq=WEEKLY,dtstart=start,until=end,byweekday=[idx for idx,day in enumerate(days) if mt[day]])
    rule = [{'month': item.month,'day':item.day} for item in rule]
    start_hour = int(mt['beginTime'][:2])
    start_min = int(mt['beginTime'][2:])
    end_hour = int(mt['endTime'][:2])
    end_min = int(mt['endTime'][2:])

    for item in rule:
        day = matrix[item['month'] - 1][item['day'] - 1]
        if start_hour == end_hour:
            day[start_hour][start_min:end_min] = 1
        else:
            day[start_hour][start_min:] = 1
            if end_hour - start_hour > 1:
                for hour in range(start_hour + 1, end_hour):
                    day[hour] = 1
            day[end_hour][:end_min] = 1

    return mt_hash,matrix

def format_table(data):
    table = {}
    
    for item in data:
        # Add the course to the table if not already in
        name = f'{item["subject"]} {item["courseNumber"]}'
        if name not in table:
            table[name] = {
                'name': name,
                'title': item['courseTitle'],
                'groups': {}
            }
        
        hashes,arrays = [],[]
        for mf in item['meetingsFaculty']:
            a,b = get_hash_matrix(mf)
            hashes.append(a)
            arrays.append(b)
        hashes.sort()
        # Add the group to the table entry if not already in
        group_hash = 0 if len(hashes) == 0 else int(''.join(hashes))
        if group_hash not in table[name]['groups']:
            table[name]['groups'][group_hash] = {
                'hash': group_hash,
                'matrix': [] if len(arrays) == 0 else np.packbits(sum(arrays)).view(np.uint32).tolist(),
                'crns': []
            }
        # Add the section to the group
        table[name]['groups'][group_hash]['crns'].append({
            'crn': int(item['courseReferenceNumber']),
            'section': item['sequenceNumber'],
            'instructors': [{'id': person['bannerId'], 'name': person['displayName']} for person in item['faculty']],
            'enrollment': {
                'capacity': item['maximumEnrollment'],
                'count': item['enrollment'],
                'available': item['seatsAvailable']
            },
            'waitlist': {
                'capacity': item['waitCapacity'],
                'count': item['waitCount'],
                'available': item['waitAvailable']
            },
            'campus': item['campusDescription']
            # 'locations':[ct['location'] for ct in arrays]
        })

    for item in table:
        groups = table[item]['groups']
        table[item]['groups'] = [groups[key] for key in groups]
    return table

def format_section(item):
    name = f'{item["subject"]} {item["courseNumber"]}'
    entry = {
        'name': name,
        'title': item['courseTitle'],
        'crn': int(item['courseReferenceNumber']),
        'section': item['sequenceNumber'],
        'instructors': [{'id': person['bannerId'], 'name': person['displayName']} for person in item['faculty']],
        'enrollment': {
            'capacity': item['maximumEnrollment'],
            'count': item['enrollment'],
            'available': item['seatsAvailable']
        },
        'waitlist': {
            'capacity': item['waitCapacity'],
            'count': item['waitCount'],
            'available': item['waitAvailable']
        },
        'campus': item['campusDescription']
    }
    
    hashes,arrays = [],[]
    for mf in item['meetingsFaculty']:
        a,b = get_hash_matrix(mf)
        hashes.append(a)
        arrays.append(b)
    hashes.sort()
    entry['hash'] = int(''.join(hashes))
    entry['matrix'] = sum(arrays)

    return entry

# data = [format_section(item) for item in data]
table = format_table(data)
data = [table[key] for key in table]


with open(args.output,'w') as file:
    json.dump(data,file, indent=2)