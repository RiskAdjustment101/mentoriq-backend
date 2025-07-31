"""
MentorIQ FastAPI Backend with Groq AI Integration
Ultra-fast inference using Groq's API for real-time conversational AI
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, List, Optional
import logging
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title="MentorIQ AI Backend",
    description="""
    AI-augmented mentor platform backend with Groq integration
    Provides ultra-fast intelligent responses for FIRST LEGO League programs.
    
    Features:
    - Landing page program discovery assistance
    - Bidirectional registration system support
    - Context-aware conversations across platform
    - Groq-powered ultra-fast inference (<500ms response time)
    """,
    version="1.2.0"
)

# CORS configuration
allowed_origins = os.getenv('ALLOWED_ORIGINS', 'http://localhost:5173,http://localhost:3000').split(',')
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

# Import Groq service
from src.services.groq_service import mentoriq_groq_ai

@app.on_event("startup")
async def startup_event():
    """Application startup"""
    logger.info("🚀 MentorIQ Backend starting up...")
    logger.info("⚡ Groq AI integration initialized for ultra-fast responses")
    
    # Check if Groq API key is available
    groq_key = os.getenv('GROQ_API_KEY')
    if groq_key:
        logger.info("✅ Groq API key found - AI responses enabled")
    else:
        logger.warning("⚠️  Groq API key not found - using fallback responses")
    
    logger.info("🎯 Ready to serve intelligent mentor platform responses!")

@app.post("/api/ai/chat/landing", response_model=AIResponse)
async def landing_chat(request: ChatRequest):
    """AI chat assistant for landing page program discovery"""
    try:
        logger.info(f"Landing chat query: {request.query}")
        
        start_time = datetime.now()
        
        response_data = await mentoriq_groq_ai.get_contextual_response(
            query=request.query,
            page_context="landing",
            user_data=request.user_context,
            conversation_history=request.conversation_history or []
        )
        
        response_time = (datetime.now() - start_time).total_seconds()
        logger.info(f"Response generated in {response_time:.3f}s")
        
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

@app.post("/api/ai/chat/registration", response_model=RegistrationAIResponse)
async def registration_chat(request: RegistrationChatRequest):
    """AI chat assistant for bidirectional registration system"""
    try:
        logger.info(f"Registration chat query: {request.query}")
        
        start_time = datetime.now()
        
        response_data = await mentoriq_groq_ai.get_contextual_response(
            query=request.query,
            page_context="registration",
            user_data=request.registration_data,
            conversation_history=request.conversation_history or []
        )
        
        response_time = (datetime.now() - start_time).total_seconds()
        logger.info(f"Registration response generated in {response_time:.3f}s")
        
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

@app.get("/api/ai/health")
async def ai_health_check():
    """Health check endpoint for Groq AI service"""
    try:
        start_time = datetime.now()
        
        # Test basic functionality
        test_response = await mentoriq_groq_ai.get_contextual_response(
            query="health check",
            page_context="landing"
        )
        
        response_time = (datetime.now() - start_time).total_seconds()
        
        return {
            "status": "healthy",
            "service": "MentorIQ AI Assistant",
            "model": mentoriq_groq_ai.model,
            "response_time": f"{response_time:.3f}s",
            "groq_available": mentoriq_groq_ai.client is not None,
            "timestamp": datetime.now().isoformat(),
            "test_response_length": len(test_response.get("response", ""))
        }
        
    except Exception as e:
        logger.error(f"AI health check failed: {e}")
        return {
            "status": "degraded",
            "error": str(e),
            "groq_available": False,
            "timestamp": datetime.now().isoformat()
        }

@app.get("/api/ai/knowledge/summary")
async def get_knowledge_summary():
    """Get summary of platform knowledge available to AI"""
    try:
        knowledge_base = mentoriq_groq_ai.knowledge_base
        
        return {
            "platform_info": knowledge_base["platform_info"]["name"],
            "mission": knowledge_base["platform_info"]["mission"],
            "current_features": list(knowledge_base["current_features"].keys()),
            "user_types": list(knowledge_base["user_types"].keys()),
            "tech_stack": knowledge_base["tech_stack"],
            "performance": knowledge_base["business_metrics"]["current_performance"],
            "last_updated": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error retrieving knowledge summary: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve knowledge summary"
        )

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "service": "MentorIQ AI Backend",
        "version": "1.2.0",
        "description": "AI-augmented mentor platform with Groq integration",
        "status": "operational",
        "ai_provider": "Groq (Ultra-fast inference)",
        "endpoints": {
            "ai_chat_landing": "/api/ai/chat/landing",
            "ai_chat_registration": "/api/ai/chat/registration", 
            "ai_health": "/api/ai/health",
            "knowledge_summary": "/api/ai/knowledge/summary"
        },
        "documentation": "/docs",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """Application health check"""
    groq_key_available = bool(os.getenv('GROQ_API_KEY'))
    
    return {
        "status": "healthy",
        "service": "MentorIQ Backend",
        "version": "1.2.0",
        "timestamp": datetime.now().isoformat(),
        "components": {
            "api": "operational",
            "groq_integration": "available" if groq_key_available else "fallback_mode",
            "knowledge_base": "loaded"
        }
    }

@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Custom 404 handler"""
    return JSONResponse(
        status_code=404,
        content={
            "error": "Endpoint not found",
            "message": "The requested endpoint does not exist",
            "available_endpoints": [
                "/",
                "/health", 
                "/api/ai/chat/landing",
                "/api/ai/chat/registration",
                "/api/ai/health",
                "/docs"
            ]
        }
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """Custom 500 handler"""
    logger.error(f"Internal server error: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred",
            "timestamp": datetime.now().isoformat()
        }
    )

if __name__ == "__main__":
    import uvicorn
    
    # Development server configuration
    uvicorn.run(
        "main-groq:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )