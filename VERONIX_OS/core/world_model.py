# AGI/core/world_model.py

class WorldModel:
    """
    Lightweight persistent internal simulation state.
    NOT a real physics/world simulator — it's a cognitive abstraction.
    """

    def __init__(self):
        self.state = {
            "users": {},
            "system_health": "stable",
            "knowledge_graph": {},
            "events": []
        }

    def update_event(self, event):
        self.state["events"].append(event)
        self.state["events"] = self.state["events"][-100:]  # limit memory

    def update_user_state(self, user, data):
        self.state["users"][user] = data

    def get_context(self):
        return {
            "system_health": self.state["system_health"],
            "recent_events": self.state["events"][-5:],
            "users": list(self.state["users"].keys())
        }