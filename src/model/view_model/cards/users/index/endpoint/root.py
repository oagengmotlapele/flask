import json
import os

class Cards:
    def __init__(self):
        self.current_dir = os.path.dirname(__file__)

    def load_data(self, path):
        with open(path, 'r') as f:
            return json.load(f)

    def get_cards_data(self,file,user) -> dict:
        PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../../../../"))
        root = os.path.join(PROJECT_ROOT, f"src/controller/cards/users/{user}/endpoint/{file}.json")
        return self.load_data(path=root)
