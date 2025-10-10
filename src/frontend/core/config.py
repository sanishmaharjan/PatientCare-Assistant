"""
Core configuration for Streamlit PatientCare Assistant
"""

# API Configuration - using hardcoded values for now
API_HOST = "localhost"
API_PORT = 8000
API_URL = f"http://{API_HOST}:{API_PORT}"
API_TIMEOUT = 60.0

# Streamlit Page Configuration
PAGE_CONFIG = {
    "page_title": "PatientCare Assistant",
    "page_icon": "🏥",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Navigation Configuration
NAVIGATION_ITEMS = ["dashboard", "qa", "upload"]
NAV_DISPLAY_LABELS = {
    "dashboard": "🏠 Dashboard", 
    "qa": "💬 Medical Q&A", 
    "upload": "📁 Upload Data"
}
NAV_PAGE_VALUES = {
    "dashboard": "dashboard", 
    "qa": "qa", 
    "upload": "upload"
}

# Application Metadata
APP_TITLE = "🏥 PatientCare Assistant"
APP_DESCRIPTION = """
This application helps healthcare providers quickly access and analyze patient information.
"""
