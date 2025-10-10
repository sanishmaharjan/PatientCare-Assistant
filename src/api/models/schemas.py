"""
Pydantic models for API request/response validation.
"""

from typing import Dict, List, Any
from pydantic import BaseModel, Field


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


class SampleFileInfo(BaseModel):
    filename: str = Field(..., description="The sample file name")
    size: str = Field(..., description="Size of the file")
    type: str = Field(..., description="Type of document")


class SampleDataResponse(BaseModel):
    files: List[SampleFileInfo] = Field(default_factory=list, description="List of sample data files")


class ProcessingResponse(BaseModel):
    success: bool = Field(..., description="Whether processing was successful")
    message: str = Field(..., description="Status message")
    processed_files: List[str] = Field(default_factory=list, description="List of processed files")


class UploadResponse(BaseModel):
    success: bool = Field(..., description="Whether upload was successful")
    message: str = Field(..., description="Status message")
    filename: str = Field(..., description="The uploaded filename")


class DeleteResponse(BaseModel):
    success: bool = Field(..., description="Whether deletion was successful")
    message: str = Field(..., description="Status message")


class ResetResponse(BaseModel):
    success: bool = Field(..., description="Whether reset was successful")
    message: str = Field(..., description="Status message")
