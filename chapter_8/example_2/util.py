from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph import add_messages, StateGraph, START, END
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from langgraph.checkpoint.mongodb import MongoDBSaver
from langgraph.types import interrupt, Command
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode, tools_condition
import json

load_dotenv()

class State(TypedDict):
    messages: Annotated[list, add_messages]

@tool
def human_assistance(query: str) -> str:
    """
    Request assistance from a human.
    """
    human_response = interrupt({"query": query})
    return human_response["data"]

tool_list = [human_assistance]

llm = init_chat_model(model_provider="openai", model="gpt-4.1-mini")
llm_with_tools = llm.bind_tools(tools=tool_list)

def amazon_chatbot(state: State):
    resp = llm_with_tools.invoke(state["messages"])
    return {"messages": [resp]}

graph_builder = StateGraph(State)
tool_node = ToolNode(tools=tool_list)

# Add Nodes
graph_builder.add_node("amazon_chatbot", amazon_chatbot)
graph_builder.add_node("tools", tool_node)

# Add Edges
graph_builder.add_edge(START, "amazon_chatbot")
graph_builder.add_conditional_edges(
    "amazon_chatbot",
    tools_condition
)
graph_builder.add_edge("tools", "amazon_chatbot")

def checkpoint_with_graph(checkpoining):
    return graph_builder.compile(checkpointer=checkpoining)

def mongo_uri():
    return "mongodb://admin:admin@localhost:27017"

def thread_id():
    return {
        "configurable": {
            "thread_id": "101"
        }
    }