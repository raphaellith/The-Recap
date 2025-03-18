import requests
from bs4 import BeautifulSoup


# Currently we only support these three topics, but more can be added in the future

SUPPORTED_TOPICS = [
    "technology",
    "business",
    "culture"
]


class Scraper:
    def __init__(self, source_name):
        """
        self.source_name is the name of the news source.
        """
        self.source_name = source_name

    def get_title_url_pairs(self, topic: str) -> [(str, str)]:  # ABSTRACT
        """
        Given a topic, returns a list of (title, url) pairs scraped from the site.
        The topic is a string that must be one of the SUPPORTED_TOPICS. See above.
        """
        raise NotImplementedError("get_title_link_pairs() is abstract and should be implemented!")

    def get_titles(self, topic: str) -> [str]:
        """
        Given a topic, returns a list of titles scraped from the site.
        """
        return list(list(zip(*self.get_title_url_pairs(topic=topic)))[0])


# ----------------------------------------------------------------------------------------------------------------------


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
