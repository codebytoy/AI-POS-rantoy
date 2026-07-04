from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

while True:
    keyword = input("\nพิมพ์คำสั้น ๆ (พิมพ์ exit เพื่อออก): ")

    if keyword.lower() == "exit":
        print("ลาก่อน 👋")
        break

    response = client.responses.create(
        model="gpt-5.5",
        input=f"""
คุณคือผู้เชี่ยวชาญด้านการเขียน Prompt สำหรับสร้างภาพ AI

จงเปลี่ยนคำสั้น ๆ ต่อไปนี้ให้เป็น Prompt ภาษาอังกฤษระดับมืออาชีพ

คำสั้น ๆ:
{keyword}

ตอบเฉพาะ Prompt ภาษาอังกฤษ
"""
    )

    print("\n==============================")
    print(response.output_text)
    print("==============================")