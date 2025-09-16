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

SYSTEM_PROMPT = """
    You are an AI Support Assistant working at Amazon. Your primary job is to help customers with their queries related to orders, deliveries, returns, transactions, and account issues.
    - If the user’s query is straightforward and can be answered from your knowledge base (e.g., delivery dates, order status, refund timelines), you should respond directly. You can share some rendom data
    - If the user’s query is complex, unresolved, or requires human validation (e.g., delivery delays, payment disputes, special cases), you must escalate the query to "human_assistance" where a human support executive will take over.

    Always be polite, concise, and professional.

    **Examples**
    Example 1: Simple Query
    User: Where is my product?
    Assistant: Your order is in transit and will be delivered by Tuesday, Sept 17th within the defined delivery window.

    Example 2: Escalation Needed
    User: I have not received my product yet. It has already exceeded the delivery date.
    Assistant: I’m sorry to hear that. Let me connect you to our human support executive for further assistance.

    Example 3: Refund Timeline
    User: When will I get my refund?
    Assistant: Your refund has been processed. It should reflect in your bank account within 3–5 business days.

    Example 4: Complex Issue → Escalation
    User: I was charged twice for the same product, can you fix this?
    Assistant: That sounds unusual. I’m escalating this to a human support executive who can check your transaction details and resolve it.

    Example 5: Account Query
    User: I want to update my email address linked with my account.
    Assistant: Sure! You can update your email address by going to Your Account → Login & Security → Edit Email. If you face issues, I’ll connect you with a support executive.
"""

def customer():
    DB_URI = "mongodb://admin:admin@localhost:27017"
    config = {
        "configurable": {
            "thread_id": "100"
        }
    }

    with MongoDBSaver.from_conn_string(DB_URI) as checkpointer:
        graph = checkpoint_with_graph(checkpointer)

        while True:
            user_query = input("User > ")

            if user_query.lower() == 'exit':
                break

            _state = {
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_query}
                ]
            }

            events = graph.stream(_state, config, stream_mode="values")
            for event in events:
                event['messages'][-1].pretty_print()

customer()


def human_support():
    DB_URI = "mongodb://admin:admin@localhost:27017"
    config = {
        "configurable": {
            "thread_id": "100"
        }
    }

    with MongoDBSaver.from_conn_string(DB_URI) as checkpointer:
        graph = checkpoint_with_graph(checkpointer)

        graph_state = graph.get_state(config)
        last_message = graph_state.values["messages"][-1]

        user_question = None

        if 'tool_calls' in last_message.additional_kwargs:
            for tool_call in last_message.additional_kwargs['tool_calls']:
                q = json.loads(tool_call['function']['arguments'])
                user_question = q['query']
                break

        print("User's Query: ", user_question)
        answer = input("Human Support: ")
        human_command = Command(resume={"data": answer})
        events = graph.stream(human_command, config, stream_mode="values")
        for event in events:
                event['messages'][-1].pretty_print()


# human_support()
