from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

SYSTEM_PROMPT = """
    You are a JavaScript AI export. 
    You solves query on javascript.
    If user ask question not related to javascript, just tell them to ask javascript related questions only
"""

while True:
    user_input = input("👨🏻‍🎓 ")

    if user_input.lower() == 'exit':
        break

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ]
    )

    print("🤖 ", response.output_text)