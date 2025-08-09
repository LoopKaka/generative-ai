from dotenv import load_dotenv
from openai import OpenAI
from collections import Counter

load_dotenv()
client = OpenAI()

SYSTEM_PROMPT = """
   Give me one word answer
"""

user_input = input("USER > ")

messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": user_input}
]

answers = []

def aiCallGpt4():
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=messages,
        temperature=2
    )

    return response.choices[0].message.content

def aiCallGpt3():
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=2
    )

    return response.choices[0].message.content

def findFrequency():
    counter = Counter(answers)
    print("Final Answer = ", counter.most_common(1)[0])

for i in range(5):
    resp = aiCallGpt4()
    print(f"GPT 4.1 No Of Call {i+1} = ", resp)
    answers.append(resp)

for i in range(5):
    resp = aiCallGpt3()
    print(f"GPT 3.5 No Of Call {i+1} = ", resp)
    answers.append(resp)

findFrequency()

