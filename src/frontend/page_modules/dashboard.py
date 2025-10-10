"""
Dashboard page for PatientCare Assistant.
"""

import streamlit as st
from components.patient import (
    render_patient_metrics,
    render_patient_table, 
    render_patient_selector,
    initialize_patient_session_state
)


def render_dashboard():
    """Render the healthcare provider dashboard."""
    st.header("Healthcare Provider Dashboard")
    
    try:
        # Initialize patient session state
        initialize_patient_session_state()
        
        # Display current date and time with patient metrics
        render_patient_metrics()
        
        # Display patient table
        patients_df = render_patient_table()
        
        # Patient selector and card
        render_patient_selector(patients_df)
        
    except Exception as e:
        st.error(f"Error in dashboard: {str(e)}")
        import traceback
        st.code(traceback.format_exc())
