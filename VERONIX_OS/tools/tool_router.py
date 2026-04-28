class ToolRouter:
    def route(self, user_input):

        text = user_input.lower()

        # scoring system (light semantic logic)
        research_score = 0

        triggers = ["search", "research", "what is", "who is", "find", "look up"]

        for t in triggers:
            if t in text:
                research_score += 1

        if research_score > 0:
            return {
                "tool": "research",
                "confidence": research_score,
                "query": self._clean(text)
            }

        return {
            "tool": "llm",
            "confidence": 1
        }

    def _clean(self, text):
        noise = [
            "search", "research", "find", "look up",
            "please", "can you", "veronix", "about", "for"
        ]

        for n in noise:
            text = text.replace(n, "")

        return text.strip()