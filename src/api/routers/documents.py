"""
Documents router - handles document upload, processing, and management.
"""

import os
import sys
import time
import json
import uuid
import gc
import shutil
import chromadb
from pathlib import Path
from fastapi import APIRouter, HTTPException, File, UploadFile
from fastapi.responses import FileResponse

from ..models import (
    DocumentListResponse,
    ProcessingResponse,
    UploadResponse,
    DeleteResponse,
    ResetResponse,
    SampleDataResponse,
    SampleFileInfo,
    DocumentInfo
)
from ..utils import (
    get_logger,
    get_paths,
    ensure_directories,
    get_document_type,
    get_size_format,
    get_file_type_from_extension,
    format_datetime,
    is_processed,
    validate_filename
)

router = APIRouter(prefix="/documents", tags=["documents"])
logger = get_logger()


@router.post("/process", response_model=ProcessingResponse)
async def process_documents():
    """Process all documents in the raw directory with enhanced ChromaDB conflict resolution."""
    logger.info("Processing documents from raw directory")
    start_time = time.time()
    
    try:
        # Clear any existing ChromaDB clients in the current process
        gc.collect()
        
        # Disable ChromaDB telemetry to reduce log noise
        try:
            import chromadb.config
            chromadb.config.Settings(anonymized_telemetry=False)
        except Exception as telemetry_e:
            logger.debug(f"Could not disable ChromaDB telemetry: {telemetry_e}")
        
        # Reset ChromaDB global state if it exists
        if hasattr(chromadb, '_clients'):
            # Close any existing client connections
            for client in chromadb._clients.values():
                try:
                    if hasattr(client, 'close'):
                        client.close()
                except Exception as close_e:
                    logger.warning(f"Failed to close ChromaDB client: {close_e}")
            chromadb._clients = {}
        
        # Additional cleanup for ChromaDB connections
        try:
            import sqlite3
            # Force close any remaining SQLite connections
            sqlite3.connect(":memory:").close()
        except Exception as sqlite_e:
            logger.warning(f"SQLite cleanup warning: {sqlite_e}")
        
        # Get paths and ensure directories exist
        paths = get_paths()
        ensure_directories()
        
        # Clean up old backups (keep only the 3 most recent)
        try:
            backup_pattern = paths["processed_dir"].glob("vector_db_backup_*")
            existing_backups = sorted([b for b in backup_pattern if b.is_dir()], 
                                    key=lambda x: x.stat().st_mtime, reverse=True)
            
            # Keep only the 3 most recent backups, delete the rest
            backups_to_delete = existing_backups[3:]  # Keep first 3, delete rest
            for old_backup in backups_to_delete:
                try:
                    shutil.rmtree(old_backup)
                    logger.info(f"Deleted old backup: {old_backup.name}")
                except Exception as delete_e:
                    logger.warning(f"Failed to delete old backup {old_backup.name}: {delete_e}")
            
            if backups_to_delete:
                logger.info(f"Cleaned up {len(backups_to_delete)} old backups")
        except Exception as cleanup_e:
            logger.warning(f"Failed to cleanup old backups: {cleanup_e}")

        # Create backup of existing vector database if it exists
        backup_created = False
        if paths["vector_db_path"].exists():
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            backup_path = paths["processed_dir"] / f"vector_db_backup_{timestamp}"
            try:
                shutil.copytree(paths["vector_db_path"], backup_path)
                backup_created = True
                logger.info(f"Created backup of vector database at {backup_path}")
                # Small delay to ensure filesystem operations complete
                time.sleep(0.1)
            except Exception as backup_e:
                logger.warning(f"Failed to create backup: {backup_e}")
        
        # Fix file permissions to prevent readonly errors (enhanced)
        if paths["vector_db_path"].exists():
            try:
                # First pass: fix directory permissions
                for root, dirs, files in os.walk(paths["vector_db_path"]):
                    # Set directory permissions
                    try:
                        os.chmod(root, 0o755)
                    except Exception as e:
                        logger.warning(f"Failed to set directory permission for {root}: {e}")
                    
                    # Set subdirectory permissions
                    for dir_name in dirs:
                        try:
                            dir_path = os.path.join(root, dir_name)
                            os.chmod(dir_path, 0o755)
                        except Exception as e:
                            logger.warning(f"Failed to set directory permission for {dir_path}: {e}")
                
                # Second pass: fix file permissions
                for root, dirs, files in os.walk(paths["vector_db_path"]):
                    for file_name in files:
                        try:
                            file_path = os.path.join(root, file_name)
                            os.chmod(file_path, 0o644)
                        except Exception as e:
                            logger.warning(f"Failed to set file permission for {file_path}: {e}")
                
                logger.info("Fixed file permissions for vector database")
            except Exception as perm_e:
                logger.warning(f"Failed to fix permissions: {perm_e}")
        
        # Import necessary modules
        sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        from ingestion.document_processor import DocumentIngestion
        from embedding.embedding_generator import EmbeddingGenerator
        
        try:
            # Process documents
            ingestion = DocumentIngestion(str(paths["raw_dir"]), str(paths["processed_dir"]))
            processed_files = ingestion.process_directory()
            
            # Count chunks
            chunk_count = 0
            for processed_file in processed_files:
                output_path = os.path.join(
                    paths["processed_dir"],
                    f"{os.path.basename(processed_file)}_chunks.json"
                )
                if os.path.exists(output_path):
                    with open(output_path, 'r') as f:
                        chunks = json.load(f)
                        chunk_count += len(chunks)
            
            # Generate embeddings with enhanced error handling
            embedding_generator = EmbeddingGenerator()
            embedding_generator.process_all_documents(str(paths["processed_dir"]))
            
            process_time = time.time() - start_time
            logger.info(f"Successfully processed {len(processed_files)} documents with {chunk_count} chunks in {process_time:.2f}s")
            
            return ProcessingResponse(
                success=True,
                message=f"Successfully processed {len(processed_files)} documents with {chunk_count} chunks",
                processed_files=processed_files
            )
            
        except Exception as chromadb_error:
            # If we encounter ChromaDB related errors, try to restore from backup
            if backup_created and "database" in str(chromadb_error).lower():
                try:
                    logger.warning(f"ChromaDB error occurred: {chromadb_error}")
                    logger.info("Attempting to restore from backup...")
                    
                    if paths["vector_db_path"].exists():
                        shutil.rmtree(paths["vector_db_path"])
                    
                    shutil.copytree(backup_path, paths["vector_db_path"])
                    logger.info("Successfully restored vector database from backup")
                    
                    # Try again with restored database
                    embedding_generator = EmbeddingGenerator()
                    embedding_generator.process_all_documents(str(paths["processed_dir"]))
                    
                    process_time = time.time() - start_time
                    logger.info(f"Successfully processed after backup restoration in {process_time:.2f}s")
                    
                    return ProcessingResponse(
                        success=True,
                        message=f"Successfully processed {len(processed_files)} documents with {chunk_count} chunks (after backup restoration)",
                        processed_files=processed_files
                    )
                    
                except Exception as restore_error:
                    logger.error(f"Failed to restore from backup: {restore_error}")
                    raise chromadb_error
            else:
                raise chromadb_error
        
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(f"Error processing documents: {str(e)} after {process_time:.2f}s")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=DocumentListResponse)
async def list_documents():
    """Get a list of documents in the system."""
    logger.info("Listing documents")
    start_time = time.time()
    
    try:
        paths = get_paths()
        documents = []
        
        if paths["raw_dir"].exists():
            for file_path in paths["raw_dir"].glob("*"):
                if not file_path.name.startswith('.') and file_path.is_file():
                    stats = file_path.stat()
                    # Check if it has been processed
                    file_is_processed = is_processed(file_path.name, paths["processed_dir"])
                    
                    documents.append(DocumentInfo(
                        filename=file_path.name,
                        added=format_datetime(stats.st_mtime),
                        size=get_size_format(stats.st_size),
                        type=get_document_type(file_path.name),
                        status="Processed" if file_is_processed else "Raw"
                    ))
        
        process_time = time.time() - start_time
        logger.info(f"Found {len(documents)} documents in {process_time:.4f}s")
        
        return DocumentListResponse(documents=documents)
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(f"Error listing documents: {str(e)} after {process_time:.4f}s")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{filename}", response_model=DeleteResponse)
async def delete_document(filename: str):
    """Delete a document from the system."""
    logger.info(f"Deleting document: {filename}")
    start_time = time.time()
    
    try:
        paths = get_paths()
        
        # Find and remove the raw file
        raw_file = paths["raw_dir"] / filename
        if raw_file.exists():
            raw_file.unlink()
        
        # Find and remove processed chunks
        for processed_file in paths["processed_dir"].glob(f"{filename}_chunks.json"):
            processed_file.unlink()
        
        process_time = time.time() - start_time
        logger.info(f"Successfully deleted document {filename} in {process_time:.4f}s")
        
        return DeleteResponse(
            success=True, 
            message=f"Successfully deleted {filename}"
        )
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(f"Error deleting document {filename}: {str(e)} after {process_time:.4f}s")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """Upload a document to the raw directory."""
    logger.info(f"Uploading document: {file.filename}")
    start_time = time.time()
    
    try:
        paths = get_paths()
        ensure_directories()
        
        # Generate a unique filename to prevent collisions
        unique_filename = f"{uuid.uuid4()}_{file.filename}"
        file_path = paths["raw_dir"] / unique_filename
        
        # Save the file
        with open(file_path, "wb") as f:
            contents = await file.read()
            f.write(contents)
        
        process_time = time.time() - start_time
        logger.info(f"Successfully uploaded document {file.filename} in {process_time:.4f}s")
        
        return UploadResponse(
            success=True,
            message=f"Successfully uploaded {file.filename}",
            filename=unique_filename
        )
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(f"Error uploading document {file.filename}: {str(e)} after {process_time:.4f}s")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/reset", response_model=ResetResponse)
async def reset_vector_database():
    """Reset the vector database by clearing all documents from raw and processed directories."""
    logger.info("Resetting vector database")
    start_time = time.time()
    
    try:
        paths = get_paths()
        
        # Clear raw directory
        if paths["raw_dir"].exists():
            for file in paths["raw_dir"].glob("*"):
                if file.is_file():
                    file.unlink()
        
        # Clear processed directory
        if paths["processed_dir"].exists():
            for file in paths["processed_dir"].glob("*_chunks.json"):
                file.unlink()
        
        # Clear vector database
        if paths["vector_db_path"].exists():
            shutil.rmtree(paths["vector_db_path"])
            os.makedirs(paths["vector_db_path"])
        
        process_time = time.time() - start_time
        logger.info(f"Successfully reset vector database in {process_time:.2f}s")
        
        return ResetResponse(
            success=True,
            message="Vector database reset successfully"
        )
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(f"Error resetting vector database: {str(e)} after {process_time:.2f}s")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sample-data", response_model=SampleDataResponse)
async def list_sample_data():
    """Get a list of available sample data files."""
    logger.info("Listing sample data files")
    start_time = time.time()
    
    try:
        paths = get_paths()
        
        # Check if directory exists
        if not paths["sample_data_dir"].exists():
            logger.warning(f"Sample data directory not found at {paths['sample_data_dir']}")
            return SampleDataResponse(files=[])
        
        # Get list of files
        sample_files = [f for f in os.listdir(paths["sample_data_dir"]) if not f.startswith('.')]
        
        if not sample_files:
            logger.info("No sample data files available")
            return SampleDataResponse(files=[])
        
        # Create file info objects for each sample file
        file_info_list = []
        for filename in sorted(sample_files):
            file_path = paths["sample_data_dir"] / filename
            
            # Get file size in human-readable format
            size_bytes = os.path.getsize(file_path)
            size = get_size_format(size_bytes)
            
            # Determine file type
            file_type = get_file_type_from_extension(filename)
            
            # Add to list
            file_info_list.append(
                SampleFileInfo(
                    filename=filename,
                    size=size,
                    type=file_type
                )
            )
        
        logger.info(f"Retrieved {len(file_info_list)} sample files in {time.time() - start_time:.2f}s")
        return SampleDataResponse(files=file_info_list)
        
    except Exception as e:
        logger.error(f"Error retrieving sample data files: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving sample data files: {str(e)}")


@router.get("/sample-data/{filename}")
async def download_sample_file(filename: str):
    """Download a sample data file."""
    logger.info(f"Downloading sample file: {filename}")
    
    try:
        # Validate filename to prevent directory traversal
        if not validate_filename(filename):
            logger.warning(f"Invalid filename requested: {filename}")
            raise HTTPException(status_code=400, detail="Invalid filename")
        
        paths = get_paths()
        sample_file_path = paths["sample_data_dir"] / filename
        
        # Check if file exists
        if not sample_file_path.exists() or not sample_file_path.is_file():
            logger.warning(f"Sample file not found: {sample_file_path}")
            raise HTTPException(status_code=404, detail=f"Sample file '{filename}' not found")
        
        # Determine media type
        media_type = None
        if filename.endswith('.pdf'):
            media_type = "application/pdf"
        elif filename.endswith('.docx'):
            media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        elif filename.endswith('.doc'):
            media_type = "application/msword"
        elif filename.endswith('.md'):
            media_type = "text/markdown"
        else:
            media_type = "text/plain"
        
        # Return file response
        return FileResponse(
            path=str(sample_file_path),
            filename=filename,
            media_type=media_type
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error downloading sample file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error downloading sample file: {str(e)}")
