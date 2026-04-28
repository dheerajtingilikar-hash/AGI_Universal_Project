import os

# Path to your Knowledge Base
KB_FOLDER = r"D:\AGI_Universal_Project\Knowledge_Base"

def audit_knowledge_base():
    if not os.path.exists(KB_FOLDER):
        print(f"❌ Path not found: {KB_FOLDER}")
        return

    files = [f for f in os.listdir(KB_FOLDER) if f.endswith(".md")]
    missing_source = []
    total_files = len(files)

    print(f"🔍 [AUDIT] Scanning {total_files} files in Knowledge Base...\n")

    for filename in files:
        file_path = os.path.join(KB_FOLDER, filename)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                
                # Check for the 'source:' field in the YAML frontmatter
                if "source:" not in content.lower():
                    missing_source.append(filename)
        except Exception as e:
            print(f"⚠️ Error reading {filename}: {e}")

    # ==========================================
    # 📊 AUDIT RESULTS
    # ==========================================
    if missing_source:
        print(f"🚩 Found {len(missing_source)} files missing 'source' metadata:")
        for name in missing_source:
            print(f"   - {name}")
        
        print("\n💡 Tip: These were likely created by the middle version of the script.")
    else:
        print("✅ ALL CLEAR: Every file contains a 'source' field.")

if __name__ == "__main__":
    audit_knowledge_base()