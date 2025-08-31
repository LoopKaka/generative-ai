from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph import add_messages, StateGraph, START, END
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.mongodb import MongoDBSaver
from dotenv import load_dotenv

load_dotenv()

class State(TypedDict):
    messages: Annotated[list, add_messages]

llm = init_chat_model(model_provider="openai", model="gpt-4.1-mini")

def chatbot_agent(state: State):
    result = llm.invoke(state["messages"])
    return {"messages": [result]}

graph_builder = StateGraph(State)

# add node
graph_builder.add_node("chatbot_agent", chatbot_agent)

# add edges
graph_builder.add_edge(START, "chatbot_agent")
graph_builder.add_edge("chatbot_agent", END)

# Compile
# graph = graph_builder.compile()
def compile_for_checkpoining(checkpoinig):
    return graph_builder.compile(checkpointer=checkpoinig)

def main():
    DB_URI = "mongodb://admin:admin@localhost:27017"
    config = {
        "configurable": {
            "thread_id": "2"
        }
    }
    with MongoDBSaver.from_conn_string(DB_URI) as checkpointer:
        graph = compile_for_checkpoining(checkpointer)

        user_query = input(" > ")

        _state = {
            "messages": [
                {"role": "user", "content": user_query}
            ]
        }

        # Call Graph or Invoke Graph
        output = graph.invoke(_state, config)
        # reset state
        print(" 🤖 ", output)

main()

