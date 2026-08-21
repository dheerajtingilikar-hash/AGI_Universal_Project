from mem0 import Memory
import os
import logging

# Try to use centralized config, fall back to direct imports
try:
    from config import get_brain_dir, OLLAMA_HOST, OLLAMA_MODEL, OLLAMA_EMBEDDER, MEMORY_USER_ID
except ImportError:
    # Fallback to direct path construction
    ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    def get_brain_dir():
        brain_dir = os.path.join(ROOT, "Brain_Data")
        os.makedirs(brain_dir, exist_ok=True)
        return brain_dir
    
    OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434")
    OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2:3b")
    OLLAMA_EMBEDDER = os.environ.get("OLLAMA_EMBEDDER", "nomic-embed-text")
    MEMORY_USER_ID = os.environ.get("MEMORY_USER_ID", "boss")

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MEMORY")

BRAIN_DIR = get_brain_dir()

try:
    memory = Memory.from_config({
        "llm": {
            "provider": "ollama",
            "config": {"model": OLLAMA_MODEL, "ollama_base_url": OLLAMA_HOST}
        },
        "embedder": {
            "provider": "ollama",
            "config": {"model": OLLAMA_EMBEDDER, "ollama_base_url": OLLAMA_HOST}
        },
        "vector_store": {
            "provider": "qdrant",
            "config": {"path": BRAIN_DIR}
        }
    })
    logger.info(f"✓ Memory system initialized with brain_dir: {BRAIN_DIR}")
except Exception as e:
    logger.error(f"Failed to initialize memory system: {e}")
    memory = None

def save(text):
    """Save text to memory with error logging"""
    if memory is None:
        logger.warning("Memory system not initialized, cannot save")
        return False
    
    try:
        memory.add(text, user_id=MEMORY_USER_ID)
        logger.info(f"✓ Saved to memory (user: {MEMORY_USER_ID}): {text[:50]}...")
        return True
    except Exception as e:
        logger.error(f"Memory save error for user {MEMORY_USER_ID}: {e}")
        return False

def search(query):
    """Search memory with error logging"""
    if memory is None:
        logger.warning("Memory system not initialized, cannot search")
        return []
    
    try:
        results = memory.search(query, filters={"user_id": MEMORY_USER_ID})
        if results:
            logger.info(f"✓ Memory search found {len(results)} results for: {query}")
        return results or []
    except Exception as e:
        logger.error(f"Memory search error for query '{query}': {e}")
        return []