import time
from .vision import VisionModule
from .policy import PolicyNetwork
from .env import OmniverseEnv
from .agent import ReasoningAgent

class EmbodiedLoop:
    def __init__(self):
        self.env = OmniverseEnv()
        self.vision = VisionModule()
        self.policy = PolicyNetwork()
        self.agent = ReasoningAgent()

    def run(self):
        obs = self.env.reset()

        while True:
            # 1. perception
            state = self.vision.process(obs)

            # 2. LLM reasoning (high-level intent)
            thought = self.agent.think(obs)

            # 3. RL policy decision
            action = self.policy.act(state)

            # combine reasoning + action
            final_action = f"{action} based_on {thought}"

            # 4. environment step
            obs, reward, done = self.env.step(final_action)

            print("[AGENT]", final_action, reward)

            time.sleep(1)

            if done:
                break