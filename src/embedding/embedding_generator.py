"""
Embedding module for converting text to vector representations.
"""

import os
import json
import sys
from typing import List, Dict, Any

import chromadb

# Local imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import OPENAI_API_KEY, EMBEDDING_MODEL, VECTOR_DB_PATH
from openai_wrapper import OpenAIEmbeddings


class EmbeddingGenerator:
    """Generate embeddings for text chunks and manage vector database."""
    
    def __init__(self):
        """Initialize the embedding generator with OpenAI embeddings."""
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=OPENAI_API_KEY,
            model=EMBEDDING_MODEL
        )
        # Ensure vector DB directory exists
        os.makedirs(VECTOR_DB_PATH, exist_ok=True)
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(path=VECTOR_DB_PATH)
        
        # Create collection if it doesn't exist
        try:
            self.collection = self.client.get_collection("medical_documents")
        except ValueError:
            self.collection = self.client.create_collection("medical_documents")
            
    def add_documents(self, documents: List[Dict[str, Any]]):
        """
        Add documents to the vector database.
        
        Args:
            documents: List of document chunks with text and metadata
        """
        # Process in batches to avoid rate limits
        batch_size = 10
        
        for i in range(0, len(documents), batch_size):
            batch = documents[i:i + batch_size]
            
            # Extract text content
            texts = [doc["text"] for doc in batch]
            
            # Generate embeddings
            embeddings = self.embeddings.embed_documents(texts)
            
            # Prepare IDs and metadata for ChromaDB
            ids = [f"doc_{i}_{j}" for j in range(len(batch))]
            metadatas = [doc["metadata"] for doc in batch]
            
            # Add to collection
            self.collection.add(
                embeddings=embeddings,
                documents=texts,
                ids=ids,
                metadatas=metadatas
            )
            
        print(f"Added {len(documents)} documents to vector database")
        
    def process_file(self, file_path: str):
        """
        Process a file of document chunks and add to vector database.
        
        Args:
            file_path: Path to JSON file containing document chunks
        """
        with open(file_path, 'r') as f:
            documents = json.load(f)
            
        self.add_documents(documents)
        
    def process_all_documents(self, processed_dir: str):
        """
        Process all document chunk files in the processed directory.
        
        Args:
            processed_dir: Directory containing processed document chunks
        """
        for root, _, files in os.walk(processed_dir):
            for filename in files:
                if filename.endswith('_chunks.json'):
                    file_path = os.path.join(root, filename)
                    try:
                        self.process_file(file_path)
                        print(f"Added embeddings for {filename}")
                    except Exception as e:
                        print(f"Error processing {filename}: {str(e)}")
                        
        print(f"Embeddings generated and stored in {VECTOR_DB_PATH}")
        
    def query_by_text(self, query_text: str, top_k: int = 5):
        """
        Query the vector database using text.
        
        Args:
            query_text: The query text
            top_k: Number of results to return
            
        Returns:
            results: List of matching documents with metadata
        """
        # Generate query embedding
        query_embedding = self.embeddings.embed_query(query_text)
        
        # Query collection
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        # Format results
        documents = []
        for i, doc in enumerate(results["documents"][0]):
            documents.append({
                "text": doc,
                "metadata": results["metadatas"][0][i]
            })
            
        return documents


if __name__ == "__main__":
    # Example usage
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    processed_dir = os.path.join(base_dir, "data", "processed")
    
    embedding_generator = EmbeddingGenerator()
    embedding_generator.process_all_documents(processed_dir)
    print("Embedding processing complete")
