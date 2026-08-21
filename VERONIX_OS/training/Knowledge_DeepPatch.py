import os

KB_FOLDER = r"D:\AGI_Universal_Project\Knowledge_Base"
targets = ["Internal Energy.md", "Master_Atlas.md", "Pillar_AI_ML.md", "Pillar_Business.md", "Pillar_Cloud.md", "Pillar_Cybersecurity.md", "Pillar_Data_Science.md", "Pillar_Law_Ethics.md", "Pillar_Philosophy.md", "Pillar_Psychology.md", "Pillar_Software_Eng.md", "Quantum mechanics.md", "SDR_Terminal.md", "Staff_Mastery_Deep_Dive.md", "Staff_Tech_Stack.md", "Tactical_Brief_2026-04-20_19-45-08.md", "Tactical_Brief_2026-04-20_20-25-33.md", "Tactical_Brief_2026-04-20_20-57-17.md", "Tactical_Brief_2026-04-20_21-35-39.md", "Tactical_Brief_2026-04-20_22-38-39.md", "UniFlow_Project.md", "Veronix_Core.md"]

patched = 0

for filename in targets:
    path = os.path.join(KB_FOLDER, filename)
    if not os.path.exists(path):
        continue

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # If it already has a source, skip it
    if "source:" in content.lower():
        continue

    # If it has a YAML header, inject the source before the closing '---'
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            # parts is the inside of the YAML block
            new_yaml = parts.rstrip() + "\nsource: NeoCore Groq Engine\n"
            new_content = f"---{new_yaml}---{parts}"
        else:
            new_content = f"---\ntopic: {filename}\nsource: NeoCore Groq Engine\n---\n\n" + content
    else:
        # No header? Create one.
        new_content = f"---\ntopic: {filename}\nsource: NeoCore Groq Engine\n---\n\n" + content

    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
    patched += 1

print(f"✅ Fixed {patched} files. Knowledge Base is now standardized.")