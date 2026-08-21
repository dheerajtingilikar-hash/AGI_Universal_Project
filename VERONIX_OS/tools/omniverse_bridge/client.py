import numpy as np

class OmniClient:
    def __init__(self):
        self.connected = False
        self.world = None
        self.stage = None
        self.robot = None
        self._init_attempted = False

        print("[OmniClient] Initializing RL-ready Isaac interface...")
        print("[OmniClient] Waiting for Isaac runtime...")

    # =========================
    # WORLD INIT (RETRY SAFE)
    # =========================
    def init_world(self):
        if self.world is not None:
            return

        # Force a retry by clearing the attempted flag if not connected
        if self._init_attempted and not self.connected:
            self._init_attempted = False

        if self._init_attempted:
            return

        self._init_attempted = True

        try:
            # Multi-API Compatibility
            try:
                from isaacsim.core.api.world import World
                print("[DEBUG] Using NEW Isaac API")
            except Exception:
                from omni.isaac.core import World
                print("[DEBUG] Using OLD Isaac API")

            self.world = World()
            self.world.reset()

            # Start the timeline (Crucial for physics to actually move)
            import omni.timeline
            timeline = omni.timeline.get_timeline_interface()
            timeline.play()

            self.connected = True
            print("[OmniClient] Isaac World Initialized")

        except Exception as e:
            print("[OmniClient] STUB MODE ACTIVE (Isaac not found or loading)")
            self.connected = False
            # Don't print full stack trace to avoid spam, just the reason
            print("[Reason]", str(e)[:100]) 

    # =========================
    # PHYSICS STEP (SELF-HEAL)
    # =========================
    def _step_physics(self):
        if not self.connected or self.world is None:
            self.init_world()

        if self.world:
            try:
                # render=True allows the UI/Camera to update
                self.world.step(render=True)
            except Exception:
                print("[PhysX Step Error] Connection lost, resetting client...")
                self.connected = False
                self.world = None
                self._init_attempted = False

    # =========================
    # ACTION (ROBOT INTERFACE)
    # =========================
    def set_joint_positions(self, action):
        if not self.connected:
            return
        # This will eventually connect to: 
        # self.robot.get_articulation_controller().apply_action(action)
        print(f"[IsaacAction] Applying: {action}")

    # =========================
    # SENSORS (STUB)
    # =========================
    def get_camera_rgb(self):
        return "RGB_IMAGE_DATA" if self.connected else None

    def get_depth(self):
        return "DEPTH_MAP_DATA" if self.connected else None

    def get_lidar(self):
        return "LIDAR_POINT_CLOUD" if self.connected else None

    def fuse_sensors(self):
        return {
            "vision": self.get_camera_rgb(),
            "depth": self.get_depth(),
            "lidar": self.get_lidar(),
            "status": "active" if self.connected else "stub"
        }

    # =========================
    # RESET
    # =========================
    def reset_sim(self):
        if not self.connected:
            self.init_world()

        if self.world:
            try:
                self.world.reset()
                import omni.timeline
                omni.timeline.get_timeline_interface().play()
                return self.fuse_sensors()
            except Exception as e:
                print("[Reset Error]", e)

        return {"obs": "reset_stub", "status": "reconnecting"}

    # =========================
    # STEP (CORE RL LOOP)
    # =========================
    def step_sim(self, action):
        # Fallback if sim is down
        if not self.connected:
            self._step_physics() # Try to reconnect
            return self.fuse_sensors(), 0.0, True

        # 1. APPLY ACTION (Must happen before physics step)
        self.set_joint_positions(action)

        # 2. STEP PHYSICS
        self._step_physics()

        # 3. OBSERVE
        obs = self.fuse_sensors()

        # 4. REWARD (Logic to be expanded based on your goals.py)
        reward = 1.0 if action is not None else 0.0

        # 5. DONE
        done = not self.connected

        return obs, reward, done

    # =========================
    # ENTRY POINTS
    # =========================
    def send_action(self, action):
        return self.step_sim(action)

    def apply_action(self, action):
        return self.step_sim(action)