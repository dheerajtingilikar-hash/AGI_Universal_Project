import time

class SleepCycle:
    def __init__(self, identity_graph):
        self.identity = identity_graph

    def sleep(self):
        print("[SLEEP] Compressing identity memory...")
        self.identity.compress()
        time.sleep(1)
        print("[SLEEP] Memory stabilized.")