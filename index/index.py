import cache

dynamodb, scheduler, os, json, asyncio, deserializer = cache.exports()
loop = asyncio.get_event_loop()

def lambda_handler(event,context):
    return loop.run_until_complete(job(event,context))

async def job(event, context):
    #params = event.body
    courseList = event['courses']
    campus = event['campus']

    print('Received the following courses: {}', courseList)

    try:
        data = await getSections(courseList, campus)
    except Exception as e:
        print('Unable to get all courses from database: {}', e)

        return {'statusCode': 500,
                'body': 'Unable to process request',
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Methods': '*',
                    'Access-Control-Allow-Origin': '*'
                }}

    schedules = scheduler.createSchedules(data)
    print('Created {} schedules', len(schedules))

    return {'statusCode': 200,
                'body': json.dumps(schedules),
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Methods': '*',
                    'Access-Control-Allow-Origin': '*'
                }}


async def getSections(courses, campus):
    return list(map(lambda course:
        deserialize(dynamodb.query(
            TableName=os.environ['TABLENAME'],
            KeyConditionExpression='#courseName = :course',
            ExpressionAttributeNames={
                "#courseName" : "courseName",
                    '#campus': 'campus',
                    '#isOpen': 'isOpen'
            },
            ExpressionAttributeValues= expressionAttributeValues(campus,course),
            FilterExpression='#isOpen = :true AND #campus IN ({})'.format(''.join(list(map(lambda camp: ':{}'.format(camp),campus))))
        ))['Items']
        ,
        courses))

def expressionAttributeValues(campus,course):
    obj = {
        ":course": {'S': str(course)},
        ':true': {'BOOL': True} 
    }
    append = {':{}'.format(camp):{'S':str(camp)} for camp in campus}

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
