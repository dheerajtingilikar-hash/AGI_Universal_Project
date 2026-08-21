from unsloth import FastLanguageModel
import torch

# 1. Load the model
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="D:/AGI_Universal_Project/Experts/python_logic",
    max_seq_length=2048,
    load_in_4bit=True,
)
FastLanguageModel.for_inference(model)

# 2. Prompt template
alpaca_prompt = """Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

### Instruction:
{}

### Input:
{}

### Response:
{}"""

# 3. Test input
instruction = "Write a Python script to check if a number is prime."
input_text = ""

inputs = tokenizer(
    [alpaca_prompt.format(instruction, input_text, "")],
    return_tensors="pt"
).to("cuda")

# 4. Generate
print("\n🚀 Logic Expert is thinking...\n" + "-"*30)

outputs = model.generate(
    **inputs,
    max_new_tokens=128,
    use_cache=True,
)

# 🔥 FIX: decode properly
response = tokenizer.batch_decode(outputs, skip_special_tokens=True)
full_text = response[0]   # ✅ extract string

# 5. Clean output
if "### Response:" in full_text:
    final_output = full_text.split("### Response:")[-1].strip()
else:
    final_output = full_text.strip()

print(final_output)