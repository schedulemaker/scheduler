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
    courses.sort(key=lambda x: len(x['groups']))
    first = courses[0]['groups'][0]
    group_idxs, temp, temp_classtimes, results = [1],[first],[first['classtimes']],[]
    course_idx = 0
    group_idx = -1

    # While there are still courses left to try
    while course_idx >= 0:
        # Resume trying remaining sections
        if course_idx + 1 != len(temp):
            group_idx = group_idxs.pop()
        # Otherwise move on to the next course
        else: 
            course_idx += 1
            group_idx = 0
        
        current_course = courses[course_idx]['groups']
        # Go through each group of the course and check if it works
        while group_idx < len(current_course): 
            group = current_course[group_idx]
            # Add the group if temp is empty, it does not conflict OR if it has no meeting times (online class)
            if len(temp) == 0 or len(group['classtimes']) == 0 or check_times(group['classtimes'], temp_classtimes[-1]):
                temp.append(group)
                if len(temp_classtimes) == 0:
                    temp_classtimes.append(group['classtimes'])
                else:
                    temp_classtimes.append([*temp_classtimes[-1], *group['classtimes']])
                # Save our place so we can resume where we left off (with the next group)
                group_idxs.append(group_idx + 1)
                break
            # Otherwise, try the next group
            else:
                group_idx += 1
        
        # Once we have a group for each course, add the schedule to the list of results and remove the last group so we can try any remaining group
        if len(temp) == len(courses):
            results.append(list(temp))
            temp.pop()
            temp_classtimes.pop()
        # Otherwise, if we have tried all of the groups for this course, go back to the previous course and try any remaining groups
        elif group_idx >= len(current_course):
            if course_idx > 0:
                temp.pop()
                temp_classtimes.pop()
            course_idx -= 1
        else:
            pass
    
    return results
