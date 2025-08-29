from pydantic_settings import BaseSettings
from pydantic import BaseModel, Field, validator
from typing import List, Optional
from enum import Enum

class FeedbackType(str, Enum):
    """Enum for feedback types."""
    LIKE = "like"
    DISLIKE = "dislike"

class QueryRequest(BaseSettings):
    """Request model for agent queries."""
    query: str = Field(..., min_length=1, description="The agent's query")
    case_id: str = Field(..., description="Case ID for tracking")
    agent_id: str = Field(..., description="Agent identifier")
    filters: Optional[dict] = Field(default=None, description="Optional filters for retrieval")

class QueryResponse(BaseSettings):
    """Response model following RAG contract specifications."""
    answer: str = Field(..., description="Generated answer")
    steps: List[str] = Field(..., description="Step-by-step guidance")
    cited_spans: List[str] = Field(..., description="Citations and source references")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score between 0 and 1")
    disclaimers: List[str] = Field(..., description="Important disclaimers and warnings")
    response_id: Optional[str] = Field(default=None, description="Unique response identifier")
    
    @validator('confidence')
    def validate_confidence(cls, v):
        if not 0.0 <= v <= 1.0:
            raise ValueError('Confidence must be between 0.0 and 1.0')
        return v

class FeedbackRequest(BaseSettings):
    """Request model for agent feedback."""
    response_id: str = Field(..., description="ID of the response being rated")
    feedback_type: FeedbackType = Field(..., description="Type of feedback: like or dislike")
    reason: Optional[str] = Field(default=None, description="Optional reason for feedback")
    agent_id: str = Field(..., description="Agent providing feedback")
    edited_response: Optional[str] = Field(default=None, description="Agent's edited version if applicable")

class UserFeedbackRequest(BaseModel):
    """Request model for user feedback on responses."""
    response_id: str = Field(..., description="ID of the response being rated")
    case_id: str = Field(..., description="Case ID for tracking")
    agent_id: str = Field(..., description="Agent identifier")
    feedback_type: FeedbackType = Field(..., description="Type of feedback (like/dislike)")
    comment: Optional[str] = Field(default=None, description="Optional feedback comment")

class AuditLog(BaseSettings):
    """Audit log model for response tracking."""
    response_id: str = Field(..., description="Unique response identifier")
    query: str = Field(..., description="Original query")
    agent_id: str = Field(..., description="Agent identifier")
    case_id: str = Field(..., description="Case identifier")
    confidence: float = Field(..., description="Response confidence")
    latency_ms: int = Field(..., description="Response latency in milliseconds")
    model_version: str = Field(..., description="Model version used")
    prompt_version: str = Field(..., description="Prompt version used")
    outcome: Optional[str] = Field(default=None, description="Response outcome (accepted/edited/rejected)")
    timestamp: str = Field(..., description="ISO timestamp")

class HealthResponse(BaseSettings):
    """Health check response model."""
    status: str = Field(..., description="Service status")
    service: str = Field(..., description="Service name")

class ChunkMetadata(BaseSettings):
    """Chunk Metadata Model"""
    product: str = Field(..., description="Product name")
    product_category: str = Field(..., description="Product category (e.g., pumps, valves, motors)")
    doc_type: str = Field(..., description="Document type")
    section_id: str = Field(..., description="Document section identifier")
    severity_level: Optional[str] = Field(default=None, description="Issue severity: critical, moderate, minor")
    applicable_models: List[str] = Field(default=[], description="Compatible product models")
    source_file: str = Field(..., description="Source file name")
    chunk_id: str = Field(..., description="Chunk identifier")
    chunk_size: int = Field(..., description="Chunk size")
    chunk_overlap: int = Field(..., description="Chunk overlap")
    timestamp: str = Field(..., description="ISO timestamp")

class DocumentChunk(BaseSettings):
    """Document Chunk Model"""
    text: str = Field(..., description="Document chunk text")
    metadata: ChunkMetadata = Field(..., description="Chunk metadata")
