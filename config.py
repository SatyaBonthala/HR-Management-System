"""
Configuration settings for the HR Management System
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Application
    APP_NAME: str = "Agentic HR Management System"
    DEBUG: bool = True
    SECRET_KEY: str = "your-secret-key-change-in-production"
    
    # Database
    DATABASE_URL: str = "postgresql://username:password@localhost:5432/hr_management"
    
    # Groq API
    GROQ_API_KEY: str
    
    # AI Agent Configuration (Groq models)
    RECRUITMENT_AGENT_MODEL: str = "llama-3.3-70b-versatile"
    ONBOARDING_AGENT_MODEL: str = "llama-3.3-70b-versatile"
    AGENT_TEMPERATURE: float = 0.7
    AGENT_MAX_TOKENS: int = 2000
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create global settings instance
settings = Settings()
