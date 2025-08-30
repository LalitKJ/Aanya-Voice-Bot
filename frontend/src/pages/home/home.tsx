// @ts-nocheck
import './home.scss'
import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'

import { startRecording } from "./home"

export interface ChatMessage {
    user: string;
    message: string;
}

export interface LiveChat {
    active: boolean;
    listening: boolean;
    chatHistory: ChatMessage[];
}

function Home() {
    const [serverOnline, setServerOnline] = useState<boolean>(false);
    const [liveChat, setLiveChat] = useState<LiveChat>({
        active: false,
        listening: false,
        chatHistory: []
    });


    function record() {
        function updateChats(data: ChatMessage) {
            console.log("Before", liveChat);
            const updatedChatHistory = liveChat.chatHistory;
            console.log("updatedChatHistory", updatedChatHistory);
            updatedChatHistory.push(data);
            setLiveChat({
                ...liveChat,
                chatHistory: updatedChatHistory
            });
            console.log("After", liveChat);
        }
        startRecording(updateChats);
    }

    useQuery({
        queryKey: ['server-connection'],
        queryFn: async () => {
            const res = await fetch('/api/');
            setServerOnline(res.status === 200);
            return res;
        },
        refetchInterval: 90000,
    });

    return (
        <div id='voice-bot'>
            <div className="message glass">
                <h1 className={serverOnline ? 'connection-success' : 'connection-error'} id='aanya'>Aanya</h1>
                <button
                    className='font-inconsolata'
                    id="toggle-live-chat"
                    disabled={!serverOnline}
                    onClick={record}
                >
                    {liveChat.active
                        ? <>
                            {liveChat.listening ? 'Listening...' : 'Live Chat'}
                            <div className="wave-line" data-listening={liveChat.listening}></div>
                        </>
                        : 'Live Chat'
                    }
                </button>
            </div>
            <div className="llm-history font-inconsolata" data-server-online={serverOnline}>
                {liveChat.chatHistory.length === 0
                    ? <div className="no-history">Start New Chat</div>
                    : liveChat.chatHistory.map((msg, index) => (
                        <div className={"chat" + (msg.user === 'bot' ? ' bot-chat' : ' user-chat')} key={msg.message}>
                            <p className="chat">{msg.message}</p>
                        </div>
                    ))
                }
            </div>
        </div>
    )
}

export default Home

{/* <div className="voice-transcript glass">
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
</div> */}