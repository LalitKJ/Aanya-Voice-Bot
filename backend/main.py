from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv
from io import BytesIO
from typing import List, Dict
import requests
import os
from pathlib import Path
import assemblyai as aai
from fastapi.middleware.cors import CORSMiddleware
import httpx
import google.generativeai as genai
# from google import generativeai as genai
import aiofiles

# Global in-memory chat history store
chat_history_store = {}

# Load Murf API key from .env
load_dotenv("../.env")
MURF_API_KEY = os.getenv("MURF_API_KEY")
ASSEMBLY_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")
GEMENAI_API_KEY = os.getenv("GEMENAI_API_KEY")

# Api key setups
aai.settings.api_key = ASSEMBLY_API_KEY
genai.configure(api_key=GEMENAI_API_KEY) # type: ignore

# Initialize FastAPI app
app = FastAPI()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Mount frontend folder (relative to backend directory)
app.mount("/static", StaticFiles(directory="../frontend"), name="static")


# 1. Serve the index.html file (Day 1)
@app.get("/")
def serve_home():
    return FileResponse("../frontend/index.html")

@app.get("/api/hello")
def say_hello():
    return {"message": "Hello from FastAPI!"}


# 2. Generate voice from text using Murf API and send audio link (Day 2)
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
async def generate_audio(input: TextInput):
    try:
        response = await text_to_murf_voice(input.text)
        return response.json()
    except Exception as e:
        import logging
        logging.error(f"TTS error: {e}")
        return await fallback_audio_response()


# 3. Play back audio from the generated link (Day 3)
# 4. Record your voice and play it back to you (Day 4)
# 5. Upload audio file (Day 5)
@app.post("/upload-audio")
async def upload_audio(file: UploadFile = File(...)):
    print("Request recieved for file upload")
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided for uploaded file.")
    try:
        file_location = UPLOAD_DIR / file.filename
        content = await file.read()
        with open(file_location, "wb") as f:
            f.write(content)
        return {
            "filename": file.filename,
            "content_type": file.content_type,
            "size": len(content)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")



# 6. Transcribing the audio data, and returning the transcription as response using AssemblyAI (Day 6)
@app.post("/transcribe/file")
async def transcribe_file(file: UploadFile = File(...)):
    try:
        # 1. transcribe the audio using AssemblyAI
        transcript = await voice_to_text(file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")
    return {"transcript": transcript}


# 7. Update your echo bot to repeat back what you said, in a murf voice. (Day 7)
@app.post("/tts/echo")
async def echo_tts(file: UploadFile = File(...)):
    try:
        transcript = await voice_to_text(file)
        response = await text_to_murf_voice(transcript)
        return response.json()
    except Exception as e:
        import logging
        logging.error(f"Echo TTS error: {e}")
        return await fallback_audio_response()


# 8. Accept text as input and return the response from the LLM API as response (Day 8)
# 9. Update your /llm/query endpoint to accept audio as input and return the response from the LLM API converted into audio using murf (Day 9)
@app.post("/llm/query")
async def llm_query(file: UploadFile = File(...)):
    try:
        transcript = await voice_to_text(file)
        transcript = transcript + " \nPlease answer the question in a concise manner and less than 2800 characters. Also keep formatting easy, do not answer in points, keep it all in a simple paragraph so that I can convert it into audio using Murf Ai."
        aiResponse = ask_gemini(transcript)
        res = aiResponse.text[:2999]
        response = await text_to_murf_voice(res)
        return response.json()
    except Exception as e:
        import logging
        logging.error(f"LLM query error: {e}")
        return await fallback_audio_response()



# 10. Chat history endpoint (Day 10)
class ChatMessage(BaseModel):
    role: str  # "User" or "Aanya"
    content: str

@app.post("/agent/chat/{session_id}")
async def agent_chat(session_id: str, file: UploadFile = File(...)):
    history: List[Dict] = chat_history_store.get(session_id, [])
    try:
        transcript = await voice_to_text(file)
        history.append({"role": "User", "content": transcript})
        prompt = "\n".join([
            ("User: " + msg["content"] if msg["role"] == "User" else "Aanya: " + msg["content"])
            for msg in history
        ])
        prompt += "\nPlease answer the question in a concise manner and less than 2800 characters. Also keep formatting easy, do not answer in points, keep it all in a simple paragraph so that I can convert it into audio using Murf Ai."
        aiResponse = ask_gemini(prompt)
        res = aiResponse.text[:2999]
        history.append({"role": "Aanya", "content": res})
        chat_history_store[session_id] = history
        response = await text_to_murf_voice(res)
        return {"audio": response.json(), "history": history}
    except Exception as e:
        import logging
        logging.error(f"Agent chat error: {e}")
        return await fallback_audio_response()
# class QueryInput(BaseModel):
#     text: str



# # # Helper function # # #
# 1. Text to Murf voice
async def text_to_murf_voice(text: str, voice_id: str = "en-IN-alia", format: str = "mp3"):
    url = "https://api.murf.ai/v1/speech/generate"
    payload = {
        "text": text,
        "voiceId": "en-IN-alia",
        "format": "mp3"
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

# 2. Voice to text
async def voice_to_text(file: UploadFile):
    if not file:
        raise HTTPException(status_code=400, detail="No file provided for transcription.")
    audio_bytes = await file.read()
    if not audio_bytes:
        raise HTTPException(status_code=400, detail="No audio data in uploaded file.")
    transcriber = aai.Transcriber()
    try:
        transcript = transcriber.transcribe(BytesIO(audio_bytes))
        return (transcript.text if transcript and transcript.text else "I couldn't understand that. Please try again.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")

#3. Ask Gemini ai
def ask_gemini(prompt: str, model_name: str = "gemini-2.5-flash"):
    if not prompt:
        raise HTTPException(status_code=400, detail="No prompt provided for Ai query.")
    try:
        model = genai.GenerativeModel(model_name) # type: ignore
        response = model.generate_content(prompt)
        return response
    except Exception as e:
        import logging
        logging.error(f"Gemini query error: {e}")
        raise
# Fallback audio response helper
async def fallback_audio_response():
    fallback_text = "I'm having trouble connecting right now."
    try:
        response = await text_to_murf_voice(fallback_text)
        return response.json()
    except Exception as e:
        import logging
        logging.error(f"Fallback TTS error: {e}")
        return JSONResponse(content={"error": "Unable to generate fallback audio."}, status_code=500)