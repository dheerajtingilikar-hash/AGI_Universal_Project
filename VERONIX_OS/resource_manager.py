"""
VERONIX Resource Management
Ensures proper cleanup of temporary files, file handles, and other resources
"""
import os
import tempfile
import logging
from pathlib import Path
from contextlib import contextmanager
from typing import Generator

logger = logging.getLogger("RESOURCES")

# ==============================================================================
# RESOURCE MANAGER
# ==============================================================================
class ResourceManager:
    """Tracks and manages temporary resources"""
    
    def __init__(self):
        self.temp_files = []
        self.open_handles = []
    
    def create_temp_file(self, suffix: str = ".tmp", prefix: str = "veronix_"):
        """Create and track a temporary file"""
        try:
            temp_file = tempfile.NamedTemporaryFile(
                delete=False,
                suffix=suffix,
                prefix=prefix
            )
            self.temp_files.append(temp_file.name)
            logger.debug(f"Created temp file: {temp_file.name}")
            return temp_file
        except Exception as e:
            logger.error(f"Failed to create temp file: {e}")
            return None
    
    def cleanup_temp_files(self):
        """Clean up all tracked temporary files"""
        for file_path in self.temp_files:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    logger.debug(f"Cleaned up temp file: {file_path}")
            except Exception as e:
                logger.warning(f"Failed to remove temp file {file_path}: {e}")
        
        self.temp_files.clear()
    
    def __del__(self):
        """Ensure cleanup on object deletion"""
        self.cleanup_temp_files()

# ==============================================================================
# CONTEXT MANAGERS FOR RESOURCE SAFETY
# ==============================================================================
@contextmanager
def safe_file_read(file_path: str, encoding: str = "utf-8") -> Generator[str, None, None]:
    """
    Context manager for safe file reading with automatic cleanup
    
    Usage:
        with safe_file_read("myfile.txt") as content:
            print(content)
    """
    file_handle = None
    try:
        file_handle = open(file_path, "r", encoding=encoding, errors="ignore")
        content = file_handle.read()
        yield content
    except FileNotFoundError:
        logger.warning(f"File not found: {file_path}")
        yield ""
    except Exception as e:
        logger.error(f"Error reading file {file_path}: {e}")
        yield ""
    finally:
        if file_handle:
            try:
                file_handle.close()
            except Exception as e:
                logger.warning(f"Error closing file {file_path}: {e}")

@contextmanager
def safe_file_write(file_path: str, encoding: str = "utf-8") -> Generator:
    """
    Context manager for safe file writing with automatic cleanup
    
    Usage:
        with safe_file_write("myfile.txt") as f:
            f.write("content")
    """
    file_handle = None
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
        file_handle = open(file_path, "w", encoding=encoding)
        yield file_handle
    except Exception as e:
        logger.error(f"Error opening file {file_path} for writing: {e}")
        yield None
    finally:
        if file_handle:
            try:
                file_handle.close()
                logger.debug(f"Successfully wrote to: {file_path}")
            except Exception as e:
                logger.warning(f"Error closing file {file_path}: {e}")

@contextmanager
def safe_temp_file(suffix: str = ".tmp") -> Generator[str, None, None]:
    """
    Context manager for safe temporary file usage with automatic cleanup
    
    Usage:
        with safe_temp_file(suffix=".mp3") as temp_path:
            # Use temp_path
            # File is automatically cleaned up when done
    """
    temp_file = None
    try:
        temp_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix,
            prefix="veronix_"
        )
        temp_path = temp_file.name
        temp_file.close()
        yield temp_path
    except Exception as e:
        logger.error(f"Error creating temp file: {e}")
        yield None
    finally:
        if temp_file and os.path.exists(temp_file.name):
            try:
                os.remove(temp_file.name)
                logger.debug(f"Cleaned up temp file: {temp_file.name}")
            except Exception as e:
                logger.warning(f"Error cleaning up temp file: {e}")

# ==============================================================================
# DIRECTORY UTILITIES
# ==============================================================================
def ensure_directory_exists(directory_path: str) -> bool:
    """
    Ensure a directory exists, creating it if necessary
    
    Returns:
        True if directory exists or was created successfully
    """
    try:
        Path(directory_path).mkdir(parents=True, exist_ok=True)
        logger.debug(f"Directory ensured: {directory_path}")
        return True
    except Exception as e:
        logger.error(f"Failed to create directory {directory_path}: {e}")
        return False

def cleanup_old_files(directory_path: str, pattern: str = "*", max_age_days: int = 7):
    """
    Clean up old files in a directory
    
    Args:
        directory_path: Directory to clean
        pattern: File pattern to match (e.g., "*.tmp")
        max_age_days: Files older than this many days are deleted
    """
    import time
    from pathlib import Path
    
    try:
        path = Path(directory_path)
        if not path.exists():
            return
        
        current_time = time.time()
        max_age_seconds = max_age_days * 24 * 3600
        
        for file_path in path.glob(pattern):
            if file_path.is_file():
                file_age = current_time - file_path.stat().st_mtime
                if file_age > max_age_seconds:
                    try:
                        file_path.unlink()
                        logger.info(f"Deleted old file: {file_path}")
                    except Exception as e:
                        logger.warning(f"Failed to delete {file_path}: {e}")
    except Exception as e:
        logger.error(f"Error cleaning up old files in {directory_path}: {e}")

# ==============================================================================
# GLOBAL RESOURCE MANAGER
# ==============================================================================
_global_resource_manager = ResourceManager()

def get_resource_manager() -> ResourceManager:
    """Get the global resource manager instance"""
    return _global_resource_manager

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    
    # Test context managers
    print("Testing resource management...")
    
    # Test temp file
    with safe_temp_file(suffix=".txt") as temp_path:
        print(f"Created temp file: {temp_path}")
        if temp_path and os.path.exists(temp_path):
            with safe_file_write(temp_path) as f:
                f.write("Test content")
            
            with safe_file_read(temp_path) as content:
                print(f"Read content: {content}")
    
    print("✓ Resource management module loaded successfully")
