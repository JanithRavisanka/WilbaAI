from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str

class ChatRequest(BaseModel):
    message: str
    thread_id: int
    conversation_history: Optional[List[ChatMessage]] = []

class ChatResponse(BaseModel):
    success: bool
    response: Optional[str] = None
    error: Optional[str] = None
    thread_id: int
    conversation_history: Optional[List[ChatMessage]] = []

class ConversationState(BaseModel):
    messages: List[ChatMessage]
    thread_id: int
    app_id: Optional[int] = None