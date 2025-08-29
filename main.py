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
import base64

# Importing services
import services.llm_service as llm
import services.tts_service as tts
import services.stt_service as stt
import services.persona as persona

# Global in-memory chat history store
# chat_history_store = {}
chat_history_store: Dict[str, List[Dict]] = {}

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



# 2. Generate voice from text using Murf API and send audio link (Day 2)
@app.get("/voices")
async def get_voices():
    try:
        res = await tts.list_voices()
        return res.json()
    except Exception as e:
        logging.error(f"Error fetching voices: {e}")
        return JSONResponse(content={"error": "Unable to fetch voices."}, status_code=500)

    history: List[Dict] = chat_history_store.get(session_id, [])
    try:
        transcript = await stt.speech_to_text(file)
        history.append({"role": "User", "content": transcript})
        prompt = "\n".join([
            ("User: " + msg["content"] if msg["role"] == "User" else "Aanya: " + msg["content"])
            for msg in history
        ])
        prompt += "\nPlease answer the question in a concise manner and less than 2800 characters. Also keep formatting easy, do not answer in points, keep it all in a simple paragraph so that I can convert it into audio using Murf Ai."
        aiResponse = llm.ask_gemini(prompt)
        res = aiResponse.text[:2999]
        history.append({"role": "Aanya", "content": res})
        chat_history_store[session_id] = history
        response = await tts.text_to_murf_voice(res)
        return {"audio": response.json(), "history": history}
    except Exception as e:
        logging.error(f"Agent chat error: {e}")
        return await tts.fallback_audio_response()


# 3. Websocket endpoint for real-time communication (Day 15)
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    try:
        if websocket is None:
            raise ValueError("WebSocket cannot be None")
        await websocket.accept()
        # msg = await llm.stream_murf_voice("Hello, this is a test message from the WebSocket endpoint.", "en-IN-alia", "mp3")
        # async for audio_chunk in llm.stream_murf_voice("Hello, this is a test message from the WebSocket endpoint.", "en-IN-alia", "mp3"):
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


# 4. Websocket endpoint for real-time communication (Day 16)
async def llm_tts_pipeline(session_id: str, text: str, websocket: WebSocket):
    await websocket.send_json({"type": "transcript", "user": "user", "text": text})
    tts_queue = asyncio.Queue()
    # Append user message to chat history
    history = chat_history_store.get(session_id, [])
    history.append({"role": "User", "content": text})
    persona_data = persona.build_persona(history, persona.PersonaType.PIRATE)

    # Task to stream LLM text and push it to the TTS queue
    async def llm_worker():
        try:
            # Construct prompt with chat history for Gemini LLM

            # Query Gemini LLM with streaming (v2 for chunked response)
            full_response = ""
            async for chunk in llm.stream_llm_response_v2(persona_data["prompt"]):
                if chunk:
                    await tts_queue.put(chunk)
                    full_response  += chunk
            # After LLM response complete, store it in chat history
            print("Full LLM response:", full_response)
            await websocket.send_json({"type": "llm-response", "user": "bot", "text": full_response})
            history.append({"role": "Aanya", "content": full_response})
            chat_history_store[session_id] = history
        finally:
            await tts_queue.put(None)  # Signal that LLM is done
    # Task to get text from queue and synthesize audio
    async def tts_worker():
        while True:
            chunk = await tts_queue.get()
            if chunk is None:
                break
            try:
                audio_bytes = tts.speak(chunk, persona_data["voiceId"])
                if audio_bytes:
                    b64_audio = base64.b64encode(audio_bytes).decode('utf-8')
                    await websocket.send_json({"type": "audio", "b64": b64_audio})
            except Exception as e:
                logging.error(f"TTS Error: {e}")
            finally:
                tts_queue.task_done()
    # Start and manage tasks
    await asyncio.gather(
        asyncio.create_task(llm_worker()),
        asyncio.create_task(tts_worker())
    )

@app.websocket("/ws/audio")
async def websocket_audio_endpoint(websocket: WebSocket):
    """Handles WebSocket connection for real-time transcription and voice response."""
    await websocket.accept()
    logging.info("WebSocket client connected.")
    # Get the current asyncio event loop
    loop = asyncio.get_event_loop()
    session_id = "default_session"
    # Callback function for when final transcription is received
    def on_final_transcript(text: str):
        print(f"Query: {text}")
        # Use run_coroutine_threadsafe to schedule the coroutine from the callback thread
        asyncio.run_coroutine_threadsafe(
            llm_tts_pipeline(session_id, text, websocket), loop
        )
    
    # Initialize the streaming transcriber
    transcriber = stt.AssemblyAIStreamingTranscriber(on_final_callback=on_final_transcript)
    try:
        while True:
            data = await websocket.receive_bytes()
            transcriber.stream_audio(data)
    except Exception as e:
        logging.info(f"WebSocket connection closed: {e}")
    finally:
        transcriber.close()
        logging.info("Transcription resources released.")



if __name__ == "__main__":
    main()
