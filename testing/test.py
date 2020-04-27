import boto3
import json
import unittest 

with open("aws_keys.json", "r") as f:
  api_keys = json.load(f)

client = boto3.client('lambda', region_name='us-east-2',
    aws_access_key_id= api_keys['aws_access_key_id'],
    aws_secret_access_key= api_keys['aws_secret_access_key']
    )

def invoke(payload):
  response = client.invoke(FunctionName=api_keys['aws_function_name'],
    Payload=payload)

  return (json.loads(response['Payload'].read()))


'''TEST ONE CAMPUS'''
def test1Campus():
    payload = '''{
      "courses": [
        "CIS-3207",
        "MATH-1041"
      ],
      "campuses": [
        "MN"
      ]
    }'''

    return invoke(payload)

test1Expected = [{
      "campus": "MN",
      "meetingTimes": [
        {
          "saturday": False,
          "weeks": [
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            13,
            14,
            15,
            16
          ],
          "endDate": "12/16/2020",
          "thursday": False,
          "building": "SERC",
          "room": "00357",
          "instructors": [
            {
              "Name": "Eugene Kwatny",
              "ID": 903510150
            }
          ],
          "sunday": False,
          "tuesday": False,
          "wednesday": True,
          "friday": False,
          "startTime": 900,
          "endTime": 1050,
          "startDate": "08/24/2020",
          "monday": False
        },
        {
          "saturday": False,
          "weeks": [
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            13,
            14,
            15,
            16
          ],
          "endDate": "12/16/2020",
          "thursday": True,
          "building": "BEURY",
          "room": "00164",
          "instructors": [
            {
              "Name": "Eugene Kwatny",
              "ID": 903510150
            }
          ],
          "sunday": False,
          "tuesday": True,
          "wednesday": False,
          "friday": False,
          "startTime": 1230,
          "endTime": 1350,
          "startDate": "08/24/2020",
          "monday": False
        }
      ],
      "isOpen": True,
      "courseName": "CIS-3207",
      "title": "Introduction to Systems Programming and Operating Systems",
      "campusName": "Main",
      "crn": 4308
    },{
      "campus": "MN",
      "meetingTimes": [
        {
          "saturday": False,
          "weeks": [
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            13,
            14,
            15,
            16
          ],
          "endDate": "12/16/2020",
          "thursday": True,
          "building": "WCHMAN",
          "room": "00307",
          "instructors": [],
          "sunday": False,
          "tuesday": True,
          "wednesday": False,
          "friday": False,
          "startTime": 800,
          "endTime": 940,
          "startDate": "08/24/2020",
          "monday": False
        }
      ],
      "isOpen": True,
      "attributes": {
        "description": "_Core Quantitative Reasoning B",
        "isZTCAttribute": False,
        "code": "QB",
        "class": "net.hedtech.banner.student.schedule.SectionDegreeProgramAttributeDecorator",
        "courseReferenceNumber": "795",
        "termCode": "202036"
      },
      "courseName": "MATH-1041",
      "title": "Calculus I",
      "campusName": "Main",
      "crn": 795
    }]

class SchedulerOneCampus(unittest.TestCase):
  def setUp(self):
    self.results = test1Campus()

  def runTest(self):
    self.assertEqual(len(self.results), 56)  #correct number of results
    self.assertEqual(self.results[0], test1Expected)   #correct first result

'''TEST MULTIPLE CAMPUSES'''
def testMultiCampus():
    payload = '''{
      "courses": [
        "CIS-3207",
        "ANTH-0831",
        "FMA-5671",
        "KINS-1223"
      ],
      "campuses": [
        "MN",
        "AMB",
        "CC"
      ]
    }'''

    return invoke(payload)

