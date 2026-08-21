"""
VERONIX Project Setup & Validation Script
Run this after installation to verify everything is configured correctly
"""
import os
import sys
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s'
)
logger = logging.getLogger("SETUP")

# ==============================================================================
# PROJECT ROOT
# ==============================================================================
SETUP_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = SETUP_DIR
VERONIX_OS = os.path.join(PROJECT_ROOT, "VERONIX_OS")

# ==============================================================================
# VALIDATION FUNCTIONS
# ==============================================================================
def check_directories():
    """Check if required directories exist"""
    logger.info("Checking directories...")
    
    required_dirs = {
        "VERONIX_OS": VERONIX_OS,
        "Knowledge_Base": os.path.join(PROJECT_ROOT, "Knowledge_Base"),
        "Brain_Data": os.path.join(PROJECT_ROOT, "Brain_Data"),
        "Models": os.path.join(PROJECT_ROOT, "Models"),
    }
    
    errors = []
    for name, path in required_dirs.items():
        if os.path.exists(path):
            logger.info(f"  ✓ {name}: {path}")
        else:
            logger.warning(f"  ⚠ {name} not found: {path}")
            errors.append(name)
    
    return errors

def check_python_modules():
    """Check if required Python modules are installed"""
    logger.info("\nChecking Python modules...")
    
    required_modules = {
        "PyQt5": "GUI Framework",
        "numpy": "Numerical Computing",
        "ollama": "LLM Integration",
        "torch": "Deep Learning",
        "edge_tts": "Text-to-Speech",
        "transformers": "Transformers Library",
        "mem0": "Memory Management",
        "qdrant_client": "Vector Database",
    }
    
    missing = []
    for module_name, description in required_modules.items():
        try:
            __import__(module_name)
            logger.info(f"  ✓ {module_name}: {description}")
        except ImportError:
            logger.warning(f"  ✗ {module_name}: NOT INSTALLED ({description})")
            missing.append(module_name)
    
    return missing

def check_config_files():
    """Check if configuration files exist"""
    logger.info("\nChecking configuration files...")
    
    config_files = {
        "VERONIX_OS/config.py": "Project Configuration",
        "VERONIX_OS/error_handling.py": "Error Handling Module",
        "VERONIX_OS/resource_manager.py": "Resource Manager",
    }
    
    missing = []
    for file_path, description in config_files.items():
        full_path = os.path.join(PROJECT_ROOT, file_path)
        if os.path.exists(full_path):
            logger.info(f"  ✓ {file_path}: {description}")
        else:
            logger.warning(f"  ✗ {file_path}: NOT FOUND ({description})")
            missing.append(file_path)
    
    return missing

def check_ollama():
    """Check if Ollama is running"""
    logger.info("\nChecking Ollama connection...")
    
    try:
        import httpx
        response = httpx.get("http://127.0.0.1:11434", timeout=2)
        if response.status_code == 200:
            logger.info("  ✓ Ollama is running on 127.0.0.1:11434")
            return True
        else:
            logger.warning(f"  ⚠ Ollama returned status {response.status_code}")
            return False
    except Exception as e:
        logger.warning(f"  ✗ Ollama not accessible: {e}")
        logger.info("    → Start Ollama with: ollama serve")
        return False

def check_env_file():
    """Check if .env file exists"""
    logger.info("\nChecking environment configuration...")
    
    env_path = os.path.join(PROJECT_ROOT, ".env")
    template_path = os.path.join(PROJECT_ROOT, ".env.template")
    
    if os.path.exists(env_path):
        logger.info(f"  ✓ .env file exists")
        return True
    elif os.path.exists(template_path):
        logger.warning(f"  ⚠ .env file not found, but template exists")
        logger.info(f"    → Copy: cp .env.template .env")
        logger.info(f"    → Then edit: .env")
        return False
    else:
        logger.warning(f"  ⚠ .env template not found")
        return False

# ==============================================================================
# INSTALLATION HELPER
# ==============================================================================
def install_requirements():
    """Help user install requirements"""
    logger.info("\n" + "="*80)
    logger.info("INSTALLING REQUIREMENTS")
    logger.info("="*80)
    
    req_files = [
        os.path.join(PROJECT_ROOT, "veronix_gui", "requirements.txt"),
        os.path.join(VERONIX_OS, "interface", "Requirements.txt"),
    ]
    
    logger.info("\nTo install all dependencies, run:")
    logger.info("")
    
    for req_file in req_files:
        if os.path.exists(req_file):
            logger.info(f"  pip install -r {req_file}")
    
    logger.info("")

# ==============================================================================
# MAIN VALIDATION
# ==============================================================================
def validate_setup():
    """Run all validation checks"""
    logger.info("="*80)
    logger.info("VERONIX PROJECT VALIDATION")
    logger.info("="*80)
    
    results = {
        "directories": check_directories(),
        "modules": check_python_modules(),
        "configs": check_config_files(),
        "env": check_env_file(),
        "ollama": check_ollama(),
    }
    
    # Summary
    logger.info("\n" + "="*80)
    logger.info("SUMMARY")
    logger.info("="*80)
    
    total_issues = sum(len(v) for v in results.values() if isinstance(v, list))
    
    if total_issues == 0 and all(results[k] for k in ["env", "ollama"]):
        logger.info("\n✅ All checks passed! VERONIX is ready to run.")
        return True
    else:
        logger.warning(f"\n⚠️  {total_issues} issue(s) found.")
        
        if results["modules"]:
            logger.info("\nTo fix missing modules, run:")
            install_requirements()
        
        if not results["ollama"]:
            logger.info("\nTo fix Ollama connection:")
            logger.info("  1. Install Ollama from: https://ollama.ai")
            logger.info("  2. Start Ollama: ollama serve")
            logger.info("  3. Run this script again")
        
        return False

# ==============================================================================
# IMPORT PATH SETUP
# ==============================================================================
def setup_import_paths():
    """Add VERONIX_OS to Python path for imports"""
    if VERONIX_OS not in sys.path:
        sys.path.insert(0, VERONIX_OS)
        logger.info(f"✓ Added {VERONIX_OS} to Python path")

# ==============================================================================
# MAIN
# ==============================================================================
if __name__ == "__main__":
    setup_import_paths()
    
    success = validate_setup()
    
    if success:
        sys.exit(0)
    else:
        logger.info("\n→ Fix the issues above and run this script again.")
        sys.exit(1)
