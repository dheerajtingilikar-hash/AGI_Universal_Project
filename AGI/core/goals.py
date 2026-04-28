# AGI/core/goals.py

from ollama import Client

client = Client(host="http://127.0.0.1:11434")
MODEL = "llama3.2:3b"

def generate_goal(state):
    prompt = f"""
You are an AI system.

Current emotion: {state.emotion}
Curiosity: {state.curiosity}

Generate ONE useful short-term goal for improvement.
"""

    res = client.chat(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    return res["message"]["content"]