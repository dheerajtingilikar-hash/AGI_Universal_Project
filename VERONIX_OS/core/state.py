# AGI/core/state.py

class BrainState:
    def __init__(self):
        self.emotion = "neutral"
        self.energy = 1.0
        self.curiosity = 0.5
        self.last_thought = None
        self.active_task = None

    def update_emotion(self, text):
        t = text.lower()

        if "help" in t:
            self.emotion = "focused"
            self.curiosity += 0.1
        elif "error" in t:
            self.emotion = "analytical"
        elif "love" in t:
            self.emotion = "warm"
        else:
            self.emotion = "neutral"

        self.curiosity = min(1.0, max(0.0, self.curiosity))