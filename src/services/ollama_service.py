"""
MentorIQ Ollama Integration Service
Provides intelligent AI responses trained on comprehensive platform knowledge
"""
import json
import logging
import re
from typing import Dict, List, Optional, Tuple
from datetime import datetime

# Note: This is a service template - actual Ollama integration would require:
# pip install ollama-python (when available) or direct HTTP requests
# from ollama import Ollama

logger = logging.getLogger(__name__)

class MentorIQOllamaService:
    """
    Intelligent AI service for MentorIQ platform using Ollama
    Trained on comprehensive platform knowledge and documentation
    """
    
    def __init__(self):
        # self.ollama = Ollama(base_url='http://localhost:11434')
        self.model = 'llama2:7b'
        self.knowledge_base = self._load_platform_knowledge()
        
    def _load_platform_knowledge(self) -> Dict:
        """Load structured knowledge from all platform documentation"""
        return {
            "platform_info": {
                "name": "MentorIQ",
                "mission": "AI-augmented mentor platform saving 60%+ administrative time",
                "vision": "Transform FIRST LEGO League mentoring through conversational AI",
                "approach": "Hybrid SaaS + conversational AI interface",
                "development_strategy": "Meta 0-to-1 methodology with rapid iteration"
            },
            
            "tech_stack": {
                "frontend": "React 18 + TypeScript + TailwindCSS + Vite",
                "backend": "Python 3.11 + FastAPI + PostgreSQL + SQLAlchemy",
                "ai_integration": "Ollama with Llama2:7b model",
                "state_management": "Zustand for React components",
                "design_system": "Anthropic UI (dark theme #0F172A, orange accents #FF6B35)",
                "hosting": "Netlify frontend, Python backend deployment"
            },
            
            "current_features": {
                "landing_page": {
                    "description": "AI-first program discovery interface",
                    "layout": "70/30 split-screen (content/AI chat)",
                    "capabilities": [
                        "Natural language program queries",
                        "Smart recommendations for parents and mentors",
                        "Multi-user conversational flows",
                        "Program matching with mentor profiles"
                    ],
                    "route": "/"
                },
                
                "registration": {
                    "description": "Revolutionary bidirectional registration system",
                    "innovation": "Real-time form ↔ chat synchronization",
                    "capabilities": [
                        "Dual interface registration (form OR chat)",
                        "Smart field extraction from natural language",
                        "Contextual responses based on email domains",
                        "Role-specific messaging for parents vs mentors",
                        "Progressive registration with completion tracking"
                    ],
                    "route": "/register"
                }
            },
            
            "user_types": {
                "parents": {
                    "primary_goal": "Find FLL programs for their children",
                    "pain_points": [
                        "Location-based program search",
                        "Mentor quality assessment",
                        "Program schedule compatibility",
                        "Cost and value comparison"
                    ],
                    "success_metrics": "Program enrollment, child satisfaction, skill development"
                },
                
                "mentors": {
                    "primary_goal": "Lead or assist with FLL teams effectively",
                    "pain_points": [
                        "Student progress tracking",
                        "Resource and scheduling management",
                        "Parent communication overhead",
                        "Competition preparation coordination"
                    ],
                    "success_metrics": "Team performance, mentor retention, time savings"
                }
            },
            
            "development_phases": {
                "phase_1": {
                    "status": "✅ Completed",
                    "title": "AI-First Landing Page",
                    "features": "Program discovery, conversational interface, Anthropic design"
                },
                "phase_1_5": {
                    "status": "✅ Current Implementation", 
                    "title": "Bidirectional Registration System",
                    "features": "Form-chat sync, field extraction, contextual AI responses"
                },
                "phase_2": {
                    "status": "🚧 Next: Weeks 5-8",
                    "title": "Core Mentor Platform",
                    "features": "Authentication, program management, mentor dashboard with AI"
                },
                "phase_2_5": {
                    "status": "📋 Planned",
                    "title": "Ollama Integration",
                    "features": "Replace pattern matching with intelligent AI across platform"
                }
            },
            
            "conversation_patterns": {
                "landing_page_queries": [
                    "Find robotics programs for my [age]-year-old near [location]",
                    "I'm an engineer wanting to start an FLL team in [location]",
                    "Show me [time] programs with experienced mentors",
                    "What programs are available for [experience_level] students?"
                ],
                
                "registration_assistance": [
                    "Guide user through name, email, user type collection",
                    "Extract information from natural language responses",
                    "Provide contextual encouragement based on role selection",
                    "Handle email domain detection (.edu, .com, etc.)",
                    "Offer role-specific value propositions"
                ]
            },
            
            "business_metrics": {
                "current_performance": {
                    "bundle_size": "177KB total (18KB increase from v1.0.0)",
                    "load_time": "<2 seconds globally",
                    "sync_speed": "<100ms bidirectional updates"
                },
                "success_targets": {
                    "registration_completion": ">90% (vs industry 60%)",
                    "user_satisfaction": ">85% helpful AI recommendations",
                    "time_to_complete": "<90 seconds average registration",
                    "mentor_time_savings": "60%+ administrative time reduction"
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
        """
        Generate intelligent response based on comprehensive platform knowledge
        
        Args:
            query: User's input message
            page_context: 'landing' or 'registration' 
            user_data: Current user context/form data
            conversation_history: Previous messages in conversation
            
        Returns:
            Dict with response, suggestions, and any field updates
        """
        if conversation_history is None:
            conversation_history = []
            
        try:
            # Build context-aware system prompt
            system_prompt = self._build_system_prompt(page_context, user_data)
            
            # Get relevant platform knowledge
            knowledge_context = self._get_relevant_knowledge(query, page_context)
            
            # For now, use enhanced pattern matching until Ollama is connected
            # This provides immediate functionality while maintaining the interface
            response_data = await self._generate_enhanced_response(
                query, page_context, user_data, knowledge_context
            )
            
            # TODO: Replace with actual Ollama integration
            # response = await self._call_ollama(system_prompt, knowledge_context, query)
            
            return response_data
            
        except Exception as e:
            logger.error(f"Error generating contextual response: {e}")
            return self._fallback_response(query, page_context)
    
    def _build_system_prompt(self, page_context: str, user_data: Optional[Dict]) -> str:
        """Build context-aware system prompt"""
        base_prompt = f"""You are an AI assistant for MentorIQ, an AI-augmented mentor platform for FIRST LEGO League programs.

Mission: {self.knowledge_base['platform_info']['mission']}
Vision: {self.knowledge_base['platform_info']['vision']}

Current Platform Status:
- Phase 1: AI-First Landing Page ✅ Completed
- Phase 1.5: Bidirectional Registration ✅ Current Implementation  
- Phase 2: Core Mentor Platform 🚧 Next

You provide helpful, accurate responses based on comprehensive platform knowledge."""

        if page_context == 'landing':
            return f"""{base_prompt}

CURRENT CONTEXT: Landing Page Program Discovery
Your role: Help users discover FLL programs through natural language queries.

Capabilities:
- Help parents find programs for their children
- Assist prospective mentors in finding opportunities  
- Provide program information (features, locations, schedules, pricing)
- Guide users toward registration when they're ready
- Share platform benefits and success stories

Always be encouraging and focus on the transformative impact of FLL participation."""

        elif page_context == 'registration':
            return f"""{base_prompt}

CURRENT CONTEXT: Bidirectional Registration System
Your role: Guide users through our innovative registration process.

Special Capabilities: 
- Extract structured information from natural language
- Provide contextual responses based on email domains
- Offer role-specific encouragement (Parent vs Mentor)
- Sync responses with form fields in real-time
- Handle both form-first and chat-first interaction flows

Current Registration Data: {json.dumps(user_data) if user_data else 'None yet'}"""

        return base_prompt
    
    def _get_relevant_knowledge(self, query: str, page_context: str) -> str:
        """Extract relevant platform knowledge based on query and context"""
        query_lower = query.lower()
        
        if page_context == 'landing':
            # Landing page knowledge
            knowledge_sections = []
            
            if any(word in query_lower for word in ['program', 'team', 'find', 'robotics']):
                knowledge_sections.append(f"""
PROGRAM DISCOVERY CONTEXT:
- Platform: {self.knowledge_base['platform_info']['name']} - AI-augmented mentor platform
- Current Feature: {self.knowledge_base['current_features']['landing_page']['description']}
- Layout: {self.knowledge_base['current_features']['landing_page']['layout']}
- User Types: Parents (finding programs) and Mentors (leading teams)
""")
            
            if any(word in query_lower for word in ['parent', 'child', 'kid', 'son', 'daughter']):
                parent_info = self.knowledge_base['user_types']['parents']
                knowledge_sections.append(f"""
PARENT USER CONTEXT:
- Primary Goal: {parent_info['primary_goal']}
- Common Concerns: {', '.join(parent_info['pain_points'])}
- Success Outcome: {parent_info['success_metrics']}
""")
                
            if any(word in query_lower for word in ['mentor', 'teach', 'coach', 'lead', 'engineer']):
                mentor_info = self.knowledge_base['user_types']['mentors']
                knowledge_sections.append(f"""
MENTOR USER CONTEXT:
- Primary Goal: {mentor_info['primary_goal']}
- Common Challenges: {', '.join(mentor_info['pain_points'])}
- Success Outcome: {mentor_info['success_metrics']}
- Platform Benefit: 60%+ administrative time savings
""")
                
            return '\n'.join(knowledge_sections)
            
        elif page_context == 'registration':
            # Registration-specific knowledge
            reg_info = self.knowledge_base['current_features']['registration']
            return f"""
REGISTRATION SYSTEM CONTEXT:
- Innovation: {reg_info['innovation']}  
- Capabilities: {', '.join(reg_info['capabilities'])}
- User Types Supported: Parents and Mentors only (no students in current phase)
- Success Target: >90% completion rate vs industry standard 60%
- Next Step: Access to mentor platform and program matching

FIELD EXTRACTION ABILITIES:
- Names: From patterns like "I'm [Name]", "My name is [Name]", or standalone names
- Emails: Automatic email detection with domain analysis
- User Types: Infer from context (parent/child keywords vs mentor/teach keywords)
"""
            
        return "General platform knowledge available for context."
    
    async def _generate_enhanced_response(
        self, 
        query: str, 
        page_context: str, 
        user_data: Optional[Dict],
        knowledge_context: str
    ) -> Dict:
        """Generate enhanced pattern-matched response with platform knowledge"""
        
        response_data = {
            "response": "",
            "suggestions": [],
            "field_updates": {},
            "context": page_context
        }
        
        if page_context == 'landing':
            response_data = await self._handle_landing_query(query, knowledge_context)
            
        elif page_context == 'registration':
            response_data = await self._handle_registration_query(query, user_data, knowledge_context)
            
        return response_data
    
    async def _handle_landing_query(self, query: str, knowledge_context: str) -> Dict:
        """Handle landing page program discovery queries"""
        query_lower = query.lower()
        
        # Parent-focused responses
        if any(word in query_lower for word in ['child', 'kid', 'son', 'daughter', 'parent']):
            if any(word in query_lower for word in ['find', 'program', 'team']):
                return {
                    "response": f"""Perfect! I'd love to help you find the ideal FLL program for your child. MentorIQ connects families with amazing mentors and teams in your area.

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
                "response": f"""Wonderful! We're always excited to connect with passionate educators and professionals who want to make a difference in students' lives.

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
        
        # General program inquiry
        if any(word in query_lower for word in ['program', 'team', 'robotics', 'fll']):
            return {
                "response": f"""Great question about FLL programs! MentorIQ connects you with high-quality FIRST LEGO League teams and mentors in your area.

Our platform features:
- AI-powered program matching based on your specific needs
- Detailed mentor profiles with backgrounds and success stories
- Transparent program information (schedules, costs, locations)
- Real-time availability and enrollment status

Programs typically run from September through February, with weekly sessions focused on:
- Robot building and programming
- Research project development
- Teamwork and presentation skills
- Competition preparation

To see programs specifically matched to your needs and location, registration takes just 2 minutes and unlocks personalized recommendations.

What specific aspects of FLL programs are you most curious about?""",
                "suggestions": [
                    "Show me programs in my area",
                    "What do programs typically cost?",
                    "How do I choose the right mentor?",
                    "Register for personalized matches"
                ],
                "context": "landing"
            }
        
        # Default landing response
        return {
            "response": f"""Welcome to MentorIQ! I'm here to help you discover amazing FLL programs and mentors.

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
    
    async def _handle_registration_query(self, query: str, user_data: Optional[Dict], knowledge_context: str) -> Dict:
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
            elif any(common in domain for common in ['gmail', 'yahoo', 'hotmail', 'outlook']):
                response_data["response"] += f"Thanks for providing your email address! "
            else:
                response_data["response"] += f"Great to have you joining from {domain}! "
                
        if user_type:
            response_data["field_updates"]["userType"] = user_type
            
            if user_type == 'parent':
                response_data["response"] += "Wonderful! We're excited to help you find the perfect FLL program for your child. Our platform connects families with amazing mentors and teams in your area, making it easy to discover opportunities that match your child's interests and your family's schedule."
            elif user_type == 'mentor':
                response_data["response"] += "Fantastic! We need more passionate mentors like you. Whether you're looking to start a new team or join an existing program, our platform provides the tools and community support to help you make a real impact on students' lives while saving you significant administrative time."
        
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
        
        # Add encouraging completion message if nearly done
        if user_data:
            completed_fields = sum(1 for v in user_data.values() if v)
            if completed_fields >= 2:
                response_data["response"] += "\n\nYou're almost done! Once registration is complete, you'll have access to personalized program recommendations and our full platform features."
        
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
    
    def _fallback_response(self, query: str, page_context: str) -> Dict:
        """Fallback response when AI service fails"""
        if page_context == 'landing':
            return {
                "response": "I'm here to help you discover FLL programs! Could you tell me more about what you're looking for?",
                "suggestions": ["Find programs for my child", "I want to become a mentor"],
                "context": "landing"
            }
        else:
            return {
                "response": "I'm here to help with your registration. What information can I help you with?",
                "field_updates": {},
                "context": "registration"
            }

# Singleton instance for use across the application
mentoriq_ai = MentorIQOllamaService()