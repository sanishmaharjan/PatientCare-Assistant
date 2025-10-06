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
    
    # Set default username for the session
    if "username" not in st.session_state:
        st.session_state.username = "Provider"
    
    # Always set logged_in to True to bypass authentication
    st.session_state.logged_in = True
    
    # Sidebar navigation
    st.title("Navigation")
    
    # Initialize page in session state if not present
    if "page" not in st.session_state:
        st.session_state.page = "Dashboard"
    
    # Navigation list with styled buttons
    st.markdown("""
    <style>
    div.nav-item {margin-bottom: 8px;}
    div.nav-item button {
        width: 100%;
        text-align: left;
        font-weight: 500;
        padding: 10px 15px;
        border: none;
        border-radius: 4px;
        transition: background-color 0.2s;
    }
    div.nav-item button.active {
        background-color: #4CAF50 !important;
        color: white !important;
    }
    div.nav-item button:hover:not(.active) {
        background-color: #f0f0f0 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Create navigation items
    for nav_item in ["Dashboard", "Q&A", "Analysis"]:
        button_class = "active" if st.session_state.page == nav_item else ""
        if st.button(nav_item, key=f"nav_{nav_item}", use_container_width=True, 
                   help=f"Go to {nav_item} page"):
            st.session_state.page = nav_item
            st.rerun()
    
    # Use the page from session state
    page = st.session_state.page

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
        
        # Create a two-column layout for the main content area
        chat_col, suggested_col = st.columns([3, 2])
        
        # Display chat messages in the first column
        with chat_col:
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
        
        # Display suggested questions in the second column
        with suggested_col:
            st.subheader("Suggested Questions")
            st.markdown("""
            <div style="font-size: 0.9em; color: #666; margin-bottom: 12px;">
            Click any question below to get an instant answer. Questions are grouped by category.
            </div>
            """, unsafe_allow_html=True)
            
            # Add styles for question buttons and category toggle buttons
            st.markdown("""
            <style>
            /* Style for regular question buttons */
            div.stButton > button {
                width: 100%;
                text-align: left;
                padding: 0.4em 0.6em;
                margin-bottom: 0.4em;
                background-color: #f0f7ff;
                color: #0066cc;
                border: 1px solid #99ccff;
                border-radius: 5px;
                font-size: 0.85em;
                transition: all 0.3s;
                line-height: 1.2;
                white-space: normal;
                height: auto;
                min-height: 0;
            }
            div.stButton > button:hover {
                background-color: #cce5ff;
                border-color: #0066cc;
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            }
            
            /* Ensure question buttons stand out from category headers */
            div.stButton > button:not(:has(span:first-child:contains("📂"))):not(:has(span:first-child:contains("📁"))) {
                background-color: #f0f7ff;
                font-size: 0.85em;
                padding: 6px 10px;
                margin-bottom: 5px;
            }
            
            /* Style for category toggle buttons */
            [data-testid="stButton"] > button[kind="secondary"] {
                background-color: #f8f9fa;
                color: #444;
                font-size: 0.95em;
                font-weight: 600;
                text-align: left;
                border-left: 4px solid #0066cc;
                padding: 8px 10px;
                margin-top: 0.8em;
                margin-bottom: 0.4em;
                border-radius: 4px;
                transition: all 0.2s ease;
            }
            [data-testid="stButton"] > button[kind="secondary"]:hover {
                background-color: #e9ecef;
                transform: translateY(-1px);
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            
            /* Special styling for category headers */
            button[data-testid="baseButton-secondary"] {
                position: relative;
                width: 100%;
            }
            
            /* Add styling for category buttons */
            div.stButton > button:has(span:first-child:contains("📂")) {
                background-color: #e6f0ff !important;
                color: #0066cc !important;
                border-left: 4px solid #0066cc !important;
                font-weight: 600 !important;
                padding-left: 12px !important;
            }
            
            div.stButton > button:has(span:first-child:contains("📁")) {
                background-color: #edf2f7 !important;
                color: #555 !important;
                border-left: 4px solid #555 !important;
                font-weight: 600 !important;
                padding-left: 12px !important;
            }
            
            /* Special styling for expanded/collapsed buttons */
            button[data-testid="baseButton-secondary"] {
                width: 100%;
            }
            </style>
            """, unsafe_allow_html=True)
            
            # Group questions by categories to make them more organized
            categories = {
                "Patient Info": [
                    "What medications is patient 12345 taking?",
                    "Summarize the patient's medical history",
                    "When was the last time the patient visited the clinic?",
                    "Is the patient allergic to any medications?",
                    "What is the patient's current diagnosis?",
                    "What is the patient's family medical history?",
                    "Has the patient reported any new symptoms?",
                    "Show the patient's vital signs from last visit",
                    "What is the patient's current BMI and weight trend?",
                    "What social determinants of health affect this patient?"
                ],
                "Medical Data": [
                    "What are the recent lab results for the diabetic patient?",
                    "What is the patient's blood pressure trend?",
                    "Show the patient's HbA1c levels over the last year",
                    "What were the findings from the latest chest X-ray?",
                    "Are there any abnormal values in the CBC results?",
                    "Show the patient's lipid profile over time",
                    "What is the patient's kidney function status?",
                    "Show the trend of inflammatory markers",
                    "What imaging studies have been performed in the last year?",
                    "Compare current lab values with results from 6 months ago",
                    "Show the most recent ECG interpretation"
                ],
                "Treatment & Medications": [
                    "Has the patient been compliant with their medication regimen?",
                    "What is the current dosage for metformin?",
                    "When was the last medication adjustment made?",
                    "List all prescription changes in the last 6 months",
                    "What are the possible side effects of the current medication?",
                    "Are there any contraindications for the current medication?",
                    "What alternative medications could be considered?",
                    "What is the treatment protocol for this condition?",
                    "Has the patient reported any adverse drug reactions?",
                    "What is the recommended titration schedule?",
                    "Are there any non-pharmacological treatments to consider?"
                ],
                "Clinical Questions": [
                    "Are there any drug interactions to be concerned about?",
                    "What are the recommended follow-up tests?",
                    "Should we consider changing the treatment plan?",
                    "Are there any clinical trials suitable for this patient?",
                    "What lifestyle modifications would benefit this patient?",
                    "What are the latest guidelines for managing this condition?",
                    "What is the differential diagnosis for these symptoms?",
                    "What are the risk factors for disease progression?",
                    "What comorbidities should we be monitoring?",
                    "What is the prognosis for this condition?",
                    "What warning signs should the patient watch for?",
                    "How does this condition affect other health parameters?"
                ],
                "Care Management": [
                    "What specialists has the patient seen recently?",
                    "Summarize the care plan for managing diabetes",
                    "What preventive screenings are due?",
                    "Has the patient completed all recommended vaccinations?",
                    "What are the patient's health goals?",
                    "What referrals need to be made?",
                    "What is the patient's care coordination status?",
                    "When should the patient be scheduled for follow-up?",
                    "What educational materials should be provided?",
                    "What support services might benefit this patient?",
                    "Has the patient been screened for depression?",
                    "What telehealth options are appropriate for this patient?",
                    "What is the patient's medication adherence plan?"
                ]
            }
            
            # Add a hint about collapsible categories
            st.markdown("""
            <div style="background-color: #f0f7ff; border-left: 4px solid #0066cc; padding: 8px 12px; margin: 10px 0; border-radius: 0 4px 4px 0;">
                <p style="margin: 0; font-size: 0.9em; color: #333;">
                    💡 <strong>Tip:</strong> Click on any category header to expand or collapse that section.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Initialize session state for category collapse states if not present
            if "category_states" not in st.session_state:
                st.session_state.category_states = {}
                # Initialize with first category expanded, rest collapsed by default
                for i, category in enumerate(categories.keys()):
                    # Set first category as expanded, others as collapsed
                    st.session_state.category_states[category] = (i > 0)  # True means collapsed
            
            # Add a clear hint about collapsible categories with an animation to draw attention
            st.markdown("""
            <style>
            @keyframes pulse {
                0% { box-shadow: 0 0 0 0 rgba(0, 102, 204, 0.4); }
                70% { box-shadow: 0 0 0 6px rgba(0, 102, 204, 0); }
                100% { box-shadow: 0 0 0 0 rgba(0, 102, 204, 0); }
            }
            .tip-box {
                background-color: #f0f7ff; 
                border-left: 4px solid #0066cc; 
                padding: 10px 15px; 
                margin: 10px 0 15px; 
                border-radius: 0 4px 4px 0;
                animation: pulse 2s infinite;
                display: flex;
                align-items: center;
            }
            .tip-icon {
                font-size: 1.5em;
                margin-right: 10px;
                color: #0066cc;
            }
            </style>
            <div class="tip-box">
                <div class="tip-icon">💡</div>
                <div>
                    <p style="margin: 0; font-size: 0.9em; color: #333;">
                        <strong>Navigation Tip:</strong> Click on any folder icon (📁/📂) to expand or collapse that category of questions.
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Add a container with a light background to group the controls
            with st.container():
                st.markdown("""
                <style>
                .control-container {
                    background-color: #f9f9f9; 
                    border: 1px solid #e6e6e6;
                    border-radius: 8px; 
                    padding: 10px 15px; 
                    margin-bottom: 15px;
                }
                .control-heading {
                    font-size: 0.85em;
                    color: #666;
                    margin-bottom: 8px;
                    font-weight: 500;
                }
                </style>
                <div class="control-container">
                    <div class="control-heading">CATEGORY CONTROLS</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Add controls to expand/collapse all categories
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("📂 Show All Questions", key="expand_all", help="Show questions in all categories", use_container_width=True):
                        # Set all categories to expanded
                        for category in categories.keys():
                            st.session_state.category_states[category] = False
                        st.rerun()
                with col2:
                    if st.button("📁 Hide All Questions", key="collapse_all", help="Hide questions to save space", use_container_width=True):
                        # Set all categories to collapsed
                        for category in categories.keys():
                            st.session_state.category_states[category] = True
                        st.rerun()
                
            # Display questions by category with collapsible sections
            for category, questions in categories.items():
                # Check if this category is collapsed in session state
                is_collapsed = st.session_state.category_states.get(category, False)
                collapsed_class = "collapsed" if is_collapsed else ""
                
                # Create divider above each category except the first one
                if list(categories.keys()).index(category) > 0:
                    st.markdown("<hr style='margin: 10px 0 5px 0; border: 0; border-top: 1px solid #eaeaea;'>", unsafe_allow_html=True)
                
                # Create the toggle button for each category with better styling and icons
                # Add question count to each category
                question_count = len(questions)
                
                # Set icon based on category
                category_icon = ""
                if category == "Patient Info":
                    category_icon = "👤"
                elif category == "Medical Data":
                    category_icon = "📊"
                elif category == "Treatment & Medications":
                    category_icon = "💊"
                elif category == "Clinical Questions":
                    category_icon = "🏥"
                elif category == "Care Management":
                    category_icon = "📝"
                
                # Create toggle text with folder icon, category icon, category name, and count
                toggle_text = f"{'📁' if is_collapsed else '📂'} {category_icon} {category} ({question_count})"
                    
                if st.button(
                    toggle_text, 
                    key=f"toggle_{category.replace(' ', '_')}",
                    type="secondary",
                    use_container_width=True
                ):
                    # Toggle the collapsed state for this category
                    st.session_state.category_states[category] = not is_collapsed
                    st.rerun()
                
                # Only show the questions if the category is not collapsed
                
                if not is_collapsed:
                
                    # Create a container for the questions with indentation and visual grouping
                    # Define category-specific border color
                    border_color = "#e6e6e6"  # Default
                    if category == "Patient Info":
                        border_color = "#4285f4"  # Blue
                    elif category == "Medical Data":
                        border_color = "#0f9d58"  # Green
                    elif category == "Treatment & Medications":
                        border_color = "#db4437"  # Red
                    elif category == "Clinical Questions":
                        border_color = "#f4b400"  # Yellow
                    elif category == "Care Management":
                        border_color = "#9c27b0"  # Purple
                        
                    with st.container():
                        st.markdown(f"""
                        <div style="margin-left: 10px; border-left: 2px solid {border_color}; padding-left: 15px; margin-bottom: 10px;">
                        """, unsafe_allow_html=True)
                        
                        # Display all questions in this category
                        for i, q in enumerate(questions):
                            if st.button(q, key=f"question_{category}_{i}"):
                                # Add user message to chat history
                                st.session_state.messages.append({"role": "user", "content": q})
                                
                                # Display the user message
                                with st.chat_message("user"):
                                    st.markdown(q)
                                
                                # Generate assistant response
                                with st.chat_message("assistant"):
                                    with st.spinner("Processing question..."):
                                        try:
                                            # Using a synchronous client instead of async
                                            response = httpx.post(
                                                f"{API_URL}/answer",
                                                json={"question": q},
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
                                                    for j, source in enumerate(data["sources"]):
                                                        with st.expander(f"Source {j+1}"):
                                                            st.write(source["text"])
                                                            if "metadata" in source:
                                                                st.caption(f"Source: {source['metadata'].get('source', 'Unknown')}")
                                            else:
                                                st.error(f"Error: {response.text}")
                                                st.session_state.messages.append({"role": "assistant", "content": f"I'm sorry, an error occurred: {response.text}"})
                                        except Exception as e:
                                            st.error(f"Error: {str(e)}")
                                            st.session_state.messages.append({"role": "assistant", "content": f"I'm sorry, an error occurred: {str(e)}"})
                                
                                # Force a rerun to update the UI after processing
                                st.rerun()
                        
                        st.markdown("</div>", unsafe_allow_html=True)

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

# Footer
st.markdown("---")
st.markdown("PatientCare Assistant | Powered by LangChain and OpenAI")


if __name__ == "__main__":
    # This will only be used when running the script directly
    # When imported as a module, Streamlit handles execution
    pass
