from flask import json

from typing import List


# func for provide test fixtures
def load_fixtures(file_path: str) -> List[dict] | dict:
    with open(file_path) as f:
        return json.load(f)
