// @ts-nocheck

// Day 17: Send audio data to the server via WebSocket
let audioWebSocket;
function connectAudioWebSocket() {
    const protocol = window.location.protocol === "https:" ? "wss" : "ws";
    const wsUrl = `${protocol}://${window.location.host}/api/ws/audio`;
    if (!wsUrl) {
        console.error("Invalid WebSocket URL:", wsUrl);
        return null;
    }
    const audioWebSocket = new WebSocket(wsUrl);

    audioWebSocket.binaryType = "arraybuffer";
    audioWebSocket.onopen = () => { console.log("WS: Connected."); };
    audioWebSocket.onclose = () => {
        stopRecording();
        console.log("WS: Closed.");
    };
    audioWebSocket.onerror = (err) => {
        if (!err) {
            console.error("Invalid WebSocket error:", err);
            return;
        }
        console.error("WS Error", err);
    };

    audioWebSocket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.type === "error") {
            alert("Transcription error: " + data.message);
        } else if (data.type === "audio") {
            console.log("Received audio chunk:", data.b64.length);
            playAudioChunk(data.b64);
        }
    };

    return audioWebSocket;
}

function displayTranscript(transcript) {
    const transcriptDiv = document.getElementById('transcript');
    transcriptDiv.innerText = transcript || '';
}

function floatTo16BitPCM(float32Array) {
    const buffer = new ArrayBuffer(float32Array.length * 2);
    const view = new DataView(buffer);
    let offset = 0;
    for (let i = 0; i < float32Array.length; i++, offset += 2) {
        let s = Math.max(-1, Math.min(1, float32Array[i]));
        view.setInt16(offset, s < 0 ? s * 0x8000 : s * 0x7fff, true);
    }
    return buffer;
}


let audioContext;
let inputStream;
let scriptProcessor;
let audioSource;
let isRecording = false;
export async function startRecording() {
    // If already recording, stop recording
    if (isRecording) {
        stopRecording();
        return;
    }

    const recordButton = document.getElementById("record-button");

    recordButton.classList.add("stop-recording");
    recordButton.innerText = "Connecting...";

    try {
        isRecording = true;
        audioWebSocket = connectAudioWebSocket();
        audioContext = new (window.AudioContext || window.webkitAudioContext)({ sampleRate: 16000 });
        inputStream = await navigator.mediaDevices.getUserMedia({ audio: true, channelCount: 1 });
        audioSource = audioContext.createMediaStreamSource(inputStream);
        scriptProcessor = audioContext.createScriptProcessor(4096, 1, 1);

        scriptProcessor.onaudioprocess = (e) => {
            if (!isRecording) return;
            const inputData = e.inputBuffer.getChannelData(0);
            const pcm16 = floatTo16BitPCM(inputData);
            if (audioWebSocket && audioWebSocket.readyState === WebSocket.OPEN) {
                setTimeout(() => console.clear(), 1000);
                console.count("Sending audio data to server...", pcm16);
                audioWebSocket.send(pcm16);
            }
        };

        audioSource.connect(scriptProcessor);
        scriptProcessor.connect(audioContext.destination);

        recordButton.innerText = "Stop Recording";
        console.log("Recording started...");
    } catch (err) {
        console.error("Error starting recording:", err);
    }
}

export function stopRecording() {
    isRecording = false;
    const recordButton = document.getElementById("record-button");

    if (scriptProcessor) {
        scriptProcessor.disconnect();
        scriptProcessor.onaudioprocess = null;
        scriptProcessor = null;
    }
    if (audioSource) {
        audioSource.disconnect();
        audioSource.onaudioprocess = null;
        audioSource = null;
    }
    if (audioContext) {
        audioContext.close();
        audioContext = null;
    }
    if (inputStream) {
        inputStream.getTracks().forEach(track => track.stop());
        inputStream = null;
    }
    if (audioWebSocket && audioWebSocket.readyState === WebSocket.OPEN) {
        audioWebSocket.close();
    }
    recordButton.innerText = "Start Recording";
    recordButton.classList.remove("stop-recording");
    console.log("Recording stopped.");
}

// Audio playback state
const playbackAudioContext = new (window.AudioContext || window.webkitAudioContext)();
let scheduledTime = playbackAudioContext.currentTime;

// Play incoming base64 audio chunks seamlessly
function playAudioChunk(base64Audio) {
    // Decode base64 to ArrayBuffer
    const audioBinary = Uint8Array.from(atob(base64Audio), c => c.charCodeAt(0)).buffer;
    playbackAudioContext.decodeAudioData(audioBinary).then(decodedBuffer => {
        const source = playbackAudioContext.createBufferSource();
        source.buffer = decodedBuffer;
        source.connect(playbackAudioContext.destination);

        // Schedule playback to avoid gaps
        const now = playbackAudioContext.currentTime;
        const startTime = Math.max(scheduledTime, now + 0.05); // 50ms delay buffer
        source.start(startTime);
        scheduledTime = startTime + decodedBuffer.duration;
    }).catch(err => {
        console.error("Error decoding audio chunk", err);
    });
}