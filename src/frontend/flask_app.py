"""
Flask-based frontend for PatientCare Assistant (Python 3 compatible)

This is a legacy frontend implementation kept for backward compatibility.
The main frontend is now implemented with Streamlit.
"""
import os
import sys
import json
import requests
from datetime import datetime
from flask import Flask, render_template_string, request, redirect, url_for, session

# Local imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import API_HOST, API_PORT, FRONTEND_PORT

# API endpoint
API_URL = "http://{}:{}".format(API_HOST, API_PORT)

# Create Flask app
app = Flask(__name__)
app.secret_key = "patientcare_assistant_key"  # For session management

# HTML Templates
BASE_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>PatientCare Assistant</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .header { background-color: #4CAF50; color: white; padding: 20px; }
        .sidebar { float: left; width: 200px; padding: 20px; background-color: #f1f1f1; min-height: 500px; }
        .content { margin-left: 240px; padding: 20px; }
        .card { border: 1px solid #ddd; padding: 20px; margin-bottom: 20px; border-radius: 5px; }
        .button { background-color: #4CAF50; color: white; padding: 10px 20px; border: none; cursor: pointer; }
        .error { color: red; }
        .success { color: green; }
        table { border-collapse: collapse; width: 100%; }
        th, td { padding: 8px; text-align: left; border-bottom: 1px solid #ddd; }
    </style>
</head>
<body>
    <div class="header">
        <h1>PatientCare Assistant</h1>
        <p>Healthcare Provider: {{ session.username }}</p>
    </div>
    <div class="sidebar">
        <h3>Navigation</h3>
        <ul>
            <li><a href="/">Dashboard</a></li>
            <li><a href="/qa">Medical Q&A</a></li>
        </ul>
    </div>
    <div class="content">
        {% block content %}{% endblock %}
    </div>
</body>
</html>
"""

# Login template removed - no longer needed

DASHBOARD_TEMPLATE = """
{% extends "base_template" %}
{% block content %}
<h2>Healthcare Provider Dashboard</h2>
<div>
    <h3>Welcome, Dr. {{ session.username }}</h3>
    <p>Current Date: {{ current_date }}</p>
</div>

<div class="card">
    <h3>Recent Patients</h3>
    <table>
        <tr>
            <th>Patient ID</th>
            <th>Name</th>
            <th>Last Visit</th>
            <th>Status</th>
        </tr>
        {% for patient in patients %}
        <tr>
            <td>{{ patient.id }}</td>
            <td>{{ patient.name }}</td>
            <td>{{ patient.last_visit }}</td>
            <td>{{ patient.status }}</td>
        </tr>
        {% endfor %}
    </table>
</div>

<div class="card">
    <h3>Quick Actions</h3>
    <a href="/qa" class="button">Medical Q&A</a>
</div>
{% endblock %}
"""

PATIENT_TEMPLATE = """
{% extends "base_template" %}
{% block content %}
<h2>Patient Search</h2>
<div class="card">
    <form method="post" action="/patient">
        <div>
            <label>Patient ID:</label><br>
            <input type="text" name="patient_id" required {% if patient_id %}value="{{ patient_id }}"{% endif %}>
        </div>
        <div style="margin-top: 15px;">
            <button type="submit" name="action" value="summary" class="button">Generate Summary</button>
            <button type="submit" name="action" value="issues" class="button">Identify Health Issues</button>
        </div>
    </form>
</div>

{% if summary %}
<div class="card">
    <h3>Patient Summary</h3>
    <p>{{ summary }}</p>
    {% if sources %}
    <details>
        <summary>View Source Documents</summary>
        <div>
            {% for source in sources %}
            <details>
                <summary>Source {{ loop.index }}</summary>
                <p>{{ source.text }}</p>
                <p><small>Source: {{ source.metadata.source }}</small></p>
            </details>
            {% endfor %}
        </div>
    </details>
    {% endif %}
</div>
{% endif %}

{% if issues %}
<div class="card">
    <h3>Health Issues</h3>
    <p>{{ issues }}</p>
    {% if sources %}
    <details>
        <summary>View Source Documents</summary>
        <div>
            {% for source in sources %}
            <details>
                <summary>Source {{ loop.index }}</summary>
                <p>{{ source.text }}</p>
                <p><small>Source: {{ source.metadata.source }}</small></p>
            </details>
            {% endfor %}
        </div>
    </details>
    {% endif %}
</div>
{% endif %}
{% endblock %}
"""

QA_TEMPLATE = """
{% extends "base_template" %}
{% block content %}
<h2>Medical Q&A</h2>
<div class="card">
    <form method="post" action="/qa">
        <div>
            <label>Question:</label><br>
            <textarea name="question" rows="3" style="width: 100%;" required></textarea>
        </div>
        <div style="margin-top: 15px;">
            <button type="submit" class="button">Ask Question</button>
        </div>
    </form>
</div>

{% if answer %}
<div class="card">
    <h3>Answer</h3>
    <p><strong>Question:</strong> {{ question }}</p>
    <p>{{ answer }}</p>
    {% if sources %}
    <details>
        <summary>View Source Documents</summary>
        <div>
            {% for source in sources %}
            <details>
                <summary>Source {{ loop.index }}</summary>
                <p>{{ source.text }}</p>
                <p><small>Source: {{ source.metadata.source }}</small></p>
            </details>
            {% endfor %}
        </div>
    </details>
    {% endif %}
</div>
{% endif %}
{% endblock %}
"""

# Routes
@app.route('/')
def index():
    # Set default session data
    session['logged_in'] = True
    if 'username' not in session:
        session['username'] = 'Provider'
    
    # Sample patient data
    patients = [
        {'id': 'PATIENT-12345', 'name': 'Jane Doe', 'last_visit': 'October 2, 2025', 'status': 'Follow-up'},
        {'id': 'PATIENT-12346', 'name': 'John Smith', 'last_visit': 'October 3, 2025', 'status': 'Stable'},
        {'id': 'PATIENT-12347', 'name': 'Maria Garcia', 'last_visit': 'October 4, 2025', 'status': 'New'}
    ]
    
    return render_template_string(
        DASHBOARD_TEMPLATE,
        base_template=BASE_TEMPLATE,
        patients=patients,
        current_date=datetime.now().strftime('%B %d, %Y')
    )

# Authentication routes removed - auto-login implemented in index route)

@app.route('/patient', methods=['GET', 'POST'])
def patient():
    # Ensure user is always considered logged in
    session['logged_in'] = True
    if 'username' not in session:
        session['username'] = 'Provider'
    
    patient_id = None
    summary = None
    issues = None
    sources = None
    
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        action = request.form['action']
        
        if action == 'summary':
            try:
                response = requests.post(
                    "{}/summary".format(API_URL),
                    json={"patient_id": patient_id}
                )
                if response.status_code == 200:
                    data = response.json()
                    summary = data["summary"]
                    sources = data.get("sources", [])
            except Exception as e:
                summary = "Error generating summary: {}".format(str(e))
        
        elif action == 'issues':
            try:
                response = requests.post(
                    "{}/health-issues".format(API_URL),
                    json={"patient_id": patient_id}
                )
                if response.status_code == 200:
                    data = response.json()
                    issues = data["issues"]
                    sources = data.get("sources", [])
            except Exception as e:
                issues = "Error identifying health issues: {}".format(str(e))
    
    return render_template_string(
        PATIENT_TEMPLATE,
        base_template=BASE_TEMPLATE,
        patient_id=patient_id,
        summary=summary,
        issues=issues,
        sources=sources
    )

@app.route('/qa', methods=['GET', 'POST'])
def qa():
    # Ensure user is always considered logged in
    session['logged_in'] = True
    if 'username' not in session:
        session['username'] = 'Provider'
    
    question = None
    answer = None
    sources = None
    
    if request.method == 'POST':
        question = request.form['question']
        try:
            response = requests.post(
                "{}/answer".format(API_URL),
                json={"question": question}
            )
            if response.status_code == 200:
                data = response.json()
                answer = data["answer"]
                sources = data.get("sources", [])
        except Exception as e:
            answer = "Error: {}".format(str(e))
    
    return render_template_string(
        QA_TEMPLATE,
        base_template=BASE_TEMPLATE,
        question=question,
        answer=answer,
        sources=sources
    )

def start_frontend():
    """Start the frontend server."""
    app.run(host='localhost', port=FRONTEND_PORT, debug=True)

if __name__ == "__main__":
    start_frontend()
