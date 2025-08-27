from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

class State(TypedDict):
    user_query: str
    result: str | None


def chat_agent(state: State) -> State:
    print(" ⚠️ call chat_agent")
    user_query = state["user_query"]
    # TODO: Call LLM
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": user_query}
        ]
    )

    state["result"] = response.choices[0].message.content
    return state

graph_builder = StateGraph(State)

# Add Node
graph_builder.add_node("chat_agent", chat_agent)

# Add Edges
graph_builder.add_edge(START, "chat_agent")
graph_builder.add_edge("chat_agent", END)

# Compile
graph = graph_builder.compile()

def main():
    user_query = input(" > ")

    _state = {
        "user_query": user_query,
        "result": None
    }

    # Call Graph or Invoke Graph
    output = graph.invoke(_state)
    print(" 🤖 ", output["result"])

main()