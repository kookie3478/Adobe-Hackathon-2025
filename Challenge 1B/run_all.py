import os
import json
from app.processor import process_collection

def run_all_collections(base_path):
    for collection_name in os.listdir(base_path):
        collection_path = os.path.join(base_path, collection_name)
        if not os.path.isdir(collection_path):
            continue

        input_path = os.path.join(collection_path, "challenge1b_input.json")
        pdf_dir = os.path.join(collection_path, "PDFs")
        output_path = os.path.join(collection_path, "challenge1b_output.json")

        if not os.path.exists(input_path) or not os.path.exists(pdf_dir):
            continue

        with open(input_path, "r", encoding="utf-8") as f:
            input_data = json.load(f)

        result = process_collection(input_data, pdf_dir)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)

if __name__ == "__main__":
    run_all_collections("collections")
