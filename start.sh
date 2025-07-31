#!/bin/bash
# Railway start script for MentorIQ backend
uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}