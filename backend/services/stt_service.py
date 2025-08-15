from fastapi import HTTPException, UploadFile
from io import BytesIO
import assemblyai as aai
from dotenv import load_dotenv
import os

load_dotenv("../../.env")

ASSEMBLY_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")

async def speech_to_text(file: UploadFile):
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
