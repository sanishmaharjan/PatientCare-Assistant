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
API_URL = f"http://{API_HOST}:{API_PORT}"

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
        .login-form { max-width: 400px; margin: 100px auto; padding: 20px; border: 1px solid #ccc; }
        .card { border: 1px solid #ddd; padding: 20px; margin-bottom: 20px; border-radius: 5px; }
        .button { background-color: #4CAF50; color: white; padding: 10px 20px; border: none; cursor: pointer; }
        .error { color: red; }
        .success { color: green; }
        table { border-collapse: collapse; width: 100%; }
        th, td { padding: 8px; text-align: left; border-bottom: 1px solid #ddd; }
    </style>
</head>
<body>
    {% if session.logged_in %}
        <div class="header">
            <h1>PatientCare Assistant</h1>
            <p>Logged in as: {{ session.username }} | <a href="/logout" style="color: white;">Logout</a></p>
        </div>
        <div class="sidebar">
            <h3>Navigation</h3>
            <ul>
                <li><a href="/">Dashboard</a></li>
                <li><a href="/patient">Patient Search</a></li>
                <li><a href="/qa">Medical Q&A</a></li>
                <li><a href="/settings">Settings</a></li>
            </ul>
        </div>
        <div class="content">
            {% block content %}{% endblock %}
        </div>
    {% else %}
        {% block login %}{% endblock %}
    {% endif %}
</body>
</html>
"""

LOGIN_TEMPLATE = """
{% extends "base_template" %}
{% block login %}
<div class="login-form">
    <h2>PatientCare Assistant Login</h2>
    {% if error %}
        <p class="error">{{ error }}</p>
    {% endif %}
    <form method="post" action="/login">
        <div>
            <label>Username:</label><br>
            <input type="text" name="username" required>
        </div>
        <div style="margin-top: 15px;">
            <label>Password:</label><br>
            <input type="password" name="password" required>
        </div>
        <div style="margin-top: 20px;">
            <button type="submit" class="button">Login</button>
        </div>
    </form>
    <p><i>Use any username and password for demo purposes</i></p>
</div>
{% endblock %}
"""

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
    <a href="/patient" class="button">Search Patient</a>
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

SETTINGS_TEMPLATE = """
{% extends "base_template" %}
{% block content %}
<h2>Settings</h2>
<div class="card">
    <h3>User Profile</h3>
    <p><strong>Username:</strong> {{ session.username }}</p>
    <p><strong>Email:</strong> {{ session.username.lower() }}@hospital.org</p>
</div>

<div class="card">
    <h3>API Configuration</h3>
    <p><strong>API URL:</strong> {{ api_url }}</p>
</div>
{% endblock %}
"""

# Routes
@app.route('/')
def index():
    if not session.get('logged_in'):
        return render_template_string(LOGIN_TEMPLATE, base_template=BASE_TEMPLATE, error=None)
    
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

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] and request.form['password']:
            session['logged_in'] = True
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        else:
            error = 'Invalid credentials'
    
    return render_template_string(LOGIN_TEMPLATE, base_template=BASE_TEMPLATE, error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/patient', methods=['GET', 'POST'])
def patient():
    if not session.get('logged_in'):
        return redirect(url_for('index'))
    
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
    if not session.get('logged_in'):
        return redirect(url_for('index'))
    
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

@app.route('/settings')
def settings():
    if not session.get('logged_in'):
        return redirect(url_for('index'))
    
    return render_template_string(
        SETTINGS_TEMPLATE,
        base_template=BASE_TEMPLATE,
        api_url=API_URL
    )

def start_frontend():
    """Start the frontend server."""
    app.run(host='localhost', port=FRONTEND_PORT, debug=True)

if __name__ == "__main__":
    start_frontend()
