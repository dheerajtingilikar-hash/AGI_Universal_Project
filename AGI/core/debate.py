# AGI/core/debate.py

from ollama import Client

client = Client(host="http://127.0.0.1:11434")
MODEL = "llama3.2:3b"

def debate(prompt):
    roles = ["Planner", "Critic", "Final Agent"]

    outputs = []

    for role in roles:
        res = client.chat(
            model=MODEL,
            messages=[{
                "role": "user",
                "content": f"You are {role}. Respond to: {prompt}"
            }]
        )
        outputs.append(res["message"]["content"])

    return "\n\n".join(outputs)