import random

class GoalSystem:
    def __init__(self):
        self.goals = []

    def generate_goal(self):
        goals = [
            "increase knowledge",
            "stabilize environment",
            "explore new state space",
            "optimize memory usage"
        ]
        g = random.choice(goals)
        self.goals.append(g)
        return g