# Aanya Voice Bot - Backend API 🚀

The FastAPI backend powering Aanya's real-time voice interaction capabilities. This service handles speech-to-text transcription, AI conversation generation, text-to-speech synthesis, and WebSocket-based real-time communication.

## 🏗️ Architecture Overview

```
┌─────────────────────┐    WebSocket    ┌─────────────────────┐
│   Frontend Client   │ ←─────────────→ │   FastAPI Backend   │
│    (React/TS)       │                 │     (Python)        │
└─────────────────────┘                 └─────────────────────┘
                                                 │
                                        ┌────────┼────────┐
                                        │        │        │
                                        ▼        ▼        ▼
                               ┌─────────────┬─────────┬─────────┐
                               │ STT Service │   LLM   │   TTS   │
                               │(AssemblyAI) │ Service │ Service │
                               │             │(Gemini) │ (Murf)  │
                               └─────────────┴─────────┴─────────┘
```

## 🎯 Core Features

### 🎤 **Real-time Speech Processing**
- **WebSocket Audio Streaming**: Handles continuous audio chunks from frontend
- **AssemblyAI Integration**: Real-time speech-to-text with streaming transcription
- **Audio Format Support**: WAV, MP3, and other common formats

### 🤖 **AI Conversation Engine**
- **Google Gemini LLM**: Advanced conversation capabilities with streaming responses
- **Persona System**: Multiple AI personalities (Pirate, Detective, Scientist, etc.)
- **Context Management**: Maintains conversation history throughout sessions
- **Streaming Text Generation**: Real-time response generation for natural conversations

### 🔊 **Voice Synthesis**
- **Murf.ai TTS Integration**: High-quality text-to-speech conversion
- **Voice Selection**: Multiple voice options with different accents and styles
- **Audio Streaming**: Base64-encoded audio chunks for real-time playback
- **Dynamic Voice Mapping**: Persona-specific voice selection

### 🌐 **WebSocket Communication**
- **Real-time Bidirectional**: Instant audio/text exchange
- **Multiple Endpoints**: Separate endpoints for different functionalities
- **Connection Management**: Robust error handling and connection recovery

## 📁 Project Structure

```
backend/
├── core/                      # Core configuration
│   └── config.py             # Environment variables & API key validation
├── services/                  # Microservices architecture
│   ├── __init__.py           # Package initialization
│   ├── stt_service.py        # Speech-to-Text (AssemblyAI)
│   ├── tts_service.py        # Text-to-Speech (Murf.ai)  
│   ├── llm_service.py        # Language Model (Google Gemini)
│   └── persona.py            # AI personality system
├── uploads/                   # Temporary audio file storage
├── main.py                    # FastAPI application & WebSocket endpoints
├── pyproject.toml            # Python dependencies (uv package manager)
├── Dockerfile                # Container configuration
└── README.md                 # Backend documentation
```

## 🛠️ Technology Stack

### **Core Framework**
- **FastAPI 0.116+**: Modern, fast web framework with automatic API documentation
- **Python 3.13**: Latest Python with enhanced performance and typing features
- **Uvicorn**: High-performance ASGI server for production deployment

### **Package Management**
- **uv**: Ultra-fast Python package installer and resolver
- **pyproject.toml**: Modern Python project configuration

### **AI & Audio Services**
- **AssemblyAI**: Real-time speech recognition with streaming capabilities
- **Google Gemini**: Advanced language model (gemini-2.5-flash & gemini-1.5-flash)
- **Murf.ai**: Premium text-to-speech with natural-sounding voices

### **Communication**
- **WebSockets**: Real-time bidirectional communication
- **HTTPX**: Async HTTP client for external API calls
- **JSON Streaming**: Efficient data serialization for real-time responses

## ⚙️ Configuration

### Environment Variables
Create a `.env` file in the project root:

```env
# Required API Keys
ASSEMBLYAI_API_KEY=your_assemblyai_api_key_here
MURF_API_KEY=your_murf_api_key_here  
GEMINI_API_KEY=your_gemini_api_key_here

# Optional Configuration
DEFAULT_VOICE_ID=en-IN-alia
LOG_LEVEL=INFO
MAX_AUDIO_DURATION=300
SESSION_TIMEOUT=3600
```

### Configuration Validation
The `core/config.py` module provides:
- **Automatic validation** of required environment variables
- **Fail-fast behavior** if API keys are missing
- **Project root detection** for file path resolution

