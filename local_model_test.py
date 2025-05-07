import os
import torch
from dotenv import load_dotenv
from transformers import AutoTokenizer, AutoModelForCausalLM

# Load token from .env
load_dotenv()
#token = os.getenv("HF_TOKEN")

# Model (TinyLLaMA or any gated/private repo)
model_id = "microsoft/phi-2" # or any model you prefer

# Download with auth token
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id)

device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
model = model.to(device)
model.eval()

# Prompt
prompt = "Convert to Pandas filter: Invoices over 500 from vendor Hayes"
inputs = tokenizer(prompt, return_tensors="pt").to(device)

with torch.no_grad():
    outputs = model.generate(**inputs, max_new_tokens=100)
    print(tokenizer.decode(outputs[0], skip_special_tokens=True))
