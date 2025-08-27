from typing_extensions import TypedDict
from typing import Literal
from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

class QueryIdentifier(BaseModel):
    is_coding_query: bool

class ValidateCode(BaseModel):
    is_valid_code: bool

class State(TypedDict):
    user_query: str
    is_coding_query: bool
    is_valid_code: bool
    result: str | None

def query_indentify_agent(state: State) -> State:
    print(" ⚠️ call query_indentify_agent")
    user_query = state["user_query"]
    # TODO: Call LLM
    response = client.chat.completions.parse(
        model="gpt-4.1-nano",
        messages=[
            {"role": "user", "content": user_query}
        ],
        response_format=QueryIdentifier
    )

    state["is_coding_query"] = response.choices[0].message.parsed.is_coding_query
    return state

def route_query_agent(state: State) -> Literal["code", "general"]:
    print(" ⚠️ call route_query_agent")
    is_coding = state["is_coding_query"]
    return "code" if is_coding else "general"

def coding_agent(state: State) -> State:
    print(" ⚠️ call coding_agent")
    SYSTEM_PROMPT = """
        You are a coding AI Agent, You solves user's query related to coding
    """
    user_query = state["user_query"]
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_query}
        ]
    )

    state["result"] = response.choices[0].message.content
    return state

def general_query_agent(state: State) -> State:
    print(" ⚠️ call general_query_agent")
    user_query = state["user_query"]
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": user_query}
        ]
    )

    state["result"] = response.choices[0].message.content
    return state

def validate_agent(state: State) -> State:
    print(" ⚠️ call validate_agent")
    user_query = state["user_query"]
    code = state['result']
    
    SYSTEM_PROMPT = f"""
        You are a coding AI agent, who validate below 'code' based on 'query'
        
        query: {user_query}
        code: {code}
    """
    # TODO: Call LLM
    response = client.chat.completions.parse(
        model="gpt-4.1-nano",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_query}
        ],
        response_format=ValidateCode
    )

    state["is_valid_code"] = response.choices[0].message.parsed.is_valid_code
    return state

def route_validate_agent(state: State) -> Literal["code", "__END__"]:
    print(" ⚠️ call route_validate_agent")
    is_valid_code = state["is_valid_code"]
    return "__END__" if is_valid_code else "code"

graph_builder = StateGraph(State)

# add Node
graph_builder.add_node("query_indentify_agent", query_indentify_agent)
graph_builder.add_node("route_query_agent", route_query_agent)
graph_builder.add_node("coding_agent", coding_agent)
graph_builder.add_node("general_query_agent", general_query_agent)
graph_builder.add_node("validate_agent", validate_agent)
graph_builder.add_node("route_validate_agent", route_validate_agent)


# add edges
graph_builder.add_edge(START, "query_indentify_agent")
graph_builder.add_conditional_edges("query_indentify_agent", route_query_agent, {"code": "coding_agent", "general": "general_query_agent"})

graph_builder.add_edge("general_query_agent", END)

graph_builder.add_edge("coding_agent", "validate_agent")
graph_builder.add_conditional_edges("validate_agent", route_validate_agent, {"code": "coding_agent", "__END__": END})

# Compile
graph = graph_builder.compile()

def main():
    user_query = input(" > ")

    _state = {
        "user_query": user_query,
        "is_coding_query": False,
        "result": None
    }

    # Call Graph or Invoke Graph
    # output = graph.invoke(_state)
    # print(" 🤖 ", output["result"])

    # Stream
    events = graph.stream(_state)
    for event in events:
        print(event)

main()

