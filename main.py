"""
MentorIQ FastAPI Backend - Ultra-Simple Version for Deployment
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional
import os
from datetime import datetime

# Create app
app = FastAPI(title="MentorIQ AI Backend", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for now
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class ChatRequest(BaseModel):
    query: str
    user_context: Optional[Dict] = None
    conversation_history: Optional[List[Dict]] = None

class AIResponse(BaseModel):
    response: str
    context: str
    suggestions: Optional[List[str]] = None
    timestamp: str

# Routes
@app.get("/")
def root():
    return {
        "service": "MentorIQ AI Backend",
        "status": "operational",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/ai/chat/landing")
def landing_chat(request: ChatRequest):
    query = request.query.lower()
    
    # Simple responses based on keywords
    if any(word in query for word in ['parent', 'child', 'kid']):
        response = "Perfect! I'd love to help you find the ideal FLL program for your child. MentorIQ connects families with amazing mentors and teams in your area."
        suggestions = ["Tell me about program costs", "How do I evaluate mentors?", "Take me to registration"]
    elif any(word in query for word in ['mentor', 'teach', 'coach']):
        response = "Wonderful! We're excited to connect with passionate educators. MentorIQ saves mentors 60%+ of administrative time through AI-powered tools."
        suggestions = ["How does the platform save time?", "What support do mentors get?", "Create my mentor profile"]
    else:
        response = "Welcome to MentorIQ! I'm here to help you discover amazing FLL programs and mentors. What brings you here today?"
        suggestions = ["I'm a parent looking for programs", "I want to become a mentor", "Tell me about your platform"]
    
    return {
        "response": response,
        "context": "landing",
        "suggestions": suggestions,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/ai/chat/registration")
def registration_chat(request: ChatRequest):
    query = request.query
    
    # Extract basic info
    field_updates = {}
    response = "I'm here to help you complete your registration! "
    
    # Simple name detection
    if "name is" in query.lower() or "i'm" in query.lower():
        words = query.split()
        for i, word in enumerate(words):
            if word.lower() in ["name", "i'm", "am"] and i + 1 < len(words):
                potential_name = words[i + 1].strip(".,!?")
                if potential_name.isalpha():
                    field_updates["name"] = potential_name
                    response = f"Hi {potential_name}! Great to meet you. "
                break
    
    # Simple email detection
    if "@" in query:
        words = query.split()
        for word in words:
            if "@" in word and "." in word:
                field_updates["email"] = word.strip(".,!?")
                response += "Thanks for providing your email address! "
                break
    
    # User type detection
    if any(word in query.lower() for word in ['parent', 'child', 'kid']):
        field_updates["userType"] = "parent"
        response += "Wonderful! We're excited to help you find the perfect FLL program for your child."
    elif any(word in query.lower() for word in ['mentor', 'teach', 'coach']):
        field_updates["userType"] = "mentor"
        response += "Fantastic! We need more passionate mentors like you."
    
    if not field_updates:
        response = "I'm here to help you complete your registration! You can tell me your name, email, and whether you're a parent or mentor."
    
    return {
        "response": response,
        "context": "registration", 
        "field_updates": field_updates,
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)