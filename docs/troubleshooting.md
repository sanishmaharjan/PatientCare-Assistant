# PatientCare Assistant - Troubleshooting Guide

This document outlines common issues and solutions for the PatientCare Assistant application.

## API Connection Issues

If you encounter "Error connecting to API: [Errno 60] Operation timed out" or similar connection issues:

1. **Check API Server Status**: Ensure the API server is running
   ```bash
   curl http://localhost:8000/
   ```

2. **Server Binding Issues**: The API server may be binding only to localhost. Make sure it's binding to all interfaces:
   ```bash
   # In src/api/app.py, ensure the server is running with host="0.0.0.0"
   uvicorn.run("app:app", host="0.0.0.0", port=API_PORT, ...)
   ```

3. **Increase Timeout Settings**: For operations that take longer, increase the timeout:
   ```python
   # Default timeout is now 60 seconds (previously 30 seconds)
   API_TIMEOUT = 60.0
   ```
   
4. **Use the api_request Helper**: The frontend now includes a helper function for robust API error handling:
   ```python
   success, data, error = api_request("endpoint", data_payload)
   if success:
       # Handle successful response
   else:
       # Display error message
   ```

5. **Restart Both Services**: Sometimes a clean restart is needed:
   ```bash
   pkill -f "uvicorn src.api.app:app"
   pkill -f "streamlit run src/frontend/app.py"
   # Then restart both services
   ```

For detailed information about API fixes, see [api-fixes.md](api-fixes.md).

## Document Upload Issues

If you encounter errors when processing uploaded documents, check for these common issues:

1. **Missing `json` import in API app**: Make sure the `json` module is imported in `src/api/app.py`:
   ```python
   import os
   import sys
   import json  # Required for document processing
   import logging
   ```

2. **Missing `time` module in frontend app**: If you see `Error: name 'time' is not defined` when processing documents, ensure the `time` module is imported in `src/frontend/app.py`:
   ```python
   import os
   import sys
   import json
   import time  # Required for time.sleep() calls
   from typing import Dict, List, Any, Optional
   ```

3. **Missing PDF dependencies**: For PDF processing, ensure `pypdf` is installed:
   ```bash
   pip install pypdf
   ```

4. **Invalid file types**: Make sure you're only uploading supported file types (PDF, DOCX, TXT, MD).

5. **Permission issues**: Ensure the application has write permissions to the `data/raw` and `data/processed` directories.

## Document Processing Issues

If you encounter issues with the `--process` command, try the following solutions:

1. **Missing dependencies**: Ensure all required packages are installed
   ```bash
   pip install langchain-community langchain-text-splitters
   ```

2. **Duplicate embedding IDs**: We've updated the embedding generator to use UUID-based IDs to prevent collisions.

3. **Clean the vector database**: If you encounter issues with the ChromaDB database, you can clean it and start fresh:
   ```bash
   rm -rf data/processed/vector_db
   python src/main.py --process
   ```

4. **Environment variables**: Make sure you have a `.env` file in the `src` directory with the required API keys and settings.

## API and Frontend Issues

1. **Port conflicts**: Make sure ports 8000 (API) and 8501 (Frontend) are available.

2. **API connection issues**: Ensure the API server is running before starting the frontend.

3. **ChromaDB warnings**: You may see telemetry-related warnings from ChromaDB - these can be safely ignored as they don't impact functionality.

## Complete System Startup

To start the complete system:

## Option 1: Using the simplified wrapper scripts

```bash
# Process documents (no warning messages)
./run_processing.sh

# Start the complete system
python src/main.py --api --frontend
```

## Option 2: Direct commands

```bash
# Process documents (may show warnings)
python src/main.py --process

# Start the API server
python src/main.py --api

# Start the frontend
python src/main.py --frontend
```

## Option 3: All-in-one command

```bash
# Start everything (setup, processing, API and frontend)
python src/main.py --all
```
