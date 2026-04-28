import threading
import time
from collections import deque

# =========================
# TASK SCHEDULER (OS BRAIN)
# =========================
class TaskScheduler:
    def __init__(self):
        self.tasks = []
        self.running = False

    def add_task(self, fn, interval):
        self.tasks.append((fn, interval, time.time()))

    def start(self):
        self.running = True

        def loop():
            while self.running:
                now = time.time()
                for i, (fn, interval, last) in enumerate(self.tasks):
                    if now - last >= interval:
                        try:
                            fn()
                        except Exception as e:
                            print("[Scheduler Error]", e)
                        self.tasks[i] = (fn, interval, now)
                time.sleep(0.1)

        threading.Thread(target=loop, daemon=True).start()

    def stop(self):
        self.running = False


# =========================
# WORLD MODEL (PERSISTENT SIM)
# =========================
class WorldModel:
    def __init__(self):
        self.state = {
            "stability": 0.5,
            "events": []
        }

    def update(self, event):
        self.state["events"].append(event)
        self.state["stability"] += 0.01
        return self.state

    def simulate(self, query):
        return f"[SIMULATION] '{query}' -> stability={self.state['stability']}"


# =========================
# IDENTITY GRAPH MEMORY
# =========================
class IdentityGraph:
    def __init__(self):
        self.nodes = []

    def add_experience(self, text):
        self.nodes.append({
            "experience": text,
            "timestamp": time.time()
        })

    def summary(self):
        return f"Identity size: {len(self.nodes)} experiences"


# =========================
# REINFORCEMENT ENGINE
# =========================
class Reinforcement:
    def __init__(self):
        self.rewards = {}

    def reward(self, action, value):
        self.rewards[action] = self.rewards.get(action, 0) + value

    def score(self):
        return sum(self.rewards.values())


# =========================
# SLEEP CYCLE (MEMORY COMPRESSION)
# =========================
class SleepCycle:
    def __init__(self, identity):
        self.identity = identity

    def sleep(self):
        # compress memory (simple simulation)
        if len(self.identity.nodes) > 5:
            self.identity.nodes = self.identity.nodes[-5:]
        print("[SleepCycle] Memory compressed:", len(self.identity.nodes))