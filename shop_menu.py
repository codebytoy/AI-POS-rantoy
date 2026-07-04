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

    elif menu == "0":
        print("ขอบคุณที่ใช้งานครับ")
        break

    else:
        print("กรุณาเลือกเมนูใหม่")