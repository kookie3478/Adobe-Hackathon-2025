import fitz  # PyMuPDF

def extract_sections(pdf_path):
    doc = fitz.open(pdf_path)
    results = []

    for i, page in enumerate(doc):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" not in block:
                continue

            text = ""
            max_font_size = 0

            for line in block["lines"]:
                for span in line["spans"]:
                    text += span["text"] + " "
                    max_font_size = max(max_font_size, span["size"])

            if text.strip():
                results.append({
                    "text": text.strip(),
                    "page": i + 1,
                    "section_title": text.strip().split(".")[0][:80],
                    "font_size": max_font_size
                })

    return results