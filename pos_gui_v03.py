import tkinter as tk
from tkinter import ttk, messagebox
from storage import load_json, save_json
from datetime import datetime


APP_NAME = "AI POS by Toy"
VERSION = "0.3 Demo"

products = load_json("products.json")
sales = load_json("sales.json")
cart = []


def search_product():
    keyword = search_entry.get().strip()

    product_table.delete(*product_table.get_children())

    for product in products:
        if keyword in product["name"] or keyword in product["barcode"]:
            product_table.insert(
                "",
                "end",
                values=(
                    product["barcode"],
                    product["name"],
                    product["price"],
                    product["qty"]
                )
            )


def add_to_cart(event):
    selected = product_table.focus()

    if not selected:
        return

    values = product_table.item(selected)["values"]

    barcode = values[0]
    name = values[1]
    price = float(values[2])

    for item in cart:
        if item["barcode"] == barcode:
            item["qty"] += 1
            item["total"] = item["qty"] * item["price"]
            refresh_cart()
            return

    cart.append({
        "barcode": barcode,
        "name": name,
        "qty": 1,
        "price": price,
        "total": price
    })

    refresh_cart()


def refresh_cart():
    cart_table.delete(*cart_table.get_children())

    total_all = 0

    for item in cart:
        cart_table.insert(
            "",
            "end",
            values=(
                item["name"],
                item["qty"],
                f"{item['total']:.2f}"
            )
        )
        total_all += item["total"]

    total_label.config(text=f"รวมทั้งหมด: {total_all:.2f} บาท")


root = tk.Tk()
root.title(f"{APP_NAME} - {VERSION}")
root.geometry("900x850")

title_label = tk.Label(
    root,
    text=f"{APP_NAME}  |  {VERSION}",
    font=("Arial", 22, "bold")
)
title_label.pack(pady=10)

search_frame = tk.Frame(root)
search_frame.pack(pady=10)

search_entry = tk.Entry(search_frame, font=("Arial", 16), width=30)
search_entry.pack(side="left", padx=5)

search_button = tk.Button(
    search_frame,
    text="ค้นหา",
    font=("Arial", 14),
    command=search_product
)
search_button.pack(side="left")

product_columns = ("barcode", "name", "price", "qty")

product_table = ttk.Treeview(
    root,
    columns=product_columns,
    show="headings",
    height=10
)

product_table.heading("barcode", text="บาร์โค้ด")
product_table.heading("name", text="ชื่อสินค้า")
product_table.heading("price", text="ราคา")
product_table.heading("qty", text="คงเหลือ")

product_table.column("barcode", width=150)
product_table.column("name", width=350)
product_table.column("price", width=100)
product_table.column("qty", width=100)

product_table.pack(pady=10)
product_table.bind("<Double-1>", add_to_cart)

cart_label = tk.Label(
    root,
    text="ตะกร้าสินค้า",
    font=("Arial", 18, "bold")
)
cart_label.pack(pady=5)

cart_columns = ("name", "qty", "total")

cart_table = ttk.Treeview(
    root,
    columns=cart_columns,
    show="headings",
    height=5
)

cart_table.heading("name", text="สินค้า")
cart_table.heading("qty", text="จำนวน")
cart_table.heading("total", text="รวม")

cart_table.column("name", width=350)
cart_table.column("qty", width=100)
cart_table.column("total", width=150)

cart_table.pack(pady=5)

total_label = tk.Label(
    root,
    text="รวมทั้งหมด: 0.00 บาท",
    font=("Arial", 18, "bold")
)
total_label.pack(pady=10)

payment_frame = tk.Frame(root)
payment_frame.pack(pady=10)

money_label = tk.Label(
    payment_frame,
    text="รับเงิน:",
    font=("Arial", 16)
)
money_label.pack(side="left", padx=5)

money_entry = tk.Entry(
    payment_frame,
    font=("Arial", 16),
    width=15
)
money_entry.pack(side="left", padx=5)
def checkout():
    if len(cart) == 0:
        messagebox.showwarning("แจ้งเตือน", "ยังไม่มีสินค้าในตะกร้า")
        return

    total_all = 0
    for item in cart:
        total_all += item["total"]

    money_text = money_entry.get().strip()

    if money_text == "":
        messagebox.showwarning("แจ้งเตือน", "กรุณากรอกจำนวนเงินที่รับ")
        return

    money = float(money_text)

    if money < total_all:
        messagebox.showerror("เงินไม่พอ", "จำนวนเงินที่รับน้อยกว่ายอดรวม")
        return

    change = money - total_all
    now = datetime.now()
    receipt_no = len(sales) + 1

    for item in cart:
        for product in products:
            if item["barcode"] == product["barcode"]:
                product["qty"] -= item["qty"]

        sale = {
            "receipt_no": receipt_no,
            "datetime": now.strftime("%d/%m/%Y %H:%M:%S"),
            "barcode": item["barcode"],
            "name": item["name"],
            "qty": item["qty"],
            "price": item["price"],
            "total": item["total"]
        }

        sales.append(sale)

    save_json("products.json", products)
    save_json("sales.json", sales)

    messagebox.showinfo(
        "คิดเงินสำเร็จ",
        f"ใบเสร็จเลขที่ {receipt_no:06d}\n"
        f"รวมเงิน {total_all:.2f} บาท\n"
        f"รับเงิน {money:.2f} บาท\n"
        f"เงินทอน {change:.2f} บาท"
    )

    cart.clear()
    refresh_cart()
    money_entry.delete(0, tk.END)
    search_product()

checkout_button = tk.Button(
    payment_frame,
    text="คิดเงิน",
    font=("Arial", 16, "bold"),
    command=checkout
)
checkout_button.pack(side="left", padx=10)

root.mainloop()