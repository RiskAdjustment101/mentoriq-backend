"""
MentorIQ FastAPI Backend with Ollama AI Integration - Minimal Version
Simplified version for testing AI responses without full dependencies
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, List, Optional
import logging
from datetime import datetime
import json
import re

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
    AI-augmented mentor platform backend providing intelligent responses 
    trained on comprehensive platform knowledge for FIRST LEGO League programs.
    
    Features:
    - Landing page program discovery assistance
    - Bidirectional registration system support
    - Context-aware conversations across platform
    - Knowledge base trained on complete platform documentation
    """,
    version="1.1.0"
)

# CORS configuration for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite dev server
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

# Simplified AI Service (embedded for testing)
class SimplifiedAI:
    """Simplified AI service for testing without external dependencies"""
    
    def __init__(self):
        self.knowledge_base = self._load_platform_knowledge()
    
    def _load_platform_knowledge(self):
        return {
            "platform_info": {
                "name": "MentorIQ",
                "mission": "AI-augmented mentor platform saving 60%+ administrative time",
                "vision": "Transform FIRST LEGO League mentoring through conversational AI"
            },
            "current_features": {
                "landing_page": {
                    "description": "AI-first program discovery interface",
                    "layout": "70/30 split-screen (content/AI chat)"
                },
                "registration": {
                    "description": "Revolutionary bidirectional registration system",
                    "innovation": "Real-time form ↔ chat synchronization"
                }
            }
        }
    
    async def get_contextual_response(
        self,
        query: str,
        page_context: str,
        user_data: Optional[Dict] = None,
        conversation_history: List[Dict] = None
    ) -> Dict:
        """Generate intelligent response based on platform knowledge"""
        if conversation_history is None:
            conversation_history = []
        
        response_data = {
            "response": "",
            "suggestions": [],
            "field_updates": {},
            "context": page_context
        }
        
        if page_context == 'landing':
            response_data = await self._handle_landing_query(query)
        elif page_context == 'registration':
            response_data = await self._handle_registration_query(query, user_data)
        
        return response_data
    
    async def _handle_landing_query(self, query: str) -> Dict:
        """Handle landing page program discovery queries"""
        query_lower = query.lower()
        
        # Parent-focused responses
        if any(word in query_lower for word in ['child', 'kid', 'son', 'daughter', 'parent']):
            return {
                "response": """Perfect! I'd love to help you find the ideal FLL program for your child. MentorIQ connects families with amazing mentors and teams in your area.

Our AI-powered platform makes it easy to discover programs that match your child's interests, your schedule, and your location. We focus on finding mentors who not only teach robotics skills but also inspire creativity and teamwork.

To get started with personalized recommendations, I'd suggest completing our quick registration. This helps us understand your specific needs and preferences.

Would you like me to guide you to registration, or do you have questions about specific programs?""",
                "suggestions": [
                    "Tell me about program costs and schedules",
                    "How do I evaluate mentor quality?",
                    "What age groups do you serve?",
                    "Take me to registration"
                ],
                "context": "landing"
            }
        
        # Mentor-focused responses  
        if any(word in query_lower for word in ['mentor', 'teach', 'coach', 'lead', 'engineer']):
            return {
                "response": """Wonderful! We're always excited to connect with passionate educators and professionals who want to make a difference in students' lives.

MentorIQ is designed to save mentors like you 60%+ of administrative time through AI-powered tools, so you can focus on what matters most - inspiring and guiding your students.

Our platform helps you:
- Streamline team management and progress tracking
- Automate parent communications and scheduling
- Access resources and best practices from successful mentors
- Connect with families actively seeking quality mentoring

Whether you're looking to start your first FLL team or enhance an existing program, we provide the tools and community support you need.

Ready to get started with your mentor profile?""",
                "suggestions": [
                    "How does the platform save time?",
                    "What support do new mentors get?",
                    "Show me mentor success stories",
                    "Create my mentor profile"
                ],
                "context": "landing"
            }
        
        # Default landing response
        return {
            "response": """Welcome to MentorIQ! I'm here to help you discover amazing FLL programs and mentors.

Whether you're a parent looking for the perfect robotics program for your child, or a mentor ready to inspire the next generation of innovators, our AI-powered platform makes connections simple and effective.

What brings you to MentorIQ today?""",
            "suggestions": [
                "I'm a parent looking for programs",
                "I want to become a mentor",
                "Tell me about FLL and robotics",
                "How does your platform work?"
            ],
            "context": "landing"
        }
    
    async def _handle_registration_query(self, query: str, user_data: Optional[Dict]) -> Dict:
        """Handle registration assistance with field extraction"""
        
        response_data = {
            "response": "",
            "field_updates": {},
            "suggestions": [],
            "context": "registration"
        }
        
        # Extract potential field values
        name = self._extract_name(query)
        email = self._extract_email(query)
        user_type = self._extract_user_type(query)
        
        # Build response based on extracted information
        if name:
            response_data["field_updates"]["name"] = name
            response_data["response"] += f"Hi {name}! Great to meet you. "
            
        if email:
            response_data["field_updates"]["email"] = email
            domain = email.split('@')[1] if '@' in email else ''
            
            if '.edu' in domain:
                response_data["response"] += f"I see you're from an educational institution ({domain}) - that's wonderful! Many of our best mentors come from educational backgrounds. "
            else:
                response_data["response"] += f"Thanks for providing your email address! "
                
        if user_type:
            response_data["field_updates"]["userType"] = user_type
            
            if user_type == 'parent':
                response_data["response"] += "Wonderful! We're excited to help you find the perfect FLL program for your child. Our platform connects families with amazing mentors and teams in your area."
            elif user_type == 'mentor':
                response_data["response"] += "Fantastic! We need more passionate mentors like you. Whether you're looking to start a new team or join an existing program, our platform provides the tools and support you need."
        
        # If no specific information extracted, provide contextual guidance
        if not any([name, email, user_type]):
            if user_data and not user_data.get('name'):
                response_data["response"] = "I'd love to know what I should call you! What's your name?"
            elif user_data and user_data.get('name') and not user_data.get('email'):
                response_data["response"] = f"Thanks {user_data.get('name')}! I'll need your email address to create your account. What email should I use?"
            elif user_data and user_data.get('name') and user_data.get('email') and not user_data.get('userType'):
                response_data["response"] = "Perfect! Just one more thing - are you here as a parent looking for programs for your child, or as a mentor wanting to help with FLL teams?"
            else:
                response_data["response"] = "I'm here to help you complete your registration! You can either fill out the form on the left, or just tell me your information and I'll take care of it. What would you prefer?"
        
        return response_data
    
    def _extract_name(self, text: str) -> Optional[str]:
        """Extract name from natural language text"""
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
    
    def _extract_email(self, text: str) -> Optional[str]:
        """Extract email from text"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        match = re.search(email_pattern, text)
        return match.group(0) if match else None
    
    def _extract_user_type(self, text: str) -> Optional[str]:
        """Extract user type from text"""
        text_lower = text.lower()
        
        parent_keywords = ['parent', 'child', 'kid', 'son', 'daughter', 'family']
        mentor_keywords = ['mentor', 'teach', 'coach', 'lead', 'engineer', 'help']
        
        if any(keyword in text_lower for keyword in parent_keywords):
            return 'parent'
        elif any(keyword in text_lower for keyword in mentor_keywords):
            return 'mentor'
            
        return None

# Initialize AI service
ai_service = SimplifiedAI()

# API Endpoints
@app.post("/api/ai/chat/landing", response_model=AIResponse)
async def landing_chat(request: ChatRequest):
    """AI chat assistant for landing page program discovery"""
    try:
        logger.info(f"Landing chat query: {request.query}")
        
        response_data = await ai_service.get_contextual_response(
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

@app.post("/api/ai/chat/registration", response_model=RegistrationAIResponse)
async def registration_chat(request: RegistrationChatRequest):
    """AI chat assistant for bidirectional registration system"""
    try:
        logger.info(f"Registration chat query: {request.query}")
        
        response_data = await ai_service.get_contextual_response(
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

@app.get("/api/ai/health")
async def ai_health_check():
    """Health check endpoint for AI service"""
    try:
        # Test basic functionality
        test_response = await ai_service.get_contextual_response(
            query="test",
            page_context="landing"
        )
        
        return {
            "status": "healthy",
            "service": "MentorIQ AI Assistant",
            "model": "Simplified Pattern Matching",
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

@app.get("/api/ai/knowledge/summary")
async def get_knowledge_summary():
    """Get summary of platform knowledge available to AI"""
    try:
        knowledge_base = ai_service.knowledge_base
        
        return {
            "platform_info": knowledge_base["platform_info"]["name"],
            "mission": knowledge_base["platform_info"]["mission"],
            "current_features": list(knowledge_base["current_features"].keys()),
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
        "version": "1.1.0",
        "description": "AI-augmented mentor platform with intelligent responses",
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

if __name__ == "__main__":
    import uvicorn
    
    # Development server configuration
    uvicorn.run(
        "main-minimal:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )