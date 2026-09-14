import re
from typing import Dict, Any
from src.text_analysis.cleaner import strip_gutenberg_headers

def compute_text_metrics(text: str) -> Dict[str, Any]:
    """
    Calculate text statistics and readability metrics:
    - word_count
    - unique_word_count
    - sentence_count
    - paragraph_count
    - avg_word_length
    - avg_sentence_length
    - dialogue_percentage
    - readability_score (Flesch Reading Ease)
    """
    cleaned = strip_gutenberg_headers(text)
    if not cleaned:
        return {
            "word_count": 0, "unique_word_count": 0, "sentence_count": 0,
            "paragraph_count": 0, "avg_word_length": 0.0, "avg_sentence_length": 0.0,
            "dialogue_percentage": 0.0, "readability_score": 0.0
        }

    words = re.findall(r'\b\w+\b', cleaned.lower())
    sentences = [s.strip() for s in re.split(r'[.!?]+', cleaned) if s.strip()]
    paragraphs = [p.strip() for p in cleaned.split('\n\n') if p.strip()]

    word_count = len(words)
    unique_words = len(set(words))
    sentence_count = len(sentences)
    paragraph_count = len(paragraphs)

    avg_word_length = round(sum(len(w) for w in words) / word_count, 2) if word_count > 0 else 0.0
    avg_sentence_length = round(word_count / sentence_count, 2) if sentence_count > 0 else 0.0

    # Count quotes for dialogue percentage estimation
    dialogue_matches = re.findall(r'"([^"]*)"', cleaned)
    dialogue_words = sum(len(re.findall(r'\b\w+\b', d)) for d in dialogue_matches)
    dialogue_percentage = round((dialogue_words / word_count) * 100, 2) if word_count > 0 else 0.0

    # Approximate Flesch Reading Ease
    syllables = sum(max(1, len(re.findall(r'[aeiouyAEIOUY]', w))) for w in words)
    if word_count > 0 and sentence_count > 0:
        flesch_score = 206.835 - (1.015 * (word_count / sentence_count)) - (84.6 * (syllables / word_count))
        readability_score = round(max(0.0, min(100.0, flesch_score)), 2)
    else:
        readability_score = 0.0

    return {
        "word_count": word_count,
        "unique_word_count": unique_words,
        "sentence_count": sentence_count,
        "paragraph_count": paragraph_count,
        "avg_word_length": avg_word_length,
        "avg_sentence_length": avg_sentence_length,
        "dialogue_percentage": dialogue_percentage,
        "readability_score": readability_score
    }
