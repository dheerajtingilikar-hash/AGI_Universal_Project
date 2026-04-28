# AGI/core/self_modify.py

from ollama import Client

client = Client(host="http://127.0.0.1:11434")
MODEL = "llama3.2:3b"

class SelfImprover:
    def __init__(self):
        self.suggestions = []

    def analyze(self, logs):
        prompt = f"""
You are a system optimizer.

Analyze this system behavior:
{logs}

Return ONLY improvements as bullet points.
"""

        res = client.chat(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}]
        )

        self.suggestions.append(res["message"]["content"])
        return res["message"]["content"]