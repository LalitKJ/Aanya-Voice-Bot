from fastapi import HTTPException
import logging
import google.generativeai as genai
from google.generativeai import types

from dotenv import load_dotenv
import os

load_dotenv("../../.env")
GEMENAI_API_KEY = os.getenv("GEMENAI_API_KEY")

genai.configure(api_key=GEMENAI_API_KEY) # type: ignore

def ask_gemini(prompt: str, model_name: str = "gemini-2.5-flash"):
    if not prompt:
        raise HTTPException(status_code=400, detail="No prompt provided for Ai query.")
    try:
        model = genai.GenerativeModel(model_name) # type: ignore
        response = model.generate_content(prompt)
        return response
    except Exception as e:
        logging.error(f"Gemini query error: {e}")
        raise

# Day 19: Stream llm response to the client
async def stream_llm_response(prompt: str, model_name: str = "gemini-2.5-flash") -> str:
    if not prompt:
        raise HTTPException(status_code=400, detail="No prompt provided for Ai query.")
    try:
        model = genai.GenerativeModel(model_name) # type: ignore
        response_stream = model.generate_content(prompt, stream=True)
        if not response_stream:
            raise HTTPException(status_code=500, detail="Gemini streaming query failed.")
        full_response = ""
        for chunk in response_stream:
            if chunk and chunk.text:
                piece = chunk.text
                full_response += piece
        print("Full LLM response:", full_response)
        return full_response
    except Exception as e:
        logging.error(f"Gemini streaming query error: {e}")
        raise  

async def stream_llm_response_v2(prompt: str):
    client = genai.GenerativeModel('gemini-1.5-flash')  # type: ignore
    stream = client.generate_content(
        contents=prompt,
        stream=True,
        generation_config=types.GenerationConfig(
            candidate_count=1,
            stop_sequences=[],
            max_output_tokens=8192,
            temperature=1.0,
            top_p=0.95,
            top_k=64
        ),
    )
    for chunk in stream:
        if getattr(chunk, "text", None):
            yield chunk.text