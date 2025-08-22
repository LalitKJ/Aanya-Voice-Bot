from fastapi import HTTPException, UploadFile
from io import BytesIO
import assemblyai as aai
import asyncio
import logging
from typing import Type
from assemblyai.streaming.v3 import (
    BeginEvent,
    StreamingClient,
    StreamingClientOptions,
    StreamingError,
    StreamingEvents,
    StreamingParameters,
    StreamingSessionParameters,
    TerminationEvent,
    TurnEvent,
)
from core.config import ASSEMBLYAI_API_KEY


# Initialize AssemblyAI client with API key
aai.settings.api_key = ASSEMBLYAI_API_KEY

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



class AssemblyAIStreamingClient:
    def __init__(self, sample_rate=16000):
        self.transcription_queue = asyncio.Queue()
        self.client = StreamingClient(
            StreamingClientOptions(
                api_key=aai.settings.api_key,
                api_host="streaming.assemblyai.com"
            )
        )
        # Bind handlers, passing ONLY event to your method
        self.client.on(StreamingEvents.Begin, lambda client, event: self.on_begin(event))
        self.client.on(StreamingEvents.Turn, lambda client, event: self.on_turn(event))
        self.client.on(StreamingEvents.Termination, lambda client, event: self.on_terminated(event))
        self.client.on(StreamingEvents.Error, lambda client, error: self.on_error(error))
        self.client.connect(StreamingParameters(
            sample_rate=sample_rate, format_turns=False
        ))

    def on_begin(self, event):
        print(f"🐍 File: services/stt_service.py | Line: 58 | __init__ ~ Transcription Session started: {event.id}")
        logging.info(f"Transcription Session started: {event.id}")

    def on_turn(self, event):
        transcript_text = event.transcript
        logging.info(f"Real-time transcript: {transcript_text}")
        # print("🐍 File: services/stt_service.py | Line: 63 | on_turn ~ transcript_text",transcript_text)
        try:
            self.transcription_queue.put_nowait({
                "type": "transcription",
                "text": transcript_text,
                "is_final": event.end_of_turn
            })
        except asyncio.QueueFull:
            logging.warning("Transcription queue is full")

        if event.end_of_turn and not event.turn_is_formatted:
            params = StreamingParameters(sample_rate=16000, format_turns=True)
            self.client.set_params(params)

    def on_terminated(self, event):
        print(f"Transcription Session terminated: {event.audio_duration_seconds} seconds processed")

    def on_error(self, error):
        logging.error(f"AssemblyAI streaming error: {error}")
        try:
            self.transcription_queue.put_nowait({
                "type": "error",
                "message": f"Transcription error: {error}"
            })
        except asyncio.QueueFull:
            logging.warning("Transcription queue is full")

    def stream(self, audio_chunk: bytes):
        self.client.stream(audio_chunk)

    def close(self):
        self.client.disconnect(terminate=True)
