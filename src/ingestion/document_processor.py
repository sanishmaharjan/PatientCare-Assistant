"""
Document ingestion module for processing and preparing medical documents.
"""

import os
import json
import sys
from typing import List, Dict, Any, Optional

# Document loaders - We use a compatibility layer to handle different versions of langchain
# and suppress deprecation warnings
import warnings

# Temporarily suppress deprecation warnings during imports
with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    warnings.filterwarnings("ignore", category=UserWarning)
    
    try:
        # Try the new import path first (langchain-community)
        from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
    except ImportError:
        # Fall back to the legacy import path
        from langchain.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader

    # Import text splitter
    try:
        from langchain_text_splitters import RecursiveCharacterTextSplitter
    except ImportError:
        from langchain.text_splitter import RecursiveCharacterTextSplitter

# Local imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import CHUNK_SIZE, CHUNK_OVERLAP


class DocumentIngestion:
    """Process medical documents into chunks for further processing."""
    
    def __init__(self, raw_data_dir, processed_data_dir):
        """
        Initialize with paths to raw and processed data directories.
        
        Args:
            raw_data_dir: Path to directory containing raw medical documents
            processed_data_dir: Path to directory for saving processed documents
        """
        self.raw_data_dir = os.path.abspath(raw_data_dir)
        self.processed_data_dir = os.path.abspath(processed_data_dir)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            separators=["\n\n", "\n", " ", ""]
        )
        
    def load_document(self, file_path):
        """
        Load a document based on its file extension.
        
        Args:
            file_path: Path to the document
            
        Returns:
            content: Loaded document content
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
            
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext == ".pdf":
            loader = PyPDFLoader(file_path)
            return loader.load()
        elif file_ext in [".docx", ".doc"]:
            loader = Docx2txtLoader(file_path)
            return loader.load()
        elif file_ext in [".txt", ".md"]:
            loader = TextLoader(file_path)
            return loader.load()
        else:
            raise ValueError(f"Unsupported file format: {file_ext}")
    
    def process_document(self, file_path: Optional[str] = None):
        """
        Process a document into chunks.
        
        Args:
            file_path: Path to the document
            
        Returns:
            chunks: List of document chunks
        """
        docs = self.load_document(file_path)
        chunks = self.text_splitter.split_documents(docs)
        
        # Save processed chunks
        output_path = os.path.join(
            self.processed_data_dir, 
            f"{os.path.basename(file_path)}_chunks.json"
        )
        
        # Convert chunks to serializable format
        serializable_chunks = []
        for chunk in chunks:
            serializable_chunks.append({
                "text": chunk.page_content,
                "metadata": chunk.metadata
            })
            
        with open(output_path, 'w') as f:
            json.dump(serializable_chunks, f)
            
        return chunks
    
    def process_directory(self) -> List[str]:
        """
        Process all documents in the raw data directory.
        
        Returns:
            processed_files: List of processed file paths
        """
        processed_files = []
        
        # Make sure directories exist
        os.makedirs(self.processed_data_dir, exist_ok=True)
        
        # Process each file in directory
        for root, _, files in os.walk(self.raw_data_dir):
            for filename in files:
                if filename.startswith('.'):
                    continue  # Skip hidden files
                    
                file_path = os.path.join(root, filename)
                file_ext = os.path.splitext(file_path)[1].lower()
                
                if file_ext in ['.pdf', '.docx', '.doc', '.txt', '.md']:
                    try:
                        self.process_document(file_path)
                        processed_files.append(file_path)
                        print(f"Processed: {file_path}")
                    except Exception as e:
                        print(f"Error processing {file_path}: {str(e)}")
        
        return processed_files


if __name__ == "__main__":
    # Example usage
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    raw_dir = os.path.join(base_dir, "data", "raw")
    processed_dir = os.path.join(base_dir, "data", "processed")
    
    ingestion = DocumentIngestion(raw_dir, processed_dir)
    processed_files = ingestion.process_directory()
    
    print("Processed {} files".format(len(processed_files)))
    for file in processed_files:
        print("  - {}".format(file))
