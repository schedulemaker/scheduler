'use strict';

if (!cache){
    var cache = require('./cache');
}

exports.handler = async (event, context) => {
    let DBToScheduler = cache.DBToScheduler;
    let SchedulerToUI = cache.SchedulerToUI;
    let scheduler = cache.Scheduler;

    let params = JSON.parse(event.body);
    let courseList = params.courses;
    console.log(`Received the following courses: ${courseList}`);

    try {
        var data = await getSections(courseList, params.campus);
    } catch (error) {
        console.log(`'Unable to get all courses from database: ${error}`);
        return {
            statusCode: '500',
            body: "Unable to process request",
            headers: {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Methods': '*',
                'Access-Control-Allow-Origin': '*'
            }
        };
    }
    
    let courses = DBToScheduler(data);
    let schedules = scheduler.createSchedules(courses);
    let results = SchedulerToUI(schedules);
    console.log(`Created ${results.length} schedules`);
    
    return {
        statusCode: '200',
        body: JSON.stringify(results),
        headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Methods': '*',
            'Access-Control-Allow-Origin': '*'
        }
    };
};

async function getSections(courses, campus){
    const docClient = cache.DocumentClient;
    return Promise.all(courses.map(course => {
        let params = {
            TableName : process.env.TABLENAME,
            KeyConditionExpression : "#courseName = :course",
            ExpressionAttributeNames : {
                "#courseName" : "courseName",
                '#campus': 'campus',
                '#isOpen': 'isOpen'
            },
            ExpressionAttributeValues : function(){
                let obj = {
                    ":course": course,
                    ':true': true
                };
                campus.forEach(campus => obj[`:${campus}`] = campus);
                return obj;
            }(),
            FilterExpression: `#isOpen = :true AND #campus IN (${campus.map(campus => `:${campus}`).join()})`
        };

        return docClient.query(params).promise();
    }));
}

