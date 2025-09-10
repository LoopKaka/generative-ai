from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph import add_messages, StateGraph, START, END
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode, tools_condition
from dotenv import load_dotenv
import requests

load_dotenv()

# Create Tools

@tool
def getWeather(place: str):
    """
        Accepts the place name as input and return the current weather of that location
    """
    url = f"http://localhost:3000/weather/{place}" # Use your API
    resp = requests.get(url)

    if resp.status_code == 200:
        return resp.text
    else:
        return "API has some issue"

@tool   
def multiply(a: int, b: int) -> int:
    """
        Multiply 2 numbers
    """
    return a * b

# List of tools   
tool_list = [getWeather, multiply]

class State(TypedDict):
    messages: Annotated[list, add_messages]

llm = init_chat_model(model_provider="openai", model="gpt-4.1-mini")
llm_with_tool = llm.bind_tools(tools=tool_list)

def chatbot_agent(state: State):
    result = llm_with_tool.invoke(state["messages"])
    return {"messages": [result]}

graph_builder = StateGraph(State)
tool_node = ToolNode(tools=tool_list)

# add node
graph_builder.add_node("chatbot_agent", chatbot_agent)
graph_builder.add_node("tools", tool_node)


# add edges
graph_builder.add_edge(START, "chatbot_agent")
graph_builder.add_conditional_edges("chatbot_agent", tools_condition)

graph_builder.add_edge("tools", "chatbot_agent")

graph = graph_builder.compile()

def main():
    user_query = input(" > ")

    _state = {
        "messages": [
            {"role": "user", "content": user_query}
        ]
    }

    events = graph.stream(_state, stream_mode="values")
    for event in events:
        event['messages'][-1].pretty_print()

main()
