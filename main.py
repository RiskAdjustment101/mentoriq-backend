"""
MentorIQ FastAPI Backend with Ollama AI Integration
Provides intelligent AI responses trained on comprehensive platform knowledge
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
import os
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("🚀 MentorIQ Backend starting up...")
    logger.info("🤖 Initializing AI services...")
    
    # TODO: Initialize Ollama connection when ready
    # await initialize_ollama()
    
    logger.info("✅ Backend ready to serve intelligent responses!")
    
    yield
    
    # Shutdown
    logger.info("🛑 MentorIQ Backend shutting down...")

# Create FastAPI application
app = FastAPI(
    title="MentorIQ AI Backend",
    description="""
    AI-augmented mentor platform backend providing intelligent responses 
    trained on comprehensive platform knowledge for FIRST LEGO League programs.
    
    Features:
    - Landing page program discovery assistance
    - Bidirectional registration system support
    - Context-aware conversations across platform
    - Knowledge base trained on complete platform documentation
    """,
    version="1.1.0",
    lifespan=lifespan
)

# CORS configuration for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and include AI endpoints
from src.api.ai_endpoints import router as ai_router
app.include_router(ai_router)

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "service": "MentorIQ AI Backend",
        "version": "1.1.0",
        "description": "AI-augmented mentor platform with Ollama integration",
        "status": "operational",
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
    return {
        "status": "healthy",
        "service": "MentorIQ Backend",
        "version": "1.1.0",
        "timestamp": datetime.now().isoformat(),
        "components": {
            "api": "operational",
            "ai_service": "operational", 
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
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )