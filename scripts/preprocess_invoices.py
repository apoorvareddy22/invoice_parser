import os
import pytesseract
from PIL import Image
import json
from tqdm import tqdm

INPUT_DIR = "data/images"
OUTPUT_DIR = "data/json"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def ocr_layoutlm_format(image_path):
    image = Image.open(image_path).convert("RGB")
    width, height = image.size

    # Run OCR
    ocr_data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)

    words = []
    for i in range(len(ocr_data['text'])):
        text = ocr_data['text'][i].strip()
        if text == "":
            continue

        word_info = {
            "text": text,
            "bbox": [
                int(ocr_data['left'][i]),
                int(ocr_data['top'][i]),
                int(ocr_data['left'][i] + ocr_data['width'][i]),
                int(ocr_data['top'][i] + ocr_data['height'][i])
            ],
            "confidence": float(ocr_data['conf'][i]),
            "page": 0
        }
        words.append(word_info)

    return {
        "id": os.path.basename(image_path),
        "words": words,
        "width": width,
        "height": height
    }

# Run preprocessing
for filename in tqdm(os.listdir(INPUT_DIR)):
    if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        continue

    image_path = os.path.join(INPUT_DIR, filename)
    result = ocr_layoutlm_format(image_path)

    with open(os.path.join(OUTPUT_DIR, filename.replace(".png", ".json")), "w") as f:
        json.dump(result, f, indent=2)
