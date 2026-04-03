# AI Tutor Agent Configuration

from pydantic import BaseSettings
from typing import Optional, List


class Settings(BaseSettings):
    # LLM Settings
    llm_provider: str = "openai"  # openai, anthropic, local
    llm_model: str = "gpt-4o-mini"
    llm_api_key: Optional[str] = None
    
    # Whisper Settings
    whisper_model: str = "base"
    whisper_language: str = "ru"
    
    # Vector DB Settings
    vector_db_type: str = "faiss"  # faiss, chroma
    vector_db_path: str = "./data/vector_store"
    embedding_model: str = "all-MiniLM-L6-v2"
    
    # Database Settings
    db_url: str = "sqlite:///./data/user_data.db"
    
    # Processing Settings
    chunk_size: int = 1000
    chunk_overlap: int = 200
    max_tokens: int = 4096
    
    # Output Settings
    output_dir: str = "./output"
    anki_export_format: str = "apkg"
    
    # User Settings
    default_explanation_level: str = "simple"  # simple, child, expert
    
    class Config:
        env_prefix = "AI_TUTOR_"
        env_file = ".env"


settings = Settings()
