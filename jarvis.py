#!/usr/bin/env python3
import speech_recognition as sr, openai, asyncio, edge_tts, pyttsx3, os, subprocess

WRITE_AUDIO_FILE = True
PLAY_AUDIO_WITH_EDGE_TTS = True

VOICE = "en-GB-ThomasNeural"
OUTPUT_FILE = "message"
CHAT_GPT_MODEL="gpt-3.5-turbo-0301"
openai.api_key = os.environ.get('OPENAI_KEY')
messages = []
rec = sr.Recognizer()
assistant="You are Jarvis assistant. Address me as Sir"
messages.append({"role": "system", "content": assistant})


p = subprocess.Popen(["uname", "-a"], stdout=subprocess.PIPE)
out, err = p.communicate()
out = out.decode().strip()
OS = 'unknown'
if 'Darwin' in out:
  OS = 'darwin'
else:
  OS = 'linux'

print(f'Working on {OS}')

def play_linux(f):
    subprocess.call(["espeak","-f",f])

def play_darwin(f):
    print(f"playing audio file {f}!")
    subprocess.call(["open","-g",f])
    print(f"played audio file {f}!")

def play_mp3(file):
    if OS == 'darwin':
      play_darwin(file)
    elif OS == 'linux':
      play_linux(file)
    else:
      print(f'Unhanded OS "{OS}"')
      sys.exit(1)

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
            if PLAY_AUDIO_WITH_EDGE_TTS:
              play_mp3(f)


    except Exception as e:
        print("An error has occurred: {}".format(e))

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(_main())
    finally:
        loop.close()
