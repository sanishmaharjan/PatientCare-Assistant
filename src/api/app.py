"""
API for the PatientCare Assistant application.
Using FastAPI.
"""

import os
import sys
import json
import logging
import time
import contextlib
from typing import Dict, List, Any, Optional

# FastAPI for modern API development
from fastapi import FastAPI, HTTPException, Depends, Request, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn
import uuid

# Local imports - use modern import style
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import API_HOST, API_PORT
from chains.medical_chain import MedicalChain

# Setup logging
def setup_logging():
    """Set up logging to both console and file."""
    log_format = "%(asctime)s - %(levelname)s - [API] %(message)s"
    log_formatter = logging.Formatter(log_format, datefmt="%Y-%m-%d %H:%M:%S")
    
    # Create logs directory if it doesn't exist
    log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "logs")
    os.makedirs(log_dir, exist_ok=True)
    
    # Get logger and clear any existing handlers to prevent duplicates
    logger = logging.getLogger("api")
    if logger.handlers:
        logger.handlers.clear()
    
    # Set up file handler
    log_file = os.path.join(log_dir, "api.log")
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(log_formatter)
    
    # Set up console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    
    # Configure logger
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    # Prevent propagation to root logger to avoid duplicate entries
    logger.propagate = False
    
    return logger

logger = setup_logging()
logger.info("PatientCare Assistant API logging initialized")


# Pydantic models for request/response validation
class QuestionRequest(BaseModel):
    question: str = Field(..., description="The medical question to answer")


class PatientRequest(BaseModel):
    patient_id: str = Field(..., description="The patient ID to retrieve information for")


class SourceDocument(BaseModel):
    text: str = Field(..., description="The text content of the source document")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Metadata about the source document")


class AnswerResponse(BaseModel):
    question: str = Field(..., description="The original question")
    answer: str = Field(..., description="The answer to the question")
    sources: List[SourceDocument] = Field(default_factory=list, description="Source documents used to generate the answer")


class SummaryResponse(BaseModel):
    patient_id: str = Field(..., description="The patient ID")
    summary: str = Field(..., description="A summary of the patient's information")
    sources: List[SourceDocument] = Field(default_factory=list, description="Source documents used to generate the summary")


class HealthIssuesResponse(BaseModel):
    patient_id: str = Field(..., description="The patient ID")
    issues: str = Field(..., description="Identified potential health issues")
    sources: List[SourceDocument] = Field(default_factory=list, description="Source documents used to identify issues")


class DocumentInfo(BaseModel):
    filename: str = Field(..., description="The original filename")
    added: str = Field(..., description="Date when the document was added")
    size: str = Field(..., description="Size of the document")
    type: str = Field(..., description="Type of document")
    status: str = Field(..., description="Processing status")


class DocumentListResponse(BaseModel):
    documents: List[DocumentInfo] = Field(default_factory=list, description="List of documents")


class ProcessingResponse(BaseModel):
    success: bool = Field(..., description="Whether processing was successful")
    message: str = Field(..., description="Status message")
    processed_files: List[str] = Field(default_factory=list, description="List of processed files")


# Define lifespan context for startup/shutdown events (modern approach)
@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events."""
    # Startup
    logger.info("PatientCare Assistant API started")
    yield
    # Shutdown
    logger.info("PatientCare Assistant API shutting down")

# Create FastAPI app
app = FastAPI(
    title="PatientCare Assistant API",
    description="API for retrieving and analyzing patient information",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (in production, restrict this)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Function to safely extract and log request body
async def get_request_body(request: Request) -> str:
    """Safely extract request body for logging purposes."""
    try:
        body = await request.body()
        body_str = body.decode('utf-8')
        # Truncate if too long
        if len(body_str) > 200:
            body_str = body_str[:197] + '...'
        return body_str
    except Exception as e:
        return f"<Error reading body: {str(e)}>"

# Middleware for request logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware to log all requests and responses"""
    request_id = f"{id(request)}"
    start_time = time.time()
    
    # Log the incoming request with body for debugging
    if request.method in ["POST", "PUT", "PATCH"]:
        body = await get_request_body(request)
        logger.info(f"Request [{request_id}] - {request.method} {request.url.path} - Started - Body: {body}")
        # Reset the request body position for further processing
        await request.body()
    else:
        logger.info(f"Request [{request_id}] - {request.method} {request.url.path} - Started")
    
    # Process the request
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        
        # Log the response with timing information
        logger.info(f"Request [{request_id}] - {request.method} {request.url.path} - "
                    f"Completed with status {response.status_code} in {process_time:.4f}s")
        
        return response
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(f"Request [{request_id}] - {request.method} {request.url.path} - "
                    f"Failed after {process_time:.4f}s: {str(e)}")
        # Log the stack trace for server errors
        import traceback
        logger.error(f"Exception traceback: {traceback.format_exc()}")
        raise

