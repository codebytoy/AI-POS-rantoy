from ai_client import client

def analysis():

    detail = input("เล่าปัญหาร้านของคุณ : ")

    response = client.responses.create(
        model="gpt-4.1-mini",
        instructions="""
คุณเป็นที่ปรึกษาธุรกิจร้านขายของชำในประเทศไทย

วิเคราะห์ปัญหาอย่างละเอียด
เสนอแนวทางแก้ไขที่ทำได้จริง
ช่วยเพิ่มยอดขาย
ช่วยลดต้นทุน
ตอบเป็นข้อ ๆ อ่านง่าย
""",
        input=detail,
    )

    print("\nผลการวิเคราะห์\n")
    print(response.output_text)