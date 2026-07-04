from storage import save_json

products = []


def add_product():
    barcode = input("สแกนบาร์โค้ดสินค้า: ")

    name = input("ชื่อสินค้า : ")

    cost = float(input("ต้นทุน : "))

    price = float(input("ราคาขาย : "))

    qty = int(input("จำนวน : "))


    product = {
        "barcode": barcode,
        "name": name,
        "cost": cost,
        "price": price,
        "qty": qty
    }

    products.append(product)
    save_json("products.json", products)

    print("\nเพิ่มสินค้าเรียบร้อย")



def show_products():

    print("\n====== รายการสินค้า ======\n")

    if len(products) == 0:
        print("ยังไม่มีสินค้า")
        return

    for i, product in enumerate(products, start=1):

        print(
            f'{product["name"]} | '
            f'ต้นทุน {product.get("cost", 0):.2f} | '
            f'ขาย {product["price"]:.2f} | '
            f'คงเหลือ {product["qty"]}'
)

        print(f"   ราคา {product['price']} บาท")

        print(f"   จำนวน {product['qty']} ชิ้น")

        print("------------------------")

def show_stock_value():
    if len(products) == 0:
        print("ยังไม่มีสินค้าให้คำนวณ")
        return

    total = 0

    print("\n===== มูลค่าสต็อกสินค้า =====")

    for product in products:
        value = product["price"] * product["qty"]
        total = total + value

        print(f"{product['name']} = {value} บาท")

    print("--------------------")
    print(f"มูลค่าสต็อกรวมทั้งหมด = {total} บาท")

def search_product():
    keyword = input("กรอกชื่อสินค้าที่ต้องการค้นหา: ")

    found = False

    for product in products:
        if keyword in product["name"]:
            print("พบสินค้า")
            print(f"ชื่อ: {product['name']}")
            print(f"ราคา: {product['price']} บาท")
            print(f"จำนวน: {product['qty']} ชิ้น")
            found = True

    if found == False:
        print("ไม่พบสินค้านี้")

def search_product_detail():
    keyword = input("กรอกบาร์โค้ดหรือชื่อสินค้า: ")

    found = False

    print("\n===== ผลการค้นหา =====")

    for product in products:
        if keyword in product["barcode"] or keyword in product["name"]:
            print(f"บาร์โค้ด: {product['barcode']}")
            print(f"ชื่อ: {product['name']}")
            print(f"ต้นทุน: {product.get('cost', 0):.2f}")
            print(f"ราคาขาย: {product['price']:.2f}")
            print(f"คงเหลือ: {product['qty']} ชิ้น")
            print("------------------------")
            found = True

    if found == False:
        print("ไม่พบสินค้านี้")

def restock_product():
    barcode = input("สแกนบาร์โค้ดสินค้าที่ต้องการเติมสต็อก: ")

    for product in products:
        if barcode == product["barcode"]:
            print(f"พบสินค้า: {product['name']}")
            print(f"คงเหลือเดิม: {product['qty']} ชิ้น")

            add_qty = int(input("จำนวนที่รับเข้า: "))

            if add_qty <= 0:
                print("จำนวนต้องมากกว่า 0")
                return

            product["qty"] += add_qty
            save_json("products.json", products)

            print("เติมสต็อกเรียบร้อย")
            print(f"{product['name']} คงเหลือใหม่: {product['qty']} ชิ้น")
            return

    print("ไม่พบสินค้านี้")

def edit_product():
    barcode = input("สแกนบาร์โค้ดสินค้าที่ต้องการแก้ไข: ")

    for product in products:
        if barcode == product["barcode"]:
            print("\nพบสินค้า")
            print(f"ชื่อเดิม: {product['name']}")
            print(f"ต้นทุนเดิม: {product.get('cost', 0)}")
            print(f"ราคาขายเดิม: {product['price']}")
            print(f"จำนวนคงเหลือ: {product['qty']}")

            new_name = input("ชื่อใหม่ (Enter = ไม่แก้): ")
            new_cost = input("ต้นทุนใหม่ (Enter = ไม่แก้): ")
            new_price = input("ราคาขายใหม่ (Enter = ไม่แก้): ")

            if new_name != "":
                product["name"] = new_name

            if new_cost != "":
                product["cost"] = float(new_cost)

            if new_price != "":
                product["price"] = float(new_price)

            save_json("products.json", products)

            print("แก้ไขข้อมูลสินค้าเรียบร้อย")
            return

    print("ไม่พบสินค้านี้")

def delete_product():
    barcode = input("สแกนบาร์โค้ดสินค้าที่ต้องการลบ: ")

    for product in products:
        if barcode == product["barcode"]:
            print("\nพบสินค้า")
            print(f"ชื่อ: {product['name']}")
            print(f"ต้นทุน: {product.get('cost', 0)}")
            print(f"ราคาขาย: {product['price']}")
            print(f"คงเหลือ: {product['qty']}")

            confirm = input("พิมพ์ yes เพื่อยืนยันการลบ: ")

            if confirm == "yes":
                products.remove(product)
                save_json("products.json", products)
                print("ลบสินค้าออกจากระบบเรียบร้อย")
            else:
                print("ยกเลิกการลบสินค้า")

            return

    print("ไม่พบสินค้านี้")

def find_product_by_keyword():
    keyword = input("พิมพ์ชื่อสินค้าหรือบาร์โค้ด: ")

    results = []

    for product in products:
        if keyword in product["name"] or keyword in product["barcode"]:
            results.append(product)

    if len(results) == 0:
        print("ไม่พบสินค้า")
        return None

    print("\n===== ผลการค้นหา =====")
    for i, product in enumerate(results, start=1):
        print(f"{i}. {product['name']} | ราคา {product['price']} บาท | เหลือ {product['qty']} ชิ้น")

    choice = int(input("เลือกเลขสินค้า: "))

    if 1 <= choice <= len(results):
        return results[choice - 1]
    else:
        print("เลือกไม่ถูกต้อง")
        return None    