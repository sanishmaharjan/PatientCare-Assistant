"""
End-to-end test for document upload, processing, and retrieval.
"""

import os
import sys
import tempfile
import unittest
import shutil
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.ingestion.document_processor import DocumentIngestion
from src.retriever.medical_retriever import MedicalRetriever
from src.embedding.embedding_generator import EmbeddingGenerator


class TestEndToEndDocumentFlow(unittest.TestCase):
    """Test the end-to-end flow from document upload to retrieval."""
    
    def setUp(self):
        """Set up test environment."""
        # Create temporary directories for testing
        self.temp_dir = tempfile.TemporaryDirectory()
        self.base_dir = Path(self.temp_dir.name)
        self.raw_dir = self.base_dir / "raw"
        self.processed_dir = self.base_dir / "processed"
        self.vector_db_dir = self.processed_dir / "vector_db"
        
        # Create the directories
        self.raw_dir.mkdir(exist_ok=True)
        self.processed_dir.mkdir(exist_ok=True)
        self.vector_db_dir.mkdir(exist_ok=True)
        
        # Create a test document with patient ID in the filename
        self.patient_id = "TEST12345"
        self.test_doc_path = self.raw_dir / f"PATIENT-{self.patient_id}_test_document.txt"
        with open(self.test_doc_path, "w") as f:
            f.write("This is a test document for patient TEST12345.\n\n")
            f.write("It contains medical information for the patient.\n\n")
            f.write("The document should be retrievable using the patient ID.")
    
    def tearDown(self):
        """Clean up test environment."""
        self.temp_dir.cleanup()
    
    def test_end_to_end_document_flow(self):
        """Test the entire flow from document upload to retrieval."""
        # Step 1: Process the document
        print("Step 1: Processing document")
        ingestion = DocumentIngestion(str(self.raw_dir), str(self.processed_dir))
        chunks = ingestion.process_document(str(self.test_doc_path))
        
        # Verify that chunks were created and have patient_id metadata
        self.assertTrue(len(chunks) > 0, "No chunks were created from the test document")
        self.assertIn("patient_id", chunks[0].metadata, "Patient ID not extracted from filename")
        self.assertEqual(chunks[0].metadata["patient_id"], self.patient_id, "Incorrect patient ID extracted")
        
        # Step 2: Generate embeddings and store in vector database
        print("Step 2: Generating embeddings and storing in vector database")
        embedding_generator = EmbeddingGenerator(str(self.processed_dir), str(self.vector_db_dir))
        
        # Delete and recreate the collection
        try:
            embedding_generator.client.delete_collection("medical_documents")
        except Exception:
            pass  # Collection may not exist yet
        embedding_generator.collection = embedding_generator.client.create_collection("medical_documents")
        
        # Process all documents
        embedding_generator.process_all_documents(str(self.processed_dir))
        
        # Step 3: Retrieve the document using the patient ID
        print("Step 3: Retrieving document using patient ID")
        retriever = MedicalRetriever(str(self.vector_db_dir))
        documents = retriever.get_patient_documents(self.patient_id)
        
        # Verify that the document was retrieved
        self.assertTrue(len(documents) > 0, "No documents retrieved for the patient ID")
        
        # Verify that the retrieved document is the correct one
        self.assertIn(self.patient_id, str(documents[0]), 
                     f"Retrieved document does not mention patient ID {self.patient_id}")


if __name__ == "__main__":
    unittest.main()
