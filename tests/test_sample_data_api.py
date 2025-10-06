"""
Tests for the sample data API endpoints.
"""

import os
import sys
import unittest
import tempfile
from pathlib import Path
import shutil
import httpx

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.config import API_HOST, API_PORT
from src.api.app import app as api_app
from fastapi.testclient import TestClient

# API endpoint for testing
API_URL = f"http://{API_HOST}:{API_PORT}"


class TestSampleDataAPI(unittest.TestCase):
    """Test cases for sample data API endpoints."""

    def setUp(self):
        """Set up test environment."""
        # Create test client
        self.client = TestClient(api_app)
        
        # Create a temporary directory for sample data
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)
        
        # Create some sample files
        self.create_sample_files()
        
        # Store original sample data path to restore later
        self.original_sample_path = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) / "data" / "sample-data"
        
    def tearDown(self):
        """Clean up after tests."""
        # Remove temporary directory
        self.temp_dir.cleanup()
        
    def create_sample_files(self):
        """Create sample files for testing."""
        # Create a PDF file (just a binary file for testing)
        pdf_path = self.temp_path / "test.pdf"
        with open(pdf_path, "wb") as f:
            f.write(b"%PDF-1.5\nTest PDF content")
            
        # Create a markdown file
        md_path = self.temp_path / "test.md"
        with open(md_path, "w") as f:
            f.write("# Test Markdown\nThis is a test markdown file.")
            
        # Create a text file
        txt_path = self.temp_path / "test.txt"
        with open(txt_path, "w") as f:
            f.write("This is a test text file.")
    
    def test_list_sample_data(self):
        """Test listing sample data files."""
        # Patch the sample data directory to use our test directory
        original_listdir = os.listdir
        original_path_exists = os.path.exists
        original_getsize = os.path.getsize
        
        try:
            # Mock os.listdir to return our test files
            def mock_listdir(path):
                if "sample-data" in str(path):
                    return ["test.pdf", "test.md", "test.txt"]
                return original_listdir(path)
            
            # Mock os.path.exists to return True for our sample data path
            def mock_path_exists(path):
                if "sample-data" in str(path):
                    return True
                return original_path_exists(path)
            
            # Mock os.path.getsize to return file size
            def mock_getsize(path):
                if "test.pdf" in str(path):
                    return 1024  # 1KB
                elif "test.md" in str(path):
                    return 512  # 512B
                elif "test.txt" in str(path):
                    return 256  # 256B
                return original_getsize(path)
            
            # Apply mocks
            os.listdir = mock_listdir
            os.path.exists = mock_path_exists
            os.path.getsize = mock_getsize
            
            # Make the request
            response = self.client.get("/documents/sample-data")
            
            # Check response
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertIn("files", data)
            self.assertEqual(len(data["files"]), 3)
            
            # Check if files are in the response
            filenames = [f["filename"] for f in data["files"]]
            self.assertIn("test.pdf", filenames)
            self.assertIn("test.md", filenames)
            self.assertIn("test.txt", filenames)
            
            # Check file types
            for file_info in data["files"]:
                if file_info["filename"] == "test.pdf":
                    self.assertEqual(file_info["type"], "PDF")
                elif file_info["filename"] == "test.md":
                    self.assertEqual(file_info["type"], "MD")
                elif file_info["filename"] == "test.txt":
                    self.assertEqual(file_info["type"], "TXT")
                    
            # Check file sizes
            for file_info in data["files"]:
                if file_info["filename"] == "test.pdf":
                    self.assertEqual(file_info["size"], "1.0 KB")
                elif file_info["filename"] == "test.md":
                    self.assertEqual(file_info["size"], "512 B")
                elif file_info["filename"] == "test.txt":
                    self.assertEqual(file_info["size"], "256 B")
        finally:
            # Restore original functions
            os.listdir = original_listdir
            os.path.exists = original_path_exists
            os.path.getsize = original_getsize
    
    def test_download_sample_file(self):
        """Test downloading a sample file."""
        # Patch the sample data path to use our test directory
        original_path = os.path.join
        
        try:
            # Mock os.path.join to return our test file path
            def mock_path_join(*args):
                if "sample-data" in args[-2]:
                    if args[-1] == "test.pdf":
                        return str(self.temp_path / "test.pdf")
                    elif args[-1] == "test.md":
                        return str(self.temp_path / "test.md")
                    elif args[-1] == "test.txt":
                        return str(self.temp_path / "test.txt")
                return original_path(*args)
            
            # Apply mock
            os.path.join = mock_path_join
            
            # Test PDF download
            response = self.client.get("/documents/sample-data/test.pdf")
            self.assertEqual(response.status_code, 200)
            self.assertIn("application/pdf", response.headers["content-type"])  # Check if content type contains application/pdf
            self.assertEqual(response.headers["content-disposition"], 'attachment; filename="test.pdf"')
            
            # Test MD download
            response = self.client.get("/documents/sample-data/test.md")
            self.assertEqual(response.status_code, 200)
            self.assertIn("text/markdown", response.headers["content-type"])  # Check if content type contains text/markdown
            self.assertEqual(response.headers["content-disposition"], 'attachment; filename="test.md"')
            
            # Test TXT download
            response = self.client.get("/documents/sample-data/test.txt")
            self.assertEqual(response.status_code, 200)
            self.assertIn("text/plain", response.headers["content-type"])  # Check if content type contains text/plain
            self.assertEqual(response.headers["content-disposition"], 'attachment; filename="test.txt"')
            
            # Test non-existent file
            response = self.client.get("/documents/sample-data/nonexistent.txt")
            self.assertEqual(response.status_code, 404)
            
            # Test directory traversal attempt
            response = self.client.get("/documents/sample-data/../../../important_file.txt")
            # The response might be 404 or 400 depending on the routing, but we shouldn't get a 200
            self.assertNotEqual(response.status_code, 200)
            
        finally:
            # Restore original function
            os.path.join = original_path


if __name__ == "__main__":
    unittest.main()
