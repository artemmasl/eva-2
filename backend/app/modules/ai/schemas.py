from datetime import datetime

from pydantic import BaseModel


class ChatContext(BaseModel):
    page: str | None = None
    complex_id: str | None = None
    complex_name: str | None = None
    space_id: str | None = None


class ChatRequest(BaseModel):
    message: str
    context: ChatContext | None = None


class ChatMessageSchema(BaseModel):
    role: str
    content: str
    created_at: datetime


class ChatHistorySchema(BaseModel):
    session_id: str
    messages: list[ChatMessageSchema]
