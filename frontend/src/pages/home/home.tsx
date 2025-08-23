import './home.scss'
import { useEffect, useState } from 'react'
import { useQuery } from '@tanstack/react-query'

import { startRecording } from "./home"

function Home() {
    const [serverOnline, setServerOnline] = useState<boolean>(false);
    const { data } = useQuery({
        queryKey: ['server-connection'],
        queryFn: async () => {
            const res = await fetch('/api/');
            const json = await res.json();
            return json;
        },
        refetchInterval: 90000, // Refetch every second

    });
    useEffect(() => {
        const statusElement = document.getElementById('aanya');
        if (data) {
            setServerOnline(true);
            statusElement?.style.setProperty('color', 'green');
        } else {
            setServerOnline(false);
            statusElement?.style.setProperty('color', 'red');
        }
    }, [data])

    return (
        <>
            <div className="message glass">
                <h3 className="message silkscreen-bold">Hello from our brand new Ai Agent</h3>
                <h4 className="name" id='aanya'>~Aanya</h4>
            </div>
            <div className="content">
                <div className="voice-transcript glass">
                    <h1>Echo Bot</h1>
                    <div className="record-audio">
                        <audio id="echo-audio" controls></audio>
                        <div className="controls">
                            <button
                                id="record-button"
                                className="start-recording"
                                onClick={startRecording}
                                disabled={!serverOnline}
                            >Start Recording</button>
                            <p id="upload-status"></p>
                        </div>
                        <div id="error-message" className="error-message" style={{ display: 'none' }}></div>
                        <audio id="llm-output" controls></audio>
                    </div>
                    <div id="chat-history" className="chat-history glass" style={{ marginTop: '1em', maxHeight: '300px', overflowY: 'auto', padding: '1em', borderRadius: '8px', background: '#f8f8ff' }} >
                        <div id="transcript"></div>
                    </div>
                </div>
            </div>
        </>
    )
}

export default Home
