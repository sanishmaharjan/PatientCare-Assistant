"""
Routers package initialization.
"""

from .medical import router as medical_router
from .documents import router as documents_router

__all__ = [
    "medical_router",
    "documents_router"
]
