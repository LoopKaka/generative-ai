from dotenv import load_dotenv
from openai import OpenAI
import base64

load_dotenv()
client = OpenAI()

def generate(text: str):
    # user_input = input("> ")
    user_input = text

    print("Generating Image...")
    
    response = client.images.generate(
        model="gpt-image-1",
        prompt=user_input,
        n=1,
        quality="low",
        size="1024x1024"
    )

    image_base64 = response.data[0].b64_json
    image_bytes = base64.b64decode(image_base64)

    with open("image.png", "wb") as f:
        f.write(image_bytes)

    print("Image Generated")


# generate()