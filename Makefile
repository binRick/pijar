setup:
	python3 -m venv .v
	sh -c 'source .v/bin/activate && pip install openai SpeechRecognition pyttsx3 edge-tts'
