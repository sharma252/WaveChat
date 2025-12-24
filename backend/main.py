from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import json

import models, schemas, database

app = FastAPI(title="WaveChat API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables
models.Base.metadata.create_all(bind=database.engine)

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.get("/messages", response_model=List[schemas.Message])
def get_messages(db: Session = Depends(database.get_db)):
    messages = db.query(models.Message).order_by(models.Message.timestamp.asc()).all()
    return messages

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str, db: Session = Depends(database.get_db)):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Save to database
            db_message = models.Message(
                username=message_data["username"],
                content=message_data["content"]
            )
            db.add(db_message)
            db.commit()
            db.refresh(db_message)
            
            # Broadcast to all
            await manager.broadcast(json.dumps({
                "id": db_message.id,
                "username": db_message.username,
                "content": db_message.content,
                "timestamp": db_message.timestamp.isoformat()
            }))
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"Error: {e}")
        manager.disconnect(websocket)
