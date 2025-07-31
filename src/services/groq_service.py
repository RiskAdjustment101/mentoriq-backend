"""
MentorIQ Groq Integration Service
Provides intelligent AI responses using Groq's ultra-fast LLM API
Trained on comprehensive platform knowledge for superior performance
"""
import json
import logging
import re
import os
from typing import Dict, List, Optional
from datetime import datetime
from groq import Groq

logger = logging.getLogger(__name__)

class MentorIQGroqService:
    """
    Intelligent AI service for MentorIQ platform using Groq
    Leverages Groq's ultra-fast inference for real-time conversational AI
    """
    
    def __init__(self):
        # Initialize Groq client
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            logger.warning("GROQ_API_KEY not found - using fallback responses")
            self.client = None
        else:
            self.client = Groq(api_key=api_key)
        
        self.model = "llama-3.3-70b-versatile"  # Groq's most capable model (Llama 3.3 70B)
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
                "backend": "Python 3.11 + FastAPI + Groq AI integration",
                "ai_service": "Groq with Llama 3.3 70B model (most capable, ultra-fast)",
                "state_management": "Zustand for React components",
                "design_system": "Anthropic UI (dark theme #0F172A, orange accents #FF6B35)",
                "hosting": "Netlify frontend, Railway/Render backend"
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
                    "success_metrics": "Team performance, mentor retention, 60%+ time savings"
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
                    "response_time": "<500ms with Groq integration",
                    "accuracy": ">95% intent recognition",
                    "completion_rate": ">90% registration completion"
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
        Generate intelligent response using Groq's ultra-fast LLM
        
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
            if self.client:
                # Use Groq for intelligent responses
                response_data = await self._generate_groq_response(
                    query, page_context, user_data, conversation_history
                )
            else:
                # Fallback to enhanced pattern matching
                response_data = await self._generate_fallback_response(
                    query, page_context, user_data
                )
            
            return response_data
            
        except Exception as e:
            logger.error(f"Error generating contextual response: {e}")
            return self._emergency_fallback(query, page_context)
    
    async def _generate_groq_response(
        self, 
        query: str, 
        page_context: str, 
        user_data: Optional[Dict],
        conversation_history: List[Dict]
    ) -> Dict:
        """Generate response using Groq's ultra-fast LLM"""
        
        # Build context-aware system prompt
        system_prompt = self._build_system_prompt(page_context, user_data)
        
        # Get relevant platform knowledge
        knowledge_context = self._get_relevant_knowledge(query, page_context)
        
        # Build conversation context
        messages = [
            {"role": "system", "content": f"{system_prompt}\n\nPLATFORM KNOWLEDGE:\n{knowledge_context}"}
        ]
        
        # Add conversation history
        for msg in conversation_history[-3:]:  # Last 3 messages for context
            role = "assistant" if msg.get("sender") == "ai" else "user"
            messages.append({"role": role, "content": msg.get("content", "")})
        
        # Add current query
        messages.append({"role": "user", "content": query})
        
        try:
            # Call Groq API
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=500,
                top_p=1,
                stream=False
            )
            
            ai_response = completion.choices[0].message.content
            
            # Extract field updates for registration context
            field_updates = {}
            if page_context == 'registration':
                field_updates = self._extract_fields_from_query(query)
            
            # Generate contextual suggestions
            suggestions = self._generate_suggestions(query, page_context, ai_response)
            
            return {
                "response": ai_response,
                "context": page_context,
                "suggestions": suggestions,
                "field_updates": field_updates
            }
            
        except Exception as e:
            logger.error(f"Groq API error: {e}")
            # Fallback to pattern matching
            return await self._generate_fallback_response(query, page_context, user_data)
    
    def _build_system_prompt(self, page_context: str, user_data: Optional[Dict]) -> str:
        """Build context-aware system prompt for Groq"""
        base_prompt = f"""You are an AI assistant for MentorIQ, an AI-augmented mentor platform for FIRST LEGO League programs.

PLATFORM OVERVIEW:
- Mission: {self.knowledge_base['platform_info']['mission']}
- Vision: {self.knowledge_base['platform_info']['vision']}
- Approach: Hybrid SaaS + conversational AI interface

RESPONSE GUIDELINES:
- Be encouraging, helpful, and knowledgeable about FLL programs
- Keep responses conversational but informative
- Focus on guiding users toward their goals (program discovery or registration)
- Use platform-specific knowledge to provide accurate information
- Be concise but comprehensive (2-4 sentences typically)"""

        if page_context == 'landing':
            return f"""{base_prompt}

CURRENT CONTEXT: Landing Page Program Discovery
Your role: Help users discover FLL programs through natural language queries.

KEY CAPABILITIES:
- Help parents find programs for their children
- Assist prospective mentors in finding opportunities
- Provide program information (features, locations, schedules, pricing)
- Guide users toward registration when they're ready
- Share platform benefits and success stories

TONE: Enthusiastic about FLL education, supportive for families, encouraging for mentors."""

        elif page_context == 'registration':
            return f"""{base_prompt}

CURRENT CONTEXT: Bidirectional Registration System
Your role: Guide users through our innovative registration process.

SPECIAL CAPABILITIES:
- Extract structured information from natural language
- Provide contextual responses based on email domains
- Offer role-specific encouragement (Parent vs Mentor)
- Help users complete registration through conversation

CURRENT USER DATA: {json.dumps(user_data) if user_data else 'None yet'}

TONE: Helpful, encouraging, professional. Make registration feel easy and exciting."""

        return base_prompt
    
    def _get_relevant_knowledge(self, query: str, page_context: str) -> str:
        """Extract relevant platform knowledge based on query and context"""
        query_lower = query.lower()
        knowledge_sections = []
        
        if page_context == 'landing':
            # Landing page knowledge
            if any(word in query_lower for word in ['program', 'team', 'find', 'robotics']):
                landing_info = self.knowledge_base['current_features']['landing_page']
                knowledge_sections.append(f"""
PROGRAM DISCOVERY:
- Platform: {self.knowledge_base['platform_info']['name']}
- Feature: {landing_info['description']}
- Layout: {landing_info['layout']}
- Capabilities: {', '.join(landing_info['capabilities'])}""")
            
            if any(word in query_lower for word in ['parent', 'child', 'kid']):
                parent_info = self.knowledge_base['user_types']['parents']
                knowledge_sections.append(f"""
PARENT USER CONTEXT:
- Goal: {parent_info['primary_goal']}
- Common Concerns: {', '.join(parent_info['pain_points'])}
- Success Outcome: {parent_info['success_metrics']}""")
                
            if any(word in query_lower for word in ['mentor', 'teach', 'coach', 'engineer']):
                mentor_info = self.knowledge_base['user_types']['mentors']
                knowledge_sections.append(f"""
MENTOR USER CONTEXT:
- Goal: {mentor_info['primary_goal']}
- Platform Benefit: {mentor_info['success_metrics']}
- Time Savings: 60%+ administrative time reduction""")
                
        elif page_context == 'registration':
            reg_info = self.knowledge_base['current_features']['registration']
            knowledge_sections.append(f"""
REGISTRATION SYSTEM:
- Innovation: {reg_info['innovation']}
- Capabilities: {', '.join(reg_info['capabilities'])}
- Target: >90% completion rate vs industry 60%""")
            
        return '\n'.join(knowledge_sections) if knowledge_sections else "General MentorIQ platform knowledge available."
    
    def _extract_fields_from_query(self, query: str) -> Dict:
        """Extract registration fields from natural language query"""
        field_updates = {}
        
        # Extract name
        name = self._extract_name(query)
        if name:
            field_updates["name"] = name
            
        # Extract email
        email = self._extract_email(query)
        if email:
            field_updates["email"] = email
            
        # Extract user type
        user_type = self._extract_user_type(query)
        if user_type:
            field_updates["userType"] = user_type
            
        return field_updates
    
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
    
    def _generate_suggestions(self, query: str, page_context: str, ai_response: str) -> List[str]:
        """Generate contextual follow-up suggestions"""
        if page_context == 'landing':
            query_lower = query.lower()
            if any(word in query_lower for word in ['parent', 'child']):
                return [
                    "Tell me about program costs and schedules",
                    "How do I evaluate mentor quality?",
                    "What age groups do you serve?",
                    "Take me to registration"
                ]
            elif any(word in query_lower for word in ['mentor', 'teach']):
                return [
                    "How does the platform save time?",
                    "What support do new mentors get?",
                    "Show me mentor success stories",
                    "Create my mentor profile"
                ]
            else:
                return [
                    "I'm a parent looking for programs",
                    "I want to become a mentor",
                    "Tell me about FLL and robotics",
                    "How does your platform work?"
                ]
        
        return []
    
    async def _generate_fallback_response(
        self, 
        query: str, 
        page_context: str, 
        user_data: Optional[Dict]
    ) -> Dict:
        """Enhanced fallback response when Groq is unavailable"""
        
        if page_context == 'landing':
            return await self._handle_landing_fallback(query)
        elif page_context == 'registration':
            return await self._handle_registration_fallback(query, user_data)
        
        return self._emergency_fallback(query, page_context)
    
    async def _handle_landing_fallback(self, query: str) -> Dict:
        """Fallback for landing page queries"""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['parent', 'child', 'kid']):
            return {
                "response": """Perfect! I'd love to help you find the ideal FLL program for your child. MentorIQ connects families with amazing mentors and teams in your area.

Our AI-powered platform makes it easy to discover programs that match your child's interests, your schedule, and your location. We focus on finding mentors who not only teach robotics skills but also inspire creativity and teamwork.

To get started with personalized recommendations, I'd suggest completing our quick registration. This helps us understand your specific needs and preferences.""",
                "suggestions": [
                    "Tell me about program costs and schedules",
                    "How do I evaluate mentor quality?",
                    "What age groups do you serve?",
                    "Take me to registration"
                ],
                "context": "landing"
            }
        
        if any(word in query_lower for word in ['mentor', 'teach', 'engineer']):
            return {
                "response": """Wonderful! We're always excited to connect with passionate educators and professionals who want to make a difference in students' lives.

MentorIQ is designed to save mentors like you 60%+ of administrative time through AI-powered tools, so you can focus on what matters most - inspiring and guiding your students.

Whether you're looking to start your first FLL team or enhance an existing program, we provide the tools and community support you need.""",
                "suggestions": [
                    "How does the platform save time?",
                    "What support do new mentors get?",
                    "Show me mentor success stories",
                    "Create my mentor profile"
                ],
                "context": "landing"
            }
        
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
    
    async def _handle_registration_fallback(self, query: str, user_data: Optional[Dict]) -> Dict:
        """Fallback for registration queries"""
        response_data = {
            "response": "",
            "field_updates": {},
            "suggestions": [],
            "context": "registration"
        }
        
        # Extract fields
        name = self._extract_name(query)
        email = self._extract_email(query)
        user_type = self._extract_user_type(query)
        
        if name:
            response_data["field_updates"]["name"] = name
            response_data["response"] += f"Hi {name}! Great to meet you. "
            
        if email:
            response_data["field_updates"]["email"] = email
            domain = email.split('@')[1] if '@' in email else ''
            if '.edu' in domain:
                response_data["response"] += f"I see you're from an educational institution ({domain}) - wonderful! "
            else:
                response_data["response"] += "Thanks for providing your email address! "
                
        if user_type:
            response_data["field_updates"]["userType"] = user_type
            if user_type == 'parent':
                response_data["response"] += "Wonderful! We're excited to help you find the perfect FLL program for your child."
            elif user_type == 'mentor':
                response_data["response"] += "Fantastic! We need more passionate mentors like you."
        
        if not response_data["response"]:
            response_data["response"] = "I'm here to help you complete your registration! You can either fill out the form on the left, or just tell me your information and I'll take care of it."
        
        return response_data
    
    def _emergency_fallback(self, query: str, page_context: str) -> Dict:
        """Emergency fallback when all else fails"""
        return {
            "response": "I'm here to help! Could you tell me more about what you're looking for?",
            "suggestions": ["Find programs for my child", "I want to become a mentor"],
            "context": page_context,
            "field_updates": {}
        }

# Singleton instance for use across the application
mentoriq_groq_ai = MentorIQGroqService()