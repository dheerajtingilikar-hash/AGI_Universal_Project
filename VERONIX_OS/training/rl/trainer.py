import random
from collections import deque

class RLAgent:
    def __init__(self):
        self.memory = deque(maxlen=1000)
        self.q_table = {}

    def get_action(self, state):
        actions = ["learn", "explore", "optimize"]
        return random.choice(actions)

    def store(self, s, a, r):
        self.memory.append((s, a, r))

    def train(self):
        # fake "weight update simulation"
        for s, a, r in list(self.memory)[-20:]:
            key = str((s, a))
            self.q_table[key] = self.q_table.get(key, 0) + r * 0.01