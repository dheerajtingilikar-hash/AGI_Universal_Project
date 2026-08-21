import time
import threading
from ollama import Client

client = Client(host="http://127.0.0.1:11434")

MODEL = "llama3.2:1b"  # match your main.py

THINKING_ENABLED = True


class Thinker:
    """
    Main reasoning layer for VERONIX
    """

    def __init__(self):
        self.memory = []

    def process(self, user_input: str, intent: str):
        """
        Converts raw input into structured prompt
        """

        context = "\n".join(self.memory[-5:])  # short memory window

        prompt = f"""
You are VERONIX OS AI.

Intent: {intent}

Recent context:
{context}

User input:
{user_input}

Respond briefly and clearly.
"""

        self.memory.append(user_input)

        return prompt


# =========================
# AUTONOMOUS THINKER LOOP
# =========================

def think_cycle():
    while THINKING_ENABLED:
        try:
            time.sleep(15)

            response = client.chat(
                model=MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You are VERONIX internal optimizer."
                    },
                    {
                        "role": "user",
                        "content": "Suggest ONE improvement in reasoning, memory, or tools."
                    }
                ]
            )

            idea = response["message"]["content"]
            print("\n🧠 [THINKER]:", idea)

        except Exception as e:
            print("[THINKER ERROR]", e)
            time.sleep(5)


def start_thinker():
    thread = threading.Thread(target=think_cycle, daemon=True)
    thread.start()