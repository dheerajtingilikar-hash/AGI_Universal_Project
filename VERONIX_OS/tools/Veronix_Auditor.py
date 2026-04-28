import ollama
import re

def audit_decision(initial_decision, candidate_data):
    # This is the "Apex Auditor" prompt for Veronix
    prompt = f"""
    SYSTEM: You are the VERONIX UNBIASED AUDITOR.
    TASK: Analyze the following decision for hidden biases (race, gender, location, prestige).
    
    INITIAL DECISION: {initial_decision}
    INPUT DATA: {candidate_data}
    
    INSTRUCTIONS:
    1. Identify if any "Proxy Variables" (like ZIP codes or names) influenced the decision.
    2. If bias is found, trigger REGENESIS and suggest a fair alternative.
    3. If no bias is found, VALIDATE the decision.
    
    Provide your reasoning clearly.
    """
    
    try:
        # Changed to 1.5b to fit in your 5.78GB Free RAM alongside Llama 3.2
        response = ollama.generate(model='deepseek-r1:1.5b', prompt=prompt)
        full_response = response['response']
        
        # Clean up the response for F.R.I.D.A.Y.'s TTS
        # This removes the <think> blocks so she only speaks the conclusion
        clean_response = re.sub(r'<think>.*?</think>', '', full_response, flags=re.DOTALL).strip()
        
        return clean_response
    
    except Exception as e:
        return f"Auditor Error: {e}"

# --- Hackathon Test Case ---
if __name__ == "__main__":
    test_decision = "Reject Candidate A because their background doesn't feel like a 'culture fit'."
    test_data = "{'name': 'John Doe', 'location': 'Low-income neighborhood', 'skills': 'Python, SQL, 5 years experience'}"

    print("⚖️  [VERONIX AUDIT START]")
    print(audit_decision(test_decision, test_data))