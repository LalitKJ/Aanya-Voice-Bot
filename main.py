from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Dict
import logging
from pathlib import Path
import uvicorn

# Importing services
from services.stt_service import speech_to_text
from services.tts_service import text_to_murf_voice, list_voices, fallback_audio_response
from services.llm_service import ask_gemini

# Global in-memory chat history store
chat_history_store = {}

def main():
    print("Hello from backend!")
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Initialize FastAPI app
app = FastAPI()
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Mount frontend folder (relative to backend directory)
app.mount("/static", StaticFiles(directory="./frontend"), name="static")


# 1. Serve the index.html file (Day 1)
@app.get("/")
def serve_home():
    return FileResponse("./frontend/index.html")


@app.get("/api/hello")
def say_hello():
    return {"message": "Hello from FastAPI!"}


# 2. Generate voice from text using Murf API and send audio link (Day 2)
@app.get("/voices")
async def get_voices():
    try:
        res = await list_voices()
        return res.json()
    except Exception as e:
        logging.error(f"Error fetching voices: {e}")
        return JSONResponse(content={"error": "Unable to fetch voices."}, status_code=500)

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
        transcript = await speech_to_text(file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")
    return {"transcript": transcript}


# 7. Update your echo bot to repeat back what you said, in a murf voice. (Day 7)
@app.post("/tts/echo")
async def echo_tts(file: UploadFile = File(...)):
    try:
        transcript = await speech_to_text(file)
        response = await text_to_murf_voice(transcript)
        return response.json()
    except Exception as e:
        logging.error(f"Echo TTS error: {e}")
        return await fallback_audio_response()


# 8. Accept text as input and return the response from the LLM API as response (Day 8)
# 9. Update your /llm/query endpoint to accept audio as input and return the response from the LLM API converted into audio using murf (Day 9)
@app.post("/llm/query")
async def llm_query(file: UploadFile = File(...)):
    try:
        transcript = await speech_to_text(file)
        transcript = transcript + " \nPlease answer the question in a concise manner and less than 2800 characters. Also keep formatting easy, do not answer in points, keep it all in a simple paragraph so that I can convert it into audio using Murf Ai."
        aiResponse = ask_gemini(transcript)
        res = aiResponse.text[:2999]
        response = await text_to_murf_voice(res)
        return response.json()
    except Exception as e:
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
        transcript = await speech_to_text(file)
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
        logging.error(f"Agent chat error: {e}")
        return await fallback_audio_response()
# class QueryInput(BaseModel):
#     text: str





if __name__ == "__main__":
    main()
