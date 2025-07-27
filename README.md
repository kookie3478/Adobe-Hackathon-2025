### ROUND 1A: PDF HEADING STRUCTURE EXTRACTION

# Goal 

Build a system that extracts a structured outline from a PDF using visual and layout-based clues to identify:
The document title
H1, H2, H3 headings (and optionally H4)
Page number and text of each heading
The system should run completely offline using a lightweight Python-based setup.

# Input

A folder of PDF documents
Each document may vary in formatting, font styles, and heading hierarchy
No consistent markup — headings must be inferred from font size or layout structure

# Output JSON
The output for each PDF must contain:

    1. Document Title->> Extracted from the first page’s largest font text (or heuristically derived)

    2. Heading Structure->>For each heading:
        a. level: H1, H2, H3, etc.
        b. text: heading content
        c. page: the page number (1-indexed)

# Constraints

| Constraint         | Value                      |
| ------------------ | -------------------------- |
| CPU only           | No GPU allowed             |
| Model size         | ≤ 200 MB                   |
| Processing time    | ≤ 20 seconds per PDF       |
| No Internet access | Must run offline in Docker |

### The solution in 3 modular parts

# STEP 1: PDF Parsing with PyMuPDF

1. Used PyMuPDF (fitz) to extract:
   a. Text spans with bounding boxes
   b. Associated font sizes
   c. Page-wise text blocks
2. Constructed a normalized list of font sizes
3. Mapped largest fonts to H1, then descending to H2, H3, etc.

# STEP 2: Heading Detection via Font Size Heuristics

1. Grouped headings based on relative font size buckets
2. Removed duplicates and overlapping text (e.g., headers/footers)
3. Assigned heading levels using:
    a. Largest font → Title or H1
    b. Next tier sizes → H2 and H3

# STEP 3: Output Formatting

1. Produced a clean JSON per file
2. Stored in sample-datasets/outputs/ matching input filenames

# STEP 4: Docker Packaging

1. Used a lightweight Python base image
2. Included only PyMuPDF, json, tqdm, etc.
3. Ensured offline, reproducible runs via Docker

# File Role Summary

| File / Folder              | Purpose                                                        |
| -------------------------- | -------------------------------------------------------------- |
| `process_pdfs.py`          | Main script to batch process PDFs from input folder            |
| `sample-datasets/pdfs/`    | Input PDFs directory                                           |
| `sample-datasets/outputs/` | Output JSON files for each processed PDF                       |
| `Dockerfile`               | Containerized the entire pipeline (offline use)                |
| `requirements.txt`         | List of packages (PyMuPDF, tqdm, etc.)                         |







### ROUND 1B: PERSONA-DRIVEN DOCUMENT INTELLIGENCE

# Goal

Build a system that extracts and prioritizes the most relevant sections from a collection of PDFs based on:
A persona (e.g., researcher, analyst, student)
A job-to-be-done (e.g., literature review, market analysis, exam prep)

# Inputs

PDF Collection: 3–10 related documents
Persona Definition: Role + expertise
Job-to-be-Done: Specific task the persona needs to accomplish
The documents and personas can be from any domain (research, education, business, etc.).

# Output JSON

The output must contain:

1. Metadata
    input_documents: list of input filenames
    persona: description
    job_to_be_done: task
    timestamp: processing time

2. Extracted Sections
    document: filename
    page_number
    section_title
    importance_rank: integer score for relevance

3. Subsection Analysis
    document
    page_number
    refined_text: extracted relevant content

# Constraints

| Constraint         | Value                       |
| ------------------ | --------------------------- |
| CPU only           | No GPU allowed              |
| Model size         | ≤ 1 GB                      |
| Processing time    | ≤ 60 seconds (for 3–5 PDFs) |
| No Internet access | Must run offline in Docker  |

## The solution in 3 modular parts

# STEP 1: Preprocess the PDFs (re-use from 1A)
    Used PyMuPDF (fitz) to extract:
    1. Text
    2. Page number
    3. Headings (if marked or via heuristics)
    4. Paragraph blocks 

# Step 2: Use a Lightweight NLP Model (<1GB)
    These are perfect for:
    1. Ranking section relevance
    2. Matching content to persona/job

    You can use cosine similarity between:
    1. Persona + job description (converted to embedding)
    2. Section/paragraph embeddings

    Used all-MiniLM-L6-v2 via HuggingFace to convert:
    1. Persona + Job to vector
    2. Each section/para to vector
    3. Rank based on cosine similarity

# STEP 3: Heuristic + Embedding Based Scoring
    Used a hybrid relevance scoring for example: FinalScore = (0.7 * semantic_similarity) + (0.3 * keyword_match_score)

# Step 4: Package in Docker
    Base image: python:3.10-slim
    Install only pdfminer, sentence-transformers, etc.
    No GPU or internet needed

## File Role Summary

| File / Folder             | Purpose                                                                 |
| ------------------------- | ----------------------------------------------------------------------- |
| `main.py`                 | Handles input/output directory parsing and calls `processor.py`         |
| `processor.py`            | Coordinates full pipeline: PDF → text → score → output JSON             |
| `pdf_utils.py`            | Uses `pdfminer.six` or `fitz` to extract page-wise content and headings |
| `model_utils.py`          | Loads MiniLM, computes embeddings, similarity, ranking                  |
| `config.py`               | Stores constants like model paths, thresholds, weights                  |
| `collections/`            | Input PDFs (mounted via Docker volume)                                  |
| `Dockerfile`              | Build image that works on AMD64                                         |
| `requirements.txt`        | List of packages (`sentence-transformers`, `pdfminer.six`, etc.)        |


