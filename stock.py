from product import *
from datetime import datetime
from storage import load_json, save_json
products = ()
products = []
sales = []
cart = []









def product_menu():
    while True:
        print("\n====== จัดการสินค้า ======")
        print("1. เพิ่มสินค้า")
        print("2. ดูรายการสินค้า")
        print("3. ดูมูลค่าสต็อกรวม")
        print("4. ค้นหาสินค้า")
        print("5. เติมสต็อกสินค้า")
        print("6. แก้ไขข้อมูลสินค้า")
        print("7. ลบสินค้าออกจากระบบ")
        print("8. ค้นหาสินค้าด้วยบาร์โค้ดหรือชื่อ")
        print("9. ค้นหาแบบเลือกเลข")
        print("0. กลับเมนูหลัก")

        choice = input("เลือกเมนู: ")

        if choice == "1":
            add_product()
        elif choice == "2":
            show_products()
        elif choice == "3":
            show_stock_value()
        elif choice == "4":
            search_product()
        elif choice == "5":
            restock_product()
        elif choice == "6":
            edit_product()
        elif choice == "7":
            delete_product()
        elif choice == "8":
            search_product_detail()
        elif choice == "9":
            find_product_by_keyword()
        elif choice == "0":
            break
        else:
            print("กรุณาเลือกเมนูให้ถูกต้อง")


def sell_menu():
    while True:
        print("\n====== ขายสินค้า ======")
        print("1. ขายสินค้าแบบเร็ว")
        print("2. ตะกร้าสินค้า")
        print("3. ขายด้วยชื่อสินค้า")
        print("0. กลับเมนูหลัก")

        choice = input("เลือกเมนู: ")

        if choice == "1":
            sell_product()
        elif choice == "2":
            scan_cart()
        elif choice == "3":
            sell_product_by_search()
        elif choice == "0":
            break
        else:
            print("กรุณาเลือกเมนูให้ถูกต้อง")


def report_menu():
    while True:
        print("\n====== รายงาน ======")
        print("1. เช็กสินค้าใกล้หมด")
        print("2. รายงานยอดขาย")
        print("3. รายงานกำไร")
        print("0. กลับเมนูหลัก")

        choice = input("เลือกเมนู: ")

        if choice == "1":
            check_low_stock()
        elif choice == "2":
            sales_report()
        elif choice == "3":
            profit_report()
        elif choice == "0":
            break
        else:
            print("กรุณาเลือกเมนูให้ถูกต้อง")


def sell_product():
    barcode = input("สแกนบาร์โค้ด: ")
    sell_qty = int(input("จำนวนที่ขาย: "))
    

    for product in products:
        if barcode == product["barcode"]:

            if sell_qty <= product["qty"]:

                product["qty"] = product["qty"] - sell_qty
                save_json("products.json", products)

                total_price = product["price"] * sell_qty

                sale = {
                    "barcode": product["barcode"],
                    "name": product["name"],
                    "qty": sell_qty,
                    "price": product["price"],
                    "total": total_price
                }

                sales.append(sale)
                save_json("sales.json", sales)

                print("ขายสินค้าเรียบร้อย")
                print(f"ขาย {product['name']} จำนวน {sell_qty} ชิ้น")
                print(f"รวมเงิน {total_price} บาท")
                print(f"คงเหลือ {product['qty']} ชิ้น")

            else:
                print("สินค้าไม่พอขาย")

            return

    print("ไม่พบสินค้านี้")

def print_receipt(items, total_all, money, change):
    now = datetime.now()
    receipt_no = len(sales) + 1

    print("\n" + "=" * 36)
    print("          ร้านชำของคุณต่อย")
    print("          AI POS by Toy")
    print("=" * 36)
    print(f"เลขที่ใบเสร็จ : {receipt_no:06d}")
    print(f"วันที่        : {now.strftime('%d/%m/%Y')}")
    print(f"เวลา         : {now.strftime('%H:%M:%S')}")
    print("-" * 36)

    for item in items:
        name = item["name"]
        qty = item["qty"]
        price = item["price"]
        total = item["total"]

        print(f"{name}")
        print(f"  {qty} x {price:.2f} = {total:.2f} บาท")

    print("-" * 36)
    print(f"รวมเงิน      {total_all:.2f} บาท")
    print(f"รับเงิน      {money:.2f} บาท")
    print(f"เงินทอน      {change:.2f} บาท")
    print("=" * 36)
    print("        ขอบคุณที่ใช้บริการ")
    print("=" * 36)


