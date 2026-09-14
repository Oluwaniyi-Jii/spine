import pytest
from src.text_analysis.metrics import compute_text_metrics

def test_compute_text_metrics():
    sample_text = """
*** START OF THIS PROJECT GUTENBERG EBOOK THE GREAT GATSBY ***
In my younger and more vulnerable years my father gave me some advice.
"Whenever you feel like criticizing any one," he told me, "just remember that all the people in this world haven't had the advantages that you've had."

He didn't say any more, but we've always been unusually communicative in a reserved way.
*** END OF THIS PROJECT GUTENBERG EBOOK THE GREAT GATSBY ***
    """

    res = compute_text_metrics(sample_text)
    assert res["word_count"] > 30
    assert res["sentence_count"] >= 2
    assert res["paragraph_count"] >= 2
    assert res["dialogue_percentage"] > 0
    assert res["readability_score"] > 0
