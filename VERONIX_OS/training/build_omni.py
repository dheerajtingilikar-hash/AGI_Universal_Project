import os
import datetime

VAULT_PATH = r"D:\AGI_Universal_Project\Knowledge_Base"

def create_note(filepath, content):
    if os.path.exists(filepath):
        print(f"[SKIPPED] {os.path.basename(filepath)}")
        return
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[CREATED] {os.path.basename(filepath)}")


def build_omni_brain():
    os.makedirs(VAULT_PATH, exist_ok=True)
    today = datetime.datetime.now().strftime("%Y-%m-%d")

    print("\n--- BUILDING UNIVERSAL OMNI-BRAIN ---\n")

    domains = {
        "Pillar_Math_Logic.md": {
            "tag": "math",
            "content": """
Pure math · Applied math · Statistics · Probability  
Linear algebra · Calculus · Discrete math · Game theory  
Formal proofs · Number theory · Topology · Cryptography
"""
        },

        "Pillar_Physical_Sciences.md": {
            "tag": "science",
            "content": """
Physics (classical, quantum, relativity, thermodynamics)  
Chemistry (organic, inorganic, physical, biochem)  
Biology (molecular, cellular, evolutionary)  
Astronomy · Earth science · Environmental science
"""
        },

        "Pillar_Engineering.md": {
            "tag": "engineering",
            "content": """
Mechanical · Electrical · Civil · Aerospace  
Control systems · Signal processing  
Embedded systems · Robotics · Hardware design
"""
        },

        "Pillar_CS_Software.md": {
            "tag": "cs",
            "content": """
Languages: Python, C, C++, Rust, Go, Java, JS, SQL  
Algorithms · Data structures · System design  
Web · Mobile · DevOps · Cloud · APIs  
Databases · Networking · Security  
OS internals · Compilers
"""
        },

        "Pillar_AI_ML.md": {
            "tag": "ai",
            "content": """
Machine learning · Deep learning · NLP · Vision  
Reinforcement learning · LLMs · Generative AI  
MLOps · AI safety · Prompt engineering · RAG
"""
        },

        "Pillar_Medicine.md": {
            "tag": "health",
            "content": """
Anatomy · Physiology · Pathology · Pharmacology  
Clinical medicine · Diagnostics  
Nutrition · Mental health · Public health
"""
        },

        "Pillar_Business.md": {
            "tag": "business",
            "content": """
Strategy · Market analysis · Operations  
Product management · Growth · Startups  
Marketing · Sales · Scaling
"""
        },

        "Pillar_Finance.md": {
            "tag": "finance",
            "content": """
Valuation · Financial modeling · Accounting  
Investing · Portfolio theory · Risk  
Crypto · Derivatives · Macro economics
"""
        },

        "Pillar_Law.md": {
            "tag": "law",
            "content": """
Contract law · Corporate law · IP  
Policy · Governance · Compliance
"""
        },

        "Pillar_Creative.md": {
            "tag": "creative",
            "content": """
Writing · Copywriting · Storytelling  
Poetry · Scripts · Communication  
Translation · Editing
"""
        },

        "Pillar_Design.md": {
            "tag": "design",
            "content": """
UX/UI · Typography · Color theory  
Branding · Layout · Visualization
"""
        },

        "Pillar_Psychology.md": {
            "tag": "psychology",
            "content": """
Cognition · Behavior · Neuroscience  
Decision making · Emotional intelligence  
Therapy · Relationships
"""
        },

        "Pillar_Philosophy.md": {
            "tag": "philosophy",
            "content": """
Epistemology · Metaphysics · Ethics  
Philosophy of mind · Political philosophy
"""
        },

        "Pillar_History.md": {
            "tag": "history",
            "content": """
World history · Society · Culture  
Anthropology · Religion · Linguistics
"""
        },

        "Pillar_Life_Mastery.md": {
            "tag": "life",
            "content": """
Productivity · Habits · Decision making  
Leadership · Communication  
Health · Performance optimization
"""
        }
    }

    # CREATE DOMAIN FILES
    for filename, data in domains.items():
        content = f"""---
type: knowledge-domain
created: {today}
tag: {data['tag']}
---

# {filename.replace('.md','').replace('_',' ')}

## Scope
{data['content']}

## Linked Systems
- [[Veronix_Core]]
- [[UniFlow_Project]]

"""
        create_note(os.path.join(VAULT_PATH, filename), content)

    # MASTER INDEX
    master = f"""---
type: master-index
created: {today}
---

# 🧠 UNIVERSAL OMNI-BRAIN

## Core Knowledge Domains

- [[Pillar_Math_Logic]]
- [[Pillar_Physical_Sciences]]
- [[Pillar_Engineering]]
- [[Pillar_CS_Software]]
- [[Pillar_AI_ML]]
- [[Pillar_Medicine]]
- [[Pillar_Business]]
- [[Pillar_Finance]]
- [[Pillar_Law]]
- [[Pillar_Creative]]
- [[Pillar_Design]]
- [[Pillar_Psychology]]
- [[Pillar_Philosophy]]
- [[Pillar_History]]
- [[Pillar_Life_Mastery]]

---

## Core Systems
- [[Veronix_Core]]
- [[UniFlow_Project]]

---

## Purpose
Complete structured representation of human knowledge.
"""

    create_note(os.path.join(VAULT_PATH, "00_OMNI_BRAIN.md"), master)

    print("\n[COMPLETE] UNIVERSAL KNOWLEDGE SYSTEM READY.")
    print("[NEXT] Open Obsidian → Graph View → See full brain map.")


if __name__ == "__main__":
    build_omni_brain()