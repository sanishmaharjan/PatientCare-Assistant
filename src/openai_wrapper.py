"""
A wrapper for the langchain_openai module.
This file helps to provide the OpenAIEmbeddings class for the tests.
"""

class OpenAIEmbeddings:
    """A simple wrapper class for OpenAI embeddings"""
    
    def __init__(self, openai_api_key=None, model=None, **kwargs):
        self.model = model
        self.openai_api_key = openai_api_key
    
    def embed_query(self, text):
        """Mock implementation for testing"""
        # Return a dummy embedding vector
        return [0.1, 0.2, 0.3, 0.4, 0.5] * 100
    
    def embed_documents(self, documents):
        """Mock implementation for testing"""
        # Return dummy embedding vectors
        return [[0.1, 0.2, 0.3, 0.4, 0.5] * 100 for _ in documents]
