class OmniClient:
    def __init__(self):
        self.connected = True
        print("[OmniClient] Initialized (placeholder connection)")

    # =========================
    # SIM CONTROL (PLACEHOLDER)
    # =========================
    def reset_sim(self):
        print("[IsaacSim] Resetting simulation")
        return {}

    def apply_action(self, action):
        print(f"[IsaacSim] Action applied: {action}")
        return {"state": "updated"}

    def get_reward(self):
        return 1.0

    def is_done(self):
        return False

    # =========================
    # SENSOR PLACEHOLDERS
    # =========================
    def get_camera_rgb(self):
        return None

    def get_depth(self):
        return None

    def get_robot_state(self):
        return {"joints": []}

    # =========================
    # FIXED ACTION API (IMPORTANT)
    # =========================
    def send_action(self, action):
        """
        Unified action interface for OmniLoop / ActionModule
        """
        print(f"[IsaacSim] Action sent: {action}")
        return self.apply_action(action)

    # backward compatibility (optional safety)
    def send_robot_command(self, action):
        return self.send_action(action)