"""
Q&A page for PatientCare Assistant.
"""

import streamlit as st
from components.chat import render_chat_interface
from components.questions import render_suggested_questions


def render_qa():
    """Render the medical Q&A page."""
    st.header("Medical Q&A")
    st.markdown("""
    Ask questions about patient records, and the system will retrieve relevant information.
    """)
    
    try:
        # Create a two-column layout for the main content area
        chat_col, suggested_col = st.columns([3, 2])
        
        # Display chat messages in the first column
        with chat_col:
            render_chat_interface()
        
        # Display suggested questions in the second column
        with suggested_col:
            render_suggested_questions()
            
    except Exception as e:
        st.error(f"Error in Q&A: {str(e)}")
        import traceback
        st.code(traceback.format_exc())