```python
# Environment validation happens at import time
from core.config import GEMINI_API_KEY, MURF_API_KEY, ASSEMBLYAI_API_KEY
```

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- API keys for AssemblyAI, Murf.ai, and Google Gemini
- UV package manager (or pip as fallback)

### Installation

#### Option 1: Using UV (Recommended)
```bash
# Install uv if not already installed
pip install uv

# Install dependencies
uv install

# Run development server
uv run python main.py
```

#### Option 2: Using Docker
```bash
# Build container
docker build -t aanya-backend .

# Run container with environment file
docker run -p 8000:8000 --env-file ../.env aanya-backend
```

#### Option 3: Manual Setup
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt  # Generate if needed: uv export > requirements.txt

# Run server
python main.py
```

### Development Server
The server will start at:
- **API Endpoints**: http://localhost:8000/api/
- **WebSocket**: ws://localhost:8000/api/ws/audio
- **API Documentation**: http://localhost:8000/docs (Swagger UI)
- **Alternative Docs**: http://localhost:8000/redoc

## 📡 API Endpoints

### REST Endpoints

#### Health Check
```http
GET /api/check-status
```
Returns server health status and connection verification.

#### Voice Management
```http
GET /api/voices
```
Retrieves available TTS voices from Murf.ai API.

### WebSocket Endpoints

#### Real-time Audio Processing
```http
WebSocket: /api/ws/audio
```

**Connection Flow:**
1. Client connects to WebSocket
2. Client sends binary audio chunks
3. Server streams transcription in real-time
4. Server generates AI response with selected persona
5. Server streams back synthesized audio chunks

**Message Types:**
```javascript
// Incoming from client
WebSocket.send(audioBuffer)  // Binary audio data

// Outgoing to client
{
  "type": "transcript",
  "user": "user", 
  "text": "transcribed speech"
}

{
  "type": "llm-response",
  "user": "bot",
  "text": "AI generated response"
}

{
  "type": "audio", 
  "b64": "base64_encoded_audio_data"
}
```

#### Simple WebSocket Testing
```http
WebSocket: /api/ws
```
Basic text echo WebSocket for testing connections.

## 🎭 Persona System

The backend supports multiple AI personalities through the `PersonaType` enum:

### Available Personas
- **DEFAULT**: Standard helpful assistant
- **PIRATE**: Nautical-themed responses with pirate lingo
- **COWBOY**: Wild West charm with Southern drawl
- **ROBOT**: Precise, logical, mechanical responses  
- **SHAKESPEARE**: Poetic, old English style
- **DETECTIVE**: Analytical, mystery-solving approach
- **SCIENTIST**: Technical, research-based answers
- **CHILD**: Curious, cheerful, simple language

### Persona Configuration
```python
from services.persona import PersonaType, build_persona

# Build persona with chat history
persona_data = build_persona(chat_history, PersonaType.PIRATE)
prompt = persona_data["prompt"]      # LLM prompt with personality
voice_id = persona_data["voiceId"]   # Matching TTS voice
```

### Custom Persona Creation
Add new personas to `services/persona.py`:

```python
CUSTOM_PERSONA = {
    "voiceId": "en-US-voice-id",
    "prompt": "You are Aanya, a [personality description]...",
    "skills": ["Skill descriptions..."]
}
```

## 🔧 Service Architecture

### STT Service (`services/stt_service.py`)
- **AssemblyAI Streaming**: Real-time transcription with turn detection
- **Audio Processing**: Handles multiple audio formats
- **Error Handling**: Graceful fallback for transcription failures

```python
# Usage example
transcriber = AssemblyAIStreamingTranscriber(
    on_final_callback=process_final_transcript
)
transcriber.stream_audio(audio_chunk)
```

### LLM Service (`services/llm_service.py`)
- **Streaming Responses**: Real-time text generation
- **Model Selection**: Multiple Gemini models supported
- **Context Management**: Conversation history integration

```python
# Streaming LLM response
async for chunk in stream_llm_response_v2(prompt):
    if chunk:
        await process_text_chunk(chunk)
