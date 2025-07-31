"""
FastAPI endpoints for MentorIQ AI integration
Provides intelligent responses using Ollama trained on platform knowledge
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, List, Optional
import logging

from ..services.ollama_service import mentoriq_ai

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/ai", tags=["AI Assistant"])

# Request/Response Models
class ChatRequest(BaseModel):
    query: str
    user_context: Optional[Dict] = None
    conversation_history: Optional[List[Dict]] = None

class RegistrationChatRequest(BaseModel):
    query: str
    registration_data: Optional[Dict] = None
    conversation_history: Optional[List[Dict]] = None

class AIResponse(BaseModel):
    response: str
    context: str
    suggestions: Optional[List[str]] = None
    timestamp: str

class RegistrationAIResponse(AIResponse):
    field_updates: Optional[Dict] = None

@router.post("/chat/landing", response_model=AIResponse)
async def landing_chat(request: ChatRequest):
    """
    AI chat assistant for landing page program discovery
    
    Provides intelligent responses for:
    - Program discovery queries
    - Parent and mentor assistance
    - Platform information
    - Registration guidance
    """
    try:
        logger.info(f"Landing chat query: {request.query}")
        
        response_data = await mentoriq_ai.get_contextual_response(
            query=request.query,
            page_context="landing",
            user_data=request.user_context,
            conversation_history=request.conversation_history or []
        )
        
        return AIResponse(
            response=response_data["response"],
            context=response_data["context"],
            suggestions=response_data.get("suggestions", []),
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Error in landing chat: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to generate AI response. Please try again."
        )

@router.post("/chat/registration", response_model=RegistrationAIResponse)
async def registration_chat(request: RegistrationChatRequest):
    """
    AI chat assistant for bidirectional registration system
    
    Provides intelligent responses with:
    - Field extraction from natural language
    - Contextual encouragement based on user type
    - Domain-aware email responses
    - Form synchronization data
    """
    try:
        logger.info(f"Registration chat query: {request.query}")
        
        response_data = await mentoriq_ai.get_contextual_response(
            query=request.query,
            page_context="registration",
            user_data=request.registration_data,
            conversation_history=request.conversation_history or []
        )
        
        return RegistrationAIResponse(
            response=response_data["response"],
            context=response_data["context"],
            suggestions=response_data.get("suggestions", []),
            field_updates=response_data.get("field_updates", {}),
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Error in registration chat: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to generate registration assistance. Please try again."
        )

@router.get("/health")
async def ai_health_check():
    """Health check endpoint for AI service"""
    try:
        # Test basic functionality
        test_response = await mentoriq_ai.get_contextual_response(
            query="test",
            page_context="landing"
        )
        
        return {
            "status": "healthy",
            "service": "MentorIQ AI Assistant",
            "model": mentoriq_ai.model,
            "timestamp": datetime.now().isoformat(),
            "test_response_length": len(test_response.get("response", ""))
        }
        
    except Exception as e:
        logger.error(f"AI health check failed: {e}")
        return {
            "status": "degraded",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@router.get("/knowledge/summary")
async def get_knowledge_summary():
    """
    Get summary of platform knowledge available to AI
    Useful for debugging and verification
    """
    try:
        knowledge_base = mentoriq_ai.knowledge_base
        
        return {
            "platform_info": knowledge_base["platform_info"]["name"],
            "mission": knowledge_base["platform_info"]["mission"],
            "current_features": list(knowledge_base["current_features"].keys()),
            "user_types": list(knowledge_base["user_types"].keys()),
            "development_phases": {
                phase: info["status"] 
                for phase, info in knowledge_base["development_phases"].items()
            },
            "tech_stack": knowledge_base["tech_stack"],
            "last_updated": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error retrieving knowledge summary: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve knowledge summary"
        )

# Enhanced endpoints for future Ollama integration

@router.post("/chat/context-aware")
async def context_aware_chat(
    query: str,
    page_context: str,
    user_session: Optional[Dict] = None,
    platform_context: Optional[Dict] = None
):
    """
    Advanced context-aware chat endpoint
    For future integration with full user session and platform state
    """
    try:
        # This endpoint is designed for future enhancement
        # when full platform context and user sessions are available
        
        enhanced_context = {
            "page": page_context,
            "user_session": user_session or {},
            "platform_state": platform_context or {},
            "timestamp": datetime.now().isoformat()
        }
        
        response_data = await mentoriq_ai.get_contextual_response(
            query=query,
            page_context=page_context,
            user_data=enhanced_context
        )
        
        return {
            "response": response_data["response"], 
            "context": enhanced_context,
            "suggestions": response_data.get("suggestions", []),
            "confidence": "high",  # Placeholder for future ML confidence scoring
            "response_time": "< 2s"  # Placeholder for actual timing
        }
        
    except Exception as e:
        logger.error(f"Error in context-aware chat: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to generate context-aware response"
        )

# Import datetime here to avoid issues
from datetime import datetime