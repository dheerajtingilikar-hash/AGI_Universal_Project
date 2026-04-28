# AGI/core/agent.py

from ollama import Client

client = Client(host="http://127.0.0.1:11434")
MODEL = "llama3.2:3b"

def generate(user_input, state):
    prompt = f"""
You are Veronix AI.

Emotion: {state.emotion}
Curiosity: {state.curiosity}

User: {user_input}

Respond naturally.
"""

    res = client.chat(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    return res["message"]["content"]