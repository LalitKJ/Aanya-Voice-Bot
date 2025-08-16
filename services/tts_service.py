import httpx
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import logging
import os

load_dotenv("../../.env")
MURF_API_KEY = os.getenv("MURF_API_KEY")

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