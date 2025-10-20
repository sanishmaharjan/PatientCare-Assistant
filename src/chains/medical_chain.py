"""
Medical chain functionality implementation using modern Python 3 features.
This uses langchain which is compatible with Python 3.
"""

import os
import sys
import json
import time
import logging
from typing import Dict, List, Any, Optional

# Modern HTTP library in Python 3
import httpx

# Local imports - use modern relative imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import OPENAI_API_KEY, COMPLETION_MODEL, TEMPERATURE, MAX_TOKENS
from retriever.medical_retriever import MedicalRetriever

# Configure logger for medical chain debugging
logger = logging.getLogger("medical_chain")
logger.setLevel(logging.DEBUG)

class MedicalChain:
    """Chain for handling medical queries about patient data (Python 3 compatible)."""
    
    def __init__(self) -> None:
        """Initialize the medical chain."""
        # Initialize retriever
        logger.debug("Creating MedicalRetriever instance...")
        self.retriever = MedicalRetriever()
        
        # OpenAI API settings
        self.api_key = OPENAI_API_KEY
        self.model = COMPLETION_MODEL
        self.temperature = TEMPERATURE
        self.max_tokens = MAX_TOKENS
        
        logger.debug(f"OpenAI configuration: model={self.model}, temperature={self.temperature}, max_tokens={self.max_tokens}")
        
        # Chat history (simple implementation)
        self.chat_history: List[Dict[str, str]] = []
    
    def _call_openai_api(self, prompt: str, system_message: Optional[str] = None) -> str:
        """Call the OpenAI API with the given prompt."""
        start_time = time.time()
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        messages = []
        if system_message:
            messages.append({
                "role": "system", 
                "content": system_message
            })
        
        messages.append({
            "role": "user",
            "content": prompt
        })
        
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }
        
        logger.debug(f"API request data: model={self.model}, messages_count={len(messages)}")
        
        try:
            # Use httpx instead of requests for modern async capabilities
            with httpx.Client(timeout=60.0) as client:
                logger.debug("Sending request to OpenAI API...")
                response = client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers=headers,
                    json=data  # json parameter automatically handles serialization
                )
                
                api_call_time = time.time() - start_time
                logger.debug(f"OpenAI API response received in {api_call_time:.2f} seconds")
                logger.debug(f"Response status code: {response.status_code}")
                
                if response.status_code != 200:
                    logger.error(f"OpenAI API error: status={response.status_code}, response={response.text}")
                    raise Exception(f"OpenAI API error: {response.text}")
                
                result = response.json()
                
                # Log usage information if available
                if "usage" in result:
                    usage = result["usage"]
                    logger.info(f"Token usage - prompt: {usage.get('prompt_tokens', 'N/A')}, "
                              f"completion: {usage.get('completion_tokens', 'N/A')}, "
                              f"total: {usage.get('total_tokens', 'N/A')}")

                return result["choices"][0]["message"]["content"]
                
        except Exception as e:
            error_time = time.time() - start_time
            logger.error(f"OpenAI API call failed after {error_time:.2f}s: {str(e)}")
            raise
        
    def answer_question(self, question: str) -> Dict[str, Any]:
        """
        Answer a medical question based on retrieved documents.
        
        Args: 
            question: The medical question
            
        Returns: 
            Dict with question, answer, and source documents
        """
        start_time = time.time()
        logger.info(f"Starting question answering for: '{question[:50]}{'...' if len(question) > 50 else ''}'")
        
        try:
            # Get relevant documents
            logger.debug("Retrieving relevant documents...")
            docs = self.retriever.query_by_text(question)
            logger.debug(f"Retrieved {len(docs)} relevant documents")
            
            # Create context
            context = "\n\n".join([doc["text"] for doc in docs])
            logger.debug(f"Combined context length: {len(context)} characters")
            
            # Generate prompt
            qa_prompt = f"""
            You are an AI assistant for healthcare professionals. You help doctors and nurses access
            patient information quickly and accurately. You should always strive to provide factual,
            evidence-based information from the provided context.

            When answering, please:
            1. Only use information explicitly stated in the context
            2. Cite the specific parts of the document where your answer comes from
            3. If the context doesn't contain the answer, say "I don't have enough information about that"
            4. Maintain confidentiality and privacy of all patient data
            5. Format your answers clearly, using bullet points and sections when appropriate

            Context:
            {context}

            Question: {question}
            """
            
            logger.debug(f"Generated QA prompt with {len(qa_prompt)} characters")
            
            # Get answer from OpenAI
            total_time = time.time() - start_time
            logger.info(f"Question answering completed in {total_time:.2f}s - Answer length: {len(answer)} characters")
            
            result = {
                "question": question,
                "answer": answer,
                "source_documents": docs
            }
            
            return result
            
        except Exception as e:
            error_time = time.time() - start_time
            logger.error(f"Question answering failed after {error_time:.2f}s: {str(e)}")
            raise
    
    def generate_patient_summary(self, patient_id: str) -> Dict[str, Any]:
        """
        Generate a summary of patient information.
        
        Args:
            patient_id: The patient ID
            
        Returns:
            Dict with summary and source documents
        """
        start_time = time.time()
        logger.debug(f"Starting patient summary generation for patient ID: {patient_id}")
        
        try:
            # Get patient documents
            logger.debug(f"Retrieving documents for patient ID: {patient_id}")
            patient_docs = self.retriever.get_patient_documents(patient_id)
            logger.debug(f"Retrieved {len(patient_docs)} documents for patient {patient_id}")
            
            if not patient_docs:
                logger.warning(f"No documents found for patient {patient_id}")
                return {
                    "summary": f"No information found for patient {patient_id}",
                    "source_documents": []
                }
            
            # Create context from documents
            context = "\n\n".join([doc["text"] for doc in patient_docs])
            
            # Generate prompt
            summary_prompt = f"""
        You are a medical professional reviewing patient records. Create a concise but comprehensive 
        summary of the patient information below. Include key demographics, medical history, 
        current medications, recent vitals, and any notable lab results.

        Patient Information:
        {context}

        Summary:
        """
            
            logger.debug(f"Generated summary prompt with {len(summary_prompt)} characters")
            
            # Get summary from OpenAI
            summary = self._call_openai_api(summary_prompt)
            
            total_time = time.time() - start_time
            logger.info(f"Patient summary generation completed in {total_time:.2f}s - Summary length: {len(summary)} characters")
            
            result = {
                "summary": summary,
                "source_documents": patient_docs
            }
            
            return result
            
        except Exception as e:
            error_time = time.time() - start_time
            logger.error(f"Patient summary generation failed after {error_time:.2f}s: {str(e)}")
            raise
    
    def identify_health_issues(self, patient_id: str) -> Dict[str, Any]:
        """
        Identify potential health issues based on patient records.
        
        Args:
            patient_id: The patient ID
            
        Returns:
            Dict with issues and source documents
        """
        start_time = time.time()
        
        try:
            # Get patient documents
            logger.debug(f"Retrieving documents for health issues analysis of patient ID: {patient_id}")
            patient_docs = self.retriever.get_patient_documents(patient_id)
            logger.debug(f"Retrieved {len(patient_docs)} documents for health issues analysis of patient {patient_id}")
            
            if not patient_docs:
                logger.warning(f"No documents found for health issues analysis of patient {patient_id}")
                return {
                    "issues": f"No information found for patient {patient_id}",
                    "source_documents": []
                }
            
            # Create context from documents
            context = "\n\n".join([doc["text"] for doc in patient_docs])
            logger.debug(f"Combined health issues analysis context length: {len(context)} characters")
            
            # Generate prompt
            issues_prompt = f"""
        You are a clinical decision support system analyzing patient data. Based on the following 
        patient information, identify potential health issues, risks, or areas of concern that 
        healthcare providers should be aware of. Consider factors such as vital signs, lab results, 
        medical history, medications, and any trends or abnormalities.

        Patient Information:
        {context}

        Analysis of Potential Health Issues:
        """
            
            logger.debug(f"Generated health issues analysis prompt with {len(issues_prompt)} characters")
            
            # Get analysis from OpenAI
            issues = self._call_openai_api(issues_prompt)
            
            total_time = time.time() - start_time
            logger.info(f"Health issues identification completed in {total_time:.2f}s - Analysis length: {len(issues)} characters")
            
            result = {
                "issues": issues,
                "source_documents": patient_docs
            }
            
            logger.debug(f"Returning health issues analysisgit with {len(result['source_documents'])} source documents")
            return result
            
        except Exception as e:
            error_time = time.time() - start_time
            logger.error(f"Health issues identification failed after {error_time:.2f}s: {str(e)}")
            raise
