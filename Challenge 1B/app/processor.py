import os
import fitz
from datetime import datetime
from app.model_utils import rank_sections
from app.config import model_name
from sentence_transformers import SentenceTransformer

model = SentenceTransformer(model_name)

def extract_sections(pdf_path):
    doc = fitz.open(pdf_path)
    sections = []
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
                sections.append({
                    "text": text.strip(),
                    "page": i + 1,
                    "section_title": text.strip().split(".")[0][:80],
                    "font_size": max_font_size
                })
    return sections

def process_collection(input_data, pdf_dir):
    persona = input_data["persona"]["role"]
    task = input_data["job_to_be_done"]["task"]
    documents = input_data["documents"]

    all_sections = []
    for doc in documents:
        filename = doc["filename"]
        path = os.path.join(pdf_dir, filename)
        if not os.path.exists(path):
            continue
        sections = extract_sections(path)
        for s in sections:
            s["document"] = filename
        all_sections.extend(sections)

    ranked = rank_sections(all_sections, persona, task)

    output = {
        "metadata": {
            "input_documents": [doc["filename"] for doc in documents],
            "persona": persona,
            "job_to_be_done": task,
            "timestamp": datetime.now().isoformat()
        },
        "extracted_sections": ranked["sections"],
        "subsection_analysis": ranked["subsections"]
    }

    return output
