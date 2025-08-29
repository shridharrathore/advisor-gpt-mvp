from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend import chroma_service
from backend.models import QueryRequest, UserFeedbackRequest
from backend.rag_orchestrator import orchestrationservice
from backend.chroma_service import ChromaService
from backend.openaiservice import openaiservice
from backend.config import get_settings
from backend.model_performance_service import ModelPerformanceService

app = FastAPI(
    title="Advisor GPT API",
    description="A chatbot assistant for customer support agents in B2B Manufacturing Company. Provides guided responses with citations for technical troubleshooting, warranty claims, and return policies.",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=False,  # Set to False when using allow_origins=["*"]
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    """Health check endpoint."""        
    return {"status": "healthy", "service": "advisor-gpt-api"}

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Advisor GPT API", "version": "1.0.0"}

@app.post("/query")
async def query(query: QueryRequest):
    """Query endpoint."""
    settings = get_settings()
    chroma_service = ChromaService(settings)
    openai_service = openaiservice(settings)
    orchestrator = orchestrationservice(chroma_service, openai_service, settings)
    response = orchestrator.process_query(query.query)
    return response

@app.post("/feedback")
async def submit_feedback(feedback: UserFeedbackRequest):
    """Submit user feedback for response quality metrics."""
    # TODO: Store feedback in database for analytics
    # For now, just log the feedback
    print(f"📊 Feedback received: {feedback.feedback_type} for response {feedback.response_id}")
    print(f"   Case: {feedback.case_id}, Agent: {feedback.agent_id}")
    chroma_service = ChromaService(get_settings())
    chroma_service.submit_feedback(feedback)
    
    return {"status": "success", "message": "Feedback recorded successfully"}

@app.get("/feedback")
async def get_all_feedback():
    chroma_service = ChromaService(get_settings())
    return chroma_service.get_all_feedback()

@app.get("/performance")
async def get_model_performance():
    settings = get_settings()
    settings.chroma_collection_name = "feedback_db"
    modelperformance_service = ModelPerformanceService(settings)    
    feedback = modelperformance_service.get_model_performance()
    return feedback
