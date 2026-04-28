"""
VERONIX Enhanced Error Handling & Logging
Provides robust error handling with proper logging instead of silent failures
"""
import logging
import sys
from functools import wraps
from typing import Optional, Callable, Any

# ==============================================================================
# LOGGER SETUP
# ==============================================================================
logger = logging.getLogger("VERONIX")
logger.setLevel(logging.INFO)

# Console handler
if not logger.handlers:
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] %(name)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

# ==============================================================================
# EXCEPTION WRAPPER
# ==============================================================================
class VeironixException(Exception):
    """Base exception for VERONIX errors"""
    pass

class MemoryException(VeironixException):
    """Memory system error"""
    pass

class ToolException(VeironixException):
    """Tool execution error"""
    pass

class ConfigException(VeironixException):
    """Configuration error"""
    pass

# ==============================================================================
# DECORATOR: Safe Error Handling
# ==============================================================================
def safe_call(
    default_return: Any = None,
    error_message: str = None,
    log_level: str = "WARNING",
    raise_exception: bool = False
):
    """
    Decorator to safely call functions with error handling
    
    Args:
        default_return: Value to return if exception occurs
        error_message: Custom error message
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        raise_exception: Re-raise exception after logging
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                msg = error_message or f"Error in {func.__name__}: {str(e)}"
                log_func = getattr(logger, log_level.lower(), logger.warning)
                log_func(msg)
                
                if raise_exception:
                    raise
                
                return default_return
        
        return wrapper
    return decorator

# ==============================================================================
# UTILITY: Safe File Operations
# ==============================================================================
def safe_read_file(
    file_path: str,
    encoding: str = "utf-8",
    default_return: str = "",
    log_errors: bool = True
) -> str:
    """
    Safely read file with proper error handling
    
    Args:
        file_path: Path to file
        encoding: File encoding (default: utf-8)
        default_return: Return value on error
        log_errors: Log errors if True
    
    Returns:
        File content or default_return on error
    """
    try:
        with open(file_path, "r", encoding=encoding, errors="ignore") as f:
            content = f.read()
            return content
    except FileNotFoundError:
        if log_errors:
            logger.warning(f"File not found: {file_path}")
    except Exception as e:
        if log_errors:
            logger.error(f"Error reading {file_path}: {e}")
    
    return default_return

def safe_write_file(
    file_path: str,
    content: str,
    encoding: str = "utf-8",
    log_errors: bool = True
) -> bool:
    """
    Safely write file with proper error handling
    
    Args:
        file_path: Path to file
        content: Content to write
        encoding: File encoding (default: utf-8)
        log_errors: Log errors if True
    
    Returns:
        True on success, False on error
    """
    try:
        with open(file_path, "w", encoding=encoding) as f:
            f.write(content)
        return True
    except Exception as e:
        if log_errors:
            logger.error(f"Error writing to {file_path}: {e}")
        return False

# ==============================================================================
# UTILITY: Safe Dictionary Operations
# ==============================================================================
def safe_dict_get(dictionary: dict, key: str, default: Any = None) -> Any:
    """Safely get dict value with logging"""
    try:
        return dictionary.get(key, default)
    except Exception as e:
        logger.warning(f"Error accessing dict key {key}: {e}")
        return default

# ==============================================================================
# UTILITY: Log Function Execution
# ==============================================================================
def log_execution(func_name: str, status: str, details: str = ""):
    """Log function execution status"""
    msg = f"[{func_name}] {status}"
    if details:
        msg += f" - {details}"
    logger.info(msg)

if __name__ == "__main__":
    logger.info("Error handling module loaded")
    
    # Test safe read
    content = safe_read_file("nonexistent.txt", default_return="test default")
    print(f"Read test result: '{content}'")
