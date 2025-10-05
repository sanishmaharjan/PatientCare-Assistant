"""
Streamlit frontend for PatientCare Assistant.
"""

import os
import sys
import json
from typing import Dict, List, Any, Optional
import pandas as pd
import streamlit as st
import httpx
from datetime import datetime

# Local imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import API_HOST, API_PORT

# API endpoint - Python 3 string formatting
API_URL = f"http://{API_HOST}:{API_PORT}"

# Page configuration
st.set_page_config(
    page_title="PatientCare Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and description
st.title("🏥 PatientCare Assistant")
st.markdown("""
This application helps healthcare providers quickly access and analyze patient information.
""")

# Authentication (simplified for demo)
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/hospital-3.png", width=100)
    st.title("Healthcare Provider")
    
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    
    if not st.session_state.logged_in:
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Login"):
            if username and password:  # Simplified auth for demo
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Invalid credentials")
    else:
        st.success(f"Logged in as {st.session_state.username}")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()
        
        # Sidebar navigation
        st.title("Navigation")
        page = st.radio("Select a page", ["Dashboard", "Patient Search", "Q&A", "Analysis", "Settings"])

# Only show content if logged in
if not st.session_state.get("logged_in", False):
    st.warning("Please log in to use the application")
    st.info("Use any username and password for demo purposes")
else:
    if page == "Dashboard":
        st.header("Healthcare Provider Dashboard")
        
        # Display current date and time
        col1, col2 = st.columns([2, 1])
        with col1:
            st.subheader(f"Welcome, Dr. {st.session_state.username}")
            st.write(f"Current Date: {datetime.now().strftime('%B %d, %Y')}")
        with col2:
            st.metric(label="Patients Today", value="12", delta="3")
        
        # Recent patients section
        st.subheader("Recent Patients")
        recent_patients = [
            {"Patient ID": "PATIENT-12345", "Name": "Jane Doe", "Last Visit": "October 2, 2025", "Status": "Follow-up"},
            {"Patient ID": "PATIENT-12346", "Name": "John Smith", "Last Visit": "October 3, 2025", "Status": "Stable"},
            {"Patient ID": "PATIENT-12347", "Name": "Maria Garcia", "Last Visit": "October 4, 2025", "Status": "New"}
        ]
        st.dataframe(pd.DataFrame(recent_patients), use_container_width=True)
        
        # Quick actions
        st.subheader("Quick Actions")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🔍 Search Patient"):
                st.session_state.page = "Patient Search"
                st.rerun()
        with col2:
            if st.button("❓ Medical Q&A"):
                st.session_state.page = "Q&A"
                st.rerun()
        with col3:
            if st.button("📊 Analysis"):
                st.session_state.page = "Analysis"
                st.rerun()
        
        # Notifications
        with st.expander("Notifications (3)"):
            st.info("New lab results for Patient PATIENT-12345")
            st.info("Medication review required for Patient PATIENT-12346")
            st.warning("Follow-up appointment scheduled for Patient PATIENT-12347")

    elif page == "Patient Search":
        st.header("Patient Search")
        
        # Patient search tabs
        tab1, tab2 = st.tabs(["Search by ID", "Browse Patients"])
        
        with tab1:
            # Patient ID input
            patient_id = st.text_input("Enter Patient ID", "PATIENT-12345")
            
            # Action buttons
            col1, col2, col3 = st.columns(3)
            with col1:
                summary_button = st.button("📋 Generate Summary")
            with col2:
                issues_button = st.button("⚠️ Identify Health Issues")
            with col3:
                history_button = st.button("📜 View History")
            
            # Handle summary generation
            if summary_button:
                with st.spinner("Generating patient summary..."):
                    try:
                        # Using a synchronous client instead of async
                        response = httpx.post(
                            f"{API_URL}/summary",
                            json={"patient_id": patient_id},
                            timeout=30.0
                        )
                        
                        if response.status_code == 200:
                            data = response.json()
                            st.success("Summary generated successfully")
                            st.subheader("Patient Summary")
                            
                            # Create patient card
                            with st.container():
                                col1, col2 = st.columns([1, 3])
                                with col1:
                                    st.image("https://img.icons8.com/color/96/000000/user-male-circle--v1.png", width=100)
                                with col2:
                                    st.subheader(f"Patient-{patient_id}")
                                    st.caption("Last updated")
                            
                            st.markdown(data["summary"])
                            
                            # Show sources
                            with st.expander("View Source Documents"):
                                st.subheader("Sources")
                                for i, source in enumerate(data["sources"]):
                                    with st.expander(f"Source {i+1}"):
                                        st.write(source["text"])
                                        st.caption(f"Source: {source['metadata'].get('source', 'Unknown')}")
                        else:
                            st.error(f"Error: {response.text}")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
            
            # Handle health issues identification
            if issues_button:
                with st.spinner("Identifying health issues..."):
                    try:
                        # Using a synchronous client instead of async
                        response = httpx.post(
                            f"{API_URL}/health-issues",
                            json={"patient_id": patient_id},
                            timeout=30.0
                        )
                        
                        if response.status_code == 200:
                            data = response.json()
                            st.success("Analysis complete")
                            st.subheader("Potential Health Issues")
                            st.markdown(data["issues"])
                            
                            # Show sources
                            with st.expander("View Source Documents"):
                                st.subheader("Sources")
                                for i, source in enumerate(data["sources"]):
                                    with st.expander(f"Source {i+1}"):
                                        st.write(source["text"])
                                        st.caption(f"Source: {source['metadata'].get('source', 'Unknown')}")
                        else:
                            st.error(f"Error: {response.text}")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
            
            # Handle history view (demo)
            if history_button:
                st.subheader("Patient History")
                history_data = [
                    {"Date": "Sep 15, 2025", "Type": "Office Visit", "Provider": "Dr. Johnson", "Notes": "Routine checkup"},
                    {"Date": "Aug 22, 2025", "Type": "Lab Work", "Provider": "Lab Corp", "Notes": "Blood panel"},
                    {"Date": "Jul 10, 2025", "Type": "Prescription", "Provider": "Dr. Johnson", "Notes": "Renewed metformin prescription"},
                    {"Date": "Jun 5, 2025", "Type": "Office Visit", "Provider": "Dr. Smith", "Notes": "Blood pressure follow-up"}
                ]
                st.dataframe(pd.DataFrame(history_data), use_container_width=True)
        
        with tab2:
            st.subheader("Browse Patients")
            # Demo patient list
            patients = [
                {"Patient ID": "PATIENT-12345", "Name": "Jane Doe", "Age": 57, "Gender": "Female", "Primary Condition": "Hypertension, Diabetes"},
                {"Patient ID": "PATIENT-12346", "Name": "John Smith", "Age": 62, "Gender": "Male", "Primary Condition": "Coronary Artery Disease"},
                {"Patient ID": "PATIENT-12347", "Name": "Maria Garcia", "Age": 45, "Gender": "Female", "Primary Condition": "Asthma"},
                {"Patient ID": "PATIENT-12348", "Name": "Robert Johnson", "Age": 71, "Gender": "Male", "Primary Condition": "Arthritis, Hypertension"},
                {"Patient ID": "PATIENT-12349", "Name": "Susan Williams", "Age": 38, "Gender": "Female", "Primary Condition": "Migraine"}
            ]
            st.dataframe(pd.DataFrame(patients), use_container_width=True)
            
            # Patient filters
            col1, col2 = st.columns(2)
            with col1:
                st.selectbox("Filter by Condition", ["All", "Hypertension", "Diabetes", "Asthma", "Arthritis", "Other"])
            with col2:
                st.selectbox("Sort by", ["Name", "Age", "Recent Visit"])

    elif page == "Q&A":
        st.header("Medical Q&A")
        st.markdown("""
        Ask questions about patient records, and the system will retrieve relevant information.
        """)
        
        # Chat interface
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {"role": "assistant", "content": "I'm your medical assistant. How can I help you today?"}
            ]
        
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask a medical question..."):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Generate assistant response
            with st.chat_message("assistant"):
                with st.spinner("Processing question..."):
                    try:
                        # Using a synchronous client instead of async
                        response = httpx.post(
                            f"{API_URL}/answer",
                            json={"question": prompt},
                            timeout=60.0
                        )
                        
                        if response.status_code == 200:
                            data = response.json()
                            message_placeholder = st.empty()
                            message_placeholder.markdown(data["answer"])
                            
                            # Add assistant response to chat history
                            st.session_state.messages.append({"role": "assistant", "content": data["answer"]})
                            
                            # Show sources
                            with st.expander("View Sources"):
                                st.subheader("Sources")
                                for i, source in enumerate(data["sources"]):
                                    with st.expander(f"Source {i+1}"):
                                        st.write(source["text"])
                                        if "metadata" in source:
                                            st.caption(f"Source: {source['metadata'].get('source', 'Unknown')}")
                        else:
                            st.error(f"Error: {response.text}")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                        st.session_state.messages.append({"role": "assistant", "content": f"I'm sorry, an error occurred: {str(e)}"})
        
        # Suggested questions
        with st.sidebar:
            st.subheader("Suggested Questions")
            example_questions = [
                "What medications is patient 12345 taking?",
                "What are the recent lab results for the diabetic patient?",
                "Are there any drug interactions to be concerned about?",
                "What is the patient's blood pressure trend?",
                "Summarize the patient's medical history"
            ]
            for q in example_questions:
                if st.button(q):
                    # Add user message to chat history
                    st.session_state.messages.append({"role": "user", "content": q})
                    st.rerun()

    elif page == "Analysis":
        st.header("Patient Data Analysis")
        st.markdown("""
        Upload patient documents for analysis or explore existing data.
        """)
        
        # Analysis options
        analysis_type = st.selectbox(
            "Select Analysis Type",
            ["Document Upload", "Lab Results Trends", "Medication Effectiveness", "Population Health"]
        )
        
        if analysis_type == "Document Upload":
            # File upload section
            st.subheader("Upload Patient Documents")
            upload_col1, upload_col2 = st.columns([2, 1])
            
            with upload_col1:
                uploaded_files = st.file_uploader("Upload patient documents", type=["pdf", "docx", "txt"], accept_multiple_files=True)
                
                if uploaded_files:
                    st.success(f"{len(uploaded_files)} file(s) uploaded successfully")
                    for file in uploaded_files:
                        st.info(f"File: {file.name}")
                    
                    process_button = st.button("Process Documents")
                    if process_button:
                        with st.spinner("Processing documents... This may take a minute."):
                            st.info("Document processing simulation (no actual backend processing)")
                            st.success("Documents processed and embeddings generated")
            
            with upload_col2:
                st.info("Supported Formats")
                st.write("- PDF (.pdf)")
                st.write("- Word (.docx, .doc)")
                st.write("- Text (.txt)")
                st.write("- Markdown (.md)")
                
                with st.expander("Processing Steps"):
                    st.write("1. Document parsing")
                    st.write("2. Text extraction")
                    st.write("3. Chunking")
                    st.write("4. Embedding generation")
                    st.write("5. Vector database indexing")
        
        elif analysis_type == "Lab Results Trends":
            st.subheader("Lab Results Trends")
            
            # Demo data for visualization
            patient_select = st.selectbox("Select Patient", ["PATIENT-12345", "PATIENT-12346", "PATIENT-12347"])
            metric = st.selectbox("Select Metric", ["HbA1c", "Blood Glucose", "Cholesterol", "Blood Pressure"])
            
            # Show demo chart
            st.subheader(f"{metric} Trend - Patient {patient_select}")
            
            # Demo data
            chart_data = pd.DataFrame({
                'Date': pd.date_range(start='1/1/2025', periods=6, freq='M'),
                'Value': [7.2, 7.0, 6.8, 6.9, 6.7, 6.5]
            })
            st.line_chart(chart_data.set_index('Date'))
            
            if metric == "HbA1c":
                st.info("HbA1c target range: 7% - 6.4%")
                st.success("Patient showing improvement trend over time")
        
        elif analysis_type == "Medication Effectiveness":
            st.subheader("Medication Effectiveness Analysis")
            
            medication = st.selectbox("Select Medication", ["Metformin", "Lisinopril", "Atorvastatin"])
            st.write(f"Analyzing effectiveness of {medication} across patient population")
            
            # Demo visualization
            effect_data = pd.DataFrame({
                'Effectiveness': ['Highly Effective', 'Moderately Effective', 'Minimal Effect', 'No Effect'],
                'Percentage': [45, 30, 15, 10]
            })
            st.bar_chart(effect_data.set_index('Effectiveness'))
            
            with st.expander("Detailed Analysis"):
                st.write(f"{medication} shows a 75% overall effectiveness rate across the patient population.")
                st.write("Side effects were reported in 15% of patients.")
                st.write("Recommended adjustments to dosage based on patient response patterns.")
        
        else:
            st.subheader("Population Health Overview")
            
            # Demo data
            st.write("Top 5 Conditions in Patient Population")
            conditions_data = pd.DataFrame({
                'Condition': ['Hypertension', 'Type 2 Diabetes', 'Hyperlipidemia', 'Obesity', 'Depression'],
                'Percentage': [42, 38, 35, 28, 22]
            })
            st.bar_chart(conditions_data.set_index('Condition'))
            
            st.subheader("Age Distribution")
            age_data = pd.DataFrame({
                'Age Group': ['18-30', '31-45', '46-60', '61-75', '76+'],
                'Count': [45, 120, 210, 175, 90]
            })
            st.bar_chart(age_data.set_index('Age Group'))
    
    elif page == "Settings":
        st.header("Settings")
        
        # Settings tabs
        tabs = st.tabs(["User Profile", "API Configuration", "Model Settings", "Display Settings"])
        
        with tabs[0]:
            st.subheader("User Profile")
            st.write(f"Username: {st.session_state.username}")
            st.write("Role")
            st.write("Last Login")
            
            with st.expander("Edit Profile"):
                st.text_input("Name", value=st.session_state.username)
                st.text_input("Email", value=f"{st.session_state.username.lower()}@hospital.org")
                st.selectbox("Department", ["Primary Care", "Cardiology", "Endocrinology", "Neurology"])
                if st.button("Save Changes"):
                    st.success("Profile updated successfully")
        
        with tabs[1]:
            st.subheader("API Configuration")
            st.text_input("API Endpoint", value=API_URL)
            api_key = st.text_input("OpenAI API Key", value="••••••••••••••••••••••••", type="password")
            if st.button("Test Connection"):
                st.success("Connection successful")
        
        with tabs[2]:
            st.subheader("Model Settings")
            st.selectbox("Embedding Model", ["text-embedding-ada-002", "text-embedding-3-small", "text-embedding-3-large"])
            st.selectbox("Completion Model", ["gpt-4", "gpt-3.5-turbo", "gpt-4-turbo"])
            st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.2, step=0.1)
            st.slider("Max Tokens", min_value=100, max_value=4000, value=1500, step=100)
            if st.button("Save Model Settings"):
                st.success("Model settings saved")
        
        with tabs[3]:
            st.subheader("Display Settings")
            st.checkbox("Dark Mode", value=False)
            st.checkbox("Compact View", value=True)
            st.selectbox("Font Size", ["Small", "Medium", "Large"])
            st.radio("Default Page", ["Dashboard", "Patient Search", "Q&A"])

# Footer
st.markdown("---")
st.markdown("PatientCare Assistant | Powered by LangChain and OpenAI")


if __name__ == "__main__":
    # This will only be used when running the script directly
    # When imported as a module, Streamlit handles execution
    pass
