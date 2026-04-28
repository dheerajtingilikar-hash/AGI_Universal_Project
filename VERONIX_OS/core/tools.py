# AGI/core/tools.py

import os
import webbrowser
import logging

# Import error handling utilities
try:
    from error_handling import safe_read_file, safe_write_file, logger
except ImportError:
    # Fallback logging if error_handling not available
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("TOOLS")
    
    def safe_read_file(path, encoding="utf-8", default_return="", log_errors=True):
        try:
            with open(path, "r", encoding=encoding, errors="ignore") as f:
                return f.read()
        except Exception as e:
            if log_errors:
                logger.error(f"Error reading {path}: {e}")
            return default_return
    
    def safe_write_file(path, content, encoding="utf-8", log_errors=True):
        try:
            with open(path, "w", encoding=encoding) as f:
                f.write(content)
            return True
        except Exception as e:
            if log_errors:
                logger.error(f"Error writing to {path}: {e}")
            return False

def read_file(path):
    """Read file with improved error handling and logging"""
    try:
        content = safe_read_file(path, default_return="")
        if content:
            logger.info(f"✓ Successfully read file: {path}")
            return content
        else:
            error_msg = f"File is empty or unreadable: {path}"
            logger.warning(error_msg)
            return "Error reading file."
    except Exception as e:
        error_msg = f"Error reading file {path}: {e}"
        logger.error(error_msg)
        return f"Error reading file: {str(e)}"

def write_file(path, content):
    """Write file with improved error handling and logging"""
    try:
        success = safe_write_file(path, content)
        if success:
            logger.info(f"✓ Successfully wrote to file: {path}")
            return "Written successfully."
        else:
            error_msg = f"Failed to write to file: {path}"
            logger.error(error_msg)
            return "Write failed."
    except Exception as e:
        error_msg = f"Error writing to {path}: {e}"
        logger.error(error_msg)
        return f"Write failed: {str(e)}"

def open_browser(url):
    """Open browser with improved error handling and logging"""
    try:
        webbrowser.open(url)
        logger.info(f"✓ Opened browser with URL: {url}")
        return "Opened browser."
    except Exception as e:
        error_msg = f"Failed to open browser for {url}: {e}"
        logger.error(error_msg)
        return f"Failed to open browser: {str(e)}"

def tool_executor(command):
    """
    SAFE TOOL ROUTER
    """
    if command["type"] == "read":
        return read_file(command["path"])

    if command["type"] == "write":
        return write_file(command["path"], command["content"])

    if command["type"] == "web":
        return open_browser(command["url"])

    return "Unknown tool"