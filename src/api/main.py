"""
Main FastAPI application - modular version.
"""

import contextlib
import logging
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import (
    API_HOST,
    API_PORT,
    API_TITLE,
    API_DESCRIPTION,
    API_VERSION,
    CORS_ORIGINS,
    CORS_CREDENTIALS,
    CORS_METHODS,
    CORS_HEADERS
)
from .utils import setup_logging, get_logger
from .middleware import log_requests
from .routers import medical_router, documents_router

# Initialize logging
logger = setup_logging()
logger.info("PatientCare Assistant API logging initialized")


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
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=CORS_CREDENTIALS,
    allow_methods=CORS_METHODS,
    allow_headers=CORS_HEADERS
)

# Add request logging middleware
app.middleware("http")(log_requests)

# Include routers
app.include_router(medical_router)
app.include_router(documents_router)

# Legacy endpoint redirects for backward compatibility
@app.post("/answer")
async def legacy_answer(request_data: dict):
    """Legacy endpoint - redirects to medical/answer."""
    from .routers.medical import answer_question, get_medical_chain
    from .models import QuestionRequest
    
    question_request = QuestionRequest(**request_data)
    return await answer_question(question_request, get_medical_chain())


@app.post("/summary")
async def legacy_summary(request_data: dict):
    """Legacy endpoint - redirects to medical/summary."""
    from .routers.medical import get_patient_summary, get_medical_chain
    from .models import PatientRequest
    
    patient_request = PatientRequest(**request_data)
    return await get_patient_summary(patient_request, get_medical_chain())


@app.post("/health-issues")
async def legacy_health_issues(request_data: dict):
    """Legacy endpoint - redirects to medical/health-issues."""
    from .routers.medical import get_health_issues, get_medical_chain
    from .models import PatientRequest
    
    patient_request = PatientRequest(**request_data)
    return await get_health_issues(patient_request, get_medical_chain())


@app.post("/documents/process")
async def legacy_process_documents():
    """Legacy endpoint - redirects to documents/process."""
    from .routers.documents import process_documents
    return await process_documents()


@app.get("/documents")
async def legacy_list_documents():
    """Legacy endpoint - redirects to documents/."""
    from .routers.documents import list_documents
    return await list_documents()


@app.get("/")
async def root():
    """Root endpoint."""
    logger.debug("Root endpoint accessed")
    return {"message": "PatientCare Assistant API is running"}


def start_api(log_level="info"):
    """
    Start the API server.
    
    Args:
        log_level: Logging level (debug, info, warning, error, critical)
    """
    logger.info(f"Starting API server on {API_HOST}:{API_PORT} with log level {log_level.upper()}")
    # Bind to all interfaces (0.0.0.0) regardless of what's in config.py
    # This ensures the API is accessible from other machines if needed
    uvicorn.run("api.main:app", host="0.0.0.0", port=API_PORT, reload=True, log_config=None)


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
