"""
PatientCare Assistant API package.

Modular FastAPI application for medical data processing and retrieval.
"""

from .main import app, start_api

__version__ = "1.0.0"
__all__ = ["app", "start_api"]
