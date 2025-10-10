"""
Data models and sample data for the application
"""
from typing import List, Dict
from datetime import datetime


# Sample patient data
SAMPLE_PATIENTS = [
    {"Patient ID": "PATIENT-12345", "Name": "Jane Doe", "Last Visit": "October 2, 2025", "Status": "Follow-up"},
    {"Patient ID": "PATIENT-12346", "Name": "John Smith", "Last Visit": "October 3, 2025", "Status": "Stable"},
    {"Patient ID": "PATIENT-12347", "Name": "Maria Garcia", "Last Visit": "October 4, 2025", "Status": "New"},
    {"Patient ID": "PATIENT-12348", "Name": "Robert Johnson", "Last Visit": "October 4, 2025", "Status": "Follow-up"},
    {"Patient ID": "PATIENT-12349", "Name": "Susan Williams", "Last Visit": "October 5, 2025", "Status": "New"},
    {"Patient ID": "PATIENT-12350", "Name": "Michael Brown", "Last Visit": "October 5, 2025", "Status": "Stable"}
]


# Q&A question categories
QA_CATEGORIES = {
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


# Category icons
CATEGORY_ICONS = {
    "Patient Info": "👤",
    "Medical Data": "📊",
    "Treatment & Medications": "💊",
    "Clinical Questions": "🏥",
    "Care Management": "📝"
}


# Category border colors
CATEGORY_BORDER_COLORS = {
    "Patient Info": "#4285f4",  # Blue
    "Medical Data": "#0f9d58",  # Green
    "Treatment & Medications": "#db4437",  # Red
    "Clinical Questions": "#f4b400",  # Yellow
    "Care Management": "#9c27b0"  # Purple
}


# Keep the function versions for backward compatibility
def get_sample_patients() -> List[Dict]:
    """Get sample patient data"""
    return SAMPLE_PATIENTS


def get_qa_categories() -> Dict[str, List[str]]:
    """Get Q&A question categories"""
    return QA_CATEGORIES


def get_category_icons() -> Dict[str, str]:
    """Get icons for each category"""
    return CATEGORY_ICONS


def get_category_border_colors() -> Dict[str, str]:
    """Get border colors for each category"""
    return CATEGORY_BORDER_COLORS
