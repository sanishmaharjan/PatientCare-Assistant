"""
Patient-related components for PatientCare Assistant.
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from services.api_service import api_request
from utils.data import SAMPLE_PATIENTS
from core.config import API_URL


def render_patient_metrics():
    """Render patient metrics section."""
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader(f"Welcome, Dr. {st.session_state.username}")
        st.write(f"Current Date: {datetime.now().strftime('%B %d, %Y')}")
    with col2:
        st.metric(label="Patients Today", value="6", delta="3")


def render_patient_table():
    """Render the patient table."""
    st.subheader("Patients")
    
    # Display the patient table
    df = pd.DataFrame(SAMPLE_PATIENTS)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    return df


def render_patient_selector(patients_df):
    """Render patient selection dropdown and handle patient selection."""
    st.markdown("### Select a patient to view summary")
    
    # Create options for dropdown - combine name and ID for better UX
    patient_options = [""] + [f"{patient['Name']} ({patient['Patient ID']})" for patient in SAMPLE_PATIENTS]
    
    # Create the dropdown
    selected_option = st.selectbox(
        "Select a patient",
        options=patient_options,
        key="patient_dropdown",
        label_visibility="collapsed"  # Hide the label since we have the header above
    )
    
    # When a patient is selected from dropdown, show their summary
    if selected_option and selected_option != "":
        # Extract patient ID from selection string
        selected_patient_id = selected_option.split("(")[1].replace(")", "")
        selected_patient = patients_df[patients_df["Patient ID"] == selected_patient_id].iloc[0]
        selected_patient_name = selected_patient["Name"]
        
        # Set selected patient in session state
        st.session_state.selected_patient_id = selected_patient_id
        st.session_state.selected_patient_name = selected_patient_name
        
        # Render patient card
        render_patient_card(selected_patient_name, selected_patient_id)


def render_patient_card(patient_name, patient_id):
    """Render patient card with summary options."""
    # Create a summary container with border styling
    summary_container = st.container()
    
    with summary_container:
        # Create patient card
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image("https://img.icons8.com/color/96/000000/user-male-circle--v1.png", width=100)
        with col2:
            st.subheader(f"{patient_name} ({patient_id})")
            st.caption(f"Last updated: {datetime.now().strftime('%B %d, %Y')}")
        
        # Add action buttons for patient
        col1, col2, col3 = st.columns(3)
        with col1:
            summary_button = st.button("📋 Generate Summary")
        with col2:
            issues_button = st.button("⚠️ Identify Health Issues")
        with col3:
            medician_button = st.button("💊 medications taking?")
        
        # Display information based on button clicks
        if summary_button:
            st.subheader("📋 Patient Summary")
            display_patient_summary(patient_id, "summary")
        
        if issues_button:
            st.subheader("⚠️ Potential Health Issues")
            display_patient_summary(patient_id, "health-issues")

        if medician_button:
            st.subheader("⚠️ Medications taking")
            display_patient_summary(patient_id, "medician-taking")
    
    # Add some spacing and separation
    st.markdown("---")


def display_patient_summary(patient_id, summary_type="summary"):
    """Display patient summary or health issues using API."""
    endpoint = "summary" if summary_type == "summary" else "health-issues"
    title = "Patient Summary" if summary_type == "summary" else "Potential Health Issues"
    
    with st.spinner(f"Generating {title.lower()}..."):
        success, data, error = api_request(endpoint, {"patient_id": patient_id})
        
        if success:
            # Display the summary or health issues
            content_key = "summary" if summary_type == "summary" else "issues"
            st.markdown(data[content_key])
            
            # Display sources if available
            if "sources" in data and data["sources"]:
                with st.expander("📋 View Source Documents", expanded=False):
                    for i, source in enumerate(data["sources"]):
                        with st.expander(f"Source {i+1}: {source.get('metadata', {}).get('source', 'Unknown')}", expanded=False):
                            st.write(source["text"])
                            if "metadata" in source:
                                metadata = source["metadata"]
                                if "source" in metadata:
                                    st.caption(f"📄 Source: {metadata['source']}")
                                if "date" in metadata:
                                    st.caption(f"📅 Date: {metadata['date']}")
        else:
            st.error(f"❌ {error}")
            st.info(f"💡 Please ensure the API server is running at {API_URL} and documents are processed")


def initialize_patient_session_state():
    """Initialize patient-related session state variables."""
    if "show_patient_summary" not in st.session_state:
        st.session_state.show_patient_summary = False
    if "selected_patient_id" not in st.session_state:
        st.session_state.selected_patient_id = ""
    if "selected_patient_name" not in st.session_state:
        st.session_state.selected_patient_name = ""
