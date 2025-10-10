"""
Utility helpers for PatientCare Assistant frontend.
"""

import os
import zipfile
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime
import streamlit as st

def format_file_size(size_bytes: int) -> str:
    """Format file size in bytes to human readable format."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f} MB"


def get_directory_size(path: Path) -> int:
    """Calculate total size of files in a directory."""
    total = 0
    if path.exists():
        for f in path.glob('**/*'):
            if f.is_file():
                total += f.stat().st_size
    return total


def format_time_ago(timestamp: float) -> str:
    """Format timestamp to human readable 'time ago' string."""
    now = datetime.now().timestamp()
    days_ago = (now - timestamp) / (60 * 60 * 24)
    
    if days_ago < 0.04:  # Less than 1 hour
        return "Just now"
    elif days_ago < 1:
        hours_ago = int(days_ago * 24)
        return f"{hours_ago} hour{'s' if hours_ago != 1 else ''} ago"
    else:
        days_ago = int(days_ago)
        return f"{days_ago} day{'s' if days_ago != 1 else ''} ago"


def get_file_icon(filename: str) -> str:
    """Get appropriate emoji icon for file type."""
    if filename.endswith('.pdf'):
        return "📕"
    elif filename.endswith(('.docx', '.doc')):
        return "📘"
    elif filename.endswith('.md'):
        return "📝"
    elif filename.endswith('.txt'):
        return "📄"
    else:
        return "📄"


def create_download_zip(file_paths: List[Path], zip_name: str = "documents.zip") -> bytes:
    """Create a zip file in memory from a list of file paths."""
    import io
    
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for file_path in file_paths:
            if file_path.exists():
                zip_file.write(file_path, arcname=file_path.name)
    
    zip_buffer.seek(0)
    return zip_buffer.getvalue()


def format_patient_date(date_str: str) -> str:
    """Format patient date from API format to display format."""
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        return date_obj.strftime("%B %d, %Y")
    except:
        return date_str  # Return original if parsing fails


def validate_file_type(filename: str, allowed_types: List[str] = None) -> bool:
    """Validate if file type is allowed."""
    if allowed_types is None:
        allowed_types = ['.pdf', '.docx', '.doc', '.txt', '.md']
    
    file_ext = Path(filename).suffix.lower()
    return file_ext in allowed_types


def get_project_root() -> Path:
    """Get the project root directory."""
    current_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    # Go up from frontend/utils to project root
    return current_dir.parent.parent.parent


def get_data_directories() -> Dict[str, Path]:
    """Get standard data directory paths."""
    project_root = get_project_root()
    return {
        'raw': project_root / "data" / "raw",
        'processed': project_root / "data" / "processed", 
        'vector_db': project_root / "data" / "processed" / "vector_db",
        'sample_data': project_root / "data" / "sample-data"
    }

def load_css_file(css_file_path: str) -> None:
    """Load CSS file and inject it into Streamlit app."""
    try:
        with open(css_file_path, 'r') as f:
            css_content = f.read()
        st.markdown(f'<style>{css_content}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"CSS file not found: {css_file_path}")
    except Exception as e:
        st.error(f"Error loading CSS file: {e}")
