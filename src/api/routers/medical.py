"""
Medical queries router - handles Q&A, summaries, and health issues.
"""

import sys
import os
import time
from fastapi import APIRouter, HTTPException, Depends

# Add src to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from chains.medical_chain import MedicalChain

from ..models import (
    QuestionRequest,
    PatientRequest,
    AnswerResponse,
    SummaryResponse,
    HealthIssuesResponse
)
from ..utils import get_logger

router = APIRouter(prefix="/medical", tags=["medical"])
logger = get_logger()


def get_medical_chain():
    """Dependency for getting the medical chain."""
    return MedicalChain()


@router.post("/answer", response_model=AnswerResponse)
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


@router.post("/summary", response_model=SummaryResponse)
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


@router.post("/health-issues", response_model=HealthIssuesResponse)
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
