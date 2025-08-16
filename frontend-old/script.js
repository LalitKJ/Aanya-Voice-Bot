// --- Session ID Management ---
function generateSessionId() {
	return "sess-" + Math.random().toString(36).substr(2, 9);
}

function getSessionId() {
	const urlParams = new URLSearchParams(window.location.search);
	let sessionId = urlParams.get("session_id");
	if (!sessionId) {
		sessionId = generateSessionId();
		urlParams.set("session_id", sessionId);
		window.history.replaceState(
			{},
			"",
			`${window.location.pathname}?${urlParams}`
		);
	}
	return sessionId;
}

const SESSION_ID = getSessionId();

async function generateAudio() {
	const text = document.getElementById("text-input").value;
	if (!text) {
		showErrorMessage("Please enter some text.");
		return;
	}

	const response = await fetch("/generate-audio", {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify({
			text: text,
			voiceId: "en-IN-alia",
			format: "mp3",
		}),
	});

	try {
		if (!response.ok) {
			const error = await response.json();
			showErrorMessage(error.detail || "Error generating audio.");
			return;
		}
		const data = await response.json();
		console.log("Murf response:", data);
		const audioUrl = data.audioFile || data.audioUrl;
		if (audioUrl) {
			const audioPlayer = document.getElementById("audio-player");
			audioPlayer.src = audioUrl;
			audioPlayer.style.display = "block";
			audioPlayer.play();
		} else {
			if (data.error) {
				showErrorMessage(data.error);
			} else {
				showErrorMessage("Audio URL not found in response.");
			}
		}
	} catch (err) {
		showErrorMessage("Error generating audio: " + (err.message || err));
	}
	// Show error message in UI
	function showErrorMessage(msg) {
		const errorDiv = document.getElementById("error-message");
		if (errorDiv) {
			errorDiv.innerHTML = `<span style='font-size:1.3em;'>❌</span> <span>${msg}</span>`;
			errorDiv.style.display = "block";
			errorDiv.style.opacity = 1;
			setTimeout(() => {
				errorDiv.style.opacity = 0.7;
			}, 2000);
			setTimeout(() => {
				errorDiv.style.display = "none";
			}, 6000);
		} else {
			alert(msg);
		}
	}
}

let mediaRecorder;
let audioChunks = [];

async function startRecording() {
	try {
		if (mediaRecorder && mediaRecorder.state === "recording") {
			stopRecording();
			return;
		}

		const recordButton = document.getElementById("record-button");
		const stream = await navigator.mediaDevices.getUserMedia({
			audio: true,
		});
		mediaRecorder = new MediaRecorder(stream);
		audioChunks = [];

		mediaRecorder.ondataavailable = (event) => {
			audioChunks.push(event.data);
		};

		mediaRecorder.onstop = () => {
			const audioBlob = new Blob(audioChunks, { type: "audio/webm" });
			const audioUrl = URL.createObjectURL(audioBlob);
			const echoAudio = document.getElementById("echo-audio");
			echoAudio.src = audioUrl;
			recordButton.innerText = "Start Recording";
			recordButton.classList.remove("stop-recording");
			echoAudio.play();
			// 1. Send the audio blob to the server (Day 5)
			// uploadAudioToServer(audioBlob);
			// 2. Send the audio and transcribe it (Day 6)
			// transcribeAudio(audioBlob);
			// 3. Synthesize the audio with Murf voice (Day 7)
			// 4. Record audio and play the llm output (Day 9)
			llmVoiceQuery(audioBlob);
			audioChunks = []; // Clear for next recording
			echoAudio.addEventListener("ended", () => {
				URL.revokeObjectURL(audioUrl); // Revoke URL object after playback has ended
			});
		};

		mediaRecorder.start();
		recordButton.innerText = "Stop Recording";
		recordButton.classList.add("stop-recording");
		console.log("Recording started...");
	} catch (error) {
		console.error("Error starting recording:", error);
	}
}

// 6. Send the recorded audio to the server to transcribe it (Day 6)
async function transcribeAudioFn(recordedBlob) {
	try {
		const data = await transcribeAudio(recordedBlob);
		document.getElementById("transcriptText").innerText = data.transcript;
	} catch (error) {
		showErrorMessage("Error transcribing audio: " + error.message);
		console.error("Transcription error:", error);
	}
}

// 7. Send the recorded audio to to murf to generate the new audio with murf voice (Day 7)
async function synthesisAudio(recordedBlob) {
	try {
		const data = await resynthesizeAudio(recordedBlob);
		const audioPlayer = document.getElementById("audio-player");
		audioPlayer.src = data.audioUrl;
		audioPlayer.style.display = "block";
		audioPlayer.play();
	} catch (error) {
		showErrorMessage("Error resynthesizing audio: " + error.message);
		console.error("Resynthesis error:", error);
	}
}

// 8. Play the llm output audio (Day 9)
// --- Chat with Agent (Day 10) ---
async function llmVoiceQuery(audio) {
	try {
		if (audio === null || audio === undefined) {
			throw new Error("No audio provided for chat query.");
		}
		const data = await agentChatQuery(audio);
		const audioUrl =
			(data.audio && (data.audio.audioFile || data.audio.audioUrl)) ||
			null;
		if (audioUrl) {
			const audioPlayer = document.getElementById("llm-output");
			if (!audioPlayer) {
				throw new Error("LLM output audio element not found.");
			}
			audioPlayer.src = audioUrl;
			audioPlayer.style.display = "block";
			audioPlayer.play();
		} else {
			if (data.error) {
				showErrorMessage(data.error);
			} else {
				showErrorMessage("No audio URL found in chat response.");
			}
		}
		if (data.history) {
			displayChatHistory(data.history);
		}
	} catch (err) {
		showErrorMessage("Error playing chat output: " + (err.message || err));
		console.error("Chat output error:", err);
	}
}

