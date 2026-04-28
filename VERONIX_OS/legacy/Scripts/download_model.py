from huggingface_hub import snapshot_download
import os

def download_base_model():
    model_id = "unsloth/Llama-3.2-1B-bnb-4bit"
    save_path = "D:/AGI_Universal_Project/Models/Llama-3.2-1B-4bit"
    
    print(f"📡 Preparing to download base model to {save_path}...")
    
    snapshot_download(
        repo_id=model_id,
        local_dir=save_path,
        local_dir_use_symlinks=False
    )
    print("✅ Base model is now stored on D: Drive.")

if __name__ == "__main__":
    # We are calling the function now because Torch is 100% ready!
    download_base_model()