"""
Python 3 compatibility module.
This file is kept for backward compatibility with existing imports,
but contains only Python 3 implementations.
"""
import sys
import os
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any, Union

# For encoding issues
def ensure_str(s: str) -> str:
    """Ensure the input is a string type."""
    if isinstance(s, bytes):
        return s.decode('utf-8')
    return s
