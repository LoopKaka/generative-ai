from langgraph.checkpoint.mongodb import MongoDBSaver
from util import (checkpoint_with_graph, mongo_uri, thread_id)
from langgraph.types import Command
import json

def human_support():
    DB_URI = mongo_uri()
    config = thread_id()

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


human_support()