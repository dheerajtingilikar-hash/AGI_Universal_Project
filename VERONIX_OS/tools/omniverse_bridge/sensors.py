class SensorModule:
    def __init__(self, client):
        self.client = client

    def observe(self):
        return {
            "rgb": self.client.get_camera_rgb(),
            "depth": self.client.get_depth(),
            "state": self.client.get_robot_state()
        }