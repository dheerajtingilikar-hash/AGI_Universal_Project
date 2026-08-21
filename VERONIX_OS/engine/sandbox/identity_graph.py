class IdentityGraph:
    def __init__(self):
        self.memory_nodes = []

    def add_experience(self, text):
        self.memory_nodes.append(text)

    def compress(self):
        # simple memory compression
        if len(self.memory_nodes) > 100:
            self.memory_nodes = self.memory_nodes[-50:]