from fastapi import APIRouter
from app.models.chat_models import ChatMessage

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/", response_model=ChatMessage)
def send_message(msg: ChatMessage):
    # Echo the message for boilerplate
    return msg