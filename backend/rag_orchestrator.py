"""UI Query --> Main --> Orchestrator --> Chunking --> Orchestrator --> Chromadb --> Orchestrator --> OpenAI --> Orchestrator --> Main --> UI"""
import logging
from backend.models import QueryResponse
from backend.openaiservice import  openaiservice 
from backend.chroma_service import ChromaService
from backend.config import Settings
from typing import List

class orchestrationservice: 
    system_message = "You are a helpful assistant that helps customer support agent of a "
    system_message += "large B2B manufacturing company to help answer queries of its customers related to troubleshooting "
    system_message += "of parts and warranty claims. You will be provided with relevant information related to query if found. "
    system_message += "Please respond in JSON format in this structure: "
    
   
    def __init__(self, vectorDbService:  ChromaService, llmService: openaiservice, settings: Settings):
        self.logger = logging.getLogger(__name__)
        self.vector_db_service = vectorDbService
        self.llm_service = llmService
        self.settings = settings

    def process_query(self, query: str):
       relevant_documents = self._get_relevant_documents(query)
       
      
       if not relevant_documents:
           print("No relevant documents found, using fallback response")
           return self._get_fallback_response(query)
       
       response = self._get_response_openai(query, relevant_documents)
       return response
    
    def _get_relevant_documents(self, query: str):
        vectordb_service = self.vector_db_service
        return vectordb_service.search(query)
    
    def _get_response_openai(self, query: str, relevant_documents: List[str]):
       user_prompt = self._build_user_prompt(query, relevant_documents)
       system_prompt = self.system_message + "\n\n" + self.settings.response_format
       openai_service = self.llm_service
       
       # Get the response from OpenAI
       openai_response = openai_service.generate_response(user_prompt, system_prompt)
       
       # Handle both string and structured responses from OpenAI
       if isinstance(openai_response, str):
           # Simple text response
           formatted_response = {
               "response": openai_response,
               "sources": [{"document": f"Technical Document {i+1}", "content": doc[:200] + "..."} for i, doc in enumerate(relevant_documents[:3])],
               "response_id": f"response_{hash(query) % 10000}",
               "confidence": 0.8
           }
       else:
           # Structured response - map fields correctly
           formatted_response = {
               "response": openai_response.get("answer", openai_response.get("response", "No response available")),
               "steps": openai_response.get("steps", []),
               "sources": [{"document": f"Technical Document {i+1}", "content": doc[:200] + "..."} for i, doc in enumerate(relevant_documents[:3])],
               "confidence": int(openai_response.get("confidence", 0.8) * 100),  # Convert to percentage
               "disclaimers": openai_response.get("disclaimers", []),
               "response_id": f"response_{hash(query) % 10000}"
           }
       
       return formatted_response
    
    def _build_user_prompt(self, query: str, relevant_documents: List[str]):
            context = "\n\n".join(relevant_documents)
            user_prompt = query + "\n\n" + context
            return user_prompt

    def _get_fallback_response(self, query: str):
        """
        Provides a fallback response when no relevant documents are found.
        This is important for user experience - never leave users hanging!
        """
        fallback_message = f"""I apologize, but I couldn't find specific information in our technical documentation to answer your question about: "{query}"

However, I can provide some general guidance:

**For Manufacturing Equipment Issues:**
1. Check the equipment manual for troubleshooting steps
2. Verify all connections and power supply
3. Review recent maintenance logs
4. Contact technical support with specific error codes

**For HydroMax Pump Issues:**
1. Check inlet/outlet pressures
2. Inspect for blockages or leaks
3. Verify electrical connections
4. Review pump specifications vs. operating conditions

**Next Steps:**
- Please provide more specific details about the issue
- Include any error codes or symptoms
- Consider escalating to Level 2 technical support

Would you like to rephrase your question or provide additional details?"""

        return {
            "response": fallback_message,
            "sources": [],
            "confidence": 0.1,  # Low confidence for fallback
            "response_id": f"fallback_{hash(query) % 10000}"
        }
