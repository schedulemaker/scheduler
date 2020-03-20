NUM_WEEKS = 16

def noConflict(section,schedule):
    '''/**
    * @function noConflict - Checks if the given section conflicts with any other sections in the schedule
    * @param {Section} section - The section to check against
    * @param {[[string, Section]]} schedule - An array of string-Section pairs representing the current schedule
    * @return {boolean} - TRUE if the section does not conflict with any other section in the array, FALSE otherwise
    */'''
    for sched in schedule:
        if hasTimeConflict(section, sched):
            return False
    return True

def hasTimeConflict(course1, course2):
    #compare both course's meeting times
    for meetingTime1 in course1['meetingTimes']:
        for meetingTime2 in course2['meetingTimes']:
            #determine common weeks between courses
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

            #element wise list of boolean AND between days1 and days2    
            aAndB = [x and y for x,y in zip(days1,days2)]

            #if they have days in common, check times
            if any(aAndB):
                if meetingTime1['startTime'] <= meetingTime2['startTime'] and meetingTime1['endTime'] >= meetingTime2['startTime']:
                    return True
                if meetingTime2['startTime'] <= meetingTime1['startTime'] and meetingTime2['endTime'] >= meetingTime1['startTime']:
                    return True

    return False  
'''
    Proposed format
{
    crn: number //RANGE key
	courseName: string //HASH key
	description: string
	attributes: string[]
    weeks: [
        {
            days: [
                {
                    day: Monday
                    meetingTimes: [
                        {
                            building:
                            room:
                            .
                            .
                            .
                            startTime:
                            endTime:
                        }
                    ]
                }
            ]
        }
    ]
}
'''

'''
    Old format

    {
	crn: number //RANGE key
	courseName: string //HASH key
	description: string
	attributes: string[]
	meetingTimes: [
		{
			startDate: string
			endDate: string
			Monday: [
                      {
				startTime: number
				endTime: number
				building: string
				room: string
				instructors: string[]
				campus: string
			    }
			]
			//Same for other days of the week
			//Incl. weekends
		}
		//Other entries for each week of the semester
	]
}'''

'''table = dynamodb.Table('Movies')

title = "The Big New Movie"
year = 2015

try:
    response = table.get_item(
        Key={
            'year': year,
            'title': title
        }
    )
except ClientError as e:
    print(e.response['Error']['Message'])
else:
    item = response['Item']
    print("GetItem succeeded:")
    print(json.dumps(item, indent=4, cls=DecimalEncoder))'''