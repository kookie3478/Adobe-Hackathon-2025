# Approach Explanation

## Objective
This solution extracts the most relevant sections from multiple PDF documents, aligned to a persona and a specific task ("job-to-be-done").

## Methodology

1. **PDF Parsing**: Uses `PyMuPDF` to extract text and structural information from each PDF.
2. **Semantic Matching**: Loads a compact SentenceTransformer (`MiniLM`) model to compute embeddings for each text block and the persona+task.
3. **Ranking**: Ranks sections based on cosine similarity between their embeddings and the query embedding.
4. **Output**: Stores top-ranked sections and their details in a structured JSON format.

## Why This Works
- Fast inference with `MiniLM` model (<100MB)
- CPU-friendly with no external calls
- Works across various document domains

## Offline Readiness
- Model is downloaded during build; no runtime internet access required.