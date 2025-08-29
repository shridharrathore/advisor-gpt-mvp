#  Manufacturing Support Assistant

A smart AI-powered support system that helps manufacturing teams troubleshoot equipment issues faster and more effectively. Think of it as having an expert technician available 24/7 who knows all your technical documentation by heart.

## What Does It Do?

 This system ingests your technical manuals, troubleshooting guides, and maintenance docs, then provides instant, step-by-step guidance when things go wrong. It helps customer service agents to effectively answer technical troubleshooting questions from the customer.

**Key Features:**
- **Smart Search**: Ask questions in plain English, get precise technical answers
- **Step-by-Step Guidance**: Structured troubleshooting with numbered action items
- **Performance Tracking**: See how well the system is helping your team
- **Feedback Loop**: Thumbs up/down to continuously improve responses
- **Case Management**: Track support requests with case and agent IDs

## How It Works

1. **Upload Your Docs**: Feed the system your technical manuals (we used HydroMax 2000 pump docs as an example)
2. **Ask Questions**: Support agents type issues like "HydroMax 2000 has low flow rate"
3. **Get Smart Answers**: The system provides structured responses with confidence scores
4. **Track Performance**: Analytics dashboard shows satisfaction rates and helpful responses

## Tech Stack

**Backend:**
- Python + FastAPI 
- ChromaDB (vector database for semantic search)
- OpenAI GPT (for intelligent responses)
- Pydantic 

**Frontend:**
- Vanilla HTML/CSS/JavaScript 
- Modern responsive design
- Real-time analytics dashboard

## Quick Start

### Prerequisites
- Python 3.9+
- OpenAI API key
- A few technical documents to get started

# Instructions for running the code

1. **Start the server**
   
   uvicorn backend.main:app --reload --port 8002
   

2. **Open the frontend**
   ``
   # Open frontend/index.html in your browser
 
   ```

## Sample Queries 

- "HydroMax 2000 pump has reduced flow rate and low discharge pressure"
- "HM-2000 operating point left of BEP with high power consumption"
- "HydroMax impeller wear exceeds 0.030 inches replacement procedure"

## Project Structure

```
advisor-gpt-mvp/
├── backend/
│   ├── main.py                 # FastAPI server
│   ├── rag_orchestrator.py     # Main RAG logic
│   ├── chroma_service.py       # Vector database operations
│   ├── data_processor.py       # Document ingestion
│   ├── model_performance_service.py  # Analytics
│   └── data/                   # Your technical documents
├── frontend/
│   ├── index.html             # Main interface
│   ├── script.js              # Frontend logic
│   └── styles.css             # Styling
└── docs/                      # Project documentation
```

## API Endpoints

- `POST /query` - Submit technical questions
- `POST /feedback` - Submit thumbs up/down feedback
- `GET /performance` - Get analytics data
- `GET /health` - System health check

## Analytics Dashboard

Click the "📊 Analytics" button to see:
- **Satisfaction Rate**: Percentage of helpful responses
- **Total Responses**: How many questions answered
- **Recent Feedback**: Latest positive feedback from agents


   ```
3. Run `python -m backend.data_processor` to ingest

## Why We Built This

Manufacturing support teams deal with complex equipment and scattered documentation. When something breaks, finding the right information quickly can mean the difference between a 5-minute fix and hours of downtime.

This system brings all that knowledge together in one place, making it searchable and actionable. Plus, the feedback system means it gets smarter over time.
