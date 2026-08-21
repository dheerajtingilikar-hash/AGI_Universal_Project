class OmniverseEnv:
    def __init__(self):
        self.step_count = 0

    def reset(self):
        self.step_count = 0
        return "scene_reset"

    def step(self, action):
        self.step_count += 1

        observation = f"state_after_{action}"
        reward = 1 if "correct" in action else -1
        done = self.step_count > 50

        return observation, reward, done