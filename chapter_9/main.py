from mem0 import Memory
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

config = {
    "llm": {
        "provider": "openai",
        "config": {
            "model": "gpt-4.1-mini"
        }
    },

    "embedder": {
        "provider": "openai",
        "config": {
            "model": "text-embedding-3-small"
        }
    },

    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": "localhost",
            "port": "6333"
        }
    },

    "graph_store": {
        "provider": "neo4j",
        "config": {
            "url": "bolt://localhost:7687",
            "username": "neo4j",
            "password": "test12345"
        }
    }
}

memory = Memory.from_config(config)

def main():
    while True:
        user_input = input("User > ")

        relevent_data = memory.search(user_id="genai", query=user_input)

        data = {}
        if 'results' in relevent_data:
            for msg in relevent_data['results']:
                id = msg['id']
                message = msg['memory']
                data[id] = message # {'21e02547-fbc9-41f0-8bc9-8dd364843195' : 'Is from India'}

        SYSTEM_PROMPT = f"""
            You are a memory aware AI agent who has information of the user in below relavent data section

            Relevent Data (Format - id: message):
            {data}
        """

        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_input}
            ]
        )

        print(response.choices[0].message.content)

        memory.add([
            {"role": "user", "content": user_input},
            {"role": "assistant", "content": response.choices[0].message.content}],
            user_id="genai"
        )
main()
