from collections import deque

def noConflict(section,schedule):
    '''
    noConflict - Checks if the given section conflicts with any other sections in the schedule
    Params: {Section} section - The section to check against
    {[[string, Section]]} schedule - An array of string-Section pairs representing the current schedule
    Returns: {boolean} - TRUE if the section does not conflict with any other section in the array, FALSE otherwise
    '''
    for scheduleSection in schedule:
        if hasTimeConflict(section, scheduleSection):
            return False
    return True

def hasTimeConflict(section1, section2):
    '''
    Returns TRUE if there is a time conflict.
    '''
    #compare both sections' meeting times
    for meetingTime1 in section1['meetingTimes']:
        for meetingTime2 in section2['meetingTimes']:
            #determine common weeks between sections
            commonWeeks = set(meetingTime1['weeks']).intersection(set(meetingTime2['weeks']))

            #if they have weeks in common, check days
            if commonWeeks:
                days1 = [meetingTime1['monday'],
                        meetingTime1['tuesday'],
                        meetingTime1['wednesday'],
                        meetingTime1['thursday'],
                        meetingTime1['friday'],
                        meetingTime1['saturday'],
                        meetingTime1['sunday']]
                days2 = [meetingTime2['monday'],
                        meetingTime2['tuesday'],
                        meetingTime2['wednesday'],
                        meetingTime2['thursday'],
                        meetingTime2['friday'],
                        meetingTime2['saturday'],
                        meetingTime2['sunday']]
            else:
                return False

            #element wise list of boolean AND between days1 and days2    
            aAndB = [x and y for x,y in zip(days1,days2)]

            #if they have days in common, check times
            if any(aAndB):
                if meetingTime1['startTime'] <= meetingTime2['startTime'] and meetingTime1['endTime'] >= meetingTime2['startTime']:
                    return True
                if meetingTime2['startTime'] <= meetingTime1['startTime'] and meetingTime2['endTime'] >= meetingTime1['startTime']:
                    return True

    return False  

class Scheduler:
    def __init__(self):
        pass

    def createSchedules(self, courses):
        '''Params: Courses - a list of list of sections'''

        #sort courses by number of meeting times least -> most
        courses = sorted(courses, key=len)

        # temp - A stack used to build a temporary schedule. Sections are pushed onto the stack as non-conflicting
        # ones are found, and popped in the case of backtracking. When the stack reaches the same size as the number of
        # courses, it is shallow copied in the results list.
        temp = deque()

        # current - A stack used to keep track of the current Course from the courses list that the algorithm
        # is processing. Courses are added to the stack once a suitable section fromt he previous course has been
        # added to temp. In the case of backtracking, Courses are popped off the stack.
        current = deque()

        # index - A stack used to keep track of the index of the Section that was pushed onto temp from the Course
        # in current. The index that is pushed is 1 greater than the index at which the suitable Section was found, so
        # that in the case of backtracking, the algorithm can pick up where it left off with the next Section in the list.
        index = deque()

        # results - An array of Maps, where each map represents a schedule. When temp reaches the same size as the
        # number of courses, a new map is created and added to results.
        results = []

        #Preload all 3 stacks with initial values
        current.append(courses[0])
        temp.append(courses[0][0])  #first course, first section
        index.append(1)

        #i is the index of which course from the courses list the algorithm is currently on
        i = 1

        # Once the first course that was preloaded has been popped off the stack (all sections have been tried), 
        # the loop will break
        while len(current) > 0:

            # If the 2 stacks do not contain the same # of items, that means that no compatible section was found
            # previously, and we pop the placeholder off the stack to pick up where we left off with the previous course
            if len(current) != len(temp):
                j = index.pop()
            else:
                # Otherwise, we can push the next course onto the current stack and iterate through it's sections
                current.append(courses[i])
                j = 0

            # Go through the sections of the top course in the stack. If a section is compatible with the current
            # temporary schedule in temp, it is pushed onto temp, and the placeholder index for the next section in 
            # the list is also saved onto the index stack. 
            top = current[-1] #peek

            while j < len(top):
                section = top[j]
                
                if len(section['meetingTimes']) == 0 or noConflict(section, temp):
                    temp.append(section)
                    index.append(j + 1)
                    break
                j += 1
            
            # Once the temp stack has the required number of sections, we do a shallow copy of temp in it's current
            # state and convert it into a map, then place it in the results list. Lastly, remove the last section so 
            # that any remaining sections of the current course can be tested.
            if len(temp) == len(courses):
                results.append(list(temp))
                temp.pop()
            # If j is not less than the number of sections in the current course, then that means that so compatible
            # section was found, so we need to backtrack to the previous course and try the remaining sections. We also
            # decrement i to keep it aligned with which course in the list we're on*/
            elif j >= len(top):
                current.pop()
                temp.pop()
                i -= 1
            # Otherwise increment i to move onto the next course in the next loop iteration
            else:
                i += 1
                
        return results
