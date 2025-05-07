from transformers import pipeline
import torch

# Detect device
if torch.cuda.is_available():
    device = 0  # CUDA
    print("✅ Using GPU (CUDA) for inference")
elif torch.backends.mps.is_available():
    device = "mps"  # Apple Silicon
    print("✅ Using GPU (MPS - Apple Silicon) for inference")
else:
    device = -1  # CPU
    print("⚡ Using CPU for inference")

# Initialize pipeline
doc_qa_pipeline = pipeline(
    "document-question-answering",
    model="impira/layoutlm-invoices",
    tokenizer="impira/layoutlm-invoices",
    device=device if device != "mps" else -1  # fallback to CPU if MPS
)

def ask_question(image, question: str):
    """
    Function to ask a question from the document using the pipeline.
    """
    result = doc_qa_pipeline(image, question)
    return result
