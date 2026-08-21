import unsloth 
from unsloth import FastLanguageModel
import torch
from trl import SFTTrainer, SFTConfig
from datasets import load_dataset

# 1. Load Model & Tokenizer
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "D:/AGI_Universal_Project/Models/Llama-3.2-1B-4bit",
    max_seq_length = 2048,
    load_in_4bit = True,
)

# 2. Add LoRA Adapters
model = FastLanguageModel.get_peft_model(
    model,
    r = 16, 
    target_modules = ["q_proj", "k_proj", "v_proj", "o_proj"],
    lora_alpha = 16,
    lora_dropout = 0, 
    bias = "none",    
    use_gradient_checkpointing = "unsloth",
    random_state = 3407,
)

# 3. Load & Pre-Tokenize (UPDATED TO 500 SAMPLE DATASET)
dataset = load_dataset(
    "json", 
    data_files = "D:/AGI_Universal_Project/Datasets/python_logic_500.jsonl", 
    split = "train"
)

alpaca_prompt = """Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

### Instruction:
{}

### Input:
{}

### Response:
{}"""

def tokenize_function(examples):
    instructions = examples["instruction"]
    inputs       = examples["input"]
    outputs      = examples["output"]
    texts = [alpaca_prompt.format(inst, inp, out) + tokenizer.eos_token for inst, inp, out in zip(instructions, inputs, outputs)]
    return tokenizer(texts, truncation=True, max_length=2048)

# Convert to numbers and remove original text to prevent dimension errors
tokenized_dataset = dataset.map(tokenize_function, batched=True)
tokenized_dataset = tokenized_dataset.remove_columns(["instruction", "input", "output"])

# 4. Trainer (UPDATED STEPS AND LEARNING RATE)
trainer = SFTTrainer(
    model = model,
    tokenizer = tokenizer,
    train_dataset = tokenized_dataset,
    args = SFTConfig(
        max_seq_length = 2048,
        per_device_train_batch_size = 2,
        gradient_accumulation_steps = 4,
        max_steps = 120,               # Increased for 500 samples
        learning_rate = 1e-4,          # Lowered for better stability
        fp16 = not torch.cuda.is_bf16_supported(),
        bf16 = torch.cuda.is_bf16_supported(),
        logging_steps = 1,
        optim = "adamw_8bit",
        seed = 3407,
        output_dir = "outputs",
        report_to = "none",
        remove_unused_columns = False,
        dataset_kwargs = {
            "skip_prepare_dataset": True,
        },
    ),
)

# 5. Launch
print("🚀 Launching Logic Expert Training on 500 samples...")
trainer.train()

# 6. Save
model.save_pretrained("D:/AGI_Universal_Project/Experts/python_logic")
tokenizer.save_pretrained("D:/AGI_Universal_Project/Experts/python_logic")
print("✅ Training complete. Expert updated with high-quality logic.")