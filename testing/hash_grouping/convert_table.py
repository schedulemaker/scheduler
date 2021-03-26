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

ct_keys = [
    'start_date',
    'end_date',
    'start_time',
    'end_time',
    'days'
]

empty_hash = '000000000000000000000000000'

with open(args.input,'r') as file:
    data = json.load(file)

# Extracts hash and classtime object from meetingFaculty entry
def get_hash_classtime(mf):
    mt = mf['meetingTime']

    mt_days = int(''.join(['1' if mt[d] else '0' for d in days]),2)
    # Format the dates as YYYYmmdd
    s_date_split = mt['startDate'].split('/')
    start_date = s_date_split[2] + s_date_split[0] + s_date_split[1]
    e_date_split = mt['endDate'].split('/')
    end_date = e_date_split[2] + e_date_split[0] + e_date_split[1]
    mt_hash = f'{start_date}{end_date}{mt["beginTime"]}{mt["endTime"]}{str(mt_days).zfill(3)}'

    classtime = {
        'start_time': int(mt['beginTime']),
        'end_time': int(mt['endTime']),
        'start_date': int(start_date),
        'end_date': int(end_date),
        'days': mt_days,
        'location': {
            'building': mt['building'],
            'room': mt['room']
        }
    }

    return mt_hash,classtime

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
        
        hashes,classtimes = [],[]
        for mf in item['meetingsFaculty']:
            a,b = get_hash_classtime(mf)
            hashes.append(a)
            classtimes.append(b)
        hashes.sort()
        # Add the group to the table entry if not already in
        group_hash = ''.join(hashes)
        if group_hash not in table[name]['groups']:
            table[name]['groups'][group_hash] = {
                'hash': group_hash,
                'classtimes': [{key: ct[key] for key in ct_keys} for ct in classtimes],
                'crns': []
            }
        # Add the section to the group
        table[name]['groups'][group_hash]['crns'].append({
            'crn': item['courseReferenceNumber'],
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
            'campus': item['campusDescription'],
            'locations':[ct['location'] for ct in classtimes]
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
    
    hashes,classtimes = [],[]
    for mf in item['meetingsFaculty']:
        a,b = get_hash_classtime(mf)
        hashes.append(a)
        classtimes.append(b)
    hashes.sort()
    entry['hash'] = ''.join(hashes)
    entry['classtimes'] = classtimes

    return entry

# data = [format_section(item) for item in data]
table = format_table(data)
data = [table[key] for key in table]


with open(args.output,'w') as file:
    json.dump(data,file)