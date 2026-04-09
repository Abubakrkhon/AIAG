"""Interview.ai - Voice AI Hiring Screener for SMBs"""

__version__ = "1.0.0"
__author__ = "Interview.ai Team"

from app.main import app
from app.voice_agent.agent import VoiceAgent, InterviewResult
from app.voice_agent.prompts import get_template, list_templates, InterviewTemplate
from app.database.models import Customer, Candidate, Interview

__all__ = [
    "app",
    "VoiceAgent",
    "InterviewResult",
    "get_template",
    "list_templates",
    "InterviewTemplate",
    "Customer",
    "Candidate",
    "Interview",
]
