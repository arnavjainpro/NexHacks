"""
Configuration Management for Veritas
Loads environment variables and provides application settings
"""

from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # API Keys
    OPENAI_API_KEY: str = ""
    ELEVENLABS_API_KEY: str = ""
    LIVEKIT_API_KEY: str = ""
    LIVEKIT_API_SECRET: str = ""
    LIVEKIT_URL: str = "wss://localhost:7880"
    TOKEN_COMPANY_API_KEY: str = ""
    TOKEN_COMPANY_BASE_URL: str = "https://api.thetokencompany.com/v1"
    
    # Database
    DATABASE_URL: str = "postgresql://localhost:5432/veritas"
    REDIS_URL: str = "redis://localhost:6379"
    
    # Application
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "DEBUG"
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    SECRET_KEY: str = "your-secret-key-change-in-production"
    
    # Privacy & Compliance Settings
    MAX_AUDIO_RETENTION_SECONDS: int = 0  # 0 means immediate deletion
    ENABLE_SLIDING_WINDOW: bool = True
    WINDOW_SIZE_SECONDS: int = 30  # Keep last 30 seconds in memory
    
    # Real-time Processing
    AUDIO_SAMPLE_RATE: int = 16000
    AUDIO_CHUNK_DURATION_MS: int = 100
    TRANSCRIPTION_PROVIDER: str = "whisper"  # or "deepgram"
    
    # Compliance Engine
    COMPLIANCE_CHECK_THRESHOLD: float = 0.7  # Confidence threshold for flagging
    ENABLE_REAL_TIME_CHECKS: bool = True
    
    # Training Mode
    TRAINING_DIFFICULTY_LEVELS: List[str] = ["beginner", "intermediate", "expert"]
    DEFAULT_AI_VOICE_ID: str = "default"  # ElevenLabs voice ID
    
    # Performance
    MAX_CONCURRENT_SESSIONS: int = 100
    RESPONSE_TIMEOUT_SECONDS: int = 5
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()


# Validate critical settings
def validate_settings():
    """Validate that critical settings are properly configured"""
    required_for_production = [
        "OPENAI_API_KEY",
        "ELEVENLABS_API_KEY",
        "LIVEKIT_API_KEY",
        "LIVEKIT_API_SECRET",
    ]
    
    if settings.ENVIRONMENT == "production":
        missing = [key for key in required_for_production if not getattr(settings, key)]
        if missing:
            raise ValueError(f"Missing required settings for production: {', '.join(missing)}")


if __name__ == "__main__":
    # Test settings loading
    print("Veritas Configuration:")
    print(f"Environment: {settings.ENVIRONMENT}")
    print(f"Log Level: {settings.LOG_LEVEL}")
    print(f"Privacy Mode: Sliding Window={settings.ENABLE_SLIDING_WINDOW}")
    print(f"Audio Retention: {settings.MAX_AUDIO_RETENTION_SECONDS}s")
    validate_settings()
