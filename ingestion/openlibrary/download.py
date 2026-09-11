import os
import requests
from tqdm import tqdm
from src.utils.config import DATA_DIR, OPENLIBRARY_DUMP_URL
from src.utils.logger import logger

DUMP_FILES = {
    "works": "ol_dump_works.txt.gz",
    "editions": "ol_dump_editions.txt.gz",
    "authors": "ol_dump_authors.txt.gz"
}

def download_file(url: str, target_path: str):
    """Download file with progress bar."""
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    logger.info(f"Downloading {url} -> {target_path}")
    response = requests.get(url, stream=True)
    response.raise_for_status()
    total_size = int(response.headers.get('content-length', 0))

    with open(target_path, 'wb') as file, tqdm(
        desc=os.path.basename(target_path),
        total=total_size,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in response.iter_content(chunk_size=1024 * 1024):
            size = file.write(data)
            bar.update(size)

def download_openlibrary_dump(dump_type: str = "works") -> str:
    """Download specific Open Library bulk dump if not already present."""
    if dump_type not in DUMP_FILES:
        raise ValueError(f"Unknown dump type: {dump_type}. Choose from {list(DUMP_FILES.keys())}")

    filename = DUMP_FILES[dump_type]
    file_url = f"{OPENLIBRARY_DUMP_URL.rstrip('/')}/{filename}"
    target_path = os.path.join(DATA_DIR, "openlibrary", filename)

    if os.path.exists(target_path):
        logger.info(f"Dump file already exists at {target_path}, skipping download.")
        return target_path

    download_file(file_url, target_path)
    return target_path

if __name__ == "__main__":
    download_openlibrary_dump("works")
