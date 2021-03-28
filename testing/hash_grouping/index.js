const create_schedules = require('./algo_group');
const aws = require('aws-sdk');

const doc = new aws.DynamoDB.DocumentClient();

exports.handler = async (event, context) => {
    const promise = await doc.batchGet({
        'RequestItems': {
            '202036': {
                'Keys': event.courses.map(c => { 
                    return {
                        'name': c
                    };
                })
            }
        }
    }).promise();

    const courses = promise.Responses['202036'];
    const start = process.hrtime();
    const results = create_schedules(courses);
    const end = process.hrtime(start);
    const duration = end[0] + Number((end[1]/1e9).toFixed(2));

    return [`duration: ${duration} seconds`,`count: ${results.length}`];
}