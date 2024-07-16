from pathlib import Path

from openai import OpenAI

from credentials import openai_api_key

client = OpenAI(api_key=openai_api_key)

speech_file_path = Path(__file__).parent / "speech.mp3"
response = client.audio.speech.create(
  model="tts-1-hd",
  voice="alloy",
  input="Жирная кошка c двумя пятнышками на жопе пошла гулять"
)

response.stream_to_file(speech_file_path)
