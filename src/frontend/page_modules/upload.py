"""
Upload/Analysis page for PatientCare Assistant.
"""

import os
import time
import io
import zipfile
from pathlib import Path
from datetime import datetime

import streamlit as st
import pandas as pd
import httpx

from core.config import API_URL
from services.api_service import api_request
from styles.styles import UPLOAD_STYLES_CSS
from utils.helpers import (
    get_file_icon,
    format_file_size,
    get_directory_size,
    format_time_ago,
    get_data_directories
)


def render_upload():
    """Render the patient data upload page."""
    st.header("Patient Data Upload")
    st.markdown("""
    Upload patient documents to add them to the system for analysis and retrieval.
    """)
    
    # Enhanced document upload interface
    upload_col1, upload_col2 = st.columns([3, 2])
    
    with upload_col1:
        _render_upload_instructions()
        _render_supported_formats()
        _render_file_uploader()
    
    with upload_col2:
        _render_sample_data_section()
    
    # Add existing documents section
    _render_existing_documents()


def _render_upload_instructions():
    """Render upload instructions."""
    st.markdown("""
    <div style="border-left: 4px solid #4CAF50; padding-left: 10px; margin-bottom: 20px;">
        <p>Upload patient documents to make them searchable in the system. Documents will be processed through 
        the following pipeline:</p>
        <ol style="margin-left: 20px; margin-top: 10px;">
            <li><strong>Document parsing</strong>: Extract text from various file formats</li>
            <li><strong>Text chunking</strong>: Break content into manageable segments</li>
            <li><strong>Embedding generation</strong>: Create vector representations</li>
            <li><strong>Vector indexing</strong>: Add to searchable database</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)


def _render_file_uploader():
    """Render the file uploader component."""
    uploaded_files = st.file_uploader(
        "Drag and drop files here", 
        type=["pdf", "docx", "txt", "md"], 
        accept_multiple_files=True,
        help="Upload patient documents to make them searchable"
    )
        
    if uploaded_files:
        st.success(f"{len(uploaded_files)} file(s) uploaded successfully")
        
        # Show file list with improved styling
        st.markdown("<strong>Uploaded files:</strong>", unsafe_allow_html=True)
        for file in uploaded_files:
            icon = get_file_icon(file.name)
            st.markdown(f"{icon} {file.name}", unsafe_allow_html=True)
        
        process_col1, process_col2 = st.columns([1, 2])
        with process_col1:
            process_button = st.button("📥 Process Documents", use_container_width=True)
            
        if process_button:
            _process_uploaded_files(uploaded_files)


def _process_uploaded_files(uploaded_files):
    """Process the uploaded files through the API."""
    with st.spinner("Processing documents... This may take a minute."):
        # Initialize progress elements with better styling
        progress_col = st.container()
        with progress_col:
            progress_bar = st.progress(0)
            progress_text = st.empty()
            status_container = st.container()
        
        try:
            # Upload files to API
            progress_text.text("📤 Uploading files to server...")
            uploaded_filenames = []
            upload_status = []
            
            for i, file in enumerate(uploaded_files):
                # Create a temporary status for this file
                with status_container:
                    st.caption(f"⏳ Uploading {file.name}...")
                
                # Upload each file to the API
                with httpx.Client() as client:
                    files = {"file": (file.name, file.getvalue(), file.type)}
                    response = client.post(
                        f"{API_URL}/documents/upload",
                        files=files
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        uploaded_filenames.append(data["filename"])
                        upload_status.append(f"✅ {file.name}")
                    else:
                        upload_status.append(f"❌ {file.name}: {response.text}")
                
                # Update progress
                progress_bar.progress((i + 1) / len(uploaded_files) * 0.4)  # First 40%
            
            # Show upload summary
            with status_container:
                for status in upload_status:
                    st.caption(status)
            
            # Process all documents
            if uploaded_filenames:
                _process_documents_pipeline(progress_bar, progress_text, status_container, uploaded_filenames)
            else:
                progress_bar.progress(1.0)
                progress_text.text("⚠️ No files uploaded!")
                with status_container:
                    st.warning("No files were uploaded successfully.")
            
            # Refresh document list
            st.info("You can now ask questions about these documents in the Q&A section")
            time.sleep(2)
            st.rerun()
        except Exception as e:
            st.error(f"Error: {str(e)}")
            progress_bar.progress(1.0)
            progress_text.text("Error occurred during processing")


def _process_documents_pipeline(progress_bar, progress_text, status_container, uploaded_filenames):
    """Process documents through the processing pipeline."""
    # Update progress stages
    progress_text.text("📄 Parsing documents...")
    progress_bar.progress(0.5)  # 50%
    time.sleep(0.5)  # Small delay for UX
    
    progress_text.text("✂️ Chunking text...")
    progress_bar.progress(0.6)  # 60%
    time.sleep(0.5)  # Small delay for UX
    
    progress_text.text("🧠 Generating embeddings...")
    progress_bar.progress(0.7)  # 70%
    
    # Call the actual processing endpoint
    with httpx.Client() as client:
        response = client.post(
            f"{API_URL}/documents/process",
            timeout=180.0  # Longer timeout for processing
        )
        
        if response.status_code == 200:
            data = response.json()
            
            progress_text.text("🗄️ Indexing vector database...")
            progress_bar.progress(0.9)  # 90%
            time.sleep(0.5)  # Small delay for UX
            
            progress_bar.progress(1.0)
            progress_text.text("✅ Processing complete!")
            
            with status_container:
                st.success(f"Successfully processed {len(uploaded_filenames)} document(s)")
                # Show processed files
                if "processed_files" in data:
                    for file in data["processed_files"]:
                        st.caption(f"✅ Processed: {os.path.basename(file)}")
        else:
            progress_bar.progress(1.0)
            progress_text.text("❌ Processing error!")
            with status_container:
                st.error(f"Error processing documents: {response.text}")


def _render_supported_formats():
    """Render supported file formats section."""
    st.markdown(UPLOAD_STYLES_CSS, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="format-box">
            <div class="format-header">SUPPORTED FORMATS</div>
            <div class="format-item"><span class="format-icon">📕</span> PDF (.pdf)</div>
            <div class="format-item"><span class="format-icon">📘</span> Word (.docx, .doc)</div>
            <div class="format-item"><span class="format-icon">📄</span> Text (.txt)</div>
            <div class="format-item"><span class="format-icon">📝</span> Markdown (.md)</div>
        </div>
        """, unsafe_allow_html=True)


