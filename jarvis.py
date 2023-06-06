#!/usr/bin/env python3
#Assignment: Python Project 3
#Joshua Pacheco (JP), 5/28/2023, Jarvis Co-pilot, Python3 project
#I am estimating this will take 10 hours to code. 5/24/23-5/28/23 It actually took 7.5 hours, as
#I had issues with Edge_tts, pyyttx3 and getting a key from open.ai

import speech_recognition as sr
import openai, asyncio, edge_tts, pyttsx3, os, subprocess

WRITE_AUDIO_FILE = True
PLAY_AUDIO_WITH_VLC = True
PLAY_AUDIO_WITH_EDGE_TTS = False
VOICE = "en-GB-ThomasNeural"
OUTPUT_FILE = "message"
CHAT_GPT_MODEL="gpt-3.5-turbo-0301"
openai.api_key = "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"
VLC_PATH = "C:\\Program Files\\VideoLAN\\VLC\\vlc.exe"

messages = []
rec = sr.Recognizer()
assistant="You are Jarvis assistant. Address me as Sir"
messages.append({"role": "system", "content": assistant})

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

async def _main() -> None:
    rec = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nWhat would you like to know?")
        audio = rec.listen(source)
    try:
        print(" *** Interpretting message ***")
        message = rec.recognize_google(audio, language='en-in')
        print(" *** Interpretted message ***")
        if message.lower() == "exit":
            print("\nGoodbye!")
            exit()
        else:
            print("JP: " + message)
            print("Processing......")
            messages.append({"role": "user", "content": message})

            chat = openai.ChatCompletion.create(
                model=CHAT_GPT_MODEL,
                messages=messages,
                temperature=0.5,
                max_tokens=500,
            )
            reply = chat.choices[0].message.content
            messages.append({"role": "assistant", "content": reply})
            print("\nJarvis : ---------------------------------------------\n")
            print(f" *** {len(reply)} byte chat gpt response: \"{reply}\"")
            if WRITE_AUDIO_FILE:
              communicate = edge_tts.Communicate(reply, VOICE)
              f = f"{OUTPUT_FILE}.mp3"
              print("writing audio file...")
              await communicate.save(f)
              print(f"wrote audio file to {f}!")
              if PLAY_AUDIO_WITH_VLC:
                subprocess.call([VLC_PATH,f])
            if PLAY_AUDIO_WITH_EDGE_TTS:
              print("playing audio file")
              engine.say(reply)
              engine.runAndWait()
              print("played audio file")


    except Exception as e:
        print("An error has occurred: {}".format(e))

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(_main())
    finally:
        loop.close()
