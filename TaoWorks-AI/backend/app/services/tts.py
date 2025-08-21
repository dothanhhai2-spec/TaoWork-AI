import os
from openai import OpenAI

TTS_MODEL = os.getenv("TTS_MODEL", "gpt-4o-mini-tts")

def synthesize_voice(text: str, out_path: str):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    # Using new-style responses API is also possible; here we call audio.speech for simplicity
    with client.audio.speech.with_streaming_response.create(
        model=TTS_MODEL,
        voice="alloy",
        input=text
    ) as response:
        response.stream_to_file(out_path)
    return out_path
