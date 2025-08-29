from backend.config import Settings
import logging
import datetime

class ChunkingService:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.logger = logging.getLogger(__name__)

    def chunk_text(self, text, metadata):
        # Implement chunking
        separators = ["\n\n", "\n", ". ", " ", ""]
        chunks = self._calculate_chunks(text, separators)

        if not chunks:
            return []
        
        overlap = self.settings.chunk_overlap
        overlapped_chunks = []

        for i in range(len(chunks) - 1):
            overlapped_chunk = chunks[i] + chunks[i + 1][:overlap]
            overlapped_chunks.append(overlapped_chunk)
        overlapped_chunks.append(chunks[-1])
        return self._add_metadata(overlapped_chunks, metadata)

    def _add_metadata(self, chunks, metadata):
        """
        Input metadata format
        metadata = {
            # Document metadata (during ingestion)
            "product": "industrial_motor",
            "doc_type": "troubleshooting_guide", 
            "clause_id": "section_4_2",
            "source_file": "motor_manual_v2.pdf",
    
                # Query metadata (during retrieval)
                "case_id": "CASE-2024-001234",
                "agent_id": "agent-456",
                "priority": "high"
            }
            Output metadata format
                            {
                    "text": "Check motor connections and voltage levels...",
                    "metadata": {
                        # Original metadata
                        "product": "industrial_motor",
                        "doc_type": "troubleshooting_guide",
                        
                        # Chunking metadata (added by service)
                        "chunk_id": "chunk_001",
                        "chunk_size": 800,
                        "chunk_overlap": 120,
                        "timestamp": "2024-01-27T18:56:10Z"
                    }
                }
        """
        # Implement metadata addition
        chunks_with_metadata = []
        for i, chunk in enumerate(chunks):
            chunk_data = {
                "text": chunk,
                "metadata": {
                    # Original metadata
                    "product": metadata["product"],
                    "doc_type": metadata["doc_type"],
                    
                    # Chunking metadata (added by service)
                    "chunk_id": f"chunk_{i+1:03d}",
                    "chunk_size": self.settings.chunk_size,
                    "chunk_overlap": self.settings.chunk_overlap,
                    "timestamp": datetime.datetime.now().isoformat()
                }
            }
            chunks_with_metadata.append(chunk_data)
        return chunks_with_metadata
    
    def _calculate_chunks(self, text, separators):

        current_separator = separators[0]
        remaining_separators = separators[1:]
        parts = text.split(current_separator)
        final_chunks = []
        
        for part in parts:
            if len(part) > self.settings.chunk_size:
               sub_chunks = self._calculate_chunks(part, remaining_separators)
               final_chunks.extend(sub_chunks)
            elif(part.strip() != ""):
                final_chunks.append(part.strip())

        return final_chunks