from unsloth import FastLanguageModel
import torch
import ollama  # <--- New Import for DeepSeek Auditor
from Veronix_Auditor import audit_decision # <--- Import your new Auditor script

# ... (Keep your 1. CONFIGURATION and 2. GENERATION FUNCTION as is) ...

# =========================
# 3. INTENT DETECTION (Updated)
# =========================
def detect_intent(query):
    q = query.lower()

    return {
        "needs_code": any(w in q for w in ["code", "program", "script", "python"]),
        "needs_explanation": any(w in q for w in ["explain", "why", "how"]),
        "is_decision": any(w in q for w in [
            "hire", "reject", "loan", "approve", "choose", "judge", "decide"
        ]), # <--- New Intent for Hackathon
    }

# =========================
# 4. TASK BUILDER (Updated)
# =========================
def build_tasks(user_query, intent):
    tasks = []

    if intent["is_decision"]:
        tasks.append(("decision", user_query)) # <--- Route to Auditor

    elif intent["needs_code"]:
        tasks.append(("code", user_query))

    elif intent["needs_explanation"]:
        tasks.append(("explain", user_query))

    if not tasks:
        tasks.append(("general", user_query))

    return tasks

# =========================
# 5. ROUTER (Updated)
# =========================
def route_task(task_type, query):

    # ---------- UNBIASED DECISION (HACKATHON MODE) ----------
    if task_type == "decision":
        print("⚖️ [VERONIX AUDITOR MODE]")
        
        # 1. First, get a raw decision from your 1B Base Model
        model.disable_adapters()
        raw_prompt = f"Act as a professional judge. Make a decision on: {query}"
        raw_decision = generate(raw_prompt)

        # 2. Call the DeepSeek-R1 Auditor to check for bias
        # This uses the script you created in the Scripts folder
        print("🔍 Auditing for hidden biases...")
        audit_report = audit_decision(raw_decision, query)

        return f"RAW DECISION: {raw_decision}\n\nVERONIX AUDIT REPORT:\n{audit_report}"

    # ---------- (Keep CODE/EXPLAIN/GENERAL sections the same) ----------
    # ...