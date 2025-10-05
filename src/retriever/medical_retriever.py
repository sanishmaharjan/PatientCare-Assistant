"""
Retriever module for finding relevant patient information.
"""

import os
import sys
from typing import List, Dict, Any

import chromadb

# Local imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import OPENAI_API_KEY, EMBEDDING_MODEL, VECTOR_DB_PATH
from openai_wrapper import OpenAIEmbeddings


class MedicalRetriever:
    """Retrieve relevant medical information based on queries."""
    
    def __init__(self):
        """Initialize the retriever with embedding model and vector database."""
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=OPENAI_API_KEY,
            model=EMBEDDING_MODEL
        )
        
        # Initialize ChromaDB client
        try:
            self.client = chromadb.PersistentClient(path=VECTOR_DB_PATH)
            self.collection = self.client.get_collection("medical_documents")
        except Exception as e:
            print(f"Warning: Could not connect to vector database: {e}")
            print(f"Vector database path: {VECTOR_DB_PATH}")
            self.client = None
            self.collection = None
            
    def query_by_text(self, query_text: str, top_k: int = 5, patient_id: str = None) -> List[Dict[str, Any]]:
        """
        Query the vector database using text.
        
        Args:
            query_text: The query text
            top_k: Number of results to return
            patient_id: Optional patient ID to filter results
            
        Returns:
            results: List of matching documents with metadata
        """
        if self.collection is None:
            print("Warning: Vector database not initialized")
            return []
            
        # Generate query embedding
        query_embedding = self.embeddings.embed_query(query_text)
        
        # Query collection with optional patient_id filter
        if patient_id:
            try:
                # Try exact match on patient_id metadata field first
                results = self.collection.query(
                    query_embeddings=[query_embedding],
                    where={"patient_id": patient_id},
                    n_results=top_k
                )
            except Exception as e:
                print(f"Error searching with metadata filter: {e}")
                # Fall back to standard query without filter
                results = self.collection.query(
                    query_embeddings=[query_embedding],
                    n_results=top_k
                )
        else:
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
        
    def get_patient_documents(self, patient_id: str, top_k: int = 10) -> List[Dict[str, Any]]:
        """
        Get documents related to a specific patient.
        
        Args:
            patient_id: The patient ID
            top_k: Maximum number of documents to return
            
        Returns:
            documents: List of documents for the patient
        """
        if self.collection is None:
            print("Warning: Vector database not initialized")
            return []
            
        # First try to find by exact patient ID match
        try:
            results = self.collection.get(
                where={"patient_id": patient_id}
            )
            
            if results and len(results["documents"]) > 0:
                documents = []
                for i, doc in enumerate(results["documents"]):
                    documents.append({
                        "text": doc,
                        "metadata": results["metadatas"][i]
                    })
                return documents[:top_k]
        except Exception as e:
            print(f"Error searching by exact patient ID match: {e}")
        
        # If no exact matches or error, try semantic search with patient ID filter
        try:
            # Try to get all documents with this patient ID first
            all_patient_docs = self.collection.get(
                where_document={"$contains": patient_id}
            )
            
            if all_patient_docs and len(all_patient_docs["documents"]) > 0:
                documents = []
                for i, doc in enumerate(all_patient_docs["documents"]):
                    documents.append({
                        "text": doc,
                        "metadata": all_patient_docs["metadatas"][i]
                    })
                return documents[:top_k]
        except Exception as e:
            print(f"Error searching by document content containing patient ID: {e}")
            
        # As a last resort, return an empty list rather than returning data for other patients
        print(f"No documents found for patient ID: {patient_id}")
        return []


if __name__ == "__main__":
    # Example usage
    retriever = MedicalRetriever()
    
    # Example query
    query = "What are the current medications for the patient with hypertension?"
    results = retriever.query_by_text(query)
    
    print("Query: {}".format(query))
    print("Results: {}".format(len(results)))
    for i, result in enumerate(results):
        print("\nResult {}:".format(i+1))
        print("Text: {}".format(result['text'][:100] + "..."))
        print("Source: {}".format(result['metadata'].get('source', 'Unknown')))
        print("Score: {}".format(result['score']))
