from datetime import datetime
from storage import load_sales, save_sales
from product import load_products, save_products


def save_sale(barcode, name, cost, price, qty):
    sales = load_sales()

    receipt_no = len(sales) + 1
    now = datetime.now()

    sale = {
        "receipt_no": receipt_no,
        "datetime": now.strftime("%d/%m/%Y %H:%M:%S"),
        "barcode": barcode,
        "name": name,
        "qty": qty,
        "cost": cost,
        "price": price,
        "total": price * qty
    }

    sales.append(sale)
    save_sales(sales)


def sell_product():
    products = load_products()

    barcode = input("บาร์โค้ดสินค้า : ").strip()

    for product in products:

        if str(product.get("barcode")) == barcode:

            print(f"\nชื่อสินค้า : {product['name']}")
            print(f"ราคา : {product['price']:.2f} บาท")
            print(f"คงเหลือ : {product['qty']} ชิ้น")

            try:
                qty = int(input("ขายกี่ชิ้น : "))
            except ValueError:
                print("กรุณากรอกจำนวนเป็นตัวเลข")
                return

            if qty <= 0:
                print("จำนวนที่ขายต้องมากกว่า 0")
                return

            if qty > product["qty"]:
                print("สินค้าไม่พอ")
                return

            product["qty"] -= qty
            save_products(products)

            save_sale(
                str(product.get("barcode")),
                product["name"],
                product.get("cost", 0),
                product["price"],
                qty
            )

            total = qty * product["price"]

            print("\nขายสำเร็จ")
            print(f"ยอดขาย : {total:.2f} บาท")
            print(f"คงเหลือ : {product['qty']} ชิ้น")

            return
        
def sales_report():
    sales = load_sales()

    if len(sales) == 0:
        print("\nยังไม่มีข้อมูลการขาย")
        return

    total_sales = 0
    total_qty = 0
    total_profit = 0

    for sale in sales:
        qty = sale.get("qty", 0)
        price = sale.get("price", 0)
        cost = sale.get("cost", 0)
        total = sale.get("total", price * qty)

        total_sales += total
        total_qty += qty
        total_profit += (price - cost) * qty

    print("\n========== รายงานยอดขาย ==========")
    print(f"จำนวนรายการขาย : {len(sales)} รายการ")
    print(f"จำนวนสินค้าที่ขาย : {total_qty} ชิ้น")
    print(f"ยอดขายรวม : {total_sales:.2f} บาท")
    print(f"กำไรรวมโดยประมาณ : {total_profit:.2f} บาท")

def today_report():
    sales = load_sales()

    today = datetime.now().strftime("%d/%m/%Y")

    today_sales = []

    for sale in sales:
        sale_datetime = sale.get("datetime", "")

        if sale_datetime.startswith(today):
            today_sales.append(sale)

    if len(today_sales) == 0:
        print("\nวันนี้ยังไม่มีข้อมูลการขาย")
        return

    total_sales = 0
    total_qty = 0
    total_profit = 0
    receipt_numbers = set()

    for sale in today_sales:
        qty = sale.get("qty", 0)
        price = sale.get("price", 0)
        cost = sale.get("cost", 0)
        total = sale.get("total", price * qty)

        total_sales += total
        total_qty += qty
        total_profit += (price - cost) * qty

        receipt_no = sale.get("receipt_no")

        if receipt_no is not None:
            receipt_numbers.add(receipt_no)

    print("\n========== สรุปยอดขายวันนี้ ==========")
    print(f"วันที่ : {today}")
    print(f"จำนวนบิล : {len(receipt_numbers)} บิล")
    print(f"จำนวนสินค้าที่ขาย : {total_qty} ชิ้น")
    print(f"ยอดขายรวม : {total_sales:.2f} บาท")
    print(f"กำไรรวมโดยประมาณ : {total_profit:.2f} บาท")