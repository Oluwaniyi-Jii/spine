import requests
from typing import Optional
from src.utils.logger import logger

GUTENBERG_TXT_BASE_URL = "https://www.gutenberg.org/files/"

def fetch_gutenberg_text(gutenberg_id: int) -> Optional[str]:
    """Download plain text file for given Project Gutenberg ID."""
    urls = [
        f"https://www.gutenberg.org/cache/epub/{gutenberg_id}/pg{gutenberg_id}.txt",
        f"https://www.gutenberg.org/files/{gutenberg_id}/{gutenberg_id}-0.txt",
        f"https://www.gutenberg.org/files/{gutenberg_id}/{gutenberg_id}.txt"
    ]

    for url in urls:
        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                return resp.text
        except Exception as e:
            logger.debug(f"Failed to fetch {url}: {str(e)}")

    return None
