import sqlite3
import json


DB_NAME = "shop.db"


def connect_db():
    return sqlite3.connect(DB_NAME)


def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products(
        barcode TEXT PRIMARY KEY,
        name TEXT,
        cost REAL,
        price REAL,
        qty INTEGER
    )
    """)

    conn.commit()
    conn.close()


def migrate_products_from_json():
    conn = connect_db()
    cursor = conn.cursor()

    with open("products.json", "r", encoding="utf-8") as f:
        products = json.load(f)

    for product in products:
        cursor.execute("""
        INSERT OR REPLACE INTO products
        (barcode, name, cost, price, qty)
        VALUES (?, ?, ?, ?, ?)
        """, (
            product["barcode"],
            product["name"],
            product.get("cost", 0),
            product["price"],
            product["qty"]
        ))

    conn.commit()
    conn.close()

    print(f"ย้ายสินค้า {len(products)} รายการ เข้า SQLite สำเร็จ")


def get_products():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT barcode, name, cost, price, qty
    FROM products
    """)

    rows = cursor.fetchall()
    conn.close()

    products = []

    for row in rows:
        product = {
            "barcode": row[0],
            "name": row[1],
            "cost": row[2],
            "price": row[3],
            "qty": row[4]
        }
        products.append(product)

    return products

def add_product(product):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO products
        (barcode, name, cost, price, qty)
        VALUES (?, ?, ?, ?, ?)
    """, (
        product["barcode"],
        product["name"],
        product.get("cost", 0),
        product["price"],
        product["qty"]
    ))

    conn.commit()
    conn.close()

def update_product_stock(barcode, qty):
    print("ลดสต๊อก", qty)
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE products
        SET qty = qty - ?
        WHERE barcode = ?
    """, (qty, barcode))

    conn.commit()
    conn.close()


def find_product_by_barcode_db(barcode):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM products
    WHERE barcode = ?
    """, (barcode,))

    product = cursor.fetchone()

    conn.close()
    return product


if __name__ == "__main__":
    create_tables()
    migrate_products_from_json()
    print(get_products())