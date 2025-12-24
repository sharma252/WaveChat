from pydantic import BaseModel
from datetime import datetime

class MessageBase(BaseModel):
    username: str
    content: str

class MessageCreate(MessageBase):
    pass

class Message(MessageBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True
