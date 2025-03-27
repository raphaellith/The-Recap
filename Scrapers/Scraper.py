SUPPORTED_TOPICS = [  # Currently we only support these three topics, but more can be added in the future
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
