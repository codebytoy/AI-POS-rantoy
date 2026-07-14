import json
import os

FILE_NAME = "products.json"


def load_products():
    if not os.path.exists(FILE_NAME):
        return []

    with open(FILE_NAME, "r", encoding="utf-8") as file:
        return json.load(file)


def save_products(products):
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(products, file, ensure_ascii=False, indent=4)


def fix_negative_stock():
    products = load_products()

    for product in products:
        if product["qty"] < 0:
            product["qty"] = 0

    save_products(products)


def add_product():
    products = load_products()

    barcode = input("บาร์โค้ดสินค้า : ").strip()
    name = input("ชื่อสินค้า : ").strip()

    if name == "":
        print("ชื่อสินค้าห้ามว่าง")
        return

    try:
        price = float(input("ราคาขาย : "))
        qty = int(input("จำนวนสินค้า : "))
    except ValueError:
        print("กรุณากรอกตัวเลขให้ถูกต้อง")
        return

    if price < 0:
        print("ราคาห้ามติดลบ")
        return

    if qty < 0:
        print("จำนวนสินค้าห้ามติดลบ")
        return

    product = {
        "barcode": barcode,
        "name": name,
        "price": price,
        "qty": qty
    }

    products.append(product)
    save_products(products)

    print("\nเพิ่มสินค้าเรียบร้อยครับ")


def show_products():
    products = load_products()

    print("\n====== รายการสินค้า ======")

    if len(products) == 0:
        print("ยังไม่มีสินค้า")
        return

    for number, product in enumerate(products, start=1):
        print(
    f"{number}. {product.get('barcode', '-')} | "
    f"{product['name']} | "
    f"ราคา {product['price']:.2f} บาท | "
    f"จำนวน {product['qty']} ชิ้น"
    )
        
def search_product_by_barcode():
    products = load_products()

    barcode = input("กรอกบาร์โค้ดสินค้า : ").strip()

    for product in products:
        if product.get("barcode") == barcode:
            print("\nพบสินค้า")
            print(f"ชื่อสินค้า : {product['name']}")
            print(f"ราคา : {product['price']:.2f} บาท")
            print(f"คงเหลือ : {product['qty']} ชิ้น")
            return

    print("\nไม่พบสินค้านี้")

def low_stock_report():
    products = load_products()

    try:
        limit = int(input("แจ้งเตือนเมื่อเหลือไม่เกินกี่ชิ้น : "))
    except ValueError:
        print("กรุณากรอกจำนวนเป็นตัวเลข")
        return

    if limit < 0:
        print("จำนวนต้องไม่ติดลบ")
        return

    low_stock_products = []

    for product in products:
        qty = product.get("qty", 0)

        if qty <= limit:
            low_stock_products.append(product)

    print("\n========== สินค้าใกล้หมด ==========")

    if len(low_stock_products) == 0:
        print(f"ไม่มีสินค้าที่เหลือไม่เกิน {limit} ชิ้น")
        return

    for product in low_stock_products:
        barcode = product.get("barcode", "-")
        name = product.get("name", "ไม่ทราบชื่อ")
        qty = product.get("qty", 0)

        if qty == 0:
            status = "สินค้าหมด"
        else:
            status = "ใกล้หมด"

        print(
            f"{barcode} | {name} | "
            f"เหลือ {qty} ชิ้น | {status}"
        )