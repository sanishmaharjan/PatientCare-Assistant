"""
Test document upload and processing functionality.
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.ingestion.document_processor import DocumentIngestion
from src.embedding.embedding_generator import EmbeddingGenerator


class TestDocumentUpload(unittest.TestCase):
    """Test document upload and processing functionality."""
    
    def setUp(self):
        """Set up test environment."""
        # Create temporary directories for testing
        self.temp_raw_dir = tempfile.TemporaryDirectory()
        self.temp_processed_dir = tempfile.TemporaryDirectory()
        
        # Create a test document
        self.test_doc_path = os.path.join(self.temp_raw_dir.name, "test_document.txt")
        with open(self.test_doc_path, "w") as f:
            f.write("This is a test document for document processing.\n\n")
            f.write("It contains multiple paragraphs to test chunking.\n\n")
            f.write("The document processor should be able to process this document correctly.\n\n")
            f.write("And generate proper chunks for embedding generation.\n\n")
            f.write("Each paragraph should ideally become a separate chunk due to our configuration.")
    
    def tearDown(self):
        """Clean up test environment."""
        self.temp_raw_dir.cleanup()
        self.temp_processed_dir.cleanup()
    
    def test_document_processing(self):
        """Test document processing functionality."""
        # Process the test document
        ingestion = DocumentIngestion(self.temp_raw_dir.name, self.temp_processed_dir.name)
        chunks = ingestion.process_document(self.test_doc_path)
        
        # Check that chunks were created
        self.assertTrue(len(chunks) > 0, "No chunks were created from the test document")
        
        # Check that the output file was created
        output_path = os.path.join(
            self.temp_processed_dir.name,
            f"{os.path.basename(self.test_doc_path)}_chunks.json"
        )
        self.assertTrue(os.path.exists(output_path), "Output file was not created")
    
    def test_directory_processing(self):
        """Test processing all documents in a directory."""
        # Create another test document
        second_doc_path = os.path.join(self.temp_raw_dir.name, "another_document.txt")
        with open(second_doc_path, "w") as f:
            f.write("This is another test document.\n\n")
            f.write("It should also be processed correctly.")
        
        # Process all documents in the directory
        ingestion = DocumentIngestion(self.temp_raw_dir.name, self.temp_processed_dir.name)
        processed_files = ingestion.process_directory()
        
        # Check that both files were processed
        self.assertEqual(len(processed_files), 2, "Not all files were processed")
        
        # Check that output files were created for both documents
        for file_path in processed_files:
            output_path = os.path.join(
                self.temp_processed_dir.name,
                f"{os.path.basename(file_path)}_chunks.json"
            )
            self.assertTrue(os.path.exists(output_path), f"Output file for {file_path} was not created")


if __name__ == "__main__":
    unittest.main()
