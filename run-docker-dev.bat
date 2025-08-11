docker run -p 8000:8000 -v %cd%/backend:/app -v %cd%/frontend:/app/frontend aanya-app

@REM python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000