import time
import threading
from collections import deque

class TaskScheduler:
    def __init__(self):
        self.tasks = deque()
        self.running = False

    def add_task(self, func, delay=0):
        self.tasks.append((time.time() + delay, func))

    def start(self):
        self.running = True
        threading.Thread(target=self.loop, daemon=True).start()

    def loop(self):
        while self.running:
            now = time.time()

            for _ in range(len(self.tasks)):
                run_at, task = self.tasks.popleft()

                if now >= run_at:
                    try:
                        task()
                    except Exception as e:
                        print("[Scheduler Error]", e)
                else:
                    self.tasks.append((run_at, task))

            time.sleep(0.2)