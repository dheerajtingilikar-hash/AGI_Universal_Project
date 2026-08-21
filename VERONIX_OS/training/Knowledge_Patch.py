import os; import re; KB = r"D:\AGI_Universal_Project\Knowledge_Base"; patched = 0;
for fn in os.listdir(KB):
    if not fn.endswith(".md"): continue
    path = os.path.join(KB, fn)
    with open(path, "r", encoding="utf-8") as f: content = f.read()
    if "source:" not in content.lower():
        # Insert source before the closing --- of the frontmatter
        new_content = re.sub(r"(---\s*)\n---", r"\1source: NeoCore Groq Engine\n---", content, count=1)
        if new_content == content: # Fallback if first regex fails
            new_content = content.replace("---\n\n", "source: NeoCore Groq Engine\n---\n\n", 1)
        with open(path, "w", encoding="utf-8") as f: f.write(new_content)
        patched += 1
print(f"✅ Successfully patched {patched} files.")