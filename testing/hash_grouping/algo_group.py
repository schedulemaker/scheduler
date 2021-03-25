hash_length = 27
empty_hash = '000000000000000000000000000'

def check_times(to_check, schedule):
    for classtime_a in to_check:
        for classtime_b in schedule:
            # Check if times overlap
            if not (classtime_a['start_time'] > classtime_b['end_time'] or classtime_b['start_time'] > classtime_a['end_time']):
                # Check if days overlap
                if classtime_a['days'] & classtime_b['days']:
                    # Check if dates overlap
                    if not (classtime_a['start_date'] > classtime_b['end_date'] or classtime_b['start_date'] > classtime_a['end_date']):
                        return False
    return True

def create_schedules(courses):
    courses.sort(key=len)
    group_idxs, temp, results = [1],[courses[0][0]],[]
    course_idx = 0
    group_idx = -1

    # For some reason, inlining `current_course` and `group` below results in an absurd speedup (0.03s vs 12s with PyPy) and even hits 0.03s with CPython

    # While there are still courses left to try
    while course_idx >= 0:
        # Resume trying remaining sections
        if course_idx + 1 != len(temp):
            group_idx = group_idxs.pop()
        # Otherwise move on to the next course
        else: 
            course_idx += 1
            group_idx = 0
        
        # current_course = courses[course_idx]
        # Go through each section of the course and check if it works
        while group_idx < len(courses[course_idx]): 
            # group = current_course[group_idx]
            # Add the section if temp is empty, it does not conflict OR if it has no meeting times (online class)
            if len(temp) == 0 or len(courses[course_idx][group_idx]['classtimes']) == 0 or check_times(courses[course_idx][group_idx]['classtimes'], [classtime for courses[course_idx][group_idx] in temp for classtime in courses[course_idx][group_idx]['classtimes']]):
                temp.append(courses[course_idx][group_idx])
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
        elif group_idx >= len(courses[course_idx]):
            if course_idx > 0:
                temp.pop()
            course_idx -= 1
        else:
            pass
    
    return results
