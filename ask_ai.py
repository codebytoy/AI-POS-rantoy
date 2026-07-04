from ai_client import client

def ask_ai():

    question = input("ถามอะไร AI : ")

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=question,
    )

    print("\nAI ตอบ\n")
    print(response.output_text)