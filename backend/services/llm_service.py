from fastapi import HTTPException
import logging
import google.generativeai as genai

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