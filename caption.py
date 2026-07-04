from ai_client import client

def caption():

    product = input("สินค้า : ")

    response = client.responses.create(
        model="gpt-4.1-mini",

        instructions="""
คุณเป็นนักเขียนการตลาด
เขียนแคปชั่น Facebook
""",

        input=f"เขียนแคปชั่นขาย {product}",
    )

    print(response.output_text)