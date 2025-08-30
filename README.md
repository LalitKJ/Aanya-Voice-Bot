# Aanya: AI-Powered Voice Assistant 🤖🎤

Aanya is a sophisticated real-time voice assistant that combines cutting-edge speech recognition, natural language processing, and text-to-speech technologies. Built with a modern full-stack architecture, it provides seamless voice interactions with AI-powered conversational capabilities.

## ✨ Key Features

### 🎙️ **Real-time Voice Interaction**
- **Live Audio Streaming**: WebSocket-based real-time audio streaming for instant responses
- **Speech-to-Text (STT)**: High-accuracy transcription using AssemblyAI's streaming API
- **Text-to-Speech (TTS)**: Natural-sounding voice synthesis with Murf.ai's premium voices
- **Echo Bot Mode**: Record, transcribe, and replay functionality for testing

### 🧠 **AI-Powered Conversations**
- **Google Gemini Integration**: Advanced conversational AI with streaming responses
- **Persona System**: Configurable AI personalities (including Pirate mode!)
- **Chat History**: Persistent conversation memory within sessions
- **Streaming Responses**: Real-time text and audio generation for natural interactions

### 🎨 **Modern Frontend**
- **React + TypeScript**: Type-safe, component-based UI architecture
- **Real-time Updates**: WebSocket integration for live chat experiences
- **Responsive Design**: SCSS-based styling with glass morphism effects
- **Audio Visualization**: Dynamic wave animations during voice interactions

### 🚀 **Production-Ready Backend**
- **FastAPI Framework**: High-performance async Python backend
- **WebSocket Support**: Real-time bidirectional communication
- **Microservices Architecture**: Modular service design for STT, TTS, and LLM
- **Docker Support**: Containerized deployment with multi-stage builds

## 🏗️ Architecture Overview

```
┌─────────────────┐    WebSocket    ┌─────────────────┐
│   React Client  │ ←─────────────→ │  FastAPI Server │
│   (TypeScript)  │                 │    (Python)     │
└─────────────────┘                 └─────────────────┘
         │                                   │
         │                          ┌───────┼───────┐
         │                          │       │       │
         ▼                          ▼       ▼       ▼
┌─────────────────┐         ┌──────────┬─────────┬─────────┐
│ Audio Recording │         │   STT    │   LLM   │   TTS   │
│   & Playback    │         │ Service  │ Service │ Service │
└─────────────────┘         │(Assembly)│(Gemini) │ (Murf)  │
                            └──────────┴─────────┴─────────┘
```

## 🛠️ Technology Stack

### Backend
- **Framework**: FastAPI (Python 3.13+)
- **Speech-to-Text**: AssemblyAI Streaming API
- **Text-to-Speech**: Murf.ai API
- **Language Model**: Google Gemini (2.5-flash)
- **WebSockets**: Native FastAPI WebSocket support
- **Package Management**: uv (modern Python package manager)

### Frontend
- **Framework**: React 19 with TypeScript
- **Build Tool**: Vite 7.x
- **State Management**: TanStack React Query
- **Styling**: SCSS with modern CSS features
- **Package Management**: Yarn

### Infrastructure
- **Containerization**: Docker with multi-stage builds
- **Development**: Hot reloading for both frontend and backend
- **Static Serving**: FastAPI serves built React app

## 📋 Prerequisites

Before getting started, ensure you have the following installed:

