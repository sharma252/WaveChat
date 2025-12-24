import { useState, useEffect, useRef } from 'react'
import './App.css'

function App() {
    const [messages, setMessages] = useState([])
    const [input, setInput] = useState('')
    const [username, setUsername] = useState('')
    const [connected, setConnected] = useState(false)
    const ws = useRef(null)

    const clientId = useRef(Math.random().toString(36).substring(7))

    useEffect(() => {
        // Fetch chat history
        fetch('/api/messages')
            .then(res => res.json())
            .then(data => setMessages(data))
            .catch(err => console.error("Failed to fetch messages:", err))

        // Setup WebSocket
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const host = window.location.host;
        ws.current = new WebSocket(`${protocol}//${host}/ws/${clientId.current}`)

        ws.current.onopen = () => {
            console.log("Connected to WebSocket")
            setConnected(true)
        }

        ws.current.onmessage = (event) => {
            const message = JSON.parse(event.data)
            setMessages((prev) => [...prev, message])
        }

        ws.current.onclose = () => {
            console.log("Disconnected from WebSocket")
            setConnected(false)
        }

        return () => {
            if (ws.current) {
                ws.current.close()
            }
        }
    }, [])

    const sendMessage = (e) => {
        e.preventDefault()
        if (input && username && connected) {
            const messageData = {
                username: username,
                content: input
            }
            ws.current.send(JSON.stringify(messageData))
            setInput('')
        }
    }

    return (
        <div className="container mt-5">
            <div className="card">
                <div className="card-header bg-primary text-white">
                    <h3 className="mb-0">WaveChat</h3>
                </div>
                <div className="card-body chat-box" style={{ height: '400px', overflowY: 'auto' }}>
                    {messages.map((msg, idx) => (
                        <div key={idx} className={`mb-2 ${msg.username === username ? 'text-end' : ''}`}>
                            <div className={`d-inline-block p-2 rounded ${msg.username === username ? 'bg-success text-white' : 'bg-light'}`}>
                                <strong>{msg.username}: </strong> {msg.content}
                                <br />
                                <small style={{ fontSize: '0.7rem', opacity: 0.8 }}>
                                    {new Date(msg.timestamp).toLocaleTimeString()}
                                </small>
                            </div>
                        </div>
                    ))}
                </div>
                <div className="card-footer">
                    {!username && (
                        <div className="mb-3">
                            <input
                                type="text"
                                className="form-control"
                                placeholder="Enter your username to chat..."
                                onChange={(e) => setUsername(e.target.value)}
                            />
                        </div>
                    )}
                    <form onSubmit={sendMessage} className="input-group">
                        <input
                            type="text"
                            className="form-control"
                            placeholder="Type a message..."
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            disabled={!username || !connected}
                        />
                        <button className="btn btn-primary" type="submit" disabled={!username || !connected}>
                            Send
                        </button>
                    </form>
                    {!connected && <div className="text-danger mt-2">Connecting to server...</div>}
                </div>
            </div>
        </div>
    )
}

export default App