def sell_product_by_search():
    keyword = input("พิมพ์ชื่อสินค้าหรือบาร์โค้ด: ")

    results = []

    for product in products:
        if keyword in product["name"] or keyword in product["barcode"]:
            results.append(product)

    if len(results) == 0:
        print("ไม่พบสินค้า")
        return

    print("\n===== ผลการค้นหา =====")
    for i, product in enumerate(results, start=1):
        print(f"{i}. {product['name']} | ราคา {product['price']} บาท | เหลือ {product['qty']} ชิ้น")

    choice = int(input("เลือกเลขสินค้า: "))

    if choice < 1 or choice > len(results):
        print("เลือกไม่ถูกต้อง")
        return

    product = results[choice - 1]

    sell_qty = int(input("จำนวนที่ขาย: "))

    if sell_qty <= 0:
        print("จำนวนต้องมากกว่า 0")
        return

    if sell_qty > product["qty"]:
        print("สินค้าไม่พอขาย")
        return

    product["qty"] = product["qty"] - sell_qty
    save_json("products.json", products)

    total_price = product["price"] * sell_qty

    sale = {
        "barcode": product["barcode"],
        "name": product["name"],
        "qty": sell_qty,
        "cost": product.get("cost", 0),
        "price": product["price"],
        "total": total_price
    }

    money = float(input("รับเงิน: "))

    if money < total_price:
        print("เงินไม่พอ ยังไม่บันทึกยอดขาย")
        product["qty"] = product["qty"] + sell_qty
        save_json("products.json", products)
        return

    change = money - total_price

    sales.append(sale)
    save_json("sales.json", sales)

    items = [sale]
    print_receipt(items, total_price, money, change)

    print(f"คงเหลือ {product['qty']} ชิ้น")

def scan_cart():
    cart = []
    now = datetime.now()
    receipt_no = len(sales) + 1

    while True:
        print("\n" * 2)
        print("=" * 35)
        print("        ตะกร้าสินค้า")
        print("=" * 35)

        total_all = 0

        if len(cart) == 0:
            print("ยังไม่มีสินค้า")
        else:
            for i, item in enumerate(cart, start=1):
                print(f"{i}. {item['name']}")
                print(f"   {item['qty']} x {item['price']:.2f} = {item['total']:.2f}")

                total_all += item["total"]

            print("-" * 35)
            print(f"รวมทั้งหมด {total_all:.2f} บาท")
            print("=" * 35)
        print("\n====== ตะกร้าสินค้า ======")
        for item in cart:
            print(f"{item['name']} x {item['qty']} = {item['total']} บาท")

        total_all = 0
        for item in cart:
            total_all += item["total"]

        print("-" * 30)
        print(f"รวมทั้งหมด: {total_all:.2f} บาท")
        print("คำสั่ง: 0=คิดเงิน | del=ลบสินค้า | search=ค้นหาด้วยชื่อ")

        barcode = input("nสแกนสินค้า / 0=คิดเงิน / del=ลบ / search=ค้นหา: ")

        if barcode == "0":
            break

        if barcode == "search":
            product = find_product_by_keyword()
            if product == None:
                continue
            barcode = product["barcode"]

        if barcode == "del":
            if len(cart) == 0:
                print("ยังไม่มีสินค้าในตะกร้า")
                continue

            for i, item in enumerate(cart, start=1):
                print(f"{i}. {item['name']} x {item['qty']} = {item['total']} บาท")

            delete_index = int(input("เลือกเลขสินค้าที่ต้องการลบ: "))

            if 1 <= delete_index <= len(cart):
                removed_item = cart.pop(delete_index - 1)
                print(f"ลบ {removed_item['name']} ออกจากตะกร้าแล้ว")
            else:
                print("เลขที่เลือกไม่ถูกต้อง")

            continue

        found = False

        for product in products:
            if barcode == product["barcode"]:
                qty = int(input("จำนวน: "))

                if qty <= 0:
                    print("จำนวนต้องมากกว่า 0")
                    found = True
                    break

                current_qty_in_cart = 0
                for cart_item in cart:
                    if cart_item["barcode"] == barcode:
                        current_qty_in_cart += cart_item["qty"]

                if current_qty_in_cart + qty > product["qty"]:
                    print("สินค้าไม่พอขาย")
                    found = True
                    break

                item_total = product["price"] * qty

                found_in_cart = False

                for cart_item in cart:
                    if cart_item["barcode"] == barcode:
                        cart_item["qty"] += qty
                        cart_item["total"] += item_total
                        found_in_cart = True
                        break

                if found_in_cart == False:
                    item = {
                        "receipt_no": receipt_no,
                        "datetime": now.strftime("%d/%m/%Y %H:%M:%S"),
                        "barcode": product["barcode"],
                        "name": product["name"],
                        "qty": qty,
                        "cost": product.get("cost", 0),
                        "price": product["price"],
                        "total": item_total
                    }

                    cart.append(item)

                print(f"เพิ่ม {product['name']} จำนวน {qty} ชิ้น เข้าตะกร้า")
                found = True
                break

        if found == False:
            print("ไม่พบสินค้านี้")

    if len(cart) == 0:
        print("ไม่มีสินค้าในตะกร้า")
        return

    total_all = 0
    for item in cart:
        total_all += item["total"]

    money = float(input("รับเงิน: "))

    if money < total_all:
        print("เงินไม่พอ ยังไม่บันทึกยอดขาย")
        return

    change = money - total_all

    for item in cart:
        for product in products:
            if item["barcode"] == product["barcode"]:
                product["qty"] -= item["qty"]

        sales.append(item)

    save_json("products.json", products)
    save_json("sales.json", sales)

    print_receipt(cart, total_all, money, change)

    cart.clear()

