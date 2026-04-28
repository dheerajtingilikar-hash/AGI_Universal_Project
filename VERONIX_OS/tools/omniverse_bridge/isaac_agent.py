import numpy as np

class IsaacAgent:
    def __init__(self, policy):
        self.policy = policy

    def act(self, observation):
        state = observation["state"]
        return self.policy(state)