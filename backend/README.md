# Aanya: Your AI-Powered Voice Assistant

Aanya is a voice-based AI assistant built using FastAPI, AssemblyAI, Murf.ai, and Google Gemini.  It allows users to record audio, transcribe it, generate speech from text using different voices, and interact with a conversational AI agent.

## Key Features

* **Audio Recording and Playback:** Record and play back your voice.
* **Speech-to-Text (STT):** Transcribe audio using AssemblyAI's powerful transcription API.
* **Text-to-Speech (TTS):** Generate speech from text using Murf.ai's high-quality voices.
* **Echo Bot:** Record audio, transcribe it, and replay the transcription using a Murf.ai voice.
* **LLM Interaction:** Send audio to Google Gemini, receive a text response, and convert it to audio using Murf.ai.
* **Conversational AI Agent:** Maintain chat history with a persistent AI agent using Google Gemini.

## Technologies Used

* **Backend:** FastAPI (Python), Uvicorn
* **STT:** AssemblyAI
* **TTS:** Murf.ai
* **LLM:** Google Gemini
* **Frontend:** HTML, CSS, JavaScript
* **Database:** In-memory storage (for chat history)
* **Containerization:** Docker


## Prerequisites

* **Docker:**  Ensure Docker Desktop is installed and running on your system.  [https://www.docker.com/](https://www.docker.com/)
* **API Keys:** You'll need API keys for Murf.ai, AssemblyAI, and Google Gemini.  Create accounts on each platform and obtain your keys.  Store them in a `.env` file in the root directory.  An example `.env.example` file is provided.  **Do not commit your actual `.env` file to version control.**
    * `MURF_API_KEY`
    * `ASSEMBLY_API_KEY`
    * `GEMENAI_API_KEY`

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   cd Aanya
   ```

2. **Create a .env file:** Rename `.env.example` to `.env` and populate it with your API keys.

3. **Build and run the Docker image:**
   ```bash
   ./run-docker-dev.bat  (Windows)
   ```
   or
   ```bash
   ./run-docker-dev.sh (Linux/macOS)
   ```

   This script builds the docker image and runs it. The backend will be accessible at `http://localhost:8000`.

4. **Access the application:** Open your web browser and go to `http://localhost:8000`.

## Usage Examples

### Echo Bot

1. Click the "Start Recording" button.
2. Speak into your microphone.
3. Click "Stop Recording".
4. Your recording will play, followed by the LLM's response generated from the transcription.

### Conversational AI Agent

1. The application will automatically generate a session ID and use it for your chat.
2. Record your message.
3. Aanya (the AI agent) will respond with an audio message.
4. Your conversation history will be displayed on the screen.


## Configuration

The application's configuration is primarily managed through environment variables in the `.env` file:

* **`MURF_API_KEY`:** Your Murf.ai API key.
* **`ASSEMBLY_API_KEY`:** Your AssemblyAI API key.
* **`GEMENAI_API_KEY`:** Your Google Gemini API key.

## Project Structure

```
Aanya/
├── backend/         # FastAPI backend code
│   ├── main.py       # Main application logic
│   └── requirements.txt # Backend dependencies
├── frontend/        # Frontend code
│   ├── index.html   # Main HTML page
│   ├── script.js    # JavaScript for user interaction
│   └── style.css    # CSS for styling
├── .dockerignore    # Files to ignore when building Docker image
├── Dockerfile       # Docker configuration
└── run-docker-dev.bat # Run script for windows (Note: run-docker-dev.sh is used for Linux and macOS)
```

## Contributing

(Add contributing guidelines if any are found in the codebase.  Currently none are specified in the provided files.)


## License

(Add license information if any is found in the codebase. Currently none is specified in the provided files.)


## Error Messages

* **"No filename provided for uploaded file." (400):**  The frontend failed to provide a filename when uploading an audio file.
* **"Failed to save file: ..." (500):** The backend encountered an error saving the uploaded file. Check server-side logs for details.
* **"Transcription failed: ..." (500):**  The AssemblyAI transcription API request failed. Check your API key and network connectivity.
* **"TTS error: ..." (500):** The Murf.ai TTS API request failed. Check your API key and network connectivity.
* **"LLM query error: ..." (500):** The Gemini LLM API request failed. Check your API key and network connectivity.
* **"No prompt provided for Ai query." (400):** No text was provided for the AI to process.
* **"No audio provided for transcription." (400):**  No audio was provided for transcription or other operations.
* **"No audio data in uploaded file." (400):**  The uploaded audio file appears to be empty.
* **"Upload failed: ..."**: An error occurred during the audio upload process. Check network connectivity and server logs.

Remember to consult the logs of the backend (if accessible) for more detailed error messages and debugging information.
