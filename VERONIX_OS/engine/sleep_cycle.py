# AGI/engine/sleep_cycle.py

import time
from ollama import Client

client = Client(host="http://127.0.0.1:11434")
MODEL = "llama3.2:3b"

compressed_memory = []

def sleep_cycle(memory, world_model):
    """
    Compress memory into abstract knowledge
    """

    raw = str(memory.search("boss"))

    prompt = f"""
Summarize and compress this memory into key insights:

{raw}

Return only compressed knowledge points.
"""

    res = client.chat(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    compressed_memory.append(res["message"]["content"])

    # simulate "forgetting noise"
    memory.clear_old()

    world_model.update_event("Sleep cycle completed")

    return compressed_memory