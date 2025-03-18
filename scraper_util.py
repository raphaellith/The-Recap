import os
import json
from scraper import TheGuardianScraper, BBCScraper

HEADLINES_FILE = "headlines.json"


def load_headlines():
    """Load existing headlines from JSON file."""
    if not os.path.exists(HEADLINES_FILE):
        return {}
    with open(HEADLINES_FILE, "r") as file:
        return json.load(file)


def save_headlines(data):
    """Save headlines to JSON file."""
    with open(HEADLINES_FILE, "w") as file:
        json.dump(data, file, indent=4)


def add_headline(topic, source, headline, url):
    """Add a headline to the JSON file, avoiding duplicates."""
    data = load_headlines()

    if topic not in data:
        data[topic] = {}
    if source not in data[topic]:
        data[topic][source] = []

    if not any(entry["url"] == url for entry in data[topic][source]):
        data[topic][source].append({"headline": headline, "url": url})
        save_headlines(data)
        print(f"Added headline: {headline}")
    else:
        print(f"Duplicate headline skipped: {headline}")


def scrape_headlines():
    """Scrape headlines using The Guardian and BBC scrapers."""
    guardian_scraper = TheGuardianScraper()
    bbc_scraper = BBCScraper()
    topics = ["technology", "business", "culture"]

    for topic in topics:
        print(f"Scraping The Guardian for topic: {topic}")
        guardian_headlines = guardian_scraper.get_title_link_pairs(topic)
        for headline, url in guardian_headlines:
            add_headline(topic, "The Guardian", headline, url)

        print(f"Scraping BBC for topic: {topic}")
        bbc_headlines = bbc_scraper.get_title_link_pairs(topic)
        for headline, url in bbc_headlines:
            add_headline(topic, "BBC", headline, url)

    print("Scraping complete. Headlines saved to headlines.json.")


if __name__ == "__main__":
    scrape_headlines()
