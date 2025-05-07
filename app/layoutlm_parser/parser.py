from PIL import Image
import torch
from app.layoutlm_parser.model import processor, model, device

def parse_invoice(image_path):
    image = Image.open(image_path).convert("RGB")

    encoding = processor(image, return_tensors="pt", truncation=True, padding="max_length")
    for k in encoding:
        encoding[k] = encoding[k].to(device)

    outputs = model(**encoding)
    logits = outputs.logits
    predictions = torch.argmax(logits, dim=2)

    tokens = processor.tokenizer.convert_ids_to_tokens(encoding["input_ids"][0])
    labels = predictions[0].tolist()

    results = []
    for token, label in zip(tokens, labels):
        results.append((token, label))

    return results

def group_entities(tokens_with_labels):
    """
    Convert BIO-tagged tokens into structured key-value entities.
    """
    entities = {}
    current_label = None
    current_value = []

    for token, label_id in tokens_with_labels:
        label = model.config.id2label[label_id]
        if label == "O":
            if current_label and current_value:
                entities.setdefault(current_label, []).append(" ".join(current_value))
                current_value = []
            current_label = None
        elif label.startswith("B-"):
            if current_label and current_value:
                entities.setdefault(current_label, []).append(" ".join(current_value))
            current_label = label[2:]
            current_value = [token]
        elif label.startswith("I-") and current_label == label[2:]:
            current_value.append(token)

    if current_label and current_value:
        entities.setdefault(current_label, []).append(" ".join(current_value))

    return {k: " ".join(v) for k, v in entities.items()}
