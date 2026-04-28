from sandbox.environment import World
from rl.trainer import RLAgent
import time

class WorldLoop:
    def __init__(self):
        self.world = World()
        self.agent = RLAgent()

    def run(self, steps=100):
        state = self.world.state

        for i in range(steps):
            action = self.agent.get_action(state)

            state, reward, done = self.world.step(action)

            self.agent.store(state, action, reward)
            self.agent.train()

            print(f"[STEP {i}] Action={action} Reward={reward} State={state}")

            if done:
                print("World ended (energy depleted)")
                break