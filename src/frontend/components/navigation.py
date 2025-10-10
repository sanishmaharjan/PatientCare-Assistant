"""
Navigation component for PatientCare Assistant.
"""

import streamlit as st
import os
from core.config import NAVIGATION_ITEMS, NAV_DISPLAY_LABELS, NAV_PAGE_VALUES, APP_TITLE
from utils.helpers import load_css_file


def render_navigation():
    """Render the sidebar navigation."""
    with st.sidebar:
        # Title
        st.title("Navigation")
        
        # Load navigation CSS
        css_path = os.path.join(os.path.dirname(__file__), '..', 'styles', 'navigation.css')
        load_css_file(css_path)
        
        # Initialize page in session state if not present
        if "page" not in st.session_state:
            st.session_state.page = "dashboard"
        
        # Create navigation items
        navigation_items = NAVIGATION_ITEMS
        nav_display_labels = NAV_DISPLAY_LABELS
        nav_page_values = NAV_PAGE_VALUES
        
        for nav_item in navigation_items:
            is_active = st.session_state.page == nav_page_values[nav_item]
            button_type = "primary" if is_active else "secondary"
            
            if st.button(nav_display_labels[nav_item], 
                        key=f"nav_{nav_item}", 
                        width="stretch",
                        type=button_type,
                        help=f"Go to {nav_item} page"):
                st.session_state.page = nav_page_values[nav_item]
                st.rerun()


def render_authentication():
    """Render authentication section."""
    with st.sidebar:
        # Set default username for the session
        if "username" not in st.session_state:
            st.session_state.username = "Provider"
        
        # Always set logged_in to True to bypass authentication
        st.session_state.logged_in = True


def render_footer():
    """Render the application footer."""
    st.markdown("---")
    st.markdown("PatientCare Assistant | Powered by LangChain and OpenAI")
