from fastapi import FastAPI, HTTPException, File, UploadFile, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Dict
import logging
from pathlib import Path
import uvicorn
import json
import asyncio
import datetime


# Importing services
from services.stt_service import speech_to_text
from services.tts_service import text_to_murf_voice, list_voices, fallback_audio_response, stream_murf_voice
from services.llm_service import ask_gemini, stream_llm_response
from services.stt_service import AssemblyAIStreamingClient

# Global in-memory chat history store
chat_history_store = {}

def main():
    print("Hello from backend!")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

# Initialize FastAPI app
app = FastAPI()
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Mount frontend folder (relative to backend directory)
app.mount("/static", StaticFiles(directory="./frontend"), name="static")


# 1. Serve the index.html file (Day 1)
@app.get("/")
def serve_home():
    return {"message": "Hello from Backend!"}


@app.get("/hello")
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


# 15. Websocket endpoint for real-time communication (Day 15)
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    try:
        if websocket is None:
            raise ValueError("WebSocket cannot be None")
        await websocket.accept()
        # msg = await stream_murf_voice("Hello, this is a test message from the WebSocket endpoint.", "en-IN-alia", "mp3")
        # async for audio_chunk in stream_murf_voice("Hello, this is a test message from the WebSocket endpoint.", "en-IN-alia", "mp3"):
        #     await websocket.send_json({"audio_base64": audio_chunk})
        #     print("Audio chunk length:", len(audio_chunk))
        while True:
            data = await websocket.receive_text()
            if data is None:
                raise ValueError("WebSocket data cannot be None")
            await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        pass
    except Exception as e:
        logging.error(f"WebSocket error: {e}")

# 17. Websocket endpoint for real-time communication (Day 16)
@app.websocket("/ws/audio")
async def websocket_audio_endpoint(websocket: WebSocket):
    if websocket is None:
        raise ValueError("WebSocket cannot be None")
    await websocket.accept()

    UPLOADS_DIR = Path("uploads")
    UPLOADS_DIR.mkdir(exist_ok=True)
    # Create a unique file path for the streamed audio
    file_path = UPLOADS_DIR / f"streamed_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.pcm"

    # Initialize AssemblyAI client
    try:
        aaiClient = AssemblyAIStreamingClient()
    except Exception as e:
        logging.error(f"AssemblyAI client initialization error: {e}")
        await websocket.send_json({"type": "error", "message": "Failed to initialize AssemblyAI client."})
        await websocket.close(code=1006, reason="Internal Server Error")
        return

    async def send_transcriptions():
        while True:
            try:
                message = await aaiClient.transcription_queue.get()
                print("Received message from transcription queue:", message)
                if message is None:
                    logging.error("Received null message from transcription queue")
                    continue
                if message["type"] == "transcription" and message["is_final"]:
                    await websocket.send_json({
                        "type": "turn_end",
                        "transcript": message["text"]
                    })
                    print("Final transcript sent:", message["text"])
                    # Get LLM response and send back
                    msg = await stream_llm_response(message["text"])
                    print("LLM response:", msg)
                    async for audio_chunk in stream_murf_voice(msg, "mp3"):
                        await websocket.send_json({"audio_base64": audio_chunk})
                    print("🐍 File: Aanya-Voice-Bot/main.py | Line: 221 | Audio streaming complete.")
                elif message["type"] == "error":
                    await websocket.send_json({"type": "error", "message": message["message"]})
                aaiClient.transcription_queue.task_done()
            except asyncio.CancelledError:
                print("Transcription sender task cancelled")
                break
            except Exception as e:
                print("🐍 File: Aanya-Voice-Bot/main.py | Line: 226 | undefined ~ e\nError:",e)
                logging.error(f"Error sending transcription: {e}")
                break

    # Start the transcription sender task
    sender_task = asyncio.create_task(send_transcriptions())

    try:
        await websocket.send_json({
            "type": "status",
            "message": "Connected to transcription service"
        })

        with open(file_path, "wb") as f:
            while True:
                try:
                    pcm_data = await websocket.receive_bytes()
                except WebSocketDisconnect:
                    print("WebSocket disconnected")
                    break

                if not pcm_data:
                    continue
                aaiClient.stream(pcm_data)
    finally:
        # Ensure the transcription sender task is cancelled and resources are cleaned up
        sender_task.cancel()
        try:
            await sender_task
        except asyncio.CancelledError:
            pass
        # Close AssemblyAI client
        aaiClient.close()
        print("AssemblyAI client disconnected")
        # Close WebSocket connection
        try:
            await websocket.close(code=1000, reason="Normal Closure")
        except Exception as e:
            logging.error(f"Error closing WebSocket: {e}")



if __name__ == "__main__":
    main()
