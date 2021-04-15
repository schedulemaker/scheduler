import numpy as np
import functools, operator

def check_times(arrays, to_check):
    arrays = [item for item in arrays if len(item) != 0]
    if len(arrays) == 0:
        return True
    else:
        return not np.bitwise_and.reduce([*arrays,to_check]).any()

def create_schedules(courses):
    courses.sort(key=lambda x: len(x['groups']))
    first = courses[0]['groups'][0]
    group_idxs, temp, results = [1],[first['matrix']],[]
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
            if len(temp) == 0 or len(group['matrix']) == 0 or check_times(temp,group['matrix']):
                temp.append(group['matrix'])
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
        # Otherwise, if we have tried all of the groups for this course, go back to the previous course and try any remaining groups
        elif group_idx >= len(current_course):
            if course_idx > 0:
                temp.pop()
            course_idx -= 1
        else:
            pass
    
    return results
