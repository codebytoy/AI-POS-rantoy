import json


def load_json(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_json(filename, data):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)