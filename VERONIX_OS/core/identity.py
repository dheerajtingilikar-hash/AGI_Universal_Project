# AGI/core/identity.py

class IdentityGraph:
    def __init__(self):
        self.nodes = {
            "self": {
                "traits": [],
                "beliefs": [],
                "history": []
            }
        }

    def add_trait(self, trait):
        self.nodes["self"]["traits"].append(trait)

    def add_belief(self, belief):
        self.nodes["self"]["beliefs"].append(belief)

    def add_event(self, event):
        self.nodes["self"]["history"].append(event)

    def summary(self):
        return {
            "traits": self.nodes["self"]["traits"][-5:],
            "beliefs": self.nodes["self"]["beliefs"][-5:],
            "recent_history": self.nodes["self"]["history"][-5:]
        }