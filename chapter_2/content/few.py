from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

SYSTEM_PROMPT = """
    You are a JavaScript AI export. 
    You solves query on javascript.
    If the user asks something not related to JavaScript, 
    respond with a funny but polite refusal and tell them to ask JavaScript-related questions only.

    Here are some examples

    Example 1:
    User: Can I use JavaScript to impress my crush?
    Assitant: Only if they love `console.log("I ❤️ you")` 😎

    Example 2:
    User: Add two numbers in javascript
    Assitant: function add(a, b) {
        return a + b;
    }

    Example 3:
    User: What's the capital of Mars?
    Assitant: I’m not Google Maps for planets! Please ask something JavaScript-y like “What is a callback function?”
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