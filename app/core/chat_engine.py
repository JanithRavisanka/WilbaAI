from app.services.gemini_service import GeminiChatService
from app.models.chat_models import ChatRequest, ChatResponse, ChatMessage
from typing import List, Dict, Any
import asyncio

class ChatEngine:
    def __init__(self):
        self.gemini_service = GeminiChatService()
    
    async def process_message(self, request: ChatRequest) -> ChatResponse:
        """Process a chat message through the Gemini service"""
        try:
            # Convert to the format expected by Gemini service
            messages = []
            for msg in request.conversation_history:
                messages.append({
                    "role": msg.role,
                    "content": msg.content
                })
            
            # Add current message
            messages.append({
                "role": "user",
                "content": request.message
            })
            
            # Get response from Gemini
            result = await self.gemini_service.chat(messages)
            
            if result["success"]:
                # Update conversation history
                response_messages = request.conversation_history.copy()
                response_messages.append(ChatMessage(role="user", content=request.message))
                response_messages.append(ChatMessage(role="assistant", content=result["response"]))
                
                return ChatResponse(
                    success=True,
                    response=result["response"],
                    conversation_history=response_messages
                )
            else:
                return ChatResponse(
                    success=False,
                    error=result["error"]
                )
                
        except Exception as e:
            return ChatResponse(
                success=False,
                error=f"Chat engine error: {str(e)}"
            )
    
    def simple_chat(self, message: str) -> str:
        """Simple chat without conversation history"""
        try:
            return self.gemini_service.simple_chat(message)
        except Exception as e:
            return f"Error: {str(e)}"
    
    async def chat_with_context(self, message: str, context: str = "") -> ChatResponse:
        """Chat with additional context"""
        try:
            # Create a message with context
            contextual_message = f"Context: {context}\n\nUser message: {message}"
            
            result = await self.gemini_service.chat([{
                "role": "user",
                "content": contextual_message
            }])
            
            if result["success"]:
                return ChatResponse(
                    success=True,
                    response=result["response"]
                )
            else:
                return ChatResponse(
                    success=False,
                    error=result["error"]
                )
                
        except Exception as e:
            return ChatResponse(
                success=False,
                error=f"Context chat error: {str(e)}"
            )