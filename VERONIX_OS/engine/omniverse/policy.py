import numpy as np

class PolicyNetwork:
    def __init__(self):
        self.weights = np.random.randn(10, 5)

    def act(self, state_vector):
        logits = np.dot(state_vector, self.weights)
        action_id = np.argmax(logits)

        actions = [
            "move_forward",
            "turn_left",
            "turn_right",
            "pick_object",
            "wait"
        ]

        return actions[action_id]