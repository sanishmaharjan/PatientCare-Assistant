"""
API configuration and settings.
"""

import os
import sys
import logging

# Add src to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from config import API_HOST, API_PORT
except ImportError:
    # Fallback values if config import fails
    API_HOST = "localhost"
    API_PORT = 8000

# Disable ChromaDB telemetry
os.environ["ANONYMIZED_TELEMETRY"] = "False"
os.environ["CHROMA_SERVER_AUTHN_PROVIDER"] = ""

# API metadata
API_TITLE = "PatientCare Assistant API"
API_DESCRIPTION = "API for retrieving and analyzing patient information"
API_VERSION = "1.0.0"

# CORS settings
CORS_ORIGINS = ["*"]  # In production, restrict this
CORS_CREDENTIALS = True
CORS_METHODS = ["*"]
CORS_HEADERS = ["*"]

# Logging configuration
LOG_FORMAT = "%(asctime)s - %(levelname)s - [API] %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_LEVEL = logging.INFO

def get_log_dir():
    """Get the logs directory path."""
    return os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), 
        "logs"
    )

def get_data_dir():
    """Get the data directory path."""
    return os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), 
        "data"
    )
