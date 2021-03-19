import json, time, calendar
from datetime import datetime
from dateutil.rrule import rrule, WEEKLY

with open('table.json', 'r') as file:
    data = json.load(file)

for item in data:
    mt = item['meetingTimes']  
    item['times'] = []  
    for m in mt:
        days = []
        for idx,day in enumerate(['monday', 'tuesday','wednesday','thursday','friday', 'saturday','sunday']):
            if m[day]:
                days.append(idx)
        start = datetime.strptime(m['startDate'], '%m/%d/%Y')
        end = datetime.strptime(m['endDate'], '%m/%d/%Y')

        starts_start = start.replace(hour=int(int(m['startTime'])/100), minute=int(int(m['startTime'])%100))
        starts_end = end.replace(hour=int(int(m['startTime'])/100), minute=int(int(m['startTime'])%100))

        ends_start = start.replace(hour=int(int(m['endTime'])/100), minute=int(int(m['endTime'])%100))
        ends_end = end.replace(hour=int(int(m['endTime'])/100), minute=int(int(m['endTime'])%100))

        starts = list(rrule(WEEKLY, byweekday=days,dtstart=starts_start,until=starts_end))
        ends = list(rrule(WEEKLY, byweekday=days,dtstart=ends_start,until=ends_end))

        item['times'] += [{'start': int(startTime.timestamp()), 'end': int(endTime.timestamp())} for startTime, endTime in zip(starts,ends)]
    item.pop('meetingTimes')

print(data)

with open('courses.json', 'w') as file:
    json.dump(data, file)


# start/end = datetime.strptime('12/16/2020', '%m/%d/%Y')
# hour = int(time/100)
# min = int(time%100)
# start/end = .replace(hour=hour, minute=min)
# rrule(WEEKLY, byweekday=(MO,WE,FR),dtstart=start,until=end)