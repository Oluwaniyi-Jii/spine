import requests
from typing import Dict, Any, Optional
from src.utils.logger import logger

LOC_BASE_URL = "https://www.loc.gov/books/"

def fetch_loc_book_metadata(lccn: str) -> Optional[Dict[str, Any]]:
    """
    Fetch structured bibliographic record from Library of Congress API by LCCN.
    """
    url = f"{LOC_BASE_URL}?q={lccn}&fo=json"
    logger.info(f"Querying Library of Congress API for LCCN {lccn}")

    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            results = data.get("results", [])
            if results:
                item = results[0]
                return {
                    "lccn": lccn,
                    "title": item.get("title"),
                    "date": item.get("date"),
                    "subjects": item.get("subject", []),
                    "contributors": item.get("contributor", []),
                    "language": item.get("language", []),
                    "source_url": item.get("url")
                }
    except Exception as e:
        logger.error(f"Error fetching LOC metadata for LCCN {lccn}: {str(e)}")
    
    return None

if __name__ == "__main__":
    # Test query for The Great Gatsby LCCN
    result = fetch_loc_book_metadata("25008748")
    print("LOC API Query Result:", result)
