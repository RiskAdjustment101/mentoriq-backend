# MentorIQ Backend - AI-Powered Mentor Platform

## Overview
FastAPI backend with Groq AI integration for ultra-fast intelligent responses.

## Features
- 🚀 Ultra-fast AI responses (<500ms) using Groq
- 🤖 Llama 3.3 70B model for superior understanding
- 💬 Context-aware conversations for landing and registration
- 🔄 Real-time field extraction from natural language

## API Endpoints
- `POST /api/ai/chat/landing` - AI assistance for program discovery
- `POST /api/ai/chat/registration` - Intelligent registration help
- `GET /api/ai/health` - Service health check
- `GET /api/ai/knowledge/summary` - Platform knowledge overview

## Environment Variables
```env
GROQ_API_KEY=your_groq_api_key
ALLOWED_ORIGINS=https://mentoriq.netlify.app
```

## Local Development
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python main-groq.py
```

## Deployment
Configured for Railway, Render, or any Python hosting platform.

## Tech Stack
- FastAPI for high-performance API
- Groq for ultra-fast AI inference
- Pydantic for data validation
- Python 3.11+