import os
import json
from Scrapers import TheGuardianScraper, BBCScraper, SUPPORTED_TOPICS


class HeadlineJsonEditor:
    def __init__(self, json_file_path="headlines.json"):
        self.json_file_path = json_file_path

    def load_json_data(self):
        """Load existing headlines from JSON file."""
        if not os.path.exists(self.json_file_path):
            return {}
        with open(self.json_file_path, "r") as file:
            return json.load(file)

    def save_headlines(self, data):
        """Save the headlines in data to JSON file."""
        with open(self.json_file_path, "w") as file:
            json.dump(data, file, indent=4)

    def add_headline(self, topic, source, title, url):
        """Add a headline to the JSON file, avoiding duplicates."""
        data = self.load_json_data()

        if topic not in data:
            data[topic] = {}
        if source not in data[topic]:
            data[topic][source] = []

        if not any(entry["url"] == url for entry in data[topic][source]):  # If url doesn't already exist
            data[topic][source].append({"title": title, "url": url})
            self.save_headlines(data)
            print(f"Added headline: {title}")
        else:
            print(f"Duplicate headline skipped: {title}")


# UTIL FUNCTIONS -------------------------------------------------------------------------------------------------------

def run_scraping_and_save_to_file(json_file_path, *scrapers):
    """Scrape headlines using a specified set of scraper objects."""
    editor = HeadlineJsonEditor(json_file_path)

    for topic in SUPPORTED_TOPICS:
        for scraper in scrapers:
            print(f"Scraping {scraper.source_name} for topic: {topic}")
            title_link_pairs = scraper.get_title_url_pairs(topic)
            for title, url in title_link_pairs:
                editor.add_headline(topic, scraper.source_name, title, url)

    print("Scraping complete. Headlines saved to headlines.json.")


if __name__ == "__main__":
    """Scrape headlines using The Guardian and BBC scrapers."""
    guardian_scraper = TheGuardianScraper()
    bbc_scraper = BBCScraper()
    run_scraping_and_save_to_file("headlines.json", bbc_scraper, guardian_scraper)
