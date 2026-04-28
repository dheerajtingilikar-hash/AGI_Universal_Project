# AGI/engine/background.py

import time
from ollama import Client

client = Client(host="http://127.0.0.1:11434")
MODEL = "llama3.2:3b"

def start_background(state, shutdown):

    def loop():
        while not shutdown.is_set():
            time.sleep(15)

            if state.curiosity < 0.3:
                continue

            try:
                res = client.chat(
                    model=MODEL,
                    messages=[{
                        "role": "user",
                        "content": "Suggest one improvement to your own system."
                    }]
                )

                state.last_thought = res["message"]["content"]

            except:
                pass

    import threading
    threading.Thread(target=loop, daemon=True).start()