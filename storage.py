from database import get_products
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


def load_products():
    return get_products()


def save_products(data):
    save_json("products.json", data)


def load_sales():
    return load_json("sales.json")


def save_sales(data):
    save_json("sales.json", data)

