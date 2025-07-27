from sentence_transformers import SentenceTransformer, util
from app.config import model_name
import re

model = SentenceTransformer(model_name)

# Define filters
NON_VEGETARIAN_KEYWORDS = [
    "beef", "pork", "shrimp", "chicken", "turkey", "meat", "fish", "lamb", "bacon", "sausage", "egg", "eggs"
]

GLUTEN_CONTAINERS = [
    "flour", "wheat", "barley", "bread", "pasta", "noodles", "bun", "tortilla"
]

def is_relevant_food_filter(task: str) -> dict:
    """
    Dynamically determine if we should filter based on vegetarian/gluten-free keywords.
    """
    task = task.lower()
    return {
        "vegetarian": "vegetarian" in task,
        "gluten_free": "gluten" in task or "gluten-free" in task
    }

def is_acceptable(text: str, filters: dict) -> bool:
    text = text.lower()
    if filters.get("vegetarian"):
        if any(word in text for word in NON_VEGETARIAN_KEYWORDS):
            return False
    if filters.get("gluten_free"):
        if any(word in text for word in GLUTEN_CONTAINERS):
            return False
    return True

def clean_section_title(text: str) -> str:
    """
    Clean section title to remove leading bullets/symbols and normalize casing.
    """
    text = re.sub(r"^[•\uf0b7oO0\s\-:•]+", "", text)
    return text.strip().capitalize()

def rank_sections(sections, persona, job):
    query = f"{persona}. Task: {job}"
    query_embedding = model.encode(query, convert_to_tensor=True)

    apply_filters = is_relevant_food_filter(job)

    ranked_sections = []
    subsection_analysis = []

    for s in sections:
        section_text = s["text"]
        embedding = model.encode(section_text, convert_to_tensor=True)
        sim_score = util.cos_sim(query_embedding, embedding).item()
        font_weight = min(s.get("font_size", 10) / 20.0, 1.0)
        final_score = 0.75 * sim_score + 0.25 * font_weight

        ranked_sections.append({
            "document": s.get("document", "unknown.pdf"),
            "page_number": s["page"],
            "section_title": clean_section_title(s["section_title"]),
            "importance_rank": round(final_score, 4),
            "text": section_text
        })

        subsection_analysis.append({
            "document": s.get("document", "unknown.pdf"),
            "page_number": s["page"],
            "refined_text": section_text
        })

    # Conditionally filter
    if apply_filters["vegetarian"] or apply_filters["gluten_free"]:
        ranked_sections = [s for s in ranked_sections if is_acceptable(s["text"], apply_filters)]
        subsection_analysis = [s for s in subsection_analysis if is_acceptable(s["refined_text"], apply_filters)]

    # Sort and convert importance_rank to clean integers (1,2,3,...)
    ranked_sections.sort(key=lambda x: x["importance_rank"], reverse=True)
    for i, s in enumerate(ranked_sections):
        s["importance_rank"] = i + 1
        s.pop("text", None)

    return {
        "sections": ranked_sections[:10],
        "subsections": subsection_analysis[:10]
    }
