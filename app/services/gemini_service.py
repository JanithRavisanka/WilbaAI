import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END
from typing import Dict, Any, List, TypedDict
from app.config import settings

# Configure Google Generative AI
genai.configure(api_key=settings.GOOGLE_API_KEY)

# Define the state structure at module level
class ChatState(TypedDict):
    messages: List[Dict[str, Any]]
    response: str
    error: str

class GeminiChatService:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-pro",
            temperature=0.7,
            google_api_key=settings.GOOGLE_API_KEY,
        )
        self.graph = self._create_chat_graph()
    
    def _create_chat_graph(self):
        """Create a LangGraph for chat processing"""
        
        # Create the graph
        workflow = StateGraph(ChatState)
        
        # Add nodes
        workflow.add_node("process_message", self._process_message)
        workflow.add_node("generate_response", self._generate_response)
        
        # Add edges
        workflow.set_entry_point("process_message")
        workflow.add_edge("process_message", "generate_response")
        workflow.add_edge("generate_response", END)
        
        return workflow.compile()
    
    def _process_message(self, state: ChatState) -> ChatState:
        """Process incoming message"""
        try:
            # Extract the latest message
            if state["messages"]:
                latest_message = state["messages"][-1]
                # You can add preprocessing logic here
                state["response"] = ""
                state["error"] = ""
            return state
        except Exception as e:
            state["error"] = f"Error processing message: {str(e)}"
            return state
    
    def _generate_response(self, state: ChatState) -> ChatState:
        """Generate response using Gemini"""
        try:
            if state["messages"]:
                # Convert messages to LangChain format
                from langchain_core.messages import HumanMessage, AIMessage
                
                langchain_messages = []
                for msg in state["messages"]:
                    if msg.get("role") == "user":
                        langchain_messages.append(HumanMessage(content=msg.get("content", "")))
                    elif msg.get("role") == "assistant":
                        langchain_messages.append(AIMessage(content=msg.get("content", "")))
                
                # Generate response
                response = self.llm.invoke(langchain_messages)
                state["response"] = response.content
            else:
                state["error"] = "No messages to process"
        except Exception as e:
            state["error"] = f"Error generating response: {str(e)}"
        
        return state
    
    async def chat(self, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Main chat method"""
        try:
            # Create initial state
            initial_state = {
                "messages": messages,
                "response": "",
                "error": ""
            }
            
            # Run the graph
            result = self.graph.invoke(initial_state)
            
            if result["error"]:
                return {
                    "success": False,
                    "error": result["error"],
                    "response": None
                }
            
            return {
                "success": True,
                "response": result["response"],
                "error": None
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Chat service error: {str(e)}",
                "response": None
            }
    
    def simple_chat(self, message: str) -> str:
        """Simple chat method for basic interactions"""
        try:
            response = self.llm.invoke([message])
            return response.content
        except Exception as e:
            return f"Error: {str(e)}" 