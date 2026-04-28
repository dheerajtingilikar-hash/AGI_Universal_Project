# AGI/core/environment.py

import random

class Environment:
    def __init__(self):
        self.state = {
            "energy": 100,
            "knowledge": 0,
            "risk": 0
        }

    def step(self, action):
        """
        Action space:
        0 = explore
        1 = learn
        2 = rest
        """

        if action == 0:
            self.state["knowledge"] += random.randint(1, 3)
            self.state["energy"] -= 2

        elif action == 1:
            self.state["knowledge"] += random.randint(2, 5)
            self.state["energy"] -= 5

        elif action == 2:
            self.state["energy"] += 3

        # environment drift
        self.state["risk"] += random.random() * 0.5

        return self.state