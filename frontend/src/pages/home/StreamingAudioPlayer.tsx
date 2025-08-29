import { useEffect, useRef } from "react";

const AUDIO_WS_URL = "ws://localhost:8000/ws/audio";

interface AudioMessage {
    audio_base64?: string;
    [key: string]: unknown;
}

function StreamingAudioPlayer() {
    const audioContextRef = useRef<AudioContext | null>(null);

    useEffect(() => {
        if (!audioContextRef.current) {
            audioContextRef.current = new (window.AudioContext || (window as any).webkitAudioContext)();
        }
        const audioContext = audioContextRef.current;
        const ws = new WebSocket(AUDIO_WS_URL);

        ws.onmessage = async (event: MessageEvent<string>) => {
            try {
                const data: AudioMessage = JSON.parse(event.data);
                if (data.audio_base64) {
                    const audioBinary = Uint8Array.from(atob(data.audio_base64), c => c.charCodeAt(0)).buffer;
                    const audioBuffer = await audioContext.decodeAudioData(audioBinary);
                    playChunk(audioContext, audioBuffer);
                }
            } catch (err) {
                console.error("Audio chunk decode error", err);
            }
        };

        ws.onopen = () => {
            console.log("WebSocket connected!");
        };
        ws.onclose = () => {
            console.log("WebSocket disconnected.");
        };

        return () => {
            ws.close();
            // Optionally close AudioContext
            // audioContext.close();
        };
    }, []);

    function playChunk(audioContext: AudioContext, audioBuffer: AudioBuffer) {
        const source = audioContext.createBufferSource();
        source.buffer = audioBuffer;
        source.connect(audioContext.destination);
        source.start();
    }

    return (
        <div>
            <h2>Streaming Audio Player</h2>
            <p>Audio will play as chunks arrive.</p>
        </div>
    );
}

export default StreamingAudioPlayer;
