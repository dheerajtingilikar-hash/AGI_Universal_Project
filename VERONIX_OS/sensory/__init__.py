"""
VERONIX Sensory Module
Handles STT (Speech-to-Text) and TTS (Text-to-Speech)
"""

from .listen import STTEngine
from .voice import TTSEngine

__all__ = ["STTEngine", "TTSEngine"]