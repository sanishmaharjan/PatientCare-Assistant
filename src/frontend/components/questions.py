"""
Suggested questions component for Q&A interface.
"""

import streamlit as st
from utils.data import QA_CATEGORIES, CATEGORY_ICONS, CATEGORY_BORDER_COLORS
from templates.styles import QA_STYLES_CSS
from components.chat import handle_suggested_question


def render_suggested_questions():
    """Render the suggested questions sidebar."""
    st.subheader("Suggested Questions")
    
    # Add styles for question buttons and category toggle buttons
    st.markdown(QA_STYLES_CSS, unsafe_allow_html=True)
    
    # Initialize session state for category collapse states if not present
    if "category_states" not in st.session_state:
        st.session_state.category_states = {}
        # Initialize with all categories collapsed by default
        for category in QA_CATEGORIES.keys():
            st.session_state.category_states[category] = True  # True means collapsed
    
    # Add navigation tip
    _render_navigation_tip()
    
    # Add expand/collapse controls
    _render_category_controls()
    
    # Display questions by category with collapsible sections
    _render_category_questions()


def _render_navigation_tip():
    """Render the navigation tip box."""
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
    <div class="tip-box">
        <div class="tip-icon">💡</div>
        <div>
            <p style="margin: 0; font-size: 0.9em; color: #333;">
                <strong>Navigation Tip:</strong> Click on any folder icon (📁/📂) to expand or collapse that category of questions.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)


def _render_category_controls():
    """Render expand/collapse all controls."""
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
        """, unsafe_allow_html=True)
        
        # Add controls to expand/collapse all categories
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📂 Show All Questions", key="expand_all", help="Show questions in all categories", use_container_width=True):
                # Set all categories to expanded
                for category in QA_CATEGORIES.keys():
                    st.session_state.category_states[category] = False
                st.rerun()
        with col2:
            if st.button("📁 Hide All Questions", key="collapse_all", help="Hide questions to save space", use_container_width=True):
                # Set all categories to collapsed
                for category in QA_CATEGORIES.keys():
                    st.session_state.category_states[category] = True
                st.rerun()


def _render_category_questions():
    """Render questions organized by categories."""
    for category, questions in QA_CATEGORIES.items():
        # Check if this category is collapsed in session state
        is_collapsed = st.session_state.category_states.get(category, False)
        
        # Create divider above each category except the first one
        if list(QA_CATEGORIES.keys()).index(category) > 0:
            st.markdown("<hr style='margin: 10px 0 5px 0; border: 0; border-top: 1px solid #eaeaea;'>", unsafe_allow_html=True)
        
        # Create the toggle button for each category with better styling and icons
        question_count = len(questions)
        category_icon = CATEGORY_ICONS.get(category, "📁")
        
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
            _render_category_question_list(category, questions)


def _render_category_question_list(category, questions):
    """Render the list of questions for a specific category."""
    # Get category-specific border color
    border_color = CATEGORY_BORDER_COLORS.get(category, "#e6e6e6")
    
    with st.container():
        st.markdown(f"""
        <div style="margin-left: 10px; border-left: 2px solid {border_color}; padding-left: 15px; margin-bottom: 10px;">
        """, unsafe_allow_html=True)
        
        # Display all questions in this category
        for i, q in enumerate(questions):
            if st.button(q, key=f"question_{category}_{i}"):
                handle_suggested_question(q)
        
        st.markdown("</div>", unsafe_allow_html=True)
