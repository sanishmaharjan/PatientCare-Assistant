"""
Utility functions for file operations and path management.
"""

import os
import datetime
from pathlib import Path
from ..config import get_data_dir


def get_paths():
    """Get standard data directory paths."""
    base_dir = Path(get_data_dir())
    return {
        "base_dir": base_dir,
        "raw_dir": base_dir / "raw",
        "processed_dir": base_dir / "processed",
        "vector_db_path": base_dir / "processed" / "vector_db",
        "sample_data_dir": base_dir / "sample-data"
    }


def ensure_directories():
    """Ensure all required directories exist."""
    paths = get_paths()
    for path in [paths["raw_dir"], paths["processed_dir"]]:
        os.makedirs(path, exist_ok=True)


def get_document_type(filename):
    """Determine document type based on file extension."""
    ext = filename.split('.')[-1].lower()
    type_mapping = {
        'pdf': "Medical Records",
        'docx': "Medical Notes",
        'doc': "Medical Notes", 
        'txt': "Lab Results",
        'md': "Patient History"
    }
    return type_mapping.get(ext, "Other")


def get_size_format(size_bytes):
    """Format file size in human-readable format."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f} MB"


def get_file_type_from_extension(filename):
    """Get file type abbreviation from filename."""
    if filename.endswith('.pdf'):
        return "PDF"
    elif filename.endswith(('.docx', '.doc')):
        return "DOC"
    elif filename.endswith('.md'):
        return "MD"
    else:
        return "TXT"


def format_datetime(timestamp):
    """Format timestamp to standard datetime string."""
    return datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")


def is_processed(filename, processed_dir):
    """Check if a file has been processed (has corresponding chunks file)."""
    return any(
        f.startswith(filename) 
        for f in os.listdir(processed_dir) 
        if f.endswith('_chunks.json')
    )


def validate_filename(filename):
    """Validate filename to prevent directory traversal."""
    return '..' not in filename and '/' not in filename
