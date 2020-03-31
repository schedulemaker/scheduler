#have to put in index folder to use
import scheduler
from collections import deque
import json

def test():
    schedule = scheduler.Scheduler(deque)

    with open("test_courses.json", "r") as raw:
        data = json.load(raw)

    results = schedule.createSchedules(data)

    print(results)

test()