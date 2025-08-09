from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

response = client.embeddings.create(
    model="text-embedding-3-small",
    input="I am LoopKaka"
)

print(response.data[0].embedding)
print(len(response.data[0].embedding))