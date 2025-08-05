// window.addEventListener("DOMContentLoaded", () => {
// 	fetch("/api/hello")
// 		.then((response) => response.json())
// 		.then((data) => {
// 			document.getElementById("message").textContent = data.message;
// 		})
// 		.catch((err) => {
// 			document.getElementById("message").textContent =
// 				"Failed to load message.";
// 		});
// });

async function generateAudio() {
	const text = document.getElementById("text-input").value;
	if (!text) {
		alert("Please enter some text.");
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

	if (!response.ok) {
		const error = await response.json();
		alert("Error: " + error.detail);
		return;
	}

	const data = await response.json();
	console.log("Murf response:", data);

	const audioUrl = data.audioFile;
	console.log("File: ", audioUrl);

	if (audioUrl) {
		const audioPlayer = document.getElementById("audio-player");
		audioPlayer.src = audioUrl;
		audioPlayer.style.display = "block";
		audioPlayer.play();
	} else {
		alert("Audio URL not found in response.");
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
