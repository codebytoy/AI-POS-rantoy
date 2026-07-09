import tkinter as tk
import win32print
from tkinter import ttk, messagebox
from storage import (
    load_products,
    save_products,
    load_sales,
    save_sales,
)
from database import get_products, add_product, update_product_stock, find_product_by_barcode_db
from product import find_product_by_barcode
from datetime import datetime


APP_NAME = "AI POS by Toy"
VERSION = "0.3 Demo"

products = get_products()
sales = load_sales()
cart = []


def search_product():
    keyword = search_entry.get().strip()

    product_table.delete(*product_table.get_children())

    latest_products = get_products()

    for product in latest_products:
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

def barcode_scan(event=None):
    barcode = search_entry.get().strip()

    products = get_products()
    product = find_product_by_barcode(products, barcode)
    
    

    if product is None:
        messagebox.showinfo("ไม่พบสินค้า", "ไม่พบสินค้า กำลังเปิดหน้าต่างเพิ่มสินค้า")
        search_entry.delete(0, tk.END)
        search_entry.focus()
        add_product_window()
        return
                
    if product["qty"] <= 0:
        messagebox.showerror("สินค้าหมด", f"{product['name']} หมดสต๊อกแล้ว")
        search_entry.delete(0, tk.END)
        search_entry.focus()
            
        return
    
    for item in cart:
        if item["barcode"] == product["barcode"]:
            if item["qty"] >= product["qty"]:
                
                messagebox.showerror("สต๊อกไม่พอ", f"{product['name']} เหลือแค่ {product['qty']}")
                search_entry.delete(0, tk.END)
                search_entry.focus()
                return

            item["qty"] += 1
            item["total"] = item["qty"] * item["price"]
            refresh_cart()
            search_entry.delete(0, tk.END)
            search_entry.focus()
            return

    cart.append({
        "barcode": product["barcode"],
        "name": product["name"],
        "qty": 1,
        "cost": product.get("cost") or 0,
        "price": product["price"],
        "total": product["price"]
            })

    refresh_cart()
    search_entry.delete(0, tk.END)
    search_entry.focus()
    
    

def add_to_cart(event):
    selected = product_table.focus()

    if not selected:
        return

    values = product_table.item(selected)["values"]

    barcode = values[0]
    name = values[1]
    price = float(values[2])
    
    product = find_product_by_barcode_db(barcode)

    cost = 0
    if product:
        cost = product[2]


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
        "cost": cost,
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

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "TButton",
    font=("Arial", 12),
    padding=6
)

style.configure(
    "TLabel",
    font=("Arial", 12)
)

style.configure(
    "Title.TLabel",
    font=("Arial", 24, "bold")
)

style.configure(
    "Dashboard.TLabelframe",
    padding=10
)

style.configure(
    "Treeview",
    font=("Arial", 11),
    rowheight=28
)

style.configure(
    "Treeview.Heading",
    font=("Arial", 11, "bold")
)



root.title("AI POS by Toy | Version 0.4")
root.geometry("1100x750")



def add_product_window():
    window = tk.Toplevel(root)
    window.title("เพิ่มสินค้า")
    window.geometry("400x350")

    tk.Label(window, text="บาร์โค้ด").pack()
    barcode_entry = tk.Entry(window, width=30)
    barcode_entry.pack()

    tk.Label(window, text="ชื่อสินค้า").pack()
    name_entry = tk.Entry(window, width=30)
    name_entry.pack()

    tk.Label(window, text="ต้นทุน").pack()
    cost_entry = tk.Entry(window, width=30)
    cost_entry.pack()

    tk.Label(window, text="ราคาขาย").pack()
    price_entry = tk.Entry(window, width=30)
    price_entry.pack()

    tk.Label(window, text="จำนวน").pack()
    qty_entry = tk.Entry(window, width=30)
    qty_entry.pack()

    def save_product():
        barcode = barcode_entry.get().strip()
        name = name_entry.get().strip()        
        
        if barcode == "" or name == "":
            messagebox.showwarning("แจ้งเตือน", "กรุณากรอกบาร์โค้ดและชื่อสินค้า")
            return

        for product in products:
            if product["barcode"] == barcode:
                messagebox.showwarning("สินค้าซ้ำ", "บาร์โค้ดนี้มีอยู่แล้วในระบบ")
                return
        
        cost = float(cost_entry.get())
        price = float(price_entry.get())
        qty = int(qty_entry.get())

        new_product = {
            "barcode": barcode,
            "name": name,
            "cost": cost,
            "price": price,
            "qty": qty
        }

        add_product(new_product)

        products.clear()
        products.extend(get_products())

        messagebox.showinfo("สำเร็จ", "เพิ่มสินค้าเรียบร้อย")

    

        window.destroy()
        search_entry.delete(0, tk.END)
        search_entry.focus()
        
        

    tk.Button(window, text="บันทึก",command=save_product).pack(pady=10)
    
    barcode_entry.focus()

