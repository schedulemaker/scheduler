import json

with open('temple-202036.json', 'r') as file:
    table = json.load(file)

items = table['Items']
courseNames = ['IH-0851', 'IH-0852', 'ENG-0802']
items = [item for item in items if item['courseName']['S'] in courseNames]
courses = [{'name':item['courseName']['S'],'crn':item['crn']['N'],'meetingTimes':[{'startDate':mt['M']['startDate']['S'],'endDate':mt['M']['endDate']['S'],'startTime':mt['M']['startTime']['N'],'endTime':mt['M']['endTime']['N'],'monday':mt['M']['monday']['BOOL'],'tuesday':mt['M']['tuesday']['BOOL'],'wednesday':mt['M']['wednesday']['BOOL'],'thursday':mt['M']['thursday']['BOOL'],'friday':mt['M']['friday']['BOOL'],'sunday':mt['M']['sunday']['BOOL'],'saturday':mt['M']['saturday']['BOOL']} for mt in item['meetingTimes']['L']]} for item in items]

with open('table.json','w') as file:
    json.dump(courses,file)