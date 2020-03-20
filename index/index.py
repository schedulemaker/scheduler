import json
import cache
import os
import asyncio

dynamodb = None
scheduler = None

loop = asyncio.get_event_loop()

def lambda_handler(event,context):
    return loop.run_until_complete(job(event,context))

async def job(event, context):
    dynamodb,scheduler = cache.exports()

    params = event.body
    courseList = params.courses

    print('Received the following courses: {}', courseList)

    try:
        data = await getSections(courseList, params.campus)
    except Exception as e:
        print('Unable to get all courses form database: {}', e)

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
        dynamodb.query(
            TableName=os.environ['TABLENAME'],
            KeyConditionExpression='courseName = :course',
            ExpressionAttributeNames={
                "#courseName" : "courseName",
                    '#campus': 'campus',
                    '#isOpen': 'isOpen'
            },
            ExpressionAttributeValues= expressionAttributeValues(campus,course),
            FilterExpression='#isOpen = :true AND #campus IN ({})'.format(''.join(list(map(lambda camp: ':${}'.format(camp),campus))))
        )
        ,
        courses))

def expressionAttributeValues(campus,course):
    obj = {
        ":course": course,
        ':true': True 
    }
    append = {':${}'.format(camp):camp for camp in campus}
    return {**obj, **append}