# ===== MENU =====
menubar = tk.Menu(root)
toolbar = tk.Frame(root, bd=1, relief=tk.RAISED)
toolbar.pack(side=tk.TOP, fill=tk.X)
add_icon = tk.Button(
    toolbar,
    text="➕ เพิ่มสินค้า",
    command=add_product_window
)

add_icon.pack(side=tk.LEFT, padx=2, pady=2)
product_btn = tk.Button(
    toolbar,
    text="📦 สินค้า",
    command=lambda: search_product()
)

product_btn.pack(side=tk.LEFT, padx=2, pady=2)
clear_btn = tk.Button(
    toolbar,
    text="🗑 ล้างตะกร้า",
    command=lambda: clear_cart()
)

clear_btn.pack(side=tk.LEFT, padx=2, pady=2)
report_btn = tk.Button(
    toolbar,
    text="📊 รายงาน",
    command=lambda: sales_report()
)

report_btn.pack(side=tk.LEFT, padx=2, pady=2)


root.config(menu=menubar)

file_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="ไฟล์", menu=file_menu)

file_menu.add_command(label="เพิ่มสินค้า",command=add_product_window)
file_menu.add_separator()
file_menu.add_command(label="ออกจากโปรแกรม", command=root.quit)
root.title(f"{APP_NAME} - {VERSION}")
root.geometry("900x850")

title_label = ttk.Label(
    root,
    text=f"{APP_NAME}  |  {VERSION}",
    style="Title.TLabel"
)

title_label.pack(pady=10)
dashboard_text = tk.StringVar()

dashboard_frame = tk.LabelFrame(
    root,
    text="📊 Dashboard วันนี้",
    font=("Arial", 12, "bold"),
    padx=15,
    pady=10
)
dashboard_frame.pack(pady=5)

dashboard_label = tk.Label(
    dashboard_frame,
    textvariable=dashboard_text,
    font=("Arial", 12),
    justify="left"
)
dashboard_label.pack()



search_frame = tk.Frame(root)
search_frame.pack(pady=10)

search_entry = tk.Entry(search_frame, font=("Arial", 16), width=30)
search_entry.focus()
search_entry.pack(side="left", padx=5)
search_entry.bind("<Return>", barcode_scan)

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

cart_table.column("name", width=420, anchor="w")
cart_table.column("qty", width=80, anchor="center")
cart_table.column("total", width=120, anchor="e")

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

def print_receipt(receipt_text):
    print("กำลังส่งไปเครื่องพิมพ์...")

    printer_name = "4BARCODE 4B-2054K"

    hPrinter = win32print.OpenPrinter(printer_name)
    try:
        hJob = win32print.StartDocPrinter(
            hPrinter,
            1,
            ("AI POS Receipt", None, "RAW")
        )
        win32print.StartPagePrinter(hPrinter)

        win32print.WritePrinter(hPrinter, receipt_text.encode("cp874", errors="replace"))
        win32print.WritePrinter(hPrinter, b"\n\n\n\n\n")

        win32print.EndPagePrinter(hPrinter)
        win32print.EndDocPrinter(hPrinter)

        print("ส่งใบเสร็จไปเครื่องพิมพ์แล้ว")
    finally:
        win32print.ClosePrinter(hPrinter)

