"""
Document Processing Script for RAG System
==========================================

This module handles the complete pipeline for converting markdown documents 
into DocumentChunk objects that can be ingested into ChromaDB for retrieval.

Key Components:
- Markdown parsing with YAML frontmatter extraction
- Section-based content splitting using markdown headers
- Integration with existing ChunkingService for text chunking
- Automatic metadata extraction and chunk creation
- ChromaDB ingestion pipeline

Usage:
    python -m backend.data_processor

Author: Manufacturing RAG System
"""

import os
import uuid
import frontmatter  # For parsing YAML frontmatter in markdown files
import re
from datetime import datetime
from typing import List, Dict, Any
from backend.models import DocumentChunk, ChunkMetadata
from backend.document_chunker import ChunkingService
from backend.config import get_settings

def parse_markdown_file(file_path: str) -> Dict[str, Any]:
    """
    Parse a markdown file and extract both metadata and content.
    
    This function reads a markdown file with YAML frontmatter and separates:
    - YAML metadata (product info, doc type, etc.)
    - Main markdown content (the actual document text)
    
    Args:
        file_path (str): Absolute path to the markdown file
        
    Returns:
        Dict containing:
        - 'metadata': Parsed YAML frontmatter as dictionary
        - 'content': Main markdown content as string
        - 'file_path': Original file path for reference
        
    Example:
        >>> result = parse_markdown_file('pump_guide.md')
        >>> print(result['metadata']['product'])  # "HydroMax 2000"
        >>> print(result['content'][:50])         # "# Troubleshooting Guide..."
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        # frontmatter.load() separates YAML header from markdown content
        post = frontmatter.load(f)
    
    return {
        'metadata': post.metadata,    # Dictionary of YAML frontmatter
        'content': post.content,      # String of markdown content
        'file_path': file_path
    }

def extract_sections_from_content(content: str) -> List[Dict[str, str]]:
    """
    Split markdown content into logical sections based on ## headers.
    
    This function identifies section boundaries using level-2 markdown headers (##)
    and creates separate sections for better chunk organization. Each section
    includes title, content, and extracted metadata like severity levels.
    
    Args:
        content (str): Raw markdown content from the document
        
    Returns:
        List of dictionaries, each containing:
        - 'title': Section title from the ## header
        - 'section_id': Unique identifier for the section
        - 'content': Section content as string
        - 'severity_level': Extracted severity (critical, moderate, minor, None)
        
    Example:
        >>> sections = extract_sections_from_content(markdown_text)
        >>> print(sections[0]['title'])          # "Low Flow Rate Issues"
        >>> print(sections[0]['severity_level']) # "moderate"
    """
    sections = []
    
    # Regular expression to find level-2 headers (## Title)
    # This creates natural section boundaries in technical documentation
    section_pattern = r'^## (.+?)$'
    parts = re.split(section_pattern, content, flags=re.MULTILINE)
    
    # Handle content before the first ## header (introduction, overview, etc.)
    if parts[0].strip():
        sections.append({
            'title': 'Introduction',
            'section_id': 'introduction',
            'content': parts[0].strip(),
            'severity_level': None  # Introduction typically has no severity
        })
    
    # Process remaining parts in pairs: [title, content, title, content, ...]
    # re.split() creates alternating title/content elements
    for i in range(1, len(parts), 2):
        if i + 1 < len(parts):
            title = parts[i].strip()
            section_content = parts[i + 1].strip()
            
            # Extract structured metadata from section content
            severity = extract_severity_from_content(section_content)
            section_id = extract_section_id_from_content(section_content)
            
            sections.append({
                'title': title,
                # Use explicit section_id if found, otherwise generate from title
                'section_id': section_id or title.lower().replace(' ', '_'),
                'content': section_content,
                'severity_level': severity
            })
    
    return sections

def extract_severity_from_content(content: str) -> str:
    """
    Extract severity level from section content using pattern matching.
    
    Looks for patterns like "**Severity:** Critical" in the section content
    to automatically categorize the importance of troubleshooting issues.
    
    Args:
        content (str): Section content to search
        
    Returns:
        str: Severity level ('critical', 'moderate', 'minor') or None if not found
        
    Example:
        >>> content = "**Severity:** Critical\nThis is a serious issue..."
        >>> extract_severity_from_content(content)  # Returns "critical"
    """
    # Pattern matches: **Severity:** followed by whitespace and word characters
    severity_pattern = r'\*\*Severity:\*\*\s*(\w+)'
    match = re.search(severity_pattern, content, re.IGNORECASE)
    return match.group(1).lower() if match else None

def extract_section_id_from_content(content: str) -> str:
    """
    Extract explicit section ID from section content.
    
    Some sections may have explicit IDs like "**Section ID:** low_flow_diagnosis"
    which provide consistent identifiers for referencing specific sections.
    
    Args:
        content (str): Section content to search
        
    Returns:
        str: Section ID if found, None otherwise
        
    Example:
        >>> content = "**Section ID:** excessive_noise\nNoise issues..."
        >>> extract_section_id_from_content(content)  # Returns "excessive_noise"
    """
    section_id_pattern = r'\*\*Section ID:\*\*\s*(\w+)'
    match = re.search(section_id_pattern, content, re.IGNORECASE)
    return match.group(1) if match else None

def create_chunks_from_sections(sections: List[Dict], metadata: Dict, chunking_service: ChunkingService) -> List[DocumentChunk]:
    """
    Convert document sections into DocumentChunk objects for ChromaDB storage.
    
    This function takes the extracted sections and uses the existing ChunkingService
    to split them into appropriately-sized chunks. Each chunk gets comprehensive
    metadata for effective retrieval and citation.
    
    Args:
        sections (List[Dict]): Sections extracted from markdown content
        metadata (Dict): Document-level metadata from YAML frontmatter
        chunking_service (ChunkingService): Configured chunking service instance
        
    Returns:
        List[DocumentChunk]: Ready-to-ingest chunks with complete metadata
        
    Process:
        1. For each section, use ChunkingService to split content
        2. Create ChunkMetadata with document + section information
        3. Generate unique chunk IDs for traceability
        4. Calculate chunk sizes and overlaps
        5. Package into DocumentChunk objects
    """
    chunks = []
    
    for section in sections:
        # Leverage existing chunking logic - respects configured chunk size/overlap
        # ChunkingService.chunk_text() expects both text and metadata parameters
        temp_metadata = {
            'product': metadata.get('product', 'Unknown'),
            'doc_type': metadata.get('doc_type', 'unknown')
        }
        section_chunks_with_metadata = chunking_service.chunk_text(section['content'], temp_metadata)
        
        # Extract just the text from the chunking service output
        section_chunks = [chunk_data['text'] for chunk_data in section_chunks_with_metadata]
        
        # Create a DocumentChunk for each text chunk
        for i, chunk_text in enumerate(section_chunks):
            # Build comprehensive metadata for this specific chunk
            chunk_metadata = ChunkMetadata(
                # Document-level metadata from YAML frontmatter
                product=metadata.get('product', 'Unknown'),
                product_category=metadata.get('product_category', 'unknown'),
                doc_type=metadata.get('doc_type', 'unknown'),
                # Keep as list for ChunkMetadata model validation
                applicable_models=metadata.get('applicable_models', []),
                source_file=metadata.get('source_file', 'unknown.md'),
                
                # Section-level metadata
                section_id=section['section_id'],
                severity_level=section['severity_level'],
                
                # Chunk-level metadata
                chunk_id=f"chunk_{uuid.uuid4().hex[:8]}",  # Unique 8-char ID
                chunk_size=len(chunk_text),
                # Only first chunk in section has no overlap
                chunk_overlap=chunking_service.settings.chunk_overlap if i > 0 else 0,
                timestamp=datetime.now().isoformat()
            )
            
            # Create the final DocumentChunk object
            chunks.append(DocumentChunk(
                text=chunk_text,
                metadata=chunk_metadata
            ))
    
    return chunks

def process_markdown_documents() -> List[DocumentChunk]:
    """
    Main orchestrator function to process all markdown documents in the data folder.
    
    This function coordinates the entire document processing pipeline:
    1. Discovers all .md files in the data directory
    2. Parses each file (frontmatter + content)
    3. Extracts sections from content
    4. Creates chunks using the chunking service
    5. Returns all chunks ready for ChromaDB ingestion
    
    Returns:
        List[DocumentChunk]: All processed chunks from all markdown files
        
    Error Handling:
        - Continues processing other files if one fails
        - Logs errors for debugging
        - Returns successfully processed chunks even if some files fail
    """
    # Initialize services with application settings
    settings = get_settings()
    chunking_service = ChunkingService(settings)
    
    # Locate the data folder relative to this script
    data_folder = os.path.join(os.path.dirname(__file__), 'data')
    all_chunks = []
    
    # Process each markdown file in the data directory
    for filename in os.listdir(data_folder):
        if filename.endswith('.md'):
            file_path = os.path.join(data_folder, filename)
            
            try:
                # Step 1: Parse the markdown file (frontmatter + content)
                parsed_doc = parse_markdown_file(file_path)
                
                # Step 2: Extract logical sections from the content
                sections = extract_sections_from_content(parsed_doc['content'])
                
                # Step 3: Convert sections to chunks with proper metadata
                chunks = create_chunks_from_sections(
                    sections, 
                    parsed_doc['metadata'], 
                    chunking_service
                )
                
                # Accumulate chunks from all files
                all_chunks.extend(chunks)
                print(f"✅ Processed {filename}: {len(chunks)} chunks created")
                
            except Exception as e:
                # Log error but continue processing other files
                print(f"❌ Error processing {filename}: {str(e)}")
    
    print(f"📊 Total chunks created: {len(all_chunks)}")
    return all_chunks

def ingest_chunks_to_chromadb(chunks: List[DocumentChunk]) -> None:
    """
    Ingest processed document chunks into ChromaDB for retrieval.
    
    This function takes the processed chunks and stores them in ChromaDB
    where they can be retrieved by the RAG system for answering queries.
    
    Args:
        chunks (List[DocumentChunk]): Processed chunks ready for storage
        
    Process:
        1. Initialize ChromaService with application settings
        2. Iterate through each chunk
        3. Store chunk in ChromaDB with embeddings
        4. Log success/failure for each chunk
        
    Error Handling:
        - Continues ingesting other chunks if one fails
        - Logs specific errors for debugging
        - Allows partial ingestion success
    """
    from backend.chroma_service import ChromaService
    
    # Initialize ChromaDB service
    settings = get_settings()
    chroma_service = ChromaService(settings)
    
    # Ingest each chunk individually with error handling
    for chunk in chunks:
        try:
            # Convert applicable_models to string for ChromaDB compatibility
            chunk.metadata.applicable_models = ', '.join(chunk.metadata.applicable_models) if chunk.metadata.applicable_models else 'Unknown'
            # ChromaService handles embedding generation and storage
            chroma_service.add_chunks(chunk)
            print(f"✅ Ingested chunk: {chunk.metadata.chunk_id}")
        except Exception as e:
            # Log error but continue with other chunks
            print(f"❌ Error ingesting chunk {chunk.metadata.chunk_id}: {str(e)}")

# Script execution entry point
if __name__ == "__main__":
    """
    Main execution flow when script is run directly.
    
    This creates a complete pipeline:
    1. Process all markdown documents
    2. Convert them to chunks with proper metadata
    3. Ingest the chunks into ChromaDB for retrieval
    
    Usage:
        python -m backend.data_processor
    """
    print("🚀 Starting document processing pipeline...")
    
    # Step 1: Process all markdown documents
    chunks = process_markdown_documents()
    
    # Step 2: Ingest chunks into ChromaDB (only if processing succeeded)
    if chunks:
        print("📥 Starting ChromaDB ingestion...")
        ingest_chunks_to_chromadb(chunks)
        print("✅ Document processing pipeline completed!")
    else:
        print("⚠️  No chunks created - check markdown files and processing errors")