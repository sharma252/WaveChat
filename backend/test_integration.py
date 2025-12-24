import asyncio
import websockets
import json
import requests
import time

def test_chat_persistence():
    url = "http://localhost/api/messages"
    ws_url = "ws://localhost/ws/test_client"
    
    # Wait for the system to be up with retries
    max_retries = 10
    connected = False
    for i in range(max_retries):
        try:
            resp = requests.get(url)
            if resp.status_code == 200:
                print("System is up and reachable!")
                connected = True
                break
        except Exception:
            print(f"Waiting for system to be reachable (attempt {i+1}/{max_retries})...")
            time.sleep(5)
    
    if not connected:
        print("Error: Could not reach the system after several attempts.")
        exit(1)

    # Connect and send message
    async def send_msg():
        async with websockets.connect(ws_url) as websocket:
            msg = {"username": "test_user", "content": "Hello World"}
            await websocket.send(json.dumps(msg))
            # Wait for broadcast
            response = await websocket.recv()
            return json.loads(response)

    try:
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
    except Exception as e:
        print(f"Error during test: {e}")
        exit(1)

if __name__ == "__main__":
    test_chat_persistence()
