# AGI/core/reward.py

class RewardSystem:
    def __init__(self):
        self.score = 0

    def reward(self, value):
        self.score += value

    def punish(self, value):
        self.score -= value

    def get_score(self):
        return self.score

    def evaluate_response(self, user_satisfaction):
        """
        user_satisfaction: 0 to 1
        """
        if user_satisfaction > 0.7:
            self.reward(1)
        else:
            self.punish(1)