# AGI/core/self_evolver.py

class SelfEvolver:
    def __init__(self):
        self.config = {
            "creativity": 0.5,
            "risk": 0.2,
            "curiosity": 0.5
        }

    def adjust(self, feedback_score):
        if feedback_score > 0.7:
            self.config["curiosity"] += 0.05
            self.config["creativity"] += 0.03
        else:
            self.config["risk"] -= 0.02

        # clamp values
        for k in self.config:
            self.config[k] = max(0.0, min(1.0, self.config[k]))

    def get_config(self):
        return self.config