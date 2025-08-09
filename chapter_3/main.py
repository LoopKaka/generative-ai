from dotenv import load_dotenv
from openai import OpenAI
import json
import requests
import os

load_dotenv()
client = OpenAI()


def systemCommand(cmd: str):
    resp = os.system(cmd)
    return resp

def getWeather(place: str):
    url = f"http://localhost:3000/weather/{place}" # Use your API
    resp = requests.get(url)

    if resp.status_code == 200:
        return resp.text
    else:
        return "API has some issue"

def conversionRate(payload):
    url = f"http://localhost:3000/currency/{payload['amount']}/{payload['from_currency']}/{payload['to_currency']}" # Use your API
    resp = requests.get(url)

    if resp.status_code == 200:
        return resp.text
    else:
        return "API has some issue"


AVAIABLE_TOOLS_MAP = {
    'getWeather': getWeather,
    'conversionRate': conversionRate,
    'systemCommand': systemCommand
}

SYSTEM_PROMPT = """
    You are a helpful AI expert who solves user queries step by step using strict reasoning and structured thinking.

    You must follow these fixed stages in every conversation:
    Analyse → Plan → Action → Observe → Result methodology for every task.

    Description of Each Step:
    1. Analyse - Analyze and interpret the user's query.
    2. Plan - Decide which available tool(s) should be used.
    3. Action - Call only one tool with relevant input.
    4. Observe - Wait for the output (observation) from the tool call.
    5. Result - Generate a final answer for the user based on observations.

    Rules
   - Never skip any step — You must go through each stage one by one in order.
   - Only one function call per `Action` step.
   - Never call a function before reaching the `Action` step.
   - You can only proceed to `analyze` after an actual output is observed.
   - You must handle unknown or unclear queries by stating you're unable to solve them with the available tools.
   - Do not answer the final user query until the `Result` step.
   - You must follow the output json format.

   Output JSON format:
   {
       "step": "string",
       "content": "string",
       "tool": "The name of the tool if step is Action",
       "input": "The input parameter for the tool",
       "output": "The final result if step is Result"
   }

   Available Tools:
   - "getWeather": Accepts the place name as input and return the current weather of that location
   - "conversionRate": Accept {amount, from_currency, to_currency} as an input and returns the conversion result as output
   - "systemCommand": Accept linux command as input and runs the command

   Example:
   User: What is the weather of Delhi?
   Output: {"step": "Analyse", "content": "The user is interesetd in weather data of Delhi" }
   Output: {"step": "Plan", "content": "From the available tools I need to call the getWeather" }
   Output: {"step": "Action", "tool": "getWeather", "input": "Delhi" }
   Output: {"step": "Observe", "content": "32 degree celecious" }
   Output: {"step": "Result", "output": "Delhi weather is 32 C" }

"""
messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    
]
while True:
    user_input = input("User > ")
    messages.append({"role": "user", "content": user_input})

    while True:
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=messages
        )

        resp = json.loads(response.choices[0].message.content)

        if resp['step'] == 'Action':
            tool_name = resp['tool']
            tool_input = resp['input']
            print(f"🪓 Tool = {tool_name} and Input = {tool_input}")

            if tool_name in AVAIABLE_TOOLS_MAP:
                tool_resp = AVAIABLE_TOOLS_MAP[tool_name](tool_input)
                messages.append({"role": "assistant", "content": json.dumps({"step": "Observe", "content": tool_resp })})
                print(f"🪜 Observe: {tool_resp} ")
                continue

        if resp['step'] == 'Result':
            print(f"🤖 {resp['step']}: {resp['output']} ")
            break

        print(f"🪜 {resp['step']}: {resp['content']} ")
        messages.append({"role": "assistant", "content": json.dumps(resp)})