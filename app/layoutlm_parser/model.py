from transformers import LayoutLMv2Processor, LayoutLMv2ForTokenClassification
import torch

MODEL_NAME = "microsoft/layoutlmv2-base-uncased"

device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")

processor = LayoutLMv2Processor.from_pretrained(MODEL_NAME)
model = LayoutLMv2ForTokenClassification.from_pretrained(MODEL_NAME).to(device)
