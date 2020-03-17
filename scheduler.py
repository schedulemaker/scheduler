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
    for week in range(0, NUM_WEEKS):
        for day in range(0,7):
            for meeting in course1['weeks'][week][day]['meetingTimes'])
            
}


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