from dotenv import load_dotenv
from openai import OpenAI
from guardrails.hub import DetectPII
from guardrails import Guard

load_dotenv()
client = OpenAI()

def gudrail_pii(user_input: str) -> bool:
    # Setup Guard
    guard = Guard().use(
        DetectPII, ["EMAIL_ADDRESS", "PHONE_NUMBER"], "exception"
    )

    try:
        guard.validate(user_input)
        return True
    except Exception as e:
        return False


# SYSTEM_PROMPT = """
#     You are a Guardrail AI Agent.
#     Your role is to validate user inputs and ensure that sensitive personal information is not accepted.

#     Rules:
#     - If the user provides an email address, phone number, or credit card information, you must reject the request.
#     - Respond with a clear rejection message explaining that such information is not allowed.
#     - Encourage the user to try another query without sharing sensitive details.

#     Example:
#     User: My email id is abc@gmail.com
#     Output: We don’t accept any information related to emails, phone numbers, or credit cards. Please try another query.
# """

def main():
    user_input = input("User >")

    is_correct = gudrail_pii(user_input)

    if is_correct == True:
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                # {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_input}
            ]
        )

        print(response.choices[0].message.content)
    else:
        print("Invalid Input")

main()