```

### TTS Service (`services/tts_service.py`)
- **Voice Synthesis**: High-quality audio generation
- **Streaming Audio**: Real-time audio chunk delivery
- **Voice Management**: Multiple voice options

```python
# Generate audio
audio_bytes = speak("Hello world", voice_id="en-IN-alia")
```

## 🔄 Real-time Pipeline

The core real-time processing pipeline in `main.py`:

```python
async def llm_tts_pipeline(session_id: str, text: str, websocket: WebSocket):
    # 1. Add user message to history
    # 2. Build persona prompt with history
    # 3. Stream LLM response in chunks
    # 4. Convert text chunks to audio
    # 5. Send audio to client in real-time
```

This pipeline ensures minimal latency between user speech and AI response.

## 🐛 Debugging & Logging

### Enable Debug Mode
```env
LOG_LEVEL=DEBUG
VERBOSE_AUDIO=true
```

### Common Debug Points
- **API Key Validation**: Check `core/config.py` imports
- **WebSocket Connections**: Monitor connection/disconnection events
- **Audio Streaming**: Verify binary data transmission
- **Service Integration**: Test individual service endpoints

### Logging Output
```python
import logging
logging.basicConfig(level=logging.INFO)

# Service-specific logging
logging.info("WebSocket client connected")
logging.error(f"TTS Error: {error}")
```

## 🧪 Testing

### Manual Testing
```bash
# Test individual services
python -c "from services.stt_service import speech_to_text; print('STT Service OK')"
python -c "from services.tts_service import speak; print('TTS Service OK')"
python -c "from services.llm_service import ask_gemini; print('LLM Service OK')"
```

### WebSocket Testing
Use tools like `wscat` or browser WebSocket clients:
```bash
# Install wscat
npm install -g wscat

# Test WebSocket connection  
wscat -c ws://localhost:8000/api/ws
```

### Load Testing
For production deployment, test with multiple concurrent connections:
```python
import asyncio
import websockets

async def test_concurrent_connections():
    # Test multiple WebSocket connections
    pass
```

## 📦 Dependencies

### Core Dependencies (pyproject.toml)
```toml
[project]
dependencies = [
    "fastapi>=0.116.1",           # Web framework
    "uvicorn>=0.35.0",            # ASGI server
    "websockets>=15.0.1",         # WebSocket support
    "assemblyai>=0.43.1",         # Speech-to-text
    "google-generativeai>=0.8.5", # LLM integration
    "murf>=2.0.2",                # Text-to-speech
    "httpx>=0.28.1",              # Async HTTP client
    "python-dotenv>=1.1.1",       # Environment management
    "python-multipart>=0.0.20",   # File upload support
]
```

### Development Dependencies
```bash
# Add development tools
uv add --dev pytest pytest-asyncio black isort mypy
```

## 🚀 Deployment

### Production Deployment
```bash
# Build production image
docker build -t aanya-backend:latest .

# Run with production configuration
docker run -d \
  --name aanya-backend \
  -p 8000:8000 \
  --env-file .env.production \
  --restart unless-stopped \
  aanya-backend:latest
```

### Environment-specific Configuration
```env
# .env.production
LOG_LEVEL=WARNING
MAX_CONNECTIONS=100
WORKER_COUNT=4
```

### Health Monitoring
The backend exposes health endpoints for monitoring:
- `/api/check-status` - Basic health check
- `/health` - Detailed service status (if implemented)

## 🔒 Security Considerations

### API Key Management
- Store API keys in environment variables, never in code
- Use different keys for development/staging/production
- Rotate keys regularly

### WebSocket Security  
- Implement rate limiting for WebSocket connections
- Validate audio data before processing
- Monitor for unusual connection patterns

### Data Privacy
- Audio data is processed in memory and not permanently stored
- Chat history is session-based and temporary
- No user data is logged in production

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/backend-enhancement`
3. Install dependencies: `uv install`
4. Make changes following the existing code style
5. Test thoroughly with all API services
6. Submit a pull request

### Code Style
- Follow PEP 8 Python style guidelines
- Use type hints for all function parameters and returns
- Add docstrings for public functions and classes
- Keep functions focused and modular

### Adding New Services
1. Create service file in `services/` directory
2. Implement consistent async/await patterns
3. Add proper error handling and logging
4. Update main.py with new endpoints if needed
5. Document API changes

---

**Backend Status**: ✅ Production Ready

This backend provides a robust, scalable foundation for real-time voice AI interactions with professional-grade error handling, comprehensive logging, and modular architecture.
