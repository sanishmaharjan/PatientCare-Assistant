"""
Medical chain functionality implementation using modern Python 3 features.
This uses langchain which is compatible with Python 3.
"""

import os
import sys
import json
from typing import Dict, List, Any, Optional

# Modern HTTP library in Python 3
import httpx

# Local imports - use modern relative imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import OPENAI_API_KEY, COMPLETION_MODEL, TEMPERATURE, MAX_TOKENS
from retriever.medical_retriever import MedicalRetriever


class MedicalChain:
    """Chain for handling medical queries about patient data (Python 3 compatible)."""
    
    def __init__(self) -> None:
        """Initialize the medical chain."""
        # Initialize retriever
        self.retriever = MedicalRetriever()
        
        # OpenAI API settings
        self.api_key = OPENAI_API_KEY
        self.model = COMPLETION_MODEL
        self.temperature = TEMPERATURE
        self.max_tokens = MAX_TOKENS
        
        # Chat history (simple implementation)
        self.chat_history: List[Dict[str, str]] = []
    
    def _call_openai_api(self, prompt: str, system_message: Optional[str] = None) -> str:
        """Call the OpenAI API with the given prompt."""
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
        
        # Use httpx instead of requests for modern async capabilities
        with httpx.Client(timeout=60.0) as client:
            response = client.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=data  # json parameter automatically handles serialization
            )
        
        if response.status_code != 200:
            raise Exception(f"OpenAI API error: {response.text}")
        
        result = response.json()
        return result["choices"][0]["message"]["content"]
        
    def answer_question(self, question: str) -> Dict[str, Any]:
        """
        Answer a medical question based on retrieved documents.
        
        Args: 
            question: The medical question
            
        Returns: 
            Dict with question, answer, and source documents
        """
        # Get relevant documents
        docs = self.retriever.query_by_text(question)
        
        # Create context
        context = "\n\n".join([doc["text"] for doc in docs])
        
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
        
        # Get answer from OpenAI
        answer = self._call_openai_api(qa_prompt)
        
        return {
            "question": question,
            "answer": answer,
            "source_documents": docs
        }
    
    def generate_patient_summary(self, patient_id: str) -> Dict[str, Any]:
        """
        Generate a summary of patient information.
        
        Args:
            patient_id: The patient ID
            
        Returns:
            Dict with summary and source documents
        """
        # Get patient documents
        patient_docs = self.retriever.get_patient_documents(patient_id)
        
        if not patient_docs:
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
         # Get summary from OpenAI
        summary = self._call_openai_api(summary_prompt)
        
        return {
            "summary": summary,
            "source_documents": patient_docs
        }
    
    def identify_health_issues(self, patient_id: str) -> Dict[str, Any]:
        """
        Identify potential health issues based on patient records.
        
        Args:
            patient_id: The patient ID
            
        Returns:
            Dict with issues and source documents
        """
        # Get patient documents
        patient_docs = self.retriever.get_patient_documents(patient_id)
        
        if not patient_docs:
            return {
                "issues": f"No information found for patient {patient_id}",
                "source_documents": []
            }
        
        # Create context from documents
        context = "\n\n".join([doc["text"] for doc in patient_docs])
        
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
        
        # Get analysis from OpenAI
        issues = self._call_openai_api(issues_prompt)
        
        return {
            "issues": issues,
            "source_documents": patient_docs
        }


if __name__ == "__main__":
    # Example usage
    chain = MedicalChain()
    
    # Example question
    result = chain.answer_question("What medications is the patient taking for diabetes?")
    print("Question:", result["question"])
    print("Answer:", result["answer"])
    
    # Example patient summary
    summary = chain.generate_patient_summary("PATIENT-12345")
    print("\nPatient Summary:")
    print(summary["summary"])
