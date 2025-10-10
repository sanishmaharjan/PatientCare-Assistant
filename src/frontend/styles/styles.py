"""
CSS styles and utilities for the Streamlit app

Note: Component-specific styles have been moved to external CSS files:
- Navigation styles: styles/navigation.css
- Questions component: styles/questions.css
These are loaded via the load_css_file() utility function.
"""


def get_navigation_styles() -> str:
    """Get CSS styles for navigation"""
    return """
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
    """


def get_qa_styles() -> str:
    """Get CSS styles for Q&A page"""
    return """
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
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(0, 102, 204, 0.4); }
        70% { box-shadow: 0 0 0 6px rgba(0, 102, 204, 0); }
        100% { box-shadow: 0 0 0 0 rgba(0, 102, 204, 0); }
    }
    .tip-box {
        background-color: #f0f7ff; 
        border-left: 4px solid #0066cc; 
        padding-left: 10px; 
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
    """


def get_upload_styles() -> str:
    """Get CSS styles for upload page"""
    return """
    <style>
    .format-box {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 20px;
    }
    .format-header {
        font-weight: bold;
        color: #4CAF50;
        margin-bottom: 10px;
    }
    .format-item {
        display: flex;
        align-items: center;
        margin-bottom: 8px;
    }
    .format-icon {
        margin-right: 10px;
        font-size: 1.2em;
    }
    .upload-card {
        background-color: #ffffff;
        border: 1px solid #e1e4e8;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .upload-card:hover {
        box-shadow: 0 2px 6px rgba(0,0,0,0.15);
        transform: translateY(-1px);
        transition: all 0.2s ease;
    }
    .status-badge {
        display: inline-block;
        padding: 4px 8px;
        border-radius: 12px;
        font-size: 0.8em;
        font-weight: 500;
        text-transform: uppercase;
    }
    .status-processing {
        background-color: #fff3cd;
        color: #856404;
        border: 1px solid #ffeaa7;
    }
    .status-completed {
        background-color: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }
    .status-error {
        background-color: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }
    .progress-bar {
        width: 100%;
        height: 8px;
        background-color: #e9ecef;
        border-radius: 4px;
        overflow: hidden;
        margin: 8px 0;
    }
    .progress-fill {
        height: 100%;
        background-color: #28a745;
        transition: width 0.3s ease;
    }
    </style>
    """


# Q&A page styles (constant for direct import)
QA_STYLES_CSS = """
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

@keyframes pulse {
    0% { box-shadow: 0 0 0 0 rgba(0, 102, 204, 0.4); }
    70% { box-shadow: 0 0 0 6px rgba(0, 102, 204, 0); }
    100% { box-shadow: 0 0 0 0 rgba(0, 102, 204, 0); }
}
.tip-box {
    background-color: #f0f7ff; 
    border-left: 4px solid #0066cc; 
    padding-left: 10px; 
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
"""


# Upload page styles (constant for direct import)
UPLOAD_STYLES_CSS = """
<style>
.format-box {
    background-color: #f8f9fa;
    border-radius: 8px;
    padding: 15px;
    margin-bottom: 20px;
}
.format-header {
    font-weight: bold;
    color: #4CAF50;
    margin-bottom: 10px;
}
.format-item {
    display: flex;
    align-items: center;
    margin-bottom: 8px;
}
.format-icon {
    margin-right: 10px;
    font-size: 1.2em;
}
.upload-card {
    background-color: #ffffff;
    border: 1px solid #e1e4e8;
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 16px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}
.upload-card:hover {
    box-shadow: 0 2px 6px rgba(0,0,0,0.15);
    transform: translateY(-1px);
    transition: all 0.2s ease;
}
.status-badge {
    display: inline-block;
    padding: 4px 8px;
    border-radius: 12px;
    font-size: 0.8em;
    font-weight: 500;
    text-transform: uppercase;
}
.status-processing {
    background-color: #fff3cd;
    color: #856404;
    border: 1px solid #ffeaa7;
}
.status-completed {
    background-color: #d4edda;
    color: #155724;
    border: 1px solid #c3e6cb;
}
.status-error {
    background-color: #f8d7da;
    color: #721c24;
    border: 1px solid #f5c6cb;
}
.progress-bar {
    width: 100%;
    height: 8px;
    background-color: #e9ecef;
    border-radius: 4px;
    overflow: hidden;
    margin: 8px 0;
}
.progress-fill {
    height: 100%;
    background-color: #28a745;
    transition: width 0.3s ease;
}
</style>
"""


def get_qa_tip_html() -> str:
    """Get HTML for Q&A navigation tip"""
    return """
    <div class="tip-box">
        <div class="tip-icon">💡</div>
        <div>
            <p style="margin: 0; font-size: 0.9em; color: #333;">
                <strong>Navigation Tip:</strong> Click on any folder icon (📁/📂) to expand or collapse that category of questions.
            </p>
        </div>
    </div>
    """


def get_upload_formats_html() -> str:
    """Get HTML for supported upload formats"""
    return """
    <div class="format-box">
        <div class="format-header">SUPPORTED FORMATS</div>
        <div class="format-item"><span class="format-icon">📕</span> PDF (.pdf)</div>
        <div class="format-item"><span class="format-icon">📘</span> Word (.docx, .doc)</div>
        <div class="format-item"><span class="format-icon">📄</span> Text (.txt)</div>
        <div class="format-item"><span class="format-icon">📝</span> Markdown (.md)</div>
    </div>
    """


def get_patient_card_styles() -> str:
    """Get CSS styles for patient cards"""
    return """
    <style>
    .patient-card {
        background-color: #ffffff;
        border: 1px solid #e1e4e8;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        transition: all 0.2s ease;
    }
    .patient-card:hover {
        box-shadow: 0 2px 6px rgba(0,0,0,0.15);
        transform: translateY(-1px);
    }
    .patient-header {
        display: flex;
        align-items: center;
        margin-bottom: 12px;
    }
    .patient-avatar {
        width: 48px;
        height: 48px;
        border-radius: 50%;
        margin-right: 12px;
        background-color: #f0f0f0;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
    }
    .patient-info h3 {
        margin: 0 0 4px 0;
        color: #2c3e50;
        font-size: 1.1em;
    }
    .patient-info p {
        margin: 0;
        color: #7f8c8d;
        font-size: 0.9em;
    }
    .patient-actions {
        display: flex;
        gap: 8px;
        margin-top: 12px;
    }
    </style>
    """