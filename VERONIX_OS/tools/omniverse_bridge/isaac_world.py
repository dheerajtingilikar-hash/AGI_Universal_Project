from omni.isaac.kit import SimulationApp
from omni.isaac.core import World


class IsaacWorld:
    def __init__(self):
        self.sim_app = SimulationApp({"headless": False})
        self.world = World(stage_units_in_meters=1.0)

    def load(self):
        self.world.reset()

    def step(self):
        self.world.step(render=True)

    def stop(self):
        self.sim_app.close()