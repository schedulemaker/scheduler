import json, time

courses = []

for course in ['IH-0851', 'IH-0852', 'ENG-0802']:
    with open(course + '.json', 'r') as file:
        string = file.read()
    courses.append(json.loads(string))

courses = sorted(courses, key=len)

def check_times(to_check, schedule):
    for section in schedule:
        for classtime_a in section['times']:
            for classtime_b in to_check['times']:
                # In order for 2 sections to be compatible, one of the following conditiions must be true:
                #   - The start time of A must be greater than the end time of B OR
                #   - The start time of B must be greater than the end time of A
                # Here, we are testing if any of the meeting times break the above rules (the negation)
                if not (classtime_a['start'] > classtime_b['end'] or classtime_b['start'] > classtime_a['end']):
                    return False
    return True

def create(courses):
    course_idx, section_idx, temp, results = [],[],[],[]
    course_idx.append(0)
    temp.append(courses[0][0])
    section_idx.append(1)

    i = 1

    # While there are still courses left to try
    while len(course_idx) > 0:
        # Resume trying remaining sections
        if len(course_idx) != len(temp):
            j = section_idx.pop()
        # Otherwise move on to the next course
        else: 
            course_idx.append(i)
            j = 0
        
        current_course = courses[course_idx[-1]]
        # Go through each section of the course and check if it works
        while j < len(current_course): 
            section = current_course[j]
            # Add the section if it does not conflict OR if it has no meeting times (online class)
            if len(section['times']) == 0 or check_times(section, temp):
                temp.append(section)
                # Save our place so we can resume where we left off (with the next section)
                section_idx.append(j + 1)
                break
            # Otherwise, try the next section
            j += 1
        
        # Once we have a section for each course, add the schedule to the list of results and remove the last section so we can try any remaining sections
        if len(temp) == len(courses):
            results.append(list(temp))
            temp.pop()
        # Otherwise, if we have tried all of the sections for this course, go back to the previous course and try any remaining sections
        elif j >= len(current_course):
            course_idx.pop()
            if len(course_idx) > 0:
                temp.pop()
            i -= 1
        # Otherwise,
        else: 
            i += 1

    return results

start = time.time()
results = create(courses)
end = time.time()
duration = round(end - start, 2)
results = [[{'name':section['name'],'crn':section['crn']} for section in result] for result in results]
results.insert(0, {'algorithm': 'timestamp', 'duration': str(duration) + ' seconds'})
with open('results.json','w') as file:
    json.dump(results, file)