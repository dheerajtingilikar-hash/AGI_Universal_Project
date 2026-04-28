import os

# --- CONFIGURATION ---
KB_PATH = r'D:\AGI_Universal_Project\Knowledge_Base'

# --- MASTER TECH STACK DATA ---
# You can edit the descriptions below to add even deeper "Mastery" notes
tech_mastery = {
    "Staff_Tech_Stack.md": """# Master Tech Stack: Sovereign Capabilities
## Languages & Foundations
- **Python**: Core engine for AGI (Veronix), SDR automation, and Data Science.
- **Java**: Multithreaded systems and legacy integration.
- **JavaScript/HTML5**: Frontend interfaces and real-time dashboards.

## AI & Data Science (The Intelligence Core)
- **PyTorch**: Deep learning model architecture and training.
- **Scikit-Learn**: Predictive modeling and classical ML.
- **Pandas/NumPy/SciPy**: High-performance data manipulation and signal processing.

## Web & Frontend (The Interface Layer)
- **React/Vite/Vue.js**: Modern, reactive UI components for UniFlow and Veronix Web.
- **Node.js**: Scalable backend services and API orchestration.

## Cloud & DevOps (The Infrastructure Layer)
- **AWS/Google Cloud**: Distributed computing and sovereign cloud hosting.
- **Render**: Rapid deployment for web services.
- **GitHub/Selenium**: Version control and automated browser testing.

## Databases (The Memory Layer)
- **MongoDB**: NoSQL document storage for unstructured brain data.
- **MySQL**: Relational database for structured student data (UniFlow).

## Creative Suite (The Aesthetic Layer)
- **After Effects/Photoshop/Canva**: Visual identity, UI design, and branding.

[[00_OMNI_BRAIN]] | [[Pillar_Software_Eng]] | [[Pillar_AI_ML]]""",

    "Staff_Workflow_Integration.md": """# Workflow Integration: Cross-Domain Strategy
- **SDR + Selenium**: Automating the capture of web-based radio nodes for the SDR terminal.
- **PyTorch + Obsidian**: Using RAG (Retrieval Augmented Generation) to feed the knowledge base into neural models.
- **React + MySQL**: Building the real-time front-end for the UniFlow Student Management System.

[[Staff_Tech_Stack]] | [[Pillar_DevOps]]"""
}

# --- EXECUTION ---
def deploy_staff():
    if not os.path.exists(KB_PATH):
        os.makedirs(KB_PATH)
        print(f"[INFO] Created directory: {KB_PATH}")

    for filename, content in tech_mastery.items():
        file_path = os.path.join(KB_PATH, filename)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"[DEPLOYED] {filename}")

    print("\n[SUCCESS] Tech Stack Mastery has been injected into the Knowledge Base.")
    print("[ACTION] Open Obsidian to see the new 'Staff' nodes connecting to your Pillars.")

if __name__ == "__main__":
    deploy_staff()