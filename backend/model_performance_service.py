from backend.chroma_service import ChromaService
from backend.config import Settings

class ModelPerformanceService():
    settings = Settings()
    settings.chroma_collection_name = "feedback"
    dbService = ChromaService(settings)

    def __init__(self, settings: Settings):
        self.settings = settings
        feedback_settings = Settings()
        feedback_settings.chroma_collection_name = "feedback_db"
        feedback_settings.chroma_host = settings.chroma_host
        feedback_settings.chroma_port = settings.chroma_port
        feedback_settings.embedding_model = settings.embedding_model
        self.dbService = ChromaService(feedback_settings)
    def get_model_performance(self):
        result = self.dbService.get_all_feedback()
        if not result["documents"]:
            return {
                "total_responses": 0,
                "helpful_responses": 0,
                "satisfaction_rate": 0.0,
                "recent_feedback": []
            }
    
        feedback_json = []

        for i, feedback in enumerate(result["documents"]):
            metadata = result["metadatas"][i]
            feedback_json.append({
                "comment": feedback,
                "feedback_type": metadata["feedback_type"],
                "response_id": metadata["response_id"],
                "case_id": metadata["case_id"],
                "agent_id": metadata["agent_id"]
                })
        
        return self.get_model_report(feedback_json)

    def get_model_report(self, feedback_list):
        total_responses = len(feedback_list)
        helpful_responses = len([x for x in feedback_list if x["feedback_type"] == "like"])
        satisfaction_rate = (helpful_responses / total_responses * 100) if total_responses > 0 else 0.0
        recent_feedback = [obj for obj in feedback_list if obj["feedback_type"] == "like"]

        return {
            "total_responses": total_responses,
            "helpful_responses": helpful_responses,
            "satisfaction_rate": satisfaction_rate,
            "recent_feedback": recent_feedback
            }
            



    
        