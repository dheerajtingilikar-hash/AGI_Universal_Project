class OmniLoop:
    def __init__(self, env, sensors, actions, agent, reward):
        self.env = env
        self.sensors = sensors
        self.actions = actions
        self.agent = agent
        self.reward = reward

    def run(self, steps=50):

        obs = self.env.reset()

        for i in range(steps):

            # -------------------------
            # SENSOR READ
            # -------------------------
            perception = self.sensors.observe() if self.sensors else obs

            # -------------------------
            # AGENT DECISION
            # -------------------------
            action = self.agent.act(perception)

            # -------------------------
            # EXECUTE ACTION
            # -------------------------
            if self.actions:
                self.actions.act(action)

            # -------------------------
            # ENV STEP (NOW CLEAN & STANDARD)
            # -------------------------
            obs, r, done = self.env.step(action)

            # -------------------------
            # LEARNING SIGNAL
            # -------------------------
            self.agent.learn(r)

            print(f"[STEP {i}] Reward: {r}")

            if done:
                obs = self.env.reset()