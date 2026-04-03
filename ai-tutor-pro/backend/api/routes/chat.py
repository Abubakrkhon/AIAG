"""
Chat API - Real-time chat with AI about learning materials
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uuid

router = APIRouter()


class ChatMessage(BaseModel):
    """Chat message model"""
    id: str = ""
    role: str  # "user" or "assistant"
    content: str
    timestamp: float = 0.0
    metadata: Dict[str, Any] = {}


class ChatRequest(BaseModel):
    """Chat request model"""
    message: str
    context_id: Optional[str] = None
    conversation_id: Optional[str] = None
    options: Dict[str, Any] = {}


class ChatResponse(BaseModel):
    """Chat response model"""
    success: bool
    message: ChatMessage
    conversation_id: str
    context_used: Optional[str] = None
    suggestions: List[str] = []


# In-memory conversation storage (use Redis in production)
conversations: Dict[str, List[ChatMessage]] = {}


@router.post("/", response_model=ChatResponse)
async def send_message(request: ChatRequest):
    """
    Send a message and get AI response.
    
    Args:
        request: Chat request with message and context
        
    Returns:
        AI response message
    """
    try:
        from ..agents.teacher import TeacherAgent
        
        # Generate conversation ID if not provided
        conversation_id = request.conversation_id or str(uuid.uuid4())
        
        # Initialize or get conversation
        if conversation_id not in conversations:
            conversations[conversation_id] = []
        
        # Create user message
        user_message = ChatMessage(
            id=str(uuid.uuid4()),
            role="user",
            content=request.message
        )
        conversations[conversation_id].append(user_message)
        
        # Get context if provided
        context = ""
        if request.context_id:
            # Retrieve context from memory/database
            # For now, just use placeholder
            context = f"Context: {request.context_id}"
        
        # Process with Teacher Agent
        teacher = TeacherAgent()
        
        explanation_level = request.options.get("level", "beginner")
        
        response = await teacher.process(
            input_data=f"{context}\n\nQuestion: {request.message}",
            options={
                "level": explanation_level,
                "include_examples": True,
                "include_analogies": True
            }
        )
        
        if not response.success:
            raise HTTPException(status_code=500, detail=response.message)
        
        # Extract answer from response
        ai_content = response.data.get("explanation", {})
        if isinstance(ai_content, dict):
            ai_text = ai_content.get("full_text", str(ai_content))
        else:
            ai_text = str(ai_content)
        
        # Create AI message
        ai_message = ChatMessage(
            id=str(uuid.uuid4()),
            role="assistant",
            content=ai_text,
            metadata={
                "level": explanation_level,
                "model": response.metadata.get("model_used", "unknown")
            }
        )
        conversations[conversation_id].append(ai_message)
        
        # Generate follow-up suggestions
        suggestions = await generate_suggestions(request.message, ai_text)
        
        return ChatResponse(
            success=True,
            message=ai_message,
            conversation_id=conversation_id,
            context_used=request.context_id,
            suggestions=suggestions
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/conversation/{conversation_id}")
async def get_conversation(conversation_id: str):
    """Get conversation history"""
    if conversation_id not in conversations:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    return {
        "success": True,
        "conversation_id": conversation_id,
        "messages": conversations[conversation_id],
        "message_count": len(conversations[conversation_id])
    }


@router.delete("/conversation/{conversation_id}")
async def delete_conversation(conversation_id: str):
    """Delete conversation"""
    if conversation_id in conversations:
        del conversations[conversation_id]
    
    return {"success": True, "message": "Conversation deleted"}


@router.get("/conversations")
async def list_conversations():
    """List all conversations"""
    return {
        "success": True,
        "conversations": [
            {
                "id": conv_id,
                "message_count": len(messages),
                "last_message": messages[-1].content if messages else ""
            }
            for conv_id, messages in conversations.items()
        ]
    }


async def generate_suggestions(user_message: str, ai_response: str) -> List[str]:
    """Generate follow-up question suggestions"""
    try:
        from ..utils.llm_client import LLMClient
        
        llm = LLMClient()
        
        prompt = f"""
        Based on this conversation, suggest 3 follow-up questions the user might ask.
        
        User asked: {user_message[:200]}
        AI answered: {ai_response[:500]}
        
        Return JSON array of 3 short question strings.
        """
        
        response = await llm.generate(prompt, max_tokens=300)
        suggestions = llm.parse_json(response, default=[])
        
        if isinstance(suggestions, list) and len(suggestions) > 0:
            return suggestions[:3]
        
    except Exception:
        pass
    
    # Default suggestions
    return [
        "Can you explain this more simply?",
        "What are some real-world examples?",
        "How does this relate to what we discussed before?"
    ]


@router.post("/voice")
async def voice_chat():
    """Voice-based chat (placeholder for future implementation)"""
    return {
        "success": False,
        "message": "Voice chat coming soon",
        "status": "not_implemented"
    }
