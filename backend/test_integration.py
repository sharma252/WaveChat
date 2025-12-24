import asyncio
import websockets
import json
import requests
import time

def test_chat_persistence():
    # Wait for the system to be up
    time.sleep(10)
    
    url = "http://localhost/api/messages"
    ws_url = "ws://localhost/ws/test_client"
    
    # Connect and send message
    async def send_msg():
        async with websockets.connect(ws_url) as websocket:
            msg = {"username": "test_user", "content": "Hello World"}
            await websocket.send(json.dumps(msg))
            # Wait for broadcast
            response = await websocket.recv()
            return json.loads(response)

    loop = asyncio.get_event_loop()
    received = loop.run_until_complete(send_msg())
    
    assert received["username"] == "test_user"
    assert received["content"] == "Hello World"
    
    # Check persistence via REST API
    resp = requests.get(url)
    messages = resp.json()
    
    found = False
    for m in messages:
        if m["username"] == "test_user" and m["content"] == "Hello World":
            found = True
            break
    
    assert found == True
    print("Test passed: Message sent via WebSocket and persisted in DB!")

if __name__ == "__main__":
    test_chat_persistence()