testMultiExpected = [
    {
      "campus": "CC",
      "meetingTimes": [
        {
          "saturday": False,
          "weeks": [
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            13,
            14,
            15,
            16
          ],
          "endDate": "12/16/2020",
          "thursday": False,
          "building": "TUCC",
          "room": "00315",
          "instructors": [
            {
              "Name": "Chris Cagle",
              "ID": 911020525
            }
          ],
          "sunday": False,
          "tuesday": True,
          "wednesday": False,
          "friday": False,
          "startTime": 1730,
          "endTime": 2050,
          "startDate": "08/24/2020",
          "monday": False
        }
      ],
      "isOpen": True,
      "courseName": "FMA-5671",
      "title": "Film History and Theory",
      "campusName": "Center City",
      "crn": 44774
    },
    {
      "campus": "MN",
      "meetingTimes": [
        {
          "saturday": False,
          "weeks": [
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            13,
            14,
            15,
            16
          ],
          "endDate": "12/16/2020",
          "thursday": False,
          "building": "SERC",
          "room": "00357",
          "instructors": [
            {
              "Name": "Eugene Kwatny",
              "ID": 903510150
            }
          ],
          "sunday": False,
          "tuesday": False,
          "wednesday": True,
          "friday": False,
          "startTime": 900,
          "endTime": 1050,
          "startDate": "08/24/2020",
          "monday": False
        },
        {
          "saturday": False,
          "weeks": [
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            13,
            14,
            15,
            16
          ],
          "endDate": "12/16/2020",
          "thursday": True,
          "building": "BEURY",
          "room": "00164",
          "instructors": [
            {
              "Name": "Eugene Kwatny",
              "ID": 903510150
            }
          ],
          "sunday": False,
          "tuesday": True,
          "wednesday": False,
          "friday": False,
          "startTime": 1230,
          "endTime": 1350,
          "startDate": "08/24/2020",
          "monday": False
        }
      ],
      "isOpen": True,
      "courseName": "CIS-3207",
      "title": "Introduction to Systems Programming and Operating Systems",
      "campusName": "Main",
      "crn": 4308
    },
    {
      "campus": "MN",
      "meetingTimes": [
        {
          "saturday": False,
          "weeks": [
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            13,
            14,
            15,
            16
          ],
          "endDate": "12/16/2020",
          "thursday": False,
          "building": None,
          "room": None,
          "instructors": [],
          "sunday": False,
          "tuesday": False,
          "wednesday": False,
          "friday": False,
          "startTime": 0,
          "endTime": 0,
          "startDate": "08/24/2020",
          "monday": False
        }
      ],
      "isOpen": True,
      "attributes": {
        "description": "GenEd Race &amp; Diversity",
        "isZTCAttribute": False,
        "code": "GD",
        "class": "net.hedtech.banner.student.schedule.SectionDegreeProgramAttributeDecorator",
        "courseReferenceNumber": "25550",
        "termCode": "202036"
      },
      "courseName": "ANTH-0831",
      "title": "Immigration and the American Dream",
      "campusName": "Main",
      "crn": 25550
    },
    {
      "campus": "MN",
      "meetingTimes": [
        {
          "saturday": False,
          "weeks": [
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            13,
            14,
            15,
            16
          ],
          "endDate": "12/16/2020",
          "thursday": True,
          "building": "ANDRSN",
          "room": "00017",
          "instructors": [
            {
              "Name": "Kyle Harris",
              "ID": 912189493
            },
            {
              "Name": "Kyle Suess",
              "ID": 914352277
            }
          ],
          "sunday": False,
          "tuesday": True,
          "wednesday": False,
          "friday": False,
          "startTime": 1400,
          "endTime": 1520,
          "startDate": "08/24/2020",
          "monday": False
        },
        {
          "saturday": False,
          "weeks": [
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            13,
            14,
            15,
            16
          ],
          "endDate": "12/16/2020",
          "thursday": True,
          "building": "PEARMC",
          "room": "0P015",
          "instructors": [
            {
              "Name": "Kyle Harris",
              "ID": 912189493
            },
            {
              "Name": "Kyle Suess",
              "ID": 914352277
            }
          ],
          "sunday": False,
          "tuesday": False,
          "wednesday": False,
          "friday": False,
          "startTime": 1730,
          "endTime": 1920,
          "startDate": "08/24/2020",
          "monday": False
        }
      ],
      "isOpen": True,
      "attributes": {
        "description": "_Core Science &amp; Technology A",
        "isZTCAttribute": False,
        "code": "SA",
        "class": "net.hedtech.banner.student.schedule.SectionDegreeProgramAttributeDecorator",
        "courseReferenceNumber": "2184",
        "termCode": "202036"
      },
      "courseName": "KINS-1223",
      "title": "Human Anatomy and Physiology I",
      "campusName": "Main",
      "crn": 2184
    }
  ]

class SchedulerMultiCampus(unittest.TestCase):
  def setUp(self):
    self.results = testMultiCampus()

  def runTest(self):
    self.assertEqual(len(self.results), 123)  #correct number of results
    self.assertEqual(self.results[0], testMultiExpected)   #correct first result

'''TEST EXCEPTIONS'''
def testNoCourses():
  payload='''{
    "courses": [
    ],
    "campuses": [
      "MN"
    ]
  }'''
  return invoke(payload)

class SchedulerNoCourses(unittest.TestCase):
  def setUp(self):
    self.results = testNoCourses()

  def runTest(self):
    self.assertTrue('list index out of range' in self.results['errorMessage'])

def testNoCampuses():
  payload='''{
    "courses": [
      "CIS-3207",
      "MATH-1041"
    ],
    "campuses": [
    ]
  }'''
  return invoke(payload)

class SchedulerNoCampuses(unittest.TestCase):
  def setUp(self):
    self.results = testNoCampuses()

  def runTest(self):
    self.assertTrue('Unable to get all courses from database' in self.results['errorMessage'])

def testCampusNotExist():
  payload='''{
    "courses": [
      "CIS-3207",
      "MATH-1041"
    ],
    "campuses": [
      "ABC"
    ]
  }'''
  return invoke(payload)

class SchedulerCampusNotExist(unittest.TestCase):
  def setUp(self):
    self.results = testCampusNotExist()

  def runTest(self):
    self.assertTrue('list index out of range' in self.results['errorMessage'])

def testCourseNotExist():
  payload='''{
    "courses": [
      "CIS-3207",
      "MATH-1041",
      "ABC-1234"
    ],
    "campuses": [
        "MN"
    ]
  }'''
  return invoke(payload)

class SchedulerCourseNotExist(unittest.TestCase):
  def setUp(self):
    self.results = testCampusNotExist()

  def runTest(self):
    self.assertTrue('list index out of range' in self.results['errorMessage'])

'''RUN TESTS'''
suite = unittest.TestSuite()

suite.addTests([SchedulerOneCampus(), SchedulerMultiCampus(), SchedulerNoCourses(), 
SchedulerNoCampuses(), SchedulerCampusNotExist(), SchedulerCourseNotExist()])

unittest.TextTestRunner().run(suite)
