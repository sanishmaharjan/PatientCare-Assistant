"""
Configuration settings for the PatientCare Assistant application.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Model settings
EMBEDDING_MODEL = "text-embedding-3-small"  # Updated from ada-002 to newer model
COMPLETION_MODEL = "gpt-3.5-turbo"  # Updated from gpt-4 to more widely available model
TEMPERATURE = 0.2
MAX_TOKENS = 1500

# Vector Database
VECTOR_DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "processed", "vector_db")

# Document settings
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# API settings
API_HOST = "localhost"  # Use localhost for frontend connections
API_PORT = 8000

# Frontend settings
FRONTEND_PORT = 8501
