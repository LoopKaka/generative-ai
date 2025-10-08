import speech_recognition as sr
from image_generator import generate

def speechToText():
    rec = sr.Recognizer()

    with sr.Microphone() as mic:
        rec.adjust_for_ambient_noise(source=mic) # Remove background noise
        rec.pause_threshold = 2 # 2 sec if user is not speaking, then take it as input

        print("Speack 📣 ")
        audio = rec.listen(source=mic)

        print("Your Voice is Processing...")
        stt = rec.recognize_google(audio)
        print("You Said: ", stt)
        generate(stt)


speechToText()