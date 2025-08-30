import httpx
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import logging
import os
import asyncio
from pathlib import Path
import websockets
from murf import Murf
import json
from core.config import MURF_API_KEY

MURF_WS_URL = "wss://api.murf.ai/v1/speech/stream-input"

STATIC_CONTEXT_ID = "aanya-demo-session"

# Ensure uploads folder exists
UPLOADS_DIR = Path(__file__).resolve().parent.parent / "uploads"
UPLOADS_DIR.mkdir(exist_ok=True)

default_voice = "en-IN-alia"

async def text_to_murf_voice(text: str, voice_id: str = "en-IN-alia", format: str = "mp3"):
    url = "https://api.murf.ai/v1/speech/generate"
    payload = {
        "text": text,
        "voiceId": voice_id,
        "format": format
    }
    async with httpx.AsyncClient() as client:
        res = await client.post(
            url,
            headers={
                "accept": "application/json",
                "content-type": "application/json",
                "api-key": MURF_API_KEY if MURF_API_KEY is not None else "",
            },
            json=payload
        )
    return res


async def stream_murf_voice(text: str, voice_id: str = "en-IN-alia", format: str = "mp3"):
    async with websockets.connect(
        f"{MURF_WS_URL}?api-key={MURF_API_KEY}&sample_rate=44100&channel_type=MONO&format=WAV"
    ) as ws:
        # Send voice config first (optional)
        voice_config_msg = {
            "voice_config": {
                "voiceId": "en-US-amara",
                "style": "Conversational",
                "rate": 0,
                "pitch": 0,
                "variation": 1
            }
        }
        print(f'Sending payload : {voice_config_msg}')
        await ws.send(json.dumps(voice_config_msg))

        # Send text in one go (or chunk if you want streaming)
        text_msg = {
            "text": text,
            "end" : True # This will close the context. So you can re-run and concurrency is available.
        }
        print(f'Sending text payload: {text_msg}')
        await ws.send(json.dumps(text_msg))

        # Receive streaming audio responses from Murf
        async for message in ws:
            try:
                response = json.loads(message)
            except Exception as e:
                logging.error(f"Error parsing Murf response: {e}")
                continue

            if "audio" in response:
                # Here, you would typically stream this audio data to the client
                yield response["audio"]

            if response.get("status") == "done":
                print("Streaming complete.")
                break


def speak(text: str, voice_id: str = default_voice, output_file: str = "stream_output.wav"):
    client = Murf(api_key=MURF_API_KEY)

    file_path = UPLOADS_DIR / output_file

    # Start with a clean file
    open(file_path, "wb").close()

    res = client.text_to_speech.stream(
        text=text,
        voice_id=voice_id,
        style="Conversational"
    )

    audio_bytes = b""
    for audio_chunk in res:
        audio_bytes += audio_chunk
        with open(file_path, "ab") as f:
            f.write(audio_chunk)

    return audio_bytes


async def list_voices():
    url = "https://api.murf.ai/v1/speech/voices"
    async with httpx.AsyncClient() as client:
        res = await client.post(
            url,
            headers={
                "accept": "application/json",
                "api-key": MURF_API_KEY if MURF_API_KEY is not None else "",
            }
        )
    return res

async def fallback_audio_response():
    fallback_text = "I'm having trouble connecting right now."
    try:
        response = await text_to_murf_voice(fallback_text)
        return response.json()
    except Exception as e:
        logging.error(f"Fallback TTS error: {e}")
        return JSONResponse(content={"error": "Unable to generate fallback audio."}, status_code=500)