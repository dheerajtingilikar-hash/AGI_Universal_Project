class IsaacSensorSystem:
    def __init__(self, camera, robot):
        self.camera = camera
        self.robot = robot

    def get_observation(self):
        rgb = self.camera.get_rgba()
        joints = self.robot.get_joint_positions()

        return {
            "vision": rgb,
            "state": joints
        }