import os

# Project Paths on your 120GB+ D: Drive
PROJECT_ROOT = "D:/AGI_Universal_Project"
MODEL_DIR = os.path.join(PROJECT_ROOT, "Models")
EXPERT_DIR = os.path.join(PROJECT_ROOT, "Experts")
DATASET_DIR = os.path.join(PROJECT_ROOT, "Datasets")

# Hardware Limits for your RTX 3050 (4.29 GB)
MAX_VRAM_GB = 4.0 
TARGET_MODEL = "unsloth/Llama-3.2-1B-bnb-4bit"

print(f"✅ Configuration Loaded. Using {PROJECT_ROOT} for storage.")