import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; WebsiteRAGBot/1.0)"
}

def is_internal_link(base_url, link):
    return urlparse(base_url).netloc == urlparse(link).netloc

def crawl_website(start_url, max_pages=20):
    visited = set()
    to_visit = [start_url]
    collected_text = []

    while to_visit and len(visited) < max_pages:
        url = to_visit.pop(0)
        if url in visited:
            continue

        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()
        except Exception:
            continue

        visited.add(url)
        soup = BeautifulSoup(response.text, "html.parser")

        # Remove scripts & styles
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        text = soup.get_text(separator=" ", strip=True)
        if text:
            collected_text.append(text)

        for a in soup.find_all("a", href=True):
            next_url = urljoin(start_url, a["href"])
            if is_internal_link(start_url, next_url):
                to_visit.append(next_url)

    return collected_text
