# PatientCare Assistant - Troubleshooting Guide

This document outlines common issues and solutions for the PatientCare Assistant application.

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
