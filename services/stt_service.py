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






class AssemblyAIStreamingTranscriber:
    """
    Wrapper around AAI StreamingClient that exposes:
        - on_partial_callback(text) for interim results
        - on_final_callback(text)   when end_of_turn=True
    """
    def __init__(
        self,
        sample_rate: int = 16000,
        on_partial_callback=None,
        on_final_callback=None,
    ):
        self.on_partial_callback = on_partial_callback
        self.on_final_callback = on_final_callback

        self.client = StreamingClient(
            StreamingClientOptions(
                api_key=aai.settings.api_key,
                api_host="streaming.assemblyai.com",
            )
        )

        # register events
        self.client.on(StreamingEvents.Begin, lambda client, event: self._on_begin(event))
        self.client.on(StreamingEvents.Turn, lambda client, event: self._on_turn(client, event))
        self.client.on(StreamingEvents.Error, lambda client, error: self._on_error(error))
        self.client.on(StreamingEvents.Termination, lambda client, event: self._on_termination(event))

        self.client.connect(
            StreamingParameters(
                sample_rate=sample_rate,
                format_turns=False,
            )
        )

    def _on_begin(self, event: BeginEvent):
        logging.info(f"AAI session started: {event.id}")

    def _on_turn(self, client: StreamingClient, event: TurnEvent):
        text = (event.transcript or "").strip()
        if not text:
            return

        if event.end_of_turn:
            if self.on_final_callback:
                self.on_final_callback(text)

            if not event.turn_is_formatted:
                try:
                    client.set_params(StreamingSessionParameters(format_turns=True))
                except Exception as set_err:
                    print("set_params error:", set_err)
        else:
            if self.on_partial_callback:
                self.on_partial_callback(text)
    
    def _on_error(self, error: StreamingError):
        print("AAI error:", error)
    
    def _on_termination(self, event: TerminationEvent):
        print(f"AAI session terminated after {event.audio_duration_seconds} s")

    def stream_audio(self, audio_chunk: bytes):
        self.client.stream(audio_chunk)

    def close(self):
        self.client.disconnect(terminate=True)

