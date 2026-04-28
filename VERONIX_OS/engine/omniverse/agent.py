from ollama import Client

class ReasoningAgent:
    def __init__(self):
        self.llm = Client(host="http://127.0.0.1:11434")

    def think(self, observation):
        response = self.llm.chat(
            model="llama3.2:3b",
            messages=[{
                "role": "user",
                "content": f"You are an embodied agent. Decide based on: {observation}"
            }]
        )

        return response["message"]["content"]