"""
Test for the patient ID extraction functionality in document processor.
"""
import os
import sys
import tempfile
import unittest
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.ingestion.document_processor import DocumentIngestion


class TestPatientIDExtraction(unittest.TestCase):
    """Test the patient ID extraction from filenames."""
    
    def setUp(self):
        """Set up test environment."""
        # Create temporary directories for testing
        self.temp_raw_dir = tempfile.TemporaryDirectory()
        self.temp_processed_dir = tempfile.TemporaryDirectory()
        
        # Initialize document ingestion
        self.ingestion = DocumentIngestion(self.temp_raw_dir.name, self.temp_processed_dir.name)
    
    def tearDown(self):
        """Clean up test environment."""
        self.temp_raw_dir.cleanup()
        self.temp_processed_dir.cleanup()
    
    def test_patient_id_extraction_from_filename(self):
        """Test extraction of patient IDs from various filename patterns."""
        test_cases = [
            ("patient_123456_lab_results.txt", "123456"),
            ("PATIENT-654321-MRI-SCAN.txt", "654321"),
            ("PT_987654_NOTES.txt", "987654"),
            ("lab_results_patient_112233.txt", "112233"),
            ("medical_history_PT-445566.txt", "445566"),
            ("regular_document_without_id.txt", None),
            ("patient_ABC123_discharge.txt", "ABC123"),
            ("PATIENT-789-SCAN.txt", "789"),
        ]
        
        for filename, expected_id in test_cases:
            # Create a test file with this name
            file_path = os.path.join(self.temp_raw_dir.name, filename)
            with open(file_path, "w") as f:
                f.write("Sample content for testing patient ID extraction.")
            
            # Process the document and check if patient ID was extracted
            chunks = self.ingestion.process_document(file_path)
            
            # Verify that chunks were created
            self.assertTrue(len(chunks) > 0, f"No chunks created for {filename}")
            
            # Check if the correct patient ID was extracted
            if expected_id is None:
                # If no patient ID is expected, the metadata should not contain patient_id
                self.assertNotIn("patient_id", chunks[0].metadata, 
                                f"Patient ID should not be extracted from {filename}")
            else:
                # If a patient ID is expected, check if it matches
                self.assertIn("patient_id", chunks[0].metadata, 
                            f"Patient ID not extracted from {filename}")
                self.assertEqual(chunks[0].metadata["patient_id"], expected_id, 
                                f"Incorrect patient ID extracted from {filename}")


if __name__ == "__main__":
    unittest.main()
