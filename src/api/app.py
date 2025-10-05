"""
API for the PatientCare Assistant application.
Using FastAPI.
"""

import os
import sys
from typing import Dict, List, Any, Optional

# FastAPI for modern API development
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn

# Local imports - use modern import style
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import API_HOST, API_PORT
from chains.medical_chain import MedicalChain


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


# Create FastAPI app
app = FastAPI(
    title="PatientCare Assistant API",
    description="API for retrieving and analyzing patient information",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (in production, restrict this)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Initialize medical chain as a dependency
def get_medical_chain():
    """Dependency for getting the medical chain."""
    return MedicalChain()


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "PatientCare Assistant API is running"}


@app.post("/answer", response_model=AnswerResponse)
async def answer_question(request: QuestionRequest, medical_chain: MedicalChain = Depends(get_medical_chain)):
    """Answer a medical question."""
    try:
        result = medical_chain.answer_question(request.question)
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
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/summary", response_model=SummaryResponse)
async def get_patient_summary(request: PatientRequest, medical_chain: MedicalChain = Depends(get_medical_chain)):
    """Generate a summary of patient information."""
    try:
        result = medical_chain.generate_patient_summary(request.patient_id)
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
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/health-issues", response_model=HealthIssuesResponse)
async def get_health_issues(request: PatientRequest, medical_chain: MedicalChain = Depends(get_medical_chain)):
    """Identify potential health issues based on patient records."""
    try:
        result = medical_chain.identify_health_issues(request.patient_id)
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
        raise HTTPException(status_code=500, detail=str(e))


def start_api():
    """Start the API server."""
    uvicorn.run("app:app", host=API_HOST, port=API_PORT, reload=True)


if __name__ == "__main__":
    start_api()
