// import { AudioRecorder } from "./audioRecorder";


// export async function startRecording() {
//     try {
//         const recorder = new AudioRecorder();
//         await recorder.start();
//     } catch (error) {
//         console.error("Error starting recording:", error);
//     }
// }

// async function llmVoiceQuery(audio: Blob) {
//     try {
//         if (audio === null || audio === undefined) {
//             throw new Error("No audio provided for chat query.");
//         }
//         const data = await agentChatQuery(audio);
//         const audioUrl =
//             (data.audio && (data.audio.audioFile || data.audio.audioUrl)) ||
//             null;
//         if (audioUrl) {
//             const audioPlayer = document.getElementById("llm-output");
//             if (!audioPlayer) {
//                 throw new Error("LLM output audio element not found.");
//             }
//             audioPlayer.src = audioUrl;
//             audioPlayer.style.display = "block";
//             audioPlayer.play();
//         } else {
//             if (data.error) {
//                 showErrorMessage(data.error);
//             } else {
//                 showErrorMessage("No audio URL found in chat response.");
//             }
//         }
//         if (data.history) {
//             displayChatHistory(data.history);
//         }
//     } catch (err) {
//         showErrorMessage("Error playing chat output: " + (err.message || err));
//         console.error("Chat output error:", err);
//     }
// }

// async function agentChatQuery(audio: Blob) {
//     if (!audio) throw new Error("No audio provided for chat query.");
//     try {
//         const formData = new FormData();
//         formData.append("file", audio, "recording.webm");
//         const url = `http://localhost:8000/agent/chat/${SESSION_ID}`;
//         const response = await fetch(url, {
//             method: "POST",
//             body: formData,
//         });
//         if (!response.ok) {
//             throw new Error(`Chat query failed: ${response.statusText}`);
//         }
//         return await response.json();
//     } catch (error) {
//         throw error;
//     }
// }

// function stopRecording() {
//     try {
//         if (mediaRecorder && mediaRecorder.state === "recording") {
//             mediaRecorder.stop();
//             console.log("Recording stopped.");
//         }
//     } catch (error) {
//         console.error("Error stopping recording:", error);
//     }
// }