def check_low_stock():
    found = False

    print("\n===== สินค้าใกล้หมด =====")

    for product in products:
        if product["qty"] <= 5:
            print(f"{product['name']} เหลือ {product['qty']} ชิ้น")
            found = True

    if found == False:
        print("ยังไม่มีสินค้าใกล้หมด")
def sales_report():
    print("\n====== รายงานยอดขาย ======")

    if len(sales) == 0:
        print("ยังไม่มีรายการขาย")
        return

    total_sales = 0
    best_seller = {}

    for sale in sales:
        total_sales += sale["total"]

        name = sale["name"]
        qty = sale["qty"]

        if name not in best_seller:
            best_seller[name] = 0

        best_seller[name] += qty

    best_name = max(best_seller, key=best_seller.get)
    best_qty = best_seller[best_name]

    print(f"จำนวนรายการขาย : {len(sales)}")
    print(f"ยอดขายรวม : {total_sales:.2f} บาท")
    print()
    print("สินค้าขายดีที่สุด")
    print(f"{best_name} ขายทั้งหมด {best_qty} ชิ้น")
def profit_report():
    print("\n====== รายงานกำไร ======")

    if len(sales) == 0:
        print("ยังไม่มีรายการขาย")
        return

    total_sales = 0
    total_cost = 0

    for sale in sales:
        total_sales += sale["total"]

        cost = sale.get("cost", 0)
        qty = sale["qty"]

        total_cost += cost * qty

    profit = total_sales - total_cost

    print(f"ยอดขายรวม : {total_sales:.2f} บาท")
    print(f"ต้นทุนรวม : {total_cost:.2f} บาท")
    print(f"กำไรรวม : {profit:.2f} บาท") 
products = load_json("products.json")

import product
product.products = products

sales = load_json("sales.json")

while True:
    print("\n========================")
    print("      POS ร้านต่อย")
    print("========================")
    print("1. จัดการสินค้า")
    print("2. ขายสินค้า")
    print("3. รายงาน")
    print("0. ออกจากโปรแกรม")

    choice = input("เลือกเมนู: ")

    if choice == "1":
        product_menu()
    elif choice == "2":
        sell_menu()
    elif choice == "3":
        report_menu()
    elif choice == "0":
        print("ออกจากโปรแกรม")
        break
    else:
        print("กรุณาเลือกเมนูให้ถูกต้อง")