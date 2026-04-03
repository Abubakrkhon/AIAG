"""
AI Tutor Agent - Main Package
Professional AI-powered learning assistant
"""

__version__ = "1.0.0"
__author__ = "AI Tutor Team"

from .core.preprocessor import TextPreprocessor, TextChunk
from .memory.vector_memory import VectorMemory, UserMemory
from .agents.reader_agent import ReaderAgent
from .agents.teacher_agent import TeacherAgent
from .agents.examiner_agent import ExaminerAgent
from .agents.anki_agent import AnkiAgent
from .agents.orchestrator_agent import OrchestratorAgent
from .parsers.pdf_parser import PDFParser
from .parsers.youtube_parser import YouTubeParser
from .parsers.audio_parser import AudioParser
from .parsers.ocr_parser import OCRParser


def create_tutor(llm_client) -> OrchestratorAgent:
    """
    Factory function to create the main tutor agent
    
    Args:
        llm_client: configured LLM client (OpenAI, Anthropic, etc.)
        
    Returns:
        OrchestratorAgent instance
    """
    return OrchestratorAgent(llm_client)


def create_parsers(whisper_model: str = "base") -> dict:
    """
    Factory function to create all parsers
    
    Args:
        whisper_model: Whisper model name for audio processing
        
    Returns:
        Dict of parser instances
    """
    return {
        'pdf': PDFParser(),
        'youtube': YouTubeParser(whisper_model=whisper_model),
        'audio': AudioParser(model_name=whisper_model),
        'ocr': OCRParser()
    }


__all__ = [
    # Main factory functions
    'create_tutor',
    'create_parsers',
    
    # Agents
    'OrchestratorAgent',
    'ReaderAgent',
    'TeacherAgent',
    'ExaminerAgent',
    'AnkiAgent',
    
    # Parsers
    'PDFParser',
    'YouTubeParser',
    'AudioParser',
    'OCRParser',
    
    # Core
    'TextPreprocessor',
    'TextChunk',
    
    # Memory
    'VectorMemory',
    'UserMemory'
]
