from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv
import requests
import os

# Load Murf API key from .env
load_dotenv(".env")
MURF_API_KEY = os.getenv("MURF_API_KEY")

app = FastAPI()

# Mount frontend folder
app.mount("/static", StaticFiles(directory="frontend"), name="static")


@app.get("/")
def serve_home():
    return FileResponse("frontend/index.html")



@app.get("/api/hello")
def say_hello():
    return {"message": "Hello from FastAPI!"}



@app.get("/voices")
def list_voices():
    url = "https://api.murf.ai/v1/speech/voices"
    headers = {
        "accept": "application/json",
        "api-key": MURF_API_KEY
    }
    res = requests.get(url, headers=headers)
    return res.json()



class TextInput(BaseModel):
    text: str
    voiceId: str = "en-IN-alia"
    format: str = "mp3"
@app.post("/generate-audio")
def generate_audio(input: TextInput):
    url = "https://api.murf.ai/v1/speech/generate"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "api-key": MURF_API_KEY
    }
    payload = {
        "text": input.text,
        "voiceId": input.voiceId,
        "format": input.format
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail=f"TTS API failed: {response.text}")
    return response.json()
