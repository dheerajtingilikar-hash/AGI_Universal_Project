# AGI/core/scheduler.py

import time
from collections import deque

class TaskScheduler:
    def __init__(self):
        self.queue = deque()

    def add_task(self, task):
        self.queue.append(task)

    def run(self, state, shutdown):
        while not shutdown.is_set():

            if not self.queue:
                time.sleep(1)
                continue

            task = self.queue.popleft()

            try:
                task(state)
            except Exception as e:
                print("Task error:", e)