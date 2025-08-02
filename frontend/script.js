window.addEventListener("DOMContentLoaded", () => {
	fetch("/api/hello")
		.then((response) => response.json())
		.then((data) => {
			document.getElementById("message").textContent = data.message;
		})
		.catch((err) => {
			document.getElementById("message").textContent =
				"Failed to load message.";
		});
});
