import random

class World:
    def __init__(self):
        self.state = {
            "energy": 100,
            "knowledge": 0,
            "environment_stability": 0.5
        }

    def step(self, action):
        # simulate environment reaction
        reward = 0

        if action == "learn":
            self.state["knowledge"] += 1
            reward = 1

        elif action == "explore":
            self.state["energy"] -= 2
            reward = 0.5

        elif action == "optimize":
            self.state["environment_stability"] += 0.05
            reward = 1.5

        # random world noise
        self.state["energy"] += random.uniform(-1, 1)

        done = self.state["energy"] <= 0

        return self.state, reward, done