"""
API for the PatientCare Assistant application.
Using FastAPI.
"""

import os
import sys
import logging
import time
import contextlib
from typing import Dict, List, Any, Optional

# FastAPI for modern API development
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn

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


def start_api(log_level="info"):
    """
    Start the API server.
    
    Args:
        log_level: Logging level (debug, info, warning, error, critical)
    """
    logger.info(f"Starting API server on {API_HOST}:{API_PORT} with log level {log_level.upper()}")
    uvicorn.run("app:app", host=API_HOST, port=API_PORT, reload=True, log_config=None)


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
