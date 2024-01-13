from openai import OpenAI
from elevenlabs import generate, play, set_api_key, voices
import speech_recognition as sr
import keyboard

import json

info = json.load(open('info.json'))

openai_key = info['OpenAIAPIKey']
elevenlabs_key = info['ElevenLabsAPIKey']

client = OpenAI(api_key=openai_key)
messages = [{"role": "user", "content": '''
            You are a human who is enthusiastic and playful, your name is Dan.

            Rules:
            1)You will say Baga-BOOSH in exclamation!
            2)You will often say poggers and rigged
            3)Sometimes bad words slip out of your mouth and you say Shit and Fuck
'''}]

set_api_key(elevenlabs_key)

while True:
    print("Press F10 to start recording your voice.")
    keyboard.wait("f10")

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Now recording voice...")
        audio = r.listen(source)

    print("Press F10 to stop recording your voice.")

    keyboard.wait("f10")

    input_words = ""

    try:
        input_words = r.recognize_whisper(audio, language="english")
        print("Whisper thinks you said " + input_words)
    except sr.UnknownValueError:
        print("Whisper could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Whisper")
    
    messages.append({"role": "user", "content": input_words})
    chat = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
    reply = chat.choices[0].message.content
    print(f"ChatGPT: {reply}")
    audio = generate(
        text=reply,
        voice="Sam",
        model="eleven_multilingual_v2"
    )
    play(audio)