// Call /agent/chat/{session_id} endpoint
async function agentChatQuery(audio) {
	if (!audio) throw new Error("No audio provided for chat query.");
	try {
		const formData = new FormData();
		formData.append("file", audio, "recording.webm");
		const url = `http://localhost:8000/agent/chat/${SESSION_ID}`;
		const response = await fetch(url, {
			method: "POST",
			body: formData,
		});
		if (!response.ok) {
			throw new Error(`Chat query failed: ${response.statusText}`);
		}
		return await response.json();
	} catch (error) {
		throw error;
	}
}

// Optional: Display chat history in the UI
function displayChatHistory(history) {
	const chatDiv = document.getElementById("chat-history");
	if (!chatDiv) return;
	chatDiv.innerHTML = history
		.map(
			(msg) =>
				`<div class="chat-msg ${msg.role}"><span class="chat-role">${msg.role}:</span> <span class="chat-content">${msg.content}</span></div>`
		)
		.join("");
	// Show error message in UI
	function showErrorMessage(msg) {
		const errorDiv = document.getElementById("error-message");
		if (errorDiv) {
			errorDiv.innerHTML = `<span style='font-size:1.3em;'>❌</span> <span>${msg}</span>`;
			errorDiv.style.display = "block";
			errorDiv.style.opacity = 1;
			setTimeout(() => {
				errorDiv.style.opacity = 0.7;
			}, 2000);
			setTimeout(() => {
				errorDiv.style.display = "none";
			}, 6000);
		} else {
			alert(msg);
		}
	}
}

// // Helper functions //

// 1. Stop recording audio
function stopRecording() {
	try {
		if (mediaRecorder && mediaRecorder.state === "recording") {
			mediaRecorder.stop();
			console.log("Recording stopped.");
		}
	} catch (error) {
		console.error("Error stopping recording:", error);
	}
}

// 2. Upload audio blob to the server
async function uploadAudio(recordedBlob, address) {
	if (recordedBlob === null || recordedBlob === undefined) {
		throw new Error("No blob provided for audio upload.");
	}
	const formData = new FormData();
	formData.append("file", recordedBlob, "recording.mp3");
	try {
		const response = await fetch(address, {
			method: "POST",
			body: formData,
		});
		if (!response.ok) {
			throw new Error(`Upload failed: ${response.statusText}`);
		}
		return response;
	} catch (error) {
		if (error instanceof Error) {
			throw error;
		} else {
			throw new Error(`Upload failed: ${error}`);
		}
	}
}

// 3. Transcribe audio using the server endpoint
async function transcribeAudio(audio) {
	uploadAudio(audio, "http://localhost:8000/transcribe/file")
		.then((response) => response.json())
		.then((data) => {
			return {
				transcript: data.transcript,
				response: data.response,
			};
		})
		.catch((error) => {
			throw new Error("Transcription error: " + error.message);
		});
}

// 4.Resynthesize audio using Murf voice
async function resynthesizeAudio(audio) {
	uploadAudio(audio, "http://localhost:8000/tts/echo")
		.then((response) => response.json())
		.then((data) => {
			return {
				audioUrl: data.audioUrl,
				response: data.response,
			};
		})
		.catch((error) => {
			throw new Error("Resynthesis error: " + error.message);
		});
}

// 5. LLM query to play the output audio
async function llmQuery(audio) {
	if (audio === null || audio === undefined) {
		throw new Error("No audio provided for LLM query.");
	}
	try {
		const response = await uploadAudio(
			audio,
			"http://localhost:8000/llm/query"
		);
		if (!response.ok) {
			throw new Error(`LLM query failed: ${response.statusText}`);
		}
		const data = await response.json();
		if (!data || !data.audioFile) {
			throw new Error("No audio URL found in LLM response.");
		}
		return {
			audioUrl: data.audioFile,
			response: data,
		};
	} catch (error) {
		if (error instanceof Error) {
			throw error;
		} else {
			throw new Error(`LLM query error: ${error}`);
		}
	}
}

//

// // After recording stops and you have the audio blob:
// async function uploadAudioToServer(audioBlob, address) {
// 	const statusElement = document.getElementById("upload-status");
// 	if (!statusElement) {
// 		throw new Error("No #upload-status element found.");
// 	}

// 	statusElement.innerText = "Uploading...";

// 	const formData = new FormData();
// 	const filename = `recording_${Date.now()}.webm`;
// 	formData.append("file", audioBlob, filename);

// 	try {
// 		const res = await fetch("/upload-audio", {
// 			method: "POST",
// 			body: formData,
// 		});

// 		if (!res.ok) {
// 			throw new Error("Upload failed: " + res.statusText);
// 		}

// 		const data = await res.json();
// 		if (!data || !data.filename || !data.size) {
// 			throw new Error("Upload failed: No valid response from server.");
// 		}

// 		statusElement.classList.remove("error");
// 		statusElement.classList.add("success");
// 		statusElement.innerText = `✅ Uploaded`;
// 	} catch (err) {
// 		console.error(err);
// 		statusElement.classList.add("error");
// 		statusElement.classList.remove("success");
// 		statusElement.innerText = "❌ Upload failed";
// 	}
// }
