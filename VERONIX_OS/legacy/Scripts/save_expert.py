import os
import json

def register_expert(subject_name, model_path):
    manifest_path = "D:/AGI_Universal_Project/manifest.json"
    
    # Create manifest if it doesn't exist
    if not os.path.exists(manifest_path):
        with open(manifest_path, "w") as f:
            json.dump({"total_experts": 0, "learned_subjects": []}, f)

    with open(manifest_path, "r") as f:
        data = json.load(f)
    
    if subject_name not in data["learned_subjects"]:
        data["learned_subjects"].append(subject_name)
        data["total_experts"] += 1
        
    with open(manifest_path, "w") as f:
        json.dump(data, f, indent=4)
        
    print(f"✅ Expertise in '{subject_name}' archived to D: Drive.")

if __name__ == "__main__":
    print("This script runs automatically after training.")