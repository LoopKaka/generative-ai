import speech_recognition as sr
from chatbot import chat_bot
from dotenv import load_dotenv
from openai import AsyncOpenAI
from openai.helpers import LocalAudioPlayer
import asyncio

load_dotenv()
client = AsyncOpenAI()

async def textToSpeech(text):
    async with client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=text,
        instructions="Speak in a cheerful and positive tone.",
        response_format="pcm"
    ) as response:
        await LocalAudioPlayer().play(response)
        


def speechToText():
    rec = sr.Recognizer()

    with sr.Microphone() as mic:
        rec.adjust_for_ambient_noise(source=mic) # Remove background noise
        rec.pause_threshold = 2 # 2 sec if user is not speaking, then take it as input

        print("Speack 📣 ")
        audio = rec.listen(source=mic)

        print("Your Voice is Processing...")
        stt = rec.recognize_google(audio)
        print("Your Said: ", stt)

        resp = chat_bot(stt)
        # print(resp)
        asyncio.run(textToSpeech(resp))

speechToText()