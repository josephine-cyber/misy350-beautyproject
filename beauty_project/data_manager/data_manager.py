import json
from pathlib import Path


class DataManager:
    def __init__(self):
        self.users_path = Path("data/users.json")
        self.services_path = Path("data/services.json")
        self.bookings_path = Path("data/bookings.json")

    def load_json(self, path):
        if path.exists():
            with path.open("r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def save_json(self, path, data):
        with path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def load_users(self):
        return self.load_json(self.users_path)

    def save_users(self, users):
        self.save_json(self.users_path, users)

    def load_services(self):
        return self.load_json(self.services_path)

    def save_services(self, services):
        self.save_json(self.services_path, services)

    def load_bookings(self):
        return self.load_json(self.bookings_path)

    def save_bookings(self, bookings):
        self.save_json(self.bookings_path, bookings)