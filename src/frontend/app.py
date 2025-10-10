"""
Streamlit frontend for PatientCare Assistant.
Refactored modular version.
"""

import streamlit as st
from core.config import PAGE_CONFIG, APP_TITLE, APP_DESCRIPTION
from components.navigation import render_navigation, render_authentication, render_footer
from page_modules.dashboard import render_dashboard
from page_modules.qa import render_qa  
from page_modules.upload import render_upload


def main():
    """Main application entry point."""
    # Page configuration
    st.set_page_config(**PAGE_CONFIG)
    
    # Authentication (simplified for demo) - do this first
    render_authentication()
    
    # Title and description
    st.title(APP_TITLE)
    st.markdown(APP_DESCRIPTION)
    
    # Initialize page from URL parameters or default to dashboard
    if "page" not in st.session_state:
        # Try to get page from URL query parameters
        try:
            import urllib.parse as urlparse
            import streamlit.web.server.server as server
            # This is a workaround since Streamlit doesn't have direct URL routing
            st.session_state.page = "dashboard"  # Default
        except:
            st.session_state.page = "dashboard"
    
    # Sidebar navigation
    render_navigation()
    
    # Get the current page from session state
    page = st.session_state.get("page", "dashboard")
    
    # Route to appropriate page
    try:        
        if page == "dashboard":
            render_dashboard()
        elif page == "qa":
            render_qa()
        elif page == "upload":
            render_upload()
        else:
            # Default to dashboard if unknown page
            st.warning(f"Unknown page: {page}, showing Dashboard instead")
            st.session_state.page = "dashboard"
            render_dashboard()
    except Exception as e:
        st.error(f"Error rendering page {page}: {str(e)}")
        # Show a basic fallback
        st.header(f"{page.title()} Page")
        st.write("There was an error loading this page. Please check the logs.")
        import traceback
        st.code(traceback.format_exc())
    
    # Footer
    render_footer()


if __name__ == "__main__":
    main()
