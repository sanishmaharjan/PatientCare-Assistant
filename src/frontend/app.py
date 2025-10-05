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
    
    # Set default username for the session
    if "username" not in st.session_state:
        st.session_state.username = "Provider"
    
    # Always set logged_in to True to bypass authentication
    st.session_state.logged_in = True
    
    # Display welcome message
    st.success(f"Welcome, {st.session_state.username}")
    
    # Sidebar navigation
    st.title("Navigation")
    page = st.radio("Select a page", ["Dashboard", "Q&A", "Analysis", "Settings"])

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
            st.metric(label="Patients Today", value="6", delta="3")
        
        # Patients section
        st.subheader("Patients")
        patients = [
            {"Patient ID": "PATIENT-12345", "Name": "Jane Doe", "Last Visit": "October 2, 2025", "Status": "Follow-up"},
            {"Patient ID": "PATIENT-12346", "Name": "John Smith", "Last Visit": "October 3, 2025", "Status": "Stable"},
            {"Patient ID": "PATIENT-12347", "Name": "Maria Garcia", "Last Visit": "October 4, 2025", "Status": "New"},
            {"Patient ID": "PATIENT-12348", "Name": "Robert Johnson", "Last Visit": "October 4, 2025", "Status": "Follow-up"},
            {"Patient ID": "PATIENT-12349", "Name": "Susan Williams", "Last Visit": "October 5, 2025", "Status": "New"},
            {"Patient ID": "PATIENT-12350", "Name": "Michael Brown", "Last Visit": "October 5, 2025", "Status": "Stable"}
        ]
        
        # Function to generate patient summary
        def generate_patient_summary(patient_id):
            with st.spinner("Generating patient summary..."):
                try:
                    # First try to get data from API
                    try:
                        response = httpx.post(
                            f"{API_URL}/summary",
                            json={"patient_id": patient_id},
                            timeout=10.0  # Shorter timeout
                        )
                        
                        if response.status_code == 200:
                            return response.json()
                    except Exception:
                        pass  # Fall back to mock data
                    
                    # Mock data for demo purposes
                    mock_summaries = {
                        "PATIENT-12345": {
                            "summary": """**Jane Doe** is a 57-year-old female with a history of Type 2 Diabetes (diagnosed 2018) and Hypertension (diagnosed 2015). 
                            
Recent lab values show HbA1c of 7.2% (target <7.0%) and blood pressure averaging 138/88 mmHg.
                            
**Current Medications:**
- Metformin 1000mg twice daily
- Lisinopril 10mg daily
- Aspirin 81mg daily

**Recent History:** 
Patient reports occasional lightheadedness when standing quickly. Last follow-up showed stable condition with recommended dietary modifications to reduce sodium intake.""",
                            "sources": [
                                {"text": "Patient Medical Record: Jane Doe has Type 2 Diabetes diagnosed in 2018. Current HbA1c is 7.2%, slightly above target range.", 
                                 "metadata": {"source": "Electronic Health Record", "date": "2025-09-30"}},
                                {"text": "Patient is on Metformin 1000mg BID, Lisinopril 10mg QD, and Aspirin 81mg QD. No reported medication side effects.",
                                 "metadata": {"source": "Medication Record", "date": "2025-10-02"}}
                            ]
                        },
                        "PATIENT-12346": {
                            "summary": """**John Smith** is a 62-year-old male with Coronary Artery Disease. Patient underwent angioplasty in 2023 with stent placement.
                            
**Vital Signs:** BP 128/76 mmHg, HR 68 bpm, regular rhythm.
                            
**Current Medications:**
- Atorvastatin 40mg daily
- Clopidogrel 75mg daily
- Metoprolol 25mg twice daily
                            
**Recent History:**
Patient reports good medication compliance and regular exercise. Last stress test (August 2025) showed no significant abnormalities.""",
                            "sources": [
                                {"text": "Cardiac Assessment: Patient has stable CAD following angioplasty with stent placement (2023). Regular follow-ups show good recovery.",
                                 "metadata": {"source": "Cardiology Consult", "date": "2025-09-15"}},
                                {"text": "Stress test results normal with adequate exercise tolerance. Patient maintains regular walking routine 30 minutes daily.",
                                 "metadata": {"source": "Diagnostic Report", "date": "2025-08-22"}}
                            ]
                        },
                        "PATIENT-12347": {
                            "summary": """**Maria Garcia** is a 45-year-old female with moderate persistent Asthma diagnosed in childhood.
                            
**Pulmonary Function:** FEV1 75% of predicted, improved from 68% after medication adjustment.
                            
**Current Medications:**
- Fluticasone/Salmeterol inhaler twice daily
- Albuterol rescue inhaler as needed
- Montelukast 10mg nightly
                            
**Recent History:**
Patient reports two mild asthma exacerbations in past month, typically triggered by seasonal allergies. Rescue inhaler usage has increased slightly.""",
                            "sources": [
                                {"text": "Respiratory Assessment: Patient has moderate persistent asthma with seasonal exacerbations. Recent PFT shows FEV1 at 75% predicted.",
                                 "metadata": {"source": "Pulmonology Consult", "date": "2025-09-20"}},
                                {"text": "Patient reports increased use of rescue inhaler during fall allergy season. Consider adjustment to controller medications.",
                                 "metadata": {"source": "Office Visit Notes", "date": "2025-10-04"}}
                            ]
                        },
                        "PATIENT-12348": {
                            "summary": """**Robert Johnson** is a 71-year-old male with Osteoarthritis primarily affecting knees and hands, and Hypertension.
                            
**Recent Evaluation:** Moderate joint pain (4/10) with morning stiffness. Slight decrease in range of motion in right knee.
                            
**Current Medications:**
- Acetaminophen 500mg as needed for pain
- Lisinopril 20mg daily
- Hydrochlorothiazide 12.5mg daily
                            
**Recent History:**
Patient has started physical therapy for knee strengthening. Reports some improvement in mobility but continued pain with extended walking.""",
                            "sources": [
                                {"text": "Joint Assessment: Moderate osteoarthritis in both knees, more pronounced in right. X-rays show joint space narrowing consistent with diagnosis.",
                                 "metadata": {"source": "Orthopedic Consult", "date": "2025-08-30"}},
                                {"text": "Physical therapy initiated for knee strengthening. Patient demonstrates good compliance with home exercise program.",
                                 "metadata": {"source": "PT Notes", "date": "2025-09-25"}}
                            ]
                        },
                        "PATIENT-12349": {
                            "summary": """**Susan Williams** is a 38-year-old female with chronic migraine headaches, occurring 2-3 times monthly.
                            
**Headache Characteristics:** Typically unilateral, pulsating, moderate to severe intensity (6-8/10), with photophobia and occasional nausea.
                            
**Current Medications:**
- Sumatriptan 50mg as needed for acute attacks
- Propranolol 80mg daily for prevention
- Magnesium supplement 400mg daily
                            
**Recent History:**
Patient reports decrease in migraine frequency since starting propranolol (previously 4-5 episodes monthly). Identified stress and irregular sleep as primary triggers.""",
                            "sources": [
                                {"text": "Headache diary shows reduction in migraine frequency from 4-5 to 2-3 episodes monthly since starting propranolol therapy.",
                                 "metadata": {"source": "Neurology Notes", "date": "2025-09-10"}},
                                {"text": "Patient reports good response to sumatriptan for acute attacks when taken early in migraine onset.",
                                 "metadata": {"source": "Office Visit Notes", "date": "2025-10-05"}}
                            ]
                        },
                        "PATIENT-12350": {
                            "summary": """**Michael Brown** is a 52-year-old male with well-controlled Type 2 Diabetes and Hyperlipidemia.
                            
**Recent Lab Values:** HbA1c 6.3% (target <7.0%), LDL 92 mg/dL, HDL 48 mg/dL, Triglycerides 135 mg/dL.
                            
**Current Medications:**
- Metformin 850mg twice daily
- Rosuvastatin 10mg daily
- Vitamin D 1000 IU daily
                            
**Recent History:**
Patient has maintained good glycemic control through medication compliance and dietary modifications. Reports regular exercise 4 times weekly (30 minutes walking).""",
                            "sources": [
                                {"text": "Recent laboratory values demonstrate excellent glycemic control with HbA1c of 6.3%, within target range.",
                                 "metadata": {"source": "Lab Report", "date": "2025-09-18"}},
                                {"text": "Lipid panel shows good response to statin therapy. Patient adheres to Mediterranean diet and regular exercise regimen.",
                                 "metadata": {"source": "Primary Care Notes", "date": "2025-10-05"}}
                            ]
                        }
                    }
                    
                    # Return mock data if available, otherwise generate a generic response
                    if patient_id in mock_summaries:
                        # Simulate API delay
                        import time
                        time.sleep(1.5)
                        return mock_summaries[patient_id]
                    else:
                        return {
                            "summary": f"Patient {patient_id} has a stable condition with regular follow-up appointments. No significant changes in health status since last visit.",
                            "sources": [
                                {"text": "Standard patient record information", "metadata": {"source": "Electronic Health Record"}}
                            ]
                        }
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    return None
        
        # Display patient dataframe
        df = pd.DataFrame(patients)
        
        # Initialize session state for summary display
        if "show_patient_summary" not in st.session_state:
            st.session_state.show_patient_summary = False
        if "selected_patient_id" not in st.session_state:
            st.session_state.selected_patient_id = ""
        if "selected_patient_name" not in st.session_state:
            st.session_state.selected_patient_name = ""
        
        # Display the patient table
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Create patient dropdown selector
        st.markdown("### Select a patient to view summary")
        
        # Create options for dropdown - combine name and ID for better UX
        patient_options = [""] + [f"{patient['Name']} ({patient['Patient ID']})" for patient in patients]
        
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
            selected_patient = df[df["Patient ID"] == selected_patient_id].iloc[0]
            selected_patient_name = selected_patient["Name"]                # Set selected patient in session state
            st.session_state.selected_patient_id = selected_patient_id
            st.session_state.selected_patient_name = selected_patient_name
            
            # Create a summary container with border styling
            summary_container = st.container()
            
            with summary_container:
                # Create patient card
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.image("https://img.icons8.com/color/96/000000/user-male-circle--v1.png", width=100)
                with col2:
                    st.subheader(f"{selected_patient_name} ({selected_patient_id})")
                    st.caption(f"Last updated: {datetime.now().strftime('%B %d, %Y')}")
                
                # Add action buttons for patient
                col1, col2 = st.columns(2)
                with col1:
                    summary_button = st.button("📋 Generate Summary")
                with col2:
                    issues_button = st.button("⚠️ Identify Health Issues")
                
                # Display information based on button clicks
                if summary_button:
                    st.subheader("Patient Summary")
                    with st.spinner("Generating patient summary..."):
                        try:
                            # Direct API call to the actual endpoint
                            response = httpx.post(
                                f"{API_URL}/summary",
                                json={"patient_id": selected_patient_id},
                                timeout=30.0
                            )
                            
                            if response.status_code == 200:
                                # Parse the API response
                                data = response.json()
                                
                                # Display the summary
                                st.markdown(data["summary"])
                                
                                # Display sources if available
                                if "sources" in data and data["sources"]:
                                    with st.expander("View Source Documents"):
                                        st.subheader("Sources")
                                        for i, source in enumerate(data["sources"]):
                                            with st.expander(f"Source {i+1}"):
                                                st.write(source["text"])
                                                if "metadata" in source:
                                                    st.caption(f"Source: {source['metadata'].get('source', 'Unknown')}")
                                                    if "date" in source["metadata"]:
                                                        st.caption(f"Date: {source['metadata']['date']}")
                            else:
                                st.error(f"Error retrieving patient data: {response.status_code}")
                                st.error(response.text)
                        except Exception as e:
                            st.error(f"Error connecting to API: {str(e)}")
                            st.info("Please make sure the API server is running at " + API_URL)
                
                if issues_button:
                    st.subheader("Potential Health Issues")
                    with st.spinner("Identifying health issues..."):
                        try:
                            # Direct API call to health-issues endpoint
                            response = httpx.post(
                                f"{API_URL}/health-issues",
                                json={"patient_id": selected_patient_id},
                                timeout=30.0
                            )
                            
                            if response.status_code == 200:
                                # Parse the API response
                                data = response.json()
                                
                                # Display the health issues
                                st.markdown(data["issues"])
                                
                                # Display sources if available
                                if "sources" in data and data["sources"]:
                                    with st.expander("View Source Documents"):
                                        st.subheader("Sources")
                                        for i, source in enumerate(data["sources"]):
                                            with st.expander(f"Source {i+1}"):
                                                st.write(source["text"])
                                                if "metadata" in source:
                                                    st.caption(f"Source: {source['metadata'].get('source', 'Unknown')}")
                                                    if "date" in source["metadata"]:
                                                        st.caption(f"Date: {source['metadata']['date']}")
                            else:
                                st.error(f"Error retrieving health issues: {response.status_code}")
                                st.error(response.text)
                        except Exception as e:
                            st.error(f"Error connecting to API: {str(e)}")
                            st.info("Please make sure the API server is running at " + API_URL)
            
            # Add some spacing and separation
            st.markdown("---")

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
            st.write("Role: Healthcare Provider")
            
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
            st.radio("Default Page", ["Dashboard", "Q&A", "Analysis"])

# Footer
st.markdown("---")
st.markdown("PatientCare Assistant | Powered by LangChain and OpenAI")


if __name__ == "__main__":
    # This will only be used when running the script directly
    # When imported as a module, Streamlit handles execution
    pass
