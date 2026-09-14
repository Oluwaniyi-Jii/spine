import re

def strip_gutenberg_headers(text: str) -> str:
    """
    Remove standard Project Gutenberg license headers and footers.
    Looks for markers like:
    *** START OF THIS PROJECT GUTENBERG EBOOK ... ***
    *** END OF THIS PROJECT GUTENBERG EBOOK ... ***
    """
    if not text:
        return ""

    lines = text.splitlines()
    start_idx = 0
    end_idx = len(lines)

    for i, line in enumerate(lines[:1000]):
        if "START OF THIS PROJECT GUTENBERG EBOOK" in line.upper() or "START OF THE PROJECT GUTENBERG EBOOK" in line.upper():
            start_idx = i + 1
            break

    for i in range(len(lines) - 1, max(0, len(lines) - 1000), -1):
        line = lines[i]
        if "END OF THIS PROJECT GUTENBERG EBOOK" in line.upper() or "END OF THE PROJECT GUTENBERG EBOOK" in line.upper():
            end_idx = i
            break

    cleaned_lines = lines[start_idx:end_idx]
    return "\n".join(cleaned_lines).strip()
