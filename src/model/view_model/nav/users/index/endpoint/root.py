import json
import os

class Nav:
    def __init__(self):
        self.current_dir = os.path.dirname(__file__)

    def load_data(self, path):
        with open(path, 'r') as f:
            return json.load(f)

    def index_py(self) -> dict:
        PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../../../../"))
        root = os.path.join(PROJECT_ROOT, "src/controller/nav/users/index/endpoint/root.json")

        return {
            "/": self.load_data(path=root)
        }

Nav().index_py()