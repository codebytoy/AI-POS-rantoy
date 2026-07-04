from ai_client import client


def promotion():

    product = input("สินค้าที่ต้องการโปรโมท : ")

    response = client.responses.create(
        model="gpt-4.1-mini",

        instructions="""
คุณเป็นผู้เชี่ยวชาญด้านการตลาดร้านขายของชำ
ช่วยคิดโปรโมชันที่น่าสนใจ
""",

        input=f"ช่วยคิดโปรโมชันสำหรับ {product}",
    )

    print(response.output_text)