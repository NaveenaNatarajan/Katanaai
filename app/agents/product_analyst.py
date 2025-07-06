import re

def analyze_title_llm(title: str) -> str:
    """
    Analyze the title or image description and classify the product category/audience.
    """
    text = title.lower()
    if any(word in text for word in ["men", "male", "gents"]):
        return "Men's T-shirt"
    elif any(word in text for word in ["women", "female", "ladies"]):
        return "Women's T-shirt"
    return "Unisex"

def extract_keywords(text: str) -> list:
    """
    Extract keywords from the description using simple noun phrase matching.
    For production, consider NLP with spaCy or LLM.
    """
    text = text.lower()
    # Simple cleanup
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    words = text.split()

    stopwords = {"the", "a", "of", "and", "with", "for", "in", "this", "is", "to"}
    keywords = [word for word in words if word not in stopwords and len(word) > 3]

    return list(set(keywords))  # Remove duplicates
