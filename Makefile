pi-setup:
	apt -y install python3-dev python3.11-venv raspi-config python3-pyaudio portaudio19-dev flac
setup:
	python3 -m venv .v
	bash -c "source .v/bin/activate && pip install openai SpeechRecognition pyttsx3 edge-tts PyAudio"

install:
	cp -prvf pyjar.service /etc/systemd/system/. && systemctl enable pyjar
