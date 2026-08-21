# AGI/core/context.py

import os
import numpy as np
from ollama import Client

client = Client(host="http://127.0.0.1:11434")
KB = r"D:\AGI_Universal_Project\Knowledge_Base"

def embed(text):
    return np.array(client.embeddings(model="nomic-embed-text", prompt=text)["embedding"])

def build_context(user_input):
    best = []

    for f in os.listdir(KB):
        if not f.endswith(".md"):
            continue

        path = os.path.join(KB, f)
        data = open(path, encoding="utf-8", errors="ignore").read()

        score = np.dot(embed(user_input), embed(data[:500]))
        best.append((score, data[:200]))

    best.sort(reverse=True, key=lambda x: x[0])
    return "\n".join([b[1] for b in best[:3]])