- **Docker Desktop**: [Download here](https://www.docker.com/)
- **Node.js 18+**: For frontend development
- **Python 3.13+**: For backend development
- **API Keys**: Required for the following services:
  - [AssemblyAI API Key](https://www.assemblyai.com/)
  - [Murf.ai API Key](https://murf.ai/)
  - [Google Gemini API Key](https://ai.google.dev/)

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd Aanya-Voice-Bot
```

### 2. Environment Setup
Create a `.env` file in the root directory:
```env
# API Keys (Required)
ASSEMBLY_API_KEY=your_assemblyai_api_key_here
MURF_API_KEY=your_murf_api_key_here
GEMENAI_API_KEY=your_gemini_api_key_here

# Optional Configuration
DEFAULT_VOICE_ID=en-IN-alia
SESSION_TIMEOUT=3600
```

### 3. Docker Deployment (Recommended)
```bash
# Windows
./dev_run.bat

# Linux/macOS
docker build -t aanya-voice-bot .
docker run -p 8000:8000 --env-file .env aanya-voice-bot
```

### 4. Development Setup (Alternative)

**Backend:**
```bash
cd backend
# Install uv if not already installed
pip install uv
uv install
uv run python main.py
```

**Frontend:**
```bash
cd frontend
yarn install
yarn dev
```

### 5. Access the Application
Open your browser and navigate to:
- **Production**: http://localhost:8000
- **Development**: http://localhost:5173 (frontend) + http://localhost:8000 (backend)

## 📁 Project Structure

```
Aanya-Voice-Bot/
├── backend/                    # Python FastAPI backend
│   ├── core/                  # Core configuration
│   │   └── config.py          # Environment variables & settings
│   ├── services/              # Microservices architecture
│   │   ├── stt_service.py     # Speech-to-Text (AssemblyAI)
│   │   ├── tts_service.py     # Text-to-Speech (Murf.ai)
│   │   ├── llm_service.py     # Language Model (Gemini)
│   │   └── persona.py         # AI personality configurations
│   ├── uploads/               # Temporary audio file storage
│   ├── main.py                # FastAPI application entry point
│   ├── pyproject.toml         # Python dependencies (uv)
│   ├── Dockerfile             # Backend containerization
│   └── README.md              # Backend-specific documentation
│
├── frontend/                  # React TypeScript frontend
│   ├── src/                   # Source code
│   │   ├── pages/home/        # Main voice interface
│   │   │   ├── home.tsx       # React component
│   │   │   ├── home.ts        # Audio recording logic
│   │   │   ├── home.scss      # Styling
│   │   │   ├── audioRecorder.ts # Audio capture utilities
│   │   │   └── StreamingAudioPlayer.tsx # Audio playback
│   │   ├── App.tsx            # Root React component
│   │   └── main.tsx           # Application entry point
│   ├── dist/                  # Built static files (production)
│   ├── public/                # Static assets
│   ├── package.json           # Node.js dependencies
│   ├── tsconfig.json          # TypeScript configuration
│   ├── vite.config.ts         # Vite build configuration
│   └── yarn.lock              # Dependency lock file
│
├── .env                       # Environment variables (create this)
├── .gitignore                # Git ignore rules
├── dev_run.bat               # Development startup script (Windows)
└── README.md                 # This comprehensive documentation
```

## 🎯 Usage Guide

### Basic Voice Interaction
1. **Start the Application**: Ensure the server status shows as connected (green "Aanya" header)
2. **Begin Conversation**: Click the "Live Chat" button
3. **Speak Naturally**: The system will automatically detect when you stop speaking
4. **Listen to Response**: Aanya will respond with both text and synthesized voice
5. **Continue Chatting**: The conversation history is maintained throughout the session

### Advanced Features

#### Custom Voice Selection
The system supports multiple voice personas through the Murf.ai integration:
- `en-IN-alia` (Default): Indian English, female
- `en-US-amara`: American English, female
- Additional voices available via the `/api/voices` endpoint

#### Persona Modes
Configure different AI personalities in `backend/services/persona.py`:
- **Default**: Professional assistant
- **Pirate**: Conversational with pirate personality
- **Custom**: Define your own persona characteristics

#### WebSocket API
For developers integrating with the voice system:

```javascript
// Connect to the voice WebSocket
const ws = new WebSocket('ws://localhost:8000/api/ws/audio');

// Send audio data (binary)
ws.send(audioBuffer);

// Receive responses
ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.type === 'transcript') {
        console.log('User said:', data.text);
    } else if (data.type === 'audio') {
        // Play base64 encoded audio
        playAudioFromBase64(data.b64);
    }
};
```

## 🔧 Configuration Options

### Backend Configuration (`backend/core/config.py`)
```python
# API Configuration
ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLY_API_KEY")
MURF_API_KEY = os.getenv("MURF_API_KEY") 
GEMENAI_API_KEY = os.getenv("GEMENAI_API_KEY")

# Audio Settings
DEFAULT_SAMPLE_RATE = 16000
AUDIO_FORMAT = "wav"
MAX_AUDIO_DURATION = 300  # seconds

# LLM Configuration
DEFAULT_MODEL = "gemini-2.5-flash"
MAX_TOKENS = 8192
TEMPERATURE = 1.0
```

### Frontend Configuration (`frontend/vite.config.ts`)
```typescript
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 5173,
    proxy: {
      '/api': 'http://localhost:8000',
      '/ws': {
        target: 'ws://localhost:8000',
        ws: true
      }
    }
  }
})
```

## 🐛 Troubleshooting

### Common Issues

#### 1. API Key Errors
```
Error: No API key provided for [Service]
```
**Solution**: Verify your `.env` file contains all required API keys and restart the application.

#### 2. Audio Recording Issues
```
Error: microphone access denied
```
**Solution**: Ensure your browser has microphone permissions enabled for the application.

#### 3. WebSocket Connection Failed
```
WebSocket connection to 'ws://localhost:8000/api/ws/audio' failed
```
**Solution**: 
- Check that the backend server is running
- Verify firewall settings allow WebSocket connections
- Try refreshing the page

#### 4. Docker Build Failures
```
Error: Docker build failed at step X
```
**Solution**:
- Ensure Docker Desktop is running
- Check available disk space (>2GB recommended)
- Clear Docker cache: `docker system prune`

### Debug Mode
Enable verbose logging by setting environment variables:
```env
LOG_LEVEL=DEBUG
VERBOSE_AUDIO=true
```

### Performance Optimization
For better performance in production:
1. **Audio Quality**: Adjust sample rate in WebSocket connection
2. **Response Time**: Use faster Gemini models (gemini-1.5-flash)
3. **Memory**: Monitor chat history size for long conversations

## 🤝 Contributing

We welcome contributions! Here's how to get started:

### Development Workflow
1. **Fork the Repository**
2. **Create Feature Branch**: `git checkout -b feature/amazing-feature`
3. **Setup Development Environment**:
   ```bash
   # Backend
   cd backend && uv install
   
   # Frontend  
   cd frontend && yarn install
   ```
4. **Make Changes**: Follow the existing code style and patterns
5. **Test Thoroughly**: Ensure both voice and text interactions work
6. **Commit Changes**: `git commit -m 'Add amazing feature'`
7. **Push Branch**: `git push origin feature/amazing-feature`
8. **Create Pull Request**

### Code Style Guidelines
- **Python**: Follow PEP 8, use type hints
- **TypeScript**: Use strict mode, prefer interfaces over types
- **Commits**: Use conventional commit messages

### Testing
```bash
# Backend tests (when implemented)
cd backend && uv run pytest

# Frontend tests (when implemented)  
cd frontend && yarn test

# Integration tests
docker-compose up --build
```

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **AssemblyAI**: For providing excellent speech recognition APIs
- **Murf.ai**: For high-quality text-to-speech synthesis
- **Google Gemini**: For advanced language model capabilities
- **FastAPI**: For the robust Python web framework
- **React Team**: For the excellent frontend framework
- **Open Source Community**: For the countless libraries that make this possible

## 📊 Project Status

- ✅ **Core Features**: Complete and tested
- ✅ **Real-time Voice**: WebSocket implementation stable
- ✅ **Docker Support**: Production-ready containerization
- 🔄 **Performance**: Ongoing optimization
- 📋 **Testing**: Test suite in development
- 🌐 **Deployment**: Cloud deployment guides coming soon

## 📞 Support

For questions, issues, or contributions:

1. **GitHub Issues**: [Create an issue](../../issues)
2. **Discussions**: [Join the discussion](../../discussions)
3. **Wiki**: [Check the wiki](../../wiki) for additional documentation

---

**Made with ❤️ by the Aanya Voice Bot team**

*Empowering natural human-AI interaction through voice technology*
