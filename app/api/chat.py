from fastapi import APIRouter, HTTPException, Depends
from app.models.chat_models import ChatRequest, ChatResponse, ChatMessage
from app.services.gemini_service import GeminiChatService
from app.db.session import SessionLocal
from app.db.thread_entity import Thread as ThreadModel
from sqlalchemy.orm import Session
from typing import List, Dict, Any

router = APIRouter(prefix="/chat", tags=["chat"])

# Initialize the chat service
chat_service = GeminiChatService()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ChatResponse)
async def send_message(request: ChatRequest, db: Session = Depends(get_db)):
    """Send a message and get response using Gemini with LangGraph"""
    try:
        # Validate thread exists
        thread = db.query(ThreadModel).filter(ThreadModel.id == request.thread_id).first()
        if not thread:
            raise HTTPException(status_code=404, detail="Thread not found")
        
        # Convert conversation history to the format expected by Gemini service
        messages = []
        for msg in request.conversation_history:
            messages.append({
                "role": msg.role,
                "content": msg.content
            })
        
        # Add the current message
        messages.append({
            "role": "user",
            "content": request.message
        })
        
        # Get response from Gemini service
        result = await chat_service.chat(messages)
        
        if result["success"]:
            # Create response with updated conversation history
            response_messages = request.conversation_history.copy()
            response_messages.append(ChatMessage(role="user", content=request.message))
            response_messages.append(ChatMessage(role="assistant", content=result["response"]))
            
            return ChatResponse(
                success=True,
                response=result["response"],
                thread_id=request.thread_id,
                conversation_history=response_messages
            )
        else:
            return ChatResponse(
                success=False,
                error=result["error"],
                thread_id=request.thread_id
            )
            
    except HTTPException:
        raise
    except Exception as e:
        return ChatResponse(
            success=False,
            error=f"Chat error: {str(e)}",
            thread_id=request.thread_id
        )

@router.post("/simple", response_model=ChatResponse)
async def simple_chat(request: ChatRequest, db: Session = Depends(get_db)):
    """Simple chat without conversation history"""
    try:
        # Validate thread exists
        thread = db.query(ThreadModel).filter(ThreadModel.id == request.thread_id).first()
        if not thread:
            raise HTTPException(status_code=404, detail="Thread not found")
        
        response = chat_service.simple_chat(request.message)
        return ChatResponse(
            success=True,
            response=response,
            thread_id=request.thread_id
        )
    except HTTPException:
        raise
    except Exception as e:
        return ChatResponse(
            success=False,
            error=f"Simple chat error: {str(e)}",
            thread_id=request.thread_id
        )

@router.get("/thread/{thread_id}/history")
async def get_thread_history(thread_id: int, db: Session = Depends(get_db)):
    """Get conversation history for a thread (placeholder for future implementation)"""
    # Validate thread exists
    thread = db.query(ThreadModel).filter(ThreadModel.id == thread_id).first()
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")
    
    # For now, return empty history - you can implement actual history storage later
    return {
        "thread_id": thread_id,
        "history": [],
        "thread_title": thread.title
    }

@router.get("/health")
async def health_check():
    """Health check for the chat service"""
    return {"status": "healthy", "service": "gemini-chat"}