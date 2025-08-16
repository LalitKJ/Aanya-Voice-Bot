import './home.scss'

function Home() {
    return (
        <>
            <div className="message glass">
                <h3 className="message silkscreen-bold">Hello from our brand new Ai Agent</h3>
                <h4 className="name">~Aanya</h4>
            </div>
            <div className="content">
                {/* <!-- <div className="text-to-speech glass">
          <textarea type="text" id="text-input" placeholder="Type something..." size="40" ></textarea>
          <button onclick="generateAudio()">Generate Audio</button>
          <audio id="audio-player" controls></audio>
        </div> --> */}
                <div className="voice-transcript glass">
                    <h1>Echo Bot</h1>
                    <div className="record-audio">
                        <audio id="echo-audio" controls></audio>
                        <div className="controls">
                            <button
                                id="record-button"
                                className="start-recording"
                            // onClick={startRecording}
                            >Start Recording</button>
                            <p id="upload-status"></p>
                        </div>
                        <div id="error-message" className="error-message" style={{ display: 'none' }}></div>
                        <audio id="llm-output" controls></audio>
                    </div>
                    <div id="chat-history" className="chat-history glass" style={{ marginTop: '1em', maxHeight: '300px', overflowY: 'auto', padding: '1em', borderRadius: '8px', background: '#f8f8ff' }} ></div>
                </div>
            </div>
        </>
    )
}

export default Home
