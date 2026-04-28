class IsaacActionController:
    def __init__(self, robot):
        self.robot = robot

    def apply_action(self, joint_targets):
        """
        joint_targets: list/array of joint positions or torques
        """
        self.robot.set_joint_positions(joint_targets)