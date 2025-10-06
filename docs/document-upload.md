# Document Upload and Processing

This document describes the document upload and processing functionality in the PatientCare Assistant application.

## Overview

The document upload and processing pipeline converts raw patient documents into searchable and retrievable data that can be used to answer questions and generate summaries.

The pipeline consists of the following steps:

1. **Document Upload**: Raw documents are uploaded to the server via the web interface.
2. **Document Parsing**: Text content is extracted from various file formats (PDF, DOCX, TXT, MD).
3. **Text Chunking**: Long documents are broken into smaller chunks for better processing.
4. **Embedding Generation**: Vector representations of each chunk are created using the OpenAI API.
5. **Vector Database Indexing**: Embeddings are stored in a vector database for semantic search.

## Supported File Formats

- PDF (.pdf)
- Word Documents (.docx, .doc)
- Text Files (.txt)
- Markdown (.md)

## Technical Implementation

### Frontend Components

The frontend interface allows users to:
- Upload multiple documents simultaneously
- View upload and processing progress
- Manage existing documents
- Reset the vector database when needed

### API Endpoints

The backend provides the following API endpoints for document management:

- `POST /documents/upload`: Upload a document to the server
- `POST /documents/process`: Process all uploaded documents
- `GET /documents`: List all available documents
- `DELETE /documents/{filename}`: Delete a specific document
- `POST /documents/reset`: Reset the vector database

### Document Processing

Documents are processed using LangChain's document loaders and text splitters. The process includes:

1. Loading documents using appropriate loaders (PyPDFLoader, Docx2txtLoader, TextLoader)
2. Splitting text into chunks using RecursiveCharacterTextSplitter
3. Saving processed chunks as JSON files
4. Generating embeddings using OpenAI's embedding model
5. Storing embeddings in ChromaDB vector database

## Error Handling

The system includes robust error handling for:
- Unsupported file formats
- Failed document parsing
- OpenAI API errors
- Database operation failures

## User Interface

The user interface provides feedback throughout the processing pipeline:
- Upload status for each file
- Progress indicators for each processing stage
- Success/error messages for completed operations
- Document management tools (delete, download)

## Data Storage

Document data is stored in several locations:
- Raw documents: `data/raw/`
- Processed chunks: `data/processed/*.json`
- Vector database: `data/processed/vector_db/`

## Performance Considerations

- Large documents are processed in chunks to avoid memory issues
- API calls for embedding generation are batched to respect rate limits
- Long-running operations use timeouts to prevent hanging requests
