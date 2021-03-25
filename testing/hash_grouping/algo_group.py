hash_length = 27
empty_hash = '000000000000000000000000000'

counters = [[0,0],[0,0],[0,0]]

def check_times(to_check, schedule):
    # First see if any hashes are already in the schedule, which would indicate a conflict, to save time
    # if schedule_hashes & to_check_hashes:
    #     return False
    # Otherwise go group by group
    schedule_classtimes = [classtime for group in schedule if group['classtimes'] for classtime in group['classtimes']]
    for classtime_a in to_check['classtimes']:
        for classtime_b in schedule_classtimes:
            # Check if times overlap
            if not (classtime_a['start_time'] > classtime_b['end_time'] or classtime_b['start_time'] > classtime_a['end_time']):
                counters[0][0] += 1
                # Check if days overlap
                if classtime_a['days'] & classtime_b['days']:
                    counters[1][0] += 1
                    # Check if dates overlap
                    if not (classtime_a['start_date'] > classtime_b['end_date'] or classtime_b['start_date'] > classtime_a['end_date']):
                        counters[2][0] += 1
                        return False
                    else:
                        counters[2][1] += 1
                else:
                    counters[1][1] += 1
            else:
                counters[0][1] += 1
    return True

def create_schedules(courses):
    courses.sort(key=len)
    group_idxs, temp, results = [1],[courses[0][0]],[]
    course_idx = 0

    # While there are still courses left to try
    while course_idx >= 0:
        # Resume trying remaining sections
        if course_idx + 1 != len(temp):
            group_idx = group_idxs.pop()
        # Otherwise move on to the next course
        else: 
            course_idx += 1
            group_idx = 0
        
        current_course = courses[course_idx]
        # Go through each section of the course and check if it works
        while group_idx < len(current_course): 
            group = current_course[group_idx]
            # Add the section if it does not conflict OR if it has no meeting times (online class)
            if len(temp) == 0 or len(group['classtimes']) == 0 or check_times(group, temp):
                temp.append(group)
                # Save our place so we can resume where we left off (with the next section)
                group_idxs.append(group_idx + 1)
                break
            # Otherwise, try the next section
            else:
                group_idx += 1
        
        # Once we have a section for each course, add the schedule to the list of results and remove the last section so we can try any remaining sections
        if len(temp) == len(courses):
            results.append(list(temp))
            temp.pop()
        # Otherwise, if we have tried all of the sections for this course, go back to the previous course and try any remaining sections
        elif group_idx >= len(current_course):
            if course_idx > 0:
                temp.pop()
            course_idx -= 1
        else:
            pass
    
    print(counters)
    return results
