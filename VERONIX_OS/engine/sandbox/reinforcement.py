class Reinforcement:
    def __init__(self):
        self.scores = {}

    def reward(self, action, score):
        self.scores[action] = self.scores.get(action, 0) + score

    def best_action(self):
        if not self.scores:
            return None
        return max(self.scores, key=self.scores.get)