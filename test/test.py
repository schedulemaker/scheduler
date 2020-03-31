import sys
sys.path.insert(1, '..\\index')

import scheduler
from collections import deque
import json

def test():
    schedule = scheduler.Scheduler(deque)

    with open("test_courses.json", "r") as raw:
        data = json.load(raw)

    schedule.createSchedules(data)

test()