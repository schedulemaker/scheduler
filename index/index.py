import cache

dynamodb, scheduler, os, json, asyncio, deserializer = cache.exports()
loop = asyncio.get_event_loop()

def lambda_handler(event,context):
    return loop.run_until_complete(job(event,context))

async def job(event, context):
    #params = event.body
    courseList = event['courses']
    campuses = event['campuses']

    print('Received the following courses: {}', courseList)

    try:
        data = await getSections(courseList, campuses)
    except Exception as e:
        # Otherwise Lambda will return success. We could also probably just not use try catch 
        # but in the future we should implement something more detailed based upon the exact type of error
        raise Exception('Unable to get all courses from database: {}', e.args) 
    

    schedules = scheduler.createSchedules(data)
    print('Created {} schedules', len(schedules))

    return schedules # No need to serialize and return status code


async def getSections(courses, campuses):
    return list(map(lambda course:
        deserialize(dynamodb.query(
            TableName=os.environ['TABLENAME'],
            KeyConditionExpression='#courseName = :course',
            ExpressionAttributeNames={
                "#courseName" : "courseName",
                    '#campus': 'campus',
                    '#isOpen': 'isOpen'
            },
            ExpressionAttributeValues= expressionAttributeValues(campuses,course),
            FilterExpression='#isOpen = :true AND #campus IN ({})'.format(','.join(list(map(lambda camp: ':{}'.format(camp),campuses))))
        ))['Items']
        ,
        courses))

def expressionAttributeValues(campuses,course):
    obj = {
        ":course": {'S': str(course)},
        ':true': {'BOOL': True} 
    }
    append = {':{}'.format(camp):{'S':str(camp)} for camp in campuses}

    return {**obj, **append}

def deserialize(data):
    if isinstance(data, list):
       return [deserialize(v) for v in data]

    if isinstance(data, dict):
        try: 
            return deserializer().deserialize(data)
        except TypeError:
            return { k : deserialize(v) for k, v in data.items() }
    else:
        return data