def _render_sample_data_section():
    """Render sample data download section."""
    st.markdown("---")
    st.subheader("Sample Data")
    st.markdown("Download these sample medical records to test the system's capabilities.")
    
    # Get sample data files from API
    success, response_data, error_message = api_request("documents/sample-data", method="get")
    
    if success and response_data:
        sample_files = response_data.get("files", [])
        
        if sample_files:
            _render_sample_files_list(sample_files)
        else:
            st.info("No sample data files available.")
    else:
        if error_message:
            st.warning(f"Error retrieving sample data: {error_message}")
        else:
            st.warning("No sample data available.")


def _render_sample_files_list(sample_files):
    """Render the list of sample files with download buttons."""
    # Create styling for sample files
    st.markdown("""
    <style>
    .file-item {
        padding: 8px 10px;
        margin: 4px 0;
        border-radius: 4px;
        border: 1px solid #eee;
        background-color: #f9f9f9;
    }
    .file-type {
        display: inline-block;
        padding: 2px 6px;
        border-radius: 3px;
        font-size: 0.8em;
        font-weight: bold;
        margin-left: 8px;
    }
    .pdf-type {
        background-color: #ffecec;
        color: #e53935;
    }
    .md-type {
        background-color: #e3f2fd;
        color: #1976d2;
    }
    .doc-type {
        background-color: #e8f5e9;
        color: #388e3c;
    }
    .txt-type {
        background-color: #f5f5f5;
        color: #616161;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Display sample files in a nice grid
    for file_info in sorted(sample_files, key=lambda x: x["filename"]):
        # Get file information
        file = file_info["filename"]
        file_type = file_info["type"]
        file_size = file_info["size"]
        
        # Determine CSS class based on file type
        type_class_map = {
            "PDF": "pdf-type",
            "DOC": "doc-type", 
            "MD": "md-type"
        }
        type_class = type_class_map.get(file_type, "txt-type")
        
        # Create columns for file display and download button
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Display file name with styled type badge and size
            st.markdown(f"""
            <div class="file-item">
                {file} <span class="file-type {type_class}">{file_type}</span>
                <span style="color:#666; font-size:0.8em; margin-left:8px;">({file_size})</span>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Create download button that links to the API endpoint
            download_url = f"{API_URL}/documents/sample-data/{file}"
            st.markdown(f'''
                <a href="{download_url}" download="{file}" target="_blank">
                    <button style="background-color:#4CAF50; color:white; border:none; 
                    padding:8px 16px; text-align:center; text-decoration:none; 
                    display:inline-block; font-size:14px; border-radius:4px; 
                    cursor:pointer;">Download</button>
                </a>
            ''', unsafe_allow_html=True)
    
    # Add a hint about the sample files
    st.info("👆 Download these files and then upload them in the file uploader above to test the system.")


def _render_existing_documents():
    """Render existing documents section with management options."""
    st.markdown("---")
    st.subheader("Existing Documents")
    
    # Get document data from API
    documents = _fetch_existing_documents()
    
    # Convert to dataframe for display
    docs_df = pd.DataFrame(documents)
    
    # Display documents table with selection
    edited_df = _render_documents_table(docs_df)
    
    # Add document management buttons
    _render_document_management(edited_df)
    
    # Usage statistics
    _render_usage_statistics()


def _fetch_existing_documents():
    """Fetch existing documents from API."""
    try:
        with st.spinner("Loading documents..."):
            with httpx.Client() as client:
                response = client.get(
                    f"{API_URL}/documents",
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    documents = data["documents"]
                    
                    # Format dates more nicely
                    for doc in documents:
                        if "added" in doc:
                            try:
                                # Parse API date format and convert to friendly format
                                date_obj = datetime.strptime(doc["added"], "%Y-%m-%d %H:%M:%S")
                                doc["added"] = date_obj.strftime("%B %d, %Y")
                            except:
                                # Keep original if parsing fails
                                pass
                    return documents
                else:
                    st.error(f"Error loading documents: {response.text}")
                    return []
    except Exception as e:
        st.error(f"Error connecting to API: {str(e)}")
        return []


def _render_documents_table(docs_df):
    """Render the documents table with selection checkboxes."""
    if len(docs_df) > 0:
        # Add a selection column
        docs_df.insert(0, 'select', False)
        
        # Create an editable dataframe with checkboxes and improved display
        edited_df = st.data_editor(
            docs_df,
            column_config={
                "select": st.column_config.CheckboxColumn(
                    "Select",
                    help="Select document",
                    default=False,
                    width="small"
                ),
                "filename": st.column_config.TextColumn(
                    "Document Name",
                    help="The name of the document",
                ),
                "added": st.column_config.TextColumn(
                    "Added",
                    help="Date when the document was added",
                    width="small"
                ),
                "size": st.column_config.TextColumn(
                    "Size",
                    help="Size of the document",
                    width="small"
                ),
                "type": st.column_config.TextColumn(
                    "Type",
                    help="Type of document",
                    width="small"
                ),
                "status": st.column_config.TextColumn(
                    "Status",
                    help="Processing status",
                    width="small"
                )
            },
            use_container_width=True,
            hide_index=True,
            num_rows="fixed"
        )
    else:
        st.info("No documents found. Upload documents to see them here.")
        edited_df = docs_df
    
    return edited_df


def _render_document_management(edited_df):
    """Render document management buttons."""
    manage_col1, manage_col2, manage_col3, manage_col4 = st.columns(4)
    
    with manage_col1:
        search_button = st.button("💬 Medical Q&A", use_container_width=True)
        if search_button:
            st.session_state.page = "Q&A"
            st.rerun()
    
    with manage_col2:
        remove_button = st.button("🗑️ Remove Selected", use_container_width=True)
        if remove_button:
            _handle_document_removal(edited_df)
    
    with manage_col3:
        download_button = st.button("📥 Download Selected", use_container_width=True)
        if download_button:
            _handle_document_download(edited_df)
    
    with manage_col4:
        reset_button = st.button("🔄 Reset Document Database", use_container_width=True)
        if reset_button:
            _handle_database_reset()


def _handle_document_removal(edited_df):
    """Handle removal of selected documents."""
    if len(edited_df) > 0:
        selected = edited_df[edited_df['select'] == True]
        if len(selected) > 0:
            with st.spinner(f"Removing {len(selected)} document(s)..."):
                try:
                    success_count = 0
                    
                    # Delete each selected file via API
                    with httpx.Client() as client:
                        for _, row in selected.iterrows():
                            filename = row['filename']
                            
                            response = client.delete(
                                f"{API_URL}/documents/{filename}",
                                timeout=10.0
                            )
                            
                            if response.status_code == 200:
                                success_count += 1
                            else:
                                st.error(f"Error removing {filename}: {response.text}")
                    
                    if success_count > 0:
                        st.success(f"Removed {success_count} document(s)")
                        time.sleep(1)
                        st.rerun()
                except Exception as e:
                    st.error(f"Error removing documents: {str(e)}")
        else:
            st.info("No documents selected")


def _handle_document_download(edited_df):
    """Handle download of selected documents."""
    if len(edited_df) > 0:
        selected = edited_df[edited_df['select'] == True]
        if len(selected) > 0:
            # Create a zip file in memory
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                data_dirs = get_data_directories()
                raw_dir = data_dirs['raw']
                
                # Add selected documents to the zip file
                files_added = 0
                for _, row in selected.iterrows():
                    # Find the actual filename in the raw directory
                    filename = row['filename']
                    for file_path in raw_dir.glob("*"):
                        if filename in file_path.name:
                            zip_file.write(file_path, arcname=filename)
                            files_added += 1
                            
            if files_added > 0:
                # Offer the zip file for download
                zip_buffer.seek(0)
                st.download_button(
                    label="Download ZIP",
                    data=zip_buffer,
                    file_name="patient_documents.zip",
                    mime="application/zip",
                    key="download_zip"
                )
            else:
                st.warning("No files found for download")
        else:
            st.info("No documents selected")


def _handle_database_reset():
    """Handle database reset operation."""
    with st.spinner("Resetting database..."):
        try:
            time.sleep(1)
            # Use API endpoint to reset database
            with httpx.Client() as client:
                response = client.post(
                    f"{API_URL}/documents/reset",
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    st.success("Database reset successfully!")
                    st.rerun()
                else:
                    st.error(f"Error resetting database: {response.text}")
        except Exception as e:
            st.error(f"Error resetting database: {str(e)}")


def _render_usage_statistics():
    """Render document storage statistics."""
    st.markdown("---")
    st.subheader("Document Storage Statistics")
    
    # Create two columns for stats
    stats_col1, stats_col2 = st.columns(2)
    
    # Get data directories
    data_dirs = get_data_directories()
    raw_dir = data_dirs['raw']
    processed_dir = data_dirs['processed']
    vector_db_dir = data_dirs['vector_db']
    
    # Count documents
    raw_count = len([f for f in raw_dir.glob("*") if f.is_file() and not f.name.startswith('.')])
    processed_count = len([f for f in processed_dir.glob("*_chunks.json")])
    
    # Calculate storage size
    raw_size = get_directory_size(raw_dir)
    db_size = get_directory_size(vector_db_dir)
    total_size = raw_size + get_directory_size(processed_dir)
    
    # Get most recent file date
    most_recent = "No uploads"
    if raw_count > 0:
        all_files = list(raw_dir.glob("*"))
        if all_files:
            most_recent_file = max(all_files, key=lambda p: p.stat().st_mtime)
            most_recent_time = most_recent_file.stat().st_mtime
            most_recent = format_time_ago(most_recent_time)
    
    with stats_col1:
        # Display metrics
        st.metric(label="Total Documents", value=str(raw_count))
        st.metric(label="Storage Used", value=format_file_size(total_size))
    
    with stats_col2:
        # Display more metrics
        pending_count = raw_count - processed_count
        pending_delta = f"{pending_count} pending" if pending_count > 0 else None
        
        st.metric(label="Documents Processed", value=str(processed_count), delta=pending_delta)
        st.metric(label="Last Upload", value=most_recent)
