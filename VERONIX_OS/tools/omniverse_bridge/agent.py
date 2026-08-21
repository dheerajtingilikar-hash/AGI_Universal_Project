import random

class Agent:
    def __init__(self):
        self.memory = []

    def act(self, obs):
        # placeholder policy (replace with PPO later)
        return [random.random() for _ in range(6)]

    def learn(self, reward):
        self.memory.append(reward)