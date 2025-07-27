import fitz  # PyMuPDF
import os
import json
import re
from pathlib import Path
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer


# Set paths
input_dir = Path("sample-datasets/pdfs")
output_dir = Path("sample-datasets/outputs")
output_dir.mkdir(parents=True, exist_ok=True)

# Font size thresholds (heuristic)
H1_THRESHOLD = 16
H2_THRESHOLD = 13
H3_THRESHOLD = 11
MIN_HEADER_LEN = 4
MAX_HEADER_LEN = 100

def clean_text(text):
    # Remove duplicated characters (e.g., RRRR -> R)
    return re.sub(r'(.)\1{2,}', r'\1', text).strip()

def classify_font_size(size):
    if size >= H1_THRESHOLD:
        return "H1"
    elif size >= H2_THRESHOLD:
        return "H2"
    elif size >= H3_THRESHOLD:
        return "H3"
    else:
        return None


def extract_title_from_fitz(pdf_path):
    doc = fitz.open(pdf_path)
    page = doc[0]

    blocks = page.get_text("dict")["blocks"]

    # Filter text blocks with largest font size
    text_blocks = []
    for b in blocks:
        for line in b.get("lines", []):
            for span in line["spans"]:
                text_blocks.append({
                    "text": span["text"].strip(),
                    "size": span["size"],
                    "bbox": span["bbox"]
                })

    if not text_blocks:
        return ""

    # Find largest font size
    max_size = max(b["size"] for b in text_blocks)
    top_lines = [b["text"] for b in text_blocks if abs(b["size"] - max_size) < 0.5]
    deduped = list(dict.fromkeys(top_lines))  # preserve order, remove duplicates

    title = " ".join(deduped)
    return title.strip()

def process_pdf(file_path):
    all_headers = []

    for page_num, layout in enumerate(extract_pages(file_path), start=1):
        for element in layout:
            if isinstance(element, LTTextContainer):
                for text_line in element:
                    line_text = text_line.get_text().strip()
                    if not line_text:
                        continue

                    sizes = [char.size for char in text_line if hasattr(char, "size")]
                    if not sizes:
                        continue

                    avg_size = sum(sizes) / len(sizes)
                    level = classify_font_size(avg_size)

                    clean_line = clean_text(line_text)

                    if level and MIN_HEADER_LEN <= len(clean_line) <= MAX_HEADER_LEN:
                        all_headers.append({
                            "level": level,
                            "text": clean_line,
                            "page": page_num
                        })

    title = extract_title_from_fitz(file_path)
    return {
        "title": title,
        "outline": all_headers
    }


def process_all_pdfs():
    pdf_files = list(input_dir.glob("*.pdf"))
    for pdf_file in pdf_files:
        result = process_pdf(pdf_file)
        output_path = output_dir / (pdf_file.stem + ".json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"✔ Processed {pdf_file.name} -> {output_path.name}")

if __name__ == "__main__":
    print("Processing PDFs...")
    process_all_pdfs()
    print("Completed.")
