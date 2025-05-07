import os
import json
from tqdm import tqdm
from app.services.preprocess import preprocess_image
from app.services.ocr_model import ask_question
from app.services.extraction_logic import FIELDS, generate_question
from app.db.crud import insert_invoice
from concurrent.futures import ThreadPoolExecutor, as_completed

# Paths
IMAGE_FOLDER = "data/images"
ANNOTATION_FOLDER = "data/json"
OUTPUT_FILE = "data/output.json"

def parse_invoice(image_path):
    """Preprocess and extract fields from an invoice image."""
    with open(image_path, "rb") as f:
        image_bytes = f.read()

    image = preprocess_image(image_bytes)

    extracted_data = {}
    for field in FIELDS:
        question = generate_question(field)
        answer = ask_question(image, question)
        extracted_data[field] = answer[0]["answer"] if answer else None

    return extracted_data

def process_invoice(filename):
    """Wrapper function to handle one invoice processing."""
    try:
        if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            return None

        image_path = os.path.join(IMAGE_FOLDER, filename)
        json_name = os.path.splitext(filename)[0] + ".json"
        json_path = os.path.join(ANNOTATION_FOLDER, json_name)

        parsed_data = parse_invoice(image_path)

        insert_invoice(filename, parsed_data)

        ground_truth = None
        if os.path.exists(json_path):
            with open(json_path, "r") as f:
                ground_truth = json.load(f)

        return filename, {
            "parsed": parsed_data,
            "ground_truth": ground_truth
        }

    except Exception as e:
        print(f"❌ Error processing {filename}: {e}")
        return None

def main():
    all_results = {}

    filenames = [
        f for f in os.listdir(IMAGE_FOLDER)
        if f.lower().endswith(('.png', '.jpg', '.jpeg'))
    ]

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(process_invoice, filename): filename for filename in filenames}

        for future in tqdm(as_completed(futures), total=len(futures), desc="Processing invoices"):
            result = future.result()
            if result:
                filename, data = result
                all_results[filename] = data

    with open(OUTPUT_FILE, "w") as f:
        json.dump(all_results, f, indent=4)

    print(f"\n✅ Parsing complete! Results saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
