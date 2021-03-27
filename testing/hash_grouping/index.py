from algo_group import create_schedules
import time, boto3

dynamodb = boto3.resource('dynamodb')
table  = dynamodb.Table('202036')

def handler(event, context):
    responses = [table.get_item(Key={'name': course}) for course in event['courses']]
    responses = [res['Item'] for res in responses]

    for item in responses:
        for group in item['groups']:
            group['classtimes'] = [{key: int(ct[key]) for key in ct} for ct in group['classtimes']]

    start = time.time()
    results = create_schedules(responses)
    end = time.time()

    duration = round(end - start, 2)

    return(f'duration: {duration} seconds',f'count: {len(results)}')
