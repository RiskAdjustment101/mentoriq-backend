"""
MentorIQ FastAPI Backend - Simplified for Render Deployment
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional
import logging
from datetime import datetime
import os
from dotenv import load_dotenv
import json
import re

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Groq
try:
    from groq import Groq
    groq_client = Groq(api_key=os.getenv('GROQ_API_KEY'))
    GROQ_AVAILABLE = True
    logger.info("✅ Groq client initialized")
except Exception as e:
    logger.warning(f"⚠️ Groq not available: {e}")
    groq_client = None
    GROQ_AVAILABLE = False

# Create FastAPI app
app = FastAPI(
    title="MentorIQ AI Backend",
    description="AI-augmented mentor platform with Groq integration",
    version="1.2.0"
)

# CORS
allowed_origins = os.getenv('ALLOWED_ORIGINS', 'http://localhost:5173,http://localhost:3000').split(',')
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
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

# Helper functions
def extract_name(text: str) -> Optional[str]:
    patterns = [
        r"(?:i'm|i am|my name is|call me)\s+([a-zA-Z\s]+)",
        r"^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)$"
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match and match.group(1):
            name = match.group(1).strip()
            if len(name) < 50 and re.match(r'^[A-Za-z\s]+$', name):
                return name
    return None

def extract_email(text: str) -> Optional[str]:
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    match = re.search(email_pattern, text)
    return match.group(0) if match else None

def extract_user_type(text: str) -> Optional[str]:
    text_lower = text.lower()
    parent_keywords = ['parent', 'child', 'kid', 'son', 'daughter', 'family']
    mentor_keywords = ['mentor', 'teach', 'coach', 'lead', 'engineer', 'help']
    
    if any(keyword in text_lower for keyword in parent_keywords):
        return 'parent'
    elif any(keyword in text_lower for keyword in mentor_keywords):
        return 'mentor'
    return None

async def get_groq_response(query: str, context: str) -> str:
    if not GROQ_AVAILABLE:
        return None
    
    try:
        system_prompt = f"""You are an AI assistant for MentorIQ, an AI-augmented mentor platform for FIRST LEGO League programs.

Mission: Transform FIRST LEGO League mentoring through conversational AI, saving mentors 60%+ administrative time.

Context: {context}

Be helpful, encouraging, and knowledgeable about FLL programs. Keep responses conversational but informative (2-3 sentences)."""

        completion = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ],
            temperature=0.7,
            max_tokens=300
        )
        
        return completion.choices[0].message.content
    except Exception as e:
        logger.error(f"Groq error: {e}")
        return None

# Routes
@app.get("/")
async def root():
    return {
        "service": "MentorIQ AI Backend", 
        "version": "1.2.0",
        "status": "operational",
        "groq_available": GROQ_AVAILABLE,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "groq_available": GROQ_AVAILABLE,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/ai/chat/landing", response_model=AIResponse)
async def landing_chat(request: ChatRequest):
    try:
        query = request.query.lower()
        
        # Try Groq first
        ai_response = await get_groq_response(request.query, "landing page program discovery")
        
        # Fallback responses
        if not ai_response:
            if any(word in query for word in ['parent', 'child']):
                ai_response = "Perfect! I'd love to help you find the ideal FLL program for your child. MentorIQ connects families with amazing mentors and teams in your area."
            elif any(word in query for word in ['mentor', 'teach']):
                ai_response = "Wonderful! We're always excited to connect with passionate educators. MentorIQ saves mentors 60%+ of administrative time through AI-powered tools."
            else:
                ai_response = "Welcome to MentorIQ! I'm here to help you discover amazing FLL programs and mentors."
        
        suggestions = [
            "I'm a parent looking for programs",
            "I want to become a mentor", 
            "Tell me about your platform",
            "Take me to registration"
        ]
        
        return AIResponse(
            response=ai_response,
            context="landing",
            suggestions=suggestions,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Landing chat error: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate response")

@app.post("/api/ai/chat/registration", response_model=RegistrationAIResponse)
async def registration_chat(request: RegistrationChatRequest):
    try:
        query = request.query
        
        # Extract fields
        field_updates = {}
        name = extract_name(query)
        email = extract_email(query) 
        user_type = extract_user_type(query)
        
        if name:
            field_updates["name"] = name
        if email:
            field_updates["email"] = email
        if user_type:
            field_updates["userType"] = user_type
        
        # Try Groq first
        ai_response = await get_groq_response(query, f"registration assistance with extracted fields: {field_updates}")
        
        # Fallback response
        if not ai_response:
            response_parts = []
            if name:
                response_parts.append(f"Hi {name}! Great to meet you.")
            if email:
                response_parts.append("Thanks for providing your email address!")
            if user_type == 'parent':
                response_parts.append("Wonderful! We're excited to help you find the perfect FLL program for your child.")
            elif user_type == 'mentor':
                response_parts.append("Fantastic! We need more passionate mentors like you.")
            
            ai_response = " ".join(response_parts) if response_parts else "I'm here to help you complete your registration!"
        
        return RegistrationAIResponse(
            response=ai_response,
            context="registration",
            field_updates=field_updates,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Registration chat error: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate response")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)