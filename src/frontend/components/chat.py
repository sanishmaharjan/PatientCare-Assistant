"""
Chat component for PatientCare Assistant Q&A interface.
"""

import httpx
import streamlit as st
from core.config import API_URL


def render_chat_interface():
    """Render the main chat interface for Q&A."""
    # Initialize chat messages if not present
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
            _process_chat_response(prompt)

        st.rerun()

def _process_chat_response(prompt):
    """Process chat response from API."""
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


def handle_suggested_question(question):
    """Handle when a suggested question is clicked."""
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": question})
    
    # Display the user message
    with st.chat_message("user"):
        st.markdown(question)
    
    # Generate assistant response
    with st.chat_message("assistant"):
        with st.spinner("Processing question..."):
            try:
                # Using a synchronous client instead of async
                response = httpx.post(
                    f"{API_URL}/answer",
                    json={"question": question},
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
