class OmniEnv:
    def __init__(self, client):
        self.client = client
        self.state = None
        self.done = False

    def reset(self):
        self.state = {"status": "reset"}
        self.done = False
        return self.state

    def step(self, action):
        """
        Standard RL step:
        MUST return: obs, reward, done
        """

        obs = self.client.send_action(action)

        # -------------------------
        # SAFE OBS HANDLING
        # -------------------------
        if obs is None:
            return self.state, 0.0, True

        if not isinstance(obs, dict):
            obs = {"state": obs}

        self.state = obs

        reward = obs.get("reward", 0.0)
        done = obs.get("done", False)

        return self.state, reward, done