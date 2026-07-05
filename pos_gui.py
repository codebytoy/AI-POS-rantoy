import tkinter as tk
from tkinter import ttk, messagebox
from storage import load_json


APP_NAME = "AI POS by Toy"
VERSION = "0.2 Demo"


products = load_json("products.json")


def search_product():
    keyword = search_entry.get()

    result_list.delete(*result_list.get_children())

    for product in products:
        if keyword in product["name"] or keyword in product["barcode"]:
            result_list.insert(
                "",
                "end",
                values=(
                    product["barcode"],
                    product["name"],
                    product["price"],
                    product["qty"]
                )
            )


root = tk.Tk()
root.title(f"{APP_NAME} - {VERSION}")
root.geometry("800x500")

title_label = tk.Label(
    root,
    text=f"{APP_NAME}  |  {VERSION}",
    font=("Arial", 20, "bold")
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

columns = ("barcode", "name", "price", "qty")

result_list = ttk.Treeview(root, columns=columns, show="headings", height=12)
result_list.heading("barcode", text="บาร์โค้ด")
result_list.heading("name", text="ชื่อสินค้า")
result_list.heading("price", text="ราคา")
result_list.heading("qty", text="คงเหลือ")

result_list.column("barcode", width=150)
result_list.column("name", width=300)
result_list.column("price", width=100)
result_list.column("qty", width=100)

result_list.pack(pady=10)
cart = []
cart = []

def add_to_cart(event):
    selected = result_list.focus()

    if not selected:
        return

    values = result_list.item(selected)["values"]

    barcode = values[0]
    name = values[1]
    price = float(values[2])

    found = False

    for item in cart:
        if item["barcode"] == barcode:
            item["qty"] += 1
            item["total"] = item["qty"] * item["price"]
            found = True
            break

    if found == False:
        item = {
            "barcode": barcode,
            "name": name,
            "qty": 1,
            "price": price,
            "total": price
        }
        cart.append(item)

    refresh_cart()

def refresh_cart():
    cart_list.delete(*cart_list.get_children())

    for item in cart:
        cart_list.insert(
            "",
            "end",
            values=(
                item["name"],
                item["qty"],
                item["total"]
            )
        )


cart_list = ttk.Treeview(
    root,
    columns=cart_columns,
    show="headings",
    height=8
)

cart_list.heading("name", text="สินค้า")
cart_list.heading("qty", text="จำนวน")
cart_list.heading("total", text="รวม")

cart_list.column("name", width=300)
cart_list.column("qty", width=80)
cart_list.column("total", width=120)

cart_list.pack()

root.mainloop()