import requests
from bs4 import BeautifulSoup

from Scrapers.Scraper import Scraper, SUPPORTED_TOPICS


class BBCScraper(Scraper):
    def __init__(self):
        super().__init__(source_name="BBC")

    def get_title_url_pairs(self, topic) -> [(str, str)]:
        assert topic in SUPPORTED_TOPICS

        if topic == "culture":
            topic = "entertainment_and_arts"

        url = f"https://www.bbc.co.uk/news/{topic}"
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')

        result = []

        for a_tag in soup.find_all("a"):
            if a_tag.get('href') is not None:
                headline_url = a_tag.get('href')
                if headline_url.startswith('/news'):
                    children = a_tag.find_all("span")
                    for child in children:
                        if child.get('aria-hidden') == 'false':
                            title = child.text
                            headline_url = 'https://www.bbc.co.uk' + headline_url
                            result.append((title, headline_url))

        return result
