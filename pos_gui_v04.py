import os
import tempfile
import win32ui
import win32con

from PIL import Image, ImageDraw, ImageFont, ImageWin
import tkinter as tk
import win32print
from tkinter import ttk, messagebox, simpledialog
from storage import (
    load_products,
    save_products,
    load_sales,
    save_sales,
)
from database import get_products, add_product, update_product_stock, find_product_by_barcode_db
from product import low_stock_report, search_product_by_barcode
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

    if not barcode:
        return

    latest_products = get_products()
    found_product = None

    for product in latest_products:
        if str(product.get("barcode", "")).strip() == barcode:
            found_product = product
            break

    if found_product is None:
        messagebox.showwarning(
            "ไม่พบสินค้า",
            f"ไม่พบสินค้าบาร์โค้ด {barcode}"
        )
        search_entry.select_range(0, tk.END)
        search_entry.focus()
        return

    stock_qty = int(found_product.get("qty", 0))

    if stock_qty <= 0:
        messagebox.showwarning(
            "สินค้าหมด",
            f"{found_product['name']} ไม่มีสินค้าในสต๊อก"
        )
        search_entry.delete(0, tk.END)
        search_entry.focus()
        return

    # ตรวจว่าสินค้านี้อยู่ในตะกร้าแล้วหรือยัง
    for item in cart:
        if str(item.get("barcode", "")) == barcode:
            new_qty = item["qty"] + 1

            if new_qty > stock_qty:
                messagebox.showwarning(
                    "สินค้าไม่พอขาย",
                    f"{found_product['name']} เหลือเพียง {stock_qty} ชิ้น"
                )
                search_entry.delete(0, tk.END)
                search_entry.focus()
                return

            item["qty"] = new_qty
            item["total"] = item["price"] * item["qty"]
            break

    else:
        cart.append({
            "barcode": str(found_product.get("barcode", "")),
            "name": found_product["name"],
            "price": float(found_product["price"]),
            "qty": 1,
            "total": float(found_product["price"])
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
    height=4
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
    height=2
)

cart_table.heading("name", text="สินค้า")
cart_table.heading("qty", text="จำนวน")
cart_table.heading("total", text="รวม")

cart_table.column("name", width=420, anchor="w")
cart_table.column("qty", width=80, anchor="center")
cart_table.column("total", width=120, anchor="e")

cart_table.pack(pady=0)

total_label = tk.Label(
    root,
    text="รวมทั้งหมด: 0.00 บาท",
    font=("Arial", 18, "bold")
)
total_label.pack(pady=10)

payment_frame = tk.Frame(root)
payment_frame.pack(pady=0)

money_label = tk.Label(
    payment_frame,
    text="รับเงิน:",
    font=("Arial", 16)
)
money_label.pack(side="left", padx=5)

def update_change(event=None):
    total = sum(item.get("total", 0) for item in cart)

    money_text = money_entry.get().strip()

    if money_text == "":
        change_label.config(text="เงินทอน: 0.00 บาท")
        return

    try:
        received = float(money_text)
    except ValueError:
        change_label.config(text="กรุณากรอกตัวเลข")
        return

    change = received - total

    if change < 0:
        change_label.config(
            text=f"เงินยังขาด: {abs(change):.2f} บาท"
        )
    else:
        change_label.config(
            text=f"เงินทอน: {change:.2f} บาท"
        )
money_entry = tk.Entry(
    payment_frame,
    font=("Arial", 16),
    width=15
)
money_entry.pack(side="left", padx=5)
change_label = ttk.Label(
    payment_frame,
    text="เงินทอน: 0.00 บาท",
    font=("Tahoma", 12, "bold")
)

change_label.pack(side="left", padx=10)
money_entry.bind("<KeyRelease>", update_change)

def print_receipt(receipt_text):
    printer_name = win32print.GetDefaultPrinter()
    print("เครื่องพิมพ์ที่ใช้:", printer_name)

    # ขนาดประมาณกระดาษ 80 มม.
    image_width = 576
    padding = 20
    line_height = 34

    lines = receipt_text.splitlines()
    image_height = max(300, padding * 2 + len(lines) * line_height)

    image = Image.new("RGB", (image_width, image_height), "white")
    draw = ImageDraw.Draw(image)

    font_path = r"C:\Windows\Fonts\tahoma.ttf"

    try:
        font = ImageFont.truetype(font_path, 25)
    except OSError:
        font = ImageFont.load_default()

    y = padding

    for line in lines:
        draw.text(
            (padding, y),
            line,
            font=font,
            fill="black"
        )
        y += line_height

    printer_dc = win32ui.CreateDC()
    printer_dc.CreatePrinterDC(printer_name)

    printable_width = printer_dc.GetDeviceCaps(win32con.HORZRES)
    printable_height = printer_dc.GetDeviceCaps(win32con.VERTRES)

    scale = printable_width / image_width
    print_height = int(image.height * scale)

    printer_dc.StartDoc("AI POS Receipt")
    printer_dc.StartPage()

    dib = ImageWin.Dib(image)

    dib.draw(
        printer_dc.GetHandleOutput(),
        (0, 0, printable_width, min(print_height, printable_height))
    )

    printer_dc.EndPage()
    printer_dc.EndDoc()
    printer_dc.DeleteDC()

    # ส่งคำสั่งตัดกระดาษ
    h_printer = win32print.OpenPrinter(printer_name)

    try:
        win32print.StartDocPrinter(
            h_printer,
            1,
            ("Cut Receipt", None, "RAW")
        )
        win32print.StartPagePrinter(h_printer)

        win32print.WritePrinter(
            h_printer,
            b"\n\n\n\x1d\x56\x00"
        )

        win32print.EndPagePrinter(h_printer)
        win32print.EndDocPrinter(h_printer)

    finally:
        win32print.ClosePrinter(h_printer)

    print("พิมพ์ใบเสร็จภาษาไทยและตัดกระดาษแล้ว")

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
    change_label.config(text="เงินทอน: 0.00 บาท")
clear_button = ttk.Button(
    payment_frame,
    text="ล้างตะกร้า",
    
    command=clear_cart
)
clear_button.pack(side="left", padx=10)

def show_low_stock():
    limit = simpledialog.askinteger(
        "สินค้าใกล้หมด",
        "แจ้งเตือนเมื่อเหลือไม่เกินกี่ชิ้น:",
        initialvalue=5,
        minvalue=0
    )

    if limit is None:
        return

    latest_products = get_products()
    low_products = []

    for product in latest_products:
        qty = product.get("qty", 0)

        if qty <= limit:
            low_products.append(product)

    if not low_products:
        messagebox.showinfo(
            "สินค้าใกล้หมด",
            f"ไม่มีสินค้าที่เหลือไม่เกิน {limit} ชิ้น"
        )
        return

    lines = []

    for product in low_products:
        barcode = product.get("barcode", "-")
        name = product.get("name", "ไม่ทราบชื่อ")
        qty = product.get("qty", 0)

        if qty == 0:
            status = "สินค้าหมด"
        else:
            status = "ใกล้หมด"

        lines.append(
            f"{barcode} | {name} | เหลือ {qty} ชิ้น | {status}"
        )

    messagebox.showwarning(
        "สินค้าใกล้หมด",
        "\n".join(lines)
    )

low_stock_button = ttk.Button(
    payment_frame,
    text="สินค้าใกล้หมด",
    command=show_low_stock
)

low_stock_button.pack(side="left", padx=10)
root.bind("<F2>", lambda event: checkout())
root.bind("<Escape>", lambda event: clear_cart())

refresh_dashboard()

root.mainloop()