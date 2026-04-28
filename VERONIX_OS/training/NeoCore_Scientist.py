import os
import sys
import re
from datetime import datetime
from groq import Groq

# ==========================================
# ⚙️ CONFIG & PATHS
# ==========================================
KB_FOLDER = r"D:\AGI_Universal_Project\Knowledge_Base"
os.makedirs(KB_FOLDER, exist_ok=True)

# 🔐 API KEY (SAFE)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    print("❌ Missing GROQ_API_KEY environment variable.")
    sys.exit(1)

client = Groq(api_key=GROQ_API_KEY)

# ==========================================
# 🧠 ROBUST CONTENT EXTRACTION
# ==========================================
def extract_content(response):
    try:
        choices = response.choices

        if not isinstance(choices, list) or len(choices) == 0:
            print("❌ No choices found.")
            return None

        first = choices[0]

        # Handle nested list case
        if isinstance(first, list):
            if len(first) == 0:
                print("❌ Empty nested list.")
                return None
            first = first[0]

        # Object-style
        if hasattr(first, "message"):
            return first.message.content

        # Dict-style
        if isinstance(first, dict):
            return first.get("message", {}).get("content", None)

        print("❌ Unknown response structure.")
        return None

    except Exception as e:
        print(f"❌ Extraction error: {e}")
        return None

# ==========================================
# 🔬 CORE FUNCTION
# ==========================================
def research_and_deploy(topic):
    if not topic or not topic.strip():
        print("⚠️ [SIGNAL ERROR] Empty topic.")
        return

    safe_name = re.sub(r'[^a-zA-Z0-9_ ]', '', topic).strip().replace(" ", "_")
    file_path = os.path.join(KB_FOLDER, f"{safe_name}.md")

    if os.path.exists(file_path):
        print(f"⏩ [SKIPPED] {topic} already exists.")
        return

    print(f"\n🔬 [DENSITY ARCHITECT] Mapping System: {topic}")

    prompt = f"""
Map the system '{topic}' with MAXIMUM DATA DENSITY.

Rules:
- Use Markdown tables
- Use [[WikiLinks]]
- No long prose
- Focus on structure, relationships, and components
"""

    try:
        # API CALL
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )

        # DEBUG (uncomment if needed)
        # print(response)
        # print(type(response.choices))

        content = extract_content(response)

        if not content:
            print("❌ Error: Content extraction failed.")
            return

        # DEPLOY FILE
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(
                f"---\n"
                f"topic: {topic}\n"
                f"date: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
                f"status: Deployed\n"
                f"---\n\n"
                f"{content}\n\n"
                f"---\n"
                f"*Entry synthesized for [[Veronix]] integration.*"
            )

        print(f"✅ [DEPLOYED] {file_path}")

    except Exception as e:
        print(f"❌ [CRITICAL ERROR]: {str(e)}")

# ==========================================
# 🚀 EXECUTION
# ==========================================
if __name__ == "__main__":
    if len(sys.argv) > 1:
        target_topic = " ".join(sys.argv[1:])
        research_and_deploy(target_topic)
    else:
        print("Usage: python NeoCore_Scientist.py <topic>")