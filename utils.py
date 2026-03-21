import json

def load_json(path):
    """Load and return JSON data from a file path."""
    with open(path, "r") as f:
        return json.load(f)