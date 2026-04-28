"""
VERONIX Configuration Management
Centralizes all paths and configuration to avoid hard-coding
"""
import os
from pathlib import Path

# ==============================================================================
# BASE PATHS (Dynamic - no hard-coding)
# ==============================================================================
VERONIX_ROOT = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(VERONIX_ROOT)
BRAIN_DATA_DIR = os.path.join(PROJECT_ROOT, "Brain_Data")
KNOWLEDGE_BASE_DIR = os.path.join(PROJECT_ROOT, "Knowledge_Base")
MODELS_DIR = os.path.join(PROJECT_ROOT, "Models")

# ==============================================================================
# OLLAMA CONFIGURATION
# ==============================================================================
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2:3b")
OLLAMA_EMBEDDER = os.environ.get("OLLAMA_EMBEDDER", "nomic-embed-text")

# ==============================================================================
# VOICE/TTS CONFIGURATION
# ==============================================================================
TTS_VOICE = os.environ.get("TTS_VOICE", "en-US-AriaNeural")
TTS_RATE = os.environ.get("TTS_RATE", "+0%")
TTS_VOLUME = os.environ.get("TTS_VOLUME", "+0%")

# ==============================================================================
# UI CONFIGURATION
# ==============================================================================
UI_WIDTH = int(os.environ.get("UI_WIDTH", "1400"))
UI_HEIGHT = int(os.environ.get("UI_HEIGHT", "900"))
ENABLE_HIGH_DPI = os.environ.get("ENABLE_HIGH_DPI", "true").lower() == "true"

# ==============================================================================
# LOGGING CONFIGURATION
# ==============================================================================
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
LOG_FILE = os.path.join(PROJECT_ROOT, "veronix.log")
MAX_LOG_SIZE = 10 * 1024 * 1024  # 10 MB

# ==============================================================================
# MEMORY CONFIGURATION
# ==============================================================================
MEMORY_USER_ID = os.environ.get("MEMORY_USER_ID", "boss")
MEMORY_SAVE_ERRORS = True  # Set to True to log memory errors

# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================
def ensure_directory(directory_path):
    """Ensure a directory exists, create if needed"""
    Path(directory_path).mkdir(parents=True, exist_ok=True)
    return directory_path

def get_brain_dir():
    """Get Brain Data directory, creating if necessary"""
    ensure_directory(BRAIN_DATA_DIR)
    return BRAIN_DATA_DIR

def get_models_dir():
    """Get Models directory, creating if necessary"""
    ensure_directory(MODELS_DIR)
    return MODELS_DIR

def get_knowledge_dir():
    """Get Knowledge Base directory, creating if necessary"""
    ensure_directory(KNOWLEDGE_BASE_DIR)
    return KNOWLEDGE_BASE_DIR

# ==============================================================================
# VALIDATION
# ==============================================================================
def validate_config():
    """Check if all required directories exist"""
    warnings = []
    
    required_dirs = {
        "Project Root": PROJECT_ROOT,
        "VERONIX Root": VERONIX_ROOT,
        "Brain Data": BRAIN_DATA_DIR,
    }
    
    for name, path in required_dirs.items():
        if not os.path.exists(path):
            warnings.append(f" {name} not found: {path}")
    
    return warnings

if __name__ == "__main__":
    print(f"✓ VERONIX_ROOT: {VERONIX_ROOT}")
    print(f"✓ PROJECT_ROOT: {PROJECT_ROOT}")
    print(f"✓ BRAIN_DATA_DIR: {BRAIN_DATA_DIR}")
    print(f"✓ OLLAMA_HOST: {OLLAMA_HOST}")
    print(f"✓ OLLAMA_MODEL: {OLLAMA_MODEL}")
    
    warnings = validate_config()
    if warnings:
        print("\nWarnings:")
        for w in warnings:
            print(f"  {w}")
