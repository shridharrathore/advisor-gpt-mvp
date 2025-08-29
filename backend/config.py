from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional
from functools import lru_cache

class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # OpenAI Configuration
    openai_api_key: str = Field(default="", env="OPENAI_API_KEY", description="OpenAI API key")
    openai_model: str = Field(default="gpt-3.5-turbo", env="OPENAI_MODEL", description="OpenAI model to use")
    response_format: str = Field(default="", env="RESPONSE_FORMAT", description="Response format")
    
    # ChromaDB Configuration
    chroma_host: str = Field(default="localhost", env="CHROMA_HOST", description="ChromaDB host")
    chroma_port: int = Field(default=8000, env="CHROMA_PORT", description="ChromaDB port")
    chroma_collection_name: str = Field(default="advisor_gpt", env="CHROMA_COLLECTION", description="ChromaDB collection name")
    embedding_model: str = Field(default="all-MiniLM-L6-v2", env="EMBEDDING_MODEL", description="Sentence transformer model for embeddings")
    # Application Configuration
    environment: str = Field(default="development", env="ENVIRONMENT", description="Application environment")
    debug: bool = Field(default=False, env="DEBUG", description="Debug mode")
    log_level: str = Field(default="INFO", env="LOG_LEVEL", description="Logging level")
    
    # RAG Configuration
    chunk_size: int = Field(default=800, env="CHUNK_SIZE", description="Document chunk size")
    chunk_overlap: int = Field(default=120, env="CHUNK_OVERLAP", description="Document chunk overlap")
    top_k: int = Field(default=4, env="TOP_K", description="Number of documents to retrieve")
    min_score: float = Field(default=0.60, env="MIN_SCORE", description="Minimum similarity score")
    
    # Security Configuration
    secret_key: str = Field(default="dev-secret-key", env="SECRET_KEY", description="Application secret key")
    allowed_origins: list = Field(default=["http://localhost:3000"], env="ALLOWED_ORIGINS", description="CORS allowed origins")
    
    # Audit Configuration
    audit_log_path: str = Field(default="./logs/audit.jsonl", env="AUDIT_LOG_PATH", description="Audit log file path")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
