class VisionModel:
    def perceive(self, frame):
        # fake perception output
        return {
            "objects": ["agent", "environment"],
            "confidence": 0.87
        }