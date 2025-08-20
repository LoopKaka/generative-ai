from pypdf import PdfReader
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

def readPDF():
    pdf = PdfReader("simple_python.pdf")
    number_of_pages = len(pdf.pages)
    output = []
    for page_no in range(number_of_pages):
        output.append({
            'page_no': page_no,
            'page_content': pdf.pages[page_no].extract_text()
        })
    return output

SYSTEM_PROMPT = f"""
    You are an AI expert assistant. Your job is to answer user queries using ONLY the information provided in the "Context" section. 
    If a user asks a question that cannot be answered from the context, politely decline and explain that the information is not available.

    ---
    ### Context
    {readPDF()}
    ---

    ### Rules
    1. Use only the provided context when answering.
    2. Keep answers concise, clear, and professional.
    3. If the answer exists in the context, include the **page number** where it was found.
    4. If the information is not in the context, respond politely:
    - Example: "I don't have information on this topic. Sorry!"
    5. Do not make up facts or provide external knowledge.

     ---

    ### Examples

    Example 1: 
    User: When was Python language created?
    Assistant: Python was released in 1991.  
    (Found in page no: 1)

    **Example 2**  
    User: Who is Salman Khan?  
    Assistant: I don’t have information on this topic. Sorry!
"""

messages = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

while True:
    user_input = input("USER >> ")
    if user_input.lower() == 'exit':
        break

    messages.append({"role": "user", "content": user_input})
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages
    )

    print("🤖", response.choices[0].message.content)