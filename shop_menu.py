from sales import sell_product, sales_report, today_report
from product import add_product, show_products, search_product_by_barcode, low_stock_report
from product import add_product, show_products
from ask_ai import ask_ai
from analysis import analysis
from promotion import promotion
from caption import caption

while True:
    print("========== AI ผู้ช่วยร้าน ==========")
    print("1. คิดโปรโมชัน")
    print("2. คิดแคปชั่น")
    print("3. วิเคราะห์ร้าน")
    print("4. ถาม AI")
    print("5. เพิ่มสินค้า")
    print("6. ดูรายการสินค้า")
    print("7. ค้นหาสินค้าด้วยบาร์โค้ด")
    print("8. ขายสินค้า")
    print("9. รายงานยอดขาย")
    print("10. รายงานยอดขายวันนี้")
    print("11. สินค้าใกล้หมด")
    print("0. ออก")

    menu = input("เลือกเมนู : ")

    if menu == "1":
        promotion()

    elif menu == "2":
        caption()

    elif menu == "3":
        analysis()

    elif menu == "4":
        ask_ai()

    elif menu == "5":
        add_product()

    elif menu == "6":
        show_products()

    elif menu == "7":
        search_product_by_barcode()

    elif menu == "8":
        sell_product()

    elif menu == "9":
        sales_report()

    elif menu == "10":
        today_report()

    elif menu == "11":
        low_stock_report()

    elif menu == "0":
        print("ขอบคุณที่ใช้งานครับ")
    break

else:
    print("กรุณาเลือกเมนูใหม่")

    