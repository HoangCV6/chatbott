from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class MessageBase(BaseModel):
    content: str

class MessageCreate(MessageBase):
    session_id: int
    role: str # user hoặc assistant

class MessageResponse(MessageBase):
    id: int
    role: str
    created_at: datetime
    class Config:
        from_attributes = True

class ChatRequest(BaseModel):
    user_id: int
    session_id: Optional[int] = None
    content: str