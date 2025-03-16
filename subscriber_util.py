import json
from scraper import TheGuardianScraper, BBCScraper

def load_subscribers(file_path="subscribers.json"):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"subscribers": {}}

def save_subscribers(data, file_path="subscribers.json"):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

def add_subscriber(user_id, first_name, email, topics, file_path="subscribers.json"):
    data = load_subscribers(file_path)
    data["subscribers"][user_id] = {
        "first_name": first_name,
        "email": email,
        "topics": topics,
        "subscribed": True
    }
    save_subscribers(data, file_path)
    print(f"Subscriber {first_name} added successfully!")

#test
add_subscriber("anotherperson", "John", "john.doe@example.com", ["technology", "business"])
print(load_subscribers())
