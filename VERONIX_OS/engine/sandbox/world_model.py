class WorldModel:
    def __init__(self):
        self.state = {
            "events": [],
            "goals": []
        }

    def update(self, event: str):
        self.state["events"].append(event)

    def simulate(self, query: str):
        return f"[SIMULATION] If this happens: '{query}', likely outcome is computed from internal model."