# Initialize medical chain as a dependency
def get_medical_chain():
    """Dependency for getting the medical chain."""
    return MedicalChain()


@app.get("/")
async def root():
    """Root endpoint."""
    logger.debug("Root endpoint accessed")
    return {"message": "PatientCare Assistant API is running"}


@app.post("/answer", response_model=AnswerResponse)
async def answer_question(request: QuestionRequest, medical_chain: MedicalChain = Depends(get_medical_chain)):
    """Answer a medical question."""
    logger.info(f"Answering question: {request.question[:50]}...")
    start_time = time.time()
    try:
        result = medical_chain.answer_question(request.question)
        process_time = time.time() - start_time
        
        # Log the successful response
        num_sources = len(result.get("source_documents", []))
        answer_length = len(result["answer"])
        logger.info(f"Successfully answered question '{request.question[:30]}...' "
                    f"with {num_sources} sources, {answer_length} chars in {process_time:.2f}s")
        
        return {
            "question": result["question"],
            "answer": result["answer"],
            "sources": [
                {
                    "text": doc["text"],
                    "metadata": doc["metadata"]
                }
                for doc in result.get("source_documents", [])
            ]
        }
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(f"Error answering question '{request.question[:30]}...': {str(e)} after {process_time:.2f}s")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/summary", response_model=SummaryResponse)
async def get_patient_summary(request: PatientRequest, medical_chain: MedicalChain = Depends(get_medical_chain)):
    """Generate a summary of patient information."""
    logger.info(f"Generating summary for patient: {request.patient_id}")
    start_time = time.time()
    try:
        result = medical_chain.generate_patient_summary(request.patient_id)
        process_time = time.time() - start_time
        
        # Log the successful response
        num_sources = len(result.get("source_documents", []))
        summary_length = len(result["summary"])
        logger.info(f"Successfully generated summary for patient {request.patient_id} "
                    f"with {num_sources} sources, {summary_length} chars in {process_time:.2f}s")
        
        return {
            "patient_id": request.patient_id,
            "summary": result["summary"],
            "sources": [
                {
                    "text": doc["text"],
                    "metadata": doc["metadata"]
                }
                for doc in result.get("source_documents", [])
            ]
        }
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(f"Error generating summary for patient {request.patient_id}: {str(e)} after {process_time:.2f}s")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/health-issues", response_model=HealthIssuesResponse)
async def get_health_issues(request: PatientRequest, medical_chain: MedicalChain = Depends(get_medical_chain)):
    """Identify potential health issues based on patient records."""
    logger.info(f"Identifying health issues for patient: {request.patient_id}")
    start_time = time.time()
    try:
        result = medical_chain.identify_health_issues(request.patient_id)
        process_time = time.time() - start_time
        
        # Log the successful response
        num_sources = len(result.get("source_documents", []))
        issues_length = len(result["issues"])
        logger.info(f"Successfully identified health issues for patient {request.patient_id} "
                    f"with {num_sources} sources, {issues_length} chars in {process_time:.2f}s")
        
        return {
            "patient_id": request.patient_id,
            "issues": result["issues"],
            "sources": [
                {
                    "text": doc["text"],
                    "metadata": doc["metadata"]
                }
                for doc in result.get("source_documents", [])
            ]
        }
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(f"Error identifying health issues for patient {request.patient_id}: {str(e)} after {process_time:.2f}s")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/documents/process")
async def process_documents():
    """Process all documents in the raw directory."""
    logger.info("Processing documents from raw directory")
    start_time = time.time()
    
    try:
        from pathlib import Path
        
        # Define paths
        base_dir = Path(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        raw_dir = base_dir / "data" / "raw"
        processed_dir = base_dir / "data" / "processed"
        
        # Make sure directories exist
        os.makedirs(raw_dir, exist_ok=True)
        os.makedirs(processed_dir, exist_ok=True)
        
        # Import necessary modules
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from ingestion.document_processor import DocumentIngestion
        from embedding.embedding_generator import EmbeddingGenerator
        
        # Process documents
        ingestion = DocumentIngestion(str(raw_dir), str(processed_dir))
        processed_files = ingestion.process_directory()
        
        # Count chunks
        chunk_count = 0
        for processed_file in processed_files:
            output_path = os.path.join(
                processed_dir,
                f"{os.path.basename(processed_file)}_chunks.json"
            )
            if os.path.exists(output_path):
                with open(output_path, 'r') as f:
                    chunks = json.load(f)
                    chunk_count += len(chunks)
        
        # Generate embeddings
        embedding_generator = EmbeddingGenerator()
        embedding_generator.process_all_documents(str(processed_dir))
        
        process_time = time.time() - start_time
        logger.info(f"Successfully processed {len(processed_files)} documents with {chunk_count} chunks in {process_time:.2f}s")
        
        return {
            "success": True,
            "message": f"Successfully processed {len(processed_files)} documents with {chunk_count} chunks",
            "processed_files": processed_files,
            "chunk_count": chunk_count,
            "processing_time_seconds": round(process_time, 2)
        }
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(f"Error processing documents: {str(e)} after {process_time:.2f}s")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/documents", response_model=DocumentListResponse)
async def list_documents():
    """Get a list of documents in the system."""
    logger.info("Listing documents")
    start_time = time.time()
    
    try:
        import os
        import datetime
        from pathlib import Path
        
        # Define paths
        base_dir = Path(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        raw_dir = base_dir / "data" / "raw"
        processed_dir = base_dir / "data" / "processed"
        
        # Function to determine document type
        def get_document_type(filename):
            ext = filename.split('.')[-1].lower()
            if ext == 'pdf':
                return "Medical Records"
            elif ext in ['docx', 'doc']:
                return "Medical Notes"
            elif ext == 'txt':
                return "Lab Results"
            elif ext == 'md':
                return "Patient History"
            else:
                return "Other"
        
        # Function for human-readable file sizes
        def get_size_format(size_bytes):
            if size_bytes < 1024:
                return f"{size_bytes} B"
            elif size_bytes < 1024 * 1024:
                return f"{size_bytes / 1024:.1f} KB"
            else:
                return f"{size_bytes / (1024 * 1024):.1f} MB"
        
        documents = []
        if raw_dir.exists():
            for file_path in raw_dir.glob("*"):
                if not file_path.name.startswith('.') and file_path.is_file():
                    stats = file_path.stat()
                    # Check if it has been processed
                    is_processed = any(
                        (processed_dir / f).name.startswith(file_path.name) 
                        for f in os.listdir(processed_dir) 
                        if f.endswith('_chunks.json')
                    )
                    
                    documents.append({
                        "filename": file_path.name,
                        "added": datetime.datetime.fromtimestamp(stats.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                        "size": get_size_format(stats.st_size),
                        "type": get_document_type(file_path.name),
                        "status": "Processed" if is_processed else "Raw"
                    })
        
        process_time = time.time() - start_time
        logger.info(f"Found {len(documents)} documents in {process_time:.4f}s")
        
        return {"documents": documents}
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(f"Error listing documents: {str(e)} after {process_time:.4f}s")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/documents/{filename}")
async def delete_document(filename: str):
    """Delete a document from the system."""
    logger.info(f"Deleting document: {filename}")
    start_time = time.time()
    
    try:
        import os
        from pathlib import Path
        
        # Define paths
        base_dir = Path(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        raw_dir = base_dir / "data" / "raw"
        processed_dir = base_dir / "data" / "processed"
        
        # Find and remove the raw file
        raw_file = raw_dir / filename
        if raw_file.exists():
            raw_file.unlink()
        
        # Find and remove processed chunks
        for processed_file in processed_dir.glob(f"{filename}_chunks.json"):
            processed_file.unlink()
        
        process_time = time.time() - start_time
        logger.info(f"Successfully deleted document {filename} in {process_time:.4f}s")
        
        return {"success": True, "message": f"Successfully deleted {filename}"}
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(f"Error deleting document {filename}: {str(e)} after {process_time:.4f}s")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/documents/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload a document to the raw directory."""
    logger.info(f"Uploading document: {file.filename}")
    start_time = time.time()
    
    try:
        # Define paths
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        raw_dir = os.path.join(base_dir, "data", "raw")
        
        # Make sure directory exists
        os.makedirs(raw_dir, exist_ok=True)
        
        # Generate a unique filename to prevent collisions
        unique_filename = f"{uuid.uuid4()}_{file.filename}"
        file_path = os.path.join(raw_dir, unique_filename)
        
        # Save the file
        with open(file_path, "wb") as f:
            contents = await file.read()
            f.write(contents)
        
        process_time = time.time() - start_time
        logger.info(f"Successfully uploaded document {file.filename} in {process_time:.4f}s")
        
        return {
            "success": True,
            "message": f"Successfully uploaded {file.filename}",
            "filename": unique_filename
        }
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(f"Error uploading document {file.filename}: {str(e)} after {process_time:.4f}s")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/documents/reset")
async def reset_vector_database():
    """Reset the vector database by clearing all documents from raw and processed directories."""
    logger.info("Resetting vector database")
    start_time = time.time()
    
    try:
        from pathlib import Path
        import shutil
        
        # Define paths
        base_dir = Path(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        raw_dir = base_dir / "data" / "raw"
        processed_dir = base_dir / "data" / "processed"
        vector_db_dir = processed_dir / "vector_db"
        
        # Clear raw directory
        if raw_dir.exists():
            for file in raw_dir.glob("*"):
                if file.is_file():
                    file.unlink()
        
        # Clear processed directory
        if processed_dir.exists():
            for file in processed_dir.glob("*_chunks.json"):
                file.unlink()
        
        # Clear vector database
        if vector_db_dir.exists():
            shutil.rmtree(vector_db_dir)
            os.makedirs(vector_db_dir)
        
        process_time = time.time() - start_time
        logger.info(f"Successfully reset vector database in {process_time:.2f}s")
        
        return {
            "success": True,
            "message": "Vector database reset successfully"
        }
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(f"Error resetting vector database: {str(e)} after {process_time:.2f}s")
        raise HTTPException(status_code=500, detail=str(e))


def start_api(log_level="info"):
    """
    Start the API server.
    
    Args:
        log_level: Logging level (debug, info, warning, error, critical)
    """
    logger.info(f"Starting API server on {API_HOST}:{API_PORT} with log level {log_level.upper()}")
    # Bind to all interfaces (0.0.0.0) regardless of what's in config.py
    # This ensures the API is accessible from other machines if needed
    uvicorn.run("app:app", host="0.0.0.0", port=API_PORT, reload=True, log_config=None)


if __name__ == "__main__":
    import argparse
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Start the PatientCare Assistant API server")
    parser.add_argument("--log-level", choices=["debug", "info", "warning", "error", "critical"],
                        default="info", help="Set logging level")
    args = parser.parse_args()
    
    # Set the logger level based on command line argument
    log_level = getattr(logging, args.log_level.upper())
    logger.setLevel(log_level)
    logger.info(f"Log level set to {args.log_level.upper()}")
    
    try:
        logger.info("PatientCare Assistant API initializing")
        start_api(args.log_level)
    except KeyboardInterrupt:
        logger.info("API server shutdown requested")
    except Exception as e:
        logger.error(f"Error in API server: {str(e)}")
        # Log the full stack trace for debugging
        import traceback
        logger.error(f"Exception traceback: {traceback.format_exc()}")
    finally:
        logger.info("API server shutdown complete")
