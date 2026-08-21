class IsaacRLEnvironment:
    def __init__(self, world, sensors, actions):
        self.world = world
        self.sensors = sensors
        self.actions = actions

        self.step_count = 0

    def reset(self):
        self.world.load()
        self.step_count = 0
        return self.sensors.get_observation()

    def step(self, action):
        # apply action to robot
        self.actions.apply_action(action)

        # simulate physics
        self.world.step()

        obs = self.sensors.get_observation()
        reward = self.compute_reward(obs)
        done = self.step_count > 500

        self.step_count += 1

        return obs, reward, done, {}

    def compute_reward(self, obs):
        # simple placeholder reward
        joint_state = obs["state"]
        return -sum(abs(joint_state)) * 0.01