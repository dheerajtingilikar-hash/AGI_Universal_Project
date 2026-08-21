# AGI/core/planner.py

import time
from ollama import Client

client = Client(host="http://127.0.0.1:11434")
MODEL = "llama3.2:3b"

class PlannerLoop:
    def __init__(self):
        self.plan = []
        self.last_update = time.time()

    def generate_plan(self, state, world_model):
        prompt = f"""
You are a planning engine.

State:
Emotion: {state.emotion}
Curiosity: {state.curiosity}

World:
{world_model.get_context()}

Generate 3-step long-term plan.
"""

        res = client.chat(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}]
        )

        self.plan = res["message"]["content"]
        self.last_update = time.time()

        return self.plan

    def tick(self, state, world_model):
        # regenerate plan every 30 seconds
        if time.time() - self.last_update > 30:
            return self.generate_plan(state, world_model)
        return self.plan