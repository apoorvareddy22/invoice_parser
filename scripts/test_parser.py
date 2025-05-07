import os
from app.layoutlm_parser.parser import parse_invoice

image_dir = "data/images"

for filename in os.listdir(image_dir):
    if filename.lower().endswith((".png", ".jpg", ".jpeg")):
        print(f"\n🧾 Parsing {filename}")
        results = parse_invoice(os.path.join(image_dir, filename))
        print(results[:20])  # show first 20 token-label pairs
