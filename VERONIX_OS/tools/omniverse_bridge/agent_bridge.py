class AgentBridge:
    def __init__(self, brain):
        self.brain = brain
        self.last_action = None
        self.memory = []

    def act(self, observation):
        """
        Convert AGI reasoning → simulation action
        Safe for:
        - None observation
        - dict observation
        - Isaac Sim sensor output later
        """

        # =========================
        # SAFE OBSERVATION HANDLING
        # =========================
        if observation is None:
            observation = {"dummy": True}

        if not isinstance(observation, dict):
            observation = {"data": observation}

        # store short-term memory
        self.memory.append(observation)
        if len(self.memory) > 50:
            self.memory.pop(0)

        # =========================
        # SIMPLE DECISION POLICY (TEMPORARY)
        # =========================

        if "vision" in observation:
            action = {"type": "scan"}

        elif observation.get("dummy"):
            action = {"type": "idle"}

        else:
            action = {"type": "move", "value": "forward"}

        self.last_action = action
        return action

    def learn(self, reward):
        """
        Placeholder learning function.
        Later replaced with:
        - PPO
        - DQN
        - policy gradients
        """

        # minimal brain update hook
        if self.brain and "rl" in self.brain:
            try:
                self.brain["rl"].reward("step", reward)
            except:
                pass