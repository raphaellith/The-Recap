import requests
from bs4 import BeautifulSoup

from Scrapers.Scraper import Scraper, SUPPORTED_TOPICS


class TheGuardianScraper(Scraper):
    def __init__(self):
        super().__init__(source_name="The Guardian")

    def get_title_url_pairs(self, topic) -> [(str, str)]:
        assert topic in SUPPORTED_TOPICS
        url = f"https://www.theguardian.com/{topic}/all"
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')

        result = []

        for a_tag in soup.find_all("a"):
            data_link_name = a_tag.get('data-link-name')
            if data_link_name is not None:
                if data_link_name.startswith("news") or data_link_name.startswith("feature"):
                    title = a_tag.get('aria-label')
                    link = "https://www.theguardian.com" + a_tag.get('href')
                    result.append((title, link))

        return result
