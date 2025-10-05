"""
Main entry point for the PatientCare Assistant application.
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path  # Python 3 built-in pathlib

# Ensure we can import from the project
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config import API_HOST, API_PORT, FRONTEND_PORT


def setup_environment():
    """Setup the environment for the application."""
    # Ensure data directories exist
    base_dir = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    raw_dir = base_dir / "data" / "raw"
    processed_dir = base_dir / "data" / "processed"
    vector_db_dir = processed_dir / "vector_db"
    
    # Python 3 Path.mkdir with parents option
    raw_dir.mkdir(parents=True, exist_ok=True)
    processed_dir.mkdir(parents=True, exist_ok=True)
    vector_db_dir.mkdir(parents=True, exist_ok=True)
    
    print("Setup complete. Data directories created.")


def process_documents():
    """Process documents and generate embeddings."""
    from ingestion.document_processor import DocumentIngestion
    from embedding.embedding_generator import EmbeddingGenerator
    
    # Get directory paths
    base_dir = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    raw_dir = base_dir / "data" / "raw"
    processed_dir = base_dir / "data" / "processed"
    
    # Process documents
    ingestion = DocumentIngestion(str(raw_dir), str(processed_dir))
    processed_files = ingestion.process_directory()
    
    print(f"Processed {len(processed_files)} files")
    
    # Generate embeddings
    embedding_generator = EmbeddingGenerator()
    embedding_generator.process_all_documents(str(processed_dir))
    
    print("Document processing and embedding generation complete")


def start_api_server():
    """Start the API server."""
    api_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "api", "app.py")
    subprocess.Popen([
        sys.executable, api_script
    ])
    print(f"API server started at http://{API_HOST}:{API_PORT}")


def start_frontend_server():
    """Start the frontend server."""
    # Use Streamlit frontend instead of Flask
    frontend_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontend", "app.py")
    subprocess.Popen([
        sys.executable, "-m", "streamlit", "run", frontend_script,
        "--server.port", str(FRONTEND_PORT),
        "--server.address", "localhost"
    ])
    print(f"Frontend server started at http://localhost:{FRONTEND_PORT}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PatientCare Assistant")
    parser.add_argument("--setup", action="store_true", help="Setup the environment")
    parser.add_argument("--process", action="store_true", help="Process documents and generate embeddings")
    parser.add_argument("--api", action="store_true", help="Start the API server")
    parser.add_argument("--frontend", action="store_true", help="Start the frontend server")
    parser.add_argument("--all", action="store_true", help="Run all components")
    
    args = parser.parse_args()
    
    if args.setup or args.all:
        setup_environment()
    
    if args.process or args.all:
        process_documents()
    
    if args.api or args.all:
        start_api_server()
    
    if args.frontend or args.all:
        start_frontend_server()
    
    if not (args.setup or args.process or args.api or args.frontend or args.all):
        parser.print_help()
