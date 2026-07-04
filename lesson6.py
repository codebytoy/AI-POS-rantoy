from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

response = client.responses.create(
    model="gpt-4.1-mini",
    input="สวัสดี แนะนำตัวเองหน่อย",
)

print(response.output_text)