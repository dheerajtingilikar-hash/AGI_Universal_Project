class OmniClient:
    def __init__(self):
        self.connected = False
        self.world = None
        self.stage = None
        self.robot = None
        self._init_attempted = False

        print("[OmniClient] Initializing RL-ready Isaac interface...")
        print("[OmniClient] Waiting for Isaac runtime...")

    def init_world(self):
        if self.world is not None:
            return

        if self._init_attempted and not self.connected:
            self._init_attempted = False

        if self._init_attempted:
            return

        self._init_attempted = True

        try:
            from isaacsim.core.api.world import World
            print("[DEBUG] Using NEW Isaac API ONLY")

            self.world = World()
            self.world.reset()

            import omni.timeline
            timeline = omni.timeline.get_timeline_interface()
            timeline.play()

            self.connected = True
            print("[OmniClient] Isaac World Initialized")

        except Exception as e:
            print("[OmniClient] STUB MODE ACTIVE")
            print("[Reason]", e)
            self.connected = False

    def _step_physics(self):
        if self.world is None:
            self._init_attempted = False
            self.init_world()

        if self.world:
            try:
                self.world.step(render=True)
            except Exception:
                print("[PhysX Step Error] Connection lost, retrying...")
                self.connected = False
                self.world = None
                self._init_attempted = False

    def set_joint_positions(self, action):
        if not self.world:
            return
        print(f"[Action] {action}")

    def get_camera_rgb(self):
        return "RGB_IMAGE" if self.world else None

    def get_depth(self):
        return "DEPTH_IMAGE" if self.world else None

    def get_lidar(self):
        return "LIDAR_SCAN" if self.world else None

    def fuse_sensors(self):
        return {
            "vision": self.get_camera_rgb(),
            "depth": self.get_depth(),
            "lidar": self.get_lidar()
        }

    def reset_sim(self):
        if self.world is None:
            self.init_world()

        if self.world:
            try:
                self.world.reset()

                import omni.timeline
                timeline = omni.timeline.get_timeline_interface()
                timeline.play()

                return self.fuse_sensors()

            except Exception as e:
                print("[Reset Error]", e)

        return {"obs": "reset_stub"}

    def step_sim(self, action):
        if self.world is None:
            return self.fuse_sensors(), 0.0, True

        print(f"[IsaacSim Step] {action}")

        self.set_joint_positions(action)
        self._step_physics()

        obs = self.fuse_sensors()
        reward = 1.0 if action else 0.0
        done = False

        return obs, reward, done

    def send_action(self, action):
        return self.step_sim(action)

    def apply_action(self, action):
        return self.step_sim(action)


# =========================
# ✅ MAIN RUNNER (OUTSIDE CLASS)
# =========================
if __name__ == "__main__":
    print("[SYSTEM] Starting OmniClient test...")

    client = OmniClient()

    obs = client.reset_sim()
    print("[RESET DONE]", obs)

    for i in range(5):
        obs, reward, done = client.step_sim({"type": "move", "value": "forward"})
        print(f"[STEP {i}] Reward:", reward)

        if done:
            print("[DONE] Episode finished")
            break

    print("[SYSTEM] Finished")