def migrate_sales_data():
    changed = 0

    for sale in sales:
        if sale.get("cost") is None:
            for product in products:
                if str(product.get("barcode")) == str(sale.get("barcode")):
                    sale["cost"] = product.get("cost") or 0
                    changed += 1
                    break

    if changed > 0:
        save_json("sales.json", sales)
        print(f"✔ Migration completed. {changed} records updated.")
    else:
        print("✔ Database already up to date.")



# migrate_sales_data()

def get_today_summary():

    today = datetime.now().strftime("%d/%m/%Y")

    total_sales = 0
    total_qty = 0
    total_profit = 0
    total_receipts = set()

    for sale in sales:

        if sale.get("datetime", "").startswith(today):

            total_sales += sale.get("total", 0)
            total_qty += sale.get("qty", 0)
            price = sale.get("price") or 0
            cost = sale.get("cost") or 0
            qty = sale.get("qty") or 0

            total_profit += (price - cost) * qty

            total_receipts.add(sale.get("receipt_no", 0))

    return {
        "sales": total_sales,
        "qty": total_qty,
        "profit": total_profit,
        "receipts": len(total_receipts)
    }

def get_low_stock_count():
    count = 0

    for product in products:
        if product.get("qty", 0) <= 5:
            count += 1

    return count

def refresh_dashboard():
    summary = get_today_summary()
    low_stock_count = get_low_stock_count()

    dashboard_text.set(
        f"💰 ยอดขายวันนี้: {summary['sales']:.2f} บาท\n"
        f"📦 ขายแล้ว: {summary['qty']} ชิ้น\n"
        f"🧾 ใบเสร็จ: {summary['receipts']} ใบ\n"
        f"💚 กำไรวันนี้: {summary['profit']:.2f} บาท\n"
        f"⚠️ สินค้าใกล้หมด: {low_stock_count} รายการ"
    )

def checkout():
    print("กดคิดเงินแล้ว")

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

    receipt_text = ""
    receipt_text += "================================\n"
    receipt_text += "        AI POS by Toy\n"
    receipt_text += "================================\n"
    receipt_text += f"เลขที่ : {receipt_no:06d}\n"
    receipt_text += f"วันที่ : {now.strftime('%d/%m/%Y %H:%M:%S')}\n"
    receipt_text += "--------------------------------\n"

    for item in cart:
        receipt_text += (
            f"{item['name']}\n"
            f"{item['qty']} x {item['price']:.2f} = {item['total']:.2f}\n"
        )

    receipt_text += "--------------------------------\n"
    receipt_text += f"รวมเงิน : {total_all:.2f} บาท\n"
    receipt_text += f"รับเงิน : {money:.2f} บาท\n"
    receipt_text += f"เงินทอน : {change:.2f} บาท\n"
    receipt_text += "================================\n"
    receipt_text += "      ขอบคุณที่ใช้บริการ\n"
    receipt_text += "================================\n"

    for item in cart:
        print("กำลังลดสต๊อก:", item["barcode"], item["qty"])
        update_product_stock(item["barcode"], item["qty"])

        sale = {
            "receipt_no": receipt_no,
            "datetime": now.strftime("%d/%m/%Y %H:%M:%S"),
            "barcode": item["barcode"],
            "name": item["name"],
            "qty": item["qty"],
            "cost": item.get("cost", 0),
            "price": item["price"],
            "total": item["total"]
        }

        sales.append(sale)

    
    save_sales(sales)

    print(receipt_text)
    print_receipt(receipt_text)

    messagebox.showinfo(
        "คิดเงินสำเร็จ",
        receipt_text
    )

    cart.clear()
    refresh_cart()
    refresh_dashboard()
    money_entry.delete(0, tk.END)
    search_entry.delete(0, tk.END)
    product_table.delete(*product_table.get_children())
    search_entry.focus()

checkout_button = ttk.Button(
    payment_frame,
    text="คิดเงิน",
    
    command=checkout
)
checkout_button.pack(side="left", padx=10)    

def clear_cart():
    cart.clear()
    refresh_cart()
    money_entry.delete(0, tk.END)
clear_button = ttk.Button(
    payment_frame,
    text="ล้างตะกร้า",
    
    command=clear_cart
)
clear_button.pack(side="left", padx=10)
root.bind("<F2>", lambda event: checkout())
root.bind("<Escape>", lambda event: clear_cart())

refresh_dashboard()

root.mainloop()