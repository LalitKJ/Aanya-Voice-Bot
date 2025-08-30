# Aanya Voice Bot - Frontend

A modern React-based web interface for the Aanya Voice Bot, featuring real-time voice interaction capabilities with WebSocket communication and audio streaming.

## 🚀 Features

- **Real-time Voice Chat**: Interactive voice communication with the AI assistant
- **WebSocket Integration**: Live connection with backend services
- **Audio Recording & Playback**: Built-in audio recording and streaming capabilities
- **Responsive UI**: Modern glassmorphism design with visual feedback
- **Connection Status**: Real-time server connection monitoring
- **Chat History**: Persistent conversation display with user and bot messages

## 🛠 Tech Stack

- **Framework**: React 19.1.1 with TypeScript
- **Build Tool**: Vite 7.1.2
- **Styling**: SCSS with modern CSS features
- **State Management**: React Hooks + TanStack Query
- **Real-time Communication**: WebSocket API
- **Development**: ESLint + TypeScript for code quality

## 📋 Prerequisites

- Node.js (see `.node-version` for specific version)
- Yarn package manager
- Backend server running on port 8000 (configurable)

## 🔧 Installation

1. **Clone and navigate to the frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   yarn install
   ```

3. **Set up environment variables**:
   - Copy `.env.development` and modify if needed
   - Default backend URL: `http://localhost:8000`

## 🚀 Development

### Start Development Server
```bash
yarn dev
```
The application will be available at `http://localhost:5173` with the development server running on all network interfaces (`0.0.0.0`).

### Build for Production
```bash
yarn build
```

### Preview Production Build
```bash
yarn preview
```

### Lint Code
```bash
yarn lint
```

## 📁 Project Structure

```
frontend/
├── public/                 # Static assets
├── src/
│   ├── pages/
│   │   └── home/          # Main chat interface
│   │       ├── home.tsx   # Home page component
│   │       ├── home.ts    # Audio recording logic
│   │       └── StreamingAudioPlayer.tsx
│   ├── App.tsx            # Main app component
│   ├── App.scss           # Global styles
│   └── main.tsx           # Application entry point
├── dist/                  # Built application
├── package.json           # Dependencies and scripts
└── vite.config.ts         # Vite configuration
```

## 🔌 API Integration

The frontend communicates with the backend through:

### HTTP Endpoints
- `GET /api/check-status` - Server health check (polled every 90 seconds)

### WebSocket Connection
- `ws://localhost:8000/api/ws` - Real-time communication channel
- Automatic protocol detection (ws/wss based on page protocol)

## 🎨 UI Components

### Main Interface (`Home`)
- **Connection Status**: Visual indicator of backend connectivity
- **Live Chat Button**: Initiates voice recording and chat
- **Chat History**: Displays conversation between user and AI
- **Audio Feedback**: Visual wave animation during listening state

### Key Features
- **Glassmorphism Design**: Modern translucent UI elements
- **Responsive Layout**: Adapts to different screen sizes
- **Real-time Updates**: Live chat history updates via WebSocket
- **Audio Recording**: Browser-based microphone access and recording

## ⚙️ Configuration

### Environment Variables
- `VITE_SERVER_URL`: Backend server URL (default: `http://localhost:8000`)

### Vite Configuration
- **Proxy Setup**: `/api` routes are proxied to the backend server
- **WebSocket Support**: Enabled for real-time communication
- **Hot Reload**: Development server with fast refresh

## 🐳 Docker Support

The project includes Docker configuration:
- `Dockerfile` for containerized deployment
- `.dockerignore` for optimized builds

## 📝 Development Notes

### TypeScript Configuration
- `tsconfig.json` - Base TypeScript configuration
- `tsconfig.app.json` - Application-specific settings
- `tsconfig.node.json` - Node.js environment settings

### Code Quality
- ESLint with React hooks and refresh plugins
- TypeScript strict mode enabled
- Modern ES modules support

## 🔊 Audio Features

The application includes sophisticated audio handling:
- **Real-time Recording**: Browser microphone access
- **Streaming Playback**: Audio response streaming from backend
- **Visual Feedback**: Wave animation during voice interaction
- **Connection Management**: Automatic WebSocket reconnection

## 🚨 Troubleshooting

### Common Issues

1. **Backend Connection Failed**:
   - Ensure backend server is running on port 8000
   - Check `VITE_SERVER_URL` environment variable
   - Verify CORS settings on backend

2. **Audio Not Working**:
   - Check browser microphone permissions
   - Ensure HTTPS for production (required for microphone access)
   - Verify WebSocket connection is established

3. **Build Errors**:
   - Clear `node_modules` and reinstall: `rm -rf node_modules yarn.lock && yarn install`
   - Check Node.js version matches `.node-version`

## 📄 License

This project is part of the Aanya Voice Bot system. Please refer to the main project license.

## 🤝 Contributing

1. Follow the existing code style and TypeScript conventions
2. Test audio functionality across different browsers
3. Ensure responsive design works on mobile devices
4. Update this README when adding new features

---

**Note**: This frontend requires the Aanya Voice Bot backend to be running for full functionality. Make sure to start the backend server before running the frontend application.
