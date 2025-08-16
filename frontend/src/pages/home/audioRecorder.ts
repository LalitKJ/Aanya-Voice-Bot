
export class AudioRecorder {
    private mediaRecorder: MediaRecorder | null = null;
    private audioChunks: Blob[] = [];
    private audioBlob: Blob | null = null;
    private audioUrl: string | null = null;
    private stream: MediaStream | null = null;
    isRecording: boolean = false;

    async start() {
        try {
            this.stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        } catch (err) {
            console.error("Microphone access denied:", err);
            return;
        }
        const mimeType = MediaRecorder.isTypeSupported("audio/webm")
            ? "audio/webm"
            : "audio/mp4";
        this.mediaRecorder = new MediaRecorder(this.stream, { mimeType });
        this.audioChunks = [];

        this.mediaRecorder.ondataavailable = (event) => {
            this.audioChunks.push(event.data);
        };

        this.mediaRecorder.onstop = () => {
            this.audioBlob = new Blob(this.audioChunks, { type: this.mediaRecorder!.mimeType });
            this.mediaRecorder = null;
            // Clean up previous URL
            if (this.audioUrl) URL.revokeObjectURL(this.audioUrl);
            this.audioUrl = URL.createObjectURL(this.audioBlob);
            this.audioChunks = [];
            // Stop mic stream
            this.stream?.getTracks().forEach(track => track.stop());
            this.stream = null;
            this.isRecording = false;
        };

        this.mediaRecorder.start();
        this.isRecording = true;
    }

    stop() {
        if (this.isRecording && this.mediaRecorder) {
            this.mediaRecorder.stop();
        }
    }

    getAudioUrl(): string | null {
        return this.audioUrl;
    }

    getAudioBlob(): Blob | null {
        return this.audioBlob;
    }
}
