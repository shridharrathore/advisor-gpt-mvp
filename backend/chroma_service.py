from ast import Not
import chromadb
from chromadb.config import Settings as ChromaSettings
from backend.config import Settings
import logging
from chromadb.utils import embedding_functions
from backend.models import DocumentChunk, UserFeedbackRequest
import time

class ChromaService:
    def __init__(self, settings: Settings):
        self.logger = logging.getLogger(__name__)

        # Initialize ChromaDb Client
        try:
            self.client = chromadb.HttpClient(host = settings.chroma_host, port = settings.chroma_port)
        except Exception as e:
            self.logger.error(f"Failed to initialize ChromaDB client: {str(e)}")
            raise
        self.settings = settings
        #Set up collection
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=settings.embedding_model)
        self.collection = self.client.get_or_create_collection(
            name=settings.chroma_collection_name, 
            embedding_function=self.embedding_function)

        
        #Configure Logging
        self.logger.log(logging.INFO, "ChromaDB initialized successfully")
        
    def get_collection(self):
        #Get or create collection
        return self.collection    

    def add_chunks(self, chunk):
        collection = self.get_collection()
        
        # Convert metadata to ChromaDB-compatible format
        metadata_dict = chunk.metadata.dict()
        
        # Convert list fields to comma-separated strings for ChromaDB compatibility
        if isinstance(metadata_dict.get('applicable_models'), list):
            metadata_dict['applicable_models'] = ', '.join(metadata_dict['applicable_models']) if metadata_dict['applicable_models'] else 'Unknown'
        
        collection.add(
            documents=[chunk.text],
            metadatas=[metadata_dict],
            ids=[chunk.metadata.chunk_id]
        )

    def search(self, query):
        collection = self.get_collection()

        if collection.count() == 0:
            print("Collection is empty")
            return []

        results = collection.query(
            query_texts=[query],
            n_results=self.settings.top_k,
            include=["documents", "distances"]
            )
        filtered_results = []
        # distances[0] contains the list of distances for the first query
        distances = results["distances"][0]
        documents = results["documents"][0]
        
        for i, distance in enumerate(distances):
            if distance < self.settings.min_score:
                filtered_results.append(documents[i])
        return filtered_results
    
    def health_check(self):
        #Test connection to chroma db
        try:
            timestamp = self.client.heartbeat()
            return {"status": "healthy", "timestamp": timestamp}
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}
    
    def submit_feedback(self, feedback: UserFeedbackRequest):
        collection = self.collection
        document_text = feedback.comment or "No comment provided"
        collection.add(
            documents=[document_text],
            metadatas=[{"feedback_type": feedback.feedback_type, "response_id": feedback.response_id, "case_id": feedback.case_id, "agent_id": feedback.agent_id}],
            ids=[f'feedback_{feedback.response_id}_{int(time.time())}']
            )

    def get_all_feedback(self):
        collection = self.collection
        return collection.get()

       