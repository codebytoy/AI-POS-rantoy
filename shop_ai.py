from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

Question = input("ถามอะไรกับ AI: ")

response = client.responses.create(
    model="gpt-4.1-mini",
    instructions="""คุณคือผู้เชี่ยวชาญด้านร้านขายของชำในประเทศไทย
    ตอบแบบเป็นกันเอง
    เน้นการเพิ่มยอดขาย ลดต้นทุน
    เสนอไอเดียใหม่ ๆ เสมอ""",
    input=Question,)

print("\nAI ตอบว่า:\n")
print(response.output_text)