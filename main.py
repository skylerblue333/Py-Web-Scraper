import requests
from bs4 import BeautifulSoup
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('WebScraper')

class RobustScraper:
    def __init__(self, user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)"):
        self.headers = {'User-Agent': user_agent}
        self.session = requests.Session()
        
    def fetch(self, url, retries=3):
        for attempt in range(retries):
            try:
                logger.info(f"Fetching {url} (Attempt {attempt+1}/{retries})")
                response = self.session.get(url, headers=self.headers, timeout=10)
                response.raise_for_status()
                return response.text
            except requests.RequestException as e:
                logger.warning(f"Error fetching {url}: {e}")
                if attempt < retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
        return None

    def parse_title(self, html):
        if not html: return None
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.title.string if soup.title else "No Title"
        return title.strip()

if __name__ == "__main__":
    scraper = RobustScraper()
    html = scraper.fetch("https://example.com")
    title = scraper.parse_title(html)
    logger.info(f"Scraped Title: {title}")