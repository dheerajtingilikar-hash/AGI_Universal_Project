import os
import sys
import re
import time
from datetime import datetime
from groq import Groq

# ==========================================
# 🔐 LOAD ENV (OPTIONAL .env SUPPORT)
# ==========================================
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass 

# ==========================================
# ⚙️ CONFIG
# ==========================================
# Aligned with your Veronix Core V4.1 paths
KB_FOLDER = r"D:\AGI_Universal_Project\Knowledge_Base"
MODEL = "llama-3.1-8b-instant"

# ==========================================
# 🔐 API KEY (SAFE)
# ==========================================
# Ensure you set this in your environment or a .env file
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    # Adding a prompt for immediate use if env is not set
    GROQ_API_KEY = "YOUR_GROQ_API_KEY_HERE" 
    if GROQ_API_KEY == "YOUR_GROQ_API_KEY_HERE":
        raise ValueError("❌ GROQ_API_KEY not set. Add it to the script or environment variables.")

client = Groq(api_key=GROQ_API_KEY)

# Ensure Knowledge_Base exists
os.makedirs(KB_FOLDER, exist_ok=True)

# ==========================================
# 🧠 MATTER-DENSITY ARCHITECT ENGINE
# ==========================================
class NeoCoreScientist:
    def research_and_deploy(self, topic):
        if not topic or not topic.strip():
            print("⚠️ [SIGNAL ERROR] Empty research topic provided.")
            return

        # --------------------------------------
        # 🧹 SAFE FILE NAME (Obsidian-Friendly)
        # --------------------------------------
        safe_name = re.sub(r'[^a-zA-Z0-9_ ]', '', topic).strip().replace(" ", "_")
        if not safe_name:
            safe_name = f"research_{int(time.time())}"

        file_path = os.path.join(KB_FOLDER, f"{safe_name}.md")

        if os.path.exists(file_path):
            print(f"⏩ [SKIPPED] {topic} already exists in Knowledge_Base.")
            return

        print(f"\n🔬 [DENSITY ARCHITECT] Mapping System: {topic}")

        # --------------------------------------
        # 🧠 THE MATTER-DENSITY PROMPT
        # --------------------------------------
        # Refined for maximum AGI ingestion and WikiLink cross-referencing
        prompt = f"""
You are the NeoCore Causal Architect. 

Map the following system with MAXIMUM DATA DENSITY and technical substance.

RULES:
- Title: # {topic}
- ## 1. Objective Function: What is the system optimizing for?
- ## 2. Core Constants & Formulas: List the specific mathematical or physical values defining this. Use LaTeX for complex math.
- ## 3. Material/Technical Properties: Provide specific hard data (e.g., density, bit-depth, voltage, specific heat).
- ## 4. Causal Structure: Primary [[Cause]] -> [[Effect]] chains.
- ## 5. Feedback Loops: [[Positive Feedback]] (Growth) and [[Negative Feedback]] (Stability) mechanisms.
- ## 6. Failure Modes: What causes the system to collapse or [[Entropy]] to take over?
- Use [[WikiLinks]] for all major technical concepts and cross-scale unification.
- FORMAT: Use Markdown Tables for data comparisons.
- No prose. No conversational filler. Maximum information density for AGI ingestion.

TOPIC: {topic}
"""

        content = None

        # ==========================================
        # 🔁 RETRY LOGIC (Groq API Handling)
        # ==========================================
        for attempt in range(3):
            try:
                response = client.chat.completions.create(
                    model=MODEL,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.1, # Decreased for even higher factual consistency
                    max_tokens=2048
                )

                if hasattr(response.choices.message, 'content'):
                    content = response.choices.message.content
                else:
                    content = str(response)

                if content:
                    break

            except Exception as e:
                print(f"❌ Attempt {attempt+1} failed: {e}")
                time.sleep(2)

        if not content:
            print("❌ Critical Failure: Failed to generate content after retries.")
            return

        # ==========================================
        # 📝 DEPLOYMENT (Write to Knowledge_Base)
        # ==========================================
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                # Obsidian-compatible Frontmatter
                f.write(
                    f"---\n"
                    f"topic: {topic}\n"
                    f"date: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
                    f"type: Sovereign_Research_Entry\n"
                    f"engine: NeoCore_Groq_Llama3.1\n"
                    f"status: Deployed\n"
                    f"---\n\n"
                    f"{content}\n\n"
                    f"--- \n"
                    f"*Entry synthesized by NeoCore Scientist for [[Veronix]] integration.*"
                )

            print(f"✅ [DEPLOYED] {file_path}")

        except Exception as e:
            print(f"❌ Deployment error: {file_path} - {e}")

# ==========================================
# 🚀 ENTRY POINT
# ==========================================
if __name__ == "__main__":
    scientist = NeoCoreScientist()

    if len(sys.argv) > 1:
        # Allows for multi-word topics: python script.py Quantum Computing
        topic = " ".join(sys.argv[1:])
        scientist.research_and_deploy(topic)
    else:
        print("Usage: python NeoCore_Scientist.py <topic>")
        # Example for quick testing:
        # scientist.research_and_deploy("Graphene Superconductors")