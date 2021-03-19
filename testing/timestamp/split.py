import json

with open('courses.json', 'r') as file:
    data = json.load(file)

d = {}
for course in data:
    if course['name'] not in d:
        d[course['name']] = []
    else:
        d[course['name']].append(course)

for key in d.keys():
    with open(key + '.json', 'w') as file:
        json.dump(list(d[key]), file)